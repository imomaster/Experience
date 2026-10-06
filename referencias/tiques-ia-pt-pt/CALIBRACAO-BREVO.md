# Calibração do verificador com copy real (Brevo) — 2026-10-06

**Autorização:** Miguel Rodrigues, leitura de campanhas enviadas no Brevo (só conteúdo das campanhas; nenhum dado de destinatários).
**Âmbito lido:** 12 das 28 campanhas enviadas (ids 6, 13, 17, 19, 24, 25, 29, 30, 31, 32, 33, 34) + 21 assuntos (truncados a 70 caracteres pela listagem). **Não lidas:** as outras 16 (ids 5, 8–11, 14–16, 18, 20–23, 27, 28, 35). O corpus (texto das campanhas) **não** está neste repositório; ficou fora por ser conteúdo teu e por eu não saber se o repositório é público. Blocos idênticos entre e-mails (listas repetidas) foram transcritos uma vez; rodapés testados à parte.
**Proveniência:** não sei quem escreveu cada e-mail nem se houve IA. A divisão é só por data: 2024-06 a 2025-10 (6 e-mails) e 2026-06 a 2026-09 (6 e-mails, série da Comunidade TSC).

## Resultado por e-mail (`--formal`)
| email | data | palavras | P1 contraste | P8 travessão | T2 «!»/emoji | T3 «???» | outros BAN/CAP |
|---|---|---|---|---|---|---|---|
| e06 | 2024-06 | 422 | 0 | 0 | 1 | 0 | 4 |
| e13 | 2025-03 | 47 | 0 | 0 | 1 | 0 | 1 |
| e17 | 2025-04 | 74 | 0 | 0 | 2 | 0 | 0 |
| e19 | 2025-05 | 255 | 1 | 1 | 9 | 0 | 5 |
| e24 | 2025-09 | 336 | 0 | 0 | 7 | 2 | 3 |
| e25 | 2025-10 | 601 | 0 | 4 | 7 | 1 | 2 |
| e29 | 2026-06 | 362 | 2 | 4 | 0 | 0 | 1 |
| e30 | 2026-09 | 562 | 1 | 7 | 2 | 0 | 0 |
| e31 | 2026-09 | 310 | 2 | 5 | 1 | 0 | 0 |
| e32 | 2026-09 | 349 | 3 | 5 | 0 | 0 | 0 |
| e33 | 2026-09 | 333 | 0 | 1 | 6 | 2 | 3 |
| e34 | 2026-09 | 334 | 0 | 2 | 7 | 2 | 2 |

**Por fase:** 2024–2025: 1 735 palavras, P1 = 1 (0,06 por 100 palavras), travessões = 5 (0,29), «!»/emoji = 27, «???» = 3. 2026: 2 250 palavras, P1 = 8 (0,36), travessões = 24 (1,07), «!»/emoji = 16, «???» = 4.

## O que isto diz
1. **A tua copy não tem os tiques «clássicos» de IA.** Não há aberturas de era, «diga adeus», «desbloqueie», vocabulário-tique nem PT-BR de IA. Nos 12 e-mails sobram: contraste «Não é X, é Y» (9), travessão, e a tua marca de casa: «!», emojis (👉 🔹 📆 📌) e «???».
2. **Há deriva de estilo em 2026:** contraste e travessões sobem de forma clara (P1: 0,06 → 0,36 por 100 palavras; travessão: 0,29 → 1,07). É compatível com redação assistida por IA, **mas não prova autoria**. Os dois e-mails de 16 e 18 de setembro (e33, e34) têm o perfil oposto: mais pontuação e maiúsculas, menos travessões.
3. **O verificador falhava um caso real:** «Não é um curso. É uma comunidade.» (contraste entre frases) passava. Regra corrigida e testada. Acrescentei também «é o contrário», «faz outra coisa», «é a diferença entre», T3 (pontuação múltipla), T4 (maiúsculas) e U1/U2 (urgência e «Sabia que»).
4. **«!» e emoji deixaram de ser BAN:** representavam 43 das ocorrências e são escolha de estilo tua, não tique. Passaram a CAP, com `--estilo-casa` para os ignorar. É decisão tua se funcionam com este público; não tenho dados de desempenho que o provem nem desmintam.
5. **Assuntos (copy curta):** 1 BAN («Não lhe vamos dar uma ferramenta. Vamos construí-la consigo») e 4 U1 (urgência de fórmula: «Vai mesmo ficar de fora?», «Últimas horas», «Últimas Inscrições»). Esta amostra é pequena e os assuntos estavam truncados.

## Achados reais nos teus e-mails (fora do que o verificador mede; confirmar antes de agir)
- **Rodapé PT-BR em todos os 12 e-mails:** «**Você** recebeu este e-mail porque se inscreveu em **nosso** boletim informativo.» (nos e-mails de 2025-09 e 2025-10 já «no nosso», mas com «Você»). Corrige-se uma vez, no modelo ou no rodapé da conta Brevo. Não o fiz: não tenho ferramenta para editar o rodapé da conta. Na e13 há também «você» no corpo do texto.
- **Gralhas:** «Rede fixa **nacioal**» (rodapé das campanhas de 2025-03 e 2025-04); «INTELIGÊNCIA **ARTIFICAL**» (2024-06); «serão muito **valiosas**» (concordância: «contributo e experiência … valiosos»); «por em prática» (pôr). A campanha de 2024-06 mistura ortografia anterior ao AO90 («sector», «actuação», «OBJECTIVA») com a posterior usada em 2025 («setor», «atividade»).
- **Urgência móvel (série TSC):** em 2026-06 «condição que não se vai repetir», «janela de fundador encerra a 31 de Julho»; em 2026-09 novo prazo (18 de setembro); e a e34 diz «Hoje é o último dia» no título e «O prazo terminou, mas ainda vou dar o fim de semana» no corpo. Se o prazo se desloca, a próxima mensagem de escassez perde credibilidade. Decisão tua, `[A VALIDAR]` se houve razão comercial para cada extensão.
- **Estatística sem fonte:** «40 % das empresas que se inscrevem connosco voltam com novos colaboradores» (e19, e24, e25). `[A VALIDAR]` se tens suporte documental.
- **Números que mudam em dois dias:** «46 horas, 23 módulos» (e30–e33) → «50 horas, 25 módulos» (e34). Pode ser atualização real; confirmar.
- **Destinatário:** a e33 abre com «Caro(a) Membro da Comunidade» mas foi enviada também à lista geral (lista 5, ~7 300 contactos), não só a membros.

## Limites
Amostra de 12/28 e de uma só voz/canal (e-mail). Sem posts, Reels, páginas Skool nem WhatsApp. Sem dados que relacionem tiques com desempenho: não afirmo que remover um tique melhora cliques. O verificador continua a apanhar só o que foi previsto.
