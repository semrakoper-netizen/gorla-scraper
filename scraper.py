import requests
from bs4 import BeautifulSoup
import json
import firebase_admin
from firebase_admin import credentials, db
import os

# Configurazione Firebase "Corazzata"
if not firebase_admin._apps:
    cred_json = os.environ.get('FIREBASE_KEY')
    if cred_json:
        # Questo pulisce la chiave da eventuali spazi o ritorni a capo sbagliati
        cred_json = cred_json.strip()
        try:
            cred_dict = json.loads(cred_json)
            # Corregge il formato della private_key se danneggiato
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app'
            })
        except Exception as e:
            print(f"Errore caricamento JSON: {e}")

def raccogli():
    print("Avvio recupero notizie...")
    try:
        res = requests.get("https://comune.gorlaminore.va.it/home")
        soup = BeautifulSoup(res.text, 'html.parser')
        # Cerchiamo i titoli delle notizie
        articoli = soup.find_all(['h3', 'h2'], limit=8)
        
        notizie = {}
        for i, art in enumerate(articoli):
            titolo = art.text.strip()
            if titolo:
                notizie[f"notizia_{i}"] = {"titolo": titolo}
        
        if notizie:
            db.reference('notizie').set(notizie)
            print("Dati inviati a Firebase con successo!")
        else:
            print("Nessuna notizia trovata.")
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    raccogli()
