import requests
from bs4 import BeautifulSoup
import json
import datetime

# L'indirizzo del sito del Comune
URL_COMUNE = "https://comune.gorlaminore.va.it/home"

def scegli_immagine_di_riserva(titolo):
    """Sceglie un'immagine coerente se il comune non ne mette una"""
    titolo_lower = titolo.lower()
    if "scuola" in titolo_lower or "nido" in titolo_lower or "mensa" in titolo_lower:
        return "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=500&q=80" # Foto scuola
    elif "strada" in titolo_lower or "viabilità" in titolo_lower or "lavori" in titolo_lower:
        return "https://images.unsplash.com/photo-1584852955931-15858fc929c4?w=500&q=80" # Foto lavori stradali
    elif "rifiuti" in titolo_lower or "sacco" in titolo_lower:
        return "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=500&q=80" # Foto ambiente/riciclo
    elif "sociali" in titolo_lower or "contributi" in titolo_lower:
        return "https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?w=500&q=80" # Foto persone/sociale
    else:
        # Foto generica del municipio o paese per tutte le altre notizie
        return "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=500&q=80" 

def raccogli_notizie():
    print("Avvio ricerca notizie sul sito di Gorla Minore...")
    
    # Fingiamo di essere un browser normale per non farci bloccare dal sito
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        risposta = requests.get(URL_COMUNE, headers=headers)
        soup = BeautifulSoup(risposta.text, 'html.parser')
        
        notizie_trovate = []
        
        # Il sito del comune raggruppa le notizie in blocchi chiamati "Novità" o simili
        # (Questo è un selettore generico, lo perfezioneremo se il sito ha strutture diverse)
        articoli = soup.find_all('div', class_='Novità') 
        
        # Se non trova 'Novità', proviamo a cercare i tag generici degli articoli
        if not articoli:
            articoli = soup.find_all('article')
            
        for articolo in articoli[:5]: # Prendiamo le ultime 5 notizie
            
            # 1. Trova il Titolo
            titolo_tag = articolo.find(['h2', 'h3', 'a'])
            titolo = titolo_tag.text.strip() if titolo_tag else "Titolo non trovato"
            
            # 2. Trova la Data (cerca un tag temporale)
            data_tag = articolo.find('time')
            if data_tag:
                data = data_tag.text.strip()
            else:
                data = datetime.datetime.now().strftime("%d %B %Y")
                
            # 3. Trova l'Immagine (se esiste) o usa quella di riserva
            img_tag = articolo.find('img')
            if img_tag and img_tag.get('src'):
                immagine = img_tag.get('src')
                # Aggiusta il link se è "rotto" (relativo)
                if immagine.startswith('/'):
                    immagine = "https://comune.gorlaminore.va.it" + immagine
            else:
                immagine = scegli_immagine_di_riserva(titolo)
                
            # Creiamo il "pacchetto" della notizia
            notizia = {
                "titolo": titolo,
                "data": data,
                "immagineUrl": immagine
            }
            notizie_trovate.append(notizia)
            
        print(f"Trovate {len(notizie_trovate)} notizie!")
        for n in notizie_trovate:
            print(f"- {n['titolo']}")
            
        return notizie_trovate

    except Exception as e:
        print(f"Errore durante la lettura del sito: {e}")
        return []

# Avvia la funzione
if __name__ == "__main__":
    raccogli_notizie()
