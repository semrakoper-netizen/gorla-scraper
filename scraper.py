import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db

def raccogli():
    try:
        # Incolla qui sotto la chiave, assicurandoti che resti tra le triple virgolette
        pk = """-----BEGIN PRIVATE KEY-----
INCOLLA_QUI_TUTTO_IL_CONTENUTO_DELLA_TUA_CHIAVE
-----END PRIVATE KEY-----"""

        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": "gorlanews-by-max",
            "private_key": pk.strip(),
            "client_email": "firebase-adminsdk-fbsvc@gorlanews-by-max.iam.gserviceaccount.com",
            "token_uri": "https://oauth2.googleapis.com/token",
        })

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gorlanews-by-max-default-rtdb.europe-west1.firebasedatabase.app/'
            })

        # Test di scrittura rapido
        db.reference('/stato').set("Motore Acceso!")

        # Scarichiamo le notizie
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get("https://comune.gorlaminore.va.it/home", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        notizie = {f"n_{i}": a.text.strip() for i, a in enumerate(soup.select('.card-title')[:10])}
        
        if notizie:
            db.reference('/notizie').set(notizie)
            print("✅ DATI INVIATI!")

    except Exception as e:
        print(f"❌ ERRORE: {e}")

if __name__ == "__main__":
    raccogli()
