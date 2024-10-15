class CatalogoTipoInsumo:
    def __init__(self, id_tipo_inventario=None, descripcion=None, id_rhcdepartamento=None):
        self.id_tipo_inventario = id_tipo_inventario
        self.descripcion = descripcion
        self.id_rhcdepartamento = id_rhcdepartamento

    def serialize(self):
        from src.schemas.catalogo_tipo_insumo import catalogo_tipo_insumo_schema
        return catalogo_tipo_insumo_schema.dump(self)

    def serializeall(self):
        return {
            'id_tipo_inventario': self.id_tipo_inventario,
            'descripcion': self.descripcion,
            'id_rhcdepartamento': self.id_rhcdepartamento
        }
