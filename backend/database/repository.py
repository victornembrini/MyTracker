from database.connection import db
import database.schemas as schemas


def get_all_exercices():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Exercices")
        data = cursor.fetchall()
        return data


def create_user(user_data):
    # 1. On réserve la table au restaurant (ouverture de la connexion)
    with db.get_connection() as conn:
        # 2. On appelle le serveur
        cursor = conn.cursor()

        # 3. On prépare la commande (la requête SQL).
        # Les "?" sont cruciaux : ils empêchent les hackers de pirater la base (Injection SQL)
        requete_sql = """
            INSERT INTO Users (username, password_hash, body_weight, height, birthdate) 
            VALUES (?, ?, ?, ?, ?)
        """

        # 4. On prépare les ingrédients (on extrait les données du colis Pydantic)
        # (Note: pour l'instant on met le password en clair, on rajoutera la sécurité du hashage plus tard)
        valeurs = (
            user_data.username,
            user_data.password,
            user_data.body_weight,
            user_data.height,
            user_data.birthdate,
        )

        cursor.execute(requete_sql, valeurs)

        conn.commit()

        return cursor.lastrowid
