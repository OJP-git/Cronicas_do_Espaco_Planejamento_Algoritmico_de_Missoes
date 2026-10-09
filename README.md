# Crônicas do Espaço: Planejamento Algorítmico de Missões (Parte 1)

**Projeto:** Sistema de Gerenciamento e Planejamento de Missões Espaciais  
**Disciplina:** Estruturas de Dados Avançadas e Algoritmos  

---

## 1. Fonte de Dados (API)

* **Nome da API:** The Solar System OpenData API.
* **Endereço Base:** `https://api.le-systeme-solaire.net/`.
* **Justificativa da Escolha:** A API disponibiliza um acervo real, científico e estruturado sobre corpos celestes (planetas, luas, asteroides e cometas), contendo atributos físicos e orbitais essenciais que viabilizam buscas detalhadas e fornecem uma base de caracteres diversa para os experimentos de compressão de telemetria.
* **Endpoints Utilizados:**
  * `GET /rest/bodies/`: Obtém a lista completa dos corpos celestes registrados e seus respectivos metadados.
* **Exemplo de Requisição HTTP:**
  GET https://api.le-systeme-solaire.net/rest/bodies/
  Headers: {"Authorization": "Bearer 151ebbcc-8737-402d-9b7d-23fb3abdffb8"}
* **Estrutura dos Dados Retornados (JSON):**
  * `bodies`: Coleção principal contendo os objetos JSON dos corpos catalogados.
    * `id` (str): Identificador textual único do corpo celeste.
    * `englishName` (str): Nome do corpo celeste em inglês (chave primária adotada na aplicação).
    * `isPlanet` (bool): Indicador booleano que classifica se o corpo é um planeta principal.
    * `mass` (dict): Objeto aninhado com massValue (float) e massExponent (int).
    * `vol` (dict): Objeto aninhado com volValue (float) e volExponent (int).
    * `gravity` (float): Aceleração da gravidade superficial em m/s².
    * `moons` (list ou None): Lista de dicionários contendo referências às luas orbitantes.

---

## 2. Modelagem do Sistema

* **Representação dos Elementos:** Cada elemento do universo astronômico é encapsulado em nós encadeados (`HashNode`), mantendo a chave de pesquisa e a estrutura original de dados devolvida pela API.
* **Atributos Utilizados:**
  * Chave de busca e dispersão: `englishName`.
  * Metadados físicos expostos na consulta: `mass`, `vol`, `moons`, `gravity`, `isPlanet`.
* **Operações Implementadas:**
  * Inserção de corpos celestes (`add_corpo`).
  * Busca exata por nome (`procura_corpo`).
  * Coleta e contagem de frequências de caracteres (`conta_frequencia`).
  * Conversão estrutural de hash para lista encadeada (`transforma_em_vetor`).
* **Decisões de Projeto:**
  * **Módulo de Aquisição Nível 1 (Consumo Dinâmico):** As requisições HTTP GET ocorrem na inicialização do sistema, realizando o parse do JSON diretamente para as estruturas internas em tempo de execução.

---

## 3. Estrutura de Dados: Tabela Hash com Encadeamento Externo

* **Estrutura Escolhida:** Tabela Hash com resolução de colisões por encadeamento externo (Separate Chaining).
* **Justificativa da Escolha:** Assegura complexidade de tempo médio O(1) para busca e inserção. O encadeamento por listas encadeadas (`HashNode`) confere tolerância a colisões em conjuntos de chaves lexicais semelhantes sem depender de sondagens destrutivas.
* **Instrumentação e Métricas Rastreadas:**
  * Número total de colisões rastreadas durante o ciclo de vida da tabela (`colisoes`).
  * Fator de carga corrente (`num_corpos / size`).
  * Capacidade total do vetor interno (`size`).
  * Quantidade líquida de elementos inseridos (`num_corpos`).  * **Proibição de Estruturas Nativas de Alto Nível:** Não foram utilizados dicionários nativos (`dict`) ou conjuntos (`set`) para a lógica central e contagem de telemetria; ambas utilizam a implementação proprietária de Tabela Hash com encadeamento.
* **Complexidade das Operações:**
  * Busca: Caso Médio O(1), Pior Caso O(n).
  * Inserção: Caso Médio O(1), Pior Caso O(n).
  * Rehashing (`dobra_tamanho`): Pior Caso O(n) isolado.

## 4. Análise de Complexidade Amortizada

A inserção individual em uma Tabela Hash possui um pior caso de O(n) devido à operação de redimensionamento dinâmico (`dobra_tamanho`), acionada quando o fator de carga atinge 0.5. Contudo, classificar a operação geral como O(n) representa um limite excessivamente pessimista perante uma sequência de n inserções consecutivas.

### Aplicação do Método Contábil (Accounting Method):
1. Defina o custo real de uma inserção sem redimensionamento como 1 unidade de custo.
2. Atribui-se uma taxa amortizada (imposto) de 3 créditos a cada inserção executada:
   * 1 crédito paga imediatamente o custo real da própria inserção na posição do bucket.
   * 1 crédito é armazenado na conta do elemento recém-inserido.
   * 1 crédito é armazenado para subsidiar a movimentação de um elemento inserido anteriormente que já esgotou seu crédito.
3. Quando a tabela atinge sua capacidade e precisa dobrar de tamanho com m elementos, o custo real do rehashing é de exatamente m operações de movimentação.
4. Como pelo menos m/2 inserções ocorreram desde a última duplicação, o saldo acumulado em créditos é de pelo menos 2 * (m/2) = m créditos.
5. Esse saldo acumulado cobre integralmente o custo real de transferir os elementos para a nova tabela sem gerar saldo negativo na conta amortizada.

Portanto, o custo total de qualquer sequência de n inserções é limitado superiormente por 3n, comprovando matematicamente que o custo amortizado por inserção é rigorosamente O(1).

---

## 5. Algoritmo Guloso: Opção B (Compressão de Huffman)

* **Problema:** Comunicação Interplanetária e Telemetria (Compressão de Dados).
* **Estratégia Adotada:** Implementação do Algoritmo de Huffman para compressão sem perdas do payload textual bruto retornado pela API.
* **Justificativa do Critério de Escolha:** A escolha gulosa seleciona a cada iteração os dois nós de menor frequência acumulada e os combina em um novo nó pai. Essa escolha local ótima garante a geração de uma árvore binária ótima com códigos de tamanho variável prefixados, minimizando o comprimento ponderado da mensagem e atingindo a entropia ideal da fonte de dados.
* **Etapas Implementadas:**
  1. Contagem de frequência de todos os caracteres do payload textual bruto via Tabela Hash própria.
  2. Extração dos pares (caractere, frequência) para ordenação decrescente.
  3. Construção da Árvore de Huffman combinando sucessivamente os nós terminais de menor frequência.
  4. Mapeamento dos caminhos binários em um dicionário de códigos (`gera_codigo`).
  5. Cálculo comparativo do total de bits originais frente ao payload comprimido via `calcula_compressao`.
