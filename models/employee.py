from config.db import app, db, ma
from models.rol import Rol
from sqlalchemy import text
from marshmallow import fields, ValidationError
# from validations.validation import validate_str, validate_int

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer)
    name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    status = db.Column(db.Boolean)

    def __init__(self, employee_id, rol_id, name, last_name, status):
        self.employee_id = employee_id
        self.rol_id = rol_id
        self.name = name
        self.last_name = last_name
        self.status = status
    
with app.app_context():
    db.create_all()

def rol_validator(val):
    rol_existing = db.session.query(Rol).filter_by(rol_id=val).first()

    if rol_existing is None:
        raise ValidationError('Rol does not exist.')

def employee_id_validator(val):
    
    raw_query = text("SELECT EXISTS(SELECT 1 FROM employee WHERE employee_id = :employee_id)")
    params = {'employee_id': val}

    employee_existing = db.session.execute(raw_query, params)
    row = employee_existing.fetchone()

    if row[0] == 1:
        raise ValidationError('Employee already exists.')

def not_existing_validator(val):
    raw_query = text("SELECT EXISTS(SELECT 1 FROM employee WHERE employee_id = :employee_id)")
    params = {'employee_id': val}

    employee_existing = db.session.execute(raw_query, params)
    row = employee_existing.fetchone()

    if row[0] == 0:
        raise ValidationError('Employee does not exist.')



class EmployeeSchema(ma.Schema):
    employee_id = fields.Integer(required=True, allow_none=False, validate=[employee_id_validator, validate_int])
    rol_id = fields.Integer(required=True, allow_none=False, validate=[rol_validator, validate_int])
    name = fields.Str(required=True, allow_none=False, validate= validate_str)
    last_name = fields.Str(required=True, allow_none=False, validate= validate_str)
    status = fields.Boolean(allown_none=True, default=True)

    class Meta:
        fields = ('employee_id', 'rol_id', 'name', 'last_name', 'status')

# employee_schema = EmployeeSchema()
# employees_schema = EmployeeSchema(many=True)