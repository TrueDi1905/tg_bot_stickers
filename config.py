from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from models import Users, Stickers

q = select([Users])
r = conn.execute(s)
print(r.fetchall())

#user = Users(user_tg=1)
#s.add(user)
#s.commit()

#sticker = Stickers(stickers_tg=1, tg_users=1)
#s.add(sticker)
#s.commit()










## Курсор для выполнения операций с базой данных
#cursor = connection.cursor()
## Распечатать сведения о PostgreSQL
#print("Информация о сервере PostgreSQL")

#connection.autocommit = True
#with connection.cursor() as cursor:
#        cursor.execute(
#                """CREATE TABLE users(
#                id serial PRIMARY KEY,
#                name VARCHAR(50) NOT NULL);"""
#        )


#with connection.cursor() as cursor:
#        cursor.execute("""INSERT INTO users (name) VALUES ('DIMA')""")


#with connection.cursor() as cursor:
#        cursor.execute("""SELECT * FROM users""")
#        print(cursor.fetchone())