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

<br>
<br>

# WIK-DPS-TP02 — Dockerisation d'une API FastAPI

## Description

Ce projet consiste à dockeriser une API REST développée en Python avec FastAPI (issue du TP01 `WIK-DPS-TP01`).  
Deux images Docker sont fournies : une image single-stage et une image multi-stage.

---

## Prérequis

- Docker installé sur la machine
- Le fichier `requirements.txt` doit contenir au minimum :
  ```
  fastapi
  uvicorn
  python-dotenv
  ```

---

## Image 1 — Single Stage

### Objectif

Image simple, un seul stage, optimisée pour le **cache des layers** lors des modifications du code source.

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN useradd -m brendan

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER brendan

EXPOSE 8000

CMD ["python", "main.py"]
```


### Build & Run

```bash
docker build -f Dockerfile -t serveur-docker .   
docker run -d -p 8080:8080 -e PING_LISTEN_PORT serveur-docker
```

---

## Image 2 — Multi-Stage

### Objectif

Image en deux stages : un stage de **build** (installation des dépendances) et un stage d'**exécution** (image finale légère, sans les sources du stage builder).

### Dockerfile

```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

RUN useradd -m brendan

COPY --from=builder /install /usr/local

COPY . .

USER brendan

EXPOSE 8000

CMD ["python", "main.py"]
```


### Build & Run

```bash
docker build -f Dockerfile.multistage -t serveur-docker-multistage .    
docker run -d -p 8080:8080 -e PING_LISTEN_PORT serveur-docker-multistage
```

---

## API — Endpoints disponibles

| Méthode | Route   | Description                                      |
|---------|---------|--------------------------------------------------|
| GET     | `/ping` | Retourne la liste des lieux                      |
| GET     | `/stats`| Retourne l'instance ID, l'uptime et le nb de requêtes |
| POST/PUT/DELETE/PATCH | `/ping` | Retourne 404 Not Found          |

---

## Variables d'environnement

| Variable            | Valeur par défaut     | Description                        |
|---------------------|-----------------------|------------------------------------|
| `PING_LISTEN_PORT`  | `8000`                | Port d'écoute du serveur           |
| `INSTANCE_ID`       | UUID généré au démarrage | Identifiant unique de l'instance |

---


## Scan de vulnérabilités

Scanner l'image avec l'un des outils suivants :

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image serveur-docker 

docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image serveur-docker-multistage 
```