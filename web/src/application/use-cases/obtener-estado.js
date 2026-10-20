// Caso de uso: estado del sistema para la pagina de inicio.
function obtenerEstado({ sistema, categoriaRepo, productoRepo }) {
  async function ejecutar() {
    const [version, categorias, productos] = await Promise.all([
      sistema.versionBaseDeDatos(),
      categoriaRepo.contar(),
      productoRepo.contar()
    ]);
    return { version, categorias, productos, ...sistema.descripcion() };
  }
  return { ejecutar };
}

module.exports = { obtenerEstado };
