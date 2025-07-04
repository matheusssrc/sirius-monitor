// Pega todos os itens do Merge
const todosOsItens = items.map(item => item.json);

// Cria um mapa para agrupar os status por MAC
const mapaMacs = {};

// Primeiro, organiza os status por MAC
todosOsItens.forEach(item => {
  const mac = item.mac ? item.mac.toUpperCase() : "DESCONHECIDO";
  if (!mapaMacs[mac]) {
    mapaMacs[mac] = [];
  }
  mapaMacs[mac].push(item.status);
});

// Agora, filtra os MACs que são "Detectado" mas não "Confiável"
const resultado = [];

for (const mac in mapaMacs) {
  const statuses = mapaMacs[mac];
  const contemConfiavel = statuses.includes("Confiável");
  const contemDetectado = statuses.includes("Detectado");

  if (contemDetectado && !contemConfiavel) {
    // Pega o primeiro item detectado com esse MAC
    const itemDetectado = todosOsItens.find(item => 
      item.mac.toUpperCase() === mac && item.status === "Detectado"
    );

    if (itemDetectado) {
      resultado.push({ json: { ...itemDetectado, statusFinal: "Desconhecido" } });
    }
  }
}

return resultado;
