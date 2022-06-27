from flask_app.config.mysqlconnection import connectToMySQL


class Favorite:
    db = "wineclub"

    @staticmethod
    def get_favorites_by_wine(data):
        query = "SELECT * FROM favorites LEFT JOIN users ON favorites.user_id = users.id WHERE favorites.wine_id = %(wine_id)s"
        results =  connectToMySQL(Favorite.db).query_db(query,data)

        if not results:
            return []

        favorites = []
        for row in results:
            if row["id"] == None:
                return []
            user_data = {
                "id" : row['id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : None,
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }

            favorites.append(user_data)
        
        return favorites 

    @staticmethod
    def get_favorites_by_user(data):
        query = "SELECT * FROM favorites LEFT JOIN users ON favorites.user_id = users.id WHERE users.id = %(user_id)s"
        results =  connectToMySQL(Favorite.db).query_db(query,data)

        if not results:
            return []

        favorites = []
        for row in results:
            if row["wine_id"] == None:
                return []
            favorites.append(row['wine_id'])

        return favorites

