import psycopg2
from flask import current_app

def get_db_connection():
    """Devuelve una conexión a la base de datos."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # Reemplaza con el nombre de tu base de datos
            user="postgres",    # Reemplaza con tu usuario de base de datos
            password="Halo3071041",  # Reemplaza con tu contraseña de base de datos
            host="localhost",       # Reemplaza con tu host de base de datos si no es local
            port="5432"            # Reemplaza con tu puerto de base de datos si no es el predeterminado
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def insert_data_batch(table_name, data):
    """Inserta un lote de datos en la tabla especificada."""

    if not data:
        return  # Nada que insertar

    conn = get_db_connection()
    if conn is None:
        raise Exception("Fallo al conectar con la base de datos")

    cursor = conn.cursor()
    try:
        if table_name == 'departments':
            columns = ['id', 'department']
        elif table_name == 'jobs':
            columns = ['id', 'job']
        elif table_name == 'hired_employees':
            columns = ['id', 'name', 'datetime', 'department_id', 'job_id']
        else:
            raise ValueError(f"Nombre de tabla inválido: {table_name}")

        # Construir la sentencia SQL INSERT
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        values_list = [tuple(row[col] for col in columns) for row in data]  # Crear una lista de tuplas

        cursor.executemany(insert_query, values_list)  # Insertar múltiples filas eficientemente
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error de base de datos: {e}")

    finally:
        cursor.close()
        conn.close()