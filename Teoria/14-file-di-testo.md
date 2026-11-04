---
materia: Programmazione a Oggetti
capitolo: 14
titolo: File di testo
livello_syllabus: 4
stato: completo
slide: ["Savitch cap. 14 slide 1-27"]
appelli: []
fonti_esterne: 8
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 14 — File di testo

## Di cosa parla questo capitolo

Finora i nostri programmi hanno parlato con il mondo attraverso due canali soltanto: la tastiera (con `Scanner`, [Capitolo 3](03-stringhe-e-console.md)) e lo schermo (con `System.out`). Sono canali effimeri: quando il programma termina, tutto ciò che contenevano sparisce. Per un programma vero questo non basta. Un registro di vendite, un elenco di nomi, la configurazione di un'applicazione devono sopravvivere alla chiusura del programma e poter essere letti da un altro programma, o dallo stesso programma la volta successiva. Per questo esistono i **file**.

In questo capitolo impariamo a scrivere e a leggere i **file di testo**, cioè i file che contengono caratteri leggibili da una persona con un normale editor. Vedremo:

- che cos'è un **flusso** (*stream*) e perché in Java ogni scambio di dati con l'esterno passa da un oggetto di questo tipo, e in che cosa un flusso di caratteri differisce da un flusso di byte;
- come **scrivere** un file con `PrintWriter` (sovrascrivendo e accodando), e perché è indispensabile chiuderlo;
- come **leggere** un file con `Scanner` e con `BufferedReader`, e come riconoscere la fine del file;
- la classe `File`, che rappresenta il *nome* di un file e permette di interrogare il file system;
- come scomporre le righe di un file **CSV** (valori separati da virgola) con `split`;
- gli **scheletri** di codice da saper scrivere a memoria su un editor senza aiuti, e gli errori che compilatore e test nascosto puniscono.

Il capitolo si appoggia su tre capitoli precedenti. Le **eccezioni controllate** ([Capitolo 13](13-eccezioni.md)) sono ovunque: quasi ogni costruttore e metodo di questo capitolo dichiara `throws FileNotFoundException` o `throws IOException`, e il compilatore ci obbliga a gestirle. Il metodo `split` e il `Scanner` sono del [Capitolo 3](03-stringhe-e-console.md). Il `finally` con la chiusura sicura delle risorse è la sezione 13.5.3 del [Capitolo 13](13-eccezioni.md), che qui applichiamo di continuo. Il capitolo successivo ([Capitolo 15](15-stream-binari-e-serializzazione.md)) tratta l'altra metà del mondo dei file: i file binari e gli oggetti serializzati.

> [!IMPORTANT]
> **Nota per l'esame — Il file come tema dell'esercizio sulle API**
> Lettura e scrittura di file fanno parte delle API di base su cui si basa il secondo esercizio della prova scritta (13 punti), insieme a eccezioni, serializzazione, socket, XML e JDBC. La traccia può imporre una **struttura precisa**: aprire il file in un certo modo (sovrascrivendo o accodando), chiudere i flussi in un blocco `finally`, leggere fino alla fine del file, stampare un output in un formato fissato. Un programma che produce il risultato giusto ma con una struttura diversa da quella richiesta perde punti. Per questo il capitolo insiste sulle **forme esatte**: firme, eccezioni da dichiarare, `import`.

---

## 14.1 Flussi e file

### 14.1.1 Perché serve un file

Una variabile vive nella memoria centrale (RAM) finché il programma è in esecuzione. Appena il programma finisce, la memoria viene restituita al sistema operativo e i valori sono persi. L'input da tastiera e l'output su schermo condividono questo carattere temporaneo: ciò che l'utente digita è usato e dimenticato, ciò che il programma stampa scorre via.

Un **file** è un contenitore di dati che vive su un supporto permanente (disco, memoria flash) ed è identificato da un **nome** all'interno di un'organizzazione a cartelle chiamata *file system*. I dati scritti in un file restano dopo la fine del programma, e il programma può riaprirli la volta successiva oppure lasciarli a un altro programma.

### 14.1.2 Il flusso

Tra il programma e il file ci sono due mondi con regole diverse: il programma lavora con oggetti e variabili, il file è una sequenza di byte sul disco. Per metterli in comunicazione, Java usa un'astrazione che già conosciamo senza averle dato il nome: il **flusso**.

> [!NOTE]
> **Definizione — Flusso (*stream*)**
> Un flusso è una sequenza ordinata di dati in movimento tra il programma e un'altra entità (la tastiera, lo schermo, un file, un'altra macchina in rete). Un flusso che porta dati *verso* il programma è un flusso di **input**; uno che li porta *fuori* dal programma è un flusso di **output**. I dati possono essere caratteri, numeri o byte.

Pensiamo a un tubo: da una parte c'è la sorgente (o la destinazione), dall'altra il nostro programma, e i dati scorrono in un solo verso, nell'ordine in cui sono stati messi. Un flusso si legge o si scrive in avanti, un elemento dopo l'altro; per rileggere ciò che è già passato bisogna riaprirlo.

I flussi sono **oggetti** di classi speciali, quasi tutte nel package `java.io`. Lo `Scanner` collegato a `System.in` è un oggetto flusso; lo è anche `System.out` (un `PrintStream`). Quando collegheremo uno `Scanner` o un `PrintWriter` a un file, non cambierà il modo di usarli: cambierà solo l'oggetto a cui sono collegati. È la ragione per cui quanto imparato sulla console ([Capitolo 3](03-stringhe-e-console.md)) torna utile quasi senza modifiche.

### 14.1.3 File di testo e file binari

Tutti i dati di un file sono, in fondo, sequenze di zeri e di uni. Quello che distingue le due grandi famiglie di file è come quelle sequenze vanno interpretate.

> [!NOTE]
> **Definizione — File di testo e file binario**
> Un **file di testo** è un file interpretato come una sequenza di **caratteri**: lo si può aprire con un editor di testo, leggere e modificare. Il codice sorgente Java è un file di testo. Tutti gli altri file sono **file binari** (un filmato, un brano musicale, un'immagine, un oggetto salvato in forma serializzata): per leggerli serve un programma specifico che ne conosca il formato.

Un esempio fa capire la differenza. Il numero intero `12345`, scritto in un file di testo, occupa **cinque caratteri**: la cifra `1`, la cifra `2`, e così via. Per leggerlo, un altro programma deve riconvertire quei cinque caratteri in un numero. Scritto in un file binario con il metodo `writeInt` ([Capitolo 15](15-stream-binari-e-serializzazione.md)), lo stesso numero occupa **quattro byte**, nella sua forma interna di `int`, e la riconversione è immediata. Il file di testo è più ingombrante e più lento da interpretare, ma è leggibile da chiunque; il file binario è compatto ma opaco.

Questo capitolo tratta solo i file di testo. I file binari e la serializzazione sono nel [Capitolo 15](15-stream-binari-e-serializzazione.md).

### 14.1.4 Flussi di caratteri e flussi di byte

Java divide le classi di input/output in due grandi famiglie, e distinguerle è una domanda classica.

> [!NOTE]
> **Definizione — Flussi di byte e flussi di caratteri**
> Un **flusso di byte** lavora con byte grezzi, senza interpretarli: serve per immagini, audio, eseguibili, oggetti serializzati. Le sue classi di base sono `InputStream` e `OutputStream`, per esempio `FileInputStream` e `FileOutputStream`.
> Un **flusso di caratteri** lavora con caratteri Unicode (`char`) e si occupa da solo di convertire i caratteri in byte (in scrittura) e i byte in caratteri (in lettura) secondo una *codifica*, per esempio UTF-8. Le sue classi di base sono `Reader` e `Writer`, per esempio `FileReader` e `FileWriter`.

La regola pratica è semplice: **testo con `Reader`/`Writer`, dati binari con `InputStream`/`OutputStream`**. Usare un flusso di caratteri su un file binario ne corrompe i dati, perché il flusso tenta di interpretare come testo byte che testo non sono.

| Compito | Classi tipiche | Famiglia |
|---|---|---|
| Scrivere testo in un file | `PrintWriter`, `FileWriter`, `BufferedWriter` | caratteri (`Writer`) |
| Leggere testo da un file | `Scanner`, `FileReader`, `BufferedReader` | caratteri (`Reader`) |
| Scrivere/leggere byte o oggetti | `FileOutputStream`, `FileInputStream`, `ObjectOutputStream`, `ObjectInputStream` | byte ([Capitolo 15](15-stream-binari-e-serializzazione.md)) |

> [!NOTE]
> **Approfondimento esterno — `FileReader` e `FileWriter`: caratteri, byte e codifica**
> La documentazione ufficiale descrive `FileReader` come la classe per leggere testo da file di caratteri («*meant for reading streams of characters*») e rimanda a `FileInputStream` per i flussi di byte grezzi; allo stesso modo `FileWriter` serve per scrivere testo e rimanda a `FileOutputStream` per i byte. La conversione tra byte e caratteri usa una codifica indicata esplicitamente (esistono costruttori con un `Charset`, per esempio `FileWriter(String fileName, Charset charset)` dalla versione 11) oppure, se non è indicata, la **codifica predefinita della piattaforma** (*platform's default charset*).
> In pratica: un file con lettere accentate letto su un sistema con una codifica predefinita diversa da quella con cui fu scritto può mostrare caratteri sbagliati.
>
> *Fonte:* [FileReader (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileReader.html) e [FileWriter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileWriter.html)

### 14.1.5 Avvolgere un flusso in un altro

Le classi di `java.io` hanno compiti molto specifici e **si combinano**. Una classe come `FileReader` sa collegarsi a un file e leggerne i caratteri, ma non sa leggere una riga intera. Una classe come `BufferedReader` sa leggere una riga intera, ma non sa da dove arrivino i caratteri: li prende da un altro flusso che le viene consegnato nel costruttore. Per avere entrambe le capacità si **avvolge** un flusso nell'altro:

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Avvolgere {
    public static void main(String[] args) throws IOException {
        FileReader grezzo = new FileReader("note.txt");       // sa leggere i caratteri del file
        BufferedReader comodo = new BufferedReader(grezzo);   // sa leggere una riga alla volta
        System.out.println(comodo.readLine());
        comodo.close();
    }
}
```

Supponiamo che `note.txt` inizi con la riga `prima riga`. L'output è:

```text
prima riga
```

Riga per riga. `new FileReader("note.txt")` apre il file e crea un flusso di caratteri collegato. `new BufferedReader(grezzo)` crea un secondo oggetto che *contiene* il primo e aggiunge due cose: una **memoria temporanea** (*buffer*) in cui preleva i caratteri a blocchi, invece di andare al disco a ogni carattere, e il metodo `readLine()`. Chi usa `comodo` parla sempre e solo con `comodo`; `grezzo` lavora dietro le quinte. Si scrive quasi sempre in un'unica espressione, `new BufferedReader(new FileReader("note.txt"))`, ed è la forma che incontreremo nel resto del capitolo.

La stessa idea vale in scrittura: `new PrintWriter(new FileWriter("a.txt", true))` è un `PrintWriter` (che sa stampare con `println`) avvolto attorno a un `FileWriter` (che sa scrivere i caratteri su file, in coda). Quando si legge un'espressione di questo tipo si procede **dall'interno verso l'esterno**: prima la sorgente o la destinazione, poi le capacità aggiunte.

> [!TIP]
> **Intuizione — Un tubo e i suoi raccordi**
> Il file è un serbatoio, il programma è l'utilizzatore. `FileReader` è un tubo semplice che arriva fino al serbatoio; `BufferedReader` è un raccordo con un piccolo serbatoio intermedio e un rubinetto che eroga una riga per volta. L'analogia ha un limite: i raccordi di `java.io` si possono sovrapporre in molti modi, ma ognuno aggiunge una sola capacità e il flusso sottostante deve rimanere raggiungibile per essere chiuso.

### 14.1.6 Le eccezioni dei flussi su file

Un file è una risorsa del mondo esterno, e il mondo esterno può rifiutarsi: il file potrebbe non esistere, essere in una cartella inesistente, essere protetto, occupare un disco pieno. Per questo la quasi totalità dei costruttori e dei metodi di `java.io` che toccano il disco dichiara eccezioni **controllate** ([Capitolo 13](13-eccezioni.md)): `FileNotFoundException` o la sua superclasse `IOException`. Il compilatore non lascia passare codice che le ignori. Il messaggio tipico è

```text
error: unreported exception FileNotFoundException; must be caught or declared to be thrown
```

e le soluzioni sono le due che già conosciamo: racchiudere il codice in `try`/`catch` oppure aggiungere `throws` alla firma del metodo. Nel seguito indicheremo, per ogni costruttore e metodo, **quale** eccezione dichiara, perché è l'informazione da cui dipende il codice che si scrive intorno.

---

## 14.2 Scrivere un file di testo

### 14.2.1 `PrintWriter` su un file

La classe più comoda per scrivere testo è `PrintWriter`, del package `java.io`. Ha gli stessi metodi di stampa di `System.out`: `print`, `println`, `printf`. Per scrivere in un file basta passare al costruttore il **nome del file**:

```text
public PrintWriter(String fileName) throws FileNotFoundException
```

L'ordine delle operazioni è sempre lo stesso: si **dichiara** una variabile per il flusso, si **apre** il file creando il `PrintWriter`, si **scrive**, si **chiude**. Tutto questo va dentro un `try`, perché il costruttore dichiara `FileNotFoundException`.

```java
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class ScriviSpesa {
    public static void main(String[] args) {
        try {
            PrintWriter out = new PrintWriter("spesa.txt"); // apre (o crea) spesa.txt
            out.println("pane");                            // scrive una riga
            out.println("latte");
            out.println("uova");
            out.close();                                    // svuota il buffer e chiude il file
            System.out.println("File spesa.txt scritto.");
        } catch (FileNotFoundException e) {
            System.out.println("Impossibile creare il file.");
        }
    }
}
```

L'output sullo schermo è:

```text
File spesa.txt scritto.
```

e il file `spesa.txt`, creato nella cartella da cui si lancia il programma, contiene tre righe:

```text
pane
latte
uova
```

Riga per riga. L'`import` porta le due classi di cui abbiamo bisogno: `PrintWriter` e l'eccezione. `new PrintWriter("spesa.txt")` ha un doppio effetto: se il file non esiste lo **crea** (vuoto), se esiste lo **svuota** (ne torneremo nella sezione 14.2.5). Da quel momento `out` rappresenta il file: `out.println("pane")` scrive `pane` seguito da un a capo, esattamente come `System.out.println` farebbe sullo schermo. Con `out.close()` si dice a Java che abbiamo finito. Il blocco `catch` gestisce il caso in cui il file non si possa creare; il messaggio che stampiamo è nostro, e il programma termina normalmente.

Un file ha quindi **due nomi** nel programma. Uno è il nome che il sistema operativo conosce (`"spesa.txt"`, una stringa passata al costruttore); l'altro è il nome della variabile (`out`), con cui il programma si riferisce al flusso aperto. Sono cose diverse e non vanno confuse: il nome della variabile non ha alcun legame con il nome del file.

> [!NOTE]
> **Approfondimento esterno — `PrintWriter(String fileName)`**
> Dalla documentazione: il costruttore `public PrintWriter(String fileName) throws FileNotFoundException` crea un `PrintWriter` *senza svuotamento automatico a ogni riga* («*without automatic line flushing*») con il nome di file indicato. Se il file esiste, viene **troncato a zero byte**; altrimenti ne viene creato uno nuovo; l'output è memorizzato in un buffer. L'eccezione `FileNotFoundException` viene lanciata se il nome non indica un file regolare scrivibile esistente e non se ne può creare uno nuovo, oppure se si verifica un altro errore nell'apertura o nella creazione del file.
> Il costruttore esiste anche nelle forme `PrintWriter(File file)` e `PrintWriter(OutputStream out)`; con il costruttore `PrintWriter(Writer out)` si può avvolgere un altro flusso di caratteri.
>
> *Fonte:* [PrintWriter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/PrintWriter.html)

### 14.2.2 Il buffer e l'importanza di `close`

Scrivere sul disco è molto più lento che scrivere in memoria. Per non rallentare il programma a ogni `println`, `PrintWriter` raccoglie i caratteri in un **buffer** in memoria e li manda al file a blocchi: quando il buffer è pieno, oppure quando glielo si chiede. Chiudere il flusso con `close()` fa due cose: **svuota** il buffer, cioè manda al file tutto ciò che vi era rimasto, e **scollega** il flusso dal file.

La conseguenza è che *se non si chiude (o non si svuota) il flusso, parte dei dati, o tutti, non arrivano nel file*. Lo vediamo misurando la lunghezza del file mentre scriviamo:

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class BufferVisibile {
    public static void main(String[] args) throws FileNotFoundException {
        PrintWriter out = new PrintWriter("buffer.txt");
        out.println("prima riga");
        out.println("seconda riga");
        File f = new File("buffer.txt");
        System.out.println("byte prima di flush: " + f.length());
        out.flush();                                   // manda al file quanto c'e' nel buffer
        System.out.println("byte dopo flush: " + f.length());
        out.println("terza riga");
        out.close();                                   // svuota e chiude
        System.out.println("byte dopo close: " + f.length());
    }
}
```

L'output (su un sistema in cui l'a capo occupa un byte, come macOS e Linux) è:

```text
byte prima di flush: 0
byte dopo flush: 24
byte dopo close: 35
```

Le due righe scritte prima dell'interrogazione sono ancora nel buffer: sul disco il file è vuoto (0 byte). `flush()` le manda al file: `prima riga` (10 caratteri) più l'a capo fa 11 byte, `seconda riga` (12) più l'a capo fa 13, in totale 24. L'ultima riga (11 byte) arriva solo con `close()`, che porta il totale a 35. La classe `File` e il suo metodo `length()` sono presentati nella sezione 14.5.

Se invece il programma finisce senza chiamare né `flush` né `close`, **il buffer non viene scaricato**: il file rimane quello che era (vuoto, se era appena stato creato). È l'errore più insidioso di questo argomento, perché il programma gira senza alcun messaggio e semplicemente non scrive (vedi *Errore 3* in fondo al capitolo).

> [!IMPORTANT]
> **Nota per l'esame — `close()` è parte della traccia**
> All'esame non si vede il file che il programma produce: si vede soltanto se il test nascosto, che lo rilegge, trova ciò che si aspetta. Un flusso di scrittura non chiuso lascia il file incompleto o vuoto, e il test fallisce senza che compaia alcun errore. Ogni apertura in scrittura deve avere una chiusura corrispondente, e quando la traccia dice «nel blocco `finally`» la chiusura va in quel blocco (sezione 14.2.6).

### 14.2.3 I metodi di `PrintWriter`

`PrintWriter` offre un sottoinsieme dei metodi che già usiamo con `System.out`. Quelli che servono all'esame sono questi:

| Metodo | Che cosa fa |
|---|---|
| `void print(String s)` e le altre versioni (`int`, `double`, `boolean`, `char`, `Object`) | scrive il valore senza andare a capo |
| `void println(String s)` e le altre versioni; `void println()` | scrive il valore e va a capo (la versione senza argomenti scrive solo l'a capo) |
| `PrintWriter printf(String format, Object... args)` e `printf(Locale l, String format, Object... args)` | scrive un testo formattato ([Capitolo 3](03-stringhe-e-console.md), sezione 3.6.3) |
| `void flush()` | manda al file il contenuto del buffer |
| `void close()` | svuota il buffer e chiude il flusso |
| `boolean checkError()` | svuota il buffer e dice se si è verificato un errore di scrittura |

Un esempio con tre dei metodi in una stessa scrittura:

```java
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Locale;

public class ScriviScheda {
    public static void main(String[] args) throws FileNotFoundException {
        PrintWriter out = new PrintWriter("scheda.txt");
        out.print("Articolo: ");                            // niente a capo
        out.println("penna");                               // ora si', a capo
        out.println("Quantita: " + 3);
        out.printf(Locale.US, "Prezzo: %.2f%n", 1.2);       // %n e' l'a capo di printf
        out.close();
        System.out.println("Scheda scritta.");
    }
}
```

Sullo schermo compare `Scheda scritta.`, e dopo l'esecuzione il file `scheda.txt` contiene:

```text
Articolo: penna
Quantita: 3
Prezzo: 1.20
```

`Locale.US` serve a fissare il punto come separatore decimale, in modo che il risultato non dipenda dalle impostazioni del computer; senza `Locale`, su un sistema italiano si otterrebbe `1,20`. Notiamo anche che `main` dichiara `throws FileNotFoundException`: è la scelta più rapida quando il metodo non deve gestire l'errore, come spiegato nel [Capitolo 13](13-eccezioni.md).

C'è una particolarità che distingue `PrintWriter` dagli altri flussi di scrittura. I suoi metodi `print`, `println`, `printf`, `flush` e `close` **non dichiarano nessuna eccezione**: quindi non è necessario un `catch` per le scritture. Gli eventuali errori di scrittura non vengono segnalati con un'eccezione: il flusso li registra e il programma può interrogarli con `checkError()`.

> [!NOTE]
> **Approfondimento esterno — `PrintWriter`, errori e svuotamento**
> Dalla documentazione: i metodi di `PrintWriter` non lanciano `IOException`; il programma deve invece chiamare `checkError()` per sapere se si è verificato un errore. `checkError()` svuota il flusso se non è chiuso e restituisce `true` se il flusso ha incontrato un errore, sia nel flusso sottostante sia durante una conversione di formato. `close()` chiude il flusso e rilascia le risorse; chiuderlo una seconda volta non ha effetto. I costruttori `PrintWriter(Writer out, boolean autoFlush)` e `PrintWriter(OutputStream out, boolean autoFlush)` hanno un secondo parametro che, se `true`, fa svuotare il buffer a ogni `println`, `printf` o `format`.
>
> *Fonte:* [PrintWriter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/PrintWriter.html)

### 14.2.4 Quando l'apertura fallisce

Il costruttore `PrintWriter(String)` dichiara `FileNotFoundException` anche se stiamo *scrivendo*: il nome è fuorviante, ma l'eccezione dice semplicemente «non sono riuscito ad aprire (o creare) quel file». La causa più comune è una cartella che non esiste: Java crea il file, ma non crea le cartelle del percorso.

```java
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class CartellaMancante {
    public static void main(String[] args) {
        try {
            PrintWriter out = new PrintWriter("archivio/dati.txt");
            out.println("ciao");
            out.close();
            System.out.println("Scrittura riuscita.");
        } catch (FileNotFoundException e) {
            System.out.println("Errore: " + e.getMessage());
        }
    }
}
```

Se la cartella `archivio` non esiste, l'output è:

```text
Errore: archivio/dati.txt (No such file or directory)
```

Il testo tra parentesi dipende dal sistema operativo (su Windows è, ad esempio, «Impossibile trovare il percorso specificato»); per questo, quando l'output è fissato dalla traccia, si stampa un messaggio scritto da noi invece di `e.getMessage()`. Notiamo anche che, quando il costruttore lancia l'eccezione, l'assegnazione a `out` **non avviene** e la variabile non contiene un flusso: tornerà utile nella sezione 14.2.6.

### 14.2.5 Sovrascrivere e informare l'utente

Aprire un file in scrittura ha due conseguenze che conviene tenere sempre presenti:

- *Aprire un file in scrittura lo svuota.* Se il file esisteva già, il suo contenuto precedente è perso nel momento stesso in cui si esegue `new PrintWriter(...)`, prima di qualunque `println`. Non c'è nessun avviso. Quando serve conservare quanto già presente, bisogna aprire il file in modalità di aggiunta (sezione 14.3).
- *Un programma che lavora con i file non dovrebbe essere «silenzioso».* Un messaggio sullo schermo («File spesa.txt scritto.») dice all'utente che l'operazione è stata fatta; un `catch` che stampa il motivo del fallimento gli dice perché non è riuscita.

### 14.2.6 Chiudere nel `finally`

Negli esempi precedenti la chiamata `out.close()` è dentro il `try`, subito dopo le scritture. Se una scrittura andasse storta e il programma saltasse al `catch`, quella chiamata non verrebbe eseguita. Il `finally` esiste proprio per questo: il suo contenuto viene eseguito **sempre**. Lo schema è quello a quattro passi del [Capitolo 13](13-eccezioni.md) (sezione 13.5.3): dichiarare il flusso **fuori** dal `try` inizializzato a `null`, aprirlo **dentro** il `try`, e nel `finally` chiuderlo dopo aver controllato che non sia `null`.

```java
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class Quadrati {
    public static void main(String[] args) {
        PrintWriter out = null;                       // passo 1: fuori dal try, a null
        try {
            out = new PrintWriter("quadrati.txt");    // passo 2: apertura dentro il try
            for (int i = 1; i <= 5; i++) {
                out.println(i + " " + i * i);
            }
            System.out.println("Quadrati scritti.");
        } catch (FileNotFoundException e) {
            System.out.println("File non creato: " + e.getMessage());
        } finally {
            if (out != null) {                        // passo 3: guardia contro null
                out.close();                          // passo 4: chiusura
            }
        }
    }
}
```

L'output è:

```text
Quadrati scritti.
```

e `quadrati.txt` contiene:

```text
1 1
2 4
3 9
4 16
5 25
```

La guardia `if (out != null)` è necessaria perché, se il costruttore lancia `FileNotFoundException`, `out` è ancora `null` e `out.close()` provocherebbe una `NullPointerException` che nasconde l'errore vero. Una particolarità di `PrintWriter` rispetto agli altri flussi che incontreremo: `close()` **non dichiara eccezioni**, quindi nel `finally` non serve un secondo `try`. Per `BufferedWriter` o `BufferedReader`, invece, `close()` dichiara `IOException` e va gestito (sezioni 14.2.7 e 14.4.2).

> [!WARNING]
> **Attenzione — `try`-with-resources e `finally` imposto dalla traccia**
> Dalla versione 7 di Java esiste il `try`-with-resources, che chiude da solo le risorse senza `finally` (sezione 13.5.4 del [Capitolo 13](13-eccezioni.md)). È una forma valida e comoda, ma se la traccia dice che la chiusura dei flussi deve avvenire nel blocco `finally`, o impone l'uso di tutte le parole chiave delle eccezioni, il `try`-with-resources **non rispetta il vincolo**: il `finally` non compare nel sorgente. Nei programmi in cui la struttura è libera si può usare; quando è imposta, si scrive lo schema a quattro passi.

### 14.2.7 Alternativa: `FileWriter` e `BufferedWriter`

`PrintWriter` non è l'unico modo di scrivere testo. Le classi `FileWriter` e `BufferedWriter` fanno lo stesso lavoro con un'interfaccia diversa, e conviene conoscerle perché in molti testi e in molte tracce compaiono.

```text
public FileWriter(String fileName) throws IOException
public BufferedWriter(Writer out)
public void write(String str) throws IOException          // ereditato da Writer
public void newLine() throws IOException                  // solo BufferedWriter
public void close() throws IOException
```

`FileWriter` è un flusso di caratteri collegato a un file; `BufferedWriter` gli aggiunge il buffer e il metodo `newLine()`, che scrive il separatore di riga del sistema (su Windows non è il solo carattere `\n`). Il metodo `write` scrive il testo *così com'è*, senza a capo: l'a capo si aggiunge a mano con `newLine()`.

```java
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class ScriviConBuffer {
    public static void main(String[] args) {
        BufferedWriter out = null;
        try {
            out = new BufferedWriter(new FileWriter("elenco.txt"));
            out.write("Rossi");
            out.newLine();
            out.write("Bianchi");
            out.newLine();
            System.out.println("Elenco scritto.");
        } catch (IOException e) {
            System.out.println("Errore di scrittura: " + e.getMessage());
        } finally {
            if (out != null) {
                try {
                    out.close();                       // close() dichiara IOException
                } catch (IOException e) {
                    System.out.println("Errore in chiusura: " + e.getMessage());
                }
            }
        }
    }
}
```

L'output è:

```text
Elenco scritto.
```

Tutti i metodi di `BufferedWriter` che toccano il file dichiarano `IOException`, che è la superclasse di `FileNotFoundException`: un unico `catch (IOException e)` basta. Nel `finally`, però, anche `close()` può lanciare `IOException`, e il compilatore pretende che la si gestisca: da qui il `try`/`catch` interno. È la differenza pratica più visibile con `PrintWriter`.

> [!NOTE]
> **Approfondimento esterno — `BufferedWriter.newLine()`**
> Dalla documentazione: `newLine()` scrive un separatore di riga, definito dalla proprietà di sistema `line.separator`, e non è necessariamente un solo carattere `\n`. Poiché non tutte le piattaforme usano `\n` per terminare le righe, chiamare `newLine()` per terminare ogni riga è preferibile a scrivere direttamente un carattere di a capo.
>
> *Fonte:* [BufferedWriter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/BufferedWriter.html)

Mettiamo a confronto le forme di scrittura che si incontrano:

| Forma | Eccezione del costruttore | Metodi di scrittura | `close()` |
|---|---|---|---|
| `new PrintWriter("f.txt")` | `FileNotFoundException` | `print`/`println`/`printf`, nessuna eccezione | nessuna eccezione |
| `new PrintWriter(new FileWriter("f.txt", true))` | `IOException` | come sopra | nessuna eccezione |
| `new PrintWriter(new FileOutputStream("f.txt", true))` | `FileNotFoundException` | come sopra | nessuna eccezione |
| `new BufferedWriter(new FileWriter("f.txt"))` | `IOException` | `write`, `newLine`: `IOException` | `IOException` |

---

## 14.3 Aggiungere in coda a un file

Con `new PrintWriter("diario.txt")` il file viene sempre ricominciato da capo. Ci sono casi in cui si vuole il contrario: un registro in cui ogni esecuzione aggiunge una riga a quelle già scritte. Si parla di **accodare** (*append*), e a questo scopo i flussi che scrivono su file hanno un costruttore con un secondo parametro `boolean`:

```text
public FileWriter(String fileName, boolean append) throws IOException
public FileOutputStream(String name, boolean append) throws FileNotFoundException
```

Se `append` è `true`, i dati vengono scritti **alla fine** del file anziché all'inizio; se il file non esiste viene creato. Poiché `PrintWriter` ha costruttori che accettano un `Writer` e un `OutputStream`, per accodare lo si avvolge attorno a uno di questi due flussi, nelle due forme equivalenti:

```text
PrintWriter out = new PrintWriter(new FileWriter(nomeFile, true));
PrintWriter out = new PrintWriter(new FileOutputStream(nomeFile, true));
```

La prima dichiara `IOException`, la seconda `FileNotFoundException`: se un programma gestisce l'una nel `catch` e viene cambiata la forma, bisogna adattare anche il `catch`.

Vediamo l'effetto con due programmi, da eseguire uno dopo l'altro. Il primo crea il diario con due voci:

```java
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class CreaDiario {
    public static void main(String[] args) throws FileNotFoundException {
        PrintWriter out = new PrintWriter("diario.txt");   // ricomincia da capo
        out.println("prima voce");
        out.println("seconda voce");
        out.close();
    }
}
```

Il secondo aggiunge una voce in coda, senza cancellare le precedenti:

```java
import java.io.FileOutputStream;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class AggiungiDiario {
    public static void main(String[] args) {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new FileOutputStream("diario.txt", true)); // true = in coda
            out.println("terza voce");
        } catch (FileNotFoundException e) {
            System.out.println("Impossibile aprire il diario: " + e.getMessage());
        } finally {
            if (out != null) {
                out.close();
            }
        }
    }
}
```

Dopo `CreaDiario` il file contiene due righe; dopo `AggiungiDiario` ne contiene tre:

```text
prima voce
seconda voce
terza voce
```

Se `AggiungiDiario` venisse eseguito di nuovo, aggiungerebbe un'altra `terza voce` in fondo. Se invece si rilanciasse `CreaDiario`, il file tornerebbe di due righe.

> [!WARNING]
> **Attenzione — Il `true` di `PrintWriter` non è l'append**
> Il costruttore `PrintWriter(OutputStream out, boolean autoFlush)` ha un secondo parametro `boolean` che significa **svuotamento automatico** del buffer, non accodamento. Scrivere `new PrintWriter(new FileOutputStream("diario.txt"), true)` compila, ma **non accoda**: il `FileOutputStream` è aperto in modalità normale e il file viene svuotato. Il `true` dell'append va sempre passato al costruttore del flusso di file (`FileOutputStream`, `FileWriter`), mai a `PrintWriter`. E `new PrintWriter("diario.txt", true)` non compila affatto, perché per `PrintWriter(String, ...)` il secondo parametro dovrebbe essere un nome di codifica (`String`) o un `Charset`.

> [!NOTE]
> **Approfondimento esterno — Il parametro `append`**
> Dalla documentazione: in `FileWriter(String fileName, boolean append)`, se `append` è `true` i dati vengono scritti alla fine del file anziché all'inizio. L'eccezione dichiarata è `IOException`, lanciata se il file esiste ma è una cartella, se non esiste e non può essere creato, o se non può essere aperto per altri motivi. Lo stesso significato ha il parametro `append` di `FileOutputStream(String name, boolean append)`, che dichiara però `FileNotFoundException`.
>
> *Fonte:* [FileWriter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileWriter.html) e [FileOutputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileOutputStream.html)

---

## 14.4 Leggere un file di testo

### 14.4.1 `Scanner` su un file

Per leggere dalla tastiera abbiamo usato `new Scanner(System.in)`. Per leggere da un file si crea lo `Scanner` su un oggetto di tipo `File`, la classe che rappresenta il nome di un file (sezione 14.5):

```text
public Scanner(File source) throws FileNotFoundException
```

Una volta creato lo `Scanner`, i metodi sono quelli che già conosciamo ([Capitolo 3](03-stringhe-e-console.md), sezione 3.7.2): `nextLine()` per una riga, `next()` per una parola, `nextInt()` per un intero, e i metodi di controllo `hasNextLine()`, `hasNext()`, `hasNextInt()`, che rispondono `true` o `false` senza consumare nulla. La differenza rispetto alla tastiera è che il file **finisce**: quando non c'è più nulla da leggere, `hasNextLine()` diventa `false`. Il ciclo di lettura è quindi:

```text
finché lo scanner ha un'altra riga:
    leggi la riga
    elaborala
```

Supponiamo che `spesa.txt` contenga le tre righe `pane`, `latte`, `uova` e leggiamolo:

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class LeggiSpesa {
    public static void main(String[] args) {
        Scanner in = null;
        try {
            in = new Scanner(new File("spesa.txt"));   // apre il file in lettura
            int n = 0;
            while (in.hasNextLine()) {                 // c'e' ancora una riga?
                String riga = in.nextLine();           // si', leggila
                n++;
                System.out.println(n + ": " + riga);
            }
        } catch (FileNotFoundException e) {
            System.out.println("File non trovato: spesa.txt");
        } finally {
            if (in != null) {
                in.close();                            // Scanner.close() non dichiara eccezioni
            }
        }
    }
}
```

L'output è:

```text
1: pane
2: latte
3: uova
```

Riga per riga. `new File("spesa.txt")` crea l'oggetto che rappresenta il nome del file; `new Scanner(...)` lo apre in lettura e può lanciare `FileNotFoundException` (che è **controllata**), a differenza dello `Scanner` sulla tastiera, che non lancia nulla. Il ciclo `while (in.hasNextLine())` rilegge l'esito della domanda «c'è un'altra riga?» a ogni giro; dentro il corpo si legge **una sola riga** con `nextLine()`, perché ogni chiamata consuma la riga. Quando le righe finiscono, `hasNextLine()` dà `false` e il ciclo termina senza eccezioni. Il `finally` chiude lo `Scanner`; `Scanner.close()` non dichiara eccezioni, quindi non serve un `try` interno.

> [!NOTE]
> **Approfondimento esterno — `Scanner(File)`, `hasNextLine`, `nextLine`**
> Dalla documentazione: il costruttore `public Scanner(File source) throws FileNotFoundException` crea uno `Scanner` che produce i valori letti dal file indicato, convertendo i byte in caratteri con la codifica predefinita della piattaforma; lancia `FileNotFoundException` se il file non viene trovato. `hasNextLine()` restituisce `true` se nell'input c'è un'altra riga e non fa avanzare lo scanner. `nextLine()` fa avanzare lo scanner oltre la riga corrente e restituisce la parte saltata, **senza il separatore di riga**; lancia `NoSuchElementException` se non c'è nessuna riga.
>
> *Fonte:* [Scanner (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Scanner.html)

Attenzione a non confondere `new Scanner(File)` con `new Scanner(String)`. Il costruttore che accetta una `String` **non apre un file**: crea uno scanner che legge *quella stringa* come se fosse il testo da analizzare. Scrivere `new Scanner("spesa.txt")` compila senza errori, ma produce una sola «riga», cioè le lettere `spesa.txt` (vedi *Errore 1*).

### 14.4.2 `BufferedReader` su `FileReader`

La seconda forma di lettura usa i flussi di caratteri visti nella sezione 14.1.5:

```text
public FileReader(String fileName) throws FileNotFoundException
public BufferedReader(Reader in)
public String readLine() throws IOException
public void close() throws IOException
```

`readLine()` legge una riga e la restituisce **senza il carattere di a capo**; quando il file è finito restituisce `null`. È questo `null` il segnale di fine file. Mettiamolo in un programma, sempre sul file `spesa.txt`:

```java
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class LeggiRighe {
    public static void main(String[] args) {
        BufferedReader in = null;
        try {
            in = new BufferedReader(new FileReader("spesa.txt"));
            String riga;
            int n = 0;
            while ((riga = in.readLine()) != null) {     // legge, assegna, controlla
                n++;
                System.out.println(n + ": " + riga);
            }
            System.out.println("Righe lette: " + n);
        } catch (FileNotFoundException e) {
            System.out.println("File non trovato: spesa.txt");
        } catch (IOException e) {
            System.out.println("Errore di lettura: " + e.getMessage());
        } finally {
            if (in != null) {
                try {
                    in.close();                           // close() dichiara IOException
                } catch (IOException e) {
                    System.out.println("Errore in chiusura: " + e.getMessage());
                }
            }
        }
    }
}
```

L'output è:

```text
1: pane
2: latte
3: uova
Righe lette: 3
```

I due `catch` sono in quest'ordine perché `FileNotFoundException` è sottoclasse di `IOException`: se si scrivesse prima `catch (IOException e)`, il secondo blocco sarebbe irraggiungibile e il compilatore darebbe errore (`exception FileNotFoundException has already been caught`, [Capitolo 13](13-eccezioni.md) sezione 13.4.2). Un solo `catch (IOException e)` sarebbe comunque sufficiente se non si vuole distinguere i due casi.

> [!NOTE]
> **Approfondimento esterno — `BufferedReader.readLine()`**
> Dalla documentazione: `public String readLine() throws IOException` legge una riga di testo. Una riga è terminata da un avanzamento di riga (`\n`), da un ritorno a capo (`\r`), da un ritorno a capo seguito subito da un avanzamento di riga, oppure dalla fine del file. Il risultato è una `String` con il contenuto della riga, **senza i caratteri di terminazione**, oppure `null` se si è raggiunta la fine del flusso senza aver letto alcun carattere.
>
> *Fonte:* [BufferedReader (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/BufferedReader.html)

### 14.4.3 Il ciclo di lettura riga per riga

L'espressione `while ((riga = in.readLine()) != null)` è lo schema più importante del capitolo, e conviene capirla pezzo per pezzo, perché in una sola riga compie tre azioni.

1. `in.readLine()` legge la prossima riga e la restituisce (oppure `null`).
2. `riga = ...` assegna il risultato alla variabile `riga`. In Java un'assegnazione è un'espressione, e il suo valore è il valore assegnato.
3. `(...) != null` confronta quel valore con `null`: se è diverso, il ciclo prosegue e `riga` contiene la riga appena letta; se è `null`, il file è finito e il ciclo termina.

Le **parentesi interne** sono obbligatorie: senza di esse `riga = in.readLine() != null` verrebbe letto come `riga = (in.readLine() != null)`, un'assegnazione di un `boolean` a una `String`, che non compila. La variabile `riga` va dichiarata **prima** del ciclo, perché l'assegnazione sta nella condizione.

Una forma equivalente, più lunga ma senza assegnazione dentro la condizione, è la lettura «di innesco»: una prima lettura prima del ciclo e una nuova lettura come ultima istruzione del corpo.

```java
import java.io.BufferedReader;
import java.io.IOException;

public class ContaRighe {
    static int conta(BufferedReader in) throws IOException {
        int n = 0;
        String riga = in.readLine();       // lettura di innesco
        while (riga != null) {
            n++;
            riga = in.readLine();          // prossima lettura, ultima istruzione del corpo
        }
        return n;
    }
}
```

Le due forme sono equivalenti. In entrambe, **`readLine()` si chiama una sola volta per ogni giro** del ciclo: ogni chiamata consuma una riga, e una seconda chiamata nello stesso giro ne butta via una (vedi *Errore 2*).

Vediamo ora tre situazioni limite, che è bene aver visto una volta. Il programma scrive tre file e li rilegge:

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class CasiLimite {
    static void leggi(String nome) throws IOException {
        BufferedReader in = new BufferedReader(new FileReader(nome));
        String riga;
        int n = 0;
        while ((riga = in.readLine()) != null) {
            n++;
            System.out.println("[" + riga + "]");
        }
        System.out.println(nome + ": " + n + " righe");
        in.close();
    }

    public static void main(String[] args) throws IOException {
        PrintWriter vuoto = new PrintWriter("vuoto.txt");
        vuoto.close();                                    // file creato, senza nulla dentro

        PrintWriter buco = new PrintWriter("buco.txt");
        buco.print("a\n\nb");                             // riga vuota in mezzo, nessun a capo finale
        buco.close();

        leggi("vuoto.txt");
        leggi("buco.txt");
    }
}
```

L'output è:

```text
vuoto.txt: 0 righe
[a]
[]
[b]
buco.txt: 3 righe
```

Un file vuoto fa subito restituire `null` alla prima `readLine()`: il ciclo non gira nemmeno una volta, ed è il comportamento corretto, senza casi speciali. Una **riga vuota** in mezzo al file è una riga valida: `readLine()` restituisce la stringa vuota `""`, che è diversa da `null` e non ferma il ciclo. L'ultima riga viene letta anche se **non è terminata da un a capo**: la fine del file chiude la riga.

### 14.4.4 `Scanner` o `BufferedReader`?

Per leggere un file di testo riga per riga le due strade sono equivalenti, e conviene conoscerle entrambe. Questa tabella riassume le differenze che contano per l'esame:

| | `Scanner` su `File` | `BufferedReader` su `FileReader` |
|---|---|---|
| Come si apre | `new Scanner(new File(nome))`, dichiara `FileNotFoundException` | `new BufferedReader(new FileReader(nome))`, dichiara `FileNotFoundException` |
| Come si chiede «c'è altro?» | `hasNextLine()` (anche `hasNext()`, `hasNextInt()`) | si legge e si controlla se `readLine()` dà `null` |
| Lettura di una riga | `nextLine()`, nessuna eccezione controllata | `readLine()`, dichiara `IOException` |
| Lettura di numeri e parole | `nextInt()`, `nextDouble()`, `next()`, comodi | solo righe: si converte a mano (`parseInt`, ...) |
| Chiusura | `close()`, nessuna eccezione | `close()`, dichiara `IOException` |

La scelta, in sintesi: se la traccia nomina una delle due classi, si usa quella; se la scelta è libera, `Scanner` ha meno obblighi (nessuna eccezione sulle letture e sulla chiusura) ed è comodo quando si leggono numeri; `BufferedReader` è la scelta classica per «un'intera riga alla volta» e per i flussi di rete ([Capitolo 19](19-networking.md)).

### 14.4.5 Leggere numeri e parole

Con `Scanner` un file di numeri si legge come si leggerebbero dalla tastiera. Il file `numeri.txt` contiene due righe, `12 7 30` e `5 8`:

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class SommaNumeri {
    public static void main(String[] args) throws FileNotFoundException {
        Scanner in = new Scanner(new File("numeri.txt"));
        int somma = 0;
        int quanti = 0;
        while (in.hasNextInt()) {          // c'e' ancora un intero?
            somma += in.nextInt();         // si': leggilo e sommalo
            quanti++;
        }
        in.close();
        System.out.println("Numeri letti: " + quanti);
        System.out.println("Somma: " + somma);
    }
}
```

L'output è:

```text
Numeri letti: 5
Somma: 62
```

I token sono letti uno alla volta, senza badare a dove finisce la riga: gli spazi e gli a capo sono delimitatori ugualmente. Il ciclo si ferma al primo token che non è un intero, o alla fine del file. Chi vuole elaborare riga per riga numeri sparsi lo fa leggendo la riga con `nextLine()` e poi scomponendola (sezione 14.7).

> [!WARNING]
> **Attenzione — `nextInt()` seguito da `nextLine()`**
> Anche su un file vale la trappola vista nel [Capitolo 3](03-stringhe-e-console.md) (sezione 3.7.3): `nextInt()` legge il numero ma **non consuma l'a capo** che lo segue; una `nextLine()` immediatamente successiva restituisce quindi il resto, vuoto, della riga del numero. Dopo `nextInt()` e prima di leggere una nuova riga intera occorre una `nextLine()` che scarti il resto della riga.

---

## 14.5 La classe `File`

### 14.5.1 Un nome, non un contenuto

Finora abbiamo identificato i file con delle `String`. La classe `java.io.File` offre qualcosa in più: un **oggetto** che rappresenta il nome di un file (o di una cartella) in modo indipendente dal sistema operativo.

> [!NOTE]
> **Definizione — `File`**
> Un oggetto `File` è la rappresentazione astratta di un percorso (*pathname*) nel file system. Non contiene i dati del file, e non li legge né li scrive: `new File("tesoro.txt")` non è semplicemente una stringa, è un oggetto che *sa* di dover indicare un file, e di cui si può chiedere se esiste, quanto è grande, se si può leggere. Crearlo **non crea** nessun file sul disco.

È come scrivere un indirizzo su una busta: l'indirizzo c'è, ma la casa potrebbe non esistere. I costruttori di `Scanner`, `FileReader`, `PrintWriter` e `FileWriter` accettano un `File` al posto della stringa, ed è il modo di prepararsi un nome da controllare prima di aprire il flusso.

### 14.5.2 I metodi di `File`

Questi sono i metodi più usati. Tutti, tranne `createNewFile()`, sono privi di eccezioni controllate.

| Metodo | Che cosa fa |
|---|---|
| `boolean exists()` | `true` se il file o la cartella esistono |
| `boolean isFile()` | `true` se è un file regolare |
| `boolean isDirectory()` | `true` se è una cartella |
| `boolean canRead()` | `true` se l'applicazione può leggere il file |
| `boolean canWrite()` | `true` se l'applicazione può scriverlo |
| `String getName()` | l'ultimo elemento del percorso (il nome del file) |
| `String getPath()` | il percorso come è stato scritto |
| `String getAbsolutePath()` | il percorso assoluto |
| `String getParent()` | il percorso della cartella che lo contiene (o `null`) |
| `long length()` | la lunghezza in byte (non specificata per le cartelle; 0 se il file non esiste) |
| `boolean delete()` | cancella il file o la cartella (vuota); `true` se riuscito |
| `boolean createNewFile() throws IOException` | crea un file vuoto, solo se non esiste; `true` se l'ha creato |
| `boolean mkdir()` | crea la cartella |
| `String[] list()` | i nomi dei file e delle cartelle contenuti, oppure `null` se non è una cartella |
| `File[] listFiles()` | come `list()`, ma restituisce oggetti `File` |

```java
import java.io.File;
import java.io.IOException;

public class EsaminaFile {
    public static void main(String[] args) throws IOException {
        File f = new File("relazione.txt");
        System.out.println("esiste: " + f.exists());
        System.out.println("creato: " + f.createNewFile());
        System.out.println("esiste: " + f.exists());
        System.out.println("isFile: " + f.isFile());
        System.out.println("isDirectory: " + f.isDirectory());
        System.out.println("nome: " + f.getName());
        System.out.println("byte: " + f.length());
        System.out.println("cancellato: " + f.delete());
        System.out.println("esiste: " + f.exists());
    }
}
```

Se `relazione.txt` non esiste all'inizio, l'output è:

```text
esiste: false
creato: true
esiste: true
isFile: true
isDirectory: false
nome: relazione.txt
byte: 0
cancellato: true
esiste: false
```

Il programma dichiara `throws IOException` solo per `createNewFile()`, l'unico metodo dell'elenco che può fallire per un problema di I/O. Gli altri non lanciano eccezioni controllate: quando non riescono, **restituiscono `false`** (o `0`, o `null`), ed è il programmatore a dover controllare il risultato. Per questo `delete()` e `mkdir()` restituiscono un `boolean` e non conviene ignorarlo.

I metodi `list()` e `listFiles()` servono a scorrere il contenuto di una cartella. L'ordine dei nomi **non è garantito**, quindi, se serve un ordine, si ordina l'array ([Capitolo 5](05-array-e-matrici.md)):

```java
import java.io.File;
import java.util.Arrays;

public class ElencoCartella {
    public static void main(String[] args) {
        File cartella = new File("dati");
        String[] nomi = cartella.list();
        if (nomi == null) {
            System.out.println("dati non e' una cartella");
        } else {
            Arrays.sort(nomi);                  // l'ordine di list() non e' garantito
            for (String nome : nomi) {
                System.out.println(nome);
            }
        }
    }
}
```

Se la cartella `dati` contiene i file `b.txt` e `a.txt`, l'output è:

```text
a.txt
b.txt
```

e, se `dati` non esiste o non è una cartella, `list()` restituisce `null` e il programma stampa il messaggio. Il controllo `nomi == null` è essenziale: lo si dimentica facilmente, e il ciclo `for` su un `null` darebbe una `NullPointerException` ([Capitolo 8](08-riferimenti-e-memoria.md)).

### 14.5.3 Percorsi assoluti e relativi, e dove sta il file

Un nome come `"spesa.txt"` indica un file nella **cartella di lavoro** del programma, cioè la cartella da cui viene lanciato (con `java Main` da terminale è la cartella in cui ci si trova). Per indicare un file altrove si scrive un **percorso**: *assoluto* se parte dalla radice del file system e contiene tutto (`/home/anna/spesa.txt`, oppure `C:\dati\spesa.txt` su Windows), *relativo* se va interpretato a partire dalla cartella di lavoro (`dati/spesa.txt`).

> [!NOTE]
> **Approfondimento esterno — Percorsi relativi e `user.dir`**
> Dalla documentazione: un percorso assoluto è completo, non servono altre informazioni per individuare il file; un percorso relativo va invece interpretato usando informazioni prese da un altro percorso. Per impostazione predefinita, le classi del package `java.io` risolvono i percorsi relativi rispetto alla **cartella corrente dell'utente**, indicata dalla proprietà di sistema `user.dir`, che di solito è la cartella in cui è stata avviata la macchina virtuale Java.
> Il separatore tra gli elementi è il valore di `File.separator`, definito dalla proprietà `file.separator`; nella conversione da stringa a percorso, i nomi possono però essere separati anche da qualunque altro separatore supportato dal sistema sottostante.
>
> *Fonte:* [File (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/File.html)

Gli stili di percorso variano da un sistema all'altro: su Unix si separa con `/`, su Windows con `\`. In una stringa Java, però, la barra rovesciata è il carattere di *escape* ([Capitolo 3](03-stringhe-e-console.md), sezione 3.3.1): per scrivere un percorso Windows bisogna raddoppiarla.

```java
import java.io.File;

public class Percorsi {
    public static void main(String[] args) {
        File relativo = new File("dati" + File.separator + "spesa.txt");
        File assoluto = new File(relativo.getAbsolutePath());
        System.out.println("relativo.isAbsolute(): " + relativo.isAbsolute());
        System.out.println("assoluto.isAbsolute(): " + assoluto.isAbsolute());
        System.out.println("stesso nome: " + relativo.getName().equals(assoluto.getName()));
        String windows = "C:\\dati\\spesa.txt";      // \\ e' una sola barra rovesciata
        System.out.println(windows);
    }
}
```

L'output è:

```text
relativo.isAbsolute(): false
assoluto.isAbsolute(): true
stesso nome: true
C:\dati\spesa.txt
```

Scrivere `"C:\dati\spesa.txt"` con barre singole non compila: `\d` e `\s` non sono sequenze di escape valide (*Errore 11*). Un'alternativa che funziona ovunque è `File.separator`, oppure scrivere il percorso con `/`.

La causa di gran lunga più frequente del `FileNotFoundException` su un file «che esiste» è proprio questa: il file è in una cartella, ma il programma viene avviato da un'altra. Quando un file non viene trovato, il primo controllo è stampare `new File("spesa.txt").getAbsolutePath()` e verificare che sia il percorso dove ci si aspetta.

### 14.5.4 Chiedere il nome del file all'utente

Un programma può chiedere il nome del file da tastiera, controllare con `File` che esista e solo allora aprirlo: è un'applicazione tipica di `File.exists()`.

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class LeggiNomeFile {
    public static void main(String[] args) {
        Scanner tastiera = new Scanner(System.in);
        System.out.print("Nome del file: ");
        String nome = tastiera.nextLine();
        File f = new File(nome);
        if (!f.exists()) {
            System.out.println("Il file " + nome + " non esiste.");
        } else if (!f.canRead()) {
            System.out.println("Il file " + nome + " non si puo' leggere.");
        } else {
            Scanner in = null;
            try {
                in = new Scanner(f);
                int righe = 0;
                while (in.hasNextLine()) {
                    in.nextLine();
                    righe++;
                }
                System.out.println("Righe nel file " + nome + ": " + righe);
            } catch (FileNotFoundException e) {
                System.out.println("Il file " + nome + " non si puo' aprire.");
            } finally {
                if (in != null) {
                    in.close();
                }
            }
        }
    }
}
```

Una possibile esecuzione, in cui la prima riga è ciò che digita l'utente, con `spesa.txt` di tre righe:

```text
Nome del file: spesa.txt
Righe nel file spesa.txt: 3
```

L'`if`/`else if` filtra i casi problematici con un messaggio dedicato; il `try`/`catch` rimane comunque necessario, perché il compilatore lo esige e perché, tra il controllo e l'apertura, il file potrebbe sparire o essere reso illeggibile. Il controllo con `File` non sostituisce la gestione dell'eccezione, la completa.

---

## 14.6 Un metodo che apre un flusso

Quando un programma apre molti file, conviene isolare l'apertura in un metodo. Il metodo riceve il **nome del file** come `String`, restituisce il **flusso già aperto** e dichiara con `throws` le eccezioni dell'apertura; ne risponde chi lo chiama, con un blocco `try`/`catch` dove decide che cosa fare in caso di errore.

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;

public class CopiaNumerata {
    static Scanner apriLettura(String nome) throws FileNotFoundException {
        return new Scanner(new File(nome));
    }

    static PrintWriter apriScrittura(String nome) throws FileNotFoundException {
        return new PrintWriter(nome);
    }

    public static void main(String[] args) {
        Scanner in = null;
        PrintWriter out = null;
        try {
            in = apriLettura("spesa.txt");
            out = apriScrittura("spesa_numerata.txt");
            int n = 0;
            while (in.hasNextLine()) {
                n++;
                out.println(n + ". " + in.nextLine());
            }
            System.out.println("Copiate " + n + " righe.");
        } catch (FileNotFoundException e) {
            System.out.println("Impossibile aprire un file: " + e.getMessage());
        } finally {
            if (in != null) {
                in.close();
            }
            if (out != null) {
                out.close();
            }
        }
    }
}
```

Con `spesa.txt` di tre righe, l'output è:

```text
Copiate 3 righe.
```

e `spesa_numerata.txt` contiene:

```text
1. pane
2. latte
3. uova
```

Il programma usa due flussi alla volta, uno in lettura e uno in scrittura. Ciascuno è dichiarato fuori dal `try` e inizializzato a `null`, e ciascuno ha la propria guardia nel `finally`. Con due flussi la guardia è ancora più importante: se l'apertura del secondo fallisce, il primo è già aperto e va chiuso comunque, mentre il secondo vale ancora `null`. I metodi `apriLettura` e `apriScrittura` **non gestiscono** l'eccezione, la lasciano passare con `throws`: sarebbe sbagliato catturarla dentro il metodo, perché il metodo non saprebbe che cosa restituire. Resta anche una regola: chi apre il flusso (qui `main`) è responsabile di **chiuderlo**.

---

## 14.7 File CSV: scomporre le righe con `split`

Un formato di file di testo molto diffuso è il **CSV** (*comma-separated values*, valori separati da virgola): ogni riga è un record e i campi della riga sono separati da virgole. È il formato tipico di un registro di cassa:

```text
SKU,Quantity,Price,Description
4039,50,0.99,SODA
9100,5,9.50,T-SHIRT
1949,30,110.00,JAVA PROGRAMMING TEXTBOOK
5199,25,1.50,COOKIE
```

La prima riga è l'**intestazione**: dà il nome delle colonne e non è un dato. Le altre contengono SKU (codice dell'articolo), quantità venduta, prezzo unitario e descrizione. Per leggere un file di questo tipo si combinano due cose già viste: la lettura riga per riga (sezione 14.4) e il metodo `split` ([Capitolo 3](03-stringhe-e-console.md), sezione 3.5), che scompone una riga in un array di campi.

Calcoliamo l'incasso totale. Per ciascuna riga si scompone con `split(",")`, si convertono la quantità e il prezzo con `Integer.parseInt` e `Double.parseDouble` ([Capitolo 6](06-metodi.md), sezione 6.6.4) e si somma il prodotto:

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Locale;
import java.util.Scanner;

public class TotaleVendite {
    public static void main(String[] args) {
        Scanner in = null;
        try {
            in = new Scanner(new File("vendite.csv"));
            in.nextLine();                                  // salta l'intestazione
            double totale = 0;
            while (in.hasNextLine()) {
                String riga = in.nextLine();
                String[] campi = riga.split(",");           // campi[0]=SKU ... campi[3]=descrizione
                int quantita = Integer.parseInt(campi[1]);
                double prezzo = Double.parseDouble(campi[2]);
                totale = totale + quantita * prezzo;
                System.out.println(campi[3] + ": " + quantita + " x " + prezzo);
            }
            System.out.printf(Locale.US, "Totale: %.2f%n", totale);
        } catch (FileNotFoundException e) {
            System.out.println("File vendite.csv non trovato.");
        } finally {
            if (in != null) {
                in.close();
            }
        }
    }
}
```

L'output è:

```text
SODA: 50 x 0.99
T-SHIRT: 5 x 9.5
JAVA PROGRAMMING TEXTBOOK: 30 x 110.0
COOKIE: 25 x 1.5
Totale: 3434.50
```

Riga per riga. `in.nextLine()` fuori dal ciclo consuma l'intestazione senza usarla. Dentro il ciclo, per esempio per `4039,50,0.99,SODA`, `split(",")` produce un array di quattro stringhe, `"4039"`, `"50"`, `"0.99"`, `"SODA"`; `campi[1]` e `campi[2]` sono **stringhe** e vanno convertite prima di moltiplicarle. I prezzi appaiono come `9.5` e `110.0` e non come `9.50` e `110.00` perché stampiamo `double`, non testo formattato; per il totale usiamo `printf` con due decimali.

Nei file reali bisogna fare i conti con righe non perfette. Alcune precauzioni, con il loro motivo:

- **Spazi attorno ai campi.** `Integer.parseInt(" 50")` lancia `NumberFormatException`: la conversione non tollera spazi. Se il file può contenerne, si usa `campi[1].trim()`.
- **Righe incomplete.** Una riga con meno campi del previsto rende `campi[3]` un indice fuori dai limiti (`ArrayIndexOutOfBoundsException`). Si controlla prima `campi.length == 4`.
- **Righe vuote.** `"".split(",")` restituisce un array di *un* elemento (la stringa vuota), quindi la riga vuota passerebbe il primo controllo e darebbe un errore alla conversione: si scartano con `riga.trim().isEmpty()`.
- **Virgole dentro un campo.** Una descrizione come `Vestito, blu` sarebbe divisa in due campi. Se si sa che solo l'ultimo campo può contenerne, si limita il numero dei pezzi con `split(",", 4)`: dopo tre separatori, il resto della riga resta nel quarto campo.

Mettendo insieme le prime tre precauzioni si ottiene una lettura che non si ferma davanti a una riga difettosa, ma la scarta e continua:

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class VenditeSicure {
    public static void main(String[] args) throws FileNotFoundException {
        Scanner in = new Scanner(new File("difettoso.csv"));
        in.nextLine();                                     // intestazione
        int valide = 0;
        int scartate = 0;
        while (in.hasNextLine()) {
            String riga = in.nextLine();
            if (riga.trim().isEmpty()) {
                continue;                                  // riga vuota: ignorata, non conta come scartata
            }
            String[] campi = riga.split(",");
            if (campi.length != 4) {
                scartate++;                                // numero di campi sbagliato
                continue;
            }
            try {
                Integer.parseInt(campi[1].trim());
                Double.parseDouble(campi[2].trim());
                valide++;
            } catch (NumberFormatException e) {
                scartate++;                                // quantita' o prezzo non numerici
            }
        }
        in.close();
        System.out.println("Valide: " + valide + ", scartate: " + scartate);
    }
}
```

Se `difettoso.csv` contiene l'intestazione, due righe corrette, una riga vuota, una riga `7001,12` (campi mancanti) e una riga `7002,abc,1.50,PENNA`, l'output è:

```text
Valide: 2, scartate: 2
```

(`continue` è del [Capitolo 4](04-strutture-di-controllo.md): salta il resto del giro e passa alla riga successiva.)

### 14.7.1 Scrivere un file CSV

Il procedimento inverso è altrettanto semplice: si compone la riga concatenando i campi con la virgola e la si stampa con `println`.

```java
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class ScriviCsv {
    public static void main(String[] args) throws FileNotFoundException {
        String[] nomi = {"Anna", "Luca", "Sara"};
        int[] voti = {28, 24, 30};
        PrintWriter out = new PrintWriter("voti.csv");
        out.println("Nome,Voto");                          // intestazione
        for (int i = 0; i < nomi.length; i++) {
            out.println(nomi[i] + "," + voti[i]);          // un record per riga
        }
        out.close();
    }
}
```

Il file `voti.csv` che ne risulta è:

```text
Nome,Voto
Anna,28
Luca,24
Sara,30
```

---

## 14.8 Dalla traccia al codice

Le tracce d'esame descrivono la struttura voluta in poche parole, e ogni parola corrisponde a una scelta di codice. Questa tabella raccoglie le corrispondenze più frequenti per i file di testo:

| La traccia dice… | Si scrive… |
|---|---|
| «scrive su un file» / «crea il file» | `new PrintWriter(nome)` (sovrascrive) |
| «in coda», «senza cancellare il contenuto già presente», «aggiunge» | `new FileWriter(nome, true)` o `new FileOutputStream(nome, true)` avvolti in `PrintWriter` |
| «legge il file riga per riga» / «fino alla fine del file» | ciclo con `hasNextLine()` oppure con `readLine() != null` |
| «chiude i flussi nel blocco `finally`» | variabile a `null` fuori dal `try`, apertura nel `try`, guardia `!= null` e `close()` nel `finally` |
| «il metodo non gestisce le eccezioni» / «le propaga» | `throws FileNotFoundException` o `throws IOException` nella firma, nessun `catch` |
| «stampa il numero di righe lette» | un contatore incrementato **una volta per riga**, stampato dopo il ciclo (e nel `finally` se la traccia lo impone) |
| «ogni riga ha i campi separati da…» | `split("…")`, attenzione ai caratteri speciali delle espressioni regolari |
| «se il file non esiste, stampa…» | `catch (FileNotFoundException e)` con la **stringa esatta** della traccia |

Tre abitudini fanno risparmiare tentativi di esecuzione:

1. **Copiare alla lettera i messaggi e il formato di output** della traccia, compresi spazi, maiuscole, punteggiatura e a capo. Il confronto con il test nascosto è carattere per carattere.
2. **Rispettare il nome del file** indicato, con la stessa grafia: `"Dati.txt"` e `"dati.txt"` sono file diversi su molti sistemi.
3. **Non lasciare file aperti**: ogni `new PrintWriter`, `new Scanner(File)` o `new BufferedReader` deve avere la sua `close()`, nella posizione che la traccia richiede.

---

## Scheletri da esame

Sono i frammenti minimi da saper scrivere a memoria, su un editor senza aiuti. Ciascuno è una classe che si compila da sola.

### Scheletro 1 — Scrivere righe in un file (sovrascrivendo)

*Quando si usa:* «scrivi in un file le righe …»; la traccia può imporre la chiusura nel `finally`.

```java
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class ScheletroScrittura {
    static void scrivi(String nomeFile, String[] righe) throws FileNotFoundException {
        PrintWriter out = null;                      // fuori dal try, a null
        try {
            out = new PrintWriter(nomeFile);         // sovrascrive il file
            for (int i = 0; i < righe.length; i++) {
                out.println(righe[i]);               // una riga per elemento
            }
        } finally {
            if (out != null) {                       // guardia: l'apertura potrebbe aver fallito
                out.close();                         // svuota il buffer e chiude
            }
        }
    }
}
```

- **Eccezioni:** `new PrintWriter(String)` dichiara `FileNotFoundException`: qui la si propaga con `throws`, ma si può gestire con un `catch` tra `try` e `finally`. `println`, `close` non dichiarano nulla.
- **Import necessari:** `java.io.FileNotFoundException`, `java.io.PrintWriter`.

### Scheletro 2 — Aggiungere una riga in coda a un file

*Quando si usa:* «aggiungi in coda al file senza cancellare il contenuto già presente».

```java
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class ScheletroAccodare {
    static void accoda(String nomeFile, String riga) throws IOException {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new FileWriter(nomeFile, true));   // true = accoda
            out.println(riga);
        } finally {
            if (out != null) {
                out.close();
            }
        }
    }
}
```

- **Eccezioni:** `new FileWriter(String, boolean)` dichiara `IOException`. Con `new FileOutputStream(nomeFile, true)` al posto di `FileWriter` l'eccezione è `FileNotFoundException`.
- **Import necessari:** `java.io.FileWriter`, `java.io.IOException`, `java.io.PrintWriter` (con `FileOutputStream`: `java.io.FileOutputStream` e `java.io.FileNotFoundException`).
- **Da ricordare:** il `true` va al costruttore di `FileWriter`/`FileOutputStream`, non a `PrintWriter`.

### Scheletro 3 — Leggere un file riga per riga con `BufferedReader`

*Quando si usa:* «leggi il file fino alla fine e …» con `BufferedReader` imposto o libero.

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ScheletroLetturaBuffered {
    static int contaRighe(String nomeFile) throws IOException {
        BufferedReader in = null;
        try {
            in = new BufferedReader(new FileReader(nomeFile));
            int n = 0;
            String riga;
            while ((riga = in.readLine()) != null) {    // null = fine del file
                n++;                                    // elaborazione della riga
            }
            return n;
        } finally {
            if (in != null) {
                in.close();                             // dichiara IOException: propagata dal throws
            }
        }
    }
}
```

- **Eccezioni:** `new FileReader(String)` dichiara `FileNotFoundException`; `readLine()` e `close()` dichiarano `IOException`. Il `throws IOException` del metodo le copre tutte (la prima è sottoclasse). Se invece si gestiscono, il `catch (FileNotFoundException e)` va **prima** di `catch (IOException e)`, e la `close()` nel `finally` ha bisogno di un proprio `try`/`catch`.
- **Import necessari:** `java.io.BufferedReader`, `java.io.FileReader`, `java.io.IOException`.

### Scheletro 4 — Leggere un file riga per riga con `Scanner`

*Quando si usa:* «leggi il file con `Scanner`» oppure quando la scelta è libera e conviene meno codice.

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ScheletroLetturaScanner {
    static void stampaRighe(String nomeFile) throws FileNotFoundException {
        Scanner in = null;
        try {
            in = new Scanner(new File(nomeFile));
            while (in.hasNextLine()) {                  // finche' c'e' una riga
                String riga = in.nextLine();            // una sola nextLine per giro
                System.out.println(riga);
            }
        } finally {
            if (in != null) {
                in.close();                             // nessuna eccezione
            }
        }
    }
}
```

- **Eccezioni:** `new Scanner(File)` dichiara `FileNotFoundException`; `hasNextLine`, `nextLine`, `close` non dichiarano eccezioni controllate (`nextLine` può lanciare `NoSuchElementException` se non si controlla `hasNextLine`).
- **Import necessari:** `java.io.File`, `java.io.FileNotFoundException`, `java.util.Scanner`.

### Scheletro 5 — Leggere un CSV e sommare una colonna

*Quando si usa:* «il file contiene righe del tipo `codice,quantità,prezzo,…`; calcola …».

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ScheletroCsv {
    static double incasso(String nomeFile) throws FileNotFoundException {
        Scanner in = null;
        double totale = 0;
        try {
            in = new Scanner(new File(nomeFile));
            in.nextLine();                                       // intestazione, se presente
            while (in.hasNextLine()) {
                String[] campi = in.nextLine().split(",");       // scompone la riga
                int quantita = Integer.parseInt(campi[1].trim());
                double prezzo = Double.parseDouble(campi[2].trim());
                totale += quantita * prezzo;
            }
        } finally {
            if (in != null) {
                in.close();
            }
        }
        return totale;
    }
}
```

- **Eccezioni:** `FileNotFoundException` dal costruttore di `Scanner`; `NumberFormatException` (non controllata) da `parseInt`/`parseDouble`; `ArrayIndexOutOfBoundsException` (non controllata) se una riga ha meno campi di quanti ne servano.
- **Import necessari:** `java.io.File`, `java.io.FileNotFoundException`, `java.util.Scanner`.

### Scheletro 6 — Copiare un file di testo in un altro

*Quando si usa:* «copia il contenuto di un file in un altro»; due flussi aperti insieme, chiusi nel `finally`.

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class ScheletroCopia {
    static void copia(String origine, String destinazione) throws IOException {
        BufferedReader in = null;
        PrintWriter out = null;
        try {
            in = new BufferedReader(new FileReader(origine));
            out = new PrintWriter(destinazione);
            String riga;
            while ((riga = in.readLine()) != null) {
                out.println(riga);                    // riscrive la riga letta
            }
        } finally {
            if (in != null) {
                in.close();
            }
            if (out != null) {
                out.close();
            }
        }
    }
}
```

- **Eccezioni:** `FileNotFoundException` dai due costruttori, `IOException` da `readLine()` e dalla `close()` del lettore: il `throws IOException` le copre tutte. Se `in.close()` lanciasse un'eccezione, `out.close()` non verrebbe eseguita: per questo, quando la chiusura deve essere garantita per entrambi, si racchiude ogni `close()` in un proprio `try`/`catch`.
- **Import necessari:** `java.io.BufferedReader`, `java.io.FileReader`, `java.io.IOException`, `java.io.PrintWriter`.

---

## Errori tipici

> [!CAUTION]
> **Errore 1 — `new Scanner("nomefile")` non apre il file**
> Il costruttore di `Scanner` che accetta una `String` legge *quella stringa*. Compila e non dà errori, ma il programma analizza le lettere del nome del file.
>
> ```java
> // ERRATO: legge il testo "spesa.txt", non il contenuto del file
> import java.util.Scanner;
>
> public class ScannerSuStringa {
>     public static void main(String[] args) {
>         Scanner in = new Scanner("spesa.txt");
>         while (in.hasNextLine()) {
>             System.out.println(in.nextLine());
>         }
>     }
> }
> ```
>
> L'output è la sola riga `spesa.txt`. Per aprire un file occorre creare un oggetto `File`:
>
> ```java
> // CORRETTO: Scanner su un File (dichiara FileNotFoundException)
> Scanner in = new Scanner(new File("spesa.txt"));
> ```

> [!CAUTION]
> **Errore 2 — `readLine()` chiamato due volte nello stesso giro**
> Ogni chiamata a `readLine()` **consuma** una riga. Controllare la condizione con una chiamata e leggere la riga con un'altra fa perdere una riga ogni giro e, a fine file, può produrre `null`.
>
> ```java
> // ERRATO: due letture per giro (file con le righe p, q, r)
> import java.io.BufferedReader;
> import java.io.FileReader;
> import java.io.IOException;
>
> public class DoppiaLettura {
>     public static void main(String[] args) throws IOException {
>         BufferedReader in = new BufferedReader(new FileReader("tre.txt"));
>         String riga;
>         while (in.readLine() != null) {      // legge p (e la butta via)
>             riga = in.readLine();            // legge q
>             System.out.println(riga);
>         }                                    // il giro dopo: legge r, poi null
>         in.close();
>     }
> }
> ```
>
> Sul file `p`, `q`, `r` l'output è `q` seguito da `null`: la riga `p` è persa, la riga `r` è consumata dalla condizione e la seconda lettura restituisce `null`. La forma corretta assegna e controlla nella stessa espressione: `while ((riga = in.readLine()) != null)`. Lo stesso accade con `Scanner` se si chiama `nextLine()` due volte dopo un solo `hasNextLine()`.

> [!CAUTION]
> **Errore 3 — Dimenticare `close()` (o `flush()`) in scrittura**
> Il `PrintWriter` raccoglie i caratteri in un buffer. Se il programma termina senza chiuderlo, il buffer non viene scaricato.
>
> ```java
> // ERRATO: manca out.close()
> import java.io.FileNotFoundException;
> import java.io.PrintWriter;
>
> public class NienteClose {
>     public static void main(String[] args) throws FileNotFoundException {
>         PrintWriter out = new PrintWriter("perso.txt");
>         out.println("uno");
>         out.println("due");
>     }
> }
> ```
>
> Il programma termina senza errori, ma `perso.txt` rimane **vuoto** (0 byte). Per il compilatore tutto è in regola, e il test nascosto che rilegge il file fallisce. La forma corretta chiude il flusso, e se la traccia lo impone lo fa nel `finally` (sezione 14.2.6).

> [!CAUTION]
> **Errore 4 — Aprire in scrittura quando serviva accodare**
> `new PrintWriter(nome)` e `new FileWriter(nome)` troncano il file all'apertura. Se la traccia chiede di aggiungere, il contenuto precedente va perso.
>
> ```java
> // ERRATO: cancella il contenuto precedente di diario.txt
> PrintWriter out = new PrintWriter(new FileWriter("diario.txt"));
> ```
>
> ```java
> // CORRETTO: il true e' il secondo argomento di FileWriter
> PrintWriter out = new PrintWriter(new FileWriter("diario.txt", true));
> ```

> [!CAUTION]
> **Errore 5 — Il `true` di `PrintWriter(OutputStream, boolean)` non accoda**
> Il secondo argomento di questo costruttore è `autoFlush`, non `append`. Il codice compila e fa apparire corretta l'idea di accodare, ma tronca il file.
>
> ```java
> // ERRATO: true = svuotamento automatico del buffer; il file viene comunque troncato
> import java.io.FileNotFoundException;
> import java.io.FileOutputStream;
> import java.io.PrintWriter;
>
> public class AppendFinto {
>     public static void main(String[] args) throws FileNotFoundException {
>         PrintWriter out = new PrintWriter(new FileOutputStream("a.txt"), true);
>         out.println("y");
>         out.close();
>     }
> }
> ```
>
> Se `a.txt` conteneva una riga `x`, dopo l'esecuzione contiene solo `y`. Il `true` dell'append va a `FileOutputStream`: `new PrintWriter(new FileOutputStream("a.txt", true))`.

> [!CAUTION]
> **Errore 6 — Passare `true` direttamente a `PrintWriter(String, ...)`**
> Un `PrintWriter` costruito direttamente su un nome di file non ha un parametro di append.
>
> ```java
> // ERRATO: non compila
> import java.io.FileNotFoundException;
> import java.io.PrintWriter;
>
> public class AppendDiretto {
>     public static void main(String[] args) throws FileNotFoundException {
>         PrintWriter out = new PrintWriter("a.txt", true);
>     }
> }
> ```
>
> Il compilatore risponde `no suitable constructor found for PrintWriter(String,boolean)`, seguito dall'elenco dei costruttori scartati: per `PrintWriter(String, String)` il secondo argomento dovrebbe essere un nome di codifica. La forma corretta è `new PrintWriter(new FileWriter("a.txt", true))`.

> [!CAUTION]
> **Errore 7 — Non gestire né dichiarare l'eccezione di apertura**
> L'apertura di un file in lettura o scrittura dichiara un'eccezione controllata ([Capitolo 13](13-eccezioni.md)).
>
> ```java
> // ERRATO: non compila
> import java.io.PrintWriter;
>
> public class SenzaEccezione {
>     public static void main(String[] args) {
>         PrintWriter out = new PrintWriter("a.txt");
>         out.close();
>     }
> }
> ```
>
> Il messaggio è `unreported exception FileNotFoundException; must be caught or declared to be thrown`. Si risolve con un `try`/`catch (FileNotFoundException e)` oppure con `throws FileNotFoundException` su `main`.

> [!CAUTION]
> **Errore 8 — `catch (IOException)` prima di `catch (FileNotFoundException)`**
> `FileNotFoundException` è sottoclasse di `IOException`: il blocco più generale, se viene prima, cattura già tutto e rende l'altro irraggiungibile.
>
> ```java
> // ERRATO: non compila
> import java.io.BufferedReader;
> import java.io.FileNotFoundException;
> import java.io.FileReader;
> import java.io.IOException;
>
> public class OrdineCatch {
>     public static void main(String[] args) {
>         try {
>             BufferedReader in = new BufferedReader(new FileReader("a.txt"));
>             in.readLine();
>         } catch (IOException e) {
>             System.out.println("io");
>         } catch (FileNotFoundException e) {
>             System.out.println("fnf");
>         }
>     }
> }
> ```
>
> Il messaggio è `exception FileNotFoundException has already been caught`. Si scrive prima il `catch` della sottoclasse, poi quello della superclasse.

> [!CAUTION]
> **Errore 9 — Dichiarare il flusso dentro il `try` e chiuderlo nel `finally`**
> Una variabile dichiarata dentro un blocco esiste solo in quel blocco: nel `finally` non è visibile.
>
> ```java
> // ERRATO: non compila
> import java.io.BufferedReader;
> import java.io.FileReader;
> import java.io.IOException;
>
> public class ScopeFinally {
>     public static void main(String[] args) throws IOException {
>         try {
>             BufferedReader in = new BufferedReader(new FileReader("tre.txt"));
>             in.readLine();
>         } finally {
>             in.close();
>         }
>     }
> }
> ```
>
> Il messaggio è `cannot find symbol` (`symbol: variable in`). La forma corretta dichiara `BufferedReader in = null;` **prima** del `try` e assegna dentro il `try` (sezione 14.2.6).

> [!CAUTION]
> **Errore 10 — `close()` nel `finally` senza il controllo `!= null`**
> Se l'apertura fallisce, la variabile resta `null`: chiamare `close()` su di essa lancia una `NullPointerException` che sostituisce l'errore vero.
>
> ```java
> // ERRATO: manca la guardia if (in != null)
> import java.io.BufferedReader;
> import java.io.FileNotFoundException;
> import java.io.FileReader;
> import java.io.IOException;
>
> public class SenzaGuardia {
>     public static void main(String[] args) throws IOException {
>         BufferedReader in = null;
>         try {
>             in = new BufferedReader(new FileReader("manca.txt"));
>             System.out.println(in.readLine());
>         } catch (FileNotFoundException e) {
>             System.out.println("File non trovato");
>         } finally {
>             in.close();
>         }
>     }
> }
> ```
>
> Con `manca.txt` inesistente, il programma stampa `File non trovato` e poi termina con `Exception in thread "main" java.lang.NullPointerException`: il `catch` aveva gestito l'errore, ma il `finally` ne ha prodotto un altro. La forma corretta è `if (in != null) { in.close(); }`.

> [!CAUTION]
> **Errore 11 — Barra rovesciata non raddoppiata in un percorso**
> In una stringa Java la barra rovesciata inizia una sequenza di escape.
>
> ```java
> // ERRATO: non compila
> public class PercorsoWindows {
>     public static void main(String[] args) {
>         String p = "C:\dati\spesa.txt";
>     }
> }
> ```
>
> Il messaggio è `illegal escape character`. Si scrive `"C:\\dati\\spesa.txt"`, oppure si usa `/` come separatore.

> [!CAUTION]
> **Errore 12 — Cercare il file nella cartella sbagliata**
> Un nome relativo come `"dati.txt"` è cercato nella cartella di lavoro del programma, non nella cartella del sorgente. Se il file è altrove, a runtime si ottiene `java.io.FileNotFoundException: dati.txt (No such file or directory)`, anche se il file esiste.
>
> ```java
> // Diagnosi: dove sta cercando il programma?
> import java.io.File;
>
> public class DoveSono {
>     public static void main(String[] args) {
>         File f = new File("dati.txt");
>         System.out.println(f.getAbsolutePath());
>         System.out.println(f.exists());
>     }
> }
> ```
>
> Il programma stampa il percorso assoluto in cui cerca e se il file esiste. Il rimedio è lanciare `java` dalla cartella giusta, oppure indicare un percorso (sezione 14.5.3).

> [!CAUTION]
> **Errore 13 — `nextLine()` senza controllare `hasNextLine()`**
> Se non ci sono più righe, `nextLine()` lancia una `NoSuchElementException` (non controllata, quindi senza avvisi del compilatore).
>
> ```java
> // ERRATO: il file ha 3 righe, il ciclo ne legge 4
> import java.io.File;
> import java.io.FileNotFoundException;
> import java.util.Scanner;
>
> public class TroppeRighe {
>     public static void main(String[] args) throws FileNotFoundException {
>         Scanner in = new Scanner(new File("tre.txt"));
>         for (int i = 0; i < 4; i++) {
>             System.out.println(in.nextLine());
>         }
>     }
> }
> ```
>
> Dopo le tre righe, il programma termina con `java.util.NoSuchElementException: No line found`. Il numero di righe di un file non è noto in anticipo: si usa `while (in.hasNextLine())`.

> [!CAUTION]
> **Errore 14 — Dare per scontata la forma di una riga CSV**
> Una riga con meno campi del previsto, o con spazi attorno ai numeri, manda in errore l'elaborazione.
>
> ```java
> // ERRATO: nessun controllo sulla forma della riga
> public class CsvFragile {
>     public static void main(String[] args) {
>         String riga = "4039,50,0.99";                // manca la descrizione
>         String[] c = riga.split(",");
>         System.out.println(c[3]);                    // indice 3: fuori dai limiti
>         int q = Integer.parseInt(" 50");             // lo spazio non e' tollerato
>     }
> }
> ```
>
> `c[3]` lancia `java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3`; e, anche con tutti i campi presenti, `Integer.parseInt(" 50")` lancia `java.lang.NumberFormatException: For input string: " 50"`. Prima di accedere ai campi si controlla `c.length`, e prima di convertire si usa `trim()` (sezione 14.7).

> [!CAUTION]
> **Errore 15 — `try`-with-resources al posto del `finally` imposto**
> Quando la traccia chiede che la chiusura dei flussi avvenga nel `finally`, un `try`-with-resources compila e funziona, ma non rispetta il vincolo.
>
> ```java
> // ERRATO se la traccia impone la chiusura nel blocco finally: il finally non c'e'
> import java.io.FileNotFoundException;
> import java.io.PrintWriter;
>
> public class SenzaFinally {
>     public static void main(String[] args) {
>         try (PrintWriter out = new PrintWriter("a.txt")) {
>             out.println("x");
>         } catch (FileNotFoundException e) {
>             System.out.println("errore");
>         }
>     }
> }
> ```
>
> L'output coincide con quello atteso, ma la struttura no: la penalità riguarda l'aderenza alla traccia, non la correttezza del programma. Si scrive lo schema a quattro passi (sezione 14.2.6, [Capitolo 13](13-eccezioni.md) sezione 13.5.3).

---

## Riassunto

I dati di un programma vivono in memoria e spariscono alla sua fine; per conservarli, o per scambiarli con altri programmi, si usano i file. In Java ogni scambio con l'esterno avviene attraverso un **flusso**, un oggetto che rappresenta una sequenza ordinata di dati in movimento, di input o di output. I file di testo, leggibili con un editor, si trattano con i **flussi di caratteri** (`Reader`, `Writer`), mentre i file binari si trattano con i **flussi di byte** (`InputStream`, `OutputStream`, [Capitolo 15](15-stream-binari-e-serializzazione.md)). Le classi di `java.io` si **avvolgono** una nell'altra, ognuna aggiungendo una capacità: una sorgente o una destinazione (`FileReader`, `FileWriter`, `FileOutputStream`) e uno strato che rende comodo l'uso (`BufferedReader`, `PrintWriter`).

Per scrivere si usa `PrintWriter`: costruito su un nome di file crea il file o lo svuota; avvolto attorno a un `FileWriter` o a un `FileOutputStream` aperti con `true` aggiunge in coda. I dati passano per un buffer, quindi **senza `close()` o `flush()` il file resta incompleto**. Per leggere si usa `Scanner` su un `File` (con `hasNextLine`/`nextLine`) oppure `BufferedReader` su un `FileReader` (con `readLine`, che restituisce `null` alla fine). Le aperture dichiarano `FileNotFoundException` o `IOException`, controllate: si gestiscono con `try`/`catch` oppure si propagano con `throws`, e la chiusura va nel `finally` con lo schema a quattro passi. La classe `File` rappresenta il nome di un file e ne permette l'ispezione; i file CSV si leggono riga per riga scomponendo ogni riga con `split`.

### Concetti chiave

- **Flusso (*stream*)**: sequenza ordinata di dati tra programma ed esterno; di input o di output, di caratteri o di byte.
- **Testo contro binario**: testo leggibile da un editor, trattato con `Reader`/`Writer`; tutto il resto è binario, con `InputStream`/`OutputStream`.
- **Avvolgimento**: `new BufferedReader(new FileReader(nome))`: si legge dall'interno verso l'esterno; ogni strato aggiunge una capacità.
- **`PrintWriter(String)`**: apre (o crea) un file in scrittura e lo **svuota**; dichiara `FileNotFoundException`; i suoi metodi di stampa e `close()` non dichiarano eccezioni.
- **Buffer**: la scrittura passa da una memoria intermedia; `close()` e `flush()` la scaricano. Un flusso non chiuso lascia il file vuoto o incompleto.
- **Append**: si passa `true` al costruttore di `FileWriter` o `FileOutputStream`, mai a `PrintWriter`; il `true` di `PrintWriter(OutputStream, boolean)` è `autoFlush`.
- **`Scanner(File)`**: `FileNotFoundException` all'apertura; `hasNextLine()` prima di `nextLine()`; `Scanner(String)` non apre un file.
- **`BufferedReader.readLine()`**: restituisce la riga senza a capo, `null` a fine file; dichiara `IOException`; ciclo `while ((riga = in.readLine()) != null)`.
- **Una lettura per giro**: ogni `readLine()` o `nextLine()` consuma una riga.
- **`File`**: rappresenta un percorso, non il contenuto; `exists`, `isFile`, `length`, `delete`, `list`; i percorsi relativi partono dalla cartella di lavoro.
- **Chiusura nel `finally`**: variabile a `null` fuori dal `try`, apertura nel `try`, guardia `!= null` e `close()` nel `finally`; con `BufferedReader`/`BufferedWriter` la `close()` dichiara `IOException`.
- **CSV**: `split(",")` scompone la riga; si convertono i campi con `parseInt`/`parseDouble`, si salta l'intestazione e si controllano `length` e spazi.

### API essenziali

| Classe | Costruttore / metodo | Eccezioni dichiarate |
|---|---|---|
| `PrintWriter` | `PrintWriter(String fileName)` | `FileNotFoundException` |
| `PrintWriter` | `PrintWriter(Writer out)`, `PrintWriter(OutputStream out)` | nessuna |
| `PrintWriter` | `void println(String x)`, `print`, `printf`, `flush()`, `close()`, `boolean checkError()` | nessuna |
| `FileWriter` | `FileWriter(String fileName)`, `FileWriter(String fileName, boolean append)` | `IOException` |
| `FileOutputStream` | `FileOutputStream(String name, boolean append)` | `FileNotFoundException` |
| `BufferedWriter` | `BufferedWriter(Writer out)`, `void write(String s)`, `void newLine()`, `void close()` | `IOException` (tranne il costruttore) |
| `FileReader` | `FileReader(String fileName)` | `FileNotFoundException` |
| `BufferedReader` | `BufferedReader(Reader in)` | nessuna |
| `BufferedReader` | `String readLine()`, `void close()` | `IOException` |
| `Scanner` | `Scanner(File source)` | `FileNotFoundException` |
| `Scanner` | `boolean hasNextLine()`, `String nextLine()`, `boolean hasNextInt()`, `int nextInt()`, `void close()` | nessuna controllata (`nextLine`: `NoSuchElementException`) |
| `File` | `File(String pathname)`, `boolean exists()`, `boolean isFile()`, `boolean isDirectory()`, `long length()`, `boolean delete()`, `String[] list()` | nessuna |
| `File` | `boolean createNewFile()` | `IOException` |
