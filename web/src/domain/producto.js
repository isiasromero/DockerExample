// Entidad Producto (tabla hija): normaliza, valida y calcula el resumen del inventario.
const { esFecha } = require('./fecha');
const { ErrorDeValidacion } = require('./errores');

function normalizarProducto(entrada = {}) {
  return {
    categoria_id: Number.parseInt(entrada.categoria_id, 10),
    nombre: (entrada.nombre || '').trim(),
    precio: Number.parseFloat(entrada.precio),
    stock: Number.parseInt(entrada.stock, 10),
    disponible: entrada.disponible === true || entrada.disponible === 'on',
    fecha_ingreso: entrada.fecha_ingreso || ''
  };
}

function validarProducto(datos) {
  const errores = [];
  if (!Number.isInteger(datos.categoria_id)) errores.push('Seleccione una categoría.');
  if (datos.nombre.length < 3 || datos.nombre.length > 100) errores.push('El nombre debe tener entre 3 y 100 caracteres.');
  if (!Number.isFinite(datos.precio) || datos.precio < 0) errores.push('El precio debe ser un número mayor o igual a 0.');
  if (!Number.isInteger(datos.stock) || datos.stock < 0) errores.push('El stock debe ser un número entero mayor o igual a 0.');
  if (!esFecha(datos.fecha_ingreso)) errores.push('La fecha de ingreso no es válida.');
  return errores;
}

function crearProducto(entrada) {
  const datos = normalizarProducto(entrada);
  const errores = validarProducto(datos);
  if (errores.length) throw new ErrorDeValidacion(errores);
  return Object.freeze(datos);
}

// Regla de negocio: totales del inventario mostrados en el listado
function resumenInventario(productos) {
  return {
    total: productos.length,
    unidades: productos.reduce((s, p) => s + Number(p.stock), 0),
    valor: productos.reduce((s, p) => s + Number(p.precio) * Number(p.stock), 0),
    disponibles: productos.filter((p) => p.disponible).length
  };
}

module.exports = { normalizarProducto, validarProducto, crearProducto, resumenInventario };
