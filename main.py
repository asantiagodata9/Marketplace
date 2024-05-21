"""
main.py

Este script ejecuta el flujo principal del proyecto, que incluye la obtención de datos de órdenes, preprocesamiento de datos,
entrenamiento de un modelo ARIMA, y realización de predicciones futuras. Además, guarda los resultados en S3 y crea una tabla
con los resultados en Athena.

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

import boto3
import logging
import numpy as np
import pandas as pd
import awswrangler as wr
from datetime import timedelta
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
    sales, train_data, test_data = prep.process_and_split_data(orders_data)
    model_fit = train.train_arima_model(train_data)
    future_forecast_df = pred.make_future_forecast(model_fit)   
except Exception as e:
    logging.error(f"Se produjo un error durante la ejecución del script: {str(e)}")
    raise


# Get the max date from the orders_test DataFrame
max_date = pd.to_datetime(sales['date']).max()

# Create a date range for the next 30 days
future_dates = pd.date_range(start=max_date + timedelta(days=1), periods=30, freq='D')

# Assign the future dates to the orders_pred DataFrame
future_forecast_df['date'] = future_dates
future_forecast_df.rename(columns={'Predictions': 'total_sales'}, inplace=True)

# Add a 'type' column
sales['type'] = 'actuals'
future_forecast_df['type'] = 'forecast'

# Concatenate the DataFrames
all_orders_forecast = pd.concat([sales, future_forecast_df[['date', 'total_sales', 'type']]])

# Ensure the date column is in datetime format
all_orders_forecast['date'] = pd.to_datetime(all_orders_forecast['date'])

# Sort by date
all_orders_forecast.sort_values(by='date', inplace=True)

# Reset index (optional)
all_orders_forecast.reset_index(drop=True, inplace=True)

# Save to a new CSV
all_orders_forecast.to_csv('./data/AWS/all_orders_forecast.csv', index=False)

# Abrir cliente de S3
session = boto3.Session(profile_name='arquitectura')
s3 = session.client('s3')
BUCKET_NAME = "itam-mgs-pf-marketplace"

# Upload los archivos a S3
s3.upload_file(Filename="./data/AWS/all_orders_forecast.csv", Bucket=BUCKET_NAME, Key="s../forecast/all_orders_forecast.csv")

query = '''
    CREATE EXTERNAL TABLE IF NOT EXISTS marketplace.all_orders_forecast (
    date string,
    total_sales float,
    type string
    ) 
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
    WITH SERDEPROPERTIES ('field.delim' = ',') 
    STORED AS TEXTFILE
    LOCATION 's3://itam-mgs-pf-marketplace/s../forecast/' 
    TBLPROPERTIES ('classification' = 'csv', 'skip.header.line.count'='1');

'''

wr.athena.read_sql_query(
    query, 
    database="marketplace", 
    ctas_approach=False, 
    boto3_session=session
)