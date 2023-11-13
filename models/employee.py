from config.db import app, db, ma

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer)
    name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    status = db.Column(db.SmallInteger)

    def __init__(self, employee_id, rol_id, name, last_name, status):
        self.employee_id = employee_id
        self.rol_id = rol_id
        self.name = name
        self.last_name = last_name
        self.status = status
    
with app.app_context():
    db.create_all()

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'rol_id', 'name', 'last_name', 'status')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)