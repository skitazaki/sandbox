# Play with Python on Sandbox

## Getting Started

Set up your virtual environment and install dependencies.

```
$ pyvenv_dir=venv
$ python3 -m venv $pyvenv_dir --prompt python-sandbox
$ source $pyvenv_dir/bin/activate
$ python3 -m pip install -U pip
$ python3 -m pip install -r requirements.txt
```

Check your installation is successful.

```
$ python3 -c "import sandboxlib"
```
