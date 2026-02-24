import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db
import os

def raccogli():
    try:
        # La tua chiave privata ricostruita correttamente
        pk = ("-----BEGIN PRIVATE KEY-----\n"
              "MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDarKfHsUJ2FLGq\n"
              "QWbi9X8WnpDwi489oqJ9Kj1cjdordZd7S81eqT8jr6IxkAH/HFEtRG1N+64hzoSW\n"
              "tM3RUq6lUjuFFFH2MzLlipM01hBtQkR6wOBCSxhO/Oq0doWUY/efMNIDEwUqvCDL\n"
              "kOPZIRdbX1H462Y2RBhZWj/NqbZfA4196CSwEl3b5q/+63e56wMTof/45mE9ubc7\n"
              "K3nhPEr/G/IoAPYQr5mUU6Gw5RRD59UXr8oPHhW9+4yhBERYrxymj2MsTnfJGZU7\n"
              "RkAAnGkY/++t9TKykmEvqoGWTDlpF2ta8HKwbFnAS70y+hVPx0as8gEOonfODYZx\n"
              "j494NgJfAgMBAAECggEABbU5W+5gkbx7Nrp7o7OiHEZfT31qa8LHAwVgkf3nPU3V\n"
              "z74WykBuCXxte2W1kkx8QfY7SYHRoHLyOwzVIoBKAWliwa0vcSxnnl4+TBlvrFUX\n"
              "0dcfA3FPsnV08D5NFlErBti7YqEoeAkZF2Hc0K9wcKN4UaBeC/noY3dbmv6xvUvK\n"
              "EMPJ+c0uOZTnSAwIwIrueXeB89F2lZLUutqWQYDswqXG4LzJaCd8krpKAykq1LEY\n"
              "DVj8U48iShUZdlisAKYbrZp4c6BM/e4/XPyaTlOCxVLpyvhx3QwcQSKXciM144FD\n"
              "0+EZRS3MhvYh5+Lt6w9UXHs+3IyjaW73fxZ7EkbLwQKBgQD8sJ5uMYwaVIlkyV4w\n"
              "+5kQwg9qNVVbZI86+LIbaCvNzKxkRVRAvX3oexX2W0N9LM4IKGPk8FXc0iV8jFD1\n"
              "/M0kHwm79GtrsrqeHgSjTBMBqOn0Og8UvQwIFFoRxhL/2obdl9JQQZ3sEQLWEBc5\n"
              "+mpucFV3fzS9Hp0yo4qbkkBfRwKBgQDdifexqr9TeiBOqJW8lKpJdGTHjGIsGmYE\n"
              "Uiv54kqYqKzj0INaOw8JG3KGscS8leLjJ5vbQvptam5fxvZlga1x42JtcHEFkWWO\n"
              "Rl1z9hxLk/L/KVaHSdTE3gfrahCELLiPYwEHwPQVk8AX60qLBfYsEZJCjrSRq7DW\n"
              "MOQbF8NAKQKBgQD7hYqNwP/mDZOdINuDAk0/4wqY+3F1QUlYt8gBg9VmSn6maGQO\n"
              "9Q9o42vfBsTMylZixGF6tsegwATUTo8f63z+oW59CjQKxaMAVHzlVonsswf9M/Vi\n"
              "/TIGsMteubybtBdeZwrPHCFnox8hmG6mJV7fgy1vfs0uGlT63NLRO+ibbQKBgQCR\nRkgHWdDdDNjiu+p1H4gLYygzMvutsCH182yjEKGaOgIl4jZAlTnm3vjbGvfIMwH1\n"
              "s6OgxOszlPeMFwy8w6zZYiLJYVK8M/xEsB/YSyuC5CIU8Sas0N2Vu4O1/HeYNTtR\n"
              "y7qBOybUf28YQFNBl0c23s7qlmoSnGP6EVWD7rE7AQKBgQC6edV4O++u1QkifE/c\n"
              "RYig+osADS1coSQjXcCO+eW89S3ryMuMN0+15HNvuqMmS8ZQXjdFwF+KNh4DYNv+\n"
              "NZIfIOmEmu2bo6DdXjF720ALBdh1ugH5gBu6g5/pBhg0skPNNCIMzDwT+G8Ne6hE\nh9VF5uHg6r7OjEa6PROuCSKXmg==\n"
              "-----END PRIVATE KEY-----\n")

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

        print("Connessione Firebase OK! Cerco le notizie...")
        res = requests.get("https://comune.gorlaminore.va.it/home")
        soup = BeautifulSoup(res.text, 'html.parser')
        
        notizie = {}
        articoli = soup.find_all(class_='card-title', limit=10)
        for i, a in enumerate(articoli):
            notizie[f"n_{i}"] = {"titolo": a.text.strip()}
            print(f"Trovata: {a.text.strip()}")
        
        db.reference('notizie').set(notizie)
        print("✅ TUTTO FATTO! DATI INVIATI!")

    except Exception as e:
        print(f"❌ ERRORE: {e}")

if __name__ == "__main__":
    raccogli()
