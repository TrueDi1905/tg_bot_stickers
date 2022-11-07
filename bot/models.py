from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import declarative_base, relationship


engine = create_engine('postgresql+psycopg2://truedi1905:chelsea1905@localhost:5432/postgres_db')

Base = declarative_base()


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
