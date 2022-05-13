from flask import Flask, request, jsonify
import db
import json
from app import app

#default api method is "get", if want to use other methods, must specify
# insert
@app.route('/api/smart', methods=['POST'])
def insert_smart():
    content = request.get_json()
    device_id = content['device_id']
    data = json.dumps(content['data']) #to get double quotation marks for jsonb
    print(f'device  {device_id}', flush=True)
    print(f'data  {data}', flush=True)
    
    try:
        conn = db.createConnection()#make connection to postgres db
        cursor = conn.cursor()
        sql = """
            INSERT INTO Smart (device_id, data) VALUES ('{}', '{}')
        """.format(device_id, data)
        print(f'sql: {sql}', flush=True)
        cursor.execute(sql) #execute the sql
        conn.commit() #to save data to database
        cursor.close()
        conn.close()

        message = {
        'baoying super':200,
        'message': 'Inserted'
        }
        resp = jsonify(message)
        return resp
    
    except Exception as e:
        message = {
            'status': 500,
            'message': str(e)


        }
        resp = jsonify(message)
        return resp

    