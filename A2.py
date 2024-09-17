import json
import matplotlib.pyplot as plt
from collections import defaultdict
import requests

# Sua chave de API do ipinfo (substitua pela sua)
API_KEY = '2a5702ed83300c'

# Carregar dados do arquivo JSON
with open('Medindo-Desempenhos-De-Destinos-Na-Internet\youtube-resolvido.json', 'r') as f:
    data = json.load(f)

# Função para geolocalizar IPs usando a API ipinfo
def geolocalizar_ip(ip):
    url = f"https://ipinfo.io/{ip}?token={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('country', 'Unknown')
        else:
            print(f"Falha ao geolocalizar IP {ip}: Status {response.status_code}")
            return 'Unknown'
    except Exception as e:
        print(f"Erro ao geolocalizar IP {ip}: {e}")
        return 'Unknown'

# Função para extrair latência (rtt) e saltos agrupados por continente e país
def extrair_dados_por_pais_continente(data):
    dados = defaultdict(lambda: defaultdict(lambda: {'rtt': [], 'hops': []}))
    
    for continente, countries in data['continents'].items():
        for pais, probes_data in countries.items():
            if pais.lower() == "unknown":  # Geolocalizar países desconhecidos
                for probe in probes_data:
                    for result in probe['result']:
                        if result['from']:  # Se houver um IP
                            pais_geolocalizado = geolocalizar_ip(result['from'])
                            if pais_geolocalizado != 'Unknown':
                                pais = pais_geolocalizado
            for probe in probes_data:
                for result in probe['result']:
                    if result['rtt'] is not None:
                        dados[continente][pais]['rtt'].append(result['rtt'])
                    if result['hop'] is not None:
                        dados[continente][pais]['hops'].append(result['hop'])
    
    return dados

# Extrair dados por país e continente
dados_por_pais_continente = extrair_dados_por_pais_continente(data)

# Função para plotar e salvar os gráficos
def plotar_dados_por_pais_continente(dados_por_pais_continente):
    for continente, paises in dados_por_pais_continente.items():
        n_paises = len(paises)
        
        print(f'Plotando dados para o continente: {continente} ({n_paises} países)')

        if n_paises == 1:
            fig, axs = plt.subplots(1, 2, figsize=(12, 5))
            axs = [axs]  # Ajeitar axs para ser iterável
        else:
            fig, axs = plt.subplots(n_paises, 2, figsize=(12, 5 * n_paises))

        fig.suptitle(f'Dados para o Continente: {continente}', fontsize=16)

        for i, (pais, dados) in enumerate(paises.items()):
            print(f"Plotando dados para o país: {pais}")
            ax_rtt, ax_hops = axs[i] if n_paises > 1 else axs

            # Gráfico de Latência
            ax_rtt.plot(dados['rtt'], label=f'{pais} - Latência')
            ax_rtt.set_title(f'Latência - {pais}')
            ax_rtt.set_xlabel('Tempo')
            ax_rtt.set_ylabel('Latência (ms)')
            ax_rtt.legend()

            # Gráfico de Saltos
            ax_hops.plot(dados['hops'], label=f'{pais} - Saltos', color='orange')
            ax_hops.set_title(f'Número de Saltos - {pais}')
            ax_hops.set_xlabel('Tempo')
            ax_hops.set_ylabel('Número de Saltos')
            ax_hops.legend()

        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        
        # Salvar o gráfico como PNG
        plt.savefig(f'{continente}_grafico.png')
        print(f'Gráfico salvo como {continente}_grafico.png')

# Plotar os gráficos
print("Iniciando a plotagem...")
plotar_dados_por_pais_continente(dados_por_pais_continente)
print("Processo de plotagem concluído.")
