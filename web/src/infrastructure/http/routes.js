// Rutas HTTP: cada una delega en un controlador.
const { Router } = require('express');

// Pasa los errores de las funciones async al manejador de errores de Express
const seguro = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

function crearRutas({ inicio, categorias, productos }) {
  const r = Router();
  r.get('/', seguro(inicio.inicio));
  r.get('/salud', inicio.salud);

  r.get('/categorias', seguro(categorias.formulario));
  r.post('/categorias', seguro(categorias.registrar));

  r.get('/productos/nuevo', seguro(productos.formulario));
  r.post('/productos', seguro(productos.registrar));
  r.get('/productos', seguro(productos.listar));
  r.get('/api/productos', seguro(productos.api));
  return r;
}

module.exports = { crearRutas };
