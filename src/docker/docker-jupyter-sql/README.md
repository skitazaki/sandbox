# Scipy Notebook plus SQL extension

[jupyter/scipy-notebook/](https://hub.docker.com/r/jupyter/scipy-notebook) plus following modules.

- [Psycopg - PostgreSQL database adapter for Python](http://pythonhosted.org/psycopg2/index.html)
- [%%sql magic for IPython, hopefully evolving into full SQL client](https://github.com/catherinedevlin/ipython-sql)

## Development

Set external port mappings to set environmental variables.

```bash
$ cp -pv .env-example .env
$ vi .env
```

Start up PostgreSQL database and Notebook containers.
After `up`, check the processes are running.

```bash
$ docker-compose up -d
$ docker-compose ps
$ docker-compose logs notebook | grep token=
```

To interact with database on cosole, use *exec* command.

```bash
$ docker-compose exec -u postgres postgres /bin/bash
```

## Misc resources

* [Ipython-quick-ref-sheets](http://damontallen.github.io/IPython-quick-ref-sheets/)
