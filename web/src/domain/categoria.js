// Entidad Categoria (tabla padre): normaliza y valida sus datos.
const { esFecha } = require('./fecha');
const { ErrorDeValidacion } = require('./errores');

function normalizarCategoria(entrada = {}) {
  return {
    codigo: (entrada.codigo || '').trim().toUpperCase(),
    nombre: (entrada.nombre || '').trim(),
    descripcion: (entrada.descripcion || '').trim(),
    activa: entrada.activa === true || entrada.activa === 'on',
    fecha_creacion: entrada.fecha_creacion || ''
  };
}

function validarCategoria(datos) {
  const errores = [];
  if (!/^[A-Z0-9]{5}$/.test(datos.codigo)) errores.push('El código debe tener exactamente 5 letras o números.');
  if (datos.nombre.length < 3 || datos.nombre.length > 80) errores.push('El nombre debe tener entre 3 y 80 caracteres.');
  if (!esFecha(datos.fecha_creacion)) errores.push('La fecha de creación no es válida.');
  return errores;
}

// Crea una categoria valida o lanza ErrorDeValidacion
function crearCategoria(entrada) {
  const datos = normalizarCategoria(entrada);
  const errores = validarCategoria(datos);
  if (errores.length) throw new ErrorDeValidacion(errores);
  return Object.freeze(datos);
}

module.exports = { normalizarCategoria, validarCategoria, crearCategoria };
