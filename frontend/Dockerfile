# build stage
FROM node:20-alpine AS builder

WORKDIR /app

# install dependencies
COPY package*.json ./
RUN npm install


# copy source code and build
COPY . .
RUN chmod +x node_modules/.bin/*
RUN npm run build

# production stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"] 