// Adaptador de entrada: traduce HTTP <-> casos de uso de categorias.
function categoriasController({ registrarCategoria }) {
  return {
    // GET /categorias
    async formulario(req, res) {
      res.render('categorias', { titulo: 'Categorías', ...(await registrarCategoria.formulario()) });
    },

    // POST /categorias
    async registrar(req, res) {
      const r = await registrarCategoria.ejecutar(req.body);
      if (r.ok) return res.redirect('/categorias?ok=' + encodeURIComponent(`Categoría "${r.categoria.nombre}" guardada.`));
      res.status(400).render('categorias', { titulo: 'Categorías', ...r });
    }
  };
}

module.exports = { categoriasController };
