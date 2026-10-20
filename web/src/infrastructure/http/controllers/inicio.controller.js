// Adaptador de entrada: pagina de inicio y chequeo de salud.
const os = require('os');

function inicioController({ obtenerEstado }) {
  return {
    async inicio(req, res) {
      res.render('index', { titulo: 'Inicio', info: await obtenerEstado.ejecutar() });
    },
    salud(req, res) {
      res.json({ estado: 'ok', contenedor: os.hostname() });
    }
  };
}

module.exports = { inicioController };
