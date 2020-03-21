BASEDIR = .
CRED_DIR = $(BASEDIR)/credential
CONFIGURATION = $(BASEDIR)/settings.ini
TARGET = cybozulive

PYTHON = python
PYTHON_PEP8 = pep8

WORK_PYTHON = $(BASEDIR)/python
WORK_JAVASCRIPT = $(BASEDIR)/js
WORK_TEST = $(BASEDIR)/test

TEST_PORT = 8080

all:
	$(PYTHON) $(WORK_PYTHON)/sample.py -v $(TARGET)

check:
	$(PYTHON_PEP8) --repeat --show-source $(WORK_PYTHON)/*.py
	$(PYTHON_PEP8) --repeat --show-source $(WORK_TEST)/websrv.py

build:
	$(PYTHON) $(WORK_JAVASCRIPT)/build.py -d $(WORK_JAVASCRIPT) -f $(CONFIGURATION) $(TARGET) >$(WORK_JAVASCRIPT)/oauth.html

prepare:
	[ -f js/jquery.min.js ] || wget -O js/jquery.min.js "http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"
	[ -f js/jquery-ui.min.js ] || wget -O js/jquery-ui.min.js "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.5/jquery-ui.min.js"
	[ -f js/reset-min.css ] || wget -O js/reset-min.css "http://yui.yahooapis.com/3.1.1/build/cssreset/reset-min.css"
	[ -f js/oauth.js ] || wget -O js/oauth.js "http://oauth.googlecode.com/svn/code/javascript/oauth.js"
	[ -f js/sha1.js ] || wget -O js/sha1.js "http://oauth.googlecode.com/svn/code/javascript/sha1.js"

run-server:
	twistd -n web -p $(TEST_PORT) --resource-script=test/websrv.py

clean:
	rm -f *~ **/*~
	rm -f python/*.pyc

