"""
prep.py

Este script realiza la obtención de datos de órdenes desde AWS Athena, procesa los datos para calcular las ventas diarias,
y divide los datos en conjuntos de entrenamiento y prueba. También guarda los DataFrames resultantes en archivos CSV y registra
los resultados en un archivo de registro.

Cómo utilizar:
  python prep.py

Parámetros:
  Ninguno.

Dependencias:
  - boto3
  - pandas
  - awswrangler
  - sklearn
  - logging

Funciones:
  - get_orders_data()
  - process_and_split_data(input_df)
"""
import boto3
import logging
import pandas as pd
import awswrangler as wr
from sklearn.model_selection import train_test_split

# Configuración de logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def get_orders_data():
    """
    Función para obtener datos de órdenes desde AWS Athena y guardarlos como un archivo CSV.

    Returns:
        pandas.DataFrame: DataFrame que contiene los datos de las órdenes.
    """
    try:
        # Crear una sesión de boto3 utilizando el perfil 'arquitectura'
        session = boto3.Session(profile_name='arquitectura')

        # Definir la consulta SQL
        query = '''
            SELECT *
            FROM marketplace.orders;
        '''

        # Ejecutar la consulta en Athena y obtener los resultados
        orders_data = wr.athena.read_sql_query(
            query,
            database="orders",
            ctas_approach=False,
            boto3_session=session
        )

        # Guardar el DataFrame como CSV en ./data/orders.csv
        orders_data.to_csv('./data/raw/orders.csv', index=False)

        logging.info(f"DataFrame con las órdenes descargado de S3 guardado en './data/raw/orders.csv'")

        return orders_data
    except Exception as e:
        logging.error(f"Error al obtener los datos de las órdenes: {str(e)}")
        raise

def process_and_split_data(input_df):
    """
    Función para procesar los datos de órdenes, calcular las ventas diarias y dividir los datos en conjuntos de entrenamiento y prueba.

    Args:
        input_df (pandas.DataFrame): DataFrame de entrada con los datos de órdenes.

    Returns:
        tuple: Dos DataFrames, uno para el conjunto de entrenamiento y otro para el conjunto de prueba.
    """
    try:
        # Convertir la columna de fecha
        input_df['date_created'] = pd.to_datetime(input_df['date_created'])

        # Agregar las ventas diarias
        daily_sales = input_df.groupby(input_df['date_created'].dt.date).agg({'total_amount': 'sum'}).reset_index()
        daily_sales.columns = ['date', 'total_sales']
        
        sales = input_df.groupby(input_df['date_created'].dt.date).agg({'total_amount': 'sum'}).reset_index()
        sales.columns = ['date', 'total_sales']

        # Asegurarse de que la fecha esté en el índice y establecer la frecuencia
        daily_sales['date'] = pd.to_datetime(daily_sales['date'])
        daily_sales.set_index('date', inplace=True)
        daily_sales = daily_sales.asfreq('D')

        # Dividir los datos en conjuntos de entrenamiento y prueba
        train_data, test_data = train_test_split(daily_sales, test_size=0.2, shuffle=False)

        # Guardar el DataFrame de entrenamiento como CSV
        train_data.to_csv("./data/clean/orders_train.csv")

        # Guardar el DataFrame de prueba como CSV
        test_data.to_csv("./data/clean/orders_test.csv")

        logging.info(f"DataFrame de entrenamiento guardado en './data/clean/orders_train.csv' y DataFrame de prueba guardado en './data/clean/orders_test.csv'")

        return sales, train_data, test_data
    except Exception as e:
        logging.error(f"Error al procesar y dividir los datos: {str(e)}")
        raise
