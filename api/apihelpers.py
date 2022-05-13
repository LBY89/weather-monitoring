from flask import request, jsonify
from psycopg2.extras import RealDictCursor
from app import app
import db
from flask import send_from_directory


# endpoint not found 
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404    
    return resp
@app.route('/api/reset', methods=['POST'])
def reset_smart():
    try:
        conn = db.createConnection()
        cursor = conn.cursor()
        sql = """
            TRUNCATE TABLE smart RESTART IDENTITY;
        """
        cursor.execute(sql)
        conn.commit()
        conn.close()
        message = {
            'status':200,
            'message':'Reseted!'
        }
        resp = jsonify(message)
        return resp
    except Exception as e:
        message = {
            'status': 500,
            'message': str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp   

@app.route('/api/dump', methods=['GET'])
def dump_smart():
    try:
        filename ='data.csv'
        conn = db.createConnection()
        cursor = conn.cursor()
        # get all signal names
        sql = """
            SELECT DISTINCT jsonb_object_keys(data) AS name 
            FROM smart
            ORDER BY name
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        names = ''
        name = ''
        for r in rows:
            name = name.join(r) #modify double to string, to remove brackets from jsonb 
            names += (f"""data->>'{name}' as "{name}",""")
        names = names.rstrip(names[-1]) # to remove last comma from the previous line of code.
        sql2 = """
            SELECT device_id, date_time, {}
            FROM smart
            ORDER BY id
        """.format(names)
        conn = db.createConnection()
        cursor = conn.cursor()
        csv_output =  "COPY (" + sql2 + ") TO STDOUT WITH CSV HEADER QUOTE '\b'"
        filename ='data.csv'
        with open(filename, 'w') as f_output:
            cursor.copy_expert(csv_output, f_output)
        return send_from_directory('', filename, as_attachment=False)

    except Exception as e:
        message = {
            'status': 500,
            'message': str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp