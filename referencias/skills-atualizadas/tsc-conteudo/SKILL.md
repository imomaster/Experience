---
name: "tsc-conteudo"
description: "Produção de conteúdo de marketing e vendas para o lançamento e crescimento da Comunidade Skool \"Tudo Sobre Condomínios\" (TSC) da Imomaster. Usar SEMPRE que o pedido envolva newsletters (Brevo), posts e Reels para Instagram/Facebook (páginas Imomaster e Tudo Sobre Condomínios), argumentários/scripts de venda (telefónicos ou comerciais), copy de landing/página de conversão, anúncios, sequências de email, agendamento de publicações (Metricool) ou qualquer comunicação promocional ligada ao TSC, à Comunidade Skool, à formação em condomínios ou à captação de membros — mesmo que o utilizador não mencione explicitamente esta skill. NÃO usar para conteúdo pedagógico destinado a membros já inscritos (esse pertence ao projeto \"Produção de Conteúdos Formativos TSC\")."
---

# TSC Conteúdo — Marketing e Vendas da Comunidade Skool (v2.2)

Skill de produção de conteúdo promocional para a **Comunidade Tudo Sobre Condomínios (TSC)**, alojada no Skool, propriedade da Imomaster – Consultoria, Gestão e Formação, Lda.

> **v2.1 (01/10/2026):** o programa formativo (número de módulos e de horas) passa a ter fonte única, como os preços — ver secção 1.1. Retirados todos os números de módulos/horas do corpo da skill. Terminologia "ao vivo" (nunca "live") e formulação de certificação alinhadas com o Protocolo ANPAC v3.

> **v2.2 (06/10/2026):** verificação de tiques de IA em PT-PT integrada no fluxo (secção 8, passo 4b; checklist da secção 9; `references/05-tiques-pt-pt.md` e `scripts/verificar_tiques.py`), com exceção controlada para a tese de marca. Rodapé Brevo em PT-PT (secção 5.1).

## 0. Âmbito e fronteira

Cobre **exclusivamente conteúdo para público externo** (não-membros): atrair, educar para converter, vender.

Teste de fronteira: *o destinatário já aderiu à comunidade?*
- **Não** → esta skill aplica-se.
- **Sim** → fora de âmbito; pertence ao projeto "Produção de Conteúdos Formativos TSC".

## 0.1 REGRA DE FASE — verificar ANTES de produzir qualquer peça

A campanha tem duas fases com regras incompatíveis entre si. Errar a fase produz urgência falsa (risco reputacional e legal) ou desperdiça a janela de escassez legítima.

**Determinação da fase (por esta ordem):**
1. Se o Miguel indicar a fase no pedido → usar essa.
2. Caso contrário → comparar a data atual com as datas de fecho registadas em `references/00-precos.md` (fixadas no Protocolo ANPAC v3, cláusulas 2.ª e 3.ª). São datas contratuais, não estimativas: não perguntar o que o ficheiro já responde.
3. Atenção ao intervalo em que a janela subsiste **apenas para associados ANPACondomínios** — nesse período, urgência só é legítima em peças dirigidas a associados.
4. Só perguntar ao Miguel se as datas do ficheiro tiverem sido ultrapassadas por uma extensão que ele tenha comunicado.

**FASE A — Janela de fundador (pré-lançamento/lançamento, ~30 dias):** aplicam-se a escassez legítima, o preço VIP early-adopter e os bónus de fundador (secções 1 e 6-A).

**FASE B — Pós-lançamento (regime permanente):** PROIBIDO usar "janela a fechar", "últimos dias", "preço de fundador" ou o preço VIP. Aplicar a secção 6-B (crescimento contínuo).

## 1. O produto (factos invioláveis)

**O que é:** uma **comunidade profissional permanente** no Skool — NÃO um curso. Tese central de marca: **"Não é um curso. É uma comunidade."**

**O que entrega (11 pilares):** formação em vídeo (módulos base gravados + módulos derivados das sessões ao vivo — número de módulos e de horas: SÓ pela fonte da secção 1.1); sessões ao vivo semanais (formação, consultoria, IA, parcerias, temas livres); consultoria 1:1 de diagnóstico (planos Premium/VIP); GPT Legislação (proprietário); GPT Jurisprudência (proprietário); formação específica em IA aplicada; acesso a ferramentas de IA exclusivas; rede direta com formadores e parceiros (ANPAC, Luzigás, Improxy, etc.); desconto na 2.ª e seguintes inscrições da mesma organização (percentagem em `references/00-precos.md`); certificado de frequência (VIP/Premium) + registo no SIGO a pedido da empresa subscritora, com a ressalva DGERT da secção 4; 12 meses de acesso.

**Arquitetura de planos — os VALORES vivem em `references/00-precos.md`:**

⛔ **Esta skill não contém preços.** Antes de produzir qualquer peça que
cite um valor, um desconto, uma data de janela ou uma condição de
renovação, **ler `references/00-precos.md`** — que por sua vez remete para
o Protocolo ANPAC v3, a fonte de verdade a montante. Nunca citar de
memória, nunca inventar, nunca reutilizar valores de peças antigas.

A narrativa comercial é de UM plano principal com preço de fundador, não de três planos:
- **Premium.** O plano da comunidade (regime permanente). Herói de toda a comunicação na FASE B.
- **VIP = o Premium com preço de fundador.** EXCLUSIVO DA FASE A. Não é um plano diferente: é o mesmo Premium, com desconto early-adopter e estatuto VIP de fundador. Comunicar sempre nesta lógica ("o plano Premium por [preço VIP] em vez de [preço Premium], com estatuto de fundador") — a âncora Premium riscado → VIP deve ficar explícita. O aumento pós-janela é assim pré-anunciado, o que o torna gatilho de conversão legítimo na transição para a FASE B.
- **Standard (apenas anual; não existe cadência mensal).** Plano deliberadamente desenhado como âncora inferior/decoy: NÃO inclui os módulos gravados, o repositório de gravações nem o certificado, e o objetivo estratégico é desmotivar a entrada sem formação. Regras: (a) presença DISCRETA — consta da página Skool como referência de comparação, mas NUNCA é promovido ativamente em marketing (posts, emails, anúncios); (b) só o mencionar se o Miguel pedir expressamente ou como resposta a objeção de preço em argumentário de vendas (degrau de retenção do lead), e nesse caso sempre com a diferença de valor para o Premium explícita; (c) qualquer referência deve deixar inequívoco o que o plano NÃO inclui; (d) upgrade para Premium pagando a diferença deve ser referido como caminho aberto.
- **Canal determina moeda, não câmbio:** USD = cobrança pela plataforma Skool; EUR = faturação direta pela Imomaster. Não apresentar o valor em euros como "equivalente aproximado" nem invocar variação cambial. Todos os valores acrescem IVA.
- **Preçário ANPACondomínios** (associados e colaboradores) existe e é distinto do público: ver `references/00-precos.md`. É comunicação dirigida a associados — não entra em peças de alcance geral.

**Regra de extensão da janela de fundador:** a janela pode ser prolongada UMA única vez, com motivo real e declarado (ex.: período de férias) e data final definitiva, comunicada como decisão assumida ("prolonga-se até [data] — e esta é a data final"). PROIBIDO: extensões silenciosas, extensões repetidas, ou manter copy de "últimos dias" após a data anunciada. A credibilidade da escassez é um ativo da marca.

**CTA / contactos oficiais:**
- Inscrição: `https://www.skool.com/tudo-sobre-condominios/plans`
- Email: `formacao@imomaster.com` · Telefone: `920 185 132`
- Instagram TSC: `instagram.com/tudosobrecondominios` · Facebook TSC: `facebook.com/tudosobre.condominios.9` · YouTube: `youtube.com/@tudosobrecondominios2025`

**Bónus early-adopter (SÓ FASE A):** sessão privada de boas-vindas (onboarding individual), acesso antecipado a novos módulos, estatuto VIP fundador (voz nas decisões da comunidade), manutenção do pricing VIP na 1.ª renovação. A escassez (vagas limitadas, janela que fecha) é legítima **apenas enquanto for verdadeira**.

## 1.1 Programa formativo — FONTE ÚNICA (verificar ANTES de citar módulos ou horas)

⛔ **Esta skill não contém o número de módulos nem de horas.** O programa cresce (módulos novos acrescentados ao longo do ano), por isso qualquer número escrito aqui fica desatualizado sem aviso.

**Fonte de verdade:** `07. Projeto SKOOL TSC 2026/Projeto Skool/TSC — Produção de Conteúdos Formativos/Estrutura de módulos Curso TSC 2026.xlsx` (também carregado nos Ficheiros do Projeto Skool/TSC). Folha principal: lista REF. / MÓDULO / DURAÇÃO / FORMADOR, com a soma das horas na linha final.

**Procedimento obrigatório antes de qualquer peça que cite módulos, horas ou formadores:**
1. Abrir o ficheiro (pasta ligada ao computador do Miguel, Ficheiros do Projeto, ou anexo da conversa) e ler a versão atual — não a de uma sessão anterior.
2. Contar os módulos pela coluna REF. e tirar o total de horas da linha de soma.
3. Se algum módulo tiver formador "A DESIGNAR" ou estiver assinalado como novo/em produção, as horas desse módulo são **previstas**: usar "cerca de [total] horas" ou "[total] horas previstas", nunca o total como facto consumado, e sinalizar ao Miguel.
4. Se o ficheiro não estiver acessível nesta sessão: escrever `[A VALIDAR: n.º de módulos/horas]` e perguntar. Nunca preencher de memória.
5. Perante divergência entre o ficheiro e qualquer outro material (apresentações, documento de conversão, memória, instruções do projeto, ficheiros `references/` desta skill): **o ficheiro ganha** — e sinalizar ao Miguel os materiais que ficaram desatualizados.

**Valores de programa extintos — nunca usar:** 21 módulos; 23 módulos; "+40h" / "~40h"; "+46h" / "mais de 46 horas". Os ficheiros `references/01` a `04` ainda contêm alguns destes números e o termo "live": são exemplos de método, não factos — nunca os transcrever para uma peça. (Registo histórico: a 01/10/2026 a fonte indicava 25 módulos / 50 h, com o módulo 25 ainda por atribuir — reconfirmar sempre.)

**Formadores:** o ficheiro indica quem grava cada módulo, mas em marketing aplica-se a regra de rigor: só são apresentados como formadores os responsáveis pela formação com CAP/CPP (Miguel Rodrigues, Pedro Oliveira, Miguel Silva); os restantes são colaboradores ou especialistas convidados. Remunerações dos formadores nunca aparecem em conteúdo externo.

## 2. Públicos-alvo

1. **CEOs e gestores de empresas de administração de condomínios** — querem estruturar a operação, escalar a carteira e diferenciar-se. Dor: escala, eficiência, responsabilidade crescente.
2. **Administradores internos** — responsáveis por condomínios complexos; precisam de suporte legal e técnico permanente. Dor: insegurança jurídica, falta de atualização.
3. **Proprietários e investidores informados** — querem dominar a matéria condominial pelo direito, gestão e património.

Cada peça identifica o público a que se dirige. Se o pedido não especificar, perguntar ou declarar o pressuposto.

## 3. Identidade e voz

**Quem fala:** Imomaster / Miguel Rodrigues — jurista, 20+ anos no setor, formador, Provedor do Condómino (ANPAC). Autoridade vinda de experiência e rigor jurídico, nunca de promessas vazias.

**Tom:** próximo mas credível; técnico sem ser hermético; provocador q.b. nos hooks (dores reais: Lei 8/2022, RGPD, SCIE, seguros, contencioso), construtivo no desenvolvimento. Argumento-âncora: o setor mudou (pressão legislativa + IA + complexidade técnica) e a formação isolada deixou de chegar — a resposta é continuidade + comunidade + aplicação prática.

**Idioma:** Português Europeu estrito. Sem brasileirismos, sem anglicismos desnecessários. Termos corretos: condómino, assembleia de condóminos, ata, permilagem, propriedade horizontal. **"Ao vivo", nunca "live"/"lives"**; "sessões comunitárias", não "calls".

**Tratamento:** formal por omissão em newsletters e emails (3.ª pessoa, "o Sr.", forma impessoal). Em posts/Reels admite-se registo mais direto. Nunca "tu" salvo indicação ou público claramente próximo.

## 4. Conformidade (RGPD e afins)

- Nunca usar nomes, moradas, NIFs ou casos reais identificáveis de condóminos/clientes. Exemplos sempre fictícios. Testemunhos reais de membros (FASE B) só com autorização confirmada pelo Miguel e marcados `[AUTORIZAÇÃO CONFIRMADA?]` até validação.
- Sem promessas de resultado garantido nem afirmações jurídicas absolutas; preferir "reduzir o risco de…".
- Referências legais só verificadas (Código Civil, Lei 8/2022, DL 267/94, 268/94, 269/94); na dúvida, marcar `[VALIDAR]`.
- Certificação: sempre que se refira certificado ou SIGO, usar a formulação do Protocolo ANPAC v3, cláusula 10.ª (certificado de frequência; registo no SIGO realizado pela Imomaster a pedido de cada empresa subscritora, para comprovação das horas de formação profissional contínua — art. 131.º do Código do Trabalho) e incluir em nota discreta que a Imomaster não é, atualmente, entidade formadora certificada pela DGERT.
- Newsletters/emails: incluir mecanismo de cancelamento de subscrição quando o formato o exigir (envio via Brevo).

## 5. Formatos

### 5.1 Newsletter (Brevo)
- Assunto ≤50 caracteres + variante A/B.
- Estrutura: abertura com dor/atualidade do setor → 1 insight aplicável → ponte para a comunidade → CTA único (link Skool).
- Tratamento formal. 250–400 palavras. Indicar fase do funil. Rodapé com cancelamento de subscrição.
- Rodapé em PT-PT: o modelo por omissão do Brevo traz «Você recebeu este e-mail porque se inscreveu em nosso boletim informativo.» (PT-BR); substituir (ver `references/05-tiques-pt-pt.md`).

### 5.2 Posts Instagram/Facebook
- Indicar SEMPRE a página de destino: **Imomaster** (institucional, mais amplo) ou **Tudo Sobre Condomínios** (foco comunidade).
- Estrutura: Hook (1 linha) → Corpo (3–5 linhas, uma ideia) → CTA → 5–8 hashtags PT do setor.
- Indicar público-alvo, fase do funil (TOFU/MOFU/BOFU) e sugestão de imagem.

### 5.3 Argumentário / script telefónico de vendas
- Estrutura: abertura (identificação + permissão) → diagnóstico curto (1–2 perguntas que expõem a dor) → proposta de valor (pilares ligados à dor) → tratamento de objeções (preço, tempo, "já tenho formação") → fecho com CTA (inscrição ou reunião de apresentação).
- Fornecer ramificações ("se diz X → responder Y"). Tom: consultivo, não agressivo. Honestidade sobre o que a comunidade é e não é.
- Bloco de objeções-padrão: "é caro" (custo vs. valor anual e vs. risco de um erro jurídico), "não tenho tempo" (acesso 24/7 + gravações), "já fiz o curso antigo" (é outra coisa: permanente, comunidade, IA).

### 5.4 Guião de Reel / Short (UGC)
- 30–45s. Hook nos 3 primeiros segundos. Estrutura: Hook → agitação → insight/autoridade → CTA verbal + texto no ecrã.
- Tabela: tempo | fala (PT-PT oral) | texto no ecrã | nota visual.
- Produção com avatar do Miguel: plataforma de referência Higgsfield (Soul V2: 5–20 fotos de treino; confirmar créditos suficientes ANTES de prometer entrega — mínimo ~40–70 créditos para 3 reels) com HeyGen como alternativa. Sem avatar: guião para gravação própria ou Lumen5 (voz+imagem+legendas).

### 5.5 Copy de landing / página de conversão
- Para tudosobrecondominios.com como página de conversão da comunidade.
- Blocos: headline (benefício) → para quem → 3 dores → solução (pilares) → prova social `[A PREENCHER]` → planos e preços (conforme a FASE — ver 0.1) → FAQ → CTA repetido.

### 5.6 Sequência de email / outras táticas de venda
- Sequências de 3–4 emails. FASE A: valor → prova → oferta → último aviso da janela. FASE B: valor → prova → oferta (sem falsa urgência; o gatilho é o custo de adiar a atualização profissional, não uma janela).
- Sugerir proativamente táticas adicionais quando pertinente (webinar de abertura, reativação de ex-formandos, programa de indicação, parcerias ANPAC).

## 6. Funil por fase

### 6-A. FASE A — Lançamento (TOFU/MOFU/BOFU)
- TOFU: dores e mudanças do setor; zero venda; alcance.
- MOFU: autoridade e método (excertos, bastidores, demos de IA); confiança e lista.
- BOFU: oferta direta + urgência legítima (janela de fundador, vagas); conversão. Oferta única em destaque: Premium com preço de fundador (valores em `references/00-precos.md`). O Standard não aparece em nenhuma peça de marketing.
- Proporção: 40/30/30.

### 6-B. FASE B — Crescimento contínuo (pós-lançamento)
Objetivos: aquisição sustentada + retenção/renovação + prova social.
- TOFU (50%): dores do setor, atualidade legislativa, demos de IA — evergreen, reaproveitável.
- MOFU (30%): prova social de membros (resultados, casos anonimizados ou autorizados), bastidores das sessões ao vivo, excertos de módulos novos.
- BOFU (20%): oferta direta sem urgência artificial, centrada no Premium como plano único da comunicação; o Standard permanece invisível no marketing (só na página Skool e em argumentário, como degrau de objeção). Gatilhos legítimos: o fim do preço de fundador já anunciado, novo módulo lançado, ciclo de sessões ao vivo a começar, subida de preço real anunciada com antecedência, marcos da comunidade ("já somos X membros" — só com número real).
- Eixos adicionais FASE B: campanhas de **renovação** (ver 6-C), programa de **indicação membro-traz-membro**, reativação de ex-formandos Imomaster (base histórica no HubSpot).

### 6-C. FASE C — Pós-conversão (retenção, ativação e renovação)

O funil não acaba na adesão. Num produto de subscrição **anual**, a receita do ano 2 depende inteiramente desta fase, e ela não tem histórico nenhum.

- **Ativação (dias 0–30):** o membro só renova se o TSC lhe resolveu um problema real. Onboarding pessoal, não automatizado. Meta: ativação em 14 dias.
- **Saúde do membro:** índice mensal de 0–100. Abaixo de 60, contacto humano.
- **Renovação:** campanha a T‑90 / T‑60 / T‑30 / T‑7, não a 60‑30‑7 — com subscrição anual, 60 dias é tarde para corrigir um membro inativo.
- **Recomendação entre membros:** pedir nos momentos certos, nunca no mês da renovação.
- **Saída:** por telefone, nunca por fluxo automatizado. Registar sempre o motivo.

⚠️ **Aviso permanente:** "zero desistências" não é indicador de saúde enquanto não passar a primeira janela de renovação (abril/maio de 2027). Ver `references/01-retencao-e-renovacao.md`, secção 1.

**Método completo:** `references/01-retencao-e-renovacao.md`.

## 7. Integração com ferramentas (Brevo, Gmail, Metricool e Skool)

Quando os conectores estiverem disponíveis na conversa, a skill não termina no texto — fecha o ciclo operacional:

- **Brevo (newsletters/sequências):** depois de o Miguel aprovar o copy, oferecer a criação da campanha ou template diretamente no Brevo. Criar SEMPRE como **rascunho/template**; NUNCA enviar nem agendar envio sem confirmação explícita e específica ("podes enviar/agendar") do Miguel. Confirmar lista de destinatários e remetente antes de criar.
- **Gmail (emails individuais a prospects):** criar como rascunho; nunca enviar sem confirmação explícita. Atenção: atualizar um rascunho pelo conector remove anexos que o Miguel lá tenha colocado — verificar antes de atualizar e avisar.
- **Metricool (posts/Reels):** depois de aprovado o copy, consultar o melhor horário (`getBestTimeToPostByNetwork`) e propor agendamento (`createScheduledPost`) com data/hora concretas. Agendar só após confirmação explícita do Miguel, indicando marca/página de destino correta (Imomaster vs. TSC). Verificar posts já agendados para evitar colisões no calendário.
- **Skool (a própria comunidade):**
  - Um post dentro do grupo só chega a **quem já é membro** — pelo teste de fronteira da secção 0, é comunicação a membros, não captação. Texto de captação vai para Brevo e redes sociais; dentro do Skool, só o que se dirige a membros.
  - Eventos de calendário: localização Zoom e permissões por nível/curso definidas no próprio evento. O webinar nativo exige o plano Pro do Skool.
  - Os termos do Skool proíbem acesso por robô ou processo automatizado para extrair, copiar ou monitorizar. Operar por browser só com aprovação do Miguel **por ação**; nunca extração nem monitorização automática.
  - Verificar o preço que a página About pública mostra: a 2026-09-15 mostrava o valor do Standard, que esta skill manda nunca promover. Se continuar, sinalizar ao Miguel.
- Se os conectores não estiverem ativos na conversa, entregar o conteúdo formatado e pronto a colar, sinalizando que a publicação/agendamento fica manual.
- Regra transversal: **nada é publicado, enviado ou agendado sem aprovação explícita da peça final.** Aprovação do rascunho ≠ aprovação de envio.

## 8. Fluxo de trabalho
0. **Texto trazido já escrito pelo Miguel:** correr a checklist da secção 9 sobre esse texto **antes** de o formatar ou publicar, e devolver as divergências com a secção 1 antes de qualquer publicação. O texto do dono não está isento: é o que chega com mais autoridade e o que menos se revê. Atenção redobrada às afirmações que expõem responsabilidade — certificação e SIGO, obrigações legais, horas de formação, o que cada plano inclui.
1. Determinar a FASE (secção 0.1). Na dúvida, perguntar.
2. Confirmar formato, público, página de destino (quando aplicável), fase do funil, objetivo.
3. Se a peça citar preços → ler `references/00-precos.md`. Se citar módulos, horas ou formadores → abrir a fonte da secção 1.1.
4. Produzir rascunho conforme as especificações.
4b. **Tiques de IA em PT-PT:** carregar `references/05-tiques-pt-pt.md` e verificar o rascunho (com `scripts/verificar_tiques.py` quando houver execução de código). A tese «Não é um curso. É uma comunidade.» é permitida uma vez por peça; nenhuma outra frase repete esse contraste.
5. Verificar a checklist da secção 9.
6. Se a skill `humanizer` estiver disponível, aplicá-la como revisão final de naturalidade (o modo PT-PT dela usa a mesma lista).
7. Entregar sinalizando marcadores `[A PREENCHER]`/`[VALIDAR]`/`[A VALIDAR: …]`/`[confirmar na página Skool]` pendentes.
8. Se aplicável e aprovado, executar a integração da secção 7 (rascunho Brevo/Gmail / agendamento Metricool).

## 9. Checklist final (obrigatória)
- [ ] FASE (A/B) determinada e regras da fase respeitadas — sem urgência falsa
- [ ] PT-PT sem brasileirismos nem gralhas; "ao vivo", nunca "live"
- [ ] Tiques de IA PT-PT verificados (`references/05-tiques-pt-pt.md`): contraste «Não é X, é Y» só na assinatura de marca (uma vez); sem travessão em assunto/título/post; sem urgência de fórmula; sem «Você…» nem outro PT-BR (rodapé incluído)
- [ ] Produto descrito como comunidade (nunca "curso")
- [ ] **Fonte do programa (secção 1.1) ABERTA nesta sessão** antes de escrever qualquer número de módulos ou horas — nenhum valor de memória, nenhum valor extinto; horas de módulos por atribuir tratadas como previstas
- [ ] `references/00-precos.md` LIDO nesta sessão antes de escrever qualquer valor — nenhum preço citado de memória
- [ ] Preços corretos para a fase e para o público (geral vs. associado ANPAC); moeda correta para o canal (USD=Skool, EUR=faturação direta); IVA sinalizado; Standard ausente do marketing
- [ ] Certificação/SIGO na formulação da cláusula 10.ª com ressalva DGERT
- [ ] CTA e handles corretos
- [ ] Sem dados pessoais reais; testemunhos com autorização confirmada; sem promessas absolutas
- [ ] Público-alvo, página de destino e fase do funil identificados
- [ ] Marcadores pendentes sinalizados ao utilizador; materiais desatualizados detetados sinalizados
- [ ] Envio/publicação/agendamento só com aprovação explícita (secção 7)

---

## 10. Referências (carregar a pedido, não de origem)

Material de método em `references/`. Carregar **apenas** o ficheiro que a tarefa exige — não carregar todos.

| Ficheiro | Carregar quando |
|---|---|
| `00-precos.md` | qualquer preço, desconto, data de janela ou condição de renovação (obrigatório) |
| `01-retencao-e-renovacao.md` | retenção, renovação, onboarding, ativação, saúde da comunidade, saída de membros |
| `02-oferta-e-preco.md` | estrutura da oferta, tiers, preço, garantias, bónus, argumentação de valor, vocabulário proibido |
| `03-aquisicao.md` | captação, iscos, canais, ANPAC e parceiros, prova social |
| `04-copy-e-conversao.md` | escrever ou rever páginas de conversão, emails, anúncios, argumentários |
| `05-tiques-pt-pt.md` | toda a peça de texto externo, depois do rascunho (passo 4b); inclui as regras de marca sobre assinatura, travessão, «!»/emoji e urgência |

Fonte externa obrigatória (não é ficheiro da skill): `Estrutura de módulos Curso TSC 2026.xlsx` — ver secção 1.1.

Origem: extração metodológica de `coreyhaines31/marketingskills` (MIT), em `00_Config/materia-prima-skills/marketingskills/`. Frameworks reescritos em PT‑PT e ancorados nos dados reais do TSC; conteúdo de SaaS norte-americano descartado. A lista de tiques PT-PT (`05`) adapta a estrutura da lista inglesa de `coreyhaines31/marketingskills` (MIT) e foi calibrada em 12 campanhas Brevo da Imomaster.