from config.db import app, db, ma

class Rol(db.Model):
  rol_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(45))

  def __init__(self, name):
    self.name = name

with app.app_context():
  db.create_all()

class RolSchema(ma.Schema):
  class Meta:
    fields = ('rol_id', 'name')

rol_schema = RolSchema()
roles_schema = RolSchema(many=True)