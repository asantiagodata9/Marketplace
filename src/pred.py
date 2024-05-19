"""
pred.py

Este script realiza predicciones futuras utilizando un modelo ARIMA previamente entrenado y guarda las predicciones en un archivo CSV.

Cómo utilizar:
  python pred.py

Parámetros:
  Ninguno.

Dependencias:
  - pandas
  - logging

Funciones:
  - make_future_forecast(model_fit, steps=30)
"""

import pandas as pd
import logging

# Configuración de logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def make_future_forecast(model_fit, steps=30):
    """
    Realiza predicciones futuras utilizando un modelo ARIMA previamente entrenado y guarda las predicciones en un archivo CSV.

    Args:
        model_fit (statsmodels.tsa.arima.model.ARIMAResultsWrapper): Modelo ARIMA entrenado.
        steps (int): Número de pasos futuros para predecir.

    Returns:
        pandas.DataFrame: DataFrame que contiene las predicciones futuras.
    """
    try:
        # Realizar predicciones futuras con el modelo ARIMA
        future_forecast = model_fit.forecast(steps=steps)

        # Crear un DataFrame para almacenar las predicciones futuras
        future_forecast_df = pd.DataFrame({'Predictions': future_forecast})
        
        # Guardar el DataFrame de prueba como CSV sin incluir el índice
        future_forecast_df.to_csv("./data/clean/orders_pred.csv", index=False)

        logging.info(f"DataFrame de predicciones guardado en './data/clean/orders_pred.csv'")

        return future_forecast_df
    except Exception as e:
        logging.error(f"Error al realizar las predicciones futuras: {str(e)}")
        raise
