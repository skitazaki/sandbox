# Scipy Notebook plus SQL extension

[jupyter/scipy-notebook/](https://hub.docker.com/r/jupyter/scipy-notebook) plus following modules.

- [Psycopg - PostgreSQL database adapter for Python](http://pythonhosted.org/psycopg2/index.html)
- [%%sql magic for IPython, hopefully evolving into full SQL client](https://github.com/catherinedevlin/ipython-sql)

## Setup

Prepare your environment with a `.env` file in order to configure port mappings and database accounts.

```bash
$ cp -pv .env-example .env
$ vi .env
```

Start up PostgreSQL database and Notebook containers with `docker-compose`.
You can find the access token on Jupyter in the log stream.

```bash
$ docker-compose up -d
$ docker-compose ps
$ docker-compose logs notebook | grep token=
```

To interact with database, use *exec* command on the *postgres* container.

```bash
$ docker-compose exec -u postgres postgres /bin/bash
```

## Notebooks

- `setupdb.ipynb`: Set up the database container
- `sample_psycopg2.ipynb`: Example of *psycopg2* package
- `pagila-example.ipynb`: Example of Pagila, Postgres clone of Sakila in MySQL
- `datareader_bokeh.ipynb`: Example of *pandas_datareader* and *bokeh*
- `datareader_to_excel.ipynb`: Example of *pandas_datareader* and *to_excel()* on pandas.DataFrame

## Misc resources

* [Ipython-quick-ref-sheets](http://damontallen.github.io/IPython-quick-ref-sheets/)
