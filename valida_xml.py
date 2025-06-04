# SEMPLICE SCRIPT PER PASSARE L'XML ALLA DTD E VALIDARLO

from lxml import etree
import os # Per gestire i percorsi in modo più robusto

# definiamo i percorsi dei file
BASE_DIR = '/Users/mariocorrente/Desktop/progetto_rasta/file_principali/'
xml_file_path = os.path.join(BASE_DIR, 'eventi_bologna.xml')
dtd_file_path = os.path.join(BASE_DIR, 'eventi_bologna.dtd')

print(f"Tentativo di validazione del file XML: {xml_file_path}")
print(f"Usando il DTD: {dtd_file_path}")

try:
    # 1. Carica il DTD
    with open(dtd_file_path, 'rb') as f:
        dtd = etree.DTD(f)              # utilizziamo la libreria lxml con etree.DTD per caricare il DTD
    print("DTD caricato con successo.")

    # 2. Parsifica il file XML (senza passare il DTD al parser)
    # Il DTD è già dichiarato nel file XML stesso, quindi lxml lo utilizzerà per il parsing
    tree = etree.parse(xml_file_path) # Rimosso l'argomento dtd qui
    print("File XML parsificato con successo.")
    
    # 3. Effettua la validazione esplicita sull'albero parsificato
    dtd.assertValid(tree) # Questa riga solleva un'eccezione se l'XML non è valido
    
    print("\n-------------------------------------------")
    print("✔️ CONFERMA: Il file XML è VALIDISSIMO rispetto al DTD!")
    print("-------------------------------------------")

except FileNotFoundError:
    print(f"\nERRORE: Assicurati che i file '{xml_file_path}' e '{dtd_file_path}' esistano e siano nei percorsi corretti.")
except etree.DocumentInvalid as e:
    print("\n-------------------------------------------")
    print("❌ ERRORE DI VALIDAZIONE: Il file XML NON è valido rispetto al DTD!")
    print("-------------------------------------------")
    print("Dettagli dell'errore:")
    # etree.DocumentInvalid contiene un log degli errori dettagliato
    for error in e.error_log:
        print(f"  Riga {error.line}, Colonna {error.column}: {error.message}")
    print("\nControlla il tuo XML e il DTD per correggere gli errori.")
except etree.XMLSyntaxError as e:
    print(f"\nERRORE DI SINTASSI XML: Il file XML ha problemi di sintassi e non può essere parsificato. Dettagli: {e}")
except Exception as e:
    print(f"\nSi è verificato un errore imprevisto: {e}")