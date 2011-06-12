#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Put 'sitecustomize.py' on your system path.

import sys
import os.path

encoding = "utf-8"
site_package = [d for d in sys.path
                    if os.path.basename(d) == "site-packages"][0]
try:
    f = open(os.path.join(site_package, "sitecustomize.py"), "w")
except IOError:
    print("Permission denied, retry with 'sudo'.")
    sys.exit(1)
f.write('''import sys
sys.setdefaultencoding("%s") ''' % encoding)
f.close()
print('''Set system encoding for Python scripts.
Confirm: %s/sitecustomize.py''' % site_package)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
