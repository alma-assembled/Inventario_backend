from marshmallow import Schema, fields, post_load

class BaseCostosInsumosAlmacenSchema(Schema):
    id_bcostoinsumo = fields.Int(required=False)   
    fecha = fields.Date(required=True)            
    costo_unidad = fields.Float(required=True) 
    cantidad_almacen = fields.Decimal(required=True) 
    cantidad_inventario = fields.Decimal(required=True) 
    uuid = fields.Str(required=False) 
    id_cinsumoalmacen = fields.Int(required=True) 
    id_bfacturacxp = fields.Int(required=False)

    @post_load
    def make_base_costos_insumos_almacen(self, data, **kwargs):
        from src.models.base_costos_insumos_almacen  import BaseCostosInsumosAlmacen
        return BaseCostosInsumosAlmacen(**data)

# Instancias del esquema
base_costos_insumos_almacen_schema = BaseCostosInsumosAlmacenSchema()
base_costos_insumos_almacen_schema_many = BaseCostosInsumosAlmacenSchema(many=True)
