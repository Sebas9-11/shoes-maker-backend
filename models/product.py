from config.db import app, db, ma
from marshmallow import fields, ValidationError
from ..validations.validation import validate_str, validate_int, validate_float
from sqlalchemy import text

class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    price = db.Column(db.Float)
    unit_payment = db.Column(db.Float)
    pay_packet = db.Column(db.Float)
    type = db.Column(db.String(45))

    def __init__(self, name, price, unit_payment, pay_packet, type):
        self.name = name
        self.price = price
        self.unit_payment = unit_payment
        self.pay_packet = pay_packet
        self.type = type

with app.app_context():
    db.create_all()

def product_validation(val):

    val =  val.lower()
    raw_query = text("SELECT EXISTS(SELECT 1 FROM product WHERE LOWER(name) = :name)")
    params = {'name': val}

    product_existing = db.session.execute(raw_query, params)
    row = product_existing.fetchone()

    if row[0] == 1:
        raise ValidationError('Product already exists')
    
def product_validation_id(val):
    raw_query = text("SELECT EXISTS(SELECT 1 FROM product WHERE product_id = :product_id)")
    params = {'product_id': val}

    product_existing = db.session.execute(raw_query, params)
    row = product_existing.fetchone()

    if row[0] == 0:
        raise ValidationError('Product does not exist')

def type_validation(val):
    val =  val.lower()
    if val !=  'cortador' and val != 'guarnecedor' and val != 'ensamblador':
        raise ValidationError('Type must be valid')

class ProductSchema(ma.Schema):
    product_id = fields.Integer(required=True)
    name = fields.Str(required=True, allow_none=False, validate=[validate_str,product_validation])
    price = fields.Float(required=True, allow_nan=False, validate= validate_float)
    unit_payment = fields.Float(required=True, allow_nan=False, validate= validate_float)
    pay_packet = fields.Float(required=True, allow_nan=False, validate= validate_float)
    type = fields.Str(required=True, allow_none=False, validate=[validate_str, type_validation])

    class Meta:
        fields = ('product_id', 'name', 'price', 'unit_payment', 'pay_packet', 'type')

# product_schema = ProductSchema()
# products_schema = ProductSchema(many=True)
# haz las querys - ignora esto jaujaja 