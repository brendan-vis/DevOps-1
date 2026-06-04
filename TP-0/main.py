from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

compteur = 0
INSTANCE_ID = os.getenv("INSTANCE_ID", str(uuid.uuid4()))  # généré une seule fois au démarrage
START_TIME = datetime.now(timezone.utc)  # heure de démarrage

donnees = {
    'lieux': [
        'Paris',
        'Lyon',
        'Marseille',
        'Montpellier',
        'Toulon',
        'Lilles',
        'Nantes']
}

@app.middleware("http")
async def compter_requetes(request: Request, call_next):
    global compteur
    compteur += 1              # 1. s'exécute AVANT la route
    response = await call_next(request)  # 2. appelle la route
    return response            # 3. retourne la réponse au client


@app.get("/ping")
async def get_lieux():
    # renvoyer nos données et 200 code OK
    return {'donnees': donnees}

@app.get("/stats")
async def get_stat():
    uptime = datetime.now(timezone.utc) - START_TIME
    return {
        'instance_id': INSTANCE_ID,
        'requetes_depuis_demarrage': compteur,
        'uptime': str(uptime).split('.')[0]  # format lisible HH:MM:SS
    }

@app.api_route("/ping", methods=["POST", "PUT", "DELETE", "PATCH"])
async def ping_not_allowed():
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

if __name__ == "__main__":
    load_dotenv()
    PORT = int(os.getenv("PING_LISTEN_PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=PORT)


# @app.post("/lieux")
# async def post_lieu(lieu: str):
#     # si le lieu est déjà présent, nous ne l'ajoutons pas aux données
#     if lieu in donnees['lieux']:
#         # donc retourner simplement la réponse avec un message disant qu'il existe déjà
#         return {'donnees': donnees, 'message': "l'emplacement existe déjà"}
    
#     # par contre s'il n'est pas présent, nous ajoutons le lieu aux données
#     else:
#         donnees['lieux'].append(lieu)
#         # réponse de retour
#         return {'donnees': donnees, 'message': "l'emplacement a été ajouté"}
    
# @app.delete("/lieux")
# async def delete_lieu(lieu: str):
#     # si le lieu est présent, supprimez-le
#     if lieu in donnees['lieux']:
#         donnees['lieux'].remove(lieu)
#         # réponse de retour confirmant la suppression
#         return {'data': donnees, 'message':'le lieu est supprimé'}
    
#     # s'il n'est pas présent, renvoyez simplement la réponse
#     else:
#         return {'data': donnees, 'message': "le lieu n'existe pas"}