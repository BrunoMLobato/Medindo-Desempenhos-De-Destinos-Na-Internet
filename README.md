# Medindo-Desempenhos-De-Destinos-Na-Internet


DOCUMENTAÇÃO: analise_dados_probes.py

Objetivo:
O script processa e analisa dados de "probes" para diferentes serviços (Kick, YouTube e Twitch) a partir de arquivos JSON, com o objetivo de gerar gráficos sobre latência (RTT), número de saltos (hops), e comparações por país, continente e serviço.

Funcionalidades:
- Carregamento de dados: O script carrega dados de três arquivos JSON, contendo informações de latência, saltos, países, continentes, destinos e timestamps.
- Processamento de dados: A função `process_data` transforma os dados dos JSON em uma lista de traços (traces) organizados.
- Geração de gráficos:
  - Latência e hops por país e continente.
  - Comparação de plataformas (Kick, YouTube e Twitch) em relação a latência e hops.
  - Média geral de latência e hops para as três plataformas ao longo do tempo.

Bibliotecas Utilizadas:
- os: Para manipulação de diretórios e arquivos.
- json: Para carregar e processar os arquivos JSON.
- pandas: Para criar e manipular os dados em DataFrames.
- matplotlib e seaborn: Para a geração dos gráficos.

Gráficos Gerados:
- Latência e hops por país.
- Latência e hops por continente.
- Média geral de latência e hops por plataforma.

Diretório de Saída:
Os gráficos gerados são salvos no diretório `graficos_gerados`.



DOCUMENTAÇÃO: atualiza_probes.go

Objetivo:
O script `atualiza_probes.go` é responsável pela atualização de dados das "probes" em tempo real. Ele coleta informações de latência e salva esses dados para serem analisados posteriormente.

Funcionalidades:
- Execução contínua: O script está configurado para funcionar continuamente, monitorando e coletando informações sobre as "probes".
- Atualização dos dados: Faz solicitações HTTP para obter dados sobre as "probes" e atualiza os arquivos JSON ou outro formato de dados para armazenar a latência e saltos das "probes".

Linguagem:
Este script está escrito em Go, e aproveita a natureza concorrente da linguagem para realizar múltiplas coletas de dados de forma simultânea e eficiente.



DOCUMENTAÇÃO: detalhado.py

Objetivo:
Este script parece estar relacionado ao processamento detalhado dos dados das "probes", fornecendo insights adicionais além do script principal de análise.

Funcionalidades:
- Geração de relatórios detalhados: É possível que este script seja utilizado para gerar relatórios com informações mais detalhadas das "probes", complementando os gráficos do script principal.
- Análise de dados adicionais: Pode incluir análise mais profunda, como correlações entre latência e saltos, análises por intervalos de tempo, etc.

Bibliotecas Utilizadas:
Provavelmente utiliza pandas, numpy, e outras bibliotecas de análise de dados para gerar tabelas ou gráficos mais específicos.
