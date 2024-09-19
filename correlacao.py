import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Definir o estilo para melhorar a visualização
sns.set(style="whitegrid", palette="pastel", font_scale=1.0)  # Diminuir o tamanho da fonte

# Definir o diretório de saída
output_dir = "correlacao_gerada"

# Criar a pasta de saída se ela não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Carregar os dados dos arquivos JSON (Kick, YouTube, Twitch) com codificação UTF-8
with open(r'kick_probes.json', encoding='utf-8') as f:
    data_kick = json.load(f)

with open(r'youtube_probes.json', encoding='utf-8') as f:
    data_youtube = json.load(f)

with open(r'twitch_probes.json', encoding='utf-8') as f:
    data_twitch = json.load(f)

# Função para processar os dados
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

### FUNÇÕES PARA CRIAR OS GRÁFICOS DE CORRELAÇÃO ###

# 1. Correlação entre latência e número de saltos por destino
def plot_latency_hops_correlation_by_destination(df, output_dir):
    destinations = df['destination'].unique()
    for destination in destinations:
        df_destination = df[df['destination'] == destination]
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.scatterplot(data=df_destination, x='hops', y='latency', hue='country', marker='o')
        plt.xlabel('Número de Hops')
        plt.ylabel('Latência (ms)')
        plt.title(f'Correlação Latência x Hops por Destino: {destination}', fontsize=16)
        plt.legend(title="País", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'latency_hops_correlation_{destination}.png'))
        plt.close()

# 2. Correlação entre latência e número de saltos por continente
def plot_latency_hops_correlation_by_continent(df, output_dir):
    continents = df['continent'].unique()
    for continent in continents:
        df_continent = df[df['continent'] == continent]
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.scatterplot(data=df_continent, x='hops', y='latency', hue='country', marker='o')
        plt.xlabel('Número de Hops')
        plt.ylabel('Latência (ms)')
        plt.title(f'Correlação Latência x Hops por Continente: {continent}', fontsize=16)
        plt.legend(title="País", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'latency_hops_correlation_continent_{continent}.png'))
        plt.close()

# 3. Correlação entre latência e número de saltos por país
def plot_latency_hops_correlation_by_country(df, output_dir):
    countries = df['country'].unique()
    for country in countries:
        df_country = df[df['country'] == country]
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.scatterplot(data=df_country, x='hops', y='latency', hue='service', marker='o')
        plt.xlabel('Número de Hops')
        plt.ylabel('Latência (ms)')
        plt.title(f'Correlação Latência x Hops por País: {country}', fontsize=16)
        plt.legend(title="Serviço", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'latency_hops_correlation_country_{country}.png'))
        plt.close()

# Chamadas das funções para gerar gráficos de correlação

plot_latency_hops_correlation_by_destination(df, output_dir)
plot_latency_hops_correlation_by_continent(df, output_dir)
plot_latency_hops_correlation_by_country(df, output_dir)
