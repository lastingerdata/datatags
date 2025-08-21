#!/usr/bin/env python3
import os, sys
BASE = os.path.dirname(__file__)
sys.path.insert(0, BASE)
sys.path.append("/reporting/python/")

from app import app as application
from flup.server.fcgi import WSGIServer

if __name__ == "__main__":
    WSGIServer(application).run()
