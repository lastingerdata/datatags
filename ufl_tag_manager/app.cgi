from wsgiref.handlers import CGIHandler
import os

from app import create_app
application = create_app()

CGIHandler().run(application)
