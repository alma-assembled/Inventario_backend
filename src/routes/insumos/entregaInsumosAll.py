from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
# Logger
from src.utils.Logger import Logger
# Services
from src.services.insumos.entregaInsumosAll import EntregaInsumos
# Security
from src.utils.Security import Security


main = Blueprint('entregaInsumoAll_blueprint', __name__)

# Función auxiliar para estandarizar las respuestas
def create_response(data=None, message="SUCCESS", success=True, status_code=200):
    return jsonify({'Data': data, 'message': message, 'success': success}), status_code

@main.route('/<int:id_tipo_invenventario>', methods=['GET'])
def get_entrega_insumos_all(id_tipo_invenventario):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            insumos_almacen = EntregaInsumos.get_entrega_insumos_all(id_tipo_invenventario)
            
            if insumos_almacen:
                return create_response(data=insumos_almacen)
            else:
                return create_response(message="NOTFOUND", success=False, status_code=404)
        
        except Exception as ex:
            Logger.add_to_log("er:", f"Error in GET /<id_insumo>: {str(ex)}")
            return create_response(message="ERROR", success=False, status_code=500)
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

