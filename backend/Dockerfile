# Dockerfile for backend container
FROM python:3.10-slim
WORKDIR /app
RUN pip install gunicorn==20.1.0
COPY requirements.txt .
RUN mkdir nginx
#RUN cp ../infra/nginx.conf .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "foodgram.wsgi"]