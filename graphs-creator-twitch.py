import json
import matplotlib.pyplot as plt
import pandas as pd

# Carregar os dados do arquivo (use o caminho correto)
with open(r'c:\Users\keven\Documents\GitHub\Medindo-Desempenhos-De-Destinos-Na-Internet\twitch-resolvido.json') as f:
    data = json.load(f)

# Função para extrair dados de latência e saltos
def extract_probe_data(probe_results):
    latencies = []
    hops = []
    for result in probe_results:
        total_latency = 0
        hop_count = 0
        for hop in result['result']:
            if hop['rtt'] is not None:
                total_latency += hop['rtt']
                hop_count += 1
        if hop_count > 0:
            latencies.append(total_latency)
            hops.append(hop_count)
    return latencies, hops

# Função para gerar gráficos por país
def plot_country_data(country, country_probes):
    latency_list = []
    hop_list = []
    
    for probe in country_probes:
        latencies, hops = extract_probe_data(probe['result'])
        latency_list.append(latencies)
        hop_list.append(hops)

    # Converter para DataFrame para manipulação mais fácil
    df_latencies = pd.DataFrame(latency_list).transpose()
    df_hops = pd.DataFrame(hop_list).transpose()

    # Gráfico de Latência
    plt.figure(figsize=(10, 6))
    for col in df_latencies.columns:
        plt.plot(df_latencies.index, df_latencies[col], label=f'Probe {col}')
    plt.title(f'Latência por Probe ({country})')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Gráfico de Saltos
    plt.figure(figsize=(10, 6))
    for col in df_hops.columns:
        plt.plot(df_hops.index, df_hops[col], label=f'Probe {col}')
    plt.title(f'Número de Saltos por Probe ({country})')
    plt.xlabel('Tempo')
    plt.ylabel('Número de Saltos')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Gráfico de Correlação Latência vs Saltos
    plt.figure(figsize=(10, 6))
    for col in df_latencies.columns:
        plt.scatter(df_hops[col], df_latencies[col], label=f'Probe {col}')
    plt.title(f'Correlação Latência vs Saltos ({country})')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotar os gráficos para os países relevantes
countries = {
    'Alemanha': data['continents']['Europe']['Germany'],
    'Brasil': data['continents']['Other']['Brazil'],
    'México': data['continents']['Other']['Mexico']
}

for country, probes in countries.items():
    plot_country_data(country, probes)
