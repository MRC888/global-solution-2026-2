# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="../../assets/logo-fiap.png"
       alt="FIAP - Faculdade de Informática e Administração Paulista"
       width="40%">
</a>
</p>

<br>

# Neighborhood Action Dashboard — Global Solution 2026.2 (CitizenTech)

## 1. Equipe

**Nome do grupo:** _(a definir)_
**Projeto:** Neighborhood Action Dashboard

### 👨‍🎓 Integrantes
- Marcelo Santos — RM 576131
- Douglas Goltz — RM 574439
- Alice Brenda — RM 574916

### 👩‍🏫 Professores
- **Tutor(a):** _(a definir)_
- **Coordenador:** [André Godoi Chiovato](https://www.linkedin.com/in/andregodoichiovato/)

## 2. O bairro, o problema e o público

**O bairro:** a **Vila Esperança** é um bairro fictício com quatro pontos de referência: o entorno da UBS, o entorno da escola, a Praça Central e o ponto de ônibus. Todas as ocorrências são inventadas e usam só esses locais genéricos, nunca o endereço de uma pessoa.

**O problema:** poste apagado, calçada sem rampa, lixo acumulado e banco quebrado são problemas que afetam o dia a dia, mas os relatos costumam ficar espalhados. Não fica claro o que é mais urgente, e os moradores não conseguem acompanhar o andamento.

**O público:** moradores e uma associação de moradores que queira organizar as demandas do bairro: registrar, acompanhar o status de cada uma e ver quais problemas se acumulam.

**O que o sistema faz:** cadastra ocorrências de quatro categorias (iluminação, acessibilidade, limpeza e conservação de espaços coletivos), valida os dados, permite consultar e filtrar, acompanha o status com histórico e calcula indicadores. É um protótipo acadêmico, sem ligação com prefeituras ou órgãos públicos.

## 3. Estruturas de dados e justificativas

Todas as estruturas ficam em um dicionário `sistema`, montado em [`src/estruturas.py`](src/estruturas.py).

| Estrutura | Onde | O que guarda | Por que esta estrutura |
|---|---|---|---|
| **Lista** | `sistema["ocorrencias"]` | Todas as ocorrências válidas, na ordem de registro | Listar, filtrar e calcular indicadores exigem percorrer **todas** as ocorrências, uma por uma |
| **Dicionário** | `sistema["por_id"]` | Código → ocorrência | A busca por código acessa a ocorrência **direto pela chave**, sem percorrer a lista |
| **Fila** | `sistema["fila"]` | Códigos com status `aberta`, por ordem de chegada | Na triagem, **quem chegou primeiro é atendido primeiro**: entra no fim (`append`) e sai do começo (`pop(0)`) |
| **Pilha** | `sistema["pilha"]` | As mudanças de status desta sessão | O "desfazer" precisa da **última** mudança: entra no topo (`append`) e sai do topo (`pop()`) |
| **Hierarquia** | `sistema["hierarquia"]` | Bairro → categoria → lista de códigos | Organiza o bairro como uma árvore e permite **navegar por partes** (opção 9): escolhe a categoria, depois a ocorrência |
| **Matriz** | `sistema["matriz"]` | Linha = categoria, coluna = status, célula = quantidade | Mostra o **cruzamento** de duas informações em uma tabela 4 × 3; a mudança de status só tira 1 de uma coluna e soma 1 em outra |
| **Lista** | `sistema["historico"]` | Todos os eventos de mudança de status | Registro permanente, que só cresce e nunca perde informação; dele sai o dia de conclusão para o tempo médio |
| **Lista** | `sistema["inconsistentes"]` | Registros com problema + os motivos | Separa o que não pode entrar nos números, sem jogar a informação fora |

**Pilha × histórico:** o histórico guarda **tudo**, para sempre. A pilha guarda só as mudanças **desta sessão**, para poder desfazer. Quando algo é desfeito, o histórico ganha um evento "desfeito" em vez de perder o evento anterior.

## 4. Regras lógicas principais

**Validação** ([`validacao.validar_registro`](src/validacao.py)): todo registro (na carga do CSV, no cadastro e na correção) passa por verificações de identificação, categoria, status, campos obrigatórios, descrição, caracteres e data simulada. O registro recebe **todos** os motivos, não só o primeiro.

| Regra | Mensagem | Por que essa mensagem aparece |
|---|---|---|
| Código vazio, não numérico ou repetido | "código ausente", "código deve ter só números", "código repetido" | Sem código único, a busca pelo dicionário não funcionaria |
| Categoria fora das 4 padronizadas | "categoria ausente" ou "categoria desconhecida" | Sem categoria válida, a ocorrência não entra na matriz nem na hierarquia |
| Status fora dos 3 padronizados | "status desconhecido (resolvido)" | O status decide a coluna da matriz e se a ocorrência vai para a fila |
| Descrição **ou** local vazio (L1) | "descrição vazia" / "local vazio" | São campos obrigatórios para entender o problema |
| `;` no texto | "o texto não pode ter ponto e vírgula" | O `;` separa os campos do CSV e quebraria o arquivo |
| Descrição acima de 120 caracteres | "descrição excede 120 caracteres" | Limita o tamanho do campo no terminal e na validação dos CSVs |
| Dia **não** numérico **ou** fora de 1 a 30 (L2) | "dia fora do período" | O tempo é simulado de 1 a 30; fora disso, os cálculos de tempo perdem o sentido |

**Mudança de status** ([`validacao.verificar_transicao`](src/validacao.py)): só para a frente, um passo por vez (`aberta → em_analise → concluida`). O `if/elif/else` testa na ordem: status desconhecido → igual ao atual → já concluída → transição proibida → aceita. Cada `elif` só roda se os anteriores falharam, então a pessoa recebe o motivo mais claro. Para corrigir um engano existe o "desfazer" (opção 7).

**Condições com `and`, `or` e `not`:**

| # | Onde | Condição |
|---|---|---|
| L1 | Validação | `campo_vazio(descricao) or campo_vazio(local)` |
| L2 | Validação do dia | `not dia.isdigit() or int(dia) < 1 or int(dia) > 30` |
| L3 | Filtro | `(categoria == "" or oc["categoria"] == categoria) and (status == "" or oc["status"] == status)` |
| L5 | Aviso de duplicada | `oc["categoria"] == categoria and oc["local"] == local and not oc["status"] == "concluida"` |
| L6 | Pendência | `not ocorrencia["status"] == "concluida"` |

### Expressão booleana documentada: o filtro (L3)

Em [`operacoes.filtrar`](src/operacoes.py), uma ocorrência aparece no resultado quando:

```python
(categoria == "" or oc["categoria"] == categoria) and (status == "" or oc["status"] == status)
```

Chamando **A** = "não escolheu categoria" (Enter), **B** = "a categoria bate", **C** = "não escolheu status" e **D** = "o status bate", a expressão é **(A ou B) e (C ou D)**:

| A | B | C | D | A ou B | C ou D | Aparece? | Situação |
|---|---|---|---|---|---|---|---|
| V | – | V | – | V | V | **sim** | Sem filtro nenhum: mostra tudo |
| F | V | V | – | V | V | **sim** | Só filtro de categoria, e a categoria bate |
| F | F | V | – | F | V | não | Só filtro de categoria, e a categoria não bate |
| F | V | F | V | V | V | **sim** | Os dois filtros, e os dois batem |
| F | V | F | F | V | F | não | Os dois filtros, mas o status não bate |
| F | F | F | V | F | V | não | Os dois filtros, mas a categoria não bate |

O `or` dentro de cada parêntese faz o filtro "não usado" deixar tudo passar. O `and` exige que os dois filtros passem ao mesmo tempo. Com os dados originais, filtrar iluminação + aberta mostra 2 ocorrências (013 e 015).

## 5. Indicadores, fórmulas e interpretação

Calculados com laços e operações simples em [`src/indicadores.py`](src/indicadores.py). A opção 10 mostra, para cada um, os **dados de origem, a fórmula e o resultado**. Valores com os dados originais (16 ocorrências válidas, "hoje" = dia 30), conferidos à mão em [`docs/dados.md`](docs/dados.md) e por `src/testes.py`:

| # | Indicador | Fórmula | Resultado |
|---|---|---|---|
| I1/I2 | Total e proporção por categoria | total da categoria ÷ total geral × 100 | Iluminação 5 (31,25%) · Acessibilidade 4 (25,00%) · Limpeza 3 (18,75%) · Conservação 4 (25,00%) |
| I3 | Total e proporção por status | total do status ÷ total geral × 100 | Aberta 6 (37,50%) · Em análise 4 (25,00%) · Concluída 6 (37,50%) |
| I4 | Matriz categoria × status | contagem em cada célula | tabela 4 × 3 |
| I5 | Pendências | abertas + em análise | 10 de 16 (62,50%) |
| I6 | Tempo médio até a conclusão | Σ(dia da conclusão − dia de abertura) ÷ nº de concluídas | 32 ÷ 6 = **5,33 dias** |
| I7 | Dias em aberto das pendentes | Σ(30 − dia de abertura) ÷ nº de pendentes da categoria | **Acessibilidade 24,67** · Limpeza 13,00 · Conservação 10,67 · Iluminação 8,00 |
| Extra | Score de prioridade | dias em aberto × peso (acessibilidade 3, iluminação 2, conservação 2, limpeza 1) | 1º 003 (27 × 3 = 81), 2º 005 (75), 3º 007 (66) |

**Interpretação** (o sistema gera estas frases por regras com `if`):
- Mais da metade das ocorrências (62,50%) ainda está pendente: o bairro tem demandas acumuladas.
- Iluminação é a categoria com mais registros (5 de 16), mas é a que menos espera.
- Acessibilidade é a categoria que espera há mais tempo (24,67 dias em média), e as pendências dela estão todas no entorno da UBS. Isso pesa mais porque afeta quem tem mobilidade reduzida e precisa chegar ao posto de saúde. Por isso as três pendências mais urgentes do ranking são dela.
- O que é resolvido sai em pouco tempo (5,33 dias em média): o problema está no que fica esperando, não na velocidade de quem resolve.

## 6. Como executar

Pré-requisito: Python 3 (só a biblioteca padrão; nada para instalar).

```bash
cd 1CC/GLOBAL-SOLUTION-2
python src/sistema.py
```

Ao abrir, o sistema procura uma sessão anterior em `data/saida/`. Se houver, pergunta se deseja **continuar de onde parou** ou **recomeçar com os dados demonstrativos originais**. Depois, mostra o resultado da validação e oferece dois caminhos:

| Caminho | O que faz |
|---|---|
| **1 - Terminal** | O sistema completo, com menu: listar, buscar, filtrar, cadastrar, triagem, atualizar status, desfazer, histórico, hierarquia do bairro, painel de indicadores e correção de inconsistências. Tem modo acessível (sem cores, frases completas, confirmação antes de cada ação) |
| **2 - Painel HTML (bônus)** | Gera o painel com os dados da sessão em `data/saida/painel/` (pasta ignorada pelo Git): `painel.html`, `solicitacoes.html` e `mapa.html`, mais as páginas fixas copiadas de `painel/`. HTML e CSS são montados pelo Python; o mapa usa JavaScript local para zoom, filtros e fichas, sem internet. Se faltar algum arquivo, o sistema avisa e não grava nada |

**Páginas do painel.** `painel.html` é a página **Início**, com mapa interativo acima dos cinco indicadores; `solicitacoes.html` lista ocorrências e histórico; `sobre.html` descreve a proposta; `formulario.html` é demonstrativo e não grava dados. O mapa vem de `src/mapa_html.py` e `painel/mapa_template.html`, com pinos provenientes apenas de ocorrências válidas e posições ilustrativas, não GPS nem coordenadas reais. Fichas, filtros, arraste e zoom usam JavaScript local, sem servidor ou API. A rolagem da página permanece ativa sobre o mapa.

A pasta `painel/` do projeto é a versão de demonstração, com os dados originais; para recriá-la, rode `python src/painel_html.py`.

**Exceções autorizadas pelo líder, só para o painel bônus:** `base64` coloca a logo FIAP dentro do HTML gerado; `tempfile` cria pastas temporárias nos testes, sem tocar nos CSVs; JavaScript local cuida de pinos, fichas, filtros, arraste e zoom do mapa, sem rede, API ou servidor. Os dados e os indicadores continuam sendo calculados em Python.

**Percentuais.** A interface apresenta duas casas decimais (por exemplo, 62,50% e 25,00%); isso não muda os cálculos.

Os dois caminhos usam os mesmos dados em memória: o que for alterado no terminal aparece no painel gerado depois. **Cada cadastro, correção, mudança de status e desfazer bem-sucedido salva automaticamente** a sessão em `data/saida/`; sair do terminal também salva. A opção de continuar recupera os registros e o histórico na próxima execução. Recomeçar com a base original permite um ensaio limpo, mas a sessão anterior será substituída ao salvar novas alterações. Os CSVs originais em `data/` nunca são modificados.

**Sobre o formulário HTML:** `painel/formulario.html` é uma **prévia visual**, sem envio ou gravação de dados. Seus campos seguem as regras do cadastro Python (categoria, descrição de até 120 caracteres, local genérico e dia de 1 a 30). O cadastro funcional é a opção 4 do terminal.

Para executar as 14 verificações automatizadas (incluindo cálculos conferidos com `docs/dados.md`, gravação/recarga isoladas, painel gerado fora do Git e entradas estranhas como `²` ou `014`):

```bash
python3 src/testes.py
```

## 7. Exemplos de uso

Saída real do sistema (caminho 1, terminal). O que a pessoa digita aparece depois de cada pergunta.

**Ao abrir com os dados originais:** a validação já separa os registros com problema.

```text
Carga dos dados: 18 registros lidos, 16 válidos, 2 inconsistentes, 16 eventos no histórico.
  - registro 017: categoria ausente (corrija pela opção 11 do terminal)
  - registro 018: status desconhecido (resolvido) (corrija pela opção 11 do terminal)
```

**Cadastro (opção 4):** o código é gerado sozinho e a categoria é sugerida pelas palavras da descrição.

```text
O código será gerado automaticamente: 019
Descrição do problema (até 120 caracteres): Poste apagado na esquina da escola
Pela descrição, parece ser da categoria Iluminação.
Usar essa categoria? (s/n): s
Escolha o local: 2
Dia de abertura (1 a 30; hoje é o dia 30): 30
[OK] Ocorrência 019 cadastrada e colocada na fila (posição 7 de 7).
Sessão salva automaticamente em data/saida/.
```

**Consulta (opção 3):** ocorrências abertas de iluminação.

```text
Filtro: categoria = Iluminação; status = Aberta

Código  Categoria        Local                Dia  Status
----------------------------------------------------------------
013     Iluminação       Praça Central         20  Aberta
015     Iluminação       Ponto de Ônibus       24  Aberta
019     Iluminação       Entorno da Escola     30  Aberta

3 ocorrência(s) encontrada(s).
```

**Alteração de status (opção 6):** a 014 vai para "em análise" e a mudança entra no histórico. Pular etapa é recusado na hora.

```text
Ocorrência 014: Mato alto ao redor dos bancos
Status atual: Aberta
Próximo status permitido: Em análise
Escolha o novo status: 3
[!] Transição não permitida: de Aberta só é possível ir para Em análise.
...
Escolha o novo status: 2
Observação curta (opcional, Enter para pular): Equipe avisada
[OK] 014: Aberta -> Em análise. Registrado no histórico.
```

**Busca de código inexistente (opção 2):**

```text
Código da ocorrência (ex.: 14 ou 014): 999
[!] Ocorrência 999 não encontrada.
```

**Saída (opção 0, depois do salvamento automático):**

```text
Nesta sessão: 1 cadastro(s) e 1 mudança(s) de status.
Estado salvo em:
  .../data/saida/ocorrencias_sessao.csv
  .../data/saida/historico_sessao.csv
Os arquivos originais em data/ não foram alterados.
Na próxima execução, será possível continuar esta sessão.
```

## 8. Acessibilidade, inclusão e privacidade

**Acessibilidade**
- **Modo acessível** (perguntado ao entrar no terminal e alternável pela opção 12): sem cores nem símbolos, cada ocorrência vira uma frase completa ("Ocorrência 014: Limpeza, Praça Central, aberta no dia 22, situação Aberta.") e o sistema pede confirmação antes de cada ação que altera dados. Isso facilita o uso com leitor de tela e por quem tem pouca familiaridade com tecnologia.
- A informação nunca depende só da cor: cada status aparece escrito, e cada barra dos gráficos tem o número ao lado.
- No painel HTML, as tabelas têm legenda (`<caption>`) e cabeçalhos marcados (`scope`), para o leitor de tela anunciar "Iluminação, Aberta: 2".
- Escolhas por lista numerada (categoria, local, status) evitam erros de digitação e acentos.

**Inclusão**
- Mensagens em português simples, dizendo **o que** está errado e **o que fazer** ("O dia deve ser um número de 1 a 30").
- O programa nunca fecha por erro de digitação: toda entrada é conferida com `if` e pedida de novo.
- A sugestão de categoria ajuda quem não sabe classificar o problema.

**Privacidade**
- Todos os dados são fictícios. O cadastro **não pede nome, e-mail nem endereço**; o local é sempre um ponto genérico do bairro ("Entorno da UBS"), nunca a casa de alguém.
- O formulário de protótipo do painel avisa para não colocar número da casa nem citar nomes de pessoas.
- Os arquivos originais não são alterados; o estado da sessão é salvo automaticamente em `data/saida/`, pasta ignorada pelo Git, e pode ser retomado na execução seguinte.

## 9. Vídeo
**Vídeo de apresentação:** link a ser incluído após a publicação no YouTube como “Não listado”.

## 10. Conclusões, limitações e aprendizados

**Conclusões:** com estruturas simples (lista, fila, pilha, dicionário, hierarquia e matriz) e regras com `if`, o sistema transforma relatos soltos em informação útil. Ele mostra o que está pendente, o que espera há mais tempo e por onde começar. No conjunto simulado, os números apontam a acessibilidade no entorno da UBS como a necessidade mais urgente da comunidade.

**Limitações:**
- Os dados são simulados: os números contam a história que foi montada, não a de um bairro real.
- O tempo é contado em dias de 1 a 30, sem datas reais; tudo o que muda na sessão acontece no "dia 30".
- O sistema não se conecta a nenhum órgão público e não garante atendimento: ele organiza e acompanha, não resolve.
- Os pesos do score de prioridade foram escolhidos pela equipe e são uma opinião, não uma regra oficial.
- O painel HTML é um retrato do momento em que foi gerado (não atualiza sozinho) e o formulário é só protótipo visual: o cadastro de verdade é feito no terminal.
- Como `try/except` não faz parte do conteúdo das Fases 1 a 3, apertar Ctrl+C ou Ctrl+D no meio de uma pergunta encerra o programa com a mensagem de erro do Python. As alterações feitas até ali já estão salvas.
- As cores do terminal usam códigos ANSI: se a saída for redirecionada para um arquivo, os códigos aparecem como texto. O modo acessível desliga as cores.
- Ao continuar uma sessão salva, a fila de triagem é remontada com as ocorrências abertas na ordem do arquivo salvo, e a pilha do desfazer começa vazia (só desfaz o que foi feito na sessão atual).

**Aprendizados técnicos demonstrados:**
- A mesma ocorrência precisa ser mantida de forma consistente em estruturas diferentes: lista para percorrer, dicionário para consultar por código, fila para triagem, pilha para desfazer, hierarquia para navegar e matriz para contar.
- A validação é essencial antes de incluir dados nos indicadores. Separar registros inconsistentes, explicar o motivo e permitir correção torna os resultados mais confiáveis.
- Regras booleanas e transições de status evitam estados impossíveis; o histórico preserva o que aconteceu, mesmo após desfazer.
- Indicadores simples podem revelar situações diferentes: a categoria mais frequente não é necessariamente a que está pendente há mais tempo.
- Persistir os dados em arquivos separados permite retomar o trabalho sem alterar a base fictícia usada para testar a aplicação.

**Aprendizados de cada integrante:** _(cada um escreve com as próprias palavras)_
- **Marcelo:** _(a escrever)_
- **Douglas:** _(a escrever)_
- **Alice:** _(a escrever)_

---

## 📁 Estrutura de pastas

* **`data/`** ocorrências e histórico simulados (CSV); a subpasta `saida/` guarda a sessão retomável localmente (ignorada pelo Git).
* **`docs/`** documentação: checklist do edital e registro do uso de IA.
* **`src/`** código-fonte Python.
* **`painel/`** painel HTML de demonstração (bônus), com os dados originais.
* **`README.md`** este arquivo.

A pasta `notebooks/` do modelo não foi criada porque o projeto não usa notebooks (o modelo permite usar só as pastas que fazem sentido).

## 📎 Observações

* **Participação na Competição:** [ ] Sim, aceitamos participar / [ ] Não vamos participar.

## 📎 Uso de inteligência artificial

O apoio de inteligência artificial ao projeto está documentado em [docs/uso_ia.md](docs/uso_ia.md).

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
