from fastapi import FastAPI
from database import repository
import database.schemas as schemas

# On initialise le "Menu" de notre API
app = FastAPI(title="MyTracker", description="1er backend")


# ---------------------------------------------------------
# 1. ROUTE D'ACCUEIL (GET)
# ---------------------------------------------------------
# Le décorateur @app.get indique que si quelqu'un tape l'URL de base,
# on exécute cette fonction. "GET" signifie qu'on veut juste LIRE une info.
@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API de Musculation ! Le serveur fonctionne 🚀"}


# ---------------------------------------------------------
# 2. ROUTE POUR LE CATALOGUE (GET)
# ---------------------------------------------------------
# Quand l'application mobile demande "/exercices", on appelle notre ouvrier.
@app.get("/exercices")
def liste_des_exercices():
    # On délègue le travail au repository ! FastAPI s'en fiche du SQL.
    data = repository.get_all_exercices()
    return {"exercices": data}


# ---------------------------------------------------------
# 3. ROUTE POUR CRÉER UN UTILISATEUR (POST)
# ---------------------------------------------------------
# "POST" signifie que le client ENVOIE de la donnée pour créer quelque chose.
# Magie de FastAPI : en mettant "user: schemas.UserCreate", FastAPI va
# AUTOMATIQUEMENT bloquer la requête si l'utilisateur ne respecte pas tes règles Pydantic !
@app.post("/users")
def inscrire_utilisateur(user: schemas.UserCreate):
    # Si le code arrive ici, c'est que la douane (Pydantic) a validé le colis.
    # On donne le colis validé à notre ouvrier.
    nouvel_id = repository.create_user(user)

    # On renvoie un reçu au client
    return {"message": "Utilisateur créé avec succès !", "user_id": nouvel_id}
