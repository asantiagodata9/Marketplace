# Marketplace

--------------------------------
Arquitectura
![Marketplace](Marketplace/Ad-InFo.png)

Hasta ahora el proyecto se divide en cuatro partes:

En la primera parte se decargan los datos usando la api de mercado libre en el archivo ./MELI - descarga de ventas.ipynb y se guardan en ./data/orders.csv. Se ejecuta este paso corriendo el script ./MELI - descarga de ventas.ipynb

En la segunda parte hacemos un ETL en la ruta ./src/ETL.ipynb donde limpiamos los datos llamando dentro del notebook al script ./src/data_preocessing.sh, los guardamos en ./data/AWS/orders.py y los cargamos a s3, despues se hace un ELT en la ruta ./src/ELT.ipynb donde descargamos los datos con ayuda de Athena en la ruta ./data/raw/orders.csv. Se ejecuta este paso corriendo los notebooks ./src/ETL.ipynb y ./src/ELT.ipynb 

En la tercera parte usamos los datos para entrenar un modelo en el notebook ./src/analytics.ipynb. Se ejecuta este paso corriendo el notebook ./src/analytics.ipynb

Finalmente dividimos el entrenamiento del modelo en tres scripts de pythonn preparandolos para usarse en la nube. En ./src/prep.py llamamos los datos desde Athena,los guardamos en ./data/raw/orders.csv y los procesamos y hacemos el train-test split y los guardamos en ./data/clean/orders_train.csv y ./data/clean/orders_test.csv. En ./src/train.py entrenamos el modelo con los datos y guardamos el modelo entrenado en ./artifacts/models/arima_model.joblib. En ./src/pred.py hacemos las prediciones y la guardamos en ./data/clean/orders_pred.py. Ejucutamos todo este paso desde el script main.py

Esctructura de carpetas
|project_root/
    |-- main.py
    |-- MELI - descarga de ventas.ipynb
    |-- data/
        |-- AWS/
            |-- orders_clean.csv
        |-- clean/
            |-- orders_pred.csv
            |-- orders_test.csv
            |-- orders_train.csv
        |-- raw/
            |-- orders.csv
        |-- orders.csv
    |-- src/
        |-- __init__.py
        |-- analytics.ipynb
        |-- data_processing.sh
        |-- ELT.ipynb
        |-- ETL.ipynb
        |-- pred.py
        |-- prep.py
        |-- train.py
    |-- artifacts/
        |-- models/
            |-- arima_model.joblib
    |-- environment.yml
    |-- api_meli_colch.env
    |-- README.md
    |-- results.log
    |-- Ad-InFo.png
    |-- Ad-InFo.drawio.html
    |-- .gitignore
