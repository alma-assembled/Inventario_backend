from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
# Routes
from .routes import  IndexRoutes, AuthRoutes
from .routes.insumos import  base_costos_insumos_almacenRoutes, base_InsumosProduccionRoutes
from .routes.insumos import  catalogo_insumos_almacenRoutes, entregaInsumosAll, inventiarioInsumosAllRoutes

app = Flask(__name__)

# Configuración de Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # Incluir todas las rutas
            "model_filter": lambda tag: True,  # Incluir todos los modelos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,  # Habilita la interfaz Swagger UI
    "specs_route": "/apidocs/"  # Ruta donde estará la documentación
}

swagger = Swagger(app,swagger_config)
#CORS(app, resources={r"/empleados/*": {"origins": "http://localhost:3000"}})
CORS(app)
def init_app(config):
    # Configuration
    app.config.from_object(config)
    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(catalogo_insumos_almacenRoutes.main, url_prefix='/insumos_almacen')
    app.register_blueprint(base_costos_insumos_almacenRoutes.main, url_prefix='/costos_insumos_almacen')
    app.register_blueprint(base_InsumosProduccionRoutes.main, url_prefix='/insumos_produccion')
    app.register_blueprint(inventiarioInsumosAllRoutes.main, url_prefix='/inventiario_insumos')
    app.register_blueprint(entregaInsumosAll.main, url_prefix='/entregas_insumos')
    app.run(host='0.0.0.0', port=5002, debug=True)
    return app