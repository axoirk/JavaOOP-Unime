# Nuovo Syllabus: Percorso Java OOP in 7 Livelli

Di seguito la guida pratica e il percorso riordinato per l'esercitazione con Java, generato per coprire integralmente tutti gli argomenti del corso.

## Livello 1: Le Basi della Programmazione e Sintassi
*(Operatori, Parole chiave, Controllo del flusso, Packages, Array Primitivi)*

* **Operatori e Parole Chiave:** Usa gli operatori aritmetici di base per calcolare l'Indice di Massa Corporea (BMI) a partire da peso e altezza inseriti dall'utente.
* **Controllo del Flusso (if-else):** Espandi il calcolatore di BMI utilizzando blocchi `if`, `else if` ed `else` per stampare se l'utente è sottopeso, normale o sovrappeso.
* **Controllo del Flusso (switch):** Usa un costrutto `switch` basato su costanti o enumerazioni per stampare un messaggio diverso in base al voto (A, B, C, D, F) di uno studente.
* **I Cicli:** Usa un ciclo `while` per calcolare la media di voti inseriti, terminando l'esecuzione quando l'utente digita un numero negativo (valore sentinella).
* **I Packages:** Crea due classi in due file separati. Inserisci la prima in un package specifico usando la direttiva `package` all'inizio del file, e importala nella seconda classe usando `import`.
* **Array Primitivi (Essenziali):** Crea un array di interi di dimensione fissa, riempilo con dei valori e usa un ciclo `for` per stamparne il contenuto e calcolarne la somma.

---

## Livello 2: Fondamenti OOP (Programmazione Orientata agli Oggetti)
*(Paradigmi, Classe/Oggetto, Variabili/Metodi, Costruttori, Information Hiding, Costanti, Classi Statiche, Collezioni Dinamiche)*

* **Classe vs Oggetto:** Definisci una classe `Automobile` con variabili d'istanza per velocità e carburante, poi istanzia due oggetti separati nel main e modificali indipendentemente.
* **I Costruttori e Overloading:** Crea una classe `Pet` con più costruttori: uno di default, uno che accetta solo il nome e uno che accetta nome ed età. Dimostra come Java li distingue tramite l'overloading.
* **Information Hiding (public, private, protected):** Rendi `private` le variabili d'istanza della tua classe e scrivi metodi `public` (getter e setter) per accedervi in modo controllato.
* **Variabili di Classe (Static) e Costanti:** Aggiungi a una classe una variabile `static` per contare quanti oggetti di quella classe sono stati creati, e usa `static final` per definire una costante inalterabile.
* **Inner Classes (Classi Interne):** Crea una classe `StringLinkedList` che contenga al suo interno una classe privata `ListNode`. Dimostra come la classe esterna possa usare i nodi nascondendoli all'esterno per evitare "privacy leak".
* **Collezioni Dinamiche (ArrayList):** Utilizza `ArrayList` per gestire una lista di stringhe che può crescere dinamicamente, esplorando i metodi `add()`, `remove()` e `size()`.

---

## Livello 3: OOP Avanzata e Gestione degli Errori
*(Ereditarietà, Polimorfismo, Binding Dinamico, Classi Astratte vs Interfacce, Eccezioni)*

* **Ereditarietà e Overriding:** Definisci una classe base `Person` e una sottoclasse `Student` (usando `extends`). Sovrascrivi un metodo di stampa in `Student` richiamando `super`.
* **Classi Astratte e Binding Dinamico:** Crea una classe `ShapeBase` dichiarata `abstract` con un metodo `drawHere()`. Implementalo diversamente in `Rectangle` e `Triangle` e testalo iterando su un array polimorfico.
* **Le Interfacce:** Dichiara un'interfaccia `Measurable` con metodi senza corpo. Falla implementare a due classi diverse per capire la differenza architetturale rispetto a una classe astratta.
* **Estensione di Interfacce:** Implementa l'interfaccia di sistema `Comparable` in una tua classe sovrascrivendo il metodo `compareTo()`, per imporre un ordinamento personalizzato a un array di oggetti.
* **Le Eccezioni:** Crea un calcolatore che può generare una divisione per zero. Usa i blocchi `try`, `catch` e `finally`, definendo e lanciando (`throw`) una tua `DivideByZeroException`.

---

## Livello 4: Dati, Input/Output e Interfacce Grafiche (GUI)
*(I/O, File, Reader/Writer, Serializable, Interfacce Grafiche)*

* **Scrittura File e I/O:** Usa la classe `PrintWriter` per catturare l'input dell'utente dalla console e scriverlo permanentemente in un file di testo `.txt`.
* **Lettura File (Reader):** Usa la classe `File` e `Scanner` per rileggere riga per riga il file creato nell'esercizio precedente e stamparlo a schermo.
* **Interfacce Grafiche (Swing):** Abbandona la console e crea una finestra usando `JFrame`. Aggiungi testo con `JLabel` e un pulsante `JButton`.
* **Layout e Action Listener:** Costruisci una mini-calcolatrice grafica con `JTextField`. Implementa un `ActionListener` per calcolare la somma quando si clicca il pulsante, gestendo la `NumberFormatException`.
* **Interfaccia Serializable:** Fai implementare `Serializable` alla tua classe base. Scrivi l'intero oggetto su un file binario usando `ObjectOutputStream` e poi rileggilo con `ObjectInputStream`.

---

## Livello 5: La Java Virtual Machine e la Concorrenza
*(Thread, Programmazione concorrente, Interfaccia Runnable, Sincronizzazione, Comunicazione tra thread)*

* **Creazione Thread:** Implementa l'interfaccia `Runnable` in due classi diverse (es. `Coffee` e `Tea`). Passale ai costruttori di due oggetti `Thread` e avviali in parallelo usando `start()`.
* **Identificazione e Ciclo di Vita:** Assegna un nome ai thread e stampalo nel blocco di esecuzione usando `getName()`. Implementa una logica basata su variabile sentinella per terminare il metodo `run()` in modo pulito.
* **Coordinamento (join, sleep, yield):** Fai in modo che il main attenda la fine dei thread figli invocando su di essi il metodo `join()`, inserendo anche dei ritardi simulati con `sleep()`.
* **La Sincronizzazione:** Simula due thread che provano ad accedere a un contatore condiviso (Race Condition). Usa la parola chiave `synchronized` sul metodo per garantire la Mutua Esclusione.
* **Comunicazione tra Thread:** Crea uno stack condiviso. Un thread "Produttore" inserisce dati, un "Consumatore" li estrae. Usa i metodi `wait()` e `notify()` della JVM per coordinarli senza sprecare risorse.

---

## Livello 6: Java in Rete e Manipolazione XML
*(Java Networking, Client/Server Socket, Datagram, XML SAX/DOM)*

* **Java & Networking:** Usa la classe `URL` per connetterti a una pagina web esistente (es. wikipedia) e usa uno `Scanner` per scaricare e stampare il codice HTML grezzo in console.
* **Client/Server (Socket TCP):** Crea un programma Server che resta in ascolto su una porta specifica. Crea un programma Client che si connette e invia un messaggio usando la comunicazione orientata alla connessione.
* **Client/Server (Datagram UDP):** Riscrivi l'esercizio precedente usando i Datagram Socket per inviare pacchetti senza garantire l'ordine di arrivo (Connectionless).
* **Java e XML (DOM):** Crea un file XML con una lista di studenti. Usa `DocumentBuilder` per caricarne l'albero in memoria (Object Model) e itera sui nodi per stamparli.
* **Java e XML (SAX):** Usa un parser a eventi (`SAXParserFactory` e `DefaultHandler`) per leggere lo stesso file XML senza caricarlo tutto in memoria, catturando i metodi `startElement` ed `endElement`.

---

## Livello 7: Ecosistema Enterprise e Build Tools
*(JDBC, NoSQL, Maven, REST/Spring)*

* **Creazione Progetto con Maven:** Usa il comando `mvn archetype:generate` da terminale per generare la struttura standard di un progetto Java con il file `pom.xml`.
* **Gestione Dipendenze e JDBC:** Inserisci nel `pom.xml` le dipendenze per connetterti a un database relazionale usando JDBC (es. driver MySQL o HSQLDB) e testa la connessione.
* **Integrazione NoSQL (MongoDB):** Sostituisci il database relazionale aggiungendo al POM la dipendenza `mongo-java-driver`. Scrivi un file nel DB documentale.
* **Architettura REST (Spring MVC):** Aggiungi le dipendenze di Spring MVC al progetto Maven. Definisci un controller base che risponda a una richiesta HTTP (simulando un'architettura web).
* **Build Automatica:** Completa il ciclo di vita eseguendo `mvn clean install` o `mvn package` per impacchettare l'intera applicazione e le sue dipendenze in un file JAR o WAR distribuibile.