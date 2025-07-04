import os
import json
from datetime import datetime

# Caminhos
LOG_PATH = "/var/log/pihole.log"
OUTPUT_PATH = "/home/umbrel/sirius/scikit/data/dns_queries.json"

def extrair_linhas_recentes():
    # Le as ultimas 100 linhas do log do Pi-hole
    with open(LOG_PATH, "r") as file:
        linhas = file.readlines()[-100:]
    return linhas

def parsear_linhas(linhas):
    # Extrai consultas DNS validas
    consultas = []
    for linha in linhas:
        if "query[A]" in linha:
            try:
                partes = linha.strip().split()
                hora_str = f"{partes[0]} {partes[1]} {partes[2]}"
                dominio = partes[7]
                ip_origem = partes[9]

                timestamp = datetime.strptime(hora_str, "%b %d %H:%M:%S")
                timestamp = timestamp.replace(year=datetime.now().year)

                consultas.append({
                    "timestamp": timestamp.isoformat(),
                    "dominio": dominio,
                    "origem": ip_origem
                })
            except Exception as e:
                print("Erro ao processar linha:", linha.strip(), "|", e)
    return consultas

def salvar_consultas(consultas):
    # Adiciona novas consultas ao arquivo JSON
    if not consultas:
        print("Nenhuma nova consulta DNS encontrada.")
        return

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    else:
        dados = []

    dados.extend(consultas)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(dados, f, indent=4)

    print(len(consultas), "novas consultas DNS salvas.")

if __name__ == "__main__":
    linhas = extrair_linhas_recentes()
    consultas = parsear_linhas(linhas)
    salvar_consultas(consultas)

