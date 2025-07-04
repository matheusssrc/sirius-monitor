import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler

# Caminhos dos arquivos
entrada_csv = "/home/umbrel/sirius/scikit/data/ia_treinamento.csv"
json_confiaveis = "/home/umbrel/sirius/scikit/data/dispositivos_confiaveis.json"
saida_csv = "/home/umbrel/sirius/scikit/data/ia_preprocessado.csv"

# Carrega o dataset principal
df = pd.read_csv(entrada_csv, na_values=["", " ", "NA", "n/a", "-", "--"])

# Remove duplicatas
df.drop_duplicates(inplace=True)

# Converte colunas numéricas (preenche com 0.0 se estiverem ausentes)
df["dns_qtd"] = pd.to_numeric(df["dns_qtd"], errors="coerce").fillna(0.0)
df["zabbix_uptime"] = pd.to_numeric(df["zabbix_uptime"], errors="coerce").fillna(0.0)
df["zabbix_latencia"] = pd.to_numeric(df["zabbix_latencia"], errors="coerce").fillna(0.0)

# Normaliza MACs para minúsculas
df["mac"] = df["mac"].astype(str).str.lower()

# Carrega o JSON com os dispositivos confiáveis
with open(json_confiaveis, "r") as f:
    confiaveis = json.load(f)

# Extrai lista de MACs confiáveis (normalizados)
macs_confiaveis = set(entry["mac"].lower() for entry in confiaveis)

# Gera a coluna 'conf_confiavel' com base na lista de MACs
df["conf_confiavel"] = df["mac"].apply(lambda x: "sim" if x in macs_confiaveis else "nao")

# Engenharia de atributos
df["frequencia_dns"] = df["dns_qtd"].apply(lambda x: "alta" if x >= 5 else "baixa")
df["latencia_alta"] = df["zabbix_latencia"].apply(lambda x: 1 if x > 200 else 0)
df["confiavel_bin"] = df["conf_confiavel"].map({"sim": 1, "nao": 0})
df["hostname_existe"] = df["hostname"].notnull().astype(int)

# Remove colunas desnecessárias para o modelo
df.drop(columns=["conf_confiavel", "ip", "mac", "hostname", "timestamp"], inplace=True, errors="ignore")

# Codifica variáveis categóricas (ex: frequencia_dns)
df = pd.get_dummies(df, columns=["frequencia_dns"], drop_first=True)

# Normaliza colunas numéricas
colunas_numericas = ["dns_qtd", "zabbix_uptime", "zabbix_latencia"]
scaler = StandardScaler()
df[colunas_numericas] = scaler.fit_transform(df[colunas_numericas])

# Exporta o dataset pronto
df.to_csv(saida_csv, index=False)
print(f"[OK] Pré-processamento finalizado com sucesso. Salvo em: {saida_csv}")
