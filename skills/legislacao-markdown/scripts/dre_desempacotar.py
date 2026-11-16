#!/usr/bin/env python3
"""Separa os PDF do pacote gravado pelo dre_descarregar.js.

Uso:  python3 dre_desempacotar.py ~/Downloads/dre_pdfs.json -o pdfs/
Cada PDF fica com o nome que tem no endereço oficial. Escreve também
pdfs/origem.json (nome do ficheiro → endereço), para a nota de cada quadro.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pacote", type=Path)
    ap.add_argument("-o", "--saida", type=Path, default=Path("pdfs"))
    a = ap.parse_args()
    pacote = json.loads(a.pacote.read_text(encoding="utf-8"))
    a.saida.mkdir(parents=True, exist_ok=True)
    mapa_f = a.saida / "origem.json"
    mapa = json.loads(mapa_f.read_text(encoding="utf-8")) if mapa_f.exists() else {}
    falhas = 0
    for url, v in pacote.items():
        if "erro" in v:
            print(f"FALHOU  {url}: {v['erro']}")
            falhas += 1
            continue
        dados = base64.b64decode(v["base64"])
        if not dados.startswith(b"%PDF") or len(dados) != v.get("bytes", len(dados)):
            print(f"FALHOU  {url}: o conteúdo não é um PDF íntegro")
            falhas += 1
            continue
        nome = url.rstrip("/").rsplit("/", 1)[-1]
        if not nome.lower().endswith(".pdf"):
            nome += ".pdf"
        (a.saida / nome).write_bytes(dados)
        mapa[nome] = url
        print(f"ok      {a.saida / nome}  ({len(dados):,} bytes)".replace(",", " "))
    mapa_f.write_text(json.dumps(mapa, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
