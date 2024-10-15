import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger

from src.schemas.base_insumos_produccion import BaseInsumosProduccionSchema 
from src.models.base_insumos_produccion import BaseInsumosProduccion

class Base_InsumosProduccionSevice():

    @classmethod
    def insert_base_insumos_produccion(cls, produccion_data):
        connection = None
        try:
            # Deserializar datos
            produccion_insumo = BaseInsumosProduccion.load(produccion_data)
            connection = get_connection()

            # Definir la consulta SQL para insertar datos en Base_CostosInsumosAlmacen
            query = '''
                INSERT INTO `OPS`.`Base_InsumosProduccion` 
                (`FECHA`, `CANTIDAD`, `COSTO`, `ID_BOP`, `ID_BCOSTOINSUMO`) 
                VALUES (%s, %s, %s, %s, %s);
            '''
            
            values = (str(produccion_insumo.fecha), str(produccion_insumo.cantidad), produccion_insumo.costo, str(produccion_insumo.id_bop), str(produccion_insumo.id_bcostoinsumo))

            with connection.cursor() as cursor:
                cursor.execute(query, values)

                if cursor.lastrowid:
                    id_insumo_produccion = cursor.lastrowid
                    Logger.add_to_log("info", f"ID del insumo de producción insertado: {id_insumo_produccion}")

            connection.commit()
            return id_insumo_produccion

        except Exception as ex:
            # Registrar el error
            Logger.add_to_log("error", f"Error al insertar insumo de producción: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return False

        finally:
            if connection:
                connection.close()
    
    @classmethod
    def update_insumos_produccion_cantidad(cls, cantidad_nueva, id_binsumoproduccion):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL para actualizar la cantidad en Base_InsumosProduccion
            query = '''
                UPDATE `OPS`.`Base_InsumosProduccion`
                SET `CANTIDAD` = %s
                WHERE `ID_BINSUMOPRODUCCION` = %s;
            '''
            
            # Definir los valores para la actualización
            values = (cantidad_nueva, id_binsumoproduccion)

            # Ejecutar la actualización de datos
            with connection.cursor() as cursor:
                cursor.execute(query, values)

                # Confirmar si se actualizó algún registro
                if cursor.rowcount > 0:
                    return id_binsumoproduccion  # Devolver el ID del registro actualizado
                else:
                    print(f"No se encontró el registro con ID_BINSUMOPRODUCCION: {id_binsumoproduccion}")
                    return None

            # Confirmar la transacción
            connection.commit()

        except Exception as ex:
            # Manejo de excepciones y registro del error
            Logger.add_to_log("error", f"Error al actualizar la cantidad de producción: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return False

        finally:
            # Asegurarse de cerrar la conexión
            if connection:
                connection.close()
