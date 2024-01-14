class Usuario:
    def __init__(self,id,usuario,cedula,correo,password):
        self.id = id
        self.usuario = usuario
        self.cedula = cedula
        self.correo = correo
        self.password = password
        
    def usuDBCollection(self):
        return{
            'id':self.id,
            'usuario':self.usuario,
            'cedula':self.cedula,
            'correo':self.correo,
            'password':self.password
            
        }