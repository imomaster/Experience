# Pareceres — energy-procurement e copywriting (2026-10-05)

Origem: pesquisa com `find-skills` (skills.sh). Pré-condições: `gh` com token inválido e `api.github.com` bloqueado pelo proxy do ambiente (403) → **modo degradado**: estrelas, forks, subscritores, release e arquivo ficam `[NÃO RECONCILIADO]`. Lido por `git clone` (permitido): commit, licença e conteúdo.

---

**Veredicto: MATÉRIA-PRIMA** — o método (compra em camadas, avaliação de propostas pelo custo total, perfil de carga) aproveita; o enquadramento é 100 % norte-americano.

**Componente:** energy-procurement · skill · ecc ef648e0, skill v1.0.0 · 2026-10-05
**Para quê:** apoio a consultoria energética · **Já existe algo que faça isto?** não

## Números — anunciado vs. reconciliado
| O que se afirma | Anunciado | Fonte oficial | O que conta |
|---|---|---|---|
| 8,7 K | skills.sh | `[NÃO RECONCILIADO]` | instalações via CLI, medidas pelo próprio diretório; sem contrapartida verificável |
| Licença | frontmatter: Apache-2.0 | LICENSE do repo: MIT | **divergência** entre o que a skill declara e o repositório |
| Versão | skill 1.0.0 | repo VERSION 2.2.3 | versões de coisas diferentes (skill vs. pacote) |
Último commit (clone): 2026-10-01 · Arquivado: `[NÃO RECONCILIADO]`
A divergência de licença não bloqueia, mas é sinal de metadados pouco cuidados.

## O que entra no sistema
- Tamanho: 1 ficheiro, ~29,7 K caracteres (~7,4 K tokens quando carregada). Sem scripts, sem dependências.
- Custo de contexto permanente: descrição de 406 caracteres. Baixo. Mas dispara em «compra de energia / tarifas», e aí injeta pressupostos dos EUA.
- Risco: scripts de instalação **limpo** · escritas fora da pasta **limpo** · permissões/credenciais **limpo** · texto imperativo ao agente **limpo** · rede/telemetria **limpo** (a skill não faz nada; é só texto).
- Risco real não é de segurança: é **conselho plausível e errado**. Zero ocorrências de ERSE, MIBEL, OMIE, potência contratada, BTE/BTN, garantias de origem; 7 de PJM, 7 de ERCOT, 28 de «$». Referências de mercado e números («prémio de risco 5–12 %», «$8–25/kW») sem fonte.

## Teste na língua / jurisdição
Não é teste de léxico, é de aplicabilidade: o papel definido é «gestor sénior de compras com $15–80 M/ano em 10–50 instalações». Um condomínio ou PME portuguesa está várias ordens de grandeza abaixo. `[A VALIDAR]` com fonte oficial (ERSE) o regime de mercado e de tarifas aplicável em Portugal: **não** faço afirmações sobre ele neste parecer.

## O que se aproveita
Aproveita-se: estrutura de RFP a comercializadores (dados de consumo a pedir, critérios para comparar), compra em camadas (tranches), fixo vs. indexado vs. misto como dilema, fator de carga, matriz de escalonamento. Deita-se fora: PJM/ERCOT/LMP, PPAs virtuais, ratchets, números em dólares, papel de gestor corporativo. Guardado em: não arquivado, aguarda aprovação.

## Estado
não instalado · Registado em: referencias/componentes-avaliados.md, linha de 2026-10-05

---

**Veredicto: MATÉRIA-PRIMA** — princípios de redação bons, mas a verificação de «tiques de IA» é inglesa e dá falsa segurança em PT-PT; o resto já está coberto por skills tuas.

**Componente:** copywriting · skill + 3 referências + evals · marketingskills dda3841, skill v2.1.0 · 2026-10-05
**Para quê:** redigir copy de marketing (TSC, Imomaster) · **Já existe algo que faça isto?** sim: tsc-conteudo (produção para a TSC) e humanizer (limpeza de texto de IA)

## Números — anunciado vs. reconciliado
| O que se afirma | Anunciado | Fonte oficial | O que conta |
|---|---|---|---|
| 216 K | skills.sh | `[NÃO RECONCILIADO]` | instalações via CLI; sem contrapartida verificável |
| «+81 % conversões, −38 % ciclo de vendas, −28 % CAC, +175 % referências» | texto da skill | sem fonte no ficheiro | `[A VALIDAR]`: estatística sem citação |
Último commit (clone): 2026-10-02 · Licença: MIT · Arquivado: `[NÃO RECONCILIADO]`

## O que entra no sistema
- Tamanho: SKILL.md ~10,9 K caracteres (~2,7 K tokens) + 3 referências (~35 K caracteres, carregadas a pedido) + evals. Sem scripts.
- Custo de contexto permanente: descrição de **946 caracteres** (cerca de 2,3× a outra). Dispara em quase qualquer pedido de «texto para uma página», sobrepondo-se à tsc-conteudo.
- Risco: scripts **limpo** · escritas fora da pasta **limpo** (lê `.agents/product-marketing.md` se existir; só leitura) · permissões **limpo** · texto imperativo **limpo** · rede/telemetria **limpo**.
- Dependências em falta: remete para as skills copy-editing, cro, emails, popups, ab-testing, que não vêm com ela. Instalada sozinha, tem referências soltas.

## Teste na língua do utilizador
| Amostra | Inglês | Português (PT-PT) | Diferencial |
|---|---|---|---|
| «It's not just software, it's a revolution» + «Say goodbye to…» + «The result? 3x faster.» | verificação da skill apanha as 3 linhas | — | referência |
| «Não é apenas um software…, é uma revolução» (contraste, padrão 1) | — | **não apanhada** | falha silenciosa |
| «Num mundo cada vez mais digital, desbloqueie…» (abertura-clichê, padrão 5) | — | **não apanhada** | falha silenciosa |
| «Diga adeus às atas: sem folhas…» e «O resultado? 3 vezes…» | — | apanhadas **só por acaso** (pelos sinais «:» e «?») | não pela palavra |
Mecanismo: a verificação da skill manda procurar `"not "`, `"isn't"`, `"no "`, `"without"`. Em português seriam «não é/não só», «sem». Das 5 linhas de teste, 2 foram assinaladas, nenhuma pela razão certa. O erro não aparece: o texto passa como «verificado».

## O que se aproveita
Aproveita-se: clareza sobre cleverness, especificidade sobre vago, o «swap test» (a frase serviria no site do concorrente?), a estrutura da hero como transformação, a regra de sinalizar `[NEED: …]` em vez de inventar prova. Deita-se fora: listas de CTAs e chavões em inglês, as estatísticas sem fonte, a verificação mecânica em inglês. Valor real: servir de modelo para uma **lista de «tiques» em PT-PT** a integrar na tsc-conteudo ou na humanizer. Guardado em: não arquivado, aguarda aprovação.

## Estado
não instalado · Registado em: referencias/componentes-avaliados.md, linha de 2026-10-05
