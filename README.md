# OpenGram

**OpenGram** _is an open source web-based photo sharing platform that allows users to share them with friends._

## Technologies
- Python3.11
- PostgreSQL
- Nginx
- Minio

## Deployment

### Dependencies

- Docker

### **Stages**
- Rename or copy `.env.example` in `.env`
```shell
cp ./.env.example .env
```
- Fill in the missing fields in .env
- After filling in the missing fields in .env, we start building the project
```shell
docker-compose up --build -d
```
- After the assembly it is necessary to execute the commands
```shell
docker-compose exec web python manage.py migrate 
docker-compose exec web python manage.py collectstatic
```

## Licence
MIT