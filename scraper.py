import requests
from bs4 import BeautifulSoup
import json
import datetime
import firebase_admin
from firebase_admin import credentials, db
import os

# 1. Configurazione Firebase
if not firebase_admin._apps:
    # GitHub caricherà la chiave segreta che abbiamo messo nei 'Secrets'
    cred_json = os.environ.get('FIREBASE_KEY')
    if cred_json:
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app'
        })

URL_COMUNE = "https://comune.gorlaminore.va.it/home"

def scegli_immagine_di_riserva(titolo):
    t = titolo.lower()
    if "scuola" in t: return "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"
    if "strada" in t or "lavori" in t: return "https://images.unsplash.com/photo-1584852955931-15858fc929c4?w=400"
    return "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400"

def raccogli_e_salva():
    print("Avvio ricerca notizie...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        risposta = requests.get(URL_COMUNE, headers=headers)
        soup = BeautifulSoup(risposta.text, 'html.parser')
        
        # Cerchiamo le notizie nel sito
        articoli = soup.find_all(['article', 'div'], class_=['news', 'Novità', 'card'])
        
        notizie_per_firebase = {}
        
        for i, art in enumerate(articoli[:10]): # Prendiamo le ultime 10
            titolo_tag = art.find(['h2', 'h3', 'a'])
            if not titolo_tag: continue
            
            titolo = titolo_tag.text.strip()
            # Puliamo il titolo se è troppo lungo
            titolo = (titolo[:75] + '..') if len(titolo) > 75 else titolo
            
            img_tag = art.find('img')
            img_url = img_tag.get('src') if img_tag else scegli_immagine_di_riserva(titolo)
            if img_url and img_url.startswith('/'):
                img_url = "https://comune.gorlaminore.va.it" + img_url
            
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            
            # Creiamo un ID unico per la notizia basato sul numero
            notizie_per_firebase[f"notizia_{i}"] = {
                "titolo": titolo,
                "data": data,
                "immagineUrl": img_url
            }

        # Salviamo tutto su Firebase sovrascrivendo le vecchie (così l'app è sempre aggiornata)
        ref = db.reference('notizie')
        ref.set(notizie_per_firebase)
        print("✅ Notizie caricate con successo su Firebase!")

    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    raccogli_e_salva()
