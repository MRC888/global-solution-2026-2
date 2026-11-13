# Algoritmo — Neighborhood Action Dashboard

## Objetivo

Organizar demandas comunitárias fictícias da Vila Esperança com fundamentos de programação em Python. Cada ocorrência possui código único, categoria, descrição, local genérico, dia simulado e situação atual. O sistema permite cadastrar, consultar, acompanhar mudanças e interpretar indicadores.

## 1. Entrada e validação

1. O programa verifica se existem arquivos de uma sessão anterior e oferece retomá-los ou carregar a base fictícia original.
2. Lê `data/ocorrencias.csv` e `data/historico.csv` (ou a sessão escolhida), em UTF-8, usando `;` como separador.
3. Para cada ocorrência, valida identificador, categoria, descrição, localidade, dia simulado e status.
4. Mantém os registros válidos nas estruturas de dados. Registros inconsistentes são separados com os motivos, sem entrar nos indicadores.
5. Carrega eventos de histórico vinculados a ocorrências válidas.

## 2. Estruturas utilizadas

| Estrutura | Papel no algoritmo |
|---|---|
| Lista | Percorrer todas as ocorrências e calcular indicadores |
| Dicionário | Localizar um código de ocorrência diretamente |
| Fila | Organizar triagem das ocorrências abertas por ordem de registro |
| Pilha | Recuperar a última mudança de status da sessão para desfazer |
| Hierarquia | Navegar por bairro → categoria → ocorrências |
| Matriz | Contar ocorrências por categoria × situação |
| Histórico | Registrar eventos de acompanhamento, preservando alterações e desfazimentos |

## 3. Cadastro

1. Solicita a descrição, com até 120 caracteres e sem ponto e vírgula.
2. Sugere uma categoria a partir de palavras-chave da descrição, com confirmação pelo usuário.
3. Solicita uma das localidades genéricas e o dia simulado entre 1 e 30.
4. Avisa quando já existe uma ocorrência possivelmente duplicada na mesma categoria e local.
5. Gera um novo identificador único e atribui a situação inicial `aberta`.
6. Se os dados forem válidos, insere o registro na lista, dicionário, hierarquia, matriz e fila.
7. Salva a sessão local automaticamente, preservando os arquivos CSV originais.

## 4. Consulta

- A busca por código utiliza o dicionário de ocorrências.
- A listagem percorre a lista de registros válidos.
- O filtro por categoria e situação usa a expressão:

```python
(categoria == "" or oc["categoria"] == categoria) and (status == "" or oc["status"] == status)
```

Um filtro em branco representa todas as opções; quando ambos são preenchidos, a ocorrência precisa satisfazer os dois.

## 5. Triagem e acompanhamento

A sequência de situações é `aberta → em_analise → concluida`. O programa rejeita situações desconhecidas, mudanças para a situação atual e saltos entre etapas.

A triagem utiliza uma fila: ocorrências abertas entram no final e são examinadas pela ordem de registro. Cada mudança válida atualiza a ocorrência e a matriz, registra um evento no histórico e entra na pilha de desfazimento. O desfazer registra um novo evento, sem apagar o histórico, e restaura a situação anterior. O estado alterado é salvo automaticamente em `data/saida/`.

## 6. Inconsistências

Registros com problemas não entram nos totais. A opção de correção solicita apenas os campos identificados como inválidos. A nova versão passa outra vez pela validação antes de entrar nas estruturas e nos indicadores.

## 7. Indicadores

Com laços e operações básicas, o sistema calcula totais e proporções por categoria e status, quantidade de pendências, tempo médio até a conclusão, tempo simulado em aberto por categoria e ranking de prioridade. A matriz resume a contagem categoria × status.

A fórmula de proporção é `(parte ÷ total) × 100`. O tempo médio até a conclusão é a soma de `dia_de_conclusao − dia_de_abertura` dividida pelo número de ocorrências concluídas com histórico válido. O ranking considera `dias_em_aberto × peso_da_categoria`; os pesos são critérios simulados definidos para o protótipo, não uma classificação oficial.

## 8. Saída e interface

A interface textual usa opções numeradas, mensagens de validação e um modo acessível que não depende de cores e pode solicitar confirmações antes de alterar dados. O gerador HTML monta, em Python, as páginas de indicadores a partir dos dados atuais da sessão e as grava em `data/saida/painel/`; o mapa bônus usa JavaScript local só para fichas, filtros, arraste e zoom. O formulário HTML apresenta os campos do cadastro, mas não envia dados; o cadastro funcional acontece no terminal.

## 9. Limitações

Os dados e dias são simulados. A aplicação não integra órgãos públicos, não encaminha demandas e não promete atendimento. O HTML gerado é uma fotografia da sessão em que foi produzido. A persistência acontece em arquivos CSV locais na pasta `data/saida/`, que não integra o versionamento do Git.

## 10. Decisões tomadas

O código cita estas decisões pelo número (por exemplo, "D7" em `src/operacoes.py`). A coluna "Escolha" é o que foi implementado.

| # | Pergunta | Opções | Escolha |
|---|---|---|---|
| D1 | Como representar a data? | (a) dia 1–30; (b) data real dd/mm | (a): a conta de tempo vira uma subtração simples |
| D2 | Formato da hierarquia | (a) bairro → categoria → ocorrências; (b) bairro → local → categoria → ocorrências | (a), como no edital |
| D3 | Menu | (a) 12 opções diretas; (b) submenus | (a), para a banca ver tudo de uma vez |
| D4 | Transições permitidas | (a) só aberta → em análise → concluída; (b) também aberta → concluída; (c) também reabrir uma concluída | (a) + desfazer para corrigir engano |
| D5 | Código no cadastro | (a) automático; (b) digitado e validado | (a): evita código repetido |
| D6 | Desfazer e histórico | (a) apaga o último evento; (b) registra um evento "desfeito" | (b): o histórico nunca perde informação |
| D7 | Fila na triagem e no desfazer | Volta para o começo ou para o fim da fila? | Começo: mantém a ordem de chegada |
| D8 | Tratar as inconsistências | (a) correção pelo menu; (b) automática na carga; (c) as duas | (a): a carga só detecta; a correção é pelo menu, com sugestão |
| D9 | Modo acessível | (a) perguntar ao abrir; (b) só pelo menu | (a) + opção no menu |
| D10 | Salvar | (a) sobrescrever os CSVs; (b) gravar em outros arquivos e manter os originais | (b): o vídeo e os testes sempre partem dos mesmos dados |
| D11 | Conclusão do painel | (a) frase gerada por regra; (b) texto fixo no README | (a) no painel + (b) no README |
| D12 | Pesos do score de prioridade | Quais pesos e por quê? | Acessibilidade 3, iluminação 2 (segurança à noite), conservação 2, limpeza 1 |
| D13 | Dados | Manter as 18 ocorrências propostas e a história da acessibilidade na UBS? | Mantidas |
| D14 | Divisão de tarefas | Quem faz o quê? | Tabela da equipe no `CLAUDE.md` da raiz |
