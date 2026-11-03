---
materia: Programmazione a Oggetti
capitolo: 5
titolo: Array e matrici
livello_syllabus: 1
stato: completo
slide: ["Savitch cap. 6 slide 4-44", "Savitch cap. 9 slide 40 (array di oggetti)"]
appelli: [EXAM2]
fonti_esterne: 6
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 5 — Array e matrici

## Di cosa parla questo capitolo

Con le variabili dei capitoli precedenti ogni valore ha un nome suo: `temperature1`, `temperature2`, e così via. Va bene per tre valori, non per cento, e non per un numero che si scopre solo quando il programma gira. Serve uno strumento che raccolga **molti valori dello stesso tipo sotto un solo nome**, e che permetta di scorrerli con un ciclo. In Java questo strumento è l'**array**.

Il capitolo si appoggia direttamente sui cicli `for` e `while` del [Capitolo 4 — Strutture di controllo](04-strutture-di-controllo.md), perché un array si usa quasi sempre insieme a un ciclo, e sul `main(String[] args)` del [Capitolo 1 — Java e la JVM](01-java-e-la-jvm.md), il cui parametro è proprio un array. Riprende anche i tipi e i valori predefiniti del [Capitolo 2 — Tipi primitivi, variabili e operatori](02-tipi-variabili-operatori.md) e le stringhe del [Capitolo 3 — Stringhe e input/output da console](03-stringhe-e-console.md), il cui metodo `split` restituisce un array.

Alla fine del capitolo saprai dichiarare, creare, riempire e percorrere un array; saprai perché `==` tra due array non confronta il contenuto e come si copia davvero un array; scriverai i metodi che ricevono e restituiscono array; saprai trovare il massimo, cercare un elemento e ordinare; userai le **matrici** (array a più dimensioni), comprese quelle con righe di lunghezza diversa; e conoscerai le insidie classiche: l'indice fuori dai limiti, l'array con gli elementi ancora `null`, l'array "copiato" che in realtà ha due nomi.

> [!IMPORTANT]
> **Array e prove scritte**
> Nelle tracce delle prove scritte l'array compare di rado come argomento dichiarato, ma spesso come **materiale da costruzione**: una classe che deve contenere "una struttura dati basata su un array primitivo con dimensione massima pari a N", un metodo che riceve un array, un `main(String[] args)`. Quando la traccia chiede un array primitivo, si usa un array primitivo: una `ArrayList` al suo posto sarebbe un'altra struttura. Vedi la sezione "Come esce all'esame".

## 5.1 Che cos'è un array

### 5.1.1 Il problema: tanti valori dello stesso tipo

Supponiamo di dover leggere le temperature di una settimana, calcolarne la media e poi elencare i giorni che stanno sopra la media. Con le sole variabili singole servirebbero sette variabili (`temperature0`, …, `temperature6`), la media si scriverebbe sommandole a mano una per una, e per ripetere lo stesso lavoro su trenta giorni bisognerebbe riscrivere tutto. Il vero guaio è che **non si può scrivere un ciclo sui nomi delle variabili**: il nome `temperature3` non si ottiene da `"temperature" + 3`.

Un array risolve il problema dando a ciascun valore un **numero** invece di un nome: un solo nome per l'insieme, `temperature`, e un numero per l'elemento, `temperature[3]`. Il numero è una normale espressione `int`, quindi può essere la variabile di un ciclo.

> [!NOTE]
> **Definizione — Array**
> Un **array** è una collezione di variabili dello stesso tipo, chiamate **elementi** (*elements*) o **variabili indicizzate** (*indexed variables*), memorizzate in sequenza sotto un unico nome. Ogni elemento si individua con un numero intero, l'**indice** (*index*). Il tipo comune degli elementi si chiama **tipo base** (*base type*) e il numero di elementi è la **lunghezza** (*length*) dell'array.

> [!TIP]
> **Intuizione — La cassettiera**
> Un array è una cassettiera con un'etichetta sola sul mobile e i cassetti numerati a partire da 0. Tutti i cassetti contengono lo stesso genere di cosa (tutti interi, oppure tutte stringhe). Per prendere qualcosa non si dice "il cassetto del martedì" ma "il cassetto numero 1". L'analogia ha un limite: i cassetti di una cassettiera si possono aggiungere, quelli di un array no. Il numero di cassetti si decide quando l'array viene creato e non cambia più (sezione 5.1.4).

### 5.1.2 Dichiarare e creare un array

Un array è un **oggetto** (lo approfondiremo nella sezione 5.4), e come ogni oggetto si crea con `new`. Servono due passi, che si possono scrivere separati o in una riga sola:

```java
double[] temperature;                  // dichiarazione: temperature è il nome di un array di double
temperature = new double[7];           // creazione: nasce un array con 7 variabili double

double[] humidity = new double[7];     // le due cose insieme
```

In forma generale:

```text
Tipo_Base[] Nome_Array = new Tipo_Base[Lunghezza];
```

Le parentesi quadre accanto al tipo (`double[]`) dicono che la variabile è un array di quel tipo. Le parentesi quadre dopo `new Tipo_Base` contengono la **lunghezza**, che può essere una qualsiasi espressione intera: una costante, una variabile, un calcolo. La lunghezza viene valutata *al momento della creazione*:

```java
int n = 5;
int[] v = new int[n * 2];              // 10 elementi
```

Il numero di elementi è deciso una volta per tutte: l'array `v` avrà sempre 10 elementi, anche se in seguito `n` cambia.

> [!NOTE]
> **Definizione — Le parentesi quadre in Java, tre usi diversi**
> Nei programmi con array le `[]` compaiono in tre ruoli che conviene distinguere:
>
> | Dove | Esempio | Significato |
> |---|---|---|
> | dopo il nome di un tipo, in una dichiarazione | `int[] pressure;` | "`pressure` è un array di `int`" |
> | dopo `new Tipo`, con un numero dentro | `pressure = new int[100];` | "crea un array con 100 elementi" |
> | dopo il nome di un array, in un'espressione | `pressure[3] = 7;` | "l'elemento di indice 3" |

#### Esempio — Le temperature della settimana

Ecco il problema di apertura risolto con un array. Per avere un esempio che si possa rieseguire senza digitare nulla, il `Scanner` legge da una stringa fissa invece che dalla tastiera (la stessa tecnica del capitolo 4: cambia solo l'argomento del costruttore).

```java
import java.util.Scanner;

public class Temperature {
    public static void main(String[] args) {
        // Scanner su una stringa fissa: l'esempio è ripetibile senza digitare nulla
        Scanner keyboard = new Scanner("18 21 19 25 24 22 20");

        int[] temperature = new int[7];          // sette variabili int, numerate da 0 a 6
        int sum = 0;
        for (int i = 0; i < temperature.length; i++) {
            temperature[i] = keyboard.nextInt(); // scrive nell'elemento i
            sum = sum + temperature[i];
        }

        double average = (double) sum / temperature.length;
        System.out.println("Media: " + average);
        for (int i = 0; i < temperature.length; i++) {
            if (temperature[i] > average) {
                System.out.println("Giorno " + i + ": " + temperature[i] + " (sopra la media)");
            }
        }
    }
}
```

Il primo ciclo riempie l'array: a ogni giro `i` vale 0, poi 1, … fino a 6, e `temperature[i] = keyboard.nextInt();` scrive il numero letto nel posto `i`. Nello stesso giro lo si aggiunge a `sum`. Il `(double)` davanti a `sum` serve perché la divisione tra due `int` darebbe un risultato intero (sezione 2.6.3). Il secondo ciclo confronta ogni elemento con la media. L'output è:

```text
Media: 21.285714285714285
Giorno 3: 25 (sopra la media)
Giorno 4: 24 (sopra la media)
Giorno 5: 22 (sopra la media)
```

Per passare da una settimana a un mese basta cambiare il `7` (e il testo letto): i cicli usano `temperature.length` e non si toccano.

### 5.1.3 Accedere agli elementi

Per leggere o scrivere un elemento si scrive il nome dell'array seguito dall'indice tra parentesi quadre. Un elemento, `temperature[3]`, si usa **ovunque si potrebbe usare una variabile del tipo base**: a sinistra di un `=`, dentro un'espressione, come argomento di un metodo, con `++`.

```java
temperature[3] = 25;                       // scrittura
int x = temperature[3] + 1;                // lettura
temperature[3]++;                          // incremento dell'elemento
```

Gli indici **cominciano da 0**. Un array di 7 elementi ha gli indici 0, 1, 2, 3, 4, 5, 6: il primo elemento è `temperature[0]`, l'ultimo è `temperature[6]`, e `temperature[7]` non esiste. La regola da ricordare è che l'ultimo indice valido è sempre **lunghezza − 1**.

> [!TIP]
> **Intuizione — L'indice è una distanza, non una posizione**
> L'indice conta quanti elementi bisogna saltare partendo dal primo. Il primo elemento dista 0 posti da sé stesso, per questo ha indice 0. È la stessa convenzione degli indici delle stringhe (sezione 3.1.3).

Il docente suggerisce di abituarsi a usare l'indice 0, senza "sprecare" l'elemento 0 per far coincidere i numeri con quelli del problema (per esempio usare 1-7 per i giorni della settimana). Sembra più comodo, ma rende il programma più difficile da leggere e da controllare.

### 5.1.4 La variabile length

Ogni array ha una sola variabile pubblica, `length`, che contiene il numero dei suoi elementi. Si scrive **senza parentesi tonde**: `temperature.length`, non `temperature.length()`. È **final**: si può leggere, ma non assegnarle un valore. L'unico modo per ottenere un array di lunghezza diversa è crearne un altro.

Il ciclo tipico su un array è quindi:

```java
for (int i = 0; i < v.length; i++) {
    // usa v[i]
}
```

con `i` che parte da 0 e la condizione `i < v.length` (mai `<=`, perché `v[v.length]` non esiste).

> [!WARNING]
> **Attenzione — `length` per gli array, `length()` per le stringhe**
> Per una `String` la lunghezza si chiede con un **metodo**: `s.length()`. Per un array è una **variabile**: `v.length`. Sbagliare il tipo di parentesi dà un errore di compilazione (`cannot find symbol`), ed è tra gli errori più comuni scrivendo a mano senza compilatore che avverta.

### 5.1.5 Indici fuori dai limiti

Se il programma usa un indice minore di 0 oppure maggiore o uguale a `length`, il compilatore non può accorgersene (l'indice è un valore calcolato quando il programma gira) e l'errore si manifesta **a tempo di esecuzione**: Java interrompe il programma lanciando un'eccezione `ArrayIndexOutOfBoundsException`.

```java
public class Fuori {
    public static void main(String[] args) {
        int[] a = new int[5];
        for (int i = 0; i <= a.length; i++) {     // ERRORE LOGICO: l'ultimo giro usa a[5]
            a[i] = i;
        }
    }
}
```

L'esecuzione termina con:

```text
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5
	at Fuori.main(Fuori.java:5)
```

Il messaggio dice qual era l'indice e qual era la lunghezza, e la riga `at …` indica dove è successo. Il formato esatto del messaggio può cambiare da una versione di Java all'altra, ma l'eccezione è la stessa.

> [!NOTE]
> **Approfondimento esterno — `ArrayIndexOutOfBoundsException` e `NegativeArraySizeException`**
> La documentazione ufficiale descrive `ArrayIndexOutOfBoundsException` come lanciata "per indicare che si è acceduti a un array con un indice illegale", cioè **negativo o maggiore o uguale alla lunghezza**. È una sottoclasse di `IndexOutOfBoundsException` (da cui discende anche `StringIndexOutOfBoundsException`, quella delle stringhe) e di `RuntimeException`: è un'eccezione **non controllata**, e il metodo non deve dichiararla con `throws` (capitolo 13). La documentazione precisa che il formato esatto del messaggio non è specificato.
> Creare un array con una lunghezza **negativa** (`new int[-2]`) lancia invece una `NegativeArraySizeException`, anch'essa sottoclasse diretta di `RuntimeException`. Una lunghezza uguale a 0 è invece lecita: l'array è vuoto.
>
> *Fonte:* [ArrayIndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/ArrayIndexOutOfBoundsException.html), [NegativeArraySizeException](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/NegativeArraySizeException.html)

La difesa è una sola: **controllare l'indice prima di usarlo** quando non viene dal programma ma dall'esterno. L'esempio che segue conta quante volte compaiono i numeri da 0 a 3: il numero letto serve da indice di `count`, quindi un valore come 7 o −1 manderebbe in errore il programma.

```java
import java.util.Scanner;

public class Frequenze {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner("0 2 2 3 1 2 7 3 0 -1");
        int[] count = {0, 0, 0, 0};              // count[k] conta quante volte compare il numero k
        for (int i = 0; i < 10; i++) {
            int num = keyboard.nextInt();
            if (num >= 0 && num < count.length) {   // controllo prima di usare num come indice
                count[num]++;
            } else {
                System.out.println("Ignorato: " + num);
            }
        }
        for (int i = 0; i < count.length; i++) {
            System.out.println("Hai scritto " + count[i] + " volte il numero " + i);
        }
    }
}
```

La condizione `num >= 0 && num < count.length` è il controllo d'indice standard: due confronti, uno per ogni lato dell'intervallo valido. Si noti che `count[num]++` usa l'elemento come **contatore** e il valore letto come **indice**: è una tecnica molto frequente. L'output è:

```text
Ignorato: 7
Ignorato: -1
Hai scritto 2 volte il numero 0
Hai scritto 1 volte il numero 1
Hai scritto 3 volte il numero 2
Hai scritto 2 volte il numero 3
```

## 5.2 Inizializzare un array

### 5.2.1 I valori predefiniti

Appena creato con `new`, un array ha tutti gli elementi già a posto con un **valore predefinito**, che dipende dal tipo base. A differenza di una variabile locale (che il compilatore pretende inizializzata prima dell'uso, sezione 2.1.3), gli elementi di un array non sono mai "indefiniti":

| Tipo base | Valore predefinito |
|---|---|
| `int`, `long`, `short`, `byte` | `0` |
| `double`, `float` | `0.0` |
| `boolean` | `false` |
| `char` | il carattere di codice 0 (`'\u0000'`) |
| qualsiasi classe (`String`, …) | `null` |

```java
public class Predefiniti {
    public static void main(String[] args) {
        int[] a = new int[3];
        double[] d = new double[2];
        boolean[] b = new boolean[2];
        char[] c = new char[2];
        String[] s = new String[2];

        System.out.println(a[0] + " " + a[1] + " " + a[2]);
        System.out.println(d[0] + " " + d[1]);
        System.out.println(b[0] + " " + b[1]);
        System.out.println((int) c[0]);          // il carattere '\u0000' non si vede: stampiamo il suo codice
        System.out.println(s[0] + " " + s[1]);
    }
}
```

```text
0 0 0
0.0 0.0
false false
0
null null
```

Per questo `count` nell'esempio delle frequenze poteva anche essere creato con `new int[4]`, senza scrivere i quattro zeri: i contatori partono comunque da 0. Scriverli rende però esplicita l'intenzione.

### 5.2.2 La lista di valori tra graffe

Se i valori sono noti in anticipo si può fornirli **alla dichiarazione**, tra graffe e separati da virgole. La lunghezza dell'array è il numero di valori elencati e non si scrive:

```java
public class Inizializza {
    public static void main(String[] args) {
        int[] primes = {2, 3, 5, 7, 11};                 // lunghezza 5, dedotta dalla lista
        String[] days = {"lun", "mar", "mer"};
        double[] empty = {};                             // array di lunghezza 0

        System.out.println(primes.length + " " + days.length + " " + empty.length);

        int[] squares = new int[5];                      // oppure un elemento alla volta, in un ciclo
        for (int i = 0; i < squares.length; i++) {
            squares[i] = i * i;
        }
        System.out.println(squares[4]);

        squares = new int[] {1, 2, 3};                   // lista di valori dopo la dichiarazione: serve new int[]
        System.out.println(squares.length);
    }
}
```

```text
5 3 0
16
3
```

Le tre strade per riempire un array sono quindi: la lista alla dichiarazione, un'assegnazione per ogni elemento (anche dentro un ciclo, come nell'esempio delle temperature), oppure un valore letto da tastiera o da file. L'ultima riga mostra una regola da ricordare: la **forma abbreviata `{...}` è ammessa solo nella dichiarazione**. Per dare una lista di valori a un array già dichiarato si scrive `new int[] {1, 2, 3}`, con il tipo ripetuto e le parentesi quadre **vuote**.

### 5.2.3 Il for-each sugli array

Nel capitolo 4 abbiamo visto il `for` a elenco applicato alle costanti di un `enum`, con `Suit.values()` (sezione 4.5.4). Il metodo `values()` restituisce proprio un array, e lo stesso `for` percorre **qualsiasi array**:

```text
for (Tipo_Base nome : Nome_Array)
    istruzione
```

Si legge "per ogni `nome` in `Nome_Array`": a ogni giro la variabile `nome` riceve il valore dell'elemento successivo, dal primo all'ultimo. Non serve l'indice e non si può sbagliare il limite.

```java
public class ForEach {
    public static void main(String[] args) {
        int[] v = {4, 8, 15};

        int sum = 0;
        for (int x : v) {                // a ogni giro x è una copia dell'elemento successivo
            sum = sum + x;
        }
        System.out.println("Somma: " + sum);

        for (int x : v) {
            x = x * 2;                   // modifica la copia, non l'array
        }
        System.out.println(v[0] + " " + v[1] + " " + v[2]);

        for (int i = 0; i < v.length; i++) {
            v[i] = v[i] * 2;             // per modificare serve l'indice
        }
        System.out.println(v[0] + " " + v[1] + " " + v[2]);
    }
}
```

```text
Somma: 27
4 8 15
8 16 30
```

Il secondo ciclo non cambia l'array: `x` è una **copia** dell'elemento (per i tipi primitivi), quindi assegnarle un valore non tocca `v`. Il `for` con indice, invece, scrive davvero in `v[i]`. La regola pratica: il for-each va bene per **leggere** (somme, stampe, ricerche); se serve **scrivere** negli elementi, o serve sapere la posizione, si usa il `for` con l'indice.

### 5.2.4 Stampare un array

Il primo istinto è `System.out.println(v)`, che però non stampa gli elementi: stampa una sigla del tipo e un numero che non ha utilità (per un `int[]` qualcosa come `[I@15db9742`). La ragione è che gli array non ridefiniscono il metodo `toString` degli oggetti (capitolo 9). Per stampare il contenuto si usa `Arrays.toString`, della classe `java.util.Arrays`:

```java
import java.util.Arrays;

public class Stampa {
    public static void main(String[] args) {
        int[] v = {3, 1, 2};
        String[] names = {"Anna", "Luca"};
        int[] none = {};
        int[] missing = null;
        System.out.println(Arrays.toString(v));
        System.out.println(Arrays.toString(names));
        System.out.println(Arrays.toString(none));
        System.out.println(Arrays.toString(missing));
        System.out.println(v.toString().startsWith("[I@"));
    }
}
```

```text
[3, 1, 2]
[Anna, Luca]
[]
null
true
```

L'ultima riga conferma che `v.toString()` diretto produce la sigla `[I@…`.

> [!NOTE]
> **Approfondimento esterno — `Arrays.toString`**
> La classe `java.util.Arrays` contiene i metodi di utilità per gli array. Per ogni tipo primitivo c'è un overload di `public static String toString(int[] a)`, e ce n'è uno per gli oggetti, `toString(Object[] a)`. Il metodo restituisce "una rappresentazione in stringa del contenuto": gli elementi **tra parentesi quadre**, separati da una virgola e uno spazio (`", "`), convertiti come da `String.valueOf`. Se l'array è `null` restituisce la stringa `"null"` e non lancia eccezioni. Per usarlo serve `import java.util.Arrays;`. La documentazione avverte che, tranne dove diversamente indicato, gli altri metodi della classe lanciano `NullPointerException` se l'array passato è `null`.
>
> *Fonte:* [java.util.Arrays](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Arrays.html)

## 5.3 Array parzialmente riempiti

Spesso non si sa in anticipo quanti valori arriveranno, ma se ne conosce un massimo. Si crea allora un array **abbastanza grande** per il caso peggiore, e se ne usa solo una parte iniziale: si parla di **array parzialmente riempito** (*partially filled array*). Le posizioni usate sono le prime e occupano un tratto contiguo da 0 in avanti; il resto dell'array è inutilizzato.

Il programmatore deve tenere traccia di quanti elementi sono davvero in uso con un'apposita variabile `int`, un **contatore**. Il contatore ha un doppio ruolo: dice **quanti** sono gli elementi validi (da `values[0]` a `values[used - 1]`) e, nello stesso tempo, è l'**indice del primo posto libero** (`values[used]`). Per inserire un valore si scrive in quel posto e poi si incrementa il contatore.

```java
import java.util.Scanner;

public class Parziale {
    public static void main(String[] args) {
        final int MAX = 10;
        int[] values = new int[MAX];             // capacità: 10 posti
        int used = 0;                            // quanti sono occupati davvero: values[0] ... values[used - 1]

        Scanner keyboard = new Scanner("12 7 30 5 0");
        int next = keyboard.nextInt();
        while (next != 0 && used < values.length) {   // sentinella 0, ma anche array pieno
            values[used] = next;
            used++;
            next = keyboard.nextInt();
        }

        System.out.println("Letti: " + used);
        for (int i = 0; i < used; i++) {          // il ciclo arriva a used, non a values.length
            System.out.println(values[i]);
        }
    }
}
```

```text
Letti: 4
12
7
30
5
```

Il ciclo `while` combina due condizioni di arresto: il valore **sentinella** `0` (sezione 4.6.2) e l'**array pieno**. Senza il secondo controllo, l'undicesimo numero letto finirebbe in `values[10]` e il programma andrebbe in errore. Il ciclo di stampa si ferma a `used` e non a `values.length`: le posizioni oltre `used` contengono solo il valore predefinito e non sono dati.

> [!WARNING]
> **Attenzione — Pieno e vuoto**
> Con un array e un contatore ci sono sempre due casi limite da considerare: l'array **pieno** (`used == values.length`, non si può inserire) e l'array **vuoto** (`used == 0`, non si può estrarre né calcolare un massimo). Che cosa fare in quei casi (non inserire, restituire un valore speciale, lanciare un'eccezione) lo decide la traccia.

## 5.4 Gli array sono oggetti

### 5.4.1 La variabile contiene un riferimento

Un array è un **oggetto**, e una variabile di un tipo oggetto non contiene l'oggetto: contiene un **riferimento** (*reference*, in pratica l'indirizzo di memoria) all'oggetto, che vive in un'altra zona di memoria (lo vedremo con precisione nel [Capitolo 8 — Riferimenti e memoria](08-riferimenti-e-memoria.md)). Dopo

```java
int[] a = {1, 2, 3};
```

esistono due cose: l'**array** vero e proprio, con i suoi tre elementi, e la **variabile `a`**, che contiene l'indirizzo di quell'array. Questa differenza ha tre conseguenze che sorprendono: l'assegnamento tra array, il confronto con `==` e il passaggio ai metodi (sezione 5.5).

### 5.4.2 L'assegnamento copia il riferimento

Scrivere `b = a`, con `a` e `b` array, **non copia gli elementi**: copia l'indirizzo. Dopo l'assegnamento `a` e `b` sono due nomi per lo *stesso* array (si dice che sono **alias**), e una modifica fatta tramite l'uno si vede tramite l'altro.

```java
import java.util.Arrays;

public class Alias {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = a;                     // copia l'indirizzo: un solo array, due nomi
        b[0] = 99;
        System.out.println(a[0]);
        System.out.println(a == b);

        int[] c = {1, 2, 3};
        int[] d = {1, 2, 3};
        System.out.println(c == d);                  // indirizzi diversi
        System.out.println(c.equals(d));             // equals ereditato da Object: ancora l'indirizzo
        System.out.println(Arrays.equals(c, d));     // elemento per elemento
    }
}
```

```text
99
true
false
false
true
```

La prima riga mostra l'alias: abbiamo scritto in `b[0]` e leggiamo la modifica in `a[0]`, perché l'array è uno solo. Poi `a == b` è `true`: i due nomi indicano lo stesso array.

### 5.4.3 Uguaglianza: `==`, `equals` e `Arrays.equals`

Dalla seconda parte dell'esempio: `c` e `d` hanno lo stesso contenuto ma sono due array distinti, in due posti diversi della memoria. L'operatore `==` confronta **gli indirizzi**, quindi dà `false`. Anche il metodo `equals`, chiamato direttamente sugli array (`c.equals(d)`), dà `false`: gli array non ridefiniscono `equals`, e quello ereditato dalla classe `Object` confronta ancora gli indirizzi (capitolo 9). Questo è diverso dalle stringhe, dove `equals` confronta il testo (sezione 3.4).

Per sapere se due array hanno gli stessi elementi, nello stesso ordine, servono due cose: o un metodo scritto a mano, che controlla la lunghezza e poi ogni coppia di elementi,

```java
public class Uguali {
    // confronto fatto a mano: stessa lunghezza e stessi elementi, nello stesso ordine
    public static boolean sameElements(int[] x, int[] y) {
        if (x.length != y.length) {
            return false;
        }
        for (int i = 0; i < x.length; i++) {
            if (x[i] != y[i]) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        int[] c = {1, 2, 3};
        int[] d = {1, 2, 3};
        int[] e = {1, 2, 4};
        System.out.println(sameElements(c, d));
        System.out.println(sameElements(c, e));
    }
}
```

```text
true
false
```

oppure il metodo di libreria `Arrays.equals(c, d)`.

> [!NOTE]
> **Approfondimento esterno — `Arrays.equals`**
> `public static boolean equals(int[] a, int[] a2)` restituisce `true` se i due array "contengono lo stesso numero di elementi e tutte le coppie di elementi corrispondenti sono uguali", cioè se hanno gli stessi elementi **nello stesso ordine**; due riferimenti entrambi `null` sono considerati uguali. Esiste un overload per ogni tipo primitivo e uno per `Object[]`, che confronta gli elementi con il loro metodo `equals`. Non lancia eccezioni.
>
> *Fonte:* [java.util.Arrays](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Arrays.html)

### 5.4.4 Copiare un array

Se serve una **copia vera**, cioè un secondo array indipendente con gli stessi valori, bisogna crearlo e riempirlo. Il metodo più elementare è il ciclo; la libreria offre `Arrays.copyOf`, `Arrays.copyOfRange` e `System.arraycopy`.

```java
import java.util.Arrays;

public class Copie {
    public static void main(String[] args) {
        int[] a = {10, 20, 30, 40};

        int[] manual = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            manual[i] = a[i];
        }

        int[] longer = Arrays.copyOf(a, 6);              // più lunga: completa con 0
        int[] shorter = Arrays.copyOf(a, 2);             // più corta: taglia
        int[] middle = Arrays.copyOfRange(a, 1, 3);      // da indice 1 incluso a 3 escluso

        int[] dest = new int[6];
        System.arraycopy(a, 0, dest, 2, 4);              // 4 elementi di a, da a[0], dentro dest da dest[2]

        manual[0] = 0;                                   // non tocca a: sono array distinti
        System.out.println(Arrays.toString(a));
        System.out.println(Arrays.toString(manual));
        System.out.println(Arrays.toString(longer));
        System.out.println(Arrays.toString(shorter));
        System.out.println(Arrays.toString(middle));
        System.out.println(Arrays.toString(dest));
    }
}
```

```text
[10, 20, 30, 40]
[0, 20, 30, 40]
[10, 20, 30, 40, 0, 0]
[10, 20]
[20, 30]
[0, 0, 10, 20, 30, 40]
```

`Arrays.copyOf(a, n)` crea un array nuovo di lunghezza `n`: se `n` è maggiore di `a.length` i posti in più sono riempiti con il valore predefinito, se minore la copia è troncata. `Arrays.copyOfRange(a, from, to)` copia l'intervallo che va da `from` (incluso) a `to` (escluso). `System.arraycopy(src, srcPos, dest, destPos, length)` non crea niente: copia `length` elementi da `src` (a partire da `srcPos`) dentro un array `dest` **già esistente** (a partire da `destPos`). È utile per far scorrere gli elementi, per esempio per fare posto a un inserimento:

```java
import java.util.Arrays;

public class Inserisci {
    public static void main(String[] args) {
        int[] v = {1, 2, 4, 5, 0};       // 4 elementi usati su 5 posti
        int used = 4;

        // inserire 3 alla posizione 2: prima si fa posto spostando a destra
        System.arraycopy(v, 2, v, 3, used - 2);   // gli intervalli si sovrappongono: va bene
        v[2] = 3;
        used++;
        System.out.println(Arrays.toString(v));
    }
}
```

```text
[1, 2, 3, 4, 5]
```

> [!NOTE]
> **Approfondimento esterno — `Arrays.copyOf`, `Arrays.copyOfRange`, `System.arraycopy`**
> - `public static int[] copyOf(int[] original, int newLength)` copia l'array "troncando o completando con zeri (se necessario) in modo che la copia abbia la lunghezza indicata". Lancia `NegativeArraySizeException` se `newLength` è negativo e `NullPointerException` se `original` è `null`. Esistono gli overload per gli altri tipi (`double[]`, …) e per gli oggetti.
> - `public static int[] copyOfRange(int[] original, int from, int to)` copia l'intervallo da `from` (incluso, tra 0 e `original.length`) a `to` (escluso, deve essere almeno `from`, può superare la lunghezza: i posti oltre la fine sono riempiti con zeri). La lunghezza del risultato è `to - from`. Lancia `ArrayIndexOutOfBoundsException` se `from < 0` o `from > original.length`, `IllegalArgumentException` se `from > to`, `NullPointerException` se `original` è `null`.
> - `public static void arraycopy(Object src, int srcPos, Object dest, int destPos, int length)` (classe `java.lang.System`) copia `length` componenti. Se `src` e `dest` sono lo stesso array, la copia avviene "come se" i componenti fossero prima copiati in un array temporaneo: per questo l'inserimento qui sopra funziona. Lancia `IndexOutOfBoundsException` se la copia uscirebbe dai limiti (tra le cause: `srcPos`, `destPos` o `length` negativi, `srcPos+length` oltre `src.length`, `destPos+length` oltre `dest.length`; in questi casi `dest` non viene modificato), `ArrayStoreException` se i tipi dei due array sono incompatibili, `NullPointerException` se uno dei due è `null`. Sono tutte eccezioni non controllate.
>
> *Fonte:* [java.util.Arrays](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Arrays.html), [java.lang.System#arraycopy](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/System.html)

> [!WARNING]
> **Attenzione — Copia superficiale con gli array di oggetti**
> Per un array di **oggetti** (sezione 5.8) le copie viste qui copiano i **riferimenti**, non gli oggetti: l'array nuovo contiene gli stessi oggetti dell'originale, e modificare un oggetto tramite l'uno lo modifica anche nell'altro. Con i tipi primitivi il problema non esiste, perché gli elementi sono valori.

## 5.5 Array e metodi

### 5.5.1 Un elemento come argomento

Un elemento di array ha il tipo base, quindi si può passare a un metodo che aspetta un valore di quel tipo. Per i tipi primitivi il passaggio è **per valore**: il metodo riceve una copia e non può alterare l'elemento originale.

### 5.5.2 Un array intero come parametro

Per passare l'intero array il parametro si dichiara con le parentesi quadre dopo il tipo, **senza la lunghezza**: `void doubleAll(int[] v)`. Lo stesso metodo accetta array di qualunque lunghezza. Nella chiamata si scrive il solo nome, **senza parentesi quadre**: `doubleAll(a)`.

Il passaggio è ancora "per valore", ma ciò che si copia è il **riferimento**. Il metodo riceve quindi l'indirizzo dello *stesso* array del chiamante e **può modificarne gli elementi**; queste modifiche restano dopo il ritorno.

```java
import java.util.Arrays;

public class Metodi {
    public static void increment(int x) {
        x = x + 1;                        // x è una copia del valore ricevuto
    }

    public static void doubleAll(int[] v) {
        for (int i = 0; i < v.length; i++) {
            v[i] = v[i] * 2;              // v è un riferimento allo stesso array del chiamante
        }
    }

    public static void replace(int[] v) {
        v = new int[] {0, 0, 0};          // cambia solo la copia locale del riferimento
    }

    public static int[] range(int n) {
        int[] result = new int[n];
        for (int i = 0; i < n; i++) {
            result[i] = i + 1;
        }
        return result;
    }

    public static void main(String[] args) {
        int[] a = {5, 6, 7};

        increment(a[0]);                  // si passa un elemento: tipo base, passaggio per valore
        System.out.println(a[0]);

        doubleAll(a);                     // si passa l'array intero: senza parentesi quadre
        System.out.println(Arrays.toString(a));

        replace(a);
        System.out.println(Arrays.toString(a));

        int[] r = range(4);
        System.out.println(Arrays.toString(r));
        System.out.println(range(3).length);
    }
}
```

```text
5
[10, 12, 14]
[10, 12, 14]
[1, 2, 3, 4]
3
```

Leggiamo i risultati. `increment(a[0])` lascia `a[0]` a 5: il metodo ha incrementato una copia. `doubleAll(a)` raddoppia davvero gli elementi, perché `v` e `a` indicano lo stesso array. `replace(a)` invece **non ha effetto**: dentro il metodo `v = new int[] {...}` fa puntare la variabile locale `v` a un array nuovo, ma `a` nel `main` continua a indicare quello vecchio. Si può modificare *il contenuto* di un array ricevuto, non *sostituirlo* al chiamante (ne parliamo ancora nel capitolo 8).

### 5.5.3 Un array come valore di ritorno

Un metodo può **restituire un array**: nell'intestazione il tipo di ritorno è il tipo array (`int[]`), nel corpo si dichiara un array locale, lo si riempie e lo si restituisce con `return`. È ciò che fa `range(4)` qui sopra. Il chiamante lo può mettere in una variabile (`int[] r = range(4);`) oppure usarlo subito (`range(3).length`).

Un caso che abbiamo già incontrato è il metodo `split` di `String` (sezione 3.5): restituisce un `String[]` con i campi in cui ha spezzato la riga.

```java
public class Campi {
    public static void main(String[] args) {
        String line = "Rossi,Anna,25";
        String[] fields = line.split(",");              // un array di 3 stringhe
        System.out.println(fields.length);
        System.out.println(fields[1]);
        int age = Integer.parseInt(fields[2]) + 1;      // il campo è testo: va convertito per fare calcoli
        System.out.println(age);
    }
}
```

```text
3
Anna
26
```

### 5.5.4 Gli argomenti del main

Torniamo all'intestazione del programma, `public static void main(String[] args)`. Adesso possiamo leggerla per intero: `args` è un **array di stringhe**. Contiene le parole scritte dopo il nome della classe quando si lancia il programma dalla riga di comando:

```java
public class Args {
    public static void main(String[] args) {
        System.out.println("Argomenti: " + args.length);
        for (int i = 0; i < args.length; i++) {
            System.out.println(i + ": " + args[i]);
        }
    }
}
```

Lanciandolo con `java Args uno due tre` si ottiene:

```text
Argomenti: 3
0: uno
1: due
2: tre
```

Se si lancia con `java Args` e basta, `args` è un array **vuoto** (lunghezza 0, non `null`) e il programma stampa `Argomenti: 0`. Gli argomenti sono sempre stringhe: per usarli come numeri si converte con `Integer.parseInt(args[0])`. Nell'ambiente della prova scritta il programma non riceve argomenti, ma il parametro `args` va comunque scritto nell'intestazione.

### 5.5.5 Un array come campo di una classe

Un array è spesso lo stato interno di una classe: la classe lo dichiara come **campo privato**, lo crea e fornisce metodi per usarlo. Le classi si studieranno nel [Capitolo 7 — Classi e oggetti](07-classi-e-oggetti.md); qui basta sapere che le variabili del campo e i metodi stanno dentro `class Nome { ... }`. L'esempio mostra un array parzialmente riempito dentro una classe, con il contatore accanto:

```java
import java.util.Arrays;

class Stazione {
    private double[] misure = new double[5];      // campo privato: array di capacità 5
    private int used = 0;

    public void add(double value) {
        if (used < misure.length) {
            misure[used] = value;
            used++;
        }
    }

    public double average() {
        double sum = 0;
        for (int i = 0; i < used; i++) {
            sum = sum + misure[i];
        }
        return used == 0 ? 0 : sum / used;
    }

    public double[] getMisureRiferimento() {
        return misure;                             // restituisce l'array interno: chi lo riceve può modificarlo
    }

    public double[] getMisure() {
        return Arrays.copyOf(misure, used);        // restituisce una copia: lo stato resta protetto
    }
}

public class Meteo {
    public static void main(String[] args) {
        Stazione s = new Stazione();
        s.add(10);
        s.add(20);
        System.out.println(s.average());

        s.getMisureRiferimento()[0] = 1000;        // modifica lo stato interno senza passare da add
        System.out.println(s.average());

        s.getMisure()[0] = -5;                     // modifica solo la copia
        System.out.println(s.average());
    }
}
```

```text
15.0
510.0
510.0
```

Il metodo `add` controlla che ci sia posto prima di scrivere (array pieno, sezione 5.3), e `average` divide per `used` e non per `misure.length`, con la guardia per il caso vuoto. I due "getter" mostrano un problema importante: restituire **il riferimento all'array privato** (`getMisureRiferimento`) permette a chiunque di modificare lo stato della classe senza passare dai suoi metodi, e la media è cambiata da 15.0 a 510.0 senza chiamare `add`. Restituendo una **copia** (`getMisure`) la modifica fatta dal chiamante colpisce solo la copia, e la media resta 510.0: il secondo intervento non ha toccato lo stato della classe.

> [!WARNING]
> **Attenzione — La perdita di riservatezza (*privacy leak*)**
> Un campo dichiarato `private` ma restituito dal suo getter **come riferimento** non è più davvero protetto: il campo è privato, ma l'oggetto a cui punta è raggiungibile da fuori. Quando un getter restituisce un array interno, la soluzione corretta è restituirne una copia. Lo stesso vale in ingresso: un costruttore che memorizza l'array ricevuto invece di copiarlo condivide l'array con il chiamante. Il tema dell'incapsulamento è ripreso nel capitolo 7.

## 5.6 Algoritmi di base sugli array

Quasi tutti i problemi su array si risolvono con pochi schemi di percorso. Qui sono presentati con il codice completo; li ritroverai come scheletri da esame.

### 5.6.1 Percorrere: somma, conteggio, massimo e minimo

Per **sommare** o **contare** si usa un accumulatore inizializzato prima del ciclo (`int sum = 0;`), come visto nella sezione 5.1.2. Il **massimo** richiede più cura: l'idea è tenere in una variabile il "miglior candidato visto finora" e confrontarlo con ogni elemento.

La domanda decisiva è **con che valore inizializzare il candidato**. Un'idea sbagliata ma tentatrice è `int max = 0;`: funziona con numeri positivi, ma se l'array contiene solo numeri negativi restituisce `0`, che nell'array non c'è. La scelta giusta è **partire dal primo elemento**, `int max = v[0];`, e far partire il ciclo da `i = 1`.

```java
public class Algoritmi {
    public static int max(int[] v) {
        int max = v[0];                       // si parte dal primo elemento, non da 0
        for (int i = 1; i < v.length; i++) {
            if (v[i] > max) {
                max = v[i];
            }
        }
        return max;
    }

    public static int indexOf(int[] v, int target) {
        for (int i = 0; i < v.length; i++) {
            if (v[i] == target) {
                return i;                     // trovato: si esce subito
            }
        }
        return -1;                            // arrivati in fondo: non c'è
    }

    public static void main(String[] args) {
        int[] v = {-7, -3, -9};
        System.out.println(max(v));
        System.out.println(indexOf(v, -3));
        System.out.println(indexOf(v, 5));
    }
}
```

```text
-3
1
-1
```

Con l'array `{-7, -3, -9}` il candidato parte da `-7`, poi `-3 > -7` lo sostituisce, poi `-9 > -3` è falso: il massimo è `-3`. Il minimo si scrive uguale, con `<` al posto di `>`.

Restano due casi limite. Con **un solo elemento** il ciclo non gira e `v[0]` è il risultato corretto, quindi non serve un trattamento speciale. Con un array **vuoto**, invece, `v[0]` non esiste e il metodo lancia `ArrayIndexOutOfBoundsException`: se la traccia prevede che l'array possa essere vuoto, bisogna controllare `v.length == 0` **prima** di leggere `v[0]` e decidere che cosa restituire.

### 5.6.2 La ricerca sequenziale

L'`indexOf` qui sopra è una **ricerca sequenziale** (*sequential search*): guarda gli elementi in ordine, dal primo all'ultimo, e si ferma quando trova ciò che cerca o quando l'array è finito. Va bene per array non ordinati. Il valore speciale `-1` (che non è un indice valido) comunica "non trovato". Se l'array è ordinato esistono ricerche più efficienti, ma fuori dal programma del corso.

Con le stringhe il confronto va fatto con `equals` e non con `==` (sezione 3.4): `v[i].equals(target)`.

### 5.6.3 L'ordinamento per selezione

Ordinare un array in senso crescente è un classico. L'algoritmo più semplice è l'**ordinamento per selezione** (*selection sort*): si cerca il più piccolo di tutti gli elementi e lo si porta in posizione 0, poi si cerca il più piccolo tra i rimanenti e lo si porta in posizione 1, e così via. Per portare un elemento al suo posto lo si **scambia** con quello che ci sta ora.

L'algoritmo, in parole: per ogni posizione `i` da 0 fino alla penultima, (1) cerca la posizione `smallest` dell'elemento minimo tra la posizione `i` e la fine; (2) scambia `v[i]` con `v[smallest]`. Si ferma alla penultima posizione perché quando resta un solo elemento è già al posto giusto.

```java
import java.util.Arrays;

public class Selezione {
    public static void selectionSort(int[] v) {
        for (int i = 0; i < v.length - 1; i++) {
            int smallest = i;                         // posizione del più piccolo visto finora
            for (int j = i + 1; j < v.length; j++) {
                if (v[j] < v[smallest]) {
                    smallest = j;
                }
            }
            int temp = v[i];                          // scambio: serve una variabile d'appoggio
            v[i] = v[smallest];
            v[smallest] = temp;
            System.out.println("i = " + i + ": " + Arrays.toString(v));
        }
    }

    public static void main(String[] args) {
        int[] v = {5, 3, 8, 1};
        selectionSort(v);
    }
}
```

```text
i = 0: [1, 3, 8, 5]
i = 1: [1, 3, 8, 5]
i = 2: [1, 3, 5, 8]
```

Seguiamo l'esecuzione a mano (sezione 4.7.1). Per `i = 0` il più piccolo di `{5, 3, 8, 1}` è `1`, in posizione 3: scambiandolo con `v[0]` si ottiene `{1, 3, 8, 5}`. Per `i = 1` il più piccolo tra `{3, 8, 5}` è `3`, già in posizione 1: lo scambio non cambia nulla. Per `i = 2` il più piccolo tra `{8, 5}` è `5`, in posizione 3: scambio e si ottiene `{1, 3, 5, 8}`. Lo scambio di due elementi richiede sempre la **variabile d'appoggio** `temp`: scrivere `v[i] = v[smallest]; v[smallest] = v[i];` perderebbe il valore originale di `v[i]`.

Il selection sort è semplice ma inefficiente per array grandi.

### 5.6.4 Arrays.sort

La libreria di Java fornisce già un ordinamento efficiente, `Arrays.sort`, che nei programmi veri si usa al posto di scriverne uno a mano.

```java
import java.util.Arrays;

public class Ordina {
    public static void main(String[] args) {
        int[] v = {5, 3, 8, 1};
        Arrays.sort(v);
        System.out.println(Arrays.toString(v));

        int[] w = {9, 7, 5, 3, 1};
        Arrays.sort(w, 1, 4);                         // solo gli indici 1, 2, 3
        System.out.println(Arrays.toString(w));

        String[] names = {"Marta", "Anna", "Carlo"};
        Arrays.sort(names);                           // ordine alfabetico: String è Comparable
        System.out.println(Arrays.toString(names));
    }
}
```

```text
[1, 3, 5, 8]
[9, 3, 5, 7, 1]
[Anna, Carlo, Marta]
```

Il metodo **modifica l'array ricevuto** (non restituisce un array nuovo). Con la forma a tre argomenti, `Arrays.sort(w, 1, 4)`, ordina solo l'intervallo da 1 (incluso) a 4 (escluso): gli elementi in posizione 0 e 4 restano dove sono.

> [!NOTE]
> **Approfondimento esterno — `Arrays.sort`**
> - `public static void sort(int[] a)` ordina l'array "in ordine numerico crescente". Esistono gli overload per gli altri tipi primitivi. Per gli `int` l'algoritmo usato è un *Dual-Pivot Quicksort*, con prestazioni O(n log n).
> - `public static void sort(int[] a, int fromIndex, int toIndex)` ordina l'intervallo da `fromIndex` (incluso) a `toIndex` (escluso); se i due indici coincidono l'intervallo è vuoto. Lancia `IllegalArgumentException` se `fromIndex > toIndex` e `ArrayIndexOutOfBoundsException` se `fromIndex < 0` o `toIndex > a.length`.
> - `public static void sort(Object[] a)` ordina un array di oggetti "in ordine crescente secondo l'**ordinamento naturale** dei suoi elementi", e l'ordinamento è **stabile** (gli elementi uguali non vengono scambiati tra loro). Lancia `ClassCastException` se gli elementi non sono mutuamente confrontabili. Gli elementi devono implementare l'interfaccia `Comparable` (capitolo 10): le stringhe e i wrapper dei numeri la implementano già.
>
> *Fonte:* [java.util.Arrays](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Arrays.html)

## 5.7 Array multidimensionali

### 5.7.1 Una tabella: due indici

Alcuni dati hanno naturalmente la forma di una **tabella**: le presenze di tre corsi in quattro settimane, i voti di cinque studenti in tre prove, le caselle di una scacchiera. Un array con **due indici**, uno per la riga e uno per la colonna, si chiama **matrice** o array bidimensionale, e si dichiara con due coppie di parentesi quadre:

```java
int[][] table = new int[3][4];            // 3 righe, 4 colonne
```

Per accedere a un elemento servono due indici: `table[1][2]` è l'elemento della riga 1, colonna 2 (anche qui si parte da 0). Tutti gli elementi partono dal valore predefinito del tipo base. Si possono avere anche più di due dimensioni (`int[][][]`), ma sono rare.

### 5.7.2 Percorrere una matrice: cicli annidati

Per toccare tutti gli elementi servono **due cicli annidati** (sezione 4.5.5): il ciclo esterno scorre le righe, quello interno le colonne di ciascuna riga.

```java
public class Tabella {
    public static void main(String[] args) {
        int[][] table = new int[3][4];                 // 3 righe, 4 colonne, tutte a 0

        for (int row = 0; row < table.length; row++) {
            for (int col = 0; col < table[row].length; col++) {
                table[row][col] = (row + 1) * (col + 1);
            }
        }

        for (int row = 0; row < table.length; row++) {
            for (int col = 0; col < table[row].length; col++) {
                System.out.printf("%4d", table[row][col]);
            }
            System.out.println();
        }
        System.out.println(table.length + " " + table[0].length);
    }
}
```

```text
   1   2   3   4
   2   4   6   8
   3   6   9  12
3 4
```

Il primo blocco riempie la matrice con la tabellina; il secondo la stampa riga per riga, con `printf("%4d", …)` che riserva 4 caratteri a ciascun numero (sezione 3.6.3) e un `println()` vuoto che va a capo alla fine di ogni riga. Le due espressioni nei limiti dei cicli sono importanti: `table.length` è il numero di **righe**, `table[row].length` è il numero di **colonne della riga `row`**. Perché la seconda formula e non semplicemente `table[0].length`? Lo vediamo nella prossima sezione.

### 5.7.3 Un array di array

In Java **non esistono davvero array a due dimensioni**: una matrice `int[][]` è un array i cui elementi sono a loro volta array. `int[][] table = new int[3][4]` crea un array di 3 elementi, ciascuno dei quali è un `int[]` di 4 elementi. Quindi `table.length` è 3, e `table[0]` è un array di tipo `int[]`, cioè **una riga intera**:

```java
public class ArrayDiArray {
    public static void main(String[] args) {
        int[][] m = new int[2][3];
        int[] firstRow = m[0];                  // m[0] è un int[]: una riga intera
        firstRow[1] = 9;
        System.out.println(m[0][1]);

        m[1] = new int[] {7, 7};                // si può sostituire una riga con un'altra, anche più corta
        System.out.println(m[1].length);
    }
}
```

```text
9
2
```

`firstRow` è un alias della riga 0 (sezione 5.4.2): scrivendo in `firstRow[1]` si cambia `m[0][1]`. E poiché ogni riga è un array a sé, si può **sostituire** con un array di lunghezza diversa.

### 5.7.4 Array irregolari

Da questa rappresentazione segue una conseguenza utile: **le righe non devono avere tutte la stessa lunghezza**. Un array con righe di lunghezze diverse si dice **irregolare** (*ragged array*). Lo si crea fissando solo il numero di righe e lasciando vuoto il secondo indice, poi si crea ogni riga a parte; oppure lo si inizializza con una lista di liste:

```java
import java.util.Arrays;

public class Irregolare {
    public static void main(String[] args) {
        int[][] ragged = new int[3][];                 // 3 righe, lunghezze ancora da stabilire
        System.out.println(ragged[0]);                 // null: la riga non esiste ancora
        ragged[0] = new int[2];
        ragged[1] = new int[4];
        ragged[2] = new int[0];                        // una riga può anche essere vuota
        for (int i = 0; i < ragged.length; i++) {
            System.out.println("riga " + i + ": " + ragged[i].length + " elementi");
        }

        int[][] groups = {{4, 7}, {9}, {1, 2, 3}, {}};   // lista di liste di valori
        System.out.println(Arrays.deepToString(groups));
        System.out.println(Arrays.toString(groups[2]));
    }
}
```

```text
null
riga 0: 2 elementi
riga 1: 4 elementi
riga 2: 0 elementi
[[4, 7], [9], [1, 2, 3], []]
[1, 2, 3]
```

Con `new int[3][]` le tre righe esistono come posti, ma non sono ancora array: contengono `null` (come ogni elemento di tipo oggetto non inizializzato, sezione 5.8), e finché non ne creiamo una usarla darebbe `NullPointerException`. Una riga può essere anche **vuota**: il ciclo interno semplicemente non gira, non è un errore.

Ecco perché i cicli su una matrice usano `m[i].length` per i limiti della colonna: con le righe di lunghezza diversa, `m[0].length` sarebbe sbagliato per tutte le altre righe.

> [!TIP]
> **Intuizione — Tre regole per le matrici**
> 1. `m.length` conta le **righe**.
> 2. `m[i].length` conta le colonne **della riga `i`**.
> 3. `m[i]` da solo è una **riga intera** (un array), `m[i][j]` è un singolo elemento.

Per stampare una matrice senza scrivere i cicli, `Arrays.toString` non basta: applicato a un `int[][]` stamperebbe la sigla dei suoi elementi (le righe, che sono oggetti). Si usa `Arrays.deepToString`, come nell'esempio qui sopra.

> [!NOTE]
> **Approfondimento esterno — `Arrays.deepToString` e `Arrays.deepEquals`**
> `public static String deepToString(Object[] a)` restituisce la rappresentazione "profonda" dell'array: se un elemento è a sua volta un array, ne mostra il contenuto, ricorsivamente. È pensato per gli array multidimensionali. Formato come `toString` (parentesi quadre, elementi separati da `", "`); restituisce `"null"` se l'array è `null`.
> `public static boolean deepEquals(Object[] a1, Object[] a2)` confronta due array annidati di profondità qualsiasi: a differenza di `equals(Object[], Object[])`, che confronta gli elementi con `equals` (e quindi, per le righe, per indirizzo), `deepEquals` confronta ricorsivamente il contenuto delle righe.
>
> *Fonte:* [java.util.Arrays](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Arrays.html)

### 5.7.5 Matrici e metodi

I parametri e i valori di ritorno possono essere matrici, con il tipo `int[][]`. Un metodo che riceve "la matrice dei dati" deve avere il parametro `int[][]` e **non** `int[]`: un `int[]` non è una matrice, e chi chiama con un `int[][]` otterrebbe un errore di compilazione.

```java
import java.util.Arrays;

public class MatriciMetodi {
    public static int[] rowSums(int[][] m) {
        int[] sums = new int[m.length];                   // una somma per ogni riga
        for (int i = 0; i < m.length; i++) {
            for (int j = 0; j < m[i].length; j++) {
                sums[i] = sums[i] + m[i][j];
            }
        }
        return sums;
    }

    public static int[][] transpose(int[][] m) {          // vale per matrici rettangolari
        int[][] t = new int[m[0].length][m.length];
        for (int i = 0; i < m.length; i++) {
            for (int j = 0; j < m[i].length; j++) {
                t[j][i] = m[i][j];
            }
        }
        return t;
    }

    public static void main(String[] args) {
        int[][] groups = {{4, 7}, {9}, {1, 2, 3}, {}};
        System.out.println(Arrays.toString(rowSums(groups)));

        int[][] m = {{1, 2, 3}, {4, 5, 6}};
        System.out.println(Arrays.deepToString(transpose(m)));
    }
}
```

```text
[11, 9, 6, 0]
[[1, 4], [2, 5], [3, 6]]
```

`rowSums` restituisce un array con **una somma per riga**: l'ultima riga è vuota e la sua somma è 0. `transpose` scambia righe e colonne: l'elemento `m[i][j]` finisce in `t[j][i]`, e la matrice risultante ha tante righe quante erano le colonne. Il metodo assume che tutte le righe abbiano la stessa lunghezza di `m[0]`: con una matrice irregolare non avrebbe senso parlare di trasposta.

## 5.8 Array di oggetti

Finora gli elementi erano numeri o stringhe. Un array può avere come tipo base **qualunque classe**, ad esempio una classe `Prodotto` scritta da noi (vedremo come nel capitolo 7; qui la usiamo soltanto). C'è però una trappola classica, che sorprende chi viene dai tipi primitivi:

> [!WARNING]
> **Attenzione — Creare un array di oggetti non crea gli oggetti**
> `Prodotto[] shelf = new Prodotto[3];` crea un array con **tre "caselle" per riferimenti**, non tre prodotti. Ogni casella parte con il valore predefinito dei riferimenti, `null`. Per poter usare `shelf[0]` bisogna prima **creare l'oggetto** con `new` e assegnarlo alla casella. Chiamare un metodo su un elemento ancora `null` (`shelf[0].getNome()`) lancia una `NullPointerException`.

```java
class Prodotto {
    private String nome;
    private double prezzo;

    public Prodotto(String nome, double prezzo) {
        this.nome = nome;
        this.prezzo = prezzo;
    }

    public String getNome() {
        return nome;
    }

    public double getPrezzo() {
        return prezzo;
    }
}

public class Oggetti {
    public static void main(String[] args) {
        Prodotto[] shelf = new Prodotto[3];        // tre "caselle" per riferimenti: nessun Prodotto esiste ancora
        System.out.println(shelf[0]);

        shelf[0] = new Prodotto("penna", 1.5);     // ogni elemento va creato con new
        shelf[1] = new Prodotto("quaderno", 3.0);

        for (int i = 0; i < shelf.length; i++) {
            if (shelf[i] != null) {                // il terzo elemento è ancora null
                System.out.println(shelf[i].getNome() + " " + shelf[i].getPrezzo());
            } else {
                System.out.println("posto " + i + " vuoto");
            }
        }

        String[] words = new String[2];            // vale anche per le stringhe
        System.out.println(words[0] + "!");
    }
}
```

```text
null
penna 1.5
quaderno 3.0
posto 2 vuoto
null!
```

Il ciclo controlla `shelf[i] != null` prima di chiamare un metodo sull'elemento: è la stessa idea dell'indice controllato prima dell'uso. L'ultima riga ricorda che per le stringhe vale lo stesso: `new String[2]` crea due caselle `null`, e la concatenazione con `+` stampa il testo `null` (sezione 3.1.5), senza errore.

Con gli array di oggetti l'assegnamento `shelf[0] = ...` copia un **riferimento** (sezione 5.4.2): due elementi possono indicare lo stesso oggetto, e una modifica fatta tramite l'uno si vede tramite l'altro.

## 5.9 Array o ArrayList?

L'array ha un limite evidente: la lunghezza è **fissa** e decisa alla creazione. Se non si sa quanti elementi serviranno bisogna prevedere un massimo e tenere un contatore (sezione 5.3), oppure creare un array più grande e copiarvi i vecchi elementi (`Arrays.copyOf`). Per questo la libreria di Java offre la classe **`ArrayList`**, una lista che cresce e si restringe da sola e ha metodi come `add`, `remove` e `size`. Dietro le quinte gestisce proprio un array, ricreandolo quando si riempie.

Le differenze da ricordare: un array ha lunghezza fissa, si usa con `[]` e `length`, e può contenere sia tipi primitivi sia oggetti; un `ArrayList` ha dimensione variabile, si usa con metodi, e può contenere **solo oggetti** (per gli interi si usa il tipo `Integer`, come vedremo con i wrapper nel capitolo 6 e le collezioni nel [Capitolo 12 — Generics e collezioni](12-generics-e-collezioni.md)). Quando la traccia chiede un array primitivo con una capienza data, si scrive un array primitivo.

## Come esce all'esame

**EXAM2 — Esercizio 3 (13 punti), concorrenza e sincronizzazione.** Le classi `Produttore` e `Consumatore` erano già fornite e interagivano con una risorsa condivisa; il candidato doveva scrivere da zero la classe `Buffer`. Per questo capitolo conta il **primo requisito** della traccia: il `Buffer` doveva "contenere una struttura dati basata su un array primitivo con dimensione massima pari a 3". Gli altri tre requisiti chiedevano tre metodi: uno che restituisce come `int` il numero di elementi presenti, uno per inserire un elemento, uno per estrarre e rimuovere un elemento, con le firme esatte da dedurre dalle chiamate presenti nel codice fornito. I concetti del capitolo che servivano sono l'array con **capacità fissa e contatore** (sezioni 5.3 e 5.5.5) e lo **scorrimento** degli elementi dopo un'estrazione (sezione 5.4.4). La sincronizzazione (la parte più impegnativa dell'esercizio) è argomento del capitolo 18.

I vincoli letterali da rispettare: array **primitivo** (non una `ArrayList`), **dimensione 3** (non una costante diversa), tre metodi con le **firme coerenti con le chiamate**.

## Scheletri da esame

### Massimo e minimo di un array

*Quando si usa:* un metodo statico riceve un array di numeri e restituisce il valore più grande o più piccolo.

```java
public class SkMaxMin {
    public static int max(int[] v) {
        int max = v[0];                          // primo elemento come candidato: funziona anche con tutti negativi
        for (int i = 1; i < v.length; i++) {     // il ciclo parte da 1: v[0] è già stato considerato
            if (v[i] > max) {
                max = v[i];
            }
        }
        return max;
    }

    public static int min(int[] v) {
        int min = v[0];
        for (int i = 1; i < v.length; i++) {
            if (v[i] < min) {
                min = v[i];
            }
        }
        return min;
    }

    public static void main(String[] args) {
        int[] v = {-4, -9, -1, -6};
        System.out.println("max = " + max(v));
        System.out.println("min = " + min(v));
        int[] one = {42};                        // un solo elemento: il ciclo non gira e il risultato è corretto
        System.out.println(max(one) + " " + min(one));
    }
}
```

```text
max = -1
min = -9
42 42
```

Nessun `import`. Nessuna eccezione da dichiarare. Con l'array vuoto `v[0]` lancia `ArrayIndexOutOfBoundsException` (non controllata): se la traccia lo prevede, controllare `v.length == 0` prima.

### Ricerca sequenziale con restituzione della posizione

*Quando si usa:* "restituire la posizione del primo elemento uguale a…, oppure −1".

```java
public class SkRicerca {
    public static int indexOf(String[] v, String target) {
        for (int i = 0; i < v.length; i++) {
            if (v[i].equals(target)) {           // le stringhe si confrontano con equals, non con ==
                return i;
            }
        }
        return -1;                               // il ciclo è finito senza trovare nulla
    }

    public static void main(String[] args) {
        String[] names = {"Anna", "Luca", "Marta"};
        System.out.println(indexOf(names, "Luca"));
        System.out.println(indexOf(names, "Paolo"));
    }
}
```

```text
1
-1
```

Nessun `import`, nessuna eccezione. Con un array di `int` il confronto è `v[i] == target`.

### Somma degli elementi di una matrice irregolare

*Quando si usa:* "la matrice contiene righe di lunghezza diversa".

```java
public class SkMatrice {
    public static int sum(int[][] m) {
        int total = 0;
        for (int i = 0; i < m.length; i++) {             // m.length = numero di righe
            for (int j = 0; j < m[i].length; j++) {      // m[i].length = colonne della riga i
                total = total + m[i][j];
            }
        }
        return total;
    }

    public static void main(String[] args) {
        int[][] m = {{4, 7}, {9}, {}, {1, 2, 3}};
        System.out.println(sum(m));
    }
}
```

```text
26
```

Nessun `import`, nessuna eccezione. Il limite del ciclo interno è `m[i].length`, mai `m[0].length`.

### Copia di un array

*Quando si usa:* serve un secondo array indipendente, non un alias.

```java
import java.util.Arrays;

public class SkCopia {
    public static int[] copy(int[] source) {
        int[] result = new int[source.length];           // nuovo array, stessa lunghezza
        for (int i = 0; i < source.length; i++) {
            result[i] = source[i];                       // copia elemento per elemento
        }
        return result;
    }

    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = copy(a);
        int[] c = Arrays.copyOf(a, a.length);            // stessa cosa con la libreria
        b[0] = 100;
        c[1] = 200;
        System.out.println(Arrays.toString(a));
        System.out.println(Arrays.toString(b));
        System.out.println(Arrays.toString(c));
    }
}
```

```text
[1, 2, 3]
[100, 2, 3]
[1, 200, 3]
```

Import: `java.util.Arrays` (solo per `copyOf` e `toString`). Nessuna eccezione da dichiarare.

### Array a capacità fissa con contatore

*Quando si usa:* "una struttura dati basata su un array primitivo con dimensione massima N", con un numero di elementi, un inserimento e un'estrazione. Lo schema è quello della sezione 5.3 dentro una classe.

```java
class Buffer {
    private int[] data = new int[3];         // array primitivo, capacità massima 3
    private int count = 0;                   // quanti posti sono occupati: data[0] ... data[count - 1]

    public int size() {
        return count;
    }

    public void put(int value) {
        data[count] = value;                 // il primo posto libero è proprio data[count]
        count++;
    }

    public int take() {
        int first = data[0];                 // si estrae l'elemento più vecchio
        for (int i = 1; i < count; i++) {
            data[i - 1] = data[i];           // gli altri scorrono di un posto a sinistra
        }
        count--;
        return first;
    }
}

public class SkBuffer {
    public static void main(String[] args) {
        Buffer b = new Buffer();
        b.put(10);
        b.put(20);
        b.put(30);
        System.out.println(b.size());
        System.out.println(b.take());
        System.out.println(b.take());
        System.out.println(b.size());
        b.put(40);
        System.out.println(b.take() + " " + b.take() + " " + b.size());
    }
}
```

```text
3
10
20
1
30 40 0
```

Nessun `import`. In questo scheletro `put` e `take` non controllano se il buffer è pieno o vuoto: con `put` su un array pieno (`count == 3`) si ha `ArrayIndexOutOfBoundsException`, e con `take` su un array vuoto si restituisce un valore senza senso. Quando più thread usano il buffer, è proprio quel controllo (aspettare finché c'è posto o finché c'è un elemento) il cuore dell'esercizio: si vedrà nel [Capitolo 18 — Sincronizzazione](18-sincronizzazione.md). Il nome dei metodi, qui `size`, `put` e `take`, va **dedotto** dalle chiamate presenti nel codice che la traccia fornisce.

## Errori tipici

> [!CAUTION]
> **Errore tipico — `<=` al posto di `<` nel limite del ciclo**
> ```java
> int[] a = new int[5];
> for (int i = 0; i <= a.length; i++) {    // ERRORE LOGICO: all'ultimo giro i vale 5
>     a[i] = i;
> }
> ```
> L'ultimo indice valido è `a.length - 1`. L'ultimo giro scrive in `a[5]` e il programma termina con `ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5`. Forma corretta: `i < a.length`.

> [!CAUTION]
> **Errore tipico — Le parentesi sbagliate: `length()` e `length`**
> ```java
> int[] a = {1, 2, 3};
> System.out.println(a.length());          // ERRORE DI COMPILAZIONE: cannot find symbol, method length()
> String s = "abc";
> System.out.println(s.length);            // ERRORE DI COMPILAZIONE: cannot find symbol, variable length
> ```
> L'array ha la **variabile** `length`, la stringa ha il **metodo** `length()`. Forma corretta: `a.length` e `s.length()`.

> [!CAUTION]
> **Errore tipico — Lunghezza e lista di valori insieme, o lunghezza nel tipo**
> ```java
> int[] a = new int[3]{1, 2, 3};           // ERRORE DI COMPILAZIONE: array creation with both dimension expression and initialization is illegal
> int[5] b;                                // ERRORE DI COMPILAZIONE: ']' expected
> int[] c = new int[];                     // ERRORE DI COMPILAZIONE: array dimension missing
> ```
> La lunghezza si scrive **o** dopo `new` (`new int[3]`) **o** si ricava dalla lista (`{1, 2, 3}`), mai entrambe; nella dichiarazione del tipo le parentesi quadre sono **vuote**; con `new` senza lista la lunghezza è obbligatoria.

> [!CAUTION]
> **Errore tipico — La lista tra graffe dopo la dichiarazione**
> ```java
> int[] a;
> a = {1, 2, 3};                           // ERRORE DI COMPILAZIONE: illegal start of expression
> ```
> La forma abbreviata `{...}` vale solo **nella dichiarazione**. Forma corretta: `a = new int[] {1, 2, 3};`.

> [!CAUTION]
> **Errore tipico — Voler cambiare la lunghezza di un array**
> ```java
> int[] a = new int[3];
> a.length = 10;                           // ERRORE DI COMPILAZIONE: cannot assign a value to final variable length
> ```
> `length` è `final`: l'array non si allunga. Per avere più posti si crea un array più grande e si copia il contenuto (`a = Arrays.copyOf(a, 10);`), oppure si usa un `ArrayList`.

> [!CAUTION]
> **Errore tipico — Confrontare due array con `==` o con `equals`**
> ```java
> int[] c = {1, 2, 3};
> int[] d = {1, 2, 3};
> if (c == d) { }                          // ERRORE LOGICO: false, confronta gli indirizzi
> if (c.equals(d)) { }                     // ERRORE LOGICO: false, anche equals confronta gli indirizzi
> ```
> Per sapere se hanno gli stessi elementi si usa `Arrays.equals(c, d)` (o un ciclo che confronta lunghezza ed elementi).

> [!CAUTION]
> **Errore tipico — Pensare che `b = a` sia una copia**
> ```java
> int[] a = {1, 2, 3};
> int[] b = a;                             // ERRORE LOGICO: non è una copia, è un alias
> b[0] = 99;                               // a[0] ora vale 99
> ```
> L'assegnamento copia l'indirizzo, non gli elementi. Forma corretta: `int[] b = Arrays.copyOf(a, a.length);`.

> [!CAUTION]
> **Errore tipico — Stampare un array con `println`**
> ```java
> int[] v = {3, 1, 2};
> System.out.println(v);                   // ERRORE LOGICO: stampa qualcosa come [I@15db9742
> ```
> `[I@…` è il tipo dell'oggetto e un numero dipendente dall'esecuzione. Se la traccia chiede un formato preciso la stampa si fa con un ciclo; per una stampa rapida si usa `System.out.println(Arrays.toString(v));`.

> [!CAUTION]
> **Errore tipico — Usare il for-each per modificare gli elementi**
> ```java
> int[] v = {1, 2, 3};
> for (int x : v) {
>     x = x * 2;                           // ERRORE LOGICO: modifica la copia x, v resta {1, 2, 3}
> }
> ```
> Con i tipi primitivi `x` è una copia dell'elemento. Per scrivere negli elementi serve il `for` con l'indice: `v[i] = v[i] * 2;`.

> [!CAUTION]
> **Errore tipico — Massimo inizializzato a 0, o lettura di `v[0]` su un array vuoto**
> ```java
> int max = 0;                             // ERRORE LOGICO: con {-7, -3, -9} restituisce 0, che nell'array non c'è
> for (int i = 0; i < v.length; i++) {
>     if (v[i] > max) {
>         max = v[i];
>     }
> }
> ```
> Il candidato deve essere un elemento dell'array: `int max = v[0];` e ciclo da `i = 1`. E se l'array può essere vuoto, `v[0]` va protetto con un controllo su `v.length`.

> [!CAUTION]
> **Errore tipico — Array di oggetti senza creare gli elementi**
> ```java
> String[] p = new String[3];
> System.out.println(p[0].length());       // ERRORE A RUNTIME: NullPointerException
> ```
> `new String[3]` crea tre caselle `null`, non tre stringhe. Ogni elemento va assegnato (`p[0] = "ciao";`) prima di chiamare metodi su di esso. Con una classe propria: `shelf[0] = new Prodotto(...)`.

> [!CAUTION]
> **Errore tipico — Il limite sbagliato nelle matrici**
> ```java
> int[][] m = {{1, 2, 3}, {4}};
> for (int i = 0; i < m.length; i++) {
>     for (int j = 0; j < m[0].length; j++) {   // ERRORE LOGICO: m[0].length vale 3 per ogni riga
>         System.out.println(m[i][j]);          // alla riga 1, j = 1: ArrayIndexOutOfBoundsException
>     }
> }
> ```
> Il numero di colonne è una proprietà della **riga**: `m[i].length`. Un errore vicino: dichiarare il parametro di un metodo come `int[] m` invece di `int[][] m`. Passandogli una matrice il compilatore risponde `incompatible types: int[][] cannot be converted to int[]`.

> [!CAUTION]
> **Errore tipico — Un indice che non è un `int`**
> ```java
> int[] a = new int[3];
> double i = 1.0;
> a[i] = 5;                                // ERRORE DI COMPILAZIONE: incompatible types: possible lossy conversion from double to int
> ```
> L'indice deve essere di tipo `int` (o di un tipo che si converte in `int` senza perdita, come `char` o `short`). Con `long` e `double` serve un cast esplicito, di solito segno che il ragionamento va rivisto.

> [!CAUTION]
> **Errore tipico — Dimenticare `import java.util.Arrays`**
> ```java
> int[] a = {1, 2};
> System.out.println(Arrays.toString(a)); // ERRORE DI COMPILAZIONE: cannot find symbol, variable Arrays
> ```
> `Arrays` non è nel package `java.lang`: va importata (`import java.util.Arrays;`). L'errore consuma un'esecuzione, perché in una prova scritta un errore di compilazione conta come un tentativo.

> [!CAUTION]
> **Errore tipico — Array parziale: scorrere fino a `length`, o inserire quando è pieno**
> ```java
> for (int i = 0; i < values.length; i++) {    // ERRORE LOGICO: oltre used ci sono solo valori predefiniti
>     System.out.println(values[i]);
> }
> values[used] = next;                         // ERRORE A RUNTIME se used == values.length
> ```
> Con un array parzialmente riempito il ciclo arriva a `used`, e prima di inserire si controlla `used < values.length`.

> [!CAUTION]
> **Errore tipico — Credere che un metodo possa sostituire l'array del chiamante**
> ```java
> public static void reset(int[] v) {
>     v = new int[v.length];               // ERRORE LOGICO: cambia solo la copia locale del riferimento
> }
> ```
> Il chiamante continua a vedere il vecchio array. Si può modificare il **contenuto** dell'array ricevuto (`v[i] = 0;` in un ciclo), oppure restituire il nuovo array con `return` e assegnarlo.

## Riassunto

Un array raccoglie sotto un solo nome molti valori dello stesso tipo, numerati da 0. Si dichiara con `Tipo[]`, si crea con `new Tipo[lunghezza]` (la lunghezza non cambia più e sta nella variabile `length`) o con una lista tra graffe alla dichiarazione, e si accede agli elementi con l'indice, quasi sempre dentro un ciclo `for`. Poiché gli array sono **oggetti**, una variabile array contiene un riferimento: l'assegnamento crea un alias, `==` confronta gli indirizzi, e un metodo che riceve un array può modificarne il contenuto ma non sostituirlo al chiamante. Per copiare e confrontare servono i metodi di `java.util.Arrays`, per ordinare `Arrays.sort`. Quando la quantità di dati è variabile si usa un array parzialmente riempito con un contatore. Le matrici sono array di array: `m.length` conta le righe, `m[i].length` le colonne della riga `i`, e le righe possono avere lunghezze diverse. Un array di oggetti nasce con tutti gli elementi `null`.

**Concetti chiave**

- **Array, elemento, indice, tipo base.** Raccolta di variabili dello stesso tipo; l'indice va da 0 a `length - 1`.
- **`length`.** Variabile `final` (senza parentesi tonde); la lunghezza è fissata alla creazione.
- **Indici fuori dai limiti.** `ArrayIndexOutOfBoundsException` a tempo di esecuzione; si controlla l'indice quando viene dall'esterno; `<=` con `length` è l'errore classico.
- **Valori predefiniti.** `0`, `0.0`, `false`, `'\u0000'`, `null`.
- **Inizializzazione.** Lista `{...}` solo alla dichiarazione, `new Tipo[] {...}` altrove, oppure un elemento alla volta.
- **for-each.** Percorre un array in lettura; l'elemento è una copia, quindi non serve per modificare.
- **Array parzialmente riempito.** Array grande più un contatore `used`: elementi validi `0..used - 1`, primo posto libero `used`.
- **Array come oggetto.** `b = a` crea un alias; `==` e `equals` confrontano gli indirizzi; `Arrays.equals` confronta gli elementi.
- **Copia.** Ciclo, `Arrays.copyOf`, `Arrays.copyOfRange`, `System.arraycopy`; con gli oggetti la copia è superficiale.
- **Metodi e array.** Il parametro `int[]` riceve il riferimento: si può modificare il contenuto, non sostituire l'array; un metodo può restituire un array; `main` riceve `String[] args`.
- **Massimo e ricerca.** Il candidato parte dal primo elemento; la ricerca sequenziale restituisce l'indice o `-1`.
- **Selection sort e `Arrays.sort`.** Lo scambio richiede una variabile d'appoggio; `Arrays.sort` ordina l'array ricevuto.
- **Matrici.** Array di array; righe irregolari; cicli annidati con `m[i].length`; `Arrays.deepToString`.
- **Array di oggetti.** Gli elementi sono `null` finché non si assegna un oggetto creato con `new`.

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `Arrays` | `toString` | `static String toString(int[] a)` (e overload per gli altri tipi e `Object[]`) | — (`"null"` se `a` è `null`) |
| `Arrays` | `deepToString` | `static String deepToString(Object[] a)` | — |
| `Arrays` | `equals` | `static boolean equals(int[] a, int[] a2)` | — |
| `Arrays` | `deepEquals` | `static boolean deepEquals(Object[] a1, Object[] a2)` | — |
| `Arrays` | `sort` | `static void sort(int[] a)`, `static void sort(int[] a, int fromIndex, int toIndex)`, `static void sort(Object[] a)` | `IllegalArgumentException`, `ArrayIndexOutOfBoundsException` (intervallo); `ClassCastException` (`Object[]`) |
| `Arrays` | `copyOf` | `static int[] copyOf(int[] original, int newLength)` | `NegativeArraySizeException`, `NullPointerException` |
| `Arrays` | `copyOfRange` | `static int[] copyOfRange(int[] original, int from, int to)` | `ArrayIndexOutOfBoundsException`, `IllegalArgumentException`, `NullPointerException` |
| `System` | `arraycopy` | `static void arraycopy(Object src, int srcPos, Object dest, int destPos, int length)` | `IndexOutOfBoundsException`, `ArrayStoreException`, `NullPointerException` |
| ogni array | `length` | `final int length` (variabile, senza parentesi tonde) | — |
