#!/usr/bin/env python3
"""Verifica que o Markdown contém exatamente as palavras do texto extraído.

Compara, artigo a artigo, a sequência de palavras do texto de origem (saída
de extrair.py) com a do Markdown, ignorando apenas o que foi acrescentado de
propósito: metadados, cabeçalho de aviso, título do ficheiro, sigla [XX] nos
títulos dos artigos e a marcação Markdown. Num diploma inteiro faz também uma
contagem global de todas as palavras.

Não deteta alterações de pontuação (só palavras e números).

Uso:
    python3 verificar.py texto.txt saida.md [--relatorio verif.json] [--marcar]

--marcar escreve o resultado no campo «verificacao» dos metadados do .md.
Código de saída 0 = sem diferenças; 1 = há diferenças.
"""
from __future__ import annotations

import argparse
import collections
import difflib
import json
import re
from pathlib import Path

RE_ARTIGO = re.compile(
    r"^(?i:artigo|art\.)\s+(?:(\d+)\s*\.?\s*[ºo°]?\s*(?:-\s*([A-Z]{1,2}))?|(?i:(único)))"
    r"\s*(?:[-–—]\s*.+|\([^)]+\))?\s*$"
)
RE_DIVISAO = re.compile(r"^(LIVRO|PARTE|TÍTULO|CAPÍTULO|SECÇÃO|SUBSECÇÃO|DIVISÃO|SUBDIVISÃO)\b|^(ANEXO|Anexo)(\s+[IVXLC\d]+(-[A-Z])?)?\s*$")
RE_FECHO = re.compile(
    r"^(Aprovad[oa]s? em|Visto e aprovado|Promulgad[oa] em|Referendad[oa] em|Publique-se|"
    r"O Presidente da República|O Primeiro-Ministro|A Primeira-Ministra|O Presidente da Assembleia|"
    r"Pel[oa] Primeir|O Ministro d|A Ministra d)"
)


def palavras(texto: str) -> list[str]:
    return re.findall(r"\w+", texto)


def chave(m: re.Match) -> tuple:
    if m.group(3):
        return (0, "ÚNICO")
    return (int(m.group(1)), m.group(2) or "")


def fechos_genuinos(linhas: list[str]) -> set[int]:
    """Linhas de fecho (assinaturas) que não são seguidas por mais artigos antes do próximo anexo."""
    prof, arts, anexos, fechos = 0, [], [], []
    for i, l in enumerate(linhas):
        if prof == 0:
            if RE_ARTIGO.match(l):
                arts.append(i)
            elif re.match(r"^(ANEXO|Anexo)(\s+[IVXLC\d]+(-[A-Z])?)?\s*$", l):
                anexos.append(i)
            elif RE_FECHO.match(l):
                fechos.append(i)
        prof += l.count("«") - l.count("»")
    bons = set()
    for f in fechos:
        prox_art = next((a for a in arts if a > f), None)
        prox_anx = next((a for a in anexos if a > f), None)
        if prox_art is None or (prox_anx is not None and prox_anx < prox_art):
            bons.add(f)
    return bons


def blocos_origem(linhas: list[str]) -> list[tuple[tuple, list[str]]]:
    blocos, atual, prof = [], None, 0
    fechos = fechos_genuinos(linhas)
    for i, l in enumerate(linhas):
        m = RE_ARTIGO.match(l) if prof == 0 else None
        if m:
            atual = (chave(m), [l])
            blocos.append(atual)
        elif prof == 0 and (RE_DIVISAO.match(l) or i in fechos):
            atual = None
        elif atual is not None:
            atual[1].append(l)
        prof += l.count("«") - l.count("»")
    return blocos


def limpar_md(md: str) -> tuple[list[str], str]:
    """Devolve (linhas do corpo sem marcação, título)."""
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    md = re.sub(r"<!-- cabecalho -->.*?<!-- /cabecalho -->", "", md, flags=re.S)
    saida, titulo_vista = [], False
    for l in md.splitlines():
        if not titulo_vista and l.startswith("# "):
            titulo_vista = True
            continue
        if l.startswith("###"):
            l = re.sub(r"^#+\s*", "", l)
            l = re.sub(r"\s\[[^\]]{1,15}\]", "", l, count=1)
            l = "§ART§ " + l
        elif l.startswith("#"):
            l = "§DIV§ " + re.sub(r"^#+\s*", "", l)
        l = l.replace("\\", "")
        saida.append(l)
    return saida, ""


def blocos_md(linhas: list[str]) -> list[tuple[tuple, list[str]]]:
    blocos, atual = [], None
    for l in linhas:
        if l.startswith("§ART§ "):
            txt = l[6:]
            rot = re.split(r"\s+—\s+", txt, maxsplit=1)[0]
            m = RE_ARTIGO.match(rot)
            atual = ((chave(m) if m else ("?", rot)), [txt])
            blocos.append(atual)
        elif l.startswith("§DIV§ ") or l.strip() == "<!-- fecho -->":
            atual = None
        elif atual is not None:
            atual[1].append(l)
    return blocos


def resumo_diff(a: list[str], b: list[str], maximo: int = 8) -> list[str]:
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        ctx = " ".join(a[max(0, i1 - 4):i1])
        if op == "delete":
            out.append(f"FALTA no .md: «{' '.join(a[i1:i2])}» (depois de «…{ctx}»)")
        elif op == "insert":
            out.append(f"A MAIS no .md: «{' '.join(b[j1:j2])}» (depois de «…{ctx}»)")
        else:
            out.append(f"TROCADO: origem «{' '.join(a[i1:i2])}» → .md «{' '.join(b[j1:j2])}» (depois de «…{ctx}»)")
        if len(out) >= maximo:
            out.append("…")
            break
    return out


def fmt(k: tuple) -> str:
    if k[0] == "?":
        return k[1]
    return "único" if k[1] == "ÚNICO" else f"{k[0]}.º" + (f"-{k[1]}" if k[1] else "")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("origem", type=Path, help="texto extraído (.txt)")
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--relatorio", type=Path)
    ap.add_argument("--marcar", action="store_true", help="gravar o resultado nos metadados do .md")
    a = ap.parse_args()

    origem = [l.strip() for l in a.origem.read_text(encoding="utf-8").splitlines() if l.strip()]
    md_txt = a.markdown.read_text(encoding="utf-8")
    excerto = bool(re.search(r'^tipo:\s*"?excerto', md_txt, re.M))
    md_linhas, _ = limpar_md(md_txt)

    bo = blocos_origem(origem)
    bm = blocos_md(md_linhas)
    por_chave = collections.defaultdict(list)
    for k, ls in bo:
        por_chave[k].append(palavras(" ".join(ls)))

    problemas, ok = [], 0
    for k, ls in bm:
        pm = palavras(" ".join(ls))
        cands = por_chave.get(k)
        if not cands:
            problemas.append({"artigo": fmt(k), "diferencas": ["Artigo não existe no texto de origem"]})
            continue
        melhor = max(cands, key=lambda c: difflib.SequenceMatcher(None, c, pm, autojunk=False).ratio())
        if melhor == pm:
            ok += 1
        else:
            problemas.append({"artigo": fmt(k), "diferencas": resumo_diff(melhor, pm)})

    global_dif = []
    if not excerto:
        co = collections.Counter(palavras(" ".join(origem)))
        cm = collections.Counter(palavras(" ".join(l[6:] if l.startswith("§") else l for l in md_linhas
                                                   if l.strip() != "<!-- fecho -->")))
        falta = co - cm
        mais = cm - co
        if falta:
            global_dif.append("Palavras em falta no .md: " + ", ".join(f"{w}×{c}" for w, c in falta.most_common(20)))
        if mais:
            global_dif.append("Palavras a mais no .md: " + ", ".join(f"{w}×{c}" for w, c in mais.most_common(20)))
        n_art_origem = len(bo)
        if n_art_origem != len(bm):
            global_dif.append(f"Número de artigos difere: origem {n_art_origem}, .md {len(bm)}")

    passou = not problemas and not global_dif
    rel = {"modo": "excerto" if excerto else "integral", "artigos_verificados": len(bm),
           "artigos_iguais": ok, "artigos_com_diferencas": problemas, "diferencas_globais": global_dif,
           "resultado": "OK" if passou else "DIFERENÇAS"}
    rel_path = a.relatorio or a.markdown.with_suffix(".verificacao.json")
    rel_path.write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Modo: {rel['modo']} · artigos verificados: {len(bm)} · iguais à origem: {ok}")
    for p in problemas[:20]:
        print(f"  Artigo {p['artigo']}:")
        for d in p["diferencas"]:
            print(f"    - {d}")
    for g in global_dif:
        print("  " + g)
    print("RESULTADO:", rel["resultado"])

    if a.marcar:
        texto = (f"automática OK: {ok}/{len(bm)} artigos palavra a palavra" if passou
                 else f"automática com diferenças ({len(problemas)} artigos) — rever")
        novo = re.sub(r'^verificacao:.*$', f'verificacao: "{texto}"', md_txt, count=1, flags=re.M)
        a.markdown.write_text(novo, encoding="utf-8")
    raise SystemExit(0 if passou else 1)


if __name__ == "__main__":
    main()
