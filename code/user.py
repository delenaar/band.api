import psycopg2
from flask_restful import Resource, reqparse


class User:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection = psycopg2.connect('dbname=bandsfollow user=postgres password=1234')
        cursor = connection.cursor()
        query = "SELECT * from users WHERE username=%s"
        result = cursor.execute(query, (username,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = none

        connection.close()
        return user
    @classmethod
    def find_by_id(cls,id):
        connection = db.connect('dbname=bandsfollow user=postgres password=1234')
        cursor = connection.cursor()
        query = "SELECT * from users WHERE id=%s"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = none

        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="this field cannot be blank"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="this field cannot be blank"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        connection = psycopg2.connect('dbname=bandsfollow user=postgres password=1234')
        cursor = connection.cursor()
        query = "INSERT INTO users(username,password) VALUES (%s, %s)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {'message': 'User created succesfully'}, 201
