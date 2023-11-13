from config.db import db
from flask import Blueprint, jsonify, request
from models.product import Product, ProductSchema

products_route = Blueprint('products_route', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Ruta para obtener todos los productos
@products_route.route('/products', methods=['GET'])
def get_all_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Ruta para obtener un producto por su id
@products_route.route('/products/<id>', methods=['GET'])
def get_product_by_id(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Ruta para crear un producto
@products_route.route('/products', methods=['POST'])
def create_product():
    name = request.json['name']
    price = request.json['price']
    unit_payment = request.json['unit_payment']
    pay_packet = request.json['pay_packet']
    type = request.json['type']

    new_product = Product(name, price, unit_payment, pay_packet, type)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Ruta para actualizar un producto
@products_route.route('/products/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    price = request.json['price']
    unit_payment = request.json['unit_payment']
    pay_packet = request.json['pay_packet']
    type = request.json['type']

    product.name = name
    product.price = price
    product.unit_payment = unit_payment
    product.pay_packet = pay_packet
    product.type = type

    db.session.commit()

    return product_schema.jsonify(product)

# Ruta para eliminar un producto
@products_route.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)