# LinkStream  
### Le courant d'infos de votre réseau LinkedIn

---

## Description du projet

**LinkStream** est une application web interactive développée avec **Streamlit**, **Supabase**, **Unipile API** et **n8n**, permettant de :

- Récupérer automatiquement les conversations et messages LinkedIn.  
- Les stocker dans une base de données relationnelle **Supabase (PostgreSQL)**.  
- Les afficher dans une interface simple et ergonomique.  
- Envoyer de nouveaux messages directement depuis l'application.

Cette solution a été développée dans le cadre d’un projet professionnel au sein de **OPS Imperium**, société spécialisée en IA et automatisation, lors d’un stage de BTS SIO SLAM.

---

## Contexte et objectifs

n8n est utilisé pour automatiser la collecte et le traitement des données issues de LinkedIn via **l’API Unipile**, tandis que **Streamlit** sert d’interface frontend pour consulter et interagir avec ces données.

Objectifs principaux :
- **Centraliser** les messages et conversations LinkedIn.  
- **Visualiser** les échanges sous forme de tableau ou de fil de discussion.  
- **Interagir** avec les conversations (lecture et envoi de messages).  
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
- n8n : automatisation de la collecte et du traitement des messages.
- Supabase : stockage structuré et accès via API.

### Frontend

Streamlit (Python) : interface graphique permettant :
- l’authentification utilisateur via Unipile ;
- la visualisation des conversations ;
- l’envoi de nouveaux messages LinkedIn.

---

## Technologies utilisées

```
  | Composant       | Outil / Technologie              |
  | --------------- | -------------------------------- |
  | Frontend        | Streamlit (Python)               |
  | Backend         | n8n (workflows d’automatisation) |
  | API             | Unipile                          |
  | Base de données | Supabase (PostgreSQL)            |
  | Déploiement     | Docker / Docker Compose          |
  | IDE             | Visual Studio Code               |
  | Versioning      | GitHub                           |

```
---

## Structure du projet

```
  📁 LinkStream/
  │
  ├── app.py            # Application principale Streamlit
  ├── venv              # Environnement virtuel Python (non versionné)
  ├── workflows/        # Workflows d’automatisation n8n => retirer pour la sécurité des données
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
  source venv/bin/activate   # (ou venv\Scripts\activate sous Windows)
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

##Fonctionnement général

***1. Authentification***
- Un lien d’authentification est généré via Unipile API (generate_auth_link()).
- Après validation, l’utilisateur est redirigé vers LinkStream.
- L’account_id LinkedIn est récupéré et transmis à n8n.

***2. Récupération des données***
- n8n reçoit les webhooks d’Unipile (nouveaux messages, chats).
- Les workflows traitent les données (nettoyage, enrichissement, insertion dans Supabase).

***3. Affichage dans Streamlit***
L’application affiche :
- la liste des conversations,
- les messages échangés (photo, nom, heure, texte),
- le profil utilisateur.

***4. Envoi de messages***
- L’utilisateur peut envoyer un message LinkedIn directement depuis Streamlit.
- La requête POST est transmise à l’API Unipile, puis synchronisée via n8n.

---

## Tests et validation
- Tests unitaires : sur les fonctions d’authentification, d’insertion et de récupération.
- Tests d’intégration : communication entre Unipile ↔ n8n ↔ Supabase ↔ Streamlit.
- Tests utilisateurs : simulation complète d’un échange LinkedIn (authentification → affichage → envoi).

---

## Améliorations futures
- Implémentation OAuth complète pour LinkedIn.
- UI responsive et personnalisée.
- Intégration d’autres réseaux (Gmail, WhatsApp, Messenger).
- Suggestions automatiques de réponse via IA générative.
- Recherche et filtrage avancés des conversations.
- Rafraîchissement automatique en temps réel.

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




