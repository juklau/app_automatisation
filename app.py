# Afficher les messages LinkedIn avec Streamlit

from urllib import response
import requests
import toml
import streamlit as st
import numpy as np
import pandas as pd
import base64
import os   #pour générer des id pour les messages envoyés 

from supabase import create_client, Client
from datetime import datetime, timezone
from datetime import timedelta


from urllib import response
import requests
import streamlit as st
import numpy as np
import pandas as pd
import base64
import os   #pour générer des id pour les messages envoyés 

from supabase import create_client, Client
from datetime import datetime, timezone
from datetime import timedelta



# génerer un lien d'authentification pour l'API Unipile
def generate_auth_link():

    # l'URL de l'API Unipile pour générer un lien d'authentification
    url = "https://api17.unipile.com:14751/api/v1/hosted/accounts/link"

    headers = {
        "X-API-KEY": st.secrets['UNIPILE_API_KEY_2'],  # Utiliser la clé API de Unipile
        "Content-Type": "application/json", 
        "accept": "application/json"
    }

    # création de la période de validité du lien
    # datetime.now(timezone.utc) => obtenir l'heure actuelle en UTC
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=15)  # lien valide pour 15 minutes
    # formatage de l'heure d'expiration en ISO 8601
    # le format "%Y-%m-%dT%H:%M:%S.%f" génère une chaîne de caractères au format ISO 8601
    # le format[:-3] + "Z" permet de conserver les 3 premiers chiffres de la microseconde et d'ajouter le suffixe "Z" pour indiquer l'heure UTC
    expire_time_iso = expiration_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


    # contenu principal envoyé dans une requête HTTP POST
    payload = {
        "type": "create",
        "providers": ["LINKEDIN"],
        "api_url": "https://api17.unipile.com:14751",
        "expiresOn": expire_time_iso,
        "success_redirect_url": "http://192.168.1.10:8501"  # URL de redirection après l'authentification
    }

    # envoie la requête POST à l'API Unipile
    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except Exception:
        data = response.text

    if response.status_code in (200, 201):
        auth_url = data.get("url")
        if(auth_url):
            return auth_url
            # st.success("Lien d'authentification généré avec succès.")
            # st.markdown(f"""
            #     <meta http-equiv="refresh" content="0; url={auth_url}">""", unsafe_allow_html=True)
        else:
            st.error("Lien d'authentification introuvable dans la réponse.")
            # st.write("Données de réponse:", data)
    else:
        st.error(f"Erreur lors de la génération du lien d'authentification : {response.status_code }")
        # st.write("Réponse de l'API:", data)
        st.error("Lien d'authentification non généré. Veuillez réessayer plus tard.")
    return None  # Retourne None si l'authentification échoue ou n'est pas générée


# Récupère l'account_id de l'utilisateur authentifié depuis l'API Unipile.
def get_account_id_from_unipile():
   
    url = "https://api17.unipile.com:14751/api/v1/accounts"
    headers = {
        "X-API-KEY": st.secrets['UNIPILE_API_KEY_2'],  # Utiliser la clé API de Unipile
        # "Content-Type": "application/json", 
        "accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Debug pour voir la structure exacte
            # st.write("Réponse Unipile Accounts:", data)
            accounts_list = data.get("items", [])
            for acc in accounts_list:
                if acc.get("type") == "LINKEDIN":
                    return acc.get("id")
                    # st.session_state["account_id"] = account_id
            st.error("Aucun compte LinkedIn trouvé dans la réponse.")
        else:
            st.error(f"Erreur API unipile : {response.status_code}")
    except Exception as e:
        st.error(f"Erreur lors de la récupération de l'account_id : {e}")
    
    return None


def post_auth_data_n8n():

    account_id = get_account_id_from_unipile() 

    if not account_id:
        st.error("Aucun account_id trouvé dans la session pour envoyer à n8n.")
        return  # Arrêter la fonction si account_id est manquant

    # Fonction pour envoyer les données d'authentification à N8N
    url = "https://juklau.app.n8n.cloud/webhook/new_user_auth"  

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "account_id": account_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in (200, 201, 202, 204):
            st.success("Données d'authentification envoyées à N8N.")
        else:
            st.error(f"Erreur lors de l'envoi des données à N8N : {response.status_code}")
    except Exception as e:
        st.error(f"Erreur réseau lors de l'envoi à N8N : {e}")

# generate_auth_link()  # Appel de la fonction pour générer le lien d'authentification

# vérification si l'user est déjà authentifié
# st.session_state =>dictionnaire persistant propre à chaque utilisateur pendant la session.
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False

if not st.session_state["is_authenticated"]:
    auth_link = generate_auth_link()
    if auth_link:
        # Affiche le lien (clic manuel) ou redirige une seule fois
        st.markdown(f"""
                <a href="{auth_link}" target="_blank" style="
                    display: inline-block;
                    margin-top: 300px;
                    margin-bottom: 30px;
                    padding: 10px 20px;
                    background-color: transparent;
                    color: white;
                    font-weight: bold;
                    text-align: center;
                    border: 1px solid white;
                    border-radius: 10px;
                    text-decoration: none;
                    cursor: pointer;
                ">Cliquez ici pour vous authentifier</a>
        """, unsafe_allow_html=True)
        if st.button("J'ai terminé l'authentification"):
            # indiquer que l’utilisateur maintenant est authentifié.
            st.session_state['is_authenticated'] = True
            st.session_state["account_id"] = get_account_id_from_unipile()  # Récupérer l'account_id depuis Unipile
            st.rerun()
else: #si is_authenticated est True
    st.success("Vous êtes authentifié !")
    post_auth_data_n8n()


    # Si l'utilisateur est authentifié, on peut continuer avec l'affichage des messages

    # initialisation de la connection => à exécuter une seule fois
    # connexion à Supabase
    @st.cache_resource
    def init_connection():
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)

    supabase = init_connection()

    # réexécution uniquement lorsque la requête change ou après 10 minutes

    # @st.cache_data(ttl=600) # => permet d’éviter les requêtes répétitives
    # récupération les messages de Supabase par le fonction écrit dedans
    def run_query():
        # reponse = supabase.table("documents").select("*").execute()
        # return reponse.data
                            # OU
        # return supabase.table("documents").select("*").eq('id', 157).execute().data 
        # return supabase.table("linkedin_messages").select("*").execute().data 

        # la méthode .rpc() pour exécuter une requête SQL directement via une fonction stockée dans Supabase
        return supabase.rpc("get_messages").execute().data

    # rows = run_query()
    # transformation le résultat en DataFrame Pandas
    
    
    # --- récupération & robustification des données ---
    rows = run_query()  # ou run_query(account_id) 
    if not rows:
        st.warning("Aucune donnée récupérée de Supabase (rows vide ou None).")
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(rows)

    # debug utile — supprime quand c'est OK
    # st.write("DEBUG - colonnes reçues :", df.columns.tolist())
    # st.write("DEBUG - 3 premières lignes :", df.head(3))

    # helper pour récupérer une série en toute sécurité
    def safe_series(df, col):
        if col in df.columns:
            return df[col].dropna()
        return pd.Series(dtype=object)

    # récupérer valeurs de profil de façon sûre
    first_valid_profile = safe_series(df, "profile_picture_url")
    first_profile_name = safe_series(df, "full_name")
    first_profile_linkedin_url = safe_series(df, "linkedin_url")

    # les données de profil
    profile_picture_url = first_valid_profile.iloc[0] if not first_valid_profile.empty else None
    profile_full_name = first_profile_name.iloc[0] if not first_profile_name.empty else None
    profile_linkedin_url = first_profile_linkedin_url.iloc[0] if not first_profile_linkedin_url.empty else None

    # Header / profil
    st.markdown("""
        <div style= "text-align: center; padding-bottom: 60px;">
            <h1> LinkStream </h1>
            <h3> Le courant d'infos de votre réseau </h3>
        </div>
    """, unsafe_allow_html=True)

    # image linkedin encodée
    # "rb" => read binary
    # f => un objet fichier
    with open("img/icons8-linkedin-48.png", "rb") as f:
        data = f.read()
    
    # base64.b64encode(data) => convertir la donnée en binaire
    # .decode() => transforme cette chaine en string
    encoded_logo = base64.b64encode(data).decode()

    # data:image/png;base64 => entête: img png encodé en base64
    logo_linkedin = f"data:image/png;base64,{encoded_logo}"

    container = st.container()
    cols = container.columns([1, 8])

    with cols[0]:
        if profile_picture_url:
            st.image(profile_picture_url, width=200)
            # ou
            # st.markdown(f"""
            #     <div style="padding-top: 20px;">
            #         <img src="{profile_picture_url}" style="border-radius: 50%; width: 200px;" />
            #     </div>
            # """, unsafe_allow_html=True)
        else:
            st.write("Aucune photo de profil disponible.")

    with cols[1]:
        st.subheader(profile_full_name or "Nom indisponible")
        st.badge("Profil")
        if profile_linkedin_url:
            st.markdown(f'<a href="{profile_linkedin_url}" target="_blank" style="color: white; text-decoration: none; font-weight:bold;"><img src="{logo_linkedin}" style="width: 30px;"></a>', unsafe_allow_html=True)

    container.divider()

    # --- Vérifier qu'on a bien la colonne chat_row_id avant de construire la map ---
    if "chat_row_id" not in df.columns or df.empty:
        st.warning("Aucune donnée de chat trouvée (colonne 'chat_row_id' manquante ou DataFrame vide).")
        # arrête le rendu pour éviter d'exécuter le reste quand il n'y a pas de données
        st.stop()  

    # Identifier qui est "moi"
    my_provider_id = st.secrets["my_provider_id"]

    # création map (dictionnaire) chat_name -> chat_id en gérant les absences && chat_id ==> nom de la personne
    chat_name_map = {}
    for chat_id in df["chat_row_id"].unique():
        participants = df[df["chat_row_id"] == chat_id]

        # déterminer qui est la personne avec "moi" discute
        others = participants[participants["sender"] != my_provider_id] if "sender" in participants.columns else participants
        
        # Extraire un nom valide de "l'autre personne"
        names = others["full_name"].dropna().unique() if "full_name" in others.columns else []

        # il faut mettre participants et pas others!!!
        # on récupère un autre champ ("nom du participant") =>c'est bien message_df!!
        # dropna() => retirer les valeurs NaN ([Alice, NaN, Michel, NaN]) => [Alice, Michel]
        # unique() => garder uniquement les valeurs distinctes restantes 
        fallback = participants["attendee_name"].dropna().unique() if "attendee_name" in participants.columns else []

        # à regarder il y a combien pax dans le chat => à mettre en commentaire
        # st.write("Tous les sender dans ce chat :", messages_df["sender"].unique())
        # st.write("Tu es :", my_provider_id)

        if len(names) > 0:
            #  on prend le 1iere pax trouvé  (pas moi) comme nom du contact
            affiche_name = names[0]
        elif len(fallback) > 0:
            affiche_name = fallback[0]
        else:
            affiche_name = f"Contact inconnu ({str(chat_id)[:5]})"

        chat_name_map[affiche_name] = chat_id

    # choix de la conversation à afficher
    if not chat_name_map:
        st.warning("Aucune conversation disponible.")
        st.stop()

    st.subheader("Choisissez une conversation: ")
    selected_name = st.selectbox("Choisissez une conversation: ", #label obligatoire pour selectbox
                                 list(chat_name_map.keys()), 
                                 label_visibility="collapsed") #cacher le label dans l'interface
    
    selected_chat = chat_name_map[selected_name]

    # filtrer les messages par chat sélectionné
    messages_df = df[df["chat_row_id"] == selected_chat].copy()

     # titre de la conversation
    st.markdown(f"### Messages du chat avec *{selected_name}*")

    # safety: trier created_at si présent
    if "created_at" in messages_df.columns:
        # convertir created_at en datetime, ignorer les erreurs de conversion
        # pd.to_datetime() => convertit les chaînes de caractères en objets datetime
        messages_df["created_at"] = pd.to_datetime(messages_df["created_at"], errors="coerce")
        messages_df = messages_df.sort_values("created_at", ascending=True)

    st.write("message trouvé: ", len(messages_df))

    # affichage des messages et des éléments
    # à la place "index" (je n'ai pas besoin) => "_" -> je ne vais pas l'utiliser
    for _, row in messages_df.iterrows():
        sender = row.get("sender", "Inconnu")
        full_name = row.get("full_name") or "Expéditeur inconnu"
        photo_url = row.get("profile_picture_url") if "profile_picture_url" in messages_df.columns else None
        message = row.get("content", "")
        is_from_me = row.get("is_from_me")
        iso_date = row.get("created_at")

        # convertir en objet datetime et formater la date
        # formatted_date = datetime.fromisoformat(iso_date).strftime("%H:%M %d/%m/%Y")

        if pd.isna(iso_date):
            formatted_date = ""
        else:
            try:
                formatted_date = pd.to_datetime(iso_date).strftime("%H:%M %d/%m/%Y")
            except Exception:
                formatted_date = str(iso_date)

        msg_container = st.container()
        # afficher une mise en page à 2 colonnes
        cols = msg_container.columns([1, 8])
        with cols[0]: # à gauche
            if photo_url:
                st.image(photo_url, width=80)
            else:
                st.markdown('<div style="font-size: 50px;">🧑</div>', unsafe_allow_html=True)
        with cols[1]: # à droite
            st.markdown(f"**{full_name}**")
            if formatted_date:
                st.markdown(f"🕒 {formatted_date}")
            if message:
                st.markdown(f"> {message}")
            else:
                st.markdown("_Message supprimé_")
        # st.markdown("---")
        st.divider()

    # récupérer account_id/provider_id/chat_id de façon sûre
    def safe_first(series_name):
        if series_name in messages_df.columns:
            s = messages_df[series_name].dropna()
            return s.iloc[0] if not s.empty else None
        return None

    account_id = safe_first("account_id")
    provider_id = safe_first("provider_id")
    chat_id_choisi = safe_first("chat_id")

    # si on a besoin d'envoyer un message, vérifier que account_id/provider_id/chat_id existent
    if not all([account_id, provider_id, chat_id_choisi]):
        st.warning("Impossible d'initialiser l'envoi de message : paramètres manquants (account_id/provider_id/chat_id).")
    else:
        # fonction pour envoyer un message à LinkedIn via l'API Unipile
        # au cas où: dans les paramètres était "linkedin_local_id" => mais on n'en a pas besoin ici
        def post_message_to_linkedin(message, chat_id, account_id, provider_id):
            url = f"https://api17.unipile.com:14751/api/v1/chats/{chat_id}/messages"
            headers = {
                "X-API-KEY": st.secrets['UNIPILE_API_KEY_2'],
                "Content-Type": "application/json",
                "accept": "application/json"
            }
            payload = {
                "chat_id": chat_id,
                "text": message,
                "account_id": account_id,
                "provider_id": provider_id,
                "message_type": "MESSAGE"
            }
            response = requests.post(url, headers=headers, json=payload)
            try:
                data = response.json()
            except:
                data = response.text

             # Vérifier si la requête a réussi
            # 201 => Created, 200 => OK
            # 202 => Accepted (la requête a été acceptée mais pas encore traitée
            if response.status_code in (200, 201):
                st.success("Message envoyé avec succès à LinkedIn.")
                st.write("Données de réponse:", data)
            else:
                st.error(f"Erreur lors de l'envoi {response.status_code}.")
                st.write("Payload envoyé:", payload)
                st.write("Données de réponse:", data)

        # pour envoyer un message par l'utilisateur: boîte de saisi de type chat
        prompt = st.chat_input(f"Rédigez un message à {full_name}")
        if prompt:
            # st.write(f"Vous avez écrit : {prompt}")
            post_message_to_linkedin(prompt, chat_id_choisi, account_id, provider_id)

        # pour rafraîchir la page et afficher le nouveau message
        st.rerun() 

