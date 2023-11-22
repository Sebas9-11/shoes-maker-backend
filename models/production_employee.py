from config.db import db,ma
from sqlalchemy import text
from marshmallow import fields

class EmployeeProduction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_mname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    unit_payment = db.Column(db.Float)
    pay_packet = db.Column(db.Float)
    total_quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    role_name = db.Column(db.String(50))

    def __init__(self, first_name, last_mname, name, unit_payment, pay_packet, total_quantity, date, price, role_name):
        self.first_name = first_name
        self.last_mname = last_mname
        self.name = name
        self.unit_payment = unit_payment
        self.pay_packet = pay_packet
        self.total_quantity = total_quantity
        self.date = date
        self.price = price
        self.role_name = role_name

    def payment_calculation(production):
        new = {}

        package_price = 12 * production['price']

        package_compensation = 12 * production * (production['package'] / 100)

        new['compensation'] = package_compensation
        new['price'] = package_price
        new['name'] = production['name']
        new['unit_price'] = production['price']
        new['percentage'] = production['package']
        new['employee_name'] = production['first_name'] + ' ' + production['last_name']
        new['date'] = production['date']
        new['role_name'] = production['role_name']

        return new
    
    def unit_calculation(production,remaining):
        new = {}

        remaining_price = remaining * production['price']
        new['compensation'] = remaining_price * (production['unit'] / 100)
        new['price'] = remaining_price
        new['name'] = production['name']
        new['quantity'] = remaining
        new['unit_price'] = production['price']
        new['percentage'] = production['unit']
        new['employee_name'] = production['first_name'] + ' ' + production['last_name']
        new['date'] = production['date']
        new['role_name'] = production['role_name']

        return new
    
    def final_object_build(production, final_object, production_object):
        production['unit'] = float(production['unit'])
        production['package'] = float(production['package'])
        production['total_quantity'] = int(production['total_quantity'])
        production['date'] = str(production['date'])
        production['price'] = int(production['price'])

        if production['total_quantity'] >= 12:
            new = EmployeeProduction.payment_calculation(production)
            final_object.append(new)
            remaining = production['total_quantity'] % 12

            if remaining > 0:
                new = EmployeeProduction.unit_calculation(production, remaining)
                final_object.append(new)
        elif production['total_quantity'] ==12:
            new = EmployeeProduction.payment_calculation(production)
            final_object.append(new)
        else:
            remaining = production['total_quantity']
            new = EmployeeProduction.unit_calculation(production, remaining)
            final_object.append(new)
        
        production_object['production'] = final_object
    
    def by_employee(employee_id, start_date, end_date):
        if start_date == None:
            start_date = '1900-01-01'
        
        if end_date == None:
            end_date = '2100-01-01'
        
        result = db.session.execute(text('''SELECT SUM(production.quantity) AS total_quantity,
                                            employee.name AS first_name, 
                                            employee.last_name, 
                                            production.date, 
                                            product.name,
                                            product.unit_payment, 
                                            product.pay_packet, 
                                            product.price, MAX(rol.name) AS role_name
                                            FROM production 
                                            JOIN product ON product.product_id = production.productId
                                            JOIN employee ON employee.employee_id = production.employeeId 
                                            JOIN rol ON rol.id = employee.rol_id
                                            WHERE employee.employee_id = :employeeId AND production.date BETWEEN :start_date AND :end_date
                                            GROUP BY employee.first_name, employee.last_name, production.date, product.name, product.product_id;'''), {'employeeId': employee_id,
                                            'start_date': start_date, 'end_date': end_date})
        
        schema = EmployeeProductionSchema(many=True)
        total_production = schema.dump(result)
        employee_production_object = {}

        package_object = []

        for production in total_production:
            production['unit'] = float(production['unit'])
            production['package'] = float(production['package'])
            production['total_quantity'] = int(production['total_quantity'])
            production['date'] = str(production['date'])
            production['price'] = int(production['price'])

            EmployeeProduction.final_object_build(production, package_object, employee_production_object)
            employee_production_object['total_compensation'] = sum([x['compensation'] for x in package_object])

        return employee_production_object
    
    def Total(start_date, end_date):
        if start_date == None:
            start_date = '1900-01-01'
        
        if end_date == None:
            end_date = '2100-01-01'
        

        result = db.session.execute(text('''SELECT SUM(production.quantity) AS total_quantity,
                                         employee.name AS first_name,
                                         employee.last_name,
                                         production.date,
                                         product.name,
                                         product.unit_payment,
                                         product.pay_packet,
                                         product.price,
                                         rol.name AS role_name

                                         FROM production
                                         JOIN product ON product.product_id = production.productId
                                         JOIN employee ON employee.employee_id = production.employeeId
                                         JOIN rol ON rol.rol_id = employee.rol_id
                                         WHERE production.date BETWEEN :start_date AND :end_date

                                         GROUP BY employee.first_name, employee.last_name, production.date, product.name, product.product_id, rol.name;'''), {'start_date': start_date, 'end_date': end_date})
        
        schema = EmployeeProductionSchema(many=True)
        total_production = schema.dump(result)
        production_object = {}
        package_object = []

        for production in total_production:
            EmployeeProduction.final_object_build(production, package_object, production_object)
        
        return production_object
 


class EmployeeProductionSchema(ma.Schema):
    id = fields.Integer(allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    name = fields.Str(required=True, allow_none=False)
    unit_payment = fields.Float(required=True, allow_nan=False)
    pay_packet = fields.Float(required=True, allow_nan=False)
    total_quantity = fields.Integer(required=True, allow_nan=False)
    date = fields.DateTime(required=True, allow_none=False)
    price = fields.Float(required=True, allow_nan=False)
    role_name = fields.Str(required=True, allow_none=False)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'name', 'unit_payment', 'pay_packet', 'total_quantity', 'date', 'price', 'role_name')