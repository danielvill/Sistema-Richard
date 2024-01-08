class Asistencia:
    def __init__(self,usuario,dias):
        self.usuario = usuario
        self.dias = dias
        
    def asisDBCollection(self):
        return{
            'usuario':self.usuario,
            'dias':self.dias
            
        }