# Relatório Parcial – Lab03S02

## 1. Introdução

Neste relatório, apresentamos as hipóteses iniciais para a investigação sobre fatores que influenciam o processo de *code review* em repositórios populares no GitHub.

Hipotetizamos que:

- PRs maiores, com mais arquivos modificados e linhas alteradas, tendem a receber mais revisões e levar mais tempo para serem aprovados ou rejeitados.
- PRs com descrições mais completas e detalhadas podem ter maior chance de aceitação.
- Um maior número de comentários e participantes nas discussões está relacionado à aprovação do PR ou a revisões mais aprofundadas.

## 2. Metodologia

Utilizamos a API GraphQL do GitHub para extrair Pull Requests dos 200 repositórios mais populares da plataforma. Os PRs foram coletados seguindo os critérios abaixo:

- Status: MERGED ou CLOSED
- Contar com ao menos uma revisão manual (`reviews.totalCount > 0`)
- Ter duração superior a uma hora entre a criação e o merge/fechamento (`createdAt` → `mergedAt` ou `closedAt`)

A coleta foi feita através de um script Python (`main.py`) que utiliza a query GraphQL (`query_prs.gql`) e salva os dados no arquivo `pull_requests.csv`.

## 3. Métricas Coletadas

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

## 4. Considerações Finais (até aqui)

Com os dados coletados, daremos sequência à análise estatística para responder às RQs do laboratório, utilizando testes de correlação como Spearman ou Pearson. Esta versão representa a entrega parcial Lab03S02 com dataset completo e hipóteses iniciais estruturadas.
