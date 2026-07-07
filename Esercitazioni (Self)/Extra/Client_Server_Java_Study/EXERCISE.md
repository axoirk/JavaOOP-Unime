# Esercizi: Architettura Client-Server in Java

Questi esercizi sono progettati per aiutarti a fissare i concetti della comunicazione TCP, dell'I/O in rete e della gestione di un semplice protocollo applicativo. Svolgili in ordine sequenziale, in quanto la difficoltà è incrementale.

---

## Esercizio 1 (Base): Echo Server

**Obiettivo:** Testare la stabilità di una connessione base, l'invio e la ricezione di testo utilizzando i flussi I/O. Il Server dovrà funzionare come un "eco", rispedendo al mittente esattamente lo stesso testo che riceve.

**Requisiti del Server:**
1. Mettiti in ascolto su una porta specifica (es. 5000).
2. Attendi la connessione di un Client.
3. Quando il Client si connette, avvia un ciclo (es. `while(true)`) in cui leggi la stringa inviata dal Client.
4. Se la stringa è uguale a `"QUIT"`, interrompi il ciclo, chiudi la connessione e attendi un nuovo Client.
5. Altrimenti, invia indietro al Client la stringa prefissata con `"ECHO: "` (es. `"ECHO: ciao"`).

**Requisiti del Client:**
1. Connettiti al Server.
2. Tramite uno `Scanner` associato a `System.in`, chiedi all'utente di digitare una frase da tastiera.
3. Invia la stringa letta al Server.
4. Leggi la risposta del Server e stampala a schermo.
5. Continua finché l'utente non digita `"QUIT"`. A quel punto invia il comando al server e chiudi le risorse locali.

---

## Esercizio 2 (Intermedio): Calcolatrice Remota

**Obiettivo:** Gestire uno scambio dati più strutturato e validare l'input. Il Client delega un calcolo matematico al Server, che esegue l'operazione e restituisce il risultato.

**Requisiti del Server:**
1. Mettiti in ascolto su una porta (es. 6000) e accetta un Client.
2. Leggi una stringa in arrivo che rappresenta un'operazione matematica formattata (es. `5 + 3` oppure `10 / 2`).
3. Analizza (parse) la stringa separando i due operandi numerici e l'operatore matematico (`+`, `-`, `*`, `/`).
4. Esegui il calcolo. Presta attenzione alla gestione di eccezioni come la divisione per zero.
5. Invia al Client il risultato come stringa (o un messaggio di errore se l'operatore non è valido o se c'è un errore matematico).

**Requisiti del Client:**
1. Connettiti al Server.
2. Chiedi all'utente di inserire il primo numero, l'operatore, e il secondo numero.
3. Costruisci una singola stringa ben formattata e inviala al Server.
4. Rimani in attesa del risultato calcolato dal Server.
5. Stampa a schermo il risultato.

---

## Esercizio 3 (Avanzato): Gestione di un Mini-Protocollo (Autenticazione)

**Obiettivo:** Progettare un protocollo a strati in cui il Client deve rispettare una "macchina a stati" (autenticazione seguita da erogazione del servizio) ed eseguire operazioni logiche più complesse simulando la lettura di un file.

**Requisiti del Server:**
1. Definisci una password "segreta" fissa nel codice (es. `"SuperSecret"`).
2. Attendi un Client. La prima fase della comunicazione è **strettamente dedicata all'autenticazione**.
3. Aspettati che il Client invii una password.
4. Se la password è sbagliata, invia `"AUTH_FAILED"` e termina immediatamente la connessione con il Client.
5. Se la password è corretta, invia `"AUTH_SUCCESS"`. Da questo momento il Server entra nello stato "pronto per il servizio".
6. Attendi il nome di un file remoto (fittizio).
7. Se il nome del file richiesto è `"appunti.txt"`, invia indietro due o tre righe di testo simulate e poi `"EOF"` per indicare la fine del file. Altrimenti invia `"ERROR: File non trovato"`.

**Requisiti del Client:**
1. Connettiti al Server.
2. Prima di fare qualsiasi altra cosa, chiedi all'utente di digitare la password e inviala al Server.
3. Leggi la risposta del Server. Se è `"AUTH_FAILED"`, stampa a video "Accesso negato" e termina l'esecuzione.
4. Se è `"AUTH_SUCCESS"`, chiedi all'utente quale file desidera "scaricare" (o leggere) dal server e inviane il nome.
5. Leggi le righe inviate dal server in un ciclo. Stampa le righe a video fino a quando il server non ti invia `"EOF"` o `"ERROR: File non trovato"`. Chiudi la connessione al termine della lettura.

---

## Esercizio 4 (Extra): Datagrammi UDP - Sistema di Broadcast Simulato

**Obiettivo:** Staccarsi dal paradigma orientato alla connessione (TCP) per utilizzare `DatagramSocket` e `DatagramPacket`. Si richiede di creare un sistema molto semplice di invio messaggi unidirezionali ("fire and forget").

**Requisiti del Server (Ricevitore):**
1. Istanzia un `DatagramSocket` in ascolto su una porta specifica (es. `7070`).
2. Avvia un ciclo infinito.
3. Alloca un array di byte sufficientemente capiente (es. 1024 byte) e crea un `DatagramPacket` vuoto che faccia da "cestino" per la ricezione.
4. Mettiti in attesa invocando il metodo `receive()`.
5. Non appena ricevi un datagramma, estrapola la stringa e l'indirizzo IP del mittente, stampandoli a schermo.
6. Il ciclo ricomincia mettendosi immediatamente in attesa del pacchetto successivo.

**Requisiti del Client (Mittente):**
1. Istanzia un `DatagramSocket` vuoto (non serve specificare la porta locale, ci pensa il sistema operativo).
2. Chiedi all'utente di scrivere un "Messaggio Lampo" da terminale usando `Scanner`.
3. Converti il messaggio in un array di byte (es. `messaggio.getBytes()`).
4. Crea un `DatagramPacket` passando i byte, la lunghezza, l'indirizzo IP del Server (risolto tramite `InetAddress.getByName()`) e la porta di destinazione (es. `7070`).
5. Invia il pacchetto tramite `send()` e chiudi il client. Non devi aspettare alcuna risposta dal server.