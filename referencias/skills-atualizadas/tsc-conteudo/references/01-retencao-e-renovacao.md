# Retenção e renovação — TSC

> Referência da skill `tsc-conteudo`. Carregar quando o trabalho for sobre
> manter membros, renovações, reativação ou saúde da comunidade.
> Método adaptado de `marketingskills/churn-prevention`, `onboarding` e
> `community-marketing` (Corey Haines, MIT). Enquadramento, números e
> táticas reescritos para o TSC.

---

## 1. O facto que muda tudo: o TSC não tem churn — tem um precipício

À data desta referência (agosto de 2026) o TSC tem **20 subscritores, todos
anuais, zero desistências**. Isso não é retenção. É aritmética.

A comunidade lançou em **meados de abril de 2026**. Uma subscrição anual não
dá ao membro nenhuma oportunidade de sair durante doze meses. A taxa de
cancelamento é zero porque **ainda não houve nenhuma decisão de renovar**.

Consequência operacional: em vez de perdas dispersas ao longo do ano, que
avisam com antecedência e se corrigem, o TSC enfrenta uma **decisão única e
simultânea de toda a base em abril/maio de 2027**. Se a proposta de valor não
estiver demonstrada nessa altura, não se perde 5% ao mês — perde-se metade da
comunidade numa semana.

**Regra:** nunca apresentar "zero desistências" como indicador de saúde num
produto de subscrição anual no primeiro ano. É ausência de dados, não
ausência de problema. Sempre que o número aparecer numa análise, num pitch a
parceiros ou numa projeção financeira, qualificá-lo com a data da primeira
janela de renovação.

**Corolário para o modelo financeiro:** ⚠️ a projeção de ~€56.865 a 12 meses foi calculada sobre a grelha de preços anterior e está desatualizada — recalcular sobre `00-precos.md` antes de a citar. A projeção a 12 meses
assume aquisição. A receita do ano 2 assume renovação, e essa não tem
histórico nenhum. Tratar a taxa de renovação como **hipótese por validar**,
nunca como pressuposto.

---

## 2. Sinais de risco no Skool

O Skool não expõe telemetria de produto como um SaaS. Os sinais observáveis
são de participação, e chegam com menos antecedência. Compensa-se com
observação manual — a 20, 50 ou 134 membros isso é viável e deixa de o ser
muito depois.

| Sinal | Risco | Antecedência típica |
|---|---|---|
| Não abre nenhum módulo há 30 dias | Alto | 2–4 meses |
| Nunca concluiu nenhum módulo do Premium | Crítico | desde o início |
| Falta a 3 lives seguidas sem ver a gravação | Alto | 2–3 meses |
| Nunca publicou nem comentou no fórum | Alto | persistente |
| Deixou de abrir a newsletter (Brevo) | Médio | 2–6 semanas |
| Publicou uma dúvida que ficou sem resposta | Crítico | imediato |
| Deixou de aparecer nas calls comunitárias | Médio | 1–2 meses |
| Mudou de empresa ou de funções | Alto | imediato |

O sinal mais grave da lista é **a pergunta sem resposta**. Num produto de
comunidade, uma dúvida ignorada destrói a premissa da compra — e não deixa
rasto em métrica nenhuma.

---

## 3. Índice de saúde do membro

Pontuação de 0 a 100, calculada manualmente ou em folha, uma vez por mês.
Só se aplica ao Premium: no Standard os sinais reduzem-se à participação no
fórum.

```
Saúde = consumo de módulos      × 0,30
      + presença em lives        × 0,25
      + participação no fórum    × 0,20
      + abertura de comunicações × 0,15
      + antiguidade e contexto   × 0,10
```

| Pontuação | Estado | Ação |
|---|---|---|
| 80–100 | Saudável | Candidato a testemunho, a caso de estudo e a 2.ª inscrição da empresa |
| 60–79 | A precisar de atenção | Mensagem pessoal com o módulo mais útil para o caso dele |
| 40–59 | Em risco | Contacto direto do Miguel, não automatizado |
| 0–39 | Crítico | Telefonema. A esta pontuação, o email não é lido |

**Não automatizar abaixo dos 60.** O TSC vende proximidade a um universo
profissional pequeno onde toda a gente se conhece. Uma sequência automática
mal calibrada aos 40 pontos é pior do que o silêncio.

---

## 4. Ativação: o momento em que o membro percebe porque pagou

O indicador que melhor prevê renovação não é o consumo total de conteúdo — é
**o primeiro momento em que o TSC resolveu um problema concreto do trabalho
do membro**.

Para o TSC, esse momento é um destes:

1. Levou uma dúvida real à live e saiu com resposta aplicável.
2. Usou uma peça, minuta ou ferramenta da comunidade num condomínio seu.
3. Obteve no fórum uma resposta que lhe poupou uma consulta jurídica.

Nenhum destes é "viu os 21 módulos". Um membro pode ver tudo e não renovar;
um membro que resolveu um problema real na primeira semana renova.

**Métricas a acompanhar:**

- % de membros que atingem a ativação nos primeiros 30 dias
- Número de dias até à ativação
- % que publica no fórum nos primeiros 7 dias
- % que assiste ou vê a gravação da primeira live após aderir

**Meta operacional:** ativação em **14 dias**. Acima de 30 dias, tratar como
membro em risco desde o primeiro mês, independentemente da pontuação.

---

## 5. Onboarding dos primeiros 30 dias

O objetivo não é mostrar a plataforma. É **provocar a ativação**.

| Momento | Ação | Responsável |
|---|---|---|
| Imediato | Mensagem pessoal de boas-vindas com **uma** pergunta: "qual é o problema que tens em mãos esta semana?" | Miguel |
| Dia 1 | Encaminhar para o módulo ou peça que responde a esse problema concreto — não para o índice | Miguel |
| Dia 3 | Convite nominal para publicar a dúvida no fórum | Equipa |
| Dia 7 | Se não publicou: contacto direto, sem automatismo | Miguel |
| Dia 14 | Convite para a próxima live com um ponto da agenda dedicado ao caso dele | Equipa |
| Dia 30 | Balanço: o que resolveu, o que falta. Registar a resposta — é matéria-prima de testemunho e de renovação | Miguel |

**Não usar percurso de onboarding genérico.** A 20 membros, cada entrada
justifica uma mensagem escrita à mão. Quando isso deixar de ser possível é
sinal de escala, não de eficiência.

---

## 6. Campanha de renovação — abril/maio de 2027

Começa **90 dias antes** da data de renovação de cada membro, não no mês.

**T-90 · Balanço de valor.** Mensagem individual com o que aquele membro
concretamente fez: módulos concluídos, lives em que participou, dúvidas
respondidas, peças que utilizou. Sem oferta, sem venda. Só o registo.
Se o balanço for pobre, é aí que se descobre — com 90 dias para corrigir.

**T-60 · Recuperação dos inativos.** Para quem tiver saúde abaixo de 60:
contacto do Miguel a propor um objetivo concreto para os dois meses
seguintes. É a última janela útil de recuperação.

**T-30 · Renovação com o que vem a seguir.** Comunicar a renovação junto com
o que está planeado para o ano seguinte — módulos novos, formadores novos,
certificação DGERT se entretanto avançar. Renova-se sobre o futuro, não
sobre o passado.

**T-7 · Confirmação.** Lembrete simples com a data e o valor. Sem pressão.

**T+1 · Quem não renovou.** Telefonema, não email. Perguntar porquê e
registar a resposta. Num universo de 20 a 134 pessoas, cada saída explicada
vale mais do que qualquer inquérito.

**Fixar já a data.** As primeiras renovações caem entre meados de abril e
maio de 2027. O T-90 arranca, portanto, em **meados de janeiro de 2027**.

---

## 7. Ofertas de retenção — o que se pode e o que não se deve

| Oferta | Usar no TSC? |
|---|---|
| **Descontar 20–30%** | Com muita reserva. O TSC já tem uma grelha de preços com vários degraus (público, associado ANPAC, 2.ª inscrição — ver `00-precos.md`). Mais um preço de retenção ensina a comunidade a ameaçar sair |
| **Descer para o Standard** | **Sim — é a melhor.** A descida Premium → Standard (valores em `00-precos.md`) mantém o membro na comunidade, preserva a relação e deixa porta aberta para voltar ao Premium |
| **Suspender a subscrição** | Não se aplica com clareza a subscrição anual. Ignorar |
| **Desbloquear algo não usado** | Sim. Sessão individual com o Miguel, ou acesso antecipado a módulo novo. Custa tempo, não margem |
| **Contacto pessoal** | Sim, para todos. A 134 membros ainda é comportável, e é o diferenciador face à ESAI e ao ISAG |

**Regra de preço:** nunca conceder desconto de retenção sem contrapartida
verificável — testemunho, caso de estudo, ou apresentação de um colega.
É a mesma posição negocial de sempre: o desconto ancora-se em algo
verificado, nunca em promessa.

---

## 8. Recomendações entre membros

O canal de aquisição do TSC é a ANPAC e o boca-a-boca de um setor pequeno.
Um programa de recomendação encaixa naturalmente, e já existe metade dele:
**50% de desconto na 2.ª inscrição da mesma empresa**.

**Momentos em que se pede** — nunca fora destes:

- Logo a seguir a uma live em que o membro participou ativamente
- Quando o membro escreve espontaneamente que algo lhe foi útil
- No balanço dos 30 dias, se a resposta for positiva
- Nunca no mês de renovação — mistura dois pedidos e enfraquece ambos

**Incentivo:** desconto na própria renovação por cada membro trazido, com
teto. Nunca comissão em dinheiro: transforma colegas em vendedores e queima
credibilidade num setor onde todos se conhecem.

---

## 9. Saúde da comunidade — indicadores semanais

- **Rácio de participação:** % de membros que entram numa semana. Abaixo de
  20% a comunidade está a morrer, mesmo com as subscrições pagas.
- **Publicações de membros novos:** % que publica nos primeiros 7 dias.
- **Taxa de resposta:** % de publicações que recebem pelo menos uma resposta.
  **Meta: 100%.** Nenhuma pergunta fica sem resposta em 24 horas.
- **Conteúdo não produzido pela equipa:** % de publicações que não são do
  Miguel nem dos formadores.
- **Membros silenciosos:** quem não publicou em 30 dias.

**Sinais de alarme:**

- A maioria das publicações é da equipa — é um canal de difusão, não uma
  comunidade, e não justifica o preço do Premium
- Perguntas sem resposta há mais de 24 horas
- As mesmas 5 pessoas geram 80% da atividade
- Membros novos publicam a apresentação e desaparecem

---

## 10. O que não fazer

- Não apresentar a taxa de cancelamento como métrica de sucesso enquanto
  não passar a primeira janela de renovação.
- Não construir fluxo de cancelamento automatizado. A 134 membros a saída
  trata-se por telefone.
- Não copiar métricas de SaaS mensal — MRR, dunning, recuperação de
  pagamentos falhados não se aplicam a subscrição anual paga de uma vez.
- Não pedir testemunho antes da ativação. Um membro que ainda não resolveu
  nada só pode elogiar as expectativas.
