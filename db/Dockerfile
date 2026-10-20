# Imagen de la base de datos relacional
FROM mysql:8.0

LABEL proyecto="Actividad sumativa Docker" \
      componente="base-de-datos"

# Codificacion y zona horaria del servidor
ENV TZ=America/Bogota

# El cliente mysql (docker exec ... mysql) usa utf8mb4 para mostrar bien las tildes
COPY cliente-utf8.cnf /etc/mysql/conf.d/cliente-utf8.cnf

# El script se ejecuta solo la primera vez (cuando el volumen esta vacio)
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql

EXPOSE 3306
