# app/__init__.py
"""
Factory de la aplicación Flask
Crea y configura la aplicación con todos sus componentes
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config import config


def create_app(config_name='default'):
    """
    Factory pattern para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar ('development', 'production')
    
    Returns:
        Flask: Instancia configurada de la aplicación
    """
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Habilitar CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))
    
    # Registrar Blueprints
    registrar_blueprints(app)
    
    # Registrar manejadores de errores
    registrar_error_handlers(app)
    
    # Ruta de salud (health check)
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Endpoint para verificar que el servidor está funcionando"""
        return jsonify({
            'status': 'ok',
            'message': 'TaskFlow API v2.0 - MVC Architecture'
        }), 200
    
    return app


def registrar_blueprints(app):
    """
    Registra todos los Blueprints de la aplicación
    
    Args:
        app: Instancia de Flask
    """
    from app.routes import users_bp, tasks_bp
    
    # Registrar Blueprints con prefijo /api
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(tasks_bp, url_prefix='/api')
    
    print("✓ Blueprints registrados:")
    print("  - users_bp en /api/users")
    print("  - tasks_bp en /api/tasks")


def registrar_error_handlers(app):
    """
    Registra manejadores de errores globales
    
    Args:
        app: Instancia de Flask
    """
    
    @app.errorhandler(404)
    def not_found(error):
        """Maneja rutas no encontradas"""
        return jsonify({
            'error': 'Endpoint no encontrado',
            'mensaje': 'La ruta solicitada no existe'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores internos del servidor"""
        return jsonify({
            'error': 'Error interno del servidor',
            'mensaje': 'Ha ocurrido un error inesperado'
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Maneja peticiones mal formadas"""
        return jsonify({
            'error': 'Petición incorrecta',
            'mensaje': 'Los datos enviados no son válidos'
        }), 400
    
    print("✓ Manejadores de errores registrados")
