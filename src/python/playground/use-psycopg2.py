# -*- coding: utf-8 -*-

"""Sample usage of `psycopg2` module.
"""

import click
import psycopg2
from dotenv import load_dotenv, find_dotenv


@click.command()
@click.option("--host", envvar="SANDBOX_POSTGRES_HOST")
@click.option("--port", envvar="SANDBOX_POSTGRES_PORT")
@click.option("--dbname", envvar="SANDBOX_POSTGRES_DBNAME")
@click.option("--username", envvar="SANDBOX_POSTGRES_USERNAME")
@click.option("--password", envvar="SANDBOX_POSTGRES_PASSWORD", prompt=True)
def main(host, port, dbname, username, password):
    table_name = f"sandbox.test"
    conn_spec = (
        f"host={host} port={port} dbname={dbname} user={username} password={password}"
    )
    conn = psycopg2.connect(conn_spec)
    cur = conn.cursor()
    cur.execute(
        f"CREATE TABLE {table_name} (id serial PRIMARY KEY, num integer, data varchar);"
    )
    cur.execute(
        f"INSERT INTO {table_name} (num, data) VALUES (%s, %s)", (100, "abc'def")
    )
    cur.execute(f"SELECT * FROM {table_name};")
    print(cur.fetchone())
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    load_dotenv(find_dotenv())  # Load an upper level file
    main()
