import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger

class InsumosModel:

    @classmethod
    def get_inventario_por_tipo(cls, id_tipo_inventario):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            inventario = []
            
            # Consulta SQL para obtener el inventario por tipo de insumo
            query = '''
                SELECT 
                    IALMACEN.INSUMO AS 'CONCEPTO', 
                    CIALMACEN.CANTIDAD_INVENTARIO AS 'CANTIDAD_INVENTARIO' 
                FROM  
                    OPS.Base_CostosInsumosAlmacen CIALMACEN,  
                    OPS.Catalogo_InsumosAlmacen IALMACEN 
                WHERE 
                    CIALMACEN.ACTIVO = TRUE 
                    AND IALMACEN.ACTIVO = TRUE
                    AND CIALMACEN.ID_CINSUMOALMACEN = IALMACEN.ID_CINSUMOALMACEN
                    AND CIALMACEN.CANTIDAD_INVENTARIO > 0 
                    AND IALMACEN.ID_TIOPOINVENTARIO = %s
                GROUP BY 
                    IALMACEN.INSUMO;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id_tipo_inventario,))
                resultset = cursor.fetchall()

                # Procesar cada fila del resultado
                for row in resultset:
                    item_inventario = {
                        'Concepto': row[0],
                        'Cantidad_Inventario': row[1]
                    }
                    inventario.append(item_inventario)

            connection.close()
            return inventario

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener inventario: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def filtroinventiarioInsumosAll(cls, var):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            inventario_insumos = []

            # Definir la consulta SQL con parámetros seguros
            query = f'''
                SELECT 
                    CIALMACEN.FECHA AS 'FECHA',
                    IALMACEN.INSUMO AS 'CONCEPTO',
                    CIALMACEN.COSTO_UNIDAD AS 'COSTO UNIDAD',
                    CIALMACEN.CANTIDAD_ALMACEN AS 'CANTIDAD ALMACEN',
                    CIALMACEN.CANTIDAD_INVENTARIO AS 'CANTIDAD INVENTARIO'
                FROM 
                    OPS.Base_CostosInsumosAlmacen CIALMACEN
                JOIN 
                    OPS.Catalogo_InsumosAlmacen IALMACEN ON CIALMACEN.ID_CINSUMOALMACEN = IALMACEN.ID_CINSUMOALMACEN
                WHERE 
                    CIALMACEN.ACTIVO = TRUE
                    AND IALMACEN.ACTIVO = TRUE
                    AND CIALMACEN.CANTIDAD_INVENTARIO > 0
                    {var}
                ORDER BY 
                    CIALMACEN.FECHA DESC;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query)
                resultset = cursor.fetchall()

                # Procesar cada fila del resultado
                for row in resultset:
                    inventario = {
                        'FECHA': row[0],
                        'CONCEPTO': row[1],
                        'COSTO UNIDAD': row[2],
                        'CANTIDAD ALMACEN': row[3],
                        'CANTIDAD INVENTARIO': row[4]
                    }
                    inventario_insumos.append(inventario)

            return inventario_insumos

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el inventario de insumos: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()
