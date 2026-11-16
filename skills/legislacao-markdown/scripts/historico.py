#!/usr/bin/env python3
"""Lê o «histórico de redação» do texto consolidado do DRE e diz, para cada
artigo ou anexo, qual foi o último ato que o alterou.

Serve para saber que PDF abrir quando o DRE mostra «(ver documento original)»:
a ligação do DRE aponta sempre para o PDF da publicação original, mesmo quando
o artigo foi alterado depois. O quadro em vigor está no PDF do último ato que
alterou esse artigo (se esse PDF o trouxer), não no original.

Entrada: o texto da página de legislação consolidada do DRE (copiado ou
guardado como .txt / .md), com linhas do tipo
  «Alterado pelo/a Artigo 2.º do/a Portaria n.º 135/2020 - Diário da República
   n.º 107/2020, Série I de 2020-06-02, em vigor a partir de 2020-08-01»

Uso:
  python3 historico.py consolidado.txt                  # só fragmentos com quadros
  python3 historico.py consolidado.txt --todos
  python3 historico.py consolidado.txt --artigo 26 --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RE_HIST = re.compile(
    r"(?P<verbo>Alterad[oa]|Aditad[oa]|Revogad[oa]|Re[c]?tificad[oa]|Republicad[oa]|Renumerad[oa]|Substituíd[oa])"
    r"\s+pel[oa]/[ao]\s+(?P<onde>.+?)\s+d[oa]/[ao]\s+(?P<ato>.+?)\s+-\s+Diário da República n\.º\s*(?P<dr>[^,]+),"
    r"\s*(?P<serie>[^,]*?)\s+de\s+(?P<data>\d{4}-\d{2}-\d{2})"
    r"(?:,\s*em vigor a partir de\s+(?P<vigor>\d{4}-\d{2}-\d{2}))?"
)
RE_FRAG = re.compile(
    r"^\s*#*\s*(?P<rot>(?:Artigo\s+\d+\.?[ºo°]?(?:\s*-\s*[A-Z]{1,2})?|Artigo único|"
    r"ANEXO(?:\s+[IVXLC\d]+(?:-[A-Z])?)?|Anexo(?:\s+[IVXLC\d]+(?:-[A-Z])?)?))\b(?P<resto>.*)$"
)
RE_ORIGINAL = re.compile(r"\(ver documento original\)", re.I)
RE_LEGENDA = re.compile(r"^\s*(QUADRO|Quadro|TABELA|Tabela|MAPA|Mapa|MODELO|Modelo)\s+[IVXLC\d]+", re.M)


def analisar(texto: str) -> list[dict]:
    frags: list[dict] = []
    atual = {"fragmento": "(antes do primeiro artigo)", "linha": 1, "historico": [], "originais": 0, "legendas": []}
    frags.append(atual)
    contexto = ""
    ultima_legenda = ""
    for n, linha in enumerate(texto.splitlines(), 1):
        m = RE_FRAG.match(linha)
        if m and not RE_HIST.search(linha) and len(linha) < 160:
            rot = re.sub(r"\s+", " ", m.group("rot")).strip()
            if rot.lower().startswith("anexo"):
                contexto = rot
            nome = rot if rot.lower().startswith("anexo") or not contexto else f"{rot} ({contexto})"
            atual = {"fragmento": nome, "linha": n, "historico": [], "originais": 0, "legendas": []}
            frags.append(atual)
            ultima_legenda = ""
            continue
        h = RE_HIST.search(linha)
        if h:
            d = h.groupdict()
            atual["historico"].append({"verbo": d["verbo"], "onde": d["onde"], "ato": d["ato"].strip(),
                                       "dr": d["dr"].strip(), "serie": d["serie"].strip(),
                                       "publicado": d["data"], "em_vigor": d["vigor"] or d["data"]})
            continue
        lm = RE_LEGENDA.match(linha)
        if lm:
            ultima_legenda = linha.strip()
        k = len(RE_ORIGINAL.findall(linha))
        if k:
            atual["originais"] += k
            atual["legendas"] += [ultima_legenda] * k
            ultima_legenda = ""
    for f in frags:
        hist = f["historico"]
        if hist:
            ult = max(enumerate(hist), key=lambda ih: (ih[1]["em_vigor"], ih[1]["publicado"], ih[0]))[1]
            f["ultimo"] = ult
            f["revogado"] = ult["verbo"].lower().startswith("revogad")
        else:
            f["ultimo"] = None
            f["revogado"] = False
    return frags


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ficheiro", type=Path)
    ap.add_argument("--artigo", help="mostrar só este artigo/anexo (ex.: 26, 26-A, \"Anexo II\")")
    ap.add_argument("--todos", action="store_true", help="incluir fragmentos sem «(ver documento original)»")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    frags = analisar(a.ficheiro.read_text(encoding="utf-8", errors="replace"))
    if a.artigo:
        alvo = a.artigo.strip().lower()
        if re.fullmatch(r"\d+(-[a-z]{1,2})?", alvo):
            num, _, suf = alvo.partition("-")
            rx = re.compile(rf"^artigo {num}\.?[ºo°]?" + (rf"\s*-\s*{suf}" if suf else r"(?!\s*-\s*[a-z])") + r"(\s|$)", re.I)
            frags = [f for f in frags if rx.match(f["fragmento"])]
        else:
            frags = [f for f in frags if f["fragmento"].lower().startswith(alvo)]
    elif not a.todos:
        frags = [f for f in frags if f["originais"]]
    if a.json:
        print(json.dumps(frags, ensure_ascii=False, indent=2))
        return
    if not frags:
        print("Nenhum fragmento encontrado com esses critérios.")
        sys.exit(1)
    atos: dict[str, int] = {}
    for f in frags:
        u = f["ultimo"]
        leg = "; ".join(l for l in f["legendas"] if l) or "—"
        print(f"\n{f['fragmento']}  (linha {f['linha']}) — {f['originais']} «(ver documento original)» · legendas: {leg[:110]}")
        if u is None:
            print("   sem histórico de redação → usar o PDF ORIGINAL do diploma")
            atos["PDF original"] = atos.get("PDF original", 0) + f["originais"]
        elif f["revogado"]:
            print(f"   REVOGADO por {u['ato']} (em vigor a partir de {u['em_vigor']}) → o quadro já não está em vigor")
        else:
            print(f"   última alteração: {u['verbo']} por {u['ato']} — DR n.º {u['dr']}, {u['serie']} de "
                  f"{u['publicado']}, em vigor a partir de {u['em_vigor']}")
            print(f"   → procurar o quadro no PDF de «{u['ato']}». Se esse PDF não o trouxer, o quadro não foi "
                  "alterado por esse ato: recuar para o ato anterior do histórico ou para o original.")
            if len(f["historico"]) > 1:
                outros = sorted({h["ato"] for h in f["historico"]} - {u["ato"]})
                if outros:
                    print(f"   atos anteriores no histórico: {', '.join(outros)}")
            atos[u["ato"]] = atos.get(u["ato"], 0) + f["originais"]
    if atos:
        print("\nResumo — PDF a obter e n.º de quadros que cada um pode resolver:")
        for ato, n in sorted(atos.items(), key=lambda x: -x[1]):
            print(f"   {n:4d}  {ato}")


if __name__ == "__main__":
    main()
