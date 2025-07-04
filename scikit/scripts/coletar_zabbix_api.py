import requests
import json
import os
from datetime import datetime

# Configuracoes de acesso
ZABBIX_URL = "http://localhost:8080/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASS = "zabbix"
OUTPUT_PATH = "/home/umbrel/sirius/scikit/data/zabbix_ia_dataset.json"

HEADERS = {"Content-Type": "application/json-rpc"}

# Autenticacao na API
def autenticar():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": ZABBIX_USER,
            "password": ZABBIX_PASS
        },
        "id": 1
    }
    try:
        r = requests.post(ZABBIX_URL, headers=HEADERS, json=payload)
        r.raise_for_status()
        return r.json().get("result")
    except Exception as e:
        print("Erro ao autenticar:", e)
        return None

# Obtem todos os hosts
def obter_hosts(token):
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "host"]
        },
        "auth": token,
        "id": 2
    }
    try:
        r = requests.post(ZABBIX_URL, headers=HEADERS, json=payload)
        r.raise_for_status()
        return r.json().get("result", [])
    except Exception as e:
        print("Erro ao obter hosts:", e)
        return []

# Obtem valor de um item especifico por chave
def obter_item(token, hostid, key):
    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["itemid", "lastvalue"],
            "hostids": hostid,
            "search": {"key_": key},
            "sortfield": "name"
        },
        "auth": token,
        "id": 3
    }
    try:
        r = requests.post(ZABBIX_URL, headers=HEADERS, json=payload)
        r.raise_for_status()
        result = r.json().get("result")
        return result[0]["lastvalue"] if result else None
    except Exception as e:
        print(f"Erro ao obter item '{key}' do host {hostid}:", e)
        return None

# Coleta dados por host
def coletar_dados(token):
    hosts = obter_hosts(token)
    dados = []

    for h in hosts:
        hostid = h["hostid"]
        hostname = h["host"]

        uptime = obter_item(token, hostid, "system.uptime")
        ping = obter_item(token, hostid, "icmpping")
        latencia = obter_item(token, hostid, "icmppingsec")
        perda = obter_item(token, hostid, "icmppingloss")

        dados.append({
            "host": hostname,
            "uptime": int(float(uptime)) if uptime else None,
            "ping": float(ping) if ping else None,
            "latencia": round(float(latencia), 4) if latencia else None,
            "perda": round(float(perda), 4) if perda else None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return dados

# Salva os dados no arquivo JSON
def salvar_json(dados):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(dados, f, indent=4)

# Execucao principal
if __name__ == "__main__":
    token = autenticar()
    if not token:
        print("Falha na autenticacao com o Zabbix.")
        exit(1)

    resultado = coletar_dados(token)
    salvar_json(resultado)
    print("Coleta finalizada com sucesso. Total de hosts:", len(resultado))
