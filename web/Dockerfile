# Imagen del servidor web (Node.js + Express)
FROM node:20-alpine

LABEL proyecto="Actividad sumativa Docker" \
      componente="servidor-web"

ENV NODE_ENV=production \
    TZ=America/Bogota

WORKDIR /app

# Primero dependencias (aprovecha la cache de capas)
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Luego el codigo fuente
COPY . .

# Ejecutar sin privilegios de root
USER node

EXPOSE 3000

CMD ["node", "src/main.js"]
