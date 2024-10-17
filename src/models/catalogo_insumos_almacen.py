class CatalogoInsumosAlmacenModel:
    def __init__(self, id_cinsumoalmacen=None, insumo=None, unidad_de_medida=None, id_tipo_inventario=None):
        self.id_cinsumoalmacen = id_cinsumoalmacen
        self.insumo = insumo
        self.unidad_de_medida = unidad_de_medida
        self.id_tipo_inventario = id_tipo_inventario

    def serialize(self):
        from src.schemas.catalogo_insumos_almacen import catalogo_insumos_almacen_schema
        return catalogo_insumos_almacen_schema.dump(self)

    def serializeall(self):
        return {
            'id_cinsumoalmacen': self.id_cinsumoalmacen,
            'insumo': self.insumo,
            'medida_unidad': self.medida_unidad,
            'id_tipo_inventario': self.id_tipo_inventario
        }
