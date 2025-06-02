# importiamo le librerie necessarie per la parsificazione del file XML e la generazione delle pagine HTML
from lxml import etree     # lxml è una libreria per la manipolazione di XML e HTML in Python
import os                  # os è una libreria standard di Python per interagire con il sistema operativo, utile per gestire i percorsi dei file
from collections import defaultdict     # defaultdict è una classe di Python che permette di creare dizionari con valori predefiniti, utile per contare eventi per categoria e zona
from datetime import datetime           # datetime è una libreria standard di Python per lavorare con date e orari (ma alla fine abbiamo deciso di non utilizzare le date)
import html                             # html è una libreria standard di Python per gestire caratteri speciali HTML, utile per evitare problemi di visualizzazione 


####### in questo blocchetto andiamo a definire i percorsi dei file e le directory di output per la generazione delle pagine HTML

BASE_DIR = '/Users/mariocorrente/Desktop/progetto_rasta/file_principali/'
xml_file_path = os.path.join(BASE_DIR, 'eventi_bologna.xml')

output_root_dir = os.path.join(BASE_DIR, 'indice')
category_output_dir = os.path.join(output_root_dir, 'categorie')
images_dir = os.path.join(output_root_dir, 'images')
zone_images_dir = os.path.join(output_root_dir, 'immagini_zone')

################################## 
##################################

# Crea le directory se non esistono già. È una sorta di controllo di sicurezza.
os.makedirs(output_root_dir, exist_ok=True)
os.makedirs(category_output_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)
os.makedirs(zone_images_dir, exist_ok=True)

##################################
##################################

# Output viisibile per avvisare che stiamo iniziando la generazione delle pagine HTML
print(f"Tentativo di generazione pagine HTML dal file XML: {xml_file_path}\n")


try:                                            # con try andiamo a gestire eventuali errori che possono verificarsi durante la parsificazione del file XML
    tree = etree.parse(xml_file_path)           # Questa riga è quella che ci permette di parsificare il file XML e creare un albero di elementi ed evidenziare se dovessero esserci problemi di formattazione o sintassi
    root = tree.getroot()                       # ottiene l'elemento radice dell'albero XML
    print("File XML parsificato con successo.\n")       # se il file XML viene parsificato correttamente, stampa un messaggio di successo

    events_by_category_count = defaultdict(int)         # fondamentalmente è un dizionario che conterà gli eventi per categoria. (int) per inizializzare lo 0, potremmo anche inserire (list) per inizializzare una lista vuota, ma in questo caso non ci serve
    events_by_category_and_zona = defaultdict(lambda: defaultdict(list))  # invece qui usiamo (list) per inizializzare una lista vuota per suddividere gli eventi prima per categoria e poi per zona di prossimità
    
    unique_zone_prossimita = set()   # Un set è una collezione di elementi non ordinata e non indicizzata che non permette duplicati. Lo usiamo per raccogliere tutte le zone di prossimità uniche presenti nel file XML per permetterci
                                     # di non avere duplicati in lista e utile per la parte statistiche del report.

    # --- Variabili per le nuove statistiche ---
    all_events_data = [] # iniziamo una lista vuota per memorizzare i dati degli eventi

    zone_event_counts = defaultdict(int)    #defaultdict per contare gli eventi per zona di prossimità
                                            # defaultdict(int) inizializza il conteggio a 0 per ogni nuova chiave del dizionario
                                            # è una funzione standard di Python che permette di creare un dizionario con valori che 
                                            # estraiamo dal file XML e che non sono ancora stati valorizzati

    # --- Variabili per nuove statistiche dettagliate nel report ---
   # altri_eventi_count = 0  # qui inizializziamo un contatore per gli eventi che non rientrano in nessuna categoria specifica. una semplice var per conteggio
                            # la variabile non viene utilizzata nello specifico, ma potrebbe essere utile per un successivo sviluppo.
    # Esempio di un evento XML per il report descrittivo
    xml_example_snippet = ""   # questa riga inizializza una stringa vuota per memorizzare un esempio di evento XML che verrà usato nel report
    
    # Questo è l'elemento radice. Andiamo a cercare il secondo evento (perché il primo era troppo lungo per la visualizzazione in report) per mostrare un esempio di struttura XML
    first_event_elem = root.xpath('//evento[2]') # i due // indicano che stiamo cercando l'elemento <evento> in qualsiasi parte del documento XML, e [2] indica il secondo elemento che troviamo.
    if first_event_elem:    # controlla se abbiamo trovato almeno un evento con la condizione if
        # Prendi l'XML del primo evento e lo formatti per la visualizzazione
        xml_example_snippet = etree.tostring(first_event_elem[0], pretty_print=True, encoding='unicode') # etree.tostring() converte l'elemento XML in una stringa formattata, con pretty_print=True per renderlo più leggibile
                                                                                                         # e first_event_elem[0] è il primo elemento trovato, [0] serve a prendere il primo elemento della lista restituita da xpath (questo verrà utilizzato nel report)
     #   xml_example_snippet = "\n".join([line.lstrip() for line in xml_example_snippet.split('\n')])     # questa riga serve a rimuovere gli spazi iniziali da ogni riga dell'XML per renderlo più leggibile nel report finale

        # IL SUCCESSIVO CICLO FOR È IL CUORE DELLA GENERAZIONE DELLE PAGINE HTML
    
    for event_elem in root.xpath('//evento'):   # Itera su ogni elemento <evento> trovato nel file XML. Ad ogni iterazione, event_elem diventa l'oggetto lxml che rappresenta l'evento corrente
                                                # se l'elemento radice dovesse cambiare da <evento> a <programma>, basterà cambiare il nome dell'elemento qui.
        event_data = {}                         # Creiamo un dizionario per memorizzare i dati dell'evento corrente al fine di inserire i dati in un file HTML
        
        # nel blocco successivo andiamo a inserire nel dizionario event_data tutti gli elementi figli di <evento> che ci interessano, con un controllo per evitare errori se l'elemento non esiste (in realtà il controllo sarebbe superfluo perché abbiamo fatto un preprocessing dei dati)
        # tuttavia, per un codice ''sostenibile'' è consigliabile inserire il controllo con l'else per evitare errori di KeyError se l'elemento non esiste nel file XML.
        event_data['titolo'] = event_elem.xpath('titolo/text()')[0] if event_elem.xpath('titolo/text()')else 'Non disponibile'
        
        # nello specifico significa che nell'elemento <evento> cerchiamo l'elemento <titolo> e prendiamo il suo testo, se esiste
        # e ripetiamo l'operazione per tutti gli elementi che ci interessano per la generazione delle pagine HTML
        # se volessimo inserire altri elementi, basterebbe aggiungere altre righe simili a quelle che seguono con i loro tag XML specifici
        event_data['indirizzo'] = event_elem.xpath('indirizzo/text()')[0] if event_elem.xpath('indirizzo/text()') else 'Non disponibile'
        event_data['descrizione'] = event_elem.xpath('descrizione/text()')[0] if event_elem.xpath('descrizione/text()') else 'Nessuna descrizione disponibile'
        event_data['url'] = event_elem.xpath('url/text()')[0] if event_elem.xpath('url/text()') else '#'
        event_data['zona_prossimita'] = event_elem.xpath('zona-prossimita/text()')[0] if event_elem.xpath('zona-prossimita/text()') else ''
        event_data['area_statistica'] = event_elem.xpath('area-statistica/text()')[0] if event_elem.xpath('area-statistica/text()') else 'Non specificata'    
        event_data['sito_web'] = event_elem.xpath('sito-web/text()')[0] if event_elem.xpath('sito-web/text()') else '#'
        
        all_events_data.append(event_data)    # qui andiamo ad aggiungere i dati dell'evento corrente alla lista all_events_data, che conterrà tutti gli eventi del file XML

        # con la riga successiva andiamo ad estrarre l'elemento 0 della lista restituita da xpath, che contiene il testo dell'elemento <categoria1>. Noi useremo sempre [0] perché sappiamo che ogni evento ha al massimo una categoria principale.
        # in caso la struttura di <categoria1> fosse qualcosa tipo:
        # <categoria1>
        #    <nome>Categoria Principale</nome>
        #    <nome>Categoria Secondaria</nome>  
        #    <nome>Categoria Terziaria</nome>
        # allora se cercassimo di estrarre il secondo elemento di <nome> dovremmo utilizzare [1] con xpath('categoria1/nome/text()') per ottenere il testo del secondo tag <nome> dalla lista.
        category = event_elem.xpath('categoria1/text()')[0] if event_elem.xpath('categoria1/text()') else 'Senza Categoria'   # ci serve per estrarre la categoria principale dell'evento corrente
        events_by_category_count[category] += 1      # qui andiamo ad incrementare il conteggio degli eventi per la categoria corrente                                                                      


        # questo blocchetto successivo serve a gestire eventuali valori vuoti o mancanti per la zona di prossimità
        # mentre event_data['zona_prossimita'].strip() rimuove gli spazi bianchi all'inizio e alla fine della stringa per evitare problemi di matching
        # se avessimo per esempio 'BARCA' e ' BARCA ' queste verrebbero trattati allo stesso modo
        zona_prossimita = event_data['zona_prossimita'].strip() 
        if not zona_prossimita:
             zona_prossimita = "Quartiere sconosciuto"
        
        unique_zone_prossimita.add(zona_prossimita)     # Aggiunge la zona di prossimità al set per raccogliere le zone uniche
        
        zone_event_counts[zona_prossimita] += 1         # Qui andiamo ad incrementare il conteggio degli eventi per la zona di prossimità corrente

        events_by_category_and_zona[category][zona_prossimita].append(event_data)  # Questa è l'operazione che sfrutta il defaultdict annidato. 
        # Prende la categoria, poi la zona di prossimità all'interno di quella categoria, 
        # e aggiunge l'intero dizionario event_data a quella lista.

    unique_categories = sorted(events_by_category_count.keys())      # ordiniamo le categorie uniche in ordine alfabetico
    
    # questi doopo sono cicli per stampare le categorie uniche e le zone di prossimità uniche trovate nel file XML.
    # è una sorta di report preliminare a terminale. non necessarie al funzionamento del codice per la generazione delle html.
    
    ######### PRINT A TERMINALE ###############
    #### NON INDISPENSABILE PER LA GENERAZIONE DELLE PAGINE HTML ####

    # print(f"Trovate {len(unique_categories)} categorie uniche.")
    # print("Elenco delle categorie uniche:")
    # for cat in unique_categories:
    #     print(f"- {cat}")     # qui andiamo semplicemente a stampare le categorie uniche trovate nel file XML
    # print()
    
    # print(f"Ci sono {len(unique_zone_prossimita)} zone di prossimità uniche nel dataset.\n") # messa in output del numero di zone di prossimità uniche trovate nel file XML
    # print("Elenco delle zone di prossimità uniche:")
    # for zona in sorted(list(unique_zone_prossimita)):
    #     print(f"- {zona}")
    # print()

    #############################################

    # qui andiamo a mappare le immagini delle categorie e delle zone di prossimità in base ai nomi. 
    # category_images, zone_images: Questi sono dizionari (mappe) 
    # che associano un nome di categoria/zona (usato nel codice) al nome del file immagine corrispondente.

    category_images = {
        'altri-spazi': 'altrispazi.jpeg',
        'amministrazione-locale': 'amministrazioni.jpeg',
        'anagrafe-e-statistiche': 'anagrafe.jpeg', 'archeologia': 'archeologia.jpeg',
        'architettura-e-urbanistica': 'architettura.jpeg', 'arte': 'arte.jpeg',
        'assistenza-e-sanita': 'sanita.jpeg', 'biblioteche': 'biblioteche.jpeg',
        'bibliotechebologna': 'bibliotechebologna.jpeg', 'campagne-mondo-rurale': 'campagna_rurale.jpeg',
        'chiesa-locale-e-culti': 'chiesaeculti.jpeg', 'cinema': 'cinema.jpeg',
        'conferenze-e-convegni': 'conferenze.jpeg', 'culturabolognaparent': 'bolognaparent.jpeg',
        'gallerie': 'gallerie.jpeg', 'incontri': 'incontri.jpeg',
        'istituzioni': 'istituzioni.jpeg', 'itinerari': 'itinerari.jpeg',
        'laboratori': 'laboratori.jpeg', 'libri': 'libri.jpeg',
        'mostre': 'mostre.jpeg', 'musica': 'musica.jpeg',
        'proiezioni': 'proiezioni.jpeg', 'special-projects': 'specialproj.jpeg',
        'spettacoli': 'spettacoli.jpeg', 'teatro-e-danza': 'teatro_e_danza.jpeg',
        'visite-guidate': 'visiteguidate.jpeg', 'senza-categoria': 'senzacategoria.jpeg'
    }
    default_image = 'default.jpg'   # immagine di fallback per le categorie che non hanno un'immagine specifica
    # noi abbiamo tutte le immagini quindi questo sarebbe una gestione delle eccezioni. utile per un codice ''sostenibile''.

    zone_images = {
        'BARCA': 'barca.png', 
        'BERTALIA - NOCE': 'bertalia_noce.png', 'BEVERARA': 'beverara.png',
        'BIRRA - BARGELLINO - LAVINO': 'birra_bargellino_lavino.png', 'BOLOGNINA': 'bolognina.png',
        'BORGO PANIGALE': 'borgo_panigale.png', 'CASTELDEBOLE - PONTELUNGO': 'casteldebole_pontelungo.png',
        'CIRENAICA - MASSARENTI - SCANDELLARA': 'cirenaica_massarenti_scandellara.png',
        'CORTICELLA - DOZZA': 'corticella_dozza.png', 'CROCE DEL BIACCO - ROVERI': 'croce_del_biacco_roveri.png',
        'FOSSOLO - DUE MADONNE': 'fossolo_due_madonne.png', 'Fuori Bologna': 'fuori_bologna.png',
        'GALVANI': 'galvani.png', 'IRNERIO': 'irnerio.png', 'LUNGO SAVENA': 'lungo_savena.png',
        'MALPIGHI': 'malpighi.png', 'MARCONI': 'marconi.png', 'MURRI': 'murri.png',
        'OSSERVANZA - PADERNO': 'osservanza_paderno.png', 'PONTEVECCHIO - MAZZINI': 'pontevecchio_mazzini.png',
        'SAFFI': 'saffi.png', 'SAN DONATO NUOVO': 'san_donato_nuovo.png', 'SAN DONATO VECCHIO': 'san_donato_vecchio.png',
        'SANTA VIOLA': 'santa_viola.png', 'SARAGOZZA - SAN LUCA': 'saragozza_sanluca.png',
        'VIA TOSCANA - S. RUFFILLO - MONTE DONATO': 'via_toscana_sruffillo_monte_donato.png',
        'Quartiere sconosciuto': 'fuori_bologna.png'
    }

    default_zone_image = 'default_zone.jpg' # stessa identica cosa di prima. immagine di fallback per le zone di prossimità che in realtà non abbiamo un'immagine di fallback

    # ora andiamo a mappare i nomi per poterli ridefinire nella homepage, per non avere i nomi originali ma più ''user-friendly''.

    nomi_a_video = {
        'senza-categoria' : 'Senza categoria',
        'altri-spazi': 'Altri spazi', 
        'amministrazione-locale': 'Amministrazione locale',
        'anagrafe-e-statistiche': 'Anagrafe e statistiche',
        'archeologia': 'Archeologia',
        'architettura-e-urbanistica': 'Architettura e urbanistica',
        'arte': 'Arte',
        'assistenza-e-sanita': 'Assistenza e sanità',
        'biblioteche': 'Biblioteche',
        'bibliotechebologna': 'Biblioteche Bologna',
        'campagne-mondo-rurale': 'Campagne e mondo rurale',
        'chiesa-locale-e-culti': 'Chiesa locale e culti',
        'cinema': 'Cinema',
        'conferenze-e-convegni': 'Conferenze e convegni',
        'culturabolognaparent': 'Cultura Bologna parent',
        'gallerie': 'Gallerie',
        'incontri': 'Incontri',
        'istituzioni': 'Istituzioni',
        'itinerari': 'Itinerari',
        'laboratori': 'Laboratori',
        'libri': 'Libri',
        'mostre': 'Mostre',
        'musica': 'Musica',
        'proiezioni': 'Proiezioni',
        'special-projects': 'Progetti speciali',
        'spettacoli': 'Spettacoli',
        'teatro-e-danza': 'Teatro e danza',
        'visite-guidate': 'Visite guidate',
    }

    ###################################################
    #  BLOCCO PER GENERAZIONE DELLE SINGOLE PAGINE PER CATEGORIA
    ###################################################

    # Questo loop itera su ogni categoria unica identificata nel XML. 
    # Per ogni categoria, verrà generata una pagina HTML separata.
    # tutto quello annidato in questo ciclo for è il cuore della generazione delle pagine HTML per ogni categoria.
    # N.B.: QUESTO È IL CICLO FOR CHE ITERA SU TUTTE LE CATEGORIE UNICHE TROVATE NEL FILE XML E 
    # GENERA PER OGNI CATEGORIA UNA PAGINA HTML SEPARATA.

    for category in unique_categories:    
        safe_category_name = category.lower().replace(' ', '-').replace('/', '-').replace('.', '').replace(',', '').replace(':', '').replace('(', '').replace(')', '') # questa è una semplce stringa di riformattazione dei nomi delle categorie per renderli "URL-friendly"
        category_html_filepath = os.path.join(category_output_dir, f"{safe_category_name}.html")  # questo costruisce il percorso del file HTML per la cateforia.
        
        # questa riga serve a recuperare il nome del file immagine associato alla categoria.
        category_image_filename = category_images.get(safe_category_name, default_image) 

        # html_content = f"""  # questa riga serve a creare il contenuto HTML della pagina per ogni categoria.
        # e utilizza f-string per inserire dinamicamente il nome della categoria e il percorso dell'immagine.
        #  Permette di scrivere blocchi di testo (in questo caso, HTML) includendo variabili Python 
        # direttamente all'interno delle graffe {}. È estremamente comodo per generare HTML.
        # Inoltre, in questo blocchetto andiamo anche a inserire i microdati per la definizione semantica.
        # In questo caso, stiamo definendo il container, che definiamo come ItemList perché
        # a livello semantico abbiamo definito una lista di Item che contiene appunto gli eventi. 
        # la costruzione dinamica del contenuto HTML risulta molto utile e facilmente leggibile.
        # richiamiamo il file CSS per lo stile della pagina HTML con class="container" e l'href per il file CSS.

        html_content = f"""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Eventi - Categoria: {category}</title>
            <link rel="stylesheet" href="../style.css">
        </head>
        <body>
            <div class="container">
                <h1>Eventi nella categoria: {category}</h1>
                <p><a href="../index.html"><u><b>TORNA ALLA HOMEPAGE</b></u></a></p>
        """

        zone_groups = events_by_category_and_zona.get(category, {})  # qui andiamo a recuperare gli eventi per la categoria corrente, raggruppati per zona di prossimità e li inseriamo in un dizionario chiamato zone_groups.
        #Recupera tutti gli eventi per la categoria corrente, raggruppati per zona. 
        # Se la categoria non avesse eventi, restituisce un dizionario vuoto. (impossibile nel nostro caso, ma è una buona prassi per codice sostenibile)

        if not zone_groups:
            html_content += "<p>Nessun evento trovato per questa categoria.</p>" # se non ci sono eventi per la categoria corrente, aggiungiamo un messaggio che informa l'utente che non ci sono eventi disponibili.
        else:                  # se invece ci sono eventi per la categoria corrente, procediamo a generare il contenuto HTML per visualizzarli.
            html_content += '<h2>Naviga per Zona di Prossimità:</h2>\n'   # Creiamo quindi l'h2 per la sezione di navigazione delle zone di prossimità all'interno della categoria selezionata.
            html_content += '<div class="category-grid">\n'               # e <div> per creare una griglia di link alle zone di prossimità.
            sorted_zones = sorted(zone_groups.keys())                     # Qui andiamo a ordinare le zone di prossimità in ordine alfabetico per una migliore leggibilità.
            for zona_prossimita in sorted_zones:                          # con il ciclo aggiungiamo il numero di eventi in ogni zona di prossimità e l'immagine associata.
                num_events_in_zone = len(zone_groups[zona_prossimita])    # in questa riga andiamo a contare il numero di eventi in ogni zona di prossimità. 
                                                                          # utile per visualizzare il numero di eventi disponibili in quella zona.
                
                current_zone_image_filename = zone_images.get(zona_prossimita, default_zone_image)   # questa riga serve a recuperare il nome del file immagine associato alla zona di prossimità corrente con il metodo get() del dizionario zone_images.
                                                                               # in teoria, nel nostro caso default_zone_image non dovrebbe è necessaria. 

                safe_anchor_name = zona_prossimita.lower().replace(' ', '-').replace('/', '-').replace('.', '').replace(',', '').replace(':', '').replace('(', '').replace(')', '') # di nuovo andiamo a riformattare il nome della zona di prossimità per renderlo "URL-friendly" e utilizzabile come anchor link.
                
                # nel successivo blocco di codice aggiungiamo alla var html_content (che è quella che genera il contenuto HTML della pagina) 
                # il link alla zona di prossimità con l'immagine e il numero di eventi in quella zona.
                # safe_anchor_name è la variabile che contiene il nome della zona di prossimità riformattati
                # e le definiamo come category-card zone-card richiamando gli stili CSS definiti nel file style.css.

                html_content += f"""
                <a href="#{safe_anchor_name}" class="category-card zone-card">
                    <img src="../immagini_zone/{current_zone_image_filename}" alt="{zona_prossimita} icon">
                    <span>{zona_prossimita} ({num_events_in_zone} eventi)</span>
                </a>
                """
            html_content += '</div>\n'    # e con la chiusura del div chiudiamo la sezione di navigazione delle zone di prossimità
                                          # iniziata nel ciclo for sopra.


            # Ora andiamo a generare il contenuto HTML per ogni zona di prossimità con i relativi eventi
            # sempre utilizzando il ciclo for sopra per iterare su ogni zona di prossimità ed eventi, ordinando gli 
            # eventi dentro le zone di prossimità ordinate alfabeticamente.
            # Creiamo quindi un h2 con id safe_anchor_name che sono i nomi riformattati delle zone di prossimità per poter essere utilizzati come anchor link.
            # e poi sempre nell'h2 ci scriviamo la zona di prossimità, ma per rendere il codice dinamico, inseriamo la var
            # zona_prossimita che contiene il nome della zona di prossimità corrente, per renderlo adattabile a tutte le pagine che verrano generate.
            # infine chiudiamo il blocco principale del for richiamando la classe events-list del CSS.

            for zona_prossimita, events_in_zona in sorted(zone_groups.items()):
                safe_anchor_name = zona_prossimita.lower().replace(' ', '-').replace('/', '-').replace('.', '').replace(',', '').replace(':', '').replace('(', '').replace(')', '')
                html_content += f'<h2 id="{safe_anchor_name}">Zona di Prossimità: {zona_prossimita}</h2>\n'
                html_content += '<div class="events-list" itemscope itemtype="https://schema.org/ItemList">\n'
                
                # entriamo nel ciclo annidato per iterare sugli eventi all'interno della zona di prossimità corrente.
                # entriamo negli eventi nella lista di zone di prossimità ordinati alfabeticamente.
                # key=lambda x: x.get('titolo', ''): All'interno di ogni zona, gli eventi vengono ordinati per titolo. 
                # lambda x: x.get('titolo', '') è una funzione anonima che dice "prendi il valore della chiave 'titolo'
                # dall'elemento x (che è un dizionario), e se non c'è, usa una stringa vuota per l'ordinamento"
                # Estraiamo i dati dell'evento dal dizionario event, tipo event['titolo']), event['descrizione'] e li
                #  usiamo per generare il contenuto HTML della pagina, della sezione del singolo evento suddiviso per categoria.

                for event in sorted(events_in_zona, key=lambda x: x.get('titolo', '')):
                    titolo = event['titolo']
                    descrizione = event['descrizione']
                    indirizzo = event['indirizzo']
                    url = event['url'] # Recupera l'URL estratto
                    sito_web = event['sito_web']
                    zona_prossimita_display = event['zona_prossimita']
                    area_statistica = event['area_statistica']
                    
                    # questo è il blocco che genera il contenuto HTML per ogni evento e semanticamente arricchito
                    html_content += f"""
                    <div class="event-detail-card" itemscope itemtype="https://schema.org/Event">
                        <h3 itemprop="name"> {titolo}</h3>
                       <div> <strong> Descrizione evento: </strong> <p itemprop="description"> {descrizione}</p> </div>
                    """
                    # Ora in teoria ci sono una serie di if per verificare la presenza di dati per la generazione delle pagine.
                    # In linea di massima, avendo fatto un robusto preprocessing per assicurarci che tutti i dati di nostro interesse
                    # siano presenti, questi if non sarebbero necessari, ma in ottica di codice sostenibile e facilmente adattabile a futuri cambiamenti,
                    # è buona prassi inserire questi controlli per evitare errori di KeyError o di visualizzazione
                    # Quindi conviene sempre inserire dei controlli di verifica.
                    # Avendo fatto il preprocessing potremmo direttamente procedere con gli html_content += f""" e il pezzo che vogliamo
                    # aggiungere alla pagina.

                    if indirizzo != 'Non disponibile' or zona_prossimita_display != 'Quartiere sconosciuto':
                        html_content += '            <div itemprop="location" itemscope itemtype="https://schema.org/Place">\n'
                    if zona_prossimita_display != 'Quartiere sconosciuto':
                        html_content += f'    <p><strong>Zona di Prossimità:</strong> <span itemprop="name">{zona_prossimita_display}</span></p>\n'
                    if indirizzo != 'Non disponibile':
                        html_content += f'    <p><strong>Indirizzo:</strong> <span itemprop="address">{indirizzo}</span></p>\n'
                    if area_statistica != 'Non specificata': html_content += f"<p><strong>Area Statistica:</strong> {area_statistica}</p>\n"
                    html_content += """ </div>\n""" # Chiude il blocco di location
                    
                    # Questo successivo è un controllo particolare sull'url. In teoria, se il preprocessing è fatto perfettamente,
                    # l'url è sempre presente e potremmo inserire direttamente:
                    # html_content += f"<p itemprop='url'><strong>Maggiori Info:</strong> <a href=\"{url}\" target=\"_blank\">{url}</a></p>\n"
                    # Tuttavia, come al solito, un controllo di verifica è sempre utile per evitare errori di visualizzazione in uno script sostenibile.
                    display_url = url
                    if display_url == '#' and sito_web != '#' and sito_web.strip() != '': # Se url è default, controlla sito_web
                        display_url = sito_web     
                    if display_url != '#' and display_url.strip() != '':
                        html_content += f" <strong>Maggiori Info:</strong> <p itemprop='url'><a href=\"{display_url}\" target=\"_blank\">{display_url}</a></p>\n"                  
                    html_content += """
                    </div>
                    """
                     # Qui chiudiamo il blocco principale della lista degli eventi per la zona di prossimità corrente.
        html_content += """
            </div>
        </body>
        </html>
        """
    ###################################################
    # FINE BLOCCO GENERAZIONE DELLE PAGINE HTML PER CATEGORIA
    ###################################################
        
        # e qui andiamo a scrivere il contenuto HTML generato nel file specificato.
        with open(category_html_filepath, 'w', encoding='utf-8') as f:       # questa riga serve a scrivere il contenuto HTML nel file
            f.write(html_content)                                            # scrive il contenuto HTML generato nel file specificato.
        print(f"Generato: {category_html_filepath}")                         # Avviso che il file HTML è stato generato correttamente

    ###################################################
    # BLOCCO PER CALCOLO DELLE STATISTICHE PER LA PAGINA REPORT
    ###################################################

    total_events_for_report = len(all_events_data) # calcola la lunghezza della lista all_events_data per ottenere il numero totale di eventi
                                                   # che ci serve per il calcolo delle statistiche nel report finale.

    # report_elements_to_check = []  # Inizializza una lista vuota per gli elementi da controllare nel report
    # sono gli elementi che andremo a controllare per il report finale.

    report_elements_to_check = [
        'titolo', 'descrizione', 'url', 
        'indirizzo', 'zona_prossimita', 'area_statistica', 'categoria1'
    ]
    
    # Qui andiamo a creare un dizionario per contare gli eventi non valorizzati per ogni elemento che ci interessa.
    # per conteggiare gli eventi non valorizzati per ogni elemento che ci interessa.

    not_valorized_defaults = {
        'titolo': 'Non disponibile',
        'descrizione': 'Nessuna descrizione disponibile',
        'url': '', 
        'sito_web': '', 
        'indirizzo': 'Non disponibile',
        'zona_prossimita': '',
        'area_statistica': 'Non specificata',
        'categoria1': 'Senza Categoria'
    }

    # Qui andiamo a creare un dizionario per contare gli eventi per ogni categoria
    # per conteggiare gli eventi valorizzati per ogni elemento che ci interessa.
    element_valorized_counts = defaultdict(int)

    # il ciclo for ci serve per iterare su tutti gli eventi raccolti in all_events_data
    # per ogni elemento event_data in all_events_data, andiamo a controllare se i campi sono valorizzati o meno
    # escludendo 'url' e 'sito_web' per ora, che gestiremo dopo in un blocco specifico.
    for event_data in all_events_data:
        # Controlla gli altri campi singolarmente, ignorando 'url' e 'sito_web' per ora
        for element_name_key, default_val in not_valorized_defaults.items():
            if element_name_key in ['url', 'sito_web']:
                continue # Salta url e sito_web, li gestiremo dopo
            
            # qui andiamo a gestire la corrispondenza tra il nome nello script e il nome dell'elemento XML
            xml_element_name = element_name_key
            if element_name_key == 'zona_prossimita': xml_element_name = 'zona-prossimita'
            elif element_name_key == 'area_statistica': xml_element_name = 'area-statistica'
            elif element_name_key == 'categoria1': xml_element_name = 'categoria1'

            # recupera il valore effettivo dell'evento per l'elemento corrente
            # ottiene il dato reale dell'evento da controllare per la valorizzazione
            actual_value_for_check = event_data.get(element_name_key)

            # Applica una regola specifica per categoria1, distinguendo tra 
            # la presenza di una categoria reale e il suo valore di "non categoria".
            if element_name_key == 'categoria1':
                if actual_value_for_check != 'Senza Categoria':
                    element_valorized_counts[xml_element_name] += 1
            # l'else per tutti gli altri campi valorizzati        
            else: # Per tutti gli altri campi con un default 'Non disponibile' o simile
                if actual_value_for_check and actual_value_for_check != default_val:
                    element_valorized_counts[xml_element_name] += 1

        # LOGICA SPECIFICA PER IL CONTEGGIO DELL'URL DELL'
        # L'URL è considerato valorizzato se url O sito_web sono validi (non vuoti e non '#')
        url_val = event_data.get('url', '')
        sito_web_val = event_data.get('sito_web', '')

        # qui andiamo a vericicare se i valori di url e sito web strippati sono diversi
        # dai valori considerabili 'nulli' (come '#' o stringhe vuote)
        # allora aggiungiamo il conteggio all'element_valorized_counts['url']
        if (url_val and url_val.strip() != '#' and url_val.strip() != '') or \
           (sito_web_val and sito_web_val.strip() != '#' and sito_web_val.strip() != ''):
            element_valorized_counts['url'] += 1 
    

    sorted_categories = sorted(events_by_category_count.items(), key=lambda item: item[1], reverse=True) 
    top_5_categories = sorted_categories[:5]      

    sorted_zones_by_count = sorted(zone_event_counts.items(), key=lambda item: item[1], reverse=True)
    top_5_zones = sorted_zones_by_count[:5]

    ###################################################
    # SEZIONE REPORT GENERATO SU UNA NUOVA PAGINA HTML 
    ###################################################

    # tutto il blocco successivo si occupa della generazione della pagina HTML 
    # del report navigabile dall'utente, che contiene le statistiche informative e i dati raccolti dal file XML.
    report_page_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report e Statistiche Dettagliate - Progetto RASTA</title>
        <link rel="stylesheet" href="style.css"> 
    </head>
    <body>
        <div class="container">
            <h1>Report e Statistiche Dettagliate</h1>
            <p><a href="index.html"> <b><u>Clicca qui per tornare all'indice delle categorie</u></b></a></p>
            <p>Questa pagina di report fornisce un'analisi dei dati dal file madre XML.  
            L'obiettivo è offrire al lettore una panoramica dei dati estratti dall'XML.</p>
            
            <div class="general-stats">
                <h3>Statistiche Generali sugli Eventi:</h3>
    """
    
    report_page_content += f"<p><strong>Numero totale di eventi:</strong> {total_events_for_report}</p>\n"
    report_page_content += f"<p><strong>Numero di categorie uniche:</strong> {len(unique_categories)}</p>\n"
    report_page_content += f"<p><strong>Numero di zone di prossimità:</strong> {len(unique_zone_prossimita)}</p>\n"

    report_page_content += """
            <div class="statistics-section xml-overview">
                <h3>Panoramica della Struttura XML</h3>
                <p>Il file originale era un json convertito in XML. Ogni evento è racchiuso nel tag <code>&lt;evento&gt;</code> e contiene diversi elementi figli che racchiudono le informazioni.</p>
                <p>Di seguito viene riportato un esempio di elemento <code>&lt;evento&gt;</code> con i suoi elementi figli:</p>
                <pre class="xml-snippet"><code>"""
    report_page_content += xml_example_snippet.replace('<', '&lt;').replace('>', '&gt;')
    report_page_content += """</code></pre>
                <p>I campi principali che vengono estratti e analizzati sono:</p>
                <ul>
                    <li><code>&lt;titolo&gt;</code>: titolo dell'evento.</li>
                    <li><code>&lt;descrizione&gt;</code>: descrizione dell'evento.</li>
                    <li><code>&lt;url&gt;</code>: Link al sito web dell'evento.</li> 
                    <li><code>&lt;data-inizio&gt;</code> e <code>&lt;data-fine&gt;</code>: Date di inizio e fine dell'evento.</li>
                    <li><code>&lt;indirizzo&gt;</code>: indirizzo della location dell'evento.</li>
                    <li><code>&lt;zona-prossimita&gt;</code> e <code>&lt;area-statistica&gt;</code>: quartiere di riferimento.</li>
                    <li><code>&lt;categoria1&gt;</code>: Categoria di riferimento dell'evento (es. Musica, arte, mostre ecc.) .</li>
                </ul>
            </div>
    """

    report_page_content += """
            <div class="statistics-section">
                <h3>Le 5 categorie con più eventi:</h3>
                <ul class="stat-list">
    """
    if top_5_categories:
        for cat, count in top_5_categories:
            report_page_content += f"<li><b>{cat}</b> <span>({count} eventi)</span></li>\n"
    else:
        report_page_content += "<li>Nessuna categoria trovata.</li>\n"
    report_page_content += "</ul></div>\n"

    report_page_content += """
            <div class="statistics-section">
                <h3>I 5 quartieri con più eventi:</h3>
                <ul class="stat-list">
    """
    if top_5_zones:
        for zona, count in top_5_zones:
            report_page_content += f"<li><b>{zona}</b> <span>({count} eventi)</span></li>\n"
    else:
        report_page_content += "<li>Nessuna zona di prossimità trovata.</li>\n"
    report_page_content += "</ul></div>\n"

    report_page_content += """
            <div class="statistics-section">
                <h3>Completezza e Valorizzazione degli Elementi per Evento:</h3>
                <p>Questa sezione mostra la percentuale di eventi in relazione alla totalità degli eventi presenti nel file originale.</p>
    """
    report_page_content += "<div class=\"valorization-items\">\n"

    if total_events_for_report > 0:
        display_names = {
            'titolo': 'Titolo Evento', 'descrizione': 'Descrizione Dettagliata', 'url': 'Link Evento', 
            'indirizzo': 'Indirizzo Specifico', 'zona-prossimita': 'Zona di Prossimità',
            'area-statistica': 'Area Statistica', 'categoria1': 'Categoria Principale'
        }

        field_descriptions = {
            'titolo': {'desc': 'Il titolo è l\'elemento più visibile e serve a identificare immediatamente l\'evento.'},
            'descrizione': {'desc': 'Fornisce i dettagli completi dell\'evento, essenziale per informare gli utenti.'},
            'url': {'desc': 'Il link diretto alla pagina originale dell\'evento o al sito web dell\'organizzatore per maggiori dettagli.'}, # Descrizione aggiornata per riflettere l'unificazione
            'indirizzo': {'desc': 'L\'indirizzo completo del luogo dell\'evento, cruciale per la navigazione.'},
            'zona_prossimita': {'desc': 'Elemento utilizzato per la suddivisione in zone.'},
            'area_statistica': {'desc': 'Un campo aggiuntivo per raggruppamenti territoriali.'},
            'categoria1': {'desc': 'La macro-categoria principale a cui appartiene l\'evento, usata per la navigazione.'}
        }


        sorted_elements_for_report = sorted(report_elements_to_check)
        for element_name_key in sorted_elements_for_report:
            xml_element_name = element_name_key 
            
            if element_name_key == 'zona_prossimita': xml_element_name = 'zona-prossimita'
            elif element_name_key == 'area_statistica': xml_element_name = 'area-statistica'
            
            count = element_valorized_counts[xml_element_name]
            percentage = (count / total_events_for_report) * 100
            
            progress_bar_color = '#28a745' 
            if percentage < 50:
                progress_bar_color = '#dc3545'
            elif percentage < 90:
                progress_bar_color = '#ffc107'

            report_page_content += f"""
            <div class="progress-item">
                <span class="field-label">{display_names.get(xml_element_name, element_name_key)}: <strong>{count}/{total_events_for_report}</strong></span>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: {percentage:.2f}%; background-color: {progress_bar_color};"></div>
                </div>
                <span class="percentage-text">{percentage:.0f}%</span>
            </div>
            <div class="field-analysis">
                <h4>Analisi Campo "{display_names.get(xml_element_name, element_name_key)}" (<code class="tag-name">&lt;{xml_element_name}&gt;</code>)</h4>
                <p>{field_descriptions[element_name_key]['desc']}</p>
            </div>
            """
    else:
        report_page_content += "<p>Nessun dato disponibile per il report di valorizzazione.</p>\n"
        
    report_page_content += """
                </div> </div>
    """

    report_page_content += """
            <div class="statistics-section about-section">
                <h3>Informazioni sul Report e Metodologia</h3>
                <p>Questo sito web e le statistiche presentate sono generati automaticamente da uno script Python. L'obiettivo è trasformare dati XML grezzi sugli eventi in un'interfaccia web navigabile e fornire metriche sulla completezza e qualità del dataset.</p>
                <p>Lo script esegue il parsing del file <code>eventi_bologna.xml</code>, raggruppa gli eventi per macroarea e zona di prossimità, e genera pagine HTML statiche collegate tra loro. Il report di valorizzazione calcola la presenza di dati chiave in ciascun evento per fornire una panoramica sullo stato del dataset.</p>
            </div>
    """

    report_page_content += """
        </div>
    </body>
    </html>
    """
    
    # Scrivi il contenuto HTML generato nel file report.html
    report_filepath = os.path.join(output_root_dir, 'report.html')
    with open(report_filepath, 'w', encoding='utf-8') as f:
        f.write(report_page_content)
    print(f"Generato: {report_filepath}")

    ###################################################
    # FINE BLOCCO GENERAZIONE DELLA PAGINA DEL REPORT
    ###################################################

    # INFINE DEFINIAMO LA VAR index_html_filename CHE È QUELLA CHE GENERA 
    # LA PAGINA HTML PRINCIPALE CHE CONTIENE I LINK ALLE PAGINE DELLE CATEGORIE E AL REPORT.

    index_html_filename = os.path.join(output_root_dir, 'index.html')
    index_html_content = f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Indice Eventi per Categoria - Progetto RASTA</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="container">
            <h1> BOLOBOOM - Eventi a Bologna </h1>
           <h2> <span style="font-size: 0.35em; font-weight: normal; margin-right: 15em;"> 
                    <a href="../../file_download/eventi_bologna.json.zip" download class="button">Scarica file JSON</a>
                    <a href="../../file_download/eventi_bologna.xml.zip" download class="button">Scarica file XML</a>
                </span> </h2>
            <p style="font-size: 1.5em; font-weight: normal; margin-right: 10em;"> <b>CLICCA SULLA CATEGORIA DI INTERESSE PER VEDERE GLI EVENTI</b></p>
            <div class="category-grid">
    """
    #il ciclo for qui serve a generare i link alle pagine delle categorie ll'interno della pagina principale index.html

    for category in unique_categories:
        safe_category_name = category.lower().replace(' ', '-').replace('/', '-').replace('.', '').replace(',', '').replace(':', '').replace('(', '').replace(')', '')
        image_filename = category_images.get(safe_category_name, default_image)
        num_events = events_by_category_count.get(category, 0)
        display_name = nomi_a_video.get(safe_category_name, "Categoria non definita")

        index_html_content += f"""
                <a href="categorie/{safe_category_name}.html" class="category-card">
                    <img src="images/{image_filename}" alt="{category} icon">
                    <span>{display_name}</span>
                </a>
        """
    
    index_html_content += """
            </div> <a href="report.html" class="linea-report"> 
                <strong><u>Clicca qui per accedere alla pagina del report</u></strong> 
            </a>
        </div> </body>
    </html>
    """
    
    ##################################################################
    ############# FINE GENERAZIONE DELLA HOMEPAGE ##################

    # Scrivi il contenuto HTML generato nel file index.html
    # QUESTO È IL FULCRO DELLA GENERAZIONE VERA E PROPRIA DEI FILE

    with open(index_html_filename, 'w', encoding='utf-8') as f: # open è una funzione built-in di Python che apre un file. index_html_filename è il percorso del file HTML che stiamo creando.
                                                                # 'w' indica che vogliamo scrivere nel file.
        f.write(index_html_content)                             # f.write prende come argomento la stringa (nel nostro caso index_html_content) e lo scrive all'interno del file che abbiamo 'aperto'
    print(f"\nGenerato il file indice: {index_html_filename}")                          # semplici print di avviso per l'utente che il file HTML è stato generato correttamente.
    print("\nProcesso di generazione delle pagine HTML completato!")
    print(f"Puoi aprire '{index_html_filename}' nella cartella '{output_root_dir}' nel tuo browser per iniziare la navigazione.")

except FileNotFoundError:
    print(f"ERRORE: Il file XML '{xml_file_path}' non è stato trovato. Assicurati che il percorso sia corretto.")
except etree.XMLSyntaxError as e:
    print(f"ERRORE DI SINTASSI XML: Il file XML ha problemi di sintassi e non può essere parsificato. Dettagli: {e}")
except Exception as e:
    print(f"Si è verificato un errore imprevisto: {e}")


    # Generiamo prima le singole pagine html per le categorie perché per la homepage ci servono tutti i link
    # da richiamare nella homepage, poi scriviamo separatamente la pagina del report e infine
    # scriviamo la homepage che contiene tutti i ref delle pagine generate per le singole categorie
    # e per la pagina del report.