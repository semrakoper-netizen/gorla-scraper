import requests
from bs4 import BeautifulSoup
import json
import firebase_admin
from firebase_admin import credentials, db
import os

def inizializza_firebase():
    print("Tentativo di inizializzazione Firebase...")
    cred_json = os.environ.get('FIREBASE_KEY')
    
    if not cred_json:
        print("ERRORE CRITICO: La chiave FIREBASE_KEY è vuota o non trovata nei Secrets di GitHub!")
        return False

    try:
        # Pulizia della chiave per evitare errori di formattazione
        cred_dict = json.loads(cred_json.strip())
        if "private_key" in cred_dict:
            cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        print("Firebase inizializzato correttamente!")
        return True
    except Exception as e:
        print(f"Errore durante l'inizializzazione: {e}")
        return False

def raccogli():
    if not inizializza_firebase():
        return

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get("https://comune.gorlaminore.va.it/home", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        articoli = soup.find_all(class_='card-title', limit=10)
        
        notizie = {}
        for i, art in enumerate(articoli):
            titolo = art.text.strip()
            if titolo:
                notizie[f"notizia_{i}"] = {"titolo": titolo}
                print(f"Trovata: {titolo}")
        
        if notizie:
            db.reference('notizie').set(notizie)
            print("DATI INVIATI A FIREBASE!")
        else:
            print("Nessuna notizia trovata sul sito.")
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    raccogli()
