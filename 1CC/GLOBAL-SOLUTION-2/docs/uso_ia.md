# Uso de inteligência artificial

O projeto utilizou ferramentas de inteligência artificial como apoio à organização de requisitos, documentação, desenvolvimento e revisão do código. Os dados apresentados são fictícios e a aplicação não realiza integrações com órgãos públicos.

## Ferramentas utilizadas

- **Claude (Anthropic), via Claude Code:** apoio à estruturação inicial, escrita de código, documentação e execução de verificações descritas no histórico de desenvolvimento.
- **Claude e ChatGPT, usados pela Alice no mapa interativo:** apoio no desenho do mapa, no CSS e no JavaScript local de fichas, filtros, arraste e zoom.
- **ChatGPT (OpenAI):** revisão do enunciado e dos arquivos, conferência independente de indicadores dos CSVs, alinhamento entre o formulário HTML e o cadastro Python, ajustes de persistência e revisão da documentação.

## Aplicações e verificações registradas

| Período | Apoio da IA | Evidências e verificação |
|---|---|---|
| 10/11/2026 | Organização dos requisitos das três primeiras fases do curso e comparação com o modelo de portfólio da coordenação. | Estrutura `1CC/GLOBAL-SOLUTION-2/` com código em `src/`, bases em `data/` e documentação em `docs/`. |
| 10/11/2026 | Elaboração inicial do algoritmo, da matriz de requisitos e do README. | Algoritmo consolidado em `docs/algoritmo_v1.md`; evidências técnicas organizadas em `docs/checklist.md`. |
| 12/11/2026 | Construção assistida do sistema Python, dados fictícios, validações, estruturas, indicadores e painéis HTML. | Os primeiros dez testes automatizados foram executados na etapa inicial, conforme o histórico do projeto, com comparação de resultados ao gabarito de `docs/dados.md`. |
| 12/11/2026 | Revisão da implementação, roteiro do vídeo e documentação de equipe. | Registro dos dez testes iniciais, sessões de terminal e correção de informações do README, conforme histórico da implementação. |
| 12/11/2026 | Revisão com ChatGPT, padronização do formulário, página Sobre, persistência e criação de teste adicional. | Leitura estática e conferência dos CSVs; suíte ampliada para onze cenários. |
| 12–13/11/2026 | Desenvolvimento assistido do mapa ilustrativo e interativo da Vila Esperança; integração Python→HTML; refinamento editorial do painel. | `src/mapa_html.py` gera marcadores apenas de dados válidos; `painel/mapa_template.html` reúne desenho, fichas, filtros, arraste e zoom local. |
| 12–13/11/2026 | Correção dos rótulos do menu e da logo FIAP branca, revisão de comentários e documentação. | `src/painel_html.py` usa `base64` e `pathlib` para incorporar a imagem; exceções técnicas documentadas em `CLAUDE.md`, mediante aprovação do líder comunicada pela equipe. |
| 12–13/11/2026 | Ampliação dos testes do painel. | Verificação automatizada de 16 pinos, exclusão de inconsistências, navegação, iframe, dados de situação e incorporação da logo; resultado da execução verificável na suíte de testes. |
| 13/11/2026 | A pedido do Marcelo, o Claude (via Claude Code) auditou a branch do mapa e corrigiu o que encontrou: validação só com dígitos de 0 a 9 (o `²` derrubava o programa), códigos `14` e `014` tratados como o mesmo, histórico incoerente recusado na carga, sessão vazia detectada, confirmação antes de recomeçar, painel do caminho 2 gravado em `data/saida/painel/` sem apagar os arquivos versionados e sem gerar arquivos vazios, pasta `painel/` movida para dentro do projeto, logo colorida de volta no README (a branca ficou só no rodapé do painel), retirada de ternários, tuplas e `raise`, e documentação atualizada. | Suíte ampliada para 14 testes, rodada no Python 3.9 e 3.13; sessões no terminal com entradas inválidas; painel gerado aberto no navegador. |

## Como verificamos o que a IA produz
- Rodamos o programa e testamos os casos de erro (entrada vazia, código inexistente, status inválido, caracteres estranhos).
- Conferimos os cálculos dos indicadores à mão (`docs/dados.md`) e com os testes automatizados.
- Cada integrante lê e explica o trecho de código pelo qual é responsável antes de ele entrar no repositório.

## Responsabilidade e limites

A aplicação usa lógica e estruturas de dados introdutórias. As escolhas técnicas estão descritas no README e nos arquivos de código. Os indicadores foram calculados a partir de dados simulados, e os pesos de prioridade são critérios definidos para o protótipo, não classificações oficiais.

O painel HTML exibe um retrato dos dados processados pelo Python, e o mapa bônus usa JavaScript local autorizado, sem geolocalização real ou conexão com prefeituras. O formulário não envia solicitações. Os registros reais da demonstração são cadastrados pelo terminal. A IA serviu como ferramenta de apoio; o funcionamento e os resultados devem ser apresentados de acordo com o código efetivamente executado.
