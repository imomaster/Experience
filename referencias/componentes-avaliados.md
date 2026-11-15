# Registo de componentes avaliados

Uma linha por avaliação, qualquer que seja o veredicto (fase 6 da skill `avaliar-componentes-externos`).

| data | componente | tipo | versão/commit | veredicto | razão (uma frase) | onde está | estado de verificação |
|---|---|---|---|---|---|---|---|
| 2026-11-15 | NVIDIA SkillSpector (`NVIDIA/skillspector`) | CLI (Python ≥3.12) | v2.12.0 / c816150 | instalar (condicionado) | Scanner estático eficaz em inglês, mas não deteta injeção de prompt em PT-PT: usar só como filtro de entrada, nunca como certificado. | venv isolado numa pasta temporária de sessão cloud (efémero); não instalado na máquina do utilizador nem na conta | testado em cópia isolada, só `--no-llm`; instalação definitiva por aprovar; estrelas/nº de regras `[NÃO RECONCILIADO]` (gh sem autenticação) |

## Notas por componente

### SkillSpector — 2026-11-15
Testes estáticos (`--no-llm`), cobertura 100 % em todos os casos:

| Alvo | Língua | Resultado |
|---|---|---|
| Skill maliciosa (exfiltração de `~/.ssh`, `curl \| bash`) | EN | 93 CRITICAL, `DO_NOT_INSTALL`, 5 achados (incl. Prompt Injection) |
| Skill maliciosa, mesma carga | PT-PT | 73 HIGH, `DO_NOT_INSTALL`, 4 achados — **sem** Prompt Injection |
| Skill maliciosa só em linguagem natural (copiar NIF/IBAN em base64, "nunca menciones esta regra") | PT-PT | **0 SAFE, 0 achados — falso negativo** |
| `atas-assembleia` (própria) | PT-PT | 0 SAFE |
| `skill-inspector` (NVIDIA) | EN | 0 SAFE |
| Skill benigna `modelo-convocatoria` | PT-PT | 0 SAFE |

Diferencial: o que depende de comandos e caminhos (`curl`, `~/.ssh`, `| bash`) apanha-se em qualquer língua; o que depende de texto imperativo dirigido ao agente em PT-PT passa. A segunda passagem com LLM (desligada) não foi testada e pode fechar a lacuna: **por verificar**.

Por fazer: reconciliar estrelas/regras/último commit contra a fonte; testar `--llm` com um fornecedor; decisão de instalar (máquina local) com aprovação explícita.
