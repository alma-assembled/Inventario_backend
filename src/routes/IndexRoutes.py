from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import traceback

# Logger
from src.utils.Logger import Logger
from flask_cors import cross_origin

main = Blueprint('index_blueprint', __name__)

@cross_origin
@main.route('/')
def index():
    try:
        Logger.add_to_log("info", "{} {}".format(request.method, request.path))
        return "Inventario Backend"
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

        response = jsonify({'message': "Internal Server Error", 'success': False})
        return response, 500