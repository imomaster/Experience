#!/usr/bin/env python3
"""Extração mecânica de texto legislativo (PDF, HTML ou TXT) para texto simples.

Nenhum passo deste programa reescreve o texto: só lê a camada de texto do
ficheiro, repõe a ordem de leitura em páginas a duas colunas, retira cabeçalhos
e rodapés repetidos, junta palavras cortadas por hífen no fim da linha e
normaliza caracteres invisíveis. Tudo o que retira ou junta fica registado no
relatório JSON, para poder ser conferido.

Uso:
    python3 extrair.py ENTRADA.pdf -o SAIDA.txt [--relatorio SAIDA.json]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

# Pronomes que, em mesóclise/ênclise, ficam depois de um hífen verdadeiro
# ("dar-se-á", "aplica-se"). Se a linha seguinte começa por um destes, o hífen
# do fim da linha é mantido.
CLITICOS = {
    "se", "lhe", "lhes", "o", "a", "os", "as", "me", "te", "nos", "vos",
    "lo", "la", "los", "las", "no", "na", "nas",
}

LIMPEZA = {
    " ": " ", " ": " ", " ": " ", " ": " ", " ": " ",
    "‐": "-", "‑": "-", "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff",
    "ﬃ": "ffi", "ﬄ": "ffl", "​": "", "﻿": "",
}

RE_ESTRUTURA = re.compile(
    r"^(Artigo\s+\d|Artigo\s+único|(LIVRO|PARTE|TÍTULO|CAPÍTULO|SECÇÃO|SUBSECÇÃO|DIVISÃO|SUBDIVISÃO|ANEXO)\b)"
)
RE_NUM_PAGINA = re.compile(r"^\s*(p[áa]g(ina)?\.?\s*)?\d{1,4}(\s*(/|de)\s*\d{1,4})?\s*$", re.I)


def limpar_linha(linha: str) -> str:
    for a, b in LIMPEZA.items():
        linha = linha.replace(a, b)
    linha = unicodedata.normalize("NFC", linha)
    return re.sub(r"[ \t]+", " ", linha).strip()


# --------------------------------------------------------------------- PDF
def linhas_da_pagina(page, clip=None) -> tuple[list[str], bool]:
    blocos = [b for b in page.get_text("blocks", sort=False, clip=clip) if b[6] == 0 and b[4].strip()]
    if not blocos:
        return [], False
    x0 = min(b[0] for b in blocos)
    x1 = max(b[2] for b in blocos)
    meio, largura = (x0 + x1) / 2, (x1 - x0)
    folga = largura * 0.02

    def lado(b):
        if b[2] <= meio + folga:
            return "E"
        if b[0] >= meio - folga:
            return "D"
        return "L"  # bloco que atravessa o meio da página

    lados = [lado(b) for b in blocos]
    n_e, n_d = lados.count("E"), lados.count("D")
    duas_colunas = n_e >= 3 and n_d >= 3 and (n_e + n_d) >= 0.6 * len(blocos)

    ordenados = sorted(zip(blocos, lados), key=lambda bl: (round(bl[0][1], 1), bl[0][0]))
    if not duas_colunas:
        ordem = [b for b, _ in ordenados]
    else:
        # Os blocos largos (títulos que atravessam a página) separam faixas;
        # em cada faixa lê-se a coluna esquerda inteira e depois a direita.
        ordem, esq, dirt = [], [], []
        for b, l in ordenados:
            if l == "L":
                ordem += esq + dirt + [b]
                esq, dirt = [], []
            elif l == "E":
                esq.append(b)
            else:
                dirt.append(b)
        ordem += esq + dirt

    linhas = []
    for b in ordem:
        linhas.extend(b[4].split("\n"))
    return [limpar_linha(l) for l in linhas if l.strip()], duas_colunas


def ler_pdf(caminho: Path, rel: dict) -> list[list[str]]:
    try:
        import pymupdf
    except ImportError:
        sys.exit("Falta o módulo pymupdf. Ver «Preparação» no SKILL.md.")
    doc = pymupdf.open(caminho)
    paginas = []
    for i, page in enumerate(doc, start=1):
        linhas, duas = linhas_da_pagina(page)
        if not linhas:
            rel["paginas_sem_texto"].append(i)
        if duas:
            rel["paginas_duas_colunas"].append(i)
        paginas.append(linhas)
    rel["paginas"] = len(paginas)
    return paginas


# -------------------------------------------------------------------- HTML
class _Html2Txt(HTMLParser):
    BLOCO = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
             "table", "section", "article", "blockquote", "dd", "dt", "td", "th"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self._ignorar = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head", "nav", "noscript"):
            self._ignorar += 1
        elif tag in self.BLOCO:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head", "nav", "noscript"):
            self._ignorar = max(0, self._ignorar - 1)
        elif tag in self.BLOCO:
            self.partes.append("\n")

    def handle_data(self, data):
        if not self._ignorar:
            self.partes.append(data.replace("\n", " "))


def ler_bytes(caminho: Path) -> str:
    dados = caminho.read_bytes()
    m = re.search(rb'charset=["\']?([\w-]+)', dados[:4000], re.I)
    for cod in ([m.group(1).decode()] if m else []) + ["utf-8", "cp1252", "latin-1"]:
        try:
            return dados.decode(cod)
        except (LookupError, UnicodeDecodeError):
            continue
    return dados.decode("latin-1", errors="replace")


def ler_html(caminho: Path, rel: dict) -> list[list[str]]:
    p = _Html2Txt()
    p.feed(ler_bytes(caminho))
    linhas = [limpar_linha(l) for l in "".join(p.partes).split("\n")]
    rel["paginas"] = 1
    return [[l for l in linhas if l]]


def ler_txt(caminho: Path, rel: dict) -> list[list[str]]:
    texto = ler_bytes(caminho)
    # Quebra de página (\f) separa páginas, por exemplo em saídas de pdftotext.
    paginas = [[limpar_linha(l) for l in pag.split("\n") if l.strip()] for pag in texto.split("\f")]
    rel["paginas"] = len(paginas)
    return paginas


# ------------------------------------------------- cabeçalhos e rodapés
def chave(linha: str) -> str:
    return re.sub(r"\d+", "#", linha.lower())


def retirar_cabecalhos(paginas: list[list[str]], rel: dict, margem: int = 3) -> list[list[str]]:
    n = len(paginas)
    contagem = collections.Counter()
    for pag in paginas:
        zona = set(chave(l) for l in pag[:margem] + pag[-margem:])
        contagem.update(zona)
    minimo = max(2, int(0.4 * n + 0.999))
    repetidas = {k for k, c in contagem.items() if n >= 2 and c >= minimo}

    retiradas = collections.Counter()
    saida = []
    for pag in paginas:
        zona = set(range(min(margem, len(pag)))) | set(range(max(0, len(pag) - margem), len(pag)))
        apagar = set()
        for i in sorted(zona):
            l = pag[i]
            if RE_ESTRUTURA.match(l):
                continue  # «Artigo 5.º», «CAPÍTULO II»… nunca são cabeçalhos de página
            if chave(l) in repetidas or RE_NUM_PAGINA.match(l):
                apagar.add(i)
        for i in sorted(apagar):
            retiradas[pag[i]] += 1
        saida.append([l for i, l in enumerate(pag) if i not in apagar])
    rel["cabecalhos_rodapes_retirados"] = [
        {"linha": l, "vezes": c} for l, c in retiradas.most_common()
    ]
    return saida


# ----------------------------------------------------------- hifenização
def fazer_lexico(linhas: list[str]) -> collections.Counter:
    """Conta as formas (com e sem hífen) que aparecem no texto, para decidir junções."""
    corpo = " ".join(linhas).lower()
    return collections.Counter(re.findall(r"[\wÀ-ÿ]+(?:-[\wÀ-ÿ]+)*", corpo))


def juntar_hifens(linhas: list[str], rel: dict, lexico=None) -> list[str]:
    """Junta palavras partidas no fim da linha.

    Decide se o hífen é de translineação (retira-se: «conser-|vação») ou faz
    parte da palavra (mantém-se: «aplica-|se», «Decreto-|Lei») com base no
    próprio documento: se a forma junta ou a forma hifenizada aparece noutro
    sítio do texto, segue-se essa. Sem pistas, fica a regra por omissão e a
    junção é marcada como «ambígua» no relatório, para conferir.
    """
    if lexico is None:
        lexico = fazer_lexico(linhas)

    saida: list[str] = []
    juncoes, ambiguas = [], []
    i = 0
    while i < len(linhas):
        atual = linhas[i]
        while i + 1 < len(linhas) and re.search(r"[A-Za-zÀ-ÿ][-­]$", atual):
            seguinte = linhas[i + 1]
            m = re.match(r"([A-Za-zÀ-ÿ]+)", seguinte)
            if not m:
                break
            frag = re.search(r"([A-Za-zÀ-ÿ]+)[-­]$", atual).group(1)
            palavra = m.group(1)
            junta = (frag + palavra).lower()
            hifen = f"{frag}-{palavra}".lower()
            ambigua = False
            if atual.endswith("­"):
                manter = False  # hífen condicional: é sempre translineação
            elif palavra[0].isupper():
                manter = True   # «Decreto-|Lei», «Regulamento-|Geral»
            elif lexico[hifen] > lexico[junta]:
                manter = True
            elif lexico[junta] > lexico[hifen]:
                manter = False
            elif palavra.lower() in CLITICOS and re.search(r"[aeiouáéíóúâêôãõàrszm]$", frag.lower()):
                # «aplica-|se» ou «análi-|se»? Sem pistas no texto, mantém o
                # hífen (é o caso mais comum em legislação) e manda conferir.
                manter, ambigua = True, True
            else:
                manter = False  # translineação normal: «conser-|vação»
            novo = atual[:-1] + ("-" if manter else "") + seguinte
            reg = {"tipo": "hifen_mantido" if manter else "hifen_retirado",
                   "de": f"{frag}- | {palavra}", "resultado": hifen if manter else junta}
            juncoes.append(reg)
            if ambigua:
                ambiguas.append(reg)
            atual = novo
            i += 1
        saida.append(atual)
        i += 1
    rel["juncoes_de_hifen"] = juncoes
    rel["juncoes_ambiguas"] = ambiguas
    return saida


RE_NOTA_PGDL = re.compile(
    r"^(Contém as alterações (dos seguintes diplomas|introduzidas pelos seguintes diplomas)|"
    r"Consultar versões anteriores deste artigo|Consultar o diploma|Versão desactualizada|Versão desatualizada)", re.I
)


def retirar_notas_pgdl(linhas: list[str], rel: dict) -> list[str]:
    """Retira as notas editoriais da PGDL (não são texto legal): a linha da nota
    e a lista de diplomas/versões que se lhe segue (linhas começadas por «-»)."""
    saida, retiradas, em_nota = [], [], False
    for l in linhas:
        if RE_NOTA_PGDL.match(l):
            em_nota = True
            retiradas.append(l)
            continue
        if em_nota and (l.startswith("-") or re.match(r"^\d+ª versão", l)):
            retiradas.append(l)
            continue
        em_nota = False
        saida.append(l)
    rel["notas_pgdl_retiradas"] = retiradas
    return saida


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", type=Path)
    ap.add_argument("-o", "--saida", type=Path, required=True)
    ap.add_argument("--relatorio", type=Path)
    ap.add_argument("--sem-cabecalhos", action="store_true",
                    help="não retirar cabeçalhos/rodapés (usar se o relatório mostrar remoções indevidas)")
    ap.add_argument("--manter-notas", action="store_true",
                    help="manter as notas editoriais da PGDL («Contém as alterações…», versões anteriores)")
    a = ap.parse_args()

    rel = {"entrada": str(a.entrada), "paginas": 0, "paginas_sem_texto": [],
           "paginas_duas_colunas": [], "cabecalhos_rodapes_retirados": [], "juncoes_de_hifen": []}
    ext = a.entrada.suffix.lower()
    if ext == ".pdf":
        paginas = ler_pdf(a.entrada, rel)
    elif ext in (".html", ".htm"):
        paginas = ler_html(a.entrada, rel)
    else:
        paginas = ler_txt(a.entrada, rel)

    if not a.sem_cabecalhos:
        paginas = retirar_cabecalhos(paginas, rel)
    linhas = juntar_hifens([l for pag in paginas for l in pag], rel)
    if not a.manter_notas:
        linhas = retirar_notas_pgdl(linhas, rel)

    a.saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    rel["linhas"] = len(linhas)
    rel["palavras"] = len(re.findall(r"\w+", "\n".join(linhas)))
    rel["alertas"] = []
    if rel["paginas_sem_texto"]:
        rel["alertas"].append(
            f"Páginas sem camada de texto (provavelmente digitalizadas): {rel['paginas_sem_texto']}. "
            "Não transcrever à mão: obter versão digital noutra fonte ou fazer OCR."
        )
    if rel["paginas"] and rel["palavras"] < 50 * rel["paginas"]:
        rel["alertas"].append("Muito pouco texto por página: confirmar se o PDF é digitalizado.")
    rel_path = a.relatorio or a.saida.with_suffix(".extracao.json")
    rel_path.write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Extraído: {rel['linhas']} linhas, {rel['palavras']} palavras, {rel['paginas']} página(s)")
    print(f"Duas colunas: {rel['paginas_duas_colunas'] or 'nenhuma'}")
    print(f"Cabeçalhos/rodapés retirados: {sum(x['vezes'] for x in rel['cabecalhos_rodapes_retirados'])} linhas "
          f"({len(rel['cabecalhos_rodapes_retirados'])} distintas)")
    if rel.get("notas_pgdl_retiradas"):
        print(f"Notas editoriais PGDL retiradas: {len(rel['notas_pgdl_retiradas'])} linhas")
    print(f"Junções de hífen: {len(rel['juncoes_de_hifen'])} (ambíguas: {len(rel['juncoes_ambiguas'])})")
    for j in rel["juncoes_ambiguas"]:
        print(f"  CONFERIR: «{j['de']}» → «{j['resultado']}»")
    for al in rel["alertas"]:
        print("ALERTA:", al)
    print(f"Relatório: {rel_path}")


if __name__ == "__main__":
    main()
