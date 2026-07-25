# 1. Use an actively supported Node 20 base image
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./

# Install clean project dependencies without injecting outdated packages
RUN npm install

COPY . .

RUN npm run build

# 2. Use the latest stable Nginx image (includes fixed OS packages)
FROM nginx:alpine

# Clean build: No hardcoded secrets or extra OS packages

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
