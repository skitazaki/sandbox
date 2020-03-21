IPython Docker image on top of Python 3.4
=========================================

Docker image to use IPython on top of Python 3.4.

These libraries are available.

* *numpy* : 1.9.1
* *scipy* : 0.14.0
* *matplotlib* : 1.4.2
* *pandas* : 0.15.1
* *scikit-learn* (*sklearn*) : 0.15.2
* *networkx* : 1.9.1
* *xlsxwriter* : 0.6.4
* *bokeh* : 0.7.0

Shared resources:

* `8888` port is exposed.
* `/notebook` directory is mountable.

Run
---

Run IPython Notebook server (default command).

    docker run -d -p 8080:8888 skitazaki/python34-ipython

Run IPython Notebook server to share local file system.

    docker run -d -p 8080:8888 -v $PWD:/notebook skitazaki/python34-ipython

Use interactive shell.

    docker run --rm -it skitazaki/python34-ipython ipython

Build
-----

    docker build --rm -t skitazaki/python34-ipython .

Links
------

* [Examples on nbviewer](http://nbviewer.ipython.org/github/skitazaki/docker-python34-ipython/tree/master/examples/)
* [Ipython-quick-ref-sheets](http://damontallen.github.io/IPython-quick-ref-sheets/)
* [How-to: Use IPython Notebook with Apache Spark](http://blog.cloudera.com/blog/2014/08/how-to-use-ipython-notebook-with-apache-spark/)
