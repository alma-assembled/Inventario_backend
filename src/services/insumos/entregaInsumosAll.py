import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger

class InsumosModel:

    @classmethod
    def get_entrega_insumos_all(cls, id_tipo_inventario):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            insumos = []
            
            # Consulta SQL para obtener los datos
            query = f'''
                SELECT 
                    IPRODUCCION.ID_BINSUMOPRODUCCION as 'ID', 
                    BOP.FOLIO AS 'OP', 
                    IPRODUCCION.FECHA,  
                    IALMACEN.INSUMO AS 'MATERIAL',  
                    IPRODUCCION.CANTIDAD
                FROM 
                    OPS.Base_InsumosProduccion IPRODUCCION
                JOIN 
                    OPS.Base_CostosInsumosAlmacen CIALMACEN ON CIALMACEN.ID_BCOSTOINSUMO = IPRODUCCION.ID_BCOSTOINSUMO
                JOIN 
                    OPS.Catalogo_InsumosAlmacen IALMACEN ON CIALMACEN.ID_CINSUMOALMACEN = IALMACEN.ID_CINSUMOALMACEN
                JOIN 
                    OPS.Base_OP BOP ON IPRODUCCION.ID_BOP = BOP.ID_BOP
                WHERE 
                    IPRODUCCION.ACTIVO = TRUE 
                    AND CIALMACEN.ACTIVO = TRUE 
                    AND IALMACEN.ACTIVO = TRUE
                    AND IPRODUCCION.CANTIDAD > 0
                    AND IALMACEN.ID_TIOPOINVENTARIO = %s
                ORDER BY 
                    IPRODUCCION.FECHA DESC;
            ''' 

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id_tipo_inventario,))
                resultset = cursor.fetchall()

                # Procesar cada fila del resultado
                for row in resultset:
                    insumo = {
                        'ID_BINSUMOPRODUCCION': row[0],
                        'OP': row[1],
                        'FECHA': row[2],
                        'MATERIAL': row[3],
                        'CANTIDAD': row[4],
                        'COSTO': row[5]
                    }
                    insumos.append(insumo)

            connection.close()
            return insumos

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener insumos: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()


    @classmethod
    def filtro_entregados(cls, consulta):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            entregados = []

            # Definir la consulta SQL con parámetros seguros
            query = f'''
                SELECT 
                    IPRODUCCION.ID_BINSUMOPRODUCCION AS 'ID',
                    BOP.FOLIO AS 'OP',
                    IPRODUCCION.FECHA,
                    IALMACEN.INSUMO AS 'MATERIAL',
                    IPRODUCCION.CANTIDAD,
                    IPRODUCCION.COSTO AS 'COSTO'
                FROM 
                    OPS.Base_InsumosProduccion IPRODUCCION
                JOIN 
                    OPS.Base_CostosInsumosAlmacen CIALMACEN ON CIALMACEN.ID_BCOSTOINSUMO = IPRODUCCION.ID_BCOSTOINSUMO
                JOIN 
                    OPS.Catalogo_InsumosAlmacen IALMACEN ON CIALMACEN.ID_CINSUMOALMACEN = IALMACEN.ID_CINSUMOALMACEN
                JOIN 
                    OPS.Base_OP BOP ON IPRODUCCION.ID_BOP = BOP.ID_BOP
                WHERE 
                    IPRODUCCION.ACTIVO = TRUE
                    AND CIALMACEN.ACTIVO = TRUE
                    AND IALMACEN.ACTIVO = TRUE
                    AND IPRODUCCION.CANTIDAD > 0
                    {consulta}
                ORDER BY 
                    IPRODUCCION.FECHA DESC;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query)
                resultset = cursor.fetchall()

                # Procesar cada fila del resultado
                for row in resultset:
                    entregado = {
                        'ID_BINSUMOPRODUCCION': row[0],
                        'OP': row[1],
                        'FECHA': row[2],
                        'MATERIAL': row[3],
                        'CANTIDAD': row[4],
                        'COSTO': row[5]
                    }
                    entregados.append(entregado)

            return entregados

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener insumos entregados: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()