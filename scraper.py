import requests
from bs4 import BeautifulSoup
import json
import firebase_admin
from firebase_admin import credentials, db
import os

# Configurazione Firebase
if not firebase_admin._apps:
    cred_json = os.environ.get('FIREBASE_KEY')
    if cred_json:
        # Pulizia della stringa per evitare errori di formattazione
        cred_json = cred_json.strip()
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app'
        })

def raccogli():
    print("Avvio...")
    res = requests.get("https://comune.gorlaminore.va.it/home")
    soup = BeautifulSoup(res.text, 'html.parser')
    articoli = soup.find_all(['h3', 'h2'], limit=5)
    
    notizie = {}
    for i, art in enumerate(articoli):
        notizie[f"n_{i}"] = {"titolo": art.text.strip()}
    
    db.reference('notizie').set(notizie)
    print("Fatto!")

if __name__ == "__main__":
    raccogli()
