# Formato dos ficheiros e uso nas bases de conhecimento

## Anatomia (gerada pelo `estruturar.py`)

```markdown
---
titulo: "Código Civil — Propriedade horizontal"
diploma: "Código Civil (Decreto-Lei n.º 47344/66, de 25 de novembro)"
sigla: "CC"
tipo: "excerto"                 # ou "integral"
artigos: "1414.º a 1438.º-A"    # ou "todos"
versao: "consolidada em vigor"
em_vigor_desde: "AAAA-MM-DD"
ultima_alteracao: "…"
fonte: "DRE"
fonte_url: "https://…"
data_consulta: "AAAA-MM-DD"
verificacao: "automática OK: 26/26 artigos palavra a palavra"
---

# Código Civil — Propriedade horizontal

<!-- cabecalho -->
> **Código Civil (…)** — texto consolidado, versão em vigor desde … (última alteração: …).
> Fonte: [DRE](https://…) · consultada em ….
> **Excerto:** contém apenas os artigos 1414.º a 1438.º-A. Um artigo que não esteja neste ficheiro pode existir no diploma.
<!-- /cabecalho -->

## CAPÍTULO VI — Propriedade horizontal

## SECÇÃO I — Disposições gerais

### Artigo 1414.º [CC] — Princípio geral

…
```

Porque é assim:

- **Metadados YAML**: permitem saber a versão e a data de consulta sem abrir o texto, e
  procurar ficheiros desatualizados quando a lei muda.
- **Aviso visível**: o ChatGPT e os Projetos do Claude nem sempre dão importância aos
  metadados; o aviso no corpo garante que a fonte e o estatuto de excerto são lidos.
- **Um artigo = um título `###` com sigla**: as bases de conhecimento partem os ficheiros
  em pedaços; com o artigo, a sigla e a epígrafe no título, cada pedaço identifica-se
  sozinho («Artigo 1424.º [CC]» não se confunde com o 1424.º de outro código).
- **Divisões como `##`**: a hierarquia completa (Livro > Título > Capítulo > Secção) fica
  achatada num só nível de propósito: níveis de título fundos variam de diploma para
  diploma e confundem a divisão em pedaços.
- **Marcadores `<!-- cabecalho -->`, `<!-- fecho -->` e `<!-- quadro … -->`**: o `verificar.py`
  usa-os para separar o que foi acrescentado do texto legal. Não os apagues.
- **Quadros**: os «(ver documento original)» do DRE ficam em parágrafo próprio. Um quadro
  reproduzido entra logo a seguir, entre `<!-- quadro … -->` e `<!-- /quadro -->`, com a nota
  de origem (PDF, página, versão). Ver `references/tabelas.md`.

## Nomes dos ficheiros

`SIGLA_tema-curto_AAAA-MM-DD.md`, em que a data é a de `em_vigor_desde`.
Exemplos: `CC_propriedade-horizontal_AAAA-MM-DD.md`, `DL268-94_condominio_AAAA-MM-DD.md`.
Sem espaços nem acentos no nome (evita problemas ao carregar em plataformas diferentes).
A data no nome mostra logo, numa lista de ficheiros, qual a versão em causa.

## Inteiro ou excerto?

- Diplomas curtos (regimes avulsos, decretos-lei de algumas dezenas de artigos): inteiros.
- Códigos grandes (Código Civil, CPC, Código do Trabalho): excertos por tema, um ficheiro
  por regime (ex.: propriedade horizontal; compropriedade; arrendamento urbano). Um código
  inteiro ocupa uma parte enorme do espaço da base de conhecimento e dilui a pesquisa.
- Num excerto, inclui o regime completo do tema (todos os artigos da secção/capítulo) e
  não artigos soltos, salvo pedido expresso: um assistente que recebe meio regime
  responde com meia resposta.

## Bases de conhecimento

- **Projetos do Claude e ChatGPT**: carrega os `.md` tal como saem; não converter para PDF
  ou Word (perde-se a estrutura de títulos). Um ficheiro por diploma/regime.
- Quando uma lei muda, substitui o ficheiro antigo (não deixes as duas versões no mesmo
  projeto: o assistente pode citar a errada).
- **Materiais TSC** (membros da comunidade): os ficheiros são texto legal, não conteúdo
  pedagógico. Para publicação, mantém o aviso de fonte e data de consulta e confere por
  amostragem no DRE. Explicações e anotações vão noutro documento, nunca misturadas com o
  texto da lei.
