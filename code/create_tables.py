import psycopg2

connection = psycopg2.connect('dbname=bandsfollow user=postgres password=1234')
cursor = connection.cursor()

create_users = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username text, password text)"
cursor.execute(create_users)
connection.commit()
connection.close()
