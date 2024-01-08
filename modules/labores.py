class Labores:
    def __init__(self,usuario,descripcion):
        self.usuario = usuario
        self.descripcion = descripcion
        
    def laboDBCollection(self):
        return{
            'usuario':self.usuario,
            'descripcion':self.descripcion
            
        }