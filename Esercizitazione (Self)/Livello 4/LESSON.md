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

### Teoria Fondamentale
Un Thread è un flusso di esecuzione "leggero" allocato in un Processo. Java implementa nativamente il Multithreading per l'esecuzione di operazioni concorrenti.

> **Definizione Accademica (Interferenza di Thread o Race Condition):**
> La **Race Condition** avviene quando più Thread accedono simultaneamente e in lettura/scrittura alla stessa porzione di memoria (es. un array condiviso o una variabile `count`). Senza supervisione, le azioni si accavallano originando dati corrotti. 
> La parola chiave **`synchronized`** applica un lucchetto (Lock o Monitor) sull'oggetto, permettendo l'ingresso al blocco critico a un solo Thread per volta (Mutua Esclusione).

| Stato del Thread | Significato |
| --- | --- |
| **New** | Istanza creata, ma `start()` non è ancora stato chiamato. |
| **Runnable / Running**| Thread pronto, in esecuzione (assegnato allo Scheduler). |
| **Blocked / Waiting** | Sospeso in attesa di un Lock o ha invocato `wait()`. |
| **Terminated** | Esecuzione del metodo `run()` completata regolarmente. |

### Sintassi ed Esempi di Codice
```java
// Il task Produttore/Consumatore condividerà questa risorsa
public class SyncStack {
    private int[] array = new int[5];
    private int count = 0;

    // Mutua Esclusione e Coordinamento Inter-Thread
    public synchronized void inserisci(int dato) throws InterruptedException {
        // OBBLIGATORIO: Utilizzo del WHILE per gestire i falsi risvegli (Spurious Wakeups)
        while (count == array.length) {
            System.out.println("Stack Pieno! Sospensione...");
            wait(); // Rilascia il lock e si addormenta
        }
        
        array[count] = dato;
        count++;
        System.out.println("Inserito: " + dato);
        
        notifyAll(); // Risveglia i thread Consumatori in attesa
    }
    
    public synchronized void estrai() throws InterruptedException {
        while (count == 0) {
            System.out.println("Stack Vuoto! Sospensione...");
            wait();
        }
        
        count--;
        int estratto = array[count];
        System.out.println("Estratto: " + estratto);
        
        notifyAll(); // Risveglia i thread Produttori
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Non chiamare `run()`!:** Chiamare esplicitamente `.run()` su un Thread esegue il metodo in modo sequenziale sul Thread Principale (main). Per attivare la magia del vero parallelismo, si deve obbligatoriamente invocare il metodo **`.start()`**, il quale affida il flusso allo Scheduler di sistema.
- **Implementare Runnable o Estendere Thread?** Dal punto di vista architetturale e accademico, è infinitamente preferibile `implements Runnable` e darlo in pasto a un `new Thread(mioRunnable)`. Essendo Java a singola eredità, estendere Thread "brucia" l'unico spazio disponibile di ereditarietà per la classe.
- **`wait()` e `notify()` orfani:** I metodi `wait()`, `notify()` e `notifyAll()` vanno invocati **esclusivamente** all'interno di metodi (o blocchi) marcati come `synchronized`. Fallire questa regola scaturisce in una violenta `IllegalMonitorStateException`.

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