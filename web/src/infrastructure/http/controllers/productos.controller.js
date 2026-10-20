// Adaptador de entrada: traduce HTTP <-> casos de uso de productos.
const os = require('os');

function productosController({ registrarProducto, consultarProductos }) {
  return {
    // GET /productos/nuevo
    async formulario(req, res) {
      res.render('producto-form', { titulo: 'Registrar producto', ...(await registrarProducto.formulario()) });
    },

    // POST /productos
    async registrar(req, res) {
      const r = await registrarProducto.ejecutar(req.body);
      if (r.ok) return res.redirect('/productos/nuevo?ok=' + encodeURIComponent(`Producto "${r.producto.nombre}" guardado en MySQL.`));
      res.status(400).render('producto-form', { titulo: 'Registrar producto', ...r });
    },

    // GET /productos (enlace diferente: consulta la base de datos)
    async listar(req, res) {
      const categoriaId = Number.parseInt(req.query.categoria, 10);
      res.render('productos', { titulo: 'Productos registrados', ...(await consultarProductos.ejecutar({ categoriaId })) });
    },

    // GET /api/productos
    async api(req, res) {
      const productos = await consultarProductos.detalle();
      res.json({ contenedor: os.hostname(), total: productos.length, productos });
    }
  };
}

module.exports = { productosController };
