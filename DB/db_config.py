from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

connection_string = 'postgresql+psycopg2://postgres:admin@localhost/flask-html'

# if you want to declare a class which will be mapped to a table
# then simply inherit from Base
Base = declarative_base()

# create table for every class that inherits from Base
def create_all_entities():
    Base.metadata.create_all(engine)


Session = sessionmaker()
engine = create_engine(connection_string, echo=True)
local_session = Session(bind=engine)