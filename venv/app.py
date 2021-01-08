import dbcreds
import mariadb

conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)

cursor = conn.cursor()

cursor.execute("INSERT INTO user(email, username, bio, birthdate, password) VALUES ('test@gmail.com', 'testuser3', 'test bio', '2020-01-01', 'password')")

cursor.execute("SELECT * FROM user")
user_list = cursor.fetchall()
for user in user_list:
    print(user[0])


conn.commit()
cursor.close()
conn.close()