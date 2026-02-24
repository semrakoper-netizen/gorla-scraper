import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db
import os
import json

def inizializza_firebase():
    try:
        # Recuperiamo la chiave dal "forziere" di GitHub
        key_data = os.environ.get('FIREBASE_KEY')
        if not key_data:
            print("ERRORE: Chiave non trovata nei Secrets!")
            return False
            
        # Trasformiamo il testo in un dizionario vero e proprio
        config = json.loads(key_data)
        
        # Pulizia manuale della chiave privata (il punto dove spesso si rompe)
        if 'private_key' in config:
            config['private_key'] = config['private_key'].replace('\\n', '\n')
            
        cred = credentials.Certificate(config)
        
        # Se l'app esiste già, la usiamo, altrimenti la creiamo
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app/'
            })
        print("✅ CONNESSIONE RIUSCITA!")
        return True
    except Exception as e:
        print(f"❌ ERRORE CONNESSIONE: {e}")
        return False

def raccogli():
    if not inizializza_firebase(): return

    print("Tentativo di lettura sito Comune...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get("https://comune.gorlaminore.va.it/home", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        articoli = soup.find_all(class_='card-title', limit=10)
        
        notizie = {}
        for i, art in enumerate(articoli):
            titolo = art.text.strip()
            if titolo:
                notizie[f"notizia_{i}"] = {"titolo": titolo}
                print(f"Trovato: {titolo}")
        
        if notizie:
            db.reference('notizie').set(notizie)
            print("🚀 DATI INVIATI CON SUCCESSO!")
        else:
            print("Nessuna notizia trovata.")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    raccogli()
