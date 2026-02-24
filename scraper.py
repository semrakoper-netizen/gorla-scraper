import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db
import os
import json

def raccogli():
    try:
        # Recupero la chiave dai Secrets
        raw_key = os.environ.get('FIREBASE_KEY')
        if not raw_key:
            print("❌ ERRORE: Chiave mancante nei Secrets!")
            return

        # Carico il JSON e pulisco la private_key in modo profondo
        info = json.loads(raw_key)
        
        # Questa è la parte magica: pulisce ogni possibile errore di formattazione
        if "private_key" in info:
            clean_key = info["private_key"].replace("\\n", "\n").strip()
            # Se per caso la chiave è stata incollata con virgolette extra, le togliamo
            if clean_key.startswith('"') and clean_key.endswith('"'):
                clean_key = clean_key[1:-1]
            info["private_key"] = clean_key

        # Inizializzazione
        if not firebase_admin._apps:
            cred = credentials.Certificate(info)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app/'
            })

        # Scraping
        res = requests.get("https://comune.gorlaminore.va.it/home", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        notizie = {f"n_{i}": {"t": a.text.strip()} for i, a in enumerate(soup.find_all(class_='card-title', limit=10))}
        
        if notizie:
            db.reference('notizie').set(notizie)
            print("✅ CE L'ABBIAMO FATTA! I DATI SONO SU FIREBASE!")
        else:
            print("⚠️ Connesso, ma non ho trovato notizie sul sito.")

    except Exception as e:
        print(f"❌ ERRORE: {e}")

if __name__ == "__main__":
    raccogli()
