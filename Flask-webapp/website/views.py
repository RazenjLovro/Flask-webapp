from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required,current_user
from.models import Note, Hole, Project, Layer
from . import db
import json
from datetime import datetime



views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
            
    return render_template("home.html", user=current_user)


@views.route('/projects', methods=['GET', 'POST'])
@login_required
def project(): 
    projects = Project.query.filter_by(user_id=current_user.id).all()  
    if request.method == 'POST':
        projectid = request.form.get('projectid')
        projectname = request.form.get('projectname')
        location = request.form.get('location')
        
        project = Project.query.filter_by(projectid=projectid).first()
        if project:
            flash('Project already exist.', category='error')
        elif len(projectid) < 1:
            flash('Project ID must be greater than 1 character', category='error')
        elif len(projectname) < 1:
            flash('Project name must be greater than 1 character', category='error')
        elif len(location) < 4:
            flash('Location must be greater than 4 characters', category='error')
        else:
            new_project = Project(projectid=projectid, projectname=projectname, location=location, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit() 
            projects.append(new_project)
            flash('Project added', category='success')
        
        
    return render_template("project.html", user=current_user, projects=projects)


@views.route('/projects/<int:project_id>/holes', methods=['GET', 'POST'])
@login_required
def hole(project_id):
    project = Project.query.get(project_id)
    if not project or project.user_id != current_user.id:
        flash('Project does not exist or is not accessible', category='error')
        return redirect(url_for('views.projects'))
    
    holes = Hole.query.filter_by(project_id=project_id).all()
    if request.method == 'POST':
        holeid = request.form.get('holeid')
        xcoordinate = request.form.get('xcoordinate')
        ycoordinate = request.form.get('ycoordinate')
        elevation = request.form.get('elevation')
        depth = request.form.get('depth')
        hole = Hole.query.filter_by(holeid=holeid, project_id=project_id).all()
        if hole:
            flash('Hole already exist', category='error')
        elif len(holeid) < 1:
            flash('Hole ID must be greater than 1 character', category='error' )
        elif len(xcoordinate) < 1:
            flash('X Coordinate must be greater than 1 character', category='error')
        elif len(ycoordinate) < 1:
            flash('Y Coordinate must be greater than 1 character', category='error')
        elif len(elevation) < 1:
            flash('Elevation must be greater than 1 character', category='error')
        elif len(depth) < 1:
            flash('Depth must be greater than 1 character', category='error')
        else:
            new_hole = Hole(holeid=holeid, xcoordinate=xcoordinate, ycoordinate=ycoordinate, elevation=elevation, depth=depth, project_id=project_id, user_id=current_user.id)
            db.session.add(new_hole)
            db.session.commit()
            holes.append(new_hole)
            flash('Hole is added', category='success')
    
    return render_template("project.html", user=current_user, project=project, holes=holes, hole=hole)

@views.route('/projects/<int:project_id>/holes/<int:hole_id>/layers', methods=['GET', 'POST'])
@login_required
def layer(hole_id, project_id):
    hole = Hole.query.get(hole_id)
    if not hole:
        flash('Hole does not exists', category='error')
        return redirect(url_for('views.projects'))
    
    layers = Layer.query.filter_by(hole_id=hole_id, project_id=project_id).all()
    if request.method == 'POST':
        layernum = request.form.get('layernum')
        layertop = request.form.get('layertop')
        layerbottom = request.form.get('layerbottom')
        layerdescription = request.form.get('layerdescription')
        layersign = request.form.get('layersign')
        layer = Layer.query.filter_by(layernum=layernum, hole_id=hole_id).all()
        if layer:
            flash('Layer already exists', category='error')
        elif len(layertop) < 1:
            flash('Layer top must be greater than 1 character', category='error')
        elif len(layerbottom) < 1:
            flash('Layer bottom must be greater than 1 character', category='error')
        elif len(layerdescription) < 1:
            flash('Layer Description must be greater than 1 character', category='error')
        elif len(layersign) < 1:
            flash('Layer sign must be greater than 1 character', category='error')
        else:
            new_layer = Layer(layernum=layernum, layertop=layertop, layerbottom=layerbottom, layerdescription=layerdescription, layersign=layersign, hole_id=hole_id, project_id=project_id, user_id=current_user.id)
            db.session.add(new_layer)
            db.session.commit()
            layers.append(new_layer)
            flash('Layer has been added', category='success')
    
    return render_template("project.html", user=current_user, hole=hole, layers=layers)
              
    

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

@views.route('/delete-project', methods=['POST'])
def delete_project():
    project = json.loads(request.data)
    projectId = project['projectId']
    project = Project.query.get(projectId)
    if project:
        if project.user_id == current_user.id:
            db.session.delete(project)
            db.session.commit()
            
    return jsonify({})

@views.route('/delete-hole', methods=['POST'])
def delete_hole():
    hole = json.loads(request.data)
    holeId = hole['holeId']
    hole = Hole.query.get(holeId)
    if hole:
            db.session.delete(hole)
            db.session.commit()
            
    return jsonify({})

@views.route('/delete-layer', methods=['POST'])
def delete_layer():
    layer = json.loads(request.data)
    layerId = layer['layerId']
    layer = Layer.query.get(layerId)
    if layer:
            db.session.delete(layer)
            db.session.commit()
            
    return jsonify({})