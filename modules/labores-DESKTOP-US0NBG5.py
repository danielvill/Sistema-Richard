class Labores:
    def __init__(self,empleado,fecha,descripcion):
        self.empleado = empleado
        self.fecha = fecha
        self.descripcion = descripcion
        
    def laboDBCollection(self):
        return{
            'empleado':self.empleado,
            'fecha':self.fecha,
            'descripcion':self.descripcion
            
        }