// Adaptadores en memoria: implementan los mismos puertos que MySQL, para probar sin base de datos.
const { CategoriaDuplicada, CategoriaInexistente } = require('../src/domain/errores');

function crearRepositoriosEnMemoria() {
  const categorias = [{ id: 1, codigo: 'TEC01', nombre: 'Tecnología', activa: true }];
  const productos = [];

  const categoriaRepo = {
    listarConTotales: async () => categorias.map((c) => ({ ...c, total_productos: productos.filter((p) => p.categoria_id === c.id).length })),
    listarActivas: async () => categorias.filter((c) => c.activa),
    listarNombres: async () => categorias.map(({ id, nombre }) => ({ id, nombre })),
    contar: async () => categorias.length,
    guardar: async (c) => {
      if (categorias.some((x) => x.codigo === c.codigo)) throw new CategoriaDuplicada();
      categorias.push({ id: categorias.length + 1, ...c });
    }
  };

  const productoRepo = {
    listar: async ({ categoriaId } = {}) => productos.filter((p) => !Number.isInteger(categoriaId) || p.categoria_id === categoriaId),
    listarDetalle: async () => productos,
    contar: async () => productos.length,
    guardar: async (p) => {
      if (!categorias.some((c) => c.id === p.categoria_id)) throw new CategoriaInexistente();
      productos.push({ id: productos.length + 1, ...p });
    }
  };

  return { categoriaRepo, productoRepo };
}

module.exports = { crearRepositoriosEnMemoria };
