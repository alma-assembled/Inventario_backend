import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger
from src.schemas.catalogo_insumos_almacen import CatalogoInsumosAlmacenSchema 

class Catalogo_InsumosAlmacenService():
    @classmethod
    def save_Catalogo_InsumosAlmacen(insumo_data):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

             # Deserializar datos
            insumo = CatalogoInsumosAlmacenSchema.load(insumo_data)

            # Ejecutar la inserción de datos en la tabla Catalogo_InsumosAlmacen
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO `OPS`.`Catalogo_InsumosAlmacen` 
                    (`INSUMO`, `MEDIDA_UNIDAD`, `ID_TIOPOINVENTARIO`) 
                    VALUES (%s, %s, %s);
                ''', (insumo.insumo, insumo.medida_unidad, insumo.id_tiopoinventario))

                if cursor.lastrowid:
                    ID_CINSUMOALMACEN = cursor.lastrowid

                # Confirmar la transacción
                connection.commit()
                return True

        except Exception as ex:
            # Registrar el error
            Logger.add_to_log("error", f"Error al agregar insumo: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return False

        finally:
            # Asegurarse de cerrar la conexión
            if connection:
                connection.close()

    @classmethod
    def get_Catalogo_InsumosAlmacen_by_Id(cls, id_tipo_insumo):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            insumos = []

            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT ID_CINSUMOALMACEN, INSUMO 
                FROM OPS.Catalogo_InsumosAlmacen 
                WHERE ACTIVO = TRUE 
                AND ID_TIOPOINVENTARIO = %s 
                ORDER BY INSUMO;
            '''

            # Ejecutar la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, (id_tipo_insumo,))
                resultset = cursor.fetchall()

                # Procesar cada fila del resultado
                for row in resultset:
                    insumo = {
                        'ID_CINSUMOALMACEN': row[0],
                        'INSUMO': row[1]
                    }
                    insumos.append(insumo)

            return insumos

        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener insumos: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()
