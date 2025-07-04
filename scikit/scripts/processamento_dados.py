import os
import json
import pandas as pd

# Caminho base no sistema real
base_path = "/home/umbrel/sirius/scikit/data"

# Caminhos dos arquivos
dns_path = os.path.join(base_path, "dns_ia_dataset.json")
zabbix_path = os.path.join(base_path, "zabbix_ia_dataset.json")
arp_path = os.path.join(base_path, "arp_dhcp_dataset.jsonl")
confiaveis_path = os.path.join(base_path, "dispositivos_confiaveis.json")
saida_path = os.path.join(base_path, "ia_treinamento.csv")

# Carregar DNS
dns_data = []
if os.path.exists(dns_path):
    with open(dns_path) as f:
        dns_data = json.load(f)

# Carregar Zabbix
zabbix_data = []
if os.path.exists(zabbix_path):
    with open(zabbix_path) as f:
        zabbix_data = json.load(f)

# Carregar ARP/DHCP
arp_data = []
if os.path.exists(arp_path):
    with open(arp_path) as f:
        arp_data = [json.loads(line) for line in f if line.strip()]

# Carregar confiáveis
confiaveis = set()
if os.path.exists(confiaveis_path):
    with open(confiaveis_path) as f:
        confiaveis_list = json.load(f)
        confiaveis = {d["mac"].upper() for d in confiaveis_list}

# Processar dados
registros = []
for evento in arp_data:
    mac = evento.get("mac", "").upper()
    ip = evento.get("ip", "")
    hostname = evento.get("hostname", "")
    tipo = evento.get("tipo", "")
    confiavel = mac in confiaveis
    dns_count = sum(1 for d in dns_data if d.get("ip") == ip)
    zabbix_info = next((z for z in zabbix_data if z.get("host") == hostname), {})
    registros.append({
        "mac": mac,
        "ip": ip,
        "hostname": hostname,
        "tipo_evento": tipo,
        "conf_confiavel": confiavel,
        "dns_qtd": dns_count,
        "zabbix_uptime": zabbix_info.get("uptime"),
        "zabbix_ping": zabbix_info.get("ping"),
        "zabbix_latencia": zabbix_info.get("latencia"),
        "zabbix_perda": zabbix_info.get("perda"),
        "timestamp": evento.get("data_detectado")
    })

# Salvar CSV final
df = pd.DataFrame(registros)
df.to_csv(saida_path, index=False)
print(f"Arquivo salvo em: {saida_path}")
