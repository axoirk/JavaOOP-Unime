---
materia: Programmazione a Oggetti
capitolo: 13
titolo: Eccezioni
livello_syllabus: 3
stato: completo
slide: ["Savitch cap. 13 slide 1-37", "EsempioEccezioniCompleto"]
appelli: [EXAM1, EXAM3]
fonti_esterne: 4
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 13 — Eccezioni

## Di cosa parla questo capitolo

Nel codice scritto finora abbiamo quasi sempre ipotizzato che tutto andasse per il verso giusto: che l'utente inserisse numeri validi, che i riferimenti non fossero mai nulli, che gli indici degli array rimanessero entro i limiti stabiliti. Nel mondo reale, tuttavia, i programmi interagiscono con fattori esterni incontrollabili: file che non esistono, connessioni di rete che cadono all'improvviso, dischi pieni, dati corrotti o input imprevisti dell'utente.

Nei linguaggi procedurali tradizionali (come il C) le condizioni anomale venivano segnalate restituendo un valore speciale: per esempio `-1`, `NULL` o `false`. Questo approccio presenta due gravi difetti:
1. **Mescola il calcolo con la gestione dell'errore**: ogni chiamata a una funzione richiede una sequenza di controlli `if` che appesantiscono la lettura della logica principale.
2. **Può essere ignorato**: se il programmatore si dimentica di verificare il valore restituito, il programma prosegue lavorando su dati corrotti, fino a produrre guasti imprevedibili a distanza di tempo.

Java affronta il problema alla radice con un meccanismo a oggetti robusto ed elegante: le **eccezioni**. Un'eccezione è un **oggetto** che incapsula la natura del problema e viene "lanciato" non appena qualcosa va storto, interrompendo il normale flusso di istruzioni. La Java Virtual Machine risale automaticamente la catena dei metodi chiamanti alla ricerca di un blocco predisposto a intercettare e gestire l'errore.

In questo capitolo studiamo l'intero ciclo di vita delle eccezioni attraverso le **cinque parole chiave** del linguaggio:
- `try`: delimita il blocco di codice "sorvegliato";
- `catch`: cattura una specifica tipologia di eccezione e ne esegue la gestione;
- `finally`: garantisce l'esecuzione di un blocco di pulizia in qualunque scenario (con successo, con errore o con salto);
- `throw`: compie l'azione imperativa di lanciare un'istanza di eccezione;
- `throws`: dichiara nell'intestazione di un metodo che esso può propagare al chiamante determinate eccezioni controllate.

Approfondiremo inoltre la gerarchia delle eccezioni, la differenza cardine tra eccezioni controllate (**checked**) e non controllate (**unchecked** / `RuntimeException`), la creazione di eccezioni personalizzate e la corretta chiusura delle risorse.

> [!IMPORTANT]
> **Nota per l'esame — Le eccezioni come prova di rigore sintattico e architetturale**
> Negli appelli d'esame (in particolare EXAM1 ed EXAM3) la gestione delle eccezioni compare come secondo esercizio della prova scritta (valore tipico: 13 punti). Il docente richiede la scrittura di metodi che gestiscono o propagano eccezioni diverse in base a un parametro numerico, imponendo vincoli stringenti:
> - l'obbligo di utilizzare **tutte e cinque le parole chiave** (`try`, `catch`, `finally`, `throw`, `throws`);
> - la conversione di un'eccezione controllata (`IOException`) in una non controllata (`RuntimeException`) che risale verso il chiamante;
> - il vincolo tassativo di collocare le stampe dei messaggi **esclusivamente all'interno del blocco `finally`**, dimostrando di aver compreso che il blocco `finally` viene eseguito sempre, persino quando un blocco `catch` rilancia un'eccezione verso l'esterno.
>
> Un codice che produce l'output atteso ma colloca le stampe dentro i blocchi `catch` viola il vincolo strutturale e viola il vincolo richiesto dalla traccia e perde punti anche se l'output coincide. In questo capitolo presentiamo gli schemi esatti, commentati riga per riga, necessari per affrontare questi requisiti.

---

## 13.1 L'idea di fondo: separare l'errore dal flusso normale

### 13.1.1 Il problema dei codici di ritorno speciali

Consideriamo un metodo che deve eseguire una divisione intera o calcolare una percentuale. In assenza di un sistema di eccezioni, per segnalare che il divisore è zero siamo costretti a restituire un valore numerico fittizio, ad esempio `-1`.

```java
// Approccio tradizionale fragile basato su valori speciali
public class DivisioneTradizionale {
    public static int dividi(int numeratore, int denominatore) {
        if (denominatore == 0) {
            return -1; // Codice speciale che indica errore
        }
        return numeratore / denominatore;
    }

    public static void main(String[] args) {
        int risultato = dividi(10, 0);
        // Se il chiamante dimentica di controllare il valore -1...
        int totaleFattura = risultato * 50;
        System.out.println("Totale calcolato: " + totaleFattura); // Stampa -50! Errore silente propagato
    }
}
```

Questo approccio fallisce per due ragioni strutturali:
1. Il valore `-1` potrebbe essere un risultato lecito in altri contesti (ad esempio se il numeratore fosse `-10` e il denominatore `10`). Non esiste un valore numerico sicuramente "distinto" dal risultato valido.
2. Il chiamante non ha alcun obbligo sintattico di verificare il valore restituito. Se omette il controllo, il numero `-1` viene usato nei calcoli successivi, corrompendo lo stato del programma senza alcun messaggio d'allarme immediato.

### 13.1.2 La soluzione di Java: l'eccezione come oggetto

In Java, un'eccezione è un'**istanza di una classe**. Quando si verifica una situazione anomala:
1. Viene creato un oggetto eccezione (`new DivideByZeroException(...)`).
2. L'oggetto viene **lanciato** tramite la parola chiave `throw`.
3. Il normale flusso sequenziale del metodo si **interrompe all'istante**: nessuna delle istruzioni successive nel blocco viene eseguita.
4. Il controllo passa al primo gestore compatibile, delimitato dalla parola chiave `catch`.

Questo meccanismo separa nettamente il "cammino felice" (*happy path*, cioè la logica di calcolo quando tutto funziona) dal cammino di recupero o segnalazione degli errori.

> [!NOTE]
> **Definizione — Eccezione**
> Un'eccezione è un oggetto che segnala il verificarsi di un evento insolito o anomalo durante l'esecuzione del programma. Il processo di creazione e trasmissione dell'oggetto è detto **lancio dell'eccezione** (*throwing an exception*), mentre il codice preposto a rilevarlo e trattarlo costituisce la **gestione dell'eccezione** (*handling the exception* o *catching*).

### 13.1.3 Anatomia minima: `try`, `throw` e `catch`

La struttura minima per sperimentare il meccanismo richiede tre componenti:
- un blocco `try { ... }` contenente il codice suscettibile di fallimento;
- una condizione in cui scatta l'istruzione `throw new ...;`;
- un blocco `catch (TipoEccezione e) { ... }` che riceve l'oggetto lanciato.

#### Esempio — Gestione esplicita di una divisione anomala

```java
public class PrimaEccezioneDemo {
    public static void main(String[] args) {
        int numeratore = 42;
        int denominatore = 0;

        try {
            System.out.println("Inizio del calcolo...");
            if (denominatore == 0) {
                // Creazione e lancio dell'oggetto eccezione
                throw new ArithmeticException("Divisione per zero non consentita");
            }
            int quoziente = numeratore / denominatore;
            System.out.println("Quoziente calcolato: " + quoziente); // Saltata se denominatore è 0!
        } catch (ArithmeticException e) {
            // Gestione dell'anomalia
            System.out.println("Si e' verificato un problema: " + e.getMessage());
        }

        System.out.println("Il programma prosegue regolarmente dopo il blocco try-catch.");
    }
}
```

```text
Inizio del calcolo...
Si e' verificato un problema: Divisione per zero non consentita
Il programma prosegue regolarmente dopo il blocco try-catch.
```

Analizziamo il comportamento passo per passo:
- Il blocco `try` inizia regolarmente stampando `"Inizio del calcolo..."`.
- La condizione `denominatore == 0` risulta vera. Viene eseguita l'istruzione `throw new ArithmeticException(...)`.
- La riga successiva (`int quoziente = numeratore / denominatore;`) **non viene mai raggiunta**.
- La JVM cerca immediatamente un blocco `catch` compatibile con il tipo `ArithmeticException`. Lo trova subito sotto.
- La variabile parametro `e` del blocco `catch` riceve il riferimento all'oggetto `ArithmeticException` appena creato.
- Il corpo del `catch` viene eseguito, stampando la descrizione dell'errore recuperata tramite `e.getMessage()`.
- Una volta concluso il blocco `catch`, il flusso **non torna** dentro il `try`, ma continua sequenzialmente con l'istruzione successiva a valle del blocco di gestione.

### 13.1.4 Il flusso di controllo: con e senza eccezione

È fondamentale visualizzare con precisione la biforcazione del flusso di controllo.

```text
                  ┌────────────────────────┐
                  │ Inizio del blocco try  │
                  └───────────┬────────────┘
                              │
                    Si verifica un errore?
                     /                  \
              NO    /                    \   SI: istruzione throw
                   v                      v
        ┌──────────────────────┐  ┌───────────────────────────────────┐
        │ Esegue tutto il try  │  │ Interruzione immediata del try    │
        │ fino alla fine       │  │ (istruzioni successive saltate)   │
        └──────────┬───────────┘  └─────────────────┬─────────────────┘
                   │                                │
                   │                                v
                   │                      ┌───────────────────┐
                   │                      │ Blocco catch(e)   │
                   │                      │ viene eseguito    │
                   │                      └─────────┬─────────┘
                   │                                │
                   v                                v
         Blocco catch IGNORATO                      │
                   │                                │
                   └───────────────┬────────────────┘
                                   │
                                   v
                  ┌─────────────────────────────────┐
                  │ Istruzioni successive esterne   │
                  └─────────────────────────────────┘
```

Se nessuna istruzione lancia eccezioni durante l'esecuzione del blocco `try`, l'intero blocco viene completato normalmente e tutti i blocchi `catch` associati vengono saltati a piè pari.

---

## 13.2 La gerarchia delle eccezioni: `Throwable`, `Error`, `Exception`

In Java tutto ciò che può essere lanciato o catturato con la sintassi delle eccezioni appartiene a una rigorosa gerarchia di classi con radice in **`java.lang.Throwable`**.

```text
java.lang.Object
  └── java.lang.Throwable
        ├── java.lang.Error (UNCHECKED — guasti irreversibili della JVM)
        │     ├── OutOfMemoryError
        │     └── StackOverflowError
        │
        └── java.lang.Exception (errori applicativi)
              ├── java.lang.RuntimeException (UNCHECKED — bug del programmatore)
              │     ├── NullPointerException
              │     ├── ArithmeticException
              │     ├── IndexOutOfBoundsException
              │     │     └── ArrayIndexOutOfBoundsException
              │     ├── IllegalArgumentException
              │     │     └── NumberFormatException
              │     └── ClassCastException
              │
              └── [Tutte le altre Exception] (CHECKED — controllate dal compilatore)
                    ├── java.io.IOException
                    │     ├── FileNotFoundException
                    │     └── EOFException
                    ├── java.lang.InterruptedException
                    ├── java.lang.ClassNotFoundException
                    ├── java.sql.SQLException
                    └── org.xml.sax.SAXException
```

### 13.2.1 `java.lang.Throwable`

È la superclasse di tutti gli errori e di tutte le eccezioni del linguaggio. Solo gli oggetti che discendono da `Throwable` possono essere passati all'istruzione `throw` o dichiarati come tipo di parametro in una clausola `catch`.

I metodi più importanti ereditati da `Throwable` sono:
- `public String getMessage()`: restituisce il messaggio descrittivo associato all'eccezione al momento della creazione (oppure `null` se non è stato specificato alcun messaggio);
- `public Throwable getCause()`: restituisce l'eccezione che ha provocato quella corrente (la *causa*), oppure `null` se non c'è o non è nota;
- `public void printStackTrace()`: stampa sullo stream standard degli errori (`System.err`) l'eccezione e la traccia dello stack di esecuzione al momento della creazione, indicando classi, metodi e numeri di riga;
- `public String toString()`: restituisce una stringa composta dal nome della classe dell'eccezione, due punti, uno spazio e il messaggio descrittivo.

#### Esempio — Che cosa restituiscono `getMessage`, `toString` e `getCause`

```java
public class MetodiDiThrowable {
    public static void main(String[] args) {
        try {
            int[] v = new int[2];
            v[5] = 1;                                   // indice fuori dai limiti
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println(e.getMessage());         // solo il messaggio
            System.out.println(e);                      // println usa toString(): classe, due punti, messaggio
            System.out.println(e.getCause());           // nessuna causa: null
            e.printStackTrace();                        // sul canale degli errori: non compare nell'output sotto
        }
    }
}
```

```text
Index 5 out of bounds for length 2
java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 2
null
```

`getMessage()` dà il solo testo; `println(e)` chiama `toString()` e aggiunge davanti il nome completo della classe; `getCause()` è `null` perché questa eccezione non è stata provocata da un'altra. L'ultima riga, `printStackTrace()`, scrive su `System.err` la stessa riga di `toString()` seguita da una riga `at ...` per ogni metodo attraversato (con nome del file e numero di riga): serve per capire **dove** è nato l'errore, e per questo è utile in fase di prova ma non produce l'output che un esercizio si aspetta sul canale standard.

> [!NOTE]
> **Approfondimento esterno — `java.lang.Throwable`**
> La Javadoc di Java 17 dice che `Throwable` è "la superclasse di tutti gli errori e le eccezioni del linguaggio Java": solo i suoi oggetti possono essere lanciati dalla JVM o dall'istruzione `throw`, e solo `Throwable` o una sua sottoclasse può essere il tipo dell'argomento di una clausola `catch`. Ai fini del controllo in compilazione, `Throwable` e ogni sottoclasse che non sia anche sottoclasse di `RuntimeException` o di `Error` sono eccezioni **controllate**. Un `Throwable` contiene un'istantanea dello stack del thread al momento della creazione, un messaggio opzionale e una causa opzionale. Firme: `public String getMessage()`, `public Throwable getCause()`, `public void printStackTrace()` (stampa su `System.err`; la prima riga è il risultato di `toString()`), `public String toString()` ("il nome della classe dell'oggetto, `": "` e il risultato di `getLocalizedMessage()`"). Costruttori: `Throwable()`, `Throwable(String message)`, `Throwable(String message, Throwable cause)`, `Throwable(Throwable cause)`.
>
> *Fonte:* [java.lang.Throwable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Throwable.html)

### 13.2.2 `java.lang.Error`: guasti gravi della JVM

Gli oggetti che discendono da `java.lang.Error` rappresentano condizioni anomale gravi dovute a problemi intrinseci del sistema o dell'ambiente di esecuzione della JVM. 
Esempi tipici:
- `OutOfMemoryError`: la JVM ha esaurito lo spazio nell'heap e il Garbage Collector non è riuscito a recuperare memoria sufficiente;
- `StackOverflowError`: lo stack di chiamate del thread ha esaurito la memoria allocata (tipicamente a causa di una ricorsione infinita senza caso base, come visto nel [Capitolo 6](06-metodi.md)).

> [!WARNING]
> **Regola fondamentale — La classe `Error` non si cattura**
> Le applicazioni non devono mai tentare di intercettare gli oggetti di tipo `Error` con blocchi `catch (Error e)`. Quando si verifica un `Error`, lo stato interno della macchina virtuale è compromesso e il programma non dispone di strumenti sicuri per ripristinare il corretto funzionamento. L'unica reazione sensata è lasciare che il thread o il processo terminino, correggendo la causa a livello di architettura o di configurazione.

### 13.2.3 `java.lang.Exception`: gli errori applicativi

La classe `java.lang.Exception` rappresenta condizioni anomale che un'applicazione ragionevole può prevedere e da cui può essere in grado di riprendersi.

Al suo interno, la gerarchia si scinde in due categorie con regole di compilazione profondamente differenti:
1. **Eccezioni non controllate (Unchecked Exceptions)**: tutte le classi che estendono **`java.lang.RuntimeException`** (più le classi che estendono `Error`).
2. **Eccezioni controllate (Checked Exceptions)**: tutte le sottoclassi di `Exception` che **non** derivano da `RuntimeException`.

### 13.2.4 Checked contro Unchecked: la regola d'oro del compilatore

Questa distinzione è il cardine dell'intero modello di affidabilità di Java:

| Proprietà | Checked Exception (Controllata) | Unchecked Exception (Non controllata) |
|---|---|---|
| **Classe base** | `Exception` (esclusa `RuntimeException`) | `RuntimeException` (o `Error`) |
| **Cosa rappresenta** | Guasto esterno al codice, prevedibile ma non dipendente dalla perfezione del programma (es. file assente, server irraggiungibile, timeout) | Difetto logico o violazione di precondizioni nel codice scritto dal programmatore (es. puntatore nullo, indice errato) |
| **Regola del compilatore** | **Obbligo tassativo**: *Catch or Declare*. Il compilatore esige che l'eccezione sia catturata in un `try-catch` o dichiarata nella firma con `throws` | **Nessun obbligo**: il compilatore non richiede né `try-catch` né clausola `throws` |
| **Se non gestita** | Errore di compilazione: `unreported exception ...; must be caught or declared to be thrown` | Il programma compila regolarmente; a runtime l'eccezione risale lo stack e, se non catturata, termina il thread |
| **Esempi tipici** | `IOException`, `FileNotFoundException`, `EOFException`, `InterruptedException`, `ClassNotFoundException` | `NullPointerException`, `ArrayIndexOutOfBoundsException`, `ArithmeticException`, `IllegalArgumentException` |

> [!TIP]
> **Intuizione — Come distinguere Checked e Unchecked**
> Chiediti: *"Se scrivessi il codice in modo assolutamente perfetto, questo evento anomalo potrebbe comunque verificarsi?"*
> - Se la risposta è **sì** (perché l'utente potrebbe staccare il cavo di rete o cancellare un file sul disco mentre il programma gira), allora è una **Checked Exception**: il sistema esterno è fuori dal controllo del programmatore e il compilatore costringe a prevedere un piano di riserva.
> - Se la risposta è **no** (perché basterebbe un controllo `if (array != null && i < array.length)` per evitarla a monte), allora è una **Unchecked Exception**: è un difetto del codice che va corretto, non una condizione ambientale da mascherare.

> [!NOTE]
> **Approfondimento esterno — `java.lang.Exception` e `java.lang.RuntimeException`**
> La Javadoc di Java 17 specifica che la classe `Exception` e le sue sottoclassi (tranne `RuntimeException`) sono eccezioni controllate (*checked exceptions*): *"Checked exceptions need to be declared in a method or constructor's throws clause if they can be thrown by the execution of the method or constructor and propagate outside the method or constructor boundary"*.
> Di contro, `RuntimeException` è la superclasse di quelle eccezioni che *"can be thrown during the normal operation of the Java Virtual Machine"* e che non necessitano di dichiarazione formale.
>
> *Fonti:* [java.lang.Exception](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Exception.html) · [java.lang.RuntimeException](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/RuntimeException.html)

---

## 13.3 Lanciare e dichiarare: `throw` contro `throws`

Tra i principianti e all'esame scritto, la somiglianza grafica tra `throw` e `throws` genera continue confusioni. Si tratta in realtà di due concetti radicalmente diversi, collocati in punti differenti del file sorgente:

| Parola chiave | Dove si scrive | Cosa accetta come argomento | Ruolo operativo |
|---|---|---|---|
| **`throw`** | **Dentro il corpo** di un metodo o costruttore (istruzione esecutiva) | Un **oggetto** (istanza di `Throwable` o sottoclasse) | Compie l'azione imperativa di lanciare l'eccezione in quel preciso istante |
| **`throws`** | **Nell'intestazione** del metodo (firma, dopo i parametri) | Uno o più **tipi / classi** separati da virgole | Dichiara ai chiamanti che il metodo potrebbe lasciar fuoriuscire quelle checked exception |

> [!IMPORTANT]
> **Regola mnemonica d'esame — L'oggetto contro il tipo**
> - `throw` è un'azione concreta: `throw new IOException("disco guasto");` → lancia l'**istanza**.
> - `throws` è un avviso contrattuale: `public void salva() throws IOException` → dichiara la **classe**.
> Scrivere `throws new IOException()` non compila; scrivere `throw IOException;` non compila.

### 13.3.1 L'istruzione `throw`

L'istruzione `throw` richiede un'espressione che valuti a un riferimento a `Throwable` (quasi sempre creato al volo con l'operatore `new`).

```java
// Forma comune: creazione e lancio immediato in una riga
throw new IllegalArgumentException("Parametro non valido: valore negativo");
```

In alternativa, l'oggetto può essere prima memorizzato in una variabile e poi lanciato:

```java
// Forma alternativa equivalente
IllegalArgumentException ex = new IllegalArgumentException("Parametro non valido: valore negativo");
throw ex;
```

Non appena l'istruzione `throw` viene eseguita:
- il metodo corrente arresta l'esecuzione;
- la JVM cerca un blocco `try` circostante con un `catch` compatibile;
- se il metodo corrente non cattura l'eccezione, il metodo viene terminato immediatamente e la JVM ripete la ricerca nel metodo chiamante (risalita dello stack).

### 13.3.2 La clausola `throws` (*Passing the Buck*)

Se un metodo contiene codice che può provocare una **checked exception** (perché la lancia direttamente con `throw`, oppure perché invoca un altro metodo che la dichiara) e **non** intende catturarla con un blocco `try-catch` locale, ha l'obbligo di delegare la responsabilità al proprio chiamante. Questa delega è detta in letteratura didattica *"passing the buck"* (scaricare la responsabilità).

La delega si esprime aggiungendo la clausola `throws` all'intestazione del metodo:

```java
import java.io.IOException;

public class EsempioDelega {
    // Il metodo dichiara che può propagare IOException al chiamante
    public static void scriviDati(String testo) throws IOException {
        if (testo == null) {
            // IOException è checked: se non la catturiamo qui, il throws è obbligatorio
            throw new IOException("Impossibile scrivere un testo nullo");
        }
        System.out.println("Scrittura effettuata: " + testo);
    }

    public static void main(String[] args) {
        // Chi chiama scriviDati deve gestire l'eccezione oppure dichiararla a sua volta nel main
        try {
            scriviDati(null);
        } catch (IOException e) {
            System.out.println("Catturata nel main: " + e.getMessage());
        }
    }
}
```

```text
Catturata nel main: Impossibile scrivere un testo nullo
```

Se il `main` avesse invocato `scriviDati(null)` senza racchiuderlo in un blocco `try-catch` e senza dichiarare a sua volta `throws IOException`, il compilatore avrebbe rifiutato il programma con l'errore:
`unreported exception java.io.IOException; must be caught or declared to be thrown`.

### 13.3.3 `throws` e l'ereditarietà: la regola di overriding

Quando una sottoclasse sovrascrive un metodo della superclasse, la clausola `throws` del metodo derivato è soggetta a un vincolo rigido:

> [!WARNING]
> **Vincolo fondamentale — Clausola `throws` nell'override (restringere sì, allargare mai)**
> Il metodo sovrascritto in una sottoclasse:
> - **può** dichiarare **meno** eccezioni controllate rispetto al metodo originale;
> - **può** dichiarare **nessuna** eccezione controllata (eliminazione completa del `throws`);
> - **può** dichiarare **sottoclassi** più specifiche delle eccezioni dichiarate dalla superclasse;
> - **NON PUÒ ASSOLUTAMENTE dichiarare eccezioni controllate NUOVE o PIÙ GENERICHE** rispetto a quelle del metodo padre.
>
> Questo vincolo si applica **solo alle checked exception**. Le eccezioni di tipo `RuntimeException` non sono soggette ad alcun vincolo di firma.

#### Perché questa regola? Il principio di sostituzione di Liskov

Immaginiamo che il metodo `Base.leggi()` dichiari `throws IOException`. Un modulo client che riceve un riferimento polimorfico di tipo `Base` organizzerà il proprio codice con un `catch (IOException e)`.

Se una classe `Derivata` potesse dichiarare `throws Exception` (tipo più generico) o `throws SQLException` (nuova checked), invocando `leggi()` su un'istanza di `Derivata` mascherata da `Base` potrebbe fuoriuscire un'eccezione che il blocco `catch (IOException e)` del client non può catturare. Il programma andrebbe in crash distruggendo la sicurezza dei tipi e il polimorfismo. Al contrario, se la sottoclasse non lancia alcuna eccezione o lancia un tipo più specifico (come `FileNotFoundException`, che è sottotipo di `IOException`), il blocco `catch (IOException e)` del client sarà perfettamente in grado di intercettarla.

#### Esempio — Overriding e clausola `throws`

```java
import java.io.FileNotFoundException;
import java.io.IOException;

class ConnessioneBase {
    public void connetti() throws IOException {
        System.out.println("Connessione base aperta.");
    }
}

// 1. Legale: restringe a un sottotipo più specifico
class ConnessioneFile extends ConnessioneBase {
    @Override
    public void connetti() throws FileNotFoundException {
        System.out.println("Connessione file specifica aperta.");
    }
}

// 2. Legale: elimina del tutto la clausola throws (zero eccezioni)
class ConnessioneMemoria extends ConnessioneBase {
    @Override
    public void connetti() {
        System.out.println("Connessione memoria sicura aperta.");
    }
}

// 3. ILLEGALE: non compila! Exception è più generale di IOException.
/*
class ConnessioneErrata extends ConnessioneBase {
    @Override
    public void connetti() throws Exception { // ERRORE DI COMPILAZIONE!
        System.out.println("Errore di override.");
    }
}
*/
```

Se proviamo a scommentare la classe `ConnessioneErrata`, il compilatore segnala:
```text
connetti() in ConnessioneErrata cannot override connetti() in ConnessioneBase
  overridden method does not throw Exception
```

---

## 13.4 Catturare le eccezioni: blocchi `catch` multipli e propagazione

### 13.4.1 Blocchi `catch` sequenziali

Un singolo blocco `try` può contenere istruzioni che provocano anomalie eterogenee: ad esempio, la lettura di una riga di testo può generare una `IOException`, mentre la conversione di tale riga in numero intero può lanciare una `NumberFormatException`.

Java consente di far seguire a un blocco `try` **più blocchi `catch`**, ciascuno specializzato per una specifica famiglia di errori:

```java
import java.io.IOException;

public class CatchMultipliDemo {
    public static void analizzaDato(String stringaNumero, boolean forzaErroreIO) {
        try {
            if (forzaErroreIO) {
                throw new IOException("Errore di lettura dal dispositivo");
            }
            // Integer.parseInt lancia NumberFormatException (unchecked) se il formato non è valido
            int valore = Integer.parseInt(stringaNumero);
            System.out.println("Numero decodificato con successo: " + valore);
        } catch (IOException e) {
            System.out.println("[Gestore I/O] Impossibile acquisire il dato: " + e.getMessage());
        } catch (NumberFormatException e) {
            System.out.println("[Gestore Formato] Il dato fornito non e' un intero: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("[Gestore Generale] Errore imprevisto: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        analizzaDato("123", false);       // Successo
        analizzaDato("testo_errato", false); // Catturata da NumberFormatException
        analizzaDato("456", true);        // Catturata da IOException
    }
}
```

```text
Numero decodificato con successo: 123
[Gestore Formato] Il dato fornito non e' un intero: For input string: "testo_errato"
[Gestore I/O] Impossibile acquisire il dato: Errore di lettura dal dispositivo
```

### 13.4.2 La regola dell'ordine: dal più specifico al più generale

Quando scatta un'eccezione, la JVM esamina i blocchi `catch` **dall'alto verso il basso**, fermandosi al **primo** blocco il cui tipo dichiarato è uguale al tipo dell'oggetto lanciato oppure ne è una **superclasse** (in virtù del polimorfismo).

Da questo meccanismo discende una regola imperativa:
I blocchi `catch` devono essere ordinati **dal tipo più specifico (sottoclasse) al tipo più generico (superclasse)**.

Se collocassimo `catch (Exception e)` per primo:
```java
// ERRATO: non compila! Ordine invertito
try {
    throw new IOException("guasto");
} catch (Exception e) {
    // Questa clausola cattura IOException (perché IOException extends Exception)
    System.out.println("Generale");
} catch (IOException e) { // ERRORE DI COMPILAZIONE: blocco irraggiungibile!
    System.out.println("I/O");
}
```

Il compilatore rifiuta categoricamente il codice producendo l'errore:
`error: exception IOException has already been caught`.

### 13.4.3 Rilancio delle eccezioni (*rethrowing*) e conversione controllata → non controllata

Un blocco `catch` non è obbligato a "risolvere" l'errore in via definitiva. Spesso il gestore locale desidera eseguire un'azione parziale (registrare il problema, liberare parzialmente lo stato) e poi **rilanciare** l'eccezione verso i chiamanti più a monte.

La tecnica del rilancio può avvenire in due modi:
1. **Rilancio diretto dell'oggetto catturato**:
   ```java
   try {
       // Operazione che può fallire
       throw new IOException("Errore di trasmissione");
   } catch (IOException e) {
       System.out.println("Errore intercettato, rilancio...");
       throw e; // Rilancia la medesima istanza
   }
   ```
2. **Conversione (o incapsulamento) di una checked in una unchecked**:
   Questa tecnica è fondamentale e compare regolarmente all'esame: si cattura un'eccezione controllata (es. `IOException`) e si lancia una `RuntimeException` che incapsula il messaggio o l'eccezione originaria. In questo modo il chiamante viene notificato del fallimento senza che il metodo sia costretto a dichiarare `throws IOException` nella propria firma.

```java
import java.io.IOException;

public class ConversioneEccezioneDemo {
    public static void elaboraArchivio(boolean simulaGuasto) {
        try {
            if (simulaGuasto) {
                throw new IOException("File danneggiato su disco");
            }
            System.out.println("Archivio elaborato con successo.");
        } catch (IOException e) {
            // Conversione checked -> unchecked
            System.out.println("Catturata IOException, conversione in RuntimeException...");
            throw new RuntimeException("Fallimento irreversibile durante l'elaborazione", e);
        }
    }

    public static void main(String[] args) {
        try {
            elaboraArchivio(true);
        } catch (RuntimeException e) {
            System.out.println("Intercettata nel main: " + e.getMessage());
            System.out.println("Causa originale: " + e.getCause().getClass().getSimpleName());
        }
    }
}
```

```text
Catturata IOException, conversione in RuntimeException...
Intercettata nel main: Fallimento irreversibile durante l'elaborazione
Causa originale: IOException
```

> [!NOTE]
> **Approfondimento esterno — `java.io.IOException`**
> Nella Javadoc di Java 17 `public class IOException extends Exception` è descritta così: "segnala che si è verificata un'eccezione di input/output di qualche tipo. Questa classe è la classe generale delle eccezioni prodotte da operazioni di I/O fallite o interrotte". Essendo sottoclasse di `Exception` e non di `RuntimeException`, è un'eccezione **controllata**: i metodi che possono lanciarla la dichiarano con `throws`.
>
> *Fonte:* [java.io.IOException](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/IOException.html)

---

## 13.5 Il blocco `finally`: l'esecuzione garantita e la gestione delle risorse

### 13.5.1 Perché serve il blocco `finally`

Quando un metodo acquisisce risorse esterne critiche (come un descrittore di file aperto, un socket TCP o una connessione a un database), il sistema operativo riserva memoria e porte che devono essere rilasciate non appena l'operazione si conclude.

Se un'eccezione viene lanciata a metà del blocco `try`, tutte le istruzioni successive vengono saltate. Se la chiusura della risorsa si trovasse in fondo al `try`, la risorsa rimarrebbe aperta indefinitamente (*resource leak*). 

Per risolvere questo problema, Java mette a disposizione il blocco **`finally`**, posizionato subito dopo l'ultimo blocco `catch` (o direttamente dopo il `try` se non ci sono `catch`).

> [!IMPORTANT]
> **La proprietà assoluta di `finally`**
> Il blocco `finally` viene eseguito **SEMPRE**:
> 1. se il blocco `try` termina con successo;
> 2. se nel blocco `try` scatta un'eccezione che viene catturata da un blocco `catch`;
> 3. se nel blocco `try` (o dentro un `catch`) scatta un'eccezione che **non** viene catturata o che viene rilanciata verso l'esterno;
> 4. persino se dal blocco `try` o `catch` si esce tramite un'istruzione di salto come **`return`**, `break` o `continue`.
>
> L'unico caso al mondo in cui il blocco `finally` non viene eseguito è l'arresto immediato e forzato della macchina virtuale tramite `System.exit(0)` o un crash a livello di sistema operativo.

### 13.5.2 I tre scenari di esecuzione

Per comprendere la precisione del flusso, osserviamo il seguente programma che testa i tre scenari possibili:

```java
public class ScenariFinallyDemo {
    public static void eseguiTest(int caso) {
        System.out.println("\n--- Avvio test caso " + caso + " ---");
        try {
            System.out.println("1. Entrato nel blocco try");
            if (caso == 1) {
                System.out.println("2. Operazione completata senza anomalie.");
            } else if (caso == 2) {
                System.out.println("2. Lancio eccezione gestita localmente...");
                throw new ArithmeticException("Errore aritmetico");
            } else if (caso == 3) {
                System.out.println("2. Lancio eccezione che risalira' al chiamante...");
                throw new IllegalArgumentException("Parametro critico illegale");
            }
        } catch (ArithmeticException e) {
            System.out.println("3. Blocco catch eseguito: " + e.getMessage());
        } finally {
            System.out.println("4. Blocco FINALLY in esecuzione (garantito SEMPRE)");
        }
        System.out.println("5. Codice successivo esterno al costrutto try-catch-finally");
    }

    public static void main(String[] args) {
        eseguiTest(1); // Uscita normale
        eseguiTest(2); // Eccezione catturata
        try {
            eseguiTest(3); // Eccezione non catturata nel metodo eseguiTest
        } catch (IllegalArgumentException e) {
            System.out.println("6. Catturata nel main dopo che il finally ha terminato!");
        }
    }
}
```

```text
--- Avvio test caso 1 ---
1. Entrato nel blocco try
2. Operazione completata senza anomalie.
4. Blocco FINALLY in esecuzione (garantito SEMPRE)
5. Codice successivo esterno al costrutto try-catch-finally

--- Avvio test caso 2 ---
1. Entrato nel blocco try
2. Lancio eccezione gestita localmente...
3. Blocco catch eseguito: Errore aritmetico
4. Blocco FINALLY in esecuzione (garantito SEMPRE)
5. Codice successivo esterno al costrutto try-catch-finally

--- Avvio test caso 3 ---
1. Entrato nel blocco try
2. Lancio eccezione che risalira' al chiamante...
4. Blocco FINALLY in esecuzione (garantito SEMPRE)
6. Catturata nel main dopo che il finally ha terminato!
```

Osserva con estrema attenzione il **caso 3**:
L'eccezione `IllegalArgumentException` non trova alcun blocco `catch` compatibile dentro `eseguiTest`. La JVM sta per far abbandonare il metodo all'eccezione, ma **prima di lasciarla uscire esegue interamente il blocco `finally`** (stampa `4`). Soltanto dopo che il `finally` ha terminato, l'eccezione raggiunge il `main`, dove viene infine intercettata (stampa `6`). La riga `5` non viene eseguita perché il metodo è terminato in modo anomalo.

### 13.5.3 La chiusura corretta dei flussi nel `finally` (schema in 4 passi)

Prima dell'introduzione del costrutto `try-with-resources`, la chiusura di file e flussi doveva avvenire rigorosamente dentro il blocco `finally`. Questo schema è **fondamentale all'esame scritto**, poiché i docenti richiedono esplicitamente di gestire la pulizia delle risorse tramite `finally`.

Scrivere questa operazione senza errori richiede di seguire scrupolosamente **quattro passi consecutivi**:

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ChiusuraCorrettaFlusso {
    public static String leggiContenuto(String percorsoFile) throws IOException {
        // PASSO 1: Dichiarare il riferimento FUORI dal blocco try, inizializzato a null
        BufferedReader lettore = null;

        try {
            // PASSO 2: Assegnare e aprire la risorsa DENTRO il blocco try
            lettore = new BufferedReader(new FileReader(percorsoFile));
            return lettore.readLine();
        } finally {
            // PASSO 3: Nel blocco finally, verificare TASSATIVAMENTE che il riferimento sia diverso da null
            if (lettore != null) {
                // PASSO 4: Invocare close(), gestendo o propagando l'eventuale IOException
                lettore.close();
            }
        }
    }
}
```

Esaminiamo perché ciascuno dei 4 passi è vitale:

| Passo | Cosa succede se lo sbagli | Errore risultante |
|---|---|---|
| **1. Dichiarazione fuori a `null`** | Se dichiari `BufferedReader lettore = ...` dentro il `try`, la variabile esiste solo dentro le parentesi graffe del `try` (*scope* di blocco). Nel blocco `finally` non è visibile. | Errore di compilazione: `cannot find symbol: variable lettore` |
| **2. Apertura dentro il `try`** | Se istanzi la risorsa prima del `try`, un fallimento del costruttore (es. file non trovato) impedisce di entrare nel blocco di protezione. | Codice non protetto |
| **3. Controllo `if (lettore != null)`** | Se il costruttore fallisce (es. `FileNotFoundException`), `lettore` rimane `null`. Chiamare `lettore.close()` senza controllo scatena una `NullPointerException`. Questa nuova eccezione **cancella e sovrascrive** l'eccezione originaria, impedendo di capire la vera causa del problema! | Bug a runtime gravissimo (`NullPointerException` che maschera l'errore vero) |
| **4. Chiamata a `close()`** | Il metodo `close()` dichiara a sua volta `throws IOException`. Il metodo contenitore deve dichiarare `throws IOException` nella firma, oppure racchiudere la chiamata a `close()` in un secondo piccolo blocco `try-catch` interno al `finally`. | Errore di compilazione: `unreported exception IOException` |

### 13.5.4 Approfondimento esterno: `AutoCloseable` e il `try-with-resources`

A partire da Java 7, il linguaggio offre una sintassi alternativa che delega al compilatore la generazione automatica del blocco `finally` di chiusura: il **`try-with-resources`**.

```java
import java.io.BufferedReader;
import java.io.StringReader;
import java.io.IOException;

public class TryWithResourcesDemo {
    public static void main(String[] args) {
        String sorgente = "Prima riga di prova\nSeconda riga di prova";
        
        // Risorsa dichiarata tra parentesi tonde subito dopo la parola chiave try
        try (BufferedReader reader = new BufferedReader(new StringReader(sorgente))) {
            String prima = reader.readLine();
            System.out.println("Riga letta: " + prima);
        } catch (IOException e) {
            System.out.println("Errore di lettura: " + e.getMessage());
        }
        // Al termine delle parentesi graffe del try, reader.close() viene invocato AUTOMATICAMENTE,
        // sia in caso di successo sia in caso di eccezione!
    }
}
```

```text
Riga letta: Prima riga di prova
```

> [!NOTE]
> **Approfondimento esterno — `java.lang.AutoCloseable`**
> La sintassi `try-with-resources` accetta qualsiasi oggetto la cui classe implementi l'interfaccia `java.lang.AutoCloseable` (o la sua sottointerfaccia `java.io.Closeable`). `AutoCloseable` dichiara un unico metodo: `void close() throws Exception`.
> Quando l'esecuzione abbandona il blocco `try`, la JVM invoca automaticamente `close()` su ciascuna risorsa aperta, in ordine inverso rispetto alla dichiarazione. Se durante la chiusura automatica si verifica un'eccezione mentre un'altra eccezione era già in corso nel `try`, la seconda viene registrata come *eccezione soppressa* (`getSuppressed()`), senza mascherare l'eccezione primaria.
>
> *Fonte:* [java.lang.AutoCloseable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/AutoCloseable.html)

> [!WARNING]
> **Avviso categorico per l'esame scritto — Quando il try-with-resources NON va usato**
> Se una traccia d'esame recita:
> *"La chiusura dei flussi deve avvenire all'interno del blocco `finally`"*
> oppure impone come vincolo architetturale:
> *"Vanno utilizzate tutte e cinque le parole chiave (`try`, `catch`, `finally`, `throw`, `throws`)"*
>
> l'uso del `try-with-resources` al posto del blocco `finally` esplicito **viola il vincolo formale richiesto dalla traccia**: il `finally` non compare nel sorgente, e la valutazione guarda alla struttura imposta, non solo al risultato. In presenza di tale vincolo, usa **esclusivamente** lo schema in 4 passi con il blocco `finally` tradizionale.

---

## 13.6 Definire le proprie eccezioni (classi personalizzate)

Sebbene Java disponga di centinaia di classi di eccezioni predefinite nella Java Standard Library, nelle applicazioni e negli appelli d'esame è frequente l'esigenza di creare classi di eccezioni dedicate al dominio del problema (ad esempio un prelievo bancario superiore al saldo disponibile).

### 13.6.1 Le regole per definire una classe di eccezione

Una classe di eccezione corretta segue poche regole precise:
1. **Scegliere la superclasse appropriata**:
   - Per creare un'eccezione **controllata (checked)**, si estende direttamente `java.lang.Exception`. Chiunque invochi codice che lancia questa eccezione sarà obbligato a gestirla o dichiararla.
   - Per creare un'eccezione **non controllata (unchecked)**, si estende `java.lang.RuntimeException`.
2. **Definire almeno due costruttori**:
   - Un **costruttore di default** (senza parametri), che invoca `super();` per impostare un messaggio generico o nullo.
   - Un **costruttore con parametro `String message`**, che trasmette la stringa al costruttore della superclasse tramite `super(message);`.
3. **Non sovrascrivere mai il metodo `getMessage()`**:
   La superclasse `Throwable` memorizza già la stringa ricevuta nel costruttore e la restituisce fedelmente quando si invoca `getMessage()`. Riscrivere il metodo è ridondante e rischia di alterare il comportamento standard.

### 13.6.2 Un esempio completo: `ContoCorrente` ed eccezioni personalizzate

L'esempio seguente, tratto dal materiale del docente, mostra un conto corrente con un'eccezione **controllata** (saldo insufficiente) e una **non controllata** (importo non valido), riorganizzato in un unico file pronto per la compilazione:

```java
// Eccezione personalizzata CHECKED: estende Exception
class OutofMoneyException extends Exception {
    public OutofMoneyException() {
        super();
    }

    public OutofMoneyException(String message) {
        super(message); // Passa la descrizione alla superclasse
    }
}

// Eccezione personalizzata UNCHECKED: estende RuntimeException
class MiaEccezioneUnchecked extends RuntimeException {
    public MiaEccezioneUnchecked() {
        super();
    }

    public MiaEccezioneUnchecked(String message) {
        super(message);
    }
}

// Classe di dominio che fa uso delle eccezioni personalizzate
class ContoCorrente {
    private float saldo;

    public ContoCorrente(float saldoIniziale) {
        this.saldo = saldoIniziale;
    }

    public float getSaldo() {
        return saldo;
    }

    public void setSaldo(float saldo) {
        this.saldo = saldo;
    }

    public void versaDenaro(float importo) {
        if (importo <= 0) {
            // Un importo negativo o nullo e' un difetto logico: unchecked exception
            throw new MiaEccezioneUnchecked("Importo di versamento non valido: " + importo);
        }
        saldo += importo;
    }

    // Trattandosi di un'eccezione CHECKED, il metodo DEVE dichiararla con 'throws'
    public void preleva(float importo) throws OutofMoneyException {
        if (importo > saldo) {
            // Condizione anomala: saldo non sufficiente
            throw new OutofMoneyException("soldi terminati");
        } else {
            saldo -= importo;
            System.out.println("hai prelevato " + importo + " il saldo attuale è: " + saldo);
        }
    }
}

public class EsempioDocenteCompleto {
    public static void main(String[] args) {
        ContoCorrente conto = new ContoCorrente(100.0f);
        conto.versaDenaro(100.0f); // Saldo sale a 200.0f

        try {
            System.out.println("Tentativo di prelievo di 250.0 euro...");
            conto.preleva(250.0f); // Lancia OutofMoneyException
        } catch (OutofMoneyException e) {
            System.out.println("Intercettata eccezione: " + e.getMessage());
        } finally {
            System.out.println("operazione terminata");
        }
    }
}
```

```text
Tentativo di prelievo di 250.0 euro...
Intercettata eccezione: soldi terminati
operazione terminata
```

Osserviamo i dettagli cardine:
- Nel metodo `preleva(float importo)`, poiché `OutofMoneyException` estende `Exception` (checked), l'istruzione `throw new OutofMoneyException(...)` obbliga il metodo a dichiarare `throws OutofMoneyException` nella propria firma.
- Il metodo `main`, invocando `conto.preleva(...)`, è a sua volta costretto a racchiudere la chiamata in un blocco `try-catch`.
- Il messaggio `"soldi terminati"` passato al costruttore viene recuperato nel `catch` tramite la chiamata `e.getMessage()`.
- Il blocco `finally` stampa `"operazione terminata"` garantendo la conclusione della transazione.

---

## 13.7 Le cinque parole chiave in sinergia

### 13.7.1 Tabella comparativa delle 5 parole chiave

Le cinque parole chiave costituiscono un vocabolario coordinato:

| Parola chiave | Natura sintattica | Posizione | Scopo |
|---|---|---|---|
| **`try`** | Istruzione di blocco | Corpo del metodo | Sorveglia una sequenza di istruzioni intercettando qualsiasi eccezione |
| **`catch`** | Clausola associata a `try` | Subito dopo il blocco `try` | Riceve come parametro un oggetto eccezione compatibile e ne esegue la gestione |
| **`finally`** | Clausola associata a `try`/`catch` | In coda all'ultimo blocco `catch` | Esegue codice di ripristino o notifica in **ogni possibile percorso di uscita** |
| **`throw`** | Istruzione esecutiva | Corpo di metodi o blocchi | Istanzia e scaglia attivamente un oggetto eccezione |
| **`throws`** | Clausola dichiarativa | Firma/intestazione del metodo | Dichiara l'elenco delle checked exception che il metodo può propagare al chiamante |

### 13.7.2 La sinergia d'esame: stampa unica nel `finally`, anche con rilancio

Le tracce amano un requisito che sembra paradossale. Si chiede un metodo che, in base a un parametro intero, si comporta in tre modi diversi, con queste condizioni:
1. usare **tutte e cinque** le parole chiave (`try`, `catch`, `finally`, `throw`, `throws`);
2. con un primo valore, lanciare un'eccezione generica e gestirla **dentro** il metodo;
3. con un secondo valore, lanciare una `IOException`, catturarla e rilanciare una `RuntimeException` verso il chiamante;
4. con ogni altro valore, nessuna eccezione;
5. in tutti i casi il messaggio va stampato **una volta sola, in un unico blocco `finally`**.

Il dubbio tipico è: *"come può il `finally` stampare un messaggio che dipende dal `catch`, se nel `catch` rilancio un'eccezione e il metodo termina?"*

La risposta sta nella semantica del `finally`: **quando un `catch` esegue `throw new RuntimeException(...)`, la JVM non abbandona subito il metodo, ma esegue prima il blocco `finally`**. Basta quindi memorizzare il messaggio in una variabile locale, dichiarata e inizializzata **prima** del `try`, e stamparla nel `finally`. Ecco lo schema con uno scenario neutro: una stazione di controllo che esamina un canale di lettura.

```java
import java.io.IOException;

public class Stazione {
    // 'throws': il metodo dichiara che può far uscire un'eccezione controllata
    public static void controlla(int canale) throws Exception {
        String esito = "lettura regolare";          // valore predefinito, prima del try

        try {                                       // 'try': il codice sorvegliato
            if (canale == 0) {
                throw new Exception("sensore muto");           // 'throw': eccezione generica
            } else if (canale == 1) {
                throw new IOException("rete non raggiungibile"); // 'throw': eccezione controllata
            }
        } catch (IOException e) {                   // 'catch' del tipo più specifico, per primo
            esito = "guasto di rete";
            throw new RuntimeException(esito);      // rilancio non controllato: il finally parte PRIMA
        } catch (Exception e) {                     // 'catch' del tipo più generale, dopo
            esito = "guasto generico";
        } finally {                                 // 'finally': l'unico punto di stampa
            System.out.println(esito);
        }
    }

    public static void main(String[] args) {
        System.out.print("controlla(0) -> ");
        try {
            controlla(0);
        } catch (Exception e) {
            // nel caso 0 nulla esce dal metodo
        }

        System.out.print("controlla(1) -> ");
        try {
            controlla(1);
        } catch (RuntimeException e) {
            System.out.println("(il chiamante riceve: " + e.getMessage() + ")");
        } catch (Exception e) {
            // non interviene
        }

        System.out.print("controlla(2) -> ");
        try {
            controlla(2);
        } catch (Exception e) {
            // non interviene
        }
    }
}
```

```text
controlla(0) -> guasto generico
controlla(1) -> guasto di rete
(il chiamante riceve: guasto di rete)
controlla(2) -> lettura regolare
```

Seguiamo il caso `canale = 1`:
1. `throw new IOException(...)` interrompe il `try`.
2. Il blocco `catch (IOException e)` intercetta l'eccezione (è il primo `catch` compatibile).
3. La variabile `esito` assume il valore `"guasto di rete"`.
4. Viene eseguita `throw new RuntimeException(esito)`.
5. La JVM **sospende** l'uscita dell'eccezione e passa al blocco `finally`.
6. Il `finally` stampa il valore di `esito`.
7. Concluso il `finally`, la `RuntimeException` riprende la sua corsa verso il chiamante, che la intercetta.

La variabile `esito` deve avere un valore su **ogni** percorso che arriva al `finally`: per questo la si inizializza alla dichiarazione, prima del `try` (vedi l'errore tipico relativo). Il metodo dichiara `throws Exception` per soddisfare la parola chiave `throws` richiesta dalla traccia, anche se il caso generico viene gestito localmente.

---

## 13.8 Quali API lanciano quali eccezioni controllate

Quando si scrivono programmi d'esame complessi (composti da lettura di file, socket di rete, parsing XML o connessioni database), il compilatore segnala frequentemente errori di tipo `unreported exception`. La tabella seguente riassume le eccezioni controllate lanciate dalle principali API della libreria standard che incontreremo nei capitoli successivi:

| API / Chiamata tipica | Eccezione Controllata | Package di appartenenza | Descrizione sintetica |
|---|---|---|---|
| `new FileReader(path)`, `new FileInputStream(path)`, `new FileOutputStream(path)`, `new Scanner(new File(...))` | **`FileNotFoundException`** | `java.io` | Il file specificato sul percorso non esiste o non è accessibile in lettura/scrittura (è sottoclasse di `IOException`). |
| `reader.readLine()`, `writer.write(...)`, `stream.close()`, `stream.flush()` | **`IOException`** | `java.io` | Errore generico di lettura o scrittura su supporto fisico o canale dati. |
| `in.readInt()`, `in.readUTF()`, `in.readObject()` su flussi binari | **`EOFException`** | `java.io` | Segnala il raggiungimento della fine del file binario (*End Of File*, sottoclasse di `IOException`). |
| `in.readObject()` (deserializzazione) | **`ClassNotFoundException`** | `java.lang` | La classe dell'oggetto letto da disco o rete non è presente nel classpath corrente (non deriva da `IOException`!). |
| `Thread.sleep(...)`, `thread.join()`, `obj.wait()` | **`InterruptedException`** | `java.lang` | Un altro thread ha inviato un segnale di interruzione mentre il thread corrente era in attesa. |
| `new Socket(host, port)`, `new ServerSocket(port)`, `serverSocket.accept()` | **`IOException`** | `java.io` / `java.net` | Errore di connessione TCP, porta già occupata o socket chiuso. |
| `InetAddress.getByName(host)` | **`UnknownHostException`** | `java.net` | L'indirizzo IP associato al nome host specificato non può essere risolto via DNS (sottoclasse di `IOException`). |
| `socket.send(packet)`, `socket.receive(packet)` (UDP) | **`IOException`** | `java.io` / `java.net` | Errore nella trasmissione o ricezione del datagramma UDP. |
| `builder.parse(...)` (XML DOM) | **`SAXException`**, **`IOException`** | `org.xml.sax`, `java.io` | Documento XML malformato (`SAXException`) o errore di I/O nel recupero del sorgente. |
| `factory.newDocumentBuilder()` | **`ParserConfigurationException`** | `javax.xml.parsers` | Impossibile creare il parser con la configurazione richiesta. |
| `DriverManager.getConnection(...)`, `stmt.executeQuery(...)`, `rs.next()` | **`SQLException`** | `java.sql` | Errore di accesso al database, sintassi SQL non valida o connessione interrotta. |

> [!TIP]
> **Consiglio per l'esame — La famiglia `IOException` copre quasi tutto l'I/O**
> Poiché `FileNotFoundException`, `EOFException` e `UnknownHostException` estendono tutte `IOException`, una singola clausola `throws IOException` nella firma del metodo o un singolo blocco `catch (IOException e)` le cattura tutte in un colpo solo.
> Attenzione invece a `ClassNotFoundException`, `InterruptedException` e `SQLException`: **non** derivano da `IOException` e devono essere gestite o dichiarate separatamente.

### 13.8.1 I messaggi d'errore del compilatore e come interpretarli

Su un editor privo di aiuti, saper diagnosticare all'istante il messaggio del compilatore fa la differenza tra completare l'esercizio o sprecare tentativi:

#### 1. `unreported exception X; must be caught or declared to be thrown`
- **Causa**: Viene invocato un metodo che lancia la checked exception `X`, ma non lo si è racchiuso in un `try-catch` e non si è scritto `throws X` nella firma del metodo.
- **Rimedio**: Se la traccia richiede che il metodo propaghi l'errore, aggiungi `throws X` all'intestazione del metodo. Se il metodo deve essere autonomo, avvolgi la riga in un blocco `try-catch (X e)`.

#### 2. `exception X is never thrown in body of corresponding try statement`
- **Causa**: È stata inserita una clausola `catch (X e)` per una checked exception `X` (ad esempio `IOException`), ma dentro il rispettivo blocco `try` non c'è **nessuna istruzione** che dichiari di poter lanciare `X`. A differenza delle unchecked exception, il compilatore vieta blocchi `catch` per checked exception impossibili.
- **Rimedio**: Verificare di aver incluso nel blocco `try` l'istruzione che effettivamente compie l'operazione rischiosa, oppure rimuovere il `catch` superfluo.

---

## Come esce all'esame

Nei compiti scritti ufficiali del corso, le eccezioni sono protagoniste del secondo esercizio. Esaminiamo le tracce tipiche e i vincoli imposti.

### EXAM1 — Esercizio 2 (13 Punti)
- **Cosa chiedeva la traccia**: Creare una classe `GestoreEccezioni` con un metodo `public static void esegui(int n)`. In base al parametro `n`:
  - se `0`: lanciare una `Exception` generica e assicurarsi che a schermo venga stampato `"eccezione generica"`;
  - se `1`: lanciare una `IOException`, catturarla internamente, rilanciare una `RuntimeException` verso l'esterno e assicurarsi che venga stampato `"eccezione runtime"`;
  - se `2`: assicurarsi che venga stampato `"no eccezioni"`.
- **Concetti del capitolo necessari**: `throw`, `throws`, conversione da checked a unchecked, blocchi `catch` specifici, rilancio delle eccezioni.
- **Vincoli letterali imposti**: Utilizzo obbligatorio di **tutte e cinque le parole chiave** della gestione delle eccezioni (`try`, `catch`, `finally`, `throw`, `throws`).

### EXAM3 — Esercizio 2 (13 Punti — Appello dell'8 luglio 2026)
- **Cosa chiedeva la traccia**: 
  1. Definire la classe `Gestore`, con il metodo `verifica`, che riceve un parametro `int` e non restituisce nulla. Il metodo dichiara di poter propagare al chiamante un'eccezione controllata (`throws Exception`).
  2. Il comportamento richiesto in base al valore ricevuto:
     - `0`: viene lanciata un'eccezione generica, che il metodo stesso cattura; il messaggio è `eccezione generica` e nulla esce dal metodo;
     - `1`: viene lanciata una `IOException`, che il metodo cattura e converte in un'eccezione non controllata, la quale raggiunge il chiamante; il messaggio è `eccezione runtime`;
     - qualsiasi altro valore: nessuna eccezione, messaggio `no eccezioni`.
- **Concetti del capitolo necessari**: Sinergia tra le 5 parole chiave, ordine dei blocchi `catch`, inizializzazione di variabili prima del blocco di controllo, esecuzione di `finally` prima della propagazione verso l'esterno.
- **Vincoli letterali imposti**:
  - Utilizzo obbligatorio di **tutte e cinque le parole chiave**.
  - **La stampa del messaggio deve trovarsi tassativamente dentro il blocco `finally`, uno solo per tutti e tre i casi**.

---

## Scheletri da esame

Questi quattro scheletri rappresentano i modelli fondamentali da memorizzare ed essere in grado di digitare senza esitazioni.

### Scheletro 1 — Metodo con le 5 parole chiave e stampa nel `finally`
*Quando si usa:* quando la traccia impone tutte e cinque le parole chiave e una stampa unica nel `finally`. Si veda la sezione 13.7.2.

```java
import java.io.IOException;

class Stazione {
    // 'throws': dichiarazione dell'eccezione controllata che può uscire
    public void controlla(int canale) throws Exception {
        String esito = "lettura regolare";           // inizializzata PRIMA del try

        try {
            if (canale == 0) {
                throw new Exception("sensore muto");              // 'throw': generica, gestita qui
            } else if (canale == 1) {
                throw new IOException("rete non raggiungibile");  // 'throw': controllata
            }
        } catch (IOException e) {                    // prima il tipo più specifico
            esito = "guasto di rete";
            throw new RuntimeException(esito);       // checked -> unchecked, esce dal metodo
        } catch (Exception e) {                      // poi il tipo più generale
            esito = "guasto generico";
        } finally {
            System.out.println(esito);               // unica stampa, eseguita in tutti i casi
        }
    }
}
```
- **Eccezioni da dichiarare/gestire:** `throws Exception` nella firma; `IOException` ed `Exception` catturate nei due `catch`.
- **Import necessari:** `import java.io.IOException;`

---

### Scheletro 2 — Eccezione personalizzata controllata e non controllata
*Quando si usa:* Quando la traccia richiede di definire classi di eccezione per un dominio applicativo specifico.

```java
// Modello per ECCEZIONE CONTROLLATA (checked): obbligo di catch o throws
class OperazioneNonConsentitaException extends Exception {
    public OperazioneNonConsentitaException() {
        super();
    }

    public OperazioneNonConsentitaException(String message) {
        super(message); // Invia la descrizione alla superclasse Throwable
    }
}

// Modello per ECCEZIONE NON CONTROLLATA (unchecked): nessun obbligo sintattico
class ParametroErratoException extends RuntimeException {
    public ParametroErratoException() {
        super();
    }

    public ParametroErratoException(String message) {
        super(message);
    }
}
```
- **Import necessari:** Nessuno (stanno in `java.lang`).

---

### Scheletro 3 — Conversione da eccezione controllata a non controllata
*Quando si usa:* Quando si desidera interrompere l'esecuzione e segnalare un guasto al chiamante senza sporcare la firma del metodo con clausole `throws`.

```java
import java.io.IOException;

class Convertitore {
    public void eseguiOperazione() {
        try {
            // Operazione a rischio che dichiara una checked exception
            throw new IOException("Connessione interrotta dal server");
        } catch (IOException e) {
            // Conversione: incapsula l'eccezione originale come causa nella nuova RuntimeException
            throw new RuntimeException("Impossibile completare l'operazione: " + e.getMessage(), e);
        }
    }
}
```
- **Import necessari:** `import java.io.IOException;`

---

### Scheletro 4 — Chiusura classica dei flussi nel `finally` con guardia `null`
*Quando si usa:* Negli esercizi con file o socket in cui la traccia impone la chiusura esplicita nel blocco `finally`.

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

class GestoreFlussoDati {
    public String leggiPrimaRiga(String percorso) throws IOException {
        BufferedReader reader = null; // 1. Dichiarazione fuori dal blocco try
        try {
            reader = new BufferedReader(new FileReader(percorso)); // 2. Istanziazione dentro
            return reader.readLine();
        } finally {
            if (reader != null) { // 3. Guardia contro NullPointerException
                reader.close();   // 4. Chiusura sicura
            }
        }
    }
}
```
- **Import necessari:** `import java.io.BufferedReader;`, `import java.io.FileReader;`, `import java.io.IOException;`

---

## Errori tipici

> [!CAUTION]
> **Errore 1 — Confondere `throw` e `throws`**
> Scrivere `throw` nell'intestazione del metodo o `throws` nel corpo per lanciare un'istanza è un errore bloccante.
>
> ```java
> // ERRATO: non compila!
> public void salvaDati() throw IOException { // Errore: throw non si usa nella firma
>     throws new IOException();               // Errore: throws non si usa per lanciare oggetti
> }
> ```
>
> ```java
> // CORRETTO: firma con 'throws', corpo con 'throw'
> public void salvaDati() throws IOException {
>     throw new IOException("disco non disponibile");
> }
> ```

---

> [!CAUTION]
> **Errore 2 — Dichiarare la variabile da chiudere dentro il blocco `try`**
> Una variabile dichiarata all'interno del blocco `try` ha uno *scope* limitato alle relative parentesi graffe. Nel blocco `finally` la variabile non esiste.
>
> ```java
> // ERRATO: non compila!
> try {
>     BufferedReader in = new BufferedReader(new FileReader("file.txt"));
>     // uso di in...
> } finally {
>     in.close(); // Errore di compilazione: cannot find symbol: variable in
> }
> ```
>
> ```java
> // CORRETTO: dichiarata all'esterno, assegnata all'interno
> BufferedReader in = null;
> try {
>     in = new BufferedReader(new FileReader("file.txt"));
>     // uso di in...
> } finally {
>     if (in != null) {
>         in.close();
>     }
> }
> ```

---

> [!CAUTION]
> **Errore 3 — Invertire l'ordine dei blocchi `catch` mettendo prima la superclasse**
> Mettere un blocco `catch` generico prima di uno più specifico rende il secondo irraggiungibile.
>
> ```java
> // ERRATO: non compila!
> try {
>     throw new IOException("errore disco");
> } catch (Exception e) {          // Cattura tutto, inclusa IOException!
>     System.out.println("Errore generico");
> } catch (IOException e) {        // Errore: exception IOException has already been caught
>     System.out.println("Errore I/O");
> }
> ```
>
> ```java
> // CORRETTO: dal più specifico al più generale
> try {
>     throw new IOException("errore disco");
> } catch (IOException e) {        // Prima la sottoclasse
>     System.out.println("Errore I/O");
> } catch (Exception e) {          // Poi la superclasse
>     System.out.println("Errore generico");
> }
> ```

---

> [!CAUTION]
> **Errore 4 — Chiamare `close()` nel `finally` senza controllo `!= null`**
> Se l'apertura del flusso fallisce nel costruttore, la variabile rimane `null`. Chiamare `.close()` senza protezione genera una `NullPointerException` che distrugge e cancella l'eccezione originaria.
>
> ```java
> // ERRATO: maschera l'eccezione originaria!
> BufferedReader in = null;
> try {
>     in = new BufferedReader(new FileReader("file_inesistente.txt"));
> } finally {
>     in.close(); // Se il file non esiste, 'in' è null -> NullPointerException!
> }
> ```
>
> ```java
> // CORRETTO: controllo preventivo di nullità
> BufferedReader in = null;
> try {
>     in = new BufferedReader(new FileReader("file_inesistente.txt"));
> } finally {
>     if (in != null) {
>         in.close();
>     }
> }
> ```

---

> [!CAUTION]
> **Errore 5 — Catturare un'eccezione controllata che il blocco `try` non può lanciare**
> A differenza delle unchecked exception (che possono sempre manifestarsi), il compilatore rifiuta un blocco `catch` per una checked exception se nessuna istruzione nel `try` la dichiara.
>
> ```java
> // ERRATO: non compila!
> try {
>     int a = 10;
>     int b = 20;
>     System.out.println(a + b);
> } catch (IOException e) { // Errore: exception IOException is never thrown in body of corresponding try statement
>     System.out.println("Errore I/O");
> }
> ```
>
> ```java
> // CORRETTO: catturare solo eccezioni effettivamente generate o unchecked
> try {
>     int a = 10;
>     int b = 20;
>     System.out.println(a + b);
> } catch (RuntimeException e) { // Lecito: unchecked exceptions ammesse ovunque
>     System.out.println("Errore runtime");
> }
> ```

---

> [!CAUTION]
> **Errore 6 — Allargare le eccezioni controllate nell'overriding**
> Quando si sovrascrive un metodo, la firma del metodo derivato non può dichiarare checked exception nuove o gerarchicamente superiori a quelle della superclasse.
>
> ```java
> class Padre {
>     public void elabora() throws IOException {}
> }
>
> // ERRATO: non compila!
> class Figlio extends Padre {
>     @Override
>     public void elabora() throws Exception { // Errore: overridden method does not throw Exception
>     }
> }
> ```
>
> ```java
> // CORRETTO: stesso tipo, sottotipo (es. FileNotFoundException) o nessuna eccezione
> import java.io.IOException;
>
> class PadreCorretto {
>     public void elabora() throws IOException {}
> }
>
> class Figlio extends PadreCorretto {
>     @Override
>     public void elabora() throws IOException {
>     }
> }
> ```

---

> [!CAUTION]
> **Errore 7 — Non inizializzare la variabile stampata nel `finally`**
> Se nel `try` o nel `catch` viene rilanciata un'eccezione, il compilatore verifica che le variabili lette nel `finally` abbiano ricevuto un valore su ogni possibile percorso di esecuzione.
>
> ```java
> // ERRATO: non compila!
> public void verifica(int n) {
>     String messaggio; // Non inizializzata!
>     try {
>         if (n == 0) throw new Exception();
>         messaggio = "ok";
>     } catch (Exception e) {
>         // Se l'eccezione si verifica, messaggio rimane senza valore!
>     } finally {
>         System.out.println(messaggio); // Errore: variable messaggio might not have been initialized
>     }
> }
> ```
>
> ```java
> // CORRETTO: inizializzare la variabile alla dichiarazione
> public void verifica(int n) {
>     String messaggio = "predefinito";
>     try {
>         if (n == 0) throw new Exception();
>         messaggio = "ok";
>     } catch (Exception e) {
>         messaggio = "errore";
>     } finally {
>         System.out.println(messaggio);
>     }
> }
> ```

---

> [!CAUTION]
> **Errore 8 — Stampare nei blocchi `catch` quando la traccia impone la stampa nel `finally`**
> Quando la traccia chiede che la stampa del messaggio si trovi in un unico blocco `finally`, inserire `System.out.println(...)` dentro i singoli blocchi `catch` viola il vincolo architetturale e fa perdere punti anche se l'output a video coincide.
>
> ```java
> // ERRATO: stampa collocata dentro il blocco catch, contro il vincolo della traccia
> try {
>     throw new IOException("guasto");
> } catch (IOException e) {
>     System.out.println("guasto di rete");            // VIETATO DALLA TRACCIA
>     throw new RuntimeException("guasto di rete");
> }
> ```
>
> ```java
> // CORRETTO: memorizzare il messaggio nella variabile e stampare SOLO nel finally
> String esito = "lettura regolare";
> try {
>     throw new IOException("guasto");
> } catch (IOException e) {
>     esito = "guasto di rete";
>     throw new RuntimeException(esito);               // il finally stampa prima che l'eccezione esca
> } finally {
>     System.out.println(esito);                       // unica stampa per tutti i casi
> }
> ```

---

> [!CAUTION]
> **Errore 9 — Blocco `catch` completamente vuoto (*eccezione ingoiata*)**
> Catturare un'eccezione senza compiere alcuna azione (né loggare, né rilanciare, né impostare uno stato di errore) nasconde completamente il malfunzionamento. Il programma continuerà a girare in uno stato corrotto, rendendo impossibile diagnosticare il guasto.
>
> ```java
> // ERRATO: l'errore scompare nel nulla senza lasciare traccia
> try {
>     throw new IOException("lettura fallita");
> } catch (IOException e) {
>     // Blocco vuoto: pessima pratica!
> }
> ```
>
> ```java
> // CORRETTO: gestire esplicitamente o rilanciare come unchecked
> try {
>     throw new IOException("lettura fallita");
> } catch (IOException e) {
>     throw new RuntimeException("Lettura fallita", e);
> }
> ```

---

> [!CAUTION]
> **Errore 10 — Usare il `try-with-resources` quando la traccia impone la parola chiave `finally`**
> Anche se nella pratica professionale moderna il `try-with-resources` è preferito per la chiusura automatica dei flussi, all'esame scritto il rispetto dei vincoli letterali è primario. Se la traccia chiede di utilizzare tutte e 5 le parole chiave o impone la chiusura nel `finally`, il `try-with-resources` non rispetta la traccia.
>
> ```java
> // ERRATO in presenza del vincolo: 'finally' non compare nel codice!
> try (BufferedReader in = new BufferedReader(new FileReader("dati.txt"))) {
>     String riga = in.readLine();
> }
> ```
>
> ```java
> // CORRETTO secondo il vincolo: uso esplicito di finally
> BufferedReader in = null;
> try {
>     in = new BufferedReader(new FileReader("dati.txt"));
>     String riga = in.readLine();
> } finally {
>     if (in != null) {
>         in.close();
>     }
> }
> ```

---

## Riassunto

Il sistema delle eccezioni di Java è un meccanismo orientato agli oggetti progettato per separare in modo rigoroso la logica di calcolo ordinaria dalla gestione degli eventi anomali. Qualsiasi anomalia è rappresentata da un'istanza di una classe derivata da `java.lang.Throwable`. La gerarchia distingue categoricamente tra `Error` (guasti irreversibili della JVM che non vanno catturati) ed `Exception` (anomalie applicative). All'interno di `Exception`, le **Checked Exceptions** (come `IOException` o `InterruptedException`) rappresentano problemi ambientali esterni e sono soggette all'obbligo vincolante del compilatore *Catch or Declare*; le **Unchecked Exceptions** (sottoclassi di `RuntimeException`, come `NullPointerException` o `ArithmeticException`) rappresentano errori logici del programmatore e non richiedono dichiarazioni obbligatorie.

La gestione si articola attorno a cinque parole chiave sincronizzate: `try` delimita il codice protetto; `catch` cattura le eccezioni specificate (con l'obbligo di ordinare i blocchi dal tipo più specifico al più generale); `finally` garantisce l'esecuzione di codice di pulizia e notifica in qualunque scenario, persino prima che un'eccezione rilanciata abbandoni il metodo o dopo un `return`; `throw` esegue il lancio materiale di un'istanza; `throws` dichiara nell'intestazione del metodo quali checked exception possono propagarsi al chiamante (con la regola di ereditarietà che vieta a una sottoclasse di allargare le eccezioni controllate).

### Concetti chiave
- **Eccezione come oggetto**: in Java le anomalie non sono codici di ritorno numerici ma oggetti ricchi di informazioni sullo stato dell'errore, istanziabili ed ereditabili.
- **Checked vs Unchecked**: le checked obbligano a `try-catch` o `throws` a pena di mancata compilazione; le unchecked (`RuntimeException`) si propagano liberamente senza vincoli sintattici.
- **`throw` contro `throws`**: `throw` è un'istruzione imperativa nel corpo del metodo che riceve un'**istanza**; `throws` è una clausola nella firma che dichiara **classi/tipi**.
- **Regola di override per `throws`**: un metodo sovrascritto in una sottoclasse può restringere o eliminare le checked exception dichiarate, ma non può mai dichiararne di nuove o più generali.
- **Ordine dei blocchi `catch`**: sempre dal sottotipo più specifico al supertipo più generale, altrimenti il compilatore rileva codice irraggiungibile.
- **Garanzia del blocco `finally`**: viene eseguito sempre, sia in caso di successo sia in caso di eccezione (anche se rilanciata o non gestita), e precede l'uscita da istruzioni di salto come `return`.
- **Chiusura a 4 passi**: dichiarazione fuori a `null`, apertura nel `try`, controllo difensivo `if (in != null)` nel `finally` e invocazione protetta di `.close()`.
- **Eccezioni personalizzate**: si estende `Exception` (per checked) o `RuntimeException` (per unchecked), fornendo almeno il costruttore di default e quello con parametro `String message` che delega a `super(message)`. Non si riscrive `getMessage()`.
- **Rilancio e conversione**: intercettare una checked e rilanciare una `RuntimeException` consente di propagare l'errore senza costringere i chiamanti ad aggiungere clausole `throws`.

### API ed elementi essenziali

| Classe / Elemento | Tipo / Modificatore | Firma o Costrutto | Descrizione |
|---|---|---|---|
| `Throwable` | Classe (`java.lang`) | `public String getMessage()` | Restituisce la descrizione testuale dell'errore. |
| `Throwable` | Metodo (`java.lang`) | `public void printStackTrace()` | Stampa la traccia dello stack delle chiamate su `System.err`. |
| `Throwable` | Costruttore (`java.lang`) | `public Throwable(String msg, Throwable cause)` | Costruttore con descrizione e causa per eccezioni concatenate. |
| `Exception` | Classe (`java.lang`) | `public class MiaEx extends Exception` | Superclasse per la definizione di eccezioni **controllate** (*checked*). |
| `RuntimeException`| Classe (`java.lang`) | `public class MiaEx extends RuntimeException` | Superclasse per la definizione di eccezioni **non controllate** (*unchecked*). |
| `try-catch-finally`| Istruzione di controllo | `try { ... } catch (E e) { ... } finally { ... }` | Struttura completa di protezione, gestione ed esecuzione garantita. |
| `throw` | Parola chiave | `throw espressioneOggetto;` | Lancia un'istanza di eccezione interrompendo il flusso corrente. |
| `throws` | Parola chiave | `void metodo() throws Tipo1, Tipo2` | Dichiara nella firma del metodo le checked exception propagate. |
| `AutoCloseable` | Interfaccia (`java.lang`) | `void close() throws Exception` | Interfaccia richiesta dagli oggetti gestiti tramite `try-with-resources`. |
