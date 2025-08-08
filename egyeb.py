

# générer un id
# def generate_id_type_linkedin(byte_length = 16):
#     random_byte = os.urandom(byte_length)
#     encoded = base64.urlsafe_b64encode(random_byte).decode('utf-8')
#     return encoded.rstrip('=') # pour enlever le padding


# c'était dans  post_message_to_linkedin(message, chat_id, account_id, provider_id)
# linkedin_message_id = data.get("message_id")

# # Mettre à jour la ligne existante avec le vrai linkedin_message_id
# if linkedin_message_id:
#     supabase.table("linkedin_messages")\
#         .update({"linkedin_message_id": linkedin_message_id})\
#         .eq("id", local_message_id)\
#         .execute()


# if prompt...:
# Envoi du message à LinkedIn via l'API Unipile
# post_message_to_linkedin(
#     message = prompt,
#     chat_id = chat_id_choisi,
#     account_id = account_id,
#     provider_id = provider_id,
# #     local_message_id = linkedin_local_id
# )

###################

 # linkedin_local_id = generate_id_type_linkedin()

# nouveau_message = {
#     "id": linkedin_local_id,
#     "linkedin_message_id": None,  # initialement None, mis à jour après l'envoi
#     "chat_row_id" :  selected_chat,
#     "chat_id" : chat_id_choisi,
#     "content" : prompt,
#     "created_at" : datetime.now(timezone.utc).isoformat(),
#     "sender" : my_provider_id,
#     "is_from_me" : True,
#     "account_id" : account_id,
#     "provider_id" : provider_id,
#     "message_type" : "MESSAGE",
#     "reactions" : {},
#     "attachments" : {},
# }

# reponse = supabase.table("linkedin_messages").insert(nouveau_message).execute()

# if reponse.data:
#     st.success("Le message a été bien enregistré dans la BDD")

# else:
#     st.error("Un erreur est survenu pendant l'enregistrement")
#     st.write(reponse)

# Pour éviter les conflits de fusion dans les PRs, on peut ajouter cette ligne
# "Prefer": "resolution=merge-duplicates"

