class Reporte:
    def __init__(self,usuario,venta):
        self.usuario = usuario
        self.venta = venta
        
        
    def repoDBCollection(self):
        return{
            'usuario':self.usuario,
            'venta':self.venta
            
        }