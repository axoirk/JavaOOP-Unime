# Livello 4: Argomenti Avanzati

## 1. File I/O, Stream e Serializzazione

### Teoria Fondamentale: Il Pattern Decorator e gli Stream
L'architettura I/O (Input/Output) di Java è basata sul concetto astratto di **Stream** (Flusso). Un flusso è un nastro trasportatore di dati continuo e sequenziale, che può scorrere in entrata (`InputStream` / `Reader`) o in uscita (`OutputStream` / `Writer`).
Java divide gli stream in due mondi:
1. **Byte Streams (8-bit):** Per dati crudi binari (immagini, audio, eseguibili). Classi base: `InputStream` e `OutputStream`.
2. **Character Streams (16-bit):** Per testo umano (Unicode). Classi base: `Reader` e `Writer`.

> **Definizione Accademica (Pattern Decorator nell'I/O):**
> Le API di I/O di Java non hanno una classe magica che fa tutto. Usano il *Pattern Decorator*. Si parte da uno stream "grezzo" (es. `FileReader`, che legge dal disco un carattere alla volta in modo lento) e lo si "incarta" o "decora" dentro uno stream più intelligente (es. `BufferedReader`), il quale aggiunge un buffer in RAM per azzerare i colli di bottiglia del disco rigido e aggiunge il comodo metodo `readLine()`.

La **Serializzazione** è il processo di ibernazione di un Oggetto. Prende l'intero "stato" (valori delle variabili) di un oggetto vivo nella memoria Heap e lo congela in una sequenza di byte crudi (Stream Binario). Questo permette di salvare l'oggetto su disco o spedirlo via rete. L'interfaccia `Serializable` è una **Marker Interface** (senza metodi): funge solo da "timbro" per autorizzare la JVM a compiere la serializzazione.

### Sintassi ed Esempi di Codice
```java
import java.io.*;

// La Marker Interface abilita la serializzazione.
public class Videogioco implements Serializable {
    // ID Univoco di Versione (Cruciale per retrocompatibilità)
    private static final long serialVersionUID = 1L;
    
    private String titolo;
    // 'transient' inibisce la serializzazione di questo specifico campo
    private transient String passwordSegreta; 
    
    public Videogioco(String titolo, String password) { 
        this.titolo = titolo; 
        this.passwordSegreta = password;
    }
    public String getTitolo() { return titolo; }
}

public class GestoreArchitetturaIO {
    public static void main(String[] args) {
        
        // 1. I/O TESTUALE: Scrittura Ottimizzata con Decorator
        // FileWriter (grezzo) -> incartato in -> PrintWriter (intelligente)
        // Il costrutto 'try-with-resources' chiude il buffer automaticamente!
        try (PrintWriter writer = new PrintWriter(new FileWriter("log.txt", true))) {
            writer.println("Operazione registrata con successo.");
        } catch (IOException e) {
            System.err.println("Errore disco: " + e.getMessage());
        }

        // 2. SERIALIZZAZIONE BINARIA (ObjectOutputStream)
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("save.dat"))) {
            Videogioco game = new Videogioco("Zelda", "qwerty1234");
            oos.writeObject(game); // Congela l'oggetto su disco
            System.out.println("Oggetto serializzato.");
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        // 3. DESERIALIZZAZIONE BINARIA (ObjectInputStream)
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("save.dat"))) {
            // DOWNCASTING OBBLIGATORIO: readObject() restituisce un 'Object' generico.
            Videogioco gameRicaricato = (Videogioco) ois.readObject();
            System.out.println("Titolo caricato: " + gameRicaricato.getTitolo());
            // La password sarà null, perché era marcata come 'transient'!
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Il Memory Leak del Buffer non svuotato:** Se non usi il `try-with-resources` e dimentichi di chiamare `.close()` (o almeno `.flush()`) su un `PrintWriter` o `BufferedWriter`, i dati rimarranno intrappolati nella RAM e il file sul disco risulterà miseramente vuoto (a 0 byte). Il `close()` forza lo svuotamento fisico sul disco.
- **La Trappola del SerialVersionUID:** Se serializzi la classe `Videogioco`, poi chiudi il programma, aggiungi una nuova variabile alla classe (es. `int anno`), e provi a deserializzare il vecchio file, la JVM lancerà un'esplosiva `InvalidClassException`. Java calcola un hash (ID) in base ai campi della classe. Se cambiano, l'ID non combacia più. *Soluzione:* Dichiara esplicitamente un `private static final long serialVersionUID = 1L;`. Questo dirà alla JVM di fidarsi e tentare il recupero anche se la struttura è leggermente mutata.

---

## 2. Multithreading e Sincronizzazione

### Teoria Fondamentale: Processi vs Thread
Un **Processo (Task)** è un programma in esecuzione. Ogni processo possiede uno **spazio di memoria privato** (context) e non può accedere a quello di altri processi (salvo meccanismi complessi come i socket o memoria condivisa). Il cambio di contesto (Context Switch) tra processi è un'operazione estremamente pesante per la CPU.

Un **Thread** è la più piccola unità di esecuzione. Un processo può essere frammentato in innumerevoli Thread. La differenza fondamentale è che i thread **condividono lo stesso spazio di memoria (Heap)** del processo padre, pur avendo ciascuno il proprio Stack privato per le variabili locali.
*Vantaggi:*
- Cambio di contesto molto più rapido e leggero.
- Comunicazione fulminea inter-thread essendo nello stesso Heap.

### Creazione di un Thread: `Runnable` vs `Thread` (Esempi Pratici)
In Java ci sono due approcci ortodossi per definire e lanciare un Thread. Questa non è solo una scelta stilistica, ma una decisione architetturale.

#### Metodo 1: Estendere la classe `Thread`
Si crea una sottoclasse di `java.lang.Thread` e si esegue l'override del metodo `run()`.
**Svantaggio Accademico Letale:** Java impone l'ereditarietà singola. Se estendi `Thread`, la tua classe non potrà **mai** estendere nessun'altra classe (es. non potrà estendere `JFrame` per creare un'interfaccia grafica o `Applet` per il web).

> **Nota del Docente (Il bypass dell'Ereditarietà Multipla):**
> L'interfaccia `Runnable` risolve in modo ingegnoso l'impossibilità di usare l'ereditarietà multipla in Java. Se la tua classe (es. `Applicazione`) *deve* per forza estendere una superclasse base (es. `extends Applet`), ma hai contemporaneamente bisogno che svolga operazioni parallele come un Thread, non puoi scrivere `extends Applet, Thread` (il compilatore lo vieta). Derivando dalla classe base e *implementando* `Runnable`, si riesce a personalizzare la classe base e allo stesso tempo ad aggiungere le funzionalità di thread. In sintesi, l'uso di `Runnable` è assolutamente obbligatorio quando la classe che vuoi rendere un thread è *già* una classe derivata!

*Esempio 1A: Definizione e lancio dal Main*
```java
// Definizione
public class MioThreadEsteso extends Thread {
    @Override
    public void run() {
        System.out.println("Esecuzione parallela tramite estensione di Thread.");
    }
}

// Lancio
public class TestEsteso {
    public static void main(String[] args) {
        MioThreadEsteso t1 = new MioThreadEsteso();
        // NON chiamare t1.run()! Devi chiamare start() per il multithreading.
        t1.start(); 
    }
}
```

*Esempio 1B: Il Thread che si "Auto-Lancia"*
Un pattern elegante è far sì che il Thread si auto-avvii non appena viene istanziato, includendo la chiamata `start()` direttamente nel suo costruttore.
```java
public class ThreadAutoAvviante extends Thread {
    public ThreadAutoAvviante() {
        // Il thread chiama start() su se stesso al momento della creazione
        this.start(); 
    }

    @Override
    public void run() {
        System.out.println("Sono partito da solo!");
    }
}

// Nel main basta solo instanziarlo:
// new ThreadAutoAvviante();
```

#### Metodo 2: Implementare l'interfaccia `Runnable` (Consigliato)
Si crea una classe che implementa il metodo `run()`, poi la si passa come parametro (target) al costruttore di un nuovo oggetto `Thread`.
**Vantaggio:** È il metodo caldamente consigliato dall'ingegneria del software. Permette alla tua classe di ereditare liberamente da altre classi padre e separa nettamente la logica del "Task" (il lavoro da svolgere) dal "Motore" (il Thread fisico che lo esegue).

*Esempio 2A: Definizione e lancio dal Main*
```java
// Definizione del Task
public class MioTask implements Runnable {
    @Override
    public void run() {
        System.out.println("Esecuzione parallela tramite Runnable.");
    }
}

// Lancio
public class TestRunnable {
    public static void main(String[] args) {
        MioTask task = new MioTask(); // Creo l'entità logica
        Thread t1 = new Thread(task); // Inietto il task nel Motore Thread
        t1.start(); // Avvio il motore
    }
}
```

*Esempio 2B: Il Runnable che si auto-avvia*
In questo caso, la classe non è un Thread, ma possiede un Thread interno (composizione) a cui passa se stessa (`this`).
```java
public class RunnableAutoAvviante implements Runnable {
    private Thread motore;

    public RunnableAutoAvviante() {
        // Inietto me stesso (this, in quanto Runnable) nel nuovo Thread
        motore = new Thread(this);
        motore.start(); // Avvio il motore
    }

    @Override
    public void run() {
        System.out.println("Runnable auto-avviato tramite composition!");
    }
}

// Nel main:
// new RunnableAutoAvviante();
```

### Gli Stati (Ciclo di Vita) di un Thread
1. **New**: Istanza appena creata, prima del `start()`.
2. **Runnable**: Dopo `start()`. È in coda, fiducioso che lo Scheduler di Sistema (che usa spesso algoritmi *Preemptive* e *Round-Robin*) gli assegni presto un "time-slice" (fetta di tempo) della CPU.
3. **Running**: Ha il controllo totale della CPU.
4. **Blocked**: Il thread è stato cacciato dalla CPU ed è "addormentato" in attesa di un I/O, della scadenza di un timer (`sleep`), o dello sblocco di un Monitor.
5. **Dead**: Il metodo `run()` è terminato. Il thread evapora.

### Metodi di Controllo e Sincronizzazione
- **`start()` vs `run()`:** Se invochi `run()` a mano, il codice viene eseguito in modo noiosamente sequenziale sul main thread! Per biforcare davvero l'esecuzione asincrona, devi categoricamente invocare **`start()`**.
- **`sleep(millis)` e `yield()`:** `sleep` paralizza il thread a tempo, **senza mai rilasciare eventuali Lock** (pericolo!). `yield` è invece un atto di gentilezza: il thread rinuncia volontariamente alla sua fetta di tempo CPU a favore di un compagno con pari priorità.
- **`join()`:** Fondamentale. Ferma l'esecuzione del thread principale e lo costringe ad aspettare finché il thread bersaglio non è morto.
- **Race Condition e `synchronized`:** Se due thread toccano l'Heap in parallelo (es. `i++`), l'operazione non essendo "atomica" causa collisioni (Race Condition). Il modificatore `synchronized` trasforma un blocco in una cassaforte. Richiede un "Lock" (Monitor) su un oggetto: entra un solo thread alla volta, realizzando la **Mutua Esclusione**.

### Nemesi e Coordinamento: `wait()`, `notify()` e Deadlock
Un **Deadlock (Stallo)** è un abbraccio mortale: il Thread A possiede il Lock 1 e aspetta il Lock 2. Il Thread B possiede il Lock 2 e aspetta il Lock 1. Nessuno molla la presa. Il software si pietrifica senza lanciare eccezioni.

Per un sano coordinamento (es. Produttore-Consumatore), Java offre (solo dentro aree `synchronized`):
- **`wait()`**: Il thread entra in un profondo sonno e, a differenza dello `sleep`, **rilascia immediatamente il Lock** che possedeva, permettendo ad altri di lavorare.
- **`notifyAll()`**: Urla al sistema di svegliare i compagni addormentati in `wait()` sullo stesso oggetto.

### Sintassi ed Esempi di Codice
```java
public class SyncBuffer implements Runnable {
    private int[] array = new int[5];
    private int count = 0;
    private boolean isProducer;

    public SyncBuffer(boolean isProducer) { this.isProducer = isProducer; }

    public synchronized void produci(int dato) throws InterruptedException {
        // Uso del WHILE obbligatorio per i "Falsi Risvegli" (Spurious Wakeups)
        while (count == array.length) {
            wait(); // Cede la risorsa e attende
        }
        array[count] = dato;
        count++;
        notifyAll(); // Risveglia eventuali Consumatori affamati
    }
    
    public synchronized void consuma() throws InterruptedException {
        while (count == 0) {
            wait(); // Cede la risorsa e attende dati
        }
        count--;
        notifyAll(); // Risveglia eventuali Produttori intasati
    }

    @Override
    public void run() {
        try {
            if (isProducer) produci(42);
            else consuma();
        } catch (InterruptedException e) { }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(new SyncBuffer(true), "Produttore");
        t1.start(); // LANCIO VERO DEL THREAD (non usare .run()!)
        
        System.out.println("Esecuzione asincrona in corso...");
        t1.join(); // Il Main aspetta pazientemente la fine di t1
    }
}
```

---

## 3. Elaborazione XML in Java: SAX, DOM e JAXP

### Teoria Fondamentale: L'Ecosistema JAXP e il Pattern Factory
L'XML (eXtensible Markup Language) è uno standard universale per la rappresentazione gerarchica dei dati. Affinché un'applicazione Java possa comprendere un file XML, necessita di un **Parser** (analizzatore sintattico), il cui compito è decomporre il documento nei suoi elementi (tag, attributi, testo) e verificarne la correttezza formale (validazione).

In Java, la gestione del parsing non avviene invocando direttamente una specifica libreria, ma passando attraverso un framework di astrazione chiamato **JAXP (Java API for XML Processing)**. 

> **Definizione Accademica (Indipendenza tramite Pattern Factory):**
> JAXP permette al programmatore di operare in totale indipendenza dall'effettiva implementazione del parser sottostante. Utilizza elegantemente il **Pattern Factory**: anziché usare la keyword `new` per istanziare un parser specifico (il che accoppierebbe il codice a quella specifica libreria), si chiede a una "Fabbrica Astratta" di fornirci un'istanza generica compatibile.
> Esempio: `SAXParserFactory.newInstance().newSAXParser();`

Dal punto di vista architetturale, l'interfacciamento tra applicazioni e parser si divide in due grandi famiglie di API diametralmente opposte per filosofia e gestione della memoria: **SAX** e **DOM**.

### Il Modello ad Eventi: Interfacce SAX (Simple API for XML)
Il parser SAX adotta un approccio puramente **sequenziale ed Event-Based**. 
- **Meccanica:** Scorre il documento dall'alto verso il basso una sola volta. Non mantiene **nulla in memoria** (nessuna rappresentazione del file XML viene salvata in RAM).
- **Vantaggi:** Estremamente veloce e leggero. È l'unica scelta ingegneristica possibile per analizzare file XML giganteschi (es. log da 5GB) senza far crollare la JVM in `OutOfMemoryError`.
- **Svantaggi:** Poiché scorre in avanti, non permette di navigare all'indietro nell'albero né di modificare il documento dinamicamente.

SAX si basa sul concetto di **Callback**. Il programmatore definisce una classe (che tipicamente estende `DefaultHandler`) contenente metodi specifici (`startElement`, `characters`, `endElement`). Il parser SAX, leggendo il file, "spara" eventi (trigger) invocando questi metodi ogni volta che incontra l'apertura di un tag, il suo contenuto testuale e la sua chiusura.

### Il Modello ad Albero: Interfacce DOM (Document Object Model)
Il DOM (standard W3C) adotta un approccio **Object-Oriented**.
- **Meccanica:** Il parser legge interamente l'XML e costruisce nella memoria RAM un immenso **Parse-Tree (Albero sintattico)**. Ogni tag diventa un oggetto di tipo `Element`, ogni attributo un `Attr` e i testi interni diventano `TextNode`. L'intero albero è racchiuso nell'oggetto radice `Document`.
- **Vantaggi:** Livello di astrazione elevatissimo. Permette di navigare liberamente in ogni direzione (figli, genitori, fratelli) e consente di manipolare il documento (aggiungere o rimuovere nodi dinamicamente).
- **Svantaggi:** Essendo l'intero albero caricato simultaneamente in RAM, richiede un quantitativo di memoria spropositato. Inadatto per file di grandi dimensioni.

### Sintassi ed Esempi di Codice: Implementazione SAX

```java
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;
import java.io.File;

public class ArchitetturaSAX {

    public static void main(String[] args) {
        try {
            // 1. IL PATTERN FACTORY DI JAXP
            // Chiediamo alla Factory di generarci un parser SAX
            SAXParserFactory factory = SAXParserFactory.newInstance();
            SAXParser saxParser = factory.newSAXParser();

            // 2. L'HANDLER DEGLI EVENTI (Callback)
            // Sviluppiamo il nostro ricettore di eventi estendendo DefaultHandler (l'interfaccia Parser-to-Application)
            DefaultHandler handler = new DefaultHandler() {
                private StringBuilder bufferTesto = new StringBuilder();
                private boolean inNome = false;

                // Evento 1: Il parser incontra l'apertura di un tag (es. <nome id="1">)
                @Override
                public void startElement(String uri, String localName, String qName, Attributes attributes) {
                    bufferTesto.setLength(0); // Resetta il buffer per il nuovo tag
                    if (qName.equalsIgnoreCase("NOME")) {
                        inNome = true;
                        // Estrazione sicura di un attributo
                        String id = attributes.getValue("id"); 
                        if(id != null) System.out.println("Trovato ID: " + id);
                    }
                }

                // Evento 2: Il parser legge il testo puro (PCDATA) tra i tag
                @Override
                public void characters(char ch[], int start, int length) {
                    if (inNome) {
                        // Accumuliamo i frammenti chirurgicamente
                        bufferTesto.append(new String(ch, start, length));
                    }
                }

                // Evento 3: Il parser incontra la chiusura del tag (es. </nome>)
                @Override
                public void endElement(String uri, String localName, String qName) {
                    if (qName.equalsIgnoreCase("NOME")) {
                        System.out.println("Valore Nome: " + bufferTesto.toString().trim());
                        inNome = false; // Chiudiamo il "cancello"
                    }
                }
            };

            // 3. AVVIO DELL'ELABORAZIONE
            // Iniezione del file fisico e dell'Handler nel motore del parser
            saxParser.parse(new File("database.xml"), handler);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Sintassi ed Esempi di Codice: Implementazione DOM

```java
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import java.io.File;

public class ArchitetturaDOM {
    public static void main(String[] args) {
        try {
            // 1. IL PATTERN FACTORY PER DOM
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = dbf.newDocumentBuilder();
            
            // 2. CREAZIONE DEL PARSE-TREE IN RAM
            Document doc = builder.parse(new File("database.xml"));
            // Ottimizza l'albero unendo nodi di testo frammentati
            doc.getDocumentElement().normalize(); 
            
            System.out.println("Elemento Radice: " + doc.getDocumentElement().getNodeName());
            
            // 3. NAVIGAZIONE DELL'OGGETTO
            // Estrae una lista ordinata di tutti i nodi <studente>
            NodeList listaStudenti = doc.getElementsByTagName("studente");
            
            for (int i = 0; i < listaStudenti.getLength(); i++) {
                // Casting accademico: ci assicuriamo che il nodo sia effettivamente un Elemento (tag)
                if (listaStudenti.item(i).getNodeType() == org.w3c.dom.Node.ELEMENT_NODE) {
                    Element elementoStudente = (Element) listaStudenti.item(i);
                    
                    // Navigazione agile tipica del DOM
                    String nome = elementoStudente.getElementsByTagName("nome").item(0).getTextContent();
                    System.out.println("Studente Trovato: " + nome);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Scelta Sbagliata dell'Architettura:** Usare DOM per leggere un file XML di 1GB porterà a un irreparabile `OutOfMemoryError`. La RAM richiesta per costruire l'albero DOM è spesso molto maggiore della dimensione del file stesso. Inversa, usare SAX per un file di configurazione minuscolo su cui bisogna iterare avanti e indietro rende il codice inutilmente complesso. Un ingegnere del software sceglie l'architettura in base alla natura del dato.
- **La frammentazione in SAX (`characters`):** L'errore universale in SAX è supporre che il testo "Ciao" tra i tag `<a>` e `</a>` venga passato interamente in una singola chiamata alla callback `characters`. Il parser si riserva il diritto di spezzare la stringa e invocare il metodo `characters` decine di volte per lo stesso tag! È per questo che è **obbligatorio** usare uno `StringBuilder` per accumulare i frammenti nell'evento `characters` e valutare la stringa completa solo all'innesco dell'`endElement`. Usare la concatenazione classica con `String` saturerebbe istantaneamente l'Heap (immutabilità delle stringhe).

---

> ⚠️ **SEGNALAZIONE: ARGOMENTI MANCANTI E DA SPOSTARE RISPETTO AL NUOVO SYLLABUS**
> In base alla nuova organizzazione a 7 livelli, in questo file mancano i seguenti argomenti (che appartengono al Livello 4):
> - **Interfacce Grafiche (GUI):** Lo sviluppo visivo tramite librerie come `Swing` (es. `JFrame`, `JLabel`, `JButton`).
> - **Layout e Action Listener:** Gestione degli eventi generati dall'interfaccia (come il click dei bottoni) e disposizione geometrica dei componenti a schermo.
> 
> *Nota Strutturale:* La teoria su **Multithreading e Sincronizzazione** (presente qui) andrebbe spostata nel `LESSON.md` del **Livello 5**. La teoria sull'**XML (SAX e DOM)** andrebbe spostata nel **Livello 6**.