-- Respaldo: carga los mismos 15 productos de datos-prueba.csv directamente en MySQL.
-- Uso (solo si no se ingresan desde la aplicacion web):
--   docker exec -i mysql-db mysql -uapp -papp123 tienda < db/seed-productos.sql
SET NAMES utf8mb4;
USE tienda;

INSERT INTO productos (categoria_id, nombre, precio, stock, disponible, fecha_ingreso) VALUES
  (1, 'Mouse inalámbrico Logitech',     45000,   25, TRUE,  '2026-09-01'),
  (1, 'Teclado mecánico RGB',          189900,   12, TRUE,  '2026-09-02'),
  (1, 'Monitor 24 pulgadas Full HD',   649000,    8, TRUE,  '2026-09-03'),
  (1, 'Memoria USB 64 GB',              32000,   40, TRUE,  '2026-09-05'),
  (2, 'Licuadora 600 W',               219000,   10, TRUE,  '2026-09-06'),
  (2, 'Juego de ollas x5',             285000,    6, TRUE,  '2026-09-08'),
  (2, 'Cafetera de goteo',             129900,    0, FALSE, '2026-09-09'),
  (2, 'Lámpara LED de escritorio',      58500,   15, TRUE,  '2026-09-10'),
  (3, 'Balón de fútbol N.° 5',          89900,   20, TRUE,  '2026-09-12'),
  (3, 'Mancuernas 5 kg (par)',         120000,    9, TRUE,  '2026-09-13'),
  (3, 'Tapete de yoga',                 65000,   18, TRUE,  '2026-09-15'),
  (3, 'Bicicleta estática',           1150000,    2, FALSE, '2026-09-16'),
  (4, 'Cuaderno argollado 100 hojas',   12500,   60, TRUE,  '2026-09-18'),
  (4, 'Caja de lapiceros x12',          18900,   35, TRUE,  '2026-09-19'),
  (4, 'Resma papel carta',              24900,   30, TRUE,  '2026-09-20');
