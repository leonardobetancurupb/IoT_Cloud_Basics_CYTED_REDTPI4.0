import pandas as pd

datos = pd.read_csv('datosTemperatura.csv')
datos["fecha"] = pd.to_datetime(datos["timestamp"],unit="ms")
datos = datos.sort_values("fecha",ascending=True)
datos = datos.reset_index()
#crear vector de tiempo en minutos
datos["minutos"] = list(map(lambda i: (i-datos["fecha"][0]).total_seconds()/(3600),datos["fecha"]))
print(datos.head())
tiempo = datos["minutos"].to_list()
temperatura = datos["valor"].to_list()

import matplotlib.pyplot as plt
plt.plot(tiempo,temperatura)
plt.title("temperatura vs tiempo")
plt.xlabel("minutos")
plt.ylabel("°C")
plt.show()

import numpy as np
t = np.linspace(135,325,1000)
from scipy.interpolate import interp1d

f = interp1d(tiempo,temperatura)
y = f(t)
plt.plot(tiempo,temperatura,'o',t,y,'-')
plt.show()

# Split data into train-test
# ==============================================================================
data = pd.DataFrame(list(zip(t,y)),columns=["t","y"])
steps = 260
data_train = data[:-steps]
data_test  = data[-steps:]

print(f"Train dates : {data_train.index.min()} --- {data_train.index.max()}  (n={len(data_train)})")
print(f"Test dates  : {data_test.index.min()} --- {data_test.index.max()}  (n={len(data_test)})")

fig, ax = plt.subplots(figsize=(6, 2.5))
data_train['y'].plot(ax=ax, label='Entrenamiento')
data_test['y'].plot(ax=ax, label='Prueba')
ax.legend()
plt.show()

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import RandomForestRegressor
from skforecast.model_selection import grid_search_forecaster
from sklearn.metrics import mean_squared_error

forecaster = ForecasterAutoreg(
                regressor = RandomForestRegressor(random_state=123),
                lags      = 125
             )

forecaster.fit(y=data_train['y'])
print(forecaster)

predictions = forecaster.predict(steps=steps)
predictions.head(5)
fig, ax = plt.subplots(figsize=(6, 2.5))
data_train['y'].plot(ax=ax, label='Entrenamiento')
data_test['y'].plot(ax=ax, label='Prueba')
predictions.plot(ax=ax, label='Predicciones')
ax.legend()
plt.show()
print("fin modelo")
