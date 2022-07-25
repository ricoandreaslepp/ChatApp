#!/bin/bash
docker build --no-cache -t chat_app .
docker run -p 8080:5000 --name chat_app_container chat_app

