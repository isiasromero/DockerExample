// Punto de composicion: crea los adaptadores, los conecta a los casos de uso y arranca el servidor.
const os = require('os');
const config = require('./infrastructure/config');

// Adaptadores de salida (MySQL)
const { crearPool, esperarBaseDeDatos } = require('./infrastructure/persistence/mysql/conexion');
const { MySqlCategoriaRepository } = require('./infrastructure/persistence/mysql/mysql-categoria-repository');
const { MySqlProductoRepository } = require('./infrastructure/persistence/mysql/mysql-producto-repository');
const { MySqlSistema } = require('./infrastructure/persistence/mysql/mysql-sistema');

// Puertos
const { comoCategoriaRepository } = require('./application/ports/categoria-repository');
const { comoProductoRepository } = require('./application/ports/producto-repository');
const { comoSistema } = require('./application/ports/sistema');

// Casos de uso
const { registrarCategoria } = require('./application/use-cases/registrar-categoria');
const { registrarProducto } = require('./application/use-cases/registrar-producto');
const { consultarProductos } = require('./application/use-cases/consultar-productos');
const { obtenerEstado } = require('./application/use-cases/obtener-estado');

// Adaptadores de entrada (HTTP)
const { inicioController } = require('./infrastructure/http/controllers/inicio.controller');
const { categoriasController } = require('./infrastructure/http/controllers/categorias.controller');
const { productosController } = require('./infrastructure/http/controllers/productos.controller');
const { crearRutas } = require('./infrastructure/http/routes');
const { crearServidor } = require('./infrastructure/http/servidor');

const pool = crearPool(config.db);
const categoriaRepo = comoCategoriaRepository(new MySqlCategoriaRepository(pool));
const productoRepo = comoProductoRepository(new MySqlProductoRepository(pool));
const sistema = comoSistema(new MySqlSistema(pool, config.db));

const casos = {
  registrarCategoria: registrarCategoria({ categoriaRepo }),
  registrarProducto: registrarProducto({ productoRepo, categoriaRepo }),
  consultarProductos: consultarProductos({ productoRepo, categoriaRepo }),
  obtenerEstado: obtenerEstado({ sistema, categoriaRepo, productoRepo })
};

const app = crearServidor(crearRutas({
  inicio: inicioController(casos),
  categorias: categoriasController(casos),
  productos: productosController(casos)
}));

esperarBaseDeDatos(pool, config.db)
  .then(() => {
    app.listen(config.puerto, () => console.log(`[web] Servidor escuchando en http://0.0.0.0:${config.puerto} (contenedor ${os.hostname()})`));
  })
  .catch((err) => {
    console.error(err.message);
    process.exit(1);
  });
