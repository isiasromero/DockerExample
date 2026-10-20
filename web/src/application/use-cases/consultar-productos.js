// Caso de uso: consultar los productos guardados (enlace diferente al formulario).
const { resumenInventario } = require('../../domain/producto');

function consultarProductos({ productoRepo, categoriaRepo }) {
  async function ejecutar({ categoriaId } = {}) {
    const filtro = Number.isInteger(categoriaId) ? categoriaId : null;
    const productos = await productoRepo.listar({ categoriaId: filtro });
    return {
      productos,
      categorias: await categoriaRepo.listarNombres(),
      filtro,
      resumen: resumenInventario(productos)
    };
  }

  // Version para la API JSON
  const detalle = () => productoRepo.listarDetalle();

  return { ejecutar, detalle };
}

module.exports = { consultarProductos };
