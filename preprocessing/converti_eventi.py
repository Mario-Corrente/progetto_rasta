# Questo codice è utile per convertire dati strutturati in JSON in un formato XML
# Definisce la funzione `convert_json_to_xml` che legge un file JSON
# lo converte in XML e lo salva in un file specificato.
#

import json
from xml.etree.ElementTree import Element, SubElement, tostring # questa serve a creare gli elementi XML
from xml.dom import minidom # questa serve a formattare l'XML in modo leggibile
import os # questa serve per gestire i percorsi dei file in modo indipendente dal sistema operativo

def convert_json_to_xml(json_file_path, xml_file_path):                     # questa riga serve a definire la funzione di conversione
    try:                                                                    # questa riga serve a gestire le eccezioni
        with open(json_file_path, 'r', encoding='utf-8') as f:              # questa riga serve ad aprire il file JSON
            data = json.load(f)                                             # questa riga serve a caricare il contenuto del file JSON in un oggetto Python
    except FileNotFoundError:                                               # questa riga serve a gestire l'eccezione se il file non viene trovato                  
        print(f"Errore: Il file '{json_file_path}' non è stato trovato.")   # questa riga serve a stampare un messaggio di errore
        return                                                              # semplicemente esci dalla funzione
    except json.JSONDecodeError:                                            # qui andiamo a gestire l'eccezione se il file non è un JSON valido
        print(f"Errore: Il file '{json_file_path}' non è un JSON valido.")  # messaggio di errore
        return                                                              # semplicemente esci dalla funzione                     


    root = Element('eventi')                                                # questa riga serve a creare l'elemento radice dell'XML

    for item in data:                                                       # questa riga serve a iterare su ogni oggetto JSON tramite un ciclo for su ogni elemento 'evento'
        if 'id' not in item or item['id'] is None:                          # questa riga verifica se la chiave 'id' non è presente o se il suo valore è nullo
            print(f"AVVISO: Evento saltato perché mancante di ID o ID nullo. Titolo (se presente): {item.get('title', 'Sconosciuto')}") # Stampa un avviso per l'evento problematico
            continue                                                        # Salta completamente questo 'item' e passa al prossimo nel ciclo, non creando il tag <evento>
        evento = SubElement(root, 'evento')                                 # Crea un elemento 'evento' per ogni oggetto JSON che viene trovato con il ciclo for
        
        # L'ID è obbligatorio nel DTD, quindi lo settiamo qui, dato che ora siamo sicuri che esista e non sia nullo
        evento.set('id', str(item['id']))                                   # questa riga serve a settare l'id come attributo dell'elemento 'evento'   
                                                                            # quindi avremo gli elementi 'evento' con l'attributo 'id' che contiene il valore dell'id dell'oggetto JSON

        for key, value in item.items():                                     # questa riga serve a iterare su ogni coppia chiave-valore dell'oggetto JSON
            if key == 'id':                                                 # questa riga serve a saltare l'id perché lo abbiamo già gestito come attributo all'inizio del ciclo esterno
                continue
            
            if key == 'coordinate':                                         # questa riga serve a verificare se la chiave è 'coordinate'
                continue                                                    # se è 'coordinate', salta al prossimo elemento del ciclo, ignorando la creazione del tag XML
            
            # Mappatura dei nomi delle chiavi JSON a nomi XML più comprensibili (mantenuta)
            xml_tag_name = key.replace('_', '-') # Sostituisci underscore con trattini per nomi più "XML-friendly"
            xml_tag_name = xml_tag_name.replace('categories-1', 'categoria1')
            xml_tag_name = xml_tag_name.replace('categories-2', 'categoria2')
            xml_tag_name = xml_tag_name.replace('categories-3', 'categoria3')
            xml_tag_name = xml_tag_name.replace('start', 'data-inizio')
            xml_tag_name = xml_tag_name.replace('end', 'data-fine')
            xml_tag_name = xml_tag_name.replace('description', 'descrizione')
            xml_tag_name = xml_tag_name.replace('title', 'titolo')
            xml_tag_name = xml_tag_name.replace('address', 'indirizzo')
            xml_tag_name = xml_tag_name.replace('online', 'online')
            xml_tag_name = xml_tag_name.replace('bolognaestate', 'bologna-estate')
            xml_tag_name = xml_tag_name.replace('quartiere', 'quartiere')
            xml_tag_name = xml_tag_name.replace('area-metropolitana', 'area-metropolitana')
            xml_tag_name = xml_tag_name.replace('zona-di-prossimita', 'zona-prossimita')
            xml_tag_name = xml_tag_name.replace('area-statistica', 'area-statistica')
            
            # Gestione dei valori nulli, dizionari e liste (mantenuta)
            if value is None:
                SubElement(evento, xml_tag_name)
            elif isinstance(value, dict):
                nested_element = SubElement(evento, xml_tag_name)
                for nested_key, nested_value in value.items():
                    if nested_value is not None:
                        SubElement(nested_element, nested_key.replace('_', '-')).text = str(nested_value)
            elif isinstance(value, list):
                list_element = SubElement(evento, xml_tag_name)
                for list_item in value:
                    if list_item is not None:
                        SubElement(list_element, "item").text = str(list_item)
            else:
                sub_element = SubElement(evento, xml_tag_name)
                clean_text = str(value).replace('<p>', '').replace('</p>', '').strip()
                sub_element.text = clean_text

    # Funzione per prettify (formattare) l'XML (mantenuta)
    def prettify(elem):
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding="utf-8")

    # Scriviamo l'XML su file (mantenuta)
    with open(xml_file_path, 'wb') as f:
        f.write(prettify(root))
    
    print(f"Conversione completata! Il file XML è stato salvato come '{xml_file_path}'")

# Percorsi dei file (mantenuti)
BASE_DIR = '/Users/mariocorrente/Desktop/progetto_rasta/file_principali/'
json_input_file = os.path.join(BASE_DIR, 'eventi_bologna.json')
xml_output_file = os.path.join(BASE_DIR, 'eventi_bologna.xml')

# Esegui la conversione (mantenuta)
if __name__ == "__main__":
    convert_json_to_xml(json_input_file, xml_output_file)