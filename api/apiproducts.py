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
@products_route.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    return product_schema.jsonify(product)

# Ruta para crear un producto
@products_route.route('/products', methods=['POST'])
def create_product():
    product = request.json
    errs = product_schema.validate(product)

    if errs:
        return {"error": errs}, 422
    
    result = Product(product['name'], product['price'], product['unit_payment'], product['pay_packet'], product['type'])
    db.session.add(result)
    db.session.commit()
    return product_schema.jsonify(result)

# Ruta para actualizar un producto
@products_route.route('/products/<id>', methods=['PUT'])
def update_product(product_id):
    product = request.json
    errs = product_schema.validate(product)

    if errs:
        return {"error": errs}, 422
    
    result = Product.query.get(product_id)
    result.name = product['name']
    result.price = product['price']
    result.unit_payment = product['unit_payment']
    result.pay_packet = product['pay_packet']
    result.type = product['type']
    db.session.commit()
    return product_schema.jsonify(result)

# Ruta para eliminar un producto
@products_route.route('/products/<id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)