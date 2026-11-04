# Livello 4: Dati, Input/Output e Interfacce Grafiche (GUI)

## 1. Java File Handling: La classe `File`

Prima di poter leggere o scrivere fisicamente i dati dentro un file, è fondamentale capire come Java rappresenta e gestisce file e cartelle a livello di file system. Questo è il compito della classe `java.io.File`.

### Teoria Fondamentale: Rappresentazione, non Contenuto
Un errore concettuale molto comune è pensare che un oggetto `File` in Java contenga i dati del file stesso (il testo, i byte, le immagini). **Falso.** Un oggetto `File` è semplicemente una *rappresentazione astratta di un percorso* (path) all'interno del sistema operativo. È come un cartello stradale che punta a un indirizzo: il file a quell'indirizzo potrebbe esistere, oppure no.

Tramite i metodi di questa classe possiamo compiere vere e proprie operazioni di "amministrazione", come verificare l'esistenza di un file, crearne uno nuovo (vuoto), eliminare documenti, controllare i permessi di lettura/scrittura o navigare all'interno di intere cartelle (directory).

*Esempio: Operazioni di base sul File System*
```java
import java.io.File;
import java.io.IOException;

public class GestioneFile {
    public static void main(String[] args) {
        // Creiamo un oggetto File. ATTENZIONE: Questo NON crea fisicamente il file sul disco!
        // Crea solo l'oggetto Java che "punta" a quel percorso.
        File mioFile = new File("archivio_dati.txt");
        File miaCartella = new File("CartellaDiTest");

        // 1. Gestione Cartelle (Directory)
        if (!miaCartella.exists()) {
            boolean creata = miaCartella.mkdir(); // mkdir() crea la cartella
            System.out.println("Cartella creata con successo? " + creata);
        }

        // 2. Creazione e Verifica di un File
        try {
            if (mioFile.exists()) {
                System.out.println("Il file esiste già!");
                System.out.println("Percorso assoluto: " + mioFile.getAbsolutePath());
                System.out.println("Dimensione in byte: " + mioFile.length());
                System.out.println("È leggibile? " + mioFile.canRead());
            } else {
                // createNewFile() tenta di creare fisicamente un file vuoto sul disco.
                // Può fallire (es. disco pieno, permessi negati), per questo serve il try-catch.
                boolean fileCreato = mioFile.createNewFile(); 
                if (fileCreato) {
                    System.out.println("Nuovo file vuoto creato fisicamente sul disco.");
                }
            }
        } catch (IOException e) {
            System.err.println("Errore di I/O durante la creazione: " + e.getMessage());
        }

        // 3. Eliminazione (Decommentare per testare)
        // if (mioFile.delete()) {
        //     System.out.println("Il file è stato eliminato definitivamente.");
        // }
    }
}
```

---

## 2. File I/O, Stream e Serializzazione

### Teoria Fondamentale: Il Pattern Decorator e gli Stream
L'architettura I/O (Input/Output) di Java affronta il problema universale di spostare dati dal programma verso il mondo esterno (Hard Disk, Rete, Monitor) e viceversa. Il concetto centrale su cui si fonda questa architettura è lo **Stream** (Flusso). Uno stream va inteso come un nastro trasportatore unidirezionale e continuo di dati. Esistono flussi in entrata, che "pompano" dati dall'esterno verso la RAM (`InputStream` / `Reader`), e flussi in uscita, che drenano dati dalla RAM verso una destinazione (`OutputStream` / `Writer`).

Perché non c'è una singola classe per fare tutto? Perché Java divide rigorosamente l'informazione in due regni:
1. **Byte Streams (Flussi a 8-bit):** Gestiscono i dati crudi nella loro forma nativa binaria. Sono indispensabili per manipolare immagini, file audio, eseguibili o flussi di rete grezzi. Le superclassi di riferimento sono `InputStream` e `OutputStream`.
2. **Character Streams (Flussi a 16-bit):** Sono specializzati nel trattamento del testo umano (caratteri Unicode). Riducono enormemente la fatica del programmatore, occupandosi automaticamente della codifica e decodifica dei caratteri (es. UTF-8). Le superclassi di riferimento sono `Reader` e `Writer`.

> **L'Eleganza del Pattern Decorator nell'I/O:**
> Le API di I/O di Java non offrono "classi magiche" monolitiche. Utilizzano invece un design pattern strutturale chiamato *Decorator*. L'idea è partire da uno stream "grezzo" e basilare (ad esempio `FileReader`, che interagisce col sistema operativo e legge il disco carattere per carattere in modo terribilmente lento) e "incartarlo" (decorarlo) passandolo al costruttore di uno stream di livello superiore e più intelligente (come `BufferedReader`). Quest'ultimo non legge direttamente dal disco, ma preleva pacchetti enormi di dati in blocco dallo stream grezzo, li immagazzina in una memoria temporanea (il buffer in RAM) e ti permette di estrarli riga per riga (tramite l'utilissimo metodo `readLine()`). Questo approccio azzera i colli di bottiglia fisici del disco rigido e rende il design estremamente modulare.

### Lettura e Scrittura di File di Testo (Character Streams)
Trattare file di testo è l'operazione di I/O più comune. L'approccio ortodosso e performante prevede l'uso di stream bufferizzati:
- Per **scrivere**, si combina un `FileWriter` (per l'accesso fisico al file) con un `BufferedWriter` (per le performance) o un `PrintWriter` (che fornisce metodi comodi come `println()`).
- Per **leggere**, si combina un `FileReader` con un `BufferedReader`.

*Esempio 1: Scrivere in un file di testo*
```java
import java.io.*;

public class EsempioScritturaFile {
    public static void main(String[] args) {
        // Il costrutto 'try-with-resources' (le parentesi tonde dopo il try) è imperativo in Java moderno!
        // Esso garantisce che il metodo .close() venga chiamato in automatico alla fine del blocco, 
        // chiudendo le risorse del sistema operativo anche in caso di eccezioni.
        // Il parametro 'true' in FileWriter abilita l'append mode: non sovrascrive, aggiunge in coda.
        try (PrintWriter writer = new PrintWriter(new FileWriter("documento.txt", true))) {
            writer.println("Questa è una riga scritta dal programma Java.");
            writer.println("I Character Stream gestiscono il testo in modo eccellente.");
            System.out.println("Scrittura completata con successo.");
        } catch (IOException e) {
            System.err.println("Impossibile accedere al file: " + e.getMessage());
        }
    }
}
```

*Esempio 2: Leggere da un file di testo*
```java
import java.io.*;

public class EsempioLetturaFile {
    public static void main(String[] args) {
        // Incartiamo il noioso FileReader dentro un BufferedReader ad alte prestazioni.
        try (BufferedReader reader = new BufferedReader(new FileReader("documento.txt"))) {
            String riga;
            // Leggiamo fino a quando readLine() non restituisce null (fine del file - EOF)
            while ((riga = reader.readLine()) != null) {
                System.out.println("Letto dal file: " + riga);
            }
        } catch (FileNotFoundException e) {
            System.err.println("Il file specificato non esiste!");
        } catch (IOException e) {
            System.err.println("Errore durante la lettura: " + e.getMessage());
        }
    }
}
```

> **`readLine()` si chiama una volta sola per giro.** Ogni chiamata **consuma** una riga: `if (reader.readLine() != null) { riga = reader.readLine(); }` legge due righe e butta via la prima. La forma giusta assegna e controlla nella stessa espressione, come nel ciclo qui sopra: `while ((riga = reader.readLine()) != null)`. Stessa regola per un file vuoto: `riga = reader.readLine(); if (riga == null) { ... }`.

> **Aprire un file in scrittura lo svuota.** `new FileWriter("a.txt")`, `new PrintWriter("a.txt")` e `new FileOutputStream("a.txt")` **troncano il file nel momento in cui lo aprono**, prima di qualunque `write`. Per accodare serve il secondo argomento `true`: `new FileWriter("a.txt", true)`, `new FileOutputStream("a.txt", true)`. Se la traccia dice "in coda, senza cancellare le righe già presenti", senza `true` perdi il contenuto.

### Lettura e Scrittura di File Binari Crudi (Byte Streams)
Oltre al testo e agli oggetti serializzati, spesso un programma deve manipolare file binari "puri", come immagini, file audio, video o eseguibili. Per questa tipologia di file non si usano i Character Streams (che corromperebbero i dati tentando di interpretarli come testo), ma si utilizzano le classi di base dei **Byte Streams**: `FileInputStream` e `FileOutputStream`.

L'approccio più efficiente per copiare o manipolare file binari è leggere pacchetti di byte (un buffer) invece di un singolo byte alla volta, per poi scriverli immediatamente a destinazione.

*Esempio 3: Copiare un file binario (es. un'immagine) ad alte prestazioni*
```java
import java.io.*;

public class CopiaFileBinario {
    public static void main(String[] args) {
        File origine = new File("immagine.jpg");
        File destinazione = new File("immagine_copia.jpg");

        // Usiamo il try-with-resources per chiudere entrambi gli stream in automatico
        try (
            FileInputStream fis = new FileInputStream(origine);
            FileOutputStream fos = new FileOutputStream(destinazione)
        ) {
            // Creiamo un "secchio" (buffer) da 4 KB per trasportare i byte a blocchi
            byte[] buffer = new byte[4096];
            int byteLetti;

            // fis.read(buffer) riempie il secchio e restituisce quanti byte ha effettivamente letto.
            // Quando restituisce -1, significa che il file è finito.
            while ((byteLetti = fis.read(buffer)) != -1) {
                // Scriviamo nel file di destinazione solo i byte effettivamente letti nel secchio
                fos.write(buffer, 0, byteLetti);
            }
            
            System.out.println("Copia binaria completata con successo!");

        } catch (FileNotFoundException e) {
            System.err.println("File sorgente non trovato.");
        } catch (IOException e) {
            System.err.println("Errore di I/O durante la copia: " + e.getMessage());
        }
    }
}
```

### La Serializzazione degli Oggetti (Byte Streams Avanzati)
E se volessimo salvare l'intero "stato" di un Oggetto in modo che persista dopo la chiusura del programma? Interviene la **Serializzazione**. Essa è un processo chimico-informatico che prende un oggetto vivo nello Heap (con tutti i suoi campi e i relativi valori) e lo "iberna", trasformandolo in una pura sequenza di byte crudi (uno Stream Binario). 

Questa sequenza di byte può essere salvata su disco con un `FileOutputStream` oppure sparata in un socket di rete. Quando ne abbiamo bisogno, possiamo "resuscitare" l'oggetto tramite il processo inverso: la **Deserializzazione**.

Affinché un oggetto sia serializzabile, la sua classe deve esplicitamente implementare l'interfaccia `java.io.Serializable`. Questa è una **Marker Interface**, ossia non contiene alcun metodo da implementare: funge puramente da "timbro" sul passaporto dell'oggetto, autorizzando la JVM a esplorare i suoi campi privati e tradurli in binario.

*Esempio 3: Serializzazione e Deserializzazione di un Prodotto*
```java
import java.io.*;

// La classe Prodotto rappresenta un esempio generico di dato serializzabile
public class Prodotto implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private String nome;
    private double prezzo;
    // 'transient' impedisce la serializzazione di dati sensibili o temporanei
    private transient String codiceFiscaleFornitore; 
    
    public Prodotto(String nome, double prezzo, String codice) { 
        this.nome = nome; 
        this.prezzo = prezzo;
        this.codiceFiscaleFornitore = codice;
    }

    @Override
    public String toString() {
        return "Prodotto: " + nome + " | Prezzo: " + prezzo + "€";
    }
}

public class GestoreMagazzino {
    public static void main(String[] args) {
        Prodotto p = new Prodotto("Smartphone", 599.99, "XYZ123");
        String file = "magazzino.dat";

        // SERIALIZZAZIONE
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(file))) {
            oos.writeObject(p); 
            System.out.println("Prodotto salvato con successo.");
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        // DESERIALIZZAZIONE
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(file))) {
            Prodotto caricato = (Prodotto) ois.readObject();
            System.out.println("Prodotto ricaricato: " + caricato);
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
```

#### Quando una classe è davvero serializzabile
`implements Serializable` da solo non basta: la JVM deve poter convertire in byte **tutto ciò che l'oggetto contiene**. Le condizioni sono tre, e la violazione si scopre solo a runtime.

1. **La classe implementa `Serializable`.** Altrimenti `writeObject` lancia `NotSerializableException` — il codice compila senza un avviso.
2. **Ogni variabile d'istanza di tipo classe deve essere a sua volta serializzabile.** Un `Ordine` serializzabile che contiene un `Cliente` non serializzabile fallisce lo stesso: la catena si interrompe al primo anello. Le classi di libreria più comuni (`String`, i wrapper, `ArrayList`, `LinkedList`, `HashMap`) lo sono già.
3. **La superclasse dev'essere serializzabile oppure avere un costruttore senza argomenti.** In deserializzazione i campi della superclasse non serializzabile non vengono ricostruiti dai byte: vengono reinizializzati chiamando il suo costruttore di default. Se quel costruttore non esiste, la deserializzazione fallisce.

Chi vuole escludere un campo dalla catena lo marca `transient`: non viene scritto, e al ritorno vale `null` (oggetti) o `0` (numeri).

#### Un oggetto scritto due volte non viene riscritto
Dentro un singolo `ObjectOutputStream` la JVM assegna un numero di serie a ogni oggetto scritto. **Se lo stesso oggetto viene passato di nuovo a `writeObject`, sullo stream finisce solo il numero di serie, non i dati aggiornati.**

```java
Prodotto p = new Prodotto("Smartphone", 599.99);
oos.writeObject(p);
p.setPrezzo(499.99);      // modifica dopo la prima scrittura
oos.writeObject(p);       // scrive solo il riferimento: rileggendo si ottengono DUE volte 599.99
```

Serve a evitare di duplicare oggetti condivisi e a gestire i riferimenti circolari, ma diventa una trappola quando si scrive in un ciclo un oggetto riutilizzato e modificato a ogni giro. Le vie d'uscita: creare un oggetto nuovo a ogni scrittura, oppure chiamare `oos.reset()` per azzerare la tabella dei numeri di serie.

#### Anche un array è un oggetto
Un array è un oggetto a tutti gli effetti, quindi si serializza in un colpo solo — a patto che il tipo degli elementi sia serializzabile. Vale anche per le collezioni.

```java
Prodotto[] catalogo = { p1, p2, p3 };
oos.writeObject(catalogo);                              // un solo writeObject
Prodotto[] letto = (Prodotto[]) ois.readObject();       // un solo readObject + cast

ArrayList<Prodotto> lista = new ArrayList<>();
oos.writeObject(lista);                                 // idem per le collezioni
```

#### "File binario" non è sinonimo di "serializzazione"
Sono due cose diverse e le tracce le distinguono. Se una traccia chiede un **file binario** e tu consegni una serializzazione (o viceversa), il file prodotto ha un formato che il test non riconosce.

| | File binario "crudo" | Serializzazione di oggetti |
| :--- | :--- | :--- |
| Classi | `FileInputStream` / `FileOutputStream`, o `DataInputStream` / `DataOutputStream` | `ObjectInputStream` / `ObjectOutputStream` |
| Cosa scrivi | byte, `int`, `double`, `String` uno alla volta (`writeInt`, `writeDouble`, `writeUTF`) | l'oggetto intero, in un colpo (`writeObject`) |
| La classe deve essere `Serializable` | No | **Sì**, altrimenti `NotSerializableException` |
| Formato del file | lo decidi tu, campo per campo | formato interno della JVM, non leggibile a mano |
| Come si rilegge | nello **stesso ordine** in cui hai scritto | `readObject()` + cast |

`DataOutputStream` è la via di mezzo che le tracce chiamano "file binario": scrive tipi primitivi in formato binario portabile, senza coinvolgere la serializzazione.

```java
try (DataOutputStream out = new DataOutputStream(new FileOutputStream("magazzino.bin"))) {
    out.writeUTF("Smartphone");   // String
    out.writeInt(12);             // int
    out.writeDouble(599.99);      // double
}
try (DataInputStream in = new DataInputStream(new FileInputStream("magazzino.bin"))) {
    String nome = in.readUTF();       // stesso ordine della scrittura, obbligatoriamente
    int quantita = in.readInt();
    double prezzo = in.readDouble();
}
```

#### Un file di record: scrivere in coda, leggere fino a fine file, chiudere nel `finally`
È la forma tipica dell'esercizio "file binario": una classe con il percorso, un metodo che **aggiunge** un record in coda e uno che **rilegge tutto**. Racchiude quattro regole che le tracce verificano.

```java
import java.io.*;

class Registro {
    private String percorso;

    public Registro(String percorso) {
        this.percorso = percorso;
    }

    // Scrive in coda; la chiusura è nel finally (forma imposta da molte tracce).
    public void aggiungi(String nome, int ora, double temp) throws IOException {
        if (ora < 0 || ora > 23) {                       // 1. si valida PRIMA di aprire il file
            throw new IllegalArgumentException("Ora non valida: " + ora);
        }
        DataOutputStream out = null;                     // 2. dichiarato FUORI dal try
        try {
            out = new DataOutputStream(new FileOutputStream(percorso, true));   // 3. true = in coda
            out.writeUTF(nome);                          // il record: stringa, int, double...
            out.writeInt(ora);
            out.writeDouble(temp);                       // ...sempre in QUESTO ordine
        } finally {
            if (out != null) {                           // 4. se l'apertura è fallita, out è ancora null
                out.close();                             // close() dichiara IOException
            }
        }
    }

    public double massima() throws IOException {
        DataInputStream in = null;
        double max = Double.NEGATIVE_INFINITY;
        try {
            in = new DataInputStream(new FileInputStream(percorso));
            while (true) {                               // quanti record? non si sa: si legge finché ce ne sono
                in.readUTF();                            // si leggono TUTTI i campi, anche quelli che non servono
                in.readInt();
                double t = in.readDouble();
                if (t > max) max = t;
            }
        } catch (EOFException fine) {
            // fine del file: è l'uscita normale dal ciclo, non un errore
        } finally {
            if (in != null) {
                in.close();
            }
        }
        return max;
    }
}
```

**Le quattro regole.**
1. **Validare prima di aprire.** `new FileOutputStream(percorso)` svuota il file subito. Se il controllo (`ora` fuori da 0-23) sta *dopo* l'apertura, un record rifiutato lascia comunque il file vuoto, mentre la traccia dice "il file resta invariato".
2. **`true` per accodare.** Senza, ogni `aggiungi` cancella i record precedenti. Con 3 record da `writeUTF("Messina")` + `writeInt` + `writeDouble`, il file pesa 63 byte (21 a record: 2 + 7 + 4 + 8).
3. **Fine file = `EOFException`.** `DataInputStream` e `ObjectInputStream` non hanno `hasNext()` e **non restituiscono mai `null` o `-1`**: quando i dati finiscono, `readUTF`, `readInt`, `readDouble` e `readObject` **lanciano `EOFException`**. Il ciclo è `while (true)` e il `catch (EOFException)` è l'uscita. Un file vuoto lancia l'eccezione al primo giro: il risultato è quello iniziale (`NEGATIVE_INFINITY`, lista vuota, `0`), non un errore.
4. **Ordine di lettura = ordine di scrittura.** Se il record è `UTF, int, double`, leggi `readUTF, readInt, readDouble`, anche se di un campo non ti serve il valore: lo leggi e lo scarti, altrimenti il record dopo è sfalsato.

**Lo stesso schema per gli oggetti.** Se scrivi più oggetti con `writeObject` uno dopo l'altro, li rileggi con un ciclo `while (true)` e `catch (EOFException)`; `readObject()` dichiara **anche** `ClassNotFoundException`, che si cattura a parte. `readObject()` **non** restituisce `null` a fine file: `while ((x = ois.readObject()) != null)` non termina mai bene.

```java
ArrayList<String> letti = new ArrayList<>();
try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("dati.dat"))) {
    while (true) {
        letti.add((String) in.readObject());     // cast: readObject restituisce Object
    }
} catch (EOFException fine) {
    // fine: uscita normale
} catch (ClassNotFoundException e) {
    System.out.println("classe sconosciuta");
} catch (IOException e) {
    System.out.println("errore di I/O");         // dopo EOFException: è la sua superclasse, va DOPO
}
```

**Tre convenzioni diverse per dire "è finito".** Vanno sapute a memoria, perché ogni flusso ha la sua:

| Flusso | Come segnala la fine | Come si scrive il ciclo |
|---|---|---|
| `BufferedReader.readLine()` | restituisce `null` | `while ((riga = r.readLine()) != null)` |
| `InputStream.read()` / `read(buffer)` | restituisce `-1` | `while ((n = in.read(buf)) != -1)` |
| `DataInputStream` (`readUTF`/`readInt`/`readDouble`), `ObjectInputStream.readObject()` | **lancia** `EOFException` | `while (true) { ... } catch (EOFException e) { }` |

### Serializzazione **attraverso la Rete**: lo stesso oggetto, un altro tubo
Questo è il punto in cui la serializzazione viene sbagliata più spesso, e l'errore non è sintattico: è di **destinazione**.

Riguarda la frase chiave del Pattern Decorator: `ObjectOutputStream` non sa niente di dove finiranno i byte. Sa solo trasformare un oggetto in byte e passarli allo stream che gli hai dato in pasto. Quello stream decide la destinazione:

```java
new ObjectOutputStream(new FileOutputStream("dati.dat"));   // i byte finiscono SU DISCO
new ObjectOutputStream(socket.getOutputStream());           // i byte finiscono IN RETE
```

Le due righe sono quasi identiche a vedersi, e questa somiglianza è una trappola: **se la traccia dice "invia l'oggetto al server" e tu costruisci l'`ObjectOutputStream` su un `FileOutputStream`, hai scritto un programma che serializza perfettamente e non comunica con nessuno.** Non è un dettaglio da qualche punto: è aver risolto un problema diverso da quello richiesto.

La regola da fissare: **il verbo della traccia ti dice quale stream avvolgere.** "Salva su file" → `FileOutputStream`. "Invia al server" / "trasmetti" / "spedisci sulla connessione" → `socket.getOutputStream()`.

#### Il ciclo completo lato client
Uno solo schema, da sapere a memoria: connetti → avvolgi → scrivi → leggi → cast.

```java
import java.io.*;
import java.net.*;

// 1. La classe da spedire DEVE essere serializzabile: senza 'implements Serializable'
//    il writeObject lancia NotSerializableException a runtime (compila benissimo!).
class Persona implements Serializable {
    // Nome ESATTO, tipo ESATTO: static final long serialVersionUID.
    // Una lettera diversa (serialversionUID, serialVersionUid) compila senza un fiato
    // e diventa un campo qualunque, inerte: la protezione di versione sparisce.
    private static final long serialVersionUID = 1L;

    private String nome;
    private String cognome;

    public Persona(String nome, String cognome) {
        this.nome = nome;
        this.cognome = cognome;
    }

    public String getNome()    { return nome; }
    public String getCognome() { return cognome; }

    @Override
    public String toString() {
        return "Persona[" + nome + " " + cognome + "]";
    }
}

class Client {

    public Persona invia(Persona p) {
        // try-with-resources: Socket e stream sono AutoCloseable, si chiudono da soli.
        try (Socket socket = new Socket("127.0.0.1", 5555);

             // 2. L'OUTPUT si apre SEMPRE PER PRIMO (vedi la trappola dell'header, sotto).
             ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
             ObjectInputStream  in  = new ObjectInputStream(socket.getInputStream())) {

            // 3. Invio: l'oggetto diventa byte e viaggia sulla connessione.
            out.writeObject(p);
            out.flush();                      // spinge fuori i byte rimasti nel buffer

            // 4. Attesa e ricostruzione: readObject() restituisce Object, il cast è obbligatorio.
            return (Persona) in.readObject();

        } catch (IOException | ClassNotFoundException e) {
            // ClassNotFoundException: i byte sono arrivati ma la classe non esiste qui.
            return null;
        }
    }
}
```

#### Il lato server, per capire cosa succede dall'altra parte
```java
try (ServerSocket server = new ServerSocket(5555)) {
    while (true) {
        try (Socket client = server.accept();
             ObjectOutputStream out = new ObjectOutputStream(client.getOutputStream());
             ObjectInputStream  in  = new ObjectInputStream(client.getInputStream())) {

            Persona ricevuta = (Persona) in.readObject();   // deserializza
            System.out.println("Arrivata: " + ricevuta);
            out.writeObject(ricevuta);                      // rimanda indietro
            out.flush();
        }
    }
}
```

> **Il punto concettuale.** L'oggetto che torna indietro **non è lo stesso oggetto** che hai spedito: è una copia ricostruita dai byte. `inviata == ricevuta` è `false`, mentre i campi coincidono. È la prova che la serializzazione è avvenuta davvero — ed è esattamente ciò che un test può controllare per distinguere una vera trasmissione da una simulazione locale.

#### File contro Rete, in una tabella
| | Serializzazione su **file** | Serializzazione su **rete** |
| :--- | :--- | :--- |
| Stream avvolto in uscita | `new FileOutputStream("dati.dat")` | `socket.getOutputStream()` |
| Stream avvolto in ingresso | `new FileInputStream("dati.dat")` | `socket.getInputStream()` |
| Chi apre il canale | nessuno: basta il percorso | `new Socket(host, porta)` lato client, `accept()` lato server |
| Quando si legge | quando vuoi, anche fra giorni | subito: c'è qualcuno dall'altra parte che aspetta |
| Se sbagli mezzo | il file compare nella cartella | non arriva niente al server |

#### Trappole specifiche della serializzazione su socket
- **La trappola dell'header (deadlock all'apertura).** Il costruttore di `ObjectOutputStream` scrive subito un'intestazione sullo stream; quello di `ObjectInputStream` **si blocca** finché non legge l'intestazione dell'altro capo. Se client e server aprono entrambi l'input per primo, restano bloccati per sempre, senza errori e senza output. **Apri sempre l'`ObjectOutputStream` per primo, su entrambi i lati.**
- **`flush()` dopo `writeObject`.** Senza, i byte possono restare nel buffer locale e il destinatario aspetta un messaggio che non è mai partito.
- **La stessa classe deve esistere su entrambi i lati**, con lo stesso nome e lo stesso `serialVersionUID`. Altrimenti `ClassNotFoundException` o `InvalidClassException`.
- **`transient` viaggia come valore di default.** Un campo `transient` non viene serializzato: dall'altra parte arriva `null` (oggetti) o `0` (numeri). Utile per le password, letale se ci metti dentro un dato che serve.
- **Non chiudere lo stream se devi ancora leggere.** `out.close()` chiude anche il socket sottostante: la risposta non arriverà mai. Usa `flush()`, e lascia che sia il `try-with-resources` a chiudere tutto alla fine.

### Best Practices & Errori Comuni
- **`while ((x = (Libro) ois.readObject()) != null)`.** `readObject()` non restituisce `null` a fine file: lancia `EOFException`. Il ciclo è `while (true)` con `catch (EOFException)`.
- **`new FileOutputStream(percorso)` senza `true` quando la traccia dice "in coda".** Ogni scrittura sovrascrive il file. E il file si svuota già all'apertura, quindi un controllo fatto dopo non protegge il vecchio contenuto.
- **Chiudere i flussi nel try-with-resources quando la traccia dice `finally`**, o dichiararli dentro il `try`. La forma è nel Livello 3 §5 e nel `Registro` qui sopra: dichiarati fuori, a `null`, `if (x != null) x.close()` nel `finally`.
- **`catch (IOException e)` prima di `catch (EOFException e)`.** Non compila (`exception EOFException has already been caught`): `EOFException` è una `IOException`, il catch più specifico va per primo.
- **Il Memory Leak del Buffer non svuotato:** Se decidi di ignorare il `try-with-resources` e gestisci gli stream manualmente senza chiamare l'indispensabile metodo `.close()` (o almeno `.flush()`) su scrittori come `PrintWriter` o `BufferedWriter`, i dati rimarranno intrappolati nella RAM e il file sul disco risulterà tristemente vuoto. Il `close()` è l'atto che forza lo svuotamento fisico sul disco.
- **La Trappola della `InvalidClassException`:** Come anticipato, se serializzi un oggetto su file, poi chiudi il programma, aggiungi una nuova variabile alla sua classe e riprovi a leggere il vecchio file di salvataggio, il programma esploderà lanciando una `InvalidClassException`. La JVM, per sicurezza, ricalcola un ID basato sulla nuova struttura della classe e, vedendo che non corrisponde a quello salvato nel file, blocca la procedura temendo una compromissione dei dati. Metti *sempre* un `serialVersionUID` statico.
- **L'Errore della Path Relativa:** In un'applicazione standard, passare semplicemente `"documento.txt"` significa dire al programma di cercare il file nella sua *Current Working Directory* (la cartella da cui è stato lanciato il programma, tipicamente la root del progetto). Attenzione che non coincide necessariamente con la cartella dove si trova il file `.java` sorgente!

---

## 3. Interfacce Grafiche (GUI) con Swing

### Teoria Fondamentale: Architettura Swing e il pattern MVC
L'interazione tramite console è limitante. Java offre il framework **Swing** (`javax.swing`), basato su **AWT** (`java.awt`), per creare interfacce moderne. Swing adotta il pattern **MVC (Model-View-Controller)**:
- **Model:** I dati e la logica (es. un oggetto `Prodotto`).
- **View:** La rappresentazione visiva (es. `JFrame`, `JLabel`).
- **Controller:** Il codice che gestisce gli eventi e aggiorna il Model/View (es. `ActionListener`).

Swing è **single-threaded**. Tutte le modifiche grafiche devono avvenire nell'**EDT (Event Dispatch Thread)**. Se blocchi l'EDT con un calcolo pesante, l'interfaccia "congela".

### Componenti e Gerarchia
Un'interfaccia è una gerarchia di contenitori (`Container`) e componenti (`JComponent`):
- **`JFrame`:** La finestra principale. I componenti non vanno aggiunti direttamente al frame, ma al suo **Content Pane** (`frame.getContentPane()`), che funge da tela principale.
- **`JPanel`:** Contenitore intermedio fondamentale. Permette di raggruppare componenti (es. un pannello di bottoni) prima di inserirli nel frame.
- **Componenti Standard:** `JButton` (click), `JLabel` (testo/icone), `JTextField` (input singola riga), `JTextArea` (testo multiriga).

### I Layout Manager (Gestione dello Spazio)
Java usa i Layout Manager per disporre i componenti in modo automatico e responsivo (basato sui **pixel**):
1. **`BorderLayout`:** (Default per `JFrame`). Divide lo spazio in 5 regioni: `NORTH`, `SOUTH`, `EAST`, `WEST` e `CENTER`. Il `CENTER` è l'area più importante: si espande per occupare tutto lo spazio residuo.
2. **`FlowLayout`:** (Default per `JPanel`). Dispone i componenti in riga, uno dopo l'altro. Quando finisce lo spazio, va a capo.
3. **`GridLayout`:** Crea una griglia rigida di celle di dimensioni uguali. Ideale per tastiere numeriche o scacchiere.

---

## 4. Gestione degli Eventi e Dialoghi Utente

### Il Pattern Observer: Sorgenti e Ascoltatori
Il cuore delle GUI è la **Programmazione Guidata dagli Eventi (Event-Driven)**.
- **Event Source:** Il componente che "lancia" (fires) l'evento (es. un `JButton`).
- **Event Listener:** L'oggetto che "cattura" l'evento e reagisce. Deve implementare un'interfaccia specifica come `ActionListener`.

*Best Practice:* Invece di far implementare l'ascoltatore alla classe principale, usa **Classi Interne (Inner Classes)** o **Classi Anonime**. Questo mantiene il codice pulito e permette all'ascoltatore di accedere facilmente alle variabili private della GUI.

### Dialoghi Rapidi: `JOptionPane`
Per interagire velocemente con l'utente (mostrare errori o chiedere conferme) senza creare nuovi frame, si usa `JOptionPane`:
- `JOptionPane.showMessageDialog(parent, "Messaggio")`: Mostra un avviso.
- `JOptionPane.showConfirmDialog(...)`: Chiede "Sì/No/Annulla".

### Sintassi ed Esempio Completo (Pannello Domotico)
Questo esempio mostra come gestire più componenti e stati diversi in un'unica interfaccia.

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class PannelloDomotico extends JFrame {
    private JLabel statusLuce;
    private boolean luceAccesa = false;

    public PannelloDomotico() {
        super("Smart Home Control");
        setSize(350, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        Container contentPane = getContentPane();
        contentPane.setLayout(new BorderLayout(10, 10));

        // Intestazione
        JLabel titolo = new JLabel("Controllo Luci Soggiorno", SwingConstants.CENTER);
        titolo.setFont(new Font("Arial", Font.BOLD, 16));
        contentPane.add(titolo, BorderLayout.NORTH);

        // Centro: Stato attuale
        statusLuce = new JLabel("STATO: SPENTA", SwingConstants.CENTER);
        statusLuce.setOpaque(true);
        statusLuce.setBackground(Color.DARK_GRAY);
        statusLuce.setForeground(Color.WHITE);
        contentPane.add(statusLuce, BorderLayout.CENTER);

        // Sud: Bottoni
        JPanel pnlBottoni = new JPanel(new FlowLayout());
        JButton btnToggle = new JButton("Accendi/Spegni");
        JButton btnInfo = new JButton("Info Sistema");

        btnToggle.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                luceAccesa = !luceAccesa;
                if (luceAccesa) {
                    statusLuce.setText("STATO: ACCESA");
                    statusLuce.setBackground(Color.YELLOW);
                    statusLuce.setForeground(Color.BLACK);
                } else {
                    statusLuce.setText("STATO: SPENTA");
                    statusLuce.setBackground(Color.DARK_GRAY);
                    statusLuce.setForeground(Color.WHITE);
                }
            }
        });

        btnInfo.addActionListener(e -> {
            JOptionPane.showMessageDialog(this, "Sistema Domotico v1.0\nStato Connessione: OK");
        });

        pnlBottoni.add(btnToggle);
        pnlBottoni.add(btnInfo);
        contentPane.add(pnlBottoni, BorderLayout.SOUTH);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new PannelloDomotico().setVisible(true);
        });
    }
}
```

---

## 5. Oltre Swing: L'Evoluzione con JavaFX

### Cos'è JavaFX?
JavaFX è la piattaforma moderna che sostituisce Swing. Mentre Swing disegna i componenti via software, JavaFX sfrutta l'**accelerazione hardware (GPU)** tramite uno **Scene Graph**.

### Architettura: Stage, Scene e Node
Per capire JavaFX, usa la metafora del teatro:
1. **Stage (Palcoscenico):** Rappresenta la finestra (il `JFrame` di Swing).
2. **Scene (Scena):** Il contenuto visibile. Una finestra può cambiare scena (es. da Menu a Gioco).
3. **Node (Nodo):** Ogni elemento della UI (bottoni, immagini, layout) è un nodo nell'albero della scena.

### Separazione con FXML e CSS
A differenza di Swing, JavaFX permette di separare nettamente l'estetica dalla logica:
- **FXML:** Un file XML per definire la struttura della UI.
- **CSS:** Supporto completo ai fogli di stile per definire colori e bordi.
- **Controller:** Classe Java che gestisce solo il comportamento (metodi `@FXML`).

> **Swing vs JavaFX: Quando scegliere?**
> Scegli **Swing** per applicazioni legacy o semplici strumenti interni dove la velocità di sviluppo conta più dell'estetica. Scegli **JavaFX** per applicazioni moderne che richiedono grafiche fluide, animazioni, CSS e una separazione professionale tra UI e logica.