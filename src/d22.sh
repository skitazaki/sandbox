#!/bin/sh
# Install PyYAML and ssl modules on Python.

python=${PYTHON-python}

[ -f ez_setup.py ] || wget -O ez_setup.py http://peak.telecommunity.com/dist/ez_setup.py
$python -c "import yaml" ||
    sudo $python ez_setup.py PyYAML
$python -c "import ssl" ||
    sudo $python ez_setup.py ssl

read -p "remove 'ez_setup.py'? [y/n] "
[ $REPLY = "y" ] && rm ez_setup.py

