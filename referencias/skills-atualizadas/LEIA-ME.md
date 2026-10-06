# Skills atualizadas — lista de tiques PT-PT integrada (2026-10-06)

Estado (2026-10-06): **carregado na conta e verificado no Claude Code (sessão cloud).** Cópia sincronizada da conta igual à versão preparada (tsc-conteudo: ficheiro a ficheiro; humanizer: corpo idêntico, só o frontmatter YAML foi reserializado pela plataforma, com o mesmo conteúdo). Chamada real a cada skill pelo nome: carregam v2.2 e 2.7.0-pt1 com as secções novas; `references/` e `scripts/` encontrados e executados. **Por verificar:** app Claude (chat) e Claude Code no computador — abrir uma conversa nova em cada e pedir para correr a skill; deve aparecer o passo 4b (tsc-conteudo) e a secção PT-PT (humanizer).

Este ficheiro é só uma nota para ti: **não faz parte das skills, não se carrega em lado nenhum** (os zips não o incluem). Podes apagá-lo.

| Skill | Versão | O que muda | Zip |
|---|---|---|---|
| tsc-conteudo | v2.1 → v2.2 | passo 4b no fluxo, linha na checklist (secção 9), linha na tabela de referências, bullet de rodapé PT-PT na 5.1, nota de versão; novo `references/05-tiques-pt-pt.md` (inclui as regras de marca) e `scripts/verificar_tiques.py` | `tsc-conteudo.zip` |
| humanizer | 2.7.0 → 2.7.0-pt1 | nota no início e nova secção «PORTUGUÊS EUROPEU (PT-PT)»; novo `references/tiques-pt-pt.md` e `scripts/verificar_tiques.py` | `humanizer.zip` |

Nada foi removido nem reescrito nos ficheiros existentes: só acrescentos. As descrições (o que dispara cada skill) ficam **idênticas**, por isso o custo de contexto permanente não aumenta. O SKILL.md cresce 1 349 caracteres (tsc-conteudo) e 2 152 (humanizer); a lista completa só se carrega a pedido.

Depois de carregares os zips: verificar de dentro de cada cliente (chat, Code) que a skill carrega e que o passo 4b / a secção PT-PT aparecem; e comparar as cópias entre superfícies com `comparar_copias.sh` da skill `avaliar-componentes-externos`.
