from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Wine:
    db = "wineclub"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.description = data['description']
        self.price = data['price']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_favorite = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO wines (name, type, description, price, user_id) VALUES (%(name)s,%(type)s,%(description)s,%(price)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)




    @classmethod
    def get_all(cls):
        query = "SELECT * FROM wines JOIN users on wines.user_id=users.id;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_wines = []
        for row in results:
            wine = cls(row)
            user_data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"],

            }
            wine.user = user.User(user_data)
            all_wines.append(wine)
        return all_wines


    @staticmethod
    def validate_wine(wine):
        is_valid = True
        if len(wine['name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters","wine")
        if len(wine['type']) < 2:
            is_valid = False
            flash("Type must be at least 2 characters","wine")
        if len(wine['price']) < 2:
            is_valid = False
            flash("Price must be at least 2 characters","wine")
        if len(wine['description']) < 2:
            is_valid = False
            flash("Description must be at least 2 characters","wine")
        return is_valid

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM wines JOIN users ON wines.user_id=users.id WHERE wines.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        wine = cls(row)
        user_data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"],
            }
        wine.user = user.User(user_data)
        return wine

    @classmethod
    def update(cls, data):
        query = "UPDATE wines SET name=%(name)s, type=%(type)s, price=%(price)s, description=%(description)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
        
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM wines WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def favorites(cls, data):
        query = "INSERT INTO favorites (wine_id, user_id) VALUES (%(wine_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unfavorites(cls, data):
        query = "DELETE FROM favorites WHERE wine_id = %(wine_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
