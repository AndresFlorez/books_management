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

4. Run Django migrations.

```bash
docker exec production-line-microservice python manage.py migrate
```

5. Create superuser

```bash
docker exec -it django_service python manage.py createsuperuser
```



## Execution

To run the project, execute the following commands in the root directory of the project:

```bash
docker-compose build
```

```bash
docker-compose up -d
```


## Running Tests

Run unit tests with the following command

```bash
docker exec -it django_service python manage.py test
```

## Test structure
The tests in this project are located in the `books_management.tests` directory.

