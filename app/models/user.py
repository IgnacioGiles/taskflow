# app/models/user.py
"""
Modelo de Usuario
Define la estructura y comportamiento de los usuarios en el sistema
"""

class User:
    """
    Representa un usuario del sistema TaskFlow
    
    Attributes:
        id (int): Identificador único del usuario
        nombre (str): Nombre completo del usuario
        email (str): Correo electrónico (único)
        rol (str): Rol del usuario (administrador, usuario)
    """
    
    def __init__(self, id, nombre, email, rol='usuario'):
        """
        Inicializa un nuevo usuario
        
        Args:
            id: ID único del usuario
            nombre: Nombre completo
            email: Correo electrónico
            rol: Rol del usuario (default: 'usuario')
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol
    
    def to_dict(self):
        """
        Convierte el usuario a un diccionario para serialización JSON
        
        Returns:
            dict: Diccionario con los datos del usuario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol
        }
    
    @staticmethod
    def from_dict(data, id=None):
        """
        Crea un usuario desde un diccionario
        
        Args:
            data: Diccionario con los datos del usuario
            id: ID opcional del usuario
            
        Returns:
            User: Nueva instancia de User
        """
        return User(
            id=id or data.get('id'),
            nombre=data.get('nombre'),
            email=data.get('email'),
            rol=data.get('rol', 'usuario')
        )
    
    def __repr__(self):
        """Representación en string del usuario"""
        return f"User(id={self.id}, nombre='{self.nombre}', email='{self.email}')"
