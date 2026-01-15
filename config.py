# config.py
"""
Configuración de la aplicación TaskFlow
Este archivo centraliza todas las configuraciones del proyecto
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Configuración base de la aplicación"""
    
    # Configuración del servidor
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'
    
    # Configuración de CORS
    CORS_ORIGINS = '*'  # En producción, especificar dominios permitidos
    
    # Configuración de la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
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
    # Configuración CORS para producción (más restrictiva)
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000')


# Diccionario de configuración
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}