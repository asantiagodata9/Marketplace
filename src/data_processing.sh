#!/bin/bash

# Convertir caracteres con acentos a caracteres sin acentos
iconv -f UTF-8 -t ASCII//TRANSLIT -c ./data/orders.csv > ./data/aws/orders_temp.csv

# Eliminar columnas id, buyer_first_name y buyer_last_name
###### Done
awk 'BEGIN {FS=OFS=","} {for (i=1; i<=NF; i++) if (i != 1 && i != 9 && i != 10) printf "%s%s", $i, (i==NF?ORS:OFS)}' ./data/aws/orders_temp.csv > ./data/aws/orders_temp2.csv

# Crear nueva columna id como índice
awk -F ',' 'BEGIN {OFS=","} {print ($1 == "1" ? "id" : NR-1), $0}' ./data/aws/orders_temp2.csv > ./data/aws/orders_temp3.csv

# Utiliza awk para realizar el cambio en el primer registro de 0 a id
awk 'BEGIN {FS=OFS=","} NR==1 {$1="id"} {print}' ./data/aws/orders_temp3.csv > ./data/aws/orders_clean.csv

# Limpiar archivos temporales
rm  ./data/aws/orders_temp.csv
rm  ./data/aws/orders_temp2.csv
rm  ./data/aws/orders_temp3.csv

echo "Proceso completado."
