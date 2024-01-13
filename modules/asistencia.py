class Asistencia:
    def __init__(self,empleado,fecha,hora,comentario):
        self.empleado = empleado
        self.fecha = fecha
        self.hora = hora
        self.comentario = comentario
        
    def asisDBCollection(self):
        return{
            'empleado':self.empleado,
            'fecha':self.fecha,
            'hora':self.hora,
            'comentario':self.comentario
            
        }