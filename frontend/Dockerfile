# Dockerfile for frontend container
FROM node:12.20.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
