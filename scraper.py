import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db
import os
import json

def raccogli():
    try:
        # Recuperiamo la chiave dai Secrets di GitHub
        key_json = os.environ.get('FIREBASE_KEY')
        
        if not key_json:
            print("❌ ERRORE: La chiave non è stata trovata su GitHub!")
            return

        # Carichiamo la chiave e puliamo i caratteri speciali
        cred_dict = json.loads(key_json)
        cred_dict["private_key"] = cred_dict["private_key"].replace('\\n', '\n')
        
        # Inizializzazione Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app/'
            })

        # Recupero notizie dal sito del Comune
        res = requests.get("https://comune.gorlaminore.va.it/home", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        notizie = {}
        
        for i, art in enumerate(soup.find_all(class_='card-title', limit=10)):
            notizie[f"notizia_{i}"] = {"titolo": art.text.strip()}
        
        # Invio a Firebase
        db.reference('notizie').set(notizie)
        print("✅ SUCCESSO! I dati sono stati inviati correttamente.")

    except Exception as e:
        print(f"❌ ERRORE FINALE: {e}")

if __name__ == "__main__":
    raccogli()
