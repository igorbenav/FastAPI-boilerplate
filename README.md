# FastAPI-boilerplate
>A template to speed your FastAPI development up.

## 0. About
**FastAPI boilerplate** creates an extendable async API using FastAPI, Pydantic V2, SQLAlchemy 2.0 and PostgreSQL:
- [`FastAPI`](https://fastapi.tiangolo.com): modern Python web framework for building APIs
- [`Pydantic V2`](https://docs.pydantic.dev/2.4/): the most widely used data validation library for Python, now rewritten in Rust [`(5x to 50x speed improvement)`](https://docs.pydantic.dev/latest/blog/pydantic-v2-alpha/)
- [`SQLAlchemy 2.0`](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html): Python SQL toolkit and Object Relational Mapper
- [`PostgreSQL`](https://www.postgresql.org): The World's Most Advanced Open Source Relational Database

## 1. Features
  - Fully async
  - Pydantic V2 and SQLAlchemy 2.0
  - User authentication with JWT
  - Easily extendable
  - Flexible

### 1.1 To do
- [ ] Redis cache
- [ ] Google SSO
- [ ] Arq job queues

## 2. Contents
0. [About](#0-about)
1. [Features](#1-features)
    1. [To do](#11-to-do)
2. [Contents](#2-contents)
3. [Usage](#3-usage)
4. [Requirements](#4-requirements)
    1. [Packages](#41-packages)
    2. [Environment Variables](#42-environment-variables)
5. [Running PostgreSQL with docker](#5-running-postgresql-with-docker)
6. [Running the api](#6-running-the-api)
7. [Creating the first superuser](#7-creating-the-first-superuser)
8. [Database Migrations](#8-database-migrations)
9. [Extending](#9-extending)
    1. [Database Model](#91-database-model)
    2. [SQLAlchemy Models](#92-sqlalchemy-model)
    3. [Pydantic Schemas](#93-pydantic-schemas)
    4. [Alembic Migrations](#94-alembic-migration)
    5. [CRUD](#95-crud)
    6. [Routes](#96-routes)
    7. [Running](#97-running)
10. [Testing](#10-testing)
11. [Contributing](#11-contributing)
12. [References](#12-references)
13. [License](#13-license)
14. [Contact](#14-contact)

___
## 3. Usage
Start by cloning the repository
```sh
git clone https://github.com/igormagalhaesr/FastAPI-boilerplate
```
___
## 4. Requirements
### 4.1 Packages
Then install poetry:
```sh
pip install poetry
```

In the **src** directory, run to install required packages:
```sh
poetry install
```

### 4.2 Environment Variables
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
## 5. Running PostgreSQL with docker:
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
## 6. Running the api
While in the **src** folder, run to start the application with uvicorn server:
```sh
poetry run uvicorn app.main:app --reload
```

___
## 7. Creating the first superuser:
While in the **src** folder, run (after you started the application at least once to create the tables):
```sh
poetry run python -m scripts.create_first_superuser
```

___
## 8. Database Migrations
Migrations done via [Alembic](https://alembic.sqlalchemy.org/en/latest/):

Whenever you change something in the database, in the **src** directory, run to create the script:
```sh
poetry run alembic revision --autogenerate
```

And to actually migrate:
```sh
poetry run alembic upgrade head
```

___
## 9. Extending
### 9.1 Database Model
Create the new entities and relationships and add them to the model
![diagram](https://user-images.githubusercontent.com/43156212/274053323-31bbdb41-15bf-45f2-8c8e-0b04b71c5b0b.png)

### 9.2 SQLAlchemy Model
Inside **app/models**, create a new **entity.py** for each new entity (replacing entity with the name) and define the attributes according to [SQLAlchemy 2.0 standards](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapping-styles):
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

### 9.3 Pydantic Schemas
Inside app/schemas, create a new entity.py for for each new entity (replacing entity with the name) and create the schemas according to [Pydantic V2](https://docs.pydantic.dev/latest/#pydantic-examples) standards:
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

### 9.4 Alembic Migration
Then, while in the **src** folder, run Alembic migrations:
```sh
poetry run alembic revision --autogenerate
```

And to apply the migration
```sh
poetry run alembic upgrade head
```

### 9.5 CRUD
Inside **app/crud**, create a new crud_entities.py inheriting from CRUDBase for each new entity:
```python
from app.crud.crud_base import CRUDBase
from app.models.entity import Entity
from app.schemas.entity import EntityCreateInternal, EntityUpdate, EntityUpdateInternal, EntityDelete

CRUDEntity = CRUDBase[Entity, EntityCreateInternal, EntityUpdate, EntityUpdateInternal, EntityDelete]
crud_entity = CRUDEntity(Entity)
```

### 9.6 Routes
Inside **app/api/v1**, create a new entities.py file and create the desired routes
```python
from typing import Annotated

from fastapi import Depends

from app.schemas.entity import EntityRead
from app.core.database import async_get_db
...

router = fastapi.APIRouter(tags=["entities"])

@router.get("/entities", response_model=List[EntityRead])
async def read_entities(db: Annotated[AsyncSession, Depends(async_get_db)]):
  entities = await crud_entities.get_multi(db=db)
    return entities

...
```
Then in **app/api/v1/__init__.py** add the router such as:
```python
from fastapi import APIRouter
from app.api.v1.entity import router as entity_router
...

router = APIRouter(prefix="/v1") # this should be there already
...
router.include_router(entity_router)
```

### 9.7 Running
While in the **src** folder, run to start the application with uvicorn server:
```sh
poetry run uvicorn app.main:app --reload
```

___
## 10. Testing
For tests, create in .env:
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

Finally create your tests (you may want to copy the structure in test_user.py), then run:
```sh
poetry run python -m pytest
```
___
## 11. Contributing
Contributions are appreciated, even if just reporting bugs, documenting stuff or answering questions. To contribute with a feature:
1. Fork it (https://github.com/igormagalhaesr/FastAPI-boilerplate)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Test your changes while in the src folder `poetry run python -m pytest`
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

## 12. References
This project was inspired by a few projects, it's based on them with things changed to the way I like (and pydantic, sqlalchemy updated)
* [`Full Stack FastAPI and PostgreSQL`](https://github.com/tiangolo/full-stack-fastapi-postgresql) by @tiangolo himself
* [`FastAPI Microservices`](https://github.com/Kludex/fastapi-microservices) by @kludex which heavily inspired this boilerplate
* [`Async Web API with FastAPI + SQLAlchemy 2.0`](https://github.com/rhoboro/async-fastapi-sqlalchemy)

## 13. License
[`MIT`](LICENSE.md)

## 14. Contact
Igor Magalhaes – [@igormagalhaesr](https://twitter.com/igormagalhaesr) – igormagalhaesr@gmail.com
[github.com/igormagalhaesr](https://github.com/igormagalhaesr/)