# `-shared` option is not supported on MacOSX.
CXX = g++
CXXFLAGS = -Wall -g

MAINFILE = compare-linkage
LIBFILE = helloworld
SHAREDLIB = lib$(LIBFILE).so

all: help

_static:
	$(CXX) $(CXXFLAGS) -c $(MAINFILE).cpp

_shared:
	$(CXX) $(CXXFLAGS) -c -o $(SHAREDLIB) -shared -fPIC $(LIBFILE).cpp

static: _static
	$(CXX) $(CXXFLAGS) -c $(LIBFILE).cpp
	$(CXX) -o static.exe $(MAINFILE).o $(LIBFILE).o

shared: _static _shared
	$(CXX) -o shared.exe $(MAINFILE).o $(SHAREDLIB)

shared-fail1: shared
	rm $(SHAREDLIB)
	-LD_LIBRARY_PATH=. ./shared.exe

shared-fail2: _shared
	$(CXX) $(CXXFLAGS) -DSHARED_FAIL -c $(MAINFILE).cpp
	$(CXX) -o shared.exe $(MAINFILE).o $(SHAREDLIB)
	LD_LIBRARY_PATH=. ./shared.exe

test: static shared
	./static.exe
	LD_LIBRARY_PATH=. ./shared.exe

clean:
	rm -f *~
	rm -f *.exe *.o *.so

help:
	@echo Available targets
	@echo - static: Build static binary.
	@echo - shared: Build shared binary.
	@echo - test  : Run each application.
	@echo - clean : Remove trash.
	@echo - help  : Show this message.
