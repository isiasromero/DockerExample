// Servidor Express: vistas, archivos estaticos, datos comunes y manejo de errores.
const path = require('path');
const os = require('os');
const express = require('express');

const RAIZ = path.join(__dirname, '..', '..', '..');

function crearServidor(rutas) {
  const app = express();
  app.set('view engine', 'ejs');
  app.set('views', path.join(RAIZ, 'views'));
  app.use(express.urlencoded({ extended: false }));
  app.use(express.static(path.join(RAIZ, 'public')));

  // Datos comunes para todas las vistas
  app.use((req, res, next) => {
    res.locals.ruta = req.path;
    res.locals.contenedor = os.hostname(); // en Docker corresponde al ID del contenedor
    res.locals.ok = req.query.ok || null;
    next();
  });

  app.use(rutas);

  app.use((req, res) => res.status(404).render('error', { titulo: 'No encontrado', mensaje: 'La página solicitada no existe.' }));
  app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).render('error', { titulo: 'Error', mensaje: 'Ocurrió un error al procesar la solicitud: ' + err.message });
  });
  return app;
}

module.exports = { crearServidor };
