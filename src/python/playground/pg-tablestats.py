# -*- coding: utf-8 -*-

"""Simple stats of PostgreSQL tables.
"""

import datetime
import logging

import click
import jinja2
import psycopg2
import yaml
from dotenv import load_dotenv, find_dotenv

import sandboxlib


template_00 = """/**
 * Show tables in the given schema.
 *
 * @query: schemaname
 */
SELECT relname
  FROM pg_catalog.pg_stat_user_tables
 WHERE schemaname = %(schemaname)s
ORDER BY relname ;
"""

template_01_j2 = """/**
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

template_02 = """/**
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

template_03_j2 = """/**
 * Calculate field summary.
 *
 * @template param: schemaname
 * @template param: tablename
 * @template param: columns
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
    cursor.execute(template_00, {"schemaname": schema})
    tables = [r[0] for r in cursor]
    n_tables = len(tables)
    logger.info(f'schema "{schema}" has {n_tables} table(s)')
    template = jinja2.Template(template_01_j2)
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
            cursor, template_02, {"schemaname": schema, "tablename": name}, logger
        )
        logger.info(f"- collected {len(columns)} column(s)")
        logger.info(f'- calculate stats over {table["n_columns"]} record(s)')
        template = jinja2.Template(template_03_j2)
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


@click.command()
@click.option("--host", envvar="SANDBOX_POSTGRES_HOST")
@click.option("--port", envvar="SANDBOX_POSTGRES_PORT")
@click.option("--dbname", envvar="SANDBOX_POSTGRES_DBNAME")
@click.option("--username", envvar="SANDBOX_POSTGRES_USERNAME")
@click.option("--password", envvar="SANDBOX_POSTGRES_PASSWORD", prompt=True)
@click.option("--schema", default="public")
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet/--no-quiet", is_flag=True)
@click.argument("output", type=click.File("w"))
def main(host, port, dbname, username, password, schema, output, verbose, quiet):
    sandboxlib.configure_logging(verbose=verbose, quiet=quiet)
    conn_spec = (
        f"host={host} port={port} dbname={dbname} user={username} password={password}"
    )
    with psycopg2.connect(conn_spec) as conn:
        with conn.cursor() as cur:
            stats = tablestats(cur, schema, logger="sandbox")
    with output:
        now = datetime.datetime.now()
        yaml.safe_dump(
            {
                "_metadata": {
                    "host": host,
                    "port": port,
                    "dbname": dbname,
                    "schema": schema,
                    "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S"),
                },
                "tables": stats,
            },
            output,
        )


if __name__ == "__main__":
    load_dotenv(find_dotenv())  # Load an upper level file
    main()
