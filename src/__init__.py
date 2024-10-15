from flask import Flask
from flask_cors import CORS

# Routes
from .routes import  IndexRoutes

app = Flask(__name__)
#CORS(app, resources={r"/empleados/*": {"origins": "http://localhost:3000"}})
CORS(app)
def init_app(config):
    # Configuration
    app.config.from_object(config)
    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.run(host='0.0.0.0', port=5002, debug=True)
    return app