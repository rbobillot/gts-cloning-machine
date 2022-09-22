# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
ENV PATH /usr/node_modules/.bin:$PATH
COPY . .
RUN npm run build
EXPOSE 8080