# QUESTO SCRIPT CI SERVE A ESTRARE LE CATEGORIE UNICHE DAGLI EVENTI PRESENTI NELL'XML.
# STAVAMO CERCANDO UN MODO PER RAGGRUPPARE GLI EVENTI PRIMA DELLA GENERAZIONE DELLE PAGINE HTML
# QUESTO SCRIPT UTILIZZA LXML PER PARSIFICARE IL FILE XML E ESTRAE LE CATEGORIE UNICHE DAGLI ELEMENTI <categoria1>
# GRAZIE ALLA QUALE ABBIAMO POTUTO CREARE UN MENU DI NAVIGAZIONE PER LE PAGINE HTML. SEMPRE NELLA SEZIONE
# DI PREPROCESSING DEI DATI.


from lxml import etree
import os

# Definisci i percorsi dei tuoi file
BASE_DIR = '/Users/mariocorrente/Desktop/progetto_rasta/file_principali/'
xml_file_path = os.path.join(BASE_DIR, 'eventi_bologna.xml')

print(f"Tentativo di estrazione categorie uniche dal file XML: {xml_file_path}\n")

try:
    # Parsifica il file XML
    tree = etree.parse(xml_file_path)
    print("File XML parsificato con successo.\n")

    # --- Estrazione delle categorie uniche ---
    # XPath '//categoria1/text()' seleziona il testo di tutti gli elementi <categoria1>.
    
    all_categories = tree.xpath('//categoria1/text()')
    
    # Un set in Python è una collezione di elementi non ordinata e che non ammette duplicati.
    # Trasformando la lista di tutte le categorie in un set, otteniamo automaticamente solo quelle uniche.
    unique_categories = sorted(list(set(all_categories))) # Convertiamo in lista e ordiniamo per una migliore leggibilità

    if unique_categories:
        print("Ecco le categorie uniche di eventi trovate:")
        for category in unique_categories:
            print(f"- {category}") # Stampiamo le categorie con un trattino
    else:
        print("Nessuna categoria trovata.")

except FileNotFoundError:
    print(f"ERRORE: Il file '{xml_file_path}' non è stato trovato. Assicurati che il percorso sia corretto.")
except etree.XMLSyntaxError as e:
    print(f"ERRORE DI SINTASSI XML: Il file XML ha problemi di sintassi e non può essere parsificato. Dettagli: {e}")
except Exception as e:
    print(f"Si è verificato un errore imprevisto: {e}")