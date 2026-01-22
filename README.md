# LinkStream  
### Le courant d'infos de votre réseau LinkedIn

---

## Présentation du projet

**LinkStream** est une application web permettant de centraliser, automatiser et exploiter les conversations LinkedIn à partir d’une interface unique.

Le projet repose sur une architecture orientée automatisation et intégration d’API, combinant :
- **Unipile API** pour l’accès aux données LinkedIn,
- **n8n** pour l’orchestration des workflows,
- **Supabase (PostgreSQL)** pour le stockage structuré,
- **Streamlit** pour l’interface utilisateur.

Ce projet a été réalisé dans le cadre de mon **stage de première année de BTS SIO SLAM** au sein de l’entreprise **OPS Imperium**, spécialisée en automatisation et intelligence artificielle.

---

## Contexte et objectifs

L’outil d’automatisation **n8n** permet de récupérer et traiter efficacement des données via API, mais ne propose pas d’interface utilisateur pour consulter ou exploiter ces données.

L’objectif de LinkStream est donc de fournir une **interface web simple et fonctionnelle** permettant de :

- **Centraliser** les conversations et messages LinkedIn,
- **Visualiser** les échanges sous forme de fil de discussion,
- **Interagir** avec les conversations (lecture et envoi de messages),
- **Automatiser** la synchronisation des données entre LinkedIn, n8n et Supabase.

---

## Architecture du système

Le projet repose sur une architecture modulaire composée de quatre couches principales :

```text
[Utilisateur]
     ↓
[Frontend Streamlit]
     ↓
[API Supabase] ↔ [Base PostgreSQL]
     ↑
[n8n Workflows]
     ↑
[Webhooks Unipile ↔ LinkedIn]
```

### Backend

- Unipile API : interface d'accès aux données LinkedIn (messages, profils, conversations).
- n8n : automatisation des flux de données (webhooks, traitements, filtrage).
- Supabase : stockage relationnel (PostgreSQL) et accès via API.

### Frontend

Streamlit (Python) : interface graphique permettant :
- l’authentification utilisateur via Unipile ;
- la visualisation des conversations ;
- l’envoi de messages LinkedIn.

---

## Technologies utilisées

```
  | Composant              | Outil / Technologie              |
  | ---------------------- | -------------------------------- |
  | Frontend               | Streamlit (Python)               |
  | Automatisation         | n8n (workflows d’automatisation) |
  | API                    | Unipile                          |
  | Base de données        | Supabase (PostgreSQL)            |
  | IDE                    | Visual Studio Code               |
  | Versioning             | GitHub                           |

```
---

## Structure du projet

```
  📁 LinkStream/
  │
  ├── app.py                 # Application principale Streamlit
  ├── venv                   # Environnement virtuel Python (non versionné)
  ├── workflows/             # Workflows d’automatisation n8n => non inclus pour raisons de sécurité
  │   └── linkedin_chats.json
  │   └── linkedin_register webhook unipile(1).json
  │   └── register webhook unipile.json
  │   └── subworkflow _linkedin_messages.json
  │   └── subworkflow_linkedin_people.json
  ├── img/                   # Ressources visuelles (logos, icônes)
  │   └── icons8-linkedin-48.png
  ├── .streamlit/            # Configuration Streamlit
  │   └── secrets.toml       # Clés API et configuration (non versionné)
  └── README.md              # Documentation principale du projet

```
---

## Configuration des secrets
```
  # Supabase
  SUPABASE_URL = "https://your-supabase-url.supabase.co"
  SUPABASE_KEY = "your-supabase-key"
  
  # Unipile
  UNIPILE_API_KEY_3 = "your-unipile-api-key"
  
  # Custom
  my_provider_id = "your-provider-id"

```

---

## Installation et exécution

***Cloner le dépôt***
```
  git clone https://github.com/juklau/app_automatisation.git
  cd app_automatisation
```

***Créer un environnement virtuel***
```
  python3 -m venv venv
  source venv/bin/activate     # Linux / macOS
  # venv\Scripts\activate      # Windows
```

***Installer les dépendances***
```
  pip install -r requirements.txt
```

***Lancer l'application***
```
  streamlit run app.py
```

---

## Fonctionnement général

***1. Authentification***
- Génération d’un lien d’authentification via l’API Unipile (generate_auth_link()).
- Après validation, l’utilisateur est redirigé vers LinkStream.
- Récupération de l’***account_id*** LinkedIn.
- Transmission de l’identifiant à n8n pour déclencher les automatisations.

***2. Automatisation des données***
- Réception des webhooks Unipile dans n8n (nouveaux messages, chats).
- Traitement, enrichissement et insertion des données dans Supabase.
- Gestion des doublons et mises à jour automatiques.

***3. Affichage dans Streamlit***
- Liste des conversations LinkedIn.
- Affichage des messages (photo, nom, horodatage, contenu).
- Affichage du profil utilisateur.

***4. Envoi de messages***
- Envoi direct de messages LinkedIn depuis Streamlit.
- Synchronisation automatique via l’API Unipile et n8n.

---

## Tests et validation
- Tests unitaires : fonctions d’authentification et d’accès aux données (insertion, récupération).
- Tests d’intégration : communication entre Unipile ↔ n8n ↔ Supabase ↔ Streamlit.
- Tests utilisateurs : scénario complet (connexion → authentification → consultation → envoi).

---

## Améliorations futures
- Implémentation OAuth complète pour LinkedIn.
- Interface utilisateur responsive et personnalisée.
- Intégration multi-plateformes (Gmail, WhatsApp, Messenger).
- Suggestions automatiques de réponse via IA générative.
- Recherche et filtrage avancés des conversations.
- Rafraîchissement en temps réel.

---

## Auteur
Klaudia Juhasz
- Étudiante BTS SIO SLAM (session 2026)
- Projet réalisé au sein de OPS Imperium, Nice
- Encadré par M. Victor Langlois

**GitHub :** [juklau/app_automatisation](https://github.com/juklau/app_automatisation/tree/main)

---

## Licence
Ce projet est distribué sous licence MIT — vous êtes libre de le réutiliser et de le modifier, sous réserve de mentionner l’auteur.

## Aperçu du flux de données
Le schéma ci-dessous illustre les interactions entre les services :
- Unipile capture les messages LinkedIn.
- n8n orchestre les workflows d’automatisation.
- Supabase stocke et expose les données via API.
- Streamlit affiche les conversations dans une interface utilisateur intuitive.




