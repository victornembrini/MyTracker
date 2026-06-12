import sqlite3

# 1. Crée le fichier muscu.db et s'y connecte
conn = sqlite3.connect("muscu.db")
cursor = conn.cursor()

# 2. Ouvre ton fichier schema.sql et lit son contenu
with open("schema.sql", "r", encoding="utf-8") as fichier_sql:
    code_sql = fichier_sql.read()

# 3. Exécute tout le code SQL d'un coup
cursor.executescript(code_sql)

# 4. Sauvegarde et ferme la connexion
conn.commit()
conn.close()

print("✅ Base de données muscu.db créée avec succès !")
