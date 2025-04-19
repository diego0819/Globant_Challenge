import psycopg2
from flask import current_app

def get_db_connection():
    
    try:
        conn = psycopg2.connect(
            dbname="postgres",  
            user="postgres",    
            password="",  
            host="localhost",      
            port="5432"            
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def insert_data_batch(table_name, data):
    

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

        # sentencia SQL INSERT
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        values_list = [tuple(row[col] for col in columns) for row in data]  

        cursor.executemany(insert_query, values_list)  
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error de base de datos: {e}")

    finally:
        cursor.close()
        conn.close()
