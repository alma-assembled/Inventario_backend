import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger


class Insumos_util():
    @classmethod
    def insumo_por_id(cls, id_insumo):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            
            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT 
                    INSUMO 
                FROM 
                    OPS.Catalogo_InsumosAlmacen 
                WHERE 
                    ID_CINSUMOALMACEN = %s;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id_insumo,))
                result = cursor.fetchone()

                # Verificar si se obtuvo un resultado
                if result:
                    return result[0]  # Retornar solo el nombre del insumo

                return None  # Retornar None si no se encontró el insumo

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener insumo por ID: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return None

        finally:
            if connection:
                connection.close()

    
    @classmethod
    def cantidad_disponible_insumos(cls, id_insumos_almacen):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            insumos_disponibles = []

            # Definir la consulta SQL
            query = '''
                SELECT 
                    ID_BCOSTOINSUMO, 
                    CANTIDAD_INVENTARIO, 
                    COSTO_UNIDAD, 
                    FECHA 
                FROM 
                    OPS.Base_CostosInsumosAlmacen 
                WHERE 
                    ID_CINSUMOALMACEN = %s 
                    AND ACTIVO = 1 
                    AND CANTIDAD_INVENTARIO > 0 
                ORDER BY 
                    FECHA;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id_insumos_almacen,))
                resultset = cursor.fetchall()

                # Procesar cada fila del resultado
                for row in resultset:
                    insumo = {
                        'ID_BCOSTOINSUMO': row[0],
                        'CANTIDAD_INVENTARIO': row[1],
                        'COSTO_UNIDAD': row[2],
                        'FECHA': row[3]
                    }
                    insumos_disponibles.append(insumo)

            return insumos_disponibles

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener la cantidad de insumos disponibles: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()


    @classmethod
    def insumo_por_nombre(cls, insumo):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT 
                    ID_CINSUMOALMACEN 
                FROM 
                    OPS.Catalogo_InsumosAlmacen 
                WHERE 
                    INSUMO = %s;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (insumo,))
                result = cursor.fetchone()

                # Verificar si se obtuvo un resultado
                if result:
                    return result[0]  # Retornar solo el ID del insumo

                return None  # Retornar None si no se encontró el insumo

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener insumo por nombre: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return None

        finally:
            if connection:
                connection.close()

    @classmethod
    def insumo_produccion_por_id(cls, id):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT * 
                FROM OPS.Base_InsumosProduccion 
                WHERE ID_BINSUMOPRODUCCION = %s;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                result = cursor.fetchone()

                return result  # Retornar el registro encontrado (puede ser None si no se encuentra)

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener insumo de producción por ID: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return None

        finally:
            if connection:
                connection.close()


    @classmethod
    def costos_insumos_almacen_por_id(cls, id):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT * 
                FROM OPS.Base_CostosInsumosAlmacen 
                WHERE ID_BCOSTOINSUMO = %s;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                result = cursor.fetchone()

                return result  # Retornar el registro encontrado (puede ser None si no se encuentra)

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener costos de insumos de almacén por ID: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return None

        finally:
            if connection:
                connection.close()

    @classmethod
    def cantidad_inventario_insumo(cls, id_insumo):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT SUM(CIALMACEN.CANTIDAD_INVENTARIO) AS SUMA 
                FROM OPS.Base_CostosInsumosAlmacen CIALMACEN
                WHERE 
                    CIALMACEN.CANTIDAD_INVENTARIO > 0
                    AND CIALMACEN.ID_CINSUMOALMACEN = %s 
                    AND CIALMACEN.ACTIVO = 1;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id_insumo,))
                result = cursor.fetchone()

                return result  # Retornar el resultado de la suma (puede ser None si no hay inventario)

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener cantidad de inventario del insumo: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return None

        finally:
            if connection:
                connection.close()
