from sqlalchemy import create_engine
from DataBaseDir.DataBaseSchema import Base


class DataBase:
    __count = 0
    engine = None

    def __init__(self):
        # Verify singleton
        if DataBase.__count == 0:
            # Connect to the database
            engine = create_engine('sqlite:///database.db')
            # Create all tables defined in the schema models
            Base.metadata.create_all(bind=engine)
            self.engine = engine
            DataBase.__count += 1
        else:
            print("Sorry, this class is intended to be a singleton - no more than one object should be instantiated.")




