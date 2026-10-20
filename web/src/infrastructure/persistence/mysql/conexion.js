// Pool de conexiones a MySQL y espera inicial hasta que la base de datos responda.
const mysql = require('mysql2/promise');

function crearPool(db) {
  return mysql.createPool({
    ...db,
    waitForConnections: true,
    connectionLimit: 10,
    dateStrings: true,      // devuelve DATE/DATETIME como texto (sin desfase de zona horaria)
    charset: 'utf8mb4'
  });
}

// Espera a que MySQL acepte conexiones (util al arrancar los contenedores)
async function esperarBaseDeDatos(pool, db, intentos = 30, esperaMs = 2000) {
  for (let i = 1; i <= intentos; i++) {
    try {
      await pool.query('SELECT 1');
      console.log(`[db] Conectado a MySQL en ${db.host}:${db.port}`);
      return;
    } catch (err) {
      console.log(`[db] Intento ${i}/${intentos}: MySQL aun no responde (${err.code})`);
      await new Promise((r) => setTimeout(r, esperaMs));
    }
  }
  throw new Error('No fue posible conectar con la base de datos');
}

module.exports = { crearPool, esperarBaseDeDatos };
