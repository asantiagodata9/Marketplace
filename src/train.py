"""
train.py

Este script entrena un modelo ARIMA utilizando los datos de ventas diarias y guarda el modelo entrenado en un archivo.

Cómo utilizar:
  python train.py

Parámetros:
  Ninguno.

Dependencias:
  - logging
  - joblib
  - statsmodels

Funciones:
  - train_arima_model(input_df)
"""
import logging
from joblib import dump
from statsmodels.tsa.arima.model import ARIMA

# Configuración de logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def train_arima_model(input_df):
    """
    Entrena un modelo ARIMA utilizando los datos de ventas totales.

    Args:
        input_df (pandas.DataFrame): DataFrame que contiene los datos de ventas totales.

    Returns:
        statsmodels.tsa.arima.model.ARIMAResultsWrapper: Modelo ARIMA entrenado.
    """
    try:
        # Entrenar el modelo ARIMA
        model = ARIMA(input_df['total_sales'], order=(5, 1, 0))  # (p, d, q) son los hiperparámetros de ARIMA
        model_fit = model.fit()

        # Guardar el modelo ARIMA en un archivo joblib
        model_path = "./artifacts/models/arima_model.joblib"
        dump(model_fit, model_path)

        logging.info("Modelo entrenado guardado en './artifacts/models/arima_model.joblib'")

        return model_fit
    except Exception as e:
        logging.error(f"Error al entrenar el modelo ARIMA: {str(e)}")
        raise
