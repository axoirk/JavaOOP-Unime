# 🎓 Q&A: Preparazione Esame Orale - Java OOP

Questo documento contiene una raccolta completa di domande e risposte (strutturate per livelli del Syllabus) per prepararti ad affrontare il colloquio orale del professore.

---

## Livello 1: Le Basi della Programmazione

**Q1: Qual è la differenza tra tipi primitivi e tipi reference in Java?**
* **Risposta:** I tipi primitivi (es. `int`, `double`, `boolean`, `char`) memorizzano direttamente il loro valore in memoria (nello stack) e non hanno metodi associati. I tipi reference (es. oggetti di classi, array, `String`) memorizzano nello stack l'indirizzo di memoria (il riferimento) che punta all'oggetto reale, il quale risiede nell'area di memoria chiamata Heap.

**Q2: Qual è la differenza tra un blocco `switch` e una catena di `if-else`?**
* **Risposta:** Il costrutto `switch` valuta una singola espressione e salta direttamente al `case` corrispondente, rendendolo spesso più leggibile e leggermente più performante per menu a scelta multipla. Una catena `if-else` valuta espressioni booleane sequenzialmente e permette controlli più complessi (es. range di valori: `x > 10 && x < 20`), cosa che lo `switch` classico non permette. Da Java 7, lo `switch` supporta anche le stringhe.

**Q3: Perché si usano i `package` e a cosa serve la direttiva `import`?**
* **Risposta:** I `package` servono a organizzare logicamente le classi (come delle cartelle nel filesystem), evitando conflitti di nomi (name-clashing) e fornendo un livello di protezione degli accessi. L'`import` permette di utilizzare classi definite in altri package senza dover scriverne ogni volta il percorso completo (Fully Qualified Name).

**Q4: Qual è la differenza tra un array primitivo (es. `int[]`) e un `ArrayList`?**
* **Risposta:** Un array primitivo ha dimensione fissa, decisa al momento della creazione, e può contenere sia tipi primitivi che oggetti. `ArrayList` è una classe della libreria dinamica (Collections) che gestisce un array sottostante in grado di crescere e restringersi automaticamente; tuttavia, `ArrayList` può contenere solo oggetti (quindi richiede i Wrapper type come `Integer` per inserire interi).

---

## Livello 2: Fondamenti OOP

**Q5: Qual è la differenza tra una Classe e un Oggetto (Istanza)?**
* **Risposta:** La Classe è un modello, un "progetto" o un "template" che definisce la struttura (variabili d'istanza) e il comportamento (metodi) di un'entità. Un Oggetto è la realizzazione concreta (l'istanza) di quella classe in memoria, creata tramite la parola chiave `new`.

**Q6: Cos'è il principio di Information Hiding (Incapsulamento) e come si realizza in Java?**
* **Risposta:** L'Information Hiding consiste nel nascondere i dettagli implementativi interni di una classe, proteggendone lo stato da modifiche dirette e incontrollate dall'esterno. In Java si realizza dichiarando `private` le variabili di istanza e fornendo accesso ad esse solo tramite metodi pubblici (i cosiddetti Getter e Setter).

**Q7: Qual è la differenza tra Overloading (Sovraccarico) e Overriding (Sovrascrittura)?**
* **Risposta:** 
  - L'**Overloading** avviene nella stessa classe (o ereditata) quando si dichiarano metodi con lo stesso nome ma *firma diversa* (numero, tipo o ordine dei parametri). La risoluzione avviene a tempo di compilazione (Compile-time).
  - L'**Overriding** avviene in una sottoclasse quando si ridefinisce un metodo ereditato dalla superclasse mantenendo l'*identica firma*. La risoluzione avviene a tempo di esecuzione (Runtime / Binding Dinamico).

**Q8: Quali sono i tipi di scope (visibilità) delle variabili in Java (Istanza, Classe, Parametri, Locali)?**
* **Risposta:** 
  - **Variabili di Istanza:** Dichiarate nella classe (senza `static`). Ne esiste una copia per ogni oggetto creato; lo scope è legato al ciclo di vita dell'oggetto.
  - **Variabili di Classe (`static`):** Condivise tra tutte le istanze della classe. Sopravvivono per tutta la durata dell'esecuzione del programma.
  - **Parametri:** Variabili passate alla firma di un metodo. Lo scope è strettamente limitato all'esecuzione del metodo stesso.
  - **Variabili Locali:** Dichiarate all'interno di un blocco di codice (es. un metodo, un costrutto `if` o `for`). Lo scope inizia dalla dichiarazione e termina alla chiusura della parentesi graffa `}` corrispondente. A differenza delle variabili d'istanza, non hanno valori di default e vanno inizializzate manualmente.

**Q9: A cosa serve la keyword `final`?**
* **Risposta:** 
  - Su una **variabile**: la rende una costante, il suo valore non può più essere modificato dopo l'inizializzazione.
  - Su un **metodo**: impedisce che venga sovrascritto (override) dalle sottoclassi.
  - Su una **classe**: impedisce che la classe possa essere estesa (nessuna classe potrà ereditare da essa, es. la classe `String`).

---

## Livello 3: OOP Avanzata e Gestione degli Errori

**Q10: Cos'è l'ereditarietà? Java supporta l'ereditarietà multipla?**
* **Risposta:** L'ereditarietà (realizzata tramite `extends`) permette a una nuova classe (Sottoclasse) di acquisire attributi e metodi di una classe esistente (Superclasse), favorendo il riuso del codice e le relazioni gerarchiche "IS-A" (è-un). Java **non** supporta l'ereditarietà multipla di classi (non si può estendere più di una classe), ma permette di implementare interfacce multiple.

**Q11: Cos'è il Polimorfismo e cos'è il Binding Dinamico?**
* **Risposta:** Il polimorfismo è la capacità di un oggetto di assumere più forme; in pratica, una variabile di tipo Superclasse può riferirsi a un oggetto di una qualsiasi Sottoclasse. 
Il Binding Dinamico (Late Binding) avviene quando viene richiamato un metodo in polimorfismo: la JVM decide a tempo di esecuzione (runtime) quale versione del metodo eseguire (quella della superclasse o quella sovrascritta della sottoclasse), basandosi sul tipo effettivo dell'oggetto in memoria, non sul tipo della variabile.

**Q12: Differenza tra Classe Astratta e Interfaccia? Quando useresti l'una o l'altra?**
* **Risposta:** 
  - Una **Classe Astratta** (`abstract class`) può avere metodi con o senza corpo, può contenere variabili di stato e costruttori. Si usa quando c'è una forte relazione "IS-A" tra oggetti che condividono molta logica comune di base.
  - Un'**Interfaccia** (`interface`) è un contratto: tradizionalmente dichiara solo metodi astratti (senza corpo) e costanti. Si usa per stabilire le "abilità" che classi completamente non imparentate devono possedere (es. `Serializable`, `Runnable`).

**Q13: Qual è la differenza tra eccezioni Checked e Unchecked?**
* **Risposta:** 
  - **Checked Exceptions** (estendono `Exception`): Il compilatore obbliga a gestirle (con un blocco `try-catch` o dichiarandole nel `throws` della firma del metodo). Rappresentano errori recuperabili al di fuori del controllo del programmatore (es. file non trovato, errore di rete).
  - **Unchecked Exceptions** (estendono `RuntimeException`): Il compilatore non obbliga a gestirle. Solitamente indicano errori logici nel codice che il programmatore dovrebbe risolvere a monte (es. `NullPointerException`, divisione per zero).

**Q14: A cosa serve il blocco `finally`?**
* **Risposta:** Viene eseguito sempre, sia che si verifichi un'eccezione nel `try`, sia che tutto vada a buon fine. È storicamente utilizzato per rilasciare in modo sicuro le risorse acquisite (chiudere stream di file, chiudere connessioni al database), anche se oggi si preferisce il `try-with-resources`.

**Q14b (Extra): Qual è il comportamento delle Eccezioni nell'Overloading e nell'Overriding?**
* **Risposta:**
  - **Nell'Overloading:** Non c'è alcuna restrizione. I metodi in overload sono considerati metodi completamente diversi e possono lanciare qualsiasi tipo di eccezione.
  - **Nell'Overriding:** Ci sono regole rigorose per le *Checked Exceptions*. Il metodo sovrascritto nella sottoclasse **NON** può dichiarare eccezioni checked "nuove" o "più generiche" rispetto a quelle del metodo della superclasse (può lanciarne di più specifiche o non lanciarne affatto). Per le *Unchecked Exceptions* (`RuntimeException`), invece, non esiste alcuna restrizione.

---

## Livello 4: Dati, I/O e GUI

**Q15: Differenza tra Stream di Byte e Stream di Caratteri?**
* **Risposta:** Le classi basate su stream di byte (es. `InputStream`, `OutputStream`, `FileInputStream`) leggono/scrivono dati binari (1 byte alla volta) e sono adatte per immagini, video o file eseguibili. Le classi basate su caratteri (es. `Reader`, `Writer`, `FileReader`) lavorano con i caratteri (solitamente 16 bit, usando codifiche come UTF-8) e sono usate per file di testo.

**Q16: Cos'è la Serializzazione e a cosa serve la keyword `transient`?**
* **Risposta:** La Serializzazione (interfaccia marker `Serializable`) è il processo di conversione dello stato di un oggetto in memoria in un flusso di byte, permettendone il salvataggio su file o l'invio su rete (e viceversa, Deserializzazione). 
La parola chiave `transient` applicata a un attributo dice alla JVM di ignorare quella variabile durante la serializzazione (il dato non verrà salvato).

**Q17: Come si gestiscono gli eventi nei bottoni in Swing?**
* **Risposta:** Tramite il pattern Observer. Si implementa l'interfaccia `ActionListener`, che obbliga a definire il metodo `actionPerformed(ActionEvent e)`. L'ascoltatore viene poi registrato sul bottone tramite `button.addActionListener(...)`. Quando il bottone viene premuto, la JVM notifica l'ascoltatore richiamando il metodo.

---

## Livello 5: La Java Virtual Machine e la Concorrenza

**Q18: Quali sono i due modi principali per creare un Thread in Java?**
* **Risposta:** 
  1. Estendere la classe `Thread` e sovrascriverne il metodo `run()`.
  2. Implementare l'interfaccia `Runnable` (metodo `run()`) e passare l'istanza al costruttore di un oggetto `Thread`. (Questo è il metodo preferito perché aggira il limite dell'ereditarietà singola).

**Q19: A cosa serve la parola chiave `synchronized`? Quale problema risolve?**
* **Risposta:** Serve a prevenire problemi di accesso concorrente a dati condivisi (Race Conditions), forzando la "Mutua Esclusione". Se un metodo o un blocco è `synchronized`, solo un thread alla volta può eseguirlo sull'oggetto ricevente (gli altri thread verranno messi in attesa finché il primo non rilascia il "lock" del monitor).

**Q20: Che differenza c'è tra chiamare `Thread.sleep()` e `wait()`?**
* **Risposta:** 
  - `sleep(millis)`: Mette in pausa temporanea il Thread senza rilasciare eventuali "lock" (chiavi di accesso) che il thread possiede.
  - `wait()`: Fa parte della comunicazione tra thread in aree sincronizzate. Mette il thread in attesa indefinita finché qualcuno non invoca `notify()`, **e rilascia il lock** per permettere agli altri di accedere alla risorsa.

**Q21: A cosa serve il metodo `join()` invocato su un Thread?**
* **Risposta:** Ordina al thread chiamante (ad esempio il Main Thread) di mettersi in attesa finché il thread su cui è stato invocato il `join()` non termina la propria esecuzione. Serve per sincronizzare il flusso e far sì che il chiamante proceda solo dopo che i figli hanno finito.

---

## Livello 6: Java in Rete e Manipolazione XML

**Q22: Qual è la differenza tra i protocolli TCP (Socket) e UDP (Datagram)?**
* **Risposta:** 
  - **TCP:** Orientato alla connessione (Connection-oriented). È affidabile: garantisce che i pacchetti arrivino tutti, intatti e nell'ordine giusto. Usa stream di dati (adatto per Web, Chat, trasferimenti file).
  - **UDP:** Senza connessione (Connectionless). È inaffidabile ma molto veloce. I pacchetti possono arrivare disordinati o andare persi (adatto per Streaming video, VoIP, giochi online veloci).

**Q22b (Extra): Come si connettono un Server e un Client in Java usando TCP e UDP? Quali classi e metodi si utilizzano?**
* **Risposta:**
  - **Per il TCP (Orientato alla connessione):**
    - Il **Server** utilizza la classe `ServerSocket(porta)` e si mette in ascolto invocando il metodo bloccante `accept()`. Questo metodo aspetta finché qualcuno non si connette, restituendo poi un oggetto `Socket`.
    - Il **Client** utilizza la classe `Socket(ip, porta)` per stabilire la connessione col server.
    - *Scambio dati:* Ottenuta la connessione, entrambi estraggono i canali di I/O dall'oggetto `Socket` tramite i metodi `getInputStream()` e `getOutputStream()` (spesso incapsulati in `Scanner` e `PrintWriter`).
  - **Per l'UDP (Senza connessione):**
    - Non esiste una distinzione netta di connessione: sia Client che Server aprono semplicemente un "nodo" usando la classe `DatagramSocket`. Non esiste alcun metodo `accept()`.
    - *Scambio dati:* Le informazioni viaggiano chiuse dentro "buste" chiamate `DatagramPacket` (che contengono array di byte, indirizzo IP e porta del destinatario). Si spedisce chiamando `socket.send(packet)` e si riceve chiamando `socket.receive(packet)`.

**Q23: Nel parsing XML, qual è la differenza fondamentale tra DOM e SAX?**
* **Risposta:** 
  - **DOM (Document Object Model):** Legge l'intero file XML e crea una struttura ad albero completa nella memoria RAM. Ottimo per fare ricerche, leggere e modificare, ma molto pesante in memoria per file grossi.
  - **SAX (Simple API for XML):** È un parser "a eventi". Legge il file riga per riga e lancia eventi (es. `startElement`, `endElement`) che lo sviluppatore cattura. Non salva nulla in memoria: ottimo per file giganteschi, ma permette sola lettura (non modifiche strutturali) ed è più complesso da scrivere.

---

## Livello 7: Ecosistema Enterprise e Build Tools

**Q24: A cosa serve Maven e qual è il ruolo del file `pom.xml`?**
* **Risposta:** Maven è un Build Automation Tool. Serve a standardizzare la struttura del progetto, automatizzare la compilazione/il packaging (es. creare un file JAR o WAR) e, soprattutto, a gestire automaticamente le dipendenze esterne. Il `pom.xml` è il file di configurazione centrale (Project Object Model) in cui dichiariamo la versione di Java, i metadati e le librerie da scaricare dal repository centrale.

**Q25: Cos'è JDBC? Quali sono i passaggi base per interrogare un database?**
* **Risposta:** JDBC (Java Database Connectivity) è l'API standard per comunicare con database relazionali. I passaggi sono: 
  1. Registrare il Driver (oggi automatico dal JAR).
  2. Stabilire la connessione tramite `DriverManager.getConnection()`.
  3. Creare uno `Statement` o `PreparedStatement`.
  4. Eseguire la query (`executeQuery()`).
  5. Scorrere i risultati col `ResultSet` (`rs.next()`).
  6. Chiudere la connessione.

**Q26: Perché si usa `PreparedStatement` al posto di `Statement` normale?**
* **Risposta:** Perché `PreparedStatement` accetta parametri (tramite il simbolo `?`) ed esegue l'escaping sicuro dei caratteri, bloccando in partenza qualsiasi tentativo di "SQL Injection" (attacco dove stringhe maligne vengono inserite al posto di input per hackerare la query). Inoltre, le query preparate sono più veloci se ripetute perché pre-compilate dal database.

**Q27: In ambito web e Spring Boot, qual è il ruolo di `@RestController`?**
* **Risposta:** In Spring, `@RestController` indica che la classe gestirà chiamate HTTP e che il valore ritornato dai metodi verrà serializzato direttamente nel corpo della risposta web (tipicamente trasformato automaticamente in formato JSON), essenziale per costruire architetture e API di tipo REST.
