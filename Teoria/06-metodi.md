---
materia: Programmazione a Oggetti
capitolo: 6
titolo: Metodi
livello_syllabus: 1-2
stato: completo
slide: ["Savitch cap. 5 slide 1-23", "Savitch cap. 7 slide 1-38", "Savitch cap. 9 slide 12-30", "Lect2 (Methods, Static Class Members)"]
appelli: [EXAM2, EXAM4]
fonti_esterne: 4
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 6 — Metodi

## Di cosa parla questo capitolo

Fin qui abbiamo scritto programmi che stanno quasi tutti dentro il `main`: una lunga sequenza di istruzioni, dall'inizio alla fine. Funziona finché il programma è piccolo. Appena il lavoro cresce, nascono due problemi. Il primo è che lo stesso calcolo serve in più punti, e ricopiarlo ogni volta moltiplica gli errori. Il secondo è che il `main` diventa un muro di righe in cui non si capisce più quale parte faccia cosa. La soluzione è dare un **nome** a un pezzo di lavoro e poterlo richiamare quando serve: è il **metodo**.

Il capitolo parte da ciò che abbiamo già visto di sfuggita. Il `public static void main(String[] args)` del [Capitolo 1 — Java e la JVM](01-java-e-la-jvm.md) è un metodo; le conversioni e il cast del [Capitolo 2 — Tipi primitivi, variabili e operatori](02-tipi-variabili-operatori.md) decidono che cosa succede quando un argomento ha un tipo diverso da quello del parametro; il `grade` del [Capitolo 4 — Strutture di controllo](04-strutture-di-controllo.md) e i metodi che ricevono e restituiscono array del [Capitolo 5 — Array e matrici](05-array-e-matrici.md) erano già metodi. Qui li mettiamo in ordine.

Alla fine del capitolo saprai definire e chiamare metodi con e senza valore di ritorno, spiegare che cosa significa **passaggio per valore** e perché un metodo non può scambiare due `int` del chiamante, distinguere un metodo `static` da uno d'istanza, usare la classe `Math` e le **classi wrapper** (`Integer`, `Double`, `Character`…), scrivere metodi in **overloading** e capire come il compilatore sceglie quello giusto, scomporre un problema in metodi collaudabili uno alla volta, e scrivere metodi **ricorsivi**: ricerca binaria e ordinamento per fusione compresi.

> [!IMPORTANT]
> **Metodi e prove scritte**
> Il metodo statico "dentro una classe" è la forma più frequente dell'esercizio da 5 punti: la traccia dà il nome della classe e la firma (oppure la descrive a parole) e chiede di scrivere il corpo. È un esercizio breve ma esigente, perché il punteggio dipende dall'**aderenza letterale**: nome della classe, nome del metodo, tipi del parametro e del valore restituito, presenza di `static`. Le sezioni 6.1 e 6.4 e gli scheletri in fondo servono a questo. Vedi la sezione "Come esce all'esame".

## 6.1 Il metodo come unità di lavoro

### 6.1.1 Il problema: lo stesso lavoro in più punti

Supponiamo di dover convertire tre distanze da chilometri a metri e stampare i risultati. Senza metodi il programma ripete la stessa moltiplicazione tre volte:

```java
public class SenzaMetodi {
    public static void main(String[] args) {
        int km1 = 2;
        int km2 = 7;
        int km3 = 15;
        System.out.println(km1 + " km = " + km1 * 1000 + " m");
        System.out.println(km2 + " km = " + km2 * 1000 + " m");
        System.out.println(km3 + " km = " + km3 * 1000 + " m");
    }
}
```

```text
2 km = 2000 m
7 km = 7000 m
15 km = 15000 m
```

Il programma è corretto, ma se domani la regola cambiasse (per esempio dovendo arrotondare), bisognerebbe correggere tre righe, e basterebbe dimenticarne una per avere risultati incoerenti. Un metodo risolve il problema: la regola si scrive **una volta sola**, con un nome, e il resto del programma si limita a chiamarla.

> [!NOTE]
> **Definizione — Metodo**
> Un **metodo** (*method*) è un blocco di istruzioni con un nome, che esegue un compito preciso e può ricevere dei dati in ingresso (i **parametri**) e restituire un risultato. Si **definisce** una sola volta e si **chiama** (o *invoca*, *invocare*, *call*, *invoke*) quante volte serve.

> [!TIP]
> **Intuizione — La ricetta**
> Un metodo è una ricetta scritta su una scheda. La scheda ha un titolo (il nome), una lista di ingredienti (i parametri) e dei passaggi (il corpo); alla fine produce un piatto (il valore restituito). Chi cucina non riscrive la ricetta a ogni portata: la prende dalla scheda e la segue. L'analogia ha un limite: una scheda di cucina non dice che cosa fare se gli ingredienti sono sbagliati, mentre in Java il compilatore verifica che gli argomenti passati abbiano il numero e il tipo giusti.

### 6.1.2 Definire un metodo

Ecco il metodo che risolve il problema precedente, dentro una classe:

```java
public class Distanze {
    // Definizione del metodo
    public static int inMetri(int km) {
        return km * 1000;
    }

    public static void main(String[] args) {
        int km1 = 2;
        int km2 = 7;
        int km3 = 15;
        System.out.println(km1 + " km = " + inMetri(km1) + " m");   // chiamata
        System.out.println(km2 + " km = " + inMetri(km2) + " m");
        System.out.println(km3 + " km = " + inMetri(km3) + " m");
    }
}
```

```text
2 km = 2000 m
7 km = 7000 m
15 km = 15000 m
```

Leggiamo la **definizione** parola per parola. La prima riga, che si chiama **intestazione** (*heading*) o **firma** nel senso comune del termine (più avanti, nella sezione 6.7, vedremo che per il compilatore la firma è una cosa un po' più stretta), è fatta così:

```text
public static int inMetri(int km)
```

| Parte | Nell'esempio | Significato |
|---|---|---|
| modificatore di accesso | `public` | chi può chiamare il metodo (approfondito nel [Capitolo 7 — Classi e oggetti](07-classi-e-oggetti.md)) |
| modificatore `static` | `static` | il metodo appartiene alla classe e si chiama senza creare un oggetto (sezione 6.4) |
| tipo di ritorno | `int` | il tipo del valore che il metodo restituisce; `void` se non ne restituisce nessuno |
| nome | `inMetri` | l'identificatore con cui si chiama il metodo; per convenzione inizia con la minuscola, e ogni parola successiva con la maiuscola |
| parametri | `(int km)` | l'elenco, tra parentesi tonde, dei dati in ingresso: ciascuno ha un tipo e un nome. L'elenco può essere vuoto: `()` |

Dopo l'intestazione viene il **corpo** (*body*), tra graffe. Il metodo `inMetri` ha un'unica istruzione, `return km * 1000;`, che calcola un valore e lo consegna a chi ha chiamato il metodo.

La sintassi generale è:

```text
modificatori tipo_di_ritorno nome(tipo1 parametro1, tipo2 parametro2, ...) {
    corpo
}
```

Un metodo si scrive sempre **dentro una classe**, mai fuori (sezione 1.10 del Capitolo 1). Ogni parametro porta il proprio tipo anche quando due parametri hanno lo stesso tipo: `int a, b` non è valido, si scrive `int a, int b`.

### 6.1.3 Chiamare un metodo

Per **chiamare** un metodo si scrive il suo nome seguito dalle parentesi tonde con gli **argomenti**, cioè i valori effettivi da dare ai parametri. Dove si scrive la chiamata dipende dal tipo di ritorno.

I metodi con un valore di ritorno si chiamano **dentro un'espressione**, in qualsiasi punto in cui sarebbe lecito scrivere un valore di quel tipo:

```java
int m = inMetri(5);                       // assegnato a una variabile
System.out.println(inMetri(5) + 1);       // usato in un'espressione
if (inMetri(km) > 10000) { ... }          // usato in una condizione
```

I metodi `void` (sezione 6.1.5) non producono un valore, quindi non si possono usare in un'espressione. Si chiamano con una **istruzione a sé**, terminata da punto e virgola:

```java
stampaSaluto("Anna");                      // istruzione: esegue l'azione
```

Il `main` è anch'esso un metodo `void`: viene chiamato dalla JVM, non dal programma (sezione 1.5.2).

### 6.1.4 L'istruzione `return`

L'istruzione `return` fa due cose insieme: **termina** subito l'esecuzione del metodo e **consegna** al chiamante il valore dell'espressione che la segue. Il tipo dell'espressione deve essere compatibile con il tipo di ritorno dichiarato.

Un metodo può avere più `return`, uno per ogni percorso possibile, ma ogni percorso deve concludersi con un `return`: il compilatore controlla che nessuna strada arrivi in fondo al metodo senza aver restituito qualcosa. Questa regola è lo scoglio più frequente nei metodi con un `if`:

```java
public class Segno {
    public static int segno(int n) {
        if (n > 0) {
            return 1;
        } else if (n < 0) {
            return -1;
        } else {
            return 0;                      // ogni ramo termina con un return
        }
    }

    public static void main(String[] args) {
        System.out.println(segno(25));
        System.out.println(segno(-3));
        System.out.println(segno(0));
    }
}
```

```text
1
-1
0
```

Se si togliesse l'`else` finale e il `return 0;`, il metodo non compilerebbe: il compilatore non sa dimostrare che `n > 0` e `n < 0` coprono tutti i casi, e segnala `missing return statement` (vedi gli errori tipici). Un'istruzione scritta **dopo** un `return` non verrebbe mai eseguita, e anche questo il compilatore lo rifiuta (`unreachable statement`).

In un metodo `void` si può scrivere `return;` senza valore per uscire in anticipo; non è obbligatorio, perché alla chiusura del corpo il metodo termina da solo.

```java
public class Uscita {
    public static void stampaRadice(double x) {
        if (x < 0) {
            System.out.println("Radice non definita");
            return;                        // esce dal metodo: le righe sotto non vengono eseguite
        }
        System.out.println("Radice = " + Math.sqrt(x));
    }

    public static void main(String[] args) {
        stampaRadice(16);
        stampaRadice(-4);
    }
}
```

```text
Radice = 4.0
Radice non definita
```

### 6.1.5 Metodi `void` ed effetti collaterali

Ci sono due tipi di metodi. Quelli che **restituiscono un valore** (tipo di ritorno diverso da `void`), come `inMetri`, servono per calcolare qualcosa. Quelli **`void`** non restituiscono nulla e servono per **fare** qualcosa: stampare, modificare lo stato di un oggetto, chiamare altri metodi. Tutto ciò che un metodo fa oltre a restituire un valore si chiama **effetto collaterale** (*side effect*): stampare a video, leggere da tastiera, cambiare il valore di un campo di un oggetto o di un elemento di un array.

```java
public class Saluto {
    public static void stampaSaluto(String nome) {       // void: non restituisce nulla
        System.out.println("Ciao, " + nome + "!");        // effetto collaterale: stampa
    }

    public static void main(String[] args) {
        stampaSaluto("Anna");
        stampaSaluto("Luca");
    }
}
```

```text
Ciao, Anna!
Ciao, Luca!
```

Una buona regola di progetto è che **ogni metodo svolga un solo compito, ben definito**. Un metodo che calcola un numero e anche lo stampa è meno riutilizzabile di due metodi distinti, uno che calcola e uno che stampa: il primo si può usare in una somma, in una condizione, in un test, il secondo no.

> [!WARNING]
> **Attenzione — Stampare non è restituire**
> `System.out.println(x)` mostra un valore sullo schermo ma non lo consegna al chiamante. Un metodo dichiarato `int` deve **restituire** il risultato con `return`; se si limita a stamparlo, non compila (manca il `return`) oppure, se il tipo è `void`, il chiamante non può usare il valore. Quando la traccia chiede che il metodo "restituisca" un valore, serve `return`; quando chiede che lo "stampi", serve `System.out.println` e di norma il tipo è `void`.

## 6.2 Variabili locali e blocchi

### 6.2.1 Variabili locali

Le variabili dichiarate **dentro** un metodo, parametri compresi, si chiamano **variabili locali** (*local variables*). Esistono solo durante l'esecuzione del metodo e sono visibili solo al suo interno. Anche tutte le variabili dichiarate nel `main` sono locali al `main`.

Ne segue una conseguenza importante: due metodi diversi possono usare lo stesso nome di variabile senza che le due variabili abbiano niente in comune.

```java
public class Locali {
    public static int raddoppia(int valore) {
        int risultato = valore * 2;          // risultato di raddoppia
        return risultato;
    }

    public static int triplica(int valore) {
        int risultato = valore * 3;          // un'altra variabile, anche se si chiama allo stesso modo
        return risultato;
    }

    public static void main(String[] args) {
        int risultato = 10;                  // una terza variabile, locale al main
        System.out.println(raddoppia(4));
        System.out.println(triplica(4));
        System.out.println(risultato);       // ancora 10: gli altri metodi non l'hanno toccata
    }
}
```

```text
8
12
10
```

Ci sono tre variabili `risultato`, una per metodo, e ciascuna è invisibile agli altri due. Dal punto di vista del programmatore è una vera comodità: chi scrive un metodo non deve preoccuparsi dei nomi usati altrove.

Una variabile locale **non ha un valore iniziale** (a differenza dei campi, vedi il Capitolo 2): va inizializzata prima dell'uso, altrimenti il compilatore segnala `variable ... might not have been initialized`.

### 6.2.2 Blocchi e ambito

Un **blocco** (*block*) è un gruppo di istruzioni racchiuso tra graffe, come il corpo di un `if`, di un `for` o di un metodo. Una variabile dichiarata dentro un blocco è visibile dal punto della dichiarazione **fino alla graffa che chiude il blocco** (lo abbiamo visto nella sezione 4.1.3). Una variabile dichiarata fuori dal blocco, prima di esso, è visibile sia fuori sia dentro.

L'intervallo del programma in cui un nome è visibile si chiama **ambito** (*scope*).

```java
public class Ambito {
    public static void main(String[] args) {
        int totale = 0;                       // ambito: da qui alla fine del main
        for (int i = 1; i <= 3; i++) {        // i: ambito solo nel for
            int quadrato = i * i;             // quadrato: ambito solo nel corpo del for
            totale = totale + quadrato;
        }
        System.out.println(totale);
        // System.out.println(i);             // ERRORE: i non esiste più qui
        // System.out.println(quadrato);      // ERRORE: nemmeno quadrato
    }
}
```

```text
14
```

`totale` è dichiarato prima del ciclo, quindi si può usare dentro e fuori. `i` e `quadrato` nascono dentro il `for` e muoiono con esso: chi vuole usarli dopo il ciclo li deve dichiarare prima. In un blocco annidato non si può ridichiarare una variabile con il **nome di una già visibile**: `int totale = 5;` dentro il `for` sarebbe un errore (`variable totale is already defined`).

## 6.3 Parametri e passaggio degli argomenti

### 6.3.1 Parametri formali e argomenti

I nomi scritti nell'intestazione si chiamano **parametri formali** (*formal parameters*): segnaposto che il metodo usa nel corpo. I valori scritti nella chiamata si chiamano **argomenti** o **parametri effettivi** (*actual parameters*, *arguments*): i valori concreti per questa chiamata. Quando il metodo viene chiamato, ogni parametro formale è inizializzato con il valore dell'argomento corrispondente, **nell'ordine** in cui sono scritti.

```java
public class Parametri {
    public static double area(double base, double altezza) {      // parametri formali: base, altezza
        return base * altezza / 2;
    }

    public static void main(String[] args) {
        double b = 6;
        System.out.println(area(b, 4));       // argomenti: b e 4 (nell'ordine)
        System.out.println(area(4, b));       // stesso risultato, ma l'ordine conta in generale
    }
}
```

```text
12.0
12.0
```

Gli argomenti devono corrispondere ai parametri per **numero**, **ordine** e **tipo** (o un tipo convertibile in quello del parametro, sezione 6.3.3). Una chiamata con un numero diverso di argomenti non compila: `method area in class Parametri cannot be applied to given types;`.

Un parametro formale si comporta come una **variabile locale** del metodo, già inizializzata con il valore dell'argomento. Si può modificarlo nel corpo, ma, come vedremo subito, la modifica non esce dal metodo.

### 6.3.2 Il passaggio per valore

Cosa accade esattamente alla chiamata? Java usa un unico meccanismo, il **passaggio per valore** (*call by value*): il parametro formale riceve una **copia** del valore dell'argomento. Per un tipo primitivo, la copia è il numero stesso. Ne segue che il metodo non può alterare la variabile del chiamante, per quanto cambi il proprio parametro.

> [!NOTE]
> **Definizione — Passaggio per valore**
> Nella chiamata di un metodo il valore di ogni argomento viene **copiato** nel parametro formale corrispondente. Il parametro è una variabile locale indipendente: assegnarle un nuovo valore non cambia la variabile usata come argomento.

```java
public class PerValore {
    public static void incrementa(int x) {
        x = x + 1;                           // cambia la copia locale
        System.out.println("dentro: x = " + x);
    }

    public static void main(String[] args) {
        int n = 5;
        incrementa(n);
        System.out.println("fuori: n = " + n);
    }
}
```

```text
dentro: x = 6
fuori: n = 5
```

Seguiamo l'esecuzione. Nel `main` la variabile `n` vale 5. Alla chiamata `incrementa(n)` nasce il parametro `x`, che riceve una copia di 5. L'istruzione `x = x + 1` porta `x` a 6 (la prima stampa lo mostra), ma `n` non ne è influenzata: sono due celle di memoria distinte. Quando il metodo termina `x` scompare, e il `main` stampa ancora `n = 5`.

Una conseguenza classica: **non si può scrivere in Java un metodo che scambia due `int` del chiamante**.

```java
public class Scambio {
    public static void scambia(int a, int b) {
        int tmp = a;
        a = b;
        b = tmp;                             // scambia le copie: il chiamante non vede nulla
    }

    public static void main(String[] args) {
        int x = 1;
        int y = 2;
        scambia(x, y);
        System.out.println(x + " " + y);
    }
}
```

```text
1 2
```

Il metodo scambia correttamente le **copie** `a` e `b`, ma `x` e `y` restano come prima. Per far uscire dal metodo un risultato si usa il valore di ritorno (che è uno solo), oppure si modifica il contenuto di un oggetto o di un array ricevuto, come vediamo ora.

### 6.3.3 La conversione automatica degli argomenti

Se il tipo dell'argomento non coincide con quello del parametro, Java applica le stesse **conversioni implicite** viste nel Capitolo 2 (sezione 2.6.1): un argomento può essere passato a un parametro di un tipo "più largo" nella catena

```text
byte → short → int → long → float → double
```

senza bisogno di un cast. Il passaggio inverso invece richiede un cast esplicito.

```java
public class Conversione {
    public static double meta(double x) {
        return x / 2;
    }

    public static void main(String[] args) {
        int n = 7;
        System.out.println(meta(n));         // int -> double: conversione implicita
        System.out.println(meta(5));         // anche con un letterale int
    }
}
```

```text
3.5
2.5
```

Il caso opposto, `int k = meta(8);`, non compila: il metodo restituisce un `double` e l'assegnamento a `int` perderebbe la parte decimale (`incompatible types: possible lossy conversion from double to int`). Per ottenere un intero servirebbe un cast, `int k = (int) meta(8);`, con la perdita di informazione che sappiamo (sezione 2.6.3).

### 6.3.4 Parametri di tipo riferimento

Finora i parametri erano di tipo primitivo. Se il parametro è un **riferimento** (un array, una stringa, qualsiasi oggetto), la regola resta la stessa: si copia il valore della variabile, e il valore di una variabile di tipo riferimento è l'**indirizzo** dell'oggetto (sezione 2.2). Dopo la chiamata ci sono dunque **due riferimenti, quello del chiamante e quello del parametro, allo stesso oggetto**. Di conseguenza:

- il metodo **può modificare il contenuto** dell'oggetto, e la modifica è visibile al chiamante, perché l'oggetto è uno solo;
- il metodo **non può far puntare** la variabile del chiamante a un altro oggetto: assegnare un nuovo valore al parametro cambia soltanto la copia locale dell'indirizzo.

Lo abbiamo già visto con gli array nella sezione 5.5.2. Lo riassumiamo in un esempio che mette a confronto i due comportamenti:

```java
import java.util.Arrays;

public class PerRiferimento {
    public static void azzeraPrimo(int[] v) {
        v[0] = 0;                            // modifica l'oggetto condiviso: il chiamante lo vede
    }

    public static void sostituisci(int[] v) {
        v = new int[] {9, 9, 9};             // il parametro punta a un altro array; il chiamante no
    }

    public static void main(String[] args) {
        int[] a = {5, 6, 7};
        azzeraPrimo(a);
        System.out.println(Arrays.toString(a));
        sostituisci(a);
        System.out.println(Arrays.toString(a));
    }
}
```

```text
[0, 6, 7]
[0, 6, 7]
```

Dopo `azzeraPrimo(a)` il primo elemento di `a` è 0, perché `v` e `a` indicano lo stesso array. Dopo `sostituisci(a)` l'array di `a` è invariato: dentro il metodo `v` è stato fatto puntare a un array nuovo, ma `a` nel `main` continua a puntare a quello vecchio. Il meccanismo non è diverso da quello dei primitivi: in entrambi i casi **si copia il contenuto della variabile**; solo che nel secondo caso il contenuto è un indirizzo. Il [Capitolo 8 — Riferimenti e memoria](08-riferimenti-e-memoria.md) lo approfondirà, con stack e heap.

Una stringa è un oggetto, ma `String` è **immutabile** (sezione 3.1.4): nessun metodo può cambiarne il contenuto, quindi un metodo che riceve una `String` non può "modificare" la stringa del chiamante, e un assegnamento al parametro, come sempre, cambia solo la copia locale.

## 6.4 Metodi statici e metodi d'istanza

### 6.4.1 Metodi `static`: appartengono alla classe

Finora ogni metodo aveva `static` nell'intestazione, e abbiamo detto solo che "si chiama senza creare un oggetto". Vediamo il perché. Una classe è, nella programmazione a oggetti, un modello da cui si creano **oggetti** (se ne parla nel [Capitolo 7 — Classi e oggetti](07-classi-e-oggetti.md)). Alcuni metodi però non hanno niente a che fare con un oggetto in particolare: calcolare il massimo di due interi, convertire una lunghezza, trasformare un carattere in maiuscolo. Per questi compiti sarebbe assurdo dover prima creare un oggetto qualsiasi solo per poterli chiamare.

Un metodo dichiarato `static` appartiene alla **classe** e non a un oggetto. Per chiamarlo da fuori si scrive il **nome della classe**, un punto e il nome del metodo:

```text
NomeClasse.nomeMetodo(argomenti)
```

```java
class Lunghezze {
    static double inCentimetri(double pollici) {
        return pollici * 2.54;
    }

    static double inPollici(double centimetri) {
        return centimetri / 2.54;
    }
}

public class ProvaLunghezze {
    public static void main(String[] args) {
        System.out.println(Lunghezze.inCentimetri(10));    // nome della classe, punto, metodo
        System.out.println(Lunghezze.inPollici(5.08));
    }
}
```

```text
25.4
2.0
```

Le due classi stanno nello stesso file (la forma d'esame, sezione 1.10) e la sola `public` è quella con il `main`. Il `main` chiama i metodi di `Lunghezze` scrivendo il nome della classe: non esiste nessun oggetto `Lunghezze`, e non serve. È la stessa forma già incontrata con `Math.sqrt(...)` e con `Integer.parseInt(...)`: `Math` e `Integer` sono classi, e quei metodi sono statici.

**Dentro la stessa classe** il nome della classe si può omettere: un metodo statico chiama un altro metodo statico della propria classe scrivendo solo il nome (è ciò che fa il `main` quando chiama `inMetri(km1)` nella sezione 6.1.2).

### 6.4.2 Variabili di classe e costanti

Anche le variabili possono essere `static`. Una variabile `static` è **condivisa** da tutta la classe: ne esiste una sola copia, a cui accedono tutti. Per questo si chiama anche **variabile di classe** (*class variable*), in contrapposizione alle **variabili d'istanza** (*instance variables*), di cui ogni oggetto ha la propria copia. Le une e le altre, insieme, si dicono **campi** (*fields*) o *data members*.

> [!NOTE]
> **Definizione — Variabile di classe e costante di classe**
> Una variabile dichiarata `static` è una **variabile di classe**: esiste in un'unica copia, condivisa da tutti. Se è dichiarata `static final` è una **costante di classe**: il valore è assegnato una volta sola e non può più cambiare. Una variabile di classe senza `final` può invece essere modificata.

Le costanti di classe le abbiamo già incontrate (sezione 2.4) e le usiamo da tempo: `Integer.MAX_VALUE` è una costante `static final` della classe `Integer`. Un esempio con una variabile che invece cambia: una classe che distribuisce numeri progressivi e tiene il conto dell'incasso.

```java
class Biglietteria {
    static final int PREZZO = 8;            // costante di classe
    private static int emessi = 0;          // variabile di classe: una sola copia per tutti

    static int prossimoNumero() {
        emessi = emessi + 1;                // modifica la variabile condivisa
        return emessi;
    }

    static int incasso() {
        return PREZZO * emessi;
    }
}

public class ProvaBiglietteria {
    public static void main(String[] args) {
        System.out.println(Biglietteria.prossimoNumero());
        System.out.println(Biglietteria.prossimoNumero());
        System.out.println(Biglietteria.prossimoNumero());
        System.out.println("Incasso: " + Biglietteria.incasso());
    }
}
```

```text
1
2
3
Incasso: 24
```

Seguiamo i valori. `emessi` parte da 0. Ogni chiamata di `prossimoNumero()` lo incrementa e restituisce il nuovo valore, quindi le tre stampe sono 1, 2, 3: la variabile conserva il suo valore **tra una chiamata e l'altra**, perché non è locale al metodo ma appartiene alla classe. Alla fine `emessi` vale 3 e `incasso()` restituisce `8 * 3 = 24`. La parola `private` davanti a `emessi` significa che solo i metodi di `Biglietteria` possono leggerla o scriverla; la tratteremo nel Capitolo 7. Per ora basta sapere che dal `main` non si può scrivere `Biglietteria.emessi`.

> [!WARNING]
> **Attenzione — Non confondere variabile di classe e variabile di tipo classe**
> Una "variabile di classe" è una variabile `static`. Una "variabile di tipo classe" è una variabile il cui tipo è una classe, per esempio `String nome;` o `Biglietteria b;`: contiene un riferimento a un oggetto. Sono due cose diverse con nomi quasi uguali.

### 6.4.3 Metodi statici e metodi d'istanza insieme

Un metodo **non** dichiarato `static` si chiama **metodo d'istanza** (*instance method*): lavora su un oggetto specifico, e per chiamarlo serve un oggetto. Un oggetto si crea con l'operatore `new` seguito dal nome della classe e da `()`, e lo si chiama scrivendo `nomeOggetto.nomeMetodo(...)`. I dettagli sono nel Capitolo 7; ci basta per capire la differenza.

```java
class Contatore {
    int valore;                              // campo d'istanza: ogni oggetto ha il suo

    void incrementa() {                      // metodo d'istanza: lavora sul campo di un oggetto
        valore = valore + 1;
    }

    static String descrizione() {            // metodo statico: non riguarda nessun oggetto
        return "Contatore di interi";
    }
}

public class ProvaContatore {
    public static void main(String[] args) {
        Contatore a = new Contatore();       // due oggetti distinti
        Contatore b = new Contatore();
        a.incrementa();
        a.incrementa();
        b.incrementa();
        System.out.println(a.valore + " " + b.valore);
        System.out.println(Contatore.descrizione());
    }
}
```

```text
2 1
Contatore di interi
```

Gli oggetti `a` e `b` hanno ciascuno il proprio `valore`: `a.incrementa()` ne ha toccato uno, `b.incrementa()` l'altro. `descrizione()` invece non ha un "proprio" oggetto: si chiama con il nome della classe.

Da questa differenza nasce una regola che il compilatore applica con rigore.

| Chi chiama | Può usare un metodo statico | Può usare un metodo d'istanza |
|---|---|---|
| metodo **statico** | sì, direttamente | **no**, a meno di indicare un oggetto: `oggetto.metodo()` |
| metodo **d'istanza** | sì, direttamente | sì, direttamente (opera sullo stesso oggetto) |

La stessa regola vale per i campi: un metodo statico non può usare direttamente un campo d'istanza, perché non sa di quale oggetto si parla. Dentro un metodo statico, `valore` da solo non ha senso; ha senso `a.valore`.

> [!CAUTION]
> **Errore tipico — Chiamare un metodo d'istanza da `main`**
> ```java
> class Prova {
>     int doppio(int n) {                  // metodo d'istanza (manca static)
>         return n * 2;
>     }
>     public static void main(String[] args) {
>         System.out.println(doppio(4));   // ERRORE DI COMPILAZIONE
>     }
> }
> ```
> Il compilatore risponde `non-static method doppio(int) cannot be referenced from a static context`. Il `main` è statico, quindi non ha alcun oggetto su cui chiamare `doppio`. Le correzioni possibili sono due: dichiarare `doppio` come `static` (la scelta giusta quando il metodo non usa campi d'istanza), oppure creare un oggetto e chiamare `new Prova().doppio(4)`. Quando una traccia dice "metodo invocabile senza creare un oggetto" richiede la prima.

Un metodo d'istanza può invece chiamare liberamente i metodi statici della propria classe. Un esempio che li mescola, un salvadanaio con un metodo d'istanza e un metodo di conversione statico:

```java
class Salvadanaio {
    double saldo;                                        // campo d'istanza

    void deposita(double euro) {                         // d'istanza: modifica lo stato
        saldo = saldo + euro;
    }

    void depositaCentesimi(int centesimi) {              // d'istanza: chiama un metodo statico
        saldo = saldo + centesimiInEuro(centesimi);
    }

    static double centesimiInEuro(int centesimi) {       // statico: nessun oggetto necessario
        return centesimi / 100.0;
    }
}

public class ProvaSalvadanaio {
    public static void main(String[] args) {
        Salvadanaio s = new Salvadanaio();
        s.deposita(10);
        s.depositaCentesimi(250);
        System.out.println(s.saldo);
        System.out.println(Salvadanaio.centesimiInEuro(75));
    }
}
```

```text
12.5
0.75
```

`depositaCentesimi` (d'istanza) chiama `centesimiInEuro` (statico) scrivendone solo il nome. Dal `main` invece la conversione si può usare anche senza oggetto: `Salvadanaio.centesimiInEuro(75)`. Si noti la divisione per `100.0` e non per `100`: con `100` la divisione tra interi darebbe `0` (Capitolo 2, sezione 2.5.2).

### 6.4.4 Un `main` dentro la classe

Finora il `main` stava in una classe a parte, solo per provare le altre. Spesso è utile metterlo **dentro la stessa classe** che si sta scrivendo, per collaudarla e, volendo, per eseguirla da sola.

```java
public class Temperatura {
    static double celsiusInFahrenheit(double celsius) {
        return celsius * 9 / 5 + 32;
    }

    public static void main(String[] args) {            // main della classe stessa
        System.out.println(celsiusInFahrenheit(100));
        System.out.println(celsiusInFahrenheit(0));
        System.out.println(celsiusInFahrenheit(-40));
    }
}
```

```text
212.0
32.0
-40.0
```

Lanciata con `java Temperatura`, la classe esegue il proprio `main`. Se invece un'altra classe usa `Temperatura.celsiusInFahrenheit(...)`, il `main` di `Temperatura` **non viene eseguito**: serve solo quando la classe è il punto di ingresso del programma. È la stessa idea di cui parla la sezione 1.10: il `main` serve per *eseguire*, non per compilare.

### 6.4.5 Dividere il `main` in sottocompiti

Un `main` che contiene tutta la logica diventa illeggibile e ripete le stesse righe. La cura è la stessa dell'inizio del capitolo: spostare ogni sottocompito in un metodo statico con un nome parlante, in modo che il `main` si legga come l'elenco dei passi.

```java
public class Rapporto {
    static void stampaLinea() {
        System.out.println("--------------------");
    }

    static void stampaTitolo(String titolo) {
        stampaLinea();                                   // un metodo che ne chiama un altro
        System.out.println(titolo);
        stampaLinea();
    }

    static double media(int[] voti) {
        int somma = 0;
        for (int v : voti) {
            somma = somma + v;
        }
        return (double) somma / voti.length;             // cast: divisione in virgola mobile
    }

    public static void main(String[] args) {
        int[] voti = {24, 28, 30, 27};
        stampaTitolo("Voti del corso");
        System.out.println("Media: " + media(voti));
        stampaLinea();
    }
}
```

```text
--------------------
Voti del corso
--------------------
Media: 27.25
--------------------
```

Il `main` dice *che cosa* si fa (titolo, media, linea) e i metodi dicono *come*. Se domani la linea dovesse essere di trenta trattini, si cambia in un punto solo. Notiamo anche che un metodo può chiamare altri metodi, non solo il `main`.

## 6.5 La classe `Math`

Molti calcoli matematici sono già pronti nella classe `Math` del package `java.lang`. È un esempio perfetto di classe fatta di metodi statici: non esistono oggetti `Math`, si chiamano i metodi con il nome della classe. Non serve nessun `import`: le classi di `java.lang` (`Math`, `String`, `Integer`, `System`…) sono sempre disponibili.

> [!NOTE]
> **Approfondimento esterno — La classe `Math`**
> La classe è `public final class Math`: i suoi membri sono tutti `static`. Le costanti sono `public static final double PI` ed `E`, i valori `double` più vicini a π e al numero di Nepero. I metodi usati più spesso sono:
> ```text
> public static int    abs(int a)             public static double abs(double a)
> public static int    max(int a, int b)      public static double max(double a, double b)
> public static int    min(int a, int b)      public static double min(double a, double b)
> public static double pow(double a, double b)
> public static double sqrt(double a)
> public static long   round(double a)        public static int    round(float a)
> public static double ceil(double a)
> public static double floor(double a)
> public static double random()
> ```
> `abs`, `max` e `min` esistono anche per `long` e `float`. `round` restituisce "il `long` più vicino all'argomento, con i casi a metà arrotondati verso l'infinito positivo"; `ceil` il più piccolo valore intero maggiore o uguale all'argomento, `floor` il più grande minore o uguale (entrambi restituiscono un `double`); `sqrt` di un numero minore di zero vale `NaN`; `random()` restituisce un `double` maggiore o uguale a `0.0` e minore di `1.0`. Per `Integer.MIN_VALUE`, `abs(int)` restituisce lo stesso valore, che è negativo.
> *Fonte:* [Math (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Math.html)

Alcuni esempi per vedere il tipo di ciò che si ottiene, che è il punto in cui di solito si sbaglia:

```java
public class UsoMath {
    public static void main(String[] args) {
        System.out.println(Math.pow(2, 10));          // 2 alla 10: il risultato è un double
        System.out.println((int) Math.pow(2, 10));    // cast per ottenere un int
        System.out.println(Math.sqrt(144));
        System.out.println(Math.sqrt(-1));            // radice di un negativo: NaN, non un errore
        System.out.println(Math.abs(-7));             // abs(int)
        System.out.println(Math.abs(-7.5));           // abs(double)
        System.out.println(Math.max(3, 8));           // max(int, int)
        System.out.println(Math.max(3, 8.5));         // un argomento double: si sceglie max(double, double)
        System.out.println(Math.round(2.4));
        System.out.println(Math.round(2.5));          // a metà: verso l'alto
        System.out.println(Math.round(-2.5));         // a metà, negativo: verso +infinito, quindi -2
        System.out.println(Math.ceil(2.1));
        System.out.println(Math.floor(2.9));
        System.out.println(Math.floor(-2.1));
        System.out.println(Math.PI);
    }
}
```

```text
1024.0
1024
12.0
NaN
7
7.5
8
8.5
2
3
-2
3.0
2.0
-3.0
3.141592653589793
```

Tre osservazioni che contano all'esame. Primo, `pow`, `sqrt`, `ceil` e `floor` restituiscono sempre un **`double`**, anche quando il risultato matematico è intero (`1024.0`): per averlo come `int` serve un cast, con la perdita di decimali che ne consegue. Secondo, `Math.round(double)` restituisce un **`long`**, non un `int`: `int r = Math.round(2.6);` non compila (`possible lossy conversion from long to int`) e si scrive `int r = (int) Math.round(2.6);`. Terzo, `abs`, `max` e `min` hanno più versioni, e il compilatore sceglie quella adatta al tipo degli argomenti: con due `int` il risultato è un `int`, con un `double` tra gli argomenti il risultato è un `double` (il meccanismo è l'**overloading**, sezione 6.7).

### 6.5.1 Arrotondare a due decimali

Un uso tipico è arrotondare un risultato a due cifre decimali. Si moltiplica per 100, si arrotonda, si divide per 100 **in virgola mobile**:

```java
public class DueDecimali {
    public static void main(String[] args) {
        double raggio = 2;
        double area = Math.PI * raggio * raggio;
        System.out.println(area);
        System.out.println(Math.round(area * 100) / 100.0);   // 100.0: il risultato resta un double
        System.out.println(Math.round(area * 100) / 100);     // 100: divisione tra long e int, intera
    }
}
```

```text
12.566370614359172
12.57
12
```

`Math.round(area * 100)` vale `1257` (un `long`). Dividendo per `100.0` si ottiene `12.57`; dividendo per `100` la divisione è tra interi e il risultato è `12`, senza decimali: lo stesso errore della sezione 2.5.2.

### 6.5.2 Numeri casuali

`Math.random()` restituisce un numero casuale `double` in `[0.0, 1.0)`. Per ottenere un intero in un intervallo si scala e si taglia: `(int) (Math.random() * 6)` dà un intero tra 0 e 5, e aggiungendo 1 si ottiene il lancio di un dado.

```java
public class Dado {
    public static void main(String[] args) {
        boolean tuttiValidi = true;
        for (int i = 0; i < 1000; i++) {
            int lancio = (int) (Math.random() * 6) + 1;       // intero tra 1 e 6
            if (lancio < 1 || lancio > 6) {
                tuttiValidi = false;
            }
        }
        System.out.println("Tutti tra 1 e 6: " + tuttiValidi);
    }
}
```

```text
Tutti tra 1 e 6: true
```

L'output di un programma che stampa i lanci cambierebbe a ogni esecuzione; per questo l'esempio verifica soltanto l'intervallo. Il cast `(int)` si applica a `Math.random() * 6` grazie alle parentesi: senza di esse il cast riguarderebbe solo `Math.random()`, che vale sempre `0` dopo il troncamento, e il risultato sarebbe sempre `1`.

## 6.6 Le classi wrapper

### 6.6.1 Il problema: un `int` non è un oggetto

I tipi primitivi (`int`, `double`, `char`…) non sono oggetti: non hanno metodi e, come sappiamo, un parametro primitivo viene passato per valore. Ma ci sono situazioni in cui serve **un oggetto che contenga un numero**. La più importante è quella delle collezioni (`ArrayList` e simili, [Capitolo 12 — Generics e collezioni](12-generics-e-collezioni.md)), che possono contenere solo oggetti; ma anche tutti i metodi che chiedono un `Object` o un tipo riferimento. In più, è comodo avere in un posto solo le funzioni che riguardano un tipo: convertire un testo in numero, sapere se un carattere è una cifra, conoscere il valore massimo.

Per questo Java fornisce, per ciascun tipo primitivo, una **classe wrapper** (*wrapper class*, "involucro") nel package `java.lang`.

| Tipo primitivo | Classe wrapper |
|---|---|
| `byte` | `Byte` |
| `short` | `Short` |
| `int` | `Integer` |
| `long` | `Long` |
| `float` | `Float` |
| `double` | `Double` |
| `char` | `Character` |
| `boolean` | `Boolean` |

Notiamo che i nomi sono quelli dei tipi con l'iniziale maiuscola, tranne due: `int` diventa `Integer` e `char` diventa `Character`.

### 6.6.2 Creare un oggetto wrapper

Un oggetto wrapper contiene un valore del tipo primitivo corrispondente e **non lo cambia mai**: i wrapper non hanno metodi *set* e sono quindi **immutabili**, come le stringhe. Per ottenere un oggetto wrapper si usa il metodo statico `valueOf`, che accetta il valore primitivo oppure una stringa:

```java
public class CreaWrapper {
    public static void main(String[] args) {
        Integer a = Integer.valueOf(42);            // da int
        Integer b = Integer.valueOf("42");          // da String
        Double d = Double.valueOf("3.5");           // da String
        int x = a.intValue();                       // dall'oggetto al primitivo
        double y = d.doubleValue();
        System.out.println(a + " " + b + " " + x);
        System.out.println(d + " " + y);
    }
}
```

```text
42 42 42
3.5 3.5
```

`intValue()` e `doubleValue()` restituiscono il valore primitivo contenuto nell'oggetto. I wrapper hanno anche un **costruttore** con lo stesso scopo, ad esempio `new Integer(42)`: nelle slide compare ancora, ma nelle versioni moderne di Java è **deprecato** e destinato alla rimozione (il compilatore lo segnala con un avviso). Si usa sempre `valueOf`.

> [!NOTE]
> **Approfondimento esterno — `Integer.valueOf` e i costruttori deprecati**
> Nella documentazione di Java SE 17 i costruttori `public Integer(int value)` e `public Integer(String s)` sono contrassegnati `@Deprecated(since="9", forRemoval=true)`: "It is rarely appropriate to use this constructor. The static factory `valueOf(int)` is generally a better choice". Il metodo `public static Integer valueOf(int i)` memorizza sempre in una cache gli oggetti per i valori da -128 a 127 compresi, e può memorizzarne altri. `Integer.valueOf(String)` interpreta l'argomento come `parseInt` e lancia `NumberFormatException` se il testo non è un intero.
> *Fonte:* [Integer (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Integer.html)

### 6.6.3 Boxing e unboxing automatici

Scrivere `Integer.valueOf(...)` e `intValue()` ogni volta sarebbe pesante. Perciò Java converte da solo tra primitivo e wrapper quando il contesto lo richiede. La conversione da primitivo a wrapper si chiama **autoboxing** (*boxing*), quella inversa **unboxing**.

```java
public class Boxing {
    public static void main(String[] args) {
        Integer n = 5;                  // autoboxing: equivale a Integer.valueOf(5)
        int m = n;                      // unboxing: equivale a n.intValue()
        Integer somma = n + 3;          // n viene "scartato", sommato, poi la somma è di nuovo "impacchettata"
        System.out.println(n + " " + m + " " + somma);

        Integer vuoto = null;
        try {
            int k = vuoto;              // unboxing di null
            System.out.println(k);
        } catch (NullPointerException e) {
            System.out.println("NullPointerException");
        }
    }
}
```

```text
5 5 8
NullPointerException
```

Le prime righe mostrano le conversioni automatiche in entrambi i sensi, comprese le espressioni aritmetiche (`n + 3` usa il valore `int` contenuto in `n`). L'ultima parte mostra il **rischio**: una variabile `Integer` è un riferimento e può essere `null`; l'unboxing di un `null` equivale a chiamare `intValue()` su `null` e lancia una `NullPointerException`. Il blocco `try`/`catch` che compare qui è lo strumento che studieremo nel [Capitolo 13 — Eccezioni](13-eccezioni.md); per ora basta leggerlo come "prova a eseguire queste righe e, se capita questa eccezione, stampa il messaggio".

### 6.6.4 I metodi statici dei wrapper

Le classi wrapper raccolgono un gran numero di metodi **statici** di utilità, che si chiamano con il nome della classe. Sono quelli che si usano più spesso all'esame.

| Classe | Metodo | Che cosa fa |
|---|---|---|
| `Integer` | `static int parseInt(String s)` | converte un testo in `int`; `NumberFormatException` se non è un intero |
| `Integer` | `static String toString(int i)` | converte un `int` in testo |
| `Integer` | `Integer.MAX_VALUE`, `Integer.MIN_VALUE` | il massimo e il minimo valore di `int` |
| `Double` | `static double parseDouble(String s)` | converte un testo in `double` |
| `Boolean` | `static boolean parseBoolean(String s)` | `true` solo se il testo è, ignorando le maiuscole, `"true"`; qualsiasi altra stringa (anche `null`) dà `false` |
| `Character` | `static boolean isDigit(char ch)` | `true` se il carattere è una cifra |
| `Character` | `static boolean isLetter(char ch)` | `true` se è una lettera |
| `Character` | `static boolean isUpperCase(char ch)` / `isLowerCase` | `true` se è maiuscola / minuscola |
| `Character` | `static boolean isWhitespace(char ch)` | `true` per spazio, tabulazione, a capo |
| `Character` | `static char toUpperCase(char ch)` / `toLowerCase` | converte il carattere |

La conversione da testo a numero con `parseInt` e `parseDouble` è già stata trattata nella sezione 2.6.4. Le funzioni di `Character` servono a esaminare una stringa carattere per carattere (i metodi `charAt` e `length` sono nella sezione 3.1.3):

```java
public class ContaCaratteri {
    public static void main(String[] args) {
        String testo = "Esame 2026: 3 esercizi!";
        int cifre = 0;
        int lettere = 0;
        int spazi = 0;
        for (int i = 0; i < testo.length(); i++) {
            char c = testo.charAt(i);
            if (Character.isDigit(c)) {
                cifre++;
            } else if (Character.isLetter(c)) {
                lettere++;
            } else if (Character.isWhitespace(c)) {
                spazi++;
            }
        }
        System.out.println("cifre: " + cifre);
        System.out.println("lettere: " + lettere);
        System.out.println("spazi: " + spazi);
        System.out.println(Character.toUpperCase('q'));
        System.out.println(Character.isUpperCase('q'));
    }
}
```

```text
cifre: 5
lettere: 13
spazi: 3
Q
false
```

Il testo contiene cinque cifre (`2`, `0`, `2`, `6`, `3`), tredici lettere (cinque in "Esame", otto in "esercizi") e tre spazi; i segni `:` e `!` non rientrano in nessuna delle tre categorie e vengono ignorati. Le ultime due righe mostrano `toUpperCase`, che restituisce il carattere convertito, e `isUpperCase`, che per `'q'` dà `false`.

Una nota sulla scelta: per sapere se un carattere è una cifra si può anche scrivere `c >= '0' && c <= '9'` (un `char` è un numero, sezione 2.2.4), e per il valore numerico di una cifra `c - '0'`. `Character.isDigit` è più leggibile e dice esattamente che cosa si sta controllando.

> [!NOTE]
> **Approfondimento esterno — I metodi di `Character`**
> Tutti questi metodi sono `public static` e ricevono un `char`. `isDigit(char ch)` "determina se il carattere specificato è una cifra": lo è se la sua categoria Unicode è `DECIMAL_DIGIT_NUMBER`, il che comprende le cifre `0`–`9` ma anche quelle di altri alfabeti. `isLetter(char ch)` è `true` per le lettere (maiuscole, minuscole e le altre categorie di lettera). `isUpperCase(char ch)` è `true` per le lettere maiuscole. Per `toUpperCase(char ch)` la documentazione avverte che `Character.isUpperCase(Character.toUpperCase(ch))` non dà sempre `true` per certi simboli e ideogrammi, e che per convertire un testo intero conviene usare `String.toUpperCase()`. Le versioni con `char` non gestiscono i caratteri fuori dal piano base di Unicode: esistono le versioni con `int`.
> *Fonte:* [Character (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Character.html)

### 6.6.5 Confrontare oggetti wrapper

Poiché un `Integer` è un oggetto, per confrontare due `Integer` valgono le regole degli oggetti (sezione 3.4.1): l'operatore `==` confronta i **riferimenti**, non i valori contenuti. Per confrontare i valori si usa `equals`.

```java
public class ConfrontoWrapper {
    public static void main(String[] args) {
        Integer a = 127;
        Integer b = 127;
        System.out.println(a == b);              // true: valori nella cache da -128 a 127
        Integer c = 1000;
        Integer d = 1000;
        System.out.println(c == d);              // false: sono due oggetti distinti
        System.out.println(c.equals(d));         // true: i valori contenuti sono uguali
        System.out.println(c == 1000);           // true: un operando è int, c viene "scartato"
        System.out.println(c.compareTo(d));      // 0: valori uguali
    }
}
```

```text
true
false
true
true
0
```

La prima riga dà `true` solo perché `Integer.valueOf` riusa lo stesso oggetto per i valori da -128 a 127 (riquadro della sezione 6.6.2); per `1000` gli oggetti sono due e `==` dà `false`. Per i valori **fuori** da quell'intervallo, la documentazione dice solo che la cache "può" servirli: il risultato di `==` non è garantito. Non bisogna quindi mai basarsi su `==` tra wrapper. La regola è semplice: tra due oggetti `Integer` (o `Double`, `Character`…) si usa `equals`, oppure si porta almeno uno dei due a tipo primitivo. Quando uno degli operandi è un `int`, come in `c == 1000`, il wrapper viene scartato e il confronto è tra numeri.

## 6.7 L'overloading

### 6.7.1 Lo stesso nome, parametri diversi

Calcolare la media di due numeri e la media di tre numeri è, a parole, lo stesso compito. Dover inventare due nomi (`media2`, `media3`) sarebbe scomodo. Java permette di dare **lo stesso nome a più metodi della stessa classe**, purché si distinguano per i parametri. Questa possibilità si chiama **overloading** (*sovraccarico*, o *sovraccaricamento*, dei metodi).

> [!NOTE]
> **Definizione — Firma e overloading**
> La **firma** (*signature*) di un metodo è il suo nome insieme al **numero**, all'**ordine** e ai **tipi** dei parametri. Il tipo di ritorno e i nomi dei parametri **non** fanno parte della firma. Due metodi della stessa classe con lo stesso nome ma firme diverse sono in **overloading**. Il compilatore li considera metodi del tutto distinti.

```java
public class Medie {
    static double media(int a, int b) {
        return (a + b) / 2.0;
    }

    static double media(int a, int b, int c) {          // numero di parametri diverso
        return (a + b + c) / 3.0;
    }

    static double media(double a, double b) {           // tipi dei parametri diversi
        return (a + b) / 2;
    }

    public static void main(String[] args) {
        System.out.println(media(4, 7));                // due int
        System.out.println(media(1, 2, 6));             // tre int
        System.out.println(media(1.5, 2.5));            // due double
        System.out.println('a');                        // println ha molte versioni: qui println(char)
        System.out.println('a' + 1);                    // 'a' + 1 è un int: println(int)
    }
}
```

```text
5.5
3.0
2.0
a
98
```

Le tre `media` hanno la stessa parola come nome e tre firme diverse: `(int, int)`, `(int, int, int)`, `(double, double)`. Il compilatore guarda gli argomenti della chiamata e decide quale versione eseguire. L'esempio più comune di overloading lo usiamo da sempre senza accorgercene: `System.out.println` ha una versione per `int`, una per `double`, una per `char`, una per `String` e così via, ed è il motivo per cui `println('a')` stampa la lettera mentre `println('a' + 1)` stampa il numero 98: nel secondo caso l'espressione ha tipo `int` (Capitolo 2, sezione 2.6.2), e viene scelta la versione per `int`.

### 6.7.2 Come il compilatore sceglie

Il compilatore sceglie il metodo **a tempo di compilazione**, guardando i tipi degli argomenti, con questa procedura:

1. cerca un metodo con la firma che **coincide** esattamente con i tipi degli argomenti;
2. se non c'è, cerca un metodo a cui gli argomenti si possano adattare con le **conversioni automatiche** della sezione 6.3.3 (per esempio da `int` a `double`), scegliendo la più vicina;
3. se non trova nulla, o ne trova due ugualmente adatte, **segnala un errore**.

```java
public class Scelta {
    static String tipo(int n) {
        return "int";
    }

    static String tipo(double x) {
        return "double";
    }

    public static void main(String[] args) {
        System.out.println(tipo(5));        // esatta: int
        System.out.println(tipo(5.0));      // esatta: double
        System.out.println(tipo(5L));       // long: non c'è tipo(long); si converte a double, non a int
        System.out.println(tipo('a'));      // char: si converte a int, la conversione più vicina
    }
}
```

```text
int
double
double
int
```

`tipo(5L)` passa un `long`. Non esiste una versione per `long`, e un `long` non si può convertire automaticamente in `int` (sarebbe un restringimento), mentre si può convertire in `double`: viene scelta quella. `tipo('a')` passa un `char`, convertibile sia in `int` sia in `double`; il compilatore preferisce la conversione più vicina nella catena `byte → short → int → long → float → double`, cioè `int`.

### 6.7.3 Overloading e conversione automatica possono scontrarsi

Una conseguenza spiacevole: poiché il compilatore **prima cerca la corrispondenza esatta** e solo dopo tenta le conversioni, un overloading con tipi numerici vicini può mandare la chiamata in una versione diversa da quella che il programmatore aveva in mente.

```java
public class Registro {
    static String registra(int eta) {
        return "eta " + eta;
    }

    static String registra(double peso) {
        return "peso " + peso;
    }

    public static void main(String[] args) {
        int kg = 70;                                    // il programmatore intende un peso
        System.out.println(registra(kg));               // ma kg è un int: viene scelta registra(int)
        System.out.println(registra((double) kg));      // con un cast si ottiene registra(double)
        System.out.println(registra(70.0));
    }
}
```

```text
eta 70
peso 70.0
peso 70.0
```

La prima chiamata è corretta per il compilatore, ma probabilmente sbagliata per chi l'ha scritta. Il consiglio che accompagna questo esempio è semplice: **quando due versioni fanno cose diverse, meglio dare nomi diversi** (`registraEta`, `registraPeso`). L'overloading va riservato ai casi in cui le versioni fanno davvero lo stesso lavoro su dati diversi, come le `media` o `Math.max`.

### 6.7.4 Il tipo di ritorno non distingue

Due metodi che differiscono **solo** per il tipo di ritorno non sono in overloading: il compilatore non potrebbe scegliere tra i due guardando la chiamata, perché l'espressione `valore(3)` ha lo stesso aspetto qualunque sia il tipo di ritorno. Il tentativo di definirli è un errore di compilazione.

> [!CAUTION]
> **Errore tipico — Overloading sul solo tipo di ritorno**
> ```java
> class Prova {
>     static int valore(int n) {
>         return n * 2;
>     }
>     static double valore(int n) {        // ERRORE DI COMPILAZIONE: stessa firma
>         return n * 2.0;
>     }
> }
> ```
> Il compilatore risponde `method valore(int) is already defined in class Prova`: la firma è `valore(int)` in entrambi i casi. Per averle entrambe bisogna cambiare i parametri o il nome (`valoreIntero`, `valoreDecimale`).

### 6.7.5 Un'annotazione `@Overload` non esiste

Per riconoscere un metodo in overloading **non esiste nessuna annotazione**: si guarda soltanto la firma. Chi ha incontrato `@Override` (che serve per un'altra cosa, il *riscrivere* un metodo di una superclasse, nel [Capitolo 9 — Ereditarietà e polimorfismo](09-ereditarieta-e-polimorfismo.md)) potrebbe aspettarsi un'annotazione gemella.

> [!CAUTION]
> **Errore tipico — Scrivere `@Overload`**
> ```java
> class Prova {
>     @Overload                            // ERRORE DI COMPILAZIONE
>     static int somma(int a, int b) {
>         return a + b;
>     }
> }
> ```
> Il compilatore risponde `cannot find symbol` (`symbol: class Overload`): in Java l'annotazione `@Overload` non esiste. Il metodo in overloading si scrive come un metodo qualsiasi, e basta che la sua firma sia diversa da quelle degli altri metodi con lo stesso nome.

Per non confondere i due termini: l'**overloading** (stessa classe, stesso nome, parametri diversi) viene risolto dal compilatore **a tempo di compilazione**; l'**overriding** (una sottoclasse riscrive un metodo ereditato, con la stessa firma) viene risolto dalla JVM **a tempo di esecuzione**, ed è il tema del Capitolo 9.

## 6.8 Progettare e collaudare i metodi

### 6.8.1 Scomporre un problema

Un metodo non si scrive quasi mai di getto. Il metodo che funziona è di solito l'ultimo anello di una **scomposizione**: si scrive a parole l'algoritmo, si individuano i sottocompiti e si traduce ogni sottocompito in poche righe, o in un metodo a parte.

Prendiamo un compito concreto: visualizzare un importo in euro, con due decimali, come `EUR 12.07`. Un `double` non si stampa a due decimali con una semplice `println`: `5.5` verrebbe stampato `5.5` e non `5.50`, e `5` come `5.0`. Un algoritmo a parole:

1. portare l'importo in **centesimi interi**, arrotondando;
2. se i centesimi sono negativi, ricordare il segno e lavorare sul valore assoluto;
3. i centesimi diviso 100 (divisione intera) sono gli **euro**; il resto della divisione per 100 sono i **centesimi**;
4. stampare `EUR`, l'eventuale segno, gli euro, un punto, i centesimi **su due cifre** (con uno zero davanti se sono meno di 10).

Ogni punto diventa una o due righe di codice:

```java
public class Importi {
    static void stampaEuro(double importo) {
        int totale = (int) Math.round(importo * 100);     // punto 1: centesimi interi, arrotondati
        System.out.print("EUR ");
        if (totale < 0) {                                  // punto 2: il segno
            System.out.print("-");
            totale = -totale;
        }
        int euro = totale / 100;                           // punto 3: divisione intera
        int centesimi = totale % 100;                      //          resto della divisione
        System.out.print(euro + ".");                      // punto 4
        if (centesimi < 10) {
            System.out.print("0");                         // zero davanti: 5 centesimi -> 05
        }
        System.out.println(centesimi);
    }

    public static void main(String[] args) {
        stampaEuro(12.07);
        stampaEuro(5);
        stampaEuro(0.5);
        stampaEuro(-3.5);
        stampaEuro(0.999);
    }
}
```

```text
EUR 12.07
EUR 5.00
EUR 0.50
EUR -3.50
EUR 1.00
```

Verifichiamo i casi limite uno alla volta. Con `5` (un `int` convertito in `double`) i centesimi sono 0 e la regola dello zero davanti produce `00`. Con `0.5` i centesimi sono 50, quindi nessuno zero davanti. Con `-3.5` il valore è `-350`: il segno è stampato una volta, poi si lavora su `350`, e senza il punto 2 la divisione `-350 / 100` darebbe `-3` ma il resto `-350 % 100` darebbe `-50`, con il segno nel posto sbagliato. Con `0.999` l'arrotondamento a 100 centesimi porta a `EUR 1.00`, e non a `0.99`, come si potrebbe pensare troncando. Una bozza che funzionasse solo con numeri positivi "tondi" avrebbe superato il primo esempio e fallito gli altri: scomporre in passi e controllare ciascuno sui casi limite è il metodo con cui si evitano questi errori.

### 6.8.2 Credere al compilatore

Quando il compilatore segnala un errore su un metodo, la regola pratica è **credergli**: il messaggio quasi sempre ha ragione, e conviene correggere il codice come richiesto invece di discutere. I due richiami più frequenti riguardano proprio i metodi: una variabile locale usata prima di essere inizializzata, e un `return` mancante su uno dei percorsi possibili (sezione 6.1.4).

```java
public class Controlli {
    static int massimoTra(int a, int b) {
        int risultato;                      // locale: nessun valore iniziale
        if (a > b) {
            risultato = a;
        } else {
            risultato = b;                  // tutti i rami assegnano: il compilatore è soddisfatto
        }
        return risultato;
    }

    public static void main(String[] args) {
        System.out.println(massimoTra(3, 9));
    }
}
```

```text
9
```

Se nel secondo ramo mancasse l'assegnamento, il compilatore direbbe `variable risultato might not have been initialized`: non sa dimostrare che la variabile ha un valore su tutti i percorsi, e quindi vieta di leggerla. È la stessa logica del `return` mancante.

### 6.8.3 Collaudare con driver e stub

Un metodo si prova da solo, separatamente dagli altri: si scrive un piccolo `main`, detto **programma pilota** (*driver*), che lo chiama con argomenti di cui si conosce il risultato. Ogni metodo di una classe andrebbe collaudato così. Ma cosa fare quando un metodo ne usa un altro che **non è ancora scritto**? Si usa un **stub**, cioè una versione semplificata del metodo mancante, che restituisce un valore fisso e serve solo a permettere il collaudo del resto. Il collaudo conviene farlo **dal basso** (*bottom-up*): prima i metodi che non ne chiamano altri, poi quelli che li usano.

```java
public class Scontrino {
    // STUB: versione provvisoria di sconto. Restituisce sempre 10, per poter provare netto e stampaNetto.
    static int sconto(int totale) {
        return 10;
    }

    static int netto(int totale) {
        return totale - sconto(totale);
    }

    static void stampaNetto(int totale) {
        System.out.println("Netto: " + netto(totale));
    }

    // DRIVER: un main che serve solo a chiamare i metodi con valori noti
    public static void main(String[] args) {
        stampaNetto(100);
        stampaNetto(50);
    }
}
```

```text
Netto: 90
Netto: 40
```

Con lo stub, `netto` e `stampaNetto` si possono verificare subito (`100 - 10 = 90`, `50 - 10 = 40`). Quando `sconto` verrà scritto per davvero, basterà sostituire il corpo dello stub e ripetere le stesse chiamate del driver.

## 6.9 La ricorsione

### 6.9.1 Un metodo che chiama se stesso

Una lista da percorrere si può guardare come "il primo elemento, più il resto della lista"; una cartella contiene file e altre cartelle. In situazioni così il compito si ripresenta, in piccolo, dentro sé stesso. In Java un metodo può **chiamare se stesso**: si parla allora di **ricorsione** (*recursion*), e il metodo è **ricorsivo**.

> [!NOTE]
> **Definizione — Metodo ricorsivo**
> Un metodo è **ricorsivo** quando, per risolvere un problema, include una chiamata a se stesso su una **versione più piccola** dello stesso problema. Deve contenere almeno un **caso base** (*base case*, o condizione di arresto): un caso abbastanza semplice da essere risolto **senza** nuove chiamate ricorsive.

Il primo esempio è volutamente semplice: dato un intero `n`, stampare i numeri da `n` fino a 1. Con un ciclo sarebbe più rapido; lo facciamo ricorsivamente per vedere il meccanismo.

Si ragiona così. Il caso più semplice è `n` minore di 1: non c'è niente da stampare, ed è il **caso base**. Per `n` più grande, il lavoro è "stampare `n`, poi stampare i numeri da `n - 1` fino a 1", e la seconda parte è lo stesso problema con un numero più piccolo.

```java
public class ContoAllaRovescia {
    static void conto(int n) {
        if (n < 1) {
            return;                         // caso base: niente da fare, nessuna nuova chiamata
        }
        System.out.println(n);              // stampa n
        conto(n - 1);                       // chiamata ricorsiva su un problema più piccolo
    }

    public static void main(String[] args) {
        conto(3);
    }
}
```

```text
3
2
1
```

### 6.9.2 Come funziona: la pila delle chiamate

Per capire che cosa succede basta ricordare che **ogni chiamata ha le proprie variabili locali e i propri parametri**. La JVM tiene una **pila delle chiamate** (*call stack*, Capitolo 1, sezione 1.9): ogni volta che un metodo viene chiamato, vi si aggiunge un riquadro con il parametro `n` di quella chiamata. Quando il metodo termina il riquadro viene tolto, e l'esecuzione riprende nel punto in cui era stata sospesa, nel metodo che aveva chiamato.

Per `conto(3)` la sequenza è la seguente (ogni rientro è una chiamata più profonda):

```text
conto(3): n = 3, stampa 3, chiama conto(2)
    conto(2): n = 2, stampa 2, chiama conto(1)
        conto(1): n = 1, stampa 1, chiama conto(0)
            conto(0): n = 0, caso base: ritorna
        conto(1) riprende, non ha altro da fare: ritorna
    conto(2) riprende, non ha altro da fare: ritorna
conto(3) riprende, non ha altro da fare: ritorna
```

Quattro riquadri sono in pila contemporaneamente, ciascuno con un `n` diverso (3, 2, 1, 0). La stampa avviene **scendendo**: prima si stampa, poi si chiama. Se si invertisse l'ordine delle due istruzioni il comportamento cambierebbe in modo istruttivo:

```java
public class DalBasso {
    static void conto(int n) {
        if (n < 1) {
            return;
        }
        conto(n - 1);                       // prima la chiamata ricorsiva...
        System.out.println(n);              // ...poi la stampa, mentre le chiamate rientrano
    }

    public static void main(String[] args) {
        conto(3);
    }
}
```

```text
1
2
3
```

Ora la stampa avviene **risalendo**. `conto(3)` chiama subito `conto(2)` senza stampare, e così via fino a `conto(0)`, che ritorna. Solo allora `conto(1)` può eseguire la sua stampa (`1`), poi tocca a `conto(2)` (`2`) e infine a `conto(3)` (`3`). Lo stesso metodo, con due righe scambiate, produce l'ordine opposto: è la prova che il lavoro "dopo la chiamata" viene fatto quando le chiamate rientrano.

### 6.9.3 Le condizioni perché funzioni

Un metodo ricorsivo corretto ha quattro caratteristiche:

1. un'istruzione di **scelta** (`if`, `switch`…) che separa i casi;
2. almeno un **caso base**, in cui **non** si fa nessuna chiamata ricorsiva;
3. almeno un ramo con una **chiamata ricorsiva**;
4. ogni chiamata ricorsiva usa un argomento **più piccolo** (più vicino al caso base) di quello ricevuto, così che prima o poi il caso base viene raggiunto.

### 6.9.4 La ricorsione infinita

Se manca il caso base, oppure l'argomento non si avvicina mai ad esso, il metodo si richiama senza fermarsi. Ogni chiamata aggiunge un riquadro alla pila; la pila ha una dimensione limitata, e a un certo punto si riempie. La JVM interrompe allora l'esecuzione lanciando un errore, `StackOverflowError`.

> [!NOTE]
> **Approfondimento esterno — `StackOverflowError`**
> La documentazione di Java SE 17 descrive `StackOverflowError` come: "Thrown when a stack overflow occurs because an application recurses too deeply". Discende da `VirtualMachineError` e da `Error` (non da `Exception`): è un errore della JVM, non un'eccezione che un programma sia tenuto a prevedere.
> *Fonte:* [StackOverflowError (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/StackOverflowError.html)

```java
public class Infinita {
    static int profondita = 0;

    static void senzaFine(int n) {
        profondita = profondita + 1;
        senzaFine(n + 1);                   // nessun caso base: non si ferma mai
    }

    public static void main(String[] args) {
        try {
            senzaFine(0);
        } catch (StackOverflowError e) {
            System.out.println("StackOverflowError");
            System.out.println(profondita > 1000);     // molte chiamate prima di esaurire la pila
        }
    }
}
```

```text
StackOverflowError
true
```

Il `try`/`catch` serve soltanto a mostrare l'errore senza far terminare il programma; nei programmi veri non si cattura un `StackOverflowError`, si corregge la ricorsione. Il numero esatto di chiamate prima dell'errore dipende dalla JVM e dalla memoria, per questo l'esempio stampa solo se è stato "molto grande". Un caso insidioso è quello in cui un caso base **esiste** ma non viene mai raggiunto: per esempio `conto(n + 1)` al posto di `conto(n - 1)`, con la condizione `n < 1` che non sarà mai vera partendo da `3`.

### 6.9.5 Ricorsione o iterazione?

Qualsiasi metodo ricorsivo si può riscrivere **senza ricorsione**, con un ciclo: la versione con il ciclo si dice **iterativa**. Prendiamo la somma dei primi `n` interi.

```java
public class SommaFinoA {
    static int ricorsiva(int n) {
        if (n <= 0) {
            return 0;                       // caso base
        }
        return n + ricorsiva(n - 1);        // n più la somma dei precedenti
    }

    static int iterativa(int n) {
        int somma = 0;
        for (int i = 1; i <= n; i++) {
            somma = somma + i;
        }
        return somma;
    }

    public static void main(String[] args) {
        System.out.println(ricorsiva(5));
        System.out.println(iterativa(5));
    }
}
```

```text
15
15
```

Le due versioni danno lo stesso risultato. Quella ricorsiva usa **più memoria** (un riquadro di pila per ogni chiamata, mentre il ciclo usa sempre le stesse due variabili) ed è di solito **più lenta**, per il lavoro che la JVM fa a ogni chiamata. Perché dunque usare la ricorsione? Perché per alcuni problemi, come la ricerca binaria e l'ordinamento per fusione che vedremo tra poco, la soluzione ricorsiva è molto più **chiara** e breve di quella iterativa. La regola pratica è: se il ciclo è altrettanto semplice, si usa il ciclo; se il problema si scompone naturalmente in sotto-problemi dello stesso tipo, si usa la ricorsione.

### 6.9.6 Metodi ricorsivi che restituiscono un valore

Le stesse regole valgono quando il metodo restituisce un valore: almeno un ramo restituisce un valore **senza** chiamate ricorsive (caso base), e almeno un ramo restituisce un valore **costruito** a partire dalla chiamata ricorsiva. L'esempio classico è il **fattoriale**: `n! = n · (n - 1) · … · 1`, con `0! = 1`. Per il matematico il fattoriale è già definito ricorsivamente: `n! = n · (n - 1)!`.

```java
public class Fattoriale {
    static long fattoriale(int n) {
        if (n <= 1) {
            return 1;                       // caso base: 0! = 1! = 1
        }
        return n * fattoriale(n - 1);       // n per il fattoriale del numero più piccolo
    }

    public static void main(String[] args) {
        System.out.println(fattoriale(0));
        System.out.println(fattoriale(5));
        System.out.println(fattoriale(20));
        System.out.println(fattoriale(21));
    }
}
```

```text
1
120
2432902008176640000
-4249290049419214848
```

Per `fattoriale(4)` il valore si costruisce **risalendo** dalle chiamate:

```text
fattoriale(4) = 4 * fattoriale(3)
                    = 3 * fattoriale(2)
                          = 2 * fattoriale(1)
                                = 1           (caso base)
fattoriale(2) = 2 * 1 = 2
fattoriale(3) = 3 * 2 = 6
fattoriale(4) = 4 * 6 = 24
```

Si noti il tipo `long`: i fattoriali crescono in fretta e `int` si esaurisce già a `13!`. Anche `long` ha un limite: `21!` non ci sta e il risultato **trabocca** (Capitolo 2, sezione 2.5.3), diventando un numero negativo senza alcun errore.

Un secondo esempio, tratto dalle slide, conta le cifre `0` di un numero non negativo. L'idea: si guarda l'ultima cifra (`n % 10`) e si ripete il conteggio sul numero senza l'ultima cifra (`n / 10`).

```java
public class ContaZeri {
    static int contaZeri(int n) {
        if (n == 0) {
            return 1;                                  // il numero 0 ha una cifra, ed è uno zero
        } else if (n < 10) {
            return 0;                                  // una sola cifra diversa da zero
        } else if (n % 10 == 0) {
            return contaZeri(n / 10) + 1;              // ultima cifra zero: la contiamo
        } else {
            return contaZeri(n / 10);                  // ultima cifra non zero: non la contiamo
        }
    }

    public static void main(String[] args) {
        System.out.println(contaZeri(0));
        System.out.println(contaZeri(407));
        System.out.println(contaZeri(2030));
        System.out.println(contaZeri(1000));
    }
}
```

```text
1
1
2
3
```

Seguiamo `contaZeri(2030)`. L'ultima cifra è `0`, quindi si calcola `contaZeri(203) + 1`. Per `203` l'ultima cifra è `3`: si calcola `contaZeri(20)`. Per `20` l'ultima cifra è `0`: `contaZeri(2) + 1`. E `contaZeri(2)` è un caso base (`n < 10`, cifra non zero): `0`. Risalendo: `0 + 1 = 1` per `20`, `1` per `203`, `1 + 1 = 2` per `2030`. Il caso `n == 0` è trattato a parte perché altrimenti `0 / 10` darebbe ancora `0` e la ricorsione non finirebbe mai.

### 6.9.7 Ripetere una lettura finché il dato è corretto

La ricorsione si può usare anche per chiedere un dato **fino a quando è valido**: il metodo legge, e se il dato non va bene richiama se stesso.

```java
import java.util.Scanner;

public class VotoValido {
    static int leggiVoto(Scanner in) {
        int voto = in.nextInt();
        if (voto < 18 || voto > 30) {
            System.out.println("Valore errato, riprova");
            return leggiVoto(in);               // chiamata ricorsiva: nuova lettura
        }
        return voto;                            // caso base: il dato è valido
    }

    public static void main(String[] args) {
        Scanner in = new Scanner("40 5 25");    // tre valori: i primi due non sono validi
        System.out.println(leggiVoto(in));
    }
}
```

```text
Valore errato, riprova
Valore errato, riprova
25
```

Funziona, ma è una tecnica da usare con cautela: **ogni tentativo sbagliato aggiunge un riquadro alla pila**, e un utente ostinato che sbagliasse migliaia di volte potrebbe provocare un `StackOverflowError`. Un ciclo `while` (Capitolo 4, sezione 4.5.1) non ha questo difetto ed è in genere la scelta migliore. Per rendere l'esempio ripetibile qui il `Scanner` legge da una stringa invece che dalla tastiera (costruttore `Scanner(String)`, Capitolo 4, sezione 4.5.2).

### 6.9.8 Ricerca binaria

Cercare un numero in un array **già ordinato** si può fare molto meglio che scorrerlo tutto. Si guarda l'elemento **centrale**: se è quello cercato, si è finito; se il numero cercato è più piccolo, può trovarsi solo nella metà sinistra; se è più grande, solo nella metà destra. In entrambi i casi il problema si è dimezzato e si ripete lo stesso ragionamento sulla metà rimasta.

Per descrivere la metà su cui lavorare servono due parametri in più: `primo` e `ultimo`, gli indici dei limiti. I casi base sono due: l'intervallo è vuoto (`primo > ultimo`: non c'è, restituiamo `-1`), oppure l'elemento centrale è quello cercato.

```java
public class RicercaBinaria {
    static int cerca(int[] a, int primo, int ultimo, int target) {
        if (primo > ultimo) {
            return -1;                                          // caso base: intervallo vuoto
        }
        int meta = (primo + ultimo) / 2;                        // indice dell'elemento centrale
        if (a[meta] == target) {
            return meta;                                        // caso base: trovato
        } else if (target < a[meta]) {
            return cerca(a, primo, meta - 1, target);           // metà sinistra
        } else {
            return cerca(a, meta + 1, ultimo, target);          // metà destra
        }
    }

    static int cerca(int[] a, int target) {                     // overloading: comodo per chi chiama
        return cerca(a, 0, a.length - 1, target);
    }

    public static void main(String[] args) {
        int[] a = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};        // ordinato in modo crescente
        System.out.println(cerca(a, 23));
        System.out.println(cerca(a, 2));
        System.out.println(cerca(a, 91));
        System.out.println(cerca(a, 7));
    }
}
```

```text
5
0
9
-1
```

Seguiamo la ricerca di `23` su dieci elementi (indici 0-9). Prima chiamata: `primo = 0`, `ultimo = 9`, `meta = 4`, `a[4] = 16`; `23 > 16`, quindi si cerca a destra con `primo = 5`. Seconda chiamata: `primo = 5`, `ultimo = 9`, `meta = 7`, `a[7] = 56`; `23 < 56`, si cerca a sinistra con `ultimo = 6`. Terza chiamata: `primo = 5`, `ultimo = 6`, `meta = 5`, `a[5] = 23`: trovato, restituisce `5`. Tre confronti su dieci elementi. Ogni passo dimezza l'intervallo, quindi su mille elementi bastano circa dieci confronti, contro i mille di una ricerca sequenziale. In cambio l'array **deve essere ordinato**: su un array non ordinato la ricerca binaria dà risultati senza senso.

Il secondo metodo `cerca(int[] a, int target)` è un caso utile di overloading (sezione 6.7): chi chiama non deve conoscere i parametri `primo` e `ultimo`, che servono solo alla ricorsione.

### 6.9.9 Ordinamento per fusione

L'ordinamento per selezione del Capitolo 5 (sezione 5.6.3) richiede un numero di confronti che cresce con il quadrato della lunghezza. L'**ordinamento per fusione** (*merge sort*) è un algoritmo del tipo **dividi e conquista** (*divide and conquer*) molto più veloce, e si scrive in modo naturale con la ricorsione:

1. se l'array ha meno di due elementi è già ordinato (caso base);
2. altrimenti lo si **divide a metà** in due array più piccoli;
3. si **ordinano le due metà**, chiamando lo stesso metodo (ricorsione);
4. si **fondono** (*merge*) le due metà ordinate in un unico array ordinato.

La fusione è facile: le due metà sono ordinate, quindi il più piccolo di tutti è il primo elemento di una delle due. Si confrontano i primi elementi delle due metà, si sposta il più piccolo nel risultato e si avanza in quella metà; si ripete finché una delle due si esaurisce, poi si copiano gli elementi rimasti dell'altra.

```java
import java.util.Arrays;

public class OrdinamentoPerFusione {
    static void mergeSort(int[] a) {
        if (a.length < 2) {
            return;                                             // caso base: già ordinato
        }
        int meta = a.length / 2;
        int[] sinistra = Arrays.copyOfRange(a, 0, meta);        // prima metà
        int[] destra = Arrays.copyOfRange(a, meta, a.length);   // seconda metà
        mergeSort(sinistra);                                    // ordina la prima metà
        mergeSort(destra);                                      // ordina la seconda
        fondi(sinistra, destra, a);                             // le riunisce dentro a
    }

    static void fondi(int[] sinistra, int[] destra, int[] risultato) {
        int i = 0;                                              // posizione in sinistra
        int j = 0;                                              // posizione in destra
        int k = 0;                                              // posizione in risultato
        while (i < sinistra.length && j < destra.length) {
            if (sinistra[i] <= destra[j]) {
                risultato[k] = sinistra[i];
                i++;
            } else {
                risultato[k] = destra[j];
                j++;
            }
            k++;
        }
        while (i < sinistra.length) {                           // avanzi della metà sinistra
            risultato[k] = sinistra[i];
            i++;
            k++;
        }
        while (j < destra.length) {                             // avanzi della metà destra
            risultato[k] = destra[j];
            j++;
            k++;
        }
    }

    public static void main(String[] args) {
        int[] a = {38, 27, 43, 3, 9, 82, 10};
        mergeSort(a);
        System.out.println(Arrays.toString(a));
    }
}
```

```text
[3, 9, 10, 27, 38, 43, 82]
```

Il metodo `mergeSort` non restituisce niente: riceve `a` e ne **modifica il contenuto**, come previsto dal passaggio dei riferimenti (sezione 6.3.4). Le due metà sono array nuovi, copiati con `Arrays.copyOfRange` (sezione 5.4.4). La riga `fondi(sinistra, destra, a)` scrive il risultato in `a`, che è lo stesso array del chiamante.

I tre cicli di `fondi` vanno letti insieme. Il primo gira finché **entrambe** le metà hanno elementi, e a ogni giro sposta il più piccolo; `<=` e non `<` rende l'ordinamento *stabile*, cioè lascia nello stesso ordine due elementi uguali. Al termine del primo ciclo una delle due metà è esaurita, e **al più uno** degli altri due cicli fa qualcosa: copia in coda ciò che resta dell'altra metà, già ordinato e già più grande di tutto ciò che è stato spostato.

## Come esce all'esame

**Appello dell'8 settembre 2026 (EXAM4) — Esercizio 3 (5 punti), logica di base.** La traccia chiedeva di definire una classe `Convertitore` e, al suo interno, un metodo `converti` "invocabile senza creare un oggetto", che riceve una distanza in chilometri (intero) e restituisce l'equivalente in metri (intero). L'output atteso mostrava il risultato di quattro chiamate, con un valore nullo e uno negativo (`converti(0) -> 0`, `converti(-3) -> -3000`). Del capitolo servono: la definizione di un metodo con parametro e tipo di ritorno (sezione 6.1.2), l'istruzione `return` (6.1.4) e soprattutto la parola chiave `static`, che la traccia esprime a parole con "invocabile senza creare un oggetto" (6.4.1). Vincoli letterali: il nome della classe, il nome del metodo, i tipi `int` del parametro e del risultato, il metodo statico.

**EXAM2 — Esercizio 1 (5 punti), logica di base.** Stessa sostanza, con la firma data per intero: "creare una classe `Convertitore` contenente un metodo statico con la firma `public static int converti(int km)`", che riceve chilometri e restituisce metri. Vincolo letterale: la firma, da copiare carattere per carattere (`public`, `static`, `int`, il nome, il tipo e il nome del parametro). La traccia dava soltanto la firma, ma il metodo va comunque scritto dentro una classe, altrimenti il file non compila (sezione 1.10).

**EXAM2 — Esercizio 3 (13 punti), concorrenza.** Tra i requisiti c'era la scrittura di tre metodi di una classe `Buffer` le cui firme esatte andavano **dedotte dalle chiamate** presenti nel codice già fornito delle altre classi. È la competenza della sezione 6.3.1: il tipo dei parametri di un metodo deve essere compatibile con gli argomenti che il chiamante passa, e il tipo di ritorno con l'uso che il chiamante fa del risultato (per esempio un valore assegnato a un `int` implica un metodo che restituisce un `int`). Il resto dell'esercizio riguarda i capitoli 5 e 18.

## Scheletri da esame

### Una classe con un metodo statico di conversione

*Quando si usa:* la traccia chiede una classe con un metodo "invocabile senza creare un oggetto" che riceve un valore e ne restituisce un altro.

```java
class Conversioni {                                      // la classe avvolge il metodo: è tutto il file
    public static int oreInMinuti(int ore) {             // static + tipo di ritorno + nome + parametro, come la traccia
        return ore * 60;
    }
}

public class ProvaConversioni {                          // la classe di prova: l'unica public
    public static void main(String[] args) {
        System.out.println("oreInMinuti(2)  ->  " + Conversioni.oreInMinuti(2));
        System.out.println("oreInMinuti(0)  ->  " + Conversioni.oreInMinuti(0));
        System.out.println("oreInMinuti(-1) ->  " + Conversioni.oreInMinuti(-1));
    }
}
```

```text
oreInMinuti(2)  ->  120
oreInMinuti(0)  ->  0
oreInMinuti(-1) ->  -60
```

Nessun `import`. Nessuna eccezione da dichiarare. In una prova scritta il `main` di prova di solito non va scritto: la classe di collaudo c'è già e chiama il metodo. Nomi, tipi e `static` si copiano dalla traccia senza cambiarli.

### Un metodo con `return` su ogni percorso

*Quando si usa:* il metodo sceglie tra più valori in base a intervalli, e il compilatore pretende un `return` su ogni strada.

```java
class Valutazione {
    static String giudizio(int voto) {
        if (voto < 0 || voto > 30) {
            return "non valido";                         // i valori non ammessi per primi
        } else if (voto < 18) {
            return "insufficiente";
        } else if (voto <= 24) {
            return "sufficiente";
        } else {
            return "ottimo";                             // l'else finale chiude tutti i percorsi
        }
    }

    public static void main(String[] args) {
        System.out.println(Valutazione.giudizio(31));
        System.out.println(Valutazione.giudizio(12));
        System.out.println(Valutazione.giudizio(18));
        System.out.println(Valutazione.giudizio(27));
    }
}
```

```text
non valido
insufficiente
sufficiente
ottimo
```

Nessun `import`, nessuna eccezione. Ogni ramo termina con `return`, e il ramo `else` finale evita il `missing return statement`. Con più `if` successivi senza `else`, il compilatore non può sapere che sono esaustivi: serve un `return` finale fuori da tutti gli `if`.

### Un metodo ricorsivo con caso base

*Quando si usa:* il problema si riduce a se stesso con un argomento più piccolo (potenza, fattoriale, somma di cifre).

```java
public class Potenze {
    static int potenza(int base, int esponente) {
        if (esponente == 0) {
            return 1;                                    // caso base: qualsiasi numero alla 0 vale 1
        }
        return base * potenza(base, esponente - 1);      // esponente più piccolo a ogni chiamata
    }

    static int potenzaIterativa(int base, int esponente) {   // la stessa funzione con un ciclo
        int risultato = 1;
        for (int i = 0; i < esponente; i++) {
            risultato = risultato * base;
        }
        return risultato;
    }

    public static void main(String[] args) {
        System.out.println(potenza(2, 10));
        System.out.println(potenza(5, 0));
        System.out.println(potenza(3, 4));
        System.out.println(potenzaIterativa(3, 4));
    }
}
```

```text
1024
1
81
81
```

Nessun `import`, nessuna eccezione. Ricetta in tre mosse: **il caso base per primo** (`return` senza chiamate), poi la chiamata ricorsiva con l'argomento ridotto, poi un `return` che usa il suo risultato. Il metodo funziona per esponenti `>= 0`; con un esponente negativo non raggiunge mai il caso base e termina con `StackOverflowError`.

### Ricerca binaria ricorsiva con metodo di comodo

*Quando si usa:* cercare un valore in un array ordinato, restituendo la posizione oppure `-1`.

```java
class Ricerca {
    static int cerca(int[] a, int primo, int ultimo, int target) {
        if (primo > ultimo) {
            return -1;                                   // intervallo vuoto: non trovato
        }
        int meta = (primo + ultimo) / 2;
        if (a[meta] == target) {
            return meta;                                 // trovato
        } else if (target < a[meta]) {
            return cerca(a, primo, meta - 1, target);    // cerca a sinistra
        } else {
            return cerca(a, meta + 1, ultimo, target);   // cerca a destra
        }
    }

    static int cerca(int[] a, int target) {              // overloading: nasconde primo e ultimo
        return cerca(a, 0, a.length - 1, target);
    }

    public static void main(String[] args) {
        int[] a = {3, 8, 15, 21, 40, 52};
        System.out.println(cerca(a, 21));
        System.out.println(cerca(a, 4));
    }
}
```

```text
3
-1
```

Nessun `import`, nessuna eccezione. Su un array **non ordinato** il risultato non è affidabile. Il caso base `primo > ultimo` va controllato **prima** di leggere `a[meta]`, altrimenti con un intervallo vuoto si accede a un indice fuori dai limiti.

### Da testo a numero, con un valore di ripiego

*Quando si usa:* i dati arrivano come testo (da file, rete, riga di comando) e un valore non valido non deve interrompere il programma.

```java
class Lettura {
    static int leggiIntero(String testo, int ripiego) {
        try {
            return Integer.parseInt(testo.trim());       // trim toglie gli spazi ai bordi
        } catch (NumberFormatException e) {
            return ripiego;                              // testo non numerico: valore di ripiego
        }
    }

    static int leggiIntero(String testo) {               // overloading: ripiego a 0
        return leggiIntero(testo, 0);
    }

    public static void main(String[] args) {
        System.out.println(leggiIntero("42"));
        System.out.println(leggiIntero(" 17 "));
        System.out.println(leggiIntero("abc"));
        System.out.println(leggiIntero("3.5", -1));
    }
}
```

```text
42
17
0
-1
```

Nessun `import` (`Integer` è in `java.lang`). `NumberFormatException` è un'eccezione **non controllata**: non va dichiarata con `throws`, ma va intercettata se il programma deve proseguire. `parseInt` non accetta spazi ai bordi né decimali: `"3.5"` è un testo non valido per un intero.

## Errori tipici

Tre errori sono già discussi nel testo: chiamare un metodo d'istanza da `main` (sezione 6.4.3), differenziare due metodi solo per il tipo di ritorno (6.7.4) e scrivere `@Overload` (6.7.5). Seguono gli altri.

> [!CAUTION]
> **Errore tipico — Un percorso senza `return`**
> ```java
> static int segno(int n) {
>     if (n > 0) {
>         return 1;
>     } else if (n < 0) {
>         return -1;
>     }                                    // ERRORE DI COMPILAZIONE: se n == 0 il metodo finisce senza return
> }
> ```
> Il compilatore risponde `missing return statement`. Non può dimostrare che le due condizioni coprano tutti i casi. Forma corretta: un `else { return 0; }` finale, oppure un `return 0;` dopo gli `if`.

> [!CAUTION]
> **Errore tipico — Il tipo restituito non corrisponde**
> ```java
> static int meta(int n) {
>     return n / 2.0;                      // ERRORE DI COMPILAZIONE: l'espressione è un double
> }
> ```
> Il compilatore risponde `incompatible types: possible lossy conversion from double to int`. Il tipo dell'espressione dopo `return` deve essere compatibile con quello dichiarato. Forma corretta: dichiarare `double` come tipo di ritorno, oppure convertire con un cast se la perdita dei decimali è voluta.

> [!CAUTION]
> **Errore tipico — Usare il risultato di un metodo `void`**
> ```java
> static void stampa(int n) {
>     System.out.println(n);
> }
> public static void main(String[] args) {
>     int x = stampa(5);                   // ERRORE DI COMPILAZIONE: stampa non restituisce nulla
> }
> ```
> Il compilatore risponde `incompatible types: void cannot be converted to int`. Un metodo `void` si chiama con un'istruzione a sé; per ottenere un valore il metodo deve avere un tipo di ritorno e un `return`.

> [!CAUTION]
> **Errore tipico — Argomenti che non corrispondono ai parametri**
> ```java
> static double area(double base, double altezza) {
>     return base * altezza / 2;
> }
> public static void main(String[] args) {
>     System.out.println(area(4));         // ERRORE DI COMPILAZIONE: un argomento in meno
> }
> ```
> Il compilatore risponde `method area in class ... cannot be applied to given types;` e aggiunge `required: double,double`, `found: int`, `reason: actual and formal argument lists differ in length`. Gli argomenti devono avere lo stesso numero e un tipo compatibile con quello dei parametri, nello stesso ordine.

> [!CAUTION]
> **Errore tipico — Dimenticare le parentesi nella chiamata, o sbagliare il nome**
> ```java
> int m = inMetri;                         // ERRORE DI COMPILAZIONE: manca (5)
> int n = inmetri(5);                      // ERRORE DI COMPILAZIONE: il nome è inMetri
> ```
> Il compilatore risponde `cannot find symbol` per entrambe: la prima è letta come il nome di una **variabile** (`symbol: variable inMetri`), la seconda cerca un metodo `inmetri` che non esiste (`symbol: method inmetri(int)`). Java distingue maiuscole e minuscole, e una chiamata ha sempre le parentesi, anche senza argomenti.

> [!CAUTION]
> **Errore tipico — Il tipo del parametro ripetuto una sola volta**
> ```java
> static int somma(int a, b) {             // ERRORE DI COMPILAZIONE
>     return a + b;
> }
> ```
> Il compilatore risponde `<identifier> expected`. Ogni parametro ha il suo tipo anche quando sono uguali: `int a, int b`.

> [!CAUTION]
> **Errore tipico — Una variabile locale usata senza valore**
> ```java
> static int doppioPositivo(int n) {
>     int risultato;
>     if (n > 0) {
>         risultato = n * 2;
>     }
>     return risultato;                    // ERRORE DI COMPILAZIONE: con n <= 0 non ha mai ricevuto un valore
> }
> ```
> Il compilatore risponde `variable risultato might not have been initialized`. Forma corretta: dare un valore iniziale (`int risultato = 0;`) oppure assegnarlo su tutti i percorsi.

> [!CAUTION]
> **Errore tipico — Una variabile usata fuori dal suo blocco**
> ```java
> for (int i = 0; i < 3; i++) {
>     int quadrato = i * i;
> }
> System.out.println(quadrato);            // ERRORE DI COMPILAZIONE: quadrato esiste solo nel ciclo
> ```
> Il compilatore risponde `cannot find symbol` (`symbol: variable quadrato`). La variabile è dichiarata dentro il blocco del `for` e finisce con esso. Forma corretta: dichiararla prima del ciclo.

> [!CAUTION]
> **Errore tipico — Aspettarsi che un metodo modifichi un parametro primitivo**
> ```java
> static void raddoppia(int n) {
>     n = n * 2;                           // cambia solo la copia locale
> }
> // main: int x = 4; raddoppia(x); System.out.println(x);   // stampa 4, non 8
> ```
> Il programma compila e stampa `4`: il parametro è una copia (sezione 6.3.2). Per far arrivare il risultato al chiamante il metodo deve restituirlo (`static int raddoppia(int n) { return n * 2; }`, chiamato come `x = raddoppia(x);`).

> [!CAUTION]
> **Errore tipico — Chiamare un metodo senza usare il risultato**
> ```java
> String testo = "ciao";
> testo.toUpperCase();                     // compila, ma non cambia nulla
> Math.sqrt(16);                           // compila, ma il risultato viene buttato
> System.out.println(testo);               // stampa ancora "ciao"
> ```
> Un metodo che restituisce un valore non modifica il suo argomento: il risultato va **raccolto** (`testo = testo.toUpperCase();`) o usato. Il compilatore non segnala nulla, e l'errore si scopre solo dall'output.

> [!CAUTION]
> **Errore tipico — Perdere i decimali nel metodo**
> ```java
> static double media(int a, int b) {
>     return (a + b) / 2;                  // ERRORE LOGICO: divisione tra interi
> }
> ```
> `media(4, 7)` restituisce `5.0` e non `5.5`: la divisione tra due `int` è intera, e il troncamento avviene **prima** della conversione a `double` (Capitolo 2, sezione 2.5.2). Forma corretta: `(a + b) / 2.0`.

> [!CAUTION]
> **Errore tipico — `Math.pow` e `Math.round` assegnati a un `int`**
> ```java
> int p = Math.pow(2, 3);                  // ERRORE DI COMPILAZIONE: pow restituisce un double
> int r = Math.round(2.6);                 // ERRORE DI COMPILAZIONE: round(double) restituisce un long
> ```
> Il compilatore risponde in entrambi i casi `incompatible types: possible lossy conversion` (da `double` a `int` la prima, da `long` a `int` la seconda). Forma corretta: `int p = (int) Math.pow(2, 3);` e `int r = (int) Math.round(2.6);`.

> [!CAUTION]
> **Errore tipico — Confrontare due `Integer` con `==`**
> ```java
> Integer a = 1000;
> Integer b = 1000;
> if (a == b) { ... }                      // ERRORE LOGICO: confronta i riferimenti
> ```
> Compila, ma il confronto è falso perché sono due oggetti distinti. Per valori piccoli (da -128 a 127) darebbe invece `true`, e questo rende l'errore difficile da scoprire. Forma corretta: `a.equals(b)`, oppure `a.intValue() == b.intValue()`.

> [!CAUTION]
> **Errore tipico — Una chiamata ambigua**
> ```java
> static String f(int a, double b) { return "id"; }
> static String f(double a, int b) { return "di"; }
> // f(1, 2) -> ERRORE DI COMPILAZIONE
> ```
> Con due argomenti `int`, entrambe le versioni richiedono una conversione e nessuna è più vicina dell'altra: il compilatore risponde `reference to f is ambiguous`. Forma corretta: un cast che indichi quale versione si vuole (`f(1, 2.0)`), oppure nomi diversi.

> [!CAUTION]
> **Errore tipico — Ricorsione senza caso base, o che non lo raggiunge**
> ```java
> static int somma(int n) {
>     return n + somma(n - 1);             // ERRORE LOGICO: nessun caso base
> }
> ```
> Compila, ma `somma(3)` si richiama all'infinito e termina con `StackOverflowError` (sezione 6.9.4). Forma corretta: aggiungere `if (n <= 0) { return 0; }` prima della chiamata. Lo stesso accade se il caso base c'è ma la chiamata non si avvicina mai a esso (`somma(n + 1)`).

> [!CAUTION]
> **Errore tipico — La chiamata ricorsiva senza `return`**
> ```java
> static int somma(int n) {
>     if (n <= 0) {
>         return 0;
>     }
>     n + somma(n - 1);                    // ERRORE DI COMPILAZIONE: non è un'istruzione
> }
> ```
> Il compilatore risponde `not a statement`: un'espressione da sola non è un'istruzione. Dimenticare il `return` davanti alla chiamata ricorsiva è lo sbaglio più comune nei metodi ricorsivi con valore. Forma corretta: `return n + somma(n - 1);`.

> [!CAUTION]
> **Errore tipico — Una firma diversa da quella richiesta dalla traccia**
> ```java
> class Conversioni {
>     public static double oreInMinuti(double ore) {      // la traccia chiedeva: int, int
>         return ore * 60;
>     }
> }
> ```
> Il codice compila e calcola il valore giusto, ma non è il metodo richiesto: il test nascosto chiama `oreInMinuti` con un `int` e stampa il risultato come numero intero (`120`), mentre questa versione produce `120.0`; l'output non coincide e un'esecuzione è consumata. Anche quando il risultato matematico è lo stesso, i **tipi** e i **nomi** della traccia vanno copiati senza modifiche, compresi `static` e `public` se compaiono.

> [!CAUTION]
> **Errore tipico — Un metodo scritto fuori dalla classe**
> ```java
> class Conversioni {
>     // ...
> }
> static int oreInMinuti(int ore) {        // ERRORE DI COMPILAZIONE: fuori da ogni classe
>     return ore * 60;
> }
> ```
> Un metodo sta sempre **dentro** le graffe di una classe (sezione 1.10). Con Java 17 il messaggio è `class, interface, enum, or record expected`; le versioni più recenti possono dare messaggi diversi, ma la causa è la stessa. Forma corretta: spostare il metodo prima della graffa che chiude la classe.

## Riassunto

Un **metodo** è un blocco di istruzioni con un nome, scritto una volta e chiamato quante volte serve. L'intestazione dice tipo di ritorno, nome e parametri; `return` termina il metodo e consegna un valore, e ogni percorso di un metodo con valore deve concludersi con un `return`. Le variabili dichiarate nel metodo, parametri compresi, sono **locali** e vivono solo lì. Gli argomenti sono **copiati** nei parametri (passaggio per valore): un metodo non può cambiare un primitivo del chiamante, e con gli oggetti copia l'indirizzo, quindi può modificarne il contenuto ma non sostituire l'oggetto. Un metodo `static` appartiene alla classe e si chiama con il nome della classe, senza oggetti, ma non può usare direttamente metodi e campi d'istanza. La classe `Math` raccoglie funzioni matematiche statiche; le **classi wrapper** (`Integer`, `Double`, `Character`…) portano i primitivi nel mondo degli oggetti, con conversione automatica (boxing e unboxing) e metodi statici di utilità come `parseInt`. L'**overloading** permette più metodi con lo stesso nome e firme diverse, scelti dal compilatore. Un metodo ricorsivo ha un caso base e una chiamata su un problema più piccolo; ricerca binaria e ordinamento per fusione ne sono i due esempi classici. I metodi si progettano scomponendo il problema e si collaudano uno alla volta con un driver, usando stub per quelli non ancora scritti.

**Concetti chiave**

- **Metodo, intestazione, corpo.** `modificatori tipo_di_ritorno nome(parametri) { corpo }`, sempre dentro una classe.
- **Chiamata.** Un metodo con valore si usa in un'espressione; un metodo `void` è un'istruzione a sé.
- **`return`.** Termina il metodo e restituisce il valore; ogni percorso deve avere il suo `return`, altrimenti `missing return statement`.
- **Effetto collaterale.** Tutto ciò che un metodo fa oltre a restituire un valore (stampare, modificare campi o array).
- **Variabile locale e ambito.** Visibile dalla dichiarazione alla fine del blocco; senza valore iniziale.
- **Parametri formali e argomenti.** Devono corrispondere per numero, ordine e tipo (con le conversioni automatiche, mai quelle che restringono).
- **Passaggio per valore.** Si copia il valore; per gli oggetti si copia l'indirizzo.
- **`static`.** Il metodo (o il campo) appartiene alla classe; `static final` definisce una costante di classe.
- **Metodo d'istanza.** Lavora su un oggetto; da un contesto statico serve un oggetto per chiamarlo.
- **`Math`.** `pow`, `sqrt`, `abs`, `max`, `min` (sempre `double` per `pow`/`sqrt`), `round` (restituisce `long`), `ceil`, `floor`, `random`.
- **Classi wrapper.** Un wrapper per ogni primitivo; `valueOf` per crearle, boxing e unboxing automatici; `equals` al posto di `==`.
- **Overloading.** Stessa firma = errore; il tipo di ritorno non fa parte della firma; `@Overload` non esiste.
- **Ricorsione.** Caso base + chiamata su un argomento più piccolo; senza caso base `StackOverflowError`.
- **Driver e stub.** Collaudare i metodi uno alla volta, dal basso.

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `Math` | `abs` | `static int abs(int a)` (e versioni per `long`, `float`, `double`) | — |
| `Math` | `max`, `min` | `static int max(int a, int b)` (e versioni per `long`, `float`, `double`) | — |
| `Math` | `pow` | `static double pow(double a, double b)` | — |
| `Math` | `sqrt` | `static double sqrt(double a)` | — (`NaN` se `a` è negativo) |
| `Math` | `round` | `static long round(double a)`, `static int round(float a)` | — |
| `Math` | `ceil`, `floor` | `static double ceil(double a)`, `static double floor(double a)` | — |
| `Math` | `random` | `static double random()` | — (valore in `[0.0, 1.0)`) |
| `Integer` | `parseInt` | `static int parseInt(String s) throws NumberFormatException` | `NumberFormatException` (non controllata) |
| `Integer` | `valueOf` | `static Integer valueOf(int i)`, `static Integer valueOf(String s) throws NumberFormatException` | `NumberFormatException` (non controllata) |
| `Integer` | `intValue` | `int intValue()` | — |
| `Integer` | `toString` | `static String toString(int i)` | — |
| `Integer` | `compareTo` | `int compareTo(Integer anotherInteger)` | — |
| `Double` | `parseDouble` | `static double parseDouble(String s) throws NumberFormatException` | `NumberFormatException`, `NullPointerException` (non controllate) |
| `Boolean` | `parseBoolean` | `static boolean parseBoolean(String s)` | — |
| `Character` | `isDigit`, `isLetter` | `static boolean isDigit(char ch)`, `static boolean isLetter(char ch)` | — |
| `Character` | `isUpperCase`, `isWhitespace` | `static boolean isUpperCase(char ch)`, `static boolean isWhitespace(char ch)` | — |
| `Character` | `toUpperCase`, `toLowerCase` | `static char toUpperCase(char ch)`, `static char toLowerCase(char ch)` | — |
