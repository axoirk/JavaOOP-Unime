# Livello 3: OOP Avanzata e Gestione degli Errori

## 1. Ereditarietà e L'Uso della Keyword `super`

### Cos'è l'Ereditarietà? (La Relazione "IS-A")
L'**Ereditarietà** è il meccanismo che permette di creare una nuova classe (Sottoclasse) basata su una classe già esistente (Superclasse). 
- **Teoria:** Pensa all'ereditarietà in biologia. Un *Cane* eredita le caratteristiche base di un *Animale* (respirare, mangiare), ma poi aggiunge comportamenti propri (abbaiare, scodinzolare). Si dice che c'è una relazione **"is-a" (è un)**: il Cane *è un* Animale.
- **Perché usarla:** Per evitare di fare copia-incolla dello stesso codice in mille classi diverse. Se tutte le entità (Studenti, Professori, Segretari) hanno un `nome` e una `dataDiNascita`, scrivi quelle variabili e i getter/setter una sola volta in una Superclasse `Persona`.

---

### Lo scoglio principale: Che cos'è `super` e quando si usa?
La parola chiave `super` è semplicemente un **riferimento alla classe padre**. È come se dicessi a Java: *"Non guardare me (la classe in cui ti trovi ora), ma guarda la classe da cui ho ereditato."*

Si usa principalmente in due contesti fondamentali. Non bisogna confonderli:

#### Caso A: `super(...)` - Costruire le fondamenta (Il Costruttore)
**Teoria:** Quando crei un oggetto `Cane`, in memoria deve prima essere costruita la sua parte di `Animale` (le sue "fondamenta"). Se la classe padre ha un costruttore che *pretende* dei parametri (es. il `nome`), la sottoclasse è **obbligata** a fornirglieli. 
**Regola d'oro:** Lo si fa invocando `super(parametro)` come **primissima istruzione obbligatoria** nel costruttore della sottoclasse.

**Esempio Pratico:**
```java
public class Animale {
    protected String nome;

    // Costruttore del Padre: pretende un nome per nascere
    public Animale(String nome) {
        this.nome = nome;
    }
}

public class Cane extends Animale {
    private String razza;

    // Costruttore del Figlio: richiede nome e razza
    public Cane(String nome, String razza) {
        // 1. DEVI chiamare il costruttore del padre e passargli il nome. 
        // Se non metti super(), il compilatore si arrabbia!
        super(nome); 
        
        // 2. Solo DOPO aver costruito l'Animale, gestisci i dati specifici del Cane
        this.razza = razza;
    }
}
```

#### Caso B: `super.nomeMetodo()` - Aggiungere funzionalità, non cancellarle
**Teoria:** Spesso, in una sottoclasse, fai l'**Override** (sovrascrivi) di un metodo del padre perché vuoi cambiarne il comportamento. Ma cosa succede se vuoi *aggiungere* qualcosa al comportamento originale, senza buttare via il codice che il padre aveva già scritto? 
Usi `super.metodo()` per dire: *"Esegui la logica base che aveva scritto mio padre, e subito dopo ci aggiungo io il resto"*.

**Esempio Pratico:**
```java
public class Dipendente {
    public void lavora() {
        System.out.println("Timbra il cartellino e inizia a lavorare.");
    }
}

public class Manager extends Dipendente {
    
    @Override
    public void lavora() {
        // Voglio che il Manager timbri il cartellino come tutti i dipendenti...
        super.lavora(); 
        
        // ...ma poi fa il suo lavoro specifico!
        System.out.println("Organizza una riunione con il team.");
    }
}
```
In questo caso, chiamando `manager.lavora()`, stamperai ENTRAMBE le frasi. Se non avessi messo `super.lavora()`, il Manager avrebbe solo organizzato la riunione senza timbrare il cartellino!

---

## 2. Classi Astratte e Polimorfismo

### Teoria Fondamentale
Una **Classe Astratta** è una classe che non può essere istanziata direttamente. Serve come modello per altre classi. Può contenere **metodi astratti** (senza corpo) che le sottoclassi *devono* implementare.

Il **Polimorfismo** permette a un riferimento di una superclasse di puntare a un oggetto di una sottoclasse, decidendo quale metodo eseguire solo a tempo di esecuzione (Runtime).

### Esempio: Calcolo Volumi (Classi Astratte)
```java
public abstract class Solido {
    public abstract double calcolaVolume();
}

public class Cubo extends Solido {
    private double lato;
    public Cubo(double l) { this.lato = l; }

    @Override
    public double calcolaVolume() {
        return Math.pow(lato, 3);
    }
}
```

---

## 3. Le Interfacce (`interface`)

### Teoria Fondamentale: Il Ruolo dei Dispositivi
Un'**Interfaccia** definisce un contratto di comportamento. Mentre l'ereditarietà definisce *cosa un oggetto è*, l'interfaccia definisce *cosa un oggetto sa fare*.

**Esempio Teorico: Dispositivi Elettronici**
Molti dispositivi diversi possono essere "accesi" o "spenti". Non importa se è una `Lampadina`, un `Computer` o un `Tostapane`: se implementano l'interfaccia `Accendibile`, garantiscono la presenza dei metodi `accendi()` e `spegni()`.

### Sintassi ed Esempi di Codice
```java
public interface Accendibile {
    void accendi(); // implicitamente public abstract
    void spegni();
}

public class Televisore implements Accendibile {
    @Override
    public void accendi() {
        System.out.println("TV Accesa: Benvenuti!");
    }

    @Override
    public void spegni() {
        System.out.println("TV Spenta: Arrivederci.");
    }
}
```

---

## 4. Ordinamento: Classe `Collections` e Interfaccia `Comparable`

### Il problema dell'ordinamento
Immagina di avere un `ArrayList<Studente>`. Se provi a chiamare il metodo di sistema `Collections.sort(listaStudenti)`, il compilatore Java andrà in panico e genererà un errore. Perché? Perché Java sa come ordinare i numeri (crescente) o le stringhe (alfabetico), ma non ha idea di cosa renda uno "Studente" più grande o più piccolo di un altro. Va ordinato per età? Per media voti? Per matricola?

### L'Interfaccia `Comparable`
Per risolvere il problema, la tua classe deve dichiarare nativamente il suo criterio di "Ordinamento Naturale" (Natural Ordering). Lo fa implementando l'interfaccia di sistema **`Comparable<T>`** che fa parte del package `java.lang`.

Questa interfaccia ti obbliga a implementare un solo metodo magico: `compareTo(T altroOggetto)`.

### Regole matematiche del `compareTo`
Il metodo `compareTo` confronta l'oggetto corrente (`this`) con l'oggetto passato come parametro (`altroOggetto`), e deve restituire un numero intero seguendo questa convenzione universale:
1. **Ritorna un numero POSITIVO (> 0)** se `this` è *maggiore* di `altroOggetto` (quindi `this` va posizionato DOPO nell'ordinamento).
2. **Ritorna un numero NEGATIVO (< 0)** se `this` è *minore* di `altroOggetto` (quindi `this` va posizionato PRIMA).
3. **Ritorna ZERO (0)** se `this` e `altroOggetto` sono considerati uguali ai fini dell'ordinamento.

### Sintassi ed Esempio Completo
Nel seguente esempio vogliamo ordinare gli studenti per **Media** in ordine Decrescente (chi ha media più alta viene per primo). Se la media è identica, usiamo la **Matricola** come spareggio in ordine Crescente (la matricola più piccola viene per prima).

```java
import java.util.*;

// Notare l'uso dei Generics <Studente> per evitare casting manuali
public class Studente implements Comparable<Studente> {
    private int matricola;
    private double media;

    public Studente(int matricola, double media) {
        this.matricola = matricola;
        this.media = media;
    }

    @Override
    public int compareTo(Studente altroStudente) {
        // Criterio 1: Media DECRESCENTE (Più alta viene prima)
        if (this.media > altroStudente.media) {
            return -1; // this ha media più alta, quindi è "più piccolo/viene prima" nell'ordine decrescente
        }
        if (this.media < altroStudente.media) {
            return 1;  // this ha media più bassa, viene dopo
        }
        
        // Criterio 2: Se la media è identica, spareggio per Matricola CRESCENTE
        // Suggerimento pro: puoi usare Integer.compare per i tipi primitivi
        return Integer.compare(this.matricola, altroStudente.matricola);
    }
    
    @Override
    public String toString() {
        return "Mat:" + matricola + " Media:" + media;
    }
}

// Classe Test
class GestoreOrdinamento {
    public static void main(String[] args) {
        List<Studente> classe = new ArrayList<>();
        classe.add(new Studente(3, 28.0));
        classe.add(new Studente(1, 30.0));
        classe.add(new Studente(2, 30.0));

        // Ora che Studente è Comparable, possiamo usare la classe di utility Collections!
        Collections.sort(classe);

        // Risultato stampato:
        // Mat:1 Media:30.0 (Viene prima per parità di media e matricola più bassa)
        // Mat:2 Media:30.0
        // Mat:3 Media:28.0
        for(Studente s : classe) {
            System.out.println(s);
        }
    }
}
```

---

## 5. Gestione delle Eccezioni

### Teoria Fondamentale
Le eccezioni sono eventi anomali che interrompono il normale flusso del programma. Java usa un sistema basato su oggetti per gestire questi errori: quando qualcosa va storto viene *creato* un oggetto eccezione e *lanciato*; il flusso normale si interrompe e la JVM risale la pila delle chiamate cercando qualcuno che lo catturi. Se nessuno lo cattura, il programma termina.

```text
Throwable
├── Error                 → guasti della JVM (OutOfMemoryError). NON si catturano.
└── Exception             → CHECKED: il compilatore ti obbliga a gestirle
    ├── IOException, FileNotFoundException, SQLException, InterruptedException...
    └── RuntimeException  → UNCHECKED: il compilatore non dice niente
        ├── NullPointerException, ArithmeticException,
        └── ArrayIndexOutOfBoundsException, NumberFormatException...
```

- **Checked Exceptions**: tutto ciò che discende da `Exception` **ma non** da `RuntimeException`. Rappresentano guasti esterni prevedibili (il file non c'è, la rete cade). Il compilatore pretende che tu faccia una delle due cose: catturarle (`try`/`catch`) oppure dichiarare che le propaghi (`throws`). Non esiste una terza via.
- **Unchecked Exceptions**: discendono da `RuntimeException`. Rappresentano errori di programmazione (puntatore nullo, indice fuori range, divisione per zero). Il compilatore le ignora: si propagano da sole fino al `main` e fanno esplodere il programma se nessuno le ferma.

**La regola operativa che serve all'esame:** se una traccia dice *"il metodo dichiara di poter propagare al chiamante un'eccezione controllata"*, sta chiedendo `throws` nella firma. Se dice *"l'eccezione raggiunge il chiamante senza essere dichiarata"*, sta chiedendo una `RuntimeException`.

### Le cinque parole chiave
Sono cinque e vanno sapute distinguere a memoria, perché le tracce le chiedono per nome.

| Keyword | Dove si scrive | Cosa fa |
| :--- | :--- | :--- |
| `try` | blocco | delimita il codice sorvegliato |
| `catch` | dopo `try` | intercetta un tipo di eccezione e la gestisce |
| `finally` | dopo `try`/`catch` | **viene eseguito sempre**: sia in caso di successo, sia dopo un `catch`, sia mentre un'eccezione sta uscendo dal metodo |
| `throw` | dentro il corpo | **lancia** un'istanza: `throw new IOException("messaggio");` |
| `throws` | nella **firma** del metodo | **dichiara** che il metodo può propagare quel tipo al chiamante |

> **`throw` contro `throws`: la confusione più comune.** `throw` è un'azione, prende **un oggetto** e lo lancia adesso. `throws` è una dichiarazione, prende **uno o più tipi**, sta nella firma e non lancia niente — avvisa soltanto il chiamante. Una `s` di differenza, due significati che non si toccano.

### `finally`: perché le tracce lo impongono
`finally` viene eseguito **sempre**, anche quando dal `try` si esce con un `return` o mentre un'eccezione sta risalendo. Il suo scopo naturale è la pulizia delle risorse (chiudere file e socket), e per questo è il posto giusto per il codice che deve avvenire in ogni scenario possibile.

Quando una traccia dice *"la stampa deve trovarsi dentro il blocco `finally`"*, sta verificando che tu abbia capito questa proprietà: **una stampa collocata altrove può produrre esattamente lo stesso output e valere comunque zero punti su quel requisito.** Il risultato a schermo non dimostra niente sulla struttura, ed è la struttura che viene valutata.

Ordine di esecuzione, da tenere a mente:

```java
try {
    System.out.println("1");
    throw new RuntimeException("boom");
} catch (RuntimeException e) {
    System.out.println("2");     // eseguito perché il tipo corrisponde
} finally {
    System.out.println("3");     // eseguito comunque, per ultimo
}
// stampa: 1, 2, 3
```

Se il `catch` non cattura quel tipo, l'ordine diventa `1`, `3`, poi l'eccezione esce dal metodo: **il `finally` gira prima che l'eccezione se ne vada.**

### Esempio completo: tutte e cinque le parole chiave in un metodo
È lo schema esatto chiesto in più appelli: un metodo che si comporta in modo diverso a seconda del parametro, con la stampa **dentro `finally`**, uno solo per tutti i casi.

```java
import java.io.IOException;

class Gestore {

    // 'throws Exception' = dichiarazione (checked propagata al chiamante).
    public void verifica(int n) throws Exception {
        // Inizializzato subito: il compilatore pretende che 'messaggio' abbia
        // un valore su OGNI cammino che arriva al finally.
        String messaggio = "no eccezioni";
        try {
            if (n == 0) {
                // 'throw' = azione. Eccezione generica, catturata qui sotto.
                throw new Exception("errore generico");
            } else if (n == 1) {
                throw new IOException("errore di I/O");
            }
        } catch (IOException e) {
            // Conversione checked -> unchecked: la RuntimeException NON va
            // dichiarata in 'throws' e raggiunge comunque il chiamante.
            messaggio = "eccezione runtime";
            System.out.println(messaggio);   // stampa prima di uscire
            throw new RuntimeException(messaggio);
        } catch (Exception e) {
            // Nota l'ordine: IOException PRIMA di Exception. Il contrario non compila.
            messaggio = "eccezione generica";
        } finally {
            // Unico punto di stampa per i casi che escono normalmente.
            if (n != 1) {
                System.out.println(messaggio);
            }
        }
    }
}
```

Due dettagli che valgono punti:
- **L'ordine dei `catch` va dal più specifico al più generale.** `catch (Exception e)` prima di `catch (IOException e)` non compila: `exception IOException has already been caught`.
- **Un `catch` multiplo** si scrive `catch (IOException | SQLException e)` quando la gestione è identica.

### `throws` e override: si può restringere, mai allargare
Quando una sottoclasse riscrive un metodo, la clausola `throws` del metodo riscritto può dichiarare **meno** eccezioni controllate di quello della superclasse, o nessuna — **mai di più**, e mai un tipo più generale.

```java
class Base {
    public void leggi() throws IOException { }
}

class Derivata extends Base {
    public void leggi() { }                              // OK: zero eccezioni, è un restringimento
}

class Altra extends Base {
    public void leggi() throws FileNotFoundException { } // OK: sottotipo di IOException
}

class Rotta extends Base {
    public void leggi() throws Exception { }             // NON COMPILA: Exception è più generale
}
```

La ragione è il polimorfismo: chi usa un `Base` ha scritto il proprio `catch` sulla base della firma di `Base`, e la sostituzione con una sottoclasse non deve poter far arrivare eccezioni impreviste. Le **unchecked** restano fuori da questa regola: si propagano comunque, dichiarate o no.

### Eccezioni personalizzate (custom)
Si creano estendendo una classe della gerarchia. La scelta della superclasse decide tutto il comportamento:

```java
// CHECKED: estende Exception. Chi la usa DEVE catturarla o dichiararla.
class SaldoInsufficienteException extends Exception {
    public SaldoInsufficienteException(String messaggio) {
        super(messaggio);   // il messaggio va passato al costruttore della superclasse
    }
}

// UNCHECKED: estende RuntimeException. Si propaga da sola, nessun obbligo.
class CodiceNonValidoException extends RuntimeException {
    public CodiceNonValidoException(String messaggio) {
        super(messaggio);
    }
}

class ContoCorrente {
    private double saldo;

    public ContoCorrente(double saldo) { this.saldo = saldo; }

    // Checked: il 'throws' è obbligatorio, il compilatore lo pretende.
    public void preleva(double importo) throws SaldoInsufficienteException {
        if (importo > saldo) {
            throw new SaldoInsufficienteException("saldo insufficiente: " + saldo);
        }
        saldo -= importo;
    }
}
```

Il messaggio si recupera con `e.getMessage()`. **Se una traccia chiede un messaggio specifico, quel messaggio deve stare nel costruttore**: `throw new Exception()` senza argomenti compila benissimo e perde il requisito senza che nulla lo segnali.

### `try-with-resources`: il `finally` scritto dal compilatore
Quando il `finally` serve solo a chiudere risorse, esiste una forma più sicura. Ogni oggetto dichiarato fra le parentesi tonde del `try` viene chiuso automaticamente all'uscita del blocco, in ogni scenario, in ordine inverso di apertura.

```java
try (BufferedReader in = new BufferedReader(new FileReader("dati.txt"))) {
    System.out.println(in.readLine());
}   // in.close() chiamato qui, sempre, anche se readLine() esplode
catch (IOException e) {
    System.err.println("errore: " + e.getMessage());
}
```
Funziona con qualunque tipo che implementi `AutoCloseable`: stream, `Socket`, `ServerSocket`, `DatagramSocket`, `Connection` JDBC. **Attenzione:** se la traccia impone esplicitamente un blocco `finally`, il `try-with-resources` non lo sostituisce agli occhi del correttore — la parola chiave richiesta deve comparire. La forma da scrivere in quel caso è nella sezione seguente.

### `finally` che chiude i flussi a mano
Quando la traccia dice *"la chiusura dei flussi deve avvenire nel blocco `finally`"*, il try-with-resources non basta: serve la forma classica. È sempre la stessa, in **quattro passi**, e ognuno evita un errore preciso.

```java
import java.io.*;

class Lettore {
    public String primaRiga(String percorso) throws IOException {
        BufferedReader in = null;                        // 1. dichiarato FUORI dal try, a null
        try {
            in = new BufferedReader(new FileReader(percorso));   // 2. assegnato DENTRO
            return in.readLine();
        } finally {
            if (in != null) {                            // 3. se FileReader è fallito, in è ancora null
                in.close();                              // 4. close() dichiara IOException: serve il throws
            }
        }
    }
}
```

| Se sbagli il passo | Cosa succede |
|---|---|
| 1. dichiari `in` **dentro** il `try` | nel `finally` la variabile non esiste: `cannot find symbol` (una variabile vive solo fra le graffe in cui nasce) |
| 3. niente controllo `null` | se l'apertura fallisce (file inesistente), `in` è `null`: `in.close()` lancia `NullPointerException` e **sovrascrive** l'eccezione vera, e anche il `return` già pronto nel `catch` |
| 4. `close()` senza `throws IOException` (o senza `try`) | `unreported exception IOException`: anche chiudere può fallire |
| usi il try-with-resources "perché è meglio" | corretto in generale, **non** quando la traccia impone il `finally`: il vincolo non è soddisfatto agli occhi del correttore |

**Se il metodo non deve propagare nulla** ("mai propagare eccezioni", "restituisce `null` in caso di errore"), il `close()` ha il suo `try/catch` dentro il `finally`, così il `return` del `catch` esterno resta valido:

```java
public String primaRigaOppureNull(String percorso) {
    BufferedReader in = null;
    try {
        in = new BufferedReader(new FileReader(percorso));
        return in.readLine();
    } catch (IOException e) {
        return null;
    } finally {
        if (in != null) {
            try {
                in.close();
            } catch (IOException e) {
                // niente da fare: stiamo già chiudendo
            }
        }
    }
}
```

Con **due** flussi annidati (`DataOutputStream` su `FileOutputStream`) si dichiara e si chiude solo quello **esterno**: chiude anche l'interno. Il caso completo con scrittura in coda è nel Livello 4.

### Quali metodi lanciano quali eccezioni controllate
Gli errori `unreported exception` nascono quasi sempre da qui: non ricordi che un'API lancia un'eccezione controllata. La tabella si impara a memoria.

| Chiamata | Eccezione controllata |
|---|---|
| `Thread.sleep(..)`, `wait()`, `join()` | `InterruptedException` |
| `new FileReader(p)`, `new FileInputStream(p)`, `new FileOutputStream(p)`, `new PrintWriter(p)`, `new Scanner(file)` | `FileNotFoundException` (è una `IOException`) |
| `new FileWriter(p)`, `readLine()`, `write..`, `read..`, `close()` su un flusso | `IOException` |
| `readUTF()`, `readInt()`, `readDouble()`, `readObject()` a **fine file** | `EOFException` (è una `IOException`) |
| `readObject()` | `IOException` **e** `ClassNotFoundException` |
| `new Socket(..)`, `serverSocket.accept()`, `getInputStream()`, `getOutputStream()` | `IOException` |
| `InetAddress.getByName(..)` | `UnknownHostException` (è una `IOException`) |
| `datagramSocket.send(..)` / `receive(..)` | `IOException` (`SocketTimeoutException` se c'è un timeout) |
| `builder.parse(..)`, `newDocumentBuilder()` (DOM) | `SAXException`, `IOException`, `ParserConfigurationException` |

Quasi tutta la famiglia dell'I/O e della rete è **sottoclasse di `IOException`**: un solo `catch (IOException e)` le copre tutte, e un solo `throws IOException` le dichiara tutte. Fanno eccezione `InterruptedException` e `ClassNotFoundException`, che non c'entrano con `IOException` e vanno dichiarate o catturate a parte.

**I due messaggi del compilatore, e come si leggono:**
- `unreported exception X; must be caught or declared to be thrown` → mancano o un `try/catch` o un `throws X` sulla firma. Se stai scrivendo il metodo che la lancia, il rimedio è la **firma**: `throws X`. Cambiare il corpo (`throw e` → `throw new IOException(e)`) sposta il problema e non lo risolve.
- `exception X is never thrown in body of corresponding try statement` → hai scritto un `catch (X)` per un `try` in cui nessuno lancia `X`. Togli il `catch`, oppure metti nel `try` la riga che davvero la lancia. Vale solo per le eccezioni **controllate**: `catch (Exception e)` e `catch (RuntimeException e)` non danno mai questo errore.

**`InterruptedException` quando il metodo non può dichiararla.** Hai tre scelte, tutte legali: dichiararla nella firma (`throws InterruptedException`, se la traccia lo chiede *o* se i chiamanti la gestiscono); catturarla e uscire in modo pulito; oppure, nel caso comune di un thread, catturarla e **ripristinare il flag** con `Thread.currentThread().interrupt()`. Non esiste `throw new InterruptedException(e)`: quel costruttore non prende una causa, e comunque rilanciarla richiede `throws`. Se vuoi trasformarla in un'eccezione non controllata, `throw new RuntimeException(e)`.

### Errori Comuni
- **Stampe fuori dal `finally` quando la traccia lo impone.** Output identico, requisito non soddisfatto: è una penalità pesante *a programma perfettamente funzionante*.
- **`throw` al posto di `throws` (e viceversa).** `throw new IOException()` nella firma non compila; `throws new IOException()` nemmeno.
- **Eccezione lanciata senza messaggio** quando la traccia ne pretende uno diverso per ogni caso.
- **`catch (Exception e)` messo per primo.** Ingoia tutto e impedisce la compilazione dei `catch` successivi più specifici.
- **`catch` vuoto.** Compila, non fa niente, e nasconde il guasto: l'errore più difficile da diagnosticare in assoluto.
- **Dichiarare `throws` su una `RuntimeException` "per sicurezza".** È legale ma inutile e segnala che la distinzione checked/unchecked non è chiara.
- **Istruzione vuota dopo un `if`:** `if (n > 0);` compila, il `;` chiude l'if e il blocco successivo viene eseguito sempre. È un errore di stile che nasce dalla fretta e sposta il comportamento del metodo.
- **Variabile del flusso dichiarata dentro il `try` e chiusa nel `finally`.** Non compila: nel `finally` non esiste. Si dichiara fuori, a `null`, e si chiude con `if (x != null)`.
- **`close()` nel `finally` senza controllo `null`.** Se l'apertura fallisce, la `NullPointerException` copre l'eccezione vera e annulla il `return` del `catch`.
- **Try-with-resources quando la traccia impone il `finally`.** Funziona, ma il vincolo di collocazione non è rispettato: è la stessa famiglia delle stampe fuori dal `finally`, con la chiusura dei flussi al posto delle stampe.
- **`throws` della classe sbagliata.** `temperaturaMassima() throws OraNonValidaException` per un metodo che legge un file: la firma dichiara ciò che il **corpo** può lanciare (`IOException`), non l'eccezione che hai appena definito.
- **Un `catch` di eccezione controllata che nessuno lancia.** `exception X is never thrown in body of corresponding try statement`. Non è un refuso: il `try` non contiene la riga che serve.
