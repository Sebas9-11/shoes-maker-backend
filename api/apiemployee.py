from config.db import db
from flask import Blueprint, jsonify, request
from models.employee import Employee, EmployeeSchema

employee_route = Blueprint('employee_route', __name__)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Ruta para obtener todos los empleados
@employee_route.route('/employees', methods=['GET'])
def get_all_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)

# Ruta para obtener un empleado por su id
@employee_route.route('/employees/<id>', methods=['GET'])
def get_employee_by_id(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)

# Ruta para crear un empleado
@employee_route.route('/employees', methods=['POST'])
def create_employee():
    try:
        rol_id = request.json['rol_id']
        name = request.json['name']
        last_name = request.json['last_name']
        status = request.json.get('status', None)

        new_employee = Employee(rol_id=rol_id, name=name, last_name=last_name, status=status)
        db.session.add(new_employee)
        db.session.commit()

        return employee_schema.jsonify(new_employee)
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e.args[0]}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar un empleado
@employee_route.route('/employees/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    rol_id = request.json['rol_id']
    name = request.json['name']
    last_name = request.json['last_name']
    status = request.json['status']

    employee.rol_id = rol_id
    employee.name = name
    employee.last_name = last_name
    employee.status = status

    db.session.commit()

    return employee_schema.jsonify(employee)

# Ruta para eliminar un empleado
@employee_route.route('/employees/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)

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


