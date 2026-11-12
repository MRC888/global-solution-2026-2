# Dados do projeto: formato, valores e gabarito

Bairro fictício: **Vila Esperança**. Todos os dados são inventados e nenhum identifica pessoas.

## Arquivos

| Arquivo | O que guarda |
|---|---|
| `data/ocorrencias.csv` | As 18 ocorrências (16 válidas e 2 inconsistentes de propósito) |
| `data/historico.csv` | 16 eventos de mudança de status |
| `data/saida/` | Guarda automaticamente `ocorrencias_sessao.csv` e `historico_sessao.csv` após cada alteração; pode ser retomada na próxima execução. É ignorada pelo Git; os arquivos originais nunca são alterados |

**Formato:** texto UTF-8, uma linha por registro, campos separados por `;`. A primeira linha é o cabeçalho. Por isso nenhum texto pode conter `;`, e o sistema recusa esse caractere no cadastro.

**Persistência:** se os dois arquivos de `data/saida/` existirem, a abertura pergunta se deseja retomar a sessão ou carregar a base fictícia original. Cadastro, correção, atualização de status e desfazer salvam automaticamente; sair pelo menu também salva. Para recomeçar a demonstração, escolha a base original. Depois de salvar mudanças nesse modo, o estado anterior em `data/saida/` é substituído. Os arquivos `ocorrencias.csv` e `historico.csv` permanecem inalterados.

## Campos de uma ocorrência (todos obrigatórios)

| Campo | Exemplo | Regra |
|---|---|---|
| `id` | `014` | Só números e único. No cadastro, é gerado automaticamente (maior código + 1) |
| `categoria` | `limpeza` | Um dos valores padronizados abaixo |
| `descricao` | `Mato alto ao redor dos bancos` | Não vazia, sem `;`, até 120 caracteres |
| `local` | `Praça Central` | Local genérico do bairro, nunca o endereço de uma pessoa |
| `dia` | `22` | Número de 1 a 30 (tempo simulado; "hoje" é o dia 30) |
| `status` | `aberta` | Um dos valores padronizados abaixo |

Campos de um evento do histórico: `id`, `dia`, `status_anterior`, `status_novo`, `observacao`.

## Valores padronizados

**Categorias:** `iluminacao`, `acessibilidade`, `limpeza`, `conservacao` (conservação de espaços coletivos).

**Locais:** Entorno da UBS, Entorno da Escola, Praça Central, Ponto de Ônibus.

**Status e significado:**

| Status | Significado |
|---|---|
| `aberta` | Registrada e aguardando a primeira análise, na fila de triagem |
| `em_analise` | Já foi examinada e a solução está em andamento |
| `concluida` | O problema foi resolvido; a ocorrência não muda mais |

**Mudanças permitidas:** `aberta` → `em_analise` → `concluida`, um passo por vez. Para corrigir um engano existe o "desfazer", que fica registrado no histórico como um novo evento.

## Registros inconsistentes (de propósito)

| Código | Problema | Como o sistema trata |
|---|---|---|
| 017 | Categoria vazia | Na carga, é separado e não entra nos números. Pela opção 11, o sistema sugere "Limpeza" pelas palavras da descrição ("entulho", "restos") |
| 018 | Status `resolvido`, que não existe | Na carga, é separado. Pela opção 11, o usuário escolhe um dos 3 status válidos |

## Gabarito dos indicadores (calculado à mão e conferido por `src/testes.py`)

Com os dados originais, antes de qualquer alteração:

| Indicador | Resultado |
|---|---|
| Registros | 18 lidos, 16 válidos, 2 inconsistentes, 16 eventos |
| Por categoria | Iluminação 5 (31,25%) · Acessibilidade 4 (25%) · Limpeza 3 (18,75%) · Conservação 4 (25%) |
| Por status | Aberta 6 (37,5%) · Em análise 4 (25%) · Concluída 6 (37,5%) |
| Matriz (aberta / em análise / concluída) | Iluminação 2/0/3 · Acessibilidade 1/2/1 · Limpeza 1/1/1 · Conservação 2/1/1 |
| Pendências | 10 de 16 (62,5%) |
| Tempo médio até a conclusão | (7 + 4 + 3 + 9 + 5 + 4) ÷ 6 = 32 ÷ 6 = **5,33 dias** |
| Dias em aberto das pendentes | Iluminação 8,00 · **Acessibilidade 24,67** · Limpeza 13,00 · Conservação 10,67 |
| Fila inicial de triagem | 005, 010, 013, 014, 015, 016 |
| Prioridade (top 3) | 003 (27 × 3 = 81), 005 (75), 007 (66): todas de acessibilidade no Entorno da UBS |

**A história que os dados contam:** os problemas de acessibilidade no entorno da UBS são os que esperam há mais tempo (24,67 dias em média). Isso é sério porque afeta justamente quem tem mobilidade reduzida e precisa chegar ao posto de saúde.
