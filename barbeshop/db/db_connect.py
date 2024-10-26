from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

user = 'usernae'
password = ''
host = 'localhost'
database = 'dbname'

def get_connection():
    return create_engine(url=f"postgresql+psycopg2://{user}:{password}@{host}/{database}")

try:
    engine = get_connection()
    print(f'Connection to the {host} for user {user} created successfully.')
except Exception as ex:
    print(f'Connection could not be made due to the following error: {ex}.')

Session = sessionmaker(bind=engine)
session = Session()