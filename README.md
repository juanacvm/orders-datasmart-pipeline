# Pipeline ETL para la creación de Data Mart de ventas

## Descripcion

Proyecto de datos que implementa un pipeline que integra ETL en Python que concluye con una creación de un almacen de datos (Data Mart) enfocado a las ventas de una pizzería. Extrae los datos de origen, estos son procesados y levantados en un **modelo estrella** de una base de datos relacional con el objetivo de maximizar el rendimiento de consultas durante el análisis de ventas.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ORIGEN DE DATOS                                │
│  ┌──────────┐  ┌───────────────┐  ┌──────────┐  ┌───────────────┐           │
│  │ orders   │  │ order_details │  │ pizzas   │  │ pizza_types   │           │
│  │  .csv    │  │     .csv      │  │  .csv    │  │     .csv      │           │
│  └────┬─────┘  └───────┬───────┘  └────┬─────┘  └───────┬───────┘           │
└───────┼────────────────┼───────────────┼────────────────┼───────────────────┘
        │                │               │                │
        v                v               v                v
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTRACCIÓN DE DATOS                                 │
│                    Pandas + chardet (encoding)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│                             TRANSFORMACIÓN                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  - Categorización de fechas (tabla dimensional fechas)              │    │
│  │  - Categorización de hora (momento del día, hora punta, AM/PM)      │    │
│  │  - Desnormalización de la tabla de pizzas                           │    │
│  │  - Creación de hechos en base llaves foráneas                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Creacion del modelo de datos                              │
│                   SQLAlchemy ORM + PostgreSQL                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODELO ESTRELLA                                     │
│                                                                             │
│      ┌───────────┐       ┌───────────┐       ┌───────────┐                  │
│      │ dim_date  │       │ dim_time  │       │ dim_pizza │                  │
│      │───────────│       │───────────│       │───────────│                  │
│      │ date_id   │       │ time_id   │       │ pizza_id  │                  │
│      │ year      │       │ hour      │       │ name      │                  │
│      │ month     │       │ minutes   │       │ category  │                  │
│      │ quarter   │       │ moment    │       │ size      │                  │
│      │ is_weekend│       │ is_rush   │       │ price     │                  │
│      └─────┬─────┘       └─────┬─────┘       └─────┬─────┘                  │
│            │                   │                   │                        │
│            └───────────────────┼───────────────────┘                        │
│                                v                                            │
│                       ┌─────────────────┐                                   │
│                       │   fact_sales    │                                   │
│                       │─────────────────│                                   │
│                       │ order_id        │                                   │
│                       │ date_id (FK)    │                                   │
│                       │ time_id (FK)    │                                   │
│                       │ pizza_id (FK)   │                                   │
│                       │ quantity        │                                   │
│                       │ total_price     │                                   │
│                       └─────────────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Tecnologias

- **Python 3.13**
- **Pandas y Numpy**: Para la transformación de datos
- **SQLAlchemy**: Para la creación de modelo de datos ORM
- **Python-dotenv**: Para la gestión de configuraciones de entorno
- **PostgreSQL**: Base de datos relacional


## Estructura

```
orders-datasmart-pipeline/
├── data/
│   ├── orders.csv
│   ├── order_details.csv
│   ├── pizzas.csv
│   └── pizza_types.csv
├── src/
│   ├── main.py            # Script principal de pipeline
│   ├── config.py          # Configuración de variables de entorno
│   ├── database.py        # Conexion PostgreSQL
│   ├── models.py          # Modelos ORM (dimensional)
│   └── etl_logic.py       # Logica de transformacion a dimensiones y hechos
├── notebooks/
│   └── script.ipynb       # Analisis exploratorio
├── .env.example
├── requirements.txt
└── README.md
```

## Instalacion y ejecución

```bash
# Clonar repositorio
git clone https://github.com/juanacvm/orders-datasmart-pipeline.git
cd orders-datasmart-pipeline

# Instalar dependencias Python
pip install -r requirements.txt

# Configurar variable de entorno
cp .env.example .env (modifica .env.example a .env)
# Editar .env con credenciales de PostgreSQL

# Ejecutar pipeline
python src/main.py
```

## Configuracion (.env)

```
DB_HOST=localhost
DB_PORT=5432 (u otro puerto habilitado)
DB_USER=postgres (u otro usuario con permisos de gestión de BD)
DB_PASS=contraseña_usuario
DB_NAME=dmsales
```

## Resultados

- ✅ Se generó un modelo estrella listo para consultas analíticas de ventas
- ✅ Diseño de tabla de fechas para análisis de tendencia de ventas según periodo
- ✅ Diseño de tabla de hora para evaluar rendimiento de ventas por turnos
- ✅ Métricas de crecimiento en ventas.
- ✅ Evaluación de pizzas más solicitadas (establecer ranking)