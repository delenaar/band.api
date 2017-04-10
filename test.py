import psycopg2
db = psycopg2
connection = db.connect('dbname=bandsfollow user=postgres password=1234')

cursor = connection.cursor()

create_table = 'CREATE TABLE users (id int, username text, password text)'
cursor.execute(create_table)


user = (1,'martijn', '1234')
insert_query = "INSERT INTO users values (%s,%s,%s)"
cursor.execute(insert_query, user)
connection.commit()

cursor.close()
connection.close()
