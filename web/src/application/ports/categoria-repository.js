// Puerto de salida: lo que la aplicacion necesita para persistir categorias.
// Cualquier adaptador (MySQL, memoria, etc.) debe implementar estos metodos.
const { exigirPuerto } = require('./exigir-puerto');

/**
 * @typedef {Object} CategoriaRepository
 * @property {() => Promise<Object[]>} listarConTotales  Categorias con su numero de productos
 * @property {() => Promise<Object[]>} listarActivas     id, codigo y nombre de las activas
 * @property {() => Promise<Object[]>} listarNombres     id y nombre de todas (para filtros)
 * @property {() => Promise<number>}   contar
 * @property {(categoria: Object) => Promise<void>} guardar  Lanza CategoriaDuplicada si el codigo existe
 */
const METODOS = ['listarConTotales', 'listarActivas', 'listarNombres', 'contar', 'guardar'];

module.exports = { comoCategoriaRepository: (impl) => exigirPuerto('CategoriaRepository', impl, METODOS) };
