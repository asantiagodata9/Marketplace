"""
main.py

Este script ejecuta el flujo principal del proyecto, que incluye la obtención de datos de órdenes, preprocesamiento de datos,
entrenamiento de un modelo ARIMA, y realización de predicciones futuras.

Cómo utilizar:
  python main.py

Parámetros:
  Ninguno.

Dependencias:
  - logging
  - numpy
  - pandas
  - src (módulo que contiene los scripts prep.py, train.py y pred.py)
  - statsmodels
  - sklearn

Funciones principales:
  - prep.get_orders_data(): Obtener datos de órdenes desde AWS Athena.
  - prep.process_and_split_data(orders_data): Procesar y dividir los datos de órdenes en conjuntos de entrenamiento y prueba.
  - train.train_arima_model(train_data): Entrenar un modelo ARIMA utilizando los datos de entrenamiento.
  - pred.make_future_forecast(model_fit): Realizar predicciones futuras utilizando un modelo ARIMA previamente entrenado.
"""

import logging
import numpy as np
import pandas as pd
from src import prep, train, pred
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV

logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

try:
    orders_data = prep.get_orders_data()
    train_data, test_data = prep.process_and_split_data(orders_data)
    model_fit = train.train_arima_model(train_data)
    future_forecast_df = pred.make_future_forecast(model_fit)   
except Exception as e:
    logging.error(f"Se produjo un error durante la ejecución del script: {str(e)}")
    raise
