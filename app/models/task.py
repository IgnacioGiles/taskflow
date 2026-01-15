# app/models/task.py
"""
Modelo de Tarea
Define la estructura y comportamiento de las tareas en el sistema
"""

class Task:
    """
    Representa una tarea en el sistema TaskFlow
    
    Attributes:
        id (int): Identificador único de la tarea
        titulo (str): Título de la tarea
        descripcion (str): Descripción detallada
        completada (bool): Estado de completitud
        prioridad (str): Nivel de prioridad (alta, media, baja)
        usuario_id (int): ID del usuario asignado
    """
    
    # Prioridades válidas
    PRIORIDADES_VALIDAS = ['alta', 'media', 'baja']
    
    def __init__(self, id, titulo, descripcion='', completada=False, 
                 prioridad='media', usuario_id=None):
        """
        Inicializa una nueva tarea
        
        Args:
            id: ID único de la tarea
            titulo: Título de la tarea
            descripcion: Descripción detallada (opcional)
            completada: Estado de completitud (default: False)
            prioridad: Nivel de prioridad (default: 'media')
            usuario_id: ID del usuario asignado (opcional)
        """
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.completada = completada
        self.prioridad = prioridad.lower()
        self.usuario_id = usuario_id
    
    def to_dict(self):
        """
        Convierte la tarea a un diccionario para serialización JSON
        
        Returns:
            dict: Diccionario con los datos de la tarea
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'completada': self.completada,
            'prioridad': self.prioridad,
            'usuario_id': self.usuario_id
        }
    
    @staticmethod
    def from_dict(data, id=None):
        """
        Crea una tarea desde un diccionario
        
        Args:
            data: Diccionario con los datos de la tarea
            id: ID opcional de la tarea
            
        Returns:
            Task: Nueva instancia de Task
        """
        return Task(
            id=id or data.get('id'),
            titulo=data.get('titulo'),
            descripcion=data.get('descripcion', ''),
            completada=data.get('completada', False),
            prioridad=data.get('prioridad', 'media'),
            usuario_id=data.get('usuario_id')
        )
    
    def marcar_completada(self):
        """Marca la tarea como completada"""
        self.completada = True
    
    def marcar_pendiente(self):
        """Marca la tarea como pendiente"""
        self.completada = False
    
    def cambiar_prioridad(self, nueva_prioridad):
        """
        Cambia la prioridad de la tarea
        
        Args:
            nueva_prioridad: Nueva prioridad a asignar
            
        Returns:
            bool: True si el cambio fue exitoso, False si la prioridad es inválida
        """
        if nueva_prioridad.lower() in self.PRIORIDADES_VALIDAS:
            self.prioridad = nueva_prioridad.lower()
            return True
        return False
    
    def __repr__(self):
        """Representación en string de la tarea"""
        estado = "✓" if self.completada else "○"
        return f"Task(id={self.id}, titulo='{self.titulo}', {estado}, prioridad={self.prioridad})"
