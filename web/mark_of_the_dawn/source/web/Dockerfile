FROM node:24.1.0-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

USER 404:404
CMD ["node", "index.js"]
