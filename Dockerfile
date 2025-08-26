FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update && apt-get install -y openssh-client tmate
COPY . /app
CMD ["python3", "main.py"]
