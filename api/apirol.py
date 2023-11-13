from config.db import db
from flask import Blueprint, jsonify, request
from models.rol import Rol, RolSchema

rol_route = Blueprint('rol_route', __name__)
rol_schema = RolSchema()
roles_schema = RolSchema(many=True)

# Ruta para obtener todos los roles
@rol_route.route('/roles', methods=['GET'])
def get_all_roles():
    all_roles = Rol.query.all()
    result = roles_schema.dump(all_roles)
    
    return jsonify(result)

# Ruta para obtener un rol por su id
@rol_route.route('/roles/<id>', methods=['GET'])
def get_rol_by_id(id):
    rol = Rol.query.get(id)

    return rol_schema.jsonify(rol)

# Ruta para crear un rol
@rol_route.route('/roles', methods=['POST'])
def create_rol():
    name = request.json['name']
    new_rol = Rol(name)
    db.session.add(new_rol)
    db.session.commit()

    return rol_schema.jsonify(new_rol)

# Ruta para actualizar un rol
@rol_route.route('/roles/<id>', methods=['PUT'])
def update_rol(id):
    rol = Rol.query.get(id)
    name = request.json['name']
    rol.name = name
    db.session.commit()

    return rol_schema.jsonify(rol)

# Ruta para eliminar un rol
@rol_route.route('/roles/<id>', methods=['DELETE'])
def delete_rol(id):
    rol = Rol.query.get(id)
    db.session.delete(rol)
    db.session.commit()

    return rol_schema.jsonify(rol)

