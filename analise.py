import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados dos arquivos JSON (Kick, YouTube, Twitch)
with open(r'kick_probes.json') as f:
    data_kick = json.load(f)

with open(r'youtube_probes.json') as f:
    data_youtube = json.load(f)

with open(r'twitch_probes.json') as f:
    data_twitch = json.load(f)

# Função para processar os dados, incluindo latência (rtt_destino), saltos, tempo e destino
def process_data(data, service_name):
    trace_list = []
    for entry in data:
        prb_id = entry.get('prb_id')
        country = entry.get('country')
        continent = entry.get('continent')
        latency = entry.get('rtt_destino')  # Latência é 'rtt_destino'
        hops = entry.get('hops')  # Número de saltos
        destination = entry.get('destination')
        timestamp = entry.get('timestamp')
        trace_list.append([prb_id, country, continent, destination, latency, hops, timestamp, service_name])
    return trace_list

# Processar os dados de cada serviço
data_kick_processed = process_data(data_kick, "Kick")
data_youtube_processed = process_data(data_youtube, "YouTube")
data_twitch_processed = process_data(data_twitch, "Twitch")

# Unir os dados de todos os serviços em um único DataFrame
processed_data = data_kick_processed + data_youtube_processed + data_twitch_processed
df = pd.DataFrame(processed_data, columns=['prb_id', 'country', 'continent', 'destination', 'latency', 'hops', 'timestamp', 'service'])

# Converter os timestamps para o formato de data
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

### LATÊNCIA ###

# Gráfico comparando a latência ao longo do tempo para cada destino
def plot_latency_comparison(df):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='timestamp', y='latency', hue='destination', style='service', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.title('Comparação da Latência ao Longo do Tempo para Todos os Destinos')
    plt.legend(title='Destino', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('latency_comparison_destinations.png')
    plt.show()

# Gráfico agregando todas as probes e comparando latência por continente
def plot_latency_by_continent(df):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='timestamp', y='latency', hue='continent', style='service', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.title('Comparação de Latência por Continente para Todos os Destinos')
    plt.legend(title='Continente', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('latency_by_continent.png')
    plt.show()

# Gráfico agregando todas as probes e comparando latência por país
def plot_latency_by_country(df):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='timestamp', y='latency', hue='country', style='service', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.title('Comparação de Latência por País para Todos os Destinos')
    plt.legend(title='País', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('latency_by_country.png')
    plt.show()

### QUANTIDADE DE SALTOS ###

# Gráfico comparando a quantidade de saltos ao longo do tempo para cada destino
def plot_hops_comparison(df):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='timestamp', y='hops', hue='destination', style='service', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade de Saltos')
    plt.title('Comparação da Quantidade de Saltos ao Longo do Tempo para Todos os Destinos')
    plt.legend(title='Destino', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('hops_comparison_destinations.png')
    plt.show()

# Gráfico agregando todas as probes e comparando quantidade de saltos por continente
def plot_hops_by_continent(df):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='timestamp', y='hops', hue='continent', style='service', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade de Saltos')
    plt.title('Comparação da Quantidade de Saltos por Continente para Todos os Destinos')
    plt.legend(title='Continente', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('hops_by_continent.png')
    plt.show()

# Gráfico agregando todas as probes e comparando quantidade de saltos por país
def plot_hops_by_country(df):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='timestamp', y='hops', hue='country', style='service', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade de Saltos')
    plt.title('Comparação da Quantidade de Saltos por País para Todos os Destinos')
    plt.legend(title='País', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('hops_by_country.png')
    plt.show()

### CORRELAÇÃO ENTRE LATÊNCIA E SALTOS ###

# Gráfico de correlação entre latência e saltos por destino
def plot_correlation_by_destination(df):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='hops', y='latency', hue='destination', style='service', marker='o')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência (ms)')
    plt.title('Correlação entre Latência e Saltos por Destino')
    plt.legend(title='Destino', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('correlation_by_destination.png')
    plt.show()

# Gráfico de correlação entre latência e saltos por continente
def plot_correlation_by_continent(df):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='hops', y='latency', hue='continent', style='service', marker='o')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência (ms)')
    plt.title('Correlação entre Latência e Saltos por Continente')
    plt.legend(title='Continente', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('correlation_by_continent.png')
    plt.show()

# Gráfico de correlação entre latência e saltos por país
def plot_correlation_by_country(df):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='hops', y='latency', hue='country', style='service', marker='o')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência (ms)')
    plt.title('Correlação entre Latência e Saltos por País')
    plt.legend(title='País', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('correlation_by_country.png')
    plt.show()

### EXECUTAR OS GRÁFICOS ###

# Chamadas das funções para gerar os gráficos
plot_latency_comparison(df)
plot_latency_by_continent(df)
plot_latency_by_country(df)
plot_hops_comparison(df)
plot_hops_by_continent(df)
plot_hops_by_country(df)
plot_correlation_by_destination(df)
plot_correlation_by_continent(df)
plot_correlation_by_country(df)
