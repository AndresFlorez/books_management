# django_template_microservice

## Description

Project for managing books

## Prerequisites

- Docker
- Docker Compose

## Configuration

1. Clone this repository to your local machine.

```sh
git clone https://github.com/AndresFlorez/books_management.git
```

2. Navigate to the project directory.

```sh
cd books_management
```

3. Create a .env file in the root directory of the project. This file should contain the following environment variables:

```sh
DB_NAME="books_management"
DB_HOST="mongodb"
DB_PORT=27017
DB_USER="root"
DB_PASSWORD="root"
```

```sh
cp .env.example .env
```
4. To run the project, execute the following commands in the root directory of the project:

```bash
docker-compose build
```

```bash
docker-compose up -d
```

4. Run Django migrations.

```bash
docker exec django_service python manage.py migrate
```

5. Create superuser

```bash
docker exec -it django_service python manage.py createsuperuser
```


## Running Tests

Run unit tests with the following command

```bash
docker exec -it django_service python manage.py test
```

## Test structure
The tests in this project are located in the `books_management.tests` directory.


## Swagger documentation

To access the swagger documentation, go to the following URL:

[http://localhost:8000/books-management/docs/](http://localhost:8000/books-management/docs/)

## JWT Authentication

To obtain a token, you must make a POST request to the following URL:

[http://localhost:8000/books-management/token/](http://localhost:8000/books-management/token/)

Send the following JSON in the request body:

```json
{
    "username": "admin",
    "password": "password"
}
```

The user must be created previously.

## Authentication

The project uses JWT authentication. To access the book API, you must include the token in the request headers.

```bash
Bearer <token>
```
