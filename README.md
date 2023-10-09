# FastAPI-boilerplate
>A template to speed your FastAPI development up.

## About
**FastAPI boilerplate** creates an extendable async API using FastAPI, Pydantic V2, SQLAlchemy 2.0 and PostgreSQL:
- [`FastAPI`](https://fastapi.tiangolo.com): modern Python web framework for building APIs
- [`Pydantic V2`](https://docs.pydantic.dev/2.4/): the most widely used data validation library for Python now rewritten in Rust [`(5x to 50x speed improvement)`](https://docs.pydantic.dev/latest/blog/pydantic-v2-alpha/)
- [`SQLAlchemy 2.0`](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html): Python SQL toolkit and Object Relational Mapper
- [`PostgreSQL`](https://www.postgresql.org): The World's Most Advanced Open Source Relational Database

## Features
  - Fully async
  - Pydantic V2 and SQLAlchemy 2.0
  - User authentication with JWT
  - Easily extendable
  - Flexible

___
# Usage
## Start by cloning the repository
```sh
git clone https://github.com/igormagalhaesr/FastAPI-boilerplate
```
___
## Requirements
### Packages
Then install poetry:
```sh
pip install poetry
```

In the **src** directory, run to install required packages:
```sh
poetry install
```

### Environment Variables
Then create a .env file:
```sh
touch .env
```

Inside of .env, create the following app settings variables:
```
# ------------- app settings ------------- 
APP_NAME="Your app name here"
APP_DESCRIPTION="Your app description here"
APP_VERSION="0.1"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
LICENSE_NAME="The license you picked"
```

For the database ([`if you don't have a database yet, click here`](#running-postgresql-with-docker)), create: 
```
# ------------- database ------------- 
POSTGRES_USER="your_postgres_user"
POSTGRES_PASSWORD="your_password"
POSTGRES_SERVER="your_server" # default localhost
POSTGRES_PORT=5432 
POSTGRES_DB="your_db"
```

For crypt:
Start by running
```sh
openssl rand -hex 32
```

And then create in .env:
```
# ------------- crypt -------------
SECRET_KEY= # result of openssl rand -hex 32
ALGORITHM= # pick an algorithm, default HS256
ACCESS_TOKEN_EXPIRE_MINUTES= # minutes until token expires, default 30
```

And finally for the first admin user:
```
# ------------- admin -------------
ADMIN_NAME="your_name"
ADMIN_EMAIL="your_email"
ADMIN_USERNAME="your_username"
ADMIN_PASSWORD="your_password"
```

___
## Running PostgreSQL with docker:
Install docker if you don't have it yet, then run:
```sh
docker pull postgres
```

And pick the port, name, user and password, replacing the fields:
```sh
docker run -d \
    -p {PORT}:{PORT} \
    --name {NAME} \
    -e POSTGRES_PASSWORD={PASSWORD} \
    -e POSTGRES_USER={USER} \
    postgres
```

Such as:
```sh
docker run -d \
    -p 5432:5432 \
    --name postgres \
    -e POSTGRES_PASSWORD=1234 \
    -e POSTGRES_USER=postgres \
    postgres
```

[`If you didn't create the .env variables yet, click here.`](#environment-variables)

___
## Running the api
While in the **src** folder, run to start the application with uvicorn server:
```sh
poetry run uvicorn app.main:app --reload
```

___
## Creating the first superuser:
While in the **src** folder, run (after you started the application at least once to create the tables):
```sh
poetry run python -m scripts.create_first_superuser
```

___
## Database Migrations
Migrations done via [Alembic](https://alembic.sqlalchemy.org/en/latest/):

Whenever you change somethin in the database, in the **src** directory, run to create the script:
```sh
poetry run alembic revision --autogenerate
```

And to actually migrate:
```sh
poetry run alembic upgrade head
```

___
## Testing
For tests, create in .env:
```
# ------------- test -------------
TEST_NAME="Tester User"
TEST_EMAIL="test@tester.com"
TEST_USERNAME="testeruser"
TEST_PASSWORD="Str1ng$t"
```

While in the tests folder, create your test file with the name "test_{object}.py", replacing object with what you're testing
```sh
touch test_items.py
```

Finally create your tests (you may want to copy the structure in test_user.py), then run:
```sh
poetry run python -m pytest
```
___
# Other stuff
## Contributing
1. Fork it (https://github.com/igormagalhaesr/FastAPI-boilerplate)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Test your changes while in the src folder `poetry run python -m pytest`
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

## References
This project was inspired by a few projects, it's based on them with things changed to the way I like (and pydantic, sqlalchemy updated)
* [`Full Stack FastAPI and PostgreSQL`](https://github.com/tiangolo/full-stack-fastapi-postgresql) by @tiangolo himself
* [`FastAPI Microservices`](https://github.com/Kludex/fastapi-microservices) by @kludex which heavily inspired this boilerplate
* [Async Web API with FastAPI + SQLAlchemy 2.0](https://github.com/rhoboro/async-fastapi-sqlalchemy)

## License
[`MIT`](LICENSE.md)

## Contact
Igor Magalhaes – [@igormagalhaesr](https://twitter.com/igormagalhaesr) – igormagalhaesr@gmail.com
[github.com/igormagalhaesr](https://github.com/igormagalhaesr/)