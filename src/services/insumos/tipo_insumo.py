import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger


class Tipo_Insumos():
    @classmethod
    def tipo_insumo(cls, id_departamento):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            tipos_insumos = []

            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT 
                    ID_TIOPOINVENTARIO, 
                    DESCRIPCION 
                FROM 
                    OPS.Catalogo_Tipo_Insumo 
                WHERE 
                    ACTIVO = TRUE 
                    AND ID_RHCDEPARTAMENTO = %s 
                ORDER BY 
                    DESCRIPCION DESC;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id_departamento,))
                resultset = cursor.fetchall()

                # Procesar cada fila del resultado
                for row in resultset:
                    tipo_insumo = {
                        'ID_TIPO_INVENTARIO': row[0],
                        'DESCRIPCION': row[1]
                    }
                    tipos_insumos.append(tipo_insumo)

            return tipos_insumos

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener tipos de insumos: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()
