---
name: legislacao-markdown
description: Converte diplomas legislativos portugueses (leis, decretos-lei, códigos, regulamentos, portarias), inteiros ou em excerto, em ficheiros Markdown fiéis ao texto consolidado em vigor, prontos para bases de conhecimento de Projetos do Claude, do ChatGPT e para materiais da comunidade TSC. Obtém o texto pela hierarquia DRE → PGDL → Alpaca, extrai-o mecanicamente de PDF/HTML, estrutura-o por artigos e verifica palavra a palavra que nada foi omitido ou alterado. Usar SEMPRE que o pedido envolva converter, passar, transcrever ou preparar legislação para Markdown/.md, montar ou atualizar uma base de conhecimento com leis, extrair artigos de um PDF do Diário da República ou da PGDL, ou preparar um código/regime jurídico (por exemplo, propriedade horizontal, Código Civil, regime do condomínio) para carregar num projeto de IA — mesmo que o utilizador não fale em «skill» nem em «Markdown» e diga só «põe-me esta lei em texto» ou «prepara-me o regime X para o projeto».
---

# Legislação → Markdown fiel

Estes ficheiros vão servir de fonte a assistentes de IA e a membros da comunidade.
Um artigo com uma alínea a menos ou um prazo trocado é pior do que não ter ficheiro,
porque passa a ser citado com confiança. Por isso a regra central desta skill é:

**O texto legal nunca é escrito por ti.** É extraído por programa, estruturado por
programa e verificado por programa. O teu trabalho é escolher a fonte certa, correr
os passos, ler os relatórios, decidir os casos ambíguos e preencher os metadados.
Se te apetecer «limpar» ou «corrigir» o texto à mão no .md, não o faças: corrige o
passo que falhou e volta a gerar.

Não uses WebFetch (nem ferramentas que resumem páginas) para obter o texto de uma
lei: devolvem uma versão processada por um modelo, não o texto. Descarrega o ficheiro
com `curl` ou pede-o ao utilizador.

## Preparação (uma vez por máquina)

Os programas estão em `scripts/` (ao lado deste ficheiro) e precisam de Python 3.10+
com o módulo `pymupdf`. Testa com `python3 -c "import pymupdf"`. Se falhar, cria um
ambiente próprio e usa esse Python em todos os comandos:

```bash
python3 -m venv ~/.venvs/legislacao && ~/.venvs/legislacao/bin/pip install pymupdf
```

Nos exemplos abaixo, `PY` é o Python que funciona e `S` a pasta `scripts/` desta skill.

## Fluxo

### 1. Fixar o pedido

Confirma, se não estiver claro: qual o diploma, se vai **inteiro** ou em **excerto**
(e que artigos), a **sigla** a usar nos títulos (CC, CPC, RJUE, RGEU…) e a pasta de
destino. Só se trabalha com a **versão consolidada em vigor**.

### 2. Obter a fonte

Segue a hierarquia do utilizador, por esta ordem, e regista qual usaste:

1. **DRE** (diariodarepublica.pt): oficial. Preferir a legislação consolidada; o PDF
   da publicação original no Diário da República só tem a redação inicial.
2. **PGDL** (pgdlisboa.pt): versões consolidadas não oficiais, em HTML. Úteis quando
   o DRE não tem consolidação. Confirmar a data da última alteração indicada.
3. **Alpaca** (ferramenta `mcp__Alpaca_Docs__*`): texto consolidado artigo a artigo,
   com data de entrada em vigor. Fonte de terceiros: último recurso para o texto, mas
   ótima para **confirmar** a versão e as datas das outras fontes.

Pormenores e armadilhas de cada fonte: `references/fontes.md` (lê antes de usar a
PGDL ou o Alpaca pela primeira vez numa sessão).

### 3. Extrair

```bash
$PY $S/extrair.py fonte.pdf -o trabalho/diploma.txt
```

Aceita `.pdf`, `.html` e `.txt`. Lê a saída e o relatório `*.extracao.json`:

- **ALERTA de páginas sem texto** → o PDF é digitalizado. Para aqui: procura outra
  fonte digital. Não transcrevas a partir da imagem.
- **CONFERIR junções de hífen** → casos como «aplica-|se» vs «análi-|se». Decide cada
  um. Se algum estiver errado, corrige no `.txt` com uma substituição pontual (ex.:
  `sed -i '' 's/análi-se/análise/' trabalho/diploma.txt` no Mac) e diz ao utilizador
  o que mudaste.
- **Cabeçalhos/rodapés retirados** → confirma, no relatório, que só saíram linhas de
  paginação (Diário da República, n.º de página, endereço do site…). Se saiu texto
  legal, repete com `--sem-cabecalhos`.
- **Notas editoriais PGDL retiradas** → as notas «Contém as alterações…» ficam no
  relatório. Usa-as para identificar a última alteração (metadados), não no texto.

### 4. Confirmar metadados

Precisas de: identificação oficial do diploma, data desde a qual a versão está em
vigor, última alteração, URL da fonte. Retira-os da própria fonte; o Alpaca indica
«Em vigor desde» por artigo e serve para confirmar. Num excerto, a data de vigência é
a **mais recente** entre os artigos incluídos. Se não conseguires confirmar um dado,
deixa-o vazio e diz ao utilizador. Nunca inventes datas nem números de diploma.

### 5. Estruturar

```bash
$PY $S/estruturar.py trabalho/diploma.txt -o destino/CC_propriedade-horizontal_AAAA-MM-DD.md \
  --titulo "Código Civil — Propriedade horizontal" \
  --diploma "Código Civil (Decreto-Lei n.º 47344/66, de 25 de novembro)" --sigla CC \
  --fonte DRE --url "URL" --em-vigor-desde AAAA-MM-DD \
  --ultima-alteracao "…" \
  --artigos "1414..1438-A"          # só em excertos; intervalos com «..»
  # --depois-de "^ANEXO"            # quando o decreto preambular repete números de artigo
  # --sem-preambulo                 # omitir preâmbulo e assinaturas num diploma inteiro
```

Lê os ALERTAS: artigos pedidos que não existem, números repetidos (normalmente o
decreto que aprova um código + o código em anexo → usar `--depois-de "^ANEXO"`),
artigos sem epígrafe (normal em diplomas antigos; estranho se forem muitos).

### 6. Verificar (obrigatório)

```bash
$PY $S/verificar.py trabalho/diploma.txt destino/FICHEIRO.md --marcar
```

Compara artigo a artigo, palavra a palavra, o Markdown com o texto extraído e grava o
resultado nos metadados (`verificacao`). Só entregas um ficheiro com `RESULTADO: OK`.
Se houver diferenças, o problema está na estruturação (ex.: um «fecho» detetado no
sítio errado): percebe a causa, corrige a origem ou as opções e gera de novo.

A verificação não apanha mudanças de pontuação nem erros que já venham da fonte ou da
extração. Por isso, no fim, mostra ao utilizador 2 ou 3 artigos lado a lado com a
fonte (escolhe os mais longos ou com mais alíneas) para uma conferência rápida.

### 7. Rever a estrutura e entregar

Corre `grep -n "^##" FICHEIRO.md` e confirma que a árvore (livros, títulos, capítulos,
secções, artigos) faz sentido. Depois entrega um resumo curto: ficheiro(s) criado(s),
fonte, versão/data, n.º de artigos, resultado da verificação, decisões tomadas
(junções de hífen, metadados por confirmar).

## Quando a única fonte é o Alpaca

O texto chega pela ferramenta, por isso tens de o escrever num ficheiro. Copia o
conteúdo devolvido **sem alterar nada** para `trabalho/diploma.txt`, no formato:

```
Artigo 1424.º
Encargos de conservação e fruição
1 - Salvo disposição em contrário, …
```

Para diplomas inteiros, obtém primeiro o índice (`get_law_index_at_date`) e depois os
artigos um a um. Corre os passos 5 e 6 normalmente e escreve na entrega que o texto foi
transcrito da ferramenta e que a verificação só confirma a estrutura. Recomenda
conferir por amostragem no DRE.

## Formato do ficheiro

Metadados YAML, título, um aviso visível (fonte, versão, e em excertos a lista de
artigos incluídos), divisões como `##` e artigos como `### Artigo N.º [SIGLA] —
Epígrafe`. A sigla e o aviso de excerto existem para que um assistente que só recebe
um pedaço do ficheiro saiba de que diploma se trata e não conclua que um artigo
inexistente no excerto não existe na lei. Pormenores, nomes de ficheiros e conselhos
para Projetos do Claude, ChatGPT e TSC: `references/formato.md`.
