# Uso de inteligência artificial

O projeto utilizou ferramentas de inteligência artificial como apoio à organização de requisitos, documentação, desenvolvimento e revisão do código. Os dados apresentados são fictícios e a aplicação não realiza integrações com órgãos públicos.

## Ferramentas utilizadas

- **Claude (Anthropic), via Claude Code:** apoio à estruturação inicial, escrita de código, documentação e execução de verificações descritas no histórico de desenvolvimento.
- **ChatGPT (OpenAI):** revisão do enunciado e dos arquivos, conferência independente de indicadores dos CSVs, alinhamento entre o formulário HTML e o cadastro Python, ajustes de persistência e revisão da documentação.

## Aplicações e verificações registradas

| Período | Apoio da IA | Evidências e verificação |
|---|---|---|
| 10/11/2026 | Organização dos requisitos das três primeiras fases do curso e comparação com o modelo de portfólio da coordenação. | Estrutura `1CC/GLOBAL-SOLUTION-2/` com código em `src/`, bases em `data/` e documentação em `docs/`. |
| 10/11/2026 | Elaboração inicial do algoritmo, da matriz de requisitos e do README. | Algoritmo consolidado em `docs/algoritmo_v1.md`; evidências técnicas organizadas em `docs/checklist.md`. |
| 12/11/2026 | Construção assistida do sistema Python, dados fictícios, validações, estruturas, indicadores e painéis HTML. | Os primeiros dez testes automatizados foram executados na etapa inicial, conforme o histórico do projeto, com comparação de resultados ao gabarito de `docs/dados.md`. |
| 12/11/2026 | Revisão da implementação, roteiro do vídeo e documentação de equipe. | Registro dos dez testes iniciais, sessões de terminal e correção de informações do README, conforme histórico da implementação. |
| 12/11/2026 | Revisão com ChatGPT, padronização dos campos do formulário HTML, ajuste da página Sobre, salvamento e retomada de sessão, validação central de descrição e criação de teste adicional. | Leitura estática dos arquivos e cálculo independente dos totais e médias a partir dos CSVs originais. O código de testes possui onze cenários; não foi realizada execução independente da suíte atualizada durante essa revisão. |

## Responsabilidade e limites

A aplicação usa lógica e estruturas de dados introdutórias. As escolhas técnicas estão descritas no README e nos arquivos de código. Os indicadores foram calculados a partir de dados simulados, e os pesos de prioridade são critérios definidos para o protótipo, não classificações oficiais.

O painel HTML exibe um retrato dos dados processados pelo Python e seu formulário não envia solicitações. Os registros reais da demonstração são cadastrados pelo terminal. A IA serviu como ferramenta de apoio; o funcionamento e os resultados devem ser apresentados de acordo com o código efetivamente executado.
