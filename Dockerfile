FROM python:3.8-slim-buster
WORKDIR /srv
COPY . .
EXPOSE 5000
CMD ["python3", "src/server.py"]
