from flask import Blueprint, request, jsonify
# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.insumos.base_costos_insumos_almacen import Base_CostosInsumosAlmacenService
from src.schemas.base_costos_insumos_almacen import BaseCostosInsumosAlmacenSchema


main = Blueprint('base_costos_insumos_almacen_blueprint', __name__)

# Función auxiliar para estandarizar las respuestas
def create_response(data=None, message="SUCCESS", success=True, status_code=200):
    return jsonify({'Data': data, 'message': message, 'success': success}), status_code

@main.route('/<int:id_insumo>', methods=['GET'])
def get_base_costos_insumos_almacen(id_insumo):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            costos_insumos_almacen = Base_CostosInsumosAlmacenService.get_Catalogo_InsumosAlmacen(id_insumo)
            
            if costos_insumos_almacen:
                return create_response(data=costos_insumos_almacen)
            else:
                return create_response(message="NOTFOUND", success=False, status_code=404)
        
        except Exception as ex:
            Logger.add_to_log("er:", f"Error in GET /<id_insumo>: {str(ex)}")
            #print(ex)
            return create_response(message="ERROR", success=False, status_code=500)
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@main.route('/', methods=['POST'])
def post_insert_base_costos_insumos_almacen():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            data = request.json
            #print(data, "data") 
            errors = BaseCostosInsumosAlmacenSchema.validate(data)
            
            if errors:
                Logger.add_to_log("er:", f"Validation errors: {errors}")
                return create_response(data=errors, message="Validation Error", success=False, status_code=400)

            evento = Base_CostosInsumosAlmacenService.insert_base_costos_insumos_almacen(data)
            
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

@main.route('/<int:id_base_costos_insumos_almacen>', methods=['PUT'])
def update_costos_insumos_almacen(id_base_costos_insumos_almacen):    
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            insumos_data = request.json
            if Base_CostosInsumosAlmacenService.update_costos_insumos_almacen_cantidad(insumos_data.cantidad, id_base_costos_insumos_almacen):
                return jsonify({"message": "Evento actualizado correctamente"}), 200
            else:
                return jsonify({"message": "Error al actualizar el evento"}), 500
        except Exception as ex:
            Logger.add_to_log(f"Error: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401