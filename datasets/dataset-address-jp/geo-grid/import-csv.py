# -*- coding: utf-8 -*-

"""Import a CSV file into the "geo_grid_lv4" table.
"""

import click
import datapackage
import psycopg2


TABLE_NAME = "geo_grid_lv4"
IMPORT_QUERY = f"""
INSERT INTO {TABLE_NAME}
  ("gid", "mesh_level4", "city_code", "geom")
  VALUES
  (%(gid)s, %(mesh_level4)s, %(city_code)s, ST_GeomFromGeoJSON(%(geom)s))
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
@click.option(
    "--truncate", is_flag=True, default=False, help="Truncate the table at first"
)
@click.argument("package_path", type=click.Path(exists=True))
def main(host, port, dbname, username, password, truncate, package_path):
    conn_spec = (
        f"host={host} port={port} dbname={dbname} user={username} password={password}"
    )
    conn = psycopg2.connect(conn_spec)
    cur = conn.cursor()
    if truncate:
        click.secho(f'Truncate the table "{TABLE_NAME}" at first', fg="red")
        cur.execute(f"TRUNCATE TABLE {TABLE_NAME}")
    package = datapackage.Package(package_path)
    columns = ["gid", "mesh_level4", "city_code", "geometry"]
    click.echo(
        click.style(f"Import datapackage ", fg="blue")
        + click.style(f"{package.descriptor.get('name')}", fg="blue", bold=True)
        + click.style(
            f", which has {len(package.resource_names)} resource(s)", fg="blue"
        )
    )
    resource_name = "geo_grid_lv4"
    resource = package.get_resource(resource_name)
    click.secho(
        f'Start to import "{resource.name}" into "{TABLE_NAME}" table', fg="green"
    )
    cnt = 0
    for r in resource.iter(keyed=True, cast=False):
        cur.execute(
            IMPORT_QUERY,
            {
                "gid": r["gid"],
                "mesh_level4": r["mesh_level4"],
                "city_code": r["city_code"],
                "geom": r["geom"],
            },
        )
        cnt += 1
        if cnt % 10000 == 0:
            click.secho(f" - processing {cnt} rows", fg="green")
    click.secho(f"Finish to import {resource.name} with {cnt:,} rows", fg="green")
    cur.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
