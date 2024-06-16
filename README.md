# silent-service

# Installation
## Local
```bash
cp .env.example .env

docker-compose -f docker-compose.dev.yml up -d --build
```

## Production
```bash
cp .env.example .env

docker-compose -f docker-compose.prod.yml up -d --build
```
