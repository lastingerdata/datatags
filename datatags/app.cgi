from wsgiref.handlers import CGIHandler

from app import create_app
application = create_app()

CGIHandler().run(application)
