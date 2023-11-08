<h1 align="center"> Fast FastAPI boilerplate</h1>
<p align="center" markdown=1>
  <i>Yet another template to speed your FastAPI development up.</i>
</p>

<p align="center">
  <a href="https://github.com/igormagalhaesr/FastAPI-boilerplate">
    <img src="https://user-images.githubusercontent.com/43156212/277095260-ef5d4496-8290-4b18-99b2-0c0b5500504e.png" width="35%" height="auto">
  </a>
</p>

<p align="center">
  <a href="">
      <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://fastapi.tiangolo.com">
      <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  </a>
  <a href="https://docs.pydantic.dev/2.4/">
      <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=for-the-badge" alt="Pydantic">
  </a>
  <a href="https://www.postgresql.org">
      <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://redis.io">
      <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=fff&style=for-the-badge" alt="Redis">
  </a>
  <a href="https://docs.docker.com/compose/">
      <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge" alt="Docker">
  </a>
</p>

## 0. About
**FastAPI boilerplate** creates an extendable async API using FastAPI, Pydantic V2, SQLAlchemy 2.0 and PostgreSQL:
- [`FastAPI`](https://fastapi.tiangolo.com): modern Python web framework for building APIs
- [`Pydantic V2`](https://docs.pydantic.dev/2.4/): the most widely used data Python validation library, rewritten in Rust [`(5x-50x faster)`](https://docs.pydantic.dev/latest/blog/pydantic-v2-alpha/)
- [`SQLAlchemy 2.0`](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html): Python SQL toolkit and Object Relational Mapper
- [`PostgreSQL`](https://www.postgresql.org): The World's Most Advanced Open Source Relational Database
- [`Redis`](https://redis.io): Open source, in-memory data store used by millions as a cache, message broker and more.
- [`ARQ`](https://arq-docs.helpmanual.io) Job queues and RPC in python with asyncio and redis.
- [`Docker Compose`](https://docs.docker.com/compose/) With a single command, create and start all the services from your configuration.

## 1. Features
- ⚡️ Fully async
- 🚀 Pydantic V2 and SQLAlchemy 2.0
- 🔐 User authentication with JWT
- 🏬 Easy redis caching
- 👜 Easy client-side caching
- 🚦 ARQ integration for task queue
- ⚙️ Efficient querying (only queries what's needed)
- ⎘ Out of the box pagination support
- 👮 FastAPI docs behind authentication and hidden based on the environment
- 🦾 Easily extendable
- 🤸‍♂️ Flexible
- 🚚 Easy running with docker compose

### 1.1 To Do
#### API
- [ ] Add a photo upload endpoint for users
- [ ] Add possibility of comments in posts
- [ ] Add webhook to notify when a new comment is added in post

#### Docs
- [ ] Docs for other databases (MysQL, SQLite)

#### Features
- [ ] Add a Rate Limiter dependency
- [ ] Add mongoDB support

#### Tests
- [ ] Add Ruff linter

## 2. Contents
0. [About](#0-about)
1. [Features](#1-features)
    1. [To Do](#11-to-do)
3. [Contents](#2-contents)
4. [Prerequisites](#3-prerequisites)
    1. [Environment Variables (.env)](#31-environment-variables-env)
    2. [Docker Compose](#32-docker-compose-preferred)
    3. [From Scratch](#33-from-scratch)
5. [Usage](#4-usage)
    1. [Docker Compose](#41-docker-compose)
    2. [From Scratch](#42-from-scratch)
        1. [Packages](#421-packages)
        2. [Running PostgreSQL With Docker](#422-running-postgresql-with-docker)
        3. [Running Redis with Docker](#423-running-redis-with-docker)
        4. [Running the API](#424-running-the-api)
    3. [Creating the first superuser](#43-creating-the-first-superuser)
    4. [Database Migrations](#44-database-migrations)
6. [Extending](#5-extending)
    1. [Project Structure](#51-project-structure)
    2. [Database Model](#52-database-model)
    3. [SQLAlchemy Models](#53-sqlalchemy-models)
    4. [Pydantic Schemas](#54-pydantic-schemas)
    5. [Alembic Migrations](#55-alembic-migrations)
    6. [CRUD](#56-crud)
    7. [Routes](#57-routes)
        1. [Paginated Responses](#571-paginated-responses)
    8. [Caching](#58-caching)
    9. [More Advanced Caching](#59-more-advanced-caching)
    10. [ARQ Job Queues](#510-arq-job-queues)
    11. [Running](#511-running)
7. [Running in Production](#6-running-in-production)
8. [Testing](#7-testing)
9. [Contributing](#8-contributing)
10. [References](#9-references)
11. [License](#10-license)
12. [Contact](#11-contact)

___
## 3. Prerequisites
Start by using the template, and naming the repository to what you want.
<p align="left">
    <img src="https://user-images.githubusercontent.com/43156212/277866726-975d1c98-b1c9-4c8e-b4bd-001c8a5728cb.png" width="35%" height="auto">
</p>

Then clone your created repository (I'm using the base for the example)
```sh
git clone https://github.com/igormagalhaesr/FastAPI-boilerplate
```

### 3.1 Environment Variables (.env)
And create a ".env" file:

Then create a `.env` file:
```sh
touch .env
```

Inside of `.env`, create the following app settings variables:
```
# ------------- app settings ------------- 
APP_NAME="Your app name here"
APP_DESCRIPTION="Your app description here"
APP_VERSION="0.1"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
LICENSE_NAME="The license you picked"
```

For the database ([`if you don't have a database yet, click here`]()), create:
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

And then create in `.env`:
```
# ------------- crypt -------------
SECRET_KEY= # result of openssl rand -hex 32
ALGORITHM= # pick an algorithm, default HS256
ACCESS_TOKEN_EXPIRE_MINUTES= # minutes until token expires, default 30
```

Then for the first admin user:
```
# ------------- admin -------------
ADMIN_NAME="your_name"
ADMIN_EMAIL="your_email"
ADMIN_USERNAME="your_username"
ADMIN_PASSWORD="your_password"
```

For redis caching:
```
# ------------- redis -------------
REDIS_CACHE_HOST="your_host" # default "localhost", if using docker compose you should user "redis"
REDIS_CACHE_PORT=6379
```

And for client-side caching:
```
# ------------- redis cache -------------
REDIS_CACHE_HOST="your_host" # default "localhost", if using docker compose you should user "redis"
REDIS_CACHE_PORT=6379
```

For ARQ Job Queues:
```
# ------------- redis queue -------------
REDIS_CACHE_HOST="your_host" # default "localhost", if using docker compose you should use "db"
REDIS_CACHE_PORT=6379
```
> **Warning** 
> You may use the same redis for both caching and queue while developing, but the recommendation is using two separate containers for production.

For tests (optional to run):
```
# ------------- test -------------
TEST_NAME="Tester User"
TEST_EMAIL="test@tester.com"
TEST_USERNAME="testeruser"
TEST_PASSWORD="Str1ng$t"
```

And Finally the environment:
```
# ------------- environment -------------
ENVIRONMENT="local"
```
`ENVIRONMENT` can be one of `local`, `staging` and `production`, defaults to local, and changes the behavior of api `docs` endpoints:
- **local:** `/docs`, `/redoc` and `/openapi.json` available
- **staging:** `/docs`, `/redoc` and `/openapi.json` available for superusers
- **production:** `/docs`, `/redoc` and `/openapi.json` not available

### 3.2 Docker Compose (preferred)
To do it using docker compose, ensure you have docker and docker compose installed, then:
While in the base project directory (FastAPI-boilerplate here), run:

```sh
docker compose up
```

You should have a `web` container, `postgres` container, a `worker` container and a `redis` container running.  
Then head to `http://127.0.0.1:8000/docs`.

### 3.3 From Scratch
Install poetry:
```sh
pip install poetry
```

## 4. Usage

### 4.1 Docker Compose
If you used docker compose, your setup is done. You just need to ensure that when you run (while in the base folder):

```sh
docker compose up
```

You get the following outputs (in addition to many other outputs):
```sh
fastapi-boilerplate-worker-1  | ... redis_version=x.x.x mem_usage=999K clients_connected=1 db_keys=0
...
fastapi-boilerplate-db-1      | ... [1] LOG:  database system is ready to accept connections
...
fastapi-boilerplate-web-1     | INFO:     Application startup complete.
```

So you may skip to [5. Extending](#5-extending).

### 4.2 From Scratch

#### 4.2.1. Packages
In the `src` directory, run to install required packages:
```sh
poetry install
```
Ensuring it ran without any problem.

#### 4.2.2. Running PostgreSQL With Docker
> If you already have a PostgreSQL running, you may skip this step.

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

#### 4.2.3. Running redis With Docker
> If you already have a redis running, you may skip this step.

Install docker if you don't have it yet, then run:
```sh
docker pull redis:alpine
```

And pick the name and port, replacing the fields:
```sh
docker run -d \
  --name {NAME}  \
  -p {PORT}:{PORT} \
redis:alpine
```

Such as
```sh
docker run -d \
  --name redis  \
  -p 6379:6379 \
redis:alpine
```

#### 4.2.4. Running the API
While in the `src` folder, run to start the application with uvicorn server:
```sh
poetry run uvicorn app.main:app --reload
```
> The --reload flag enables auto-reload once you change (and save) something in the project

### 4.3 Creating the first superuser
#### 4.3.1 Docker Compose
If you are using docker compose, you should uncomment this part of the docker-compose.yml:
```
  # #-------- uncomment to create first superuser --------
  # create_superuser:
  #   build: 
  #     context: .
  #     dockerfile: Dockerfile
  #   env_file:
  #     - ./src/.env
  #   depends_on:
  #     - db
  #   command: python -m src.scripts.create_first_superuser
  #   volumes:
  #     - ./src:/code/src
```

Getting:
```
  #-------- uncomment to create first superuser --------
  create_superuser:
    build: 
      context: .
      dockerfile: Dockerfile
    env_file:
      - ./src/.env
    depends_on:
      - db
    command: python -m src.scripts.create_first_superuser
    volumes:
      - ./src:/code/src
```

While in the base project folder run to start the services:
```sh
docker-compose up -d
```

It will automatically run the create_superuser script as well, but if you want to rerun eventually:
```sh
docker-compose run --rm create_superuser
```

to stop the create_superuser service:
```sh
docker-compose stop create_superuser
```


#### 4.3.2 From Scratch
While in the `src` folder, run (after you started the application at least once to create the tables):
```sh
poetry run python -m scripts.create_first_superuser
```

### 4.4 Database Migrations
While in the `src` folder, run Alembic migrations:
```sh
poetry run alembic revision --autogenerate
```

And to apply the migration
```sh
poetry run alembic upgrade head
```

> If you do not have poetry, you may run it without poetry after running `pip install alembic`

## 5. Extending 
### 5.1 Project Structure
First, you may want to take a look at the project structure and understand what each file is doing.
```sh
.                                     # FastAPI-boilerplate folder. Rename it to suit your project name
├── Dockerfile                        # Dockerfile for building the application container.
├── LICENSE.md                        # License file for the project.
├── README.md                         # Project README providing information and instructions.
├── docker-compose.yml                # Docker Compose file for defining multi-container applications.
│
└── src                               # Source code directory.
    ├── __init__.py                   # Initialization file for the src package.
    ├── alembic.ini                   # Configuration file for Alembic (database migration tool).
    ├── poetry.lock
    ├── pyproject.toml                # Configuration file for Poetry, lists project dependencies.
    │
    ├── app                           # Main application directory.
    │   ├── __init__.py               # Initialization file for the app package.
    │   ├── main.py                   # Entry point that imports and creates the FastAPI application instance.
    │   ├── worker.py                 # Worker script for handling background tasks.
    │   │
    │   ├── api                       # Folder containing API-related logic.
    │   │   ├── __init__.py
    │   │   ├── dependencies.py       # Defines dependencies that can be reused across the API endpoints.
    │   │   ├── exceptions.py         # Contains custom exceptions for the API.
    │   │   ├── paginated.py          # Provides utilities for paginated responses in APIs
    │   │   │
    │   │   └── v1                    # Version 1 of the API.
    │   │       ├── __init__.py
    │   │       ├── login.py          # API routes related to user login.
    │   │       ├── posts.py          # API routes related to posts.
    │   │       ├── tasks.py          # API routes related to background tasks.
    │   │       └── users.py          # API routes related to user management.
    │   │
    │   ├── core                      # Core utilities and configurations for the application.
    │   │   ├── __init__.py
    │   │   ├── cache.py              # Utilities related to caching.
    │   │   ├── config.py             # Application configuration settings.
    │   │   ├── database.py           # Database connectivity and session management.
    │   │   ├── exceptions.py         # Contains core custom exceptions for the application.
    │   │   ├── models.py             # Base models for the application.
    │   │   ├── queue.py              # Utilities related to task queues.
    │   │   ├── security.py           # Security utilities like password hashing and token generation.
    │   │   └── setup.py              # File defining settings and FastAPI application instance definition.
    │   │
    │   ├── crud                      # CRUD operations for the application.
    │   │   ├── __init__.py
    │   │   ├── crud_base.py          # Base CRUD operations class that can be extended by other CRUD modules.
    │   │   ├── crud_posts.py         # CRUD operations for posts.
    │   │   ├── crud_users.py         # CRUD operations for users.
    │   │   └── helper.py             # Helper functions for CRUD operations.
    │   │
    │   ├── models                    # ORM models for the application.
    │   │   ├── __init__.py
    │   │   ├── post.py               # ORM model for posts.
    │   │   └── user.py               # ORM model for users.
    │   │
    │   └── schemas                   # Pydantic schemas for data validation.
    │       ├── __init__.py
    │       ├── job.py                # Schemas related to background jobs.
    │       ├── post.py               # Schemas related to posts.
    │       └── user.py               # Schemas related to users.
    │
    ├── migrations                    # Directory for Alembic migrations.
    │   ├── README                    # General info and guidelines for migrations.
    │   ├── env.py                    # Environment configurations for Alembic.
    │   ├── script.py.mako            # Template script for migration generation.
    │   │
    │   └── versions                  # Folder containing individual migration scripts.
    │       └── README.MD
    │
    ├── scripts                       # Utility scripts for the project.
    │   ├── __init__.py
    │   └── create_first_superuser.py # Script to create the first superuser in the application.
    │
    └── tests                         # Directory containing all the tests.
        ├── __init__.py               # Initialization file for the tests package.
        ├── conftest.py               # Configuration and fixtures for pytest.
        ├── helper.py                 # Helper functions for writing tests.
        └── test_user.py              # Tests related to the user model and endpoints.

```

### 5.2 Database Model
Create the new entities and relationships and add them to the model
![diagram](https://user-images.githubusercontent.com/43156212/274053323-31bbdb41-15bf-45f2-8c8e-0b04b71c5b0b.png)

### 5.3 SQLAlchemy Models
Inside `app/models`, create a new `entity.py` for each new entity (replacing entity with the name) and define the attributes according to [SQLAlchemy 2.0 standards](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapping-styles):

> **Warning**
> Note that since it inherits from `Base`, the new model is mapped as a python `dataclass`, so optional attributes (arguments with a default value) should be defined after required  attributes.

```python
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Entity(Base):
  __tablename__ = "entity"

  id: Mapped[int] = mapped_column(
    "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
  )
  name: Mapped[str] = mapped_column(String(30))
  ...
```

### 5.4 Pydantic Schemas
Inside `app/schemas`, create a new `entity.py` for for each new entity (replacing entity with the name) and create the schemas according to [Pydantic V2](https://docs.pydantic.dev/latest/#pydantic-examples) standards:
```python
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, HttpUrl, ConfigDict

class EntityBase(BaseModel):
  name: Annotated[
    str, 
    Field(min_length=2, max_length=30, examples=["Entity Name"])
    ...
  ]

class Entity(EntityBase):
  ...

class EntityRead(EntityBase):
  ...

class EntityCreate(EntityBase):
  ...

class EntityCreateInternal(EntityCreate):
  ...

class EntityUpdate(BaseModel):
  ...

class EntityUpdateInternal(BaseModel):
  ...

class EntityDelete(BaseModel):
    model_config = ConfigDict(extra='forbid')

    is_deleted: bool
    deleted_at: datetime

```

### 5.5 Alembic Migrations
Then, while in the `src` folder, run Alembic migrations:
```sh
poetry run alembic revision --autogenerate
```

And to apply the migration
```sh
poetry run alembic upgrade head
```

### 5.6 CRUD
Inside `app/crud`, create a new `crud_entities.py` inheriting from `CRUDBase` for each new entity:
```python
from app.crud.crud_base import CRUDBase
from app.models.entity import Entity
from app.schemas.entity import EntityCreateInternal, EntityUpdate, EntityUpdateInternal, EntityDelete

CRUDEntity = CRUDBase[Entity, EntityCreateInternal, EntityUpdate, EntityUpdateInternal, EntityDelete]
crud_entity = CRUDEntity(Entity)
```

So, for users:
```python
# crud_users.py
from app.model.user import User
from app.schemas.user import UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete

CRUDUser = CRUDBase[User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete]
crud_users = CRUDUser(User)
```

When actually using the crud in an endpoint, to get data you just pass the database connection and the attributes as kwargs:
```python
# Here I'm getting the first user with email == user.email (email is unique in this case)
user = await crud_users.get(db=db, email=user.email)
```

To get a list of objects with the attributes, you should use the get_multi:
```python
# Here I'm getting at most 10 users with the name 'User Userson' except for the first 3
user = await crud_users.get_multi(
  db=db,
  offset=3,
  limit=100,
  name="User Userson"
)
```
> **Warning**
> Note that get_multi returns a python `dict`.

Which will return a python dict with the following structure:
```javascript
{
  "data": [
    {
      "id": 4,
      "name": "User Userson",
      "username": "userson4",
      "email": "user.userson4@example.com",
      "profile_image_url": "https://profileimageurl.com"
    },
    {
      "id": 5,
      "name": "User Userson",
      "username": "userson5",
      "email": "user.userson5@example.com",
      "profile_image_url": "https://profileimageurl.com"
    }
  ],
  "total_count": 2,
  "has_more": false,
  "page": 1,
  "items_per_page": 10
}
```

To create, you pass a `CreateSchemaType` object with the attributes, such as a `UserCreate` pydantic schema:
```python
from app.core.schemas.user import UserCreate

# Creating the object
user_internal = UserCreate(
  name="user",
  username="myusername",
  email="user@example.com"
)

# Passing the object to be created
crud_users.create(db=db, object=user_internal)
```

To just check if there is at least one row that matches a certain set of attributes, you should use `exists`
```python
# This queries only the email variable
# It returns True if there's at least one or False if there is none
crud_users.exists(db=db, email=user@example.com)
```

You can also get the count of a certain object with the specified filter:
```python
# Here I'm getting the count of users with the name 'User Userson'
user = await crud_users.count(
  db=db,
  name="User Userson"
)
```

To update you pass an `object` which may be a `pydantic schema` or just a regular `dict`, and the kwargs.
You will update with `objects` the rows that match your `kwargs`.
```python
# Here I'm updating the user with username == "myusername". 
# #I'll change his name to "Updated Name"
crud_users.update(db=db, object={name="Updated Name"}, username="myusername")
```

To delete we have two options:
- db_delete: actually deletes the row from the database
- delete: 
    - adds `"is_deleted": True` and `deleted_at: datetime.utcnow()` if the model inherits from `PersistentDeletion` (performs a soft delete), but keeps the object in the database.
    - actually deletes the row from the database if the model does not inherit from `PersistentDeletion`

```python
# Here I'll just change is_deleted to True
crud_users.delete(db=db, username="myusername")

# Here I actually delete it from the database
crud_users.db_delete(db=db, username="myusername")
```

#### More Efficient Selecting
For the `get` and `get_multi` methods we have the option to define a `schema_to_select` attribute, which is what actually makes the queries more efficient. When you pass a `pydantic schema` (preferred) or a list of the names of the attributes in `schema_to_select` to the `get` or `get_multi` methods, only the attributes in the schema will be selected.
```python
from app.schemas.user import UserRead
# Here it's selecting all of the user's data
crud_user.get(db=db, username="myusername")

# Now it's only selecting the data that is in UserRead. 
# Since that's my response_model, it's all I need
crud_user.get(db=db, username="myusername", schema_to_select=UserRead)
```

### 5.7 Routes
Inside `app/api/v1`, create a new `entities.py` file and create the desired routes
```python
from typing import Annotated

from fastapi import Depends

from app.schemas.entity import EntityRead
from app.core.database import async_get_db
...

router = fastapi.APIRouter(tags=["entities"])

@router.get("/entities/{id}", response_model=List[EntityRead])
async def read_entities(
  request: Request,
  id: int,
  db: Annotated[AsyncSession, Depends(async_get_db)]
):
  entity = await crud_entities.get(db=db, id=id)  
  
  return entity

...
```
Then in `app/api/v1/__init__.py` add the router such as:
```python
from fastapi import APIRouter
from app.api.v1.entity import router as entity_router
...

router = APIRouter(prefix="/v1") # this should be there already
...
router.include_router(entity_router)
```

#### 5.7.1 Paginated Responses
With the `get_multi` method we get a python `dict` with full suport for pagination:
```javascript
{
  "data": [
    {
      "id": 4,
      "name": "User Userson",
      "username": "userson4",
      "email": "user.userson4@example.com",
      "profile_image_url": "https://profileimageurl.com"
    },
    {
      "id": 5,
      "name": "User Userson",
      "username": "userson5",
      "email": "user.userson5@example.com",
      "profile_image_url": "https://profileimageurl.com"
    }
  ],
  "total_count": 2,
  "has_more": false,
  "page": 1,
  "items_per_page": 10
} 
```

And in the endpoint, we can import from `app/api/paginated` the following functions and Pydantic Schema:
```python
from app.api.paginated import (
  PaginatedListResponse, # What you'll use as a response_model to validate
  paginated_response,    # Creates a paginated response based on the parameters
  compute_offset         # Calculate the offset for pagination ((page - 1) * items_per_page)
)
```

Then let's create the endpoint:
```python
import fastapi

from app.schemas.entity imoport EntityRead
...

@router.get("/entities", response_model=PaginatedListResponse[EntityRead])
async def read_entities(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10
):
    entities_data = await crud_entity.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=UserRead, 
        is_deleted=False
    )
    
    return paginated_response(
        crud_data=entities_data, 
        page=page,
        items_per_page=items_per_page
    )
```

### 5.8 Caching
The `cache` decorator allows you to cache the results of FastAPI endpoint functions, enhancing response times and reducing the load on your application by storing and retrieving data in a cache.

Caching the response of an endpoint is really simple, just apply the `cache` decorator to the endpoint function. 

> **Warning**
> Note that you should always pass request as a variable to your endpoint function if you plan to use the cache decorator.

```python
...
from app.core.cache import cache

@app.get("/sample/{my_id}")
@cache(
    key_prefix="sample_data",
    expiration=3600,
    resource_id_name="my_id"
)
async def sample_endpoint(request: Request, my_id: int):
    # Endpoint logic here
    return {"data": "my_data"}
```

The way it works is:
- the data is saved in redis with the following cache key: `sample_data:{my_id}`
- then the time to expire is set as 3600 seconds (that's the default)

Another option is not passing the `resource_id_name`, but passing the `resource_id_type` (default int):
```python
...
from app.core.cache import cache

@app.get("/sample/{my_id}")
@cache(
    key_prefix="sample_data",
    resource_id_type=int
)
async def sample_endpoint(request: Request, my_id: int):
    # Endpoint logic here
    return {"data": "my_data"}
```
In this case, what will happen is:
- the `resource_id` will be inferred from the keyword arguments (`my_id` in this case)
- the data is saved in redis with the following cache key: `sample_data:{my_id}`
- then the the time to expire is set as 3600 seconds (that's the default)

Passing resource_id_name is usually preferred.

### 5.9 More Advanced Caching
The behaviour of the `cache` decorator changes based on the request method of your endpoint. 
It caches the result if you are passing it to a **GET** endpoint, and it invalidates the cache with this key_prefix and id if passed to other endpoints (**PATCH**, **DELETE**).

If you also want to invalidate cache with a different key, you can use the decorator with the `to_invalidate_extra` variable.

In the following example, I want to invalidate the cache for a certain `user_id`, since I'm deleting it, but I also want to invalidate the cache for the list of users, so it will not be out of sync.

```python
# The cache here will be saved as "{username}_posts:{username}":
@router.get("/{username}/posts", response_model=List[PostRead])
@cache(key_prefix="{username}_posts", resource_id_name="username")
async def read_posts(
    request: Request,
    username: str, 
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    ...

...

# Invalidating cache for the former endpoint by just passing the key_prefix and id as a dictionary:
@router.delete("/{username}/post/{id}")
@cache(
    "{username}_post_cache", 
    resource_id_name="id", 
    to_invalidate_extra={"{username}_posts": "{username}"} # also invalidate "{username}_posts:{username}" cache
)
async def erase_post(
    request: Request, 
    username: str,
    id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    ...

# And now I'll also invalidate when I update the user:
@router.patch("/{username}/post/{id}", response_model=PostRead)
@cache(
    "{username}_post_cache", 
    resource_id_name="id", 
    to_invalidate_extra={"{username}_posts": "{username}"} 
)
async def patch_post(
    request: Request,
    username: str,
    id: int,
    values: PostUpdate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    ...
```

> **Warning**
> Note that adding `to_invalidate_extra` will not work for **GET** requests.

#### Client-side Caching
For `client-side caching`, all you have to do is let the `Settings` class defined in `app/core/config.py` inherit from the `ClientSideCacheSettings` class. You can set the `CLIENT_CACHE_MAX_AGE` value in `.env,` it defaults to 60 (seconds).

### 5.10 ARQ Job Queues
Create the background task in `app/worker.py`:
```python
...
# -------- background tasks --------
async def sample_background_task(ctx, name: str) -> str:
    await asyncio.sleep(5)
    return f"Task {name} is complete!"
```

Then add the function to the `WorkerSettings` class `functions` variable:
```python
# -------- class --------
...
class WorkerSettings:
    functions = [sample_background_task]
    ...
```

Add the task to be enqueued in a **POST** endpoint and get the info in a **GET**:
```python
...
@router.post("/task", response_model=Job, status_code=201)
async def create_task(message: str):
    job = await queue.pool.enqueue_job("sample_background_task", message)
    return {"id": job.job_id}


@router.get("/task/{task_id}")
async def get_task(task_id: str):
    job = ArqJob(task_id, queue.pool)
    return await job.info()

```

And finally run the worker in parallel to your fastapi application.

If you are using `docker compose`, the worker is already running.
If you are doing it from scratch, run while in the `src` folder:
```sh
poetry run arq app.worker.WorkerSettings
```

### 5.11 Running
If you are using docker compose, just running the following command should ensure everything is working:
```sh
docker compose up
```

If you are doing it from scratch, ensure your postgres and your redis are running, then
while in the `src` folder, run to start the application with uvicorn server:
```sh
poetry run uvicorn app.main:app --reload
```

And for the worker:
```sh
poetry run arq app.worker.WorkerSettings
```

## 6. Running in Production
In production you probably should run using gunicorn workers:
```sh
command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
``` 
Here it's running with 4 workers, but you should test it depending on how many cores your machine has.

To do this if you are using docker compose, just replace the comment:
This part in docker-compose.yml:
```python
# -------- replace with comment to run with gunicorn --------
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Should be changed to:
```python
# -------- replace with comment to run with uvicorn --------
# command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

> **Warning**
> Do not forget to set the `ENVIRONMENT` in `.env` to `production` unless you want the API docs to be public.

More on running it in production later.

## 7. Testing
For tests, ensure you have in `.env`:
```
# ------------- test -------------
TEST_NAME="Tester User"
TEST_EMAIL="test@tester.com"
TEST_USERNAME="testeruser"
TEST_PASSWORD="Str1ng$t"
```

While in the tests folder, create your test file with the name "test_{entity}.py", replacing entity with what you're testing
```sh
touch test_items.py
```

Finally create your tests (you may want to copy the structure in test_user.py)

Now, to run:

### 7.1  Docker Compose
First you need to uncomment the following part in the `docker-compose.yml` file:
```
  # #-------- uncomment to run tests --------
  # pytest:
  #   build: 
  #     context: .
  #     dockerfile: Dockerfile 
  #   env_file:
  #     - ./src/.env 
  #   depends_on:
  #     - db
  #     - create_superuser
  #     - redis
  #   command: python -m pytest
  #   volumes:
  #     - ./src:/code/src
```

You'll get:
```
  #-------- uncomment to run tests --------
  pytest:
    build: 
      context: .
      dockerfile: Dockerfile 
    env_file:
      - ./src/.env 
    depends_on:
      - db
      - create_superuser
      - redis
    command: python -m pytest
    volumes:
      - ./src:/code/src
```

Start the Docker Compose services:

```sh
docker-compose up -d
```

It will automatically run the tests, but if you want to run again later:
```sh
docker-compose run --rm pytest
```

### 7.2  From Scratch

While in the `src` folder, run:
```sh
poetry run python -m pytest
```

## 8. Contributing
Contributions are appreciated, even if just reporting bugs, documenting stuff or answering questions. To contribute with a feature:
1. Fork it (https://github.com/igormagalhaesr/FastAPI-boilerplate)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Test your changes while in the src folder `poetry run python -m pytest`
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

## 9. References
This project was inspired by a few projects, it's based on them with things changed to the way I like (and pydantic, sqlalchemy updated)
* [`Full Stack FastAPI and PostgreSQL`](https://github.com/tiangolo/full-stack-fastapi-postgresql) by @tiangolo himself
* [`FastAPI Microservices`](https://github.com/Kludex/fastapi-microservices) by @kludex which heavily inspired this boilerplate
* [`Async Web API with FastAPI + SQLAlchemy 2.0`](https://github.com/rhoboro/async-fastapi-sqlalchemy) for sqlalchemy 2.0 ORM examples
* [`FastaAPI Rocket Boilerplate`](https://github.com/asacristani/fastapi-rocket-boilerplate/tree/main) for docker compose

## 10. License
[`MIT`](LICENSE.md)

## 11. Contact
Igor Magalhaes – [@igormagalhaesr](https://twitter.com/igormagalhaesr) – igormagalhaesr@gmail.com
[github.com/igormagalhaesr](https://github.com/igormagalhaesr/)
