import flask
import mysql.connector as mys
from flask_cors import CORS


app = flask.Flask(__name__)
CORS(app)

@app.route('/data', methods=['POST'])
def data():
   print("entrando al post")
   valores = flask.request.values
   id=flask.request.values.get("id")
   temp=flask.request.values.get("temperatura")
   hum=flask.request.values.get("humedad")
   luz=flask.request.values.get("luz")
   usuarioSensor = "1"
   fecha = "NOW()"
   print("valores capturados desde el sensor")
   print("niciando conextion a la  db")
   cnx = mys.connect(user='administrador', password='12345678',
                                 host='iot-plantas.cck19a8z9zmf.us-east-1.rds.amazonaws.com',
                                 database='plantas')
   cur = cnx.cursor()
   cur.execute("INSERT INTO Sensores VALUES(default,"+id+","+temp+","+hum+","+luz+","+fecha+");")
   cnx.commit()
   cur.close()
   cnx.close()
   print("finaliza la conexion")
   print(str(id)+str(temp)+str(hum)+str(luz))
   return "ok"

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=80)
