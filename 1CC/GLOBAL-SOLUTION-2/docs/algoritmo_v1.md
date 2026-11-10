# Algoritmo v1 — Neighborhood Action Dashboard (Vila Esperança)

> **Rascunho para a reunião da equipe.** Nada aqui é definitivo. Anotem, risquem e mudem. Só depois de fechado este algoritmo é que o código começa.
>
> Como ler: cada passo diz **o que** o sistema faz, **como** (em português, sem código) e **por quê**. Os pontos marcados com **❓ D1, D2…** são decisões para a reunião e estão reunidos na seção 12.

---

## 1. Visão geral

O sistema é um painel no terminal. Uma associação de moradores fictícia registra e acompanha problemas do bairro.

Todo o programa segue o mesmo caminho:

```
ENTRADA                  REGRA                         SAÍDA
(CSV ou teclado)   →     (validar, decidir com if)  →  (tabela, painel, mensagem)
```

Ciclo de vida de uma ocorrência:

```
  [cadastro] → ABERTA ──(triagem: examinada)──→ EM ANÁLISE ──(resolvida)──→ CONCLUÍDA
                 │                                                ▲
                 └──────────── ❓ D4: pode pular direto? ─────────┘
```

---

## 2. Dados de entrada (proposta)

Proposta para a reunião. Os arquivos de dados ainda **não** entraram neste repositório: serão criados depois que a equipe aprovar o formato (❓ D13).

- **Ocorrência** = id, categoria, descrição, local, dia de abertura, status.
- **Evento do histórico** = id, dia, status anterior, status novo, observação.
- **Valores padronizados:**
  - categorias: `iluminacao`, `acessibilidade`, `limpeza`, `conservacao`;
  - status: `aberta`, `em_analise`, `concluida`;
  - locais: Entorno da UBS, Entorno da Escola, Praça Central, Ponto de Ônibus.
- **Tempo:** dias de 1 a 30; "hoje" = dia 30. ❓ D1
- **Dados de propósito:** 16 ocorrências válidas e 2 inconsistentes (017 sem categoria; 018 com status `resolvido`).

---

## 3. Estruturas de dados (para que serve cada uma)

| Estrutura | O que guarda | Por que esta estrutura | Onde é usada |
|---|---|---|---|
| **Lista** `ocorrencias` | Todas as ocorrências válidas | Precisa ser percorrida inteira: listar, filtrar, contar | Listagem, filtros, indicadores |
| **Dicionário** `por_id` | id → ocorrência | Acha uma ocorrência direto pelo código, sem percorrer a lista | Buscar, atualizar |
| **Fila** `fila_triagem` | ids com status `aberta`, por ordem de registro | Quem chegou primeiro é examinado primeiro (como senha de banco) | "Chamar próxima" |
| **Pilha** `pilha_alteracoes` | As últimas mudanças de status | A última mudança é a primeira a ser desfeita | "Desfazer" e "eventos recentes" |
| **Hierarquia** `bairro` | Bairro → categoria → lista de ids | Organiza o bairro como uma árvore e permite navegar por partes | Menu "explorar o bairro" |
| **Matriz** `matriz` | Linhas = categorias, colunas = status, célula = quantidade | Mostra o cruzamento de duas informações em uma tabela | Painel e mapa de calor |
| **Lista** `inconsistentes` | Registros com problema + motivo | Separa o que não pode entrar nos números | Relatório de inconsistências |
| **Lista** `historico` | Todos os eventos, em ordem | Registro permanente, que só cresce | Tempo até a conclusão, consulta do histórico |

**Pilha × histórico:** o histórico guarda **tudo** para sempre. A pilha guarda só as mudanças **desta sessão**, para poder desfazer. ❓ D6

**Fila e pilha** são feitas com lista comum, como na Fase 2:
- a fila entra no fim com `append` e sai do começo com `pop(0)`;
- a pilha entra no topo com `append` e sai do topo com `pop()`.

❓ D2: a hierarquia é bairro → **categoria** → ocorrências (como no edital) ou bairro → **local** → categoria → ocorrências?

---

## 4. Passo a passo ao abrir o programa

1. **Mostrar a abertura:** nome do bairro e pergunta "Usar modo acessível? (s/n)". ❓ D9
2. **Ler `ocorrencias.csv` linha por linha.** Para cada linha:
   1. separar os campos pelo `;`;
   2. **validar** (seção 6.1);
   3. se estiver válida, guardar em `ocorrencias` e em `por_id`;
   4. se não estiver, guardar em `inconsistentes`, junto com o motivo.
3. **Ler `historico.csv`**, guardar em `historico` e conferir se cada evento aponta para um id que existe.
4. **Montar as estruturas** a partir de `ocorrencias`:
   1. fila = ids com status `aberta`, em ordem crescente de id;
   2. hierarquia = percorrer a lista e encaixar cada id na sua categoria;
   3. matriz = começa com zeros; para cada ocorrência, somar 1 na linha da categoria e na coluna do status.
5. **Mostrar o relatório de carga**, por exemplo: "18 registros lidos, 16 válidos, 2 inconsistentes" e a lista dos problemas encontrados.
6. **Ir para o menu principal.**

---

## 5. Menu principal (proposta)

```
 1. Listar todas as ocorrências
 2. Buscar por código
 3. Filtrar por categoria e/ou status
 4. Cadastrar nova ocorrência
 5. Triagem: chamar a próxima da fila
 6. Atualizar status
 7. Desfazer a última alteração
 8. Ver histórico / eventos recentes
 9. Explorar o bairro (hierarquia)
10. Painel de indicadores
11. Inconsistências (ver e corrigir)
12. Alternar modo acessível
 0. Salvar e sair
```

❓ D3: 12 opções é muito? Alternativa: agrupar em submenus (Consultar / Alterar / Painel).

**Regra do menu:**
- ler a opção como texto;
- se não for uma das opções válidas, mostrar "Opção inválida, digite um número de 0 a 12" e mostrar o menu de novo;
- o programa **nunca fecha por erro de digitação**.

---

## 6. Algoritmo de cada operação

### 6.1 Validar um registro (usada na carga, no cadastro e na correção)
1. Se o id estiver vazio **ou** já existir em `por_id`, o registro é inválido: "código ausente ou repetido".
2. Se a categoria **não** estiver na lista de categorias, é inválido: "categoria ausente ou desconhecida".
3. Se o status **não** estiver na lista de status, é inválido: "status desconhecido".
4. Se a descrição **ou** o local estiverem vazios, é inválido: "campo obrigatório vazio".
5. Se o dia **não** for um número **ou** estiver fora de 1 a 30, é inválido: "dia fora do período".
6. Se passou por tudo, o registro é válido.

Todas as verificações rodam, e o registro recebe **todos** os motivos, não só o primeiro. Exemplo: "017: categoria ausente".

### 6.2 Listar (opção 1)
1. Se a lista estiver vazia, mostrar "Nenhuma ocorrência cadastrada".
2. Senão, mostrar uma tabela com código, categoria, local e status, uma linha por ocorrência.
3. No rodapé, mostrar o total exibido.

### 6.3 Buscar por código (opção 2)
1. Pedir o código e completar com zeros à esquerda: "14" vira "014".
2. Se o código **não** estiver em `por_id`, mostrar "Ocorrência 014 não encontrada".
3. Senão, mostrar a ficha completa e o histórico daquela ocorrência.

### 6.4 Filtrar (opção 3)
1. Pedir a categoria (Enter = todas) e o status (Enter = todos).
2. Se o valor digitado não for vazio **e** não for válido, avisar e pedir de novo.
3. Percorrer a lista e mostrar só as ocorrências que passam na condição:
   `(categoria escolhida vazia OU categoria igual) E (status escolhido vazio OU status igual)`
4. Se nenhuma passar, mostrar "Nenhuma ocorrência com esses filtros".

### 6.5 Cadastrar (opção 4)
1. Gerar o id automaticamente: maior id + 1, com 3 dígitos. ❓ D5
2. Pedir a descrição.
3. *(diferencial)* Sugerir uma categoria pelas palavras da descrição (seção 9).
4. Pedir a categoria (lista numerada), o local (lista numerada) e o dia.
5. O status começa sempre como `aberta`.
6. Validar (6.1). Se houver erro, mostrar o motivo e pedir só o campo errado de novo.
7. *(diferencial)* Se já houver ocorrência com a mesma categoria **e** o mesmo local **e** ainda não concluída, avisar que pode ser duplicada e perguntar se quer cadastrar mesmo assim.
8. Guardar na lista, no dicionário, na hierarquia, na matriz **e no fim da fila**.
9. Mostrar "Ocorrência 019 cadastrada e colocada na fila (posição N)".

### 6.6 Triagem: chamar a próxima (opção 5)
1. Se a fila estiver vazia, mostrar "Nenhuma ocorrência aguardando triagem".
2. Senão, tirar o **primeiro** id da fila e mostrar a ficha.
3. Perguntar "Marcar como em análise? (s/n)".
4. Se a resposta for "s", fazer a mudança de status (6.7) para `em_analise`.
5. Se for "n", devolver o id para o começo da fila. ❓ D7

### 6.7 Atualizar status (opção 6) — o coração do sistema
1. Pedir o código. Se não existir, mostrar "não encontrada" e voltar.
2. Mostrar o status atual e pedir o novo.
3. Verificar a transição:
   1. se o novo status **não** for válido, mostrar "Status desconhecido";
   2. senão, se o novo for **igual** ao atual, mostrar "A ocorrência já está nesse status";
   3. senão, se o atual for `concluida`, mostrar "Ocorrência concluída não pode mudar" ❓ D4;
   4. senão, se a transição não for permitida, mostrar "Transição não permitida" ❓ D4;
   5. senão, a mudança é aceita.
4. Se a mudança foi aceita:
   1. pedir uma observação curta (opcional);
   2. mudar o status na ocorrência;
   3. criar o evento (id, dia, anterior, novo, observação), colocá-lo no **histórico** e **empilhá-lo na pilha**;
   4. atualizar a matriz: −1 na coluna do status antigo e +1 na do novo;
   5. se a ocorrência saiu de `aberta`, tirá-la da fila;
   6. mostrar "014: aberta → em análise. Registrado no histórico."

### 6.8 Desfazer (opção 7)
1. Se a pilha estiver vazia, mostrar "Nada para desfazer".
2. Senão, tirar o **topo** da pilha (a última mudança).
3. Voltar a ocorrência para o status anterior.
4. Ajustar a matriz e a fila: se voltou para `aberta`, recolocar na fila. ❓ D7
5. No histórico: ❓ D6
   - opção A: apagar o último evento;
   - opção B: registrar um novo evento "desfeito".
6. Mostrar "Desfeito: 014 voltou para aberta".

### 6.9 Histórico (opção 8)
1. Mostrar os últimos N eventos, do mais recente ao mais antigo (é a leitura da pilha **sem tirar nada**).
2. Opção de ver o histórico completo de uma ocorrência.

### 6.10 Explorar o bairro (opção 9)
1. Mostrar a árvore: Vila Esperança → cada categoria, com a quantidade.
2. A pessoa escolhe uma categoria e vê as ocorrências dela.
3. A pessoa escolhe uma ocorrência e vê a ficha.
4. Em qualquer nível, "0" volta um nível.

### 6.11 Inconsistências (opção 11)
1. Mostrar cada registro inconsistente com o motivo.
2. Perguntar se quer corrigir.
3. Se quiser, pedir só os campos com problema e validar de novo (6.1).
4. Se ficou válido, tirar o registro de `inconsistentes` e colocá-lo nas estruturas, como no cadastro.

❓ D8: a correção é pelo menu (sugerido) ou automática na carga? Exemplo de correção automática: `resolvido` → `concluida`; categoria vazia → categoria sugerida pelas palavras.

### 6.12 Salvar e sair (opção 0)
1. Gravar as ocorrências e o histórico nos CSVs. ❓ D10
2. Mostrar o resumo da sessão: N cadastros e N mudanças.
3. Encerrar.

---

## 7. Regras lógicas com `and`, `or` e `not`

O edital pede pelo menos 3 condições distintas e uma delas documentada no README.

| # | Onde | Condição (em português) | Operadores |
|---|---|---|---|
| L1 | Validação (6.1) | descrição vazia **ou** local vazio → inválido | `or` |
| L2 | Validação (6.1) | **não** é número **ou** está fora de 1 a 30 → dia inválido | `not`, `or` |
| L3 | Filtro (6.4) | (sem filtro de categoria **ou** categoria igual) **e** (sem filtro de status **ou** status igual) | `or`, `and` |
| L4 | Transição (6.7) | status válido **e** diferente do atual **e** **não** concluída → muda | `and`, `not` |
| L5 | Duplicada (6.5) | mesma categoria **e** mesmo local **e** **não** concluída → aviso | `and`, `not` |
| L6 | Pendente (indicadores) | **não** concluída → é pendência | `not` |

**Sugestão para o README:** a L3 (filtro), com tabela-verdade, porque liga direto com a lógica booleana da Fase 3, Cap 2.

---

## 8. Indicadores (painel, opção 10)

Para cada indicador, o painel mostra **os dados de origem, a fórmula e o resultado**, como pede o edital.

| # | Indicador | Fórmula | Resultado com os dados propostos |
|---|---|---|---|
| I1 | Total por categoria | contar as ocorrências de cada categoria | 5 / 4 / 3 / 4 |
| I2 | Proporção por categoria | total da categoria ÷ total geral × 100 | 31,25% / 25% / 18,75% / 25% |
| I3 | Total e proporção por status | idem, por status | 6 (37,5%) / 4 (25%) / 6 (37,5%) |
| I4 | Matriz categoria × status | célula [categoria][status] | tabela 4 × 3 |
| I5 | Pendências | abertas + em análise | 10 |
| I6 | Tempo médio até a conclusão | Σ(dia da conclusão − dia de abertura) ÷ nº de concluídas | 32 ÷ 6 = 5,33 dias |
| I7 | Dias em aberto das pendentes, por categoria | Σ(30 − dia de abertura) ÷ nº de pendentes | acessibilidade 24,67 |

- **Dia da conclusão:** vem do histórico, no evento cuja coluna `status_novo` é `concluida`.
- **Conclusão escrita:** a frase final é gerada por regra (`if`). Exemplo: "A categoria com mais tempo em aberto é acessibilidade (24,7 dias), concentrada no Entorno da UBS". ❓ D11

**Visual (diferencial):** barras em ASCII por categoria e mapa de calor da matriz. No modo acessível, só números e texto.

---

## 9. Diferenciais (só depois que o obrigatório estiver pronto)

| Diferencial | Como funciona | Status |
|---|---|---|
| Score de prioridade | `dias em aberto × peso da categoria`. Pesos sugeridos: acessibilidade 3, iluminação 2, conservação 2, limpeza 1 | ❓ D12 |
| Sugestão de categoria | Procura palavras na descrição: "poste", "lâmpada", "escuro" → iluminação; "rampa", "calçada", "piso" → acessibilidade; "lixo", "entulho" → limpeza; "banco", "brinquedo", "muro" → conservação | ideia |
| Duplicadas | Regra L5 | ideia |
| Terminal colorido | Códigos ANSI (sem biblioteca) com cor por status, barras e mapa de calor | ideia |
| Modo acessível | Sem cores nem símbolos, frases explicativas e confirmação antes de cada ação | ideia |
| Testes | `assert` comparando com os resultados calculados à mão | ideia |

---

## 10. Arquivos do código (proposta)

| Arquivo | Responsabilidade | Quem (sugestão) |
|---|---|---|
| `src/sistema.py` | Ponto de entrada e menu | Marcelo |
| `src/dados.py` | Ler e salvar os CSVs | Marcelo |
| `src/estruturas.py` | Montar a lista, o dicionário, a fila, a pilha, a hierarquia e a matriz | Marcelo |
| `src/validacao.py` | Seção 6.1, regras L1–L5, transições | Integrante 2 |
| `src/operacoes.py` | Buscar, filtrar, cadastrar, atualizar, desfazer, triagem | Marcelo + Integrante 2 |
| `src/indicadores.py` | I1–I7, conclusão, score | Integrante 2 |
| `src/interface.py` | Tabelas, cores, barras, mapa de calor, modo acessível | Integrante 3 |
| `tests/` | Testes com `assert` | todos |

Os módulos e o `import` entre arquivos foram ensinados na Fase 3, Cap 3. **`try/except` não foi ensinado**, então as entradas são validadas com `if`.

---

## 11. Ordem de construção (depois da reunião)

1. Carga + validação + estruturas (seções 4 e 6.1).
2. Listar, buscar, filtrar (6.2–6.4).
3. Cadastrar, atualizar, triagem, desfazer (6.5–6.8).
4. Indicadores e conclusão (seção 8).
5. Inconsistências, hierarquia, histórico (6.9–6.11).
6. Salvar (6.12).
7. Interface bonita + modo acessível.
8. Diferenciais, README, vídeo.

Cada passo é feito, testado e mostrado à equipe antes do próximo.

---

## 12. Decisões para a reunião

| # | Pergunta | Opções | Sugestão |
|---|---|---|---|
| D1 | Como representar a data? | (a) dia 1–30; (b) data real dd/mm | (a): a conta de tempo vira uma subtração simples |
| D2 | Formato da hierarquia | (a) bairro → categoria → ocorrências; (b) bairro → local → categoria → ocorrências | (a), como no edital; (b) mostraria melhor a UBS |
| D3 | Menu | (a) 12 opções diretas; (b) submenus | (a) para a banca ver tudo de uma vez |
| D4 | Transições permitidas | (a) só aberta → em análise → concluída; (b) também aberta → concluída; (c) também reabrir uma concluída | (a) + desfazer para corrigir engano |
| D5 | Id no cadastro | (a) automático; (b) digitado e validado | (a): evita id repetido |
| D6 | Desfazer e histórico | (a) apaga o último evento; (b) registra um evento "desfeito" | (b): o histórico nunca perde informação |
| D7 | Fila na triagem e no desfazer | Volta para o começo ou para o fim da fila? | Começo: mantém a ordem de chegada |
| D8 | Tratar as inconsistências | (a) correção pelo menu; (b) automática na carga; (c) as duas | (a) na carga só detecta; corrige no menu, com sugestão |
| D9 | Modo acessível | (a) perguntar ao abrir; (b) só pelo menu | (a) + opção no menu |
| D10 | Salvar | (a) sobrescrever os CSVs; (b) gravar em outros arquivos e manter os originais | (b): o vídeo e os testes sempre partem dos mesmos dados |
| D11 | Conclusão do painel | (a) frase gerada por regra; (b) texto fixo no README | (a) no painel + (b) no README |
| D12 | Pesos do score de prioridade | Quais pesos e por quê? | Acessibilidade 3, iluminação 2 (segurança à noite), conservação 2, limpeza 1 |
| D13 | Dados | Mantém as 18 ocorrências propostas e a história da acessibilidade na UBS? | Manter; ajustar se alguém tiver ideia melhor |
| D14 | Divisão de tarefas | A tabela da seção 10 está boa? | — |

### Ainda faltam para a entrega
Prazo · nome da equipe · RMs · turma (pasta do portfólio) · repositório no GitHub · roteiro do vídeo.

---

## Anotações da reunião

_(espaço para a equipe anotar)_
