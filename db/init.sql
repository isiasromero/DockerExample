-- =====================================================================
-- Script de base de datos: tienda
-- Motor: MySQL 8.0
-- Modelo entidad-relacion: categorias (1) ---- (N) productos
-- Se ejecuta automaticamente la primera vez que arranca el contenedor
-- (carpeta /docker-entrypoint-initdb.d de la imagen oficial de MySQL).
-- =====================================================================

SET NAMES utf8mb4;
SET time_zone = '-05:00';

CREATE DATABASE IF NOT EXISTS tienda
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tienda;

-- ---------------------------------------------------------------------
-- Tabla padre: categorias (7 columnas)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
  id              INT           NOT NULL AUTO_INCREMENT,           -- entero
  codigo          CHAR(5)       NOT NULL,                          -- caracter fijo
  nombre          VARCHAR(80)   NOT NULL,                          -- cadena
  descripcion     TEXT          NULL,                              -- texto largo
  activa          BOOLEAN       NOT NULL DEFAULT TRUE,             -- booleano
  fecha_creacion  DATE          NOT NULL,                          -- fecha
  actualizado_en  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                ON UPDATE CURRENT_TIMESTAMP,       -- fecha y hora
  CONSTRAINT pk_categorias PRIMARY KEY (id),
  CONSTRAINT uq_categorias_codigo UNIQUE (codigo)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Tabla hija: productos (7 columnas), depende de categorias
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
  id              INT            NOT NULL AUTO_INCREMENT,          -- entero
  categoria_id    INT            NOT NULL,                         -- entero (llave foranea)
  nombre          VARCHAR(100)   NOT NULL,                         -- cadena
  precio          DECIMAL(10,2)  NOT NULL,                         -- decimal
  stock           INT            NOT NULL DEFAULT 0,               -- entero
  disponible      BOOLEAN        NOT NULL DEFAULT TRUE,            -- booleano
  fecha_ingreso   DATE           NOT NULL,                         -- fecha
  CONSTRAINT pk_productos PRIMARY KEY (id),
  CONSTRAINT fk_productos_categorias
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  CONSTRAINT ck_productos_precio CHECK (precio >= 0),
  CONSTRAINT ck_productos_stock  CHECK (stock >= 0)
) ENGINE = InnoDB;

CREATE INDEX ix_productos_categoria ON productos (categoria_id);

-- ---------------------------------------------------------------------
-- Datos iniciales de la tabla padre (los 15 productos se ingresan
-- desde la aplicacion web durante la demostracion)
-- ---------------------------------------------------------------------
INSERT INTO categorias (codigo, nombre, descripcion, activa, fecha_creacion) VALUES
  ('TEC01', 'Tecnología', 'Equipos de cómputo, periféricos y accesorios electrónicos', TRUE, '2026-01-15'),
  ('HOG01', 'Hogar',      'Artículos para cocina, limpieza y decoración del hogar',     TRUE, '2026-02-01'),
  ('DEP01', 'Deportes',   'Implementos deportivos y ropa para actividad física',       TRUE, '2026-03-10'),
  ('PAP01', 'Papelería',  'Útiles escolares y de oficina',                              TRUE, '2026-04-05');

-- ---------------------------------------------------------------------
-- Consultas de verificacion (para mostrar en el video)
-- ---------------------------------------------------------------------
-- SHOW TABLES;
-- DESCRIBE categorias;
-- DESCRIBE productos;
-- SELECT COUNT(*) AS total_productos FROM productos;
-- SELECT p.id, p.nombre, c.nombre AS categoria, p.precio, p.stock,
--        p.disponible, p.fecha_ingreso
--   FROM productos p
--   INNER JOIN categorias c ON c.id = p.categoria_id
--   ORDER BY p.id;
