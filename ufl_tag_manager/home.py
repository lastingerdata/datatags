#!/usr/bin/env python3
import cgi
import cgitb; cgitb.enable()
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from tags_index import main

main()
