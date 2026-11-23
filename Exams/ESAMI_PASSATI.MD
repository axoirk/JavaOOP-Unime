## Dettagli e Regole Appelli
* **Ambiente:** pagina Moodle, area di scrittura di livello blocco note (nessun controllo di sintassi, nessun completamento). Tutte le classi di un esercizio in un **unico file**.
* **Tempo a disposizione:** 45 minuti totali per 3 esercizi, gestibili liberamente (si può passare da un esercizio all'altro).
* **Esecuzione:** pulsante *Esegui* che compila e confronta l'output con un test **non visibile**. L'output atteso è indicato nella traccia. Massimo 5 esecuzioni "pulite" per esercizio; oltre, penalità. Un errore di compilazione consuma un tentativo come un'esecuzione riuscita.
* **Punteggio Totale:** 31 punti (5 + 13 + 13).

## Scala di Valutazione e Struttura dell'Esame

L'esame è in due prove: **scritto**, che viene corretto, e **orale**, con domande su **tutto il programma**. Raggiunta la soglia minima allo scritto, **l'orale è obbligatorio** — non è un'opzione per alzare il voto.

| Voto scritto | Esito |
|---|---|
| < 16 | Non superato. Si ripete lo scritto |
| ≥ 16 e < 18 | **Riserva** — orale obbligatorio, serve a raggiungere almeno 18. Solo dopo si accetta o si rifiuta |
| ≥ 18 | **Passato** — orale obbligatorio comunque, ma il voto di partenza è già accettabile |

Conseguenza pratica: **un buon voto allo scritto non chiude l'esame, lo mette in sicurezza.** Con 18+ si affronta l'orale da una posizione di forza; con 16 l'orale è l'unica strada per passare. La preparazione teorica non è rinviabile a dopo lo scritto: tra correzione e orale può passare pochissimo tempo.

# 📝 TRACCIA ESAME 1

### Esercizio 1 (5 Punti) - OOP Base (Classi Astratte e Polimorfismo)
Creare una classe astratta `Animale` e definire un metodo astratto `String verso()`. Definire due sottoclassi `Cane` e `Gatto` che implementano il metodo e ritornano rispettivamente "bau" e "miao".

### Esercizio 2 (13 Punti) - Gestione Avanzata Eccezioni (Le 5 Keywords)
Definire un metodo che accetta un parametro `int` e gestire i seguenti casi:
* Se `0`: lanciare una `Exception` generica e stampare "eccezione generica".
* Se `1`: lanciare una `IOException`, catturarla, rilanciare una `RuntimeException` e stampare "eccezione runtime".
* Se `2`: stampare "no eccezioni".
* **Vincolo Architetturale:** Si devono obbligatoriamente utilizzare **tutte e 5 le parole chiave** della gestione delle eccezioni (`try`, `catch`, `finally`, `throw`, `throws`).

### Esercizio 3 (13 Punti) - Ereditarietà, Thread e Information Hiding
Data una classe `Persona` con costruttore `(String nome, String cognome)`:
1. Definire una sottoclasse `Studente` che implementa l'interfaccia `Runnable`.
2. Definire in `Studente` due costruttori in overload:
   * Il primo accetta: `nome`, `cognome`, `matricola` (int).
   * Il secondo accetta: `matricola` (int), `cds` (String). 
3. Fare l'override del metodo `run()`: dovrà elevare la `matricola` al quadrato e sovrascriverne il valore.
4. **Vincolo Architetturale:** Usare rigorosamente l'Information Hiding (tutte le variabili d'istanza devono essere `private` e bisogna definire i relativi metodi `get` e `set`).

---

### Analisi del Livello di Difficoltà
**Difficoltà Stimata:** Alta 🔴
* **Motivazione:** Non per la complessità logica (le operazioni richieste sono basilari), ma per la **pressione del tempo** (45 minuti per 3 esercizi, un quarto d'ora a esercizio) unita alla **penalità sul compilatore**. Richiede di scrivere codice a mente, pulito e sintatticamente corretto "alla prima stesura", padroneggiando a memoria i costrutti chiave (abstract, keyword eccezioni, ereditarietà con super(), e Runnable).

# 📝 TRACCIA ESAME 2

### Esercizio 1 (5 Punti) - Logica di Base
Implementare un metodo statico con la seguente firma: `public static int converti(int km)`. Il metodo deve ricevere in input un valore espresso in chilometri (km) e restituire il suo equivalente convertito in metri.

### Esercizio 2 (13 Punti) - Networking (Socket)
Definire una classe `Client`. Essendo noti a priori un indirizzo IP (es. "127.0.0.1") e un numero di porta, instaurare una connessione di rete verso il server in ascolto su tali coordinate e trasmettere al destinatario un messaggio testuale arbitrario. Non sono richiesti costrutti per la ricezione della risposta.

### Esercizio 3 (13 Punti) - Concorrenza e Sincronizzazione (Wait/Notify)
All'interno del workspace sono già fornite le classi `Produttore` e `Consumatore`, completamente implementate. Tali classi sono progettate per interagire concorrentemente con una risorsa condivisa.

Si richiede allo studente di implementare ex-novo la classe `Buffer` (attualmente vuota), col fine di risolvere il problema della concorrenza garantendo la mutua esclusione e la corretta sincronizzazione dei thread. La classe `Buffer` deve obbligatoriamente soddisfare i seguenti requisiti:
1. Contenere una struttura dati basata su un array primitivo con dimensione massima pari a 3.
2. Definire un metodo che restituisca sotto forma di intero il numero di elementi attualmente presenti nel buffer.
3. Definire un metodo per l'inserimento di un elemento nel buffer.
4. Definire un metodo per l'estrazione e rimozione di un elemento dal buffer.

*(Nota: Le firme esatte dei metodi per la classe `Buffer` devono essere dedotte dallo studente analizzando le invocazioni presenti nel codice fornito delle classi Produttore e Consumatore).*

---

# 📝 APPELLO SOSTENUTO — 8 luglio 2026

Primo appello effettivamente sostenuto in aula (il secondo è quello di settembre, sotto). **È la fonte più attendibile** su come il docente costruisce e corregge le tracce: le altre sono ricostruzioni. Voto rifiutato.

Tracce e tester eseguibili: `Exams/Appelli Ufficiali Unime/EXAM3/`.

### Esercizio 1 (5 Punti) — Interfacce
Implementare un'interfaccia elementare su una classe.

**Nessuna insidia particolare:** l'esercizio da 5 punti resta il più lineare dei tre.

### Esercizio 2 (13 Punti) — Le 5 Parole Chiave delle Eccezioni
Stessa struttura della traccia dell'Esame 1: gestire i casi previsti utilizzando obbligatoriamente tutte e cinque le parole chiave (`try`, `catch`, `finally`, `throw`, `throws`).

**Trappola:** un programma che compila e produce l'output corretto viene comunque penalizzato di 3-5 punti se le stampe **non stanno dentro il blocco `finally`** che la traccia impone. L'output giusto non dimostra niente sulla struttura, ed è la struttura a essere valutata.

### Esercizio 3 (13 Punti) — Serializzazione di Oggetti su Socket
Il **server era già fornito e attivo**, non andava scritto: la traccia dava host e porta.
1. Definire una classe `Persona` con alcune variabili d'istanza e una **costante di versione per la serializzazione** (`serialVersionUID`).
2. Realizzare una classe `Client` che si connette alle coordinate indicate e invia l'oggetto `Persona` **serializzato** sullo stream del socket.
3. Il server restituisce lo stesso oggetto, che va **deserializzato** lato client.

**Trappola:** costruire l'`ObjectOutputStream` su un `FileOutputStream` invece che su `socket.getOutputStream()`. La serializzazione è corretta in sé, ma la destinazione è un'altra: l'esercizio risolve un problema diverso da quello chiesto e viene sostanzialmente azzerato.

---

### Cosa insegna questo appello

1. **L'Esercizio 3 non è necessariamente su thread e concorrenza.** Qui era serializzazione + networking. Il terzo esercizio è "il difficile da 13 punti", non "quello sui thread".
2. **Il docente penalizza la struttura, non solo il risultato.** Vedi Esercizio 2: tutto funzionante, punti via lo stesso.
3. **Gli argomenti si presentano combinati.** Serializzazione *e* socket nello stesso esercizio: saperli separatamente non basta, serve saperli comporre.
4. **Il confine `FileOutputStream` / `socket.getOutputStream()` è il punto critico.** `ObjectOutputStream` avvolge indifferentemente entrambi: la sintassi è quasi identica, il significato no.


---

# 📝 APPELLO SOSTENUTO — 8 settembre 2026

Secondo appello effettivamente svolto. Tracce ricostruite a memoria subito dopo la prova:
struttura, vincoli e argomenti sono quelli reali, i dettagli operativi sono dichiarati come tali
nel README della cartella.

Tracce e tester eseguibili: `Exams/Appelli Ufficiali Unime/EXAM4/`.

### Esercizio 1 (13 Punti) — Classi Annidate e Information Hiding
1. Classe `Asta`, costruttore con `codiceAsta` (`String`), `quota` (`double`), `nomeMigliorOfferente` (`String`). Variabili d'istanza rigorosamente private.
2. Dentro `Asta`, una classe annidata **non statica** `Offerta`, costruttore con `nomeOfferente` (`String`) e `quotaOfferta` (`double`), variabili private.
3. Dentro `Offerta`, due metodi: `stato()` che restituisce `"prezzo asta attuale: " + quota + "euro. miglior offerente" + nomeMigliorOfferente`, e `aggiungiOfferta(double)` che restituisce `false` se l'importo è minore della quota attuale, altrimenti sovrascrive quota e miglior offerente dell'asta e restituisce `true`.
4. **Vincoli architetturali espliciti nella traccia:** la classe annidata non deve essere statica; dentro `Offerta` non va dichiarato nessun oggetto `Asta`.

**Trappola:** scrivere `class Offerta extends Asta` credendo che `extends` produca l'annidamento. Non compila: il costruttore di `Offerta` invoca implicitamente un `Asta()` senza argomenti che non esiste. Una inner class è una classe scritta dentro il corpo di un'altra, **senza `static`**, e nient'altro.

### Esercizio 2 (13 Punti) — Comunicazione di Rete su Protocollo UDP
Il server UDP era già attivo e non andava scritto; host e porta erano dati nella traccia.
1. Classe `ClientUDP`, costruttore con host e porta.
2. Metodo `inviaMessaggio(String)` che restituisce una `String`: apre una comunicazione UDP verso il server, invia il messaggio, **attende la risposta**, la riconverte da byte a testo e la restituisce.

**Due trappole.** `new InetAddress(host, porta)` non compila: `InetAddress` non ha costruttori pubblici (serve `InetAddress.getByName(host)`) e non contiene la porta, che si scrive sul `DatagramPacket`. E fermarsi dopo `send()`: su UDP la risposta è un secondo datagramma che va atteso con `receive()`, altrimenti metà del requisito non è affrontata.

### Esercizio 3 (5 Punti) — Logica di Base
Metodo statico che converte chilometri in metri. Stessa sostanza dell'Esercizio 1 dell'Esame 2.

**Trappola:** scrivere il metodo **fuori da qualsiasi classe**. In Java un metodo non può stare al primo livello di un file: `javac` si ferma con `class, interface, enum, or record expected` e l'esercizio non produce nulla, per quanto la logica sia corretta.

---

### Cosa insegna questo appello

1. **L'Esercizio grande non è né thread né serializzazione, necessariamente.** Qui erano classi annidate e UDP: due argomenti mai comparsi prima. Il bacino del docente è più largo del previsto — le classi annidate e UDP vanno in rotazione.
2. **UDP esiste.** Fino a qui la rete era sempre TCP (`Socket`/`ServerSocket`) con serializzazione. `DatagramSocket`, `DatagramPacket` e `InetAddress.getByName` sono un blocco da sapere a memoria: su UDP il destinatario si scrive sul pacchetto, non sul socket, e non c'è nessuno stream da cui leggere.
3. **Il primo Esegui va speso presto, anche sull'esercizio che sembra banale.** Gli errori più cari di questo appello sono tutti errori che il compilatore avrebbe mostrato al primo tentativo. Quindici esecuzioni disponibili in totale: non usarne nessuna è il modo più economico di perdere punti.
4. **La forma costa più della logica.** A luglio il mezzo sbagliato, a settembre la classe mancante e la keyword sbagliata: in entrambi i casi il ragionamento era corretto e i punti sono andati via lo stesso.


---

# 📝 APPELLO SOSTENUTO — 23 novembre 2026

Terzo appello effettivamente svolto, **superato con 30 e lode**. Tracce ricostruite a memoria
subito dopo la prova: argomenti, nomi e vincoli sono quelli reali, i dettagli operativi sono
dichiarati come tali nel README della cartella.

Tracce e tester eseguibili: `Exams/Appelli Ufficiali Unime/EXAM5/`.

### Esercizio 1 (5 Punti) — Classi Astratte e Polimorfismo
Classe astratta `Animale` con il metodo astratto `verso`; sottoclassi `Cane` e `Gatto` che lo
implementano restituendo `bau` e `miao`. È l'Esercizio 1 dell'Esame 1.

### Esercizio 2 (13 Punti) — Le 5 Parole Chiave delle Eccezioni
Classe `Automobile`, metodo `guida` con un parametro intero `n`:
* Se `0`: lancia un'eccezione controllata che il metodo non gestisce, la gestisce il chiamante. Messaggio `eccezione`.
* Se `1`: lancia una `IOException`, catturata dal `catch`, che a sua volta lancia una `RuntimeException`. Messaggio `eccezione in run time`.
* Se `2`: non fa nulla. Messaggio `nessuna eccezione`.
* Il messaggio di ogni caso va stampato in console, usando **tutte e cinque le parole chiave**.

Stessa struttura degli Esami 1 e 3, con nomi nuovi. Il caso `0` qui **esce** dal metodo, mentre
nell'Esame 3 il metodo lo catturava: è la parte da leggere con attenzione.

### Esercizio 3 (13 Punti) — Comunicazione di Rete su Protocollo UDP
Il `ClientUDP` dell'Esame 4, con le coordinate del server già date. Unica aggiunta: la conversione
tra testo e byte va fatta in `UTF-8` (`getBytes("UTF-8")` all'invio, `new String(dati, 0, lunghezza, "UTF-8")` alla ricezione).

---

### Cosa insegna questo appello

1. **Tutti e tre gli esercizi possono essere riciclati.** Luglio e settembre riprendevano un solo esercizio da un appello precedente; qui li riprendevano tutti e tre. Rifare gli appelli passati fino a scriverli senza esitazione è la preparazione che rende di più.
2. **Una traccia riciclata cambia nei dettagli.** Nomi delle classi, testo dei messaggi, il caso che esce dal metodo invece di essere catturato, la codifica dei byte: chi ricorda la vecchia soluzione invece di rileggere la traccia perde punti sull'aderenza letterale.
