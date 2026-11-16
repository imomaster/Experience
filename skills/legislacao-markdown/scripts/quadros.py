#!/usr/bin/env python3
"""Integra nos ficheiros Markdown os quadros extraídos pelo tabelas.py.

Três operações, todas feitas por programa (nada é copiado à mão):

  inserir  põe um quadro verificado a seguir ao «(ver documento original)» certo
  contar   diz quantos quadros de um ficheiro foram reproduzidos e quantos ficaram só com ligação
  juntar   une as partes de um quadro que continua noutra coluna ou página

Uso:
  python3 quadros.py inserir BLOCO.md quadros/doc_p11_q1.md --legenda "QUADRO XX"
  python3 quadros.py inserir BLOCO.md quadros/doc_p25_q2.md --ocorrencia 14
  python3 quadros.py inserir BLOCO.md quadros/x.md --legenda "Tabela I" --aprovado     # modo linear
  python3 quadros.py contar BLOCO_05.md BLOCO_06.md
  python3 quadros.py juntar quadros/a_p25_q2.md quadros/a_p25_q4.md -o quadros/anexo2.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RE_ORIGINAL = re.compile(r"\(ver documento original\)", re.I)
RE_ABRE = re.compile(r"<!-- quadro (?P<attrs>.*?) -->")
FECHA = "<!-- /quadro -->"


def attrs_de(linha: str) -> dict[str, str]:
    m = RE_ABRE.search(linha)
    return dict(re.findall(r'(\w+)="([^"]*)"', m.group("attrs"))) if m else {}


def ler_quadro(caminho: Path) -> tuple[dict[str, str], list[str]]:
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    ini = next((i for i, l in enumerate(linhas) if RE_ABRE.search(l)), None)
    fim = next((i for i, l in enumerate(linhas) if l.strip() == FECHA), None)
    if ini is None or fim is None or fim < ini:
        sys.exit(f"{caminho}: não é um quadro gerado pelo tabelas.py (faltam os marcadores).")
    return attrs_de(linhas[ini]), linhas[ini:fim + 1]


def ocorrencias(linhas: list[str]) -> list[dict]:
    """Cada «(ver documento original)» do ficheiro, com o estado do quadro que tem a seguir."""
    out, dentro = [], False
    for i, l in enumerate(linhas):
        if RE_ABRE.search(l):
            dentro = True
        if l.strip() == FECHA:
            dentro = False
            continue
        if dentro:
            continue
        for _ in RE_ORIGINAL.finditer(l):
            j = i + 1
            while j < len(linhas) and not linhas[j].strip():
                j += 1
            at = attrs_de(linhas[j]) if j < len(linhas) and RE_ABRE.search(linhas[j]) else None
            out.append({"linha": i, "quadro": at, "inicio_quadro": j if at is not None else None})
    return out


def cmd_inserir(a) -> None:
    bloco = Path(a.bloco)
    linhas = bloco.read_text(encoding="utf-8").splitlines()
    at, quadro = ler_quadro(Path(a.quadro))
    modo, res = at.get("modo", ""), at.get("resultado", "")
    if res != "OK":
        sys.exit(f"Recusado: o quadro está com resultado «{res or '?'}» (modo {modo}). Só entram quadros "
                 "com RESULTADO: OK. Um quadro recusado fica só com a ligação ao PDF que já lá está.")
    if modo == "linear" and not a.aprovado:
        sys.exit("Recusado: o quadro está em modo linear (sem colunas). Só entra depois de aprovação "
                 "humana; repetir com --aprovado quando o utilizador o tiver visto e aceitado.")
    if modo not in ("grelha", "linear"):
        sys.exit(f"Recusado: modo «{modo}».")

    ocs = ocorrencias(linhas)
    if not ocs:
        sys.exit(f"{bloco}: não tem nenhum «(ver documento original)».")
    if a.ocorrencia:
        if not 1 <= a.ocorrencia <= len(ocs):
            sys.exit(f"{bloco} tem {len(ocs)} ocorrência(s).")
        alvo = ocs[a.ocorrencia - 1]
    elif a.legenda:
        rx = re.compile(r"(?<!\w)" + r"\s+".join(re.escape(t) for t in a.legenda.split()) + r"(?!\w)", re.I)
        marcos = [i for i, l in enumerate(linhas) if rx.search(l) and not RE_ABRE.search(l)]
        cands = []
        for m in marcos:
            seg = next((o for o in ocs if o["linha"] >= m), None)
            if seg is not None and seg["linha"] - m <= 12 and seg not in cands:
                cands.append(seg)
        if not cands:
            sys.exit(f"Não encontrei «(ver documento original)» logo a seguir a «{a.legenda}» em {bloco}.")
        if len(cands) > 1:
            nums = [ocs.index(c) + 1 for c in cands]
            sys.exit(f"«{a.legenda}» aparece antes de várias ocorrências ({nums}). Indicar --ocorrencia N.")
        alvo = cands[0]
    else:
        sys.exit("Indicar --legenda ou --ocorrencia.")

    n = ocs.index(alvo) + 1
    if alvo["quadro"] is not None:
        if not a.substituir:
            sys.exit(f"A ocorrência {n} já tem um quadro inserido. Repetir com --substituir para o trocar.")
        ini = alvo["inicio_quadro"]
        fim = next(i for i in range(ini, len(linhas)) if linhas[i].strip() == FECHA)
        linhas[ini:fim + 1] = quadro
    else:
        linhas[alvo["linha"] + 1:alvo["linha"] + 1] = [""] + quadro + [""]
    bloco.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Inserido em {bloco}, ocorrência {n} de {len(ocs)} (linha {alvo['linha'] + 1}), modo {modo}.")


def contagem(caminho: Path) -> dict:
    ocs = ocorrencias(caminho.read_text(encoding="utf-8").splitlines())
    c = {"ficheiro": str(caminho), "total": len(ocs), "grelha": 0, "linear": 0, "so_ligacao": 0}
    for o in ocs:
        m = (o["quadro"] or {}).get("modo")
        c["grelha" if m == "grelha" else "linear" if m == "linear" else "so_ligacao"] += 1
    return c


def cmd_contar(a) -> None:
    res = [contagem(Path(f)) for f in a.ficheiros]
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print(f"{'ficheiro':<48} {'total':>6} {'grelha':>7} {'linear':>7} {'só ligação':>11}")
    for c in res:
        print(f"{Path(c['ficheiro']).name[:48]:<48} {c['total']:>6} {c['grelha']:>7} {c['linear']:>7} {c['so_ligacao']:>11}")
    if len(res) > 1:
        t = {k: sum(c[k] for c in res) for k in ("total", "grelha", "linear", "so_ligacao")}
        print(f"{'TOTAL':<48} {t['total']:>6} {t['grelha']:>7} {t['linear']:>7} {t['so_ligacao']:>11}")


def cmd_juntar(a) -> None:
    partes = [ler_quadro(Path(f)) for f in a.partes]
    cab = None
    corpo: list[str] = []
    paginas, fontes, versoes = [], [], []
    for (at, linhas), f in zip(partes, a.partes):
        if at.get("modo") != "grelha" or at.get("resultado") != "OK":
            sys.exit(f"{f}: só se juntam quadros em grelha com RESULTADO: OK "
                     f"(este está em {at.get('modo')}/{at.get('resultado')}).")
        tab = [l for l in linhas if l.startswith("|")]
        if len(tab) < 3:
            sys.exit(f"{f}: sem linhas de dados.")
        if cab is None:
            cab = tab[:2]
        elif tab[0] != cab[0]:
            sys.exit(f"{f}: o cabeçalho é diferente do da primeira parte. Não são o mesmo quadro "
                     f"(ou a continuação não repete o cabeçalho).\n  1.ª parte: {cab[0]}\n  esta:      {tab[0]}")
        corpo += tab[2:]
        paginas.append(at.get("pagina", "?"))
        fontes.append(at.get("fonte", ""))
        versoes.append(at.get("versao", ""))
    if len(set(fontes)) > 1 or len(set(versoes)) > 1:
        sys.exit("As partes vêm de PDF ou versões diferentes: não se juntam.")
    pags = ", ".join(dict.fromkeys(paginas))
    fonte, versao = fontes[0] or "PDF", versoes[0]
    v = f", versão: {versao}" if versao else ""
    out = [f'<!-- quadro fonte="{fontes[0]}" pagina="{pags}" versao="{versao}" modo="grelha" resultado="OK" -->',
           *cab, *corpo, "",
           f"> Quadro extraído do PDF oficial ({fonte}, págs. {pags}{v}) — verificado; "
           f"reunido a partir de {len(partes)} partes.",
           FECHA]
    Path(a.saida).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Quadro reunido: {len(corpo)} linhas de {len(partes)} partes → {a.saida}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inserir", help="inserir um quadro verificado num ficheiro Markdown")
    i.add_argument("bloco")
    i.add_argument("quadro")
    i.add_argument("--legenda", help="texto que antecede o quadro no ficheiro (ex.: \"QUADRO XX\")")
    i.add_argument("--ocorrencia", type=int, help="n.º do «(ver documento original)» no ficheiro (1 = primeiro)")
    i.add_argument("--aprovado", action="store_true", help="o utilizador viu e aprovou um quadro em modo linear")
    i.add_argument("--substituir", action="store_true", help="trocar um quadro já inserido nessa ocorrência")
    i.set_defaults(func=cmd_inserir)
    c = sub.add_parser("contar", help="contar quadros reproduzidos e só com ligação")
    c.add_argument("ficheiros", nargs="+")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_contar)
    j = sub.add_parser("juntar", help="unir as partes de um quadro que continua noutra coluna/página")
    j.add_argument("partes", nargs="+")
    j.add_argument("-o", "--saida", required=True)
    j.set_defaults(func=cmd_juntar)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
