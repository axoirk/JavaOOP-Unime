---
materia: Programmazione a Oggetti
capitolo: 12
titolo: Generics e collezioni
livello_syllabus: 2-3
stato: completo
slide: ["Savitch cap. 12 slide 1-18", "Savitch cap. 15 slide 1-12 e 17-30"]
appelli: []
fonti_esterne: 11
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 12 — Generics e collezioni

## Di cosa parla questo capitolo

Nel [Capitolo 5](05-array-e-matrici.md) abbiamo incontrato il limite più fastidioso degli array: la lunghezza è decisa al momento della creazione e non cambia più. Per aggirarlo abbiamo usato un contatore e un array "abbastanza grande", oppure abbiamo copiato tutto in un array più grande. Sono rimedi che funzionano ma che costringono a riscrivere ogni volta la stessa logica. In questo capitolo vediamo come la libreria di Java e il linguaggio stesso risolvono il problema in modo definitivo: con **strutture dati che crescono da sole**, le *collezioni*, e con la **notazione** che dice di che tipo sono gli elementi che contengono, i *generics*.

Il percorso ha tre tappe. Prima la collezione più semplice e più usata, l'`ArrayList`, che si comporta come un array che si allunga e si accorcia a richiesta. Poi i **generics**: che cosa significa la scrittura `ArrayList<String>`, come si dichiara una classe con un parametro di tipo, e perché non si può scrivere `ArrayList<int>`. Infine la seconda grande idea per rappresentare una sequenza, la **lista concatenata**: ne scriviamo una a mano, con il nodo nascosto dentro la lista (la tecnica del [Capitolo 11](11-classi-annidate.md)), le aggiungiamo un **iteratore** e la rendiamo generica. Il capitolo si chiude con le collezioni che la libreria offre già pronte: la `LinkedList`, gli insiemi (`HashSet`, `TreeSet`), le mappe (`HashMap`, `TreeMap`), e gli strumenti per ordinarle (`Comparator`, `Collections.sort`).

Alla fine saprai creare e usare un `ArrayList`, scrivere correttamente i tipi con le parentesi angolari, definire una piccola classe generica, scrivere una lista concatenata con nodo interno privato e iteratore, e scegliere tra lista, insieme e mappa in base a ciò che la traccia chiede. Saprai anche evitare gli errori che il compilatore o il test nascosto puniscono: l'indice fuori dai limiti, il `remove` che sceglie l'overload sbagliato, la collezione modificata mentre la si percorre.

> [!IMPORTANT]
> **Nota per l'esame — Le collezioni sono "materiale da costruzione"**
> Le collezioni sono la parte del programma che più spesso si incontra *dentro* altri esercizi: un `ArrayList` per tenere gli oggetti creati, una `HashMap` per contare o per cercare per nome, un `Collections.sort` per stamparli in ordine. Nessun appello ufficiale le assegna come tema dichiarato, ma fanno parte delle API di base (insieme a file, socket, XML e JDBC) su cui si basa il secondo esercizio della prova. Per questo il capitolo dà le **firme esatte** e gli **scheletri** da saper scrivere a memoria, e insiste sui nomi dei metodi (`size`, non `length`; `get`, non `[ ]`) e sugli `import`, perché su un editor senza aiuti un nome sbagliato vale un'esecuzione persa.

## 12.1 L'array che cresce: `ArrayList`

### 12.1.1 Il problema: un array non si allunga

Immagina di dover tenere l'elenco dei prodotti di una spesa mentre l'utente li digita, senza sapere quanti saranno. Con un array dobbiamo decidere in anticipo la capienza. Se la scegliamo piccola, a un certo punto non c'è più posto; se la scegliamo enorme, sprechiamo memoria quasi sempre. L'alternativa del Capitolo 5 è creare un array più grande e copiarvi tutto ogni volta che si riempie: si può fare, ma è un lavoro "goffo e artificioso" da ripetere in ogni programma.

La libreria di Java offre una classe fatta apposta, **`ArrayList`**, nel package `java.util`. È una **lista**: una sequenza ordinata di elementi in cui si può aggiungere in fondo, all'inizio o in mezzo, e anche modificare, togliere, leggere e contare gli elementi. La sua lunghezza cambia mentre il programma gira.

L'`ArrayList` ha due prezzi da pagare. Il primo è l'efficienza: è meno efficiente di un array, perché dietro le quinte **usa davvero un array**, che quando si riempie viene sostituito da uno più grande (esattamente la tecnica "goffa" di cui sopra, scritta una volta per tutte dentro la classe). Il secondo è che **può contenere solo oggetti**: non si può mettere dentro un `int`, un `double` o un `char` direttamente, mentre un array può contenere sia primitivi sia oggetti. Vedremo in §12.1.4 come si aggira, con le classi *wrapper* del [Capitolo 6](06-metodi.md).

### 12.1.2 Creare un `ArrayList`

Per usare la classe va importata, e al momento di creare la lista si dice **di che tipo sono gli elementi** che conterrà, scrivendo il tipo tra parentesi angolari.

```java
import java.util.ArrayList;

public class SpesaVuota {
    public static void main(String[] args) {
        ArrayList<String> spesa = new ArrayList<String>(20);   // lista di String, capacità iniziale 20
        ArrayList<String> altra = new ArrayList<>();           // forma abbreviata: il tipo si deduce
        System.out.println(spesa.size());
        System.out.println(altra.size());
    }
}
```

```text
0
0
```

Leggiamo le due righe di creazione.

- `ArrayList<String>` è il **tipo** della variabile: "lista di `String`". Il tipo tra parentesi angolari è il *parametro di tipo* e lo studiamo in §12.2; per ora basta leggerlo come "contiene `String`".
- `new ArrayList<String>(20)` crea la lista e dice che, all'inizio, ha **posto per 20 elementi**. La capacità iniziale non è un limite: se gli elementi superano 20, la lista si allarga da sola. Serve solo a evitare riallocazioni quando si sa già più o meno quanti elementi arriveranno.
- `new ArrayList<>()` non indica la capacità, e allora è dieci (lo dice la documentazione). Le parentesi angolari lasciate vuote, `<>`, sono lecite dalla versione 7 di Java e si leggono "il tipo è lo stesso della variabile a sinistra". Sono la forma più comoda, e le userò d'ora in poi; ma la forma completa, con il tipo ripetuto, è equivalente e va riconosciuta nel codice altrui e nelle slide.
- Appena creata la lista è **vuota**: `size()` restituisce 0. Una lista vuota non è `null`: è un oggetto valido con zero elementi.

> [!NOTE]
> **Approfondimento esterno — `java.util.ArrayList`**
> La Javadoc di Java 17 la descrive come *"Resizable-array implementation of the List interface"*, che "permette tutti gli elementi, compreso `null`". I costruttori sono due: `public ArrayList(int initialCapacity)`, che lancia `IllegalArgumentException` se la capacità iniziale è negativa, e `public ArrayList()`, che crea una lista vuota "con una capacità iniziale di dieci". Le operazioni `size`, `isEmpty`, `get` e `set` richiedono tempo costante, e `add` tempo costante ammortizzato; tutte le altre tempo lineare. Ogni istanza ha una *capacity*, "la dimensione dell'array usato per conservare gli elementi", sempre almeno pari alla dimensione della lista, e che cresce automaticamente; i dettagli della politica di crescita non sono specificati. La classe **non è sincronizzata**: l'uso da più thread richiede una sincronizzazione esterna (Capitolo 18).
>
> *Fonte:* [java.util.ArrayList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/ArrayList.html)

### 12.1.3 I metodi essenziali

Un array si usa con le parentesi quadre; un `ArrayList` si usa **solo con metodi**. Non esistono `lista[0]` né `lista.length`. Con `ArrayList<String> lista` i metodi da conoscere a memoria sono questi.

| Voglio | Scrivo | Note |
|---|---|---|
| aggiungere in fondo | `lista.add(x)` | restituisce `boolean` (sempre `true`) |
| inserire in una posizione | `lista.add(indice, x)` | gli elementi successivi scorrono a destra; `void` |
| leggere l'elemento in posizione `i` | `lista.get(i)` | restituisce il tipo `E` (qui `String`) |
| sostituire l'elemento in posizione `i` | `lista.set(i, x)` | restituisce il **vecchio** elemento |
| togliere l'elemento in posizione `i` | `lista.remove(i)` | gli elementi successivi scorrono a sinistra; restituisce l'elemento tolto |
| togliere la prima occorrenza di `x` | `lista.remove(x)` | restituisce `boolean`: `true` se l'ha trovato |
| quanti elementi | `lista.size()` | un `int`; non `length` e non `length()` |
| è vuota? | `lista.isEmpty()` | un `boolean` |
| contiene `x`? | `lista.contains(x)` | confronto con `equals` |
| posizione della prima occorrenza di `x` | `lista.indexOf(x)` | `-1` se non c'è |
| svuotarla | `lista.clear()` | |

Le posizioni (gli *indici*) partono da **0**, come negli array: il primo elemento è `get(0)`, l'ultimo `get(size() - 1)`.

#### Esempio — Una lista della spesa

Il programma crea una lista, vi aggiunge tre elementi, ne inserisce uno in mezzo, ne sostituisce uno e ne toglie uno. Dopo ogni passo stampiamo la lista: la stampa di un `ArrayList` mostra gli elementi tra parentesi quadre, separati da una virgola e uno spazio.

```java
import java.util.ArrayList;

public class ListaDellaSpesa {
    public static void main(String[] args) {
        ArrayList<String> spesa = new ArrayList<>();

        spesa.add("pane");                       // [pane]
        spesa.add("latte");                      // [pane, latte]
        spesa.add("uova");                       // [pane, latte, uova]
        System.out.println(spesa);

        spesa.add(1, "burro");                   // inserisce in posizione 1: gli altri scorrono a destra
        System.out.println(spesa);

        String vecchio = spesa.set(0, "pasta");  // sostituisce la posizione 0 e restituisce "pane"
        System.out.println(vecchio + " -> " + spesa.get(0));

        spesa.remove(2);                         // toglie la posizione 2 ("latte")
        System.out.println(spesa);

        boolean tolto = spesa.remove("uova");    // toglie la prima occorrenza di "uova"
        System.out.println(tolto + " " + spesa);

        System.out.println(spesa.size() + " " + spesa.indexOf("burro") + " " + spesa.contains("pane"));
    }
}
```

```text
[pane, latte, uova]
[pane, burro, latte, uova]
pane -> pasta
[pasta, burro, uova]
true [pasta, burro]
2 1 false
```

Seguiamo l'esecuzione. Dopo le tre `add` la lista è `[pane, latte, uova]`. `add(1, "burro")` infila `"burro"` in posizione 1 e fa scorrere `"latte"` e `"uova"` di un posto a destra. `set(0, "pasta")` rimpiazza `"pane"`, che il metodo restituisce (lo conserviamo in `vecchio`). Ora la lista è `[pasta, burro, latte, uova]` e `remove(2)` toglie la posizione 2, cioè `"latte"`, facendo scorrere `"uova"` a sinistra. `remove("uova")` cerca l'oggetto e lo toglie: restituisce `true`. Alla fine la lista ha due elementi; `indexOf("burro")` vale 1 e `contains("pane")` è `false` perché `"pane"` era stato rimpiazzato.

Un dettaglio che conta in un esame: `lista.add(i, x)` ha **due** argomenti, con l'indice **per primo**, e `lista.set(i, x)` ugualmente. Il `add` a un solo argomento aggiunge in fondo.

> [!NOTE]
> **Approfondimento esterno — `add`, `get`, `set`, `remove` e le loro eccezioni**
> Le firme della Javadoc di `ArrayList<E>` sono: `public boolean add(E e)`, `public void add(int index, E element)`, `public E get(int index)`, `public E set(int index, E element)`, `public E remove(int index)`, `public boolean remove(Object o)`, `public int size()`, `public boolean isEmpty()`, `public boolean contains(Object o)`, `public int indexOf(Object o)`, `public void clear()`. `set` e `remove(int)` restituiscono l'elemento che c'era prima (`E`). `get`, `set` e `remove(int)` lanciano `IndexOutOfBoundsException` "se l'indice è fuori dall'intervallo" (indice negativo, oppure maggiore o uguale a `size()`); anche `add(int, E)` la lancia, ma con un intervallo più largo: l'indice può valere `size()` (inserire in fondo) e non oltre. `remove(Object)` toglie "la prima occorrenza" dell'elemento, con `Objects.equals(o, get(i))`, e restituisce `true` se la lista conteneva l'elemento. `contains` e `indexOf` confrontano con `equals`, non con `==`.
>
> *Fonte:* [java.util.ArrayList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/ArrayList.html)

### 12.1.4 Solo oggetti: le liste di numeri e il `remove` ambiguo

Come detto un `ArrayList` contiene soltanto oggetti. Per tenere dei numeri si usa il tipo **wrapper**, cioè la classe che avvolge il primitivo (Capitolo 6, sezione 6.6): `Integer` per `int`, `Double` per `double`, `Character` per `char`, `Boolean` per `boolean`. Scrivere `ArrayList<int>` non compila; si scrive `ArrayList<Integer>`. La conversione tra `int` e `Integer` è automatica nei due sensi (*autoboxing* e *unboxing*, §6.6.3), quindi il codice si scrive come se la lista contenesse `int`.

#### Esempio — Una lista di numeri

```java
import java.util.ArrayList;

public class ListaDiNumeri {
    public static void main(String[] args) {
        ArrayList<Integer> voti = new ArrayList<>();
        voti.add(28);                        // autoboxing: 28 diventa un Integer
        voti.add(30);
        voti.add(24);

        int primo = voti.get(0);             // unboxing: l'Integer torna int
        int somma = 0;
        for (int v : voti) {                 // il for-each estrae i valori come int
            somma += v;
        }
        System.out.println(primo + " " + somma + " " + (double) somma / voti.size());
    }
}
```

```text
28 82 27.333333333333332
```

`voti.add(28)` equivale a `voti.add(Integer.valueOf(28))`. Nel `for (int v : voti)` ogni elemento `Integer` viene convertito in `int` al volo. L'ultima espressione divide la somma, trasformata in `double` con il cast, per `voti.size()` (il numero degli elementi, 3).

C'è però una trappola che nei numeri interi è quasi inevitabile, perché `remove` esiste in **due forme**: `remove(int index)` e `remove(Object o)`. Con una `ArrayList<Integer>` il compilatore sceglie quella che si adatta meglio all'argomento che scriviamo, e un `int` "puro" si adatta a `remove(int index)`.

```java
import java.util.ArrayList;

public class RemoveAmbiguo {
    public static void main(String[] args) {
        ArrayList<Integer> numeri = new ArrayList<>();
        numeri.add(10);
        numeri.add(20);
        numeri.add(30);

        numeri.remove(1);                    // int: toglie la POSIZIONE 1, cioè il 20
        System.out.println(numeri);

        numeri.remove(Integer.valueOf(30));  // Integer: toglie l'OGGETTO 30
        System.out.println(numeri);
    }
}
```

```text
[10, 30]
[10]
```

`numeri.remove(1)` non cerca il valore 1: il literal `1` è un `int`, e per un `int` il metodo più adatto è `remove(int index)`, che toglie la posizione 1. Per togliere *il valore* bisogna passare un oggetto `Integer`, ad esempio con `Integer.valueOf(30)` o con il cast `(Integer) 30`. Con una `ArrayList<String>` il problema non esiste, perché un `String` non può essere scambiato per un indice.

> [!NOTE]
> **Approfondimento esterno — Le due forme di `remove`**
> Nella Javadoc di Java 17 le due versioni sono dichiarate `public E remove(int index)` ("rimuove l'elemento in una posizione data e sposta a sinistra gli elementi successivi") e `public boolean remove(Object o)` ("rimuove la prima occorrenza dell'elemento, se presente"). Sono due metodi diversi, con firme diverse (*overloading*, Capitolo 6, sezione 6.7), e la scelta tra loro la fa il compilatore dal tipo dell'argomento.
>
> *Fonte:* [java.util.ArrayList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/ArrayList.html)

### 12.1.5 Scorrere una lista

Per vedere tutti gli elementi di una lista ci sono due modi. Il primo è il `for` con l'indice, come per gli array, usando `size()` come limite e `get(i)` per leggere. Il secondo è il **`for-each`** (Capitolo 5, sezione 5.2.3), che funziona identico sulle liste: legge ogni elemento in ordine, senza indice.

#### Esempio — Una lista di oggetti

Qui la lista contiene oggetti di una classe nostra. È il caso più frequente: la collezione tiene gli oggetti che il programma crea, e il ciclo li percorre.

```java
import java.util.ArrayList;

class Attivita {
    private String descrizione;
    private int minuti;

    public Attivita(String descrizione, int minuti) {
        this.descrizione = descrizione;
        this.minuti = minuti;
    }

    public int getMinuti() {
        return minuti;
    }

    public String toString() {
        return descrizione + " (" + minuti + " min)";
    }
}

public class Agenda {
    public static void main(String[] args) {
        ArrayList<Attivita> agenda = new ArrayList<>();
        agenda.add(new Attivita("studiare", 90));
        agenda.add(new Attivita("pausa", 15));
        agenda.add(new Attivita("esercizi", 60));

        for (int i = 0; i < agenda.size(); i++) {          // ciclo con indice
            System.out.println(i + ": " + agenda.get(i));
        }

        int totale = 0;
        for (Attivita a : agenda) {                        // for-each: a ogni giro un'Attivita
            totale += a.getMinuti();
        }
        System.out.println("totale " + totale + " minuti");
    }
}
```

```text
0: studiare (90 min)
1: pausa (15 min)
2: esercizi (60 min)
totale 165 minuti
```

`agenda.get(i)` restituisce un `Attivita`, e la concatenazione `i + ": " + ...` chiama `toString` sull'oggetto (Capitolo 9, sezione 9.7.2). Nel for-each la variabile `a` è un riferimento a ciascun oggetto della lista: leggere `a.getMinuti()` è lecito. Non scriviamo nessun cast, e questo è uno dei vantaggi dei generics (§12.2): il compilatore sa che la lista contiene `Attivita`.

> [!WARNING]
> **Attenzione — `get` non si usa al posto delle parentesi quadre**
> `agenda[0]`, `agenda.length` e `agenda.length()` non compilano con un `ArrayList`: l'errore è `array required, but ArrayList<Attivita> found` per il primo e `cannot find symbol` per gli altri. La forma giusta è `agenda.get(0)` e `agenda.size()`. E viceversa, su un array si scrive `a.length` (senza parentesi) e su una `String` `s.length()`. Tre strumenti diversi, tre scritture diverse.

### 12.1.6 Gli indici fuori dai limiti

Come per gli array, un indice sbagliato non è un errore di compilazione: si manifesta all'esecuzione. Per una lista l'eccezione è `IndexOutOfBoundsException`, con un messaggio che riporta l'indice e la dimensione.

```java
import java.util.ArrayList;

public class FuoriDaiLimiti {
    public static void main(String[] args) {
        ArrayList<String> l = new ArrayList<>();
        l.add("a");
        l.add("b");

        System.out.println(l.get(1));
        System.out.println(l.get(2));        // ci sono due elementi: gli indici validi sono 0 e 1
    }
}
```

```text
b
```

Dopo aver stampato `b` il programma si interrompe sulla seconda `println` e il sistema scrive sul canale degli errori, al posto del risultato, un messaggio che comincia con `Exception in thread "main" java.lang.IndexOutOfBoundsException: Index 2 out of bounds for length 2`, seguito da alcune righe `at ...` (la *traccia dello stack*). Ciò che conta è il messaggio `Index 2 out of bounds for length 2` (indice 2, lunghezza 2) e, tra le righe `at ...`, l'ultima, che indica il punto del *nostro* programma in cui è partito l'errore; il resto della traccia varia con la versione di Java. Un indice valido per `get` va da `0` a `size() - 1`. Per `add(indice, x)` l'indice può arrivare a `size()` (che significa "in fondo"); un valore maggiore lancia la stessa eccezione. Le eccezioni sono il tema del [Capitolo 13](13-eccezioni.md).

### 12.1.7 Capacità, copia e `trimToSize`

Due dettagli, entrambi nelle slide del corso. Il primo è `trimToSize()`: dopo aver riempito una lista la sua capacità può essere più grande del necessario, e questo metodo la riduce alla dimensione effettiva, per risparmiare memoria. Non cambia gli elementi, e di solito non serve in un esame.

Il secondo è la **copia**. Copiare una lista con l'assegnazione non crea una seconda lista: come per tutti gli oggetti (Capitolo 8, sezione 8.2), si copia il *riferimento*.

```java
import java.util.ArrayList;

public class CopiaDiLista {
    public static void main(String[] args) {
        ArrayList<String> a = new ArrayList<>();
        a.add("x");
        a.add("y");

        ArrayList<String> alias = a;                       // stessa lista, due nomi
        ArrayList<String> copia = new ArrayList<>(a);      // lista nuova con gli stessi elementi

        a.add("z");
        System.out.println("a     = " + a);
        System.out.println("alias = " + alias);
        System.out.println("copia = " + copia);
    }
}
```

```text
a     = [x, y, z]
alias = [x, y, z]
copia = [x, y]
```

`alias` e `a` sono la stessa lista, quindi l'aggiunta di `"z"` si vede in entrambe. `copia` è una lista **nuova**, creata dal costruttore `ArrayList(Collection<? extends E> c)`, che prende un'altra collezione e ne copia gli elementi: l'aggiunta a `a` non la tocca. Le slide propongono invece il metodo `clone()`, che esiste ma ha un inconveniente: restituisce `Object`, e per usarlo come lista serve un cast (`(ArrayList<String>) a.clone()`), con un avviso del compilatore. Il costruttore di copia è più comodo e non richiede il cast, ed è quello che useremo.

> [!WARNING]
> **Attenzione — La copia è "superficiale"**
> `new ArrayList<>(a)` e `a.clone()` copiano la **lista** ma non gli oggetti che contiene: i due elenchi condividono gli stessi elementi. Per le `String` e i `Integer`, che non cambiano mai, non fa differenza. Se invece la lista contiene oggetti modificabili (le `Attivita` di prima, se avessero un setter), cambiare un oggetto attraverso una lista lo cambia anche nell'altra. La Javadoc di `clone` lo dice: *"Returns a shallow copy of this ArrayList instance. (The elements themselves are not copied.)"*. La copia degli oggetti, uno per uno, con un costruttore di copia, è nel Capitolo 8, sezione 8.6.

## 12.2 Classi parametriche e generics

### 12.2.1 Che cosa vuol dire `ArrayList<String>`

Fin qui abbiamo scritto `ArrayList<String>` come una formula. Fermiamoci a capire che cosa significa, perché sullo stesso meccanismo si regge tutta la libreria delle collezioni e, in piccolo, le classi che scriveremo noi.

`ArrayList` è una **classe parametrica** (*parameterized class*): una classe che ha un **parametro**, e questo parametro è un **tipo**. Il tipo tra parentesi angolari dice che cosa la lista contiene. Se l'`ArrayList` non fosse parametrica dovrebbe contenere elementi di un tipo qualunque (`Object`, la superclasse di tutte, Capitolo 9, sezione 9.7.1), e ogni volta che si legge un elemento servirebbe un cast verso il tipo vero. Con il parametro, invece, il compilatore sa fin dall'inizio che la lista contiene `String`, ti impedisce di inserirvi altro e ti consegna i `String` già pronti da usare. Le versioni di Java precedenti alla 5.0 avevano un `ArrayList` non parametrico, che è la ragione per cui il codice più vecchio ne è pieno.

La tecnica prende il nome di **generics** (*generici*) ed è disponibile a partire da Java 5.0.

> [!NOTE]
> **Definizione — Classe parametrica**
> Una classe è *parametrica* (o *generica*) se nella sua intestazione dichiara uno o più **parametri di tipo**, tra parentesi angolari: `class NomeClasse<T>`. Nel corpo, `T` si usa come se fosse il nome di una classe. Chi usa la classe sceglie il tipo vero scrivendolo al posto di `T`: `NomeClasse<String>`.

### 12.2.2 Scrivere una classe generica

Vediamo come si dichiara una classe con un parametro di tipo. L'esempio è una scatola che contiene un solo oggetto, di un tipo che si decide al momento dell'uso.

```java
class Scatola<T> {                          // T è il parametro di tipo
    private T contenuto;

    public Scatola(T contenuto) {
        this.contenuto = contenuto;
    }

    public T getContenuto() {
        return contenuto;
    }

    public void setContenuto(T contenuto) {
        this.contenuto = contenuto;
    }
}

public class ProvaScatola {
    public static void main(String[] args) {
        Scatola<String> s = new Scatola<String>("ciao");
        String testo = s.getContenuto();             // nessun cast: il compilatore sa che è un String
        System.out.println(testo.length());

        Scatola<Integer> n = new Scatola<>(42);
        n.setContenuto(n.getContenuto() + 1);        // unboxing e boxing automatici
        System.out.println(n.getContenuto());
    }
}
```

```text
4
43
```

Leggiamo i punti essenziali.

- `class Scatola<T>`: `T` è il parametro di tipo. Il nome è libero ma per convenzione è una lettera maiuscola: `T` per *type*, `E` per *element* (lo usano le collezioni), `K` e `V` per *key* e *value* (le mappe).
- Nel corpo, `T` compare dove si userebbe un nome di classe: come tipo del campo, del parametro, del valore restituito.
- `Scatola<String> s = new Scatola<String>("ciao")` sostituisce `T` con `String` dappertutto. Il `getContenuto()` restituisce un `String`; passare un `int` a `new Scatola<String>(...)` non compilerebbe.
- Con `Scatola<Integer>` la scatola contiene un `Integer`; `n.getContenuto() + 1` scarta l'oggetto in `int` per sommare e lo ricompatta nel `setContenuto`.

Un parametro di tipo può comparire quasi ovunque ci stia un nome di classe: come tipo di variabile, di parametro, di ritorno, e come argomento di un'altra classe parametrica (`ArrayList<T>`). Ha però due limiti che vanno ricordati perché si incontrano subito.

- **Non si può usare per allocare memoria.** Scrivere `new T[20]` (o `new T()`) è un errore di compilazione. Il motivo, semplificato: il compilatore usa il parametro per controllare i tipi, ma a esecuzione non sa quale classe vera sia `T`, e quindi non saprebbe che array costruire. L'errore è `generic array creation`.
- **Non si può usare un tipo primitivo come argomento.** `Scatola<int>` non compila: il parametro deve essere una classe. Si scrive `Scatola<Integer>`, come per `ArrayList<Integer>`.

Una classe generica può avere più parametri, separati da virgole.

```java
class Coppia<A, B> {
    private A primo;
    private B secondo;

    public Coppia(A primo, B secondo) {
        this.primo = primo;
        this.secondo = secondo;
    }

    public A getPrimo() {
        return primo;
    }

    public B getSecondo() {
        return secondo;
    }
}

public class ProvaCoppia {
    public static void main(String[] args) {
        Coppia<String, Integer> c = new Coppia<>("Anna", 30);
        System.out.println(c.getPrimo() + " " + c.getSecondo());
    }
}
```

```text
Anna 30
```

È lo stesso schema delle mappe di §12.6, che hanno due parametri, `Map<K,V>`.

### 12.2.3 Che cosa si rischia senza il parametro

Se si omette il parametro di tipo, la classe parametrica si usa nella sua forma "antica", detta **tipo grezzo** (*raw type*). Il programma compila ancora, ma il compilatore non può più aiutarci.

```java
import java.util.ArrayList;

public class TipoGrezzo {
    public static void main(String[] args) {
        ArrayList lista = new ArrayList();      // niente <...>: tipo grezzo
        lista.add("uno");
        lista.add(2);                           // nessuno lo impedisce

        String s = (String) lista.get(0);       // serve il cast: get restituisce Object
        System.out.println(s);
        String t = (String) lista.get(1);       // compila, ma a esecuzione fallisce
        System.out.println(t);
    }
}
```

Compilando, `javac` stampa l'avviso `Note: TipoGrezzo.java uses unchecked or unsafe operations.` e il programma, eseguito, si ferma sull'ultima riga con `java.lang.ClassCastException: class java.lang.Integer cannot be cast to class java.lang.String`. Con `ArrayList<String>` l'inserimento di `2` sarebbe stato rifiutato **in compilazione** (`incompatible types: int cannot be converted to String`): un errore trovato subito, invece che durante l'esecuzione, e senza consumare nessun tentativo di esecuzione in più. Conclusione: all'esame il tipo tra parentesi angolari va sempre scritto.

## 12.3 Le liste concatenate

### 12.3.1 Un altro modo di tenere una sequenza

Un `ArrayList` tiene gli elementi in un array: stanno in caselle consecutive, e per raggiungere la numero `i` basta un calcolo. Esiste un secondo modo, del tutto diverso, di rappresentare una sequenza: la **lista concatenata** (*linked list*). Qui gli elementi non stanno vicini in memoria. Ogni elemento sta in un piccolo oggetto, il **nodo**, che contiene due cose: il **dato** e un **collegamento** (*link*) al nodo successivo. Per ritrovare la sequenza basta un solo riferimento, quello al primo nodo, detto **testa** (*head*); l'ultimo nodo ha il collegamento a `null`, che segnala "qui finisce".

Immagina una caccia al tesoro: ogni biglietto contiene un indizio (il dato) e l'indirizzo del biglietto successivo (il collegamento). Per iniziare ti serve soltanto il primo biglietto; per arrivare al decimo devi leggere i nove precedenti. L'analogia ha un limite: nella caccia al tesoro i biglietti sono pezzi di carta, mentre i nodi sono oggetti che possiamo ricollegare a piacere.

Disegniamo una lista di tre stringhe. Ogni riquadro è un nodo; il riferimento `testa` indica il primo; il collegamento dell'ultimo nodo è `null`.

```text
testa
  |
  v
[ "a" | * ]--->[ "b" | * ]--->[ "c" | null ]
```

I due modi di tenere una sequenza hanno vantaggi opposti. Nell'array (e quindi nell'`ArrayList`) l'accesso alla posizione `i` è immediato, ma inserire o togliere un elemento in mezzo obbliga a spostare tutti i successivi. Nella lista concatenata inserire o togliere un elemento in testa (o dopo un nodo già raggiunto) richiede soltanto di cambiare uno o due collegamenti, ma per arrivare alla posizione `i` bisogna percorrere la catena dall'inizio.

La libreria di Java include una classe già pronta, `LinkedList` (§12.6.2). Qui ne scriviamo una a mano per due ragioni: capire come funzionano le strutture concatenate, e saperle scrivere quando una traccia lo chiede. Lo stesso schema (un nodo con un dato e un riferimento allo stesso tipo di nodo) sta anche dietro alle pile, alle code e agli alberi di §12.5.

### 12.3.2 Il nodo e la lista

Il nodo è una classe con due campi. Il secondo, il collegamento, ha come tipo **la classe stessa**: un `Nodo` contiene un riferimento a un altro `Nodo`. Come abbiamo visto nel [Capitolo 11](11-classi-annidate.md), sezione 11.3, conviene dichiarare il nodo come **classe interna privata** della lista, in modo che il resto del programma non possa né vedere né modificare i collegamenti (la *perdita di riservatezza* del [Capitolo 7](07-classi-e-oggetti.md), sezione 7.3.7). La lista tiene un solo campo, `testa`.

Le operazioni che aggiungono in testa e in coda, e quelle che contano e stampano, sono già nella sezione 11.3. Qui aggiungiamo le due operazioni che modificano la catena togliendo nodi, che sono le più delicate: **eliminare la testa** e **rimuovere un valore dato**.

```java
import java.util.NoSuchElementException;

class ListaDiStringhe {

    private class Nodo {
        private String dato;
        private Nodo successivo;

        Nodo(String dato, Nodo successivo) {
            this.dato = dato;
            this.successivo = successivo;
        }
    }

    private Nodo testa;

    public void aggiungiInTesta(String s) {
        testa = new Nodo(s, testa);
    }

    public String eliminaTesta() {
        if (testa == null) {
            throw new NoSuchElementException("lista vuota");
        }
        String eliminato = testa.dato;
        testa = testa.successivo;               // il vecchio primo nodo non è più raggiungibile
        return eliminato;
    }

    public boolean rimuovi(String s) {
        Nodo precedente = null;
        Nodo corrente = testa;
        while (corrente != null) {
            if (corrente.dato.equals(s)) {
                if (precedente == null) {
                    testa = corrente.successivo;                  // si toglie il primo nodo
                } else {
                    precedente.successivo = corrente.successivo;  // il precedente scavalca il nodo
                }
                return true;
            }
            precedente = corrente;
            corrente = corrente.successivo;
        }
        return false;                            // arrivati in fondo: s non c'era
    }

    public int dimensione() {
        int n = 0;
        for (Nodo c = testa; c != null; c = c.successivo) {
            n++;
        }
        return n;
    }

    public String toString() {
        String r = "[";
        for (Nodo c = testa; c != null; c = c.successivo) {
            r += c.dato;
            if (c.successivo != null) {
                r += ", ";
            }
        }
        return r + "]";
    }
}

public class ProvaRimozioni {
    public static void main(String[] args) {
        ListaDiStringhe l = new ListaDiStringhe();
        l.aggiungiInTesta("c");
        l.aggiungiInTesta("b");
        l.aggiungiInTesta("a");
        System.out.println(l);

        System.out.println(l.rimuovi("b"));      // nodo in mezzo
        System.out.println(l);
        System.out.println(l.rimuovi("z"));      // valore assente

        System.out.println(l.eliminaTesta());
        System.out.println(l.eliminaTesta());
        try {
            l.eliminaTesta();                    // la lista è ormai vuota
        } catch (NoSuchElementException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

```text
[a, b, c]
true
[a, c]
false
a
c
lista vuota
```

Seguiamo le due operazioni nuove.

- **`eliminaTesta`.** Se `testa` è `null` la lista è vuota e non c'è niente da togliere. Altrimenti si conserva il dato del primo nodo (perché dopo non sarà più raggiungibile), poi si sposta `testa` sul **secondo** nodo con `testa = testa.successivo`. Il vecchio primo nodo non è più puntato da nessuno: è un oggetto irraggiungibile, e il *garbage collector* ne libera la memoria (Capitolo 8, sezione 8.7), senza che il programma debba fare altro.
- **`rimuovi`.** Per togliere un nodo in mezzo non basta trovarlo: bisogna agire sul nodo **precedente**, il cui collegamento deve "scavalcare" quello da eliminare (`precedente.successivo = corrente.successivo`). Ma un nodo non conosce il proprio precedente: perciò il ciclo tiene due riferimenti che avanzano insieme, `precedente` (dietro) e `corrente` (davanti). Quando si elimina il **primo** nodo non c'è nessun precedente (`precedente == null`) e si aggiorna `testa`: è il caso particolare da non dimenticare.
- Il metodo restituisce `true` se ha tolto qualcosa, `false` altrimenti, e confronta con `equals` (Capitolo 8, sezione 8.4), non con `==`.

Un disegno della rimozione di `"b"` da `[a, b, c]`: prima il nodo `"a"` punta a `"b"`, poi punta direttamente a `"c"`, e `"b"` non è più raggiungibile.

```text
prima:   testa -> [a|*] -> [b|*] -> [c|null]
dopo:    testa -> [a|*] ---------> [c|null]        ([b|*] non è più raggiungibile)
```

> [!WARNING]
> **Attenzione — Il programma conosce solo la testa**
> Dalla lista il programma tiene in mano un solo riferimento, `testa`. Tutti gli altri nodi si raggiungono da lì, uno dopo l'altro. Due conseguenze. Primo: per scorrere la catena si usa una **variabile locale** (`corrente`) che avanza, e **mai** il campo `testa`, altrimenti i nodi che si lasciano alle spalle diventano irraggiungibili e vanno persi. Secondo: se per errore si scrive `corrente.successivo` quando `corrente` è `null` si ottiene una `NullPointerException` (Capitolo 8, sezione 8.3.2), e la riga indicata dal messaggio dice dove la catena è finita prima del previsto.

### 12.3.3 Errori nelle operazioni: lanciare un'eccezione

Nella versione del libro, quando un'operazione non poteva essere eseguita (per esempio togliere la testa di una lista vuota) il metodo stampava un messaggio e terminava il programma. È una scelta rigida: chi scrive la lista non può sapere che cosa preferisce chi la usa. La soluzione più elegante è **lanciare un'eccezione**, lasciando a chi chiama il metodo la decisione su come reagire.

È ciò che fa `eliminaTesta` nell'esempio precedente: se la lista è vuota esegue `throw new NoSuchElementException("lista vuota")`. `NoSuchElementException` è un'eccezione della libreria (package `java.util`) che significa "l'elemento richiesto non esiste": è la stessa che lanciano gli iteratori quando sono finiti. Il `main` della prova la intercetta con `try`/`catch` e stampa il messaggio. Come si dichiara, si lancia e si cattura un'eccezione, e come se ne definisce una propria, è il tema del [Capitolo 13](13-eccezioni.md); qui conta l'idea: un errore di utilizzo **si segnala**, non si nasconde dietro una stampa.

### 12.3.4 La lista generica

La lista che abbiamo scritto contiene solo `String`. Per avere una lista di interi, una di `Attivita` e una di qualsiasi altro tipo non vogliamo copiare la classe tre volte, e qui ritornano i generics. La trasformazione è meccanica: si sostituisce `String` con un parametro di tipo (`E`, come *element*) dichiarato nell'intestazione, e le sue occorrenze nel codice diventano `E`. Le slide chiamano questa classe `LinkedList<E>`; noi la chiamiamo `ListaCollegata<E>` per non confonderla con la `LinkedList` della libreria.

```java
class ListaCollegata<E> {

    private class Nodo {                        // classe interna: può usare E dell'esterna
        private E dato;
        private Nodo successivo;

        Nodo(E dato, Nodo successivo) {
            this.dato = dato;
            this.successivo = successivo;
        }
    }

    private Nodo testa;

    public void aggiungiInTesta(E e) {
        testa = new Nodo(e, testa);
    }

    public void aggiungiInCoda(E e) {
        Nodo nuovo = new Nodo(e, null);
        if (testa == null) {
            testa = nuovo;
            return;
        }
        Nodo corrente = testa;
        while (corrente.successivo != null) {
            corrente = corrente.successivo;
        }
        corrente.successivo = nuovo;
    }

    public int dimensione() {
        int n = 0;
        for (Nodo c = testa; c != null; c = c.successivo) {
            n++;
        }
        return n;
    }

    public String toString() {
        String r = "[";
        for (Nodo c = testa; c != null; c = c.successivo) {
            r += c.dato;                        // la stringa di c.dato è quella del suo toString
            if (c.successivo != null) {
                r += ", ";
            }
        }
        return r + "]";
    }
}

public class ProvaListaGenerica {
    public static void main(String[] args) {
        ListaCollegata<String> parole = new ListaCollegata<>();
        parole.aggiungiInCoda("uno");
        parole.aggiungiInCoda("due");
        parole.aggiungiInTesta("zero");

        ListaCollegata<Integer> numeri = new ListaCollegata<>();
        numeri.aggiungiInCoda(10);
        numeri.aggiungiInCoda(20);

        System.out.println(parole + " " + parole.dimensione());
        System.out.println(numeri + " " + numeri.dimensione());
    }
}
```

```text
[zero, uno, due] 3
[10, 20] 2
```

Confrontiamo con la versione per `String`. Dove c'era `String` ora c'è `E`: nel campo `dato`, nel parametro del costruttore del nodo, nei metodi che ricevono un dato. L'intestazione `class ListaCollegata<E>` dichiara il parametro. La classe interna `Nodo` non ha un proprio `<E>`: essendo una classe **interna** (non statica), vive dentro un oggetto `ListaCollegata<E>` e usa direttamente il suo `E`. Chi la usa scrive `ListaCollegata<String>` o `ListaCollegata<Integer>`, e il compilatore controlla che nella lista entrino solo dati di quel tipo. Come per `ArrayList`, il parametro è un tipo-classe: `ListaCollegata<int>` non compila.

Le due caratteristiche del §12.2.2 valgono anche qui: dentro la lista non si può scrivere `new E()` né `new E[10]`.

## 12.4 Gli iteratori

### 12.4.1 Il problema: come percorrere una collezione

Per percorrere un array abbiamo una variabile intera che indica la **posizione**: l'indice `i`. Per percorrere una lista concatenata l'indice non basta, perché non esiste un accesso diretto alla posizione `i`: l'unico modo di avanzare è seguire un collegamento. Nel codice di prima il ruolo dell'indice lo faceva la variabile `corrente`, un riferimento a un nodo che avanza. Ma `corrente` è un tipo di dato **interno** della lista (`Nodo`, privato): chi usa la lista dall'esterno non può averlo in mano, e non dovrebbe.

Serve quindi un oggetto che rappresenti "una posizione dentro la collezione", con operazioni per avanzare e per leggere l'elemento corrente, senza far vedere come la collezione è fatta dentro. Questo oggetto è l'**iteratore** (*iterator*).

### 12.4.2 L'interfaccia `Iterator` e il for-each

Java formalizza l'idea con un'interfaccia del package `java.util`, `Iterator<E>`, con tre metodi:

- `boolean hasNext()`: dice se ci sono ancora elementi da restituire;
- `E next()`: restituisce l'elemento successivo e avanza;
- `void remove()`: toglie dalla collezione l'ultimo elemento restituito da `next()`.

Ogni collezione della libreria ha un metodo `iterator()` che restituisce un `Iterator` posizionato **prima del primo elemento**. Il ciclo di scansione ha sempre la stessa forma: finché `hasNext()` è vero si chiama `next()`.

```java
import java.util.ArrayList;
import java.util.Iterator;

public class ScansioneConIteratore {
    public static void main(String[] args) {
        ArrayList<String> colori = new ArrayList<>();
        colori.add("rosso");
        colori.add("verde");
        colori.add("blu");

        Iterator<String> it = colori.iterator();    // posizionato prima del primo
        while (it.hasNext()) {
            String c = it.next();                   // restituisce l'elemento e avanza
            System.out.println(c);
        }
    }
}
```

```text
rosso
verde
blu
```

C'è un legame importante con il for-each che usiamo da tempo. Il `for-each` non è una sintassi riservata alle liste e agli array: funziona su **qualunque oggetto che realizzi l'interfaccia `Iterable<T>`**, che ha un solo metodo da scrivere, `Iterator<T> iterator()`. Il compilatore riscrive `for (String c : colori) { ... }` nel `while` con `hasNext` e `next` mostrato sopra. Tutte le collezioni della libreria sono `Iterable`, e lo possiamo essere anche noi (§12.4.3).

> [!NOTE]
> **Approfondimento esterno — `Iterator<E>` e `Iterable<T>`**
> Nella Javadoc di Java 17, `Iterator<E>` (package `java.util`) dichiara `boolean hasNext()` ("true se l'iterazione ha altri elementi"), `E next()` (restituisce l'elemento successivo, e lancia `NoSuchElementException` "se l'iterazione non ha altri elementi") e `default void remove()`, che "rimuove dalla collezione sottostante l'ultimo elemento restituito da questo iteratore (operazione opzionale)" e "può essere chiamato una sola volta per ogni chiamata di `next()`". L'implementazione di default di `remove` lancia `UnsupportedOperationException`; un iteratore che la supporta la ridefinisce, e lancia `IllegalStateException` se `next` non è ancora stato chiamato o se `remove` è già stato chiamato dopo l'ultimo `next`. Il comportamento è *unspecified* se la collezione viene modificata durante l'iterazione in modo diverso dal `remove` dell'iteratore. `Iterable<T>` (package `java.lang`) è l'interfaccia che, "se realizzata, permette a un oggetto di essere il bersaglio dell'istruzione *enhanced for*"; il suo metodo astratto è `Iterator<T> iterator()`.
>
> *Fonte:* [java.util.Iterator](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Iterator.html), [java.lang.Iterable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Iterable.html)

### 12.4.3 Un iteratore per la nostra lista

Per far funzionare la `ListaCollegata<E>` con il for-each, dichiariamo che realizza `Iterable<E>` e scriviamo `iterator()`. L'iteratore è un oggetto di una classe che realizza `Iterator<E>`, e conviene farne una **classe interna privata** della lista (Capitolo 11): così vede `testa` e i nodi per nome e nessun altro li vede. Lo stato dell'iteratore è la sua posizione, cioè `prossimo`, il nodo che `next()` restituirà.

Per realizzare anche `remove()` serve un dettaglio in più, lo stesso di `rimuovi` in §12.3.2: per togliere un nodo bisogna intervenire sul precedente. L'iteratore tiene perciò tre riferimenti: `prossimo` (il nodo da restituire), `ultimo` (quello restituito dall'ultimo `next`, che `remove` toglierebbe) e `prima` (il nodo che precede `ultimo`, oppure `null` se `ultimo` è la testa).

```java
import java.util.Iterator;
import java.util.NoSuchElementException;

class ListaCollegata<E> implements Iterable<E> {

    private class Nodo {
        private E dato;
        private Nodo successivo;

        Nodo(E dato, Nodo successivo) {
            this.dato = dato;
            this.successivo = successivo;
        }
    }

    private Nodo testa;

    public void aggiungiInTesta(E e) {
        testa = new Nodo(e, testa);
    }

    public void aggiungiInCoda(E e) {
        Nodo nuovo = new Nodo(e, null);
        if (testa == null) {
            testa = nuovo;
            return;
        }
        Nodo corrente = testa;
        while (corrente.successivo != null) {
            corrente = corrente.successivo;
        }
        corrente.successivo = nuovo;
    }

    public Iterator<E> iterator() {
        return new IteratoreLista();                  // un nuovo iteratore, posizionato sulla testa
    }

    private class IteratoreLista implements Iterator<E> {
        private Nodo prossimo = testa;                // il nodo che next() restituirà
        private Nodo ultimo = null;                   // l'ultimo nodo restituito da next()
        private Nodo prima = null;                    // il nodo che precede "ultimo" (null: ultimo è la testa)
        private boolean puoRimuovere = false;         // true solo dopo un next() non ancora "pagato" da un remove()

        public boolean hasNext() {
            return prossimo != null;
        }

        public E next() {
            if (prossimo == null) {
                throw new NoSuchElementException();
            }
            if (puoRimuovere) {
                prima = ultimo;                       // l'ultimo restituito resta in lista: diventa il precedente
            }
            ultimo = prossimo;
            prossimo = prossimo.successivo;
            puoRimuovere = true;
            return ultimo.dato;
        }

        public void remove() {
            if (!puoRimuovere) {
                throw new IllegalStateException();    // nessun next() da annullare
            }
            if (prima == null) {
                testa = ultimo.successivo;            // si toglie il primo nodo
            } else {
                prima.successivo = ultimo.successivo; // il precedente scavalca il nodo
            }
            puoRimuovere = false;                     // un solo remove() per ogni next()
        }
    }
}

public class ProvaIteratore {
    public static void main(String[] args) {
        ListaCollegata<Integer> numeri = new ListaCollegata<>();
        for (int i = 1; i <= 6; i++) {
            numeri.aggiungiInCoda(i);
        }

        for (int n : numeri) {                        // for-each: funziona perché la lista è Iterable
            System.out.print(n + " ");
        }
        System.out.println();

        Iterator<Integer> it = numeri.iterator();
        while (it.hasNext()) {
            if (it.next() % 2 == 0) {
                it.remove();                          // toglie i numeri pari mentre si scorre
            }
        }

        for (int n : numeri) {
            System.out.print(n + " ");
        }
        System.out.println();
    }
}
```

```text
1 2 3 4 5 6 
1 3 5 
```

Vediamo i punti chiave.

- `class ListaCollegata<E> implements Iterable<E>` e il metodo `iterator()` bastano a rendere la lista utilizzabile nel for-each, nella forma `for (int n : numeri)`. Ogni chiamata di `iterator()` crea un **nuovo** `IteratoreLista`, che parte dalla testa: due scansioni indipendenti non si disturbano.
- `IteratoreLista` è una classe interna **non statica** e privata. Il campo `prossimo = testa` ha come valore iniziale la testa della lista che l'ha creato: è la stessa regola della classe interna del Capitolo 11 (ogni iteratore appartiene a un oggetto esterno).
- Il metodo `next()` verifica la fine (`prossimo == null` significa che non c'è nulla da restituire: eccezione `NoSuchElementException`, come dice la documentazione), poi fa avanzare le tre posizioni. La riga `if (puoRimuovere) prima = ultimo;` è la più sottile: se l'elemento restituito dall'ultimo `next` è ancora in lista, diventa il precedente del prossimo; se invece è stato appena rimosso con `remove()`, il precedente resta quello di prima.
- `remove()` fa la stessa cosa di `rimuovi` in §12.3.2, ma sul nodo `ultimo`. Chiamarlo prima di un `next()`, o due volte di seguito, lancia `IllegalStateException`, come prescrive la documentazione.
- Nel `main` si eliminano i numeri pari **durante** la scansione: è proprio il caso d'uso di `remove()` e il motivo per cui esiste.

> [!TIP]
> **Intuizione — L'iteratore è un segnalibro**
> Una collezione è un libro; l'iteratore è un segnalibro. `next()` legge la pagina successiva e sposta il segnalibro; `hasNext()` chiede se ci sono ancora pagine; `remove()` strappa l'ultima pagina letta. Si possono avere più segnalibri nello stesso libro (più iteratori indipendenti). L'analogia ha un limite: se qualcuno strappa pagine o ne aggiunge senza passare dal nostro segnalibro, il segnalibro perde il senso. È il problema della sezione seguente.

Le slide presentano una variante in cui l'iteratore è anche in grado di **inserire** un nodo dopo la posizione corrente (`insertAfterIterator`). L'idea è la stessa di `remove`: per inserire dopo un nodo basta cambiare il collegamento di quel nodo, che l'iteratore ha in mano. La libreria offre questa possibilità nell'interfaccia `ListIterator`, che qui non approfondiamo.

### 12.4.4 Modificare una collezione mentre la si percorre

Che cosa succede se, durante un for-each su un `ArrayList`, si toglie un elemento con `lista.remove(...)` invece che con `it.remove()`? L'iteratore non lo sa: la sua idea di "elemento successivo" è ormai sbagliata. Gli iteratori della libreria si accorgono dell'inconsistenza e **lo segnalano subito** con un'eccezione, `ConcurrentModificationException`. Si dicono *fail-fast*, "che falliscono in fretta".

```java
import java.util.ArrayList;

public class ModificaDuranteLaScansione {
    public static void main(String[] args) {
        ArrayList<String> nomi = new ArrayList<>();
        nomi.add("Anna");
        nomi.add("Luca");
        nomi.add("Sara");

        for (String n : nomi) {
            System.out.println(n);
            if (n.equals("Anna")) {
                nomi.remove(n);              // modifica la lista senza passare dall'iteratore
            }
        }
    }
}
```

```text
Anna
```

Il programma stampa `Anna`, poi alla chiamata di `next()` del giro successivo l'iteratore si accorge che la lista è stata modificata e il programma termina con `Exception in thread "main" java.util.ConcurrentModificationException`. La forma corretta per togliere elementi durante una scansione è la `remove()` **dell'iteratore**.

```java
import java.util.ArrayList;
import java.util.Iterator;

public class RimozioneSicura {
    public static void main(String[] args) {
        ArrayList<String> nomi = new ArrayList<>();
        nomi.add("Anna");
        nomi.add("Luca");
        nomi.add("Sara");

        Iterator<String> it = nomi.iterator();
        while (it.hasNext()) {
            String n = it.next();
            if (n.startsWith("L")) {
                it.remove();                 // rimozione attraverso l'iteratore: lecita
            }
        }
        System.out.println(nomi);
    }
}
```

```text
[Anna, Sara]
```

> [!NOTE]
> **Approfondimento esterno — Iteratori *fail-fast***
> La Javadoc di `ArrayList` dice che "gli iteratori restituiti dai metodi `iterator` e `listIterator` sono *fail-fast*: se la lista viene modificata strutturalmente in qualsiasi momento dopo la creazione dell'iteratore, in qualsiasi modo tranne che attraverso i metodi `remove` o `add` dell'iteratore stesso, l'iteratore lancerà una `ConcurrentModificationException`". Una *modifica strutturale* è "qualunque operazione che aggiunge o elimina uno o più elementi"; cambiare il valore di un elemento con `set` non lo è. Il comportamento *fail-fast* non è garantito in ogni caso: la documentazione lo definisce "*best-effort*". Non si deve quindi costruire un programma che dipenda da questa eccezione per essere corretto: serve solo a scoprire gli errori.
>
> *Fonte:* [java.util.ArrayList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/ArrayList.html), [java.util.ConcurrentModificationException](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/ConcurrentModificationException.html)

## 12.5 Altre strutture collegate: la pila e l'albero

Lo schema del nodo con un riferimento a un altro nodo si presta a strutture più ricche di una semplice sequenza. Le slide ne citano due, e ne diamo qui l'idea essenziale.

### 12.5.1 La pila

Una **pila** (*stack*) è una struttura in cui gli elementi si tolgono **nell'ordine inverso** a quello di inserimento: l'ultimo a entrare è il primo a uscire (*LIFO*, *last in first out*). È come una pila di piatti: si aggiunge e si prende sempre dalla cima. Le operazioni tradizionali si chiamano `push` (inserisci in cima) e `pop` (togli dalla cima e restituiscilo).

Una pila si realizza benissimo con una lista concatenata, perché la cima è la testa della catena e inserire o togliere in testa sono le due operazioni economiche.

```java
import java.util.NoSuchElementException;

class Pila<E> {

    private class Nodo {
        private E dato;
        private Nodo sotto;

        Nodo(E dato, Nodo sotto) {
            this.dato = dato;
            this.sotto = sotto;
        }
    }

    private Nodo cima;

    public void push(E e) {
        cima = new Nodo(e, cima);                 // il nuovo nodo sta sopra il vecchio
    }

    public E pop() {
        if (cima == null) {
            throw new NoSuchElementException("pila vuota");
        }
        E e = cima.dato;
        cima = cima.sotto;
        return e;
    }

    public boolean isEmpty() {
        return cima == null;
    }
}

public class ProvaPila {
    public static void main(String[] args) {
        Pila<String> p = new Pila<>();
        p.push("primo");
        p.push("secondo");
        p.push("terzo");

        while (!p.isEmpty()) {
            System.out.println(p.pop());
        }
    }
}
```

```text
terzo
secondo
primo
```

Gli elementi escono nell'ordine inverso. Notiamo che `push` è esattamente `aggiungiInTesta` e `pop` è `eliminaTesta`: cambia solo il nome, che riflette l'uso.

### 12.5.2 L'albero binario

In un **albero** ogni nodo può condurre a **più** altri nodi invece che a uno solo. In un **albero binario** ogni nodo ne ha al più due, tradizionalmente chiamati figlio sinistro e figlio destro. La struttura parte da un nodo, la **radice**, e i nodi senza figli si chiamano **foglie**. Il nodo ha tre campi: il dato e due riferimenti.

```text
        10
       /  \
      5    20
     /
    3
```

```java
class NodoAlbero {
    int valore;
    NodoAlbero sinistro;
    NodoAlbero destro;

    NodoAlbero(int valore) {
        this.valore = valore;
    }
}

public class ProvaAlbero {

    static int conta(NodoAlbero n) {
        if (n == null) {
            return 0;                                    // caso base: albero vuoto
        }
        return 1 + conta(n.sinistro) + conta(n.destro);  // questo nodo, più i due sottoalberi
    }

    public static void main(String[] args) {
        NodoAlbero radice = new NodoAlbero(10);
        radice.sinistro = new NodoAlbero(5);
        radice.destro = new NodoAlbero(20);
        radice.sinistro.sinistro = new NodoAlbero(3);

        System.out.println(conta(radice));
    }
}
```

```text
4
```

Il metodo `conta` usa la **ricorsione** del [Capitolo 6](06-metodi.md), sezione 6.9, e rispecchia la definizione dell'albero: un albero è vuoto oppure è un nodo con due alberi più piccoli. I campi qui non sono `private` per brevità; in una classe vera si nasconderebbe il nodo, come nella lista. Gli alberi ordinati e le loro operazioni non sono trattati qui.

## 12.6 Le collezioni della libreria

Con `ArrayList` e con la lista scritta a mano abbiamo visto due modi di rappresentare una sequenza. La libreria standard di Java, nel package `java.util`, ne organizza molti altri in un unico insieme coerente, il **Java Collections Framework**. Non serve conoscerlo tutto: bastano le interfacce `List`, `Set` e `Map` e le loro implementazioni più usate. Le diamo qui come riferimento per le prove scritte, con le firme verificate sulla documentazione ufficiale.

### 12.6.1 La mappa dei tipi: interfacce e implementazioni

Il framework separa **che cosa** una collezione sa fare (un'*interfaccia*) da **come** lo fa (una *classe* che la realizza), esattamente come visto nel [Capitolo 10](10-classi-astratte-e-interfacce.md). Le interfacce principali sono tre.

- **`List<E>`**: una sequenza ordinata, con accesso per posizione, che ammette duplicati. Implementazioni: `ArrayList`, `LinkedList`.
- **`Set<E>`**: un insieme di elementi **senza duplicati** (due elementi `a` e `b` con `a.equals(b)` non possono coesistere). Implementazioni: `HashSet`, `TreeSet`.
- **`Map<K,V>`**: una raccolta di coppie **chiave → valore**, in cui ogni chiave compare una volta sola. Implementazioni: `HashMap`, `TreeMap`.

`List` e `Set` condividono un'interfaccia più generale, `Collection<E>`, che raccoglie le operazioni comuni (`add`, `remove`, `contains`, `size`, `isEmpty`, `clear`, `iterator`) ed estende `Iterable<E>`: per questo ogni lista e ogni insieme si può percorrere con il for-each. `Map` invece sta da sola, perché ha due parametri di tipo. Lo schema, semplificato:

```text
Iterable<E>
    |
Collection<E>                                   Map<K,V>
    |                                              |
    +--- List<E>  : ArrayList, LinkedList          +--- HashMap, TreeMap
    |
    +--- Set<E>   : HashSet, TreeSet
```

> [!NOTE]
> **Approfondimento esterno — `Collection`, `List`, `Set`, `Map`**
> Secondo la Javadoc di Java 17, `Collection<E>` è "l'interfaccia radice della gerarchia delle collezioni": rappresenta "un gruppo di oggetti, detti elementi"; alcune collezioni ammettono duplicati e altre no, alcune sono ordinate e altre no. Il JDK non fornisce implementazioni dirette di `Collection`, ma di sottointerfacce più specifiche come `Set` e `List`. `List<E>` è "una collezione ordinata (detta anche sequenza)", in cui "l'utente ha un controllo preciso su dove ogni elemento viene inserito", può accedere agli elementi per indice, e che "di norma ammette duplicati". `Set<E>` è "una collezione che non contiene elementi duplicati", cioè nessuna coppia `e1`, `e2` con `e1.equals(e2)`. `Map<K,V>` è "un oggetto che associa chiavi a valori": "una mappa non può contenere chiavi duplicate; ogni chiave può corrispondere al massimo a un valore".
>
> *Fonte:* [java.util.Collection](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Collection.html), [java.util.List](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/List.html), [java.util.Set](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Set.html), [java.util.Map](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Map.html)

Un'abitudine utile, che deriva dal polimorfismo del [Capitolo 9](09-ereditarieta-e-polimorfismo.md): **dichiarare la variabile con il tipo dell'interfaccia** e creare l'oggetto con la classe concreta. Scrivere `List<String> l = new ArrayList<>();` invece di `ArrayList<String> l = new ArrayList<>();` rende il resto del codice indipendente dall'implementazione scelta: per passare a `LinkedList` basta cambiare la parola dopo `new`. Lo stesso vale per i parametri dei metodi.

```java
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class SommaDiUnaLista {

    static int somma(List<Integer> numeri) {         // accetta qualunque List<Integer>
        int totale = 0;
        for (int n : numeri) {
            totale += n;
        }
        return totale;
    }

    public static void main(String[] args) {
        List<Integer> a = new ArrayList<>();
        List<Integer> b = new LinkedList<>();
        for (int i = 1; i <= 4; i++) {
            a.add(i);
            b.add(i * 10);
        }
        System.out.println(somma(a) + " " + somma(b));
    }
}
```

```text
10 100
```

Il metodo `somma` non sa e non gli interessa se riceve un `ArrayList` o una `LinkedList`: gli basta che sia una `List<Integer>`. I metodi della tabella di §12.1.3 sono quelli dell'interfaccia `List`, quindi valgono per entrambe.

### 12.6.2 `LinkedList`

La classe `LinkedList<E>` del package `java.util` è la lista concatenata già pronta. A differenza di quella che abbiamo scritto, i suoi nodi hanno due collegamenti (avanti e indietro: è una lista *doppiamente concatenata*), e realizza **due** interfacce: `List<E>` e `Deque<E>`, una coda a doppia entrata. Quindi ha tutti i metodi di `List` (`add`, `get`, `remove`, `size`...), più quelli per lavorare agli estremi.

| Voglio | Scrivo | Se la lista è vuota |
|---|---|---|
| inserire in testa | `l.addFirst(x)` | — |
| inserire in coda | `l.addLast(x)` | — |
| leggere il primo | `l.getFirst()` | `NoSuchElementException` |
| leggere l'ultimo | `l.getLast()` | `NoSuchElementException` |
| togliere e restituire il primo | `l.removeFirst()` | `NoSuchElementException` |
| togliere e restituire l'ultimo | `l.removeLast()` | `NoSuchElementException` |
| leggere il primo senza lanciare | `l.peek()` | `null` |
| togliere il primo senza lanciare | `l.poll()` | `null` |
| comportarsi da pila | `l.push(x)` / `l.pop()` | `pop`: `NoSuchElementException` |

`push` equivale a `addFirst` e `pop` a `removeFirst`: sono i nomi della pila di §12.5.1. Con `add` in coda e `poll` o `removeFirst` in testa la stessa classe si comporta da **coda** (*queue*): il primo a entrare è il primo a uscire (*FIFO*).

```java
import java.util.LinkedList;

public class ProvaLinkedList {
    public static void main(String[] args) {
        LinkedList<String> l = new LinkedList<>();
        l.add("b");                          // in coda: [b]
        l.addFirst("a");                     // in testa: [a, b]
        l.addLast("c");                      // in coda: [a, b, c]
        System.out.println(l + " " + l.getFirst() + " " + l.getLast());

        System.out.println(l.removeFirst());  // a
        System.out.println(l);

        l.push("z");                         // come addFirst
        System.out.println(l.pop() + " " + l);  // come removeFirst

        LinkedList<String> vuota = new LinkedList<>();
        System.out.println(vuota.poll());    // null, nessuna eccezione
    }
}
```

```text
[a, b, c] a c
a
[b, c]
z [b, c]
null
```

Nell'ultima riga `poll` su una lista vuota restituisce `null` invece di lanciare: lo stesso errore è segnalato con un'eccezione da `removeFirst`, con un valore speciale da `poll`. Quale forma usare dipende da chi chiama: se la lista vuota è un caso previsto, `poll`; se è un errore, `removeFirst`.

> [!NOTE]
> **Approfondimento esterno — `java.util.LinkedList`**
> La Javadoc di Java 17 la descrive come "implementazione di lista doppiamente concatenata delle interfacce `List` e `Deque`", che implementa tutte le operazioni opzionali di lista e permette tutti gli elementi, compreso `null`. Le operazioni che usano un indice "attraversano la lista dall'inizio o dalla fine, a seconda di quale sia più vicina all'indice". Come `ArrayList`, non è sincronizzata. Firme verificate: `public void addFirst(E e)`, `public void addLast(E e)`, `public E getFirst()` e `public E removeFirst()` (entrambi lanciano `NoSuchElementException` "se la lista è vuota"), `public E peek()` e `public E poll()` (restituiscono `null` se la lista è vuota), `public void push(E e)` e `public E pop()`.
>
> *Fonte:* [java.util.LinkedList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/LinkedList.html)

Come scegliere tra `ArrayList` e `LinkedList`: come per le strutture di §12.3.1, l'`ArrayList` è più comoda quando serve leggere per posizione (`get(i)` è immediato) e si aggiunge soprattutto in fondo; la `LinkedList` è più comoda quando si inserisce e si toglie spesso agli estremi. Nelle prove scritte la scelta quasi sempre non conta per il risultato, e l'`ArrayList` è la scelta di partenza.

### 12.6.3 Gli insiemi: `Set`, `HashSet`, `TreeSet`

Un **insieme** (`Set<E>`) non contiene mai due elementi uguali. Il metodo `add` lo garantisce: se l'elemento è già presente la collezione non cambia e `add` restituisce `false`; se è nuovo, lo aggiunge e restituisce `true`. L'uguaglianza è quella di `equals`, non di `==`.

Un insieme non ha posizioni: non esistono `get(i)` né `set(i, x)`. Si può chiedere se contiene un elemento (`contains`), togliere un elemento (`remove(x)`), contare (`size`), percorrere (for-each).

Le due implementazioni principali si distinguono per l'**ordine** in cui restituiscono gli elementi.

- **`HashSet<E>`** non garantisce nessun ordine, e l'ordine può cambiare nel tempo. In cambio `add`, `remove` e `contains` sono molto rapide. È la scelta di partenza quando conta solo l'appartenenza.
- **`TreeSet<E>`** mantiene gli elementi **in ordine crescente**, secondo l'ordine naturale (`Comparable`, [Capitolo 10](10-classi-astratte-e-interfacce.md), sezione 10.4) oppure secondo un `Comparator` dato alla creazione (§12.6.5). Le operazioni sono un po' più lente.

```java
import java.util.HashSet;
import java.util.TreeSet;

public class ProvaInsiemi {
    public static void main(String[] args) {
        HashSet<String> parole = new HashSet<>();
        System.out.println(parole.add("sole"));       // true: nuovo
        System.out.println(parole.add("luna"));       // true: nuovo
        System.out.println(parole.add("sole"));       // false: c'è già

        System.out.println(parole.size());
        System.out.println(parole.contains("luna"));
        parole.remove("luna");
        System.out.println(parole.contains("luna"));

        parole.add("stella");
        parole.add("alba");
        TreeSet<String> ordinate = new TreeSet<>(parole);   // copia ordinata
        System.out.println(ordinate);
    }
}
```

```text
true
true
false
2
true
false
[alba, sole, stella]
```

La seconda `add("sole")` restituisce `false` e l'insieme ha ancora due elementi. Dopo aver tolto `"luna"` e aggiunto `"stella"` e `"alba"` l'insieme contiene `sole`, `stella`, `alba`; non stampiamo l'`HashSet` direttamente perché l'ordine non è definito, ma lo copiamo in un `TreeSet` con il costruttore `TreeSet(Collection)`, che lo restituisce in ordine alfabetico. Questo è l'uso classico del `TreeSet`: eliminare i duplicati e ordinare in un colpo solo.

> [!NOTE]
> **Approfondimento esterno — `Set`, `HashSet`, `TreeSet`**
> La Javadoc di Java 17 dice che `HashSet` è "retto da una tabella hash (in realtà un'istanza di `HashMap`)", "non dà garanzie sull'ordine di iterazione" e offre tempo costante per `add`, `remove`, `contains` e `size`. `TreeSet` è basato su una `TreeMap`; gli elementi sono ordinati "secondo il loro ordinamento naturale, oppure secondo un `Comparator` fornito alla creazione, a seconda del costruttore usato", con costo logaritmico per le operazioni di base. `boolean add(E e)` "aggiunge l'elemento se non è già presente [...]; se l'insieme contiene già l'elemento, la chiamata lascia l'insieme invariato e restituisce `false`", dove la presenza si controlla con `Objects.equals`. Nel `TreeSet` gli elementi devono essere "mutuamente confrontabili": `add` di un elemento non confrontabile lancia `ClassCastException`. Una avvertenza generale di `Set`: "occorre grande attenzione se si usano come elementi oggetti modificabili", perché il comportamento non è specificato se un elemento cambia in modo che influisca su `equals` mentre è nell'insieme.
>
> *Fonte:* [java.util.HashSet](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/HashSet.html), [java.util.TreeSet](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/TreeSet.html), [java.util.Set](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Set.html)

#### Gli insiemi di oggetti nostri: `equals` e `hashCode`

Con `String` e con i wrapper l'insieme funziona subito perché quelle classi hanno già un `equals` sul contenuto. Con una classe nostra **non** funziona, a meno di averlo scritto: per due oggetti con gli stessi campi, `equals` ereditato da `Object` dice "diversi" (Capitolo 8, sezione 8.4). Inoltre `HashSet` (e `HashMap`) usa anche `hashCode()` per decidere in che "scomparto" cercare l'elemento, e perciò **vanno riscritti insieme** `equals` e `hashCode`, come visto nel [Capitolo 9](09-ereditarieta-e-polimorfismo.md), sezione 9.7.4. Verifichiamo la differenza.

```java
import java.util.HashSet;
import java.util.Objects;

class PuntoSenza {
    private int x;
    private int y;

    public PuntoSenza(int x, int y) {
        this.x = x;
        this.y = y;
    }
}

class PuntoCompleto {
    private int x;
    private int y;

    public PuntoCompleto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        PuntoCompleto altro = (PuntoCompleto) o;
        return x == altro.x && y == altro.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);               // gli stessi campi di equals
    }
}

public class InsiemeDiOggetti {
    public static void main(String[] args) {
        HashSet<PuntoSenza> a = new HashSet<>();
        a.add(new PuntoSenza(1, 2));
        a.add(new PuntoSenza(1, 2));             // stesso contenuto, ma per Object è un altro oggetto
        System.out.println(a.size());

        HashSet<PuntoCompleto> b = new HashSet<>();
        b.add(new PuntoCompleto(1, 2));
        b.add(new PuntoCompleto(1, 2));
        System.out.println(b.size());
        System.out.println(b.contains(new PuntoCompleto(1, 2)));
    }
}
```

```text
2
1
true
```

Con `PuntoSenza` l'insieme tiene i due "punti uguali" come elementi distinti. Con `PuntoCompleto`, che riscrive `equals` e `hashCode` sugli stessi campi, la seconda `add` è riconosciuta come duplicato e anche una ricerca con un oggetto *nuovo* ma uguale (`contains(new PuntoCompleto(1, 2))`) lo trova.

### 12.6.4 Le mappe: `Map`, `HashMap`, `TreeMap`

Una **mappa** associa a ogni **chiave** un **valore**: come una rubrica, in cui il nome (la chiave) permette di trovare il numero (il valore). Le chiavi sono tutte diverse tra loro; i valori possono ripetersi. Una mappa ha due parametri di tipo, `Map<K,V>`: il tipo delle chiavi e quello dei valori. Le implementazioni principali sono `HashMap` (nessun ordine, molto rapida) e `TreeMap` (chiavi sempre **ordinate**), con la stessa differenza dei due insiemi, che peraltro si appoggiano internamente alle mappe.

I metodi da conoscere a memoria, con `Map<String, Integer> m`:

| Voglio | Scrivo | Note |
|---|---|---|
| inserire o sostituire | `m.put(chiave, valore)` | restituisce il **valore precedente** (o `null` se la chiave era nuova) |
| leggere un valore | `m.get(chiave)` | `null` se la chiave non c'è |
| leggere con un valore di ripiego | `m.getOrDefault(chiave, 0)` | se la chiave non c'è restituisce il secondo argomento |
| la chiave esiste? | `m.containsKey(chiave)` | |
| il valore esiste? | `m.containsValue(valore)` | confronta tutti i valori |
| togliere una coppia | `m.remove(chiave)` | restituisce il valore tolto, o `null` |
| quante coppie | `m.size()` | non `length` |
| è vuota? | `m.isEmpty()` | |
| tutte le chiavi | `m.keySet()` | un `Set<K>` |
| tutti i valori | `m.values()` | una `Collection<V>` |
| tutte le coppie | `m.entrySet()` | un `Set<Map.Entry<K,V>>` |

Per percorrere una mappa si percorre una di queste tre "viste". La più completa è `entrySet()`: ogni elemento è una **coppia** (di tipo `Map.Entry<K,V>`, un'interfaccia annidata dentro `Map`, [Capitolo 11](11-classi-annidate.md), sezione 11.4.4), da cui si leggono `getKey()` e `getValue()`.

#### Esempio — Contare le occorrenze

Un uso tipico: contare quante volte compare ciascuna parola. La chiave è la parola, il valore è il conteggio. Per ogni parola, se la chiave non c'è ancora si inserisce con valore 1; se c'è, si rimpiazza il valore con il valore precedente più uno.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

public class ContaParole {
    public static void main(String[] args) {
        String[] parole = {"sole", "luna", "sole", "stella", "luna", "sole"};

        Map<String, Integer> conteggio = new HashMap<>();
        for (String p : parole) {
            if (conteggio.containsKey(p)) {
                conteggio.put(p, conteggio.get(p) + 1);     // la chiave c'è: valore + 1
            } else {
                conteggio.put(p, 1);                        // prima occorrenza
            }
        }

        System.out.println(conteggio.get("sole"));          // 3
        System.out.println(conteggio.get("cometa"));        // null: la chiave non c'è
        System.out.println(conteggio.getOrDefault("cometa", 0));
        System.out.println(conteggio.size());

        TreeMap<String, Integer> ordinata = new TreeMap<>(conteggio);   // chiavi in ordine
        for (Map.Entry<String, Integer> e : ordinata.entrySet()) {
            System.out.println(e.getKey() + " -> " + e.getValue());
        }
    }
}
```

```text
3
null
0
3
luna -> 2
sole -> 3
stella -> 1
```

Seguiamo il programma. Il ciclo costruisce la mappa: la prima volta che compare `"sole"` si fa `put("sole", 1)`, la seconda `put("sole", 1 + 1)`, la terza `put("sole", 2 + 1)`. `conteggio.get("sole")` vale 3. `get("cometa")` restituisce `null`, perché la chiave non c'è, mentre `getOrDefault("cometa", 0)` evita il `null` e restituisce 0. Le chiavi sono tre, quindi `size()` vale 3. Per stampare le coppie in ordine copiamo la mappa in una `TreeMap` e la percorriamo con `entrySet()`: il tipo del ciclo è `Map.Entry<String, Integer>`, e `e.getKey()` e `e.getValue()` danno chiave e valore. Il `HashMap` non garantisce nessun ordine, quindi non si stampa direttamente se l'ordine conta.

Una forma più compatta dello stesso ciclo usa `getOrDefault`: `conteggio.put(p, conteggio.getOrDefault(p, 0) + 1);`.

Due trappole tipiche delle mappe.

- **`get` restituisce `null` per una chiave assente.** Se il valore è un `Integer` e lo si assegna a un `int` (`int n = m.get("assente");`) avviene un *unboxing* di `null` e si ottiene una `NullPointerException` (Capitolo 6, sezione 6.6.3). Si usa `getOrDefault`, oppure si controlla prima con `containsKey`.
- **`getValue` non è un metodo di `Map`.** Appartiene a `Map.Entry`, cioè alla coppia ottenuta da `entrySet()`. Sulla mappa si scrive `m.get(chiave)`.

#### Esempio — Una rubrica

Qui la mappa associa un nome a un numero di telefono, e mostra come `put` su una chiave già presente **sostituisce** il valore e restituisce quello vecchio.

```java
import java.util.HashMap;
import java.util.Map;

public class Rubrica {
    public static void main(String[] args) {
        Map<String, String> telefono = new HashMap<>();
        telefono.put("Anna", "333111");
        telefono.put("Luca", "333222");

        String vecchio = telefono.put("Anna", "333999");   // chiave già presente: sostituisce
        System.out.println(vecchio);
        System.out.println(telefono.get("Anna"));

        System.out.println(telefono.remove("Luca"));       // restituisce il valore tolto
        System.out.println(telefono.containsKey("Luca"));
        System.out.println(telefono.size());
    }
}
```

```text
333111
333999
333222
false
1
```

> [!NOTE]
> **Approfondimento esterno — `Map`, `HashMap`, `TreeMap`, `Map.Entry`**
> Nella Javadoc di Java 17 le firme sono: `V put(K key, V value)` ("associa il valore alla chiave; se la mappa conteneva già una mappatura per la chiave, il vecchio valore viene sostituito", e restituisce "il valore precedentemente associato a `key`, oppure `null` se non c'era una mappatura"); `V get(Object key)` ("il valore associato alla chiave, o `null` se la mappa non contiene una mappatura per la chiave"); `default V getOrDefault(Object key, V defaultValue)`; `boolean containsKey(Object key)`; `V remove(Object key)`; `Set<K> keySet()`; `Collection<V> values()`; `Set<Map.Entry<K,V>> entrySet()`. Le tre viste sono "sostenute dalla mappa": una modifica alla mappa si riflette sulla vista, e rimuovere dalla vista rimuove dalla mappa. `HashMap` è basata su tabella hash, "permette valori `null` e la chiave `null`" e "non dà garanzie sull'ordine della mappa"; `TreeMap` è basata su un albero rosso-nero e ordina le chiavi "secondo il loro ordinamento naturale, oppure secondo un `Comparator` fornito alla creazione". `Map.Entry<K,V>` dichiara `K getKey()` e `V getValue()`. Come per `Set`, la Javadoc avverte che modificare una chiave in modo che influisca su `equals` mentre è nella mappa dà un comportamento non specificato.
>
> *Fonte:* [java.util.Map](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Map.html), [java.util.HashMap](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/HashMap.html), [java.util.TreeMap](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/TreeMap.html), [java.util.Map.Entry](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Map.Entry.html)

Poiché `HashMap` e `HashSet` usano `hashCode` ed `equals` delle **chiavi** (o degli elementi), le classi nostre usate come chiavi richiedono le stesse due ridefinizioni di §12.6.3. Le chiavi `String`, `Integer` e simili le hanno già.

### 12.6.5 Ordinare: `Comparable`, `Comparator`, `Collections.sort`

Per mettere in ordine un array abbiamo usato `Arrays.sort` (Capitolo 5, sezione 5.6), e per far funzionare l'ordinamento di un array di oggetti nostri abbiamo realizzato `Comparable` (Capitolo 10, sezione 10.4). Per le liste lo strumento è `Collections.sort`, dove `Collections` (con la **s** finale) è una classe di metodi statici di utilità, diversa dall'interfaccia `Collection`.

`Collections.sort(lista)` ordina una lista secondo l'ordine **naturale** dei suoi elementi, quello definito dal loro `compareTo`: gli elementi devono quindi realizzare `Comparable`. È la stessa regola di `Arrays.sort`.

```java
import java.util.ArrayList;
import java.util.Collections;

class Pianeta implements Comparable<Pianeta> {
    private String nome;
    private int diametro;                    // in chilometri

    public Pianeta(String nome, int diametro) {
        this.nome = nome;
        this.diametro = diametro;
    }

    public String getNome() {
        return nome;
    }

    public int getDiametro() {
        return diametro;
    }

    public int compareTo(Pianeta altro) {
        return Integer.compare(diametro, altro.diametro);       // ordine naturale: per diametro crescente
    }

    public String toString() {
        return nome + " " + diametro;
    }
}

public class OrdineNaturale {
    public static void main(String[] args) {
        ArrayList<Pianeta> lista = new ArrayList<>();
        lista.add(new Pianeta("Giove", 139820));
        lista.add(new Pianeta("Marte", 6779));
        lista.add(new Pianeta("Terra", 12742));

        Collections.sort(lista);                                  // usa compareTo
        System.out.println(lista);

        Collections.reverse(lista);                               // inverte l'ordine
        System.out.println(lista);
    }
}
```

```text
[Marte 6779, Terra 12742, Giove 139820]
[Giove 139820, Terra 12742, Marte 6779]
```

Se la lista contiene oggetti di una classe **senza** `Comparable`, `Collections.sort(lista)` non compila. La firma lo spiega: `public static <T extends Comparable<? super T>> void sort(List<T> list)` si legge "per un qualunque tipo `T` che sia confrontabile, ordina una `List<T>`". Il `<T ...>` prima del `void` dichiara il parametro di tipo del *metodo*, come `<E>` lo dichiara per una classe; il vincolo `extends Comparable<? super T>` impone che `T` sappia confrontarsi. Il compilatore rifiuta quindi l'invocazione con un errore, che in pratica significa "questa classe non realizza `Comparable`".

Un solo ordine naturale per classe non basta sempre: lo stesso elenco di pianeti potrebbe servire in ordine alfabetico. Serve allora un oggetto che esprima un **criterio di confronto separato dalla classe**: un `Comparator<T>`. È un'interfaccia (package `java.util`) con un metodo da scrivere, `int compare(T o1, T o2)`, che deve restituire un numero negativo, zero o positivo secondo che `o1` sia minore, uguale o maggiore di `o2`. A differenza di `compareTo`, che confronta `this` con un altro oggetto, `compare` riceve **entrambi** gli oggetti.

Si può realizzare con una classe a parte, oppure con una classe anonima ([Capitolo 11](11-classi-annidate.md), sezione 11.5), e passare a `Collections.sort(lista, comparator)`.

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

class Pianeta {
    private String nome;
    private int diametro;

    public Pianeta(String nome, int diametro) {
        this.nome = nome;
        this.diametro = diametro;
    }

    public String getNome() {
        return nome;
    }

    public int getDiametro() {
        return diametro;
    }

    public String toString() {
        return nome + " " + diametro;
    }
}

class PerNome implements Comparator<Pianeta> {              // una classe a parte
    public int compare(Pianeta a, Pianeta b) {
        return a.getNome().compareTo(b.getNome());          // si delega al compareTo di String
    }
}

public class OrdineConComparator {
    public static void main(String[] args) {
        ArrayList<Pianeta> lista = new ArrayList<>();
        lista.add(new Pianeta("Giove", 139820));
        lista.add(new Pianeta("Marte", 6779));
        lista.add(new Pianeta("Terra", 12742));

        Collections.sort(lista, new PerNome());
        System.out.println(lista);

        Comparator<Pianeta> perDiametro = new Comparator<Pianeta>() {   // classe anonima
            public int compare(Pianeta a, Pianeta b) {
                return Integer.compare(a.getDiametro(), b.getDiametro());
            }
        };
        Collections.sort(lista, perDiametro);
        System.out.println(lista);

        lista.sort(new PerNome());                          // il metodo sort della lista: stesso effetto
        System.out.println(lista);
    }
}
```

```text
[Giove 139820, Marte 6779, Terra 12742]
[Marte 6779, Terra 12742, Giove 139820]
[Giove 139820, Marte 6779, Terra 12742]
```

La classe `Pianeta` qui non realizza `Comparable`: i due criteri stanno fuori dalla classe, in `PerNome` e nell'oggetto anonimo `perDiametro`. `PerNome` confronta i nomi con il `compareTo` di `String` (Capitolo 3, sezione 3.4). L'oggetto anonimo è creato con `new Comparator<Pianeta>() { ... }` e il suo `compare` usa `Integer.compare(int, int)`, che restituisce un numero negativo, zero o positivo come richiede `compare`. Infine `lista.sort(new PerNome())` fa lo stesso di `Collections.sort(lista, new PerNome())`: `sort` è un metodo dell'interfaccia `List`.

Non si scrive mai `return a.getDiametro() - b.getDiametro();` per i numeri: sembra comodo ma può dare un risultato sbagliato se la sottrazione va in overflow (due numeri molto grandi di segno opposto), e un `compare` sbagliato porta a un ordine scorretto senza nessun errore. `Integer.compare` e `Double.compare` evitano il problema.

Il `Comparator` si passa anche alle strutture che mantengono l'ordine da sole: `new TreeSet<>(comparator)` e `new TreeMap<>(comparator)`. Senza comparator, un `TreeSet` o una `TreeMap` usano l'ordine naturale e quindi richiedono `Comparable`; se gli elementi (o le chiavi) non lo sono, l'inserimento lancia `ClassCastException` a esecuzione.

> [!NOTE]
> **Approfondimento esterno — `Comparator` e `Collections.sort`**
> La Javadoc di Java 17 dichiara `public interface Comparator<T>` con il metodo `int compare(T o1, T o2)`, che "confronta i suoi due argomenti per l'ordine" e "restituisce un intero negativo, zero o positivo a seconda che il primo argomento sia minore, uguale o maggiore del secondo". Chi la realizza deve garantire `signum(compare(x, y)) == -signum(compare(y, x))` e la transitività. I comparator si possono passare "a un metodo di ordinamento (come `Collections.sort` o `Arrays.sort`)" e anche a insiemi e mappe ordinati. `Collections` dichiara `public static <T extends Comparable<? super T>> void sort(List<T> list)` ("ordina la lista in ordine crescente secondo l'ordinamento naturale degli elementi"; lancia `ClassCastException` se gli elementi non sono mutuamente confrontabili) e `public static <T> void sort(List<T> list, Comparator<? super T> c)`. Entrambe sono **stabili**: "gli elementi uguali non vengono riordinati". La lista deve essere modificabile. Anche `List` ha un metodo `default void sort(Comparator<? super E> c)`. Per invertire una lista, `public static void reverse(List<?> list)`.
>
> *Fonte:* [java.util.Comparator](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Comparator.html), [java.util.Collections](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Collections.html), [java.util.List](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/List.html)

### 12.6.6 Quale struttura scegliere

Quando la traccia dice "tieni traccia di", "raccogli", "associa", "senza duplicati", la scelta della struttura segue dal verbo.

| La traccia chiede | Struttura | Perché |
|---|---|---|
| un numero fisso e noto di elementi, anche primitivi | array | lunghezza fissa, nessun costo (Capitolo 5) |
| una sequenza che cresce, accesso per posizione | `ArrayList` | `get(i)` immediato, `add` in fondo |
| inserire e togliere spesso agli estremi, pila o coda | `LinkedList` | `addFirst`, `removeFirst`, `push`, `pop` |
| elementi **senza duplicati** | `HashSet` | `add` restituisce `false` se già presente |
| senza duplicati **e ordinati** | `TreeSet` | elementi sempre in ordine |
| associare un valore a una chiave, cercare per nome | `HashMap` | `put`, `get` |
| come sopra, chiavi **in ordine** | `TreeMap` | percorrere le chiavi in ordine |
| lista in un ordine diverso da quello di inserimento | `Collections.sort` | con `Comparable` o `Comparator` |

Tre domande permettono di decidere in pochi secondi. *Si accede per posizione?* Lista. *Importa l'unicità?* Insieme. *Si cerca per una chiave?* Mappa. Poi: *serve l'ordine?* Allora le versioni `Tree...`, oppure una lista ordinata con `Collections.sort`.

## Scheletri da esame

Nessun appello ufficiale ha assegnato le collezioni come tema dichiarato, ma sono lo strumento che sta dentro molti esercizi di API. Questi cinque frammenti sono quelli da saper scrivere a memoria su un editor senza aiuti.

### Una lista di oggetti: riempire, sommare, cercare, togliere

*Quando si usa:* la traccia chiede di tenere una raccolta di oggetti di lunghezza non nota, con operazioni di somma, ricerca per nome e rimozione secondo una condizione. Si veda la sezione 12.1 e la 12.4.4.

```java
import java.util.ArrayList;
import java.util.Iterator;

class Articolo {
    private String nome;
    private double prezzo;

    public Articolo(String nome, double prezzo) {
        this.nome = nome;
        this.prezzo = prezzo;
    }

    public String getNome() {
        return nome;
    }

    public double getPrezzo() {
        return prezzo;
    }

    public String toString() {
        return nome + " " + prezzo;
    }
}

public class SchemaLista {
    public static void main(String[] args) {
        ArrayList<Articolo> carrello = new ArrayList<>();      // tipo tra <>, import di java.util.ArrayList
        carrello.add(new Articolo("penna", 2.5));
        carrello.add(new Articolo("gomma", 0.5));
        carrello.add(new Articolo("quaderno", 4.0));

        double totale = 0;
        for (Articolo a : carrello) {                          // percorrere
            totale += a.getPrezzo();
        }
        System.out.println(totale);

        Articolo trovato = null;
        for (Articolo a : carrello) {                          // cercare per nome: equals, non ==
            if (a.getNome().equals("gomma")) {
                trovato = a;
            }
        }
        System.out.println(trovato);

        Iterator<Articolo> it = carrello.iterator();           // togliere durante la scansione
        while (it.hasNext()) {
            if (it.next().getPrezzo() < 1.0) {
                it.remove();                                   // remove dell'iteratore, mai della lista
            }
        }
        System.out.println(carrello + " " + carrello.size());
    }
}
```

```text
7.0
gomma 0.5
[penna 2.5, quaderno 4.0] 2
```

Import: `java.util.ArrayList`, `java.util.Iterator`. Nessuna eccezione da dichiarare. Punti da controllare: i nomi `add`, `get`, `size` (mai `[ ]`, `length`); il tipo tra `<>` è una classe (`Articolo`, `Integer`, mai `int`); i confronti tra stringhe con `equals`; per togliere durante un ciclo si usa l'iteratore.

### Una lista concatenata generica con nodo interno privato e iteratore

*Quando si usa:* la traccia chiede di realizzare una struttura concatenata, magari generica, percorribile con il for-each. Si vedano le sezioni 12.3 e 12.4.

```java
import java.util.Iterator;

class Catena<E> implements Iterable<E> {

    private class Nodo {                           // interna e privata: nessuno fuori vede i nodi
        private E dato;
        private Nodo successivo;

        Nodo(E dato, Nodo successivo) {
            this.dato = dato;
            this.successivo = successivo;
        }
    }

    private Nodo testa;                            // null = lista vuota

    public void aggiungiInTesta(E e) {
        testa = new Nodo(e, testa);                // il nuovo nodo punta al vecchio primo
    }

    public Iterator<E> iterator() {                // public: viene dall'interfaccia
        return new Iteratore();
    }

    private class Iteratore implements Iterator<E> {
        private Nodo prossimo = testa;             // posizione: il nodo che next() restituirà

        public boolean hasNext() {
            return prossimo != null;
        }

        public E next() {
            E dato = prossimo.dato;                // si legge il dato...
            prossimo = prossimo.successivo;        // ...e si avanza
            return dato;
        }
    }
}

public class SchemaCatena {
    public static void main(String[] args) {
        Catena<String> c = new Catena<>();
        c.aggiungiInTesta("c");
        c.aggiungiInTesta("b");
        c.aggiungiInTesta("a");
        for (String s : c) {
            System.out.print(s + " ");
        }
        System.out.println();
    }
}
```

```text
a b c 
```

Import: `java.util.Iterator`. Nessuna eccezione da dichiarare: se la traccia lo chiede, `next` lancia `NoSuchElementException` (import `java.util.NoSuchElementException`) quando `prossimo == null`, come in 12.4.3. Punti da controllare: `Iterable<E>` e `Iterator<E>` con il parametro di tipo; i metodi `iterator`, `hasNext`, `next` dichiarati `public` (vengono da un'interfaccia); il campo `prossimo` inizializzato a `testa`; il nodo e l'iteratore sono classi interne **non statiche**.

### Contare con una mappa

*Quando si usa:* la traccia chiede "quante volte compare ciascun valore" oppure "associa a ogni chiave un valore" e poi un riepilogo. Si veda la sezione 12.6.4.

```java
import java.util.Map;
import java.util.TreeMap;

public class SchemaMappa {
    public static void main(String[] args) {
        String[] voti = {"B", "A", "C", "A", "B", "A"};

        Map<String, Integer> conteggio = new TreeMap<>();      // TreeMap: chiavi stampate in ordine
        for (String v : voti) {
            conteggio.put(v, conteggio.getOrDefault(v, 0) + 1);    // 0 se la chiave non c'è ancora
        }

        for (Map.Entry<String, Integer> e : conteggio.entrySet()) {
            System.out.println(e.getKey() + ": " + e.getValue());
        }
        System.out.println(conteggio.containsKey("D"));
    }
}
```

```text
A: 3
B: 2
C: 1
false
```

Import: `java.util.Map`, `java.util.TreeMap` (o `java.util.HashMap`). Nessuna eccezione da dichiarare. Punti da controllare: `Map<String, Integer>` con **due** tipi (mai `int`); `get`, `put`, `containsKey`, `entrySet` (non `getValue` sulla mappa: `getKey` e `getValue` sono della coppia `Map.Entry`); `getOrDefault` per non incontrare `null`.

### Ordinare con un `Comparator`

*Quando si usa:* la traccia chiede di stampare gli oggetti "in ordine di..." un criterio diverso o più complesso dell'ordine naturale. Si veda la sezione 12.6.5.

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

class Atleta {
    private String nome;
    private int punti;

    public Atleta(String nome, int punti) {
        this.nome = nome;
        this.punti = punti;
    }

    public String getNome() {
        return nome;
    }

    public int getPunti() {
        return punti;
    }

    public String toString() {
        return nome + " " + punti;
    }
}

public class SchemaOrdinamento {
    public static void main(String[] args) {
        ArrayList<Atleta> classifica = new ArrayList<>();
        classifica.add(new Atleta("Rita", 80));
        classifica.add(new Atleta("Carlo", 95));
        classifica.add(new Atleta("Anna", 80));

        Collections.sort(classifica, new Comparator<Atleta>() {
            public int compare(Atleta a, Atleta b) {                       // public, int, due parametri
                int c = Integer.compare(b.getPunti(), a.getPunti());       // punti decrescenti
                if (c != 0) {
                    return c;
                }
                return a.getNome().compareTo(b.getNome());                 // a parità, per nome
            }
        });
        System.out.println(classifica);
    }
}
```

```text
[Carlo 95, Anna 80, Rita 80]
```

Import: `java.util.ArrayList`, `java.util.Collections`, `java.util.Comparator`. Nessuna eccezione da dichiarare. Punti da controllare: `Comparator<Atleta>` con il tipo; `compare` dichiarato `public int compare(Atleta a, Atleta b)`; il numero **negativo** significa "`a` viene prima"; per l'ordine decrescente si scambiano gli argomenti di `Integer.compare`; la parità si risolve con un secondo criterio, altrimenti l'ordine tra i pari resta quello di partenza (l'ordinamento è stabile).

### Eliminare i duplicati

*Quando si usa:* la traccia chiede "elementi senza ripetizioni" oppure di segnalare le ripetizioni. Si veda la sezione 12.6.3.

```java
import java.util.HashSet;
import java.util.TreeSet;

public class SchemaInsieme {
    public static void main(String[] args) {
        String[] ingressi = {"rossi", "bianchi", "rossi", "verdi", "bianchi"};

        HashSet<String> visti = new HashSet<>();
        for (String s : ingressi) {
            if (!visti.add(s)) {                       // add restituisce false se c'era già
                System.out.println("ripetuto: " + s);
            }
        }

        TreeSet<String> ordinati = new TreeSet<>(visti);   // senza duplicati e in ordine alfabetico
        System.out.println(ordinati + " " + ordinati.size());
    }
}
```

```text
ripetuto: rossi
ripetuto: bianchi
[bianchi, rossi, verdi] 3
```

Import: `java.util.HashSet`, `java.util.TreeSet`. Nessuna eccezione da dichiarare. Punti da controllare: per oggetti **nostri** serve la coppia `equals`/`hashCode` (12.6.3), altrimenti i duplicati non sono riconosciuti; con `TreeSet` serve invece `Comparable` o un `Comparator`; il tipo tra `<>` è una classe; un `HashSet` non garantisce nessun ordine di stampa.

## Errori tipici

Alcuni errori sono già discussi nel testo: `get`, `size` e le parentesi quadre al posto dei metodi (sezione 12.1.5), l'indice fuori dai limiti (12.1.6), la copia con l'assegnazione (12.1.7), il tipo grezzo (12.2.3), i nodi che si perdono scorrendo la lista con `testa` (12.3.2), la collezione modificata durante il for-each (12.4.4), `getValue` e `get` che restituisce `null` per le mappe (12.6.4), `equals` e `hashCode` per gli insiemi (12.6.3). Seguono gli altri.

> [!CAUTION]
> **Errore tipico — Un tipo primitivo tra le parentesi angolari**
> ```java
> ArrayList<int> voti = new ArrayList<>();          // ERRORE
> Map<String, double> medie = new HashMap<>();      // ERRORE
> ```
> Il compilatore risponde `unexpected type`, con `required: reference` e `found: int` (o `double`). Il parametro di tipo deve essere una **classe**. Forma corretta: `ArrayList<Integer>` e `Map<String, Double>`. Il passaggio da `int` a `Integer` e viceversa è automatico (Capitolo 6, sezione 6.6.3).

> [!CAUTION]
> **Errore tipico — Dimenticare `import` e confondere `Collection` con `Collections`**
> ```java
> public class Prova {
>     public static void main(String[] args) {
>         ArrayList<String> l = new ArrayList<>();      // ERRORE: manca import java.util.ArrayList;
>     }
> }
> ```
> Il compilatore risponde `cannot find symbol`, `symbol: class ArrayList`. Le classi delle collezioni stanno in `java.util` e non sono visibili senza `import`; lo stesso vale per `Iterator`, `Map`, `HashMap`, `Collections`, `Comparator`. Una confusione parente: `Collection` (senza la **s**) è un'interfaccia, `Collections` è la classe dei metodi di utilità; scrivere `Collection.sort(l)` dà `cannot find symbol`, `symbol: method sort(ArrayList<String>)`, `location: interface Collection`. Si ordina con `Collections.sort(l)`.

> [!CAUTION]
> **Errore tipico — `remove(1)` su una lista di `Integer`**
> ```java
> ArrayList<Integer> l = new ArrayList<>();
> l.add(10); l.add(20); l.add(1);
> l.remove(1);                       // toglie la POSIZIONE 1 (il 20), non il valore 1
> System.out.println(l);             // [10, 1]
> ```
> Il programma compila e non lancia nulla, ma toglie l'elemento sbagliato. Forma corretta per togliere il valore: `l.remove(Integer.valueOf(1));` (sezione 12.1.4). Se l'indice scritto non esiste, l'eccezione è `IndexOutOfBoundsException`.

> [!CAUTION]
> **Errore tipico — Il ciclo che va troppo avanti**
> ```java
> for (int i = 0; i <= l.size(); i++) {      // ERRORE: <= invece di <
>     System.out.println(l.get(i));
> }
> ```
> L'ultimo giro chiede `l.get(l.size())`, che non esiste: `IndexOutOfBoundsException: Index 1 out of bounds for length 1` con una lista di un elemento. Gli indici validi vanno da `0` a `size() - 1`; il ciclo si scrive con `<`, oppure con il for-each, che non ha indice.

> [!CAUTION]
> **Errore tipico — Una lista di un tipo contro una di un altro**
> ```java
> ArrayList<String> l = new ArrayList<>();
> l.add(2);                                          // ERRORE
> ArrayList<String> m = new ArrayList<Object>();     // ERRORE
> ```
> Il primo errore è `incompatible types: int cannot be converted to String`: un `ArrayList<String>` accetta solo `String`, ed è proprio ciò per cui si scrive il tipo. Il secondo è `incompatible types: ArrayList<Object> cannot be converted to ArrayList<String>`: due istanziazioni diverse di una classe parametrica non sono compatibili, nemmeno quando una è `Object`. I due tipi tra le parentesi angolari devono essere **identici**.

> [!CAUTION]
> **Errore tipico — Creare un array del tipo parametro**
> ```java
> class Pila<T> {
>     private T[] elementi = new T[20];          // ERRORE
> }
> ```
> Il compilatore risponde `generic array creation`. Dentro una classe generica non si scrive `new T[...]` né `new T()`. Si usa una struttura che non richiede di creare un `T`, come una lista concatenata di nodi (sezione 12.3.4) o una `ArrayList<T>`.

> [!CAUTION]
> **Errore tipico — Ordinare oggetti che non sanno confrontarsi**
> ```java
> ArrayList<Pianeta> l = new ArrayList<>();      // Pianeta NON realizza Comparable
> Collections.sort(l);                           // ERRORE di compilazione
> TreeSet<Pianeta> s = new TreeSet<>();
> s.add(new Pianeta("Marte", 6779));             // compila, ma lancia ClassCastException
> ```
> `Collections.sort(l)` non compila: il messaggio comincia con `no suitable method found for sort(ArrayList<Pianeta>)` e spiega che `T` ha `incompatible bounds` rispetto a `Comparable`. Il `TreeSet`, invece, compila e fallisce a esecuzione: `ClassCastException: class Pianeta cannot be cast to class java.lang.Comparable`. Rimedi: far realizzare `Comparable<Pianeta>` alla classe (Capitolo 10, sezione 10.4), oppure passare un `Comparator` (sezione 12.6.5).

> [!CAUTION]
> **Errore tipico — `compare`, `compareTo`, `hasNext`... senza `public`**
> ```java
> class PerNome implements Comparator<String> {
>     int compare(String a, String b) {                  // ERRORE: manca public
>         return a.compareTo(b);
>     }
> }
> ```
> Il compilatore risponde `compare(String,String) in PerNome cannot implement compare(T,T) in Comparator`, con `attempting to assign weaker access privileges; was public`. I metodi di un'interfaccia sono `public` e chi li realizza deve dichiararli `public` (Capitolo 10, sezione 10.2.3). Lo stesso vale per `compareTo`, `iterator`, `hasNext`, `next`, `remove`. Se invece il tipo di ritorno è sbagliato (`boolean compare(...)`), l'errore è `return type boolean is not compatible with int`.

> [!CAUTION]
> **Errore tipico — Usare `next` e `remove` fuori sequenza**
> ```java
> Iterator<String> it = lista.iterator();
> it.remove();           // IllegalStateException: nessun next() prima
> it.next();             // NoSuchElementException se la lista è vuota
> ```
> `next()` chiamato quando `hasNext()` è falso lancia `NoSuchElementException`; `remove()` chiamato prima di un `next()`, o due volte di fila, lancia `IllegalStateException`. Lo schema corretto è sempre `while (it.hasNext()) { x = it.next(); ... it.remove(); ... }`, con al più un `remove()` per ogni `next()`.

> [!CAUTION]
> **Errore tipico — Contare su un ordine che la collezione non garantisce**
> ```java
> HashMap<String, Integer> m = new HashMap<>();
> HashSet<String> s = new HashSet<>();
> // ...inserimenti...
> System.out.println(m);     // l'ordine delle coppie non è specificato
> System.out.println(s);     // l'ordine degli elementi non è specificato
> ```
> `HashMap` e `HashSet` non garantiscono nessun ordine di scansione, e può cambiare quando la collezione cresce. Se la traccia mostra un output in un ordine preciso, il programma che stampa direttamente una di queste strutture può produrre le stesse righe in ordine diverso e non superare il confronto con l'output atteso. Rimedi: `TreeMap` e `TreeSet` per l'**ordine crescente delle chiavi**; una `ArrayList` per l'**ordine di inserimento**; oppure le classi `LinkedHashMap` e `LinkedHashSet`, che la Javadoc descrive con "ordine di iterazione prevedibile", normalmente quello di inserimento.
>
> *Fonte:* [java.util.LinkedHashMap](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/LinkedHashMap.html)

> [!CAUTION]
> **Errore tipico — La mappa dichiarata ma non popolata**
> ```java
> class Punteggi {
>     private Map<String, Integer> punti = new HashMap<>();     // vuota!
>
>     public void aggiungi(String nome) {
>         punti.put(nome, punti.get(nome) + 1);                 // NullPointerException: get restituisce null
>     }
> }
> ```
> Dichiarare una mappa la crea **vuota**: per una chiave nuova `get` restituisce `null`, e `null + 1` provoca un unboxing di `null` (`NullPointerException: Cannot invoke "java.lang.Integer.intValue()" because the return value of "java.util.Map.get(Object)" is null`). Se la traccia dà l'elenco delle chiavi al costruttore, è il costruttore che deve fare `put(chiave, 0)` per ognuna; altrimenti si scrive `punti.getOrDefault(nome, 0) + 1`.

## Riassunto

Un array ha la lunghezza fissa; l'**`ArrayList`** è un array che cresce e si accorcia da solo, e si usa **solo con metodi** (`add`, `get`, `set`, `remove`, `size`, `contains`, `indexOf`, `isEmpty`, `clear`). Contiene soltanto oggetti, quindi per i numeri si usano i wrapper (`ArrayList<Integer>`), e va importato da `java.util`. Il tipo tra le parentesi angolari è il **parametro di tipo** di una **classe parametrica**: i *generics* permettono di scrivere una volta sola una classe che funziona per qualunque tipo di elemento, di far controllare i tipi al compilatore e di evitare i cast. Le classi generiche si dichiarano con `class Nome<T>`; il parametro è sempre una classe (mai un primitivo) e non si può usare per allocare memoria (`new T[]`).

La seconda grande rappresentazione di una sequenza è la **lista concatenata**: una catena di nodi, ciascuno con un dato e un riferimento al successivo, raggiunta tramite il riferimento alla testa. Il nodo si nasconde come classe interna privata. Le operazioni di inserimento e rimozione cambiano pochi collegamenti, e si scrivono con un riferimento che avanza (e, per togliere, un secondo che segue). Per scorrere una collezione senza esporne la struttura si usa un **iteratore** (`Iterator<E>`: `hasNext`, `next`, `remove`); una classe che realizza `Iterable<E>` e scrive `iterator()` si può usare nel for-each. Modificare una collezione durante la scansione, senza passare dalla `remove` dell'iteratore, lancia `ConcurrentModificationException`.

La libreria offre le collezioni già pronte: `List` (`ArrayList`, `LinkedList`), `Set` (`HashSet`, `TreeSet`) per elementi senza duplicati, `Map` (`HashMap`, `TreeMap`) per associare chiavi a valori. Le versioni `Hash...` non garantiscono nessun ordine; le versioni `Tree...` mantengono l'ordine. Gli insiemi e le mappe a tabella hash richiedono `equals` e `hashCode` coerenti; quelle ad albero richiedono `Comparable` o un `Comparator`. Si ordina una lista con `Collections.sort`, con l'ordine naturale (`Comparable`, Capitolo 10) o con un `Comparator<T>`, la cui `compare` riceve i due oggetti.

**Concetti chiave**

- **`ArrayList<E>`.** Lista che cambia lunghezza a esecuzione; usa un array internamente; solo oggetti; tipo degli elementi tra `<>`.
- **Metodi di `ArrayList`.** `add(x)` in fondo, `add(i, x)` in mezzo, `get(i)`, `set(i, x)`, `remove(i)` per posizione, `remove(x)` per valore, `size()`, `contains(x)`, `indexOf(x)`, `isEmpty()`, `clear()`.
- **Indici.** Da 0 a `size() - 1`; fuori dai limiti, `IndexOutOfBoundsException`. Con `ArrayList<Integer>`, `remove(int)` e `remove(Object)` sono due metodi diversi.
- **Copia.** `b = a` copia il riferimento; `new ArrayList<>(a)` crea una lista nuova (copia superficiale: gli oggetti restano condivisi).
- **Classe parametrica / generics.** Classe con parametro di tipo: `class Nome<T>`. Il parametro non può essere primitivo, e non si può usare con `new T[...]`.
- **Tipo grezzo.** Classe parametrica usata senza parametro: compila ma perde il controllo dei tipi (avviso `unchecked`, cast necessari, `ClassCastException`).
- **Lista concatenata.** Nodi con dato e collegamento; `testa` indica il primo, `null` chiude la catena; il nodo è classe interna privata della lista.
- **Rimozione in una lista concatenata.** Serve il nodo precedente; la testa è un caso a parte.
- **`Iterator<E>`.** `hasNext()`, `next()`, `remove()` (al più uno per ogni `next`).
- **`Iterable<T>`.** Un solo metodo, `iterator()`; abilita il for-each.
- **Fail-fast.** Gli iteratori della libreria lanciano `ConcurrentModificationException` se la collezione è modificata senza passare dall'iteratore.
- **Pila.** Si inserisce e si toglie dalla cima (LIFO); `push` e `pop`; in `LinkedList` anche `push` e `pop`.
- **Albero binario.** Nodo con dato e due riferimenti; la radice è il primo nodo; i metodi sono ricorsivi.
- **`List`, `Set`, `Map`.** Sequenza con posizioni e duplicati; insieme senza duplicati; coppie chiave → valore con chiavi uniche.
- **`LinkedList`.** Lista doppiamente concatenata che realizza anche `Deque`: `addFirst`, `addLast`, `getFirst`, `removeFirst`, `peek`, `poll`.
- **`HashSet` / `TreeSet`.** Insieme senza ordine e rapido / insieme ordinato. `add` restituisce `false` se l'elemento c'è già.
- **`HashMap` / `TreeMap`.** Mappa senza ordine e rapida / mappa con chiavi ordinate; `put`, `get`, `getOrDefault`, `containsKey`, `remove`, `keySet`, `values`, `entrySet`.
- **`Map.Entry<K,V>`.** La coppia ottenuta da `entrySet()`: `getKey()` e `getValue()`.
- **`equals` e `hashCode`.** Vanno riscritti insieme per usare oggetti nostri in un `HashSet` o come chiavi di una `HashMap`.
- **`Comparator<T>`.** Un criterio di ordinamento separato dalla classe: `int compare(T o1, T o2)`; negativo = il primo viene prima.
- **`Collections.sort`.** Ordina una lista; con un solo argomento richiede `Comparable`, con due accetta un `Comparator`; è stabile.
- **Scegliere la struttura.** Posizioni: lista. Unicità: insieme. Chiave: mappa. Ordine: versione `Tree...`.

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `ArrayList<E>` (`java.util`) | costruttori | `ArrayList()`, `ArrayList(int initialCapacity)`, `ArrayList(Collection<? extends E> c)` | `IllegalArgumentException` se la capacità è negativa |
| `ArrayList<E>` | `add` | `boolean add(E e)`, `void add(int index, E element)` | `IndexOutOfBoundsException` (secondo caso, se `index > size()` o negativo) |
| `ArrayList<E>` | `get`, `set` | `E get(int index)`, `E set(int index, E element)` | `IndexOutOfBoundsException` |
| `ArrayList<E>` | `remove` | `E remove(int index)`, `boolean remove(Object o)` | `IndexOutOfBoundsException` (primo caso) |
| `ArrayList<E>` | altri | `int size()`, `boolean isEmpty()`, `boolean contains(Object o)`, `int indexOf(Object o)`, `void clear()`, `void trimToSize()` | — |
| `Iterator<E>` (`java.util`) | metodi | `boolean hasNext()`, `E next()`, `void remove()` | `NoSuchElementException` (`next`); `IllegalStateException`, `UnsupportedOperationException` (`remove`) |
| `Iterable<T>` (`java.lang`) | metodo | `Iterator<T> iterator()` | — |
| `LinkedList<E>` | testa e coda | `void addFirst(E e)`, `void addLast(E e)`, `E getFirst()`, `E removeFirst()`, `E peek()`, `E poll()`, `void push(E e)`, `E pop()` | `NoSuchElementException` per `getFirst`, `removeFirst`, `pop` su lista vuota; `peek` e `poll` restituiscono `null` |
| `HashSet<E>`, `TreeSet<E>` | `add` | `boolean add(E e)` | `ClassCastException` per `TreeSet` se non confrontabile |
| `Map<K,V>` | accesso | `V put(K key, V value)`, `V get(Object key)`, `V getOrDefault(Object key, V defaultValue)`, `V remove(Object key)`, `boolean containsKey(Object key)`, `int size()` | — |
| `Map<K,V>` | viste | `Set<K> keySet()`, `Collection<V> values()`, `Set<Map.Entry<K,V>> entrySet()` | — |
| `Map.Entry<K,V>` | metodi | `K getKey()`, `V getValue()` | — |
| `Collections` (`java.util`) | `sort` | `static <T extends Comparable<? super T>> void sort(List<T> list)`, `static <T> void sort(List<T> list, Comparator<? super T> c)` | `ClassCastException` |
| `Collections` | `reverse` | `static void reverse(List<?> list)` | — |
| `Comparator<T>` (`java.util`) | `compare` | `int compare(T o1, T o2)` | — |
| `List<E>` | `sort` | `default void sort(Comparator<? super E> c)` | — |
