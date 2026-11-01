# Livello 5: La Java Virtual Machine e la Concorrenza (Thread)

## 1. Multithreading e Sincronizzazione

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

*Esempio 1B: il thread NON si avvia nel proprio costruttore*
Può sembrare comodo far partire il thread da solo, con `this.start()` dentro il costruttore. **È un errore**, e le correzioni lo hanno penalizzato più volte. Il costruttore deve **preparare** l'oggetto; è **chi lo crea** a decidere quando farlo partire.

```java
// SBAGLIATO: il thread parte dentro il costruttore
public class ThreadAutoAvviante extends Thread {
    private String nome;

    public ThreadAutoAvviante(String nome) {
        this.start();            // il thread gira GIÀ, e il costruttore non ha finito
        this.nome = nome;        // quando run() legge 'nome' può trovare ancora null
    }

    @Override
    public void run() {
        System.out.println("Sono " + nome);
    }
}

// GIUSTO: il costruttore prepara, il chiamante fa partire
public class MioThread extends Thread {
    private String nome;

    public MioThread(String nome) {
        this.nome = nome;        // solo stato, nessun start()
    }

    @Override
    public void run() {
        System.out.println("Sono " + nome);
    }
}

// nel main (o in chi coordina):
MioThread t = new MioThread("A");
t.start();                       // la decisione è di chi crea
```

**Perché è sbagliato.**
- **Può partire due volte.** Se chi usa la classe fa, come ci si aspetta, `new Thread(oggetto).start()` o `oggetto.start()`, i thread che girano sullo **stesso oggetto** sono due. Con un `run()` che modifica uno stato (un bonus, un contatore), il risultato raddoppia.
- **Il thread può girare su un oggetto non ancora completo.** Dopo `start()` il nuovo thread è indipendente: può eseguire `run()` prima che il costruttore abbia assegnato i campi successivi, e prima che il costruttore di una **sottoclasse** abbia finito.
- **Toglie la decisione a chi coordina.** Quando la traccia dice "il manager crea **e avvia** i thread", l'avvio è del manager. Una classe che parte da sola gli ruba il lavoro: è l'anti-pattern che l'esame penalizza.

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

*Esempio 2B: il Runnable che possiede il proprio Thread (avvio su richiesta)*
In questo caso la classe non è un Thread, ma ne possiede uno interno (composizione) a cui passa se stessa (`this`). Il `Thread` si **prepara** nel costruttore e si **avvia** con un metodo esplicito: nel costruttore non si chiama `start()` (vedi Esempio 1B).
```java
public class RunnableConMotore implements Runnable {
    private Thread motore;                    // composizione: il Runnable possiede il suo Thread

    public RunnableConMotore() {
        motore = new Thread(this);            // solo preparato: NON avviato
    }

    public void avvia() {
        motore.start();                       // lo avvia chi coordina, quando vuole
    }

    public void attendi() throws InterruptedException {
        motore.join();
    }

    @Override
    public void run() {
        System.out.println("Runnable avviato su richiesta.");
    }
}

// Nel main:
// RunnableConMotore r = new RunnableConMotore();
// r.avvia();
// r.attendi();
```

*Esempio 2C: Implementazione tramite Classe Anonima o Lambda Expression*
Questa è una tecnica estremamente utile ed elegante (specie negli esami) per risparmiare tempo e definire un Thread al volo senza dover creare una classe esterna. Si può istanziare una classe anonima che implementa `Runnable`, oppure usare la sintassi iper-compatta delle Lambda.
```java
// Metodo con Classe Anonima
Runnable taskAnonimo = new Runnable() {
    @Override
    public void run() {
        System.out.println("Esecuzione parallela tramite classe anonima.");
    }
};
Thread t1 = new Thread(taskAnonimo);
t1.start();

// Metodo con Lambda Expression (moderno e rapido)
Runnable taskLambda = () -> {
    try {
        System.out.println("Esecuzione parallela tramite Lambda.");
        Thread.sleep(50);
    } catch(InterruptedException e) {
        System.out.println("Interrotto.");
    }
};
Thread t2 = new Thread(taskLambda);
t2.start();
```


### Gli Stati (Ciclo di Vita) di un Thread
1. **New**: Istanza appena creata, prima del `start()`.
2. **Runnable**: Dopo `start()`. È in coda, fiducioso che lo Scheduler di Sistema (che usa spesso algoritmi *Preemptive* e *Round-Robin*) gli assegni presto un "time-slice" (fetta di tempo) della CPU.
3. **Running**: Ha il controllo totale della CPU.
4. **Blocked**: Il thread è stato cacciato dalla CPU ed è "addormentato" in attesa di un I/O, della scadenza di un timer (`sleep`), o dello sblocco di un Monitor.
5. **Dead**: Il metodo `run()` è terminato. Il thread evapora.

### Metodi di Controllo e Sincronizzazione
- **`start()` vs `run()`:** Se invochi `run()` a mano, il codice viene eseguito in modo noiosamente sequenziale sul main thread! Per biforcare davvero l'esecuzione asincrona, devi categoricamente invocare **`start()`**.
- **`getName()` e `currentThread()`:** Ogni thread può avere un nome (es. `t1.setName("Downloader")`). All'interno del codice, puoi ottenere il riferimento al thread in esecuzione con `Thread.currentThread()` e recuperarne il nome con `.getName()`. Questo è vitale per il debugging in sistemi complessi.
- **Terminazione Pulita (Variabile Sentinella):** Mai usare metodi deprecati come `stop()` per uccidere un thread. L'approccio corretto è usare una **Variabile Sentinella** (un booleano `volatile` o un flag) che il thread controlla periodicamente nel suo ciclo. Quando il flag cambia, il thread esce dal metodo `run()` in modo naturale.
- **`sleep(millis)` e `yield()`:** `sleep` paralizza il thread a tempo, **senza mai rilasciare eventuali Lock** (pericolo!). `yield` è invece un atto di gentilezza: il thread rinuncia volontariamente alla sua fetta di tempo CPU a favore di un compagno con pari priorità.
- **`join()`:** Fondamentale. Ferma l'esecuzione del thread principale e lo costringe ad aspettare finché il thread bersaglio non è morto.
- **Race Condition e `synchronized`:** Se due thread toccano l'Heap in parallelo (es. `i++`), l'operazione non essendo "atomica" causa collisioni (Race Condition). Il modificatore `synchronized` trasforma un blocco in una cassaforte. Richiede un "Lock" (Monitor) su un oggetto: entra un solo thread alla volta, realizzando la **Mutua Esclusione**.

> **Nota Tecnica: La Keyword `volatile`**
> Quando si usa una **Variabile Sentinella** (come un flag booleano per fermare un thread), è fondamentale dichiararla come `volatile`. 
> In Java, ogni thread può creare una copia locale delle variabili nella cache della CPU per velocizzare l'esecuzione. Senza `volatile`, un thread potrebbe continuare a leggere il valore "vecchio" dalla sua cache, ignorando il cambiamento effettuato da un altro thread. La keyword `volatile` obbliga la JVM a leggere e scrivere la variabile direttamente nella **Memoria Centrale (RAM)**, garantendo la visibilità immediata delle modifiche a tutti i thread coinvolti.

### Il quadro dei metodi di `Thread`
| Metodo | Statico? | Cosa fa |
| :--- | :--- | :--- |
| `start()` | no | rende il thread schedulabile: la JVM invocherà `run()` su un nuovo flusso |
| `run()` | no | il codice da eseguire. **Invocarlo a mano non crea nessun thread** |
| `sleep(ms)` | **sì** | sospende il **thread corrente**. Si può chiamare da qualsiasi classe, anche senza avere un oggetto `Thread` sotto mano. **Non rilascia i lock** |
| `yield()` | **sì** | il thread corrente cede volontariamente la CPU ad altri di pari priorità, restando `runnable` |
| `join()` | no | attende la morte del thread bersaglio |
| `join(ms)` | no | come sopra, ma con un tetto massimo di attesa: dopo quel tempo il chiamante riprende comunque |
| `isAlive()` | no | `true` se il thread è partito e non è ancora morto |
| `getName()` / `setName(s)` | no | nome del thread, utile in stampa e debug. Si può passare anche al costruttore: `new Thread(task, "Bot-Alpha")` |
| `Thread.currentThread()` | **sì** | riferimento al thread che sta eseguendo in questo momento |
| `setPriority(int)` / `getPriority()` | no | priorità da `Thread.MIN_PRIORITY` (1) a `Thread.MAX_PRIORITY` (10), default `NORM_PRIORITY` (5) |
| `stop()`, `suspend()`, `resume()` | no | **deprecati**: interrompono senza permettere alcuna pulizia. Si usa una variabile sentinella `volatile` |

La priorità è un **suggerimento** allo scheduler, non una garanzia: quanta CPU tocchi davvero a un thread dipende anche dal sistema operativo. Non si progetta la correttezza di un programma sulle priorità.

### Su cosa si prende il lock
`synchronized` non blocca "il metodo": acquisisce il **monitor di un oggetto**. Cambia l'oggetto a seconda della forma:

```java
public synchronized void m() { ... }          // lock su 'this' (l'istanza)
public static synchronized void s() { ... }   // lock sull'oggetto Class: uno solo per TUTTA la classe
public void b() {
    synchronized (risorsa) { ... }            // lock sull'oggetto indicato: blocco arbitrario
}
```

Le prime due forme sono equivalenti a:

```java
public void m() { synchronized (this) { ... } }
public static void s() { synchronized (NomeClasse.class) { ... } }
```

Conseguenza pratica: un metodo `synchronized` d'istanza e uno `static synchronized` della stessa classe **non si escludono a vicenda**, perché i due lock sono diversi. E la forma a blocco è preferibile quando la sezione critica è solo una parte del metodo: tiene il lock per meno tempo.

### Nemesi e Coordinamento: `wait()`, `notify()` e Deadlock
Un **Deadlock (Stallo)** è un abbraccio mortale: il Thread A possiede il Lock 1 e aspetta il Lock 2. Il Thread B possiede il Lock 2 e aspetta il Lock 1. Nessuno molla la presa. Il software si pietrifica senza lanciare eccezioni.

Per un sano coordinamento (es. Produttore-Consumatore), Java offre (solo dentro aree `synchronized`):
- **`wait()`**: Il thread entra in un profondo sonno e, a differenza dello `sleep`, **rilascia immediatamente il Lock** che possedeva, permettendo ad altri di lavorare.
- **`notifyAll()`**: Urla al sistema di svegliare i compagni addormentati in `wait()` sullo stesso oggetto.

### Sintassi ed Esempio di Codice (Web Crawler Simulato)
Questo esempio mostra la sincronizzazione di una risorsa condivisa (una lista di URL visitati) e l'uso di nomi per i thread e di una variabile sentinella per la chiusura.

```java
import java.util.ArrayList;
import java.util.List;

public class WebCrawler implements Runnable {
    private final List<String> urlVisitati = new ArrayList<>();
    private volatile boolean attivo = true; // Variabile Sentinella

    public void arresta() {
        this.attivo = false;
    }

    public synchronized void logUrl(String url) {
        urlVisitati.add(url);
        System.out.println(Thread.currentThread().getName() + " ha analizzato: " + url);
        notifyAll(); 
    }

    @Override
    public void run() {
        String crawlerName = Thread.currentThread().getName();
        System.out.println("Crawler " + crawlerName + " in funzione...");

        while (attivo) {
            try {
                // Simula l'analisi di una pagina
                Thread.sleep(800); 
                logUrl("https://unime.it/page_" + (int)(Math.random() * 100));
            } catch (InterruptedException e) {
                System.out.println(crawlerName + " interrotto forzatamente.");
                break;
            }
        }
        System.out.println(crawlerName + " spento correttamente.");
    }

    public static void main(String[] args) throws InterruptedException {
        WebCrawler bot = new WebCrawler();
        
        Thread t1 = new Thread(bot, "Bot-Alpha");
        Thread t2 = new Thread(bot, "Bot-Beta");

        t1.start();
        t2.start();

        Thread.sleep(3000); // Lascia i bot lavorare
        bot.arresta(); // Terminazione pulita via sentinella

        t1.join();
        t2.join();
        System.out.println("Indicizzazione completata.");
    }
}
```
---

## 2. Il Coordinamento in Pratica: Produttore/Consumatore

### La regola d'oro: `wait()` va dentro un `while`, mai dentro un `if`
È il punto tecnico più importante di tutta la concorrenza in Java, e l'errore più frequente.

```java
// SBAGLIATO
if (buffer.isEmpty()) {
    wait();
}
preleva();     // può eseguire su un buffer vuoto!

// CORRETTO
while (buffer.isEmpty()) {
    wait();
}
preleva();     // qui la condizione è garantita falsa
```

Il motivo è che **`wait()` non promette che, al risveglio, la condizione sia cambiata.** Promette solo che qualcuno ha chiamato `notify`/`notifyAll` — o nemmeno quello:

1. **`notifyAll()` sveglia tutti.** Se tre consumatori aspettano e viene prodotto **un** elemento, tutti e tre si risvegliano e rientrano in competizione per il lock. Il primo consuma l'elemento; il secondo e il terzo, con un `if`, proseguirebbero come se ci fosse ancora qualcosa da prendere.
2. **Fra il risveglio e la riacquisizione del lock passa del tempo**, e in quel tempo un altro thread può aver cambiato di nuovo lo stato.
3. **Esistono i risvegli spuri** (*spurious wakeups*): la specifica Java consente che un thread esca da `wait()` senza che nessuno l'abbia notificato.

Il `while` è l'unica forma che ricontrolla la condizione dopo ogni risveglio. Con l'`if` la controlli una volta sola, prima di dormire, e agisci su un'informazione vecchia.

**Vincolo di linguaggio:** `wait()`, `notify()` e `notifyAll()` si possono invocare **solo** possedendo il lock dell'oggetto, cioè dentro un metodo o un blocco `synchronized` su quell'oggetto. Fuori, la JVM lancia `IllegalMonitorStateException` a runtime (il codice compila).

### Esempio completo: Buffer condiviso con capienza limitata (FIFO)
Lo schema classico: un `Deposito` con capienza massima, produttori che si bloccano quando è pieno, consumatori che si bloccano quando è vuoto.

```java
import java.util.LinkedList;
import java.util.Queue;

class Deposito {
    // La risorsa condivisa è privata: nessuno la tocca se non attraverso i metodi sincronizzati.
    private final Queue<Integer> coda = new LinkedList<>();
    private final int capienza;

    public Deposito(int capienza) {
        this.capienza = capienza;   // assegnare DAVVERO il parametro: vedi Errori Comuni
    }

    // synchronized => mutua esclusione: un solo thread alla volta dentro questo metodo.
    public synchronized void inserisci(int valore) throws InterruptedException {
        while (coda.size() == capienza) {   // while, non if
            wait();                          // rilascia il lock e dorme
        }
        coda.add(valore);                    // add in coda
        System.out.println(Thread.currentThread().getName() + " ha prodotto " + valore);
        notifyAll();                         // sveglia chi aspetta (produttori E consumatori)
    }

    public synchronized int preleva() throws InterruptedException {
        while (coda.isEmpty()) {             // while, non if
            wait();
        }
        int valore = coda.poll();            // poll dalla TESTA => FIFO
        System.out.println(Thread.currentThread().getName() + " ha consumato " + valore);
        notifyAll();
        return valore;
    }

    // Un getter LEGGE E BASTA: sincronizzato per la visibilità, mai bloccante.
    public synchronized int getDimensione() {
        return coda.size();
    }
}

class Produttore implements Runnable {
    private final Deposito deposito;
    public Produttore(Deposito deposito) { this.deposito = deposito; }

    @Override
    public void run() {
        try {
            for (int i = 1; i <= 5; i++) {
                deposito.inserisci(i);
                Thread.sleep(50);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();   // ripristina il flag, non ingoiare l'interruzione
        }
    }
}

class Consumatore implements Runnable {
    private final Deposito deposito;
    public Consumatore(Deposito deposito) { this.deposito = deposito; }

    @Override
    public void run() {
        try {
            for (int i = 1; i <= 5; i++) {
                deposito.preleva();
                Thread.sleep(80);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

class Magazzino {
    public static void main(String[] args) throws InterruptedException {
        Deposito deposito = new Deposito(3);

        Thread p = new Thread(new Produttore(deposito), "Produttore");
        Thread c = new Thread(new Consumatore(deposito), "Consumatore");

        p.start();
        c.start();
        p.join();
        c.join();

        System.out.println("Elementi rimasti: " + deposito.getDimensione());
    }
}
```

> **FIFO contro LIFO.** Con una `Queue` si aggiunge in coda (`add`) e si preleva dalla testa (`poll`): primo entrato, primo uscito. Se implementi il buffer con un array e **un solo indice**, usato sia per inserire sia per prelevare, ottieni una pila (LIFO): l'ultimo prodotto è il primo consumato. Compila, sembra funzionare, e se la traccia parla di "coda" o mostra un ordine atteso nell'output è un errore logico che costa punti. Servono **due indici** (o una `Queue`).

---

## 3. Parallelismo Reale con `join()`

`join()` blocca il thread chiamante finché il thread bersaglio non è morto. Serve a due cose: aspettare che il lavoro sia finito, e leggere in sicurezza il risultato prodotto dal thread (dopo `join()` la visibilità in memoria è garantita).

### L'errore che annulla il parallelismo
```java
// SBAGLIATO: avvia e aspetta nello stesso ciclo
for (int i = 0; i < n; i++) {
    ContaThread t = new ContaThread(dati, i);
    t.start();
    t.join();      // il main si ferma qui: il thread successivo parte solo dopo
}
// Risultato: i thread girano UNO DOPO L'ALTRO. Nessun parallelismo.

// CORRETTO: due cicli distinti
ContaThread[] worker = new ContaThread[n];
for (int i = 0; i < n; i++) {
    worker[i] = new ContaThread(dati, i);
    worker[i].start();          // 1° ciclo: li avvia TUTTI
}
for (int i = 0; i < n; i++) {
    worker[i].join();           // 2° ciclo: li aspetta TUTTI
}
```

**Il pattern è sempre lo stesso: un ciclo che avvia, un ciclo che aspetta.** Mai i due nello stesso `for`.

### Esempio: partizionare un array fra più thread
```java
class ContaPari extends Thread {
    private final int[] dati;
    private final int da, a;
    private int risultato;      // scritto dal thread, letto dal main DOPO il join()

    public ContaPari(int[] dati, int da, int a) {
        this.dati = dati;
        this.da = da;
        this.a = a;
    }

    @Override
    public void run() {
        for (int i = da; i < a; i++) {
            if (dati[i] % 2 == 0) {
                risultato++;
            }
        }
    }

    // Getter sul TIPO CONCRETO: il main deve dichiarare ContaPari, non Thread.
    public int getRisultato() { return risultato; }
}

class Analizzatore {
    public static void main(String[] args) throws InterruptedException {
        int[] dati = new int[1000];
        for (int i = 0; i < dati.length; i++) dati[i] = i;

        int nThread = 4;
        int blocco = dati.length / nThread;
        ContaPari[] worker = new ContaPari[nThread];   // NON Thread[]: servirebbe un cast

        for (int i = 0; i < nThread; i++) {
            int da = i * blocco;
            int a = (i == nThread - 1) ? dati.length : da + blocco;   // l'ultimo prende il resto
            worker[i] = new ContaPari(dati, da, a);
            worker[i].start();
        }

        int totale = 0;
        for (int i = 0; i < nThread; i++) {
            worker[i].join();                  // prima aspetta...
            totale += worker[i].getRisultato(); // ...poi legge
        }
        System.out.println("Numeri pari: " + totale);
    }
}
```

Ogni worker scrive in un campo **proprio**: nessuna variabile condivisa, quindi nessun `synchronized` necessario. La sincronizzazione serve solo quando più thread toccano lo *stesso* dato.

### Con `Runnable` i due oggetti sono due: `Reparto[]` e `Thread[]`
L'esempio sopra usa `extends Thread`: l'oggetto **è** il thread, quindi un solo array basta. Ma le tracce spesso dicono *"`Reparto` implementa `Runnable`"* (o lasciano libera la scelta, e `Runnable` è quella consigliata). Allora **gli oggetti sono due per ogni lavoro**: il `Runnable` (che ha i dati e il getter del risultato) e il `Thread` che lo esegue (che ha `start()` e `join()`). Servono **due array paralleli**, e il getter si chiama sempre sul `Runnable`.

L'esempio completo, su una **matrice** con un thread per riga:

```java
import java.util.*;

class Reparto implements Runnable {
    private int[] misure;
    private int min;
    private int max;
    private int fuori = 0;                       // scritto dal thread, letto dal main DOPO il join()

    public Reparto(int[] misure, int min, int max) {
        this.misure = misure;
        this.min = min;
        this.max = max;
    }

    @Override
    public void run() {
        for (int i = 0; i < misure.length; i++) {
            if (misure[i] < min || misure[i] > max) fuori++;
        }
    }

    public int getFuori() {
        return fuori;
    }
}

class Controllo {
    private int[] parziali = new int[0];

    public int esamina(int[][] matrice, int min, int max) {
        Reparto[] lavori = new Reparto[matrice.length];     // i dati: hanno getFuori()
        Thread[] thread = new Thread[matrice.length];       // i thread: hanno start() e join()
        for (int i = 0; i < matrice.length; i++) {          // ciclo 1: crea e avvia TUTTI
            lavori[i] = new Reparto(matrice[i], min, max);
            thread[i] = new Thread(lavori[i]);
            thread[i].start();
        }
        parziali = new int[matrice.length];
        int totale = 0;
        for (int i = 0; i < matrice.length; i++) {          // ciclo 2: aspetta, poi legge
            try {
                thread[i].join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            parziali[i] = lavori[i].getFuori();             // il getter è sul Reparto, non sul Thread
            totale += parziali[i];
        }
        return totale;
    }

    public int[] getParziali() {
        return parziali.clone();                            // copia: niente privacy leak
    }
}
```

Con la matrice `{{8,12,25,10}, {15,20,11}, {30,9,21,14,5}, {}}` e l'intervallo `[10, 20]`: `esamina` restituisce `6` e `getParziali()` `[2, 0, 4, 0]`. La riga vuota è un reparto con zero misure: il suo thread parte, il ciclo non gira, `getFuori()` vale `0`.

**Cinque cose da ricordare.**
1. **Due cicli**, non uno: il primo crea e avvia, il secondo aspetta e legge.
2. **Il risultato si legge dopo il `join()`**, e dal `Runnable` (`lavori[i].getFuori()`): `thread[i].getFuori()` non compila.
3. **`join()` dichiara `InterruptedException`**: se il metodo non la dichiara (la traccia dice "la gestisce internamente"), `try/catch` attorno al `join()`.
4. **`getParziali()` restituisce una copia** (`clone()`), non il campo.
5. **Una riga = un thread** quando la traccia dice "un `Reparto` per ogni riga": `matrice.length` thread, nessuna formula di partizionamento.

### Partizionare un array fra `n` thread: il `for`, non il `while`
Quando il numero di thread è un **parametro** (non uno per riga), l'array va diviso in `n` blocchi. L'ultimo prende il resto della divisione. Il ciclo è un `for` su `i`, con gli estremi calcolati per ogni blocco.

```java
int passo = dati.length / n;                          // dimensione base di un blocco
for (int i = 0; i < n; i++) {
    int da = i * passo;
    int a = (i == n - 1) ? dati.length : (i + 1) * passo;   // l'ultimo arriva fino in fondo
    lavori[i] = new ContaPositivi(dati, da, a);        // [da, a): 'a' ESCLUSO
    thread[i] = new Thread(lavori[i]);
    thread[i].start();
}
```

**Perché non il `while`.** Un ciclo come `while (fine != dati.length - 1)` con gli indici aggiornati a mano è fragile: con `n = 1` la condizione è già falsa alla partenza e il ciclo **non gira mai**, quindi nessun thread parte e il risultato è `0`. Il `for` su `i` funziona anche con `n = 1`, e con `n` che non divide la lunghezza (`1000` elementi su `3` thread: blocchi da `333`, `333` e `334`). **Estremo escluso:** se la traccia dice "da `inizio` incluso a `fine` escluso", il ciclo è `i < fine`, non `i <= fine`.

---

## 4. Errori Comuni sulla Concorrenza

- **`wait()` dentro un `if`.** Trattato sopra: è l'errore numero uno.
- **Un getter che si mette in attesa.** `public synchronized int getDimensione() { while (coda.isEmpty()) wait(); ... }` è concettualmente sbagliato: chiedere *"quanti elementi ci sono?"* non deve mai bloccare il chiamante. Se il buffer è vuoto la risposta corretta è `0`, immediata. Un getter legge e torna.
- **Chiamare `run()` invece di `start()`.** Il metodo viene eseguito, in modo perfettamente sequenziale, sul thread chiamante. Nessun thread nuovo nasce e il programma sembra funzionare.
- **`start()` e `join()` nello stesso ciclo.** Annulla il parallelismo (vedi sopra).
- **Dichiarare l'array come `Thread[]` e poi chiamare un getter del worker.** `Thread` non conosce `getRisultato()`: con `extends Thread` si dichiara l'array del tipo concreto, con `Runnable` servono **due array** (`Reparto[]` per i dati, `Thread[]` per `start`/`join`), come nell'esempio sopra.
- **`start()` nel costruttore del thread.** Può far partire il lavoro due volte e su un oggetto non ancora completo; l'avvio spetta a chi coordina (vedi Esempio 1B).
- **Campo mai assegnato nel costruttore.** `public Deposito(int capienza) { capienza = capienza; }` assegna il parametro a se stesso: il campo resta a `0` e il buffer si comporta come se fosse sempre pieno. Serve `this.capienza = capienza;`. È un bug che i test sullo stato finale spesso non intercettano, perché il valore finale può coincidere per caso.
- **`synchronized` su metodi che non toccano lo stato condiviso.** Non è più sicuro: è solo più lento, e segnala che non si è capito su cosa serve la mutua esclusione.
- **Il lock è sull'oggetto, non sul metodo.** Due metodi `synchronized` della stessa istanza si escludono a vicenda; gli stessi metodi su **due istanze diverse** non si escludono affatto. Se la risorsa condivisa deve essere unica, deve esserci **un solo oggetto** condiviso fra i thread.
- **Deadlock AB-BA.** Due thread che prendono due lock in ordine opposto (`A` poi `B` uno, `B` poi `A` l'altro) si bloccano a vicenda per sempre. La difesa è banale e va ricordata: **acquisire sempre i lock nello stesso ordine** in tutto il programma. L'esempio completo, con i due conti, è nell'ultima sezione.
- **`sleep()` non rilascia il lock, `wait()` sì.** Dormire dentro un blocco `synchronized` congela tutti gli altri thread in attesa di quel lock.

---

## 5. Deadlock AB-BA: il trasferimento fra due conti

È l'esercizio classico: due conti, due thread che si trasferiscono denaro **in direzioni opposte**. Il `synchronized` sul metodo non basta.

```java
// INCOMPLETO: blocca solo il conto di ORIGINE
public synchronized void trasferisci(Conto destinazione, int importo) {
    saldo -= importo;
    destinazione.setSaldo(destinazione.getSaldo() + importo);   // due chiamate separate sul conto di destinazione
}
```

Qui `synchronized` tiene il lock di `this` per tutta l'operazione, ma il conto di **destinazione** viene toccato con `getSaldo()` e `setSaldo()` separati, ciascuno dei quali (se sono `synchronized`) prende e rilascia subito il proprio lock: fra la lettura e la scrittura c'è una finestra in cui un altro thread può modificare lo stesso saldo. E se si prova a risolvere bloccando entrambi i conti, senza un ordine, si cade nel deadlock: il thread `A→B` tiene `A` e chiede `B`; il thread `B→A` tiene `B` e chiede `A`; restano bloccati per sempre.

**La soluzione: entrambi i lock, per tutta l'operazione, sempre nello stesso ordine globale.** L'ordine lo dà un **identificativo progressivo** assegnato nel costruttore con un contatore `static`.

```java
class Conto {
    private static int prossimoId = 1;           // condiviso da tutti i Conto
    private final int id;
    private int saldo;

    public Conto(int saldo) {
        this.id = prossimoId++;                  // assegnato nel costruttore: 1, 2, 3...
        this.saldo = saldo;
    }

    public int getId() { return id; }
    public synchronized int getSaldo() { return saldo; }

    public void trasferisci(Conto destinazione, int importo) {
        // Lock SEMPRE nello stesso ordine globale (per id), qualunque sia la direzione.
        Conto primo = (this.id < destinazione.id) ? this : destinazione;
        Conto secondo = (primo == this) ? destinazione : this;
        synchronized (primo) {
            synchronized (secondo) {             // entrambi bloccati per TUTTA l'operazione
                this.saldo -= importo;
                destinazione.saldo += importo;
            }
        }
    }
}
```

**Perché funziona.** `A→B` e `B→A` prendono **entrambi** prima il conto con l'id più piccolo: non esiste un istante in cui un thread tenga il lock del conto grande e aspetti il piccolo. L'attesa circolare, che è la condizione del deadlock, è impossibile. Con due thread da 20 000 trasferimenti di segno opposto il programma termina sempre, e i saldi finali tornano agli iniziali.

**Tre punti da ricordare.**
1. **Il contatore è `static`**, altrimenti ogni conto avrebbe il suo e tutti gli `id` varrebbero `1`. Un `id` che resta `0` per ogni conto è il sintomo del costruttore non scritto.
2. **`synchronized (oggetto)` a blocchi annidati**, non `synchronized` sul metodo: il metodo blocca solo `this`.
3. **L'ordine si stabilisce con un dato che non cambia** (l'`id`, `final`), non con il saldo né con l'ordine degli argomenti.

