# Tienda Docker: aplicación contenerizada (Node.js + MySQL)

Aplicación web en **Node.js** (Express, arquitectura hexagonal) conectada a una base de datos **MySQL 8**, cada una en su propio contenedor y orquestadas con **Docker Compose**. Permite registrar categorías y productos, guardarlos en MySQL y consultarlos desde un enlace diferente; los datos persisten en un volumen de Docker.

## Contenido

1. [Requisitos](#1-requisitos)
2. [Instalar Docker Desktop](#2-instalar-docker-desktop)
3. [Descargar el proyecto](#3-descargar-el-proyecto)
4. [Levantar la aplicación](#4-levantar-la-aplicación)
5. [Usar la aplicación](#5-usar-la-aplicación)
6. [Consultar los datos en MySQL](#6-consultar-los-datos-en-mysql)
7. [Probar la persistencia](#7-probar-la-persistencia)
8. [Comandos básicos de Docker (carpeta demo)](#8-comandos-básicos-de-docker-carpeta-demo)
9. [Ejecutar las pruebas](#9-ejecutar-las-pruebas)
10. [Detener y limpiar](#10-detener-y-limpiar)
11. [Arquitectura](#11-arquitectura)
12. [Modelo entidad-relación](#12-modelo-entidad-relación)
13. [Estructura del proyecto](#13-estructura-del-proyecto)
14. [Solución de problemas](#14-solución-de-problemas)

---

## 1. Requisitos

- **Docker Desktop** (Windows o macOS) o Docker Engine con Docker Compose v2 (Linux).
- **Git**, para clonar el repositorio (opcional: también se puede descargar el ZIP).
- Puertos libres en el equipo: **3000** (aplicación web) y **3307** (MySQL, opcional).

No hace falta instalar Node.js ni MySQL: todo corre dentro de los contenedores.

## 2. Instalar Docker Desktop

**Windows**

1. Descargar Docker Desktop desde la documentación oficial: <https://docs.docker.com/desktop/setup/install/windows-install/>.
2. Ejecutar el instalador y dejar marcada la opción **Use WSL 2 instead of Hyper-V** (recomendada).
3. Al terminar, reiniciar si lo pide y abrir **Docker Desktop**. Aceptar los términos; iniciar sesión no es necesario para trabajar en local.
4. Esperar a que en la parte inferior aparezca **Engine running**.

**macOS**: descargar el instalador para Apple Silicon o Intel desde <https://docs.docker.com/desktop/setup/install/mac-install/> y arrastrarlo a Aplicaciones.

**Comprobar la instalación** (en PowerShell, CMD o Terminal):

```bash
docker --version
docker compose version
docker run hello-world
```

El último comando descarga una imagen de prueba y muestra *Hello from Docker!* si todo funciona.

## 3. Descargar el proyecto

```bash
git clone https://github.com/isiasromero/DockerExample.git
cd DockerExample
```

## 4. Levantar la aplicación

Desde la carpeta del proyecto:

```bash
docker compose up -d --build
```

Este único comando:

1. Construye las imágenes `tienda-mysql:1.0` (carpeta `db/`) y `tienda-web:1.0` (carpeta `web/`).
2. Crea la red `tienda_red-tienda` y el volumen `tienda_db_data`.
3. Arranca el contenedor `mysql-db`; la primera vez ejecuta `db/init.sql`, que crea las tablas e inserta 4 categorías.
4. Cuando MySQL está *healthy* (chequeo de salud), arranca el contenedor `node-web`.

Comprobar que todo está en marcha:

```bash
docker compose ps          # mysql-db debe decir (healthy) y node-web Up
docker compose logs web    # debe mostrar "[db] Conectado a MySQL en db:3306"
```

Abrir en el navegador: **<http://localhost:3000>**

La página de inicio muestra el *hostname* del servidor, que es el ID del contenedor `node-web`. Se puede comparar con:

```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## 5. Usar la aplicación

| Página | Dirección | Qué hace |
|---|---|---|
| Inicio | <http://localhost:3000> | Estado del contenedor web y de la base de datos |
| Categorías | <http://localhost:3000/categorias> | Lista y registra categorías (tabla padre) |
| Registrar producto | <http://localhost:3000/productos/nuevo> | Formulario para ingresar productos (tabla hija) |
| Ver datos | <http://localhost:3000/productos> | Consulta MySQL con `INNER JOIN`, resumen y filtro por categoría |
| API JSON | <http://localhost:3000/api/productos> | Los mismos datos en formato JSON |

### Ingresar los 15 productos

El archivo `datos-prueba.csv` contiene 15 productos de ejemplo (categoría, nombre, precio, stock, disponible y fecha). Hay dos formas de cargarlos:

- **Desde la aplicación (recomendado):** ir a *Registrar* e ingresarlos uno por uno. Los campos se validan (por ejemplo, un precio negativo se rechaza con un mensaje de error).
- **Por consola (respaldo):**

  ```bash
  docker exec -i mysql-db mysql -uapp -papp123 tienda < db/seed-productos.sql
  ```

  En PowerShell, si el `<` no funciona, usar:

  ```powershell
  Get-Content db/seed-productos.sql | docker exec -i mysql-db mysql -uapp -papp123 tienda
  ```

Después, en *Ver datos* (<http://localhost:3000/productos>) aparecen los 15 registros.

## 6. Consultar los datos en MySQL

Directamente dentro del contenedor `mysql-db`:

```bash
docker exec mysql-db mysql -uapp -papp123 --default-character-set=utf8mb4 tienda -t -e "SHOW TABLES;"
docker exec mysql-db mysql -uapp -papp123 --default-character-set=utf8mb4 tienda -t -e "DESCRIBE productos;"
docker exec mysql-db mysql -uapp -papp123 --default-character-set=utf8mb4 tienda -t -e "SELECT COUNT(*) AS total_productos FROM productos;"
docker exec mysql-db mysql -uapp -papp123 --default-character-set=utf8mb4 tienda -t -e "SELECT p.id, p.nombre, c.nombre AS categoria, p.precio, p.disponible FROM productos p INNER JOIN categorias c ON c.id = p.categoria_id;"
```

Para una sesión interactiva: `docker exec -it mysql-db mysql -uapp -papp123 tienda`.

Desde el equipo (MySQL Workbench u otro cliente): host `localhost`, puerto `3307`, usuario `app`, clave `app123`, base `tienda`.

## 7. Probar la persistencia

```bash
docker compose down        # detiene y ELIMINA los contenedores (el volumen se conserva)
docker ps -a               # ya no hay contenedores; http://localhost:3000 no responde
docker compose up -d       # crea contenedores nuevos
docker compose ps
```

Al recargar <http://localhost:3000/productos> los 15 productos siguen ahí: MySQL guarda los datos en el volumen `tienda_db_data`, que es independiente de los contenedores.

## 8. Comandos básicos de Docker (carpeta demo)

La carpeta `demo/` tiene una imagen mínima (nginx + una página HTML) para practicar cómo se **crea y se elimina una imagen y un contenedor**:

```bash
# Imágenes
docker pull nginx:alpine                  # descargar una imagen
docker images                             # listar imágenes locales
docker image history nginx:alpine         # capas de la imagen
cd demo
docker build -t demo-web:1.0 .            # CREAR una imagen a partir del Dockerfile

# Contenedores
docker run -d --name web-demo -p 8081:80 demo-web:1.0   # CREAR un contenedor (http://localhost:8081)
docker ps                                 # contenedores en ejecución
docker logs web-demo                      # logs
docker exec web-demo ls /usr/share/nginx/html           # ejecutar un comando dentro
docker inspect web-demo --format "IP: {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} Estado: {{.State.Status}}"
docker stats --no-stream                  # consumo de CPU y memoria
docker stop web-demo                      # detener
docker rm web-demo                        # ELIMINAR el contenedor
docker rmi demo-web:1.0                   # ELIMINAR la imagen (primero el contenedor, luego la imagen)
cd ..

# Redes y volúmenes
docker network ls
docker network create red-demo && docker network inspect red-demo && docker network rm red-demo
docker volume ls
docker volume create vol-demo && docker volume inspect vol-demo && docker volume rm vol-demo

# Información del motor y limpieza
docker version                            # cliente y servidor (arquitectura cliente-servidor)
docker info
docker system df
docker container prune -f
docker image prune -f
```

## 9. Ejecutar las pruebas

Los casos de uso tienen pruebas con repositorios en memoria (no necesitan MySQL). Sin instalar Node.js, usando un contenedor temporal:

```bash
docker run --rm -v "${PWD}/web:/app" -w /app node:20-alpine sh -c "npm ci && npm test"
```

En CMD de Windows reemplazar `${PWD}` por `%cd%`. Con Node.js 20 instalado en el equipo también funciona: `cd web && npm ci && npm test`.

## 10. Detener y limpiar

```bash
docker compose down        # detiene y elimina los contenedores, conserva los datos
docker compose down -v     # además borra el volumen: la próxima vez se recrea la base desde init.sql
```

Para borrar también las imágenes construidas: `docker rmi tienda-web:1.0 tienda-mysql:1.0`.

## 11. Arquitectura

**Contenedores**

```
   Navegador ──► localhost:3000 ──►  node-web (tienda-web:1.0)
                                        │  red red-tienda (bridge), host "db"
                                        ▼
   Workbench ──► localhost:3307 ──►  mysql-db (tienda-mysql:1.0) ──► volumen db_data
```

- `node-web` se conecta a MySQL usando el nombre del servicio, `db`, gracias a la red de Docker Compose.
- `node-web` solo arranca cuando `mysql-db` pasa su chequeo de salud (`mysqladmin ping`).
- La imagen web corre con el usuario `node` (no root) e instala dependencias en una capa aparte para aprovechar la caché.

**Aplicación web: arquitectura hexagonal (puertos y adaptadores)**

- **Dominio** (`web/src/domain`): entidades `Categoria` y `Producto`, sus reglas de validación y errores. No depende de Express ni de MySQL.
- **Aplicación** (`web/src/application`): *puertos* (contratos de los repositorios) y *casos de uso* (registrar categoría, registrar producto, consultar productos, estado).
- **Infraestructura** (`web/src/infrastructure`): adaptador de salida para MySQL (consultas parametrizadas, sin inyección SQL) y adaptador de entrada HTTP con Express (servidor, rutas y controladores).
- **Composición** (`web/src/main.js`): crea los adaptadores, los conecta a los casos de uso y arranca el servidor.

Gracias a los puertos, los casos de uso se prueban con repositorios en memoria (`web/tests`), y cambiar de base de datos solo requeriría un adaptador nuevo.

## 12. Modelo entidad-relación

`categorias` (1) ── (N) `productos`, mediante la llave foránea `productos.categoria_id → categorias.id` (`ON DELETE RESTRICT`). Cada tabla tiene 7 columnas con distintos tipos de datos:

| categorias | Tipo | productos | Tipo |
|---|---|---|---|
| id | INT PK, autoincremental | id | INT PK, autoincremental |
| codigo | CHAR(5) UNIQUE | categoria_id | INT FK |
| nombre | VARCHAR(80) | nombre | VARCHAR(100) |
| descripcion | TEXT | precio | DECIMAL(10,2), CHECK ≥ 0 |
| activa | BOOLEAN | stock | INT, CHECK ≥ 0 |
| fecha_creacion | DATE | disponible | BOOLEAN |
| actualizado_en | DATETIME | fecha_ingreso | DATE |

El script completo está en `db/init.sql`.

## 13. Estructura del proyecto

```
DockerExample/
├── docker-compose.yml        Orquesta los dos servicios, la red y el volumen
├── datos-prueba.csv          Los 15 productos de ejemplo
├── db/                       Imagen tienda-mysql:1.0 (MySQL 8.0)
│   ├── Dockerfile
│   ├── init.sql              Script de la base de datos (tablas, llave foránea, CHECK, datos iniciales)
│   ├── seed-productos.sql    Carga los 15 productos por consola
│   └── cliente-utf8.cnf      El cliente mysql usa utf8mb4 (tildes correctas)
├── web/                      Imagen tienda-web:1.0 (Node 20 alpine)
│   ├── Dockerfile
│   ├── package.json          npm start · npm test
│   ├── src/
│   │   ├── domain/           Entidades, validaciones y errores
│   │   ├── application/
│   │   │   ├── ports/        Puertos de los repositorios
│   │   │   └── use-cases/    Casos de uso
│   │   ├── infrastructure/
│   │   │   ├── persistence/mysql/  Adaptadores MySQL
│   │   │   └── http/         Servidor, rutas y controladores (Express)
│   │   └── main.js           Punto de composición
│   ├── tests/                Pruebas con repositorios en memoria
│   ├── views/                Vistas EJS
│   └── public/estilos.css
└── demo/                     Imagen mínima (nginx) para practicar comandos de Docker
```

## 14. Solución de problemas

- **El puerto 3000 o 3307 está ocupado:** cambiar el lado izquierdo del mapeo en `docker-compose.yml` (por ejemplo `"3001:3000"`) y abrir ese puerto.
- **Cambié `db/init.sql` y no se aplica:** el script solo se ejecuta con el volumen vacío. Ejecutar `docker compose down -v` y luego `docker compose up -d --build`.
- **`docker` no responde o dice que no encuentra el motor:** abrir Docker Desktop y esperar a *Engine running*.
- **Las tildes salen mal en la consola de MySQL:** usar `--default-character-set=utf8mb4`, como en los comandos de la sección 6.
- **La aplicación no conecta a la base de datos:** revisar `docker compose logs db` y `docker compose logs web`; el servidor web reintenta la conexión durante un minuto al arrancar.
