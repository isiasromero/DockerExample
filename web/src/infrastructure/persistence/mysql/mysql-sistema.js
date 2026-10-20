// Adaptador de salida: implementa el puerto Sistema (version de MySQL y datos del contenedor).
const os = require('os');

class MySqlSistema {
  constructor(pool, db) {
    this.pool = pool;
    this.db = db;
  }

  async versionBaseDeDatos() {
    const [[{ version }]] = await this.pool.query('SELECT VERSION() AS version');
    return version;
  }

  descripcion() {
    return {
      dbHost: this.db.host,
      dbName: this.db.database,
      node: process.version,
      so: `${os.type()} ${os.release()}`
    };
  }
}

module.exports = { MySqlSistema };
