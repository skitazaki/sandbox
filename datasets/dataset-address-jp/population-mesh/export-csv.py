# -*- coding: utf-8 -*-

"""Export "mesh4_pop_00" table without geom field.
"""

import csv

import click
import psycopg2


@click.command()
@click.option("--host", envvar="SANDBOX_POSTGRES_HOST")
@click.option("--port", envvar="SANDBOX_POSTGRES_PORT")
@click.option("--dbname", envvar="SANDBOX_POSTGRES_DBNAME")
@click.option("--username", envvar="SANDBOX_POSTGRES_USERNAME")
@click.option(
    "--password", envvar="SANDBOX_POSTGRES_PASSWORD", prompt=True, hide_input=True
)
def main(host, port, dbname, username, password):
    conn_spec = (
        f"host={host} port={port} dbname={dbname} user={username} password={password}"
    )
    conn = psycopg2.connect(conn_spec)
    cur = conn.cursor()
    columns = ["gid", "mesh_id", "city_code"]
    for p in ("", "a", "b", "c", "d"):
        columns.append("pop2010{}".format(p))
        columns.extend(["pop{}{}".format(y, p) for y in range(2020, 2051, 5)])
        columns.extend(["index{}{}".format(y, p) for y in range(2020, 2051, 5)])
    click.secho(f"Export {len(columns)} columns", fg="blue")
    query = "SELECT {} FROM mesh4_pop_00 ORDER BY 1".format(",".join(columns))
    cur.execute(query)
    counter = 0
    fname = "/tmp/mesh4-population.csv"
    with open(fname, "w") as fp:
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        writer.writerow(columns)
        for record in cur:
            # Format each cell as string
            r = [record[0], record[1]]  # gid, mesh_id
            r.append("{:05d}".format(record[2]))  # city_code
            for v in record[3:]:
                r.append("{:.02f}".format(v))
            writer.writerow(r)
            counter += 1
    click.secho(f"Wrote {counter} records to {fname}", fg="bright_blue", bold=True)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
