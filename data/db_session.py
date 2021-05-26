import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm.session import sessionmaker

SqlAlchemyBase = dec.declarative_base()

__factory = None

def global_init():
    global __factory

    if __factory:
        return

    try:
        conn_str = open('./data/auth.txt').read()
    except FileNotFoundError:
        raise FileNotFoundError('создайте и укажите данные для подключения к базе данных в файле data/auth.txt')
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()