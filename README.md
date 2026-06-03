# Serveur FastAPI — `/ping`

Serveur HTTP minimaliste en Python avec FastAPI, exposant une route `GET /ping` retournant une liste de lieux, ainsi qu'une route `GET /stats` pour monitorer l'instance.

---

## Prérequis

- Python 3.10+
- pip

---

## Installation

```bash
pip install fastapi uvicorn python-dotenv
```

---

## Configuration

Crée un fichier `.env` à la racine du projet :

```env
PING_LISTEN_PORT=8080
```

| Variable | Description | Défaut |
|---|---|---|
| `PING_LISTEN_PORT` | Port d'écoute du serveur | `8000` |

---

## Lancement

```bash
python main.py
```

Le serveur démarre sur `http://127.0.0.1:<PORT>`.

---

## Routes

### `GET /ping`

Retourne la liste des lieux.

**Réponse `200 OK` :**
```json
{
  "donnees": {
    "lieux": ["Paris", "Lyon", "Marseille", "Montpellier", "Toulon", "Lilles", "Nantes"]
  }
}
```

### `GET /stats`

Retourne les informations de monitoring de l'instance.

**Réponse `200 OK` :**
```json
{
  "instance_id": "a3f2c1d4-9b8e-4c2a-bf10-123456789abc",
  "requetes_depuis_demarrage": 7,
  "uptime": "0:02:22"
}
```

| Champ | Description |
|---|---|
| `instance_id` | Identifiant unique généré au démarrage (UUID v4) |
| `requetes_depuis_demarrage` | Nombre total de requêtes reçues depuis le lancement |
| `uptime` | Temps écoulé depuis le démarrage au format `HH:MM:SS` |

### Toute autre méthode sur `/ping`

Retourne une réponse `404 Not Found` :
```json
{
  "detail": "Not Found"
}
```

---

## Exemples

```bash
# GET - récupérer les lieux
curl http://127.0.0.1:8000/ping
```

---

## Structure du projet

```
.
├── main.py       # Application FastAPI
├── .env          # Variables d'environnement
|── .gitignore
└── README.md
```