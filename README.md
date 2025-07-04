# SIRIUS - Inteligencia Artificial Local para Monitoramento de Rede

O objetivo deste modulo do projeto SIRIUS e realizar a deteccao inteligente de dispositivos e atividades incomuns na rede local, utilizando coleta de dados com Zabbix, Scapy e Pi-hole, aliando isso a um modelo de IA local com Scikit-learn e a automacao de alertas via n8n + Telegram.

## Como funciona

1. Zabbix coleta metricas e eventos do sistema.
2. Scapy escuta pacotes ARP e DHCP, detectando novos dispositivos.
3. Pi-hole registra todos os dominios consultados na rede.
4. Todos os dados sao processados e combinados em arquivos JSON e CSV dentro da pasta scikit/.
5. Um modelo treinado com Scikit-learn identifica padroes de comportamento e aponta possiveis anomalias.
6. O n8n orquestra o fluxo de dados, decide quando acionar alertas e envia mensagens automatizadas ao Telegram para aprovacao ou bloqueio.

## Funcionalidades

- Coleta automatica de:
  - Dispositivos conectados via pacotes ARP e DHCP (Scapy)
  - Consultas DNS via banco do Pi-hole
  - Eventos e metricas via API REST do Zabbix
- Unificacao de dados em tempo real
- Treinamento e uso de IA local com Scikit-learn
- Envio de alertas para Telegram com sugestao da IA (Aprovar ou Bloquear)
- Execucao 100 por cento offline e local, sem dependencia de nuvem externa

## Organizacao do Projeto

Este modulo esta estruturado em:

sirius/
└── scikit/
    ├── data/                # Dados coletados (dns, zabbix, scapy, dispositivos confiaveis)
    ├── models/              # Modelos treinados da IA
    ├── scripts/             # Scripts de processamento e treinamento
    └── main.py              # Script de inferencia da IA

O n8n executa o fluxo:

- Recebe Webhooks do Scapy
- Verifica se o dispositivo e confiavel
- Aciona a IA para tomada de decisao
- Envia alerta ao Telegram

## Inteligencia Artificial

A IA local foi treinada com dados reais da rede:

- Classificacao binaria (comportamento normal ou suspeito)
- Modelo base: RandomForestClassifier
- Dataset unificado com cruzamento de IP, MAC, hostname, vendor e dados de DNS e Zabbix

A IA e atualizada com novas decisoes enviadas via Telegram.

## Integracoes

| Componente  | Descricao                                                                 |
|-------------|---------------------------------------------------------------------------|
| Scapy       | Escuta passiva de pacotes ARP e DHCP, detectando novos dispositivos       |
| Pi-hole     | Extracao de logs DNS diretamente do banco pihole-FTL.db                   |
| Zabbix      | Consulta via API REST para extrair eventos e estado de hosts              |
| n8n         | Orquestra as acoes e envia alertas para Telegram                          |
| Telegram    | Bot envia mensagens com sugestao da IA e registra resposta do usuario     |

## Fluxo de Deteccao

1. Novo dispositivo detectado envia webhook ao n8n
2. n8n consulta lista de confiaveis
3. Caso nao encontrado, IA e acionada
4. Se IA classificar como suspeito, um alerta e enviado para o Telegram
5. Usuario pode aprovar ou bloquear
6. Feedback e registrado e usado no proximo treino da IA

## Requisitos

- Python 3.10 ou superior
- Pi-hole e Zabbix funcionando na rede local
- Bot do Telegram com webhook ativo
- n8n instalado (pode rodar no Umbrel)
- Permissao de leitura nos diretorios do Pi-hole e Zabbix

## IA com Scikit-learn

- main.py executa a classificacao
- processamento_dados.py prepara os dados para treino
- treino_modelo.py treina e salva o modelo

## Estrutura de Arquivos

scikit/
├── data/
│   ├── arp_dhcp_dataset.jsonl
│   ├── dispositivos_confiaveis.json
│   ├── dns_ia_dataset.json
│   ├── ia_treinamento.csv
│   ├── zabbix_ia_dataset.json
│   └── ia_preprocessado.csv
│ 
├── scripts/
│   ├── arp_dhcp_sniffer.py
│   ├── coletar_zabbix_api.py
│   ├── coletor_dns_pihole.py
│   ├── extrair_log_pihole.sh
│   ├── preprocessar_dados.py
│   ├── processamento_dados.py
│   ├── treinar_modelo.py
│   ├── utils.py
│   └── webhook_sender.py
└── main.py

## Privacidade e Seguranca

Todo o processamento ocorre localmente, garantindo que nenhum dado da rede seja enviado para servidores externos. O sistema aprende com o ambiente da propria rede e se adapta com o tempo.

## Consideracoes Finais

Este modulo faz parte do projeto maior SIRIUS, voltado para monitoramento inteligente e seguro de redes residenciais. Futuramente serao adicionados:

- Interface web para gestao
- Reclassificacao automatica de dispositivos
- Bloqueio automatico via firewall ou Pi-hole

Autor: Matheus Rossi Carvalho
Projeto: SIRIUS - Smart Intelligent Response for Intrusion and Unusual Signals
LinkedIn: https://www.linkedin.com/in/matheusrossicarvalho/