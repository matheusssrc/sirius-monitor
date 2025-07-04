from scapy.all import sniff, ARP, DHCP, BOOTP, Ether
from datetime import datetime
import pytz
import json
from webhook_sender import enviar_webhook
from utils import is_mac_confiavel

jsonl_file = "/home/umbrel/sirius/scikit/data/arp_dhcp_dataset.jsonl"
tz = pytz.timezone('America/Sao_Paulo')

def registrar_evento(info):
    mac = info["mac"]
    if is_mac_confiavel(mac):
        print("Ignorado: MAC confiavel detectado:", mac)
        return

    # Salva em JSONL estruturado
    with open(jsonl_file, "a") as jf:
        jf.write(json.dumps(info, ensure_ascii=False) + "\n")

    print("Evento registrado:", info)

    # Envia via webhook (opcional)
    enviar_webhook(
        tipo=info["tipo"],
        ip=info["ip"],
        mac=mac,
        hostname=info["hostname"],
        vendor_class=info["vendor_class"],
        requested_ip=info["requested_ip"],
        data_detectado=info["data_detectado"]
    )

def extrair_info(packet):
    resultado = {
        "mac": "Desconhecido",
        "ip": "Desconhecido",
        "hostname": "Desconhecido",
        "vendor_class": "Desconhecido",
        "requested_ip": "Desconhecido",
        "tipo": "Desconhecido",
        "data_detectado": datetime.now(tz).isoformat()
    }

    if packet.haslayer(ARP) and packet[ARP].op == 1:
        resultado["tipo"] = "ARP"
        resultado["mac"] = packet[Ether].src
        resultado["ip"] = packet[ARP].psrc

    elif packet.haslayer(DHCP):
        resultado["tipo"] = "DHCP"
        resultado["mac"] = packet[Ether].src

        if packet.haslayer(BOOTP):
            resultado["ip"] = packet[BOOTP].yiaddr

        for opt in packet[DHCP].options:
            if isinstance(opt, tuple):
                if opt[0] == 'hostname':
                    try:
                        resultado["hostname"] = opt[1].decode(errors='ignore') if isinstance(opt[1], bytes) else opt[1]
                    except Exception:
                        resultado["hostname"] = "Erro ao decodificar"
                elif opt[0] == 'requested_addr':
                    resultado["requested_ip"] = opt[1]
                elif opt[0] == 'vendor_class_id':
                    try:
                        resultado["vendor_class"] = opt[1].decode(errors='ignore') if isinstance(opt[1], bytes) else opt[1]
                    except Exception:
                        resultado["vendor_class"] = "Erro ao decodificar"

    return resultado

def detectar_pacote(packet):
    if ARP in packet and packet[ARP].op == 1:
        info = extrair_info(packet)
        registrar_evento(info)
    elif DHCP in packet:
        info = extrair_info(packet)
        registrar_evento(info)

print("Monitorando ARP e DHCP... (Ctrl+C para parar)")
sniff(filter="arp or (udp and (port 67 or 68))", prn=detectar_pacote, store=0)

