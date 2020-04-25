# -*- coding: utf-8 -*-

"""Concatenate CSV files in Zip files.
"""

import csv
import zipfile
from collections import Counter
from pathlib import Path

import click
import yaml

DOWNLOADED_FILE_ENCODING = "cp932"


@click.command()
@click.argument("dirpath", type=click.Path(exists=True))
def main(dirpath):
    basedir = Path(dirpath)
    counter_stats = Counter()
    counter = Counter()
    outputs = {}
    for i, x in enumerate(sorted(basedir.glob("*.zip"))):
        click.secho(f"[{i+1}] {x.name}", bold=True, fg="bright_red")
        counter_stats["n_files"] += 1
        ftype = x.stem.split("-")[1]
        click.secho(f" - File type is {ftype} ({ftype[-1]})", fg="magenta")
        counter_stats[f"n_files_{ftype}"] += 1
        with zipfile.ZipFile(x) as z:
            names = z.namelist()
            click.secho(f" - Zip file contains {len(names)} files")
            for name in names:
                if name.lower().endswith(".csv"):
                    click.secho(f" - Found a CSV file: {name}", fg="red")
                    with z.open(name) as csvbytes:
                        reader = csv.reader(
                            map(lambda s: s.decode(DOWNLOADED_FILE_ENCODING), csvbytes)
                        )
                        header = next(reader)
                        click.secho(f" - The CSV file has {len(header):,} columns")
                        if ftype not in outputs:
                            out = open(f"locref-{ftype}.csv", "w")
                            outputs[ftype] = out
                            w = csv.writer(out)
                            w.writerow(header)
                        for row in reader:
                            counter[name] += 1
                            out = outputs[ftype]
                            w = csv.writer(out)
                            w.writerow(row)
                            counter_stats[f"n_records_{ftype}"] += 1
                    click.secho(f" - The CSV file has {counter[name]:,} records")
    for k in outputs:
        click.secho(f"Close an output stream {k}")
        outputs[k].close()
    click.secho(f"Write metadata into locref-meta.yaml", bold=True, fg="blue")
    with open("locref-meta.yaml", "w") as fp:
        yaml.safe_dump({"stats": dict(counter_stats), "sources": dict(counter),}, fp)


if __name__ == "__main__":
    main()
