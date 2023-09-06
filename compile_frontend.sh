docker login -u antaresweb
docker build -t antaresweb/foodgram-frontend:latest ./frontend -f ./frontend/Dockerfile
docker push antaresweb/foodgram-frontend:latest
