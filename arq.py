import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Seaborn pode ajudar com gráficos de dispersão mais claros

# Carregar os dados do arquivo JSON
with open(r'youtube_probes.json') as f:  # Substitua pelo caminho correto do arquivo
    data = json.load(f)

# Função para processar os dados, incluindo latência (rtt_destino), saltos, tempo e destino
def process_data(data):
    trace_list = []
    for entry in data:
        prb_id = entry.get('prb_id')
        country = entry.get('country')
        continent = entry.get('continent')
        latency = entry.get('rtt_destino')  # Latência é 'rtt_destino'
        hops = entry.get('hops')  # Número de saltos
        destination = entry.get('destination')
        timestamp = entry.get('timestamp')
        trace_list.append([prb_id, country, continent, destination, latency, hops, timestamp])
    return trace_list

# Processar os dados
processed_data = process_data(data)

# Criar DataFrame a partir dos dados processados
df = pd.DataFrame(processed_data, columns=['prb_id', 'country', 'continent', 'destination', 'latency', 'hops', 'timestamp'])

# Converter os timestamps para o formato de data, se necessário
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Função para gerar gráfico de latência ao longo do tempo por destino (horizontal)
def plot_latency_over_time(df):
    if df['latency'].isnull().all():
        print("Nenhum dado de latência encontrado.")
        return

    plt.figure(figsize=(12, 8))
    
    for destination, group in df.groupby('destination'):
        plt.plot(group['latency'], group['timestamp'], label=f'Destino: {destination}')
    
    plt.ylabel('Tempo')
    plt.xlabel('Latência (ms)')
    plt.title('Variação da Latência ao Longo do Tempo por Destino')
    plt.legend()
    plt.tight_layout()
    plt.savefig('latency_over_time_horizontal.png')
    plt.show()

# Função para gerar gráfico da quantidade de saltos ao longo do tempo por destino (horizontal)
def plot_hops_over_time(df):
    if df['hops'].isnull().all():
        print("Nenhum dado de saltos encontrado.")
        return

    plt.figure(figsize=(12, 8))
    
    for destination, group in df.groupby('destination'):
        plt.plot(group['hops'], group['timestamp'], label=f'Destino: {destination}')
    
    plt.ylabel('Tempo')
    plt.xlabel('Quantidade de Saltos')
    plt.title('Variação da Quantidade de Saltos ao Longo do Tempo por Destino')
    plt.legend()
    plt.tight_layout()
    plt.savefig('hops_over_time_horizontal.png')
    plt.show()

# Função para gerar gráfico de correlação entre latência e saltos por destino
def plot_latency_hops_correlation(df):
    if df['latency'].isnull().all() or df['hops'].isnull().all():
        print("Dados de latência ou saltos ausentes.")
        return

    plt.figure(figsize=(14, 10))
    
    # Usar seaborn para uma melhor visualização de gráficos de dispersão
    sns.scatterplot(data=df, x='hops', y='latency', hue='destination', palette='tab20', s=100, alpha=0.7)

    # Adicionar uma linha de tendência para cada destino
    for destination, group in df.groupby('destination'):
        sns.regplot(data=group, x='hops', y='latency', scatter=False, ci=None, label=f'Destino: {destination}', line_kws={"linewidth":1.5})
    
    plt.xlabel('Quantidade de Saltos')
    plt.ylabel('Latência (ms)')
    plt.title('Correlação entre Latência e Quantidade de Saltos por Destino')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Colocar a legenda fora do gráfico
    plt.tight_layout()
    plt.savefig('latency_hops_correlation_improved.png')
    plt.show()

# Função para gerar gráficos por continente (horizontal)
def plot_by_continent(df, metric='latency'):
    plt.figure(figsize=(12, 8))
    
    for continent, group in df.groupby('continent'):
        plt.plot(group[metric], group['timestamp'], label=f'Continente: {continent}')
    
    plt.ylabel('Tempo')
    if metric == 'latency':
        plt.xlabel('Latência (ms)')
        plt.title('Variação da Latência por Continente')
    else:
        plt.xlabel('Quantidade de Saltos')
        plt.title('Variação da Quantidade de Saltos por Continente')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{metric}_by_continent_horizontal.png')
    plt.show()

# Função para gerar gráficos por país (horizontal)
def plot_by_country(df, metric='latency'):
    plt.figure(figsize=(12, 8))
    
    for country, group in df.groupby('country'):
        plt.plot(group[metric], group['timestamp'], label=f'País: {country}')
    
    plt.ylabel('Tempo')
    if metric == 'latency':
        plt.xlabel('Latência (ms)')
        plt.title('Variação da Latência por País')
    else:
        plt.xlabel('Quantidade de Saltos')
        plt.title('Variação da Quantidade de Saltos por País')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{metric}_by_country_horizontal.png')
    plt.show()

# Chamadas das funções para gerar os gráficos
plot_latency_over_time(df)
plot_hops_over_time(df)
plot_latency_hops_correlation(df)
plot_by_continent(df, metric='latency')
plot_by_continent(df, metric='hops')
plot_by_country(df, metric='latency')
plot_by_country(df, metric='hops')
