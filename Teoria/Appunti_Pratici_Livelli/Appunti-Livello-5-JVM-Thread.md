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
- **`getName()` e `currentThread()`:** Ogni thread può avere un nome (es. `t1.setName("Downloader")`). All'interno del codice, puoi ottenere il riferimento al thread in esecuzione con `Thread.currentThread()` e recuperarne il nome con `.getName()`. Questo è vitale per il debugging in sistemi complessi.
- **Terminazione Pulita (Variabile Sentinella):** Mai usare metodi deprecati come `stop()` per uccidere un thread. L'approccio corretto è usare una **Variabile Sentinella** (un booleano `volatile` o un flag) che il thread controlla periodicamente nel suo ciclo. Quando il flag cambia, il thread esce dal metodo `run()` in modo naturale.
- **`sleep(millis)` e `yield()`:** `sleep` paralizza il thread a tempo, **senza mai rilasciare eventuali Lock** (pericolo!). `yield` è invece un atto di gentilezza: il thread rinuncia volontariamente alla sua fetta di tempo CPU a favore di un compagno con pari priorità.
- **`join()`:** Fondamentale. Ferma l'esecuzione del thread principale e lo costringe ad aspettare finché il thread bersaglio non è morto.
- **Race Condition e `synchronized`:** Se due thread toccano l'Heap in parallelo (es. `i++`), l'operazione non essendo "atomica" causa collisioni (Race Condition). Il modificatore `synchronized` trasforma un blocco in una cassaforte. Richiede un "Lock" (Monitor) su un oggetto: entra un solo thread alla volta, realizzando la **Mutua Esclusione**.

> **Nota Tecnica: La Keyword `volatile`**
> Quando si usa una **Variabile Sentinella** (come un flag booleano per fermare un thread), è fondamentale dichiararla come `volatile`. 
> In Java, ogni thread può creare una copia locale delle variabili nella cache della CPU per velocizzare l'esecuzione. Senza `volatile`, un thread potrebbe continuare a leggere il valore "vecchio" dalla sua cache, ignorando il cambiamento effettuato da un altro thread. La keyword `volatile` obbliga la JVM a leggere e scrivere la variabile direttamente nella **Memoria Centrale (RAM)**, garantendo la visibilità immediata delle modifiche a tutti i thread coinvolti.

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