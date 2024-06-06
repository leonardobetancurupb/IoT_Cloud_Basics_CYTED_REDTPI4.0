from flask import Flask, render_template, jsonify, request
import sqlite3
import sys

db_path = 'Sensor_Database/sensorData.db'


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/registro')
def registro():
    return render_template('registro.html')
@app.route('/borrardb')
def borrardb():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data (idsensor NUMERIC, timestamp DATETIME, temp NUMERIC, lat NUMERIC, lon NUMERIC)")
    con.commit()
    con.close()
    return render_template('index.html')
@app.route("/visualizacion")
def captura():
    sensorID = []
    sensorTime = []
    sensorTemp = []
    sensorLat = []
    sensorLon = []
    con = sqlite3.connect(db_path)
    curs = con.cursor()
    for fila in curs.execute("SELECT * FROM data"):
        sensorID.append(fila[0])
        sensorTime.append(fila[1])
        sensorTemp.append(fila[2])
        sensorLat.append(fila[3])
        sensorLon.append(fila[4])
    con.close()
    print(sensorID)
    leyenda = 'Temperatura sensor'
    etiquetas = sensorTime
    valores = sensorTemp
    return render_template('chart.html', values=valores, labels=etiquetas, legend=leyenda)

@app.route('/sensor_send_data', methods=['POST'])
def sensor_send():
    values = request.data
    print(values)
    a=str(request.values.get('id'))
    print(a.split(";")[0])
    print(a.split(";")[1].split("=")[1])
    print(a.split(";")[2].split("=")[1])
    print(a.split(";")[3].split("=")[1])
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO data VALUES(" + a.split(";")[0] + "," + "datetime('now')," + a.split(";")[1].split("=")[1] + "," + a.split(";")[3].split("=")[1] + "," + a.split(";")[2].split("=")[1] + ")")
    con.commit()
    con.close()
    return "ok",201

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0',port=80)
