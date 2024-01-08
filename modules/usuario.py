class Usuario:
    def __init__(self,usuario,cedula,correo,password):
        self.usuario = usuario
        self.cedula = cedula
        self.correo = correo
        self.password = password
        
    def usuDBCollection(self):
        return{
            'usuario':self.usuario,
            'cedula':self.cedula,
            'correo':self.correo,
            'password':self.password
            
        }