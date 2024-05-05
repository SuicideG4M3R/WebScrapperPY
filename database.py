from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def connect_to_database():
    engine = create_engine('sqlite:///myDatabase.db')
    Base = declarative_base()

    class House(Base):
        __tablename__ = 'Houses'

        id = Column(Integer, primary_key=True)
        url = Column(String, unique=True)
        title = Column(String)
        price = Column(String)
        location = Column(String)
        area = Column(String)
        rent = Column(String)
        number_of_rooms = Column(String)
        deposit = Column(String)
        floor = Column(String)
        type_of_construction = Column(String)
        available_from = Column(String)
        additional = Column(String)
        remote_service = Column(String)
        finishing_condition = Column(String)
        additional_info_1 = Column(String, nullable=True)
        additional_info_2 = Column(String, nullable=True)
        additional_info_3 = Column(String, nullable=True)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session, House


def add_to_database(session, House, url
                    , title, price, location, area, rent, number_of_rooms, deposit, floor,
                    type_of_construction, available_from, additional, remote_service, finishing_condition, *args
                    ):
    new_house = House(url=url
                           , title=title, price=price, location=location, area=area, rent=rent,
                           number_of_rooms=number_of_rooms, deposit=deposit, floor=floor,
                           type_of_construction=type_of_construction, available_from=available_from,
                           additional=additional, remote_service=remote_service,
                           finishing_condition=finishing_condition
                           )
    session.add(new_house)
    session.commit()
    session.refresh(new_house)
    print(f'Added new entry to the database: {new_house.url}')
    return new_house


def check_if_already_in_database(session, House, url):
    return session.query(House).filter_by(url=url).first()


def close_connection(session):
    session.close()


def print_data(session, table):
    print(f'Showing table: {table.__tablename__}')
    print(f'Entries: {session.query(table).count()}')
    for row in session.query(table).all():
        record_data = vars(row)
        columns_data = {col: record_data[col] for col in record_data if not col.startswith('_')}
        print('')
        for key, value in columns_data.items():
            print(f'{key}: {value}')
