from config.db import app, db, ma
from .rol import Rol 
from sqlalchemy import text
from marshmallow import fields, ValidationError, validates_schema
from ..validations.validation import validate_str, validate_int, validate_float
from .product import product_validation_id
from .employee import not_existing_validator

class Production(db.Model):
    __tablename__ = 'production'
    id = db.Column(db.Integer, primary_key=True)
    employeeId = db.Column(db.Integer)
    productId = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, employeeId, productId, quantity, date):
        self.employeeId = employeeId
        self.productId = productId
        self.quantity = quantity
        self.date = date
    
    def ByEmployee(employeeId):
        result = db.session.execute(text(""" SELECT SUM(production.quantity) AS total_quantity,
                                         employee.name, employee.last_name, production.date,
                                         product.name AS product_name, product.unit_payment, product.pay_packet
                                         
                                         FROM production JOIN product ON product.product_id = production.productId
                                         JOIN employee ON employee.employee_id = production.employeeId
                                         WHERE employee.employee_id = :employeeId GROUP BY employee.name, employee.last_name, production.date, 
                                         product.name, product.product_id"""),{'employeeId': employeeId})
        
        return result
    
with app.app_context():
    db.create_all()

class ProductionSchema(ma.Schema):
   id = fields.Integer(allow_none=False)
   employeeId = fields.Integer(required=True, allow_none=False, validate=[not_existing_validator, validate_int])
   productId = fields.Integer(required=True, allow_none=False, validate=[product_validation_id, validate_int])
   quantity = fields.Integer(required=True, allow_none=False, validate=[validate_int])
   date = fields.DateTime(required=True, allow_none=False)

   class Meta:
       fields = ('id', 'employeeId', 'productId', 'quantity', 'date')
    
   @validates_schema(skip_on_field_errors=False)
   def product_employee_validation(self,data,**kwargs):
        employeeId = data.get('employeeId')
        productId = data.get('productId')

        raw_query = text("SELECT LOWER(type) FROM product WHERE id = :id")
        params = {'id': productId}
        product_existing = db.session.execute(raw_query, params)
        result1 = product_existing.fetchone()

        raw_query = text("SELECT LOWER(rol.name) FROM employee JOIN rol on rol.rol_id = employee.rol_id WHERE employee.id = :id")
        params = {'id': employeeId}
        employee_existing = db.session.execute(raw_query, params)
        result2 = employee_existing.fetchone()

        if result1[0] != result2[0]:
            raise ValidationError('Employee and product are not compatible.')