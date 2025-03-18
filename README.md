## Blog api

### Technologies Used
- Python
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

### .env file example
```dosini
DJANGO_SECRET_KEY=your-key...
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_HOST=postgres-db
POSTGRES_PORT=5432
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
```

### docker-compose.override.yml
For debugging. VS Code laucnch config example:
```json
{
    "name": "Docker: Debug DRF",
    "type": "debugpy",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678,
    },
    "pathMappings": [
        {
        "localRoot": "${workspaceFolder}/blog",
        "remoteRoot": "/app/blog",
        }
    ]
}
```