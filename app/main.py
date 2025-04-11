from flask import Blueprint, request, jsonify
import csv
from app.db import insert_data_batch
from datetime import datetime

main_bp = Blueprint('main', __name__)


def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Handle datetime (as before, if needed)
                if 'datetime' in row:  # Check if the column exists
                    datetime_str = row['datetime'].replace('Z', '+00:00')
                    row['datetime'] = str(datetime.fromisoformat(datetime_str).date())

                # Handle department_id
                if 'department_id' in row:  # Check if the column exists
                    row['department_id'] = row['department_id'].strip()
                    if row['department_id'] == '':
                        row['department_id'] = None
                    else:
                        try:
                            row['department_id'] = int(row['department_id'])
                        except ValueError:
                            row['department_id'] = None

                # Handle job_id
                if 'job_id' in row:  # Check if the column exists
                    row['job_id'] = row['job_id'].strip()
                    if row['job_id'] == '':
                        row['job_id'] = None
                    else:
                        try:
                            row['job_id'] = int(row['job_id'])
                        except ValueError:
                            row['job_id'] = None

            except KeyError as e:
                print(f"KeyError: {e} not found in row: {row}")
                continue  # Skip row or handle error

            except Exception as e:
                print(f"General error processing row: {row}, error: {e}")
                continue  # Skip row or handle error

            data.append(row)
        return data

@main_bp.route('/upload-csv/<string:table_name>', methods=['POST'])
def upload_csv(table_name):
    """Maneja la carga de archivos CSV e inserta los datos en la tabla especificada."""

    if table_name not in ('departments', 'jobs', 'hired_employees'):
        return jsonify({'error': 'Nombre de tabla inválido'}), 400

    file_path = request.args.get('file_path')  # Obtener la ruta del archivo del parámetro de consulta
    if not file_path:
        return jsonify({'error': 'La ruta del archivo es requerida'}), 400

    try:
        data = read_csv(file_path)
        insert_data_batch(table_name, data)  # Asumiendo que esta función maneja el loteo
        return jsonify({'message': f'Datos cargados exitosamente en {table_name}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/insert-batch/<string:table_name>', methods=['POST'])
def insert_batch(table_name):
    """Inserta un lote de datos en la tabla especificada."""

    if table_name not in ('departments', 'jobs', 'hired_employees'):
        return jsonify({'error': 'Nombre de tabla inválido'}), 400

    data = request.get_json()
    if not isinstance(data, list) or len(data) > 1000 or len(data) == 0:
        return jsonify({'error': 'Formato de datos o tamaño de lote inválido'}), 400

    try:
        insert_data_batch(table_name, data)
        return jsonify({'message': f'Se insertaron exitosamente {len(data)} filas en {table_name}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500