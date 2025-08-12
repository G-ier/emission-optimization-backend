# Running the app

## Prerequisites

To run the app you need to have the following programs installed:
- Docker - [Installation guide](https://docs.docker.com/get-started/get-docker/)

Additionally, it is required to create a `.env` file in the project root with 
the following content:

```dotenv
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=postgres
```

## Run backend app

Running the following command will start the backend application together with
the database service:

```bash
docker compose up backend
```

The database should be initialized with all the necessary tables and data.
If for some reason the data is not there, you can run the initialize script
(`database_init/database_dump.sql`) directly in the database.

## Swagger API documentation

After starting the app you should be able to reach the following website with
the API documentation: http://localhost:8000/api/docs


# Development

## Prerequisites

To develop the app you need to have the following programs installed:
- Python 3.13 - [Python official website](https://www.python.org/)
- UV - [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

## Dependency installation

This command will create the virtual environment and install all the required
dependencies inside:

```bash
uv sync
```

The virtual environment should be created inside the project in the `.venv` directory.

# Testing 

## Simple local testing mechanism

Run all test using:

```bash
uv run pytest -q
```

Run single tests, for example:
```bash
uv run pytest app/tests/test_products_routes.py::test_get_product_details_no_contributors
```

## One-off test container

After building run only the database. Then run the tests.
```bash
docker compose build

```
```bash
docker compose up -d database
```
```bash
docker compose run --rm --entrypoint "" backend uv run pytest -q
```
```bash
docker compose down -v
```