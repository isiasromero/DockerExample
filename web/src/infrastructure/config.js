// Configuracion leida de las variables de entorno (definidas en docker-compose.yml).
module.exports = {
  puerto: Number(process.env.PORT || 3000),
  db: {
    host: process.env.DB_HOST || 'localhost',
    port: Number(process.env.DB_PORT || 3306),
    user: process.env.DB_USER || 'app',
    password: process.env.DB_PASSWORD || 'app123',
    database: process.env.DB_NAME || 'tienda'
  }
};
