# config.py
"""
Configuración de la aplicación TaskFlow
Este archivo centraliza todas las configuraciones del proyecto
"""

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración del servidor
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'
    
    # Configuración de CORS
    CORS_ORIGINS = '*'  # En producción, especificar dominios permitidos
    
    # Configuración de la aplicación
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    @staticmethod
    def init_app(app):
        """Inicializa configuraciones adicionales"""
        pass


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    # En producción, SECRET_KEY debe venir de variable de entorno


# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
