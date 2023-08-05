FROM python:3.8-slim-buster
WORKDIR /srv
COPY . .
EXPOSE 5000
ENV HOST=0.0.0.0 PORT=5000 LOGGING_DISABLED=False
ENTRYPOINT ["python3", "src/server.py"]
