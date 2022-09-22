# WebApp
---

# How to run the services

```
./run
# or
# docker-compose up --build
```
---

For now only 2 services must be Dockerized:
 - gts-front (localhost:8080)
 - gts-service (localhost:8081) + gts-db

gts-nds-flat-pass (localhost:8082) should run locally,
because the communication between NDS and a Dockerized app, seems to be buggy
