# app/models/__init__.py
"""
Módulo de modelos
Exporta todos los modelos de datos del sistema
"""

from .user import User
from .task import Task

__all__ = ['User', 'Task']
