class BaseInsumosProduccion:
    def __init__(self, id_binsumoproduccion=None, fecha=None, costo=None, id_bop=None, id_bcostoinsumo=None):
        self.id_binsumoproduccion = id_binsumoproduccion
        self.fecha = fecha
        self.costo = costo
        self.id_bop = id_bop
        self.id_bcostoinsumo = id_bcostoinsumo

    def serialize(self):
        from src.schemas.base_insumos_produccion import base_insumos_produccion_schema
        return base_insumos_produccion_schema.dump(self)

    def serializeall(self):
        return {
            'id_binsumoproduccion': self.id_binsumoproduccion,
            'fecha': self.fecha,
            'costo': self.costo,
            'id_bop': self.id_bop,
            'id_bcostoinsumo': self.id_bcostoinsumo
        }

