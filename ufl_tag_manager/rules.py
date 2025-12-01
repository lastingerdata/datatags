#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, traceback, urllib.parse
from urllib.parse import quote
from html import escape

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import safe_request

BASE_PATH = "/ufl_tag_manager"
EXT = ".py"

REPORT_LOGS_URL = "https://compute.lastinger.center.ufl.edu/rules"
API_KEY = "596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce"

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)
def fetch_rules():
    headers = {"Accept": "application/json", "ApiKey": API_KEY}
    resp = safe_request(REPORT_LOGS_URL, headers=headers, verify=False)