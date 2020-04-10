# -*- coding: utf-8 -*-

"""Helper HTTP server for JavaScript playground.

$ export FLASK_APP=sandboxlib.httpsrv
$ export FLASK_ENV=development
$ export SANDBOX_STATIC_DIR=$PWD/../javascript/playground
$ export SANDBOX_TEMPLATE_DIR=$PWD/../javascript/playground
$ flask run
"""

import os
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template


def create_app(test_config=None):
    try:
        from dotenv import load_dotenv, find_dotenv

        load_dotenv(find_dotenv())  # Load an upper level file as well
    except ImportError:
        pass

    app = Flask(__name__, instance_relative_config=True, static_url_path="/static")
    if static_dir := os.getenv("SANDBOX_STATIC_DIR"):
        app.static_folder = static_dir
    if template_dir := os.getenv("SANDBOX_TEMPLATE_DIR"):
        app.template_folder = template_dir

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow()}

    @app.route("/<name>.html")
    def hello(name):
        static_dir = Path(app.static_folder)
        use_css = True if (static_dir / f"{name}.css").exists() else False
        use_js = True if (static_dir / f"{name}.js").exists() else False
        return render_template(
            f"{name}.html", name=name, use_css=use_css, use_js=use_js
        )

    return app
