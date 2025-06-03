# QUESTO SCRIPT PYTHON SERVE A PRODURRE UN REPORT A TERMINE DELL'ANALISI DELL'XML.
# CARICA L'XML, TROVA TUTTI GLI EVENTI E ANALIZZA LA PRESENZA E LA VALORIZZAZIONE DEI CAMPI.
# PER OGNI CAMPO SPECIFICATO IN `fields_to_check`, STAMPA IL NUMERO DI EVENTI VALORIZZATI.
# INOLTRE PRESENTA UN CONTROLLO PER EVITARE CHE I PLACEHOLDER VENGANO CONSIDERATI COME VALORIZZATI.

from lxml import etree
import os
from collections import defaultdict

# --- Configurazione del percorso del file XML ---
BASE_DIR = '/Users/mariocorrente/Desktop/progetto_rasta/file_principali/'
xml_file_path = os.path.join(BASE_DIR, 'eventi_bologna.xml')

print("=" * 60)
print(f" AVVIO ANALISI FILE XML: {xml_file_path}")
print("=" * 60)

try:
    tree = etree.parse(xml_file_path)
    root = tree.getroot()
    all_events = root.xpath('//evento')
    num_total_events = len(all_events)

    if num_total_events == 0:
        print("⚠ Nessun elemento <evento> trovato. L'analisi viene interrotta.")
        exit()

    print(f"\n✔ Trovati {num_total_events} elementi <evento> nel file XML.\n")

    # ========== SEZIONE 1: ANALISI PRESENZA ELEMENTI NIPOTI ==========
    print("-" * 60)
    print("SEZIONE 1: PRESENZA E VALORIZZAZIONE DIRETTA DI CAMPI SOTTO <evento>")
    print("-" * 60)

    fields_to_check = [
        'titolo', 'descrizione', 'url', 'indirizzo',
        'categoria1', 'categoria2', 'categoria3',
        'online', 'data-inizio', 'data-fine', 'date-multiple',
        'bologna-estate', 'quartiere', 'area-metropolitana',
        'zona-prossimita', 'area-statistica'
    ]

    for field in fields_to_check:
        events_with_valorized_field = root.xpath(f'//evento[{field} and normalize-space({field}) != ""]') # CONTROLLA SE CI SONO PLACEHOLDER
        count = len(events_with_valorized_field)
        percent = (count / num_total_events) * 100
        print(f"- '{field}': {count}/{num_total_events} valorizzati ({percent:.2f}%)")
        if count < num_total_events:                                                        # SE IL NUMERO DI EVENTI CON IL CAMPO VALORIZZATO È MENO DEL TOTALE
            print(f"  ↳ {num_total_events - count} eventi non hanno il campo '{field}' valorizzato o presente.")   # ALLORA STAMPA IL MESSAGGIO DI AVVISO CON IL NUMERO DI EVENTI MANCANTI

    # ========== SEZIONE 2: ANALISI RISPETTO AI VALORI DI DEFAULT ==========
    print("\n" + "-" * 60)                                              # È SOLO UN OUTPUT VISIVO PER RENDERE CHIARO IL REPORT A TERMINALE
    print("SEZIONE 2: VERIFICA CONTRO VALORI DI DEFAULT IMPOSTATI")
    print("-" * 60)

    elements_to_check = [
        'titolo', 'descrizione', 'data-inizio', 'data-fine', 'orario',
        'luogo', 'indirizzo', 'zona-prossimita', 'area-statistica',
        'sito-web', 'costo', 'email', 'telefono', 'organizzatore', 'categoria1'
    ]

    default_values = {
        'titolo': 'Non disponibile',
        'descrizione': 'Nessuna descrizione disponibile',
        'data-inizio': 'Non disponibile',
        'data-fine': '',
        'orario': 'Non specificato',
        'luogo': 'Non specificato',
        'indirizzo': 'Non disponibile',
        'zona-prossimita': '',
        'area-statistica': 'Non specificata',
        'sito-web': '#',
        'costo': 'Non specificato',
        'email': 'Non specificata',
        'telefono': 'Non specificato',
        'organizzatore': 'Non specificato',
        'categoria1': 'Senza Categoria'
    }

    valorized_counts = defaultdict(int)

    # QUESTO È IL CICLO PRINCIPALE CHE ANALIZZA OGNI CAMPO PER OGNI EVENTO
    for event_elem in all_events:
        for el in elements_to_check:
            text_values = event_elem.xpath(f'{el}/text()')
            text = text_values[0].strip() if text_values else ''
            default = default_values.get(el, '')

            if el == 'sito-web':
                if text and text != '#':
                    valorized_counts[el] += 1
            elif el in ['zona-prossimita', 'data-fine']:
                if text != '':
                    valorized_counts[el] += 1
            else:
                if text and text != default:
                    valorized_counts[el] += 1

    for el in elements_to_check:
        count = valorized_counts[el]
        percent = (count / num_total_events) * 100
        print(f"- '{el}': {count}/{num_total_events} valorizzati ({percent:.2f}%)")

    print("\n" + "=" * 60)
    print("✅ REPORT COMPLETATO.")
    print("=" * 60)

except FileNotFoundError:
    print(f"❌ ERRORE: File non trovato → '{xml_file_path}'")
except etree.XMLSyntaxError as e:
    print(f"❌ ERRORE DI SINTASSI XML: {e}")
except Exception as e:
    print(f"❌ ERRORE IMPREVISTO: {e}")
