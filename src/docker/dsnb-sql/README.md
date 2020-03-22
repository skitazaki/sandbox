# Data Science Notebook plus SQL extension

[jupyter/datascience-notebook/](https://hub.docker.com/r/jupyter/datascience-notebook/) plus following modules.

- [Psycopg - PostgreSQL database adapter for Python](http://pythonhosted.org/psycopg2/index.html)
- [%%sql magic for IPython, hopefully evolving into full SQL client](https://github.com/catherinedevlin/ipython-sql)

## Development

Set external port mappings to set environmental variables.

```bash
$ source .envrc
```

Start up PostgreSQL database and Notebook containers.
After `up`, check the processes are running.

```bash
$ docker-compose up -d
$ docker-compose ps
```

To interact with database on cosole, use *pgcli* service.

```bash
$ docker-compose run --rm pgcli
```

## Test data

Use *pagila* as test data.

At first, clone the repository from GitHub.

```bash
$ cd data
$ git clone https://github.com/devrimgunduz/pagila.git
$ cd pagila
$ git checkout pagila-0.11.0
$ cd ../..
```

Run SQL queries on *pgcli* container.

```bash
$ docker-compose run --rm pgcli psql -f /data/pagila/pagila-schema.sql
$ docker-compose run --rm pgcli psql -f /data/pagila/pagila-data.sql
```