ESSA ATIVIDADE DEVE SER ENTREGUE NA FASE 4! 



A Global Solution – 2º Semestre de 2026 propõe o desafio CitizenTech: desenvolver tecnologias voltadas às necessidades reais das pessoas nas cidades e comunidades. O case Neighborhood Action Dashboard convida as equipes a criar uma aplicação para registrar, organizar e acompanhar demandas de melhoria em bairros, como iluminação, acessibilidade, limpeza e conservação de espaços coletivos.

Problemas cotidianos de infraestrutura e manutenção afetam a qualidade de vida da população. Muitas vezes, os registros são dispersos, as prioridades não ficam claras e os moradores não conseguem acompanhar a situação das solicitações. Uma aplicação simples, organizada e compreensível pode ajudar a transformar relatos em informações úteis para a comunidade.

Neste contexto, as equipes desenvolverão um protótipo funcional capaz de cadastrar ocorrências fictícias ou consentidas, categorizá-las, consultar seu andamento e apresentar indicadores básicos. O desafio é aplicar lógica de programação, estruturas de dados e algoritmos estudados nas três primeiras fases, sem depender de serviços externos, integração com órgãos públicos ou conhecimentos de fases posteriores.

A proposta também incentiva uma reflexão sobre acessibilidade, inclusão, privacidade e responsabilidade no uso da tecnologia. O foco estará na qualidade do funcionamento, na clareza das informações e na justificativa das escolhas técnicas.

PERÍODO E FORMATO DE PARTICIPAÇÃO
Período de realização: conforme as datas informadas oficialmente na plataforma FIAP ON para a Global Solution 2026.2.

Formato: o projeto pode ser desenvolvido individualmente ou em grupo de até 5 pessoas, conforme as orientações oficiais da turma. Recomenda-se a organização de responsabilidades e o registro das decisões da equipe.

 

Aviso sobre as orientações de abertura:

As informações sobre abertura, esclarecimento de dúvidas e acompanhamento serão comunicadas pelos canais oficiais da FIAP.

Os prazos e links oficiais divulgados pela instituição prevalecem sobre qualquer planejamento interno da equipe.

 

CONTEXTO DO DESAFIO

Os bairros e comunidades apresentam demandas de infraestrutura e conservação que podem ser descritas, classificadas e acompanhadas. Quando essas informações estão organizadas, torna-se mais simples identificar tipos de problemas frequentes e avaliar quais solicitações permanecem em aberto.

Neste desafio, sua equipe deverá criar o Neighborhood Action Dashboard, uma aplicação que simula um painel comunitário de ocorrências. O sistema deverá permitir registrar solicitações, consultar registros, alterar situações e exibir um resumo dos indicadores. Os dados podem ser inventados ou consentidos e não devem revelar informações pessoais.

O desafio envolve tanto construir as funcionalidades quanto decidir como representar e consultar dados, tratar registros incompletos ou inconsistentes e explicar resultados de maneira compreensível. Não se espera integração real com prefeituras ou promessa de atendimento das demandas.

 

OBJETIVO GERAL

Desenvolver um protótipo funcional de cadastro e acompanhamento de ocorrências comunitárias, aplicando programação em Python, algoritmos, estruturas de dados introdutórias, lógica booleana e análise simples de indicadores, com foco na organização das informações, no acompanhamento de status e na clareza de uso.

CONTEÚDOS INTEGRADOS

Este projeto reúne exclusivamente conhecimentos das fases 1, 2 e 3 do curso, aplicando-os à organização de demandas comunitárias.





Figura 1 - Conteúdos mobilizados por fase do curso

Fonte: Elaborada pelo autor (2026)

 

MISSÃO DA EQUIPE

A equipe deverá desenvolver uma aplicação de acompanhamento de ocorrências capaz de executar as seguintes tarefas:

Cadastrar ocorrências com identificador, categoria, descrição, local genérico, data simulada e situação atual;
Organizar os registros em estruturas como listas, filas, pilhas, dicionários e matrizes, de acordo com sua finalidade;
Consultar registros por identificador, categoria e status, aplicando condições e busca;
Atualizar o status das demandas e preservar um histórico simples das alterações realizadas;
Calcular e apresentar indicadores básicos, como total de ocorrências por categoria, quantidade por situação e tempo simulado de acompanhamento;
Exibir orientações e informações de forma compreensível, utilizando uma interface textual funcional ou outra solução compatível com os conteúdos estudados.
DADOS SIMULADOS OBRIGATÓRIOS

A equipe poderá criar um conjunto fictício de ocorrências ou utilizar registros devidamente consentidos e sem identificação pessoal. O pacote mínimo de dados deverá conter:

Pelo menos 12 ocorrências, identificadas por código único e distribuídas entre iluminação, acessibilidade, limpeza e conservação de espaços coletivos;
Para cada ocorrência: categoria, descrição breve, localidade genérica, data ou período simulado de abertura e status;
No mínimo três situações distintas, como aberta, em análise e concluída, documentando o significado de cada uma;
Histórico simulado com pelo menos 8 atualizações de status ou eventos de acompanhamento;
Pelo menos um registro com campo ausente ou inconsistente, a ser identificado e tratado por uma regra de validação.
 

REQUISITOS TÉCNICOS DO SISTEMA

Cadastro e interpretação de ocorrências

O sistema deverá ler ocorrências de um arquivo CSV ou TXT simples, ou inicializar os registros no próprio código Python. O formato adotado deverá ser explicado na documentação.

Requisitos específicos:

Definir os campos que caracterizam uma ocorrência e informar quais são obrigatórios;
Usar identificadores e valores padronizados para representar categorias e situações;
Apresentar uma listagem legível contendo código, categoria, localidade genérica e status;
Implementar pelo menos uma validação lógica, como impedir cadastro sem categoria ou impedir atualização para situação desconhecida.
Organização dos dados

Os dados deverão ser organizados com estruturas estudadas nas três primeiras fases, com justificativa de sua utilização.

Requisitos específicos:

Utilizar lista para armazenar o conjunto de ocorrências e permitir percorrê-lo;
Utilizar fila para organizar demandas ainda não examinadas por ordem de registro;
Utilizar pilha para registrar as últimas atualizações ou permitir consultar eventos recentes;
Utilizar dicionário ou estrutura equivalente para acessar dados de uma ocorrência pelo identificador;
Representar uma hierarquia simples, por exemplo: bairro → categoria → ocorrências, explicando como ela ajuda a organizar as informações;
Utilizar uma matriz ou lista de listas para sintetizar quantidades por categoria e por situação.
 Regras lógicas

O sistema deverá aplicar regras condicionais para validar registros, pesquisar demandas e atualizar seu andamento.

Requisitos específicos:

Utilizar IF, ELIF e ELSE para verificar entradas, categorias ou mudanças de situação;
Utilizar operadores AND, OR e NOT em pelo menos três condições distintas;
Documentar no README uma expressão booleana utilizada em uma validação ou filtro;
Explicar por que as condições produzem cada mensagem, consulta ou alteração de status.
Consultas, filtros e atualização de status

A aplicação deverá permitir acompanhar as ocorrências por consultas e mudanças simuladas de situação.

Requisitos específicos:

Cadastrar novos registros com verificação dos campos obrigatórios;
Pesquisar ocorrências por código e filtrar ao menos por categoria ou status;
Atualizar a situação de uma ocorrência existente e registrar a alteração em histórico;
Informar de forma clara quando um registro não for encontrado ou quando os dados fornecidos forem inválidos.
Análise de indicadores

A equipe deverá construir indicadores simples a partir das ocorrências cadastradas, sem utilizar técnicas avançadas de análise de dados.

Requisitos específicos:

Calcular totais e proporções de ocorrências por categoria e por status, usando operações matemáticas e laços;
Calcular um indicador adicional simples, como tempo médio simulado entre registro e conclusão ou quantidade de pendências;
Mostrar os dados de origem, a fórmula ou regra de cálculo e os resultados em tabela ou painel textual;
Interpretar os números em uma conclusão breve, indicando o que o conjunto simulado sugere sobre as necessidades da comunidade.
 

EXEMPLO DE FUNCIONAMENTO

O exemplo abaixo é apenas ilustrativo. A equipe poderá definir outra organização, desde que cumpra os requisitos técnicos.

Entrada simulada: id = 014, categoria = iluminação, local = Praça Central, status = aberta, abertura = dia 2.
Consulta: exibir todas as ocorrências abertas da categoria iluminação.
Indicadores: 12 ocorrências cadastradas; 5 abertas; 4 em análise; 3 concluídas.
Ação 1: validar os dados e cadastrar uma nova demanda com identificador único.
Ação 2: alterar a ocorrência 014 para “em análise” e registrar a mudança no histórico.
Ação 3: atualizar os indicadores e exibir o resumo das demandas por situação.
ENTREGÁVEIS OBRIGATÓRIOS
Envie um arquivo .TXT pela plataforma FIAP ON contendo apenas os dois links abaixo:

Link direto do repositório GitHub público da equipe;
Link do vídeo de apresentação publicado no YouTube como “Não Listado”.

      Todos os arquivos desenvolvidos nesta etapa deverão estar organizados no repositório GitHub do grupo, seguindo o modelo oficial disponibilizado pela coordenação.
Repositório modelo da coordenação:
https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master

Seu repositório GitHub deverá conter os arquivos e pastas indicados na tabela, organizados de modo a permitir a correção:



Figura 2 - Estrutura e conteúdo dos arquivos do repositório

Fonte: Elaborada pelo autor (2026)

 

ESTRUTURA DO README

Nome da equipe e RMs dos integrantes;
Descrição do bairro ou comunidade simulada, problema e público beneficiado;
Estruturas de dados utilizadas e justificativa de cada escolha;
Regras lógicas principais de cadastro, validação, consulta e atualização;
Indicadores implementados, fórmulas e interpretação dos resultados;
Como executar: python src/sistema.py;
Exemplo de cadastro, consulta, alteração de status e saída do sistema;
Cuidados adotados com acessibilidade, inclusão e privacidade;
Link do vídeo no YouTube;
Conclusões, limitações e aprendizados.
 

REGRAS TÉCNICAS

Utilize somente conceitos desenvolvidos nas fases 1, 2 e 3;
Uma interface textual no terminal é suficiente; telas gráficas e aplicações web não são obrigatórias;
Não são exigidos pandas, numpy, scikit-learn, streamlit, frameworks web, banco de dados ou APIs;
Utilize Python básico, funções, condicionais, laços, listas, dicionários e outras estruturas estudadas, com leitura simples de arquivos se necessário;
Os indicadores devem ser calculados com operações simples; integração com órgãos públicos e dados pessoais não são exigidas.
 

 USO DE INTELIGÊNCIA ARTIFICIAL

A IA poderá ser utilizada para discutir ideias, revisar a documentação, esclarecer conceitos e gerar dados fictícios. A equipe deve compreender, testar e justificar o código e as análises apresentadas. Caso utilize IA, registre no arquivo docs/uso_ia.md como ela apoiou o desenvolvimento e como os resultados foram verificados.

CHECKLIST DE ENTREGA

Repositório GitHub público e acessível?
Arquivo .TXT enviado na plataforma contém os links corretos?
Vídeo disponível no YouTube como “Não Listado”?
Código Python funciona sem erros nas operações demonstradas?
Cadastro, busca, filtragem e atualização de status documentados?
Estruturas de dados aplicadas e justificadas?
Indicadores calculados e interpretados corretamente?
Validação de dados e tratamento de inconsistências funcionando?
Interface textual ou equivalente apresenta informações de forma clara?
Uso de IA documentado, quando aplicável?
 

OBJETIVO FINAL

Ao final da Global Solution, espera-se que cada equipe demonstre capacidade de transformar necessidades cotidianas de uma comunidade em uma aplicação funcional: cadastrar informações, organizá-las, aplicar regras de consulta e atualização e produzir indicadores úteis.

Mais do que apresentar funcionalidades isoladas, a equipe deverá justificar escolhas de estruturas de dados e algoritmos, demonstrar a aplicação em funcionamento e reconhecer os limites de dados simulados e de uma solução que não se conecta a serviços públicos.

O Neighborhood Action Dashboard deverá evidenciar como os fundamentos da Ciência da Computação podem apoiar participação cidadã, acessibilidade, organização de informações e acompanhamento responsável de demandas locais.