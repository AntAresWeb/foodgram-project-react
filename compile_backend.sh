docker login -u antaresweb
docker build -t antaresweb/foodgram_backend:latest ./backend -f ./backend/Dockerfile.prod
docker push antaresweb/foodgram_backend:latest
