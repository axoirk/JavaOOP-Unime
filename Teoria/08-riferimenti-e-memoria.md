---
materia: Programmazione a Oggetti
capitolo: 8
titolo: Riferimenti e memoria
livello_syllabus: 2
stato: completo
slide: ["Savitch cap. 8 slide 39-55", "Savitch cap. 9 slide 31-32, 40", "Savitch cap. 15 slide 12-13", "Lect2 (Variable, Reference types, Methods)", "Multithreading p. 4"]
appelli: [EXAM3]
fonti_esterne: 3
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 8 — Riferimenti e memoria

## Di cosa parla questo capitolo

Nel [Capitolo 7 — Classi e oggetti](07-classi-e-oggetti.md) abbiamo imparato a definire classi e a creare oggetti con `new`. Chi prova a usarli, però, si imbatte presto in tre comportamenti che sembrano strani. Il primo: scrivere `q = p`, con `p` e `q` oggetti, **non crea una copia**, e una modifica fatta tramite `q` si vede anche tramite `p`. Il secondo: due oggetti con esattamente gli stessi dati, confrontati con `==`, risultano **diversi**. Il terzo: un programma che compila senza errori si interrompe in esecuzione con una `NullPointerException`, perché si è usata una variabile che "non indica niente".

I tre fatti hanno la stessa radice. Una variabile di tipo primitivo contiene il valore; una variabile di tipo classe, invece, **non contiene l'oggetto**: contiene l'*indirizzo* di dove l'oggetto si trova in memoria, cioè un **riferimento**. Questo capitolo parte da lì. Ricostruisce la mappa della memoria della JVM che avevamo abbozzato nel [Capitolo 1](01-java-e-la-jvm.md) (sezione 1.9), dalla quale deriva il comportamento dell'assegnamento, già incontrato con gli array nel [Capitolo 5 — Array e matrici](05-array-e-matrici.md) (sezione 5.4) e con i parametri dei metodi nel [Capitolo 6 — Metodi](06-metodi.md) (sezione 6.3.4). Poi ne trae le conseguenze una per una: il valore `null` e la `NullPointerException`, la differenza tra `==` e `equals`, che cosa può e che cosa non può fare un metodo che riceve un oggetto, come si copia davvero un oggetto, e infine quando un oggetto smette di esistere e chi lo elimina.

Alla fine del capitolo saprai **disegnare la memoria** di un programma riga per riga (variabili da una parte, oggetti dall'altra, frecce in mezzo) e prevedere con quel disegno che cosa stamperà; saprai dire quando una `NullPointerException` può verificarsi e come evitarla; saprai scrivere un metodo che confronta due oggetti in base al **contenuto**; saprai distinguere un metodo che *modifica* l'oggetto ricevuto da uno che non può *sostituirlo*; saprai scrivere un costruttore di copia e riconoscere quando la copia è solo apparente; e saprai spiegare che cos'è il *garbage collector* e perché in Java non si libera la memoria a mano.

> [!IMPORTANT]
> **Nota per l'esame — I riferimenti non compaiono mai nelle tracce con questo nome**
> Nessuna traccia scrive "si ricordi che una variabile contiene un riferimento". Le conseguenze però ci sono sempre: un metodo che "restituisce `null` in caso di fallimento", un oggetto che viaggia su un socket e ne torna un altro "identico", una copia che deve essere "indipendente dall'originale", un confronto tra oggetti. Chi ha chiaro il modello della memoria di questo capitolo non deve ricordare regole separate: le deduce. Vedi la sezione "Come esce all'esame".

## 8.1 Variabili e oggetti: due cose diverse

### 8.1.1 Il problema: una copia che non copia

Cominciamo da un programma che mette a confronto una variabile primitiva e una variabile di tipo classe. La classe `Punto` rappresenta un punto del piano ed è abbastanza semplice da non distrarci: due campi privati, un costruttore, un metodo che sposta il punto e uno che ne restituisce la descrizione.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

public class Sorpresa {
    public static void main(String[] args) {
        int a = 5;
        int b = a;                       // copia il numero
        b = b + 10;
        System.out.println("a = " + a + ", b = " + b);

        Punto p = new Punto(1, 2);
        Punto q = p;                     // copia... che cosa?
        q.sposta(10, 10);
        System.out.println("p = " + p.descrivi() + ", q = " + q.descrivi());
    }
}
```

```text
a = 5, b = 15
p = (11, 12), q = (11, 12)
```

La prima parte si comporta come ci si aspetta: `b` riceve una copia di `a`, quindi cambiare `b` non tocca `a`. Nella seconda parte la struttura del codice è identica (`Punto q = p;`, poi si modifica `q`), ma il risultato no: abbiamo spostato **`q`** e si è spostato anche **`p`**. Non c'è nessun errore: il programma fa esattamente ciò che Java prevede, e ciò che Java prevede dipende da *che cosa* contengono le due variabili.

### 8.1.2 Variabili primitive e variabili di riferimento

Una variabile è, per definizione, il nome di un posto in memoria. La differenza sta in che cosa si trova in quel posto.

- In una variabile di **tipo primitivo** (`int`, `double`, `boolean`, `char`…) c'è il valore stesso: nel posto chiamato `a` c'è il numero `5`.
- In una variabile di **tipo classe** (e anche di tipo array, e quindi `String`, che è una classe) non c'è l'oggetto. L'oggetto si trova *altrove*, in un'altra zona della memoria; nel posto chiamato `p` c'è l'**indirizzo** di quell'oggetto, cioè l'informazione che permette di ritrovarlo.

> [!NOTE]
> **Definizione — Riferimento**
> Un **riferimento** (*reference*) è l'indirizzo in memoria di un oggetto. Una variabile di tipo classe o di tipo array contiene un riferimento, non l'oggetto: per questo i tipi classe e i tipi array si dicono **tipi riferimento** (*reference types*). Dire che una variabile "si riferisce a" un oggetto, "punta a" un oggetto o "indica" un oggetto significa che il suo contenuto è l'indirizzo di quell'oggetto.

Il riferimento è un valore a tutti gli effetti, e come ogni valore può essere copiato in un'altra variabile. Quando scriviamo `Punto q = p;`, Java fa ciò che fa sempre un assegnamento: **copia il contenuto** di `p` dentro `q`. Ma il contenuto di `p` è un indirizzo, quindi dopo l'assegnamento `p` e `q` contengono lo *stesso* indirizzo. L'oggetto è uno solo, e ora ha due nomi.

> [!TIP]
> **Intuizione — L'indirizzo di casa**
> Pensa a una casa e al suo indirizzo scritto su un biglietto. Se fai una fotocopia del biglietto e la dai a un amico, ora due biglietti riportano lo stesso indirizzo, ma la casa è una sola: se l'amico ci entra e sposta un mobile, tu, entrandoci dopo, trovi il mobile spostato. Le variabili sono i biglietti; l'oggetto è la casa. Un'immagine altrettanto utile è il telecomando: due telecomandi possono comandare lo stesso televisore. L'analogia funziona fino a un certo punto: con un biglietto reale si potrebbe fare un calcolo sull'indirizzo ("la casa accanto"), mentre in Java **non si possono fare operazioni sul valore di un riferimento**: si può solo copiarlo, confrontarlo e usarlo per raggiungere l'oggetto.

Riassumiamo le differenze in una tabella.

| | Variabile primitiva | Variabile di riferimento |
|---|---|---|
| Che cosa contiene | il valore (`5`, `3.14`, `true`) | l'indirizzo di un oggetto, oppure `null` |
| Dove sta l'oggetto | non c'è nessun oggetto | in un'altra zona della memoria (lo *heap*, sezione 8.1.3) |
| L'assegnamento `y = x` | copia il valore | copia l'indirizzo: due nomi per lo stesso oggetto |
| Valore predefinito di un campo | `0`, `0.0`, `false`, carattere di codice 0 | `null` |
| L'operatore `==` | confronta i valori | confronta gli indirizzi (sezione 8.4) |

Il fatto che i tipi classe funzionino così non è un difetto: è una scelta che rende la gestione della memoria più efficiente. Un oggetto può essere grande (pensiamo a un array di mille elementi o a un oggetto con decine di campi), e copiarlo per intero a ogni assegnamento o a ogni chiamata di un metodo sarebbe costoso. Copiare un indirizzo costa quanto copiare un intero, qualunque sia la dimensione dell'oggetto a cui si riferisce.

### 8.1.3 Stack e heap

Nel Capitolo 1 (sezione 1.9) abbiamo visto che la JVM organizza la memoria in più zone. Due ci servono ora.

- Lo **stack** (*pila*) è la zona delle chiamate di metodo. Ogni volta che un metodo viene chiamato, la JVM vi riserva un blocco, il **frame** (*record di attivazione*), che contiene i parametri e le variabili locali di quella chiamata. Quando il metodo termina il suo frame viene tolto, e con esso tutte le sue variabili locali. Ogni flusso di esecuzione (*thread*) ha il proprio stack.
- Lo **heap** è la zona degli **oggetti**: tutto ciò che viene creato con `new` (compresi gli array) vive lì. Lo heap è unico, condiviso da tutti i thread, e gli oggetti che non servono più vengono eliminati automaticamente dal *garbage collector* (sezione 8.7).

Ne segue una regola molto semplice da ricordare:

> [!NOTE]
> **Definizione — Dove vive che cosa**
> Le **variabili locali e i parametri** dei metodi vivono nello **stack**, nel frame del metodo. Gli **oggetti** (e gli array) vivono nello **heap**. Una variabile locale di tipo primitivo contiene il valore; una variabile locale di tipo riferimento contiene nello stack l'**indirizzo** di un oggetto che sta nello heap.

Una precisazione importante: i **campi** di un oggetto, anche quelli di tipo primitivo, fanno parte dell'oggetto e quindi stanno nello heap, *dentro* l'oggetto. Non è vero che "i primitivi stanno nello stack": ci stanno quando sono variabili locali o parametri. Un campo `int x` di un `Punto` si trova nello heap, insieme al campo `y`.

Vediamo la memoria quando `main` ha eseguito le tre righe seguenti. Il disegno è un modo di rappresentare la situazione, non un'immagine fedele dei byte, ma è esattamente quello che useremo per ragionare.

```java
int n = 5;
Punto p = new Punto(1, 2);
Punto q = p;
```

```text
        STACK (frame di main)                       HEAP
   +----------------+
   | n = 5          |                   +-----------------+
   | p   *----------|----------+------->| Punto           |
   | q   *----------|----------+        |   x = 1         |
   +----------------+                   |   y = 2         |
                                        +-----------------+
```

Nello stack ci sono tre variabili: `n`, che contiene il numero `5`, e `p` e `q`, che contengono ciascuna un indirizzo, disegnato come freccia. Le due frecce arrivano allo stesso oggetto, nello heap, che contiene i campi `x` e `y`. L'oggetto non ha un nome proprio: lo si raggiunge solo seguendo una freccia, cioè attraverso una variabile.

### 8.1.4 Che cosa fanno la dichiarazione e `new`

Possiamo ora dire con precisione che cosa fanno le due metà di una riga come `Punto p = new Punto(1, 2);`.

- La **dichiarazione** `Punto p` crea soltanto la variabile `p` nello stack: un posto capace di contenere l'indirizzo di un `Punto`. **Non crea nessun punto.** Se non la inizializziamo, la variabile locale non contiene niente di utilizzabile, e il compilatore ci impedisce di usarla (`variable p might not have been initialized`).
- L'espressione `new Punto(1, 2)` **crea l'oggetto** nello heap, esegue il costruttore (sezione 7.2.7) e produce come risultato l'indirizzo dell'oggetto appena creato.
- L'**assegnamento** `=` copia quell'indirizzo nella variabile `p`.

Per questo ogni `new` produce un oggetto nuovo, distinto da tutti gli altri: due `new Punto(1, 2)` consecutivi creano due oggetti separati, anche se hanno gli stessi valori nei campi. E per questo una variabile può cambiare oggetto: se poi scriviamo `p = new Punto(9, 9);`, nella variabile `p` viene scritto un indirizzo diverso. L'oggetto precedente non viene toccato (resta nello heap finché qualcuno ci si riferisce, sezione 8.7).

### 8.1.5 Disegnare la memoria a mano

Per prevedere il risultato di un programma che usa oggetti il metodo più sicuro è il disegno. Si procede così, riga per riga:

1. a sinistra si scrivono le **variabili** con il loro contenuto: un valore per i primitivi, una freccia (o `null`) per i riferimenti;
2. a destra si disegna un **riquadro nuovo** per ogni `new`, con i suoi campi;
3. un assegnamento tra due riferimenti (`r = p`) **copia la freccia**: `r` punta dove punta `p`;
4. un assegnamento con `new` (`p = new …`) **cancella la freccia vecchia** e ne disegna una nuova; il riquadro vecchio resta dov'è;
5. l'operatore punto (`p.sposta(…)`, `p.x`) **segue la freccia** e lavora sul riquadro a cui arriva.

#### Esempio — Seguire un programma sul disegno

Seguiamo sei righe di un programma, con il disegno dopo la quarta e dopo la sesta.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

public class Traccia {
    public static void main(String[] args) {
        Punto p = new Punto(1, 2);       // riga 1
        Punto q = new Punto(5, 5);       // riga 2
        Punto r = p;                     // riga 3
        r.sposta(1, 1);                  // riga 4
        p = q;                           // riga 5
        p.sposta(10, 10);                // riga 6
        System.out.println(p.descrivi() + " " + q.descrivi() + " " + r.descrivi());
    }
}
```

```text
(15, 15) (15, 15) (2, 3)
```

Dopo la riga 4 la situazione è questa. Alle righe 1 e 2 sono nati due oggetti, che chiamiamo A e B; alla riga 3 `r` ha copiato la freccia di `p`, quindi punta ad A; alla riga 4 `r.sposta(1, 1)` ha seguito la freccia e ha cambiato A da `(1, 2)` a `(2, 3)`.

```text
       STACK                                HEAP
   +----------------+
   | p   *----------|----------+        +--------------+
   | r   *----------|----------+------->| A  (2, 3)    |
   |                |                   +--------------+
   | q   *----------|----------+        +--------------+
   +----------------+          +------->| B  (5, 5)    |
                                        +--------------+
```

Alla riga 5 `p = q` copia la freccia di `q` dentro `p`: ora `p` non punta più ad A ma a B. A non è stato toccato, e `r` lo indica ancora. Alla riga 6 `p.sposta(10, 10)` segue la freccia di `p`, cioè arriva a B, e lo porta a `(15, 15)`.

```text
       STACK                                HEAP
   +----------------+                   +--------------+
   | r   *----------|------------------>| A  (2, 3)    |
   |                |                   +--------------+
   | p   *----------|----------+        +--------------+
   | q   *----------|----------+------->| B  (15, 15)  |
   +----------------+                   +--------------+
```

Il programma stampa quindi `p` e `q` come `(15, 15)`, perché sono due nomi dello stesso oggetto B, e `r` come `(2, 3)`, perché indica ancora A. Chi prova a prevedere questo output "a occhio", senza il disegno, sbaglia quasi sempre alla riga 5.

## 8.2 L'assegnamento copia il riferimento

### 8.2.1 Due nomi per lo stesso oggetto

Il comportamento del paragrafo 8.1.1 è ora spiegabile in due righe. Con `Punto q = p;` Java copia il contenuto di `p` in `q`. Il contenuto è un indirizzo, perciò dopo l'assegnamento **esiste un solo oggetto e due variabili che lo indicano**. Due variabili che indicano lo stesso oggetto si dicono **alias** (lo abbiamo già visto con gli array nella sezione 5.4.2): una modifica fatta all'oggetto attraverso una variabile si vede attraverso l'altra, per il semplice motivo che l'oggetto è quello.

Il comportamento si legge in quattro passi:

1. si crea l'oggetto con `new` e si assegna a una variabile, che ne contiene l'indirizzo;
2. si crea una seconda variabile e le si assegna la prima: le due frecce arrivano allo stesso riquadro;
3. si modifica l'oggetto attraverso la seconda variabile: il riquadro cambia, e lo si vede anche dalla prima;
4. si assegna alla seconda variabile un altro oggetto con `new`: la seconda freccia si sposta, l'altra e il primo oggetto restano come sono.

### 8.2.2 Modificare l'oggetto o cambiare la freccia

Il punto più importante di questa sezione è distinguere due operazioni che nel linguaggio di tutti i giorni si confondono ("ho cambiato `q`"). Con una variabile di riferimento si può fare:

- **modificare l'oggetto** a cui punta, chiamando un suo metodo o assegnando un suo campo: cambia il riquadro nello heap, e tutti gli alias lo vedono;
- **cambiare l'oggetto a cui punta**, con un nuovo assegnamento: cambia la freccia di *quella* variabile, e le altre variabili, e l'oggetto di prima, non sono toccati.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

public class DueOperazioni {
    public static void main(String[] args) {
        Punto p = new Punto(0, 0);
        Punto q = p;

        q.sposta(3, 4);                  // modifica l'oggetto: lo vedono sia p sia q
        System.out.println(p.descrivi() + " " + q.descrivi());

        q = new Punto(7, 7);             // q punta a un altro oggetto: p non se ne accorge
        System.out.println(p.descrivi() + " " + q.descrivi());
    }
}
```

```text
(3, 4) (3, 4)
(3, 4) (7, 7)
```

La prima riga di output mostra la modifica vista da entrambi gli alias. Dopo l'assegnamento `q = new Punto(7, 7)` le due variabili indicano oggetti diversi: `q` stampa il nuovo punto, `p` continua a stampare quello vecchio, che `q.sposta(3, 4)` aveva portato a `(3, 4)`.

### 8.2.3 Oggetti che contengono riferimenti

I campi di un oggetto possono essere a loro volta di tipo classe, e allora contengono riferimenti ad altri oggetti. Nel disegno ogni riquadro può avere frecce che escono dai suoi campi. Quando un oggetto viene costruito con parametri che sono oggetti, e li memorizza così come li riceve, si ottiene un'altra forma di alias: **più oggetti che condividono lo stesso componente**. A volte è proprio ciò che si vuole.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

class Segmento {
    private Punto inizio;
    private Punto fine;

    public Segmento(Punto inizio, Punto fine) {
        this.inizio = inizio;            // memorizza i riferimenti ricevuti, senza copiarli
        this.fine = fine;
    }

    public String descrivi() {
        return inizio.descrivi() + "-" + fine.descrivi();
    }
}

public class Condivisione {
    public static void main(String[] args) {
        Punto a = new Punto(0, 0);
        Punto b = new Punto(4, 0);
        Punto c = new Punto(4, 3);

        Segmento s1 = new Segmento(a, b);
        Segmento s2 = new Segmento(b, c);   // b è il vertice comune dei due segmenti

        b.sposta(0, 1);                     // si sposta il vertice: cambiano entrambi i segmenti
        System.out.println(s1.descrivi());
        System.out.println(s2.descrivi());
    }
}
```

```text
(0, 0)-(4, 1)
(4, 1)-(4, 3)
```

Il punto `b` è un oggetto solo, indicato dalla variabile `b` e dal campo `fine` di `s1` e dal campo `inizio` di `s2`. Spostandolo una volta, `s1` e `s2` mostrano entrambi il vertice nella nuova posizione. Se i due segmenti avessero dovuto muoversi in modo indipendente, il costruttore avrebbe dovuto **copiare** i punti ricevuti: è il tema della sezione 8.6, e la cura per la perdita di riservatezza già vista nel Capitolo 7 (sezione 7.3.7), che nasce proprio da questo meccanismo.

> [!WARNING]
> **Attenzione — Condividere non è sempre un errore**
> L'alias è uno strumento: è la ragione per cui un oggetto può essere usato da molte parti di un programma senza duplicarlo. Diventa un problema solo quando si condivide *senza volerlo*. Prima di scrivere codice che memorizza o restituisce un oggetto, conviene sempre chiedersi: "chi altro ha questo riferimento, e che cosa succede se lo modifica?".

## 8.3 `null`: la variabile che non indica niente

### 8.3.1 Il valore `null`

Una variabile di riferimento non è obbligata a indicare un oggetto. Il valore speciale **`null`** significa "nessun oggetto": la variabile esiste, ha un posto in memoria, ma quel posto non contiene l'indirizzo di niente. `null` si può assegnare a una variabile di **qualsiasi** tipo riferimento (classe, array, `String`) e non a una variabile di tipo primitivo: un `int` contiene sempre un numero.

`null` è anche il valore predefinito che Java dà a un campo di tipo riferimento, e a ogni elemento di un array di oggetti, quando non è stato inizializzato (sezioni 7.1.5 e 5.8). Le variabili **locali** invece non hanno valore predefinito: il compilatore pretende che siano assegnate prima dell'uso.

```java
public class ValoreNull {
    private static int[] dati;                 // campo statico di tipo array: parte a null

    public static void main(String[] args) {
        String s = null;                       // nessuna stringa
        Object nulla = null;
        System.out.println(s == null);         // true: si testa con ==
        System.out.println(dati == null);      // true: valore predefinito di un campo
        System.out.println(s);                 // println stampa il testo "null"
        System.out.println(nulla == s);        // true: null è sempre lo stesso valore
    }
}
```

```text
true
true
null
true
```

Le due prime righe mostrano che `null` si riconosce con l'operatore `==`: qui `==` è esattamente lo strumento giusto, perché si chiede se la freccia manca. La terza riga è un'abitudine di `println`: davanti a un riferimento `null` stampa la parola `null`, senza errori. L'errore arriva solo quando si prova a **usare** il riferimento.

> [!TIP]
> **Intuizione — Il telecomando senza televisore**
> Un riferimento `null` è come un telecomando che non è collegato a nessun apparecchio: puoi tenerlo in mano, passarlo, confrontarlo con un altro telecomando, ma se premi un tasto non succede nulla di sensato. Java, invece di non fare niente, interrompe il programma.

Il `null` è diverso dalla **stringa vuota** `""` (sezione 3.1.5): la stringa vuota è un oggetto vero, con zero caratteri, su cui si possono chiamare i metodi; `null` non è un oggetto, e non si può chiamare nessun metodo.

### 8.3.2 La `NullPointerException`

Seguire una freccia che non c'è è l'errore a runtime più frequente in Java. L'operatore punto (`p.sposta(…)`, `p.x`) significa "vai all'oggetto indicato da `p` e lavora su di esso". Se `p` vale `null`, non c'è nessun oggetto dove andare, e la JVM lancia una `NullPointerException`.

> [!NOTE]
> **Approfondimento esterno — `java.lang.NullPointerException`**
> La Javadoc di Java SE 17 dichiara `public class NullPointerException extends RuntimeException`, cioè un'eccezione **non controllata** (non va dichiarata né gestita). Viene lanciata "when an application attempts to use `null` in a case where an object is required", e l'elenco ufficiale dei casi è: chiamare un metodo d'istanza di un oggetto `null`; accedere a un campo di un oggetto `null`, in lettura o in scrittura; prendere la lunghezza di `null` come se fosse un array; accedere a un elemento di `null` come se fosse un array; lanciare `null` come se fosse un `Throwable`. La classe ha due costruttori, `NullPointerException()` e `NullPointerException(String s)`.
>
> *Fonte:* [java.lang.NullPointerException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/NullPointerException.html)

Vediamo i primi quattro casi dell'elenco, uno per volta, in un programma che li provoca di proposito. Per far proseguire il programma dopo ogni errore usiamo un blocco `try`/`catch`, che si studia nel [Capitolo 13 — Eccezioni](13-eccezioni.md): per ora basta sapere che il codice dentro `try` viene eseguito e che, se lancia una `NullPointerException`, il programma salta al blocco `catch` invece di terminare.

```java
class Cella {
    public int valore;
}

public class QuattroModi {
    public static void main(String[] args) {
        String s = null;
        Cella c = null;
        int[] v = null;

        try {
            s.length();                  // 1. metodo d'istanza di un oggetto null
        } catch (NullPointerException e) {
            System.out.println("1. metodo");
        }
        try {
            c.valore = 7;                // 2. campo di un oggetto null
        } catch (NullPointerException e) {
            System.out.println("2. campo");
        }
        try {
            int n = v.length;            // 3. lunghezza di null come se fosse un array
        } catch (NullPointerException e) {
            System.out.println("3. length");
        }
        try {
            v[0] = 1;                    // 4. elemento di null come se fosse un array
        } catch (NullPointerException e) {
            System.out.println("4. elemento");
        }
    }
}
```

```text
1. metodo
2. campo
3. length
4. elemento
```

Il compilatore non può accorgersi di nessuno di questi errori: ogni riga è corretta per quanto riguarda i tipi. Solo in esecuzione la JVM scopre che la variabile contiene `null`. Se il programma non ha il `catch`, l'esecuzione si interrompe stampando sull'errore standard una riga come questa, seguita dalla pila delle chiamate:

```text
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.length()" because "<local1>" is null
	at Prova.main(Prova.java:4)
```

La prima riga dice il tipo dell'eccezione e, nelle versioni recenti di Java, anche **quale** riferimento valeva `null` e che cosa si stava cercando di fare; la seconda dice in quale metodo e a quale riga del file è successo. Il nome della variabile compare solo se il file è stato compilato con le informazioni di debug (`javac -g`): con la compilazione normale il messaggio usa un segnaposto come `"<local1>"`, come nell'esempio, per la prima variabile locale del metodo. In entrambi i casi la riga indicata è il punto da cui partire per cercare il riferimento mancante.

### 8.3.3 Come evitarla: controllare prima di usare

Il rimedio è semplice: quando un riferimento *può* essere `null`, si controlla prima di usarlo.

```java
if (p != null) {
    p.sposta(1, 1);                      // qui p indica certamente un oggetto
}
```

Quando il controllo è unito ad altre condizioni con `&&` conta l'**ordine**. L'operatore `&&` valuta il secondo operando solo se il primo è `true` (cortocircuito, [Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.7.3), quindi il controllo su `null` va scritto *prima* della condizione che userebbe l'oggetto.

```java
public class Ordine {
    static boolean nonVuota(String s) {
        return s != null && s.length() > 0;    // se s è null, && si ferma: length() non viene chiamato
    }

    public static void main(String[] args) {
        System.out.println(nonVuota("ciao"));
        System.out.println(nonVuota(""));
        System.out.println(nonVuota(null));
    }
}
```

```text
true
false
false
```

Scritta al contrario (`s.length() > 0 && s != null`) la stessa condizione lancia la `NullPointerException` proprio quando il controllo sarebbe servito: la `length()` viene chiamata *prima* di scoprire che `s` è `null`. La stessa logica spiega l'abitudine del Capitolo 3 (sezione 3.4.1) di scrivere il letterale per primo, `"ciao".equals(s)`: il letterale non è mai `null`, quindi il confronto non può fallire.

### 8.3.4 `null` come "nessun risultato"

Quando un metodo può non avere un risultato da restituire, una convenzione molto diffusa è restituire `null`. La traccia di un esercizio lo può imporre in modo esplicito ("in caso di fallimento il metodo restituisce `null`"). Chi riceve il risultato deve però ricordarsi che può mancare, e controllare. Il programma seguente cerca un giocatore per nome in un array parzialmente riempito (sezione 5.3) di oggetti.

```java
class Giocatore {
    private String nome;
    private int punti;

    public Giocatore(String nome, int punti) {
        this.nome = nome;
        this.punti = punti;
    }

    public String getNome() {
        return nome;
    }

    public int getPunti() {
        return punti;
    }
}

class Squadra {
    private Giocatore[] rosa = new Giocatore[5];   // cinque caselle, tutte a null
    private int quanti = 0;                        // quante sono occupate

    public void aggiungi(Giocatore g) {
        if (quanti < rosa.length) {
            rosa[quanti] = g;
            quanti++;
        }
    }

    public Giocatore trova(String nome) {
        for (int i = 0; i < quanti; i++) {         // si scorrono solo le caselle occupate
            if (rosa[i].getNome().equals(nome)) {
                return rosa[i];
            }
        }
        return null;                               // nessun giocatore con quel nome
    }
}

public class Ricerca {
    public static void main(String[] args) {
        Squadra s = new Squadra();
        s.aggiungi(new Giocatore("Ada", 12));
        s.aggiungi(new Giocatore("Bruno", 7));

        Giocatore g = s.trova("Bruno");
        if (g != null) {
            System.out.println(g.getNome() + ": " + g.getPunti());
        } else {
            System.out.println("Bruno: non trovato");
        }

        Giocatore h = s.trova("Carla");
        if (h != null) {
            System.out.println(h.getNome() + ": " + h.getPunti());
        } else {
            System.out.println("Carla: non trovata");
        }
    }
}
```

```text
Bruno: 7
Carla: non trovata
```

Il ciclo di `trova` scorre `quanti` caselle e non `rosa.length`: le ultime tre caselle contengono `null`, e `rosa[3].getNome()` lancerebbe una `NullPointerException`. È l'errore tipico degli array di oggetti, di cui abbiamo parlato nel Capitolo 5 (sezione 5.8): l'array contiene *posti* per oggetti, non oggetti. Nel `main`, la chiamata `s.trova("Carla")` restituisce `null`, e `h.getNome()` senza il controllo avrebbe lo stesso effetto.

> [!IMPORTANT]
> **Nota per l'esame — `null` letterale**
> Se la traccia dice che un metodo "restituisce `null`" in un certo caso, quel caso va risolto con l'istruzione `return null;`. Restituire una stringa vuota, la stringa `"null"` o un oggetto "vuoto" costruito con `new` produce un output diverso (e, per un tester che confronta con `null`, un esito sbagliato). Quando invece è la traccia a dire che un risultato è sempre presente, non serve riempire il codice di controlli: i controlli vanno dove il testo li giustifica.

## 8.4 Uguali o identici: `==` e `equals`

### 8.4.1 `==` confronta i riferimenti

Tra due variabili di tipo primitivo, `==` confronta i valori. Tra due variabili di tipo riferimento `==` fa la stessa cosa che ha sempre fatto, cioè **confronta il contenuto delle variabili**; ma il contenuto, ora, è un indirizzo. `p == q` è quindi vero se e solo se `p` e `q` **indicano lo stesso oggetto**, e non dice nulla sui valori che gli oggetti contengono.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }
}

public class Identici {
    public static void main(String[] args) {
        Punto p = new Punto(2, 3);
        Punto q = new Punto(2, 3);       // stessi valori, ma è un altro oggetto
        Punto r = p;                     // stesso oggetto, secondo nome

        System.out.println(p == q);
        System.out.println(p == r);
    }
}
```

```text
false
true
```

Due oggetti con gli stessi dati, ma creati da due `new` distinti, non sono la stessa cosa: sono due riquadri separati nello heap, con due indirizzi diversi, e `p == q` è `false`. Per distinguere i due concetti si usa un vocabolario preciso:

- due variabili sono **identiche** quando indicano *lo stesso oggetto* (`p == r`): è la domanda a cui risponde `==`;
- due oggetti sono **uguali** quando hanno lo stesso *contenuto*, secondo un criterio deciso da chi ha scritto la classe: è la domanda a cui risponde il metodo `equals`.

Due oggetti identici sono sempre uguali; due oggetti uguali non sono necessariamente identici.

### 8.4.2 Il metodo `equals`

Le stringhe lo mostrano già: `s1.equals(s2)` confronta il testo (Capitolo 3, sezione 3.4.1). Quel metodo, però, è stato scritto da chi ha scritto la classe `String`. Per una classe nostra, come `Punto`, Java non può indovinare quali campi contino nell'uguaglianza: due conti correnti sono uguali se hanno lo stesso titolare, oppure lo stesso numero? Ogni classe nasce con un metodo `equals` ereditato dalla classe `Object` (di cui si parla nel [Capitolo 9](09-ereditarieta-e-polimorfismo.md)), ma quel metodo non fa niente di più di `==`.

> [!NOTE]
> **Approfondimento esterno — `Object.equals`**
> La Javadoc di `java.lang.Object` dichiara `public boolean equals(Object obj)` e dice che "indicates whether some other object is 'equal to' this one". Per la classe `Object` il metodo "implements the most discriminating possible equivalence relation on objects", cioè restituisce `true` se e solo se `x` e `y` "refer to the same object (`x == y` has the value `true`)". Un `equals` ben scritto deve inoltre restituire `false` quando riceve `null`: "for any non-null reference value `x`, `x.equals(null)` should return `false`". Le altre proprietà che la documentazione richiede (riflessività, simmetria, transitività, coerenza) e la regola che lega `equals` a `hashCode` sono trattate nel Capitolo 9.
>
> *Fonte:* [java.lang.Object#equals (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#equals(java.lang.Object))

Per una nostra classe, dunque, `a.equals(b)` senza altro lavoro equivale ad `a == b`: anche `Punto(2, 3)` e `Punto(2, 3)` risultano diversi. Se il confronto sul contenuto serve, va **scritto** nella classe.

### 8.4.3 Scrivere un metodo `equals`

Un metodo di confronto sul contenuto è un metodo `boolean` (come quelli del Capitolo 7, sezione 7.1.7) che riceve **un altro oggetto della stessa classe** e restituisce `true` se i suoi campi coincidono con quelli dell'oggetto su cui è chiamato. Scriviamo `equals` per una classe `Specie` con due campi, un nome e una popolazione.

```java
class Specie {
    private String nome;
    private int popolazione;

    public Specie(String nome, int popolazione) {
        this.nome = nome;
        this.popolazione = popolazione;
    }

    public boolean equals(Specie altra) {
        return altra != null                      // 1. se manca l'altro oggetto, non può essere uguale
            && nome.equals(altra.nome)            // 2. campo String: con equals, non con ==
            && popolazione == altra.popolazione;  // 3. campo int: con ==
    }
}

public class ProvaEquals {
    public static void main(String[] args) {
        Specie a = new Specie("Lupo", 40);
        Specie b = new Specie("Lupo", 40);
        Specie c = new Specie("Orso", 40);

        System.out.println(a == b);              // identici?
        System.out.println(a.equals(b));         // uguali?
        System.out.println(a.equals(c));
        System.out.println(a.equals(null));
    }
}
```

```text
false
true
false
false
```

Riga per riga. L'intestazione `public boolean equals(Specie altra)` dice che il metodo si chiama su una `Specie` (`a.equals(…)`) e riceve un'altra `Specie`. Dentro il metodo, `nome` e `popolazione` sono i campi dell'oggetto su cui è stato chiamato (`a`), mentre `altra.nome` e `altra.popolazione` sono i campi dell'oggetto ricevuto. Possiamo leggere `altra.nome` anche se `nome` è `private`, perché `private` limita l'accesso al **codice della classe**, non al singolo oggetto (Capitolo 7, sezione 7.1.7). Il `return` unisce le condizioni con `&&`: la prima, `altra != null`, protegge da una chiamata come `a.equals(null)` (ultima riga del `main`); le altre confrontano i campi, con `equals` per il campo `String` e con `==` per il campo `int`.

Due regole per scegliere l'operatore su ciascun campo:

- campo di **tipo primitivo**: si confronta con `==`;
- campo di **tipo riferimento** (come `String`): si confronta con `equals`, perché `==` confronterebbe gli indirizzi dei due oggetti, non il testo.

> [!WARNING]
> **Attenzione — I campi `double`**
> Se un campo è un `double`, il confronto con `==` richiede cautela: due valori ottenuti con calcoli diversi possono differire per un'inezia (è l'errore tipico del Capitolo 2: confrontare due `double` con `==`). Se il criterio di uguaglianza della traccia non è esatto, il confronto va fatto con una tolleranza.

> [!WARNING]
> **Attenzione — Questo `equals` non è ancora quello definitivo**
> Il metodo di questa sezione ha il parametro di tipo `Specie`. In Java il metodo `equals` ereditato da `Object` ha invece il parametro di tipo `Object`, e un metodo con un parametro diverso non lo *sostituisce*: ne è un secondo, indipendente, che convive con quello ereditato (si chiama *overloading*, Capitolo 6, sezione 6.7). Basta dichiarare la stessa specie con tipo `Object` per accorgersene.

```java
class Specie {
    private String nome;
    private int popolazione;

    public Specie(String nome, int popolazione) {
        this.nome = nome;
        this.popolazione = popolazione;
    }

    public boolean equals(Specie altra) {
        return altra != null && nome.equals(altra.nome) && popolazione == altra.popolazione;
    }
}

public class LaTrappola {
    public static void main(String[] args) {
        Specie a = new Specie("Lupo", 40);
        Specie b = new Specie("Lupo", 40);
        Object o = new Specie("Lupo", 40);       // stessa cosa, ma vista come Object

        System.out.println(a.equals(b));          // sceglie equals(Specie): il nostro
        System.out.println(a.equals(o));          // sceglie equals(Object): quello ereditato
    }
}
```

```text
true
false
```

La scelta tra i due metodi la fa il compilatore, in base al **tipo con cui l'argomento è dichiarato**. Con `o` dichiarato `Object` viene scelto il metodo ereditato, che confronta gli indirizzi, e il risultato è `false` anche se il contenuto è lo stesso. Le classi della libreria (per esempio le collezioni del Capitolo 12) chiamano sempre `equals(Object)`: perché un nostro confronto funzioni anche lì, l'`equals` deve avere il parametro di tipo `Object`, e questo è il tema del Capitolo 9. In questo capitolo scriviamo `equals` con il parametro di tipo della classe, perché è la forma più semplice per capire che cosa deve controllare.

### 8.4.4 Che cosa confrontano `==` e `equals` nei vari tipi

Ora possiamo mettere in ordine tutto ciò che abbiamo visto nei capitoli precedenti.

| Che cosa si confronta | `==` | `equals` |
|---|---|---|
| Due `int`, `double`, `boolean`, `char` | i valori | non esiste (un primitivo non ha metodi) |
| Due `String` | gli indirizzi (anche se il testo è uguale) | il testo (sezione 3.4.1) |
| Due array | gli indirizzi | ancora gli indirizzi; per il contenuto `Arrays.equals` (sezione 5.4.3) |
| Due oggetti wrapper (`Integer`…) | gli indirizzi (la cache per i valori piccoli può ingannare) | il valore (sezione 6.6.5) |
| Due oggetti di una nostra classe senza `equals` scritto | gli indirizzi | ancora gli indirizzi |
| Due oggetti di una nostra classe con `equals` scritto | gli indirizzi | il criterio scritto nella classe |
| Una variabile di riferimento e `null` | `p == null` è il modo giusto di chiedere se manca | `p.equals(null)` è `false` se `p` esiste, e `NullPointerException` se `p` è `null` |

L'ultima riga merita un commento. Per sapere se un riferimento è `null` si usa **sempre** `==`. Scrivere `if (p.equals(null))` non è un controllo: se `p` è `null` lancia l'errore che si voleva evitare, e se `p` esiste restituisce comunque `false`.

### 8.4.5 Stesso contenuto, altro oggetto: gli oggetti che viaggiano

Il confronto tra identità e uguaglianza si presenta in modo concreto ogni volta che un oggetto **viene ricostruito**. Se un oggetto viene scritto su un file e riletto, oppure inviato su una connessione di rete e ricevuto dall'altra parte (capitoli [15](15-stream-binari-e-serializzazione.md) e [19](19-networking.md)), ciò che arriva a destinazione è un **oggetto nuovo**, creato con gli stessi valori nei campi, in un'altra zona di memoria (in un altro programma, addirittura in un'altra macchina). L'oggetto di partenza e quello di arrivo non sono mai identici, e non sono nemmeno uguali nel senso di `equals`, a meno che la classe non abbia un suo `equals`. Quello che si può verificare è il contenuto: per esempio, stampare i campi.

È proprio il caso della traccia che compare nella sezione "Come esce all'esame": il server rimanda l'oggetto "identico", e ciò che si controlla è che la stampa dell'oggetto ricevuto mostri gli stessi valori, non che sia lo stesso oggetto.

## 8.5 Oggetti e parametri dei metodi

### 8.5.1 Il valore che si copia è l'indirizzo

Nel Capitolo 6 (sezione 6.3.2) abbiamo stabilito che in Java il passaggio dei parametri avviene **sempre per valore**: al momento della chiamata il valore dell'argomento viene copiato nel parametro formale. Per un `int` si copia il numero; per un oggetto si copia il **riferimento**, cioè l'indirizzo. Lo stesso vale per gli array. Dopo la chiamata ci sono due variabili, quella del chiamante e il parametro del metodo, che indicano **lo stesso oggetto**.

Le conseguenze sono due, e vale la pena tenerle in testa insieme:

- il metodo **può modificare l'oggetto** a cui il parametro si riferisce, e il chiamante vede la modifica, perché l'oggetto è uno solo;
- il metodo **non può cambiare a quale oggetto punta la variabile del chiamante**: assegnare qualcosa al parametro cambia soltanto la copia locale dell'indirizzo, che sparisce con il frame del metodo.

Sono le due operazioni della sezione 8.2.2 (modificare l'oggetto, cambiare la freccia), viste dalla parte di un metodo.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

public class Parametri {
    static void azzeraNumero(int n) {
        n = 0;                               // cambia la copia locale del numero
    }

    static void spostaPunto(Punto p) {
        p.sposta(1, 1);                      // segue la freccia e modifica l'oggetto
    }

    static void sostituisciPunto(Punto p) {
        p = new Punto(0, 0);                 // cambia solo la freccia locale
    }

    public static void main(String[] args) {
        int k = 5;
        azzeraNumero(k);
        System.out.println("k = " + k);

        Punto a = new Punto(5, 5);
        spostaPunto(a);
        System.out.println(a.descrivi());

        sostituisciPunto(a);
        System.out.println(a.descrivi());
    }
}
```

```text
k = 5
(6, 6)
(6, 6)
```

`azzeraNumero(k)` non cambia `k`: il parametro `n` è una copia del numero. `spostaPunto(a)` cambia il punto: il parametro `p` e la variabile `a` indicano lo stesso oggetto, e `p.sposta(1, 1)` lo modifica davvero. `sostituisciPunto(a)` non ha nessun effetto visibile: dentro il metodo `p` viene fatto puntare a un oggetto nuovo, ma `a` nel `main` continua a puntare al vecchio. Ecco il disegno nel momento in cui `sostituisciPunto` ha eseguito la sua unica riga:

```text
       STACK                                HEAP
   frame di main
   +----------------+                   +--------------+
   | k = 5          |          +------->| (6, 6)       |
   | a   *----------|----------+        +--------------+
   +----------------+
   frame di sostituisciPunto
   +----------------+                   +--------------+
   | p   *----------|------------------>| (0, 0)       |
   +----------------+                   +--------------+
```

Il parametro `p` è nato con la stessa freccia di `a` (come dice la regola della copia), poi l'assegnamento l'ha spostata sul nuovo oggetto. Quando il metodo termina il suo frame viene tolto: la freccia di `p` sparisce, e l'oggetto `(0, 0)` non è più indicato da nessuno.

### 8.5.2 Che cosa può e che cosa non può fare un metodo

| Il metodo riceve un oggetto `p` e… | Il chiamante se ne accorge? |
|---|---|
| chiama un metodo che cambia i campi (`p.sposta(1, 1)`) | sì |
| assegna un campo accessibile (`p.campo = …`) | sì |
| assegna un nuovo oggetto al parametro (`p = new …`) | no |
| assegna `null` al parametro (`p = null`) | no |

Per un oggetto **immutabile**, come una `String` (Capitolo 3, sezione 3.1.4), la prima e la seconda riga non esistono: nessun metodo può cambiare il contenuto della stringa. Per questo un metodo che riceve una `String` non può "modificare" la stringa del chiamante: può solo, al massimo, costruirne un'altra e restituirla.

### 8.5.3 Scambiare due oggetti

Una domanda classica: è possibile scrivere un metodo che scambi due oggetti? La risposta dipende da che cosa si intende per "scambiare". Scambiare i **riferimenti** non si può: il metodo riceve due copie delle frecce, le scambia tra loro, e le copie spariscono. Scambiare il **contenuto**, invece, sì: si modifica l'oggetto.

```java
class Casella {
    private int numero;

    public Casella(int numero) {
        this.numero = numero;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }
}

public class Scambio {
    static void scambiaRiferimenti(Casella x, Casella y) {
        Casella temporanea = x;
        x = y;
        y = temporanea;                      // scambia le due copie locali delle frecce
    }

    static void scambiaContenuto(Casella x, Casella y) {
        int temporaneo = x.getNumero();
        x.setNumero(y.getNumero());          // cambia gli oggetti veri
        y.setNumero(temporaneo);
    }

    public static void main(String[] args) {
        Casella a = new Casella(1);
        Casella b = new Casella(2);

        scambiaRiferimenti(a, b);
        System.out.println(a.getNumero() + " " + b.getNumero());

        scambiaContenuto(a, b);
        System.out.println(a.getNumero() + " " + b.getNumero());
    }
}
```

```text
1 2
2 1
```

Dopo `scambiaRiferimenti(a, b)` le caselle sono ancora `1 2`: nel `main` le variabili `a` e `b` non si sono mosse. Dopo `scambiaContenuto(a, b)` sono `2 1`: gli oggetti indicati da `a` e `b` sono gli stessi di prima, ma con i numeri scambiati. È lo stesso fatto che abbiamo visto con i primitivi nel Capitolo 6 (sezione 6.3.2): un metodo non può scambiare due variabili del chiamante; ma può cambiare ciò che le variabili indicano, se sono oggetti modificabili.

### 8.5.4 Un metodo che restituisce un oggetto

Anche il valore restituito da un metodo è un riferimento, e restituire un oggetto significa restituire una freccia, non una copia. Se il metodo restituisce uno dei suoi parametri, o un oggetto che un'altra parte del programma possiede, il chiamante ottiene un **alias**.

```java
class Casella {
    private int numero;

    public Casella(int numero) {
        this.numero = numero;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }
}

public class Maggiore {
    static Casella maggiore(Casella x, Casella y) {
        if (x.getNumero() >= y.getNumero()) {
            return x;                        // restituisce lo stesso oggetto ricevuto, non una copia
        }
        return y;
    }

    public static void main(String[] args) {
        Casella a = new Casella(9);
        Casella b = new Casella(4);

        Casella m = maggiore(a, b);
        m.setNumero(0);                      // m e a sono lo stesso oggetto

        System.out.println("a = " + a.getNumero() + ", b = " + b.getNumero());
    }
}
```

```text
a = 0, b = 4
```

`m` non è una nuova casella: è un altro nome per quella che `maggiore` ha scelto, cioè `a`. Azzerare `m` ha azzerato `a`. È lo stesso meccanismo della perdita di riservatezza di un `get` che restituisce un oggetto interno (Capitolo 7, sezione 7.3.7), e si risolve allo stesso modo: se il chiamante non deve poter modificare l'originale, il metodo restituisce una **copia** (sezione 8.6).

## 8.6 Copiare un oggetto

### 8.6.1 Il costruttore di copia

Quando si vuole davvero una copia, cioè un secondo oggetto indipendente con gli stessi valori, bisogna crearlo con `new` e riempirlo con i valori dell'originale. Il modo più naturale è un **costruttore di copia** (*copy constructor*): un costruttore in overload (Capitolo 7, sezione 7.2.4) che riceve un oggetto della stessa classe e ne copia i campi. Si può scrivere riusando l'altro costruttore con `this(...)` (sezione 7.2.5).

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Punto(Punto altro) {                  // costruttore di copia
        this(altro.x, altro.y);                  // riusa il costruttore principale
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

public class CopiaPunto {
    public static void main(String[] args) {
        Punto p = new Punto(1, 2);
        Punto copia = new Punto(p);              // un oggetto nuovo, con gli stessi valori
        Punto alias = p;                         // lo stesso oggetto

        copia.sposta(10, 10);
        alias.sposta(100, 100);

        System.out.println("p     = " + p.descrivi());
        System.out.println("copia = " + copia.descrivi());
    }
}
```

```text
p     = (101, 102)
copia = (11, 12)
```

La differenza tra `copia` e `alias` è l'intera sezione 8.2 in una riga: `new Punto(p)` crea un oggetto nuovo, che ha una vita indipendente (spostarlo non tocca `p`), mentre `Punto alias = p` crea soltanto un secondo nome per `p`. Lo spostamento fatto tramite `alias` si vede in `p`, quello fatto tramite `copia` no.

### 8.6.2 Quando la copia è solo apparente

Copiare i campi di un oggetto basta quando i campi sono primitivi o oggetti immutabili come le `String`. Se un campo è un oggetto **modificabile**, copiare il campo significa copiare un **riferimento**: l'originale e la copia, allora, si ritrovano con il campo che indica lo *stesso* oggetto, e la copia è solo apparente. Si usano due nomi per le due scelte: la copia che duplica soltanto l'oggetto esterno e lascia in comune quelli interni si dice **superficiale** (*shallow copy*); quella che duplica anche gli oggetti interni, in modo che nulla sia condiviso, si dice **profonda** (*deep copy*).

Riprendiamo il segmento della sezione 8.2.3, con due punti come campi, e scriviamo due versioni, con costruttore di copia superficiale e profondo.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Punto(Punto altro) {
        this(altro.x, altro.y);
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

class SegmentoSuperficiale {
    private Punto inizio;
    private Punto fine;

    public SegmentoSuperficiale(Punto inizio, Punto fine) {
        this.inizio = inizio;
        this.fine = fine;
    }

    public SegmentoSuperficiale(SegmentoSuperficiale altro) {
        this.inizio = altro.inizio;              // copia i riferimenti: i punti restano gli stessi
        this.fine = altro.fine;
    }

    public void spostaFine(int dx, int dy) {
        fine.sposta(dx, dy);
    }

    public String descrivi() {
        return inizio.descrivi() + "-" + fine.descrivi();
    }
}

class SegmentoProfondo {
    private Punto inizio;
    private Punto fine;

    public SegmentoProfondo(Punto inizio, Punto fine) {
        this.inizio = new Punto(inizio);         // copia anche i punti ricevuti
        this.fine = new Punto(fine);
    }

    public SegmentoProfondo(SegmentoProfondo altro) {
        this.inizio = new Punto(altro.inizio);   // un nuovo punto per ciascun campo
        this.fine = new Punto(altro.fine);
    }

    public void spostaFine(int dx, int dy) {
        fine.sposta(dx, dy);
    }

    public String descrivi() {
        return inizio.descrivi() + "-" + fine.descrivi();
    }
}

public class CopiaSegmento {
    public static void main(String[] args) {
        SegmentoSuperficiale s1 = new SegmentoSuperficiale(new Punto(0, 0), new Punto(1, 1));
        SegmentoSuperficiale s2 = new SegmentoSuperficiale(s1);
        s1.spostaFine(5, 5);
        System.out.println("superficiale: " + s1.descrivi() + " " + s2.descrivi());

        SegmentoProfondo t1 = new SegmentoProfondo(new Punto(0, 0), new Punto(1, 1));
        SegmentoProfondo t2 = new SegmentoProfondo(t1);
        t1.spostaFine(5, 5);
        System.out.println("profonda:     " + t1.descrivi() + " " + t2.descrivi());
    }
}
```

```text
superficiale: (0, 0)-(6, 6) (0, 0)-(6, 6)
profonda:     (0, 0)-(6, 6) (0, 0)-(1, 1)
```

Nel caso superficiale `s2` è un oggetto `SegmentoSuperficiale` distinto da `s1`, ma i suoi campi `inizio` e `fine` indicano gli **stessi** punti di `s1`. Spostare la fine di `s1` sposta anche quella di `s2`. Nel caso profondo ogni segmento ha i suoi punti: `t2` non si accorge di nulla. Il primo costruttore di `SegmentoProfondo` copia anche i punti ricevuti come argomento: così non si perde la riservatezza in ingresso (sezione 7.3.7), perché il chiamante che conserva i suoi `Punto` non può più modificare il segmento attraverso di essi.

### 8.6.3 Copiare un array di oggetti

Un array è un oggetto che contiene riferimenti, quindi lo stesso ragionamento vale a due livelli. I metodi di copia degli array visti nel Capitolo 5 (sezione 5.4.4) copiano **gli elementi**, e gli elementi di un array di oggetti sono frecce: la copia ottenuta con `Arrays.copyOf` è un nuovo array le cui caselle indicano gli stessi oggetti dell'originale. Per una copia indipendente bisogna creare un oggetto nuovo per ogni casella.

```java
import java.util.Arrays;

class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Punto(Punto altro) {
        this(altro.x, altro.y);
    }

    public void sposta(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

public class CopiaArray {
    public static void main(String[] args) {
        Punto[] originali = {new Punto(0, 0), new Punto(1, 1)};

        Punto[] soloFrecce = Arrays.copyOf(originali, originali.length);   // nuovo array, stessi punti
        soloFrecce[0].sposta(5, 5);
        System.out.println(originali[0].descrivi());                       // cambiato anche l'originale

        Punto[] copiaVera = new Punto[originali.length];
        for (int i = 0; i < originali.length; i++) {
            copiaVera[i] = new Punto(originali[i]);                        // un punto nuovo per casella
        }
        copiaVera[1].sposta(7, 7);
        System.out.println(originali[1].descrivi());                       // l'originale non cambia
    }
}
```

```text
(5, 5)
(1, 1)
```

La regola per ricordare tutto questo è una sola: **un assegnamento, un passaggio di parametri, un `copyOf` o un costruttore che memorizza ciò che riceve copiano frecce; per avere oggetti nuovi serve un `new` per ogni oggetto che non deve essere condiviso.**

## 8.7 Vita e morte degli oggetti

### 8.7.1 Quanto vive una variabile locale

Una variabile locale e un parametro esistono finché il metodo che li contiene è in esecuzione: nascono nel frame creato alla chiamata e spariscono con esso al termine del metodo (sezione 8.1.3). Questo vale anche per le variabili di tipo riferimento, ma la sparizione riguarda **la freccia, non l'oggetto**. L'oggetto continua a vivere nello heap finché qualcuno può ancora raggiungerlo.

Un metodo può quindi creare un oggetto e "consegnarlo" al chiamante restituendolo: la variabile locale del metodo sparisce, l'oggetto no, perché il valore restituito è una nuova freccia verso di esso.

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public String descrivi() {
        return "(" + x + ", " + y + ")";
    }
}

public class Consegna {
    static Punto creaOrigine() {
        Punto locale = new Punto(0, 0);          // 'locale' vive solo durante la chiamata
        return locale;                           // l'oggetto, invece, esce dal metodo
    }

    public static void main(String[] args) {
        Punto o = creaOrigine();                 // il frame di creaOrigine non c'è più
        System.out.println(o.descrivi());        // l'oggetto sì
    }
}
```

```text
(0, 0)
```

### 8.7.2 L'oggetto irraggiungibile

Un oggetto resta nello heap finché è **raggiungibile**, cioè finché esiste almeno una catena di frecce che parte da una variabile viva (una variabile locale di un metodo in esecuzione, un campo statico, un campo di un oggetto a sua volta raggiungibile) e arriva a lui. Quando l'ultima freccia scompare, nessuno potrà più usare l'oggetto: è diventato spazzatura (*garbage*). Può succedere in tre modi:

- si **riassegna** l'unica variabile che lo indicava (`p = new Punto(…)` oppure `p = null`);
- il **frame** della variabile che lo indicava viene tolto, perché il metodo è terminato;
- l'oggetto era indicato **dal campo** di un altro oggetto che a sua volta è diventato irraggiungibile.

Il terzo caso si vede bene con una catena di oggetti in cui ciascuno indica il successivo. È la struttura chiamata *lista concatenata*, e il programma ha una sola variabile, `testa`, che indica il primo oggetto; da lì si raggiungono tutti gli altri.

```java
class Nodo {
    private String dato;
    private Nodo successivo;

    public Nodo(String dato, Nodo successivo) {
        this.dato = dato;
        this.successivo = successivo;
    }

    public String getDato() {
        return dato;
    }

    public Nodo getSuccessivo() {
        return successivo;
    }
}

public class Catena {
    public static void main(String[] args) {
        Nodo c = new Nodo("C", null);            // l'ultimo non ha un successivo
        Nodo b = new Nodo("B", c);
        Nodo testa = new Nodo("A", b);           // testa -> A -> B -> C

        b = null;
        c = null;                                // B e C restano raggiungibili passando da A

        testa = testa.getSuccessivo();           // ora testa -> B: nessuno indica più A

        for (Nodo n = testa; n != null; n = n.getSuccessivo()) {
            System.out.println(n.getDato());
        }
    }
}
```

```text
B
C
```

All'inizio tre oggetti sono indicati da `c`, `b` e `testa`. Con `b = null` e `c = null` le variabili `b` e `c` non indicano più niente, ma gli oggetti `B` e `C` sono ancora raggiungibili: `testa` indica `A`, il campo `successivo` di `A` indica `B`, il campo `successivo` di `B` indica `C`. Con `testa = testa.getSuccessivo()` la variabile `testa` passa a indicare `B`, e **nessuna freccia arriva più ad `A`**: `A` è irraggiungibile. Il ciclo `for` finale mostra l'uso più comune di `null` in una struttura simile, la condizione `n != null` che dice "mi fermo quando non c'è più un successivo".

### 8.7.3 Il garbage collector

In molti linguaggi chi crea un oggetto deve anche liberare la memoria che occupa; dimenticarsene fa consumare memoria senza ritegno, liberare un oggetto ancora in uso provoca errori difficili da trovare. Java toglie questa responsabilità al programmatore: non esiste nessuna istruzione per "distruggere" un oggetto. Un componente della JVM, il **garbage collector** (*raccoglitore di rifiuti*), controlla periodicamente lo heap, individua gli oggetti irraggiungibili e ne **restituisce la memoria** al sistema.

> [!NOTE]
> **Definizione — Garbage collector**
> Il **garbage collector** è il componente della JVM che recupera automaticamente la memoria occupata dagli oggetti dello heap diventati irraggiungibili. Il programmatore non lo invoca e non decide quando agisce.

> [!NOTE]
> **Approfondimento esterno — `Runtime.gc` e `System.gc`**
> La classe `java.lang.Runtime` ha il metodo `public void gc()`, e `System.gc()` ne è "the conventional and convenient means of invoking". La documentazione dice che chiamarlo "suggests that the Java Virtual Machine expend effort toward recycling unused objects": è un suggerimento, e "there is no guarantee" che il recupero riguardi un certo numero di oggetti o avvenga in un certo momento. Aggiunge che "the Java Virtual Machine performs this recycling process automatically as needed, in a separate thread, even if the `gc` method is not invoked explicitly".
>
> *Fonte:* [java.lang.Runtime#gc (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Runtime.html#gc())

La conseguenza pratica è che negli esercizi non ci si occupa mai della liberazione della memoria. Non esiste "l'istruzione che cancella l'oggetto": `p = null` toglie una freccia, e l'oggetto sparisce solo se era l'ultima. Non si può nemmeno prevedere *quando* un oggetto irraggiungibile verrà raccolto, perciò un programma non deve basare la propria logica su di esso.

### 8.7.4 Un solo heap, più stack

Il Capitolo 1 (sezione 1.9) lo ha anticipato: nello schema delle zone di memoria della JVM ogni thread ha il proprio stack, mentre lo heap è uno solo. Possiamo ora dire che cosa significa. Ogni thread ha i propri frame, e quindi le proprie variabili locali: due thread non si scambiano per errore le variabili locali di un metodo. Se però due thread hanno una **freccia verso lo stesso oggetto** (per esempio perché ricevono tutti e due lo stesso riferimento nel costruttore), quell'oggetto è condiviso, e le modifiche di uno si vedono dall'altro, con tutti i problemi che ne seguono. Il [Capitolo 17 — Thread](17-thread.md) e il [Capitolo 18 — Sincronizzazione](18-sincronizzazione.md) ripartono da qui.

## Come esce all'esame

**Appello dell'8 luglio 2026 (EXAM3) — Esercizio 3 (13 punti), serializzazione di oggetti su socket.** La traccia presentava un server già in ascolto, da non scrivere, che riceve un oggetto, lo rimanda indietro identico sulla stessa connessione e chiude, con indirizzo e porta forniti. Chiedeva tre cose. Primo, una classe `Persona` il cui costruttore riceve nell'ordine nome e cognome (entrambi testuali), con i rispettivi metodi di lettura, **tutte le variabili d'istanza private**, convertibile in una sequenza di byte e ricostruibile altrove, con una costante di versione di tipo `long` pari a `1`, e con rappresentazione testuale nella forma `Persona[Mario Rossi]`. Secondo, una classe `Client` con un metodo `invia` che riceve una persona e ne restituisce una: apre la connessione verso le coordinate indicate, trasmette l'oggetto ricevuto come parametro, attende l'oggetto rimandato dal server, lo ricostruisce e lo restituisce. Terzo, "in caso di fallimento della comunicazione il metodo restituisce `null`". L'output atteso, inviando `new Persona("Mario", "Rossi")`, era `Persona[Mario Rossi]`.

Del capitolo servono tre idee. La prima: l'oggetto restituito da `invia` è un **oggetto nuovo**, costruito leggendo i byte arrivati dalla rete, con gli stessi valori di quello inviato ma un'altra identità (sezione 8.4.5): non ha senso aspettarsi che sia lo stesso oggetto, né confrontarlo con `==`; il test verifica la stampa del suo contenuto. La seconda: il valore di ritorno nel caso di errore è il **`null` letterale** (sezione 8.3.4), e il codice che chiama `invia` deve poter controllare che il risultato non sia `null` prima di usarlo (sezione 8.3.3). La terza, di sfondo: i campi `private` con costruttore nell'ordine richiesto e i metodi di lettura sono quelli del [Capitolo 7](07-classi-e-oggetti.md). La serializzazione e la costante di versione sono nel [Capitolo 15](15-stream-binari-e-serializzazione.md), i socket nel [Capitolo 19](19-networking.md), la rappresentazione testuale `Persona[Mario Rossi]` nel [Capitolo 9](09-ereditarieta-e-polimorfismo.md). Vincoli letterali: il nome `invia`, la costante `long` di valore `1`, `null` e non altro in caso di fallimento, il formato esatto della stringa `Persona[Mario Rossi]`.

## Scheletri da esame

### Un metodo che confronta il contenuto di due oggetti

*Quando si usa:* la traccia chiede di "confrontare due oggetti" in base ai valori dei loro campi. La forma qui è quella con il parametro della classe (sezione 8.4.3); la forma con il parametro `Object`, richiesta dalle collezioni, è nel Capitolo 9.

```java
class Persona {
    private String nome;
    private String cognome;

    public Persona(String nome, String cognome) {
        this.nome = nome;
        this.cognome = cognome;
    }

    public boolean equals(Persona altra) {
        return altra != null                       // un altro oggetto esiste?
            && nome.equals(altra.nome)             // campi String con equals, mai ==
            && cognome.equals(altra.cognome);      // altri campi primitivi: con ==
    }
}
```

Non servono import né eccezioni da dichiarare. Se un campo può essere `null`, `nome.equals(…)` lancia una `NullPointerException`: in quel caso si controlla `nome != null` oppure si usa un metodo ausiliario.

### Una ricerca che restituisce `null` e il controllo del chiamante

*Quando si usa:* la traccia dice "restituisce l'oggetto trovato, oppure `null`".

```java
class Persona {
    private String nome;
    private String cognome;

    public Persona(String nome, String cognome) {
        this.nome = nome;
        this.cognome = cognome;
    }

    public String getCognome() {
        return cognome;
    }
}

class Elenco {
    // v: array parzialmente riempito; quanti: numero di caselle occupate
    static Persona cerca(Persona[] v, int quanti, String cognome) {
        for (int i = 0; i < quanti; i++) {          // solo le caselle occupate, non v.length
            if (v[i].getCognome().equals(cognome)) {
                return v[i];                        // trovata: restituisce l'oggetto, non una copia
            }
        }
        return null;                                // non trovata: null letterale
    }

    public static void main(String[] args) {
        Persona[] v = new Persona[3];
        v[0] = new Persona("Ada", "Rossi");
        Persona p = cerca(v, 1, "Verdi");
        if (p != null) {                            // il chiamante controlla prima di usare
            System.out.println(p.getCognome());
        } else {
            System.out.println("non trovata");
        }
    }
}
```

Nessun import né eccezione. Se la traccia dà l'array già completamente riempito, il ciclo si scrive con `v.length`; se alcune caselle possono essere `null`, nel ciclo va aggiunto `v[i] != null &&` prima di usare l'elemento.

### Un costruttore di copia e una copia difensiva

*Quando si usa:* la traccia chiede che una classe non "esponga" né "condivida" oggetti modificabili, oppure che un oggetto sia "copiato" in modo indipendente.

```java
class Persona {
    private String nome;
    private String cognome;

    public Persona(String nome, String cognome) {
        this.nome = nome;
        this.cognome = cognome;
    }

    public Persona(Persona altra) {                // costruttore di copia
        this(altra.nome, altra.cognome);
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }
}

class Incarico {
    private Persona responsabile;

    public Incarico(Persona responsabile) {
        this.responsabile = new Persona(responsabile);   // in ingresso: copia, non memorizza l'originale
    }

    public Persona getResponsabile() {
        return new Persona(responsabile);                // in uscita: copia, non restituisce l'originale
    }
}
```

Non servono import. Per gli oggetti **immutabili** (una `String`) la copia non è necessaria; per i campi che sono a loro volta oggetti modificabili il costruttore di copia deve copiare anche quelli (sezione 8.6.2).

### Un array di oggetti: `new` per ogni casella e controllo di `null`

*Quando si usa:* la traccia chiede un array di oggetti "riempito" con alcuni elementi e poi percorso.

```java
class Persona {
    private String cognome;

    public Persona(String cognome) {
        this.cognome = cognome;
    }

    public String getCognome() {
        return cognome;
    }
}

public class ProvaArray {
    public static void main(String[] args) {
        Persona[] v = new Persona[4];              // quattro caselle, tutte null: nessuna persona
        v[0] = new Persona("Rossi");               // una new per ogni casella da riempire
        v[1] = new Persona("Verdi");

        for (int i = 0; i < v.length; i++) {
            if (v[i] != null) {                    // le caselle vuote valgono null
                System.out.println(v[i].getCognome());
            }
        }
    }
}
```

Nessun import. Se l'array è tenuto insieme a un contatore, il ciclo scorre il contatore (come nel secondo scheletro) e il controllo `!= null` non serve.

### Un metodo che modifica l'oggetto ricevuto

*Quando si usa:* la traccia chiede un metodo che "modifica" o "scambia" i contenuti di due oggetti passati come parametri.

```java
class Casella {
    private int numero;

    public Casella(int numero) {
        this.numero = numero;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }
}

class Utilita {
    static void scambiaContenuto(Casella x, Casella y) {
        int temporaneo = x.getNumero();            // si lavora sul contenuto, non sulle frecce
        x.setNumero(y.getNumero());
        y.setNumero(temporaneo);
    }
}
```

Nessun import. Un metodo che scambiasse i **riferimenti** (`Casella t = x; x = y; y = t;`) compilerebbe ma non avrebbe nessun effetto per il chiamante (sezione 8.5.3).

## Errori tipici

Alcuni errori sono già discussi nel testo: usare `==` al posto di `equals` sulle stringhe (Capitolo 3, sezione 3.4.1), scorrere un array di oggetti fino a `length` quando non è pieno (sezione 8.3.4), scambiare due oggetti con un metodo che scambia i riferimenti (sezione 8.5.3), scrivere un costruttore di copia superficiale per una classe con campi modificabili (sezione 8.6.2), scrivere `equals` con il parametro della classe e chiamarlo con un argomento dichiarato `Object` (sezione 8.4.3). Seguono gli altri.

> [!CAUTION]
> **Errore tipico — Credere che `=` copi l'oggetto**
> ```java
> Punto originale = new Punto(1, 2);
> Punto copia = originale;                 // NON è una copia: è un secondo nome
> copia.sposta(10, 10);                    // sposta anche l'originale
> ```
> Il programma compila e funziona senza errori, ma `originale` e `copia` indicano lo stesso oggetto, quindi `originale` è diventato `(11, 12)`. Forma corretta: `Punto copia = new Punto(originale);`, con un costruttore di copia (sezione 8.6.1).

> [!CAUTION]
> **Errore tipico — Confrontare il contenuto con `==`**
> ```java
> Punto a = new Punto(1, 2);
> Punto b = new Punto(1, 2);
> if (a == b) {                            // mai vero: due new, due oggetti
>     System.out.println("uguali");
> }
> ```
> Il confronto è `false` anche se i campi coincidono, perché `==` confronta gli indirizzi (sezione 8.4.1). Forma corretta: `a.equals(b)`, dopo aver scritto `equals` nella classe, perché quello ereditato fa lo stesso che `==`.

> [!CAUTION]
> **Errore tipico — Confrontare un campo `String` con `==` dentro `equals`**
> ```java
> public boolean equals(Specie altra) {
>     return nome == altra.nome && popolazione == altra.popolazione;
> }
> // nel main:
> Specie a = new Specie("Lupo", 40);
> Specie b = new Specie(new String("Lupo"), 40);
> System.out.println(a.equals(b));         // false
> ```
> Con due letterali uguali il confronto può risultare `true` per un accidente (il compilatore fa condividere ai letterali lo stesso oggetto), e questo nasconde l'errore; appena una stringa nasce da `new String(...)`, da una lettura da tastiera o da un file, il confronto è `false`. Forma corretta: `nome.equals(altra.nome)`.

> [!CAUTION]
> **Errore tipico — Dimenticare il controllo di `null` in `equals`**
> ```java
> public boolean equals(Specie altra) {
>     return nome.equals(altra.nome) && popolazione == altra.popolazione;
> }
> // nel main:
> a.equals(null);                          // ERRORE A RUNTIME: NullPointerException
> ```
> `altra.nome` segue una freccia che non c'è. Un `equals` ben scritto restituisce `false` quando riceve `null` (riquadro della sezione 8.4.2). Forma corretta: iniziare il `return` con `altra != null && …`.

> [!CAUTION]
> **Errore tipico — Un campo di tipo classe mai creato**
> ```java
> class Garage {
>     private Auto auto;                   // vale null: il campo non crea nessuna Auto
>
>     public void avvia() {
>         auto.accendi();                  // ERRORE A RUNTIME: NullPointerException
>     }
> }
> ```
> Dichiarare un campo (o una variabile) di tipo classe riserva solo lo spazio per una freccia, e per un campo quel posto vale `null` (sezione 8.1.4). Forma corretta: creare l'oggetto, per esempio nel costruttore con `auto = new Auto();`, oppure ricevere nel costruttore un oggetto già creato.

> [!CAUTION]
> **Errore tipico — Usare un elemento di un array di oggetti senza averlo creato**
> ```java
> Punto[] v = new Punto[3];
> v[0].sposta(1, 1);                       // ERRORE A RUNTIME: NullPointerException
> ```
> `new Punto[3]` crea un array con tre *posti* per punti, tutti a `null` (sezione 8.3.4). Forma corretta: `v[0] = new Punto(0, 0);` prima di usare `v[0]`.

> [!CAUTION]
> **Errore tipico — Il controllo di `null` nell'ordine sbagliato**
> ```java
> if (s.length() > 0 && s != null) {       // ERRORE A RUNTIME se s è null
>     System.out.println(s);
> }
> ```
> La condizione di sinistra viene valutata per prima e, se `s` è `null`, `s.length()` lancia l'eccezione prima che il controllo possa evitarla (sezione 8.3.3). Forma corretta: `if (s != null && s.length() > 0)`.

> [!CAUTION]
> **Errore tipico — Controllare `null` con `equals`**
> ```java
> if (p.equals(null)) {                    // NON è un controllo di null
>     System.out.println("manca");
> }
> ```
> Se `p` è `null`, chiamare `equals` su di esso lancia una `NullPointerException`; se `p` esiste, `equals(null)` restituisce `false`. In nessun caso la condizione serve a qualcosa. Forma corretta: `if (p == null)`.

> [!CAUTION]
> **Errore tipico — `null` dove serve un valore primitivo**
> ```java
> int n = null;                            // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `incompatible types: <null> cannot be converted to int`. `null` è un valore di riferimento e non si può assegnare a una variabile primitiva, né restituire da un metodo che dichiara un tipo primitivo (`return null;` in un metodo `int` dà lo stesso errore). Se serve un "nessun valore" per un numero, la traccia deve prevedere un valore speciale (per esempio `-1`) oppure un tipo oggetto come `Integer`.

> [!CAUTION]
> **Errore tipico — Una variabile locale di tipo classe senza `new`**
> ```java
> Punto p;
> p.sposta(1, 1);                          // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `variable p might not have been initialized`: la dichiarazione riserva solo la variabile, nessun oggetto (sezione 8.1.4). Forma corretta: `Punto p = new Punto(0, 0);`. Per un **campo**, invece, il compilatore non protesta: il campo vale `null` e l'errore si manifesta solo in esecuzione (errore precedente).

> [!CAUTION]
> **Errore tipico — Pensare che un metodo possa sostituire l'oggetto del chiamante**
> ```java
> static void azzera(Punto p) {
>     p = new Punto(0, 0);                 // NON ha effetto per il chiamante
> }
> ```
> Il parametro è una copia della freccia: assegnarle un altro oggetto cambia solo la copia (sezione 8.5.1). Forme corrette: modificare l'oggetto con un suo metodo (`p.sposta(…)`), oppure restituire il nuovo oggetto (`static Punto azzera() { return new Punto(0, 0); }`) e far assegnare il risultato al chiamante (`p = azzera();`).

> [!CAUTION]
> **Errore tipico — Credere che `null` cancelli l'oggetto**
> ```java
> Punto p = new Punto(1, 2);
> Punto q = p;
> p = null;                                // "elimino" il punto
> System.out.println(q.descrivi());        // stampa (1, 2)
> ```
> `p = null` toglie la freccia di `p`, non distrugge l'oggetto: finché `q` lo indica, l'oggetto esiste ed è utilizzabile. L'oggetto sparisce solo quando non lo indica più nessuno (sezione 8.7.2), e quando accade lo decide il garbage collector.

> [!CAUTION]
> **Errore tipico — Contare su `System.gc()`**
> ```java
> p = null;
> System.gc();                             // "così la memoria è liberata subito"
> ```
> `System.gc()` è un suggerimento, e la Javadoc precisa che non garantisce che la memoria venga recuperata in un certo momento (sezione 8.7.3). Un programma non deve dipendere da ciò che il garbage collector fa o non fa. Negli esercizi la chiamata non serve mai.

## Riassunto

Una variabile di tipo primitivo contiene un valore; una variabile di tipo classe o array contiene un **riferimento**, cioè l'indirizzo di un oggetto che vive nello **heap**, mentre le variabili locali e i parametri dei metodi vivono nello **stack**, in un frame per ogni chiamata. Da questo modello discendono tutte le conseguenze del capitolo. L'**assegnamento** tra riferimenti copia l'indirizzo e crea un **alias**: un solo oggetto, due nomi; modificare l'oggetto si vede da entrambi, cambiare la freccia di una variabile no. Il valore **`null`** indica che una variabile non si riferisce a nessun oggetto; usarla con l'operatore punto, o come array, lancia una `NullPointerException`, che si evita controllando prima (con `!= null`, nell'ordine giusto nelle condizioni `&&`). L'operatore **`==`** confronta gli indirizzi (identità), `equals` confronta il contenuto (uguaglianza); quello ereditato da `Object` coincide con `==`, perciò per una classe nostra l'`equals` va scritto, confrontando i campi primitivi con `==` e quelli riferimento con `equals`. Un metodo che riceve un oggetto riceve una **copia della freccia**: può modificare l'oggetto, non sostituire la variabile del chiamante. Una copia vera richiede un `new` (costruttore di copia) e, se i campi sono oggetti modificabili, un `new` anche per ciascuno di essi. Un oggetto resta nello heap finché è **raggiungibile**; quando non lo è più, il **garbage collector** ne recupera la memoria da solo, senza che il programmatore possa o debba farlo.

**Concetti chiave**

- **Riferimento.** L'indirizzo di un oggetto; è ciò che una variabile di tipo classe o array contiene.
- **Stack e heap.** Lo stack contiene i frame delle chiamate, con variabili locali e parametri; lo heap contiene gli oggetti e gli array, compresi i campi primitivi dentro gli oggetti.
- **Alias.** Due variabili che indicano lo stesso oggetto; nasce da `q = p`, da un parametro, da un valore restituito.
- **Modificare l'oggetto contro cambiare la freccia.** La prima operazione vale per tutti gli alias, la seconda solo per la variabile assegnata.
- **`new`.** Crea un oggetto nuovo e ne restituisce il riferimento: ogni `new` è un oggetto distinto.
- **`null`.** Nessun oggetto; valore predefinito dei campi e degli elementi di array di tipo riferimento; non assegnabile ai primitivi; si testa con `==`.
- **`NullPointerException`.** Eccezione non controllata lanciata se si usa un riferimento `null` come oggetto o come array.
- **Identità e uguaglianza.** `==` risponde "è lo stesso oggetto?", `equals` "ha lo stesso contenuto?"; senza un `equals` scritto, i due coincidono.
- **Scrivere `equals`.** `altra != null` e poi confronto campo per campo, `==` per i primitivi, `equals` per i riferimenti.
- **Parametri oggetto.** Si copia la freccia: il metodo modifica l'oggetto ma non sostituisce la variabile del chiamante; scambiare i riferimenti non ha effetto.
- **Copia.** Costruttore di copia con `new`; copia superficiale se gli oggetti interni restano condivisi, profonda se ne vengono creati di nuovi; `Arrays.copyOf` su un array di oggetti copia le frecce.
- **Raggiungibilità e garbage collector.** Un oggetto sparisce quando non è più raggiungibile; la memoria viene recuperata automaticamente, in un momento che non si controlla.
- **Oggetto ricostruito.** Un oggetto letto da un file o da una connessione è un oggetto nuovo con gli stessi valori, non l'oggetto di partenza.

**Sintassi essenziale**

| Elemento | Forma |
|---|---|
| Creare un oggetto | `Punto p = new Punto(1, 2);` |
| Secondo nome per lo stesso oggetto | `Punto q = p;` |
| Controllare l'assenza di oggetto | `if (p == null) { … }` / `if (p != null) { … }` |
| Copia con costruttore di copia | `Punto c = new Punto(p);` |
| Confronto sul contenuto | `a.equals(b)` (dopo averlo scritto nella classe) |
| Confronto delle identità | `a == b` |
| Array di oggetti pronto all'uso | `Punto[] v = new Punto[n]; v[i] = new Punto(…);` |
| Restituire "nessun risultato" | `return null;` |

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `NullPointerException` (`java.lang`) | costruttori | `NullPointerException()`, `NullPointerException(String s)` | è essa stessa un'eccezione non controllata (`extends RuntimeException`) |
| `Object` (`java.lang`) | `equals` | `public boolean equals(Object obj)` (predefinito: identità) | — |
| `Runtime` (`java.lang`) | `gc` | `public void gc()` (suggerimento al garbage collector) | — |
| `System` (`java.lang`) | `gc` | `public static void gc()` (equivale a `Runtime.getRuntime().gc()`) | — |
| `Arrays` (`java.util`) | `copyOf` | `public static <T> T[] copyOf(T[] original, int newLength)` (copia i riferimenti; `<T>` indica un tipo qualsiasi, vedi Capitolo 12) | `NegativeArraySizeException`, `NullPointerException` |
