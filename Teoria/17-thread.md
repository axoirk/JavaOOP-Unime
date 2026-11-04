---
materia: Programmazione a Oggetti
capitolo: 17
titolo: Thread
livello_syllabus: 5
stato: completo
slide: ["Multithreading.pdf slide 1-33", "Threads.pdf slide 1-30"]
appelli: [EXAM1]
fonti_esterne: 11
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 17 — Thread

## Di cosa parla questo capitolo

Tutti i programmi che abbiamo scritto fin qui hanno un solo **flusso di esecuzione**: il `main` parte, esegue un'istruzione dopo l'altra, e il programma finisce quando il `main` finisce. Basta questo per tanti problemi, ma non per tutti. Immaginiamo un programma che deve scaricare un file e intanto continuare a rispondere ai clic dell'utente; oppure un programma che deve sommare i numeri di un array molto lungo e vuole farlo con più "operai" che lavorano ciascuno su una parte dell'array. In casi come questi serve poter dire: *queste due attività vanno avanti insieme*.

In Java si ottiene con i **thread** (*thread*, in italiano "filo" di esecuzione): ogni thread è un flusso di istruzioni che procede per conto suo, dentro lo stesso programma, e tutti i thread di un programma lavorano **sulla stessa memoria**. Questa è insieme la loro forza (comunicare è facile: basta leggere e scrivere gli stessi oggetti) e il loro pericolo (due thread che toccano lo stesso dato nello stesso momento possono combinare guai: ne parliamo nel [Capitolo 18](18-sincronizzazione.md)).

In questo capitolo vedremo:

- che cosa sono un **processo** e un **thread**, che cosa condividono e che cosa no, e perché l'ordine in cui i thread procedono **non è prevedibile**;
- la classe **`Thread`**, i metodi **`run`** e **`start`**, e la differenza tra chiamare l'uno o l'altro;
- i **due modi** di creare un thread: estendere `Thread` oppure realizzare l'interfaccia **`Runnable`**, e quando conviene l'uno o l'altro;
- il **ciclo di vita** di un thread (gli stati, la terminazione, la variabile **sentinella** con `volatile`);
- i metodi di controllo: **`currentThread`**, **`getName`**/**`setName`**, **`sleep`**, **`yield`**, **`join`**, **`isAlive`**, le **priorità**, e l'eccezione **`InterruptedException`**;
- come far lavorare **più thread insieme** su un problema: la partizione di un array tra `n` thread, con il pattern *avvia tutti, poi aspetta tutti*;
- gli **scheletri** da saper scrivere a memoria e gli **errori tipici**.

Questo capitolo si appoggia su molti dei precedenti. Un thread è un **oggetto** ([Capitolo 7](07-classi-e-oggetti.md)); `Runnable` è un'**interfaccia** e `Thread` si può **estendere** ([Capitolo 9](09-ereditarieta-e-polimorfismo.md) e [Capitolo 10](10-classi-astratte-e-interfacce.md)); le classi anonime del paragrafo 17.3.4 sono nel [Capitolo 11](11-classi-annidate.md); `InterruptedException` è un'eccezione **controllata** ([Capitolo 13](13-eccezioni.md)); per capire che cosa i thread condividono servono lo stack e lo heap del [Capitolo 8](08-riferimenti-e-memoria.md). I dati da condividere in modo sicuro, con `synchronized`, `wait` e `notifyAll`, sono il tema del capitolo successivo.

> [!IMPORTANT]
> **Nota per l'esame — Thread**
> I thread sono il tema tipico di uno dei due esercizi grandi. Nei compiti ufficiali la traccia dà sempre l'**output atteso**: perciò i programmi d'esame sono scritti in modo che l'output sia **sempre lo stesso**, qualunque sia l'ordine in cui lo scheduler fa procedere i thread. Il mezzo per ottenerlo è quasi sempre **`join`**: si fa terminare ogni thread *prima* di stampare il risultato che da esso dipende (paragrafi 17.5.4 e 17.6). Il codice che serve a memoria è poco, ma va scritto **esatto**: `public void run()`, `start()` e non `run()`, `join()` dentro un `try`/`catch` di `InterruptedException`.

---

## 17.1 Dal flusso unico ai flussi paralleli

### 17.1.1 Processi e multitasking

Un **processo** (*process*, o *task*) è un flusso di esecuzione del processore che corrisponde a un programma in esecuzione. La caratteristica fondamentale di un processo è che ha uno **spazio di memoria privato**: nessun altro processo può accedervi, salvo casi eccezionali come la memoria condivisa esplicita. Il **contesto** di un processo è tutto ciò che serve per riprenderlo esattamente da dove era stato interrotto: lo stato dei registri del processore, la memoria del processo, i dati che gestisce e il suo *stack* (lo spazio per le chiamate dei metodi e le variabili locali, [Capitolo 8](08-riferimenti-e-memoria.md)).

Un computer ha molti più processi in esecuzione che processori. Il sistema operativo li fa avanzare tutti con il **multitasking**: l'esecuzione è *contemporanea o pseudo-contemporanea*. Il tipo più diffuso è il multitasking a **time-slicing** (o *time-sharing*) e **preemptive**:

- con il **time-slicing** il sistema operativo assegna la CPU a ogni processo per un intervallo di tempo prefissato, e poi passa a un altro, **senza che il processo lo sappia o intervenga**. Il passaggio da un processo all'altro si chiama **cambio di contesto** (*context switch*);
- con il comportamento **preemptive** (*con prelazione*) un processo di priorità maggiore può sottrarre il processore a uno di priorità minore;
- tra processi di **uguale priorità** si usa di solito il **round-robin**: un processo, dopo che ha usato la sua porzione di tempo, finisce **in fondo alla coda** dei processi in attesa con la stessa priorità.

### 17.1.2 Che cos'è un thread

Il processo è un'unità indivisibile: se un programma vuole fare due cose in parallelo, con i soli processi deve creare due processi figli indipendenti, che per scambiarsi dati devono ricorrere a meccanismi di comunicazione laboriosi. Il **thread** risolve il problema spezzando il processo.

> [!NOTE]
> **Definizione — Thread**
> Un **thread** è un flusso di esecuzione *dentro* un processo, in cui le operazioni si svolgono nel modo procedurale di sempre (un'istruzione dopo l'altra). Un processo può contenere più thread; i thread dello stesso processo **condividono le stesse aree di memoria**, ad eccezione dello **stack**, che ciascun thread possiede per le proprie variabili locali e le proprie chiamate.

Le conseguenze di questa condivisione sono due, una buona e una cattiva:

- **il cambio di contesto tra thread è molto meno pesante** di quello tra processi, e **comunicare è molto più semplice**, perché un thread può leggere e scrivere gli stessi oggetti di un altro;
- proprio perché la memoria è condivisa, i **problemi di sincronizzazione** diventano frequenti e rilevanti: due thread che modificano lo stesso dato possono dare risultati sbagliati (paragrafo 17.6.5 e [Capitolo 18](18-sincronizzazione.md)).

Anche in Java vale la differenza: un **multitasking** gestisce processi, ciascuno con la propria memoria locale; il **multithreading** realizza più flussi di controllo *concorrenti* all'interno di una stessa applicazione, che condividono i dati e che il programmatore può controllare e coordinare con appositi metodi.

I vantaggi che la programmazione con i thread offre, in sintesi:

1. **non si blocca l'utente**: i thread sono indipendenti e si possono svolgere più operazioni nello stesso momento;
2. **si risparmia tempo** facendo più cose insieme;
3. **un'eccezione in un thread non influisce sugli altri**: ogni thread è un percorso di esecuzione separato (lo vedremo nel paragrafo 17.4.3).

> [!TIP]
> **Intuizione — L'officina e gli artigiani**
> Un processo è come un'officina con i suoi banchi, i suoi materiali e i suoi addetti: due officine non si scambiano gli attrezzi. I thread sono gli artigiani **della stessa officina**: ognuno ha un proprio foglio su cui segna i passaggi del lavoro che sta facendo (lo stack), ma tutti prendono dallo stesso armadio dei materiali e lavorano sullo stesso banco (lo heap). Lavorare in due è più veloce, e passarsi un pezzo è immediato; ma se due artigiani vogliono lo stesso attrezzo nello stesso istante, bisogna mettersi d'accordo. L'analogia funziona fino a un certo punto: un artigiano vede che cosa fa il collega, i thread no, e possono "vedersi" solo attraverso i dati che condividono.

### 17.1.3 Che cosa è privato e che cosa è condiviso

La macchina virtuale Java ([Capitolo 1](01-java-e-la-jvm.md) e [Capitolo 8](08-riferimenti-e-memoria.md)) organizza la memoria in aree. Quando ci sono più thread, le aree si dividono così:

| Area | Di chi è | Che cosa contiene |
|---|---|---|
| **Program counter** | di **ciascun** thread | l'istruzione a cui il thread è arrivato |
| **Stack** | di **ciascun** thread | variabili locali e parametri dei metodi in corso |
| **Heap** | **condiviso** da tutti i thread | gli oggetti, creati dinamicamente e raccolti dal *garbage collector* |
| **Method area** | **condivisa** | la descrizione delle classi (campi, metodi), caricata dal class loader |

La regola pratica che se ne ricava, da tenere a mente per il resto del capitolo, è questa:

> [!IMPORTANT]
> **Nota per l'esame — Locale o condiviso**
> Le **variabili locali** (e i parametri) di un metodo sono **private di ogni thread**: due thread che eseguono lo stesso metodo hanno due copie distinte delle sue variabili locali. I **campi degli oggetti** e le variabili `static` stanno nello heap e sono **visibili a tutti i thread** che ne possiedono un riferimento. Due thread sono "in conflitto" solo se toccano lo stesso oggetto.

### 17.1.4 Concorrenza e ordine imprevedibile

Con una sola CPU, due thread non possono davvero andare avanti nello stesso istante: lo scheduler (la parte della JVM e del sistema operativo che decide chi esegue) li alterna a piccoli intervalli, in modo analogo al time-slicing dei processi. Con più CPU alcuni thread possono davvero procedere in parallelo. In entrambi i casi la conseguenza per noi è la stessa e va scolpita bene:

> [!WARNING]
> **Attenzione — L'ordine tra thread non è deciso dal programma**
> Se due thread stampano righe, **l'ordine in cui le righe compaiono può cambiare da un'esecuzione all'altra**. Il programma non decide quando un thread viene sospeso e quando riprende. Un programma corretto non deve dipendere da questo ordine: quando un risultato dipende dalla fine di un altro thread, si usa `join` (paragrafo 17.5.4) e si ha la certezza.

### 17.1.5 Il thread principale, e quando finisce il programma

Ogni programma Java ha **almeno un thread**: quello che esegue il `main`, detto **thread principale** (*main thread*), e che ha il nome `main`. Tutti gli altri thread li crea il programma. Una conseguenza che sorprende: il programma **non finisce quando finisce il `main`**.

> [!NOTE]
> **Approfondimento esterno — Quando termina la JVM**
> La documentazione Java SE 17 della classe `Thread` dice che la macchina virtuale Java continua a eseguire thread fino a quando si verifica una di due cose: viene chiamato il metodo `exit` della classe `Runtime`, oppure *tutti i thread che non sono daemon sono morti*, sia perché sono usciti dalla chiamata a `run`, sia perché un'eccezione è uscita da `run` senza essere gestita. Un thread *daemon* è un thread di servizio, che non trattiamo; tutti i thread che creeremo in questo capitolo sono **non daemon**.
>
> *Fonte:* [Thread (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html)

Vediamo la cosa con un esempio. Il `main` crea un thread che dorme un istante e poi stampa, e finisce subito.

#### Esempio — Il `main` finisce per primo

```java
public class MainFinisceSubito {
    public static void main(String[] args) {
        Thread t = new Thread() {                    // classe anonima che estende Thread (Capitolo 11)
            public void run() {
                try {
                    Thread.sleep(200);               // il thread aspetta 200 millisecondi
                } catch (InterruptedException e) {
                }
                System.out.println("il thread ha finito");
            }
        };
        t.start();                                   // il thread parte
        System.out.println("il main ha finito");     // il main arriva in fondo subito
    }
}
```

```text
il main ha finito
il thread ha finito
```

Il `main` stampa e termina; ma il programma resta in vita ancora 200 millisecondi, finché il thread non ha finito. La riga del thread esce **dopo** quella del `main` perché il thread sta dormendo; questa volta l'ordine è prevedibile solo perché abbiamo imposto una pausa di durata molto superiore al tempo che il `main` impiega a stampare.

---

## 17.2 La classe `Thread`, `run` e `start`

### 17.2.1 Ogni thread è un oggetto

In Java ogni thread è un **oggetto**: è un'istanza della classe **`java.lang.Thread`**. La classe sta nel package `java.lang`, quindi **non serve nessun `import`**. Un oggetto `Thread` ha due compiti: contiene il **codice che il thread deve eseguire**, nel metodo `run()`, e ha i metodi per controllare il thread (avviarlo, attenderlo, dargli un nome, e così via).

I due metodi da distinguere subito, senza confusione:

- **`run()`** è il metodo che contiene il codice del thread. Lo scriviamo noi, ma **non lo chiamiamo noi**;
- **`start()`** è il metodo che **crea il nuovo flusso di esecuzione**: la JVM lo chiama e fa eseguire `run()` in quel nuovo flusso. Terminato `run()`, il thread cessa la sua attività e le risorse che aveva impegnato vengono rilasciate.

> [!NOTE]
> **Approfondimento esterno — `Thread`, `run` e `start`**
> La documentazione Java SE 17 dichiara `public class Thread extends Object implements Runnable`. Dice che *esistono due modi* di creare un nuovo thread: dichiarare una sottoclasse di `Thread` che **ridefinisce** il metodo `run`, oppure dichiarare una classe che **realizza l'interfaccia `Runnable`** e quindi definisce `run`. Il metodo `public void start()` *"causes this thread to begin execution; the Java Virtual Machine calls the `run` method of this thread"* e dichiara **`IllegalThreadStateException`** "se il thread è già stato avviato": *"It is never legal to start a thread more than once. In particular, a thread may not be restarted once it has completed execution."* Il metodo `public void run()` chiama `run` dell'oggetto `Runnable` con cui il thread è stato costruito; se il thread non ha un `Runnable`, `run` **non fa nulla**. `IllegalThreadStateException` estende `IllegalArgumentException`, quindi è **non controllata**.
>
> *Fonte:* [Thread (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html)

### 17.2.2 Lo schema interno di `Thread`

Per capire perché i due modi di creare un thread (paragrafo 17.3) funzionano, conviene guardare uno schema semplificato della classe `Thread`:

```text
public class Thread implements Runnable {
    Runnable target;                       // il "lavoro" da eseguire, può essere null

    public void start() { ... run(); }     // lancia il thread: la JVM esegue run() in un nuovo flusso

    public void run() {
        if (target != null) { target.run(); }   // se c'è un Runnable, esegue il suo run()
    }

    public Thread(Runnable t) { target = t; ... }
}

public interface Runnable {
    public abstract void run();
}
```

Lo schema dice due cose. La prima: `Thread.run()` di per sé **non fa nulla**, a meno che il thread sia stato costruito con un oggetto `Runnable`: in quel caso chiama il `run` di quell'oggetto. La seconda: `start()` è il metodo che "lancia" il thread, rendendolo *schedulabile*, cioè pronto a essere scelto dallo scheduler. Il codice reale di `start` crea il flusso e *poi* esegue `run()` al suo interno: ecco perché `run()` non va mai chiamato direttamente.

Quindi per avere un thread che fa qualcosa bisogna riempire `run()`: o **ridefinendolo** in una sottoclasse di `Thread` (primo modo), oppure **fornendo un `Runnable`** al costruttore (secondo modo).

### 17.2.3 `start` contro `run`

Vediamo con un programma la differenza tra le due chiamate. La classe `Saluto` estende `Thread` e il suo `run` stampa il nome del thread che lo sta eseguendo, ottenuto con `Thread.currentThread().getName()` (paragrafo 17.5.1).

```java
class Saluto extends Thread {
    public void run() {
        System.out.println("run() eseguito da: " + Thread.currentThread().getName());
    }
}

public class StartControRun {
    public static void main(String[] args) throws InterruptedException {
        Saluto s = new Saluto();
        s.run();         // chiamata ordinaria: nessun nuovo thread
        s.start();       // nuovo thread: la JVM esegue run() al suo interno
        s.join();        // il main aspetta la fine del thread (paragrafo 17.5.4)
    }
}
```

```text
run() eseguito da: main
run() eseguito da: Thread-0
```

La prima chiamata, `s.run()`, è un **metodo qualunque**: viene eseguito dal thread che lo chiama, cioè dal `main`, e il programma resta a un solo flusso. La seconda, `s.start()`, crea davvero un nuovo thread: questa volta `run` è eseguito dal thread chiamato `Thread-0`, il nome che Java dà al primo thread senza nome creato dal programma.

> [!WARNING]
> **Attenzione — Il thread parte una sola volta**
> Chiamare `start()` due volte sullo stesso oggetto lancia **`IllegalThreadStateException`**, anche se il primo thread è già finito. Un thread che è terminato non si riavvia: per rifare lo stesso lavoro si crea un **nuovo** oggetto `Thread` (con lo stesso `Runnable`, se serve).

### 17.2.4 I costruttori di `Thread`

I costruttori che servono sono quattro; tutti `public`, nessuno dichiara eccezioni.

| Costruttore | Significato |
|---|---|
| `Thread()` | thread senza lavoro proprio e con un nome generato (`Thread-0`, `Thread-1`, …); utile solo se si ridefinisce `run` in una sottoclasse |
| `Thread(Runnable r)` | thread che eseguirà il `run` di `r` |
| `Thread(String name)` | come il primo, ma con il nome dato |
| `Thread(Runnable r, String name)` | il lavoro `r` e il nome insieme |

I nomi di default sono `Thread-0`, `Thread-1`, … numerati in ordine di creazione. Il nome serve solo a riconoscere il thread (nelle stampe, nel debug); non ne cambia il comportamento.

---

## 17.3 Creare un thread: due modi

Il vostro compito è sempre lo stesso: **mettere il codice del thread in un metodo `public void run()`** e far sì che un oggetto `Thread` lo usi. I due modi differiscono solo nel *come* si arriva a quel `run`.

### 17.3.1 Primo modo: estendere `Thread`

Si scrive una sottoclasse di `Thread`, si ridefinisce `run()` e si chiama `start()` su un'istanza della sottoclasse. L'ereditarietà è quella del [Capitolo 9](09-ereditarieta-e-polimorfismo.md): la sottoclasse eredita `start()` e ridefinisce `run()`.

#### Esempio — Un conto alla rovescia

```java
class ContoAllaRovescia extends Thread {
    private int da;

    public ContoAllaRovescia(int da) {
        this.da = da;                           // il costruttore PREPARA lo stato, non avvia nulla
    }

    public void run() {                         // public void run(): firma esatta
        for (int i = da; i >= 1; i--) {
            System.out.println(i);
        }
    }
}

public class PrimoModo {
    public static void main(String[] args) throws InterruptedException {
        ContoAllaRovescia c = new ContoAllaRovescia(3);  // 1. si crea l'oggetto
        c.start();                                       // 2. si avvia il thread
        c.join();                                        // 3. il main attende la fine
        System.out.println("Partenza");
    }
}
```

```text
3
2
1
Partenza
```

Il thread stampa `3`, `2`, `1` e finisce; il `main`, che ha aspettato con `join`, stampa `Partenza` **dopo**. Senza il `join` le righe `Partenza` e quelle del conto alla rovescia si potrebbero mescolare in ordine imprevedibile.

### 17.3.2 Secondo modo: realizzare `Runnable`

Si scrive una classe che **realizza l'interfaccia `Runnable`** ([Capitolo 10](10-classi-astratte-e-interfacce.md)), cioè dichiara `implements Runnable` e definisce il metodo `public void run()`. Poi si crea un oggetto `Thread` passandogli, nel costruttore, un'istanza di quella classe; infine si chiama `start()` **sul `Thread`**, non sull'oggetto `Runnable`.

```text
Runnable        ──────>  public interface Runnable { public abstract void run(); }

class Applicazione implements Runnable {
    public void run() { <corpo> }
}
...
Applicazione a = new Applicazione();  // l'oggetto che contiene il lavoro da eseguire
Thread th = new Thread(a);            // il thread, a cui si passa il lavoro
th.start();                           // lancia il thread: la JVM esegue a.run()
```

Qui gli oggetti sono **due**: l'oggetto `Runnable` (il *lavoro*, con i suoi campi) e l'oggetto `Thread` (il *motore* che lo esegue). È un dettaglio che si dimentica facilmente e che causa un errore tipico (paragrafo 17.6.1).

> [!NOTE]
> **Approfondimento esterno — L'interfaccia `Runnable`**
> La documentazione Java SE 17 dice che l'interfaccia `Runnable` deve essere realizzata da ogni classe le cui istanze siano destinate a essere eseguite da un thread. Dichiara un solo metodo, **`void run()`**, senza clausola `throws`: *"When an object implementing interface `Runnable` is used to create a thread, starting the thread causes the object's `run` method to be called in that separately executing thread."* Il contratto di `run` è che può compiere qualsiasi azione.
>
> *Fonte:* [Runnable (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Runnable.html)

#### Esempio — Un saluto con `Runnable` e con un nome

```java
class Saluta implements Runnable {
    private String chi;

    public Saluta(String chi) {
        this.chi = chi;
    }

    public void run() {
        System.out.println("Ciao da " + chi + " (" + Thread.currentThread().getName() + ")");
    }
}

public class SecondoModo {
    public static void main(String[] args) throws InterruptedException {
        Saluta lavoro = new Saluta("Anna");              // il lavoro
        Thread t = new Thread(lavoro, "Filo-1");         // il motore, con un nome
        t.start();
        t.join();
    }
}
```

```text
Ciao da Anna (Filo-1)
```

`Saluta` **non è** un `Thread`: non ha `start()`, e scrivere `lavoro.start()` non compilerebbe (lo vediamo tra gli errori tipici). Il `Thread` è un oggetto separato, creato con `new Thread(lavoro, "Filo-1")`. Il nome del thread è `Filo-1`, e infatti `Thread.currentThread().getName()` dentro `run` lo restituisce.

### 17.3.3 Quale dei due modi scegliere

Dagli esempi i due modi sembrano equivalenti, e anzi `Runnable` sembra complicare inutilmente le cose: perché rendere `Runnable` un oggetto, se basta una sottoclasse di `Thread`? La risposta è nell'**ereditarietà singola** di Java ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)): una classe può avere **una sola** superclasse.

> [!IMPORTANT]
> **Nota del docente — `Runnable` quando la classe ha già una superclasse**
> Se si vuole che una classe sia *contemporaneamente* un thread e una specializzazione di un'altra classe (per esempio una finestra, o una classe `Sensore` che già estende un'altra), non si può scrivere `extends Altra, Thread`: l'ereditarietà multipla in Java non esiste. Si **estende la classe base** e si **realizza `Runnable`**: così si personalizza la classe base e le si aggiunge la funzione di thread. Quindi, in modo semplificato, l'uso di `Runnable` al posto della derivazione da `Thread` **si rende necessario quando la classe che si vuole rendere eseguibile in un thread è già una classe derivata**.

In pratica:

| Situazione | Che cosa si usa |
|---|---|
| la classe non estende niente di particolare e vogliamo solo "un thread che fa questo" | `extends Thread` o `implements Runnable`, indifferente |
| la classe **deve** estendere un'altra classe | **`implements Runnable`** (obbligatorio) |
| lo stesso lavoro va affidato a più thread, o il lavoro va separato dal "motore" | `implements Runnable` |
| la traccia dice "implementa l'interfaccia `Runnable`" | `implements Runnable`, e si rispetta la lettera |

#### Esempio — Una classe che ha già una superclasse

```java
class Sensore {
    private String nome;

    public Sensore(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }
}

class SensoreAttivo extends Sensore implements Runnable {   // extends PRIMA di implements
    public SensoreAttivo(String nome) {
        super(nome);                                         // costruttore della superclasse
    }

    public void run() {
        System.out.println("Il sensore " + getNome() + " ha letto un valore");
    }
}

public class ConSuperclasse {
    public static void main(String[] args) throws InterruptedException {
        SensoreAttivo s = new SensoreAttivo("S1");
        Thread t = new Thread(s);
        t.start();
        t.join();
    }
}
```

```text
Il sensore S1 ha letto un valore
```

`SensoreAttivo` è un `Sensore` (eredita `getNome`) **e** un `Runnable` (definisce `run`). Per eseguirlo in un thread lo si passa a `new Thread(s)`. Se invece avessimo scritto `class SensoreAttivo extends Sensore, Thread`, il compilatore avrebbe rifiutato il programma. L'ordine delle clausole è fisso: prima `extends`, poi `implements`.

### 17.3.4 Un `Runnable` anonimo

Quando il lavoro è breve e serve in un solo punto, non occorre scrivere una classe con un nome: si può creare al volo una **classe anonima** ([Capitolo 11](11-classi-annidate.md)) che realizza `Runnable`.

```java
public class RunnableAnonimo {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(new Runnable() {         // classe anonima che realizza Runnable
            public void run() {
                System.out.println("lavoro eseguito da " + Thread.currentThread().getName());
            }
        }, "Filo-A");
        t.start();
        t.join();
    }
}
```

```text
lavoro eseguito da Filo-A
```

Le regole sono quelle viste nel Capitolo 11: dentro la classe anonima si possono usare le variabili locali del metodo che la contiene solo se sono `final` o *effettivamente* `final`, cioè mai riassegnate.

### 17.3.5 Più thread alla volta

Finora abbiamo avviato un solo thread per volta. Il vero vantaggio sta nell'avviarne **più di uno** e lasciarli procedere insieme. Riprendiamo un esempio classico, in cui un `main` crea e lancia due thread che stampano righe diverse; le pause con `sleep` (paragrafo 17.5.2) servono a farli alternare in modo visibile.

```java
class Coffee extends Thread {
    public void run() {
        for (int i = 1; i <= 3; i++) {
            System.out.println("I like coffee " + i);
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
            }
        }
    }
}

class Tea extends Thread {
    public void run() {
        try {
            Thread.sleep(100);                   // parte "sfasato" di 100 ms
        } catch (InterruptedException e) {
        }
        for (int i = 1; i <= 3; i++) {
            System.out.println("I like tea " + i);
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
            }
        }
    }
}

public class DueThread {
    public static void main(String[] args) throws InterruptedException {
        Coffee c = new Coffee();
        Tea t = new Tea();
        c.start();                                // i due thread partono quasi insieme...
        t.start();
        c.join();                                 // ...e il main li aspetta entrambi
        t.join();
        System.out.println("Fine");
    }
}
```

Una esecuzione tipica:

```text
I like coffee 1
I like tea 1
I like coffee 2
I like tea 2
I like coffee 3
I like tea 3
Fine
```

Le righe si **alternano**: i due thread procedono insieme. Il `Fine` esce sempre per ultimo, perché il `main` lo stampa solo dopo i due `join`. L'alternanza `coffee`/`tea`, invece, *dipende dai tempi*: con pause di 200 e 100 millisecondi è praticamente sempre quella, ma il programma non la garantisce, e senza le pause l'ordine tra le righe dei due thread sarebbe imprevedibile (paragrafo 17.1.4).

### 17.3.6 Chi avvia il thread

Nei programmi si incontrano due stili. Nel primo, **chi crea** il thread lo avvia (nel `main` di prima: `c.start()`). Nel secondo, **ogni oggetto lancia il proprio thread** dentro il costruttore: nel caso di un `Runnable` si crea il `Thread` passando `this` e lo si avvia subito; nel caso di una sottoclasse di `Thread`, il costruttore chiama `start()`.

```java
class Caffe implements Runnable {
    private Thread th;                       // il Runnable possiede il suo Thread

    public Caffe() {
        th = new Thread(this);               // 'this' è il Runnable
        th.start();                          // il thread parte DENTRO il costruttore
    }

    public void run() {
        System.out.println("I like coffee");
    }
}

public class AutoAvvio {
    public static void main(String[] args) throws InterruptedException {
        Caffe c = new Caffe();               // basta creare l'oggetto: il thread è già partito
        Thread.sleep(100);                   // diamo il tempo al thread di stampare
    }
}
```

```text
I like coffee
```

Funziona, e si incontra spesso. Ma ha due inconvenienti da conoscere, ed è per questo che la forma consigliata resta quella in cui **chi crea decide quando avviare**:

1. il thread parte **mentre il costruttore non è ancora finito**: `run()` può eseguire e leggere campi non ancora assegnati. Nel costruttore di `Caffe` sopra il thread parte prima che il costruttore finisca; se dopo `th.start()` ci fossero altre assegnazioni, `run` potrebbe vederle ancora ai valori iniziali (`null`, `0`). Peggio ancora se la classe ha una sottoclasse, il cui costruttore non è nemmeno cominciato;
2. se poi il chiamante, convinto che serva, scrive anche `new Thread(c).start()`, i thread che girano sullo **stesso oggetto** diventano due.

> [!WARNING]
> **Attenzione — Quando la traccia dice chi avvia**
> Se la traccia scrive che "il `main` crea e avvia i thread", l'avvio è del `main`: una classe che parte da sola nel costruttore non rispetta la struttura richiesta, anche se l'output è giusto. Il costruttore **prepara** l'oggetto; l'avvio spetta a chi lo usa.

---

## 17.4 Il ciclo di vita di un thread

### 17.4.1 Gli stati: la descrizione classica

Un thread, nella sua vita, passa per alcuni **stati**. La macchina virtuale distingue:

| Stato | Quando |
|---|---|
| **initial** (o *new*) | il thread è stato creato (`new Thread(...)`) ma `start()` non è ancora stato chiamato |
| **runnable** | dopo `start()`: il thread può essere eseguito in qualunque momento, ma lo scheduler non l'ha ancora scelto |
| **running** | il thread è **in esecuzione**: su un sistema a una CPU è uno solo, il *thread corrente*; in genere non è considerato uno stato a parte |
| **blocked** (o *non-runnable*) | il thread è vivo ma **non può essere eseguito**: aspetta un evento (la fine di un `sleep`, un'operazione di I/O, la fine di un altro thread, lo sblocco di un lock) |
| **dead** (o *terminated*) | `run()` è terminato: il thread è finito |

Lo schema delle transizioni:

```text
                     start()                         sleep(), wait(), join() ...
   new Thread() ───────────────> RUNNABLE ─────────────────────────────> BLOCKED
   (initial)                      │    ▲   <─────────────────────────────  │
                                  │    │     fine dell'attesa / notify()    │
                           yield()│    │                                    │
                                  ▼    │                                    │
                              (di nuovo in coda)                            │
                                  │                                         │
                                  │ run() termina                           │
                                  ▼                                         │
                                DEAD  <─────────────────────────────────────┘
```

In altre parole: da *initial* si passa a *runnable* con `start()`; da *runnable* a *blocked* quando il thread si mette ad aspettare; da *blocked* a *runnable* quando l'attesa finisce; da *runnable* a *dead* quando `run()` termina. *Dead* non ha uscite: da dead non si torna indietro.

### 17.4.2 Gli stati secondo la Javadoc: `Thread.State` e `getState`

La Javadoc distingue sei stati, raccolti nell'enumerazione `Thread.State` ([Capitolo 7](07-classi-e-oggetti.md), `enum`), e un metodo `getState()` che restituisce lo stato di un thread.

> [!NOTE]
> **Approfondimento esterno — `Thread.State` e `getState`**
> La documentazione Java SE 17 definisce `public static enum Thread.State` con sei costanti: **`NEW`** (thread non ancora avviato), **`RUNNABLE`** (thread eseguibile), **`BLOCKED`** (thread bloccato in attesa di un *monitor lock*), **`WAITING`** (thread in attesa), **`TIMED_WAITING`** (thread in attesa con un tempo massimo specificato), **`TERMINATED`** (thread terminato). Il metodo `public Thread.State getState()` *"returns the state of this thread. This method is designed for use in monitoring of the system state, not for synchronization control."*
>
> *Fonte:* [Thread.State (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.State.html)

La corrispondenza con la descrizione classica è:

| Descrizione classica | `Thread.State` |
|---|---|
| initial / new | `NEW` |
| runnable e running | `RUNNABLE` |
| blocked (attesa di un lock) | `BLOCKED` |
| blocked (`sleep` con tempo, `join` con tempo) | `TIMED_WAITING` |
| blocked (`wait()` o `join()` senza tempo) | `WAITING` |
| dead | `TERMINATED` |

Vediamo gli stati con un programma. Il thread dorme mezzo secondo; il `main` ne guarda lo stato in tre momenti.

```java
public class StatiDiUnThread {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(new Runnable() {
            public void run() {
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                }
            }
        });
        System.out.println(t.getState());     // creato, non avviato
        t.start();
        Thread.sleep(100);                    // diamo tempo al thread di mettersi a dormire
        System.out.println(t.getState());     // sta dormendo
        t.join();                             // attendiamo la fine
        System.out.println(t.getState());     // finito
        System.out.println(t.isAlive());
    }
}
```

```text
NEW
TIMED_WAITING
TERMINATED
false
```

Prima di `start()` lo stato è `NEW`. Dopo 100 ms il thread è dentro `sleep(500)`: è vivo ma sta aspettando per un tempo preciso, quindi `TIMED_WAITING`. Dopo il `join` il thread è finito: `TERMINATED`, e `isAlive()` (paragrafo 17.5.4) dà `false`.

### 17.4.3 Quando un thread termina

Un thread continua a eseguire fino a quando accade una di queste cose:

1. **`run()` ritorna**: finite le istruzioni, il thread cessa la sua attività e le risorse che aveva impegnato vengono rilasciate. È di gran lunga il caso più comune e quello da ricercare;
2. **un'eccezione esce da `run()`**: un'eccezione non gestita (non intercettata da un `catch` dentro `run`) interrompe il thread;
3. **viene chiamato `stop()`**: ma questo metodo è **deprecato** (lo vediamo qui sotto) e non va usato.

Vediamo il secondo caso, perché mostra una proprietà importante: **l'eccezione termina quel thread, non il programma né gli altri thread.**

```java
class Guasto extends Thread {
    public void run() {
        System.out.println("prima dell'errore");
        int[] v = new int[2];
        v[5] = 1;                                       // ArrayIndexOutOfBoundsException
        System.out.println("questa riga non viene mai stampata");
    }
}

public class EccezioneNelThread {
    public static void main(String[] args) throws InterruptedException {
        Guasto g = new Guasto();
        g.start();
        g.join();
        System.out.println("il main continua");
    }
}
```

Sulla console compare (la prima e l'ultima riga sono l'output normale; le righe centrali sono la segnalazione dell'eccezione, che Java stampa sullo standard error):

```text
prima dell'errore
Exception in thread "Thread-0" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 2
	at Guasto.run(EccezioneNelThread.java:5)
il main continua
```

L'eccezione esce da `run`, il thread `Thread-0` muore e Java stampa la segnalazione con il nome del thread; il `main` non ne è toccato e prosegue. È uno dei vantaggi della programmazione a thread: *thread indipendenti, un errore in uno non ferma gli altri*. Ma attenzione: l'eccezione **non arriva al `main`**, che quindi non potrebbe catturarla con un `try`/`catch` attorno a `g.start()`. Un `catch` che serve va scritto **dentro `run`**.

> [!NOTE]
> **Approfondimento esterno — `stop`, `suspend` e `resume` sono deprecati**
> La documentazione Java SE 17 segna `stop()` come `@Deprecated(since="1.2")` e lo definisce *"inherently unsafe"* (intrinsecamente non sicuro): il thread viene forzato a fermarsi a metà di ciò che stava facendo, senza la possibilità di fare pulizia. I metodi `suspend()` e `resume()` sono `@Deprecated(since="1.2", forRemoval=true)`: la Javadoc dice che sono *"inherently deadlock-prone"* (soggetti a stallo) e che *"this API element is subject to removal in a future version"*. Non si usano.
>
> *Fonte:* [Thread (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html)

### 17.4.4 Fermare un thread: la variabile sentinella

Spesso un thread deve vivere a lungo e fare lo stesso lavoro ripetutamente: un orologio che aggiorna l'ora ogni secondo, un controllo periodico, e così via. Per fermarlo **senza `stop()`** si usa una **variabile sentinella** (*flag*): un campo `boolean` che il thread controlla a ogni giro del ciclo. Quando qualcun altro lo cambia, il thread esce dal ciclo, `run` termina e il thread finisce in modo ordinato, dopo aver magari fatto pulizia.

```java
class Ciclo implements Runnable {
    private volatile boolean attivo = true;          // la sentinella: volatile!

    public void ferma() {                            // chiamato da un altro thread
        attivo = false;
    }

    public void run() {
        System.out.println("partito");
        while (attivo) {                             // controlla la sentinella a ogni giro
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
            }
        }
        System.out.println("fermato");
    }
}

public class FermareUnThread {
    public static void main(String[] args) throws InterruptedException {
        Ciclo c = new Ciclo();
        Thread t = new Thread(c);
        t.start();
        Thread.sleep(100);                           // il thread lavora per un po'
        c.ferma();                                   // il main abbassa la sentinella
        t.join();                                    // e aspetta che il thread esca
        System.out.println("fine");
    }
}
```

```text
partito
fermato
fine
```

Il campo `attivo` è dichiarato **`volatile`**, e la parola è essenziale. Il punto è che il thread scrive-e-legge lo stesso dato da due thread diversi: il `main` lo scrive (`ferma()`), il thread di `Ciclo` lo legge (`while (attivo)`). Se la variabile **non** è `volatile`, la macchina virtuale è libera di tenere nel thread una copia della variabile e di non accorgersi mai che è cambiata: il thread **potrebbe non fermarsi mai**.

> [!NOTE]
> **Approfondimento esterno — `volatile` e la visibilità tra thread**
> Il riepilogo del package `java.util.concurrent` di Java SE 17, nella sezione *Memory Consistency Properties*, dice che *"the `synchronized` and `volatile` constructs, as well as the `Thread.start()` and `Thread.join()` methods, can form happens-before relationships"*, e precisa: *"A write to a `volatile` field happens-before every subsequent read of that same field."* Scritture e letture di campi `volatile` hanno gli stessi effetti sulla consistenza della memoria dell'entrata e dell'uscita da un monitor, ma **non** comportano mutua esclusione. In parole semplici: se un thread scrive un campo `volatile`, ogni lettura successiva di quel campo, da qualunque thread, **vede il nuovo valore**.
>
> *Fonte:* [java.util.concurrent (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/package-summary.html)

La regola da ricordare: **una sentinella condivisa tra thread si dichiara `volatile`**. `volatile` garantisce la **visibilità** della modifica, ma non rende atomiche operazioni composte come `contatore++` (paragrafo 17.6.5).

---

## 17.5 I metodi che controllano un thread

### 17.5.1 Identificare un thread: `currentThread`, `getName`, `setName`

Ogni thread ha un **nome**. Il metodo statico `Thread.currentThread()` restituisce il **riferimento al thread che sta eseguendo il codice in questo momento**, e con `getName()` se ne legge il nome. Funziona dentro qualunque metodo, anche di classi che non c'entrano nulla con i thread.

```java
public class Nomi {
    public static void main(String[] args) {
        Thread io = Thread.currentThread();         // il thread che esegue il main
        System.out.println(io.getName());           // main
        io.setName("principale");                   // si può rinominare
        System.out.println(io.getName());           // principale

        Thread a = new Thread();                    // nome generato
        Thread b = new Thread();
        Thread c = new Thread("mio");               // nome scelto
        System.out.println(a.getName() + " " + b.getName() + " " + c.getName());
    }
}
```

```text
main
principale
Thread-0 Thread-1 mio
```

Il thread del `main` si chiama `main`; i thread senza nome ricevono `Thread-0`, `Thread-1`, …, in ordine di creazione. Il nome si può dare già nel costruttore o cambiare dopo con `setName(String)`.

> [!WARNING]
> **Attenzione — Non si stampa l'oggetto `Thread`**
> `System.out.println(t)` stampa il `toString` del thread, che **cambia da una versione di Java all'altra**: in Java 17 è `Thread[main,5,main]` (nome, priorità, gruppo), nelle versioni successive è `Thread[#1,main,5,main]` con un identificatore in più. Per avere un output stabile si stampa `t.getName()`.

### 17.5.2 Una pausa: `sleep`

`sleep` sospende il **thread corrente** per un tempo dato in millisecondi: il thread passa allo stato *blocked* (`TIMED_WAITING`), lo scheduler esegue un altro thread, e allo scadere del tempo il thread torna *runnable*. È un metodo **statico** della classe `Thread` e agisce sempre sul thread **che lo chiama**: si può usare da qualunque classe, anche senza avere sotto mano un oggetto di tipo `Thread`.

```java
public class ContoSleep {
    public static void main(String[] args) {
        for (int n = 3; n >= 1; n--) {
            System.out.println(n);
            try {
                Thread.sleep(200);                  // pausa di 200 ms
            } catch (InterruptedException e) {      // obbligatorio: sleep dichiara questa eccezione
                System.out.println("interrotto");
            }
        }
        System.out.println("Via!");
    }
}
```

```text
3
2
1
Via!
```

Il programma stampa i numeri a intervalli di 200 millisecondi.

> [!NOTE]
> **Approfondimento esterno — `Thread.sleep` e `InterruptedException`**
> La documentazione Java SE 17 dichiara `public static void sleep(long millis) throws InterruptedException` (e `sleep(long millis, int nanos)`, con `nanos` tra 0 e 999999): *"causes the currently executing thread to sleep (temporarily cease execution) for the specified number of milliseconds, subject to the precision and accuracy of system timers and schedulers. The thread does not lose ownership of any monitors."* Se `millis` è negativo lancia `IllegalArgumentException`. L'eccezione `InterruptedException` ha come superclasse `Exception` (non `RuntimeException`): è **controllata**, e la sua descrizione è *"Thrown when a thread is waiting, sleeping, or otherwise occupied, and the thread is interrupted, either before or during the activity."*
>
> *Fonte:* [Thread#sleep (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html#sleep(long)) e [InterruptedException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/InterruptedException.html)

Per `sleep` valgono due fatti da ricordare, ciascuno con un'importanza propria.

**Primo: `sleep` non rilascia i lock.** Un thread che dorme dentro un blocco o un metodo `synchronized` ([Capitolo 18](18-sincronizzazione.md)) continua a **tenere il lock**: gli altri thread che lo vogliono restano fermi. Per questo una sospensione con `sleep` può essere pericolosa nei programmi con gestione sincronizzata dei dati.

**Secondo: l'`InterruptedException` va gestita.** Poiché è un'eccezione **controllata** ([Capitolo 13](13-eccezioni.md)), il compilatore pretende che chi chiama `sleep` (e, vedremo, `join`) o la **catturi** o la **dichiari** con `throws`. Ci sono due modi, entrambi corretti:

```java
// 1. si cattura dove serve (tipico dentro run(), che non può dichiarare eccezioni)
try {
    Thread.sleep(500);
} catch (InterruptedException e) {
    System.out.println("interrotto");
}

// 2. si dichiara nel metodo (tipico per il main)
public static void main(String[] args) throws InterruptedException {
    Thread.sleep(500);
}
```

Dentro `run()` si deve **catturare**: il metodo `run()` di `Runnable` e di `Thread` non ha clausola `throws`, e un metodo che ridefinisce un altro non può dichiarare eccezioni controllate in più ([Capitolo 13](13-eccezioni.md)). Nel `main` si può scegliere liberamente.

L'eccezione viene lanciata quando un altro thread *interrompe* il thread che sta dormendo (o aspettando) chiamando il metodo `interrupt()` su di esso. Negli esempi di questo capitolo nessuno lo fa mai, quindi il `catch` non viene mai eseguito: serve solo a far compilare il programma. Quando non si ha nulla da fare nel `catch`, lo si scrive comunque, con il blocco vuoto o con una stampa.

### 17.5.3 Cedere il turno: `yield`

`yield()` è un metodo statico, come `sleep`, che dice allo scheduler: "per ora posso cedere il processore a un altro thread". Il thread **non** diventa *blocked*: rimane *runnable*, ed è spostato in fondo alla coda dei thread della sua stessa priorità. Se nessun altro è in attesa, il thread continua senza un inutile cambio di contesto. Si usa per favorire la cooperazione tra thread quando uno impegnerebbe il processore a lungo.

```java
class Patata implements Runnable {
    public void run() {
        for (int i = 0; i < 3; i++) {
            System.out.println(Thread.currentThread().getName());
            Thread.yield();                                // cedo il turno
        }
    }
}

public class ConYield {
    public static void main(String[] args) throws InterruptedException {
        Patata lavoro = new Patata();                      // UN SOLO Runnable...
        Thread a = new Thread(lavoro, "una patata");       // ...condiviso da DUE thread
        Thread b = new Thread(lavoro, "due patate");
        a.start();
        b.start();
        a.join();
        b.join();
    }
}
```

Una possibile esecuzione:

```text
una patata
due patate
una patata
due patate
una patata
due patate
```

L'esempio mostra due cose. Una: **lo stesso oggetto `Runnable` può essere affidato a più thread**, e `Thread.currentThread().getName()` permette di distinguere chi sta eseguendo. L'altra, importante: **l'ordine delle righe non è garantito**.

> [!NOTE]
> **Approfondimento esterno — `Thread.yield`**
> La documentazione Java SE 17 dice che `yield` è *"a hint to the scheduler that the current thread is willing to yield its current use of a processor. The scheduler is free to ignore this hint."* Quindi è un **suggerimento**, che lo scheduler può ignorare: un programma non deve fondare la propria correttezza sul fatto che `yield` produca una certa alternanza.
>
> *Fonte:* [Thread#yield (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html#yield())

### 17.5.4 Attendere un altro thread: `join` e `isAlive`

`join()` fa aspettare il thread che lo chiama **finché il thread su cui è invocato non termina**. Il nome viene dall'idea del thread chiamante che attende che l'altro si "riunisca" a lui. È il metodo più importante da saper usare.

- `t.join()`: aspetta **senza limite** la morte di `t`;
- `t.join(long millis)`: aspetta **al massimo** `millis` millisecondi, poi ritorna comunque (con `0` significa "per sempre");
- `t.isAlive()`: restituisce `true` se `t` è **vivo**, cioè è stato avviato e non è ancora morto; `false` altrimenti.

Sia `join()` sia `join(long)` dichiarano `InterruptedException`, che va gestita come per `sleep`.

> [!NOTE]
> **Approfondimento esterno — `join` e `isAlive`**
> La documentazione Java SE 17 dichiara `public final void join() throws InterruptedException` (*"waits for this thread to die"*, equivalente a `join(0)`), `public final void join(long millis) throws InterruptedException` (*"waits at most `millis` milliseconds for this thread to die. A timeout of `0` means to wait forever"*) e `public final boolean isAlive()` (*"tests if this thread is alive. A thread is alive if it has been started and has not yet died"*). La Javadoc consiglia di non usare `wait`, `notify` o `notifyAll` su oggetti `Thread`.
>
> *Fonte:* [Thread#join (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html#join())

Un programma che mostra `isAlive` e `join` con tempo massimo:

```java
public class AttesaConJoin {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(new Runnable() {
            public void run() {
                try {
                    Thread.sleep(300);
                } catch (InterruptedException e) {
                }
            }
        });
        System.out.println("prima di start: " + t.isAlive());
        t.start();
        System.out.println("dopo start: " + t.isAlive());
        t.join(50);                                          // attesa massima 50 ms
        System.out.println("dopo join(50): " + t.isAlive()); // il thread dorme ancora
        t.join();                                            // attesa senza limite
        System.out.println("dopo join(): " + t.isAlive());
    }
}
```

```text
prima di start: false
dopo start: true
dopo join(50): true
dopo join(): false
```

Prima di `start` il thread **non è vivo**: non è ancora partito. Dopo `start` è vivo. `join(50)` ritorna dopo al massimo 50 ms, ma il thread dorme ancora 300 ms: quindi è ancora vivo. `join()` senza limite ritorna solo quando il thread è finito, e a quel punto `isAlive()` è `false`.

A che serve `join` nella pratica? A due scopi, che il compito d'esame richiede spesso:

1. **sincronizzare la stampa**: il `main` stampa una riga (per esempio un risultato) solo dopo che i thread che la producono hanno finito;
2. **leggere un risultato calcolato da un altro thread**: si aspetta che il thread finisca, poi si legge il dato (paragrafo 17.6.1).

Con `sleep` l'attesa ha una durata prefissata; con `join` dura quanto serve, e potrebbe anche non finire mai se l'altro thread non termina: per questo esiste la forma con tempo massimo.

### 17.5.5 Le priorità

Ogni thread ha una **priorità**, un numero intero che lo scheduler usa come indicazione di quando farlo eseguire. Si legge con `getPriority()` e si cambia con `setPriority(int)`. Le costanti della classe `Thread` sono `MIN_PRIORITY` (1), `NORM_PRIORITY` (5, il valore di partenza) e `MAX_PRIORITY` (10); `setPriority` accetta solo valori da `MIN_PRIORITY` a `MAX_PRIORITY`.

La macchina virtuale usa uno scheduling preemptive basato sulla priorità: quando un thread di priorità più alta diventa runnable, può sottrarre il processore a quello in esecuzione; **a parità di priorità** si usa il round-robin (paragrafo 17.1.1).

```java
public class Priorita {
    public static void main(String[] args) {
        Thread t = new Thread();
        System.out.println(t.getPriority());               // 5, il valore normale
        t.setPriority(Thread.MAX_PRIORITY);
        System.out.println(t.getPriority());               // 10
        try {
            t.setPriority(11);                             // fuori dall'intervallo 1..10
        } catch (IllegalArgumentException e) {
            System.out.println("priorità non valida");
        }
    }
}
```

```text
5
10
priorità non valida
```

> [!NOTE]
> **Approfondimento esterno — `setPriority` e le costanti di priorità**
> La documentazione Java SE 17 dichiara `public final void setPriority(int newPriority)` (*"changes the priority of this thread"*) e `public final int getPriority()`; `setPriority` lancia `IllegalArgumentException` *"if the priority is not in the range `MIN_PRIORITY` to `MAX_PRIORITY`"*. Le costanti `MIN_PRIORITY`, `NORM_PRIORITY` e `MAX_PRIORITY` sono `public static final int` che indicano la priorità minima, quella assegnata per default e la massima. Si noti che `setPriority` è `final` e restituisce `void`.
>
> *Fonte:* [Thread#setPriority (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html#setPriority(int))

> [!WARNING]
> **Attenzione — La priorità è un suggerimento**
> Quanto tempo di processore riceve davvero un thread dipende anche dal sistema operativo e da altri fattori, non solo dalla priorità. Un programma non deve basare la propria **correttezza** sulle priorità: per imporre un ordine si usano `join` e, come vedremo, i meccanismi di sincronizzazione.

### 17.5.6 Il quadro dei metodi

| Metodo | Statico? | Che cosa fa |
|---|---|---|
| `start()` | no | lancia il thread: la JVM esegue `run()` in un nuovo flusso. Una volta sola |
| `run()` | no | il codice del thread. **Chiamarlo a mano non crea un thread** |
| `sleep(long ms)` | **sì** | sospende il **thread corrente** per `ms` millisecondi; non rilascia i lock; `throws InterruptedException` |
| `yield()` | **sì** | il thread corrente suggerisce allo scheduler di passare ad altri della stessa priorità |
| `currentThread()` | **sì** | restituisce il thread che sta eseguendo |
| `join()` / `join(long ms)` | no | attende la morte del thread (al massimo `ms` ms); `throws InterruptedException` |
| `isAlive()` | no | `true` se il thread è avviato e non ancora morto |
| `getName()` / `setName(String)` | no | nome del thread |
| `getPriority()` / `setPriority(int)` | no | priorità (1-10, normale 5) |
| `getState()` | no | stato (`Thread.State`) |
| `stop()`, `suspend()`, `resume()` | no | **deprecati**: non si usano |

Il fatto che `sleep`, `yield` e `currentThread` siano **statici** conta: riguardano *sempre il thread che sta eseguendo*, mai un altro. Scrivere `t.sleep(100)` su un thread `t` compila (lo vediamo tra gli errori tipici), ma fa dormire **chi scrive la riga**, non `t`.

---

## 17.6 Più thread che lavorano insieme

### 17.6.1 Un thread, un lavoro, un risultato

Spesso si affida a un thread un lavoro che produce un **risultato**: una somma, un conteggio. Un thread non "restituisce" nulla: `run()` è `void`. Il risultato va **depositato in un campo** dell'oggetto che contiene il lavoro, e letto da chi lo vuole **dopo che il thread è finito**. È il motivo per cui ha senso separare il lavoro (il `Runnable`) dal motore (il `Thread`): il **risultato sta nel `Runnable`**.

```java
class Fattoriale implements Runnable {
    private int n;
    private long risultato;                 // il risultato verrà depositato qui

    public Fattoriale(int n) {
        this.n = n;
    }

    public void run() {
        long f = 1;
        for (int i = 2; i <= n; i++) {
            f *= i;
        }
        risultato = f;                      // run() è void: il dato si lascia in un campo
    }

    public long getRisultato() {
        return risultato;
    }
}

public class UnRisultato {
    public static void main(String[] args) throws InterruptedException {
        Fattoriale lavoro = new Fattoriale(10);
        Thread t = new Thread(lavoro);
        t.start();
        t.join();                                         // PRIMA si aspetta...
        System.out.println(lavoro.getRisultato());        // ...POI si legge, dal Runnable
    }
}
```

```text
3628800
```

I punti da ricordare sono due, ed entrambi si possono sbagliare in un compito:

1. si legge il risultato **dopo `join()`**: prima, il thread potrebbe non averlo ancora calcolato e si leggerebbe `0`;
2. il metodo `getRisultato()` è un metodo di **`Fattoriale`**, non di `Thread`: si chiama su `lavoro`, non su `t`. Scrivere `t.getRisultato()` non compila, perché `Thread` non ha quel metodo. Il programma deve **tenere in mano entrambi gli oggetti**, il `Runnable` e il `Thread`.

Quando i thread sono più d'uno servono **due array paralleli**: uno di `Runnable` (da cui leggere i risultati) e uno di `Thread` (su cui fare `start` e `join`), con lo stesso indice `k` per lavoro e thread corrispondente.

### 17.6.2 Dividere un array tra `n` thread

Il problema tipico: sommare gli elementi di un array lungo con `n` thread, ciascuno su una **porzione** diversa. Ogni thread riceve nel costruttore l'array e gli estremi della sua porzione `[da, a)` (da incluso, a escluso), calcola la somma parziale e la lascia in un campo.

La porzione di ciascun thread si calcola così: con `passo = lunghezza / n`, il thread `k` lavora da `k * passo` a `(k + 1) * passo`; **l'ultimo thread prende il resto**, fino alla fine dell'array, perché `lunghezza` può non essere divisibile per `n`.

```java
class SommaParziale implements Runnable {
    private int[] dati;
    private int da;                          // incluso
    private int a;                           // escluso
    private long somma;

    public SommaParziale(int[] dati, int da, int a) {
        this.dati = dati;
        this.da = da;
        this.a = a;
    }

    public void run() {
        for (int i = da; i < a; i++) {
            somma += dati[i];
        }
    }

    public long getSomma() {
        return somma;
    }
}

public class SommaConThread {
    public static void main(String[] args) throws InterruptedException {
        int[] dati = new int[10];
        for (int i = 0; i < dati.length; i++) {
            dati[i] = i + 1;                                  // 1, 2, ..., 10
        }

        int n = 3;                                            // numero di thread
        int passo = dati.length / n;                          // 10 / 3 = 3
        SommaParziale[] lavori = new SommaParziale[n];        // i Runnable
        Thread[] thread = new Thread[n];                      // i Thread

        for (int k = 0; k < n; k++) {                         // PRIMO CICLO: crea e avvia tutti
            int da = k * passo;
            int a = (k == n - 1) ? dati.length : da + passo;  // l'ultimo prende il resto
            lavori[k] = new SommaParziale(dati, da, a);
            thread[k] = new Thread(lavori[k]);
            thread[k].start();
        }

        long totale = 0;
        for (int k = 0; k < n; k++) {                         // SECONDO CICLO: attende e raccoglie
            thread[k].join();
            totale += lavori[k].getSomma();
        }
        System.out.println("Totale: " + totale);
    }
}
```

```text
Totale: 55
```

Seguiamo l'esecuzione. Con 10 elementi e 3 thread, `passo = 3`: il thread 0 somma gli indici 0-2 (1+2+3 = 6), il thread 1 gli indici 3-5 (4+5+6 = 15), il thread 2 gli indici 6-9 (7+8+9+10 = 34, l'ultimo prende il resto). Il totale è 6 + 15 + 34 = 55.

Il punto da imparare è la **struttura a due cicli**:

1. **il primo ciclo crea e avvia** tutti i thread, uno dopo l'altro: appena un thread parte, il ciclo continua a creare il successivo, e tutti lavorano insieme;
2. **il secondo ciclo attende e raccoglie**: per ogni thread fa `join` e poi legge il risultato.

> [!CAUTION]
> **Errore tipico — `start` e `join` nello stesso ciclo**
> ```java
> // ERRORE logico: i thread non lavorano insieme
> for (int k = 0; k < n; k++) {
>     thread[k] = new Thread(lavori[k]);
>     thread[k].start();
>     thread[k].join();        // il main aspetta qui, prima di avviare il successivo
> }
> ```
> Il programma compila e dà il risultato giusto, ma **ogni thread parte solo dopo che il precedente è finito**: il lavoro è eseguito uno alla volta, esattamente come in un programma senza thread, e si perde ogni vantaggio. La forma corretta è la struttura a due cicli: prima *tutti* gli `start`, poi *tutti* i `join`.

### 17.6.3 Una matrice: un thread per riga

Se i dati sono in una matrice ([Capitolo 5](05-array-e-matrici.md)), la divisione più naturale assegna **una riga a ogni thread**. Il lavoro riceve la riga (un `int[]`) e depositano la somma in un campo; il resto del programma ha la stessa forma a due cicli.

```java
class SommaRiga implements Runnable {
    private int[] riga;
    private int somma;

    public SommaRiga(int[] riga) {
        this.riga = riga;
    }

    public void run() {
        for (int x : riga) {
            somma += x;
        }
    }

    public int getSomma() {
        return somma;
    }
}

public class SommaMatrice {
    public static void main(String[] args) throws InterruptedException {
        int[][] m = { {1, 2, 3}, {4, 5}, {6, 7, 8, 9} };      // righe di lunghezza diversa

        SommaRiga[] lavori = new SommaRiga[m.length];
        Thread[] thread = new Thread[m.length];
        for (int r = 0; r < m.length; r++) {                  // avvia un thread per riga
            lavori[r] = new SommaRiga(m[r]);                  // m[r] è un int[]
            thread[r] = new Thread(lavori[r]);
            thread[r].start();
        }
        int totale = 0;
        for (int r = 0; r < m.length; r++) {                  // attende e raccoglie
            thread[r].join();
            System.out.println("Riga " + r + ": " + lavori[r].getSomma());
            totale += lavori[r].getSomma();
        }
        System.out.println("Totale: " + totale);
    }
}
```

```text
Riga 0: 6
Riga 1: 9
Riga 2: 30
Totale: 45
```

Il secondo ciclo stampa le somme **in ordine di riga** (0, 1, 2), perché le legge in quell'ordine dopo aver atteso ciascun thread: l'output è sempre lo stesso, pur essendo i thread liberi di finire in un ordine qualsiasi.

### 17.6.4 Perché leggere il risultato dopo `join` è sicuro

C'è una domanda legittima: i campi `somma` non sono `volatile` né protetti da un lock, e sono scritti da un thread e letti dal `main`. Come si è certi che il `main` veda il valore giusto? La risposta è `join` stesso: tra i meccanismi che formano le relazioni *happens-before* la Javadoc cita proprio `Thread.start()` e `Thread.join()`.

> [!NOTE]
> **Approfondimento esterno — `start` e `join` e la visibilità dei dati**
> Il riepilogo del package `java.util.concurrent` di Java SE 17 dice, nella sezione *Memory Consistency Properties*: *"A call to `start` on a thread happens-before any action in the started thread."* e *"All actions in a thread happen-before any other thread successfully returns from a `join` on that thread."* In termini pratici: quello che un thread ha scritto prima di terminare è **visibile** al thread che ha fatto `join` su di lui, quando `join` ritorna; e quello che il `main` ha scritto prima di `start` è visibile al thread avviato.
>
> *Fonte:* [java.util.concurrent (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/package-summary.html)

Quindi il modello a due cicli è anche **corretto**: i dati passati nel costruttore (visibili al thread, per l'`start`) e i risultati letti dopo `join` (visibili al `main`) non richiedono altro. Vale solo **dopo** `join`: leggere `getSomma()` *prima*, mentre il thread lavora ancora, dà un valore parziale o `0`.

### 17.6.5 Quando i thread toccano gli stessi dati

Nei due esempi precedenti i thread non entrano mai in conflitto: ognuno **scrive solo nel proprio campo** e **legge soltanto la propria porzione** dell'array. Questa è la forma più semplice e più sicura di lavoro in parallelo, e quando il problema lo permette è quella da preferire.

La situazione cambia quando più thread **modificano lo stesso dato**. Vediamo cosa succede con il caso più semplice: due thread incrementano 100000 volte lo stesso contatore, condiviso perché sono due thread sullo stesso oggetto.

```java
class Incrementa implements Runnable {
    int contatore = 0;                       // UN SOLO campo, condiviso dai due thread

    public void run() {
        for (int i = 0; i < 100000; i++) {
            contatore++;                     // non è un'operazione atomica
        }
    }
}

public class ContatoreSbagliato {
    public static void main(String[] args) throws InterruptedException {
        Incrementa lavoro = new Incrementa();         // un solo oggetto...
        Thread t1 = new Thread(lavoro);               // ...affidato a due thread
        Thread t2 = new Thread(lavoro);
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(lavoro.contatore);
    }
}
```

Il risultato "atteso" è `200000`. Il risultato effettivo è un valore **diverso a ogni esecuzione**, quasi sempre molto minore: per esempio `114966`, poi `128519`, poi `106815`.

Il motivo: `contatore++` non è un'unica operazione ma tre passi (leggi il valore, aggiungi uno, riscrivi il risultato). Se due thread leggono lo stesso valore prima che uno dei due lo riscriva, uno degli incrementi va perso. Quando il risultato dipende da *come si alternano* i thread, si parla di **race condition** (*situazione di competizione*). Si risolve con la **mutua esclusione**: far eseguire l'operazione a un thread alla volta, con `synchronized`. È l'argomento del [Capitolo 18](18-sincronizzazione.md). Qui basta ricordare che **`volatile` non basta** a correggere questo programma: `volatile` rende *visibile* il valore, non rende *atomica* l'operazione composta `contatore++`.

---

## 17.7 Dalla traccia al codice

Le tracce d'esame sui thread usano formule ricorrenti. Ognuna ha una traduzione precisa nel codice; scegliere quella giusta è metà dell'esercizio.

| Frase della traccia | Che cosa si scrive |
|---|---|
| "una classe che **implementa l'interfaccia `Runnable`**" | `class X implements Runnable` con `public void run()`; **non** `extends Thread` |
| "una sottoclasse **di `Thread`**" | `class X extends Thread` con `public void run()` |
| "una sottoclasse di `Persona` che implementa `Runnable`" | `extends` e poi `implements`; i costruttori chiamano `super(...)` ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)) |
| "il metodo `run` deve fare ..." | si scrive il corpo in `public void run()`; nessun `throws` |
| "il `main` **crea e avvia** i thread" | `new Thread(...)` e `start()` nel `main`; il costruttore non avvia nulla |
| "aspetta che i thread terminino", "prima di stampare il totale" | `join()` su ciascun thread, dentro `try`/`catch (InterruptedException)` o con `throws` nel `main` |
| "**`n` thread**, ciascuno su una porzione dell'array" | due array (lavori e thread), ciclo di `start`, ciclo di `join`, ultimo thread con il resto |
| "ogni thread calcola un valore parziale, il `main` lo somma" | il risultato va in un campo del `Runnable`; il `main` lo legge **dopo** `join`, dal `Runnable` |
| "il thread si ferma quando ..." | variabile sentinella `volatile boolean`, controllata nel ciclo di `run` |
| "attende N millisecondi" | `Thread.sleep(N)` dentro `try`/`catch (InterruptedException)` |
| "l'output deve essere sempre lo stesso" | si impone l'ordine con `join` (o con una sola stampa nel `main`, a thread finiti) |

Il filo conduttore è che i thread dei compiti sono strumenti per **dividere un lavoro** o per **mostrare un meccanismo**, e il risultato che si stampa deve essere *deterministico*. Ogni volta che state per stampare un valore calcolato da un altro thread, chiedetevi se ci sarà un `join` prima.

---

## Come esce all'esame

### EXAM1 — Esercizio 3 (13 punti)

- **Cosa chiedeva la traccia.** Data una classe `Persona`, già fornita, con un costruttore `(String nome, String cognome)`: (1) definire una sottoclasse `Studente` che implementa l'interfaccia `Runnable`; (2) definire in `Studente` due costruttori in overload, il primo con parametri `nome`, `cognome`, `matricola` (`int`), il secondo con `matricola` (`int`) e `cds` (`String`); (3) ridefinire il metodo `run()`, in modo che elevi la `matricola` al quadrato e ne sovrascriva il valore; (4) rispettare l'*information hiding*: tutte le variabili d'istanza `private` e relativi metodi `get` e `set`.
- **Concetti del capitolo necessari.** Realizzare `Runnable` con `implements` e definire `public void run()` (paragrafi 17.3.2 e 17.3.3); la sottoclasse di una classe già esistente (`extends` prima, `implements` poi, paragrafo 17.3.3). Il resto dell'esercizio sta nei capitoli precedenti: il secondo costruttore non ha `nome` e `cognome` e la superclasse non ha un costruttore senza parametri ([Capitolo 9](09-ereditarieta-e-polimorfismo.md), paragrafo 9.3.4), campi privati e metodi `get`/`set` ([Capitolo 7](07-classi-e-oggetti.md)).
- **Vincoli letterali imposti.** `Studente` deve **implementare** `Runnable` (non estendere `Thread`); due costruttori con quei parametri **in quell'ordine**; `run()` che **sovrascrive** il valore della `matricola` con il suo quadrato; tutti i campi `private` con `get` e `set`.

La traccia non chiede di avviare il thread: l'esercizio verifica che si sappia **realizzare `Runnable`** e scrivere correttamente `run`.

### EXAM2 — Esercizio 3 (13 punti)

La traccia fornisce già le classi `Produttore` e `Consumatore`, che usano un `Buffer` condiviso da realizzare; è un esercizio di **sincronizzazione** (`synchronized`, `wait`, `notify`), trattato nel [Capitolo 18](18-sincronizzazione.md). Dal punto di vista di questo capitolo, richiede solo di capire che `Produttore` e `Consumatore` sono due thread che condividono un oggetto.

---

## Scheletri da esame

### Scheletro 1 — Un thread con `Runnable`, avviato dal `main`

*Quando si usa:* ogni volta che la traccia dice "implementa `Runnable`" e poi chiede di eseguire il lavoro in un thread. È il minimo da saper scrivere a occhi chiusi.

```java
class Lavoro implements Runnable {                  // implements Runnable
    private String nome;

    public Lavoro(String nome) {
        this.nome = nome;
    }

    public void run() {                             // public void run(): firma esatta, senza throws
        System.out.println("Eseguo " + nome);
    }
}

public class Principale {
    public static void main(String[] args) throws InterruptedException {
        Lavoro l = new Lavoro("A");                 // 1. il lavoro
        Thread t = new Thread(l);                   // 2. il thread, con il lavoro
        t.start();                                  // 3. start(), non run()
        t.join();                                   // 4. attende la fine
    }
}
```

Import: nessuno (`Thread` e `Runnable` sono in `java.lang`). Eccezione: `join` dichiara `InterruptedException` (controllata): qui il `main` la dichiara con `throws`; in alternativa un `try`/`catch`.

### Scheletro 2 — Attendere i thread con `join` e gestire `InterruptedException`

*Quando si usa:* quando il `main` deve aspettare uno o più thread prima di stampare o di usare un risultato.

```java
public class Attesa {
    public static void main(String[] args) {
        Thread t = new Thread(new Runnable() {
            public void run() {
                System.out.println("lavoro");
            }
        });
        t.start();
        try {
            t.join();                               // join dentro try/catch
        } catch (InterruptedException e) {
            System.out.println("interrotto");
        }
        System.out.println("dopo il thread");       // esce sempre dopo "lavoro"
    }
}
```

Eccezioni: `InterruptedException` va catturata (come qui) **oppure** dichiarata con `throws` nel metodo che contiene `join`. Con più thread i `join` stanno in un **secondo ciclo**, dopo il ciclo degli `start`.

### Scheletro 3 — Partizione di un array tra `n` thread

*Quando si usa:* "dividere un array tra `n` thread e combinare i risultati parziali". Il lavoro è contare gli elementi pari, ma lo schema è lo stesso per qualunque calcolo su una porzione.

```java
class ConteggioPari implements Runnable {
    private int[] dati;
    private int da, a;                              // porzione [da, a)
    private int pari;                               // risultato parziale

    public ConteggioPari(int[] dati, int da, int a) {
        this.dati = dati;
        this.da = da;
        this.a = a;
    }

    public void run() {
        for (int i = da; i < a; i++) {
            if (dati[i] % 2 == 0) pari++;
        }
    }

    public int getPari() {                          // il risultato si legge dal Runnable
        return pari;
    }
}

public class Partizione {
    public static void main(String[] args) throws InterruptedException {
        int[] dati = {4, 7, 10, 3, 8, 2, 9, 6};
        int n = 3;
        int passo = dati.length / n;
        ConteggioPari[] lavori = new ConteggioPari[n];   // array dei Runnable
        Thread[] thread = new Thread[n];                   // array dei Thread

        for (int k = 0; k < n; k++) {                      // ciclo 1: crea e avvia
            int da = k * passo;
            int a = (k == n - 1) ? dati.length : da + passo;   // l'ultimo prende il resto
            lavori[k] = new ConteggioPari(dati, da, a);
            thread[k] = new Thread(lavori[k]);
            thread[k].start();
        }
        int totale = 0;
        for (int k = 0; k < n; k++) {                      // ciclo 2: attende e raccoglie
            thread[k].join();
            totale += lavori[k].getPari();
        }
        System.out.println("Pari: " + totale);
    }
}
```

```text
Pari: 5
```

Eccezioni: `InterruptedException` per `join` (qui dichiarata con `throws` nel `main`). I cinque punti da ricordare: **due array** (lavori e thread); **due cicli** (uno di `start`, uno di `join`); il risultato si legge dal **`Runnable`**, mai dal `Thread`; **l'ultimo thread prende il resto**; `join` **prima** di leggere.

### Scheletro 4 — Sentinella `volatile` per fermare un thread

*Quando si usa:* quando un thread deve ripetere un lavoro finché non gli si dice di smettere.

```java
class Ripete implements Runnable {
    private volatile boolean attivo = true;             // volatile: visibile agli altri thread

    public void ferma() {
        attivo = false;
    }

    public void run() {
        while (attivo) {                                // controlla la sentinella a ogni giro
            System.out.println("lavoro...");
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
            }
        }
        System.out.println("terminato");
    }
}

public class FermaSentinella {
    public static void main(String[] args) throws InterruptedException {
        Ripete r = new Ripete();
        Thread t = new Thread(r);
        t.start();
        Thread.sleep(120);                              // lasciamo lavorare il thread
        r.ferma();                                      // abbassa la sentinella
        t.join();                                       // attende l'uscita ordinata
    }
}
```

Una esecuzione tipica:

```text
lavoro...
lavoro...
lavoro...
terminato
```

Il numero di righe `lavoro...` dipende dalla durata della pausa; `terminato` è sempre l'ultima. Import: nessuno. `InterruptedException` va gestita in `sleep` dentro `run` e dichiarata nel `main` per `Thread.sleep` e `join`.

### Scheletro 5 — Sottoclasse con `Runnable`, due costruttori e *information hiding*

*Quando si usa:* quando la traccia chiede una classe che estende un'altra classe, realizza `Runnable` e ha campi privati con `get`/`set`.

```java
class Veicolo {
    private String marca;
    private String modello;

    public Veicolo(String marca, String modello) {          // nessun costruttore senza parametri
        this.marca = marca;
        this.modello = modello;
    }

    public String getMarca() {
        return marca;
    }
}

class Furgone extends Veicolo implements Runnable {         // extends PRIMA, implements DOPO
    private int carico;
    private String colore;

    public Furgone(String marca, String modello, int carico) {
        super(marca, modello);                              // obbligatorio: la superclasse lo richiede
        this.carico = carico;
    }

    public Furgone(int carico, String colore) {
        super("n.d.", "n.d.");                              // il costruttore deve comunque chiamare super(...)
        this.carico = carico;
        this.colore = colore;
    }

    public void run() {                                     // ridefinisce Runnable.run
        carico = carico * 2;                                // sovrascrive il campo
    }

    public int getCarico() {
        return carico;
    }

    public void setCarico(int carico) {
        this.carico = carico;
    }

    public String getColore() {
        return colore;
    }

    public void setColore(String colore) {
        this.colore = colore;
    }
}

public class ProvaFurgone {
    public static void main(String[] args) throws InterruptedException {
        Furgone f = new Furgone("Fiat", "Ducato", 5);
        Thread t = new Thread(f);
        t.start();
        t.join();
        System.out.println(f.getCarico());
    }
}
```

```text
10
```

Punti che l'esame verifica alla lettera: `extends` prima di `implements`; **ogni** costruttore di `Furgone` chiama `super(...)`, perché `Veicolo` non ha un costruttore senza parametri; `run` è `public void run()`; i campi sono `private`.

---

## Errori tipici

> [!CAUTION]
> **Errore tipico — Chiamare `run()` invece di `start()`**
> ```java
> // ERRORE: nessun nuovo thread
> Thread t = new Thread(new Saluta("Anna"));
> t.run();                     // chiamata ordinaria, eseguita dal main
> ```
> Il programma compila e produce l'output previsto, ma **non è concorrente**: `run()` viene eseguito dal thread che lo chiama, cioè dal `main`, uno dopo l'altro. Se la traccia chiede di eseguire il lavoro "in un thread", l'output potrebbe essere identico e il codice comunque sbagliato (il nome stampato da `Thread.currentThread().getName()` sarebbe `main`). Forma corretta: `t.start();`.

> [!CAUTION]
> **Errore tipico — `start()` sullo stesso thread due volte**
> ```java
> // ERRORE a runtime
> Thread t = new Thread(new Saluta("Anna"));
> t.start();
> t.start();                   // IllegalThreadStateException
> ```
> Si lancia `java.lang.IllegalThreadStateException`: un thread si avvia **una sola volta**, anche se il primo `start` è già concluso. Forma corretta: per ripetere il lavoro si crea un **nuovo** `Thread`, `new Thread(lavoro).start();`.

> [!CAUTION]
> **Errore tipico — Dimenticare `start()`**
> ```java
> // ERRORE logico: il thread non parte mai
> Thread t = new Thread(new Saluta("Anna"));
> t.join();                    // ritorna subito: t non è mai stato avviato
> ```
> Il programma compila e non dà errori, ma il lavoro **non viene mai eseguito**: il thread resta nello stato `NEW`. `join` su un thread mai avviato ritorna subito (un thread non avviato non è vivo). Forma corretta: `t.start();` prima del `join`.

> [!CAUTION]
> **Errore tipico — `sleep` o `join` senza gestire `InterruptedException`**
> ```java
> // ERRORE di compilazione
> public class SenzaCatch {
>     public static void main(String[] args) {
>         Thread.sleep(100);
>     }
> }
> ```
> Il compilatore rifiuta il programma: `unreported exception java.lang.InterruptedException; must be caught or declared to be thrown`. L'eccezione è **controllata** ([Capitolo 13](13-eccezioni.md)). Forma corretta: racchiudere la chiamata in `try { ... } catch (InterruptedException e) { ... }`, oppure dichiarare `throws InterruptedException` nel metodo. Dentro `run()`, che non può dichiarare eccezioni controllate, resta solo il `try`/`catch`.

> [!CAUTION]
> **Errore tipico — `throws InterruptedException` sul metodo `run()`**
> ```java
> // ERRORE di compilazione
> class Lavoro implements Runnable {
>     public void run() throws InterruptedException {
>         Thread.sleep(100);
>     }
> }
> ```
> `run()` di `Runnable` non dichiara eccezioni, e un metodo che lo ridefinisce non può dichiararne di controllate: errore `run() in Lavoro cannot implement run() in Runnable; overridden method does not throw InterruptedException`. Forma corretta: il `try`/`catch` **dentro** `run`.

> [!CAUTION]
> **Errore tipico — `run()` senza `public`, o con la firma sbagliata**
> ```java
> // ERRORE 1: senza public
> class Lavoro implements Runnable {
>     void run() { }
> }
> ```
> Compilare dà `run() in Lavoro cannot implement run() in Runnable; attempting to assign weaker access privileges; was public`: i metodi di un'interfaccia sono pubblici e la ridefinizione non può esserlo meno ([Capitolo 10](10-classi-astratte-e-interfacce.md)). Se invece il metodo si chiama `Run`, o riceve un parametro (`public void run(int n)`), non è la `run()` dell'interfaccia: la classe resta senza il metodo richiesto e l'errore è `Lavoro is not abstract and does not override abstract method run() in Runnable`. Forma corretta: esattamente `public void run()`.

> [!CAUTION]
> **Errore tipico — Sottoclasse di `Thread` con un `run` dalla firma sbagliata (che compila)**
> ```java
> // ERRORE logico, senza messaggio del compilatore
> class Lavoro extends Thread {
>     public void run(int volte) {                 // overloading, NON override
>         System.out.println("lavoro");
>     }
> }
> // new Lavoro().start();  ->  non stampa nulla
> ```
> Con `extends Thread` non c'è un metodo astratto che obblighi a ridefinire `run`: `Thread` ha già un `run()` (che non fa nulla). Scrivere `run(int volte)` definisce un metodo **diverso** (overloading), il programma **compila**, e `start()` esegue il `run()` ereditato, cioè niente. Si evita con `@Override` davanti al metodo ([Capitolo 9](09-ereditarieta-e-polimorfismo.md), paragrafo 9.4.2), che fa emergere subito l'errore: `method does not override or implement a method from a supertype`. Forma corretta: `public void run()`.

> [!CAUTION]
> **Errore tipico — Chiamare `start()` su un oggetto che realizza solo `Runnable`**
> ```java
> // ERRORE di compilazione
> Saluta lavoro = new Saluta("Anna");          // Saluta implements Runnable
> lavoro.start();                              // cannot find symbol
> ```
> `Saluta` è un `Runnable`, non un `Thread`: non ha `start()`. Il compilatore segnala `cannot find symbol` su `start()`. Forma corretta: `new Thread(lavoro).start();`.

> [!CAUTION]
> **Errore tipico — Chiamare sul `Thread` un metodo del `Runnable`**
> ```java
> // ERRORE di compilazione
> Fattoriale lavoro = new Fattoriale(10);
> Thread t = new Thread(lavoro);
> t.start();
> t.join();
> long r = t.getRisultato();                   // cannot find symbol
> ```
> Il risultato sta nell'oggetto `Fattoriale`, non nel `Thread`: `Thread` non ha un metodo `getRisultato`. Forma corretta: `long r = lavoro.getRisultato();`. Per questo, con più thread, si tengono **due array**: uno di `Runnable` e uno di `Thread`.

> [!CAUTION]
> **Errore tipico — Leggere il risultato prima di `join`**
> ```java
> // ERRORE logico: il thread non ha ancora finito
> Thread t = new Thread(lavoro);
> t.start();
> System.out.println(lavoro.getRisultato());   // stampa 0 (o un valore parziale)
> t.join();
> ```
> `start` non aspetta: il thread lavora per conto suo, e il `main` legge il campo subito. Se `run` impiega un po' di tempo, si legge il valore iniziale (nella prova, con un `run` che dorme 100 millisecondi prima di calcolare, la lettura anticipata ha dato `0` e quella dopo `join` il valore giusto). Forma corretta: `t.join();` **prima** di leggere il risultato.

> [!CAUTION]
> **Errore tipico — `t.sleep(...)`: `sleep` non agisce su `t`**
> ```java
> // ERRORE logico: compila, ma fa dormire il thread sbagliato
> Thread t = new Thread(new Saluta("Anna"));
> t.start();
> t.sleep(1000);                // dorme il MAIN, non t
> ```
> `sleep` è un metodo **statico**: la riga viene letta come `Thread.sleep(1000)` e sospende il thread che la sta eseguendo, cioè il `main`. Il compilatore, di norma, non dice nulla (con l'opzione `-Xlint:static` segnala soltanto che un metodo statico andrebbe chiamato con il nome della classe). Forma corretta: per far dormire un thread, la chiamata va scritta **dentro il suo `run`**: `Thread.sleep(1000);`.

> [!CAUTION]
> **Errore tipico — Sentinella senza `volatile`**
> ```java
> // ERRORE: il thread può non fermarsi mai
> class Ciclo implements Runnable {
>     private boolean attivo = true;               // manca volatile
>     public void ferma() { attivo = false; }
>     public void run() {
>         while (attivo) { }                       // ciclo che non fa altro
>     }
> }
> ```
> Il programma compila. Ma se un thread esegue questo ciclo e un altro chiama `ferma()`, la macchina virtuale può continuare a usare per sempre il valore `true` che il thread ha letto all'inizio: in una prova su questo schema il thread era **ancora vivo** due secondi dopo `ferma()`. Forma corretta: `private volatile boolean attivo = true;`.

> [!CAUTION]
> **Errore tipico — Avviare il thread nel costruttore**
> ```java
> // ERRORE di struttura: il thread parte prima che l'oggetto sia completo
> class Notifica extends Thread {
>     private String testo;
>
>     public Notifica(String testo) {
>         start();                                 // il thread parte qui...
>         this.testo = testo;                      // ...ma testo viene assegnato dopo
>     }
>
>     public void run() {
>         System.out.println("Testo: " + testo);   // può stampare "Testo: null"
>     }
> }
> ```
> Compila, e in molte esecuzioni stampa bene; ma `run()` può partire **prima** che il costruttore abbia assegnato `testo` e stampare `Testo: null`. Inoltre, se il chiamante avvia lo stesso oggetto con `start()`, si ottiene un'`IllegalThreadStateException`. Forma corretta: il costruttore assegna i campi e basta; `start()` lo chiama chi crea l'oggetto, dopo `new`.

> [!CAUTION]
> **Errore tipico — Un solo `Runnable` per tutti i thread, quando ognuno ha il suo stato**
> ```java
> // ERRORE logico: tutti i thread lavorano sullo stesso oggetto
> SommaParziale lavoro = new SommaParziale(dati, 0, 3);
> for (int k = 0; k < n; k++) {
>     thread[k] = new Thread(lavoro);              // lo stesso lavoro per tutti
>     thread[k].start();
> }
> ```
> Se ogni thread deve lavorare su una **porzione diversa** o depositare un **risultato proprio**, serve **un oggetto `Runnable` per ciascuno**: con un solo oggetto, tutti i thread leggono e scrivono gli stessi campi e i risultati si sovrappongono. Forma corretta: dentro il ciclo, `lavori[k] = new SommaParziale(dati, da, a);`.

> [!CAUTION]
> **Errore tipico — Fidarsi dell'ordine delle stampe, di `yield` o delle priorità**
> ```java
> // ERRORE logico: l'ordine non è garantito
> Thread a = new Thread(new Saluta("A"));
> Thread b = new Thread(new Saluta("B"));
> b.setPriority(Thread.MAX_PRIORITY);
> a.start();
> b.start();                                       // "B prima di A"? non è garantito
> ```
> Né la priorità né `yield` né l'ordine degli `start` fissano l'ordine con cui i thread stampano: lo decide lo scheduler. Una traccia con un **output atteso** non può dipendere da questo. Se si vuole un ordine, lo si impone: si avvia `a`, si fa `a.join()`, poi si avvia `b`; oppure si fanno stampare i risultati al `main`, dopo i `join`, nell'ordine desiderato.

---

## Riassunto

Un programma normale ha un solo flusso di esecuzione; un programma con **thread** ne ha più, che procedono insieme dentro lo stesso processo e **condividono la memoria** (lo heap), tenendo ciascuno per sé soltanto lo stack. Questo rende facile comunicare e pericoloso modificare gli stessi dati, ed è per questo che l'ordine con cui i thread avanzano non è prevedibile e un programma corretto non deve dipenderne. In Java un thread è un **oggetto `Thread`**, il cui metodo `run()` contiene il codice da eseguire e il cui metodo `start()` crea il nuovo flusso. Il codice di `run()` si fornisce in due modi: **estendendo `Thread`** e ridefinendo `run`, oppure **realizzando `Runnable`** e passando l'oggetto a `new Thread(...)`; il secondo modo è obbligatorio quando la classe ha già una superclasse. Un thread attraversa un ciclo di vita (creato, eseguibile, in attesa, terminato) e termina quando `run` ritorna; per fermarlo si usa una **sentinella `volatile`**, non `stop()`. I metodi di controllo sono `currentThread`, `getName`, `sleep` (che dichiara `InterruptedException`), `yield`, `join` e `isAlive`, e le priorità. Per far lavorare più thread su un problema si usa il pattern **avvia tutti, poi aspetta tutti**: due array (`Runnable` e `Thread`), un ciclo di `start`, un ciclo di `join`, e il risultato si legge dal `Runnable` dopo `join`.

**Concetti chiave**

- **Processo e thread**: il processo ha memoria privata; i thread di uno stesso processo condividono lo heap, ma ognuno ha il proprio stack. Il cambio di contesto tra thread è più leggero.
- **Ordine imprevedibile**: lo scheduler decide quando ogni thread procede. Un programma non deve dipendere dall'ordine tra le stampe di thread diversi; lo si impone con `join`.
- **Thread principale**: ogni programma ha almeno il thread `main`; il programma termina quando tutti i thread (non daemon) sono finiti, non quando finisce il `main`.
- **`run` e `start`**: `run()` contiene il codice; `start()` crea il flusso e lo avvia, **una sola volta** (`IllegalThreadStateException` altrimenti). Chiamare `run()` a mano non crea un thread.
- **Due modi**: `extends Thread` + `public void run()`, oppure `implements Runnable` + `new Thread(oggetto)` + `start()` sul `Thread`. `Runnable` quando c'è già una superclasse.
- **Chi avvia**: il codice che crea il thread lo avvia; il costruttore prepara soltanto.
- **Stati**: `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, `TERMINATED` (`Thread.State`, `getState()`); terminazione quando `run` ritorna o quando un'eccezione ne esce senza fermare gli altri thread.
- **Sentinella `volatile`**: campo `boolean` letto da un thread e scritto da un altro; `volatile` garantisce la visibilità della modifica.
- **`sleep`**: statico, sospende il thread corrente; non rilascia i lock; dichiara `InterruptedException`, controllata, da catturare dentro `run`.
- **`join`**: attende la fine di un thread (`join(long)` con tempo massimo); si usa per ordinare le stampe e per leggere i risultati; dichiara `InterruptedException`. `isAlive()` dice se il thread è avviato e non finito.
- **`yield` e priorità**: suggerimenti allo scheduler, non garanzie.
- **Più thread insieme**: un `Runnable` per ogni thread, due array, due cicli; l'ultimo thread prende il resto; il risultato si legge dal `Runnable`, dopo `join`.
- **Race condition**: più thread che modificano lo stesso dato danno risultati imprevedibili (`contatore++` non è atomico). Si risolve con la mutua esclusione ([Capitolo 18](18-sincronizzazione.md)); `volatile` non basta.

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `Thread` | costruttori | `Thread()`, `Thread(Runnable)`, `Thread(String)`, `Thread(Runnable, String)` | — |
| `Thread` | `start` | `void start()` | `IllegalThreadStateException` (non controllata) |
| `Thread` | `run` | `void run()` | — |
| `Thread` | `sleep` | `static void sleep(long millis)` | `InterruptedException` (controllata); `IllegalArgumentException` se negativo |
| `Thread` | `join` | `final void join()`, `final void join(long millis)` | `InterruptedException` (controllata) |
| `Thread` | `isAlive` | `final boolean isAlive()` | — |
| `Thread` | `currentThread` | `static Thread currentThread()` | — |
| `Thread` | `getName`, `setName` | `final String getName()`, `final void setName(String)` | — |
| `Thread` | `yield` | `static void yield()` | — |
| `Thread` | `getPriority`, `setPriority` | `final int getPriority()`, `final void setPriority(int)` | `IllegalArgumentException` se fuori da 1-10 |
| `Thread` | `getState` | `Thread.State getState()` | — |
| `Runnable` | `run` | `void run()` | — (nessuna eccezione controllata) |
| `InterruptedException` | — | `class InterruptedException extends Exception` | è controllata |
