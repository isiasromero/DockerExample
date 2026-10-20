// Puerto de salida: persistencia de productos.
const { exigirPuerto } = require('./exigir-puerto');

/**
 * @typedef {Object} ProductoRepository
 * @property {(filtro?: {categoriaId?: number}) => Promise<Object[]>} listar  Productos con su categoria (JOIN)
 * @property {() => Promise<Object[]>} listarDetalle  Todos los campos, para la API
 * @property {() => Promise<number>}   contar
 * @property {(producto: Object) => Promise<void>} guardar  Lanza CategoriaInexistente si falla la llave foranea
 */
const METODOS = ['listar', 'listarDetalle', 'contar', 'guardar'];

module.exports = { comoProductoRepository: (impl) => exigirPuerto('ProductoRepository', impl, METODOS) };
