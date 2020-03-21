@echo OFF
setlocal

SET BASEDIR=.
SET TARGET=cybozulive

python "python\sample.py" -v %TARGET%

endlocal
