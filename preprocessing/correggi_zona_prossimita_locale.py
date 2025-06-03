# ALTRO SCRIPT DI PREPROCESSING PER CORREGGERE I VALORI MANCANTI O VUOTI DELL'ELEMENTO <zona-prossimita>
# SICCOME ALCUNI VALORI ERANO MANCANTI PER QUANTO RIGUARDA ZONA DI PROSSIMITA, ABBIAMO PENSATO
# DI SOSTITUIRE LA MANCANZA DI ZONA DI PROSSIMITÀ CON UN VALORE DI DEFAULT ' QUARTIERE SCONOSCIUTO ' 

from lxml import etree
import os

# --- Configurazione dei percorsi ---
BASE_DIR = '/Users/mariocorrente/Desktop/progetto_rasta/file_principali/'
xml_file_path = os.path.join(BASE_DIR, 'eventi_bologna.xml') # Il tuo file XML originale

# Nome per il file XML modificato (salveremo una nuova versione per sicurezza)
# Questo file sarà salvato nella stessa cartella del progetto
output_xml_file_path = os.path.join(BASE_DIR, 'eventi_bologna_corretto.xml') 

default_zona_prossimita_value = "Quartiere sconosciuto"

print(f"Inizio correzione dell'elemento <zona-prossimita> nel file: {xml_file_path}\n")

modified_count = 0

try:
    # Parsifica il file XML
    tree = etree.parse(xml_file_path)
    root = tree.getroot() # Ottieni l'elemento radice
    print("File XML parsificato con successo.\n")

    # Seleziona tutti gli elementi <evento>
    events = root.xpath('//evento')
    print(f"Trovati {len(events)} eventi totali nell'XML.\n")

    for i, event in enumerate(events):
        event_id = event.xpath('id/text()')
        event_title = event.xpath('titolo/text()')
        
        event_id_str = event_id[0] if event_id else f"Evento senza ID (posizione: {i+1})"
        event_title_str = event_title[0] if event_title else "Titolo non disponibile"

        zona_prossimita_element = event.xpath('zona-prossimita')

        if not zona_prossimita_element:
            # L'elemento <zona-prossimita> è mancante, crealo e aggiungilo
            # Lo aggiungiamo come ultimo figlio dell'elemento 'evento'
            new_zona_prossimita = etree.SubElement(event, 'zona-prossimita')
            new_zona_prossimita.text = default_zona_prossimita_value
            print(f"  - Aggiunto e valorizzato <zona-prossimita> per '{event_title_str}' (Mancante).")
            modified_count += 1
        else:
            # L'elemento esiste, controlliamo il suo valore
            zona_prossimita_tag = zona_prossimita_element[0]
            if not zona_prossimita_tag.text or zona_prossimita_tag.text.strip() == "":
                # L'elemento è presente ma vuoto o contiene solo spazi bianchi, valorizzalo
                zona_prossimita_tag.text = default_zona_prossimita_value
                print(f"  - Valorizzato <zona-prossimita> per '{event_title_str}' (Era vuoto).")
                modified_count += 1
    
    # Salva il file XML modificato
    # Usiamo 'pretty_print=True' per formattare l'XML in modo leggibile
    # xml_declaration=True aggiunge <?xml version="1.0" encoding="utf-8"?> all'inizio
    tree.write(output_xml_file_path, pretty_print=True, encoding='utf-8', xml_declaration=True)

    print(f"\nCorrezione completata!")
    print(f"Totale elementi <zona-prossimita> corretti: {modified_count}.")
    print(f"Il file XML modificato è stato salvato come: {output_xml_file_path}")
    print(f"Ricorda di usare 'eventi_bologna_corretto.xml' per le prossime elaborazioni.")

except FileNotFoundError:
    print(f"ERRORE: Il file XML '{xml_file_path}' non è stato trovato. Assicurati che il percorso sia corretto.")
except etree.XMLSyntaxError as e:
    print(f"ERRORE DI SINTASSI XML: Il file XML ha problemi di sintassi e non può essere parsificato. Dettagli: {e}")
except Exception as e:
    print(f"Si è verificato un errore imprevisto durante la correzione: {e}")