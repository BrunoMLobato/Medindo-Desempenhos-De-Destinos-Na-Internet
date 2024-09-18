import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Definir o estilo para melhorar a visualização
sns.set(style="whitegrid", palette="pastel", font_scale=1.2)

# Definir o diretório de saída
output_dir = "compara_resumido"

# Criar a pasta de saída se ela não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Carregar os dados dos arquivos JSON (Kick, YouTube, Twitch)
with open(r'kick_probes.json') as f:
    data_kick = json.load(f)

with open(r'youtube_probes.json') as f:
    data_youtube = json.load(f)

with open(r'twitch_probes.json') as f:
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

### FUNÇÕES PARA CRIAR OS GRÁFICOS ###

# 1. Probes por site (latência) para cada serviço
def plot_probes_latency_by_site_individual(df, output_dir):
    services = df['service'].unique()
    for service in services:
        df_service = df[df['service'] == service]
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.lineplot(data=df_service, x='timestamp', y='latency', hue='country', marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Tempo')
        plt.ylabel('Latência (ms)')
        plt.title(f'Latência (RTT) por País - {service}', fontsize=18)
        plt.legend(title="País", bbox_to_anchor=(1.05, 1), loc='upper left')  # Colocar a legenda fora do gráfico
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'probes_latency_{service.lower()}.png'))
        plt.show()

# 2. Países por site (latência e saltos)
def plot_latency_hops_by_country_individual(df, output_dir):
    services = df['service'].unique()
    for service in services:
        df_service = df[df['service'] == service]

        # Latência por país
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.lineplot(data=df_service, x='timestamp', y='latency', hue='country', marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Tempo')
        plt.ylabel('Latência (ms)')
        plt.title(f'Latência (RTT) por País para {service}', fontsize=18)
        plt.legend(title="País", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'latency_country_{service.lower()}.png'))
        plt.show()

        # Saltos por país
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.lineplot(data=df_service, x='timestamp', y='hops', hue='country', marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Tempo')
        plt.ylabel('Quantidade de Saltos')
        plt.title(f'Quantidade de Saltos por País para {service}', fontsize=18)
        plt.legend(title="País", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'hops_country_{service.lower()}.png'))
        plt.show()

# 3. Continente por site (latência e saltos)
def plot_latency_hops_by_continent_individual(df, output_dir):
    services = df['service'].unique()
    for service in services:
        df_service = df[df['service'] == service]

        # Latência por continente
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.lineplot(data=df_service, x='timestamp', y='latency', hue='continent', marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Tempo')
        plt.ylabel('Latência (ms)')
        plt.title(f'Latência (RTT) por Continente para {service}', fontsize=18)
        plt.legend(title="Continente", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'latency_continent_{service.lower()}.png'))
        plt.show()

        # Saltos por continente
        plt.figure(figsize=(16, 6))  # Ajuste horizontal
        sns.lineplot(data=df_service, x='timestamp', y='hops', hue='continent', marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Tempo')
        plt.ylabel('Quantidade de Saltos')
        plt.title(f'Quantidade de Saltos por Continente para {service}', fontsize=18)
        plt.legend(title="Continente", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'hops_continent_{service.lower()}.png'))
        plt.show()

# 4. Média geral por site (latência e saltos)
def plot_avg_latency_hops_by_site(df, output_dir):
    avg_df = df.groupby('service').agg({'latency': 'mean', 'hops': 'mean'}).reset_index()

    plt.figure(figsize=(16, 6))
    sns.barplot(x='service', y='latency', data=avg_df, palette='muted')
    plt.xticks(rotation=45)
    plt.xlabel('Site')
    plt.ylabel('Latência Média (ms)')
    plt.title('Latência Média (RTT) por Site', fontsize=18)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'avg_latency_by_site.png'))
    plt.show()

    plt.figure(figsize=(16, 6))
    sns.barplot(x='service', y='hops', data=avg_df, palette='muted')
    plt.xticks(rotation=45)
    plt.xlabel('Site')
    plt.ylabel('Quantidade Média de Saltos')
    plt.title('Quantidade Média de Saltos por Site', fontsize=18)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'avg_hops_by_site.png'))
    plt.show()

### EXECUTAR OS GRÁFICOS ###

# Chamadas das funções para gerar e salvar os gráficos
plot_probes_latency_by_site_individual(df, output_dir)
plot_latency_hops_by_country_individual(df, output_dir)
plot_latency_hops_by_continent_individual(df, output_dir)
plot_avg_latency_hops_by_site(df, output_dir)
