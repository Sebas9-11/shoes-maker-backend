from config.db import db
from flask import Blueprint, jsonify, request
from models.employee import Employee, EmployeeSchema
import json


employee_route = Blueprint('employee_route', __name__)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Ruta para obtener todos los empleados
@employee_route.route('/employees', methods=['GET'])
def get_all_employees():
    result = db.session.execute("""SELECT employee.employee_id,
                                 employee.name,
                                 employee.last_name,
                                 rol.name AS rol_name,
                                 rol.rol_id,
                                 employee.status
                                 FROM employee JOIN rol ON rol.rol_id = employee.rol_id""")
    
    resultall = result.fetchall()

    all_employees = []

    for employee in resultall:
        json = {
            "employee_id": employee[0],
            "name": employee[1],
            "last_name": employee[2],
            "rol_name": employee[3],
            "rol_id": employee[4],
            "status": employee[5]
        }


# Ruta para obtener un empleado por su id
@employee_route.route('/employees/<id>', methods=['GET'])
def get_employee_by_id(id):
    
    result = db.session.execute("""SELECT employee.employee_id,
                                 employee.name,
                                 employee.last_name,
                                 rol.name AS rol_name,
                                 rol.rol_id,
                                 employee.status
                                 FROM employee JOIN rol ON rol.rol_id = employee.rol_id
                                 WHERE employee.employee_id = :rol_id""", {'rol_id': id})
    
    return jsonify(json)

# Ruta para crear un empleado n
@employee_route.route('/employees', methods=['POST'])
def create_employee():
    json_data = request.json
    errs = employee_schema.validate(json_data)

    if errs:
        return {"Error": errs}, 422
    
    result = Employee(json_data['employee_id'], json_data['rol_id'], json_data['name'], json_data['last_name'])
    db.session.add(result)
    db.session.commit()
    return employee_schema.jsonify(result)

# Ruta para actualizar un empleado
@employee_route.route('/employees/<id>', methods=['PUT'])
def update_employee(employee_id):
    json_data = request.json

    result = Employee.query.get(employee_id)
    result.employee_id = json_data['employee_id']
    result.rol_id = json_data['rol_id']
    result.name = json_data['name']
    result.last_name = json_data['last_name']
    result.status = json_data['status']

    db.session.commit()
    return employee_schema.jsonify(result)

# Ruta para eliminar un empleado
@employee_route.route('/employees/<id>', methods=['DELETE'])
def delete_employee(employee_id):

    result = Employee.query.get(employee_id)
    result.status = False
    db.session.commit()
    return employee_schema.jsonify(result)

# Ruta para obtener todos los empleados activos
@employee_route.route('/employees/active', methods=['GET'])
def get_all_active_employees():
    all_employees = Employee.query.filter_by(status=1)
    result = employees_schema.dump(all_employees)
    return jsonify(result)

# Ruta para obtener todos los empleados inactivos
@employee_route.route('/employees/inactive', methods=['GET'])
def get_all_inactive_employees():
    all_employees = Employee.query.filter_by(status=0)
    result = employees_schema.dump(all_employees)
    return jsonify(result)


