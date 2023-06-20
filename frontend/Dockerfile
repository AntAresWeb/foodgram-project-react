# Dockerfile for frontend container
FROM node:12.20.0-alpine as build
WORKDIR /app
COPY package*.json ./
COPY ../docs ./
COPY ../infra/nginx.conf ./nginx/
RUN npm install
COPY . ./
RUN npm run build
#CMD cp -r build result_build
