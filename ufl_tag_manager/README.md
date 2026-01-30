
# DataTags Web Application

This repository contains the codebase for the DataTags web application hosted by the Lastinger Center at the University of Florida.

##  Hosting & Deployment

The application is hosted on UFIT-managed Apache infrastructure. It uses **CGI** for Python execution and **Shibboleth** for authentication. The default entry point is home.py, redirected via index.html.

Example command to pip install:
python3 -m pip install --user jinja2

Test Server:
ssh cnswww-test.datatags.lastinger@az1-apacheint-prod02.server.ufl.edu

Production Server:
ssh cnswww-datatags.lastinger@az1-apacheint-prod02.server.ufl.edu

The application reads from an env.txt file to determine the environment:
test → uses test API endpoints
prod → uses production endpoints

The application requires the following pip modules:
- `ibna`
- `requests`
-  `jinja2`

## File Permissions

For convenience, you can fix script permissions across the project using:
find ./ -name "*.py" -exec chmod 755 {} \;


contact Sushma-(su.palle@ufl.edu) for SSH access requests.
