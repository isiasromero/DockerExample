// Adaptador de salida: implementa el puerto ProductoRepository con MySQL.
const { CategoriaInexistente } = require('../../../domain/errores');

class MySqlProductoRepository {
  constructor(pool) {
    this.pool = pool;
  }

  // Consultas parametrizadas: evitan la inyeccion SQL
  async listar({ categoriaId } = {}) {
    const filtrar = Number.isInteger(categoriaId);
    const [rows] = await this.pool.query(
      `SELECT p.id, p.nombre, p.precio, p.stock, p.disponible, p.fecha_ingreso,
              c.codigo AS categoria_codigo, c.nombre AS categoria
         FROM productos p
        INNER JOIN categorias c ON c.id = p.categoria_id
        ${filtrar ? 'WHERE p.categoria_id = ?' : ''}
        ORDER BY p.id`,
      filtrar ? [categoriaId] : []
    );
    return rows;
  }

  async listarDetalle() {
    const [rows] = await this.pool.query(
      `SELECT p.*, c.nombre AS categoria FROM productos p
        INNER JOIN categorias c ON c.id = p.categoria_id ORDER BY p.id`
    );
    return rows;
  }

  async contar() {
    const [[{ total }]] = await this.pool.query('SELECT COUNT(*) AS total FROM productos');
    return total;
  }

  async guardar(p) {
    try {
      await this.pool.execute(
        `INSERT INTO productos (categoria_id, nombre, precio, stock, disponible, fecha_ingreso)
         VALUES (?, ?, ?, ?, ?, ?)`,
        [p.categoria_id, p.nombre, p.precio, p.stock, p.disponible, p.fecha_ingreso]
      );
    } catch (err) {
      if (err.code === 'ER_NO_REFERENCED_ROW_2') throw new CategoriaInexistente();
      throw err;
    }
  }
}

module.exports = { MySqlProductoRepository };
