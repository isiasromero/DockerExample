// Utilidades de fecha usadas por las reglas del dominio.

const hoy = () => new Date().toISOString().slice(0, 10);
const esFecha = (v) => /^\d{4}-\d{2}-\d{2}$/.test(v) && !Number.isNaN(Date.parse(v));

module.exports = { hoy, esFecha };
