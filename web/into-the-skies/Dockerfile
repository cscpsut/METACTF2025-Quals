FROM node:22-alpine

WORKDIR /app

COPY source/package.json .

RUN npm install

RUN npm i -g serve

COPY source/ .

RUN npm run build

EXPOSE 3000

CMD [ "serve", "-s", "dist" ]