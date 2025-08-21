import os, sys, logging
from flask import Flask, render_template, request, session


package_directory = "/reporting/python/"
if package_directory not in sys.path:
    sys.path.append(package_directory)

from flask_restful import Api
from flasgger import Swagger

from libs.db_ops import (
    get_all_tags, add_tag, delete_tag,
    get_tag_values, add_tag_value, delete_tag_value,
    get_all_tag_values, get_section_tag_mappings,
    delete_section_tag, update_tag_value,
    get_course_sections, map_tag_to_sections, delete_section_tag
)
from auth import login_required, auth_blueprint

app = Flask(__name__)
Api(app)
app.register_blueprint(auth_blueprint)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-secret')


app.config['SWAGGER'] = {'title': 'My API','uiversion': 3,"specs_route": "/swagger/"}
Swagger(app)

@app.route('/debug_session')
def debug_session():
    return f"Session: {session.get('user')}"

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
    from flask import redirect, url_for, flash
    if request.method == 'POST':
        tag_name = request.form.get('tag_name')
        description = request.form.get('description')
        if tag_name:
            try:
                add_tag(tag_name, description); flash("Tag added", "success")
            except Exception as e:
                flash(str(e), "danger")
    tags = get_all_tags()
    return render_template('tags.html', tags=tags)

@app.route('/delete_tag', methods=['POST'])
@login_required
def delete_tag_route():
    from flask import redirect, url_for, flash
    tag_id = request.form.get('tag_id')
    try:
        delete_tag(tag_id); flash("Tag deleted", "success")
    except Exception:
        flash("Cannot delete tag (likely has associated values)", "warning")
    return redirect(url_for('tags'))

@app.route('/tag_values', methods=['GET', 'POST'])
@login_required
def tag_values():
    from flask import redirect, url_for, flash
    tags = get_all_tags()
    selected_tag_id = request.form.get('selected_tag') or request.args.get('selected_tag')
    if request.method == 'POST':
        if 'add_value' in request.form:
            tag_value = request.form.get('tag_value')
            description = request.form.get('description')
            if tag_value and selected_tag_id:
                try:
                    add_tag_value(selected_tag_id, tag_value, description); flash("Value added", "success")
                except Exception as e:
                    flash(str(e), "danger")
        elif 'update_value' in request.form:
            tag_entry_id = request.form.get('tag_entry_id')
            updated_value = request.form.get('updated_tag_value')
            description = request.form.get('updated_description')
            if tag_entry_id and updated_value:
                try:
                    update_tag_value(tag_entry_id, updated_value, description); flash("Value updated", "success")
                except Exception as e:
                    flash(str(e), "danger")
    values = get_tag_values(selected_tag_id) if selected_tag_id else []
    return render_template('tag_values.html', tags=tags, values=values,
                           selected_tag_id=int(selected_tag_id) if selected_tag_id else None)

@app.route('/delete_tag_value', methods=['POST'])
@login_required
def delete_tag_value_route():
    from flask import redirect, url_for, flash
    tag_entry_id = request.form.get('tag_entry_id')
    tag_id = request.form.get('tag_id')
    if tag_entry_id:
        try:
            delete_tag_value(tag_entry_id); flash("Value deleted", "success")
        except Exception as e:
            flash(str(e), "danger")
    return redirect(url_for('tag_values', selected_tag=tag_id))

@app.route('/delete_section_tag', methods=['POST'])
@login_required
def delete_section_tag_route():
    from flask import redirect, url_for, flash
    d2l_id = request.form.get('d2l_OrgUnitId')
    section_id = request.form.get('genius_sectionId')
    tag_entry_id = request.form.get('tag_entry_id')
    try:
        delete_section_tag(d2l_id, section_id, tag_entry_id); flash("Section tag deleted", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('section_tags'))

@app.route('/section_tags', methods=['GET', 'POST'])
@login_required
def section_tags():
    tag_values = get_all_tag_values()
    mappings = get_section_tag_mappings()
    return render_template('section_tags.html', tag_values=tag_values, mappings=mappings)

@app.route('/section_tags_inserts', methods=['GET', 'POST'])
@login_required
def section_tags_inserts():
    from flask import redirect, url_for, flash
    tag_values = get_all_tag_values()
    search = request.args.get('search', '').strip().lower()
    tag_entry_id = (request.form.get('tag_entry_id') if request.method == 'POST'
                    else request.args.get('tag_entry_id'))
    courses = get_course_sections(search, tag_entry_id)
    if request.method == 'POST' and 'map' in request.form:
        selected = request.form.getlist('selected_courses')
        if not tag_entry_id:
            flash("Please select a tag to apply.", "danger")
        elif not selected:
            flash("Please select at least one course.", "danger")
        else:
            map_tag_to_sections(tag_entry_id, selected)
            flash("Tag applied to selected courses", "success")
            return redirect(url_for('section_tags_inserts', tag_entry_id=tag_entry_id, search=search))
    return render_template('section_tags_bulk_update.html', tag_values=tag_values,
                           courses=courses, tag_entry_id=tag_entry_id, search=search)
