import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db
import os

def raccogli():
    try:
        # Ora prendiamo SOLO la lunga frase
        pk = os.environ.get('FIREBASE_KEY')
        if not pk:
            print("❌ ERRORE: Chiave non trovata!")
            return

        # Ripariamo i simboli 'a capo'
        pk = pk.replace('\\n', '\n')

        # Costruiamo noi il certificato con i tuoi dati
        cred_dict = {
            "type": "service_account",
            "project_id": "gorlanews-by-max",
            "private_key": pk,
            "client_email": "firebase-adminsdk-fbsvc@gorlanews-by-max.iam.gserviceaccount.com",
            "token_uri": "https://oauth2.googleapis.com/token",
        }

        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app/'
            })

        # Recupero notizie
        res = requests.get("https://comune.gorlaminore.va.it/home")
        soup = BeautifulSoup(res.text, 'html.parser')
        notizie = {f"n_{i}": {"t": a.text.strip()} for i, a in enumerate(soup.find_all(class_='card-title', limit=10))}
        
        db.reference('notizie').set(notizie)
        print("✅ CE L'ABBIAMO FATTA! CONTROLLA FIREBASE!")

    except Exception as e:
        print(f"❌ ERRORE: {e}")

if __name__ == "__main__":
    raccogli()
