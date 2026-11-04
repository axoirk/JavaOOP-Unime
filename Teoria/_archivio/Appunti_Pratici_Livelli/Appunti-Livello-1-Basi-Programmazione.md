# Livello 1: Le Basi della Programmazione e Sintassi

## 1. Input/Output e Variabili

### Teoria Fondamentale: Tipi di Dato e Flussi di Sistema
In Java, l'interazione con l'utente avviene tramite i flussi standard (Standard Streams). La classe `Scanner` (presente nel package `java.util`) funge da interprete del flusso di byte in ingresso (tipicamente `System.in`, la tastiera). Mentre il flusso di base vede solo byte crudi, lo `Scanner` li "tokenizza", ovvero li scompone e li converte automaticamente in tipi primitivi Java (`int`, `double`, `String`, ecc.) basandosi su delimitatori (di default gli spazi bianchi o gli 'a capo').

> **Definizione Accademica (Variabile e Stato):**
> Una variabile è un'astrazione della cella di memoria RAM. Essa è caratterizzata da un **tipo**, un **nome (identificatore)** e un **valore**. Java è un linguaggio **fortemente tipizzato** (strongly typed) e **staticamente tipizzato**.

### Esempio: Calcolo dell'Area di un Cerchio
In questo esempio, chiediamo all'utente il raggio di un cerchio e calcoliamo l'area, dimostrando l'uso di `Scanner` e `double`.

```java
import java.util.Scanner;

public class CalcoloArea {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Inserisci il raggio del cerchio: ");
        double raggio = input.nextDouble();
        
        // Uso della costante Math.PI e del metodo Math.pow per l'elevamento a potenza
        double area = Math.PI * Math.pow(raggio, 2);
        
        System.out.printf("L'area del cerchio con raggio %.2f è: %.2f\n", raggio, area);
        
        input.close();
    }
}
```

---

## 2. Strutture di Controllo Condizionali

### Teoria Fondamentale: Biforcazione Algoritmica
Le strutture condizionali permettono al flusso di esecuzione di biforcarsi basandosi sulla valutazione di espressioni logico-booleane. 
L'istruzione **`if-else`** gestisce intervalli o condizioni complesse, mentre lo **`switch`** è ottimizzato per il confronto di una singola variabile con più valori costanti (Jump Table).

### Esempio: Classificazione Temperature e Stagioni
Usiamo un `if-else` per classificare il clima e uno `switch` per stampare un messaggio in base alla stagione.

```java
public class Clima {
    public enum Stagione { PRIMAVERA, ESTATE, AUTUNNO, INVERNO }

    public static void main(String[] args) {
        double temperatura = 25.5;

        // 1. Controllo IF-ELSE
        if (temperatura < 10) {
            System.out.println("Clima Rigido");
        } else if (temperatura <= 25) {
            System.out.println("Clima Temperato");
        } else {
            System.out.println("Clima Caldo");
        }

        // 2. Costrutto SWITCH con Enum
        Stagione attuale = Stagione.ESTATE;
        switch (attuale) {
            case ESTATE:
                System.out.println("Tempo di vacanze!");
                break;
            case INVERNO:
                System.out.println("Tempo di sciare!");
                break;
            default:
                System.out.println("Goditi il paesaggio.");
                break;
        }
    }
}
```

---

## 3. I Cicli (Iterazioni)

### Teoria Fondamentale: Cicli Definiti e Indefiniti
- **`for`**: Ideale quando conosciamo a priori il numero di iterazioni.
- **`while`**: Ideale quando il ciclo continua finché una condizione è vera (es. valore sentinella).
- **`do-while`**: Garantisce almeno un'esecuzione del blocco di codice.

### Esempio: Calcolo del Fattoriale e Inserimento Validato
```java
import java.util.Scanner;

public class Iterazioni {
    public static void main(String[] args) {
        // 1. Ciclo FOR per il Fattoriale
        int n = 5;
        long fattoriale = 1;
        for (int i = 1; i <= n; i++) {
            fattoriale *= i;
        }
        System.out.println("Il fattoriale di " + n + " è: " + fattoriale);

        // 2. Ciclo WHILE per validazione input
        Scanner sc = new Scanner(System.in);
        int scelta;
        
        System.out.println("Scegli un numero tra 1 e 3:");
        scelta = sc.nextInt();
        
        while (scelta < 1 || scelta > 3) {
            System.out.println("Errore! Scegli un numero VALIDO (1-3):");
            scelta = sc.nextInt();
        }
        
        System.out.println("Hai scelto l'opzione: " + scelta);
        sc.close();
    }
}
```

---

## 4. I Packages

### Teoria Fondamentale: Organizzazione in Namespace
I package evitano conflitti di nomi e riflettono la struttura delle cartelle sul disco. La direttiva `package` deve essere la prima riga del file.

### Esempio: Geometria e Applicazione
**File: `it/unime/geo/Rettangolo.java`**
```java
package it.unime.geo;

public class Rettangolo {
    public double calcolaArea(double b, double h) {
        return b * h;
    }
}
```

**File: `it/unime/main/App.java`**
```java
package it.unime.main;
import it.unime.geo.Rettangolo;

public class App {
    public static void main(String[] args) {
        Rettangolo r = new Rettangolo();
        System.out.println("Area: " + r.calcolaArea(5, 10));
    }
}
```

---

## 5. Array Primitivi (Essenziali)

### Teoria Fondamentale: Memoria Contigua e Indici
Un array è un contenitore di dimensione fissa che ospita elementi dello stesso tipo in memoria contigua. L'accesso avviene tramite indice (0-based).

### Esempio: Gestione Inventario
```java
public class Inventario {
    public static void main(String[] args) {
        // Dichiarazione e inizializzazione di un array di interi
        int[] scorte = {150, 20, 45, 12, 80};
        String[] prodotti = {"Bulloni", "Viti", "Chiodi", "Dadi", "Rondelle"};

        System.out.println("Stato Magazzino:");
        for (int i = 0; i < prodotti.length; i++) {
            System.out.println(prodotti[i] + ": " + scorte[i] + " unità");
        }
    }
}
```

### Array bidimensionali (matrici)
Una matrice in Java è **un array di array**: ogni riga è un array a sé, e righe diverse possono avere lunghezze diverse, anche zero. Le tracce lo sfruttano: *"le righe possono avere lunghezze diverse"* è la frase che annuncia `int[][]`.

```java
public class Matrici {
    public static void main(String[] args) {
        int[][] reparti = new int[4][];            // 4 righe, ognuna ancora da creare
        reparti[0] = new int[]{8, 12, 25, 10};
        reparti[1] = new int[]{15, 20, 11};
        reparti[2] = new int[]{30, 9, 21, 14, 5};
        reparti[3] = new int[0];                   // riga vuota: legale

        System.out.println("righe: " + reparti.length);              // 4   -> numero di righe
        System.out.println("riga 2: " + reparti[2].length);          // 5   -> lunghezza DI QUELLA riga
        System.out.println("riga 3: " + reparti[3].length);          // 0

        int somma = 0;
        for (int i = 0; i < reparti.length; i++) {                   // righe
            for (int j = 0; j < reparti[i].length; j++) {            // colonne DI QUELLA riga
                somma += reparti[i][j];
            }
        }
        System.out.println("somma: " + somma);                       // 180

        int righeNonVuote = 0;
        for (int[] riga : reparti) {                                 // for-each: ogni elemento è un int[]
            if (riga.length > 0) righeNonVuote++;
        }
        System.out.println("righe non vuote: " + righeNonVuote);     // 3

        int[][] tabella = {{1, 2, 3}, {4, 5, 6}};                    // forma compatta, righe uguali
        System.out.println(tabella[1][2]);                           // 6: riga 1, colonna 2
    }
}
```

**Tre regole.** `m.length` conta le **righe**; `m[i].length` conta le colonne **della riga `i`** (mai `m[0].length` per tutte: le righe possono differire). Un metodo che riceve "la matrice delle misure" ha il parametro `int[][]`, **non** `int[]`: con il tipo sbagliato il metodo non esiste per chi lo chiama (`cannot find symbol` o `NoSuchMethodError`). E una riga può essere vuota: il ciclo interno semplicemente non gira, non è un errore.

---

## 6. Manipolazione delle Stringhe e Dimensioni (Length vs Size)

### Teoria Fondamentale: String non è un Array primitivo
A differenza del C o C++, in Java la `String` è un **Oggetto** a tutti gli effetti, non un semplice array di caratteri (non si possono usare le parentesi quadre `[i]` per leggere i caratteri). Ha a disposizione un ricco arsenale di metodi per la manipolazione.

### Esempio: Contare le parole (Split vs Ciclo Manuale)
Un caso tipico è dividere o analizzare una stringa di testo. Il metodo `split(String regex)` è lo strumento più potente per "tagliare" le stringhe usando un delimitatore (es. uno spazio vuoto).

```java
public class AnalisiStringhe {
    public static void main(String[] args) {
        String frase = "Questa è una prova tecnica";

        // METODO 1 (Smart): Usare split() per tagliare tramite spazio
        String[] parole = frase.split(" ");
        System.out.println("Numero totale di parole: " + parole.length); // Stampa 5

        // METODO 2 (Manuale): Contare gli spazi uno ad uno
        int counterSpazi = 0;
        // Non si può fare frase[i]! Si usa il metodo charAt()
        for (int i = 0; i < frase.length(); i++) {
            if (frase.charAt(i) == ' ') { 
                counterSpazi++;
            }
        }
        
        // Le parole sono gli spazi totali + 1
        System.out.println("Numero di parole (manuale): " + (counterSpazi + 1));
    }
}
```

### Il Grande Dilemma: `length` vs `length()` vs `size()`
In Java, chiedere "quanto è lungo" qualcosa ha una sintassi diversa a seconda della **famiglia** a cui l'oggetto appartiene. Memorizza bene questa regola d'oro:

1. **`length` (Senza parentesi tonde)**
   - **Famiglia:** **Array Primitivi** (es. `int[]`, `String[]`, `double[]`).
   - **Cos'è:** È una *variabile pubblica* strutturale, non un metodo. L'array ha una dimensione fissa e immutabile registrata in questa variabile.
   - **Esempio:** `int numeroDiParole = parole.length;`

2. **`length()` (Con parentesi tonde)**
   - **Famiglia:** Classe **`String`** (e classi affini come `StringBuilder`).
   - **Cos'è:** È un vero e proprio *metodo* che ispeziona l'oggetto stringa e calcola quanti caratteri contiene.
   - **Esempio:** `int lettereTotali = frase.length();`

3. **`size()` (Con parentesi tonde)**
   - **Famiglia:** Il framework delle **Collections** (Liste, Mappe, Set -> es. `ArrayList`, `HashMap`).
   - **Cos'è:** È il metodo universale per chiedere a strutture dati dinamiche (che si allargano e restringono a runtime) quanti elementi ospitano in quel preciso istante.
   - **Esempio:** `int numeroInvitati = listaInvitati.size();`

*(Nota a margine: non esiste un metodo standard universale `getLength()` nelle strutture base di Java. Incontri `getLength()` solo in librerie specifiche e molto settoriali, come ad esempio le `NodeList` quando fai il parsing dei file XML (DOM)!).*

---

## 7. Numeri: divisione fra interi, cast e formato di stampa

### La divisione fra interi tronca
Se **entrambi** gli operandi sono `int`, il risultato è un `int`: la parte decimale sparisce **prima** di qualunque conversione. Mettere il risultato in un `double` non la fa tornare.

```java
public class Numeri {
    public static void main(String[] args) {
        int somma = 55;
        int quanti = 2;
        double sbagliata = somma / quanti;           // int / int = 27, poi promosso a 27.0
        double giusta = (double) somma / quanti;     // 27.5
        double giusta2 = somma / 2.0;                // basta UN operando double
        System.out.println(sbagliata + " " + giusta + " " + giusta2);   // 27.0 27.5 27.5

        // (double) davanti a una PARENTESI converte il risultato, quando la divisione è già avvenuta
        System.out.println((double) (somma / quanti));   // 27.0
    }
}
```

**Il sintomo:** una media o una percentuale esce tonda (`27.0`) quando non dovrebbe. Il colpevole è quasi sempre `somma / contatore` con due `int`. Il cast va sul **primo operando**, `(double) somma / quanti`, non sul risultato.

### Da `String` a numero: si parsa, non si fa il cast
`(double) words[1]` con `words[1]` `String` **non compila** (`incompatible types: String cannot be converted to double`): una `String` e un numero non sono tipi imparentati, il cast non converte. Si usa `Integer.parseInt("42")` o `Double.parseDouble("2.5")`; su testo non numerico lanciano `NumberFormatException` (non controllata). Se i dati arrivano da `split`, ricordati `trim()`: `Double.parseDouble(w[1].trim())`.

### Formattare un `double`: la traccia ti mostra il formato
| Scrivo | Stampa per `18.5` | Quando |
|---|---|---|
| `"" + t` oppure `String.valueOf(t)` | `18.5` | la traccia mostra il valore "come viene" (`18.5`, `24.0`) |
| `String.format("%.2f", t)` | `18,50` (locale italiano) o `18.50` | la traccia mostra **sempre** due decimali |
| `String.format(Locale.US, "%.2f", t)` | `18.50` | due decimali con il **punto**, a prescindere dal computer |
| `Math.round(t * 100) / 100.0` | `18.5` | arrotondare a due decimali **restando** un `double` |

`%.2f` mette **sempre** due decimali e, su una JVM con locale italiano, la **virgola**: se la traccia scrive `Messina, ore 8: 18.5`, `%.2f` produce `18,50` e il confronto fallisce. Regola: **guarda l'esempio di output della traccia, carattere per carattere**, e scegli la forma che lo riproduce. Un `double` concatenato mostra sempre almeno un decimale (`24.0`, non `24`).

---

## 8. Casi limite: la lista da controllare prima di consegnare

Un metodo che funziona sull'esempio della traccia può sbagliare su un caso che il test nascosto prova di sicuro. Prima di consegnare un metodo che lavora su dati, passa questi casi, uno per uno:

| Caso | Cosa va storto | Come si scrive |
|---|---|---|
| **`null`** | `NullPointerException` se chiami un metodo sul `null` | il controllo `x == null` va **per primo**: `if (v == null \|\| v.size() == 0)`, mai al contrario |
| **vuoto** (`""`, array di lunghezza 0, lista vuota) | `v[0]` fuori dai limiti; un ciclo che non gira | decidi cosa restituire **prima** di accedere a `v[0]` |
| **un solo elemento** | `if (length > 1) ... else return 0` scarta un array che ha un massimo ben definito | l'array di un elemento ha massimo, minimo e media: sé stesso |
| **tutti negativi** | `int max = 0;` restituisce `0`, che non è nell'array | si parte dal **primo elemento**: `int max = v[0];` e il ciclo da `i = 1` |
| **tutti uguali** | "il secondo massimo" non esiste se lo cerchi con `>` stretto | leggi la traccia: spesso "coincide con il massimo" |
| **soli spazi** (`"   "`) | `length() == 0` non li rifiuta | `s.trim().isEmpty()` |
| **riga vuota in un file** | `riga.charAt(0)` lancia `StringIndexOutOfBoundsException` | `riga.startsWith("#")`, che su `""` dà `false` |
| **estremi** (incluso o escluso) | `i <= fine` invece di `i < fine` | la traccia dice "estremo escluso": `<` |

```java
public class CasiLimite {
    // massimo: si parte dal PRIMO elemento, non da 0 e non da un valore inventato
    static int massimo(int[] v) {
        int max = v[0];
        for (int i = 1; i < v.length; i++) {
            if (v[i] > max) max = v[i];
        }
        return max;
    }

    // controllo null PRIMA di ogni altra cosa sull'oggetto
    static int contaVuote(String[] righe) {
        if (righe == null) {
            throw new IllegalArgumentException("righe null");
        }
        int n = 0;
        for (String r : righe) {
            if (r.trim().isEmpty()) n++;     // "" e "   " sono entrambe vuote
        }
        return n;
    }

    public static void main(String[] args) {
        System.out.println(massimo(new int[]{-5, -2, -9}));                  // -2
        System.out.println(massimo(new int[]{42}));                          // 42
        System.out.println(contaVuote(new String[]{"a", "", "   ", "b"}));   // 2

        String riga = "";
        System.out.println(riga.startsWith("#"));                            // false, nessuna eccezione
        // riga.charAt(0) qui lancerebbe StringIndexOutOfBoundsException

        System.out.println("".split(" ").length);                            // 1: un elemento, la stringa vuota
        System.out.println("a  b".split(" ").length);                        // 3: c'è un elemento vuoto in mezzo
        System.out.println("a  b".split(" +").length);                       // 2: " +" = uno o più spazi
    }
}
```

Due note su `split`. `split(" ")` su due spazi di fila produce un elemento **vuoto** in mezzo; per "uno o più spazi" si usa `split(" +")`. E "numero di parole = numero di spazi + 1" vale solo con **uno** spazio fra le parole e senza spazi in testa o in coda: altrimenti conviene `trim()` e poi `split`.

**Quando lanci un'eccezione per input non valido** controlla *prima* di fare qualunque altra cosa, con `throw new IllegalArgumentException("messaggio")`: la `new` e le parentesi non si dimenticano (`throw NullPointerException;` non compila). E distingui `null` da vuoto: se la traccia dice "se la lista è `null`", una lista vuota **non** è `null` e va trattata normalmente.

---

## 9. La forma dell'appello: un file, solo classi

All'appello scrivi in un'area di testo, **tutte le classi di un esercizio in un unico file**, senza nessun controllo di sintassi. La forma conta quanto la logica.

### Regole di forma
1. **In un file Java esistono solo classi, interfacce ed enum.** Metodi e variabili stanno **dentro** una classe, mai al primo livello. Un metodo statico "scritto per conto suo" non compila: la prima riga di ogni esercizio che chiede un metodo è `class Convertitore {` (o il nome che la traccia dà). Su Java recenti l'errore è `compact source file does not have main method`, su quelli precedenti `class, interface, enum, or record expected`: stessa causa.
2. **Nessuna classe `public`**, salvo al più una che abbia il nome del file. Con più classi nello stesso file e una `public class Altro`, il compilatore risponde `class Altro is public, should be declared in a file named Altro.java`. Si scrive `class Altro { ... }` e basta. (Gli esempi di questi appunti sono file a sé stanti, ognuno con la sua `public class` e il suo `main`: all'appello, invece, tutto sta in un file solo e senza `public`.)
3. **I nomi della traccia si copiano.** Classe, metodo, parametri, messaggi di errore, formato di stampa: sono verificati lettera per lettera. `Operario` per `Operaio` o `aggiung` per `aggiungi` falliscono: con il test già compilato dopo che il tuo file compila (`NoClassDefFoundError`, `NoSuchMethodError` a runtime), con le classi nello stesso file direttamente in compilazione (`cannot find symbol`).
4. **Il primo `Esegui` entro cinque minuti.** Anche sulla prima classe, anche a metà: un run di compilazione ti dice in un secondo cosa ti avrebbe fatto perdere punti alla fine.

### I messaggi del compilatore, e cosa significano davvero
| Messaggio | Cosa è successo |
|---|---|
| `';' expected` | manca un `;`, o c'è una `,` dove ci voleva (`for (i = 0; i < n, i++)`) |
| `missing return statement` | un metodo con tipo di ritorno non restituisce su **ogni** strada (ramo `catch`, `else` mancante) |
| `variable x might not have been initialized` | una variabile **locale** non parte da zero da sola (i campi sì): `int somma = 0;` |
| `incompatible types: possible lossy conversion from double to int` | stai mettendo un `double` in un `int` (spesso un getter dichiarato `int` su un campo `double`) |
| `incompatible types: String cannot be converted to int` | serve `Integer.parseInt`, non un cast |
| `cannot find symbol` | nome che non esiste: refuso (`getOutpustStream`), nome inventato (`exists()` su `FileReader`, `Map.getValue`), variabile fuori scope, classe non scritta. Guarda la riga `symbol:` sotto |
| `array required, but String found` | hai scritto `s[0]` su una `String`: `s.charAt(0)` |
| `unclosed string literal` | virgolette non chiuse |
| `int cannot be dereferenced` | un metodo chiamato su un tipo primitivo (`x.foo()` con `x` `int`) |
| `non-static variable g cannot be referenced from a static context` | un metodo `static` che usa un campo d'istanza |
| `unreported exception X; must be caught or declared to be thrown` | manca `throws X` o `catch`: vedi Livello 3 §5 |
| `exception X is never thrown in body of corresponding try statement` | un `catch (X)` su un `try` che nessuno fa lanciare X: vedi Livello 3 §5 |

Il compilatore segnala la **riga e la colonna** (`^`): leggi la riga indicata **e quella prima**, perché un `;` mancante viene scoperto alla riga successiva.

### Checklist di 60 secondi prima di ogni Esegui
- ogni metodo ha **tipo di ritorno e `()`**;
- ogni `for` ha **due** `;`, ogni `if`/`while` le sue parentesi, ogni `{` la sua `}`;
- ogni stringa ha **due virgolette**;
- ogni nome che compare nella traccia (classe, metodo, messaggio, formato) è **copiato**, non riscritto;
- ogni variabile locale ha un **valore iniziale**;
- ogni nome di API lo scrivi come in un esempio che hai davanti: `getOutputStream`, `readLine`, `writeDouble`, `InterruptedException` (se non ricordi, apri l'esempio);
- ogni classe ha **`class`** davanti e nessuna è `public`.

