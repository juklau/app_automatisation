

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
        "expiresOn": expire_time_iso
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
            st.success("Lien d'authentification généré avec succès.")
            st.markdown(f"""
                <meta http-equiv="refresh" content="0; url={auth_url}">""", unsafe_allow_html=True)
        else:
            st.error("Lien d'authentification introuvable dans la réponse.")
            # st.write("Données de réponse:", data)
    else:
        st.error(f"Erreur lors de la génération du lien d'authentification : {response.status_code }")
        # st.write("Réponse de l'API:", data)
        st.error("Lien d'authentification non généré. Veuillez réessayer plus tard.")


generate_auth_link()  # Appel de la fonction pour générer le lien d'authentification