from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectid = db.Column(db.String(50), unique=True, nullable=False)
    projectname = db.Column(db.String(200))
    location = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    holes = db.relationship('Hole', backref='project')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    layers = db.relationship('Layer', backref='project')

class Hole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    holeid = db.Column(db.String(50))
    xcoordinate = db.Column(db.Float, nullable=False)
    ycoordinate = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)
    depth = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    layers = db.relationship('Layer', backref='hole')
    
class Layer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    layernum = db.Column(db.Float(100), nullable=False)
    layersign = db.Column(db.String(10), nullable=False)
    layertop = db.Column(db.Float(50), nullable=False)
    layerbottom = db.Column(db.Float(50), nullable=False)
    layerdescription = db.Column(db.String(1000), nullable=False)
    hole_id = db.Column(db.Integer, db.ForeignKey('hole.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    projects = db.relationship('Project')
    holes = db.relationship('Hole')
    layers = db.relationship('Layer')