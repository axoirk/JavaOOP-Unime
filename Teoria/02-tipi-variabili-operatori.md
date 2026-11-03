---
materia: Programmazione a Oggetti
capitolo: 2
titolo: Tipi primitivi, variabili e operatori
livello_syllabus: 1
stato: completo
slide: ["Savitch cap. 2 slide 7-64, 104-107", "Savitch cap. 3 slide 13-22, 35-37, 43-44, 47-55", "Savitch cap. 9 slide 21", "Lect2 (Variable, Literal Constants, Named Constant, Primitive Data Types, Reference types, Assignments and Expressions)"]
appelli: [EXAM2, EXAM4]
fonti_esterne: 3
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 2 — Tipi primitivi, variabili e operatori

## Di cosa parla questo capitolo

Un programma serve a elaborare dati: numeri, lettere, vero e falso. Per elaborarli bisogna poterli ricordare da qualche parte, dare loro un nome e dire al compilatore di che genere sono. Questo capitolo riguarda proprio questo: le **variabili**, i **tipi primitivi** che descrivono i dati più semplici, e gli **operatori** con cui si combinano per ottenere nuovi valori. Riprende la struttura di un file e il metodo `main` del [Capitolo 1 — Java e la JVM](01-java-e-la-jvm.md), che ora riempiamo di istruzioni vere.

Il capitolo ha un filo conduttore: in Java ogni valore ha un tipo, e il tipo decide che cosa si può fare con quel valore e che risultato dà un'operazione. Una divisione tra due interi dà un intero, una tra un intero e un `double` dà un `double`, un confronto dà un `boolean`. Quasi tutti gli errori di questo livello nascono dal non pensare al tipo di ciò che si sta scrivendo, e sono gli errori che l'esame scritto punisce di più, perché il programma compila, gira, e stampa un numero sbagliato.

Alla fine del capitolo saprai dichiarare e inizializzare variabili e costanti, scegliere tra gli otto tipi primitivi, prevedere il tipo e il valore di un'espressione aritmetica o logica, convertire un valore da un tipo a un altro (e sapere quando la conversione perde informazione), e riconoscere a colpo d'occhio le trappole della divisione tra interi e del confronto tra numeri in virgola mobile.

## 2.1 Variabili

Una **variabile** è un nome dato a una posizione della memoria in cui il programma conserva un dato. Il dato conservato si chiama **valore** della variabile, e può cambiare durante l'esecuzione: da qui il nome. Nel [Capitolo 1](01-java-e-la-jvm.md) abbiamo visto che la memoria principale è una sequenza di byte numerati; le variabili ci permettono di non occuparci degli indirizzi e di ragionare con nomi come `count` o `speed`.

### 2.1.1 Dichiarare una variabile

Prima di usare una variabile bisogna **dichiararla**, cioè dire al compilatore il suo nome e il suo **tipo**. Il tipo stabilisce quali valori la variabile può contenere (numeri interi, numeri con la virgola, un carattere…) e quanta memoria occupa. La sintassi è:

```text
tipo variabile_1, variabile_2, ...;
```

Il tipo si scrive una volta sola, seguito dai nomi delle variabili separati da virgole. Per esempio:

```java
int styleChoice, numberOfChecks;   // due variabili intere
double balance, interestRate;      // due numeri in virgola mobile
char jointOrIndividual;            // un carattere
```

Questo frammento è una sequenza di dichiarazioni (per eseguirlo va messo dentro un metodo, come `main`). Ogni dichiarazione termina con il punto e virgola. Java è un linguaggio **fortemente tipizzato** (*strongly typed*): una variabile dichiarata `int` resta `int` per tutta la sua vita e non può contenere, per esempio, un numero con la virgola. È il compilatore a far rispettare questa regola, prima ancora che il programma parta.

Una variabile deve essere dichiarata **prima** di essere usata. Si dichiara subito prima del primo utilizzo oppure all'inizio del blocco di graffe `{ }` che la contiene, per esempio all'inizio di `main`.

### 2.1.2 Identificatori, parole chiave e convenzioni

Il nome di una variabile (come il nome di una classe o di un metodo) è un **identificatore**. Le regole del linguaggio sono precise:

- un identificatore può contenere **lettere**, **cifre** (da 0 a 9), il carattere di sottolineatura `_` e il simbolo `$` (che ha un significato speciale e per ora non si usa);
- il **primo carattere non può essere una cifra**;
- non può contenere spazi, punti, asterischi o altri simboli: `7-11`, `oracle.com` e `util.*` non sono identificatori validi;
- può essere lungo quanto si vuole;
- Java distingue **maiuscole e minuscole** (*case sensitive*): `stuff`, `Stuff` e `STUFF` sono tre identificatori diversi.

Alcune parole hanno un significato predefinito nel linguaggio e si chiamano **parole chiave** (*keywords*) o **parole riservate**: `int`, `public`, `class`, `if`, `while`, `static`, `final` e così via. Non si possono usare come identificatori.

Oltre alle regole obbligatorie esistono le **convenzioni di nome**, che il compilatore non controlla ma che tutti i programmatori Java rispettano, perché rendono il codice leggibile:

| Che cosa | Convenzione | Esempi |
|---|---|---|
| Classi | iniziale **maiuscola** | `String`, `Scanner`, `Orologio` |
| Tipi primitivi | tutto **minuscolo** | `int`, `double`, `boolean` |
| Variabili, metodi | iniziale **minuscola** | `myName`, `myBalance`, `taxRate` |
| Nomi di più parole | iniziale maiuscola a ogni parola dopo la prima (*camel case*) | `numberOfBaskets`, `eggsPerBasket` |
| Costanti | tutto **maiuscolo**, parole separate da `_` | `PI`, `INTEREST_RATE` |

Il nome di una variabile deve **suggerire il suo uso**: `count` e `speed` sono nomi utili, `c` e `s` no.

> [!WARNING]
> **Attenzione — `Totale` e `totale` sono variabili diverse**
> Poiché Java distingue maiuscole e minuscole, scrivere `Totale = 5;` quando la variabile dichiarata è `totale` è un errore: il compilatore risponde `cannot find symbol`. Lo stesso vale per i nomi delle classi della libreria: `string` non è `String` e `system` non è `System` (errori già visti nel Capitolo 1).

### 2.1.3 Variabili non inizializzate

Una variabile appena dichiarata esiste, ma non ha ancora un valore sensato: si dice **non inizializzata**. Per i campi di una classe (che vedremo nel [Capitolo 7](07-classi-e-oggetti.md)) Java assegna un valore predefinito, mentre per una **variabile locale**, cioè dichiarata dentro un metodo, il compilatore pretende che le venga assegnato un valore prima del primo uso, altrimenti rifiuta il programma. Vale la regola: non contare mai sui valori predefiniti.

Per evitare il problema alla radice si assegna un valore **al momento della dichiarazione**, con la sintassi:

```text
tipo variabile_1 = espressione_1, variabile_2 = espressione_2, ...;
```

Per esempio:

```java
int count = 0;
char grade = 'A';
```

Le variabili di tipo riferimento (come `String`), se non inizializzate, valgono `null`, cioè "nessun oggetto" (lo vedremo nel [Capitolo 8](08-riferimenti-e-memoria.md)).

## 2.2 I tipi primitivi

I dati di un programma si dividono in due grandi famiglie. I **tipi primitivi** descrivono valori semplici e indivisibili: un numero, un carattere, un valore di verità. I **tipi classe** (o tipi riferimento) descrivono oggetti, che hanno sia dati sia metodi; `String` è un tipo classe, e `"Java is fun"` è un valore di tipo `String`. In questo capitolo ci occupiamo solo dei primitivi; i tipi classe tornano dal [Capitolo 3](03-stringhe-e-console.md) in poi.

### 2.2.1 Gli otto tipi

Java ha **otto** tipi primitivi, divisi per categoria:

- quattro tipi per i numeri **interi**: `byte`, `short`, `int`, `long`;
- due tipi per i numeri **in virgola mobile** (con la parte frazionaria): `float` e `double`;
- un tipo per i **caratteri**: `char`;
- un tipo per i **valori di verità**: `boolean`.

I tipi `int` e `double` sono i più usati: `int` per i numeri interi, `double` per quelli con la virgola. I tipi interi e `char` si chiamano insieme **tipi integrali**; i tipi integrali e quelli in virgola mobile sono i **tipi numerici** (o aritmetici).

La differenza fra i tipi interi è lo spazio che occupano, e quindi l'intervallo di valori che possono contenere. Più bit ha un tipo, più valori distinti può rappresentare.

| Tipo | Categoria | Dimensione | Valore minimo | Valore massimo |
|---|---|---|---|---|
| `byte` | intero | 8 bit | −128 | 127 |
| `short` | intero | 16 bit | −32768 | 32767 |
| `int` | intero | 32 bit | −2147483648 | 2147483647 |
| `long` | intero | 64 bit | −9223372036854775808 | 9223372036854775807 |
| `float` | virgola mobile | 32 bit | −3.4028235E38 | 3.4028235E38 (circa 3.4 · 10<sup>38</sup>) |
| `double` | virgola mobile | 64 bit | −1.7976931348623157E308 | 1.7976931348623157E308 (circa 1.8 · 10<sup>308</sup>) |
| `char` | carattere | 16 bit | `'\u0000'` (codice 0) | `'￿'` (codice 65535) |
| `boolean` | verità | | `false` | `true` |

Per i tipi in virgola mobile il minimo è l'opposto del massimo, e i valori indicati sono i limiti finiti (oltre c'è l'infinito, sezione 2.5.3). Per `boolean` ci interessa solo che abbia due valori, `true` e `false`, e non quanti bit occupi. I valori della tabella non vanno imparati a memoria: li forniscono le costanti `MIN_VALUE` e `MAX_VALUE` delle classi `Byte`, `Short`, `Integer`, `Long` e così via (vedi il riquadro più sotto). Conviene però ricordare un ordine di grandezza: un `int` arriva a circa 2 miliardi, un `long` a circa 9 miliardi di miliardi.

> [!NOTE]
> **Approfondimento esterno — Intervalli dei tipi numerici**
> Le classi `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double` e `Character` del package `java.lang` hanno ciascuna due costanti pubbliche che danno i limiti del tipo corrispondente. Per esempio, in `Integer`:
> ```text
> public static final int MIN_VALUE   // -2^31
> public static final int MAX_VALUE   //  2^31 - 1
> ```
> Per i tipi in virgola mobile attenzione a `Double.MIN_VALUE`: non è il numero più negativo, ma il **più piccolo numero positivo diverso da zero** (circa `4.9E-324`). Il numero più negativo è `-Double.MAX_VALUE`. `Double` fornisce anche le costanti `POSITIVE_INFINITY` e `NaN` (*Not a Number*), che compaiono nel risultato di certe operazioni (sezione 2.5.3).
> *Fonte:* [Integer, Double, Long, Byte, Short, Float, Character (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Integer.html)

#### Esempio — Stampare i limiti dei tipi

Il programma seguente chiede a Java stesso quali sono i limiti dei tipi.

```java
public class LimitiDeiTipi {
    public static void main(String[] args) {
        System.out.println("byte  : " + Byte.MIN_VALUE + " .. " + Byte.MAX_VALUE);
        System.out.println("short : " + Short.MIN_VALUE + " .. " + Short.MAX_VALUE);
        System.out.println("int   : " + Integer.MIN_VALUE + " .. " + Integer.MAX_VALUE);
        System.out.println("long  : " + Long.MIN_VALUE + " .. " + Long.MAX_VALUE);
        System.out.println("float : max " + Float.MAX_VALUE);
        System.out.println("double: max " + Double.MAX_VALUE);
        // il cast (int) trasforma il carattere nel suo codice numerico (sezione 2.6.3)
        System.out.println("char  : " + (int) Character.MIN_VALUE + " .. " + (int) Character.MAX_VALUE);
    }
}
```

Ogni riga costruisce una stringa con l'operatore `+` (che con le stringhe concatena, [Capitolo 3](03-stringhe-e-console.md)) e la stampa. L'output è:

```text
byte  : -128 .. 127
short : -32768 .. 32767
int   : -2147483648 .. 2147483647
long  : -9223372036854775808 .. 9223372036854775807
float : max 3.4028235E38
double: max 1.7976931348623157E308
char  : 0 .. 65535
```

I numeri in virgola mobile molto grandi o molto piccoli vengono stampati in **notazione scientifica**: `3.4028235E38` significa 3.4028235 · 10<sup>38</sup>.

### 2.2.2 I letterali

Un valore scritto direttamente nel codice si chiama **letterale** (*literal*) o costante letterale. Il tipo di un letterale si legge da come è scritto:

- un numero **senza punto decimale** (`0`, `365`, `-1`, `12000`) è un letterale di tipo `int`. Non si scrivono virgole come separatori (`12,000` è un errore) e non si usano zeri iniziali;
- se il valore non sta in un `int`, si aggiunge una **`L`** finale e il letterale diventa `long`: `3000000000L`;
- un numero **con il punto decimale** (`0.99`, `-22.8`, `3.14159`, `5.0`) è un letterale di tipo `double`;
- per ottenere un `float` si aggiunge una **`f`** finale: `3.14f`;
- un numero molto grande o molto piccolo si può scrivere in **notazione scientifica** (o notazione *e*): `865000000.0` si scrive `8.65e8` e `0.000483` si scrive `4.83e-4`. Il numero prima della `e` non ha bisogno del punto decimale. Il risultato è sempre un `double`;
- un singolo carattere si scrive tra **apici singoli**: `'a'`, `'A'`, `'#'`, `' '` sono letterali di tipo `char`;
- un testo si scrive tra **virgolette doppie**: `"This is a string of characters"` è un letterale di tipo `String` (non un tipo primitivo, [Capitolo 3](03-stringhe-e-console.md));
- `true` e `false` sono i due letterali di tipo `boolean`.

Un letterale numerico può essere preceduto dal segno `+` o `-`.

```java
public class Letterali {
    public static void main(String[] args) {
        int a = 365;                    // letterale int
        long grande = 3000000000L;      // senza la L non starebbe in un int
        double d = 5.0;                 // letterale double
        float f = 3.14f;                // la f finale lo rende float
        double scientifico = 8.65e8;    // 865000000.0
        double piccolo = 4.83e-4;       // 0.000483
        char lettera = 'W';             // apici singoli
        boolean vero = true;
        System.out.println(a);
        System.out.println(grande);
        System.out.println(d);
        System.out.println(f);
        System.out.println(scientifico);
        System.out.println(piccolo);
        System.out.println(lettera);
        System.out.println(vero);
    }
}
```

Ogni variabile riceve un valore del suo stesso tipo. L'output è:

```text
365
3000000000
5.0
3.14
8.65E8
4.83E-4
W
true
```

Si noti che `System.out.println` stampa un `double` sempre con la parte decimale (`5.0`) e usa la notazione scientifica per i valori molto grandi o molto piccoli (`8.65E8`).

> [!WARNING]
> **Attenzione — Lo zero iniziale cambia il valore**
> Un letterale intero che comincia con `0` non è scritto in base dieci: `010` vale 8, non 10 (è un numero scritto in base otto). Per questo, scrivendo numeri, non si mettono zeri iniziali: `System.out.println(010);` stampa `8`.

### 2.2.3 I numeri in virgola mobile sono approssimati

Un computer memorizza ogni numero con un numero finito di bit. Gli interi sono rappresentati esattamente (purché stiano nell'intervallo del tipo), ma i numeri con la parte frazionaria no: spesso `float` e `double` conservano soltanto un'**approssimazione** del valore matematico. Il motivo è lo stesso per cui in base dieci non si riesce a scrivere esattamente un terzo (`0.3333…`): anche in base due ci sono frazioni, come `0.1`, che richiederebbero infinite cifre.

Le conseguenze sono concrete, e vale la pena vederle una volta.

```java
public class Approssimazioni {
    public static void main(String[] args) {
        System.out.println(0.1 + 0.2);          // non è 0.3
        System.out.println(1.0 / 3.0);
        System.out.println(0.1 + 0.2 == 0.3);   // il confronto con == fallisce
        double tolleranza = 1e-9;
        double differenza = Math.abs((0.1 + 0.2) - 0.3);
        System.out.println(differenza < tolleranza);   // il confronto con tolleranza funziona
    }
}
```

La prima riga stampa un valore che si discosta da `0.3` nell'ultima cifra; la seconda stampa un terzo con un numero finito di cifre; la terza mostra che due numeri "uguali" in matematica non lo sono per `==`; la quarta usa il metodo `Math.abs` (valore assoluto, [Capitolo 6](06-metodi.md)) per confrontare i due numeri a meno di una piccola **tolleranza**. L'output è:

```text
0.30000000000000004
0.3333333333333333
false
true
```

Da qui la regola: `==` va bene per interi e caratteri, **non** per confrontare due numeri in virgola mobile. Per quelli si confronta la differenza con una tolleranza (`Math.abs(b - c) < epsilon`).

> [!TIP]
> **Intuizione — Il righello senza i millimetri**
> Pensa a un righello graduato solo in centimetri: puoi misurare 3 cm o 4 cm, ma 3.5 cm solo in modo approssimato. Un `double` ha una "graduazione" molto più fine di un righello, ma non infinitamente fine: alcuni valori cadono tra due tacche e vengono sostituiti con la tacca più vicina. Quando fai calcoli, le piccole differenze si accumulano e due strade diverse per arrivare allo stesso valore possono finire su tacche diverse.

### 2.2.4 `char`: un carattere è un numero

Una variabile `char` contiene un **carattere**, ma internamente è un numero: il codice di quel carattere nella tabella **Unicode**. Unicode comprende i caratteri di molti alfabeti e include la più semplice tabella ASCII (le lettere inglesi, le cifre, la punteggiatura). Un `char` occupa 16 bit, quindi i suoi codici vanno da 0 a 65535 (tabella della sezione 2.2.1).

Il fatto che un `char` sia un numero ha conseguenze sull'aritmetica, che vediamo nella sezione 2.6.2. Ricorda intanto due cose: un carattere si scrive tra **apici singoli** (`'a'`), mentre un testo tra **virgolette doppie** (`"a"`); e `'a'` e `"a"` sono due cose di tipo diverso, un `char` e una `String` di un carattere. Le sequenze di escape come `'\n'` e `'\''` si trattano nel [Capitolo 3](03-stringhe-e-console.md).

### 2.2.5 Tipi primitivi e tipi riferimento

Esiste una differenza profonda fra i due modi di conservare un dato, e conviene fissarla subito.

Una variabile di **tipo primitivo** contiene direttamente il suo valore. Dopo `int x = 5;` la posizione di memoria chiamata `x` contiene il numero 5. Un valore primitivo **non è un oggetto**: non ha metodi, non si scrive `x.qualcosa()`.

Una variabile di **tipo riferimento** (*reference type*), come `String name;`, contiene invece il **riferimento** a un oggetto, cioè l'indirizzo della zona di memoria (lo *heap*, [Capitolo 1](01-java-e-la-jvm.md)) dove l'oggetto si trova. Il programmatore non può fare calcoli sull'indirizzo: può solo assegnarlo ad altre variabili dello stesso tipo e usarlo per raggiungere l'oggetto.

| | Tipo primitivo | Tipo riferimento |
|---|---|---|
| Esempi | `int`, `double`, `char`, `boolean` | `String`, le classi, gli array |
| Cosa contiene la variabile | il valore stesso | l'indirizzo di un oggetto |
| Ha metodi? | no | sì |
| Valore se non inizializzata (campo) | `0`, `0.0`, `false` | `null` |

Questa differenza spiega comportamenti importanti, come quello del confronto con `==` e del passaggio di parametri ai metodi; li approfondiremo nel [Capitolo 6 — Metodi](06-metodi.md) e nel [Capitolo 8 — Riferimenti e memoria](08-riferimenti-e-memoria.md). Per ogni tipo primitivo esiste anche una **classe wrapper** (`Integer` per `int`, `Double` per `double`, `Character` per `char`…) che avvolge il valore in un oggetto: la incontreremo nel Capitolo 6.

## 2.3 L'assegnamento

L'**istruzione di assegnamento** (*assignment statement*) dà un valore a una variabile:

```text
variabile = espressione;
```

Il simbolo `=` è l'**operatore di assegnamento**, e si legge "diventa" o "riceve", non "è uguale a". L'espressione a destra può essere un letterale, un'altra variabile, una costante, o una combinazione di tutti questi elementi con degli operatori (`+`, `-`, …). Esempi:

```text
amount = 3.99;
firstInitial = 'W';
score = numberOfCards + handicap;
eggsPerBasket = eggsPerBasket - 2;
```

L'ultima riga mostra che a destra dell'`=` può comparire anche la variabile stessa. Succede perché l'assegnamento si esegue in due tempi:

1. si **valuta l'espressione** a destra, usando i valori che le variabili hanno in quel momento;
2. il risultato viene **scritto nella variabile** a sinistra, cancellando il valore precedente.

Se `eggsPerBasket` vale 6, in `eggsPerBasket = eggsPerBasket - 2;` si calcola prima `6 - 2`, cioè 4, poi si scrive 4 in `eggsPerBasket`.

#### Esempio — Uova e cestini

Il programma calcola il numero totale di uova in un certo numero di cestini e poi ne toglie due per cestino.

```java
public class Cestini {
    public static void main(String[] args) {
        int numberOfBaskets, eggsPerBasket, totalEggs;   // dichiarazione di tre variabili
        numberOfBaskets = 10;                            // assegnamento di un letterale
        eggsPerBasket = 6;
        totalEggs = numberOfBaskets * eggsPerBasket;     // l'espressione usa due variabili
        System.out.println("Uova totali: " + totalEggs);

        eggsPerBasket = eggsPerBasket - 2;               // prima si calcola 6 - 2, poi si scrive 4
        totalEggs = numberOfBaskets * eggsPerBasket;     // va ricalcolato: totalEggs non si aggiorna da solo
        System.out.println("Uova totali dopo averne tolte due per cestino: " + totalEggs);
    }
}
```

L'output è:

```text
Uova totali: 60
Uova totali dopo averne tolte due per cestino: 40
```

Il dettaglio importante è nella penultima riga: `totalEggs` conserva il valore calcolato prima e **non si aggiorna da solo** quando cambia `eggsPerBasket`. Una variabile non è una formula: è una scatola che contiene un valore. Se i dati da cui dipende cambiano, il calcolo va rifatto.

Un'espressione di assegnamento è a sua volta un'espressione, con un valore: il valore assegnato. Perciò si possono concatenare più assegnamenti.

```java
public class AssegnamentiMultipli {
    public static void main(String[] args) {
        int a, b, x, y;
        x = y = 0;               // y riceve 0, poi x riceve il valore di (y = 0), cioè 0
        a = 5 + (b = 4);         // (b = 4) vale 4 e assegna 4 a b; poi a riceve 5 + 4
        System.out.println(x + " " + y);
        System.out.println(a + " " + b);
    }
}
```

La catena `x = y = 0` si legge da destra a sinistra. L'output è:

```text
0 0
9 4
```

Gli assegnamenti incorporati dentro altre espressioni, come `a = 5 + (b = 4)`, si possono scrivere ma rendono il codice difficile da leggere; all'esame conviene evitarli.

## 2.4 Le costanti con nome

Un numero scritto direttamente nel codice, come `3.14159` o `6.65`, si chiama **costante letterale** (*literal constant*). Usarla nel mezzo di un programma è sconsigliato per due motivi. Il primo è la leggibilità: nell'espressione `area = 3.14159 * radius * radius;` non è ovvio che `3.14159` sia il pi greco. Il secondo è la manutenzione: se lo stesso valore compare in venti punti e va cambiato, bisogna modificarli tutti, e si rischia di cambiare per errore un altro numero che per caso aveva lo stesso valore.

La soluzione è la **costante con nome** (*named constant*): una variabile a cui si dà un nome significativo, si assegna il valore una sola volta e si impedisce che venga mai modificata. In Java si ottiene con la parola chiave **`final`**:

```text
public static final Tipo NOME = valore;
```

Per esempio:

```java
public static final double PI = 3.14159;
public static final String MOTTO = "The customer is always right.";
```

`final` vuol dire "non modificabile dopo l'assegnamento": un tentativo di cambiare il valore è un errore di compilazione. Per convenzione il nome di una costante si scrive in **lettere maiuscole**, con il carattere `_` tra una parola e l'altra (`INTEREST_RATE`). La costante si dichiara all'interno della classe, fuori dai metodi, in modo che sia visibile in tutta la classe, e di solito all'inizio. `public` e `static` hanno un significato preciso (accessibile dall'esterno, appartenente alla classe e non a un singolo oggetto) che spiegheremo nei capitoli [6](06-metodi.md) e [7](07-classi-e-oggetti.md); per ora si ricopia la forma `public static final`. Il valore va fissato **nella stessa riga** della dichiarazione.

Una costante si può dichiarare anche *dentro* un metodo, e in quel caso basta `final`, ad esempio `final int GIORNI_SETTIMANA = 7;`.

```java
public class AreaCerchio {
    public static final double PI = 3.14159;    // costante di classe, fuori dai metodi

    public static void main(String[] args) {
        double radius = 2.0;
        double area = PI * radius * radius;     // si legge: pi greco per raggio al quadrato
        System.out.println("Area: " + area);
    }
}
```

La costante `PI` è visibile dentro `main` perché sta nella stessa classe. L'output è:

```text
Area: 12.56636
```

Se in seguito servisse una precisione maggiore, basterebbe cambiare il valore di `PI` in un solo punto del programma.

## 2.5 Operatori aritmetici

Le espressioni aritmetiche si formano con i quattro operatori `+`, `-`, `*`, `/` e con l'operatore **resto** (o *modulo*) `%`, applicati a variabili e numeri chiamati **operandi**. Un'espressione con più operatori si può vedere come una successione di passi, ciascuno con due soli operandi: il risultato di un passo diventa operando del passo successivo.

### 2.5.1 Il tipo del risultato

Il tipo del risultato dipende dal tipo degli operandi, secondo due regole:

- se **entrambi gli operandi hanno lo stesso tipo**, il risultato ha quel tipo;
- se i tipi sono **diversi**, il risultato ha il tipo "più a destra" nella catena

```text
byte -> short -> int -> long -> float -> double
```

Per esempio, se `hoursWorked` è un `int` che vale 40 e `payRate` è un `double` che vale 8.25, allora `hoursWorked * payRate` è un `double`, e vale 330.0. Un'espressione che mescola un intero e un numero in virgola mobile dà sempre un risultato in virgola mobile.

### 2.5.2 La divisione tra interi e il resto

L'operatore `/` si comporta come ci si aspetta se almeno un operando è in virgola mobile. Se **entrambi gli operandi sono interi**, il risultato è un intero: la parte frazionaria viene **troncata**, cioè buttata via, non arrotondata. Quindi `99 / 100` vale `0`, non `0.99`.

L'operatore **`%`** (*mod*, resto) si usa con operandi interi e dà il **resto** della divisione intera. Poiché 14 diviso 4 fa 3 con il resto di 2, `14 / 4` vale `3` e `14 % 4` vale `2`. Il resto serve soprattutto in due casi: per sapere se un numero è pari o dispari (`n % 2` vale 0 o 1) e per sapere se un intero è divisibile per un altro (`n % d == 0`).

```java
public class Divisioni {
    public static void main(String[] args) {
        int hoursWorked = 40;
        double payRate = 8.25;
        System.out.println(hoursWorked * payRate);   // int * double = double
        System.out.println(99 / 100);                // entrambi int: troncato
        System.out.println(99 / 100.0);              // un double: divisione vera
        System.out.println(14 / 4);                  // 3
        System.out.println(14 % 4);                  // 2
        System.out.println(-7 / 2);                  // tronca verso lo zero
        System.out.println(-7 % 2);                  // il resto ha il segno del dividendo
    }
}
```

Ogni riga mette alla prova una regola. L'output è:

```text
330.0
0
0.99
3
2
-3
-1
```

Le ultime due righe mostrano che con operandi negativi il troncamento va **verso lo zero** (−3,5 diventa −3, non −4) e che il resto ha il segno del dividendo, in modo che valga sempre la relazione `(a / b) * b + (a % b) == a`.

> [!IMPORTANT]
> **Nota del docente — La divisione tra interi**
> È l'insidia più tipica del Livello 1: `(a + b) / 2` con `a` e `b` interi non calcola la media, ma la media troncata, e l'errore si manifesta solo come un risultato sbagliato. Se il risultato deve avere la parte decimale, almeno uno degli operandi deve essere in virgola mobile *prima* della divisione (sezione 2.6.3).

#### Esempio — Una media che sembra giusta

Il metodo `mediaSbagliata` ha l'aspetto di una media, ma commette un errore logico (il terzo tipo di errore del [Capitolo 1](01-java-e-la-jvm.md)): il programma compila, gira e stampa un numero sbagliato.

```java
public class Medie {
    static double mediaSbagliata(int a, int b) {
        return (a + b) / 2;            // la divisione è tra due int: viene troncata
    }

    static double mediaGiusta(int a, int b) {
        return (a + b) / 2.0;          // 2.0 è un double: la divisione è in virgola mobile
    }

    public static void main(String[] args) {
        System.out.println(mediaSbagliata(3, 4));
        System.out.println(mediaGiusta(3, 4));
    }
}
```

In `mediaSbagliata`, `a + b` vale 7 ed è un `int`; `7 / 2` fra interi dà `3`; solo dopo il valore `3` viene convertito in `double` per essere restituito, e diventa `3.0`. In `mediaGiusta` il denominatore `2.0` è un `double`, quindi `7 / 2.0` dà `3.5`. Il dettaglio fondamentale è che il tipo del risultato si decide **prima** della conversione per il `return`. L'output è:

```text
3.0
3.5
```

### 2.5.3 Divisione per zero e superamento dei limiti

Due situazioni portano un'operazione fuori dai valori normali.

**Divisione per zero.** Dividere un intero per zero (`5 / 0`, oppure `5 % 0`) è un errore di esecuzione: la JVM lancia l'eccezione `java.lang.ArithmeticException` con il messaggio `/ by zero`, e il programma si interrompe se l'eccezione non viene gestita ([Capitolo 13](13-eccezioni.md)). Con i numeri in virgola mobile invece **non c'è nessuna eccezione**: `5 / 0.0` vale `Infinity`, `-5 / 0.0` vale `-Infinity` e `0.0 / 0.0` vale `NaN` (*Not a Number*).

> [!NOTE]
> **Approfondimento esterno — `ArithmeticException` e le costanti di `Double`**
> `ArithmeticException` è una classe di `java.lang` che estende `RuntimeException`: è quindi un'eccezione **non controllata** (*unchecked*), che non va dichiarata con `throws`. La documentazione la descrive così: "Thrown when an exceptional arithmetic condition has occurred. For example, an integer "divide by zero" throws an instance of this class." Il risultato di una divisione in virgola mobile per zero è invece rappresentato dalle costanti `Double.POSITIVE_INFINITY`, `Double.NEGATIVE_INFINITY` e `Double.NaN`.
> *Fonte:* [ArithmeticException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/ArithmeticException.html)

**Superamento dei limiti** (*overflow*). Un `int` ha un intervallo limitato. Se un'operazione produce un valore fuori da quell'intervallo, Java **non** segnala nulla: il risultato "torna a capo" dall'altra parte dell'intervallo, come il contachilometri di un'automobile che supera il suo massimo e riparte da zero.

```java
public class Overflow {
    public static void main(String[] args) {
        int max = Integer.MAX_VALUE;
        System.out.println(max);
        System.out.println(max + 1);       // oltre il massimo: nessun errore, risultato senza senso
        long grande = max + 1L;            // 1L è un long: l'addizione avviene tra long
        System.out.println(grande);
        System.out.println(5 / 0.0);       // in virgola mobile niente eccezione
    }
}
```

Nella seconda riga dell'output `max + 1` vale il minimo, perché si avvolge. Nella terza l'addizione è già fatta tra `long`, e il risultato è corretto. L'output è:

```text
2147483647
-2147483648
2147483648
Infinity
```

La lezione è che quando si prevedono numeri grandi bisogna scegliere `long` fin dalla dichiarazione, perché l'errore di overflow non produce alcun messaggio.

### 2.5.4 Precedenza e parentesi

Quando un'espressione contiene più operatori, Java segue le **regole di precedenza** (*precedence rules*): gli operatori con precedenza più alta si eseguono prima. Le regole fondamentali per l'aritmetica:

- gli operatori **unari** (con un solo operando: `+`, `-`, `++`, `--`, `!`, e il cast) hanno precedenza **più alta** dei binari;
- `*`, `/`, `%` hanno precedenza più alta di `+` e `-` binari;
- a **parità di precedenza** gli operatori binari si eseguono da **sinistra a destra**; gli operatori unari da destra a sinistra.

Le **parentesi** cambiano l'ordine: ciò che sta tra parentesi si calcola per primo. Esempio: `balance + interestRate * balance` calcola prima il prodotto, e le parentesi `balance + (interestRate * balance)` non cambiano il risultato ma rendono chiaro l'ordine a chi legge. Gli spazi, invece, non hanno alcun effetto sulla precedenza.

Una tabella completa degli operatori di questo capitolo, dal più forte al più debole, è nella sezione 2.7.4. La regola pratica è: **quando hai un dubbio, metti le parentesi**. Costano un carattere e tolgono ogni ambiguità.

### 2.5.5 Gli assegnamenti composti

Un'operazione come `amount = amount + 5;` è così frequente che esiste una forma abbreviata: l'**assegnamento composto**. Si ottiene scrivendo l'operatore aritmetico prima dell'`=`.

| Forma abbreviata | Equivale a |
|---|---|
| `amount += 5;` | `amount = amount + 5;` |
| `amount -= 5;` | `amount = amount - 5;` |
| `amount *= 5;` | `amount = amount * 5;` |
| `amount /= 5;` | `amount = amount / 5;` |
| `amount %= 5;` | `amount = amount % 5;` |

> [!WARNING]
> **Attenzione — L'assegnamento composto fa un cast nascosto**
> Con `x` di tipo `int`, l'istruzione `x *= 1.5;` compila, pur moltiplicando per un `double`: l'assegnamento composto converte da solo il risultato nel tipo di `x`, troncandolo. Se `x` vale 5, dopo `x *= 1.5;` vale `7` (e non `7.5`: un `int` non può contenere la parte frazionaria). La forma estesa `x = x * 1.5;` invece non compila, come spiega la sezione 2.6.1.

### 2.5.6 Incremento e decremento

Aumentare o diminuire di 1 una variabile è un'operazione così comune che ha due operatori dedicati: l'**incremento** `++` e il **decremento** `--`. Le tre scritture seguenti sono equivalenti quando compaiono come istruzione a sé:

```text
count++;     ++count;     count = count + 1;
count--;     --count;     count = count - 1;
```

La differenza fra `count++` (forma **postfissa**) e `++count` (forma **prefissa**) emerge quando l'operatore sta dentro un'espressione più grande:

- `++m` **prima** incrementa `m` e **poi** usa il nuovo valore nell'espressione;
- `m++` **usa** il valore attuale di `m` nell'espressione e **poi** incrementa.

In entrambi i casi, alla fine, `m` è stata incrementata di 1.

```java
public class Incrementi {
    public static void main(String[] args) {
        int m = 4;
        int result = 3 * (++m);      // m diventa 5, poi si calcola 3 * 5
        System.out.println(result + " " + m);

        m = 4;
        result = 3 * (m++);          // si usa 4, poi m diventa 5: 3 * 4
        System.out.println(result + " " + m);
    }
}
```

Nella prima parte `result` vale `15` e `m` vale `5`; nella seconda `result` vale `12` e `m` vale ancora `5`. L'output è:

```text
15 5
12 5
```

Per leggere o scrivere codice senza trabocchetti, conviene usare `++` e `--` quasi sempre come istruzioni isolate (`count++;`), come nei cicli del [Capitolo 4](04-strutture-di-controllo.md), e riconoscerli quando li si incontra dentro altre espressioni.

#### Esempio — Il resto in monete

Un caso d'uso completo di divisione intera e resto: dato un importo da 1 a 99 centesimi, trovare una combinazione di monete che lo costituisca, usando il minor numero di monete di taglio 25, 10, 5 e 1. Il metodo: il numero di monete da 25 è la divisione intera dell'importo per 25; il **resto** di quella divisione è l'importo ancora da coprire; si ripete con 10, con 5, e infine l'avanzo sono le monete da 1.

Prima di scrivere il codice conviene notare un tranello: se l'importo di partenza viene modificato mentre si calcola, il suo valore originale va perso. Per questo il programma ne conserva una copia in `originalAmount`.

```java
public class ResoInMonete {
    public static void main(String[] args) {
        int amount = 87;                          // importo da scomporre
        int originalAmount = amount;              // copia: amount verrà modificata

        int quarters = amount / 25;               // monete da 25: 87 / 25 = 3
        amount = amount % 25;                     // resto: 87 % 25 = 12

        int dimes = amount / 10;                  // monete da 10: 12 / 10 = 1
        amount = amount % 10;                     // resto: 12 % 10 = 2

        int nickels = amount / 5;                 // monete da 5: 2 / 5 = 0
        int pennies = amount % 5;                 // le monete da 1: 2 % 5 = 2

        System.out.println(originalAmount + " cents in coins:");
        System.out.println("    quarters: " + quarters);
        System.out.println("    dimes: " + dimes);
        System.out.println("    nickels: " + nickels);
        System.out.println("    pennies: " + pennies);
    }
}
```

Seguiamo i calcoli per 87: dopo le monete da 25 (tre, che valgono 75) restano 12; di questi, una moneta da 10 ne copre 10 e ne restano 2; nessuna moneta da 5 sta in 2; restano 2 monete da 1. L'output è:

```text
87 cents in coins:
    quarters: 3
    dimes: 1
    nickels: 0
    pennies: 2
```

Un programma di questo tipo si collauda con importi che producono zero per ciascun taglio, e con i valori al confine dei tagli (per esempio 24, 25, 26, oppure 0, 1, 98, 99), perché è lì che gli errori logici emergono.

## 2.6 Le conversioni tra tipi

Poiché Java è fortemente tipizzato, non si può mettere un valore di un tipo in una variabile di un altro tipo senza riflettere. Esistono però dei casi in cui la conversione è sicura e il compilatore la fa da solo, e altri casi in cui la conversione può far perdere informazione e il compilatore chiede al programmatore di dichiararla esplicitamente.

### 2.6.1 La conversione implicita

Un valore può essere assegnato a una variabile di un tipo "più a destra" nella catena della sezione 2.5.1:

```text
byte -> short -> int -> long -> float -> double
```

Il valore viene convertito automaticamente. Per esempio, se `doubleVariable` è un `double`, l'assegnamento `doubleVariable = 7;` è lecito: l'intero 7 diventa il `double` `7.0`. Si può anche assegnare un `char` a una variabile `int`, che riceve il codice del carattere. È una conversione **verso un tipo più capace**, e in genere non perde nulla.

Il passaggio inverso, da un tipo "più a destra" a uno "più a sinistra" (per esempio da `double` a `int`), **non è permesso** senza un cast, perché si perderebbe la parte decimale. Il compilatore lo segnala con il messaggio `incompatible types: possible lossy conversion from double to int` ("conversione con perdita possibile").

> [!WARNING]
> **Attenzione — `byte b = 10;` compila anche se 10 è un `int`**
> Per i letterali interi c'è un'eccezione di comodo: un valore costante che sta nell'intervallo di `byte`, `short` o `char` si può assegnare a una variabile di quel tipo senza cast. `byte b = 10;` compila; `byte b = 200;` no, perché 200 non sta in un `byte`. Vale **solo per le costanti**: se il valore viene da un'espressione con variabili, la regola generale riprende il suo posto (vedi l'errore tipico "somma di `byte`" nel seguito).

### 2.6.2 La promozione nelle espressioni

Nelle espressioni aritmetiche Java converte gli operandi **prima** di eseguire l'operazione, per portarli a un tipo comune. La regola è quella che già conosciamo: se i tipi sono diversi, il tipo più "piccolo" viene promosso a quello più "grande" (sezione 2.5.1). Esiste una regola in più per i tipi piccoli: i valori di tipo `byte`, `short` e `char` vengono sempre promossi ad almeno `int` prima di un'operazione aritmetica. Da qui due conseguenze.

La prima riguarda `char`. Poiché un `char` diventa un `int` quando partecipa a un calcolo, `'a' + 1` non è un carattere ma l'intero 98, perché il codice di `'a'` è 97. Per riottenere un carattere servirà un cast (sezione 2.6.3). Gli operatori `++` e `--` e gli assegnamenti composti sono un caso a parte, perché riconvertono da soli nel tipo della variabile: dato `char c = 'a';`, l'istruzione `c++;` lascia in `c` il carattere `'b'`.

La seconda riguarda la somma di due `short` o `byte`: il risultato è un `int`, e per memorizzarlo in un `byte` serve un cast.

### 2.6.3 Il cast

Un **cast** (o *type cast*, conversione esplicita) converte un valore in un altro tipo anche contro la direzione "sicura". Si scrive il tipo desiderato tra parentesi tonde davanti al valore da convertire:

```text
(tipo) valore
```

Il cast si assume la responsabilità della conversione, quindi **può perdere informazione**: nel caso di un numero in virgola mobile convertito in intero la parte frazionaria viene **troncata**, non arrotondata. Il valore della variabile originale non cambia: il cast produce un nuovo valore temporaneo.

```java
public class Conversioni {
    public static void main(String[] args) {
        double doubleVariable = 7;                    // int -> double, implicito
        System.out.println(doubleVariable);

        double distance = 9.99;
        int points = (int) distance;                  // cast: la parte decimale è troncata
        System.out.println(points);
        System.out.println(distance);                 // la variabile originale non cambia
        System.out.println((int) -9.99);              // troncamento verso lo zero

        int a = 7, b = 2;
        System.out.println(a / b);                    // divisione tra int
        System.out.println((double) a / b);           // cast di a, poi divisione in virgola mobile
        System.out.println((double) (a / b));         // prima la divisione tra int, poi il cast

        char c = 'a';
        System.out.println(c + 1);                    // char promosso a int: 98
        System.out.println((char) (c + 1));           // cast di nuovo a char: 'b'
    }
}
```

Le prime righe mostrano la conversione implicita e il troncamento di `(int) 9.99`. Le tre righe sulla divisione sono quelle decisive. Nella prima, `a / b` è una divisione tra interi e dà `3`. Nella seconda il cast `(double)` si applica solo ad `a`, perché il cast ha precedenza più alta della divisione: l'espressione si legge `((double) a) / b`, quindi si divide un `double` per un `int` e si ottiene `3.5`. Nella terza le parentesi fanno sì che il cast riguardi il **risultato** della divisione, già troncato a `3`, e si ottiene `3.0`. L'output è:

```text
7.0
9
9.99
-9
3
3.5
3.0
98
b
```

> [!WARNING]
> **Attenzione — Un cast può perdere anche l'intervallo, non solo i decimali**
> Se il valore non sta nel tipo di arrivo, il cast produce un risultato che non ha senso. `(byte) 200` vale `-56`, perché il numero "si avvolge" come nell'overflow; `(int) 3e10` (30 miliardi in virgola mobile) vale `2147483647`, cioè `Integer.MAX_VALUE`. Un cast verso un tipo più piccolo si usa solo quando si è sicuri che il valore ci stia.

### 2.6.4 Da testo a numero

Un `String` come `"42"` contiene dei caratteri, non un numero, e **non si può convertire con un cast**: scrivere `(int) "42"` è un errore di compilazione (`incompatible types: String cannot be converted to int`). La conversione si fa con due metodi statici delle classi wrapper: `Integer.parseInt` per ottenere un `int` e `Double.parseDouble` per ottenere un `double`. È la situazione tipica quando i numeri arrivano dalla tastiera o da un file sotto forma di testo.

> [!NOTE]
> **Approfondimento esterno — `Integer.parseInt` e `Double.parseDouble`**
> ```text
> public static int parseInt(String s) throws NumberFormatException
> public static double parseDouble(String s) throws NumberFormatException
> ```
> Entrambi i metodi sono in `java.lang`. `parseInt` interpreta la stringa come intero in base dieci: le cifre possono essere precedute da un segno `-` o `+`. Lancia `NumberFormatException` se la stringa non contiene un intero valido, e anche se è `null` o vuota. `parseDouble` lancia `NumberFormatException` se la stringa non è un `double` valido e `NullPointerException` se è `null`. `NumberFormatException` estende `IllegalArgumentException`, che estende `RuntimeException`: è un'eccezione **non controllata**, e non va dichiarata con `throws` (le eccezioni sono nel [Capitolo 13](13-eccezioni.md)).
> *Fonte:* [Integer.parseInt(String) (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Integer.html#parseInt(java.lang.String))

```java
public class DaTestoANumero {
    public static void main(String[] args) {
        int n = Integer.parseInt("42");
        double d = Double.parseDouble("2.5");
        System.out.println(n + 1);       // ora è un int: si può fare aritmetica
        System.out.println(d * 2);

        try {
            Integer.parseInt("12a");     // contiene una lettera: non è un intero
        } catch (NumberFormatException e) {
            System.out.println("Non numerico: " + e.getMessage());
        }
    }
}
```

Dopo la conversione `n` e `d` si usano come numeri qualunque. Il blocco `try`/`catch` serve a mostrare che cosa succede con un testo non numerico (lo spiegheremo nel [Capitolo 13](13-eccezioni.md)): l'eccezione contiene nel messaggio il testo che ha causato il problema. L'output è:

```text
43
5.0
Non numerico: For input string: "12a"
```

Attenzione al testo che contiene spazi: `Integer.parseInt(" 12")` lancia lo stesso `NumberFormatException`, perché lo spazio non è una cifra. I metodi di pulizia del testo sono nel [Capitolo 3](03-stringhe-e-console.md).

## 2.7 Valori di verità e operatori logici

### 2.7.1 Il tipo `boolean`

Il tipo **`boolean`** ha due soli valori, `true` e `false`. Un'**espressione booleana** è un'espressione il cui valore è `true` o `false`, per esempio `time < limit` o `balance <= 0`. Si può assegnare un'espressione booleana a una variabile `boolean`:

```text
boolean isPositive = (number > 0);
```

e usare poi la variabile al posto dell'espressione, per esempio in un `if` ([Capitolo 4](04-strutture-di-controllo.md)). Le variabili booleane rendono il programma più leggibile se hanno un nome che si legge come una domanda: `isPositive` o `systemsAreOk`, non `numberSign` o `systemStatus`.

### 2.7.2 Operatori relazionali e di uguaglianza

I **confronti** producono un `boolean`. Gli operatori sono sei:

| Operatore | Significato | Esempio |
|---|---|---|
| `<` | minore | `time < limit` |
| `<=` | minore o uguale | `balance <= 0` |
| `>` | maggiore | `score > 90` |
| `>=` | maggiore o uguale | `score >= 60` |
| `==` | uguale | `a == 3` |
| `!=` | diverso | `number != 0` |

Il confronto di uguaglianza si scrive con **due** simboli uguali, `==`; l'`=` singolo è l'assegnamento. Confondere i due è un errore classico (vedi gli errori tipici).

Come abbiamo visto nella sezione 2.2.3, `==` va usato per gli interi e per i caratteri, non per i numeri in virgola mobile. E non è adatto nemmeno per confrontare due oggetti, come le stringhe: `s1 == s2` controlla soltanto se le due variabili si riferiscono *allo stesso oggetto in memoria*, non se contengono lo stesso testo. Per i testi si usa il metodo `equals` ([Capitolo 3](03-stringhe-e-console.md)).

### 2.7.3 Operatori logici e cortocircuito

Più condizioni si combinano con i tre **operatori logici**:

| Operatore | Nome | Risultato |
|---|---|---|
| `&&` | *and* (e) | `true` solo se **entrambi** gli operandi sono `true` |
| `\|\|` | *or* (o) | `true` se **almeno uno** degli operandi è `true` |
| `!` | *not* (non) | inverte: `!true` è `false` |

Un esempio: `(score > 0) && (score <= 100)` è vero solo se il punteggio sta tra 1 e 100. Il connettivo `||` è l'*or* **inclusivo**: è vero anche quando sono veri entrambi gli operandi. L'*or* esclusivo (vero se è vero uno solo dei due) si ottiene combinando gli altri: `(a || b) && !(a && b)`.

Un trabocchetto di scrittura: la condizione matematica `0 < score <= 100` **non è ammessa** in Java. Va spezzata in due confronti uniti da `&&`: `(0 < score) && (score <= 100)`.

Gli operatori `&&` e `||` valutano gli operandi da sinistra a destra e si fermano appena il valore dell'intera espressione è determinato: è la **valutazione in cortocircuito** (*short-circuit evaluation*, o *lazy evaluation*, "pigra").

- in `A && B`, se `A` è `false` l'espressione è già `false`, e `B` **non viene valutata**;
- in `A || B`, se `A` è `true` l'espressione è già `true`, e `B` non viene valutata.

Il cortocircuito non è soltanto una questione di efficienza: spesso è **essenziale**. Nell'espressione `(number != 0) && (sum / number > 5)` la seconda parte dà un errore a runtime (divisione per zero) quando `number` è zero, ma grazie al cortocircuito non viene mai valutata in quel caso.

Esistono anche gli operatori `&` e `|`, che calcolano lo stesso risultato di `&&` e `||` ma valutano **sempre entrambi** gli operandi. Sostituendoli, si ottiene la *valutazione completa*.

```java
public class Condizioni {
    public static void main(String[] args) {
        int score = 75;
        boolean inRange = (score > 0) && (score <= 100);
        boolean isExtreme = score < 10 || score > 90;
        System.out.println(inRange);
        System.out.println(!isExtreme);

        int number = 0;
        int sum = 12;
        if ((number != 0) && (sum / number > 5)) {    // il cortocircuito evita la divisione per zero
            System.out.println("Quoziente grande");
        } else {
            System.out.println("Nessuna divisione eseguita");
        }

        int k = 0;
        boolean corto = (k > 0) && (++k > 0);         // ++k non viene eseguito
        System.out.println(corto + " " + k);
        boolean completo = (k > 0) & (++k > 0);       // & valuta entrambi: ++k viene eseguito
        System.out.println(completo + " " + k);
    }
}
```

Le prime due righe dell'output sono valori di verità; la terza è il ramo `else` perché `number != 0` è falso e il cortocircuito salta la divisione; le ultime due mostrano la differenza con `&`: con `&&` il contatore `k` resta a 0, con `&` diventa 1. L'output è:

```text
true
true
Nessuna divisione eseguita
false 0
false 1
```

### 2.7.4 La precedenza degli operatori

Riunendo le regole dei paragrafi precedenti, ecco l'ordine di valutazione degli operatori incontrati in questo capitolo, **dal più forte al più debole**. Gli operatori di una stessa riga hanno la stessa precedenza.

| Livello | Operatori | Associatività |
|---|---|---|
| 1 | `x++`, `x--` (postfissi) | da sinistra |
| 2 | `++x`, `--x`, `+x`, `-x`, `!`, cast `(tipo)` | da destra |
| 3 | `*`, `/`, `%` | da sinistra |
| 4 | `+`, `-` | da sinistra |
| 5 | `<`, `<=`, `>`, `>=` | da sinistra |
| 6 | `==`, `!=` | da sinistra |
| 7 | `&`, poi `\|` | da sinistra |
| 8 | `&&` | da sinistra |
| 9 | `\|\|` | da sinistra |
| 10 | `? :` | da destra |
| 11 | `=`, `+=`, `-=`, `*=`, `/=`, `%=` | da destra |

L'*or* esclusivo `^` e gli altri operatori sui bit non sono trattati in questi appunti e non compaiono in tabella.

Per leggere un'espressione lunga si applicano le regole passo per passo, mettendo mentalmente le parentesi. Per esempio:

```java
public class Precedenze {
    public static void main(String[] args) {
        int score = 5;
        int min = 40;
        // score < min/2 - 10 || score > 90   si legge, con tutte le parentesi:
        // ((score < ((min / 2) - 10)) || (score > 90))
        boolean senzaParentesi = score < min / 2 - 10 || score > 90;
        boolean conParentesi = ((score < ((min / 2) - 10)) || (score > 90));
        System.out.println(senzaParentesi);
        System.out.println(conParentesi);
    }
}
```

La divisione `min / 2` vale 20; sottraendo 10 si ottiene 10; poi il confronto `5 < 10` è vero, e l'`||` finale è vero senza guardare il secondo operando. Le due scritture sono equivalenti. L'output è:

```text
true
true
```

### 2.7.5 L'operatore condizionale

L'**operatore condizionale** (o operatore *ternario*, perché ha tre operandi) sceglie fra due valori in base a una condizione:

```text
condizione ? valore_se_vera : valore_se_falsa
```

Scrive in una riga ciò che altrimenti richiederebbe un `if`/`else` ([Capitolo 4](04-strutture-di-controllo.md)). Il caso tipico è assegnare il maggiore di due numeri:

```text
max = (n1 > n2) ? n1 : n2;
```

che equivale a `if (n1 > n2) max = n1; else max = n2;`. Si usa spesso anche dentro `println` per scegliere un testo.

```java
public class Condizionale {
    public static void main(String[] args) {
        int n1 = 17;
        int n2 = 42;
        int max = (n1 > n2) ? n1 : n2;              // il maggiore dei due
        System.out.println("Maggiore: " + max);

        int hours = 1;
        System.out.println("You worked " + hours + ((hours > 1) ? " hours" : " hour"));
    }
}
```

Il primo `println` stampa il maggiore; il secondo sceglie fra singolare e plurale in base al valore di `hours`. Si noti che i due punti separano le due alternative, come in `? :`. L'output è:

```text
Maggiore: 42
You worked 1 hour
```

## 2.8 Un metodo statico con tipi misti

Riuniamo quanto visto in un esercizio nella forma in cui si presenta all'esame: una classe con un metodo statico che riceve dei numeri e restituisce un risultato. Supponiamo che la traccia chieda: "Definire la classe `Sconto` con un metodo statico `percentuale` che riceve il prezzo originale e il prezzo scontato, entrambi interi (in euro), e restituisce di quanti punti percentuali è sceso il prezzo, come numero con la virgola".

La traccia non dà la firma, ma la fissa quasi del tutto: `static` perché va invocato senza creare un oggetto, due parametri `int`, valore restituito `double`. La logica è `(prezzoOriginale - prezzoScontato) / prezzoOriginale * 100`. Se però si scrive l'espressione così com'è con due `int`, la divisione è tra interi e il risultato è `0` per qualsiasi sconto inferiore al 100%. Servono un operando in virgola mobile prima della divisione.

```java
public class ProvaSconto {
    public static void main(String[] args) {
        System.out.println(Sconto.percentuale(80, 60));
        System.out.println(Sconto.percentuale(50, 50));
        System.out.println(Sconto.percentuale(30, 45));
    }
}

class Sconto {
    static double percentuale(int prezzoOriginale, int prezzoScontato) {
        // 100.0 è un double: da qui in poi il calcolo avviene in virgola mobile
        return (prezzoOriginale - prezzoScontato) * 100.0 / prezzoOriginale;
    }
}
```

Moltiplicare per `100.0` (un `double`) *prima* di dividere porta tutta l'espressione in virgola mobile, perché `(prezzoOriginale - prezzoScontato) * 100.0` è già un `double` e la divisione successiva è tra un `double` e un `int`. Con `80` e `60` si ottiene `20 * 100.0 / 80`, cioè `25.0`. L'ultima chiamata mostra un valore negativo: il prezzo "scontato" è più alto dell'originale, quindi il risultato è `-50.0`. L'output è:

```text
25.0
0.0
-50.0
```

## Come esce all'esame

**Appello dell'8 settembre 2026 (EXAM4) — Esercizio 3, logica di base.** La traccia chiedeva una classe `Convertitore` con il metodo `converti`, "invocabile senza creare un oggetto", che riceve una distanza in chilometri (intero) e restituisce l'equivalente in metri (intero). L'output atteso mostrava `converti(1) -> 1000`, `converti(0) -> 0`, `converti(7) -> 7000` e `converti(-3) -> -3000`. Servono di questo capitolo: il tipo `int` per parametro e valore restituito (sezione 2.2.1) e l'operatore `*` con un letterale `int` (sezione 2.5), che si comporta correttamente anche con zero e con numeri negativi. Vincoli letterali: il nome della classe e del metodo, i tipi `int`, il metodo statico.

**EXAM2 — Esercizio 1, logica di base.** Stessa sostanza: il metodo `public static int converti(int km)`, che converte chilometri in metri. Vincolo letterale: la firma, da copiare esattamente.

In esercizi di questo genere la logica è una moltiplicazione e non servono né cast né divisioni, ma il punteggio dipende dalla fedeltà alla traccia: tipi, nome e firma vanno rispettati alla lettera. Una variante con la conversione inversa (da metri a chilometri) richiederebbe invece di pensare alla divisione tra interi delle sezioni 2.5.2 e 2.6.3.

## Errori tipici

> [!CAUTION]
> **Errore tipico — Una divisione tra interi che doveva dare un decimale**
> ```java
> int a = 3, b = 4;
> double media = (a + b) / 2;   // ERRORE LOGICO: media vale 3.0, non 3.5
> ```
> Il programma compila e non dà alcun messaggio, ma `(a + b) / 2` è una divisione tra due `int`, quindi la parte frazionaria viene troncata *prima* dell'assegnamento a `double`. Forma corretta: rendere in virgola mobile uno degli operandi prima della divisione, `(a + b) / 2.0`, oppure `(double) (a + b) / 2`.

> [!CAUTION]
> **Errore tipico — Un cast nel posto sbagliato**
> ```java
> int a = 7, b = 2;
> double r = (double) (a / b);   // ERRORE LOGICO: r vale 3.0
> ```
> Le parentesi fanno sì che il cast si applichi al risultato della divisione, quando questa è già stata troncata a `3`. Forma corretta: `(double) a / b`, dove il cast riguarda soltanto `a` e dà `3.5`.

> [!CAUTION]
> **Errore tipico — Assegnare un valore con la virgola a un `int`**
> ```java
> int n = 3.5;      // ERRORE: da double a int senza cast
> float f = 3.14;   // ERRORE: 3.14 è un double, non un float
> ```
> Il compilatore risponde `incompatible types: possible lossy conversion from double to int` (e `... from double to float`). Forme corrette: `int n = (int) 3.5;` se si vuole davvero troncare, oppure `double n = 3.5;`; e `float f = 3.14f;` con la `f` finale.

> [!CAUTION]
> **Errore tipico — Un letterale intero troppo grande**
> ```java
> long grande = 3000000000;   // ERRORE: il letterale è un int e non ci sta
> ```
> Un numero senza `L` è un `int`: il compilatore risponde `integer number too large` anche se la variabile di destinazione è un `long`. Forma corretta: `long grande = 3000000000L;`.

> [!CAUTION]
> **Errore tipico — Usare una variabile prima di assegnarle un valore**
> ```java
> int totale;
> System.out.println(totale);   // ERRORE: totale non è stata inizializzata
> ```
> Il compilatore risponde `variable totale might not have been initialized`. Forma corretta: assegnare il valore alla dichiarazione, `int totale = 0;`.

> [!CAUTION]
> **Errore tipico — Modificare una costante**
> ```java
> final double PI = 3.14159;
> PI = 3.14;   // ERRORE: PI è final
> ```
> Il compilatore risponde `cannot assign a value to final variable PI`. Una costante riceve il suo valore una volta sola, nella dichiarazione.

> [!CAUTION]
> **Errore tipico — `=` al posto di `==`**
> ```java
> int x = 5;
> if (x = 3) { }   // ERRORE: assegnamento al posto di confronto
> ```
> Il compilatore risponde `incompatible types: int cannot be converted to boolean`: `x = 3` è un assegnamento, il cui valore è un `int`, ma la condizione di un `if` deve essere un `boolean`. Forma corretta: `if (x == 3)`.

> [!CAUTION]
> **Errore tipico — Una catena di confronti alla maniera della matematica**
> ```java
> int score = 50;
> boolean ok = 0 < score <= 100;   // ERRORE: non si possono concatenare i confronti
> ```
> Prima si valuta `0 < score`, che è un `boolean`, e poi il `boolean` viene confrontato con `100`: il compilatore risponde `bad operand types for binary operator '<='`. Forma corretta: `boolean ok = (0 < score) && (score <= 100);`.

> [!CAUTION]
> **Errore tipico — Confrontare due `double` con `==`**
> ```java
> double somma = 0.1 + 0.2;
> if (somma == 0.3) { System.out.println("uguali"); }   // non stampa mai
> ```
> `0.1 + 0.2` vale `0.30000000000000004` e il confronto è falso, senza alcun errore. Forma corretta: confrontare con una tolleranza, `Math.abs(somma - 0.3) < 1e-9`.

> [!CAUTION]
> **Errore tipico — La somma di due `byte` o `short` non sta in un `byte` o `short`**
> ```java
> byte a = 10, b = 20;
> byte c = a + b;   // ERRORE: a + b è un int
> ```
> Prima di sommare, `a` e `b` vengono promossi a `int` e il risultato è un `int`: il compilatore risponde `incompatible types: possible lossy conversion from int to byte`. Forma corretta: `int c = a + b;` oppure `byte c = (byte) (a + b);`.

> [!CAUTION]
> **Errore tipico — Convertire un testo in numero con un cast**
> ```java
> String s = "42";
> int n = (int) s;   // ERRORE: String non si converte con un cast
> ```
> Il compilatore risponde `incompatible types: String cannot be converted to int`. Forma corretta: `int n = Integer.parseInt(s);` (e `Double.parseDouble` per un `double`).

> [!CAUTION]
> **Errore tipico — Dichiarare due volte la stessa variabile**
> ```java
> int x = 1;
> int x = 2;   // ERRORE: x esiste già
> ```
> Il compilatore risponde `variable x is already defined in method main(String[])`. La seconda volta si assegna, senza ripetere il tipo: `x = 2;`.

> [!CAUTION]
> **Errore tipico — `i = i++`**
> ```java
> int i = 5;
> i = i++;   // ERRORE LOGICO: i resta 5
> ```
> L'espressione `i++` vale il valore *vecchio* di `i` (5) e incrementa `i` a 6; subito dopo l'assegnamento riscrive in `i` il valore dell'espressione, cioè 5. Il risultato è che `i` resta 5. Forma corretta: `i++;` da solo.

> [!CAUTION]
> **Errore tipico — Mescolare caratteri e numeri nella stampa**
> ```java
> char c = 'a';
> System.out.println(c + 1);   // stampa 98, non b
> ```
> Poiché `c` viene promosso a `int`, la somma è un `int` e `println` stampa il numero 98. Forma corretta, se si vuole il carattere successivo: `System.out.println((char) (c + 1));`, che stampa `b`.

## Riassunto

Una variabile è un nome dato a una posizione di memoria che contiene un valore di un tipo ben preciso; si dichiara indicando il tipo e il nome, e conviene inizializzarla subito. Java ha otto tipi primitivi, quattro interi (`byte`, `short`, `int`, `long`), due in virgola mobile (`float`, `double`), `char` e `boolean`; i più usati sono `int` e `double`. Un valore primitivo si memorizza direttamente nella variabile, mentre una variabile di tipo riferimento contiene l'indirizzo di un oggetto. Gli interi sono esatti nel loro intervallo ma vanno in overflow senza avvisi, e i numeri in virgola mobile sono solo approssimati. Le costanti con nome (`public static final`) danno un significato ai valori fissi e li rendono modificabili in un solo punto. Gli operatori aritmetici danno un risultato il cui tipo dipende da quello degli operandi: la divisione tra interi tronca, e per ottenere un risultato decimale almeno un operando deve essere in virgola mobile prima della divisione. Le conversioni verso un tipo più capace sono automatiche, le altre richiedono un cast, che tronca e può perdere informazione; un testo si converte in numero con `Integer.parseInt` o `Double.parseDouble`. I confronti e gli operatori logici producono un `boolean`; `&&` e `||` si fermano appena il risultato è noto.

**Concetti chiave**

- **Variabile**: nome di una posizione di memoria con un tipo; si dichiara prima di usarla, e una variabile locale va inizializzata prima del primo uso.
- **Identificatori e convenzioni**: lettere, cifre, `_` e `$`, mai una cifra all'inizio; maiuscole e minuscole distinte; classi con l'iniziale maiuscola, variabili e metodi con la minuscola, costanti tutte maiuscole.
- **Tipi primitivi**: `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`; i loro limiti sono le costanti `MIN_VALUE` e `MAX_VALUE` delle classi wrapper.
- **Letterali**: `int` senza punto, `long` con `L`, `double` con il punto, `float` con `f`, `char` con apici singoli, `String` con virgolette doppie.
- **Approssimazione dei numeri in virgola mobile**: `0.1 + 0.2` non è `0.3`; non si confrontano con `==`, ma con una tolleranza.
- **Tipo primitivo e tipo riferimento**: la variabile primitiva contiene il valore; quella di tipo riferimento contiene l'indirizzo di un oggetto.
- **Assegnamento**: prima si valuta l'espressione a destra, poi si scrive il risultato nella variabile a sinistra.
- **Costante con nome**: `final` impedisce la modifica; `public static final` per le costanti di classe.
- **Divisione intera e resto**: tra due interi `/` tronca verso zero e `%` dà il resto, con il segno del dividendo.
- **Divisione per zero e overflow**: tra interi la divisione per zero lancia `ArithmeticException`; in virgola mobile dà `Infinity` o `NaN`; l'overflow tra interi non segnala nulla.
- **Precedenza**: unari, poi `* / %`, poi `+ -`, poi confronti, poi `&&`, poi `||`, poi `? :`, poi l'assegnamento; nel dubbio, parentesi.
- **Assegnamenti composti, `++` e `--`**: abbreviano `x = x op y` e `x = x ± 1`; nella forma prefissa si usa il valore nuovo, nella postfissa quello vecchio.
- **Conversione implicita e promozione**: da `byte` verso `double` automatica; `byte`, `short` e `char` diventano `int` nelle espressioni.
- **Cast**: `(tipo) valore`, tronca e può perdere informazione; ha precedenza più alta degli operatori binari.
- **`parseInt` e `parseDouble`**: convertono un testo in numero; lanciano `NumberFormatException` (non controllata) se il testo non è valido.
- **Operatori relazionali e logici**: producono `boolean`; `&&` e `||` valutano in cortocircuito, `&` e `|` valutano sempre entrambi i lati.
- **Operatore condizionale**: `condizione ? a : b`, una riga al posto di un `if`/`else`.

**API essenziali**

| Classe | Membro | Dichiarazione | Eccezioni |
|---|---|---|---|
| `java.lang.Integer` | `MIN_VALUE`, `MAX_VALUE` | `public static final int` | — |
| `java.lang.Long` | `MIN_VALUE`, `MAX_VALUE` | `public static final long` | — |
| `java.lang.Double` | `MAX_VALUE`, `MIN_VALUE` | `public static final double` | — |
| `java.lang.Integer` | `parseInt` | `public static int parseInt(String s) throws NumberFormatException` | `NumberFormatException` (non controllata) |
| `java.lang.Double` | `parseDouble` | `public static double parseDouble(String s) throws NumberFormatException` | `NumberFormatException`, `NullPointerException` (non controllate) |
| `java.lang.Math` | `abs` | `public static int abs(int a)` (esistono gli overload per `long`, `float`, `double`) | — |
