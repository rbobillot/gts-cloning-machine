# WebApp
---

# How to run the services

In a first Terminal (window, tab, split...)
```
# pwd: /path/to/gts-cloning-machine/app

./run

# or
# docker-compose up --build
```
In a second Terminal
```
# pwd: /path/to/gts-cloning-machine/app/gts-nds-flat-pass

./flat-pass
```
---

For now only 3 services must be Dockerized:
 - gts-front (localhost:8080)
 - gts-service (localhost:8081) + gts-db
 - gts-event-manager

gts-nds-flat-pass (localhost:8082) should run locally,
because the communication between NDS and a Dockerized app, seems to be buggy
