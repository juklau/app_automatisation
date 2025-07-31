# Afficher les messages LinkedIn avec Streamlit
import streamlit as st
import numpy as np
import pandas as pd


from supabase import create_client, Client
from datetime import datetime 

st.title("LinkStream")
st.subheader("_Le courant d'infos de votre réseau_")

# initialisation de la connection => à exécuter une seule fois

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# réexécution uniquement lorsque la requête change ou après 10 minutes
@st.cache_data(ttl=600) # => permet d’éviter les requêtes répétitives
def run_query():
    # reponse = supabase.table("documents").select("*").execute()
    # return reponse.data
                        # OU
    # return supabase.table("documents").select("*").eq('id', 157).execute().data 
    # return supabase.table("document_metadata").select("*").execute().data 
    return supabase.table("linkedin_messages").select("*").execute().data 

    # la méthode .rpc() pour exécuter une requête SQL directement via une fonction stockée dans Supabase
    # return supabase.rpc("get_messages").execute().data

rows = run_query()

df = pd.DataFrame(rows)


# photo de l'utilisateur
container = st.container(height=200, border=True)
container.write("la place du photo")
# container.image("adresse", caption="Photo du profil", width=80)
container.divider()


container.markdown("""<a href="https://www.linkedin.com/in/klaudia-juhasz-a165002bb/" target="_blank" style= "color: white; text-decoration: none; font-weight:bold;">Profil de user </a>""", unsafe_allow_html=True)

container.divider()

# container.write("Affichage de message")

# # pour envoyer un message
# prompt = container.chat_input("Rédigez un message à xy")
# if prompt:
#     container.write(f"L'utilisateur a envoyé le message suivant : {prompt}")


if df.empty:
    st.warning("Aucun donnée de chat trouvéé...")
else:
    chat_ids = df["chat_row_id"].unique().tolist()
    selected_chat = st.selectbox("Choisissez une conversation: ", chat_ids)

# filtrer les messages par chat séléctionné
messages_df = df[df["chat_row_id"] == selected_chat]

st.markdown(f"### Messages pour le chat: `{selected_chat}`")

#trier par date
if "created_at" in messages_df.columns:

    # trier du plus ancien au plus récent
    messages_df = messages_df.sort_values("created_at", ascending=True)

st.write("message trouvé: ", len(messages_df))


for _, row in messages_df.iterrows():
    sender = row.get("sender", "Inconnu")
    account_id = row.get("account_id", "Inconnu")
    message = row.get("content", "")
    is_from_me = row.get("is_from_me")

    # la date ISO initiale en string
    iso_date = row.get("created_at")

    # convertir en objet dateime
    dt = datetime.fromisoformat(iso_date)

    # formater la date
    formatted_date = dt.strftime("%H:%M %d/%m/%Y")

    if(is_from_me):
        st.markdown(f"**{account_id}** ")
    else:
        st.markdown(f"**{sender}** ")

    st.markdown(f"{'🕒  '}{formatted_date}")
    st.markdown(f"> {message}")
    # st.markdown("---")
    st.divider()

# pour envoyer un message
prompt = st.chat_input("Rédigez un message à xy")
if prompt:
    st.write(f"L'utilisateur a envoyé le message suivant : {prompt}")

# st.dataframe(df[['content', 'created at']])

# for row in rows:
#     st.write(row['message'])
#     st.divider()

# for i, item in enumerate(rows):
#     st.write(f"{i+1}. {item}")


# # photo de l'utilisateur
# container = st.container(height=500, border=True)
# container.write("la place du photo")
# # container.image("adresse", caption="Photo du profil", width=80)
# container.divider()


# container.markdown("""<a href="https://www.linkedin.com/in/klaudia-juhasz-a165002bb/" target="_blank" style= "color: white; text-decoration: none; font-weight:bold;">Profil de user </a>""", unsafe_allow_html=True)

# container.divider()

# container.write("Affichage de message")

# # pour envoyer un message
# prompt = container.chat_input("Rédigez un message à xy")
# if prompt:
#     container.write(f"L'utilisateur a envoyé le message suivant : {prompt}")