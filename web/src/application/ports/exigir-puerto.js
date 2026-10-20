// Verifica al arrancar que un adaptador cumple el contrato de su puerto.
function exigirPuerto(nombre, impl, metodos) {
  const faltan = metodos.filter((m) => typeof impl?.[m] !== 'function');
  if (faltan.length) throw new Error(`${nombre}: el adaptador no implementa ${faltan.join(', ')}`);
  return impl;
}

module.exports = { exigirPuerto };
