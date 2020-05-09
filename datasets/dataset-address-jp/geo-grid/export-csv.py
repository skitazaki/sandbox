# -*- coding: utf-8 -*-

"""Export "mesh4_pop_00" table with several fields.
"""

import csv

import click
import psycopg2

EXPORT_QUERY = """
SELECT
    gid
  , LPAD(mesh_id::VARCHAR, 9, '0')
  , LPAD(city_code::VARCHAR, 5, '0')
  , ST_AsGeoJSON(geom)
FROM mesh4_pop_00 ORDER BY 1
"""


@click.command()
@click.option("--host", required=True, envvar="SANDBOX_POSTGRES_HOST")
@click.option("--port", required=True, envvar="SANDBOX_POSTGRES_PORT")
@click.option("--dbname", required=True, envvar="SANDBOX_POSTGRES_DBNAME")
@click.option("--username", required=True, envvar="SANDBOX_POSTGRES_USERNAME")
@click.option(
    "--password",
    required=True,
    envvar="SANDBOX_POSTGRES_PASSWORD",
    prompt=True,
    hide_input=True,
)
@click.argument("output", type=click.File("w"))
def main(host, port, dbname, username, password, output):
    conn_spec = (
        f"host={host} port={port} dbname={dbname} user={username} password={password}"
    )
    conn = psycopg2.connect(conn_spec)
    cur = conn.cursor()
    columns = ["gid", "mesh_level4", "city_code", "geom"]
    click.secho(f"Export {len(columns)} columns", fg="blue")
    cur.execute(EXPORT_QUERY)
    counter = 0
    writer = csv.writer(output)
    writer.writerow(columns)
    for record in cur:
        writer.writerow(record)
        counter += 1
    click.secho(f"Wrote {counter:,} records", fg="bright_blue", bold=True)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
