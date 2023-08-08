# Messaging application

A multithreaded dockerized Python messaging application without any security whatsoever.

![Example](images/server_running.png)

# Usage

For an interactive server logging session run:
```bash
docker-compose up --build
```
Then client to connect with:
```bash
nc localhost 8080
```
CTRl-C to kill the server

# To-Do
    1) Login system (username, password hash, better ID method)
    2) Make a database with sqlite3
    3) Encrypt traffic
    4) Improve chat printing (functionality, colors, saved messages)
    5) Make chatrooms
