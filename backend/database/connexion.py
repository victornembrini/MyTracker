import sqlite3
import threading
from contextlib import contextmanager


class DatabaseSingleton:
    _instance = None
    _lock = threading.Lock()  # Le fameux "videur" pour gérer la concurrence

    def __new__(cls):
        """
        Cette méthode magique garantit la création d'une instance UNIQUE.
        Même si 10 utilisateurs appellent la classe, ils auront le même objet.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseSingleton, cls).__new__(cls)
                cls._instance.db_path = "muscu.db"
        return cls._instance

    @contextmanager
    def get_connection(self):
        """
        Le Context Manager (le robinet).
        Il s'assure d'ouvrir et de fermer la connexion proprement.
        """
        # check_same_thread=False est requis car FastAPI gère plusieurs requêtes en même temps (multithreading)
        conn = sqlite3.connect(self.db_path, check_same_thread=False)

        # Astuce très utile : permet de recevoir les données SQL sous forme
        # de dictionnaire (ex: ligne['username']) au lieu d'un tuple illisible (ex: ligne[1])
        conn.row_factory = sqlite3.Row

        try:
            yield conn  # On "prête" la connexion au code qui l'a demandée
        finally:
            conn.close()  # Le ménage automatique quoi qu'il arrive (même en cas de crash)


# On crée l'instance unique qui sera importée par FastAPI plus tard
db = DatabaseSingleton()


# ==========================================
# 🧪 SCRIPT DE TEST (À exécuter localement)
# ==========================================
if __name__ == "__main__":
    print("Tentative de connexion à la base...")

    try:
        # On teste notre context manager avec le mot-clé 'with'
        with db.get_connection() as connexion_test:
            cursor = connexion_test.cursor()

            # On interroge SQLite pour qu'il nous donne la liste de tes tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            print("\n✅ Connexion réussie et gérée par le Singleton !")
            print("Voici les tables trouvées dans ton fichier muscu.db :")
            for table in tables:
                print(f" 🏋️ - {table['name']}")

    except Exception as e:
        print(f"\n❌ Erreur lors de la connexion : {e}")
