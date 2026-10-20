// Pruebas de los casos de uso con adaptadores en memoria (node --test).
const test = require('node:test');
const assert = require('node:assert');
const { crearRepositoriosEnMemoria } = require('./en-memoria');
const { registrarProducto } = require('../src/application/use-cases/registrar-producto');
const { registrarCategoria } = require('../src/application/use-cases/registrar-categoria');
const { consultarProductos } = require('../src/application/use-cases/consultar-productos');

const producto = { categoria_id: '1', nombre: 'Mouse inalámbrico', precio: '45000', stock: '25', disponible: 'on', fecha_ingreso: '2026-09-01' };

test('registra un producto valido', async () => {
  const repos = crearRepositoriosEnMemoria();
  const r = await registrarProducto(repos).ejecutar(producto);
  assert.equal(r.ok, true);
  assert.equal(await repos.productoRepo.contar(), 1);
});

test('rechaza precio negativo y nombre vacio', async () => {
  const repos = crearRepositoriosEnMemoria();
  const r = await registrarProducto(repos).ejecutar({ ...producto, nombre: '', precio: '-5' });
  assert.equal(r.ok, false);
  assert.ok(r.errores.includes('El precio debe ser un número mayor o igual a 0.'));
  assert.ok(r.errores.includes('El nombre debe tener entre 3 y 100 caracteres.'));
  assert.equal(await repos.productoRepo.contar(), 0);
});

test('no acepta una categoria inexistente (llave foranea)', async () => {
  const r = await registrarProducto(crearRepositoriosEnMemoria()).ejecutar({ ...producto, categoria_id: '99' });
  assert.deepEqual(r.errores, ['La categoría seleccionada no existe.']);
});

test('no permite codigos de categoria duplicados', async () => {
  const repos = crearRepositoriosEnMemoria();
  const r = await registrarCategoria(repos).ejecutar({ codigo: 'tec01', nombre: 'Otra', fecha_creacion: '2026-10-17', activa: 'on' });
  assert.deepEqual(r.errores, ['Ya existe una categoría con ese código.']);
});

test('calcula el resumen del inventario', async () => {
  const repos = crearRepositoriosEnMemoria();
  await registrarProducto(repos).ejecutar(producto);
  await registrarProducto(repos).ejecutar({ ...producto, nombre: 'Teclado', precio: '100', stock: '2', disponible: '' });
  const { resumen } = await consultarProductos(repos).ejecutar();
  assert.deepEqual(resumen, { total: 2, unidades: 27, valor: 45000 * 25 + 200, disponibles: 1 });
});
