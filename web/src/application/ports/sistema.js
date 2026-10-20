// Puerto de salida: informacion del entorno (motor de base de datos y contenedor).
const { exigirPuerto } = require('./exigir-puerto');

/**
 * @typedef {Object} Sistema
 * @property {() => Promise<string>} versionBaseDeDatos
 * @property {() => Object} descripcion  host y nombre de la base, version de Node, sistema y contenedor
 */
const METODOS = ['versionBaseDeDatos', 'descripcion'];

module.exports = { comoSistema: (impl) => exigirPuerto('Sistema', impl, METODOS) };
