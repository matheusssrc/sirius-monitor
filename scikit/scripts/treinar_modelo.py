import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Caminhos
entrada = "/home/umbrel/sirius/scikit/data/ia_preprocessado.csv"
modelo_saida = "/home/umbrel/sirius/scikit/models/modelo_rf.pkl"

# Carregar o dataset
df = pd.read_csv(entrada)

# Remover registros sem classe definida
df.dropna(subset=["confiavel_bin"], inplace=True)

# Garantir que o alvo seja numérico (inteiro)
df["confiavel_bin"] = df["confiavel_bin"].astype(int)

# Codificar colunas categóricas (ex: tipo_evento) se existirem
if "tipo_evento" in df.columns:
    df = pd.get_dummies(df, columns=["tipo_evento"], drop_first=True)

# Separar preditores (X) e alvo (y)
X = df.drop("confiavel_bin", axis=1)
y = df["confiavel_bin"]

# Validação: garantir que todas as colunas de X sejam numéricas
if not all(X.dtypes.apply(lambda t: pd.api.types.is_numeric_dtype(t))):
    print("[ERRO] Existem colunas não numéricas em X:")
    print(X.dtypes)
    exit(1)

# Separar treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Treinar o modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Avaliação
y_pred = modelo.predict(X_test)
print("[Matriz de Confusão]")
print(confusion_matrix(y_test, y_pred))
print("\n[Relatório de Classificação]")
print(classification_report(y_test, y_pred, target_names=["Nao confiavel", "Confiavel"]))

# Salvar modelo
joblib.dump(modelo, modelo_saida)
print(f"\n[OK] Modelo salvo em: {modelo_saida}")
