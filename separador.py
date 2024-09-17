import json
import requests

def get_probe_info(probe_id):
    url = f"https://atlas.ripe.net/api/v2/probes/%7Bprobe_id%7D/?optional_fields=country_name"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar informações da probe {probe_id}")
        return None
