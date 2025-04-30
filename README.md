# Mosaic Note API Server

This API Server is for the Mosaic Note project.

## setup environment

> All setup commands should be run in the root directory of the project.

### install poetry

> Familiar with the use of Poetry.
> 
> Refer to [Poetry installation](https://python-poetry.org/docs/)

### virtualenv

```shell
poetry install
poetry shell
```

### docker

Make sure you have Docker installed and running.

> start up local redis and postgresql server with `docker-compose.yml`

```shell
docker compose up -d
```

### copy local settings

```shell
cp example.env .env
```

> Edit `.env` file to set up your local environment variables.

### init db

> How to use Alembic to manage database migrations.
> 
> Refer to [Alembic documentation](http://alembic.sqlalchemy.org/en/latest/tutorial.html)

#### About Branch

> The concept is similar to a branch in git.
> 
> It allows you to create a new version of the database schema without affecting the current version.

[Alembic Branching](https://alembic.sqlalchemy.org/en/latest/branches.html)

#### Init Migration

> Refer to [Alembic(First Migration)](https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration)

```shell
alembic upgrade head
```

#### Create Migration

```shell
alembic revision -m "{your message}"
```

#### Upgrade Migration

> Refer to [Alembic(Partial Revision Identifiers)](https://alembic.sqlalchemy.org/en/latest/tutorial.html#partial-revision-identifiers)

```shell
alembic upgrade {revision}
```

#### Downgrade Migration

> Refer to [Alembic(Relative Migration Identifiers)](https://alembic.sqlalchemy.org/en/latest/tutorial.html#relative-migration-identifiers)

```shell
alembic downgrade -1
```
or
```shell
alembic downgrade {revision}
```

#### Get Current Version

> Refer to [Alembic(Getting Information)](https://alembic.sqlalchemy.org/en/latest/tutorial.html#getting-information)
```shell
alembic current
```

#### Show Migration History

> Refer to [Alembic(Viewing History Ranges)](https://alembic.sqlalchemy.org/en/latest/tutorial.html#viewing-history-ranges)

```shell
alembic history
```
or
```shell
alembic history --verbose
```

## Run Fastapi server

```shell
# debug
uvicorn app:app --reload
```

### Output

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [68287] using StatReload
INFO:     Started server process [68289]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### API documentation

API documentation reference clicks [here](http://127.0.0.1:8000/docs)
