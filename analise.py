import json
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo JSON com múltiplas entradas
data = []
with open(r'C:\Users\yurit\OneDrive\Documentos\faculdade\trab2-redes\youtube.json') as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a linha: {e}")
            continue

# Função para extrair a latência e o número de saltos
def process_trace(data):
    trace_list = []
    for entry in data:
        msm_id = entry.get('msm_id')
        timestamp = entry.get('timestamp')
        dst_name = entry.get('dst_name')
        
        # Verifica se há a chave 'result'
        if 'result' in entry:
            for result in entry['result']:
                hop_count = len(result.get('result', []))
                for hop in result.get('result', []):
                    if 'rtt' in hop:
                        rtt = hop['rtt']
                        trace_list.append([msm_id, timestamp, dst_name, hop_count, rtt])
                    else:
                        trace_list.append([msm_id, timestamp, dst_name, hop_count, None])
        else:
            print(f"'result' não encontrado em entry: {entry}")
    return trace_list

# Processar os dados de traceroute
trace_data = process_trace(data)

# Criar DataFrame a partir dos dados processados
df = pd.DataFrame(trace_data, columns=['msm_id', 'timestamp', 'dst_name', 'hop_count', 'rtt'])

# Converter timestamp para um formato de data legível
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Filtrar dados sem latência
df = df.dropna(subset=['rtt'])

# Calcular o intervalo de tempo entre o primeiro e o último timestamp
min_timestamp = df['timestamp'].min()
max_timestamp = df['timestamp'].max()

# Exibir o intervalo de tempo
print(f"Os dados estão sendo medidos entre {min_timestamp} e {max_timestamp}")
print(f"Duração total da medição: {max_timestamp - min_timestamp}")

# Agrupar por destino para análise
grouped = df.groupby('dst_name')

# Função para gerar gráficos de latência ao longo do tempo
def plot_latency(grouped):
    plt.figure(figsize=(10, 6))
    for name, group in grouped:
        plt.plot(group['timestamp'], group['rtt'], label=f'Destino: {name}')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.title('Latência ao longo do tempo por destino')
    plt.legend()
    plt.savefig(f'latencia_{name}.png')  # Salva o gráfico como um arquivo PNG
    plt.close()  # Fecha o gráfico para evitar sobreposição

# Função para gerar gráficos do número de saltos
def plot_hops(grouped):
    plt.figure(figsize=(10, 6))
    for name, group in grouped:
        plt.plot(group['timestamp'], group['hop_count'], label=f'Destino: {name}')
    plt.xlabel('Tempo')
    plt.ylabel('Número de Saltos')
    plt.title('Número de saltos ao longo do tempo por destino')
    plt.legend()
    plt.savefig(f'hops_{name}.png')  # Salva o gráfico como um arquivo PNG
    plt.close()

# Função para gerar gráfico de correlação entre latência e número de saltos com linha
def plot_latency_hops_correlation(df):
    plt.figure(figsize=(10, 6))
    
    # Agrupando por número de saltos e tirando a média de latência
    grouped_correlation = df.groupby('hop_count')['rtt'].mean().reset_index()
    
    # Gerar gráfico de linha
    plt.plot(grouped_correlation['hop_count'], grouped_correlation['rtt'], marker='o')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência Média (ms)')
    plt.title('Correlação entre número de saltos e latência média')
    plt.savefig('correlation_latency_hops.png')  # Salva o gráfico como um arquivo PNG
    plt.close()

# Chamar as funções para gerar os gráficos e salvar automaticamente
plot_latency(grouped)
plot_hops(grouped)
plot_latency_hops_correlation(df)
