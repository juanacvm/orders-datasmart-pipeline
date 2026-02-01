from config import db_host, db_port, db_user, db_password, db_name
from sqlalchemy import create_engine


url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(url)