Access Dashboard
================

## Prerequisites

* Python 3.4
* Node
    * NPM
    * Bower
* *direnv* for easy development setup
* Docker (If you need runtime container)

## Development Setup

Common:

    $ cp .envrc.template .envrc
    $ vim .envrc    # Edit manually on your own.
    $ direnv allow .

Server side: (Note that `requirements.txt` will be moved into `src`)

    $ pip install -r requirements.txt

Client side:

    $ cd client
    $ npm install && bower install
    $ cp -p app/bower_components/nvd3/nv.d3.css app/bower_components/nvd3/nv.d3.scss
    $ grunt serve

Server APIs accept cross domain requests on local development server.

## Database Setup

Edit `src/dashboard/settings.py` on your own.
And, run Django's management command to create base tables and a super user.

    $ cd src
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py makemigrations accesslog
    $ python manage.py sqlmigrate accesslog 0001
    $ python manage.py migrate

## Sample Setup

Import raw accsslog:

    $ python manage.py importlog --source {SERVER} {/path/to/access_log}
    $ python manage.py makesummary --source {SERVER} --action day

If your access logs are transfered by "Fluend" to S3, you can use "fluentd" parser.

    $ python manage.py importlog --parser fluentd {/path/to/fluentd.log}

## Build

Client side:

    $ cd client
    $ grunt build

OR

    $ cd client
    $ docker build --rm --no-cache -t my/nodejs-build .
    $ docker run -v `pwd`/dist:/tmp/dist --rm -it my/nodejs-build "cp -r /app/dist /tmp"

Server side:

    $ docker build --rm -t my/dashboard .

Run the container:

    $ docker run -p 80:80 -d my/dashboard

Note that put following files on the top directory before building server runtime.
They are ignored for git versioning.

* `sshkey.pub` : Public key of ssh connection for docker container.
* `secret_key.txt` : One line text file which contains secret key for `settings.py`.

All operations are integrated into `build.sh`.
