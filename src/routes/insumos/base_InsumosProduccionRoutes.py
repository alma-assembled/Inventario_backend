from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
# Logger
from src.utils.Logger import Logger
# Services
from src.services.insumos.base_InsumosProduccion import Base_InsumosProduccionSevice
from src.schemas.base_insumos_produccion import BaseInsumosProduccionSchema
# Security
from src.utils.Security import Security

main = Blueprint('base_insumos_production_blueprint', __name__)

# Función auxiliar para estandarizar las respuestas
def create_response(data=None, message="SUCCESS", success=True, status_code=200):
    return jsonify({'Data': data, 'message': message, 'success': success}), status_code

@main.route('/', methods=['POST'])
def post_insert_base_insumos_produccion():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            data = request.json
            #print(data, "data") 
            errors = BaseInsumosProduccionSchema.validate(data)
            
            if errors:
                Logger.add_to_log("er:", f"Validation errors: {errors}")
                return create_response(data=errors, message="Validation Error", success=False, status_code=400)

            evento = Base_InsumosProduccionSevice.insert_base_insumos_produccion(data)
            
            if evento:
                return create_response(message="Resource created", success=True, status_code=201)
            else:
                return create_response(message="Error al guardar el evento", success=False, status_code=500)
        
        except Exception as ex:
            Logger.add_to_log("er:", f"Error in POST /: {str(ex)}")
            return create_response(message="ERROR", success=False, status_code=500)
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@main.route('/<int:id_base_insumos_produccion>', methods=['PUT'])
def update_base_insumo_produccion(id_base_insumos_produccion):    
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            insumos_data = request.json
            if Base_InsumosProduccionSevice.update_insumos_produccion_cantidad(insumos_data.cantidad, id_base_insumos_produccion):
                return jsonify({"message": "Evento actualizado correctamente"}), 200
            else:
                return jsonify({"message": "Error al actualizar el evento"}), 500
        except Exception as ex:
            Logger.add_to_log(f"Error: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401