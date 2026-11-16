#!/usr/bin/env python3
"""Converte texto legislativo extraído (saída de extrair.py) em Markdown estruturado.

Regra de ouro: este programa só reorganiza linhas e acrescenta marcação
(títulos, separação de parágrafos, cabeçalho de metadados). Não altera, não
resume e não acrescenta palavras ao texto legal. O verificar.py confirma isso.

Uso (diploma inteiro):
    python3 estruturar.py texto.txt -o saida.md --titulo "..." --diploma "..." \
        --sigla CC --fonte DRE --url URL --em-vigor-desde 2022-04-10 \
        --ultima-alteracao "Lei n.º 8/2022, de 10 de janeiro"

Uso (excerto):
    ... --artigos "1414..1438-A, 1305"    (intervalos com «..», «:» ou « a »)
    ... --depois-de "^ANEXO"              (ignora o articulado antes desta linha,
                                           útil quando o decreto que aprova um
                                           código tem artigos com o mesmo número)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

RE_ARTIGO = re.compile(
    r"^(?P<rot>(?i:artigo|art\.)\s+(?:(?P<num>\d+)\s*\.?\s*[ºo°]?\s*(?:-\s*(?P<suf>[A-Z]{1,2}))?|(?P<unico>(?i:único))))"
    r"\s*(?:[-–—]\s*(?P<ep1>.+)|\((?P<ep2>[^)]+)\))?\s*$"
)
NIVEIS = {"LIVRO": 1, "PARTE": 1, "TÍTULO": 2, "CAPÍTULO": 3, "SECÇÃO": 4,
          "SUBSECÇÃO": 5, "DIVISÃO": 6, "SUBDIVISÃO": 7}
RE_DIVISAO = re.compile(
    r"^(?P<tipo>LIVRO|PARTE|TÍTULO|CAPÍTULO|SECÇÃO|SUBSECÇÃO|DIVISÃO|SUBDIVISÃO)"
    r"(?:\s+(?P<id>[IVXLCDM]+(?:-[A-Z])?|\d+(?:\.º)?(?:-[A-Z])?|ÚNIC[OA]|PRELIMINAR|PRIMEIR[OA]|SEGUND[OA]|TERCEIR[OA]))?"
    r"\s*(?:[-–—.]\s*(?P<tit>.+))?$"
)
RE_ANEXO = re.compile(r"^(ANEXO|Anexo)(\s+[IVXLC\d]+(-[A-Z])?)?\s*$")
RE_INICIO = re.compile(
    r"^(\d+\s*[-–—]\s|\d+\.\s+[A-ZÀ-Ý«(]|\d+\.\s*$|[a-z]{1,2}\)\s|[ivxlc]+\)\s|«)"
)
# marcas do DRE para quadros e figuras que só existem no PDF, e as respetivas legendas:
# ficam sempre em parágrafo próprio, para o quadros.py as encontrar
RE_VDO = re.compile(r"(?:[a-z]{1,3}\)\s*)?\(ver documento original\)[;.,]?", re.I)
RE_LEGENDA = re.compile(r"(QUADRO|TABELA|MAPA|MODELO|FIGURA)\s+[IVXLC\d]+(-[A-Z])?\.?$")
RE_FECHO = re.compile(
    r"^(Aprovad[oa]s? em|Visto e aprovado|Promulgad[oa] em|Referendad[oa] em|Publique-se|"
    r"O Presidente da República|O Primeiro-Ministro|A Primeira-Ministra|O Presidente da Assembleia|"
    r"Pel[oa] Primeir|O Ministro d|A Ministra d)"
)


def eh_estrutura(l: str) -> bool:
    return bool(RE_ARTIGO.match(l) or RE_DIVISAO.match(l) or RE_ANEXO.match(l))


def termina_frase(l: str) -> bool:
    return bool(re.search(r"[.;:,]$", l))


def comeca_maiuscula(l: str | None) -> bool:
    return l is None or bool(re.match(r"[A-ZÀ-Ý0-9«(\"“]", l))


def chave_artigo(m: re.Match) -> tuple:
    if m.group("unico"):
        return (0, "ÚNICO")
    return (int(m.group("num")), m.group("suf") or "")


def ordem(k: tuple) -> tuple:
    num, suf = k
    return (num, len(suf), suf)


def parse_lista(spec: str) -> list[tuple]:
    partes = []
    for bloco in re.split(r"\s*[,;]\s*", spec.strip()):
        if not bloco:
            continue
        lim = re.split(r"\s*(?:\.\.|:|\sa\s)\s*", bloco)
        ks = []
        for x in lim:
            m = re.match(r"^(\d+)\s*\.?º?\s*(?:-\s*([A-Za-z]{1,2}))?$", x.strip())
            if not m:
                raise SystemExit(f"Artigo inválido em --artigos: {x!r}")
            ks.append((int(m.group(1)), (m.group(2) or "").upper()))
        partes.append((ks[0], ks[-1]))
    return partes


# ------------------------------------------------------------------ análise
def analisar(linhas: list[str]) -> tuple[list[dict], int]:
    """Divide as linhas em unidades: pre, div, art, fecho. Cada unidade guarda
    os seus parágrafos (listas de linhas originais)."""
    unidades: list[dict] = [{"tipo": "pre", "pars": []}]
    prof = 0  # profundidade de aspas « »
    i, n = 0, len(linhas)
    # Linhas bem mais curtas do que a média costumam fechar um parágrafo
    # (ou ser títulos soltos, como a data do diploma).
    compr = sorted(len(l) for l in linhas) or [80]
    mediana = compr[len(compr) // 2]

    def novo_par(u, linha):
        u["pars"].append([linha])

    while i < n:
        l = linhas[i]
        if prof == 0 and (m := RE_ARTIGO.match(l)):
            u = {"tipo": "art", "linha_cab": l, "rotulo": m.group("rot").strip(),
                 "chave": chave_artigo(m), "epigrafe": None, "pars": [], "idx": i}
            ep = m.group("ep1") or m.group("ep2")
            j = i + 1
            if ep:
                u["epigrafe"] = [ep]
            else:
                k = j
                while k < n and k - j <= 3 and not eh_estrutura(linhas[k]) and not RE_INICIO.match(linhas[k]):
                    k += 1
                entre = linhas[j:k]
                if (0 < len(entre) <= 3 and k < n and re.match(r"^1\s*[-–—.]", linhas[k])
                        and all(len(x) <= 150 for x in entre) and not termina_frase(entre[-1])):
                    u["epigrafe"] = entre
                    j = k
                elif j < n:
                    c = linhas[j]
                    seg = linhas[j + 1] if j + 1 < n else None
                    parenteses = c.startswith("(") and c.endswith(")")
                    if parenteses or (len(c) <= 150 and not RE_INICIO.match(c) and not eh_estrutura(c)
                                      and not termina_frase(c) and comeca_maiuscula(seg)):
                        u["epigrafe"] = [c]
                        j += 1
            unidades.append(u)
            i = j
            continue
        if prof == 0 and (RE_DIVISAO.match(l) or RE_ANEXO.match(l)):
            md = RE_DIVISAO.match(l)
            anexo = not md
            u = {"tipo": "div", "nivel": 0 if anexo else NIVEIS[md.group("tipo")],
                 "linhas": [l], "pars": [], "idx": i}
            j = i + 1
            while j < n and len(u["linhas"]) < 4:
                c = linhas[j]
                if eh_estrutura(c) or RE_INICIO.match(c) or len(c) > 150 or termina_frase(c):
                    break
                if not anexo and len(u["linhas"]) > 1 and comeca_maiuscula(c):
                    break
                if md and md.group("tit") and comeca_maiuscula(c):
                    break
                u["linhas"].append(c)
                j += 1
            unidades.append(u)
            i = j
            continue
        if prof == 0 and RE_FECHO.match(l) and unidades[-1]["tipo"] != "fecho":
            unidades.append({"tipo": "fecho", "pars": [[l]], "idx": i})
            prof += l.count("«") - l.count("»")
            i += 1
            continue

        u = unidades[-1]
        if u["tipo"] == "div":  # texto solto depois de um título de divisão
            u = {"tipo": "pre", "pars": [], "idx": i}
            unidades.append(u)
        anterior = u["pars"][-1][-1] if u["pars"] else None
        curta = anterior is not None and len(anterior) < 0.6 * mediana and not anterior.endswith("-")
        if (not u["pars"] or RE_INICIO.match(l) or RE_VDO.fullmatch(l) or RE_LEGENDA.match(l)
                or (anterior is not None and (RE_VDO.fullmatch(anterior) or RE_LEGENDA.match(anterior)))
                or (anterior is not None and (re.search(r"[.:;»]$", anterior) or curta) and comeca_maiuscula(l))):
            novo_par(u, l)
        else:
            u["pars"][-1].append(l)
        prof += l.count("«") - l.count("»")
        i += 1

    # Um «fecho» (assinaturas, «Aprovado em…») só o é se não vier mais nenhum
    # artigo antes do próximo anexo. Caso contrário era texto do próprio artigo
    # (ex.: «O Presidente da Assembleia…» numa norma) e volta para lá.
    final: list[dict] = []
    for pos, u in enumerate(unidades):
        if u["tipo"] == "fecho":
            seguinte_art = False
            for v in unidades[pos + 1:]:
                if v["tipo"] == "div" and v["nivel"] == 0:
                    break
                if v["tipo"] == "art":
                    seguinte_art = True
                    break
            if seguinte_art and final:
                final[-1]["pars"].extend(u["pars"])
                continue
        final.append(u)
    return final, prof


# --------------------------------------------------------------- escrita
def escapar(texto: str) -> str:
    texto = re.sub(r"^(\d+)\.(\s)", r"\1\\.\2", texto)
    texto = re.sub(r"^([#>+*-])", r"\\\1", texto)
    return texto


def juntar(linhas: list[str]) -> str:
    return " ".join(x.strip() for x in linhas)


def titulo_div(u: dict) -> str:
    rot = u["linhas"][0]
    resto = juntar(u["linhas"][1:])
    return f"{rot} — {resto}" if resto else rot


def titulo_art(u: dict, sigla: str | None) -> str:
    rot = u["rotulo"]
    s = f" [{sigla}]" if sigla else ""
    if u["epigrafe"]:
        ep = juntar(u["epigrafe"])
        if ep.startswith("(") and ep.endswith(")"):
            ep = ep[1:-1]
        return f"{rot}{s} — {ep}"
    return f"{rot}{s}"


def yaml_valor(v) -> str:
    if v is None or v == "":
        return '""'
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", type=Path, help="texto extraído (.txt)")
    ap.add_argument("-o", "--saida", type=Path, required=True)
    ap.add_argument("--titulo", required=True, help="título do ficheiro, ex.: «Código Civil — Propriedade horizontal»")
    ap.add_argument("--diploma", required=True, help="identificação oficial, ex.: «Decreto-Lei n.º 47344/66, de 25 de novembro»")
    ap.add_argument("--sigla", help="sigla curta que vai em cada artigo, ex.: CC, CPC, RJUE")
    ap.add_argument("--fonte", required=True, help="DRE, PGDL, Alpaca ou outra")
    ap.add_argument("--url", default="")
    ap.add_argument("--em-vigor-desde", default="", help="AAAA-MM-DD da versão consolidada")
    ap.add_argument("--ultima-alteracao", default="")
    ap.add_argument("--data-consulta", default=dt.date.today().isoformat())
    ap.add_argument("--artigos", help="excerto: lista de artigos/intervalos")
    ap.add_argument("--depois-de", help="regex: só considerar artigos depois da primeira linha que lhe corresponda")
    ap.add_argument("--sem-preambulo", action="store_true", help="omitir texto antes do articulado e o fecho (assinaturas)")
    ap.add_argument("--relatorio", type=Path)
    a = ap.parse_args()

    linhas = [l.strip() for l in a.entrada.read_text(encoding="utf-8").splitlines() if l.strip()]
    unidades, prof_final = analisar(linhas)

    inicio = 0
    if a.depois_de:
        rx = re.compile(a.depois_de)
        pos = next((i for i, l in enumerate(linhas) if rx.search(l)), None)
        if pos is None:
            raise SystemExit(f"--depois-de: nenhuma linha corresponde a {a.depois_de!r}")
        inicio = pos

    intervalos = parse_lista(a.artigos) if a.artigos else None

    def selecionado(u) -> bool:
        if u.get("idx", 0) < inicio:
            return False
        if intervalos is None:
            return True
        k = u["chave"]
        return any(ordem(x) <= ordem(k) <= ordem(y) for x, y in intervalos)

    excerto = intervalos is not None
    corpo: list[str] = []
    pilha: dict[int, dict] = {}
    emitidas: set[int] = set()
    arts_encontrados, arts_emitidos, sem_epigrafe, vistos = [], [], [], {}
    ultimo_emitido = False

    for u in unidades:
        t = u["tipo"]
        if t == "div":
            nivel = u["nivel"]
            for k in [k for k in pilha if k >= nivel]:
                del pilha[k]
            pilha[nivel] = u
            if not excerto and u["idx"] >= inicio:
                corpo += [f"## {titulo_div(u)}", ""]
                emitidas.add(id(u))
            continue
        if t == "art":
            arts_encontrados.append(u["chave"])
            vistos[u["chave"]] = vistos.get(u["chave"], 0) + 1
            if not selecionado(u):
                ultimo_emitido = False
                continue
            if excerto:
                for nivel in sorted(pilha):
                    d = pilha[nivel]
                    if id(d) not in emitidas:
                        corpo += [f"## {titulo_div(d)}", ""]
                        emitidas.add(id(d))
            corpo += [f"### {titulo_art(u, a.sigla)}", ""]
            for p in u["pars"]:
                corpo += [escapar(juntar(p)), ""]
            arts_emitidos.append(u["rotulo"])
            if not u["epigrafe"]:
                sem_epigrafe.append(u["rotulo"])
            ultimo_emitido = True
            continue
        # pre / fecho
        if excerto or a.sem_preambulo or u.get("idx", inicio) < inicio:
            continue
        if not u["pars"]:
            continue
        if t == "fecho":
            corpo += ["<!-- fecho -->", ""]
        for p in u["pars"]:
            corpo += [escapar(juntar(p)), ""]

    def fmt(k):
        return "único" if k[1] == "ÚNICO" else f"{k[0]}.º" + (f"-{k[1]}" if k[1] else "")

    em_falta = []
    if intervalos:
        for x, y in intervalos:
            if x == y and x not in vistos:
                em_falta.append(fmt(x))
            elif not any(ordem(x) <= ordem(k) <= ordem(y) for k in vistos):
                em_falta.append(f"{fmt(x)} a {fmt(y)}")
    repetidos = [fmt(k) for k, c in vistos.items() if c > 1]

    lista_excerto = None
    if excerto:
        presentes = [(x, y) for x, y in intervalos
                     if (fmt(x) if x == y else f"{fmt(x)} a {fmt(y)}") not in em_falta]
        lista_excerto = ", ".join(fmt(x) if x == y else f"{fmt(x)} a {fmt(y)}" for x, y in presentes) or "nenhum"

    fm = {
        "titulo": a.titulo, "diploma": a.diploma, "sigla": a.sigla or "",
        "tipo": "excerto" if excerto else "integral",
        "artigos": lista_excerto or "todos",
        "versao": "consolidada em vigor",
        "em_vigor_desde": a.em_vigor_desde, "ultima_alteracao": a.ultima_alteracao,
        "fonte": a.fonte, "fonte_url": a.url, "data_consulta": a.data_consulta,
        "verificacao": "pendente",
    }
    cab = ["---"] + [f"{k}: {yaml_valor(v)}" for k, v in fm.items()] + ["---", "", f"# {a.titulo}", "",
                                                                       "<!-- cabecalho -->"]
    vig = f", versão em vigor desde {a.em_vigor_desde}" if a.em_vigor_desde else ", versão em vigor (data por confirmar)"
    alt = f" (última alteração: {a.ultima_alteracao})" if a.ultima_alteracao else ""
    cab.append(f"> **{a.diploma}** — texto consolidado{vig}{alt}.  ")
    fonte_txt = f"[{a.fonte}]({a.url})" if a.url else a.fonte
    cab.append(f"> Fonte: {fonte_txt} · consultada em {a.data_consulta}.  ")
    if excerto:
        cab.append(f"> **Excerto:** contém apenas os artigos {lista_excerto}. "
                   "Um artigo que não esteja neste ficheiro pode existir no diploma.")
    cab += ["<!-- /cabecalho -->", ""]

    a.saida.write_text("\n".join(cab + corpo).rstrip() + "\n", encoding="utf-8")

    alertas = []
    if prof_final != 0:
        alertas.append("Aspas « » desequilibradas no texto: a deteção de artigos pode ter falhado depois de uma citação.")
    if em_falta:
        alertas.append(f"Artigos pedidos e não encontrados: {em_falta}")
    if repetidos and not a.depois_de:
        alertas.append(f"Números de artigo repetidos ({repetidos[:10]}…): pode ser o decreto preambular e o código "
                       "anexo; usar --depois-de \"^ANEXO\" ou confirmar.")
    if not a.em_vigor_desde or not a.url:
        alertas.append("Metadados em falta (--em-vigor-desde e/ou --url): preencher antes de publicar.")
    if not arts_encontrados:
        alertas.append("Nenhum artigo detetado: confirmar se o texto é mesmo um articulado.")

    rel = {"artigos_detetados": len(arts_encontrados), "artigos_no_ficheiro": len(arts_emitidos),
           "sem_epigrafe": sem_epigrafe, "repetidos": repetidos, "em_falta": em_falta, "alertas": alertas}
    rel_path = a.relatorio or a.saida.with_suffix(".estrutura.json")
    rel_path.write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Artigos detetados: {len(arts_encontrados)} · no ficheiro: {len(arts_emitidos)}")
    print(f"Sem epígrafe: {len(sem_epigrafe)}" + (f" ({', '.join(sem_epigrafe[:15])})" if sem_epigrafe else ""))
    for al in alertas:
        print("ALERTA:", al)
    print(f"Markdown: {a.saida}")


if __name__ == "__main__":
    main()
