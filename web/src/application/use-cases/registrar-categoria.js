// Caso de uso: registrar una categoria (tabla padre).
const { crearCategoria, normalizarCategoria } = require('../../domain/categoria');
const { ErrorDeValidacion, CategoriaDuplicada } = require('../../domain/errores');
const { hoy } = require('../../domain/fecha');

function registrarCategoria({ categoriaRepo }) {
  async function formulario(datos = { fecha_creacion: hoy(), activa: true }, errores = []) {
    return { categorias: await categoriaRepo.listarConTotales(), datos, errores };
  }

  async function ejecutar(entrada) {
    try {
      const categoria = crearCategoria(entrada);
      await categoriaRepo.guardar(categoria);
      return { ok: true, categoria };
    } catch (err) {
      if (err instanceof ErrorDeValidacion) return { ok: false, ...(await formulario(normalizarCategoria(entrada), err.errores)) };
      if (err instanceof CategoriaDuplicada) return { ok: false, ...(await formulario(normalizarCategoria(entrada), [err.message])) };
      throw err;
    }
  }

  return { formulario, ejecutar };
}

module.exports = { registrarCategoria };
