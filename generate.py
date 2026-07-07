from pyrogram import Client

api_id = int(input("API_ID: "))
api_hash = input("API_HASH: ")

with Client(
    "my_account",
    api_id=api_id,
    api_hash=api_hash,
    in_memory=True
) as app:
    print("\nYour String Session:\n")
    print(app.export_session_string())