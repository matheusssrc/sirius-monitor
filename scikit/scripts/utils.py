import json
import os

def is_mac_confiavel(mac):
    caminho_arquivo = "/home/umbrel/sirius/scikit/data/dispositivos_confiaveis.json"
    mac = mac.upper()

    if not os.path.exists(caminho_arquivo):
        return False

    with open(caminho_arquivo, "r") as file:
        dispositivos = json.load(file)
        for dispositivo in dispositivos:
            if dispositivo["mac"].upper() == mac:
                return True
    return False

