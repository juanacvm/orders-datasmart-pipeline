from sqlalchemy import Column 
from sqlalchemy.types import Integer, Numeric, Boolean, VARCHAR, DATE, TIME
from sqlalchemy.orm import declarative_base 

Base = declarative_base()

#Crea tabla dimensional de fechas
class Dates(Base):
    __tablename__ = 'dim_date'
    date_id = Column(Integer, primary_key=True, autoincrement = False)
    date = Column(DATE)
    year = Column(Integer)
    month = Column(VARCHAR(10))
    day = Column(VARCHAR(10))
    month_name_eng = Column(VARCHAR(15))
    month_name_spa = Column(VARCHAR(15))
    day_name_eng = Column(VARCHAR(15))
    day_name_spa = Column(VARCHAR(15))
    quarter = Column(Integer)
    is_weekend = Column(Boolean)

#Crea tabla dimensional de tiempo
class Times(Base):
    __tablename__ = 'dim_time'
    time_id = Column(Integer, primary_key=True, autoincrement = False)
    time = Column(TIME)
    hour = Column(Integer)
    minutes = Column(Integer)
    time_ampm = Column(VARCHAR(20))
    moment_day = Column(VARCHAR(20))
    is_rushhour = Column(Boolean)

#Crea la tabla dimensional de Pizzas
class Pizzas(Base):
    __tablename__ = 'dim_pizza'
    id = Column(Integer, primary_key=True, autoincrement = False)
    name = Column(VARCHAR(250))
    category = Column(VARCHAR(100))
    size = Column(VARCHAR(10))
    price = Column(Numeric(19,2))

#Crea la tabla de hechos de ventas
class Sales(Base):
    __tablename__ = 'fact_sales'
    order_id = Column(Integer)
    order_details_id = Column(Integer, primary_key=True, autoincrement = False)
    date_id = Column(Integer)
    time_id = Column(Integer)
    pizza_id = Column(Integer)
    quantity = Column(Integer)
    unit_price = Column(Numeric(19,2))
    total_price = Column(Numeric(19,2))