# Afficher les messages LinkedIn avec Streamlit
import streamlit as st
from supabase import create_client, Client

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
@st.cache_data(ttl=600)
def run_query():
    # reponse = supabase.table("documents").select("*").execute()
    # return reponse.data
                        # OU
    # return supabase.table("documents").select("*").eq('id', 157).execute().data 
    return supabase.table("document_metadata").select("*").execute().data 

rows = run_query()

for row in rows:
    st.write(row['title'])
    st.divider()

# for i, item in enumerate(rows):
#     st.write(f"{i+1}. {item}")