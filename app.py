# Afficher les messages LinkedIn avec Streamlit
import time
from urllib import response
import requests
import streamlit as st
import numpy as np
import pandas as pd
import base64
import os   #pour générer des id pour les messages envoyés 

from supabase import create_client, Client
from datetime import datetime, timezone

st.markdown("""
        <div style= "text-align: center; padding-bottom: 60px;">
            <h1> LinkStream </h1>
            <h3> Le courant d'infos de votre réseau </h3>
        </div>
 """, unsafe_allow_html=True)

# st.title("LinkStream")
# st.header("_Le courant d'infos de votre réseau_")

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

rows = run_query()
# transformation le résultat en DataFrame Pandas
df = pd.DataFrame(rows)

# pour aider..
# st.write("colomne disponible: ", df.columns.tolist())
# st.write("donnée récupéré: ", df)

# affichage de la photo de l'utilisateur (profil)
first_valid_profile = df["profile_picture_url"].dropna().values
first_profile_name = df["full_name"].dropna().values
first_profile_linkedin_url = df["linkedin_url"].dropna().values

if len(first_valid_profile) > 0:
    profile_picture_url = first_valid_profile[0]
else:
    profile_picture_url = None

if len(first_profile_name) > 0:
    profile_full_name = first_profile_name[0]
else:
    profile_full_name = None

if len(first_profile_linkedin_url) > 0:
    profile_linkedin_url = first_profile_linkedin_url[0]
else:
    profile_linkedin_url = None

# "rb" => read binary
# f => un objet fichier
with open("img/icons8-linkedin-48.png", "rb") as f:
    data = f.read()
    # base64.b64encode(data) => convertir la donnée en binaire
    # .decode() => transforme cette chaine en string
    encoded_logo = base64.b64encode(data).decode()



# data:image/png;base64 => entête: img png encodé en base64
logo_linkedin =  f"data:image/png;base64,{encoded_logo}"

container = st.container()
cols = container.columns([1, 8])

with cols[0]:
    if profile_picture_url:
        st.markdown(f"""
            <div style="padding-top: 20px;">
                <img src="{profile_picture_url}" style="border-radius: 50%; width: 200px;" />
            </div>
        """, unsafe_allow_html=True)
        # st.image(profile_picture_url) # il faut mettre st.image et non container.image (passe les img en dehors de colonnes)!!
    else:
        st.write("Aucune photo de profil disponible.")

with cols[1]:
    st.subheader(profile_full_name)
    st.badge("Profil")
    st.markdown(f"""<a href="{profile_linkedin_url}" target="_blank" style= "color: white; text-decoration: none; font-weight:bold;"><img src="{logo_linkedin}" style="width: 30px;"></a>""", unsafe_allow_html=True)
   

container.divider()

# Identifier qui est "moi"
my_provider_id = st.secrets["my_provider_id"]

# création un dictionnonaire: chat_id ==> nom de la personne
chat_name_map = {}
for chat_id in df["chat_row_id"].unique():
    participants = df[df["chat_row_id"] == chat_id]
    others = participants[participants["sender"] != my_provider_id]
    names = others["full_name"].dropna().unique()
   
    fallback = participants["attendee_name"].dropna().unique()  # il faut mettre participants et pas others!!!
    # fallback_id = others["attendee_provider_id"].dropna().unique()

    if len(names) > 0:
        affiche_name = names[0]
    elif len(fallback) > 0 :
        affiche_name = fallback[0]
       
    else:
        affiche_name = f"Contact inconnu ({chat_id[:5]})"

    chat_name_map[affiche_name] = chat_id


# choix de la conversation à afficher
if df.empty:
    st.warning("Aucune donnée de chat trouvée...")
else:
    st.subheader("Choisissez une conversation: ")
    selected_name = st.selectbox("Choisissez une conversation: ", #label obligatoire pour selectbox
                                 list(chat_name_map.keys()), 
                                 label_visibility="collapsed") #cacher le label dans l'interface

selected_chat = chat_name_map[selected_name]

# filtrer les messages par chat séléctionné
messages_df = df[df["chat_row_id"] == selected_chat]

# déterminer qui est la personne avec "moi" discute
other_person = messages_df[messages_df["sender"] != my_provider_id]

# Extraire un nom valide de "l'autre personne"
valid_names = other_person["full_name"].dropna().unique()

# on récupère un autre champ ("nom du participant") =>c'est bien message_df!!
# dropna() => retirer les valeurs NaN ([Alice, NaN, Michel, NaN]) => [Alice, Michel]
# unique() => garder uniquement les valeurs distinctes restantes 
fallback_name = messages_df["attendee_name"].dropna().unique()

# à regarder il y a combien pax dans le chat => à mettre en commentaire
# st.write("Tous les sender dans ce chat :", messages_df["sender"].unique())
# st.write("Tu es :", my_provider_id)


if len(valid_names) > 0:
    #  on prend le 1iere pax trouvé  (pas moi) comme nom du contact
    contact_person =  valid_names[0]
else:
    # contact_person = fallback_name[0] if len(fallback_name)>0 else "contact inconnu" => ez plus simple
    if len(fallback_name)>0:
        # on prend le premier nom dans "attendee_name"
        contact_person = fallback_name[0]
    else:
        contact_person = "un contact inconnu"
    
# titre de la conversation
st.markdown(f"### Messages du chat avec *{contact_person}*")

#trier par date croissante
if "created_at" in messages_df.columns:

    # trier du plus ancien au plus récent
    messages_df = messages_df.sort_values("created_at", ascending=True)

st.write("message trouvé: ", len(messages_df))


# affichage des messages et des éléments
# à la place "index" (je n'ai pas besoin) => "_" -> je ne vais pas l'utiliser
for _, row in messages_df.iterrows():
    sender = row.get("sender", "Inconnu")
    full_name = row.get("full_name") if (row.get("full_name")) else "Expéditeur inconnu"
    photo_url = row.get("profile_picture_url")
    message = row.get("content", "")
    is_from_me = row.get("is_from_me")

    # la date ISO initiale en string
    iso_date = row.get("created_at")

    # convertir en objet dateime
    dt = datetime.fromisoformat(iso_date)

    # formater la date
    formatted_date = dt.strftime("%H:%M %d/%m/%Y")

    # if(is_from_me):
    #     st.markdown(f"**{account_id}** ")
    # else:
    #     st.markdown(f"**{sender}** ")

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
        st.markdown(f"{'🕒  '}{formatted_date}")

        if(message):
            st.markdown(f"> {message}")
        else:
            st.markdown("_Message supprimé_")
       
    # st.markdown("---")
    st.divider()

# générer un id
def generate_id_type_linkedin(byte_length = 16):
    random_byte = os.urandom(byte_length)
    encoded = base64.urlsafe_b64encode(random_byte).decode('utf-8')
    return encoded.rstrip('=') # pour enlever le padding

# récuperer les données pour l'envoie dans Supabase
account_id = messages_df["account_id"].dropna().iloc[0]
provider_id = messages_df["provider_id"].dropna().iloc[0]
chat_id_choisi = messages_df["chat_id"].dropna().iloc[0]
# st.write(f"chat_id_choisi : {chat_id_choisi}")


# fonction pour envoyer un message à LinkedIn via l'API Unipile
def post_message_to_linkedin(message, chat_id, account_id, provider_id):
   
    url = f"https://api17.unipile.com:14751/api/v1/chats/{chat_id}/messages"

    headers = {
        "X-API-KEY": st.secrets['UNIPILE_API_KEY_2'],  # Utiliser la clé API de Unipile
        "Content-Type": "application/json", 
        "accept": "application/json"
    }

    payload = {
        "chat_id" : chat_id,
        "text" : message,
        "account_id" : account_id,
        "provider_id" : provider_id,
        "message_type" : "MESSAGE"
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
prompt = st.chat_input(f"Rédigez un message à {contact_person}")
if prompt:
    st.write(f"Vous avez écrit : {prompt}")

    nouveau_message = {
        "id": generate_id_type_linkedin(),
        "chat_row_id" :  selected_chat,
        "chat_id" : chat_id_choisi,
        "content" : prompt,
        "created_at" : datetime.now(timezone.utc).isoformat(),
        "sender" : my_provider_id,
        "is_from_me" : True,
        "account_id" : account_id,
        "provider_id" : provider_id,
        "message_type" : "MESSAGE",
        "reactions" : {},
        "attachments" : {}
    }

    reponse = supabase.table("linkedin_messages").insert(nouveau_message).execute()

    if reponse.data:
        st.success("Le message a été bien enregistré dans la BDD")

        # Envoi du message à LinkedIn via l'API Unipile
        post_message_to_linkedin(
            message=prompt,
            chat_id=chat_id_choisi,
            account_id=account_id,
            provider_id=provider_id
        )
        
        # mise à jour la conversation en récupérant les messages du chat
        # messages = supabase.table("linkedin_messages")\
        #         .select("*")\
        #         .eq("chat_id", chat_id_choisi)\
        #         .execute().data

        # if messages:
        #     for msg in messages:
        #         if msg["is_from_me"]:
        #             st.chat_message("user").write(msg["content"])
        #         else:
        #             st.chat_message("assistant").write(msg["content"])  

        # time.sleep(1)  # attendre un peu pour que le message soit bien envoyé

        # # recharger la page pour afficher le nouveau message
        st.rerun()
    else:
        st.error("Un erreur est survenu pendant l'enregistrement")
        st.write(reponse)






# Bonjour Victor, aujourd'hui est mercredi et je vais bien t'embeter sur linkedin





# Pour éviter les conflits de fusion dans les PRs, on peut ajouter cette ligne
# "Prefer": "resolution=merge-duplicates"
