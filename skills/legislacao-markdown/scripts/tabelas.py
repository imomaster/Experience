#!/usr/bin/env python3
"""Extrai um quadro (tabela) de um PDF oficial para Markdown, com prova visual.

Princípio: nada do que entra na tabela é escrito por um modelo. As colunas vêm
das linhas verticais desenhadas no PDF (ou, na falta delas, do alinhamento do
texto); as linhas vêm das regras horizontais e do alinhamento do texto; o
conteúdo de cada célula vem da camada de texto. O resultado é verificado de
duas formas (coerência da grelha e segunda extração independente). Se a
grelha não for fiável, o quadro sai em modo «linear» ou é recusado.

Modos de saída (sempre declarados):
  grelha    tabela Markdown verificada
  linear    conteúdo linha a linha, sem reproduzir as colunas
  recusada  fica só a ligação ao PDF e a página; a razão fica no relatório

Uso:
  python3 tabelas.py DOC.pdf --pagina 11 --listar
  python3 tabelas.py DOC.pdf --pagina 11 --legenda "QUADRO XX" -o quadros/ \
      --url "https://files.diariodarepublica.pt/…pdf" --versao "Portaria n.º 135/2020"
  python3 tabelas.py DOC.pdf --pagina 10 --tabela 2 --trocar "«=≤" --trocar "‹=<" --trocar "›=>"

Cada quadro gera três ficheiros: .md (tabela), .json (relatório) e .png (imagem
da página recortada, para comparar lado a lado antes de aprovar).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extrair as EX  # noqa: E402

try:
    import pymupdf
except ImportError:  # pragma: no cover
    sys.exit("Falta o módulo pymupdf. Ver «Preparação» no SKILL.md.")

RE_PONTOS = re.compile(r"(?<![\[(.])(?:\s*\.){3,}(?![\])])")
RE_PONTOS_FIM = re.compile(r"(?:\s+\.)+\s*$")
RE_FONTE_SIMBOLOS = re.compile(r"^\d+$|symbol|wingding|dingbat|zapf|mtextra|mt-extra|universalgreek", re.I)
RE_ORDINAL = re.compile(r"^\d+\.?[ºª°]$")


# ----------------------------------------------------------------- palavras
class Palavra:
    __slots__ = ("chars", "dir", "lid", "x0", "y0", "x1", "y1")

    def __init__(self, chars, direcao, lid):
        self.chars, self.dir, self.lid = chars, direcao, lid
        self.x0 = min(c["x0"] for c in chars)
        self.y0 = min(c["y0"] for c in chars)
        self.x1 = max(c["x1"] for c in chars)
        self.y1 = max(c["y1"] for c in chars)

    @property
    def cx(self):
        return (self.x0 + self.x1) / 2

    @property
    def cy(self):
        return (self.y0 + self.y1) / 2

    @property
    def tam(self):
        # o corpo da palavra é a letra maior: índices e expoentes são sempre mais pequenos
        return max(c["tam"] for c in self.chars)

    @property
    def base(self):
        t = self.tam
        return statistics.median(c["base"] for c in self.chars if c["tam"] == t)

    @property
    def texto(self):
        return "".join(c["c"] for c in self.chars)

    @property
    def so_pontos(self):
        return all(c["c"] == "." for c in self.chars)


def motivo_suspeito(c: str, fonte: str) -> str | None:
    if c in "‹›":
        return "aspa angular simples (pode ser < ou >)"
    if "\ue000" <= c <= "\uf8ff" or c == "\ufffd":
        return "carácter sem correspondência na camada de texto"
    if RE_FONTE_SIMBOLOS.search(fonte):
        cat = unicodedata.category(c)
        if cat == "Sm" or c in "●•°µ" or "\u0370" <= c <= "\u03ff" or c == "∆":
            return None  # já é um símbolo matemático/grego a sério
        return f"vem de um tipo de letra de símbolos («{fonte}»)"
    return None


def ler_palavras(page, clip) -> list[Palavra]:
    flags = pymupdf.TEXTFLAGS_RAWDICT & ~pymupdf.TEXT_PRESERVE_IMAGES
    rd = page.get_text("rawdict", clip=clip, flags=flags)
    saida: list[Palavra] = []
    for bi, b in enumerate(rd["blocks"]):
        if b.get("type", 0) != 0:
            continue
        for li, l in enumerate(b["lines"]):
            dx, dy = l["dir"]
            if abs(dx - 1) < 0.03 and abs(dy) < 0.03:
                d = "h"
            elif abs(dx) < 0.03 and abs(dy + 1) < 0.03:
                d = "v-"  # rodado 90°, lê-se de baixo para cima
            elif abs(dx) < 0.03 and abs(dy - 1) < 0.03:
                d = "v+"  # rodado 90°, lê-se de cima para baixo
            else:
                d = "x"   # inclinado ou invertido
            atual: list[dict] = []
            ant = None

            def fecha():
                nonlocal atual
                if atual:
                    saida.append(Palavra(atual, d, (bi, li)))
                atual = []

            seq = [(ch, s) for s in l["spans"] for ch in s["chars"]]
            for i, (ch, s) in enumerate(seq):
                tam = round(s["size"], 1)
                c = ch["c"]
                if c.isspace():
                    # espaço «fantasma»: o carácter seguinte começa no mesmo sítio
                    # (artefacto da camada de texto, ex.: «2.1 -A» por «2.1-A»)
                    seg = seq[i + 1][0] if i + 1 < len(seq) else None
                    if (d == "h" and seg is not None and not seg["c"].isspace()
                            and seg["bbox"][0] <= ch["bbox"][0] + 0.5 and atual):
                        continue
                    fecha()
                    ant = None
                    continue
                x0, y0, x1, y1 = ch["bbox"]
                if d == "h" and ant is not None and x0 - ant > 1.0 * tam:
                    fecha()
                ox, oy = ch["origin"]
                atual.append({"c": c, "x0": x0, "y0": y0, "x1": x1, "y1": y1, "tam": tam,
                              "fonte": s["font"], "base": oy if d == "h" else ox,
                              "susp": motivo_suspeito(c, s["font"])})
                ant = x1
            fecha()
    return saida


# ------------------------------------------------------------------- regras
def _agrupa(vals: list[float], tol: float) -> list[float]:
    grupos: list[list[float]] = []
    for v in sorted(vals):
        if grupos and v - grupos[-1][-1] <= tol:
            grupos[-1].append(v)
        else:
            grupos.append([v])
    return [sum(g) / len(g) for g in grupos]


def ler_regras(page):
    """Devolve (H, V): regras horizontais (y, x0, x1, esp) e verticais (x, y0, y1, esp),
    com os segmentos colineares já unidos."""
    hs, vs = [], []

    def seg(ax, ay, bx, by, w):
        if abs(ay - by) < 0.8 and abs(ax - bx) > 3:
            hs.append(((ay + by) / 2, min(ax, bx), max(ax, bx), w))
        elif abs(ax - bx) < 0.8 and abs(ay - by) > 3:
            vs.append(((ax + bx) / 2, min(ay, by), max(ay, by), w))

    for dr in page.get_drawings():
        w = dr.get("width") or 0
        for it in dr["items"]:
            if it[0] == "l":
                seg(it[1].x, it[1].y, it[2].x, it[2].y, w)
            elif it[0] in ("re", "qu"):
                r = it[1] if it[0] == "re" else it[1].rect
                if r.height < 2.5 and r.width > 3:
                    hs.append(((r.y0 + r.y1) / 2, r.x0, r.x1, max(w, r.height)))
                elif r.width < 2.5 and r.height > 3:
                    vs.append(((r.x0 + r.x1) / 2, r.y0, r.y1, max(w, r.width)))
                elif r.width > 3 and r.height > 3:
                    seg(r.x0, r.y0, r.x1, r.y0, w)
                    seg(r.x0, r.y1, r.x1, r.y1, w)
                    seg(r.x0, r.y0, r.x0, r.y1, w)
                    seg(r.x1, r.y0, r.x1, r.y1, w)

    def unir(segs):
        segs = sorted(segs, key=lambda s: (round(s[0] / 0.8), s[1]))
        out: list[list[float]] = []
        for p, a, b, w in segs:
            if out and abs(out[-1][0] - p) <= 0.8 and a - out[-1][2] <= 1.8:
                out[-1][2] = max(out[-1][2], b)
                out[-1][3] = max(out[-1][3], w)
            else:
                out.append([p, a, b, w])
        return [tuple(o) for o in out]

    return unir(hs), unir(vs)


class Regiao:
    def __init__(self, x0, y0, x1, y1, aberta=False, origem="regras grossas"):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.aberta, self.origem = aberta, origem
        self.legenda = ""
        self.leg_rect = None

    @property
    def rect(self):
        return pymupdf.Rect(self.x0, self.y0, self.x1, self.y1)


def detetar_regioes(page, H, V) -> list[Regiao]:
    """Um quadro do Diário da República começa e acaba numa regra horizontal grossa,
    com as mesmas extremidades. Se não houver regra de fecho (o quadro continua
    noutra coluna ou página), acaba onde acabam as linhas verticais."""
    regs: list[Regiao] = []
    esp = [h[3] for h in H if h[3] > 0 and h[2] - h[1] > 40]
    # só há «regras grossas» se também houver regras claramente mais finas
    if esp and min(esp) < 0.7 * max(esp):
        grossas = sorted([h for h in H if h[3] >= 0.8 * max(esp) and h[2] - h[1] > 40], key=lambda h: h[0])
        usadas: set[int] = set()

        def mesma(a, b):
            return abs(a[1] - b[1]) <= 2.5 and abs(a[2] - b[2]) <= 2.5

        for i, t in enumerate(grossas):
            if i in usadas:
                continue
            alcance = None
            for x, y0, y1, _ in V:
                if t[1] - 1.5 <= x <= t[2] + 1.5 and y0 <= t[0] + 4 and y1 > t[0] + 4:
                    alcance = max(alcance or 0, y1)
            fim, aberta = None, False
            for j in range(i + 1, len(grossas)):
                if j in usadas or not mesma(t, grossas[j]):
                    continue
                y = grossas[j][0]
                if alcance is None or abs(alcance - y) <= 3:
                    fim = y                     # as linhas verticais acabam nesta regra: é o fecho
                    usadas.add(j)
                    break
                if alcance > y + 3:
                    usadas.add(j)               # as verticais continuam: é uma regra interior grossa
                    continue
                break                           # as verticais acabam antes: o quadro não tem fecho
            if fim is None and alcance is not None and alcance - t[0] > 12:
                fim, aberta = alcance, True
            if fim is not None:
                regs.append(Regiao(t[1], t[0], t[2], fim, aberta=aberta))
            usadas.add(i)
    if not regs:
        for estrategia in ("lines", "text"):
            try:
                tabs = page.find_tables(strategy=estrategia).tables
            except Exception:
                tabs = []
            for t in tabs:
                x0, y0, x1, y1 = t.bbox
                regs.append(Regiao(x0, y0, x1, y1, origem=f"deteção automática ({estrategia})"))
            if regs:
                break
    regs.sort(key=lambda r: (round(r.x0 / 150), r.y0))
    for r in regs:
        _legenda(page, r)
    return regs


def _legenda(page, r: Regiao) -> None:
    """Texto imediatamente acima do quadro (ex.: «QUADRO XX» e o título)."""
    clip = pymupdf.Rect(r.x0 - 2, max(0, r.y0 - 70), r.x1 + 2, r.y0 - 0.5)
    linhas = []
    for b in page.get_text("dict", clip=clip)["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                linhas.append((l["bbox"][1], l["bbox"][3], t, l["bbox"]))
    linhas.sort(reverse=True)
    escolhidas, topo = [], r.y0
    for y0, y1, t, bb in linhas:
        if topo - y1 > 16 or len(escolhidas) >= 5:
            break
        escolhidas.append((t, bb))
        topo = y0
    escolhidas.reverse()
    # ficar a partir da última linha «QUADRO/TABELA/ANEXO…»; sem ela, só as 2 linhas mais próximas
    marcos = [i for i, (t, _) in enumerate(escolhidas)
              if re.match(r"(QUADRO|TABELA|ANEXO|MAPA|MODELO|Quadro|Tabela|Anexo|Mapa|Modelo)\b", t)]
    escolhidas = escolhidas[marcos[-1]:] if marcos else escolhidas[-2:]
    r.legenda = " ".join(t for t, _ in escolhidas)
    if escolhidas:
        r.leg_rect = pymupdf.Rect(min(b[0] for _, b in escolhidas), min(b[1] for _, b in escolhidas),
                                  max(b[2] for _, b in escolhidas), max(b[3] for _, b in escolhidas))


# ------------------------------------------------------------ linhas visuais
def linhas_visuais(palavras: list[Palavra]) -> list[list[Palavra]]:
    """Agrupa palavras horizontais em linhas pelo alinhamento vertical.
    Índices e expoentes (letra mais pequena) juntam-se à linha mais próxima."""
    if not palavras:
        return []
    tams = [p.tam for p in palavras]
    modo = max(set(tams), key=tams.count)
    normais = sorted([p for p in palavras if p.tam > 0.8 * modo], key=lambda p: p.base)
    peq = [p for p in palavras if p.tam <= 0.8 * modo]
    linhas: list[dict] = []
    for p in normais:
        if linhas and abs(p.base - linhas[-1]["base"]) <= 0.4 * modo:
            ln = linhas[-1]
            ln["ps"].append(p)
            ln["base"] = statistics.mean(q.base for q in ln["ps"])
        else:
            linhas.append({"ps": [p], "base": p.base})
    for p in peq:
        prox = min(linhas, key=lambda ln: abs(ln["base"] - p.base), default=None)
        if prox is not None and abs(prox["base"] - p.base) <= 0.9 * modo:
            prox["ps"].append(p)
        else:
            linhas.append({"ps": [p], "base": p.base})
    linhas.sort(key=lambda ln: ln["base"])
    return [sorted(ln["ps"], key=lambda p: p.x0) for ln in linhas]


class Ctx:
    """Estado partilhado de uma extração: decisões humanas, registos e alertas."""

    def __init__(self, trocas: dict[str, str], lexico):
        self.trocas, self.lexico = trocas, lexico
        self.conferir: list[dict] = []
        self.decisoes: collections.Counter = collections.Counter()
        self.juncoes: list[dict] = []
        self.pontos = 0
        self.alertas: list[str] = []

    def alerta(self, msg: str):
        if msg not in self.alertas:
            self.alertas.append(msg)


def marcar_aspas_soltas(linha: list[Palavra]) -> None:
    """« ou » isolado entre dois valores (ex.: «C « 80») é quase de certeza um
    símbolo mal codificado. Marca-o para conferir."""
    for i, p in enumerate(linha):
        if p.texto in ("«", "»") and 0 < i < len(linha) - 1:
            a, b = linha[i - 1].texto, linha[i + 1].texto
            if re.search(r"[\w%)\]]$", a) and re.match(r"[\w(\[]", b):
                for c in p.chars:
                    c["susp"] = c["susp"] or "aspa isolada entre dois valores (pode ser ≤, ≥, < ou >)"


def render_linha(linha: list[Palavra], ctx: Ctx, onde: str, marcas: bool = True) -> str:
    """Texto de uma linha de palavras. Com marcas=True aplica <sub>/<sup> e as
    decisões humanas sobre símbolos; com marcas=False devolve o texto cru."""
    if not linha:
        return ""
    horizontal = linha[0].dir == "h"
    if horizontal:
        marcar_aspas_soltas(linha)
    tams = [p.tam for p in linha]
    modo = max(set(tams), key=lambda t: (tams.count(t), t))
    base = statistics.median(c["base"] for p in linha for c in p.chars if c["tam"] == modo)
    partes = []
    for p in linha:
        s, etq = "", None
        for c in p.chars:
            ch = c["c"]
            nova = None
            if marcas and horizontal and c["tam"] <= 0.8 * modo:
                if c["base"] < base - 0.12 * modo:
                    nova = "sup"
                elif c["base"] > base + 0.08 * modo:
                    nova = "sub"
            if nova != etq:
                if etq:
                    s += f"</{etq}>"
                if nova:
                    s += f"<{nova}>"
                etq = nova
            if marcas and c["susp"]:
                if ch in ctx.trocas:
                    ctx.decisoes[f"{ch}→{ctx.trocas[ch]}"] += 1
                    ch = ctx.trocas[ch]
                else:
                    ctx.conferir.append({"onde": onde, "caracter": ch, "motivo": c["susp"],
                                         "linha": " ".join(q.texto for q in linha)})
            s += ch
        if etq:
            s += f"</{etq}>"
        partes.append(s)
    txt = " ".join(partes)
    return txt.replace("</sub> <sub>", " ").replace("</sup> <sup>", " ")


def sem_pontos(txt: str, ctx: Ctx | None = None) -> str:
    novo, n = RE_PONTOS.subn(" ", txt)
    novo, m = RE_PONTOS_FIM.subn("", novo)  # restos no fim da linha: «4.ª . .»
    n += m
    if ctx is not None:
        ctx.pontos += n
    return EX.limpar_linha(novo)


def acaba_em_pontos(linha: list[Palavra]) -> bool:
    return bool(re.search(r"(?:\s*\.){3,}\s*$", " ".join(p.texto for p in linha)))


def texto_de_linhas(linhas: list[list[Palavra]], ctx: Ctx, onde: str) -> str:
    """Junta as linhas de uma célula: tira pontos de preenchimento e une as
    palavras cortadas por hífen (com o mesmo registo do extrair.py)."""
    txts = [sem_pontos(render_linha(l, ctx, onde), ctx) for l in linhas]
    txts = [t for t in txts if t]
    rel: dict = {}
    juntas = EX.juntar_hifens(txts, rel, lexico=ctx.lexico)
    for j in rel["juncoes_de_hifen"]:
        ctx.juncoes.append({**j, "onde": onde, "ambigua": j in rel["juncoes_ambiguas"]})
    return " ".join(juntas)


def linhas_da_celula(palavras: list[Palavra]) -> list[list[Palavra]]:
    """Linhas de uma célula, incluindo texto rodado 90° (lido pela rotação certa)."""
    hor = [p for p in palavras if p.dir == "h"]
    rod = [p for p in palavras if p.dir in ("v-", "v+")]
    linhas = linhas_visuais(hor)
    if rod:
        grupos: dict = collections.defaultdict(list)
        for p in rod:
            grupos[p.lid].append(p)
        # de baixo para cima: as linhas sucedem-se da esquerda para a direita
        ordem = sorted(grupos.values(), key=lambda g: statistics.mean(q.cx for q in g),
                       reverse=(rod[0].dir == "v+"))
        linhas += ordem
    return linhas


# ------------------------------------------------------------------- grelha
def colunas_por_texto(palavras: list[Palavra], x0: float, x1: float) -> list[float]:
    """Sem linhas verticais desenhadas: as colunas são os «rios» de espaço em
    branco que nenhuma linha de texto atravessa."""
    linhas = linhas_visuais([p for p in palavras if p.dir == "h" and not p.so_pontos])
    n = len(linhas)
    if n < 2:
        return [x0, x1]
    larg = int(x1 - x0) + 2
    cob = [0] * larg
    for ln in linhas:
        ints: list[list[float]] = []
        for p in ln:
            if ints and p.x0 - ints[-1][1] < 0.6 * p.tam + 1:
                ints[-1][1] = max(ints[-1][1], p.x1)
            else:
                ints.append([p.x0, p.x1])
        for a, b in ints:
            for i in range(max(0, int(a - x0)), min(larg, int(b - x0) + 1)):
                cob[i] += 1
    lim = int(0.08 * n)
    seps, i = [], 0
    while i < larg:
        if cob[i] <= lim:
            j = i
            while j < larg and cob[j] <= lim:
                j += 1
            if j - i >= 5 and i > 3 and j < larg - 3:
                seps.append(x0 + (i + j) / 2)
            i = j
        else:
            i += 1
    return [x0] + seps + [x1]


def analisar(page, reg: Regiao, H, V, ctx: Ctx, modo_linhas: str = "auto") -> dict:
    """Constrói a grelha de um quadro. Devolve um dicionário com 'cabecalho',
    'linhas', os textos crus para a verificação e os dados da estrutura; ou
    {'recusa': razão}."""
    clip = pymupdf.Rect(reg.x0 - 2, reg.y0 - 1, reg.x1 + 2, reg.y1 + 1)
    palavras = ler_palavras(page, clip)
    if not palavras:
        return {"recusa": "sem texto na zona do quadro"}
    if any(p.dir == "x" for p in palavras):
        return {"recusa": "texto inclinado ou invertido: a ordem de leitura não é fiável"}
    if sum(1 for p in palavras if p.dir != "h") > 0.5 * len(palavras):
        return {"recusa": "o quadro está deitado na página (texto rodado 90°): não é reproduzido"}

    # colunas
    vxs = [v[0] for v in V if reg.x0 + 3 < v[0] < reg.x1 - 3 and v[2] > reg.y0 + 1 and v[1] < reg.y1 - 1]
    por_regras = bool(vxs)
    if por_regras:
        xs = [reg.x0] + _agrupa(vxs, 1.5) + [reg.x1]
        estrategia = "linhas desenhadas"
    else:
        xs = colunas_por_texto(palavras, reg.x0, reg.x1)
        estrategia = "alinhamento do texto"
    ncol = len(xs) - 1
    if ncol < 2:
        return {"recusa": "não foi possível identificar colunas", "estrategia": estrategia}

    # faixas (entre regras horizontais)
    hys = [h[0] for h in H if reg.y0 + 2 < h[0] < reg.y1 - 2
           and min(h[2], reg.x1) - max(h[1], reg.x0) > 0.05 * (reg.x1 - reg.x0)]
    ys = [reg.y0] + _agrupa(hys, 1.2) + [reg.y1]
    nb = len(ys) - 1

    def cob_h(y, a, b):
        tot = sum(max(0, min(h[2], b) - max(h[1], a)) for h in H if abs(h[0] - y) <= 1.2)
        return tot / max(1e-6, b - a)

    def cob_v(x, a, b):
        tot = sum(max(0, min(v[2], b) - max(v[1], a)) for v in V if abs(v[0] - x) <= 1.5)
        return tot / max(1e-6, b - a)

    def faixa_de(p: Palavra) -> int:
        y = p.cy
        for b in range(nb):
            if y < ys[b + 1]:
                return b
        return nb - 1

    def atravessa(b: int, x: float) -> bool:
        """Sem linhas desenhadas: há texto corrido a passar por cima da separação?"""
        grupos: dict = collections.defaultdict(list)
        for p in palavras:
            if p.dir == "h" and faixa_de(p) == b and not p.so_pontos:
                grupos[p.lid].append(p)
        for g in grupos.values():
            g.sort(key=lambda p: p.x0)
            for p in g:
                if p.x0 < x - 1 and p.x1 > x + 1:
                    return True
            for p, q in zip(g, g[1:]):
                if p.x1 <= x <= q.x0 and q.x0 - p.x1 < 0.6 * p.tam + 1:
                    return True
        return False

    # cabeçalho: até à primeira regra interior a toda a largura
    hfim = next((k for k in range(1, nb) if cob_h(ys[k], reg.x0, reg.x1) >= 0.95), 0)

    # Há quadros em que as linhas verticais do cabeçalho não estão na mesma posição
    # das do corpo. Se houver tantas separações só-do-cabeçalho como só-do-corpo, e
    # alternarem, são as mesmas colunas (deslocadas); caso contrário, recusa-se.
    xs_cab, xs_corpo = xs, xs
    if por_regras and hfim:
        tipo = {}
        for x in xs[1:-1]:
            no_cab = any(cob_v(x, ys[b], ys[b + 1]) >= 0.7 for b in range(hfim))
            no_corpo = any(cob_v(x, ys[b], ys[b + 1]) >= 0.7 for b in range(hfim, nb))
            tipo[x] = "ambos" if no_cab and no_corpo else "cab" if no_cab else "corpo" if no_corpo else "nenhum"
        so_cab = [x for x in xs[1:-1] if tipo[x] == "cab"]
        if so_cab:
            so_corpo = [x for x in xs[1:-1] if tipo[x] == "corpo"]
            seq = [tipo[x] for x in xs[1:-1] if tipo[x] in ("cab", "corpo")]
            pares_ok = len(so_cab) == len(so_corpo) and all(
                {seq[i], seq[i + 1]} == {"cab", "corpo"} for i in range(0, len(seq), 2))
            if not pares_ok:
                return {"recusa": "as colunas do cabeçalho não coincidem com as do corpo do quadro",
                        "estrategia": estrategia}
            fixos = [x for x in xs[1:-1] if tipo[x] == "ambos"]
            xs_cab = [xs[0]] + sorted(fixos + so_cab) + [xs[-1]]
            xs_corpo = [xs[0]] + sorted(fixos + so_corpo) + [xs[-1]]
            ncol = len(xs_corpo) - 1
            ctx.alerta("As linhas verticais do cabeçalho e do corpo não estão na mesma posição: as colunas "
                       "foram emparelhadas pela ordem. Conferir com a imagem.")
        else:
            mortas = [x for x in xs[1:-1] if tipo[x] == "nenhum"]
            if mortas:
                xs = [x for x in xs if x not in mortas]
                xs_cab = xs_corpo = xs
                ncol = len(xs) - 1

    def xs_de(b: int) -> list[float]:
        return xs_cab if b < hfim else xs_corpo

    def sep_v(b: int, c: int) -> bool:  # separação entre as colunas c-1 e c, na faixa b
        x = xs_de(b)[c]
        if por_regras:
            return cob_v(x, ys[b], ys[b + 1]) >= 0.7
        return not atravessa(b, x)

    def sep_h(k: int, c: int) -> bool:  # regra em ys[k] por baixo da coluna c
        e = xs_de(k - 1)
        return cob_h(ys[k], e[c], e[c + 1]) >= 0.7

    # fusão de células (união de conjuntos)
    pai = {(b, c): (b, c) for b in range(nb) for c in range(ncol)}

    def raiz(a):
        while pai[a] != a:
            pai[a] = pai[pai[a]]
            a = pai[a]
        return a

    def une(a, b):
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            pai[max(ra, rb)] = min(ra, rb)

    sv = {(b, c): sep_v(b, c) for b in range(nb) for c in range(1, ncol)}
    for (b, c), ha in sv.items():
        if not ha:
            une((b, c - 1), (b, c))
    for k in range(1, nb):
        if k == hfim:
            continue  # o cabeçalho nunca se funde com o corpo
        for c in range(ncol):
            if not sep_h(k, c):
                une((k - 1, c), (k, c))

    # partir palavras que atravessam uma separação desenhada
    if por_regras:
        novas: list[Palavra] = []
        for p in palavras:
            b = faixa_de(p)
            e = xs_de(b)
            cortes = [e[c] for c in range(1, ncol) if sv[(b, c)] and p.x0 < e[c] - 1 and p.x1 > e[c] + 1]
            if p.dir != "h" or not cortes:
                novas.append(p)
                continue
            grupos: dict = collections.defaultdict(list)
            for ch in p.chars:
                grupos[sum(1 for x in cortes if (ch["x0"] + ch["x1"]) / 2 > x)].append(ch)
            novas += [Palavra(g, p.dir, p.lid) for _, g in sorted(grupos.items())]
        palavras = novas

    def coluna_de(p: Palavra) -> int:
        x, e = p.cx, xs_de(faixa_de(p))
        for c in range(ncol):
            if x < e[c + 1]:
                return c
        return ncol - 1

    conteudo: dict = collections.defaultdict(list)
    for p in palavras:
        conteudo[raiz((faixa_de(p), coluna_de(p)))].append(p)

    membros: dict = collections.defaultdict(list)
    for cel in pai:
        membros[raiz(cel)].append(cel)

    crus: list[str] = []  # texto cru de cada célula, uma vez, para a verificação

    def cru(ps: list[Palavra]) -> None:
        for l in linhas_da_celula(ps):
            crus.append(sem_pontos(render_linha(l, ctx, "", marcas=False)))

    tem_rodado = any(p.dir != "h" for p in palavras)
    fundidas = sum(1 for m in membros.values() if len(m) > 1)

    # ---- cabeçalho: um título por coluna, juntando os níveis com « — »
    cab = [""] * ncol
    if hfim:
        textos: dict = {}
        for r, m in membros.items():
            if r[0] < hfim:
                cru(conteudo.get(r, []))
                textos[r] = texto_de_linhas(linhas_da_celula(conteudo.get(r, [])), ctx, "cabeçalho")
        for c in range(ncol):
            niveis: list[str] = []
            vistos: set = set()
            for b in range(hfim):
                r = raiz((b, c))
                if r not in vistos and textos.get(r):
                    niveis.append(textos[r])
                vistos.add(r)
            cab[c] = " — ".join(niveis)
    else:
        ctx.alerta("Quadro sem linha de cabeçalho identificável.")

    # ---- corpo
    linhas_md: list[list[str]] = []
    conflitos = soltas = 0
    inferidas = False
    acumuladas: list[str] = []
    corpo = list(range(hfim, nb))
    n_faixas_corpo = len(corpo)

    def grupos_de_colunas(b: int) -> list[list[int]]:
        gs: dict = collections.defaultdict(list)
        for c in range(ncol):
            gs[raiz((b, c))].append(c)
        return [sorted(g) for g in gs.values()]

    por_faixa: dict[int, dict] = {}
    for b in corpo:
        simples = {r: m for r, m in membros.items() if all(x[0] == b for x in m)}
        ps = [p for r in simples for p in conteudo.get(r, []) if p.dir == "h"]
        lvs = linhas_visuais(ps)
        por_col: list[dict[int, list[Palavra]]] = []
        for lv in lvs:
            d: dict = collections.defaultdict(list)
            for p in lv:
                d[raiz((b, coluna_de(p)))[1]].append(p)
            por_col.append({c: v for c, v in d.items() if not all(q.so_pontos for q in v)})
        por_col = [d for d in por_col if d]
        multi = sum(1 for d in por_col if len(d) >= 2)
        pontos_col: collections.Counter = collections.Counter()
        for d in por_col:
            for c, v in d.items():
                if acaba_em_pontos(v):
                    pontos_col[c] += 1
        por_faixa[b] = {"simples": simples, "por_col": por_col, "multi": multi,
                        "pontos": max(pontos_col.values(), default=0)}

    ha_pontos = any(f["pontos"] >= 2 for f in por_faixa.values())
    for b in corpo:
        f = por_faixa[b]
        if modo_linhas == "texto":
            inferir = len(f["por_col"]) > 1
        elif modo_linhas == "regras":
            inferir = False
        elif n_faixas_corpo >= 3 and not ha_pontos:
            inferir = False  # quadro com uma regra por linha
        else:
            inferir = f["pontos"] >= 2 or f["multi"] >= 3 or (f["multi"] >= 2 and n_faixas_corpo <= 2
                                                              and len(f["por_col"]) == f["multi"])
        rodado_aqui = any(p.dir != "h" for r in f["simples"] for p in conteudo.get(r, []))
        if inferir and rodado_aqui:
            return {"recusa": "texto rodado no corpo do quadro, em linhas sem regras: leitura não fiável",
                    "estrategia": estrategia}

        sub: list[dict[int, list[list[Palavra]]]] = []
        if not inferir:
            linha_unica: dict = {}
            for r in f["simples"]:
                ls = linhas_da_celula(conteudo.get(r, []))
                ls = [l for l in ls if not all(q.so_pontos for q in l)]
                if ls:
                    linha_unica[r[1]] = ls
                    if sum(1 for l in ls if acaba_em_pontos(l)) >= 2:
                        acumuladas.append(f"faixa {b - hfim + 1}, coluna {r[1] + 1}")
            if linha_unica:
                sub.append(linha_unica)
        else:
            inferidas = True
            # Em que colunas o recuo tem significado? Só nas alinhadas à esquerda
            # (entradas à margem, continuações recuadas). Em colunas centradas
            # ou alinhadas à direita, a posição de início não diz nada.
            ext: dict[int, list[tuple[float, float]]] = collections.defaultdict(list)
            for d in f["por_col"]:
                for c, v in d.items():
                    uteis = [q for q in v if not q.so_pontos]
                    ext[c].append((uteis[0].x0, uteis[-1].x1))
            base_x: dict[int, float] = {}
            for c, es in ext.items():
                niveis = _agrupa([e[0] for e in es], 1.0)          # posições de início distintas

                def media(nv, f):
                    vs = [f(e) for e in es if abs(e[0] - nv) <= 1.5]
                    return sum(vs) / len(vs)

                larg_col = xs_de(b)[c + 1] - xs_de(b)[c]
                curtas = max(e[1] - e[0] for e in es) < 0.6 * larg_col
                centros = [media(nv, lambda e: (e[0] + e[1]) / 2) for nv in niveis]
                fins = [media(nv, lambda e: e[1]) for nv in niveis]
                centrada = len(niveis) > 1 and max(centros) - min(centros) <= 1.5
                a_direita = len(niveis) > 1 and curtas and max(fins) - min(fins) <= 1.5
                # alinhada à esquerda (ou justificada): poucos níveis de início = margem + recuos
                if not centrada and not a_direita and len(niveis) <= 3:
                    base_x[c] = min(niveis)

            def recuo(v: list[Palavra]) -> float:
                return max(1.5, 0.35 * v[0].tam)  # um recuo a sério é ~1 quadratim

            def recuada(c: int, v: list[Palavra]) -> bool:
                return c in base_x and v[0].x0 > base_x[c] + recuo(v)

            def aberta(ls: list[list[Palavra]]) -> bool:
                """A entrada ainda não acabou? (sem pontos de preenchimento nem pontuação final)"""
                t = " ".join(q.texto for q in ls[-1])
                return not acaba_em_pontos(ls[-1]) and not re.search(r"[.;:!?»)\]]$", t)

            atual: dict | None = None
            pend: dict[int, list[list[Palavra]]] = {}
            for d in f["por_col"]:
                if len(d) >= 2:
                    nova = {c: [v] for c, v in d.items()}
                    # o que estava pendente é o início desta linha (rótulo que começa
                    # antes dos valores) se a continuação vier recuada; senão é uma linha própria
                    prefixo = any(c in d and d[c][0].x0 > pre[0][0].x0 + recuo(d[c]) for c, pre in pend.items())
                    if pend and prefixo:
                        for c, pre in pend.items():
                            nova[c] = pre + nova.get(c, [])
                    elif pend:
                        if len(pend) == 1:
                            soltas += 1
                        sub.append(pend)
                    elif atual is not None:
                        for c, v in d.items():
                            if c in atual and recuada(c, v) and aberta(atual[c]):
                                conflitos += 1  # um texto que continua de uma linha do quadro para a outra
                    pend = {}
                    sub.append(nova)
                    atual = nova
                    continue
                (c, v), = d.items()
                if pend:
                    pend.setdefault(c, []).append(v)       # continua a entrada que começou sozinha
                elif atual is not None and recuada(c, v):
                    atual.setdefault(c, []).append(v)      # continuação recuada da linha atual
                else:
                    pend[c] = [v]                          # à margem: começa uma entrada nova
            if pend:
                if len(pend) == 1 and len(sub) > 0:
                    soltas += 1
                sub.append(pend)

        # texto das células de cada sub-linha
        gcs = grupos_de_colunas(b)
        linhas_b: list[list[str]] = []
        for i, s in enumerate(sub):
            row = [""] * ncol
            for c, ls in s.items():
                onde = f"linha {len(linhas_md) + len(linhas_b) + 1}, coluna {c + 1}"
                for l in ls:
                    crus.append(sem_pontos(render_linha(l, ctx, "", marcas=False)))
                row[c] = texto_de_linhas(ls, ctx, onde)
            for g in gcs:  # células fundidas na horizontal: repetir o valor
                if len(g) > 1 and len(g) < ncol and row[g[0]]:
                    for c in g[1:]:
                        row[c] = row[g[0]]
            linhas_b.append(row)
        # grupo: a 1.ª coluna só tem valor na primeira sub-linha da faixa → repetir
        if inferir and n_faixas_corpo >= 2 and len(linhas_b) >= 2 and linhas_b[0][0] \
                and not any(r[0] for r in linhas_b[1:]):
            for r in linhas_b[1:]:
                r[0] = linhas_b[0][0]
            ctx.alerta("Na 1.ª coluna, o valor de cada grupo (delimitado por regras) foi repetido "
                       "nas linhas do grupo: conferir com a imagem.")
        por_faixa[b]["linhas"] = linhas_b
        linhas_md += linhas_b

    # células que atravessam várias faixas do corpo (fundidas na vertical): repetir
    for r, m in membros.items():
        fs = sorted({x[0] for x in m})
        if r[0] >= hfim and len(fs) > 1:
            cru(conteudo.get(r, []))
            t = texto_de_linhas(linhas_da_celula(conteudo.get(r, [])), ctx, "célula fundida")
            cols = sorted({x[1] for x in m})
            for b in fs:
                for row in por_faixa[b].get("linhas", []):
                    for c in cols:
                        row[c] = t

    if inferidas:
        ctx.alerta("As linhas do quadro foram deduzidas do alinhamento do texto (não há uma regra "
                   "por linha): conferir a correspondência entre colunas na imagem.")
    if fundidas:
        ctx.alerta(f"{fundidas} célula(s) fundida(s): o texto foi repetido em cada coluna/linha abrangida.")
    if tem_rodado:
        ctx.alerta("Há texto rodado 90° (lido pela rotação): conferir com a imagem.")

    if soltas:
        ctx.alerta(f"{soltas} linha(s) do quadro só têm texto numa coluna: pode ser uma linha própria ou a "
                   "continuação da anterior. Conferir com a imagem.")
    return {"cabecalho": cab, "linhas": linhas_md, "crus": crus, "estrategia": estrategia,
            "ncol": ncol, "inferidas": inferidas, "fundidas": fundidas, "acumuladas": acumuladas,
            "conflitos": conflitos, "soltas": soltas,
            "clip": clip, "rodado": tem_rodado}


# -------------------------------------------------------------- verificação
def tokens(txt: str) -> list[str]:
    return re.findall(r"\w+", re.sub(r"</?su[bp]>", "", txt))


def verificar(page, g: dict) -> dict:
    """R5: coerência da grelha + dupla extração (contra o extrair.py)."""
    cab, linhas, ncol = g["cabecalho"], g["linhas"], g["ncol"]
    coer: list[str] = []
    if not linhas:
        coer.append("sem linhas de dados")
    if any(len(r) != ncol for r in linhas):
        coer.append("número de colunas instável")
    todas = [cab] + linhas
    cheias = sum(1 for r in todas for c in r if c.strip())
    frac = cheias / max(1, len(todas) * ncol)
    if frac < 0.6:
        coer.append(f"só {frac:.0%} das células preenchidas (mínimo 60 %)")
    if g.get("conflitos"):
        coer.append("há texto que continua de uma linha do quadro para a seguinte (rótulo comum a várias "
                    "linhas): a grelha não o consegue representar")
    if g["acumuladas"]:
        coer.append("células acumuladas (várias entradas na mesma célula): " + "; ".join(g["acumuladas"][:5]))
    for i, r in enumerate(linhas, 1):
        for j, c in enumerate(r, 1):
            tk = c.split()
            if sum(1 for t in tk if RE_ORDINAL.match(t)) >= 4 and len(tk) <= 12:
                coer.append(f"célula acumulada (enumeração) na linha {i}, coluna {j}")

    linear, _ = EX.linhas_da_pagina(page, clip=g["clip"])
    a = collections.Counter(t for s in g["crus"] for t in tokens(s))
    b = collections.Counter(t for s in linear for t in tokens(sem_pontos(s)))
    dupla = {"palavras_grelha": sum(a.values()), "palavras_linear": sum(b.values()), "igual": a == b}
    if a != b:
        ca = collections.Counter("".join(a.elements()))
        cb = collections.Counter("".join(b.elements()))
        dupla["so_na_grelha"] = [f"{w}×{n}" for w, n in (a - b).most_common(12)]
        dupla["so_na_linear"] = [f"{w}×{n}" for w, n in (b - a).most_common(12)]
        dupla["so_espacamento"] = ca == cb
    ok_dupla = dupla["igual"] or dupla.get("so_espacamento", False)
    return {"coerencia": {"ok": not coer, "problemas": coer, "celulas_preenchidas": round(frac, 2)},
            "dupla_extracao": dupla, "ok": (not coer) and ok_dupla}


# -------------------------------------------------------------------- saída
def esc(c: str) -> str:
    return c.replace("|", "\\|").replace("\n", " ").strip()


def md_grelha(cab: list[str], linhas: list[list[str]]) -> str:
    out = ["| " + " | ".join(esc(c) for c in cab) + " |",
           "|" + "|".join(" --- " for _ in cab) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in linhas]
    return "\n".join(out)


def md_linear(page, reg: Regiao, ctx: Ctx) -> tuple[str, list[str]]:
    """Conteúdo pela ordem de leitura, uma linha de texto do PDF por linha.
    Usa as linhas tal como estão na camada de texto: não reagrupa nada."""
    clip = pymupdf.Rect(reg.x0 - 2, reg.y0 - 1, reg.x1 + 2, reg.y1 + 1)
    blocos: dict = collections.defaultdict(lambda: collections.defaultdict(list))
    for p in ler_palavras(page, clip):
        if p.dir == "h":
            blocos[p.lid[0]][p.lid[1]].append(p)
    ordem = sorted(blocos.values(), key=lambda b: (round(min(q.y0 for l in b.values() for q in l), 1),
                                                   min(q.x0 for l in b.values() for q in l)))
    out, crus = [], []
    n = 0
    for b in ordem:
        for li in sorted(b):
            lv = [q for q in b[li] if not q.so_pontos]
            if not lv:
                continue
            n += 1
            crus.append(sem_pontos(render_linha(b[li], ctx, "", marcas=False)))
            t = sem_pontos(render_linha(lv, ctx, f"linha {n}"), ctx)
            if t:
                out.append(t)
    return "\n".join(f"- {l}" for l in out), crus


def nota(modo: str, url: str, pagina: int, versao: str, estado: str) -> str:
    fonte = url or "PDF"
    v = f", versão: {versao}" if versao else ""
    if modo == "grelha":
        return f"> Quadro extraído do PDF oficial ({fonte}, pág. {pagina}{v}) — {estado}."
    if modo == "linear":
        return (f"> Conteúdo do quadro extraído do PDF oficial ({fonte}, pág. {pagina}{v}), linha a linha — "
                f"{estado}. **A disposição em colunas não é reproduzida:** consultar o PDF.")
    return f"> Quadro não reproduzido. Consultar o PDF oficial ({fonte}, pág. {pagina}{v})."


def procurar_legenda(page, legenda: str) -> list:
    """Linhas da página que contêm a legenda como expressão inteira
    («QUADRO I» não apanha «QUADRO II» nem «QUADRO IV»)."""
    rx = re.compile(r"(?<!\w)" + r"\s+".join(re.escape(t) for t in legenda.split()) + r"(?!\w)", re.I)
    achados = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            if rx.search("".join(sp["text"] for sp in l["spans"])):
                achados.append(pymupdf.Rect(l["bbox"]))
    return achados


def processar(doc, page, pagina: int, k: int, reg: Regiao, H, V, a, lexico) -> dict:
    trocas = {}
    for t in a.trocar or []:
        if "=" not in t or len(t.split("=", 1)[0]) != 1:
            sys.exit(f"--trocar inválido: {t!r} (formato: \"«=≤\")")
        de, para = t.split("=", 1)
        trocas[de] = para
    ctx = Ctx(trocas, lexico)
    base = f"{Path(a.pdf).stem}_p{pagina}_q{k}"
    dest = Path(a.saida)
    dest.mkdir(parents=True, exist_ok=True)
    rel: dict = {"pdf": str(a.pdf), "pdf_url": a.url, "versao": a.versao, "pagina": pagina, "quadro": k,
                 "bbox": [round(v, 1) for v in (reg.x0, reg.y0, reg.x1, reg.y1)],
                 "legenda": reg.legenda, "regiao": reg.origem, "continua": reg.aberta}

    # imagem de prova (R3)
    r = reg.rect + (-12, -12, 12, 12)
    if reg.leg_rect is not None:
        r |= reg.leg_rect + (-4, -4, 4, 4)
    r &= page.rect
    png = dest / f"{base}.png"
    page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=r).save(png)
    rel["imagem"] = str(png)

    modo, razao, corpo_md, ver = "recusada", "", "", None
    g = {"recusa": "modo linear pedido"} if a.modo == "linear" else analisar(page, reg, H, V, ctx, a.linhas)
    rel["estrategia"] = g.get("estrategia", "")
    if "recusa" not in g:
        ver = verificar(page, g)
        rel.update({"linhas": len(g["linhas"]) + 1, "colunas": g["ncol"],
                    "linhas_inferidas": g["inferidas"], "celulas_fundidas": g["fundidas"]})
        if ver["ok"]:
            modo, corpo_md = "grelha", md_grelha(g["cabecalho"], g["linhas"])
        else:
            razao = "grelha não passou a verificação: " + "; ".join(
                ver["coerencia"]["problemas"] or ["a segunda extração não coincide"])
    else:
        razao = g["recusa"]

    if modo != "grelha":
        ctx_lin = Ctx(trocas, lexico)
        tem_rodado = any(p.dir != "h" for p in ler_palavras(page, reg.rect))
        if a.modo == "grelha" or tem_rodado or "sem texto" in razao or "inclinado" in razao:
            modo = "recusada"
            if tem_rodado and "rodado" not in razao:
                razao += " (há texto rodado: o modo linear também não é fiável)"
        else:
            corpo_md, crus = md_linear(page, reg, ctx_lin)
            linear, _ = EX.linhas_da_pagina(page, clip=pymupdf.Rect(reg.x0 - 2, reg.y0 - 1, reg.x1 + 2, reg.y1 + 1))
            ta = collections.Counter(t for s in crus for t in tokens(s))
            tb = collections.Counter(t for s in linear for t in tokens(sem_pontos(s)))
            igual = ta == tb or collections.Counter("".join(ta.elements())) == collections.Counter("".join(tb.elements()))
            if corpo_md and igual:
                modo = "linear"
                ctx_lin.alertas = ctx.alertas + ctx_lin.alertas
                ctx = ctx_lin
                ctx.alerta("Modo linear: " + razao)
            else:
                modo = "recusada"
                razao += "; a extração linear também não coincide"

    if reg.aberta:
        ctx.alerta("O quadro não tem regra de fecho: continua noutra coluna ou página. "
                   "Extrair cada parte em separado.")
    pend = [c for c in ctx.conferir]
    if a.simbolos_conferidos:
        pend = []
    if modo == "recusada":
        resultado, estado = f"RECUSADA ({razao})", ""
    elif pend:
        resultado, estado = f"CONFERIR ({len(pend)} símbolo(s) por decidir)", "símbolos por conferir"
    else:
        resultado, estado = "OK", "verificado"
        if ctx.decisoes:
            estado += "; símbolos corrigidos por conferência com a imagem"

    rel.update({"modo": modo, "razao": razao, "resultado": resultado, "alertas": ctx.alertas,
                "conferir": pend, "decisoes_humanas": dict(ctx.decisoes),
                "simbolos_confirmados_como_estao": bool(a.simbolos_conferidos and ctx.conferir),
                "juncoes_de_hifen": ctx.juncoes, "pontos_de_preenchimento_retirados": ctx.pontos,
                "verificacao": ver})
    attrs = f'fonte="{a.url}" pagina="{pagina}" versao="{a.versao}" modo="{modo}" resultado="{resultado.split(" ")[0]}"'
    partes = [f"<!-- quadro {attrs} -->"]
    if corpo_md and modo != "recusada":
        partes += [corpo_md, ""]
    partes += [nota(modo, a.url, pagina, a.versao, estado), "<!-- /quadro -->"]
    md = dest / f"{base}.md"
    md.write_text("\n".join(partes) + "\n", encoding="utf-8")
    rel["markdown"] = str(md)
    (dest / f"{base}.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    print(f"\n== Quadro {k} (pág. {pagina}) — {reg.legenda[:90] or 'sem legenda'}")
    print(f"   modo: {modo}" + (f" · {rel.get('linhas')} linhas × {rel.get('colunas')} colunas · {rel['estrategia']}"
                                if modo == "grelha" else ""))
    for al in ctx.alertas:
        print(f"   ALERTA: {al}")
    for c in pend[:12]:
        print(f"   CONFERIR [{c['onde']}]: «{c['caracter']}» em «{c['linha'][:70]}» — {c['motivo']}")
    if len(pend) > 12:
        print(f"   … e mais {len(pend) - 12} (ver relatório)")
    amb = [j for j in ctx.juncoes if j.get("ambigua")]
    for j in amb:
        print(f"   CONFERIR hífen: «{j['de']}» → «{j['resultado']}»")
    print(f"   imagem: {png}\n   tabela: {md}")
    print(f"   RESULTADO: {resultado}")
    return rel


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--pagina", type=int, help="página do PDF (1 = primeira)")
    ap.add_argument("--legenda", help="texto da legenda a procurar (ex.: \"QUADRO XX\"); escolhe o quadro logo abaixo")
    ap.add_argument("--tabela", type=int, help="n.º do quadro na página (ver --listar)")
    ap.add_argument("--bbox", help="zona do quadro: x0,y0,x1,y1 em pontos do PDF")
    ap.add_argument("--listar", action="store_true", help="só listar os quadros detetados na página")
    ap.add_argument("-o", "--saida", default="quadros", help="pasta de saída (por omissão: quadros/)")
    ap.add_argument("--url", default="", help="endereço oficial do PDF (vai para a nota e o relatório)")
    ap.add_argument("--versao", default="", help="ato a que o PDF corresponde (ex.: \"Portaria n.º 135/2020\")")
    ap.add_argument("--trocar", action="append", metavar="X=Y",
                    help="decisão humana sobre um símbolo assinalado (ex.: \"«=≤\"). Só se aplica aos "
                         "carateres marcados CONFERIR. Pode repetir-se.")
    ap.add_argument("--simbolos-conferidos", action="store_true",
                    help="declarar que os símbolos assinalados foram conferidos na imagem e estão certos")
    ap.add_argument("--linhas", choices=("auto", "regras", "texto"), default="auto",
                    help="como separar as linhas: pelas regras desenhadas, pelo alinhamento do texto, ou automático")
    ap.add_argument("--modo", choices=("auto", "grelha", "linear"), default="auto")
    a = ap.parse_args()

    doc = pymupdf.open(a.pdf)
    paginas = [a.pagina] if a.pagina else []
    if not paginas and a.legenda:
        paginas = [i for i, p in enumerate(doc, 1) if procurar_legenda(p, a.legenda)]
        if not paginas:
            sys.exit(f"Legenda não encontrada no PDF: {a.legenda!r}")
        if len(paginas) > 1:
            sys.exit(f"A legenda aparece em várias páginas ({paginas}): algumas serão só remissões no texto. "
                     "Ver cada uma com --pagina N --listar e indicar --pagina.")
    if not paginas:
        sys.exit("Indicar --pagina (ou --legenda).")
    pagina = paginas[0]
    if not 1 <= pagina <= len(doc):
        sys.exit(f"O PDF tem {len(doc)} páginas.")
    page = doc[pagina - 1]

    # R6: sem camada de texto → parar, sem OCR
    if not page.get_text("words"):
        doc_sem_texto = not any(p.get_text("words") for p in doc)
        msg = ("digitalizado: o PDF não tem camada de texto" if doc_sem_texto
               else "digitalizado: esta página não tem camada de texto")
        dest = Path(a.saida)
        dest.mkdir(parents=True, exist_ok=True)
        base = f"{Path(a.pdf).stem}_p{pagina}"
        rel = {"pdf": str(a.pdf), "pdf_url": a.url, "pagina": pagina, "modo": "recusada", "razao": msg,
               "resultado": f"RECUSADA ({msg})"}
        (dest / f"{base}.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
        (dest / f"{base}.md").write_text(
            f'<!-- quadro fonte="{a.url}" pagina="{pagina}" versao="{a.versao}" modo="recusada" resultado="RECUSADA" -->\n'
            + nota("recusada", a.url, pagina, a.versao, "") + "\n<!-- /quadro -->\n", encoding="utf-8")
        print(f"RESULTADO: RECUSADA ({msg}). Não se faz OCR de legislação: fica a ligação ao PDF e a página.")
        raise SystemExit(2)

    if page.rotation:
        page.remove_rotation()  # página deitada: trabalhar nas coordenadas tal como se vê
    H, V = ler_regras(page)
    if a.bbox:
        try:
            x0, y0, x1, y1 = (float(v) for v in a.bbox.split(","))
        except ValueError:
            sys.exit("--bbox inválido (formato: x0,y0,x1,y1)")
        r = Regiao(x0, y0, x1, y1, origem="zona indicada (--bbox)")
        _legenda(page, r)
        regs = [r]
    else:
        regs = detetar_regioes(page, H, V)
    def inalterado() -> bool:
        """Num ato de alteração, um quadro que não muda aparece como uma linha de pontos."""
        for t in (procurar_legenda(page, a.legenda) if a.legenda else []):
            zona = pymupdf.Rect(page.rect.x0, t.y1, page.rect.x1, t.y1 + 75)
            for l in page.get_text("text", clip=zona).splitlines():
                if re.fullmatch(r"[\s.…]{12,}", l) and l.count(".") + l.count("…") >= 8:
                    return True
        return False

    def sem_quadro():
        if inalterado():
            print(f"RESULTADO: INALTERADO — neste PDF, por baixo de «{a.legenda}» está só uma linha de pontos: "
                  "este ato não alterou o quadro. Usar o PDF do ato anterior do histórico ou o original.")
            raise SystemExit(3)
        print("Nenhum quadro detetado" + (f" por baixo de «{a.legenda}»" if a.legenda else "")
              + " nesta página. Ver --listar, ou indicar a zona com --bbox x0,y0,x1,y1.")
        raise SystemExit(2)

    if not regs:
        sem_quadro()

    escolha = list(enumerate(regs, 1))
    if a.legenda and not a.bbox:
        alvos = procurar_legenda(page, a.legenda)
        if not alvos:
            sys.exit(f"Legenda não encontrada na página {pagina}: {a.legenda!r}")

        def dist(reg: Regiao) -> float:
            best = 1e9
            for t in alvos:
                sobrepoe = min(t.x1, reg.x1) - max(t.x0, reg.x0) > 0
                dy = reg.y0 - t.y1
                if sobrepoe and dy >= -3:
                    best = min(best, dy)
            return best

        k, reg = min(escolha, key=lambda kr: dist(kr[1]))
        if dist(reg) > 120:
            sem_quadro()
        escolha = [(k, reg)]
    elif a.tabela:
        if not 1 <= a.tabela <= len(regs):
            sys.exit(f"A página tem {len(regs)} quadro(s). Usar --listar.")
        escolha = [(a.tabela, regs[a.tabela - 1])]

    if a.listar:
        print(f"Página {pagina}: {len(regs)} quadro(s) detetado(s)")
        for k, r in enumerate(regs, 1):
            print(f"  {k}. zona {r.x0:.0f},{r.y0:.0f},{r.x1:.0f},{r.y1:.0f}"
                  f"{' (continua)' if r.aberta else ''} — {r.legenda[:100] or 'sem legenda'}")
        return

    linhas_pag, _ = EX.linhas_da_pagina(page)
    lexico = EX.fazer_lexico(linhas_pag)
    resultados = [processar(doc, page, pagina, k, reg, H, V, a, lexico) for k, reg in escolha]
    raise SystemExit(0 if all(r["resultado"] == "OK" for r in resultados) else 1)


if __name__ == "__main__":
    main()
