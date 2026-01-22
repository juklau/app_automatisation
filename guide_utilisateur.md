# LinkStream - Guide Utilisateur

> Gérez vos conversations LinkedIn depuis une interface simple et intuitive

[![Version](https://img.shields.io/badge/Version-1.0-blue.svg)]()
[![Support](https://img.shields.io/badge/Support-BTS%20SIO%20SLAM-green.svg)]()

---

## 📑 Sommaire

1. [Qu'est-ce que LinkStream ?](#-quest-ce-que-linkstream)
2. [Premiers pas](#-premiers-pas)
3. [Authentification LinkedIn](#-authentification-linkedin)
4. [Consulter vos conversations](#-consulter-vos-conversations)
5. [Envoyer des messages](#-envoyer-des-messages)
6. [Comprendre l'interface](#-comprendre-linterface)
7. [Questions fréquentes (FAQ)](#-questions-fréquentes-faq)
8. [Résolution de problèmes](#-résolution-de-problèmes)
9. [Aide et contact](#-aide-et-contact)

---

## Qu'est-ce que LinkStream ?

**LinkStream** est une application web qui centralise toutes vos conversations LinkedIn dans une interface unique et facile à utiliser.

### Fonctionnalités principales

-  **Consultation** de tous vos messages LinkedIn
- **Envoi** de nouveaux messages
- **Synchronisation automatique** avec LinkedIn
- **Affichage des profils** (photo, nom, lien LinkedIn)
- **Interface simple** sans installation nécessaire

---

## Premiers pas

### Prérequis

Vous avez besoin de :
- Un compte **LinkedIn** actif
- Un navigateur web moderne (Chrome, Firefox, Safari, Edge)
- Une connexion Internet

### Accéder à l'application

1. Ouvrez votre navigateur
2. Rendez-vous sur l'URL fournie par votre administrateur :
   ```
   http://localhost:8501
   ```
   *Ou l'URL de déploiement (ex: `https://linkstream.streamlit.app`)*

3. Vous arrivez sur la page d'accueil 

---

## Authentification LinkedIn

### Première connexion

Lors de votre première visite, vous devez connecter votre compte LinkedIn à LinkStream.

#### Étape 1 : Cliquer sur le bouton d'authentification

Sur la page d'accueil, vous verrez :

```
┌─────────────────────────────────────┐
│                                     │
│         LinkStream                  │
│  Le courant d'infos de votre réseau │
│                                     │
│   [Cliquez ici pour vous            │
│    authentifier]                    │
│                                     │
└─────────────────────────────────────┘
```

**Cliquez** sur le bouton bleu **"Cliquez ici pour vous authentifier"**

#### Étape 2 : Se connecter à LinkedIn

Une nouvelle page s'ouvre (Unipile Authentication Assistant) :

1. **Entrez votre email LinkedIn**
2. **Entrez votre mot de passe LinkedIn**
3. Cliquez sur **"Login"**

**Sécurité** : Vos identifiants LinkedIn ne sont **jamais** stockés par LinkStream. L'authentification passe par un service tiers sécurisé (Unipile).

#### Étape 3 : Retour à LinkStream

Une fois connecté à LinkedIn :

1. Vous êtes redirigé vers la page d'accueil de LinkStream
2. Cliquez sur le bouton **"J'ai terminé l'authentification"**
3. Vos conversations apparaissent automatiquement 

### Durée de la session

Votre connexion reste active tant que vous gardez LinkStream ouvert. Si vous fermez l'application, vous devrez vous reconnecter lors de votre prochaine visite.

---

## Consulter vos conversations

### Vue d'ensemble

Une fois authentifié, vous voyez :

```
┌─────────────────────────────────────────────────┐
│  LinkStream                                     │
│  Le courant d'infos de votre réseau             │
├─────────────────────────────────────────────────┤
│                                                 │
│  👤 [Votre photo]    Votre Nom                  │
│                      Profil                     │
│                      🔗 LinkedIn                │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Choisissez une conversation:                   │
│  ┌───────────────────────────────────────┐      │
│  │ Victor Langlois                    ▼  │      │
│  └───────────────────────────────────────┘      │
│                                                 │
│  Messages du chat avec Victor Langlois          │
│                                                 │
│  ┌─────────────────────────────────────┐        │
│  │ 👤 Victor Langlois                  │        │
│  │ 🕒 10:42 22/01/2025                 │        │
│  │ > Bonjour Klaudia, comment avances- │        │
│  │   tu sur le projet ?                │        │
│  └─────────────────────────────────────┘        │
│                                                 │
│  ┌─────────────────────────────────────┐        │
│  │ 👤 Klaudia Juhasz                   │        │
│  │ 🕒 10:45 22/01/2025                 │        │
│  │ > Très bien ! Je termine les tests. │        │
│  └─────────────────────────────────────┘        │
│                                                 │
│  [Rédigez un message                      >]    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Sélectionner une conversation

1. **Liste déroulante** : Cliquez sur le menu déroulant "Choisissez une conversation"
2. **Sélectionner** : Choisissez le contact avec qui vous voulez discuter
3. **Consultation** : Tous les messages s'affichent automatiquement

### Informations affichées

Pour chaque message, vous voyez :

| Élément                | Description                                          |
|------------------------|------------------------------------------------------|
| 👤 **Photo de profil** | Photo LinkedIn de l'expéditeur                       |
| **Nom complet**        | Nom de la personne                                   |
| 🕒 **Horodatage**      | Date et heure du message (format : HH:MM JJ/MM/AAAA) |
| 💬 **Contenu**         | Texte du message                                     |

### Ordre d'affichage

Les messages sont affichés **du plus ancien au plus récent** (comme une conversation normale), 
avec le dernier message en bas.

---

##  Envoyer des messages

### Composer un message

1. **Sélectionnez** une conversation dans la liste déroulante
2. **Descendez** en bas de la page
3. **Cliquez** dans le champ "Rédigez un message"
4. **Tapez** votre message
5. **Appuyez** sur `Entrée` ou cliquez sur l'icône `>`

### Confirmation d'envoi

Une fois le message envoyé :
-  Un message de confirmation s'affiche
-  La page se rafraîchit automatiquement
-  Votre message apparaît dans la conversation

### Exemple pratique

```
┌─────────────────────────────────────┐
│ Rédigez un message                  │
│ Merci pour ton retour !             │
│                                  [>]│
└─────────────────────────────────────┘
```

1. Je tape : "Merci pour ton retour !"
2. J'appuie sur `Entrée`
3. Le message est envoyé sur LinkedIn
4. Il apparaît dans la conversation

---

##  Comprendre l'interface

### Zone d'en-tête

```
┌─────────────────────────────────────┐
│  LinkStream                         │
│  Le courant d'infos de votre réseau │
└─────────────────────────────────────┘
```

Titre de l'application et slogan.

### Zone profil

```
┌─────────────────────────────────────┐
│  👤 [Photo]    Klaudia Juhasz       │
│                Profil               │
│                🔗 LinkedIn          │
└─────────────────────────────────────┘
```

- **Photo** : Votre photo de profil LinkedIn
- **Nom** : Votre nom complet
- **Badge** : Indique que c'est votre profil
- **Lien** : Accès direct à votre profil LinkedIn

### Zone de sélection

```
┌─────────────────────────────────────┐
│ Choisissez une conversation:        │
│ ┌─────────────────────────────┐     │
│ │ Victor Langlois          ▼  │     │
│ └─────────────────────────────┘     │
└─────────────────────────────────────┘
```

Menu déroulant listant tous vos contacts LinkedIn avec qui vous avez échangé.

### Zone de messages

```
┌─────────────────────────────────────┐
│ Messages du chat avec Victor        │
│                                     │
│ [Message 1]                         │
│ [Message 2]                         │
│ [Message 3]                         │
└─────────────────────────────────────┘
```

Affichage chronologique de tous les messages échangés avec le contact sélectionné.

### Zone de saisie

```
┌─────────────────────────────────────┐
│ [Rédigez un message              >] │
└─────────────────────────────────────┘
```

Champ de texte pour composer et envoyer vos messages.

---

##  Questions fréquentes (FAQ)

###  Sécurité et confidentialité

**Q : Mes identifiants LinkedIn sont-ils stockés ?**  
R : Non. L'authentification passe par Unipile, un service tiers sécurisé. LinkStream ne stocke jamais vos identifiants.

**Q : Qui peut voir mes messages ?**  
R : Seul vous avez accès à vos conversations. Chaque utilisateur voit uniquement ses propres messages LinkedIn.

**Q : Mes données sont-elles sauvegardées ?**  
R : Oui, vos conversations sont synchronisées automatiquement avec LinkedIn et stockées dans une base de données sécurisée.

---

###  Messages

**Q : Combien de temps faut-il pour voir un nouveau message ?**  
R : Les nouveaux messages apparaissent automatiquement dès réception grâce à la synchronisation en temps réel.

**Q : Puis-je supprimer un message ?**  
R : Non, LinkStream affiche les messages tels qu'ils apparaissent sur LinkedIn. Pour supprimer un message, vous devez le faire directement sur LinkedIn.

**Q : Puis-je envoyer des pièces jointes ?**  
R : Actuellement, LinkStream ne supporte que l'envoi de messages texte. Pour les pièces jointes, utilisez LinkedIn directement.

---

###  Synchronisation

**Q : Mes anciennes conversations sont-elles importées ?**  
R : Oui, lors de votre première connexion, toutes vos conversations LinkedIn existantes sont importées automatiquement.

**Q : Les messages que j'envoie depuis LinkStream apparaissent-ils sur LinkedIn ?**  
R : Oui, absolument. LinkStream et LinkedIn sont synchronisés.

**Q : Et si j'envoie un message depuis LinkedIn directement ?**  
R : Il apparaîtra automatiquement dans LinkStream grâce à la synchronisation bidirectionnelle.

---

###  Technique

**Q : LinkStream fonctionne-t-il sur mobile ?**  
R : L'interface est conçue pour être utilisée sur ordinateur.
Une version mobile optimisée sera l'objet du prochain version.

**Q : Quels navigateurs sont compatibles ?**  
R : Chrome, Firefox, Safari, Edge (versions récentes).

**Q : Ai-je besoin d'installer quelque chose ?**  
R : Non, LinkStream fonctionne directement dans votre navigateur web.

---

## Résolution de problèmes

### Problème : Je ne vois pas mes conversations

**Causes possibles :**
- Vous n'êtes pas authentifié
- Aucune conversation LinkedIn existante
- Problème de synchronisation

**Solutions :**
1. Vérifiez que vous avez cliqué sur "J'ai terminé l'authentification"
2. Actualisez la page (F5 ou Ctrl+R)
3. Reconnectez-vous en fermant et rouvrant LinkStream

---

### Problème : L'authentification ne fonctionne pas

**Causes possibles :**
- Identifiants LinkedIn incorrects
- Lien d'authentification expiré (15 minutes)
- Problème de connexion Internet

**Solutions :**
1. Vérifiez vos identifiants LinkedIn
2. Régénérez un nouveau lien d'authentification (actualisez la page)
3. Vérifiez votre connexion Internet

---

### Problème : Mon message n'est pas envoyé

**Causes possibles :**
- Connexion Internet instable
- Session expirée
- Message vide

**Solutions :**
1. Vérifiez votre connexion Internet
2. Reconnectez-vous à LinkStream
3. Assurez-vous que le message contient du texte

---

### Problème : La photo de profil ne s'affiche pas

**Causes possibles :**
- Profil LinkedIn sans photo
- Problème de chargement

**Solutions :**
1. Actualisez la page
2. Vérifiez que le profil LinkedIn possède bien une photo
3. Un emoji 🧑 s'affiche par défaut si aucune photo n'est disponible

---

### Problème : L'application est lente

**Causes possibles :**
- Trop de messages à charger
- Connexion Internet lente
- Navigateur surchargé

**Solutions :**
1. Fermez les onglets inutiles de votre navigateur
2. Videz le cache de votre navigateur
3. Attendez quelques secondes lors du premier chargement

---

## Aide et contact

### Obtenir de l'aide

Si vous rencontrez un problème non résolu par ce guide :

1. **Vérifiez** d'abord la section [Résolution de problèmes](#-résolution-de-problèmes)
2. **Consultez** la [FAQ](#-questions-fréquentes-faq)
3. **Contactez** votre administrateur système

### Signaler un bug

Pour signaler un problème technique :

1. Décrivez le problème rencontré
2. Indiquez les étapes pour le reproduire
3. Précisez votre navigateur et système d'exploitation
4. Ajoutez des captures d'écran si possible

 **Contact** : [Votre administrateur LinkStream]

---

### Proposer une amélioration

Vous avez une idée pour améliorer LinkStream ? N'hésitez pas à la partager !

Améliorations futures prévues :
-  Version mobile responsive
-  Recherche dans les conversations
-  Thèmes personnalisables
-  Notifications en temps réel
-  Statistiques d'utilisation

---

##  Glossaire

| Terme                | Définition                                                        |
|----------------------|-------------------------------------------------------------------|
| **Authentification** | Processus de connexion à votre compte LinkedIn via Unipile        |
| **Conversation**     | Ensemble d'échanges de messages avec un contact LinkedIn          |
| **Synchronisation**  | Mise à jour automatique des messages entre LinkedIn et LinkStream |
| **Provider ID**      | Identifiant unique LinkedIn d'un utilisateur                      |
| **Webhook**          | Système permettant la réception automatique des nouveaux messages |
| **RPC**              | Remote Procedure Call - Appel de fonction sur le serveur          |

---

## Checklist de démarrage

Pour commencer à utiliser LinkStream efficacement :

- [ ] J'ai accédé à l'URL de LinkStream
- [ ] J'ai authentifié mon compte LinkedIn
- [ ] J'ai cliqué sur "J'ai terminé l'authentification"
- [ ] Je vois mes conversations dans la liste déroulante
- [ ] J'ai sélectionné une conversation
- [ ] J'ai lu les messages d'un contact
- [ ] J'ai envoyé un message de test
- [ ] Mon message apparaît dans la conversation
- [ ] J'ai compris comment naviguer entre les conversations



---

## Pour aller plus loin

### Bonnes pratiques

 **À faire :**
- Gardez votre navigateur à jour
- Utilisez LinkStream sur un réseau sécurisé
- Fermez votre session après utilisation sur un ordinateur partagé

 **À éviter :**
- Partager vos identifiants LinkedIn
- Laisser LinkStream ouvert sans surveillance
- Utiliser LinkStream sur un réseau public non sécurisé

---

##  À propos

**LinkStream** a été développé dans le cadre d'un stage de BTS SIO SLAM (session 2026) au sein de l'entreprise **OPS Imperium**, spécialisée en automatisation et intelligence artificielle.

**Note importante** : LinkStream est actuellement un **prototype en développement**. Bien que l'application soit fonctionnelle, des bugs ou des 
ralentissements peuvent survenir. Votre patience et vos retours sont précieux pour améliorer le projet.

### Développé par

**Klaudia Juhasz**  
Étudiante BTS SIO SLAM  
Stage réalisé chez OPS Imperium, Nice  
Encadré par M. Victor Langlois

### Technologies utilisées

- **Frontend** : Streamlit (Python)
- **Backend** : n8n (automatisation)
- **API** : Unipile (LinkedIn)
- **Base de données** : Supabase (PostgreSQL)

---

##  Licence

Ce projet est distribué sous licence MIT - Vous êtes libre de l'utiliser sous réserve de mentionner l'auteur.

---

**Version** : 1.0  
**Dernière mise à jour** : Janvier 2025

---