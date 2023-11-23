from config.db import app, db, ma
from marshmallow import fields, ValidationError
from sqlalchemy import text
from ..validations.validation import validate_str

class Rol(db.Model):
  __tablename__ = 'rol'
  rol_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(45))

  def __init__(self, name):
    self.name = name

with app.app_context():
  db.create_all()

def name_validator(val):
  val = val.lower()
  raw_query = text("SELECT EXISTS(SELECT 1 FROM rol WHERE name = :name)")
  params = {'name': val}

  rol_exist = db.session.execute(raw_query, params)
  row = rol_exist.fetchone()

  if row[0] == 1:
    raise ValidationError('Rol already exists.')
  

class RolSchema(ma.Schema):
  rol_id = fields.Integer(allow_none=True)
  name = fields.Str(required=True, allow_none= False, validate=[name_validator, validate_str])

  class Meta:
    fields = ('rol_id', 'name')

# rol_schema = RolSchema()
# roles_schema = RolSchema(many=True)