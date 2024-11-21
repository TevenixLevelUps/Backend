from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

user = ''
password = ''
host = '127.0.0.1'
database = ''

def get_connection():
    return create_engine(url=f"postgresql+psycopg2://{user}:{password}@{host}/{database}")

try:
    engine = get_connection()
    print(f'Connection to the {host} for user {user} created sucessfully.')
except Exception as ex:
    print(f'Connection could not be made due to the following error: {ex}.')

Base.metadata.create_all(engine)