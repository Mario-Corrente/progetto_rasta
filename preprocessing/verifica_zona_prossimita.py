from lxml import etree
import os

# --- Configurazione dei percorsi ---
BASE_DIR = '/Users/mariocorrente/Desktop/progetto_rasta/'
xml_file_path = os.path.join(BASE_DIR, 'eventi_bologna.xml')

print(f"Inizio verifica degli elementi <data-inizio> e <zona-prossimita> nel file: {xml_file_path}\n")

missing_or_empty_zona_prossimita = []
missing_or_empty_data_inizio = []

try:
    # Parsifica il file XML
    tree = etree.parse(xml_file_path)
    print("File XML parsificato con successo.\n")

    # Seleziona tutti gli elementi <evento>
    events = tree.xpath('//evento')
    print(f"Trovati {len(events)} eventi totali nell'XML.\n")

    for i, event in enumerate(events):
        # Estrai ID, Titolo e Data di Inizio
        event_id = event.xpath('id/text()')
        event_title = event.xpath('titolo/text()')
        date_inizio = event.xpath('data-inizio/text()')
        
        # Converte a stringa, gestendo il caso in cui ID o Titolo siano mancanti
        event_id_str = event_id[0] if event_id else f"Evento senza ID (posizione: {i+1})"
        event_title_str = event_title[0] if event_title else "Titolo non disponibile"
        date_inizio_str = date_inizio[0] if date_inizio else "Data di inizio non disponibile"

        # Verifica <zona-prossimita>
        zona_prossimita_element = event.xpath('zona-prossimita')
        if not zona_prossimita_element:
            # L'elemento <zona-prossimita> è mancante
            missing_or_empty_zona_prossimita.append(
                f"ID Evento: {event_id_str} - Titolo: '{event_title_str}' - <zona-prossimita> è MANCANTE."
            )
        else:
            # L'elemento esiste, ora controlliamo il suo valore
            zona_prossimita_value = zona_prossimita_element[0].text
            if not zona_prossimita_value or zona_prossimita_value.strip() == "":
                # L'elemento è presente ma vuoto o contiene solo spazi bianchi
                missing_or_empty_zona_prossimita.append(
                    f"ID Evento: {event_id_str} - Titolo: '{event_title_str}' - <zona-prossimita> è PRESENTE MA VUOTO."
                )

        # Verifica <data-inizio>
        date_inizio_element = event.xpath('data-inizio')
        if not date_inizio_element:
            missing_or_empty_data_inizio.append(
                f"ID Evento: {event_id_str} - Titolo: '{event_title_str}' - <data-inizio> è MANCANTE."
            )
        else:
            # L'elemento esiste, ora controlliamo il suo valore
            if not date_inizio_element[0].text or date_inizio_element[0].text.strip() == "":
                missing_or_empty_data_inizio.append(
                    f"ID Evento: {event_id_str} - Titolo: '{event_title_str}' - <data-inizio> è PRESENTE MA VUOTO."
                )

    # --- Riporta i risultati ---
    if not missing_or_empty_zona_prossimita:
        print("🎉 Ottimo! L'elemento <zona-prossimita> è valorizzato per TUTTI gli eventi.")
    else:
        print("\nATTENZIONE: Sono stati trovati eventi con <zona-prossimita> mancante o vuota:\n")
        for entry in missing_or_empty_zona_prossimita:
            print(f"- {entry}")
        print(f"\nTotale eventi con problemi: {len(missing_or_empty_zona_prossimita)} su {len(events)}.")

    if not missing_or_empty_data_inizio:
        print("🎉 Ottimo! L'elemento <data-inizio> è valorizzato per TUTTI gli eventi.")
    else:
        print("\nATTENZIONE: Sono stati trovati eventi con <data-inizio> mancante o vuota:\n")
        for entry in missing_or_empty_data_inizio:
            print(f"- {entry}")
        print(f"\nTotale eventi con problemi: {len(missing_or_empty_data_inizio)} su {len(events)}.")    

except FileNotFoundError:
    print(f"ERRORE: Il file XML '{xml_file_path}' non è stato trovato. Assicurati che il percorso sia corretto.")
except etree.XMLSyntaxError as e:
    print(f"ERRORE DI SINTASSI XML: Il file XML ha problemi di sintassi e non può essere parsificato. Dettagli: {e}")
except Exception as e:
    print(f"Si è verificato un errore imprevisto durante la verifica: {e}")