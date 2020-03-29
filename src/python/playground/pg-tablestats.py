# -*- coding: utf-8 -*-

"""Simple stats of PostgreSQL tables.
"""

import datetime
import logging

import click
import jinja2
import psycopg2
import yaml

import sandboxlib


query_template_00 = """/**
 * Show tables in the given schema.
 *
 * @query: schemaname
 */
SELECT relname
  FROM pg_catalog.pg_stat_user_tables
 WHERE schemaname = %(schemaname)s
ORDER BY relname ;
"""

query_template_01_j2 = """/**
 * Show table name and number of columns and records.
 *
 * @query: schemaname
 * @template: schemaname
 * @template: tables
 */
WITH c AS (
  SELECT table_name,
         COUNT(*) AS n_columns,
         COUNT(*) FILTER (WHERE LOWER(is_nullable) = 'no') AS n_columns_notnull
    FROM information_schema.columns
   WHERE table_schema = %(schemaname)s
  GROUP BY table_name
), t AS (
{% for table in tables -%}
{% if not loop.first %}UNION ALL{% endif %}
  SELECT '{{ table }}' AS table_name,
         COUNT(*) AS n_records
    FROM "{{ schemaname }}"."{{ table }}"
{% endfor -%}
)
SELECT ROW_NUMBER() OVER (ORDER BY c.table_name) AS "number",
       c.table_name,
       c.n_columns,
       c.n_columns_notnull,
       t.n_records
  FROM c
       INNER JOIN t USING (table_name)
ORDER BY "number" ;
"""

query_template_02 = """/**
 * Show column information in the given table.
 *
 * @query: schemaname
 * @query: tablename
 */
SELECT column_name,
       is_nullable,
       data_type,
       character_maximum_length,
       numeric_precision,
       numeric_precision_radix,
       numeric_scale,
       datetime_precision,
       interval_type,
       interval_precision,
       udt_name,
       column_default
  FROM information_schema.columns
 WHERE table_schema = %(schemaname)s AND table_name = %(tablename)s
ORDER BY ordinal_position ;
"""

query_template_03_j2 = """/**
 * Calculate field summary.
 *
 * @template: schemaname
 * @template: tablename
 * @template: columns
 */
WITH t AS (
{% for column in columns -%}
{% if not loop.first %}UNION ALL{% endif %}
SELECT CAST('{{ column.column_name }}' AS TEXT) AS column_name,
       COUNT("{{ column.column_name }}") AS n_records,
       COUNT(DISTINCT "{{ column.column_name }}") AS n_patterns
  FROM "{{ schemaname }}"."{{ tablename }}"
{% endfor -%}
)
SELECT column_name,
       n_records,
       n_patterns
  FROM t ;
"""

output_template_html = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
<title>Table stats on {{ _metadata.dbname }}.{{ _metadata.schema }}</title>
</head>
<body>
<header>
<div class="container">
</div>  <!-- /container -->
</header>
<main role="main">
<div class="container">
<h1>Table stats on {{ _metadata.dbname }}.{{ _metadata.schema }}</h1>
<table class="table table-striped table-condensed table-hover">
<thead>
<tr>
  <th>Table name</th>
  <th>Number of columns</th>
  <th>Number of columns with not null</th>
  <th>Number of records</th>
</th>
</thead>
<tbody>
{%- for table in tables -%}
<tr>
  <th><a href="#{{ _metadata.schema }}.{{ table.name }}">{{ table.name }}</a></th>
  <td>{{ table.n_columns }}</td>
  <td>{{ table.n_columns_notnull }}</td>
  <td>{{ "{:,}".format(table.n_records) }}</td>
</tr>
{%- endfor -%}
</tbody>
</table>
{%- for table in tables -%}
<a name="{{ _metadata.schema }}.{{ table.name }}"><h2>{{ table.name }}</h2></a>
<table class="table table-striped table-condensed table-hover">
<thead>
<tr>
  <th>Column name</th>
  <td>Is Nullable</td>
  <td>Data type</td>
  <td>Character maximum length</td>
  <td>Numeric precision</td>
  <td>Numeric precision radix</td>
  <td>Numeric scale</td>
  <td>Datetime precision</td>
  <td>Interval type</td>
  <td>Interval precision</td>
  <td>Udt name</td>
  <td>Column default</td>
  <td>Number of records</td>
  <td>Number of patterns</td>
</th>
</thead>
<tbody>
{%- for column in table.columns -%}
<tr>
  <th>{{ column.column_name }}</th>
  <td>{{ column.is_nullable }}</td>
  <td>{{ column.data_type }}</td>
  <td>{{ column.character_maximum_length or '' }}</td>
  <td>{{ column.numeric_precision or '' }}</td>
  <td>{{ column.numeric_precision_radix or '' }}</td>
  <td>{{ column.numeric_scale or '' }}</td>
  <td>{{ column.datetime_precision or '' }}</td>
  <td>{{ column.interval_type or '' }}</td>
  <td>{{ column.interval_precision or '' }}</td>
  <td>{{ column.udt_name or '' }}</td>
  <td>{{ column.column_default or '' }}</td>
  <td>{{ "{:,}".format(column.n_records) }}</td>
  <td>{{ "{:,}".format(column.n_patterns) }}</td>
</tr>
{%- endfor -%}
</tbody>
</table>
{%- endfor -%}
</div>  <!-- /container -->
</main>
<footer class="text-muted">
<div class="container">
<p class="float-right">
generated at {{ _metadata.generated_at }}
</p>
</div>  <!-- /container -->
</footer>
</body>
</html>
"""


def fetch_as_dict_records(cursor, query: str, params: dict = None, logger="") -> list:
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    logger.debug(f"fetch_as_dict_records() execute: {query}")
    cursor.execute(query, params)
    names = [column.name for column in cursor.description]
    dt = [dict(zip(names, r)) for r in cursor]
    logger.debug(
        f"fetch_as_dict_records() fetched: {len(names)} column(s), {len(dt)} row(s)"
    )
    return dt


def tablestats(cursor, schema: str, logger="") -> list:
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    cursor.execute(query_template_00, {"schemaname": schema})
    tables = [r[0] for r in cursor]
    n_tables = len(tables)
    logger.info(f'schema "{schema}" has {n_tables} table(s)')
    if n_tables == 0:
        return
    template = jinja2.Template(query_template_01_j2)
    q = template.render(schemaname=schema, tables=tables)
    table_results = fetch_as_dict_records(cursor, q, {"schemaname": schema}, logger)
    results = []
    for i, table in enumerate(table_results):
        name = table["table_name"]
        logger.info(f"[{i+1}/{n_tables}] {name}")
        r = {
            "name": name,
            "n_columns": table["n_columns"],
            "n_columns_notnull": table["n_columns_notnull"],
            "n_records": table["n_records"],
        }
        columns = fetch_as_dict_records(
            cursor, query_template_02, {"schemaname": schema, "tablename": name}, logger
        )
        logger.info(f"- collected {len(columns)} column(s)")
        logger.info(f'- calculate stats over {table["n_columns"]} record(s)')
        template = jinja2.Template(query_template_03_j2)
        q = template.render(schemaname=schema, tablename=name, columns=columns)
        columns_stats = fetch_as_dict_records(cursor, q, logger=logger)
        for s in columns_stats:
            for c in columns:
                if s["column_name"] == c["column_name"]:
                    c["n_records"] = s["n_records"]
                    c["n_patterns"] = s["n_patterns"]
        r["columns"] = columns
        results.append(r)
    return results


def write_as_yaml(data, output):
    yaml.safe_dump(data, output)


def write_as_html(data, output):
    template = jinja2.Template(output_template_html)
    template.stream(data).dump(output)


@click.command()
@click.option("--host", envvar="SANDBOX_POSTGRES_HOST")
@click.option("--port", envvar="SANDBOX_POSTGRES_PORT", type=int)
@click.option("--dbname", envvar="SANDBOX_POSTGRES_DBNAME")
@click.option("--username", envvar="SANDBOX_POSTGRES_USERNAME")
@click.option("--password", envvar="SANDBOX_POSTGRES_PASSWORD", prompt=True)
@click.option(
    "--schema",
    default="public",
    show_default=True,
    help="name of schema you want to see",
)
@click.option(
    "--format",
    help="output format",
    default="yaml",
    show_default=True,
    type=click.Choice(["yaml", "html"], case_sensitive=False),
)
@click.option("-v", "--verbose", count=True, help="increase logging verbosity")
@click.option(
    "-q", "--quiet/--no-quiet", is_flag=True, help="set logging to quiet mode"
)
@click.argument("output", type=click.File("w"))
def main(
    host, port, dbname, username, password, schema, output, format, verbose, quiet
):
    sandboxlib.configure_logging(verbose=verbose, quiet=quiet)
    conn_spec = (
        f"host={host} port={port} dbname={dbname} user={username} password={password}"
    )
    with psycopg2.connect(conn_spec) as conn:
        with conn.cursor() as cur:
            stats = tablestats(cur, schema, logger="sandbox")
    if stats is None:
        return
    with output:
        now = datetime.datetime.now()
        data = {
            "_metadata": {
                "host": host,
                "port": port,
                "dbname": dbname,
                "schema": schema,
                "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            "tables": stats,
        }
        if format == "yaml":
            write_as_yaml(data, output)
        elif format == "html":
            write_as_html(data, output)


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv, find_dotenv

        load_dotenv(find_dotenv())  # Load an upper level file as well
    except ImportError:
        pass
    main()
