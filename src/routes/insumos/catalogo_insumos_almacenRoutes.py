from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.insumos.catalogo_insumos_almacen import Catalogo_InsumosAlmacenService
from src.schemas.catalogo_insumos_almacen import CatalogoInsumosAlmacenSchema

from src.services.insumos.catalogo_tipo_insumo import Catalogo_Tipo_Insumos

main = Blueprint('insumosAlmacen_blueprint', __name__)

# Función auxiliar para estandarizar las respuestas
def create_response(data=None, message="SUCCESS", success=True, status_code=200):
    return jsonify({'Data': data, 'message': message, 'success': success}), status_code

@main.route('/<int:id_insumo>', methods=['GET'])
def get_insumos_almacen(id_insumo):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            insumos_almacen = Catalogo_InsumosAlmacenService.get_Catalogo_InsumosAlmacen_by_Id(id_insumo)
            
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

@main.route('/', methods=['POST'])
def post_insert_insumos_almacen():
    try:
        data = request.json
        #print(data, "data") 
        errors = CatalogoInsumosAlmacenSchema.validate(data)
        
        if errors:
            Logger.add_to_log("er:", f"Validation errors: {errors}")
            return create_response(data=errors, message="Validation Error", success=False, status_code=400)

        evento = Catalogo_InsumosAlmacenService.save_Catalogo_InsumosAlmacen(data)
        
        if evento:
            return create_response(message="Resource created", success=True, status_code=201)
        else:
            return create_response(message="Error al guardar el evento", success=False, status_code=500)
    
    except Exception as ex:
        Logger.add_to_log("er:", f"Error in POST /: {str(ex)}")
        print(str(ex))
        return create_response(message="ERROR", success=False, status_code=500)


@main.route('/tipo_insumo/', methods=['GET'])
def get_tipo_insumos_almacen():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            insumos_almacen = Catalogo_Tipo_Insumos.get_catalogo_tipo_insumo()
            
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