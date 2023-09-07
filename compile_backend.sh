docker login -u antaresweb
docker build -t antaresweb/foodgram-backend:latest ./backend -f ./backend/Dockerfile.prod
docker push antaresweb/foodgram-backend:latest
