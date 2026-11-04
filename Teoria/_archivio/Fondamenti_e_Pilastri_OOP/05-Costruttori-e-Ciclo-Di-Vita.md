# 05. Costruttori, la Parola Chiave 'this' e il Ciclo di Vita

## Il Big Bang dell'Oggetto: La Parola Chiave `new`

In Java, la semplice dichiarazione di una variabile di tipo Oggetto non genera l'oggetto stesso. Come abbiamo visto studiando lo Stack e l'Heap, `Studente s;` crea solo un puntatore vuoto. 

Il vero "Big Bang", l'istante in cui lo spazio viene ritagliato nella memoria Heap e l'oggetto prende materialmente forma, avviene **esclusivamente** tramite l'uso della parola chiave spaziatrice `new`.

```java
// Fase 1: Creazione dell'istanza in Heap tramite 'new'
// Fase 2: Chiamata al metodo speciale "Costruttore" ( Studente() )
// Fase 3: Assegnazione dell'indirizzo risultante alla variabile 's' nello Stack
Studente s = new Studente(); 
```

Ma cosa accade in quell'esatto millisecondo in cui l'oggetto è appena stato forgiato nell'Heap ma non è ancora stato consegnato al programmatore? È qui che entra in gioco il **Costruttore**.

## Il Costruttore: Architetto dello Stato Iniziale

Il Costruttore è un metodo speciale la cui unica vocazione è **inizializzare lo stato** dell'oggetto neonato. Assicura che l'oggetto non nasca in un limbo di variabili vuote (i `null` e gli zero di default di Java), ma entri nel mondo con un'identità coerente e pronta all'uso.

> **Regole Auree del Costruttore:**
> 1. Il nome del costruttore deve corrispondere **esattamente e senza eccezioni** al nome della Classe.
> 2. A differenza dei metodi normali, il costruttore **non ha alcun tipo di ritorno**, nemmeno `void`. Se gli aggiungi `void`, il compilatore smetterà di trattarlo come costruttore e lo degraderà a metodo normale, causando bachi spaventosi.

### Il Costruttore di Default
Se tu non scrivi alcun costruttore all'interno della tua classe, il compilatore Java, mosso a compassione, ne inietterà uno invisibile, vuoto e senza parametri, noto come *Default Constructor*. Questo assicura che `new Oggetto()` funzioni sempre.
Tuttavia, **non appena scrivi un singolo costruttore personalizzato**, Java ritira la sua offerta: il costruttore di default scompare. Se ne hai bisogno, dovrai scriverlo esplicitamente a mano.

## Overloading e Flessibilità di Nascita

Grazie alla caratteristica dell'**Overloading (Sovraccarico)**, una classe può offrire molteplici costruttori, a patto che ognuno abbia una "firma" (numero o tipo di parametri) diversa. Questo permette al software di avere diverse "opzioni di fabbrica" al momento della creazione.

```java
public class Libro {
    private String titolo;
    private String autore;
    private int pagine;

    // Costruttore 1: Opzione completa (Tutti i parametri)
    public Libro(String titolo, String autore, int pagine) {
        this.titolo = titolo;
        this.autore = autore;
        this.pagine = pagine;
    }

    // Costruttore 2: Overloading (Opzione veloce senza pagine)
    public Libro(String titolo, String autore) {
        // Usa il costruttore precedente per evitare duplicazioni di codice
        this(titolo, autore, 0); 
    }
}
```

## L'Identità Autoreferenziale: La Parola Chiave `this`

La parola chiave `this` è un concetto filosofico prima che tecnico: è l'ego dell'oggetto. È un riferimento implicito che **l'oggetto usa per puntare a se stesso**.

In ambito accademico, l'uso del `this` è obbligatorio per risolvere il problema dello **Shadowing (Oscuramento) delle variabili**.
Quando un parametro del costruttore ha lo stesso identico nome di una variabile d'istanza della classe, il parametro più "vicino" oscura la variabile della classe.

```java
public class Punto2D {
    private int x; // Variabile d'istanza (Stato)

    // 'x' tra parentesi è il Parametro Locale. Oscura temporaneamente lo Stato.
    public Punto2D(int x) {
        // "La x di QUESTO (this) oggetto" = "Il parametro locale x"
        this.x = x; 
    }
}
```

Senza il `this`, scrivere `x = x;` equivarrebbe ad assegnare il parametro a se stesso, lasciando lo stato dell'oggetto miseramente vuoto e non inizializzato.

## La Fine del Viaggio: Il Garbage Collector

In linguaggi arcaici come il C++, la distruzione di un oggetto e la conseguente liberazione della memoria Heap è un compito estenuante a carico esclusivo del programmatore (usando istruzioni manuali come `free` o `delete`). Se il programmatore dimentica di liberare la memoria, il software si gonfia fino a collassare (il temibile *Memory Leak*).

Java automatizza questo processo drammatico tramite una divinità invisibile: il **Garbage Collector (Raccoglitore di Rifiuti)**.

Il ciclo di vita di un oggetto termina implicitamente. Il Garbage Collector è un processo (un demone a bassa priorità) della JVM che pattuglia costantemente l'Heap. La sua missione è scovare l'**Unreachable Memory** (Oggetti Irraggiungibili).
Se un oggetto nell'Heap non ha più alcun riferimento nello Stack che punta verso di esso (ad esempio, tutte le variabili che lo puntavano sono morte a causa delle regole di Scope, o sono state poste volontariamente a `null`), quell'oggetto viene giudicato "morto". 

A quel punto, il Garbage Collector entra in azione, distrugge l'oggetto e restituisce preziosa memoria RAM al sistema operativo. Questa automazione è una delle colonne portanti della stabilità e della sicurezza intrinseca delle architetture Java.