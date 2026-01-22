# LinkStream - Documentation Développeur

> Application web d'automatisation et centralisation des conversations LinkedIn

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📑 Table des matières

1. [Vue d'ensemble](#-vue-densemble)
2. [Architecture](#-architecture)
3. [Installation](#-installation)
4. [Configuration](#-configuration)
5. [Structure du code](#-structure-du-code)
6. [Workflows n8n](#-workflows-n8n)
7. [Base de données](#-base-de-données)
8. [API et intégrations](#-api-et-intégrations)
9. [Déploiement](#-déploiement)
10. [Résolution de problèmes](#-résolution-de-problèmes)

---

## Vue d'ensemble

**LinkStream** est une application développée dans le cadre d'un stage de première année BTS SIO SLAM chez OPS Imperium. Elle permet d'automatiser la récupération, 
le stockage et la consultation des conversations LinkedIn via une interface web intuitive:

- **Backend** : n8n (workflows) + Unipile API (LinkedIn)
- **Base de données** : Supabase (PostgreSQL)
- **Frontend** : Streamlit (Python)

### Objectifs

- Centraliser les messages LinkedIn et les contacts dans une base structurée  
- Automatiser la synchronisation via webhooks  
- Offrir une interface intuitive de consultation et d'envoi  

### Technologies utilisées

| Composant                  | Technologie                       |
|----------------------------|-----------------------------------|
| **Backend automatisation** | n8n (workflows cloud)             |
| **API unifiée**            | Unipile API                       |
| **Base de données**        | Supabase (PostgreSQL)             |
| **Frontend**               | Streamlit (Python)                |
| **Langages**               | Python 3.x, SQL                   |
| **Librairies Python**      | `requests`, `pandas`, `streamlit` |
| **IDE**                    | Visual Studio Code                |
| **Versioning**             | GitHub                            |

---

## Architecture

```
┌─────────────┐
│ Utilisateur │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  Streamlit (UI)  │  ← app.py
└──────┬───────────┘
       │
       ↓
┌──────────────────┐      ┌────────────────┐
│  Supabase API    │ ←───→│  PostgreSQL    │
│  (read-only)     │      │  (3 tables)    │
└──────────────────┘      └────────────────┘
       ↑                          ↑
       │                          │
┌──────────────────┐              │
│  n8n Workflows   │──────────────┘
│ (Automatisation) │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐      ┌────────────────┐
│  Unipile API     │ ←───→│   LinkedIn     │
└──────────────────┘      └────────────────┘
```

### Flux de données

1. **Authentification** : Streamlit → Unipile → account_id récupéré
2. **Notification** : Streamlit → webhook n8n (`/new_user_auth2`)
3. **Récupération auto** : n8n → Unipile (chats, messages, profils)
4. **Insertion BDD** : n8n → Supabase (3 workflows)
5. **Affichage** : Streamlit → Supabase RPC `get_messages()`
6. **Envoi message** : Streamlit → Unipile → LinkedIn

---

## Installation

### Prérequis

- Python 3.8+
- Compte [Unipile](https://unipile.com) (API key)
- Projet [Supabase](https://supabase.com) configuré
- Compte [n8n Cloud](https://n8n.cloud) ou self-hosted

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/juklau/app_automatisation.git
cd app_automatisation

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les secrets (voir section suivante)

# 5. Lancer l'application
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

---

## Configuration

### 1. Fichier `.streamlit/secrets.toml`

Créer ce fichier à la racine :

```toml
# Supabase
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"

# Unipile
UNIPILE_API_KEY_3 = "sk_live_xxxxx"

# Custom (votre provider_id LinkedIn)
my_provider_id = "urn:li:person:xxxxx"
```

**Important** : Ce fichier contient des informations sensibles. Ne **jamais** le committer sur GitHub:
```
.streamlit/secrets.toml
venv/
__pycache__/
```

### 2. Base de données Supabase

Créer les 3 tables suivantes :

**Table `linkedin_people`**
```sql
CREATE TABLE linkedin_people (
     row_id SERIAL PRIMARY KEY,
     id TEXT UNIQUE NOT NULL,
     full_name TEXT,
     first_name TEXT,
     last_name TEXT,
     headline TEXT,
     linkedin_url TEXT,
     profile_picture_url TEXT,
     company TEXT,
     title TEXT,
     location TEXT,
     account_id TEXT,
     provider_id TEXT,
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW()
);
```

**Table `linkedin_chats`**
```sql
CREATE TABLE linkedin_chats (
    row_id SERIAL PRIMARY KEY,
    id TEXT UNIQUE NOT NULL,
    folder TEXT,
    time_stamp TIMESTAMP,
    account_id TEXT,
    provider_id TEXT,
    account_type TEXT,
    attendee_provider_id TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Table `linkedin_messages`**
```sql
CREATE TABLE linkedin_messages (
   row_id SERIAL PRIMARY KEY,
   id TEXT UNIQUE NOT NULL,
   chat_row_id TEXT,
   chat_id TEXT,
   content TEXT,
   sender TEXT,
   created_at TIMESTAMP,
   seen BOOLEAN DEFAULT FALSE,
   deleted BOOLEAN DEFAULT FALSE,
   chat_provider_id TEXT,
   sender_attendee_id TEXT,
   is_from_me BOOLEAN,
   account_id TEXT,
   provider_id TEXT
);
```

**Fonction SQL `get_messages()`**

```sql
CREATE OR REPLACE FUNCTION get_messages()
RETURNS TABLE (
  message_id text,
  content text,
  sender text,
  full_name text,
  linkedin_url text,
  profile_picture_url text,
  created_at timestamp,
  chat_row_id text,
  is_from_me boolean,
  attendee_provider_id text,
  attendee_name text,
  account_id text,
  chat_id text,
  provider_id text
) 
LANGUAGE SQL AS $$
  SELECT
    lm.id AS message_id,
    lm.content,
    lm.sender,
    COALESCE(lp.full_name, lp2.full_name) AS full_name,
    COALESCE(lp.linkedin_url, lp2.linkedin_url) AS linkedin_url,
    COALESCE(lp.profile_picture_url, lp2.profile_picture_url) AS profile_picture_url,
    lm.created_at,
    lm.chat_row_id::text,
    lm.is_from_me,
    lc.attendee_provider_id,
    lp2.full_name AS attendee_name,
    lm.account_id,
    lm.chat_id,
    lm.provider_id
  FROM linkedin_messages lm
  LEFT JOIN linkedin_people lp ON lm.sender = lp.id
  LEFT JOIN linkedin_chats lc ON lm.chat_row_id = lc.row_id
  LEFT JOIN linkedin_people lp2 ON lc.attendee_provider_id = lp2.id
  ORDER BY lm.created_at DESC;
$$;
```

### 3. Webhooks Unipile

Dans le dashboard Unipile :
1. Créer un webhook **Messaging - Multiple events**
2. URL cible : `https://votre-instance.n8n.cloud/webhook/linkedin_webhook`
3. Événements : `message.received`, `message.sent`

### 4. Workflows n8n

Importer les 4 workflows JSON (non fournis ici pour raisons de sécurité) :
- `linkedin_chats.json` : Récupération conversations
- `subworkflow_linkedin_messages.json` : Traitement messages
- `subworkflow_linkedin_people.json` : Enrichissement profils
- `linkedin_register_webhook_unipile.json` - Enregistrement du webhook Unipile

---

##  Structure du code

```
LinkStream/
├── app.py                  # ⭐ Application principale (419 lignes)
├── venv/                   # Environnement virtuel (non versionné)
├── .streamlit/
│   └── secrets.toml        # Secrets (non versionné)
├── img/
│   └── icons8-linkedin-48.png
├── requirements.txt        # Dépendances Python
└── README.md               # Documentation utilisateur
```

### app.py - Fonctions principales

| Fonction                        | Lignes  | Description                       |
|---------------------------------|---------|-----------------------------------|
| `generate_auth_link()`          | 18-69   | Génère lien auth Unipile (15 min) |
| `get_account_id_from_unipile()` | 73-100  | Récupère account_id après auth    |
| `post_auth_data_n8n()`          | 103-130 | Notifie n8n du nouvel utilisateur |
| `init_connection()`             | 177-181 | Connexion Supabase (cached)       |
| `run_query()`                   | 189-197 | Appel RPC `get_messages()`        |
| `post_message_to_linkedin()`    | 418-449 | Envoi message via Unipile         |

---

## Workflows n8n

### 1. linkedin_chats

**Objectif** : Récupérer et stocker les conversations

**Déclenchement** : 
- Webhook Unipile (nouveau message)
- Appel manuel depuis app.py

**Étapes clés** :
1. HTTP Request → `/chats` (Unipile API)
2. Loop Over Items → Traiter chaque chat
3. SQL Query → Vérifier existence (`row_id`)
4. Switch → Insérer si nouveau
5. Execute Workflow → `linkedin_messages`

### 2. subworkflow_linkedin_messages

**Objectif** : Récupérer et stocker les messages de chaque conversation

**Déclenchement** : Appelé par `linkedin_chats`

**Étapes clés** :
1. HTTP Request → `/chats/{id}/messages`
2. Transform → Formatage données
3. SQL Query → Vérifier doublons
4. Supabase Insert → Nouveaux messages
5. Execute Workflow → `linkedin_people`

### 3. subworkflow_linkedin_people

**Objectif** : Enrichir les profils utilisateurs

**Étapes clés** :
1. HTTP Request → `/users/{provider_id}`
2. Transform → Formatage
3. Supabase Insert → Si nouveau profil

---

## Base de données

### Modèle relationnel

```
linkedin_people (utilisateurs)
├── row_id (PK, auto-incrémenté)
├── id (UNIQUE, NOT NULL) ← LinkedIn ID
├── full_name
├── profile_picture_url
├── linkedin_url
└── ...

linkedin_chats (conversations)
├── row_id (PK, auto-incrémenté)
├── id (UNIQUE, NOT NULL) ← LinkedIn chat_id
├── account_id
├── attendee_provider_id (FK → linkedin_people.id)
└── ...

linkedin_messages (messages)
├── row_id (PK, auto-incrémenté)
├── id (UNIQUE, NOT NULL) ← LinkedIn message_id
├── chat_row_id (FK → linkedin_chats.row_id)
├── sender (FK → linkedin_people.id)
├── content
├── is_from_me
└── created_at
```

### Relations

- **1 utilisateur ↔ N conversations** (participant)
- **1 conversation ↔ N messages** (échanges)

---

## API et intégrations

### Unipile API

**Base URL** : `https://api18.unipile.com:14803/api/v1`

| Endpoint                | Méthode  | Utilisé dans            | Ligne app.py |
|-------------------------|----------|-------------------------|--------------|
| `/hosted/accounts/link` | POST     | Génération lien auth    | 21           |
| `/accounts`             | GET      | Récupération account_id | 75           |
| `/chats/{id}/messages`  | POST     | Envoi message           | 419          |
| `/chats`                | GET      | *N8n uniquement*        | -            |
| `/chats/{id}/messages`  | GET      | *N8n uniquement*        | -            |
| `/users/{provider_id}`  | GET      | *N8n uniquement*        | -            |

**Headers requis** :
```python
headers = {
    "X-API-KEY": st.secrets["UNIPILE_API_KEY_3"],
    "Content-Type": "application/json",
    "accept": "application/json"
}
```

### Supabase API

**Base URL :** `https://your-project.supabase.co`

**Méthode d'accès :** Utilisation du SDK Python `supabase-py` (pas d'appels REST directs)

**Opération unique dans app.py** :

```python
from supabase import create_client

# Connexion
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Lecture messages (RPC - Remote Procedure Call)
messages = supabase.rpc("get_messages").execute().data
```

**Note importante** : L'application Streamlit ne fait **QUE de la lecture**.
Les insertions sont gérées exclusivement par les workflows n8n.

### Webhook n8n

**URL** : `https://juklau.app.n8n.cloud/webhook/new_user_auth2`

**Payload** :
```json
{
  "account_id": "acc_xxxxx"
}
```

---

## Dépendances

### requirements.txt

```
streamlit==1.47.0
pandas==2.3.1
requests==2.32.4
supabase==2.10.0
python-dateutil==2.9.0.post0
```

### Rôle de chaque package

| Package           | Utilisation                             |
|-------------------|-----------------------------------------|
| `streamlit`       | Interface web, session state, cache     |
| `pandas`          | Manipulation DataFrames, tri/filtrage   |
| `requests`        | Appels API Unipile (auth, messages)     |
| `supabase`        | Client BDD (SDK Python, RPC)            |
| `python-dateutil` | Formatage timestamps (`%H:%M %d/%m/%Y`) |

---

## Déploiement

### Docker (optionnel)

**Dockerfile** :
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml** :
```yaml
version: '3.8'

services:
  linkstream:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./.streamlit/secrets.toml:/app/.streamlit/secrets.toml:ro
    restart: unless-stopped
```

```bash
# Build
docker-compose build

# Lancer
docker-compose up -d

# Vérifier les logs
docker-compose logs -f linkstream
```
---

## Résolution de problèmes

### Problème : Aucun message affiché

**Cause** : `chat_row_id` manquant dans les messages

**Solution** :
```sql
-- Vérifier que get_messages() retourne bien chat_row_id
SELECT * FROM get_messages() LIMIT 1;
```

### Problème : Erreur d'authentification Unipile

**Cause** : Clé API invalide ou expirée

**Solution** :
1. Vérifier `UNIPILE_API_KEY_3` dans `.streamlit/secrets.toml`
2. Tester l'API manuellement :
```bash
curl -H "X-API-KEY: sk_live_xxxxx" \
  https://api18.unipile.com:14803/api/v1/accounts
```

### Problème : Connexion Supabase échouée

**Solution** :
```python
# Dans app.py, décommenter pour debug :
st.write("SUPABASE_URL:", st.secrets["SUPABASE_URL"])
st.write("SUPABASE_KEY:", st.secrets["SUPABASE_KEY"][:10] + "...")
```

### Problème : Erreur d'insertion avec noms accentués (ex: "Cédric")

**Cause** : Problème d'encodage avec nœud HTTP Request

**Solution** : Le remplacer par nœud Supabase natif de n8n

### Problème : Photo du contact incorrect

**Cause** : Jointure SQL incomplète dans `get_messages()`

**Solution** : Vérifier que la fonction utilise bien :
```sql
LEFT JOIN linkedin_people lp2 ON lc.attendee_provider_id = lp2.id
```

### Problème : Rafraîchissement infini

**Cause** : `st.rerun()` mal placé

**Solution** : S'assurer qu'il est uniquement dans :
```python
if prompt := st.chat_input("Rédigez un message"):
    post_message_to_linkedin(prompt, chat_id_choisi, account_id, provider_id)
    st.rerun()  # ← Uniquement ici
```

---

## Ressources

### Documentation

- [Streamlit Docs](https://docs.streamlit.io/)
- [Supabase Docs](https://supabase.com/docs)
- [Unipile Developer Docs](https://developer.unipile.com/docs)
- [n8n Docs](https://docs.n8n.io/)
- [Pandas Docs](https://pandas.pydata.org/docs/)

### Tutoriels

- [n8n YouTube - Workflows](https://www.youtube.com/watch?v=sh6K862NAkk)
- [Streamlit Tutorial](https://www.youtube.com/watch?v=ITF1IzvfHmA)
- [Docker Basics](https://www.youtube.com/watch?v=P3uvEikM_T0)

### Communauté

- [n8n Community Forum](https://community.n8n.io/)
- [Streamlit Community](https://discuss.streamlit.io/)
- [Supabase Discord](https://discord.supabase.com/)

---

## Auteur

**Klaudia Juhasz**  
Étudiante BTS SIO SLAM (session 2026)  
Stage réalisé chez **OPS Imperium**, Nice (juillet-août 2025)  
Encadré par M. Victor Langlois

**GitHub** : [juklau/app_automatisation](https://github.com/juklau/app_automatisation)

---

## Licence

MIT License - Libre d'utilisation avec mention de l'auteur

---

**Dernière mise à jour** : Janvier 2025
