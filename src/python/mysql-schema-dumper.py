#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dump all tables information from MySQL.
"""

import logging
import optparse
import os.path
import sys
import ConfigParser
from string import Template

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

try:
    import MySQLdb
except ImportError:
    raise SystemError("sudo apt-get install python2.6-mysqldb")


__doc__ = """\
python %prog [options] {database_setting_file.ini}

Show all databases schema as HTML format.
"""

IGNORE_DATABASES = ('information_schema', 'mysql', 'test', 'performance_schema')

BASE_HTML = Template("""<!DOCTYPE html>
<html lang="ja"><head>
<meta charset="UTF-8" />
<title>MySQL Database schema</title>
<style>$style</style>
</head><body>
<div id="container">$body</div>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6/jquery.min.js"></script>
<script>!window.jQuery && document.write('<script src="jquery.min.js"><\/script>')</script>
<script>$script</script>
</body></html>""")

SECTION_HTML = Template("""<div class="section database">
<h2 class="title">$database</h2>
$contents
</div>""")

CONTENT_HTML = Template("""<div class="content table">
<h3 class="title"><a name="$table">$table</a></h3>
<table><thead>
<tr>
    <th>Name</th>
    <th>Type</th>
    <th>Not Null</th>
    <th>Key</th>
    <th>Default</th>
    <th>Note</th>
</tr>
</thead><tbody>
$info
</tbody></table>
<pre class="code sql">$ddl</pre>
</div>""")

TABLE_FIELD_HTML = Template("""<tr>
    <td>$name</td>
    <td>$type</td>
    <td>$notnull</td>
    <td>$key</td>
    <td>$default</td>
    <td>$note</td>
</tr>""")

STYLE_CSS = """
table { border-collapse:collapse; width:100%; margin:auto; }
thead { background-color: #CCCCFF; }
th, td { border: solid 1px gray; }
h2.title { border-bottom: solid 1px black; }
h3.title { border-left: solid 1em blue; border-bottom: solid 1px blue; padding-left: 3px; }
.section { padding: 5px; border: solid 1px black; }
.content { padding: 5px; }
pre.code { padding: 5px; border: solid 1px gray; }
"""

SCRIPT_JS = """
$(function() {
    $(".section").each(function() {
        var $toc = $("<ul></ul>");
        $("h3.title").each(function() {
            var t = $(this).text();
            $("<li></li>").append(
                $("<a></a>", {href: "#" + t}).text(t))
                    .appendTo($toc);
        });
        $("h2.title", this).next().prepend($toc);
    });
});
"""

def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")

    opts, args = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if len(args) != 1:
        parser.error("Give me setting file.")

    return args[0]


class DBManager(object):

    _conn = None

    def __init__(self, setting):
        """Args:
        setting is a `dict` object whose keys are:
        * host: address to connect with MySQL. (default: 127.0.0.1)
        * port: port number of MySQL. (default: 3306)
        * username: user name of MySQL not local account. (default: mysql)
        * password: password of MySQL. (default: `None`)
        """
        self._setting = setting

    def _connect(self):
        """Try to connect MySQL database. If failed, throw IOError.
        """
        host = self._setting.get("host", "127.0.0.1")
        port = int(self._setting.get("port", 3306))
        username = self._setting.get("username", "mysql")
        password = self._setting.get("password", None)
        try:
            if password:
                self._conn = MySQLdb.connect(host=host, port=port,
                                user=username, passwd=password)
            else:
                self._conn = MySQLdb.connect(host=host, port=port,
                                user=username)
        except Exception:
            raise IOError("could not connect MySQL server with:" +
                    "host=%s, port=%d, username=%s, password=%s" %
                      (host, port, username, password))

    def _getcursor(self):
        if not self._conn:
            self._connect()
        return self._conn.cursor()

    def show_all_databases(self, writer):
        databases = self.get_all_databases()
        for dbname in databases:
            w = StringIO()
            self.show_schema(dbname, w)
            writer.write(SECTION_HTML.substitute(database=dbname,
                            contents=w.getvalue()))

    def get_all_databases(self):
        cursor = self._getcursor()
        cursor.execute("SHOW DATABASES")
        databases = [r[0] for r in cursor.fetchall()
            if not r[0] in IGNORE_DATABASES]
        cursor.close()
        return databases

    def get_tables(self, dbname):
        cursor = self._getcursor()
        cursor.execute("USE %s" % (dbname,))
        cursor.execute("SHOW TABLES")
        tables = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return tables

    def get_table_info(self, table):
        cursor = self._getcursor()
        cursor.execute("SHOW CREATE TABLE %s" % (table,))
        ret = cursor.fetchone()
        if ret and len(ret) == 2:
            ddl = ret[1]
        else:
            logging.info("No data definition query on %s" % (table,))
            ddl = None
        cursor.execute("DESC %s" % (table,))
        info = cursor.fetchall()
        cursor.close()
        return (ddl, info)

    def show_schema(self, dbname, writer):
        """Print out schema information as HTML format.
        """
        tables = self.get_tables(dbname)
        for t in tables:
            ddl, info = self.get_table_info(t)
            w = StringIO()
            for r in info:
                w.write(TABLE_FIELD_HTML.substitute(name=r[0], type=r[1],
                            notnull=r[2], key=r[3], default=r[4], note=r[5]))
            writer.write(CONTENT_HTML.substitute(table=t, ddl=ddl,
                            info=w.getvalue()))


def load_setting(fname):
    parser = ConfigParser.SafeConfigParser()
    try:
        parser.read(fname)
    except Exception, e:
        raise SystemExit("%s is invalid format." % (fname,))

    items = dict(parser.items('mysql')) \
                if parser.has_section('mysql') else {}
    setting = {}
    for k in items:
        if k.startswith('mysql_'):
            setting[k[6:]] = items[k]
        else:
            setting[k] = items[k]
    return setting


def main():
    fname = parse_args()
    setting = load_setting(fname) if os.path.exists(fname) else {}

    writer = StringIO()
    DBManager(setting).show_all_databases(writer)
    print BASE_HTML.substitute(body=writer.getvalue(),
            style=STYLE_CSS, script=SCRIPT_JS)

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
