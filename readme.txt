README dei file:


-  La cartella preprocessing contiene tutti i file che sono stati utilizzati per il preprocessing dei dati.

	- converti_eventi è lo scipt utilizzato per convertire il JSON in XML
	- valida_xml passa l'xml alla dtd per verificarne l'idoneità 
	- estrae_dati_xml è il primo script di analisi che analizza la valorizzazione degli elementi
	- estrae_categorie_eventi serve a valutare la quantità di aree tematiche per una successiva suddivisione
	- verifica_zona_prossimita serve a valutare se tutti gli elementi <zona-prossimita> sono valorizzati per la successiva suddivisione
	- correggi_zona_prossimita viene utilizzato per valorizzare gli elementi <zona-prossimita> vuoti inserendo il valore 'Quartiere sconosciuto'


- La cartella file_principali invece contiene:
	- dtd per la validazione
	- file json e xml
	- cartella indice dove vengono generate tutte le pagine html navigabili e le immagini utilizzate

 - La cartella genera_html contiene solamente il file:
	- genera_pagine_html che è il core del progetto. Il file che serve a generare automaticamente le pagine navigabili

- La cartella file_downlad contiene:
	- i file Json e XML zippati per il download automatico dalla homepage