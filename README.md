# Auction Backend

We are using FastAPI for backend and sqlalchemy for database operations. 

We are also using celery + rabbitmq for background tasks.

Its assumed that this backend will be behind a load balancer or something similar

# API documentation
API documentation can be read at localhost:8000/docs after running the server.

Swagger JSON file could be found @ openapi.json

# Tests
Tests can be run using
pytest

# Run
This can be run using:

docker-compose build
docker-compose up

# Future Improvements
1. Currently we are not using cache as I believe db read replica should be enough to handle traffic for this application.
2. 
