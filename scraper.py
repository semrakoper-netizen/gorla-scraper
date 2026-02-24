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
        cred_json = cred_json.strip()
        try:
            cred_dict = json.loads(cred_json)
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app/'
            })
        except Exception as e:
            print(f"Errore caricamento Firebase: {e}")

def raccogli():
    print("Avvio recupero notizie col travestimento...")
    try:
        # IL TRAVESTIMENTO: Facciamo finta di essere Google Chrome su un normale PC
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get("https://comune.gorlaminore.va.it/home", headers=headers)
        
        # Controlliamo se il Comune ci fa entrare (Dovrebbe stampare 200)
        print(f"Risposta dal sito: {res.status_code}")
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # MIRINO ALLARGATO: Cerchiamo qualsiasi cosa abbia la classe "card-title"
        articoli = soup.find_all(class_='card-title', limit=10)
        
        notizie = {}
        for i, art in enumerate(articoli):
            titolo = art.text.strip()
            if titolo:
                notizie[f"notizia_{i}"] = {"titolo": titolo}
                print(f"TROVATA: {titolo}") # Lo stampiamo per vederlo
        
        if notizie:
            db.reference('notizie').set(notizie)
            print("VITTORIA! Dati inviati a Firebase.")
        else:
            print("Il sito ci fa entrare ma non trova i titoli.")
            
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    raccogli()
