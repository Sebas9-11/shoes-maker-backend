from flask import Blueprint, jsonify, request
from config.db import db
from ..models.production import Production, ProductionSchema
from ..models.production_employee import EmployeeProduction, EmployeeProductionSchema
from sqlalchemy import text

production_route = Blueprint('production_route', __name__)
production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)

#get 
@production_route.route('/productions', methods=['GET'])
@production_route.route('/productions/<int:id>', methods=['GET'])

def get_all_productions(employeeId=None):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if employeeId ==None:
        result_all = EmployeeProduction.Total(start_date, end_date)
        return jsonify(result_all)
    
    result_all = EmployeeProduction.by_employee(employeeId, start_date, end_date)
    return jsonify(result_all)

#get all production
@production_route.route('/productions/total', methods=['GET'])

def total_production():
    result = db.session.execute(text(""" SELECT
                                         production.id,
                                         employee.name,
                                         employee.last_name,
                                         rol.name AS rol_name,
                                         production.quantity,
                                         production.date,
                                         production.productId,
                                         production.employeeId,
                                         product.name AS product_name
                                         
                                         FROM production 
                                         JOIN product ON product.product_id = production.productId
                                         JOIN employee ON employee.employee_id = production.employeeId
                                         JOIN rol ON rol.rol_id = employee.rol_id """))
    
    resultall = result.fetchall()

    json = []

    for production in resultall:
        new = {
            "id": production[0],
            "name": production[1],
            "last_name": production[2],
            "rol_name": production[3],
            "quantity": production[4],
            "date": production[5],
            "productId": production[6],
            "employeeId": production[7],
            "product_name": production[8]
        }
        json.append(new)
    
    return jsonify(json)

#get production by employee
@production_route.route('/productions/totañ/<int:id>', methods=['GET'])

def total_production_by_employee(id):
    
    result = db.session.execute(text(""" SELECT production.id,
                                     employee.name AS first_name, 
                                     employee.last_name,
                                     rol.name AS rol_name,
                                     production.quantity,
                                     production.date,
                                     production.productId,
                                     production.employeeId,
                                     product.name AS product_name
                                     
                                     FROM production
                                     JOIN product ON product.product_id = production.productId
                                     JOIN employee ON employee.employee_id = production.employeeId
                                     JOIN rol ON rol.rol_id = employee.rol_id
                                     WHERE production.id = :employee_id """), {"employee_id": id})
    
    result = result.fetchall()

    json = {
        "id": result[0],
        "first_name": result[1],
        "last_name": result[2],
        "rol_name": result[3],
        "quantity": result[4],
        "date": result[5],
        "productId": result[6],
        "employeeId": result[7],
        "product_name": result[8]
    }

    return jsonify(json)

    
#post production
@production_route.route('/productions', methods=['POST'])
def create_production():
    json_data = request.json
    errs = production_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Production(json_data['employeeId'], json_data['productId'], json_data['quantity'], json_data['date'])
    db.session.add(result)
    db.session.commit()
    return production_schema.jsonify(result)

#put production
@production_route.route('/productions/<int:id>', methods=['PUT'])
def update_production(id):
    json_data = request.json
    errs = production_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Production.query.get(id)
    result.employeeId = json_data['employeeId']
    result.productId = json_data['productId']
    result.quantity = json_data['quantity']
    result.date = json_data['date']

    db.session.commit()
    return production_schema.jsonify(result)

#delete production
@production_route.route('/productions/<int:id>', methods=['DELETE'])
def delete_production(id):
    result = Production.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return production_schema.jsonify(result)


