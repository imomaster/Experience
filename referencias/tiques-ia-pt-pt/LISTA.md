# Tiques de IA em português europeu — lista de trabalho (v0.1, 2026-10-05)

Adaptação ao PT-PT da lista inglesa de `coreyhaines31/marketingskills` (copywriting, MIT), reescrita para a forma como o português se comporta, não traduzida. Os padrões estruturais (P) passam quase intactos para português; os de vocabulário e fórmulas (A, M, V) são específicos da língua e foram refeitos. A secção **B** (PT-BR) não existe na lista inglesa: é um problema próprio de quem escreve em PT-PT com modelos treinados sobretudo em português do Brasil.

**Como usar:** `python3 verificar_tiques.py texto.txt` (ou `--formal` para cartas e peças jurídicas). O verificador aponta; não decide. Cada ocorrência resolve-se **reescrevendo a partir dos factos** (número, nome, mecanismo, passo concreto), nunca trocando por sinónimo, que cria um tique novo.

**Níveis:** BAN = tique mesmo uma só vez. CAP = tolerável uma vez, tique se repetido; duas ocorrências no mesmo parágrafo → reescrever o parágrafo.
**Âmbito:** copy, newsletters, posts, anúncios, páginas. Em correspondência formal e peças jurídicas aplica-se só o que está marcado «sempre».

## P — Estruturais (mais graves que qualquer lista de palavras)
| Id | Nível | Padrão | ✗ | ✓ |
|---|---|---|---|---|
| P1 | BAN | **Contraste «Não é X, é Y»**; variantes «Não se trata de X, trata-se de Y», «Mais do que X, é Y», «Não só X, mas também Y» (esta, CAP) | Não é apenas um software, é uma revolução na administração. | Reduz de duas tardes para 20 minutos a preparação de uma convocatória. |
| P2 | BAN | **Lista de negações** «sem X, sem Y, sem Z», «zero X» | Sem papel, sem folhas de cálculo, sem dores de cabeça. | As atas ficam no sistema e chegam aos condóminos em 24 horas. |
| P3 | CAP | **Rematar com gerúndio**: «…, garantindo / permitindo / assegurando / proporcionando…» | Sincroniza a agenda, garantindo que nada falha. | Sincroniza a agenda. As convocatórias saem na data certa. |
| P4 | BAN | **Pergunta retórica + resposta** | O resultado? 3 vezes mais rápido. | A preparação passa de 4 horas para 80 minutos. |
| P5 | BAN | **Revelação com dois pontos** «O segredo:», «A melhor parte:» | A melhor parte: aprende consigo. | Aprende com cada correção que faz. |
| P6 | CAP | **Fragmentos em bateria** (máx. um por secção) | Simples. Rápido. Feito. | Uma frase com um facto. |
| P7 | CAP | **Três por reflexo** (máx. um por secção) | Rápido, seguro e escalável. | O número ou prazo concreto que isso representa. |
| P8 | CAP/BAN | **Travessão longo** — BAN em título, anúncio, assunto de email, post; máx. 1–2 por página em texto longo | Não é uma ferramenta — é uma equipa. | Ponto, vírgula, dois pontos ou parênteses. |
| P9 | CAP | **Ritmo uniforme** (todas as frases com 12–18 palavras, todos os parágrafos iguais) | — | Variar de propósito; secção de duas linhas se for o que há. |
| P10 | CAP | **Fugir a «é» e «ter»**: «constitui», «representa», «assume-se como», «ostenta» | Constitui uma plataforma central. | É a plataforma onde estão todos os contratos. |
| P11 | CAP | **Sujeito abstrato** «A plataforma permite/capacita…» | A solução capacita equipas. | A sua equipa fecha o mês sem pedir um ficheiro a ninguém. |

## A — Aberturas, fechos e preparações (BAN, salvo indicação)
| Id | Padrão | Em vez disso |
|---|---|---|
| A1 | **Abertura de era**: «Num mundo cada vez mais digital/competitivo», «Nos dias de hoje», «Na era digital», «No atual panorama/contexto», «Em constante evolução» (CAP) | Abrir pelo problema do cliente |
| A2 | **Falsa alternativa**: «Quer seja X ou Y», «Seja um… ou um…» | Dizer a quem se destina |
| A3 | «**Imagine**…» | Mostrar o antes e o depois reais |
| A4 | **Pigarro**: «A verdade é que», «Vamos ser honestos», «A questão é simples». CAP, e **sempre** idiomático em peça jurídica: «Convém/Importa referir/salientar/sublinhar», «É importante destacar» | Cortar; se a afirmação não se aguenta sozinha, falta-lhe prova |
| A5 | **Anúncio**: «Neste artigo, vamos explorar», «Vamos mergulhar», «Mergulhe» (calque de *dive in*) | Começar pelo conteúdo |
| A6 | **Fecho-resumo** (CAP; **sempre** legítimo em memorandos e peças): «Em suma», «Em conclusão», «No final do dia» (calque), «Em última análise» | Terminar no último ponto concreto ou no apelo à ação |
| A7 | **Remate pseudo-profundo**: «Porque o futuro não espera.», «E isso muda tudo.» | Cortar |
| A8 | **Transições de enchimento** (CAP): «Além disso,», «Adicionalmente,», «Acima de tudo,» | Apagar; quase sempre a frase funciona sem elas |

## M — Frases de marketing (BAN)
«**Diga adeus a** X» · «**Desbloqueie** o potencial / o poder de X» · «Leve X **para o próximo nível**» · «**Transforme a forma como** trabalha» / «Revolucione» / «Reinvente» · «**O futuro de X chegou**» · «**Tudo o que precisa** para X» / «tudo-em-um» · «**Sem esforço**» / «em apenas alguns cliques» · «**Junte-se a milhares** de clientes satisfeitos» · «**Mudança de jogo**» (*game-changer*). CAP: «solução inovadora / completa / à medida», «de ponta», «de excelência», «de referência».
**Em vez disso:** o resultado com número («3 passos, cerca de 4 minutos»), o cliente real e o gatilho, a contagem ou o nome verdadeiros.

## V — Vocabulário
- **BAN:** *alavancar* (calque de *leverage*), *sinergia(s)*, *holístico*, *paradigma*, *uma infinidade de*, *tapeçaria*, *um testemunho de*, «**desempenha um papel crucial/fundamental/vital**», «no (atual) **panorama**», «no **ecossistema**», «**navegar** pelo complexo mundo de».
- **CAP** (duas num parágrafo → reescrever): *robusto, abrangente, impulsionar, potenciar, otimizar/optimizar, elevar, crucial, vital, inovador, revolucionário, transformador, de vanguarda, dinâmico*.
- **CAP, intensificadores vazios:** *verdadeiramente, genuinamente, incrivelmente, profundamente, significativamente, simplesmente, literalmente, realmente, fundamentalmente*.
- Trocar a palavra pela coisa que ela escondia: «robusto» → «99,9 % de disponibilidade em dois anos».

## H, T e F — Evasivas, tom, formatação
- **H1 CAP** acumulação de ressalvas: «pode potencialmente ajudar a eventualmente reduzir». **H2 BAN** fonte vaga: «especialistas concordam», «estudos mostram», «líderes do setor», «de acordo com estudos recentes»: citar a fonte ou cortar. **H3 BAN** inflação: «marca um momento decisivo», «redefine o setor».
- **T1 BAN** familiaridade fabricada: «Ótima pergunta!», «Vamos lá», «Sabemos como se sente». **T2 BAN** pontos de exclamação e emojis (copy e correspondência formal).
- **F CAP:** etiqueta a negrito em todos os pontos de uma lista; todos os pontos a começar por «Garante… / Permite… / Proporciona…»; Títulos Em Maiúsculas Todos; títulos de secção «O quê / Porquê / Como».

## B — Contaminação PT-BR (não é tique de IA; é desvio de variante)
O verificador marca como `BR`; confirmar sempre no contexto, porque algumas palavras existem em PT-PT com outro sentido (ex.: «arquivo», «senha»).
| PT-BR | PT-PT |
|---|---|
| você(s) | tu / o Sr., a Sr.ª / V. Exa. (conforme o registo) |
| usuário | utilizador |
| equipe, time | equipa |
| planilha | folha de cálculo |
| celular | telemóvel |
| tela | ecrã |
| arquivo (informático) | ficheiro |
| baixar | descarregar |
| compartilhar | partilhar |
| gerenciar | gerir |
| cadastro | registo / inscrição |
| contato | contacto |
| «está fazendo» (gerúndio progressivo) | «está a fazer» |

## Regras de reescrita
1. Reescrever a partir dos factos; sinónimo novo = tique novo. 2. **Teste da especificidade:** cada afirmação leva número, nome, mecanismo ou ação concreta. 3. **Teste da troca:** se a frase serviria no site do concorrente, reescrever. 4. **Não inventar para limpar:** «líder do setor» não se troca por uma estatística inventada; marcar `[NEED: prova]`. 5. **Variar as correções:** se todo o «não é X, é Y» passa a «, porque…», é tique novo. 6. **Respeitar o registo:** uma frase formal com afirmação específica está bem; não achatar um tom institucional em *startup*.

## Estado de validação — ler antes de confiar
- **Origem:** estrutura e níveis vêm da lista inglesa (com fontes citadas por ela: Wikipedia «Signs of AI writing», estudos de vocabulário em inglês). **Os padrões e exemplos PT-PT são adaptação minha**, a partir de como o português reproduz esses mecanismos e de calques frequentes (*leverage → alavancar*, *dive in → mergulhar*, *at the end of the day → no final do dia*). **Não foram validados contra um corpus de português** nem contra textos de IA em PT-PT medidos. `[A VALIDAR]`
- **Testes feitos (2026-10-05):** (1) amostra de 5 linhas com tiques deliberados: o verificador marca 8 ocorrências BAN, incluindo as duas que o verificador inglês deixava passar («Não é apenas… é…» e «Num mundo cada vez mais digital»); (2) texto limpo de copy: 0 ocorrências; (3) amostra PT-BR: 10 marcas; (4) carta formal: 2 CAP, 0 com `--formal`; (5) falsos positivos nos teus 4 textos PT (skills tsc-conteudo, tsc-membros, parecer-provedor-condominio, impugnar-contraordenacao): quase tudo travessões e frases longas (ruído de texto de instruções, não de copy); sobram 6 BAN em tsc-conteudo, 1 em cada uma das outras duas e 0 em tsc-membros, em frases de instrução onde o padrão é intencional («Sem brasileirismos, sem anglicismos…»).
- **Não testado:** em copy real tua (newsletters Brevo, posts Metricool, páginas da TSC). Sem isso, a taxa real de falsos positivos e de tiques por apanhar é desconhecida. Calibrar com 5–10 textos reais antes de usar como filtro.
- **Limites do método:** expressão regular só apanha o que foi previsto; não deteta tiques de ritmo (P9), nem «sujeito abstrato» (P11) nem sinónimos novos. A leitura em voz alta continua a ser o teste final.
