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
@rol_route.route('/roles/<int:id>', methods=['GET'])
def get_rol_by_id(rol_id):
    rol = Rol.query.get(rol_id)
    return rol_schema.jsonify(rol)

# Ruta para crear un rol
@rol_route.route('/roles', methods=['POST'])
def create_rol():
    rol = request.json
    errs = rol_schema.validate(rol)

    if errs:
        return {"error": errs}, 422
    
    result = Rol(rol['name'])
    db.session.add(result)
    db.session.commit()
    return rol_schema.jsonify(result)

# Ruta para actualizar un rol
@rol_route.route('/roles/<int:id>', methods=['PUT'])
def update_rol(rol_id):
    rol = request.json
    errs = rol_schema.validate(rol)

    if errs:
        return {"error": errs}, 422
    
    result = Rol.query.get(rol_id)
    result.name = rol['name']
    db.session.commit()
    return rol_schema.jsonify(result)


# Ruta para eliminar un rol
@rol_route.route('/roles/<int:id>', methods=['DELETE'])
def delete_rol(rol_id):
    rol = Rol.query.get(rol_id)
    db.session.delete(rol)
    db.session.commit()
    return rol_schema.jsonify(rol)

