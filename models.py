from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


engine = create_engine('postgresql://truedi1905:chelsea1905@localhost:5432/postgres_db', echo=True)

Base = declarative_base()


class Stickers(Base):
    __tablename__ = 'Stickers'

    id = Column(Integer, primary_key=True)
    stickers_tg = Column(Integer)
    tg_users = Column(Integer, ForeignKey('Users.user_tg'))


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    user_tg = Column(Integer, unique=True)


Base.metadata.create_all(engine)
