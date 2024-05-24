# Fase 1: Construir la aplicación Vue.js con Vite
FROM node:20 as build-stage
WORKDIR /app
COPY package*.json ./
COPY nginx.conf ./
RUN npm install
COPY . .
RUN npm run build

# Fase 2: Servir la aplicación con Nginx
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]