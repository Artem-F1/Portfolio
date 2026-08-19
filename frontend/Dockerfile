FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Используем минимальный образ и ставим serve
FROM node:18-alpine
RUN npm install -g serve
WORKDIR /app
COPY --from=builder /app/dist .
EXPOSE 5173
CMD ["serve", "-s", ".", "-l", "5173"]