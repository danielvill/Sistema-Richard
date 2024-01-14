class Ventas:
    def __init__(self,vendedor,categoria, cantidad,fecha,venta):
        self.vendedor = vendedor
        self.categoria = categoria
        self.cantidad = cantidad
        self.fecha=fecha
        self.venta = venta

    def ventDBCollection(self):
        return{
            'vendedor':self.vendedor,
            'categoria':self.categoria,
            'cantidad':self.cantidad,
            'fecha':self.fecha,
            'venta':self.venta    
        }