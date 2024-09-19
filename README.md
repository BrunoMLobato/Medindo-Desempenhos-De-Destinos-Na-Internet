**DOCUMENTAÇÃO: analise_dados.py**

**Objetivo:**

- O script analise_dados.py é responsável por processar e analisar dados a partir de um arquivo CSV, gerando estatísticas e gráficos sobre as informações coletadas.

**Funcionalidades:**

- Carregamento de Dados: Lê os dados de um arquivo CSV e realiza a limpeza, removendo valores ausentes e normalizando as informações.
- Processamento de Dados: Calcula estatísticas descritivas, como média, mediana e desvio padrão, para fornecer insights sobre os dados.
- Geração de Gráficos: Cria gráficos para visualizar a distribuição dos dados, auxiliando na identificação de padrões e tendências.

**Bibliotecas Utilizadas:**
- pandas: Para carregar e manipular os dados em DataFrames.
- numpy: Para cálculos numéricos.
- matplotlib: Para geração de gráficos.
- Gráficos Gerados:
  - Histogramas, gráficos de dispersão e gráficos de barras para representar as estatísticas dos dados.
  - Diretório de Saída
  - Os gráficos gerados são salvos em um diretório especificado no script.

**DOCUMENTAÇÃO: correlacao.py**

**Objetivo:**

- O script correlacao.py calcula a correlação entre variáveis presentes em um conjunto de dados, auxiliando na identificação de relações entre diferentes métricas.

**Funcionalidades:**

- Cálculo de Correlações: Gera uma matriz de correlação para as variáveis numéricas do conjunto de dados, destacando a força e direção das relações.
- Visualização: Cria gráficos de calor (heatmaps) para facilitar a interpretação das correlações.
- Exportação de Resultados: A matriz de correlação gerada é exportada para um arquivo CSV.
- Bibliotecas Utilizadas
- pandas: Para manipulação dos dados.
- numpy: Para cálculos numéricos.
- matplotlib e seaborn: Para visualização dos gráficos.
- Gráficos Gerados:
  - Heatmap para a matriz de correlação, ilustrando as relações entre as variáveis.
  - Diretório de Saída
  - Os gráficos e arquivos de correlação são salvos no diretório especificado no script.


**DOCUMENTAÇÃO: atualiza_probes.go**

**Objetivo:**

- O script atualiza_probes.go é responsável pela atualização de dados das "probes" em tempo real, coletando informações como latência e número de saltos para posterior análise.

**Funcionalidades:**

Execução Contínua: O script é configurado para rodar continuamente, monitorando e coletando dados das probes.
Atualização de Dados: Faz solicitações HTTP para obter dados atualizados sobre as probes, armazenando informações de latência e saltos em arquivos JSON ou outro formato.
Relatórios: Gera relatórios sobre o status das atualizações realizadas.
Linguagem
Este script é escrito em Go e utiliza a natureza concorrente da linguagem para realizar múltiplas coletas de dados de forma eficiente.

**DOCUMENTAÇÃO: dados_detalhados.py**

**Objetivo:**

- O script dados_detalhados.py realiza uma análise detalhada de dados de latência coletados de diversas plataformas, gerando gráficos que permitem comparações aprofundadas.

**Funcionalidades**

- Carregamento de Dados: Carrega dados de múltiplos arquivos JSON (youtube_probes.json, twitch_probes.json, kick_probes.json).
- Processamento de Dados: Extrai informações de latência, hops, países, continentes e timestamps, organizando-as em uma estrutura para análise.
- Geração de Gráficos:
  - Latência e número de hops por país e continente.
  - Comparação de plataformas (YouTube, Twitch, Kick) em relação à latência e número de hops.
  - Média geral de latência e hops ao longo do tempo para cada plataforma.

**Bibliotecas Utilizadas**
- os: Para manipulação de diretórios e arquivos.
- json: Para carregar e processar os arquivos JSON.
- pandas: Para criação e manipulação dos dados em DataFrames.
- matplotlib e seaborn: Para geração e customização dos gráficos.
- Gráficos Gerados
  - Gráficos de barras e linhas comparando a latência e número de hops por plataforma, país e continente.
  - Diretório de Saída
- Os gráficos gerados são salvos no diretório graficos_detalhados.
