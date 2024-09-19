import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

# Configuração para garantir que os gráficos usem UTF-8 e exibam acentos corretamente
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

# Dicionário para mapear as siglas dos países para os nomes completos
country_mapping = {
    'AR': 'Argentina',
    'BR': 'Brasil',
    'US': 'Estados Unidos',
    'FR': 'França',
    'DE': 'Alemanha',
    'JP': 'Japão',
    'CN': 'China',
    'RU': 'Rússia',
    'IN': 'Índia',
    'MX': 'México',
    'CA': 'Canadá',
    'ES': 'Espanha',
    # Adicione outros países conforme necessário
}

# Criar pasta para salvar os gráficos se ela não existir
output_dir = 'graficos_detalhados'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Função para carregar e processar os dados de um arquivo JSON
def load_and_process_data(file_path, platform):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    
    trace_list = []
    for entry in data:
        prb_id = entry.get('prb_id')
        country = country_mapping.get(entry.get('country'), entry.get('country'))  # Mapeando a sigla do país
        continent = entry.get('continent')
        latency = entry.get('rtt_destino')  # Latência é 'rtt_destino'
        hops = entry.get('hops')  # Número de saltos
        destination = entry.get('destination')
        timestamp = entry.get('timestamp')
        trace_list.append([prb_id, country, continent, destination, latency, hops, timestamp, platform])
    return trace_list

# Carregar e processar os dados dos três arquivos JSON
youtube_data = load_and_process_data('youtube_probes.json', 'YouTube')
twitch_data = load_and_process_data('twitch_probes.json', 'Twitch')
kick_data = load_and_process_data('kick_probes.json', 'Kick')

# Combinar todos os dados em uma única lista
combined_data = youtube_data + twitch_data + kick_data

# Criar DataFrame a partir dos dados processados
df = pd.DataFrame(combined_data, columns=['prb_id', 'country', 'continent', 'destination', 'latency', 'hops', 'timestamp', 'platform'])

# Converter os timestamps para o formato de data
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Função para formatar o eixo de tempo (data/hora)
def format_time_axis():
    date_format = DateFormatter("%d/%m - %H:%M")
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()

# Gráfico: Todas as probes por site (latência - Latência (ms))
def plot_probes_by_platform(df):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='timestamp', y='latency', hue='platform', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.title('Latência de Todas as Probes por Plataforma')
    plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
    format_time_axis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'all_probes_latency_by_platform.png'))
    plt.close()  # Fechar a figura sem mostrar

# Gráficos: Países por site (RTT e hops)
def plot_by_country(df, metric='latency'):
    for country, group in df.groupby('country'):
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=group, x='timestamp', y=metric, hue='platform', marker='o')
        plt.xlabel('Tempo')
        if metric == 'latency':
            plt.ylabel('Latência (ms)')
        else:
            plt.ylabel(f'{metric.capitalize()}')
        plt.title(f'{metric.capitalize()} por País: {country}')
        plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
        format_time_axis()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{metric}_by_country_{country}.png'))
        plt.close()  # Fechar a figura sem mostrar

# Gráficos: Continente por site (RTT e hops)
def plot_by_continent(df, metric='latency'):
    for continent, group in df.groupby('continent'):
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=group, x='timestamp', y=metric, hue='platform', marker='o')
        plt.xlabel('Tempo')
        if metric == 'latency':
            plt.ylabel('Latência (ms)')
        else:
            plt.ylabel(f'{metric.capitalize()}')
        # Corrigindo o termo 'América' e garantindo UTF-8
        continent_name = 'América' if continent == 'America' else continent
        plt.title(f'{metric.capitalize()} por Continente: {continent_name}')
        plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
        format_time_axis()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{metric}_by_continent_{continent_name}.png'))
        plt.close()  # Fechar a figura sem mostrar

# Gráficos: Média geral de RTT e hops para os três sites
def plot_overall_average(df):
    df_mean = df.groupby(['platform', 'timestamp']).mean().reset_index()

    # Média de latência (RTT)
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df_mean, x='timestamp', y='latency', hue='platform', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Média de Latência (ms)')
    plt.title('Média Geral de Latência por Plataforma')
    plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
    format_time_axis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'average_latency_by_platform.png'))
    plt.close()  # Fechar a figura sem mostrar

    # Média de hops
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df_mean, x='timestamp', y='hops', hue='platform', marker='o')
    plt.xlabel('Tempo')
    plt.ylabel('Média de Hops')
    plt.title('Média Geral de Hops por Plataforma')
    plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
    format_time_axis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'average_hops_by_platform.png'))
    plt.close()  # Fechar a figura sem mostrar

# Chamando as funções para gerar os gráficos solicitados
plot_probes_by_platform(df)
plot_by_country(df, metric='latency')
plot_by_country(df, metric='hops')
plot_by_continent(df, metric='latency')
plot_by_continent(df, metric='hops')
plot_overall_average(df)
