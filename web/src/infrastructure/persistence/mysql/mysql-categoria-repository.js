// Adaptador de salida: implementa el puerto CategoriaRepository con MySQL.
const { CategoriaDuplicada } = require('../../../domain/errores');

class MySqlCategoriaRepository {
  constructor(pool) {
    this.pool = pool;
  }

  async listarConTotales() {
    const [rows] = await this.pool.query(
      `SELECT c.*, COUNT(p.id) AS total_productos
         FROM categorias c
         LEFT JOIN productos p ON p.categoria_id = c.id
        GROUP BY c.id
        ORDER BY c.id`
    );
    return rows;
  }

  async listarActivas() {
    const [rows] = await this.pool.query('SELECT id, codigo, nombre FROM categorias WHERE activa = TRUE ORDER BY nombre');
    return rows;
  }

  async listarNombres() {
    const [rows] = await this.pool.query('SELECT id, nombre FROM categorias ORDER BY nombre');
    return rows;
  }

  async contar() {
    const [[{ total }]] = await this.pool.query('SELECT COUNT(*) AS total FROM categorias');
    return total;
  }

  async guardar(c) {
    try {
      await this.pool.execute(
        `INSERT INTO categorias (codigo, nombre, descripcion, activa, fecha_creacion)
         VALUES (?, ?, ?, ?, ?)`,
        [c.codigo, c.nombre, c.descripcion || null, c.activa, c.fecha_creacion]
      );
    } catch (err) {
      if (err.code === 'ER_DUP_ENTRY') throw new CategoriaDuplicada();
      throw err;
    }
  }
}

module.exports = { MySqlCategoriaRepository };
