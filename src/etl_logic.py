import pandas as pd
import numpy as np
import chardet
import os

#Metodo que lee el formato de los archivos CSV y los devuelve procesados
def smart_read_csv(file_path) -> pd.DataFrame:
    with open(file_path,'rb') as f:
        res = chardet.detect(f.read(1000))

    return pd.read_csv(file_path, encoding=res['encoding'], encoding_errors='replace')

#Metodo que busca el archivo order.csv y los envia a leer al metodo smart_read_csv
def get_orders_data() -> pd.DataFrame:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__)) #busca la direccion actual del script main
        file_path = os.path.join(script_dir,'../data/orders.csv') #busca la direccion del archivo .csv
        raw_orders = smart_read_csv(file_path)
        return raw_orders
    except FileNotFoundError as e:
        print(f"Error en extraer los datos de las ordenes: {e}")

#Metodo que busca el archivo order_details.csv y los envia a leer al metodo smart_read_csv
def get_order_details_data() -> pd.DataFrame:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__)) #busca la direccion actual del script main
        file_path = os.path.join(script_dir,'../data/order_details.csv') #busca la direccion del archivo .csv
        raw_orders = smart_read_csv(file_path)
        return raw_orders
    except FileNotFoundError as e:
        print(f"Error en extraer los datos del detalle de las ordenes: {e}")

#Metodo que busca el archivo pizzas.csv y los envia a leer al metodo smart_read_csv
def get_pizzas_data() -> pd.DataFrame:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        file_path = os.path.join(script_dir,'../data/pizzas.csv') 
        raw_orders = smart_read_csv(file_path)
        return raw_orders
    except FileNotFoundError as e:
        print(f"Error en extraer los datos de pizza: {e}")

#Metodo que busca el archivo pizza_types.csv y los envia a leer al metodo smart_read_csv
def get_pizza_types_data() -> pd.DataFrame:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir,'../data/pizza_types.csv')
        raw_orders = smart_read_csv(file_path)
        return raw_orders
    except FileNotFoundError as e:
        print(f"Error en leer los datos relacionados al tipo de pizza: {e}")

#Metodo que crea un DataFrame dimensional de fechas en base a la columna de fechas del DataFrame de pedidos
def transform_dimensional_date_table(raw_orders) -> pd.DataFrame:
    dimDate = pd.to_datetime(raw_orders['date'],errors='coerce').dt.strftime('%Y%m%d').astype(int).to_frame('date_id')
    dimDate = dimDate.drop_duplicates()
    dimDate['date'] = pd.to_datetime(raw_orders['date'], errors='coerce')
    dimDate['year'] = dimDate['date'].dt.year
    dimDate['month'] = dimDate['date'].dt.strftime('%m')
    dimDate['day'] = dimDate['date'].dt.strftime('%d')
    dimDate['month_name_eng'] = dimDate['date'].dt.month_name()
    dimDate['month_name_spa'] = dimDate['date'].dt.month_name(locale='es_ES')
    dimDate['day_name_eng'] = dimDate['date'].dt.day_name()
    dimDate['day_name_spa'] = dimDate['date'].dt.day_name(locale='es_ES')
    dimDate['quarter'] = dimDate['date'].dt.quarter
    dimDate['is_weekend'] = dimDate['date'].dt.weekday >= 5

    return dimDate

#Metodo que crea un DataFrame dimensional de horas en base a la columna de horas del DataFrame de pedidos
def transform_dimensional_hour_table(raw_orders) -> pd.DataFrame:
    dimTime = pd.to_datetime(raw_orders['time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H%M').astype(int).to_frame(name='time_id')
    dimTime = dimTime.drop_duplicates()
    dimTime['time'] = pd.to_datetime(raw_orders['time'], format='%H:%M:%S', errors='coerce')
    dimTime['hour'] = dimTime['time'].dt.hour
    dimTime['minutes'] = dimTime['time'].dt.minute
    dimTime['time_ampm'] = dimTime['time'].dt.strftime('%I:%M %p')

    time_conditions=[
        (dimTime['hour'] >= 0) & (dimTime['hour'] < 6),
        (dimTime['hour'] >= 6) & (dimTime['hour'] < 12),
        (dimTime['hour'] >= 12) & (dimTime['hour'] < 19),
        (dimTime['hour'] >= 19)
    ]

    time_results = ['night','morning', 'afternoon', 'night']

    dimTime['moment_day'] = np.select(time_conditions, time_results, default='Unknown')
    dimTime['is_rushhour'] = (((dimTime['hour'] >= 6) & (dimTime['hour'] < 9)) | ((dimTime['hour'] >= 18) & (dimTime['hour'] < 20)))

    return dimTime

#Crea el DF dimensional parcial de pizza en base a la información de pizzas
#Se deja parcialmente completado el proceso debido a que queda pendiente crea la tabla de hechos de ventas.
def transform_dimensional_pizza_table(raw_pizzas, raw_pizza_types) -> pd.DataFrame:
    dimPizza = pd.merge(raw_pizzas, raw_pizza_types, how= "left", on = "pizza_type_id")
    dimPizza['id'] = range(1, len(dimPizza) + 1)
    dimPizza = dimPizza.drop(
        columns = ['pizza_type_id', 'ingredients']
    )

    return dimPizza

#Se crea el DF de hechos de ventas a través de las tablas dimensionales
#Por medio de las llaves id para mantener la misma cantidad de registros
def transform_fact_sales_table(raw_orders, raw_orders_details, dimDate, dimTime, dimPizza) -> pd.DataFrame:
    factSales = pd.merge(raw_orders, raw_orders_details, how='left', on='order_id')
    factSales['date_id'] = pd.to_datetime(factSales['date'],errors='coerce').dt.strftime('%Y%m%d').astype(int)
    factSales = pd.merge(factSales, dimDate[['date_id','date']], on='date_id', how="left")
    factSales['time_id'] = pd.to_datetime(factSales['time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H%M').astype(int)
    factSales = pd.merge(factSales, dimTime[['time_id']], on='time_id', how="left")
    factSales = pd.merge(factSales, dimPizza[['id','pizza_id','price']], on = 'pizza_id', how='left')
    factSales['total_price'] = factSales['quantity'] * factSales['price']
    factSales = factSales.drop(
        columns = ['time','pizza_id']
    )
    factSales = factSales.rename(
        columns = {
            'price': 'unit_price',
            'id': 'pizza_id'
        }
    )
    factSales = factSales[['order_id','order_details_id','date_id','time_id','pizza_id','quantity','unit_price','total_price']]

    return factSales

#Metodo que elimina el identificador de la antigua tabla de pizzas y ordena el DF dimensional
def standarize_dimensional_pizza_table(dimPizza) -> pd.DataFrame:
    dimPizza = dimPizza.drop(
    columns= ['pizza_id']
    )
    dimPizza = dimPizza[['id','name','category','size','price']]
    return dimPizza