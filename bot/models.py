from dotenv import dotenv_values
from sqlalchemy import Column, Integer, \
    ForeignKey, String, BigInteger, orm, create_engine


ENV = dotenv_values('../.env')
DB_USER = ENV['DB_USER']
DB_PASSWORD = ENV['DB_PASSWORD']
DB_HOST = ENV['DB_HOST']
DB_PORT = ENV['DB_PORT']
DB_NAME = ENV['DB_NAME']


engine = create_engine(f'postgresql+psycopg2://'
                       f'{DB_USER}:{DB_PASSWORD}'
                       f'@{DB_HOST}:{DB_PORT}/{DB_NAME}')

Base = orm.declarative_base()


class Stickers(Base):
    __tablename__ = 'Stickers'

    id = Column(Integer, primary_key=True)
    stickers_tg = Column(String)
    tg_users = Column(BigInteger, ForeignKey('Users.user_tg'))


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    user_tg = Column(BigInteger, unique=True)


Base.metadata.create_all(engine)
