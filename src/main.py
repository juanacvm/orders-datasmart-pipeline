import logging
import sys
from database import engine
from models import Base
from etl_logic import *

#Configuracion basica de log
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Se crea log
log = logging.getLogger(__name__)

def run_pipeline():
    log.info('Iniciando pipeline de Data Mart de Ventas en una Pizzeria...')
    try:
        


        log.info('Eliminado tablas existentes...')
        Base.metadata.drop_all(engine)

        
        log.info('Creando tablas dimensionales y hechos...')
        Base.metadata.create_all(engine)

        
        log.info('Extrayendo datos de ordenes...')
        raw_orders = get_orders_data()

        log.info('Extrayendo datos de detalle de las ordenes...')
        raw_order_details = get_order_details_data()
        
        log.info('Extrayendo datos de pizza...')
        raw_pizzas = get_pizzas_data()

        log.info('Extrayendo datos de categoria de pizza...')
        raw_pizza_details = get_pizza_types_data()

        log.info('Creando tabla dimensional de fecha...')
        dimDate = transform_dimensional_date_table(raw_orders)

        log.info('Creando tabla dimensional de horas...')
        dimTime = transform_dimensional_hour_table(raw_orders)

        log.info('Creando tabla dimensional de pizza...')
        dimPizza = transform_dimensional_pizza_table(raw_pizzas, raw_pizza_details)

        log.info('Creando tabla de hechos de ventas...')
        factSales = transform_fact_sales_table(raw_orders, raw_order_details, dimDate, dimTime, dimPizza)
        
        log.info('Optimizando tabla dimensional de pizza...')
        dimPizza = standarize_dimensional_pizza_table(dimPizza)

        log.info('Creando tabla dimensional (fecha) en Postgresql...')
        dimDate.to_sql(name='dim_date', con=engine, if_exists='append', index=False)

        log.info('Creando tabla dimensional (hora) en Postgresql...')
        dimTime.to_sql(name='dim_time', con=engine, if_exists='append', index=False)

        
        log.info('Creando tabla dimensional (pizza) en Postgresql...')
        dimPizza.to_sql(name='dim_pizza', con=engine, if_exists='append', index=False)
        
        log.info('Creando tabla de hechos (ventas) en Postgresql...')
        factSales.to_sql(name='fact_sales', con=engine, if_exists='append', index=False)
        
        log.info('¡Ha culminado la creacion del Data Mart de ventas!')
    
    except FileNotFoundError as e:
        log.error(f"No se ha podido cargar los documentos de datos: {e}")
        sys.exit(1)

    except ValueError as e:
        log.error(f"Hubo error con el procesamiento de datos {e}")
        sys.exit(1)

    except Exception as e:
        log.error(f"El proceso de pipeline se detuvo debido a un error inesperado {e}")
        sys.exit(1)


if __name__ == '__main__':
    run_pipeline()