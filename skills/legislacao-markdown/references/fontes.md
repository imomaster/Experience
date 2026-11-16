# Fontes: DRE, PGDL e Alpaca

Ordem de preferência definida pelo utilizador: **DRE → PGDL → Alpaca**. Regista sempre
qual foi usada (`--fonte`) e o endereço exato (`--url`).

## DRE — Diário da República Eletrónico (oficial)

- Há duas coisas diferentes no DRE e convém não as confundir:
  - **a publicação no Diário da República** (o PDF do diploma tal como saiu), que tem
    só a redação original e, no caso de leis de alteração, só as alterações;
  - **a legislação consolidada**, que junta o diploma com todas as alterações em vigor.
  É esta que se quer.
- Se o utilizador fornecer um PDF, confirma qual dos dois é: um PDF da publicação traz
  cabeçalhos «Diário da República, 1.ª série» e número/data da série; um diploma de
  alteração (que diz «O artigo X passa a ter a seguinte redação») **não** serve como
  texto consolidado.
- Quando o diploma foi **republicado** em anexo a uma lei de alteração, essa
  republicação é texto consolidado à data dessa lei — útil, mas verifica se houve
  alterações posteriores (o Alpaca dá a data de vigência de cada artigo).
- O site do DRE depende de JavaScript: descarregar com `curl` pode não devolver o texto.
  Se não conseguires, pede ao utilizador o PDF ou que guarde a página.

## PGDL — Procuradoria-Geral Distrital de Lisboa (pgdlisboa.pt)

- Versões consolidadas em HTML, muito usadas na prática, mas **não oficiais**, e a
  atualização pode atrasar-se em relação às alterações mais recentes.
- Cada artigo alterado traz notas editoriais («Contém as alterações dos seguintes
  diplomas: …», «Consultar versões anteriores deste artigo»). O `extrair.py` retira-as
  do texto e guarda-as no relatório: usa-as para confirmar a última alteração.
- As epígrafes aparecem entre parênteses, «(Encargos de conservação e fruição)»: o
  `estruturar.py` trata disso.
- As páginas costumam estar em ISO-8859-1. Descarrega com `curl -L -o pagina.html URL`;
  o `extrair.py` deteta a codificação.
- Num diploma inteiro, a página traz menus e texto de navegação antes do articulado:
  usa `--sem-preambulo` ou confirma o início do texto no `.txt` e corta o lixo inicial
  com `sed` antes de estruturar (diz ao utilizador o que cortaste).
- Antes de confiar na PGDL, compara a data da última alteração com a do Alpaca para
  2 ou 3 artigos. Se a PGDL estiver atrasada, avisa e muda de fonte.

## Alpaca (ferramentas `mcp__Alpaca_Docs__*`)

- `search_legal_docs` (jurisdição `pt`, `doc_type: legislation`, âmbito `consolidated`
  por omissão): devolve o texto consolidado **atual** de cada artigo, com o caminho na
  estrutura (Livro > Título > Capítulo…) e «Em vigor desde AAAA-MM-DD».
- `get_law_index_at_date`: lista os artigos de um diploma numa data; serve para montar
  diplomas inteiros e para saber que artigos existem.
- `get_article_at_date`: um artigo na versão em vigor numa data.
- Limitações vistas na prática: funciona artigo a artigo (um diploma grande são muitos
  pedidos); a numeração herdada é irregular («1 -» e «1.» no mesmo artigo, tal como na
  fonte original); a pesquisa traz ruído de outros diplomas com artigos de número igual
  (ex.: o antigo Código de Processo Civil quando se procura o art. 1424.º do Código
  Civil) — confirma sempre o campo `law` de cada resultado.
- É fonte de terceiros. Para materiais publicados (TSC), confere por amostragem no DRE.

## Datas e versões

- `--em-vigor-desde` é a data desde a qual **este texto** está em vigor. Num excerto
  com vários artigos, usa a data mais recente entre eles.
- `--ultima-alteracao` identifica o diploma que fez a última alteração (ex.: «Lei n.º
  8/2022, de 10 de janeiro»), se a fonte a indicar.
- Se as fontes não coincidirem, não escolhas em silêncio: diz ao utilizador o que cada
  uma indica.
