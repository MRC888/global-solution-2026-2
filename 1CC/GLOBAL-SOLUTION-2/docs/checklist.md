# Checklist do edital — Neighborhood Action Dashboard

Legenda: ✅ atendido e testado · 🟡 em andamento · ⬜ pendente.
Coluna **Evidência**: arquivo, função ou teste que comprova o item.

## Dados simulados
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| D1 | No mínimo 12 ocorrências com código único | ⬜ | |
| D2 | Categorias: iluminação, acessibilidade, limpeza e conservação de espaços coletivos | ⬜ | |
| D3 | Cada ocorrência com categoria, descrição, localidade genérica, data simulada e status | ⬜ | |
| D4 | No mínimo 3 status, com o significado documentado | ⬜ | |
| D5 | Histórico com pelo menos 8 atualizações ou eventos | ⬜ | |
| D6 | Pelo menos 1 registro com campo ausente ou inconsistente, detectado e tratado | ⬜ | |
| D7 | Sem informações pessoais (dados inventados) | ⬜ | |

## Cadastro e interpretação
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| C1 | Ler ocorrências de CSV/TXT (formato explicado na documentação) | ⬜ | |
| C2 | Campos obrigatórios definidos | ⬜ | |
| C3 | Identificadores e valores padronizados para categoria e status | ⬜ | |
| C4 | Listagem legível: código, categoria, localidade e status | ⬜ | |
| C5 | Pelo menos uma validação lógica (sem categoria, status desconhecido…) | ⬜ | |

## Organização dos dados (com justificativa)
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| E1 | Lista: conjunto de ocorrências percorrível | ⬜ | |
| E2 | Fila: demandas não examinadas, por ordem de registro | ⬜ | |
| E3 | Pilha: últimas atualizações e eventos recentes | ⬜ | |
| E4 | Dicionário: acesso pelo identificador | ⬜ | |
| E5 | Hierarquia (bairro → categoria → ocorrências), explicada | ⬜ | |
| E6 | Matriz: quantidades por categoria × situação | ⬜ | |

## Regras lógicas
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| R1 | `if` / `elif` / `else` em entradas, categorias e mudanças de status | ⬜ | |
| R2 | `and`, `or` e `not` em pelo menos 3 condições distintas | ⬜ | |
| R3 | Uma expressão booleana documentada no README | ⬜ | |
| R4 | Explicação de por que cada condição gera cada mensagem/ação | ⬜ | |

## Consultas, filtros e atualização
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| Q1 | Cadastrar com verificação dos campos obrigatórios | ⬜ | |
| Q2 | Buscar por código | ⬜ | |
| Q3 | Filtrar por categoria e/ou status | ⬜ | |
| Q4 | Atualizar status e registrar no histórico | ⬜ | |
| Q5 | Mensagem clara para registro inexistente ou dado inválido | ⬜ | |

## Indicadores
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| I1 | Totais e proporções por categoria | ⬜ | |
| I2 | Totais e proporções por status | ⬜ | |
| I3 | Indicador extra (tempo médio simulado ou pendências) | ⬜ | |
| I4 | Dados de origem, fórmula e resultado em tabela/painel textual | ⬜ | |
| I5 | Conclusão curta interpretando os números | ⬜ | |

## Regras técnicas
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| T1 | Só conceitos das Fases 1, 2 e 3 | ⬜ | |
| T2 | Sem pandas, numpy, sklearn, streamlit, web, banco de dados ou APIs | ⬜ | |
| T3 | Só biblioteca padrão (fora `csv`/`os`, com aprovação do Marcelo) | ⬜ | |
| T4 | Executa com `python src/sistema.py` | ⬜ | |

## README (estrutura obrigatória)
| # | Seção | Situação |
|---|---|---|
| M1 | Nome da equipe e RMs | 🟡 |
| M2 | Bairro, problema e público beneficiado | ⬜ |
| M3 | Estruturas de dados e justificativas | ⬜ |
| M4 | Regras lógicas principais | ⬜ |
| M5 | Indicadores, fórmulas e interpretação | ⬜ |
| M6 | Como executar | 🟡 |
| M7 | Exemplo de cadastro, consulta, alteração e saída | ⬜ |
| M8 | Acessibilidade, inclusão e privacidade | ⬜ |
| M9 | Link do vídeo | ⬜ |
| M10 | Conclusões, limitações e aprendizados | ⬜ |

## Entrega
| # | Item | Situação |
|---|---|---|
| F1 | Repositório GitHub público, no modelo da coordenação | 🟡 (criado privado; tornar público antes da entrega) |
| F2 | Vídeo no YouTube como "Não listado" | ⬜ |
| F3 | TXT na FIAP ON com só os dois links | ⬜ |
| F4 | Uso de IA documentado em `docs/uso_ia.md` | 🟡 |
| F5 | Código sem erros nas operações demonstradas | ⬜ |
