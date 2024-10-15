class BaseCostosInsumosAlmacen:
    def __init__(self, id_bcostoinsumo=None, fecha=None, costo_unidad=None, cantidad_almacen=None, 
                 cantidad_inventario=None, uuid=None, id_cinsumoalmacen=None, id_bfacturacxp=None):
        self.id_bcostoinsumo = id_bcostoinsumo
        self.fecha = fecha
        self.costo_unidad = costo_unidad
        self.cantidad_almacen = cantidad_almacen
        self.cantidad_inventario = cantidad_inventario
        self.uuid = uuid
        self.id_cinsumoalmacen = id_cinsumoalmacen
        self.id_bfacturacxp = id_bfacturacxp

    def serialize(self):
        from src.schemas.base_costos_insumos_almacen import base_costos_insumos_almacen_schema
        return base_costos_insumos_almacen_schema.dump(self)

    def serializeall(self):
        return {
            'id_bcostoinsumo': self.id_bcostoinsumo,
            'fecha': self.fecha,
            'costo_unidad': self.costo_unidad,
            'cantidad_almacen': self.cantidad_almacen,
            'cantidad_inventario': self.cantidad_inventario,
            'uuid': self.uuid,
            'id_cinsumoalmacen': self.id_cinsumoalmacen,
            'id_bfacturacxp': self.id_bfacturacxp
        }
