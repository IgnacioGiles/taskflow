# app/services/__init__.py
"""
Módulo de servicios
Lógica de negocio de la aplicación
"""

from . import user_service
from . import task_service

__all__ = ['user_service', 'task_service']
