from marshmallow import Schema, fields, post_load

class BaseCostosInsumosAlmacenSchema(Schema):
    id_bcostoinsumo = fields.Int(required=True)   # Campo entero obligatorio
    fecha = fields.Date(required=True)            # Campo de fecha obligatorio
    costo_unidad = fields.Float(required=True)    # Campo de costo por unidad (flotante)
    cantidad_almacen = fields.Int(required=True)  # Cantidad en almacén
    cantidad_inventario = fields.Int(required=True) # Cantidad en inventario
    uuid = fields.Str(required=True)              # Identificador UUID (cadena de texto)
    id_cinsumoalmacen = fields.Int(required=True) # ID de insumo de almacén
    id_bfacturacxp = fields.Int(required=True)    # ID de la factura

    @post_load
    def make_base_costos_insumos_almacen(self, data, **kwargs):
        from src.models.base_costos_insumos_almacen  import BaseCostosInsumosAlmacen
        return BaseCostosInsumosAlmacen(**data)

# Instancias del esquema
base_costos_insumos_almacen_schema = BaseCostosInsumosAlmacenSchema()
base_costos_insumos_almacen_schema_many = BaseCostosInsumosAlmacenSchema(many=True)
