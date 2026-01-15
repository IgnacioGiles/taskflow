# app/routes/__init__.py
"""
Módulo de rutas (Blueprints)
Endpoints de la API
"""

from .users import users_bp
from .tasks import tasks_bp

__all__ = ['users_bp', 'tasks_bp']
