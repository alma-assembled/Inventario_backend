from marshmallow import Schema, fields, post_load

class BaseInsumosProduccionSchema(Schema):
    id_binsumoproduccion = fields.Int(required=False) 
    fecha = fields.Date(required=True) 
    cantidad = fields.Decimal(required=True)
    costo = fields.Float(required=True)  
    id_bop = fields.Int(required=True) 
    id_bcostoinsumo = fields.Int(required=False)

    @post_load
    def make_base_insumos_produccion(self, data, **kwargs):
        from src.models.base_insumos_produccion import BaseInsumosProduccion
        return BaseInsumosProduccion(**data)

# Instancias del esquema
base_insumos_produccion_schema = BaseInsumosProduccionSchema()
base_insumos_produccion_schema_many = BaseInsumosProduccionSchema(many=True)
