const input = items[0].json.body;

// Normalizar MAC para letras maiúsculas
const macFormatado = input.mac ? input.mac.toUpperCase() : "Desconhecido";

// Garantir IP, Hostname e Tipo existindo
const ip = input.ip || "Desconhecido";
const hostname = input.hostname || "Desconhecido";
const tipo = input.tipo || "Desconhecido";

// Corrigir fuso horário manualmente para UTC-3 (Brasília)
const agora = new Date();
agora.setHours(agora.getHours() - 3);
const data_detectado = agora.toISOString().replace('T', ' ').split('.')[0];

return [
  {
    json: {
      tipo: tipo,
      ip: ip,
      mac: macFormatado,
      hostname: hostname,
      data_detectado: data_detectado,
      status: "Detectado"
    }
  }
];
