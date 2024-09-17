import json
import requests

def get_probe_location(prb_id):
    url = f"https://atlas.ripe.net/api/v2/probes/{prb_id}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            country = data.get('country_code')
            return country
        else:
            print(f"Erro ao buscar a probe {prb_id}: Status {response.status_code}")
            return "Unknown"
    except Exception as e:
        print(f"Erro ao buscar a probe {prb_id}: {e}")
        return "Unknown"
