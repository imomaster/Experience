# Quadros e tabelas a partir do PDF oficial

Para os «(ver documento original)» do texto consolidado do DRE: quadros, tabelas e
anexos que só existem no PDF publicado no Diário da República.

Índice: 1. Princípio · 2. Que PDF usar (versão em vigor) · 3. Obter o PDF · 4. Extrair
· 5. Ler o resultado · 6. Símbolos · 7. Inserir e contar · 8. Limites conhecidos

## 1. Princípio

Nada do que entra num quadro é escrito por ti. O `tabelas.py` tira as colunas das
linhas verticais desenhadas no PDF, as linhas das regras horizontais e do alinhamento
do texto, e o conteúdo da camada de texto. Depois verifica o resultado de duas formas.
Tu escolhes o PDF e a página, olhas para a imagem, decides os símbolos com o
utilizador e corres a inserção. Se o resultado não for fiável, o quadro fica recusado
e mantém-se a ligação ao PDF. Um quadro «arranjado» à mão não entra em nenhum bloco.

Três modos, sempre declarados no ficheiro e no relatório:

| Modo | O que é | Entra no bloco? |
|---|---|---|
| `grelha` | tabela Markdown que passou as duas verificações | sim, depois de vista com a imagem |
| `linear` | o texto do quadro, linha a linha, sem colunas, com aviso explícito | só com aprovação expressa do utilizador |
| `recusada` | só a razão registada | não: fica a ligação ao PDF e a página |

## 2. Que PDF usar (versão em vigor)

A ligação «(ver documento original)» do DRE aponta **sempre** para o PDF da publicação
original, mesmo que o artigo tenha sido alterado. Num teste com o RT-SCIE (Portaria
n.º 1532/2008), 48 de 56 quadros estavam em artigos alterados pela Portaria n.º
135/2020, e o mesmo quadro tinha cabeçalhos diferentes nas duas versões.

```bash
$PY $S/historico.py consolidado.txt            # só artigos/anexos com quadros
$PY $S/historico.py consolidado.txt --artigo 26
```

`consolidado.txt` é o texto da página de legislação consolidada do DRE (com as linhas
«Alterado pelo/a Artigo X do/a <ato> - Diário da República n.º …, em vigor a partir
de …»). Para cada fragmento o programa indica o último ato e, no fim, um resumo dos PDF
a obter. Regras:

- **Sem histórico** → PDF original do diploma.
- **Com histórico** → PDF do último ato, **se trouxer o quadro**. Um ato de alteração
  só reproduz o que muda: um quadro inalterado aparece como uma linha de pontos por
  baixo da legenda. Nesse caso o `tabelas.py --legenda` responde `RESULTADO: INALTERADO`
  e recuas para o ato anterior do histórico, ou para o original.
- **Revogado** → o quadro já não está em vigor: não se reproduz; avisa o utilizador.
- Se o ato alterar e também republicar o diploma, a legenda aparece em várias páginas.
  Usa a da republicação (normalmente a última) e confirma com `--pagina N --listar`.
- Regista sempre em `--versao` o ato de onde o quadro foi tirado. É isso que vai para a
  nota do quadro.

Para chegar ao PDF de um ato: pesquisar o ato no DRE, abrir a página «detalhe» e copiar
a ligação para `files.diariodarepublica.pt` (as páginas do DRE precisam de JavaScript:
usar o browser, não `curl`).

## 3. Obter o PDF

1. `curl -L -o pdfs/NOME.pdf "https://files.diariodarepublica.pt/…pdf"`.
2. Se for recusado (403): o pedido tem de partir do browser. Abre um separador numa
   página do DRE, corre lá o conteúdo de `scripts/dre_descarregar.js` e chama
   `await descarregarPDFs([lista de endereços])`. O browser grava um único ficheiro
   `dre_pdfs.json` (um só, porque o Chrome bloqueia várias transferências automáticas
   seguidas). Depois: `$PY $S/dre_desempacotar.py ~/Downloads/dre_pdfs.json -o pdfs/`.
   O `pdfs/origem.json` guarda o endereço oficial de cada ficheiro, para o `--url`.
3. Nunca WebFetch nem ferramentas que «leem» o PDF por ti.

## 4. Extrair

```bash
$PY $S/tabelas.py pdfs/NOME.pdf --pagina 11 --listar          # o que há na página
$PY $S/tabelas.py pdfs/NOME.pdf --pagina 11 --legenda "QUADRO XX" -o quadros/ \
    --url "https://files.diariodarepublica.pt/…pdf" --versao "Portaria n.º 1532/2008"
```

- `--pagina` é a página do PDF (1 = primeira), não o número impresso no Diário.
- `--legenda` procura a expressão inteira («QUADRO I» não apanha «QUADRO II») e escolhe
  o quadro logo abaixo. Sem `--pagina`, procura no PDF todo e, se houver várias
  páginas, lista-as (muitas são só remissões no texto).
- `--tabela K` escolhe pelo número do `--listar`; `--bbox x0,y0,x1,y1` indica a zona à
  mão quando o quadro não é detetado (coordenadas em pontos do PDF).
- Sem `--legenda` nem `--tabela`, extrai todos os quadros da página.
- `--linhas regras|texto` força a forma de separar as linhas quando o automático errar
  (ver secção 5). `--modo linear` pede logo o modo linear.

Saída, por quadro: `NOME_pN_qK.md`, `.json` e `.png` (recorte da página a 2x, com a
legenda). Código de saída 0 = todos `OK`; 1 = há algo por decidir ou recusado; 2 = sem
quadro ou digitalizado; 3 = `INALTERADO`.

## 5. Ler o resultado

**Abre sempre o `.png` e compara com o `.md` antes de mostrar ao utilizador**, e mostra
os dois juntos. O programa verifica que nenhuma palavra se perdeu nem foi inventada;
não consegue garantir que cada valor está na linha certa quando as linhas não têm
regras desenhadas. É isso que tu e o utilizador conferem.

O que os ALERTAS querem dizer e onde olhar:

- **«As linhas do quadro foram deduzidas do alinhamento do texto»**: o quadro não tem
  uma regra por linha (o mais comum no Diário da República). Confere duas ou três
  linhas ao acaso, e sobretudo as que têm texto em mais de uma linha.
- **«N linha(s) só têm texto numa coluna»**: pode ser uma linha própria (um subtítulo
  dentro do quadro) ou a continuação da anterior que não foi reconhecida. Vê na imagem.
  Se for continuação, o quadro está mal partido: tenta `--linhas regras`; se não
  resolver, fica `linear` ou recusado.
- **«Células fundidas: o texto foi repetido»**: um cabeçalho ou valor que abrange várias
  colunas/linhas foi repetido em cada uma. No cabeçalho, os níveis juntam-se com « — »
  («Via acima do plano de referência — H ≤ 28 m»). Confirma que a repetição corresponde
  ao que a imagem mostra.
- **«Na 1.ª coluna, o valor de cada grupo foi repetido»**: grupos delimitados por regras
  (ex.: «Enclausurada» para duas linhas). Confirma os limites dos grupos.
- **«As linhas verticais do cabeçalho e do corpo não estão na mesma posição»**: as
  colunas foram emparelhadas pela ordem. Confirma que cada título está sobre a coluna
  certa.
- **«Há texto rodado 90°»**: títulos de coluna escritos na vertical, lidos pela rotação.
  Confirma a ordem das palavras.
- **«O quadro não tem regra de fecho: continua…»**: o quadro segue noutra coluna ou
  página. Extrai cada parte e une-as com `quadros.py juntar` (exige o mesmo cabeçalho
  em todas as partes; se a continuação não repetir o cabeçalho, não se juntam).
- **`CONFERIR hífen`**: palavra cortada no fim da linha em que o hífen pode ser da
  palavra. Decide como no `extrair.py`.

Marcas no texto: índices e expoentes saem como `<sub>…</sub>` e `<sup>…</sup>`
(«F<sub>s</sub>», «m<sup>2</sup>»). Os pontos de preenchimento («R . . . . .») são
retirados e contados no relatório.

Razões habituais para `linear` ou `recusada` (são o comportamento certo, não um erro):
menos de 60 % das células preenchidas; várias entradas acumuladas numa célula; um
rótulo que é comum a várias linhas do quadro; colunas do cabeçalho que não coincidem
com as do corpo; texto inclinado; quadro deitado na página; página sem camada de texto
(digitalizada: **não se faz OCR**).

## 6. Símbolos

Alguns PDF têm na camada de texto um carácter diferente do que se vê. Casos reais:

| No texto extraído | Na imagem | Onde apareceu |
|---|---|---|
| `C « 80`, `L « 102` | ≤ | DL n.º 9/2007, tipo de letra «8881» |
| `80 ‹ C`, `C › 175` | < e > | idem |
| `H d 28 m` | ≤ | Portaria n.º 1532/2008, tipo de letra «SymbolMT» |

O programa assinala `CONFERIR` em cada ocorrência (carácter vindo de um tipo de letra
de símbolos, aspas angulares simples, aspa isolada entre dois valores) e **nunca
substitui sozinho**. A tabela acima são exemplos, não uma regra: o símbolo certo
confirma-se sempre na imagem daquele quadro. Depois de o utilizador decidir:

```bash
$PY $S/tabelas.py … --trocar "«=≤" --trocar "‹=<" --trocar "›=>"
```

A troca só se aplica aos carateres assinalados (as aspas normais do resto do quadro
ficam como estão) e fica registada no relatório e na nota do quadro. Se o símbolo
assinalado estiver certo como está, usa `--simbolos-conferidos`.

## 7. Inserir e contar

```bash
$PY $S/quadros.py inserir BLOCO.md quadros/NOME_p11_q1.md --legenda "QUADRO XX"
$PY $S/quadros.py inserir BLOCO.md quadros/NOME_p25_q2.md --ocorrencia 14
$PY $S/quadros.py contar BLOCO_*.md
```

- O quadro entra logo a seguir ao «(ver documento original)» certo, entre os marcadores
  `<!-- quadro … -->` e `<!-- /quadro -->`, com a nota «Quadro extraído do PDF oficial
  (URL, pág. N, versão: <ato>) — verificado». Não apagues os marcadores: o
  `verificar.py` usa-os para ignorar o quadro quando confere o texto do diploma.
- `--legenda` procura o «(ver documento original)» que vem a seguir a essa legenda no
  ficheiro; se houver mais de um candidato, usa `--ocorrencia N`.
- Só entram quadros com `resultado="OK"`. `CONFERIR` e `recusada` são rejeitados pelo
  programa; `linear` exige `--aprovado` (aprovação expressa do utilizador).
  `--substituir` troca um quadro já inserido (por exemplo, quando sai nova versão).
- Depois de inserir, corre de novo o `verificar.py` sobre o ficheiro: confirma que o
  texto do diploma não foi tocado.
- `contar` dá, por ficheiro, o total de «(ver documento original)», quantos têm grelha,
  quantos têm versão linear e quantos ficaram só com ligação. Regista esses números na
  ficha do diploma.

## 8. Limites conhecidos

- Só trata quadros com texto. Figuras, plantas, fórmulas desenhadas e modelos de
  impressos ficam com a ligação ao PDF.
- A deteção assenta no desenho dos quadros do Diário da República (regra grossa no topo
  e no fecho). Foi testada em PDF de 2007, 2008 e 2020. Noutros desenhos pode não
  detetar nada: usa `--bbox`.
- A verificação garante o conteúdo (palavras), não a posição de cada valor em quadros
  sem regras por linha. A conferência com a imagem não é opcional.
- Quadros que continuam noutra página sem repetir o cabeçalho não se juntam
  automaticamente.
- O `historico.py` diz qual o último ato que alterou o **artigo**. Não sabe se esse ato
  mexeu no quadro: é o `INALTERADO` do `tabelas.py` que o confirma.
