# Play with Python on Sandbox

## Getting Started

Set up your virtual environment and install dependencies.

```
$ pyvenv_dir=$HOME/.local/share/virtualenvs/python-sandbox
$ python3 -m venv $pyvenv_dir --prompt python-sandbox
$ source $pyvenv_dir/bin/activate
$ python3 -m pip install -U pip
$ python3 -m pip install -r requirements.txt
$ python3 -m pip install -r requirements-dev.txt
```

Check your installation is successful.

```
$ python3 -c "import sandboxlib"
```
