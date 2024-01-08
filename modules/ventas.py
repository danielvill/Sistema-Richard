class Ventas:
    def __init__(self,usuario,cedula,correo,password):
        self.usuario = usuario
        self.cedula = cedula
        self.correo = correo
        self.password = password
        
    def ventDBCollection(self):
        return{
            'usuario':self.usuario,
            'cedula':self.cedula,
            'correo':self.correo,
            'password':self.password
            
        }