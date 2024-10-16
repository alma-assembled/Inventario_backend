import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger

from src.schemas.base_costos_insumos_almacen import BaseCostosInsumosAlmacenSchema 
from src.models.base_costos_insumos_almacen import BaseCostosInsumosAlmacen

class Base_CostosInsumosAlmacenService():

    @classmethod
    def insert_base_costos_insumos_almacen(cls, costos_data):
        connection = None
        try:
             # Deserializar datos
            costos_insumo = BaseCostosInsumosAlmacenSchema.load(costos_data)
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL para insertar datos en Base_CostosInsumosAlmacen
            query = '''
                INSERT INTO `OPS`.`Base_CostosInsumosAlmacen` 
                (`FECHA`, `COSTO_UNIDAD`, `CANTIDAD_ALMACEN`, `CANTIDAD_INVENTARIO`, `ID_CINSUMOALMACEN`) 
                VALUES (%s, %s, %s, %s, %s);
            '''
            
            # Definir los valores a insertar
            values = (str(costos_insumo.fecha), costos_insumo.costo, str(costos_insumo.cantidad_almacen), str(costos_insumo.cantidad_inventario), str(costos_insumo.id_insumo))

            # Ejecutar la inserción de datos
            with connection.cursor() as cursor:
                cursor.execute(query, values)

                # Obtener el ID del costo insertado
                if cursor.lastrowid:
                    id_costo_insumo = cursor.lastrowid
                    #Logger.add_to_log("info", f"ID del costo de insumo insertado: {id_costo_insumo}")

            # Confirmar la transacción
            connection.commit()
            return id_costo_insumo

        except Exception as ex:
            # Registrar el error
            Logger.add_to_log("error", f"Error al insertar costos del insumo: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return False

        finally:
            # Asegurarse de cerrar la conexión
            if connection:
                connection.close()

    @classmethod
    def update_costos_insumos_almacen(cls, id_bcostoinsumo, cantidad_nueva):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL para actualizar la cantidad de inventario en Base_CostosInsumosAlmacen
            query = '''
                UPDATE `OPS`.`Base_CostosInsumosAlmacen` 
                SET `CANTIDAD_INVENTARIO` = %s 
                WHERE `ID_BCOSTOINSUMO` = %s;
            '''
            
            # Definir los valores para la actualización
            values = (cantidad_nueva, id_bcostoinsumo)

            # Ejecutar la actualización de datos
            with connection.cursor() as cursor:
                cursor.execute(query, values)

                # Verificar si se actualizó algún registro
                if cursor.rowcount > 0:
                    #Logger.add_to_log("info", f"Actualización exitosa para ID: {id_bcostoinsumo}")
                    return id_bcostoinsumo  # Devolver el ID del costo actualizado
                else:
                    print(f"No se encontró el registro con ID_BCOSTOINSUMO: {id_bcostoinsumo}")
                    return None

            # Confirmar la transacción
            connection.commit()

        except Exception as ex:
            # Registrar el error
            Logger.add_to_log("error", f"Error al actualizar costos del insumo: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return False

        finally:
            # Asegurarse de cerrar la conexión
            if connection:
                connection.close()

    @classmethod
    def update_costos_insumos_almacen_cantidad(cls, cantidad_nueva, id_bcostoinsumo):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()

            # Definir la consulta SQL para actualizar la cantidad de inventario en Base_CostosInsumosAlmacen
            query = '''
                UPDATE `OPS`.`Base_CostosInsumosAlmacen` 
                SET `CANTIDAD_INVENTARIO` = %s 
                WHERE `ID_BCOSTOINSUMO` = %s;
            '''
            
            # Definir los valores para la actualización
            values = (cantidad_nueva, id_bcostoinsumo)

            # Ejecutar la actualización de datos
            with connection.cursor() as cursor:
                cursor.execute(query, values)

                # Confirmar si se actualizó algún registro
                if cursor.rowcount > 0:
                    return id_bcostoinsumo  # Devolver el ID del registro actualizado
                else:
                    print(f"No se encontró el registro con ID_BCOSTOINSUMO: {id_bcostoinsumo}")
                    return None

            # Confirmar la transacción
            connection.commit()

        except Exception as ex:
            # Manejo de excepciones y registro del error
            Logger.add_to_log("error", f"Error al actualizar la cantidad de inventario: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return False

        finally:
            # Asegurarse de cerrar la conexión
            if connection:
                connection.close()

    @classmethod
    def get_Catalogo_InsumosAlmacen(cls, id_tipo_insumo):
        connection = None
        try:
            # Obtener conexión a la base de datos
            connection = get_connection()
            insumos = []

            # Definir la consulta SQL con parámetros seguros
            query = '''
                SELECT 
                    IALMACEN.ID_CINSUMOALMACEN, 
                    IALMACEN.INSUMO 
                FROM 
                    OPS.Catalogo_InsumosAlmacen IALMACEN
                JOIN 
                    OPS.Base_CostosInsumosAlmacen CIALMACEN ON IALMACEN.ID_CINSUMOALMACEN = CIALMACEN.ID_CINSUMOALMACEN
                WHERE 
                    CIALMACEN.CANTIDAD_INVENTARIO > 0
                    AND IALMACEN.ACTIVO = 1 
                    AND CIALMACEN.ACTIVO = 1 
                    AND IALMACEN.ID_TIOPOINVENTARIO = %s
                GROUP BY 
                    IALMACEN.ID_CINSUMOALMACEN;
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
            Logger.add_to_log("error", f"Error al obtener insumos del almacén: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return []

        finally:
            if connection:
                connection.close()
