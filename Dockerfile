FROM ubuntu:latest
WORKDIR /srv
COPY . .
RUN apt-get update
RUN apt-get install -y python3
EXPOSE 5000
CMD ["python3", "server.py"]

