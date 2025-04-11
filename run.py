import psycopg2
from flask import Flask, jsonify, g

app = Flask(__name__)

DATABASE_URL = 'postgresql://postgres:Halo3071041@localhost:5432/postgres' # Reemplaza con tus credenciales

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

@app.route('/hires_by_quarter', methods=['GET'])
def get_hires_by_quarter():
    conn = get_db()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    query = """
    SELECT
            d.department,
            j.job,
            SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM
            hired_employees h
        JOIN
            departments d ON h.department_id = d.id
        JOIN
            jobs j ON h.job_id = j.id
        WHERE
            EXTRACT(YEAR FROM h.datetime) = 2021
        GROUP BY
            d.department,
            j.job
        ORDER BY
            d.department ASC,
            j.job ASC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    output = []
    column_names = [desc[0] for desc in cursor.description]
    for row in results:
        output.append(dict(zip(column_names, row)))

    return jsonify(output)

@app.route('/departments_above_average_hires', methods=['GET'])
def get_departments_above_average_hires():
    conn = get_db()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    query = """
        SELECT
            d.department,
            COUNT(h.id) AS hired
        FROM
            hired_employees h
        JOIN
            departments d ON h.department_id = d.id
        WHERE
            EXTRACT(YEAR FROM h.datetime) = 2021
        GROUP BY
            d.department
        HAVING
            COUNT(h.id) > (SELECT AVG(hires_per_dept) FROM (SELECT COUNT(id) as hires_per_dept FROM hired_employees WHERE EXTRACT(YEAR FROM datetime) = 2021 GROUP BY department_id) AS dept_counts)
        ORDER BY
            hired DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    output = []
    column_names = [desc[0] for desc in cursor.description]
    for row in results:
        output.append(dict(zip(column_names, row)))

    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
