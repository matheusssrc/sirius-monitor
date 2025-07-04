import requests

def enviar_webhook(tipo, ip, mac, hostname="Desconhecido", vendor_class="Desconhecido", requested_ip="Desconhecido", data_detectado="Desconhecido"):
    url = "http://umbrel.local:5678/webhook/sirius-ingest"

    payload = {
        "tipo": tipo,
        "ip": ip,
        "mac": mac,
        "hostname": hostname,
        "vendor_class": vendor_class,
        "requested_ip": requested_ip,
        "data_detectado": data_detectado
    }

    try:
        response = requests.post(url, json=payload, timeout=3)
        print(f"Webhook enviado com sucesso: {payload} - Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar Webhook: {e}")
