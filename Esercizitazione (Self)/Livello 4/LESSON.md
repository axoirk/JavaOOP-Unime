# Livello 4: Argomenti Avanzati

## 1. File I/O e Serializzazione

### Teoria Fondamentale
In Java, l'I/O su disco prevede l'uso di stream. `PrintWriter` si occupa di riversare dati testuali su file fisici ottimizzandone l'output tramite buffer interni. 

La **Serializzazione** è un meccanismo binario. Consente di catturare l'intero "stato" (valori delle variabili) di un Oggetto in memoria Heap e congelarlo in un flusso binario, tipicamente per il salvataggio su un file non leggibile in testo chiaro. 

> **Nota del Docente (Interfacce Segnaposto):**
> L'interfaccia `Serializable` è un'interfaccia vuota (Marker Interface). Non ha metodi. La sua unica utilità è apporre un "timbro" visibile alla JVM (Reflection), indicandole esplicitamente: *"Ho il permesso dell'autore di permettere la serializzazione per questa classe"*.

### Sintassi ed Esempi di Codice
```java
import java.io.*;

// Classe che autorizza la serializzazione
public class Videogioco implements Serializable {
    private String titolo;
    // La keyword 'transient' impedisce alla variabile di essere serializzata (ottima per password)
    private transient int identificatoreSegreto; 
    
    public Videogioco(String titolo) { this.titolo = titolo; }
    public String getTitolo() { return titolo; }
}

public class GestoreIO {
    public static void main(String[] args) {
        // SALVATAGGIO TESTUALE
        try (PrintWriter writer = new PrintWriter(new File("testo.txt"))) {
            // Il costrutto try-with-resources chiude automaticamente il buffer! Nessun Memory Leak.
            writer.println("Salvataggio di un dato testuale.");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        // SERIALIZZAZIONE BINARIA (ObjectOutputStream)
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("save.dat"))) {
            Videogioco game = new Videogioco("Zelda");
            oos.writeObject(game); // Congela l'oggetto su disco
            System.out.println("Oggetto salvato.");
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        // DESERIALIZZAZIONE BINARIA (ObjectInputStream)
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("save.dat"))) {
            // È obbligatorio il Casting Esplicito: il readObject torna un Object generico.
            Videogioco gameRicaricato = (Videogioco) ois.readObject();
            System.out.println("Caricato: " + gameRicaricato.getTitolo());
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Try-with-Resources:** Usare sempre la sintassi `try(Risorsa r = new Risorsa()) { }` introdotta in Java 7 per gestire i file. Chiama automaticamente il metodo `.close()` e azzera la possibilità di buffer intasati e Memory Leaks, che accadono spessissimo quando si lasciano PrintWriter "appesi".
- **SerialVersionUID mancante:** Modificare i campi di una classe dopo averla serializzata porta a eccezioni (`InvalidClassException`) in fase di lettura. Questo avviene perché Java calcola un ID di versione nascosto. È sempre buona prassi inserire il `private static final long serialVersionUID = 1L;` fisso nella classe!

---

## 2. Multithreading e Sincronizzazione

### Teoria Fondamentale: Processi vs Thread
Un **Processo (Task)** è un programma in esecuzione. Ogni processo possiede uno **spazio di memoria privato** e non può accedere a quello di altri processi (salvo meccanismi complessi di memoria condivisa). Il cambio di contesto (Context Switch) tra processi è oneroso perché coinvolge il salvataggio di registri, stack e memoria.

Un **Thread** è un "sotto-processo" leggero. La differenza fondamentale è che i thread di uno stesso processo **condividono lo stesso spazio di memoria (Heap)**, pur avendo ciascuno il proprio Stack privato per le variabili locali.
Vantaggi del Multithreading:
- Cambio di contesto molto più rapido e leggero rispetto ai processi.
- Facile condivisione dei dati e comunicazione inter-thread.
- Esecuzione realmente (o pseudo) parallela di operazioni concorrenti.

### Creazione di un Thread: `Runnable` vs `Thread`
In Java ci sono due metodi principali per creare un thread:
1. **Estendere la classe `java.lang.Thread`**: Si crea una sottoclasse e si esegue l'override del metodo `run()`. **Svantaggio Accademico**: In Java c'è l'ereditarietà singola. Se estendi `Thread`, precludi alla tua classe la possibilità di estendere qualsiasi altra classe.
2. **Implementare l'interfaccia `Runnable`**: Si crea una classe che implementa il metodo `run()`, poi la si passa come parametro al costruttore di un nuovo `Thread` (es. `new Thread(mioRunnable).start()`). **Vantaggio**: È il metodo caldamente consigliato dall'ingegneria del software. Permette alla tua classe di ereditare liberamente da altre classi padre e separa nettamente la logica del "Task" da quella del "Motore" (il Thread).

### Gli Stati (Ciclo di Vita) di un Thread
1. **New (Initial)**: Istanza creata con `new Thread()`, ma non è ancora stato invocato il metodo `start()`.
2. **Runnable**: Dopo aver chiamato `start()`. Il thread è pronto e in attesa che lo Scheduler gli assegni il processore (spesso basato su priorità e meccanismi *Round-Robin/Preemptive*).
3. **Running**: Il thread sta attualmente eseguendo il suo metodo `run()` occupando la CPU.
4. **Blocked / Waiting / Sleeping**: Il thread è sospeso in attesa di un evento (I/O, rilascio di un lock di mutua esclusione, fine del timer di `sleep`, o una chiamata a `wait()`).
5. **Dead (Terminated)**: Il metodo `run()` è giunto al termine naturalmente (o per un'eccezione non gestita). Le risorse vengono rilasciate.

### Il Controllo dei Thread: Metodi Fondamentali
La classe `Thread` fornisce metodi essenziali per controllare il flusso:
- **`start()`**: Lancia il thread, rendendolo schedulabile. Chiama internamente il `run()`. 
- **`sleep(long millis)`** (Statico): Sospende l'esecuzione del thread corrente per un tempo prefissato. *Trick Accademico*: Non rilascia MAI gli eventuali lock acquisiti, rendendolo molto pericoloso se usato male in blocchi sincronizzati.
- **`yield()`** (Statico): Cede volontariamente e amichevolmente l'uso del processore ad altri thread in attesa con priorità uguale o superiore. Passa da *Running* a *Runnable*.
- **`join()`**: Forza il thread *chiamante* a mettersi in attesa e bloccarsi finché il thread *su cui è stato invocato* `join()` non termina. Vitale per raccogliere i risultati di elaborazioni parallele. È possibile specificare un timeout: `join(long millis)`.
- **`setPriority()` / `getPriority()`**: Modifica/legge la priorità (da `MIN_PRIORITY` a `MAX_PRIORITY`) suggerendo allo scheduler l'importanza del thread.
- **`isAlive()`**: Ritorna `true` se il thread è stato avviato e non è ancora morto.

### Sincronizzazione, Race Condition e Mutua Esclusione
Condividendo la stessa memoria (Heap), più thread possono leggere e scrivere la stessa variabile simultaneamente. Se l'operazione non è *atomica* (es. l'incremento `i = i + 1` prevede 3 passi: lettura, somma, scrittura), si verifica una gravissima **Race Condition (Competizione)** causando corruzione dei dati.

Per garantire la **Mutua Esclusione**, Java usa i *Lock* (Monitor). Si ottiene tramite il modificatore **`synchronized`** (applicabile a metodi o interi blocchi di codice specificando l'oggetto). Quando un thread entra in un blocco `synchronized` sull'oggetto `X`, ne "ruba la chiave". Ogni altro thread che tenti di entrare in un blocco sincronizzato sullo stesso `X` troverà la porta chiusa e passerà in stato di *Blocked* finché il primo non uscirà rilasciando il lock.

### Coordinamento Avanzato: `wait()` e `notify()`
Spesso i thread devono collaborare ("Il Consumatore aspetta che il Produttore inserisca dati nel buffer"). Per fare questo si usano i metodi della superclasse assoluta `Object` (non di `Thread`!), da chiamare **esclusivamente** all'interno di contesti `synchronized`:
- **`wait()`**: Il thread in esecuzione *rilascia immediatamente il lock* dell'oggetto e si congela, entrando in stato di *Waiting*.
- **`notify()` / `notifyAll()`**: Risveglia uno (o tutti) i thread che si erano precedentemente addormentati in `wait()` su quel medesimo oggetto, permettendogli di competere di nuovo per riacquistare il lock.

### Il Nemico Mortale: Il Deadlock (Stallo)
Un **Deadlock** è uno stallo fatale e irrisolvibile. Si verifica quando due o più thread si bloccano a vicenda attendendo risorse l'uno dall'altro. 
*Esempio Classico:*
1. Il Thread 1 acquisisce il lock dell'oggetto A, poi ha bisogno del lock dell'oggetto B.
2. Il Thread 2 acquisisce il lock dell'oggetto B, poi ha bisogno del lock dell'oggetto A.
Entrambi aspetteranno in eterno che l'altro rilasci la risorsa. Il programma si congela. Java *non dispone di alcun meccanismo magico per prevenire o uccidere un deadlock*; è esclusiva responsabilità dell'architetto del software progettare gerarchie rigorose nell'acquisizione dei lock.

### Sintassi ed Esempi di Codice
```java
// Implementazione consigliata tramite Runnable per il pattern Produttore-Consumatore
public class SyncStack implements Runnable {
    private int[] array = new int[5];
    private int count = 0;
    private boolean isProducer;

    public SyncStack(boolean isProducer) { this.isProducer = isProducer; }

    // Mutua Esclusione e Coordinamento Inter-Thread (wait/notify)
    public synchronized void inserisci(int dato) throws InterruptedException {
        // OBBLIGATORIO: Utilizzo del WHILE per gestire i falsi risvegli (Spurious Wakeups)
        while (count == array.length) {
            System.out.println("Stack Pieno! Produttore in wait()...");
            wait(); // Rilascia il lock dell'oggetto e si addormenta
        }
        array[count] = dato;
        count++;
        System.out.println("Inserito: " + dato);
        notifyAll(); // Risveglia i thread Consumatori in attesa
    }
    
    public synchronized void estrai() throws InterruptedException {
        while (count == 0) {
            System.out.println("Stack Vuoto! Consumatore in wait()...");
            wait();
        }
        count--;
        int estratto = array[count];
        System.out.println("Estratto: " + estratto);
        notifyAll(); // Risveglia i thread Produttori
    }

    @Override
    public void run() {
        try {
            if (isProducer) { 
                inserisci(10); 
                Thread.sleep(500); // sleep sospende il thread senza cedere lock
            } else { 
                estrai(); 
                Thread.yield(); // yield cede gentilmente il passo allo Scheduler
            }
        } catch (InterruptedException e) {
            System.out.println("Thread interrotto violentemente!");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        SyncStack risorsa = new SyncStack(true); // Simulazione del Produttore
        
        // La nostra classe passata in pasto al motore Thread
        Thread t1 = new Thread(risorsa, "IlMioThread");
        
        // ERRORE GRAVE: t1.run(); (Lo eseguirebbe sequenzialmente nel main)
        t1.start(); // Avvio corretto asincrono
        
        System.out.println("Thread vivo? " + t1.isAlive());
        
        // Il Main Thread si blocca e aspetta che t1 muoia prima di procedere
        t1.join(); 
        
        System.out.println("Programma terminato regolarmente.");
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Non chiamare `run()`!:** Come visto nell'esempio, invocare esplicitamente `.run()` trasforma il task in una noiosa esecuzione sequenziale. Per la magia asincrona serve obbligatoriamente `.start()`.
- **`wait()` e `notify()` orfani:** I metodi di wait/notify vanno invocati **esclusivamente** all'interno di metodi (o blocchi) marcati come `synchronized`. Se lo fai fuori da un blocco monitorato, la JVM lancerà un'atroce `IllegalMonitorStateException`.
- **Prevenire i Deadlock:** La regola d'oro accademica per evitare i deadlock è forzare tutti i thread ad acquisire lock multipli sempre ed esclusivamente nello stesso identico ordine.

---

## 3. XML Parsing

### Teoria Fondamentale
L'estrapolazione di dati da file XML avviene tramite Parser. In Java, un approccio ottimizzato, specialmente per file giganteschi, è il **SAX Parser (Simple API for XML)**. SAX non carica l'intero albero XML in RAM (al contrario del DOM), ma scorre i nodi uno ad uno e reagisce generando "eventi" sequenziali gestiti tramite Callback (tecnica *Push* o guidata da eventi).

> **Nota del Docente (Le Callback SAX):**
> Estendendo la classe `DefaultHandler`, sovrascriviamo tre metodi d'intercettazione cruciali:
> - `startElement`: Scatta alla vista di un tag di apertura (es. `<studente>`).
> - `characters`: Estrae il vero e proprio testo contenuto tra i due tag.
> - `endElement`: Scatta alla chiusura (es. `</studente>`).

### Sintassi ed Esempi di Codice
```java
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;
import java.io.File;

public class LettoreXML {

    public static void main(String[] args) {
        try {
            // Configurazione Fabbrica e Parser
            SAXParserFactory factory = SAXParserFactory.newInstance();
            SAXParser saxParser = factory.newSAXParser();

            // Sviluppo dell'Handler Custom
            DefaultHandler handler = new DefaultHandler() {
                boolean bNome = false;

                // Evento di Apertura
                public void startElement(String uri, String localName, String qName, Attributes attributes) {
                    if (qName.equalsIgnoreCase("NOME")) {
                        bNome = true;
                    }
                }

                // Evento di Estrazione Testuale
                public void characters(char ch[], int start, int length) {
                    if (bNome) {
                        System.out.println("Nome studente XML: " + new String(ch, start, length));
                        bNome = false; // Resetto il flag
                    }
                }

                // Evento di Chiusura
                public void endElement(String uri, String localName, String qName) {
                    if (qName.equalsIgnoreCase("STUDENTE")) {
                        System.out.println("Fine lettura record studente.");
                    }
                }
            };

            // Avvio della cattura eventi passandogli un file (es. database.xml) e l'Handler
            File inputFile = new File("database.xml");
            saxParser.parse(inputFile, handler);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Il problema della stringa spezzata in `characters`:** Il metodo `characters` non garantisce matematicamente di restituire il contenuto di un tag in un singolo colpo di callback; l'XML parser può frammentare le stringhe molto lunghe su invocazioni multiple. Spesso, un robusto Handler deve usare un `StringBuilder` concatenando i pezzi ad ogni scatto e chiudere la valutazione solo nell'`endElement`.