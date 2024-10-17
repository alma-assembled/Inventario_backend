from marshmallow import Schema, fields, post_load

class CatalogoInsumosAlmacenSchema(Schema):
    id_cinsumoalmacen = fields.Int(required=False , allow_none=True)
    insumo = fields.Str(required=True)
    unidad_de_medida = fields.Str(required=True)
    id_tipo_inventario = fields.Int(required=True)

    @post_load
    def make_catalogo_insumos_almacen(self, data, **kwargs):
        from src.models.catalogo_insumos_almacen import CatalogoInsumosAlmacenModel
        return CatalogoInsumosAlmacenModel(**data)

# Instancias del esquema
catalogo_insumos_almacen_schema = CatalogoInsumosAlmacenSchema()
catalogo_insumos_almacen_schema_many = CatalogoInsumosAlmacenSchema(many=True)
