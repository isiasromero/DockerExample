// Caso de uso: registrar un producto (formulario de ingreso de los 15 datos).
const { crearProducto, normalizarProducto } = require('../../domain/producto');
const { ErrorDeValidacion, CategoriaInexistente } = require('../../domain/errores');
const { hoy } = require('../../domain/fecha');

function registrarProducto({ productoRepo, categoriaRepo }) {
  // Datos que necesita el formulario: categorias activas y cuantos productos hay
  async function formulario(datos = { fecha_ingreso: hoy(), disponible: true, stock: 0 }, errores = []) {
    return { categorias: await categoriaRepo.listarActivas(), total: await productoRepo.contar(), datos, errores };
  }

  async function ejecutar(entrada) {
    try {
      const producto = crearProducto(entrada);
      await productoRepo.guardar(producto);
      return { ok: true, producto };
    } catch (err) {
      if (err instanceof ErrorDeValidacion) return { ok: false, ...(await formulario(normalizarProducto(entrada), err.errores)) };
      if (err instanceof CategoriaInexistente) return { ok: false, ...(await formulario(normalizarProducto(entrada), [err.message])) };
      throw err;
    }
  }

  return { formulario, ejecutar };
}

module.exports = { registrarProducto };
