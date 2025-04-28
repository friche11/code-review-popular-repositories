# Relatório Final

## Introdução

Neste estudo, analisamos pull requests (PRs) dos 200 repositórios mais populares do GitHub, que possuem pelo menos 100 PRs com status "merged" e "closed". Para garantir a relevância dos dados, foram selecionados apenas PRs com status merged ou closed com pelo menos uma revisão com duração superior a uma hora. O objetivo é entender como diferentes características dos PRs, como tamanho, tempo de análise, descrição e interações, se relacionam com o feedback final das revisões e o número de revisões realizadas.

## Hipóteses Iniciais

#### RQ 01. Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
  _É provável que PRs maiores têm maior probabilidade de serem rejeitados, devido à complexidade e ao número de pontos que podem ser questionados durante a revisão._

#### RQ 02. Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
  _É provável que PRs que levam mais tempo para serem analisados têm maior probabilidade de serem aceitos (merged), pois o processo de revisão pode indicar mais detalhamento e melhorias no código antes da aprovação final._

#### RQ 03. Qual a relação entre a descrição dos PRs e o feedback final das revisões?
  _É provável que PRs com descrições mais detalhadas têm maior chance de serem aceitos (merged), pois a clareza na descrição facilita a compreensão das mudanças e pode reduzir dúvidas durante o processo de revisão._

#### RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?
  _É provável que PRs com mais interações (comentários e participantes) têm maior chance de serem aceitos (merged), pois essas interações indicam que os revisores estão mais envolvidos no processo de validação do código, o que pode resultar em melhorias mais significativas antes da aprovação final._

#### RQ 05. Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
  _É provável que PRs maiores tendem a passar por mais revisões, já que a complexidade maior exige mais revisores ou revisões para garantir que todas as mudanças sejam verificadas corretamente._

#### RQ 06. Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
  _É provável que PRs com maior tempo de análise provavelmente passaram por mais revisões, já que os revisores podem ter dado mais feedback ou sugerido mais mudanças antes de uma decisão final._

#### RQ 07. Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
  _É provável que PRs com descrições mais claras e detalhadas tendem a ter menos revisões, pois os revisores conseguem entender rapidamente o que foi alterado e quais são os objetivos, o que pode acelerar o processo de aprovação._

#### RQ 08. Qual a relação entre as interações nos PRs e o número de revisões realizadas?
  _É provável que PRs com mais interações (comentários e participantes) terão mais revisões realizadas, pois um maior número de participantes envolvidos no processo possivelmente gera mais revisões._

## 2. Metodologia

Para responder às questões de pesquisa, realizamos a coleta e análise de dados dos 200 repositórios mais populares no GitHub, seguindo os seguintes passos:
1. **Coleta dos Repositórios Com Pelo o Menos 100 Pull Requests Com Status (Merged + Closed) :**  
   - Executamos a opção 1 do script principal `main.py` que utiliza a API GraphQL do GitHub para buscar os repositórios com pelo o menos 100 pull requests com status (Merged + Closed).
   - Os resultados foram armazenados em um arquivo `repositories.csv` dentro da pasta `outputs`.
     
2. **Buscar PRs a partir dos repositórios coletados:**
   - Ao executar a opção 2 do script `main.py` os repositórios da planilha `repositories.csv` são lidos e os PRs de cada repositório são coletados, levando em conta apenas os que possuem pelo o menos 1 review de duração maior que 1 hora. Isso porque a intenção é remover do nosso dataset PRs que foram revisados de forma
   automática (por meio de bots ou ferramentas de CI/CD).
   - Os PRs coletados e suas métricas foram armazenados na planilha `pull_requests.csv` dentro da pasta `outputs`.
   - As métricas dos PRs coletados foram:

        | Métrica                | Descrição |
        |------------------------|-----------|
        | **Duração (h)**        | Tempo entre a criação e o fechamento do PR |
        | **Arquivos Modificados** | Número de arquivos alterados |
        | **Linhas Adicionadas** | Total de linhas adicionadas |
        | **Linhas Removidas**   | Total de linhas removidas |
        | **Tamanho da Descrição** | Número de caracteres da descrição do PR |
        | **Qtd Reviews**        | Quantidade de revisões feitas no PR |
        | **Qtd Comentários**    | Número de comentários feitos na discussão |
        | **Qtd Participantes**  | Quantidade de usuários distintos interagindo no PR |
        | **Status**             | Resultado do PR: MERGED ou CLOSED |

3. **Analisar os dados coletados com estatística e gráficos**
   - Ao executar a opção 3 do script `main.py` o código analisa as colunas e linhas da planilha que contém todos os PRs extraídos e analisa por valores medianos a fim de responder as RQs.
   - Gráficos são gerados para cada RQ e a matriz de correlação de Spearman é gerada em um png. Todos eles estão na pasta `docs`.

## Resultados Obtidos com valores medianos

### RQ 01. Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

![rq01](https://github.com/user-attachments/assets/43fb99dc-9ad7-4849-b896-ef5f5a48c134)

PRs fechados (CLOSED) têm, pela mediana:
- 1 arquivo modificado
- 7 linhas adicionadas
- 1 linha removida

PRs mesclados (MERGED) têm, pela mediana:
- 2 arquivos modificados

- 12 linhas adicionadas
- 3 linhas removidas

A hipótese inicial propunha que PRs maiores têm maior probabilidade de serem rejeitados. Esses resultados refutam parcialmente a hipótese inicial. Na prática, PRs maiores (em termos de adições e alterações) foram mais aceitos do que rejeitados.

### RQ 02. Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

![rq02](https://github.com/user-attachments/assets/4f8c663e-dee6-4cd0-aff3-64dad52c2f0b)

A hipótese sugeria que PRs com mais tempo de análise teriam maior chance de serem aceitos (merged).
Os resultados mostram:

Tempo mediano (Duração em horas):
- MERGED: 264.58 horas
- CLOSED: 35.73 horas

Isso confirma a hipótese inicial. PRs que ficaram mais tempo sendo analisados tiveram maior chance de serem aceitos.

### RQ 03. Qual a relação entre a descrição dos PRs e o feedback final das revisões?

![rq03](https://github.com/user-attachments/assets/4de9d7ef-ba28-4377-9ff6-0ff5b2bd960b)

A hipótese previa que descrições mais detalhadas aumentariam as chances de aceitação.
Observamos que:

Tamanho da descrição (número de caracteres medianos):
- MERGED: 287 caracteres
- CLOSED: 236 caracteres

Isso confirma a hipótese inicial: PRs aceitos apresentaram descrições mais longas, sugerindo que explicações mais completas favorecem a compreensão e aprovação do código.

### RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?

![rq04](https://github.com/user-attachments/assets/a830f80f-e84e-4f59-8b43-ffcbd31eb437)

A hipótese previa que PRs com mais interações teriam maior chance de aceitação.
A análise mostrou:

Comentários medianos:
- MERGED: 1 comentários
- CLOSED: 2 comentários

Participantes medianos:

- MERGED: 2 participantes
- CLOSED: 2 participantes

Esses dados refutam a hipótese inicial mas não são significativos o suficiente para indicar uma relação clara entre o volume de interações e a aceitação do PR. PRs que foram fechados (CLOSED) apresentaram ligeiramente mais comentários do que PRs que foram mesclados (MERGED), enquanto o número de participantes foi idêntico em ambos os casos.

### RQ 05. Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

![rq05](https://github.com/user-attachments/assets/a019cc83-e0c8-4ab7-b589-fc79a0a465b0)

A hipótese era de que PRs maiores teriam mais revisões.
Os dados mostram:
- PRs com apenas 1 revisão modificaram, em mediana:
1 arquivo,
8 linhas adicionadas,
2 linhas removidas.
- PRs com 3 ou mais revisões modificaram, em mediana:
3 arquivos,
25 linhas adicionadas,
7 linhas removidas.

À medida que o número de revisões aumenta, os PRs tendem a ficar maiores (mais arquivos modificados, mais linhas adicionadas e removidas).
Esses resultados confirmam a hipótese inicial: PRs maiores geralmente passam por mais revisões antes de serem aprovados.

### RQ 06. Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?

![rq06](https://github.com/user-attachments/assets/c1561ac3-8626-44a0-a276-729cc7f77f96)

A hipótese era de que PRs com maior tempo de análise provavelmente passaram por mais revisões.

Os dados mostram que:
- PRs com apenas 1 revisão levaram em mediana 42 horas para serem analisados.
- PRs com 3 ou mais revisões levaram em mediana 310 horas para serem analisados.

Esses resultados confirmam a hipótese inicial: quanto maior o número de revisões, maior o tempo total de análise do PR.

### RQ 07. Qual a relação entre a descrição dos PRs e o número de revisões realizadas?

![rq07](https://github.com/user-attachments/assets/b40242aa-fd6e-4b54-823b-da75588b8958)

A hipótese era de que PRs com descrições mais claras e detalhadas tendem a ter menos revisões.
Os dados mostram que:

PRs com mais revisões tendem a ter descrições maiores.
Exemplo: 
- PRs com 1 revisão tinham descrições em torno de 250 caracteres.
- PRs com 3 ou mais revisões tinham descrições acima de 300 caracteres.

Esses resultados refutam a hipótese inicial:
PRs mais complexos, que naturalmente exigem mais revisões, também tendem a ter descrições maiores.
Isso indica que descrições detalhadas são uma necessidade para PRs complicados, mas não necessariamente reduzem o número de revisões.

### RQ 08. Qual a relação entre as interações nos PRs e o número de revisões realizadas?

![rq08](https://github.com/user-attachments/assets/46aa55a0-57a6-4a27-821e-03bf859ac331)

A hipótese era de que PRs com mais interações (comentários e participantes) terão mais revisões realizadas.

Os dados mostram que:
- PRs com apenas 1 revisão tiveram em mediana:
1 comentário,
2 participantes.
- PRs com 3 ou mais revisões tiveram em mediana:
4 comentários,
3 participantes.

Esses dados confirmam a hipótese inicial: à medida que o número de revisões aumenta, o número de comentários e participantes também cresce, indicando revisões mais colaborativas e complexas.

## Resultados com teste estatístico de Spearman

Decidimos adotar Spearman porque os dados a serem analisados têm muita variação e outliers. Spearman é mais seguro porque ele se baseia apenas nas posições relativas dos valores, e não nos valores em si.

O Estado(merged ou closed) foi transformado em 0 e 1 para ser incluído na correlação.

MERGED → 1

CLOSED → 0

![correlacao_spearman](https://github.com/user-attachments/assets/9a3f2ca9-2c45-416a-aa40-532e7f43a905)

### RQ 01. Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

- **Resultados**:
  - **Arquivos Modificados vs. Estado_num**: Correlação = 0.11
  - **Linhas Adicionadas vs. Estado_num**: Correlação = 0.06
  - **Linhas Removidas vs. Estado_num**: Correlação = 0.14

  As correlações são positivas, mas muito fracas (entre 0.06 e 0.14).
  - PRs maiores (mais arquivos ou linhas) têm uma leve tendência a serem aceitos (MERGED), especialmente quando há mais linhas removidas (correlação de 0.14), mas a relação é quase insignificante.

### RQ 02. Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

- **Resultado**:
  - **Duração (h) vs. Estado_num**: Correlação = -0.29

  A correlação é negativa e fraca (-0.29).
  - PRs com maior tempo de análise têm uma leve tendência a serem rejeitados (CLOSED). Isso pode indicar que PRs que levam mais tempo para revisar enfrentam mais problemas ou discussões, resultando em rejeições.

### RQ 03. Qual a relação entre a descrição dos PRs e o feedback final das revisões?

- **Resultado**:
  - **Tamanho Descrição vs. Estado_num**: Correlação = 0.06

  A correlação é positiva, mas praticamente nula (0.06).
  - O tamanho da descrição do PR não parece influenciar significativamente o feedback final.
  - Descrições mais longas não aumentam nem diminuem a chance de um PR ser aceito ou rejeitado de forma relevante.

### RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?

- **Resultados**:
  - **Comentários vs. Estado_num**: Correlação = -0.16
  - **Participantes vs. Estado_num**: Correlação = -0.15
    
  Ambas as correlações são negativas e fracas (-0.16 e -0.15).
  - PRs com mais interações (mais comentários ou participantes) têm uma leve tendência a serem rejeitados (CLOSED). Isso pode indicar que PRs com mais discussões ou envolvidos enfrentam mais problemas ou controvérsias.

### RQ 05. Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

- **Resultados**:
  - **Arquivos Modificados vs. Revisões**: Correlação = 0.20
  - **Linhas Adicionadas vs. Revisões**: Correlação = 0.25
  - **Linhas Removidas vs. Revisões**: Correlação = 0.14
  
  As correlações são positivas e fracas (entre 0.14 e 0.25).
  - PRs maiores (mais arquivos ou linhas) tendem a ter um pouco mais de revisões, especialmente quando há mais linhas adicionadas (correlação de 0.25).
  - Isso sugere que PRs maiores ou mais complexos podem demandar mais atenção dos revisores, resultando em mais revisões.

### RQ 06. Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?

- **Resultado**:
  - **Duração (h) vs. Revisões**: Correlação = 0.14

  A correlação é positiva, mas muito fraca (0.14).
  - PRs com maior tempo de análise têm uma leve tendência a receber mais revisões, possivelmente devido a iterações adicionais durante a análise.

### RQ 07. Qual a relação entre a descrição dos PRs e o número de revisões realizadas?

- **Resultado**:
  - **Tamanho Descrição vs. Revisões**: Correlação = 0.11

  A correlação é positiva, mas muito fraca (0.11).
  - Descrições mais longas levam a mais revisões.

### RQ 08. Qual a relação entre as interações nos PRs e o número de revisões realizadas?

- **Resultados**:
  - **Comentários vs. Revisões**: Correlação = 0.27
  - **Participantes vs. Revisões**: Correlação = 0.58

  As correlações são positivas e variam de fracas a moderadas (0.27 para Comentários, 0.58 para Participantes).
  - PRs com mais participantes têm uma associação mais forte com mais revisões (correlação de 0.58), indicando que a presença de mais pessoas (ex.: revisores) leva a mais iterações.
  - Mais comentários também estão associados a mais revisões, mas a relação é mais fraca (0.27).
  - Isso sugere que o envolvimento de mais participantes é um fator mais relevante para o aumento do número de revisões do que o número de comentários.

## Comparação entre Métodos

Este estudo analisou pull requests (PRs) de repositórios populares do GitHub utilizando dois métodos complementares: análise de valores medianos e correlação de Spearman. Ambos os métodos forneceram insights sobre as relações entre características dos PRs (tamanho, tempo de análise, descrição e interações) e os desfechos das revisões (feedback final e número de revisões), mas apresentaram diferenças e semelhanças significativas em suas conclusões.

### Semelhanças entre os Métodos
Ambos os métodos confirmaram algumas hipóteses e refutaram outras de maneira consistente. Para a **RQ 05** (tamanho dos PRs e número de revisões), tanto os valores medianos quanto a correlação de Spearman indicaram que PRs maiores tendem a ter mais revisões, com medianas mostrando aumentos claros (ex.: de 1 para 3 arquivos modificados) e Spearman apontando correlações positivas fracas (0.14 a 0.25). Da mesma forma, na **RQ 06** (tempo de análise e número de revisões), ambos os métodos identificaram uma relação positiva, com valores medianos mostrando tempos maiores para PRs com mais revisões (42h para 1 revisão vs. 310h para 3+ revisões) e Spearman indicando uma correlação fraca (0.14). Para a **RQ 08** (interações e número de revisões), os dois métodos confirmaram a hipótese inicial, com medianas mostrando mais comentários e participantes em PRs com mais revisões (ex.: 4 comentários e 3 participantes para 3+ revisões) e Spearman destacando correlações positivas, especialmente forte para participantes (0.58).

### Diferenças entre os Métodos
Os métodos divergiram em algumas RQs, refletindo suas abordagens distintas. A análise de valores medianos foca em diferenças centrais entre grupos (ex.: MERGED vs. CLOSED), enquanto Spearman captura relações monotônicas em todo o dataset, sendo mais robusto a outliers. Para a **RQ 01** (tamanho dos PRs e feedback final), os valores medianos refutaram a hipótese inicial ao mostrar que PRs aceitos (MERGED) eram ligeiramente maiores (ex.: 12 linhas adicionadas vs. 7 para CLOSED), sugerindo que PRs maiores têm maior chance de aceitação. No entanto, Spearman mostrou correlações muito fracas (0.06 a 0.14), indicando que o tamanho tem impacto quase nulo no feedback final. Essa diferença sugere que, embora a mediana revele uma tendência em grupos específicos, a relação geral não é forte o suficiente para ser capturada por Spearman.

Na **RQ 02** (tempo de análise e feedback final), os valores medianos confirmaram a hipótese inicial, mostrando que PRs aceitos têm tempos de análise muito maiores (264.58h vs. 35.73h para CLOSED), sugerindo que mais tempo leva a aceitação. Em contrapartida, Spearman indicou uma correlação negativa fraca (-0.29), sugerindo que tempos maiores estão associados a rejeições. Essa discrepância pode ser explicada por outliers: a mediana é menos sensível a valores extremos (ex.: PRs com durações muito longas), enquanto Spearman considera a ordenação de todos os dados, possivelmente capturando casos em que tempos longos refletem problemas que levam à rejeição.

Para a **RQ 03** (descrição e feedback final), os valores medianos confirmaram a hipótese (287 caracteres para MERGED vs. 236 para CLOSED), enquanto Spearman mostrou uma correlação quase nula (0.06), indicando que o tamanho da descrição não tem impacto relevante. Novamente, a mediana destaca diferenças entre grupos, mas Spearman revela que essa relação não é consistente em todo o dataset. Na **RQ 04** (interações e feedback final), os valores medianos mostraram pouca diferença (1 comentário para MERGED vs. 2 para CLOSED, 2 participantes em ambos), refutando a hipótese, enquanto Spearman indicou uma leve tendência de rejeição com mais interações (-0.16 e -0.15), alinhando-se parcialmente com os valores medianos, mas com maior clareza na direção da relação.

Na **RQ 07** (descrição e número de revisões), os valores medianos refutaram a hipótese ao mostrar que descrições maiores estão associadas a mais revisões (250 caracteres para 1 revisão vs. 300+ para 3+ revisões), enquanto Spearman indicou uma correlação muito fraca (0.11), sugerindo impacto quase nulo. A mediana capturou uma tendência mais clara em grupos específicos, mas Spearman diluiu essa relação ao considerar todo o dataset.

### Implicações e Considerações
Os valores medianos fornecem uma visão mais direta das diferenças entre grupos (ex.: MERGED vs. CLOSED, 1 revisão vs. 3+ revisões), sendo úteis para identificar tendências práticas. No entanto, eles podem mascarar variações dentro dos dados e são menos robustos para capturar relações gerais, especialmente em datasets com outliers. Spearman, por outro lado, oferece uma análise mais abrangente e robusta a outliers, mas suas correlações fracas (abaixo de 0.3 na maioria dos casos) indicam que as variáveis analisadas têm influência limitada nos desfechos. A correlação mais forte (0.58 para Participantes vs. Revisões) foi consistente em ambos os métodos, destacando a importância do envolvimento colaborativo no processo de revisão.

### Conclusão
A análise mostrou que o tamanho dos pull requests, o tempo de duração, a descrição e a quantidade de interações têm pouca influência no número de revisões e no feedback final. A única característica que demonstrou um impacto consistente foi o número de participantes: quanto mais participantes, maior o número de revisões.

Comparando os métodos, a análise usando valores medianos foi mais útil para identificar diferenças práticas entre os grupos, enquanto a correlação de Spearman confirmou que, no geral, não existem relações fortes entre as variáveis analisadas.

Para trabalhos futuros, seria interessante utilizar testes estatísticos, como p-valores, para avaliar a significância das correlações encontradas.


