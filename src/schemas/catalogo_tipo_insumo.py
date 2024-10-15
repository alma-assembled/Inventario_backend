from marshmallow import Schema, fields, post_load

class CatalogoTipoInsumoSchema(Schema):
    id_tipo_inventario = fields.Int(required=True)
    descripcion = fields.Str(required=True)
    id_rhcdepartamento = fields.Int(required=True)

    @post_load
    def make_catalogo_tipo_insumo(self, data, **kwargs):
        from src.models.catalogo_tipo_insumo import CatalogoTipoInsumo  
        return CatalogoTipoInsumo(**data)

# Instancias del esquema
catalogo_tipo_insumo_schema = CatalogoTipoInsumoSchema()              
catalogo_tipo_insumo_schema_many = CatalogoTipoInsumoSchema(many=True)  
