from marshmallow import Schema, fields, post_load

class BaseInsumosProduccionSchema(Schema):
    id_binsumoproduccion = fields.Int(required=True) 
    fecha = fields.Date(required=True) 
    costo = fields.Float(required=True)  
    id_bop = fields.Int(required=True) 
    id_bcostoinsumo = fields.Int(required=True)

    @post_load
    def make_base_insumos_produccion(self, data, **kwargs):
        from src.models.base_insumos_produccion import BaseInsumosProduccion
        return BaseInsumosProduccion(**data)

# Instancias del esquema
base_insumos_produccion_schema = BaseInsumosProduccionSchema()
base_insumos_produccion_schema_many = BaseInsumosProduccionSchema(many=True)
