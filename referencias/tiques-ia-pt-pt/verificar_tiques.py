#!/usr/bin/env python3
"""Verificador de «tiques de IA» em português europeu (PT-PT).

Uso:  python3 verificar_tiques.py FICHEIRO [--formal]
      cat texto.txt | python3 verificar_tiques.py - [--formal]

Procura os padrões de LISTA.md por expressão regular. Não prova que um texto
foi escrito por IA nem que está bom: aponta o sítio onde um padrão aparece.
BAN = tique mesmo uma só vez. CAP = tolerável uma vez, tique se repetido.
--estilo-casa: ignora «!» e emoji (T2), quando são escolha de estilo tua.
--formal: desliga os padrões que são fórmula legítima em cartas e peças
jurídicas («importa referir», «em suma») e o aviso de frases longas.
Estado de calibração: ver LISTA.md, secção «Estado de validação».
"""
import re, sys

I = re.IGNORECASE
# (id, nível, formal_ok, expressão, nota)
R = [
 # Estruturais
 ("P1", "BAN", False, r"\bn[ãa]o (é|são|foi|era|se trata)\b[^.!?\n]{0,90}?[,;:—–-]\s*(mas\s+|antes\s+)?(é|são|foi|era|trata-se|sim)\b", "contraste «Não é X, é Y»"),
 ("P1", "BAN", False, r"\bn[ãa]o se trata (apenas |só |simplesmente )?de\b", "contraste «Não se trata de X»"),
 ("P1", "BAN", False, r"\bn[ãa]o (é|são|foi|era|lhe vamos|vamos|fazemos|substituem|substitui)\b[^.!?\n]{0,70}[.!]\s+(é|são|foi|vamos|fazem|faz|fazemos|trata-se|sim)\b", "contraste entre frases «Não é X. É Y.»"),
 ("P1", "BAN", False, r"\b(fazem|faz|fazemos) outra coisa\b|\bé o contrário\b|\bé a diferença entre\b", "contraste «faz outra coisa / é o contrário / é a diferença entre»"),
 ("P1", "BAN", False, r"\bmais (do )?que (um|uma|o|a|apenas)\b[^.!?\n]{0,70},\s*(é|são|somos)\b", "contraste «Mais do que X, é Y»"),
 ("P1", "CAP", False, r"\bn[ãa]o (só|apenas|somente)\b[^.!?\n]{0,80}\bmas (também|ainda)\b", "«não só… mas também» (legítimo uma vez)"),
 ("P2", "BAN", False, r"\bsem\b[^,.;!?\n]{1,40},\s*sem\b[^,.;!?\n]{1,40}", "lista de negações «sem X, sem Y»"),
 ("P2", "BAN", False, r"\b(zero|nenhum[a]?)\b[^,.;!?\n]{1,30},\s*(zero|nenhum[a]?)\b", "lista de negações «zero X, zero Y»"),
 ("P3", "CAP", False, r",\s*(garantindo|permitindo|assegurando|proporcionando|promovendo|potenciando|facilitando|possibilitando|contribuindo|criando)\b", "oração em gerúndio a rematar (acumulação final)"),
 ("P4", "BAN", False, r"\b(o resultado|a diferença|o segredo|a boa notícia|a má notícia|o truque|o problema|a questão|a verdade|o melhor)\s*\?\s+\S", "pergunta retórica a que o texto responde"),
 ("P4", "BAN", False, r"\b(porqu[êe]|porque é que (isto|isso) importa)\s*\?\s+(porque|pois)", "«Porquê? Porque…»"),
 ("P5", "BAN", False, r"\b(a melhor parte|o melhor de tudo|o segredo|a verdade|a boa notícia|uma palavra|a regra de ouro)\s*:", "revelação com dois pontos"),
 ("P8", "CAP", False, r"[—–]", "travessão longo (ban em copy curta: título, anúncio, assunto, post; no máximo 1–2 por página em texto longo)"),
 # Aberturas, fechos, preparações
 ("A1", "BAN", False, r"\b(num|no) mundo (cada vez mais|atual|de hoje|em constante)", "abertura de era"),
 ("A1", "BAN", False, r"\b(nos dias de hoje|na era digital|no atual (panorama|contexto|cenário)|num (setor|mercado|panorama|cenário) em constante)\b", "abertura de era"),
 ("A1", "CAP", False, r"\bem constante (evolução|mudança|transformação)\b", "«em constante evolução»"),
 ("A2", "BAN", False, r"\b(quer|seja)\s+(seja\s+)?(um|uma|o|a|que|se trate)\b[^.!?\n]{0,70}\b(quer|ou)\b", "falsa alternativa de abertura «Quer seja X ou Y»"),
 ("A3", "BAN", False, r"(?:^|(?<=[.!?]\s))imagine\b", "«Imagine…»"),
 ("A4", "BAN", False, r"\b(a verdade é que|vamos ser (honestos|sinceros)|para ser (honesto|sincero)|deixe-me ser claro|a questão é simples)\b", "pigarro / preparação"),
 ("A4", "CAP", True,  r"\b(convém|importa|vale a pena|é (importante|fundamental|essencial))\s+(referir|salientar|sublinhar|destacar|notar|ressalvar)\b", "enchimento («importa salientar»); idiomático em peças jurídicas"),
 ("A5", "BAN", False, r"\b(neste (artigo|guia|texto|post|email),?\s+(vamos|iremos|veremos|exploraremos)|vamos (mergulhar|explorar|descobrir|desvendar)|mergulhe)\b", "anúncio do que vai ser dito"),
 ("A6", "CAP", True,  r"\b(em suma|em conclusão|no final do dia|em última análise|em jeito de conclusão)\b", "fecho-resumo"),
 ("A7", "BAN", False, r"\b(porque o futuro não espera|e isso muda tudo|o resto é história|e é aqui que (tudo )?(muda|começa))\b", "remate pseudo-profundo"),
 ("A8", "CAP", True,  r"(?:^|(?<=[.!?]\s))(além disso|adicionalmente|por outro lado|acima de tudo),", "transição de enchimento"),
 # Frases de marketing
 ("M1", "BAN", False, r"\bdig[ao]\s+(adeus|olá)\s+(a|à|às|ao|aos)\b", "«Diga adeus a…»"),
 ("M2", "BAN", False, r"\b(desbloqueie|liberte|desencadeie)\b[^.!?\n]{0,30}\b(poder|potencial)\b", "«Desbloqueie o potencial»"),
 ("M3", "BAN", False, r"\bpara o próximo nível\b|\bao próximo nível\b", "«para o próximo nível»"),
 ("M4", "BAN", False, r"\b(transforme|revolucione|reinvente)\b[^.!?\n]{0,25}\b(a (forma|maneira) como|o seu negócio|o modo como)\b", "«Transforme a forma como…»"),
 ("M5", "BAN", False, r"\bo futuro d[eoa]s?\b[^.!?\n]{0,30}\b(chegou|é agora|começa aqui)\b", "«O futuro de X chegou»"),
 ("M6", "BAN", False, r"\b(tudo o que (precisa|necessita)|tudo-em-um|all-in-one|solução (completa|integrada) para tudo)\b", "«tudo o que precisa»"),
 ("M7", "BAN", False, r"\b(sem esforço|em apenas (alguns|poucos|dois|três) cliques|à distância de um clique)\b", "«sem esforço / em poucos cliques»"),
 ("M8", "BAN", False, r"\bjunte-se a (milhares|centenas|milhões)\b|\bmilhares de clientes satisfeitos\b", "prova social vaga"),
 ("M9", "BAN", False, r"\b(mudança de jogo|game[- ]?changer|muda as regras do jogo)\b", "«game-changer»"),
 ("M10", "CAP", False, r"\b(solução|soluções) (inovador[a]s?|completa[s]?|à medida|de ponta)\b|\b(de ponta|de excelência|de referência)\b", "adjetivação vazia"),
 # Vocabulário
 ("V1", "BAN", False, r"\b(alavancar|alavanque|alavancagem d[eao])\b", "calque de «leverage»"),
 ("V1", "BAN", False, r"\b(sinergias?|holístic[oa]s?|paradigmas?|uma infinidade de|tapeçaria|um testemunho d[eoa])\b", "palavra de enchimento"),
 ("V1", "BAN", False, r"\bdesempenha(m)? um papel (crucial|fundamental|vital|essencial|central|decisivo)\b", "«desempenha um papel crucial»"),
 ("V1", "BAN", False, r"\b(no|num) (atual |complexo |vasto )?(panorama|ecossistema)\b|\bnavegar (pel[oa]s?|n[oa]s?) (complex|vast)", "«panorama / ecossistema / navegar»"),
 ("V2", "CAP", False, r"\b(robust[oa]s?|abrangente[s]?|impulsion(ar|e|a)|potenci(ar|e|a)|otimiz(ar|e)|optimiz(ar|e)|elevar|elevado|crucial|vital|pivotal|inovador[a]?s?|revolucionári[oa]s?|transformador[a]?s?|de vanguarda|dinâmic[oa])\b", "vocabulário-tique (2 num parágrafo → reescrever)"),
 ("V3", "CAP", False, r"\b(verdadeiramente|genuinamente|incrivelmente|profundamente|significativamente|simplesmente|literalmente|realmente|fundamentalmente)\b", "intensificador vazio"),
 # Evasivas
 ("H1", "CAP", False, r"\b(pode|poderá|poderão|podem) (potencialmente|eventualmente)\b|\bpoderá (eventualmente )?(ajudar|contribuir)\b", "acumulação de ressalvas"),
 ("H2", "BAN", False, r"\b(especialistas|peritos|analistas) (concordam|afirmam|defendem|garantem)\b|\bestudos (recentes )?(mostram|demonstram|indicam|comprovam)\b|\blíderes (do|de) (setor|mercado|indústria)\b|\bde acordo com (estudos|especialistas)\b", "fonte vaga («estudos mostram»)"),
 ("H3", "BAN", False, r"\b(marca um momento (decisivo|crucial)|redefine (a|o) (categoria|setor|mercado))\b", "inflação de importância"),
 # Tom
 ("T1", "BAN", False, r"\b(ótima|excelente|boa) pergunta\b|\bvamos lá\b|\bsabemos como (é|se sente)\b", "tom de familiaridade fabricada"),
 ("T2", "CAP", False, r"!", "ponto de exclamação (estilo da casa: decisão tua; ban em correspondência formal)"),
 ("T2", "CAP", False, r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50]", "emoji (estilo da casa: decisão tua; ban em correspondência formal)"),
 ("T3", "BAN", False, r"[?!]{2,}", "pontuação múltipla («???», «?!?!», «!!!»)"),
 ("T4", "CAP", False, r"\b(?:[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{3,}\s+){3,}[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{3,}\b", "texto em maiúsculas (4+ palavras seguidas)"),
 ("U1", "CAP", False, r"\b(garanta já|a não perder|não perca|últimas (horas|vagas|inscrições)|vai (mesmo )?(perder|ficar de fora)|decisão mais importante)\b", "urgência de fórmula (só com prazo real e verificável)"),
 ("U2", "CAP", False, r"(?:^|(?<=[.!?]\s))sabia que\b", "gancho «Sabia que…?» (só com número e fonte)"),
 # Contaminação PT-BR (não é «tique de IA», é desvio de variante)
 ("B1", "BR", False, r"\b(você|vocês|usuári[oa]s?|equipes?|planilhas?|celular(es)?|gerenci(ar|amento|e)|cadastr(o|ar|e)|compartilh(ar|e|amento)|baixar|contatos?)\b", "possível PT-BR (PT-PT: tu/o Sr., utilizador, equipa, folha de cálculo, telemóvel, gerir, registo, partilhar, descarregar, contacto)"),
 ("B2", "BR", False, r"\b(estou|estás|está|estamos|estão|estava|estavam|estive)\s+\w+(ando|endo|indo|ondo)\b", "gerúndio progressivo (PT-PT: «estou a fazer»)"),
 ("B3", "BR", False, r"\b(tela|time de|arquivo[s]? (anexo|em pdf|do word)|ônibus|trem)\b", "possível PT-BR (ecrã, equipa, ficheiro, autocarro, comboio)"),
]

def split_paragraphs(t):
    return [p for p in re.split(r"\n\s*\n", t) if p.strip()]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--") or a == "-"]
    formal = "--formal" in sys.argv
    casa = "--estilo-casa" in sys.argv
    if not args:
        print(__doc__); sys.exit(2)
    text = sys.stdin.read() if args[0] == "-" else open(args[0], encoding="utf-8").read()
    rules = [(i, n, f, re.compile(p, I if i not in ("T4",) else re.UNICODE), m) for i, n, f, p, m in R
             if not (formal and f) and not (casa and i == "T2")]
    hits, per_par = [], {}
    pos = 0
    for pi, par in enumerate(split_paragraphs(text)):
        start = text.find(par, pos); pos = start + len(par)
        for (rid, lvl, _, rx, msg) in rules:
            for m in rx.finditer(par):
                ln = text.count("\n", 0, start + m.start()) + 1
                hits.append((ln, rid, lvl, m.group(0).strip()[:60], msg))
                if lvl in ("CAP", "BAN") and rid not in ("P8", "T2"):
                    per_par.setdefault(pi, []).append(rid)
    # frases longas com mais de 2 vírgulas (autoverificação passo 2)
    for ln, line in ([] if formal else enumerate(text.splitlines(), 1)):
        for s in re.split(r"(?<=[.!?])\s+", line):
            if len(s.split()) > 20 and s.count(",") > 2:
                hits.append((ln, "S1", "CAP", s[:60] + "…", "frase longa com mais de 2 vírgulas: verificar acumulação"))
    hits.sort()
    for ln, rid, lvl, frag, msg in hits:
        print(f"L{ln:<4} {lvl:<3} {rid:<4} «{frag}» — {msg}")
    n = {k: sum(1 for h in hits if h[2] == k) for k in ("BAN", "CAP", "BR")}
    stack = [pi + 1 for pi, v in per_par.items() if len(v) >= 2]
    palavras = max(1, len(text.split())); dashes = sum(1 for h in hits if h[1] == "P8")
    print(f"\nTravessões: {dashes} ({100*dashes/palavras:.1f} por 100 palavras)")
    print(f"Resumo: {n['BAN']} BAN · {n['CAP']} CAP · {n['BR']} PT-BR"
          + (f" · parágrafos com 2+ ocorrências (reescrever): {stack}" if stack else ""))
    sys.exit(1 if n["BAN"] else 0)

if __name__ == "__main__":
    main()
