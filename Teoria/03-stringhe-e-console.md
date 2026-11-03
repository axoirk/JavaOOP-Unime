---
materia: Programmazione a Oggetti
capitolo: 3
titolo: Stringhe e input/output da console
livello_syllabus: 1
stato: completo
slide: ["Savitch cap. 2 slide 65-92", "Savitch cap. 3 slide 35-42", "Savitch cap. 5 slide 15-18", "Savitch cap. 14 slide 26-27"]
appelli: []
fonti_esterne: 6
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 3 — Stringhe e input/output da console

## Di cosa parla questo capitolo

Fino a qui i nostri programmi hanno maneggiato numeri, caratteri e valori di verità. Ma quasi ogni programma vero lavora anche con il **testo**: nomi, frasi, righe lette da un file, messaggi da mostrare. In Java il testo si rappresenta con la classe `String`, e questo capitolo la affronta da due lati. Il primo è la **stringa come dato**: come si scrive, si concatena, si misura, si taglia, si confronta, si divide in pezzi. Il secondo è la **stringa come mezzo di comunicazione con l'utente**: come si stampa sullo schermo e come si legge dalla tastiera con `Scanner`.

Il capitolo riprende le variabili e gli operatori del [Capitolo 2 — Tipi primitivi, variabili e operatori](02-tipi-variabili-operatori.md), dove avevamo incontrato `String` solo di sfuggita, e il `main` con `System.out.println` e `Scanner` del [Capitolo 1 — Java e la JVM](01-java-e-la-jvm.md). La novità concettuale è che `String` **non è un tipo primitivo**: è una classe, e un valore di tipo `String` è un **oggetto**, cioè qualcosa che ha dei metodi da chiamare con il punto (`s.length()`). Da questa differenza discendono quasi tutte le trappole del capitolo: il confronto con `==`, l'immutabilità, il valore `null`.

Alla fine del capitolo saprai scrivere e concatenare stringhe prevedendo il risultato, usare i metodi più comuni della classe `String` con la firma esatta e sapendo quando sollevano un'eccezione, confrontare due stringhe nel modo giusto, spezzare una riga di testo con `split`, formattare l'output con `printf` e `String.format`, e leggere dati dalla tastiera con `Scanner` senza cadere nella trappola di `nextLine` dopo `nextInt`.

> [!NOTE]
> **Sull'uso nei programmi d'esame**
> Le prove scritte descritte nell'[indice](_indice.md) hanno un output fisso, verificato da un test, e nelle tracce degli appelli ufficiali l'input da tastiera non compare. L'input con `Scanner` serve quindi soprattutto a capire il linguaggio e a scrivere programmi di prova; i **metodi di `String`**, invece, sono strumenti di tutti i giorni (elaborare righe di testo, costruire i messaggi da stampare), e il **formato dell'output** è proprio ciò che il test confronta carattere per carattere (sezione 3.6).

## 3.1 La classe `String`

### 3.1.1 Una stringa è un oggetto

Una **stringa** è una sequenza di caratteri trattata come un unico valore. Nel [Capitolo 2](02-tipi-variabili-operatori.md) abbiamo visto che un testo tra virgolette doppie, come `"Enter a whole number from 1 to 99."`, è un letterale. Ora aggiungiamo che il suo tipo è `String`, una classe della libreria standard che sta nel package `java.lang`, il quale Java importa automaticamente: non serve nessun `import`.

Si può dichiarare una variabile di tipo `String` e assegnarle un valore in più modi equivalenti:

```java
public class Saluto {
    public static void main(String[] args) {
        String greeting;                         // dichiarazione
        greeting = "Hello!";                     // assegnamento di un letterale
        String other = "Hi!";                    // dichiarazione e assegnamento insieme
        String third = new String("Hey!");       // creazione esplicita di un oggetto
        System.out.println(greeting);
        System.out.println(other);
        System.out.println(third);
    }
}
```

L'output è:

```text
Hello!
Hi!
Hey!
```

Riga per riga. `String greeting;` crea una variabile capace di *riferirsi* a una stringa, ma ancora senza valore. `greeting = "Hello!";` le assegna il letterale. `String other = "Hi!";` fa le due cose in un colpo solo ed è la forma che useremo quasi sempre. `new String("Hey!")` crea esplicitamente un nuovo oggetto `String` con quel contenuto: è corretta e funziona, ma è più lunga e, come vedremo nella sezione 3.4, ha una conseguenza sul confronto. Per scrivere una stringa basta il letterale.

> [!TIP]
> **Intuizione — Primitivi e oggetti**
> Un `int` è un valore: la variabile *contiene* il numero. Una `String` è un oggetto: la variabile contiene un **riferimento** (un indirizzo) all'oggetto, che vive altrove in memoria. Ci vorrà il [Capitolo 8](08-riferimenti-e-memoria.md) per raccontarlo bene; per ora basta ricordare che un oggetto ha dei **metodi** (si scrivono dopo il punto: `greeting.length()`) e che un tipo classe si scrive con l'iniziale **maiuscola**, `String`, mentre i primitivi sono minuscoli (`int`).

Una variabile `String` può anche non riferirsi a nessun oggetto: in tal caso vale `null`. Lo vediamo nella sezione 3.1.5.

### 3.1.2 La concatenazione con `+`

Per unire due stringhe in una sola si usa l'operatore `+`, che con le stringhe si chiama **concatenazione**. Si possono concatenare quante stringhe si vuole, e il risultato è una **nuova** stringa:

```java
public class Concatenazione {
    public static void main(String[] args) {
        String name = "Ada";
        int age = 36;
        double height = 1.7;
        char initial = 'A';
        boolean ok = true;
        String sentence = "Name: " + name + ", age: " + age + ", height: " + height;
        System.out.println(sentence);
        System.out.println("Initial " + initial + ", ok? " + ok);
        System.out.println("The answer is " + 42);
        String text = "ab";
        text += "cd";
        text += 5;
        System.out.println(text);
    }
}
```

L'output è:

```text
Name: Ada, age: 36, height: 1.7
Initial A, ok? true
The answer is 42
abcd5
```

Quando uno degli operandi di `+` è una stringa e l'altro no, Java **converte l'altro operando in stringa** (un `int` nella sua scrittura decimale, un `double` con la virgola, un `char` nel carattere stesso, un `boolean` in `true` o `false`) e poi concatena. Per questo `"The answer is " + 42` dà `"The answer is 42"`. L'operatore composto `+=` funziona come con i numeri: `text += "cd"` equivale a `text = text + "cd"`. Se l'operando non stringa è `null`, la conversione dà la scritta `"null"`.

> [!WARNING]
> **Attenzione — `+` si valuta da sinistra a destra**
> Il `+` ha due significati, somma e concatenazione, e quale dei due scatta dipende dai tipi degli operandi *a ogni passo*, procedendo da sinistra (gli operatori `+` hanno la stessa precedenza e si associano da sinistra, [Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.5.4). Il risultato può sorprendere:
> ```java
> System.out.println("a" + 1 + 2);       // a12   : prima "a" + 1 = "a1", poi "a1" + 2
> System.out.println(1 + 2 + "a");       // 3a    : prima 1 + 2 = 3, poi 3 + "a"
> System.out.println("a" + (1 + 2));     // a3    : le parentesi forzano la somma
> System.out.println('a' + 'b' + "c");   // 195c  : 'a' + 'b' sono due char, si sommano come numeri (97 + 98)
> System.out.println("" + 'a' + 'b');    // ab    : partendo da una stringa, tutto è concatenazione
> ```
> Se vuoi la somma dentro un testo, metti le parentesi; se vuoi concatenare dei `char` come testo, parti da una stringa (anche vuota).

Un'ultima regola pratica, che le slide ricordano: se un'istruzione è troppo lunga per stare su una riga, puoi andare a capo **solo subito prima o subito dopo l'operatore `+`**, mai dentro un letterale tra virgolette (un letterale `String` deve chiudersi sulla stessa riga in cui si apre).

```java
System.out.println("Lucky number = " + 13
                   + ", secret number = " + 42);
```

### 3.1.3 Lunghezza e indici

Una stringa è una sequenza ordinata di caratteri, e ogni carattere ha una **posizione**, detta **indice** (*index*). Gli indici partono da **0**, non da 1: nella stringa `"Java is fun."` il carattere `'J'` è in posizione 0, il primo `'a'` in posizione 1, e così via. Contando anche gli spazi e il punto finale:

```text
posizione:  0 1 2 3 4 5 6 7 8 9 10 11
carattere:  J a v a   i s   f u n  .
```

La `'f'` di "fun" sta quindi in posizione 8. I due metodi di base sono:

```text
public int  length()            // il numero di caratteri
public char charAt(int index)   // il carattere in posizione index
```

`length()` restituisce un `int` e si può usare ovunque serva un `int`: `int count = command.length();`, `"Length is " + command.length()`, `command.length() + 3`. `charAt(i)` restituisce un `char`. Poiché gli indici partono da 0, l'**ultimo** carattere è in posizione `length() - 1`:

```java
public class Posizioni {
    public static void main(String[] args) {
        String s = "Java is fun.";
        System.out.println(s.length());                // 12
        System.out.println(s.charAt(0));               // J
        System.out.println(s.charAt(8));               // f
        System.out.println(s.charAt(s.length() - 1));  // .
    }
}
```

L'output è:

```text
12
J
f
.
```

Se si chiede un indice che non esiste, cioè negativo oppure maggiore o uguale a `length()`, il programma si ferma con un'eccezione `StringIndexOutOfBoundsException` (una sottoclasse di `IndexOutOfBoundsException`, che è l'eccezione dichiarata dalla documentazione). Nel [Capitolo 13](13-eccezioni.md) vedremo le eccezioni nel dettaglio; per ora ricorda che `s.charAt(s.length())` è **sempre** un errore, perché l'ultimo indice valido è `s.length() - 1`.

> [!WARNING]
> **Attenzione — `length()`, `length`, `size()`**
> Tre strumenti diversi per tre cose diverse, che si confondono spesso. Per una **stringa** si scrive `s.length()` (metodo, con le parentesi). Per un **array** si scrive `a.length` (campo, *senza* parentesi, [Capitolo 5](05-array-e-matrici.md)). Per una **collezione** come `ArrayList` si scrive `list.size()` ([Capitolo 12](12-generics-e-collezioni.md)). Scrivere `s.length` su una stringa, o `a.length()` su un array, è un errore di compilazione (`cannot find symbol`). E poiché una stringa non è un array, `s[0]` non si può scrivere: si usa `s.charAt(0)`.

Un esempio tipico è scorrere tutta la stringa un carattere alla volta, qui per contare quante volte compare una lettera. Il ciclo `for` verrà spiegato nel [Capitolo 4](04-strutture-di-controllo.md): per ora leggilo come "per `i` che va da 0 fino a `length() - 1`".

#### Esempio — Contare un carattere

```java
public class ContaCaratteri {
    public static void main(String[] args) {
        String text = "banana";
        int count = 0;
        for (int i = 0; i < text.length(); i++) {   // i = 0, 1, ..., length() - 1
            if (text.charAt(i) == 'a') {            // char confrontato con un char
                count++;
            }
        }
        System.out.println(count);
    }
}
```

L'output è `3`. La condizione del `for` usa `<` e non `<=`: con `i <= text.length()` l'ultimo giro chiamerebbe `text.charAt(6)`, fuori dai limiti, e il programma terminerebbe con `StringIndexOutOfBoundsException`. Il confronto `text.charAt(i) == 'a'` è lecito perché `charAt` restituisce un `char` e `==` va bene per i caratteri ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.7.2).

### 3.1.4 Le stringhe sono immutabili

Ecco una proprietà fondamentale: **nessun metodo di `String` modifica la stringa su cui viene chiamato**. Un oggetto `String` non cambia mai il proprio contenuto dopo essere stato creato: si dice **immutabile**. I metodi che sembrano "modificare" (`toUpperCase`, `trim`, `replace`, `substring`…) in realtà **restituiscono una nuova stringa**, lasciando intatta quella originale.

```java
public class Immutabile {
    public static void main(String[] args) {
        String word = "java";
        word.toUpperCase();                  // il risultato viene buttato via
        System.out.println(word);            // java
        String big = word.toUpperCase();     // il risultato va salvato in una variabile
        System.out.println(big);             // JAVA
        System.out.println(word);            // java: l'oggetto originale non è cambiato
        word = word.toUpperCase();           // si cambia la variabile, non l'oggetto
        System.out.println(word);            // JAVA
    }
}
```

L'output è:

```text
java
JAVA
java
JAVA
```

La seconda riga, `word.toUpperCase();`, compila e gira senza errori ma non serve a niente: la nuova stringa `"JAVA"` viene creata e subito dimenticata. Alla quarta istruzione cambia il valore della **variabile** `word`, che ora si riferisce a un altro oggetto; l'oggetto `"java"` non è stato toccato.

> [!TIP]
> **Intuizione — La variabile è un'etichetta, la stringa è incisa**
> Pensa a una stringa come a una frase incisa nella pietra: non la puoi correggere, puoi solo incidere una frase nuova. La variabile è un'etichetta che puoi staccare dalla pietra vecchia e attaccare a quella nuova. L'analogia regge finché si parla di stringhe; per altri oggetti (che invece si possono modificare) vedremo che il discorso cambia.

### 3.1.5 La stringa vuota e `null`

Una stringa può avere un numero qualsiasi di caratteri, **zero compreso**. La stringa con zero caratteri si chiama **stringa vuota** e si scrive `""`. È un oggetto a tutti gli effetti, con `length()` uguale a 0.

Da non confondere con `null`, che significa invece "questa variabile non si riferisce a **nessun** oggetto". Sulla stringa vuota si possono chiamare i metodi; su `null` no, e provarci provoca una `NullPointerException`.

```java
public class Vuote {
    public static void main(String[] args) {
        String empty = "";
        String spaces = "   ";
        String nothing = null;
        System.out.println(empty.length());            // 0
        System.out.println(spaces.length());           // 3
        System.out.println(empty.isEmpty());           // true
        System.out.println(spaces.isEmpty());          // false: contiene tre spazi
        System.out.println(spaces.trim().isEmpty());   // true: dopo trim() non resta nulla
        System.out.println(nothing == null);           // true
        System.out.println("x" + nothing);             // xnull
    }
}
```

L'output è:

```text
0
3
true
false
true
true
xnull
```

Il metodo `isEmpty()` è vero se e solo se `length()` è 0. Una stringa fatta di soli spazi **non** è vuota: per accorgersene si toglie prima lo spazio con `trim()` (sezione 3.2). L'ultima riga mostra che `null` non provoca errori nella concatenazione (diventa la scritta `null`); un errore c'è invece se si scrive `nothing.length()`: lo vedremo tra gli errori tipici.

La stringa vuota è utile in pratica: come punto di partenza per costruire una stringa pezzo per pezzo (`String result = "";` e poi `result += ...`), o come risultato di "non c'era niente da dire".

## 3.2 I metodi più usati

Oltre a `length` e `charAt`, la classe `String` offre molti metodi. Ecco quelli che servono più spesso, con la firma esatta così come compare nella documentazione.

| Metodo | Cosa fa | Esempio con `s = "banana"` |
|---|---|---|
| `int length()` | numero di caratteri | `s.length()` → `6` |
| `char charAt(int index)` | carattere in posizione `index` | `s.charAt(1)` → `'a'` |
| `String substring(int beginIndex)` | dalla posizione `beginIndex` (inclusa) fino alla fine | `s.substring(2)` → `"nana"` |
| `String substring(int beginIndex, int endIndex)` | da `beginIndex` (inclusa) a `endIndex` (**esclusa**) | `s.substring(1, 4)` → `"ana"` |
| `int indexOf(String str)` | posizione della prima occorrenza di `str`, oppure `-1` | `s.indexOf("na")` → `2` |
| `int indexOf(int ch)` | posizione della prima occorrenza del carattere `ch`, oppure `-1` | `s.indexOf('a')` → `1` |
| `int indexOf(int ch, int fromIndex)` | come sopra, cercando a partire da `fromIndex` | `s.indexOf('a', 2)` → `3` |
| `int lastIndexOf(int ch)` | posizione dell'**ultima** occorrenza di `ch`, oppure `-1` | `s.lastIndexOf('a')` → `5` |
| `boolean contains(CharSequence s)` | vero se contiene la sequenza data | `s.contains("nan")` → `true` |
| `boolean startsWith(String prefix)` | vero se inizia con `prefix` | `s.startsWith("ban")` → `true` |
| `boolean endsWith(String suffix)` | vero se finisce con `suffix` | `s.endsWith("na")` → `true` |
| `String toUpperCase()` | tutte maiuscole | `s.toUpperCase()` → `"BANANA"` |
| `String toLowerCase()` | tutte minuscole | `"Ab".toLowerCase()` → `"ab"` |
| `String trim()` | toglie gli spazi iniziali e finali | `"  ab ".trim()` → `"ab"` |
| `String replace(char oldChar, char newChar)` | sostituisce ogni `oldChar` con `newChar` | `s.replace('a', 'o')` → `"bonono"` |
| `String replace(CharSequence target, CharSequence replacement)` | sostituisce ogni occorrenza di una sequenza | `s.replace("an", "AN")` → `"bANANa"` |
| `boolean isEmpty()` | vero se `length()` è 0 | `"".isEmpty()` → `true` |

Alcune note sulla tabella, che evitano gli errori più comuni.

- **`substring` e l'estremo escluso.** `substring(inizio, fine)` prende i caratteri da `inizio` fino a `fine - 1`: la lunghezza del risultato è `fine - inizio`. Con `"banana".substring(1, 4)` si prendono le posizioni 1, 2 e 3, cioè `"ana"`. `substring(n)` con `n` uguale a `length()` dà la stringa vuota; con `n` maggiore di `length()`, oppure con indici negativi o `inizio > fine`, solleva `StringIndexOutOfBoundsException` (anch'essa figlia di `IndexOutOfBoundsException`).
- **`indexOf` e `-1`.** Se ciò che cerchi non c'è, il risultato è `-1`: un valore che non è un indice valido, e che va controllato prima di usarlo come posizione.
- **`indexOf(int ch)` prende un `int`.** Funziona anche passando un `char`, perché un `char` si promuove automaticamente a `int` ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.6.2): `s.indexOf('a')` è corretto.
- **I metodi non modificano la stringa** (sezione 3.1.4): `s.toUpperCase()` restituisce una stringa nuova, e se non la si salva è lavoro buttato.
- **`trim()`** toglie i caratteri il cui codice è minore o uguale a quello dello spazio (quindi anche tabulazioni e a capo), ma solo agli estremi, non dentro il testo.

> [!NOTE]
> **Approfondimento esterno — La classe `String` nella documentazione**
> Le firme precedenti sono quelle della classe `java.lang.String`. Alcuni dettagli utili che la documentazione precisa:
> - `charAt(int index)` e `substring(...)` dichiarano `IndexOutOfBoundsException`; in esecuzione il tipo effettivamente lanciato è la sottoclasse `StringIndexOutOfBoundsException`.
> - `trim()` rimuove i caratteri con codice `U+0020` (lo spazio) o inferiore, agli estremi.
> - `isEmpty()` esiste dalla versione 1.6 di Java. Dalla versione 11 esistono anche `boolean isBlank()` (vero se la stringa è vuota **o contiene solo spazi bianchi**) e `String strip()` (come `trim()`, ma sui veri spazi bianchi Unicode); le slide non le presentano e negli esempi di questi appunti si usa la forma classica `s.trim().isEmpty()`.
> - `String.valueOf(...)` è un metodo **statico** che converte in stringa un valore di qualunque tipo primitivo o un oggetto: `String.valueOf(3.0)` dà `"3.0"`.
> *Fonte:* [Class String (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html)

#### Esempio — Un tour dei metodi

```java
public class TourMetodi {
    public static void main(String[] args) {
        String s = "  Java is fun.  ";
        String t = s.trim();                           // "Java is fun."
        System.out.println("[" + t + "]");
        System.out.println(t.substring(5));            // is fun.
        System.out.println(t.substring(5, 7));         // is
        System.out.println(t.indexOf("is"));           // 5
        System.out.println(t.indexOf("xyz"));          // -1
        System.out.println(t.contains("fun"));         // true
        System.out.println(t.startsWith("Java"));      // true
        System.out.println(t.endsWith("fun"));         // false: finisce con il punto
        System.out.println(t.toUpperCase());           // JAVA IS FUN.
        System.out.println(t.replace('a', 'o'));       // Jovo is fun.
        System.out.println(t.replace("fun", "cool"));  // Java is cool.
        String b = "banana";
        System.out.println(b.indexOf('a'));            // 1
        System.out.println(b.indexOf('a', 2));         // 3
        System.out.println(b.lastIndexOf('a'));        // 5
        System.out.println(String.valueOf(3.0) + String.valueOf(true));  // 3.0true
    }
}
```

L'output è:

```text
[Java is fun.]
is fun.
is
5
-1
true
true
false
JAVA IS FUN.
Jovo is fun.
Java is cool.
1
3
5
3.0true
```

Alcuni passaggi da seguire con la tabella degli indici: in `"Java is fun."` la "i" di "is" è in posizione 5, quindi `substring(5)` parte da lì e `substring(5, 7)` prende le posizioni 5 e 6, cioè `"is"`. `t.endsWith("fun")` è falso perché la stringa finisce con `"fun."`, punto compreso.

#### Esempio — Dividere un nome di file in nome ed estensione

Un uso classico di `lastIndexOf` e `substring`: trovare l'ultimo punto e tagliare prima e dopo.

```java
public class NomeFile {
    public static void main(String[] args) {
        String file = "relazione.finale.pdf";
        int dot = file.lastIndexOf('.');             // posizione dell'ULTIMO punto: 16
        String base = file.substring(0, dot);        // da 0 a dot - 1
        String ext = file.substring(dot + 1);        // da dot + 1 fino alla fine
        System.out.println(base);
        System.out.println(ext);
        System.out.println("README".lastIndexOf('.'));   // senza punto: -1
    }
}
```

L'output è:

```text
relazione.finale
pdf
-1
```

Si usa `lastIndexOf` e non `indexOf` perché il nome contiene due punti e interessa l'estensione, cioè quello che sta dopo l'**ultimo**. `substring(0, dot)` esclude il punto (l'estremo finale è escluso) e `substring(dot + 1)` parte dal carattere dopo il punto. Il terzo caso mostra che, se manca il punto, `lastIndexOf` dà `-1`: un programma completo dovrebbe controllare `dot >= 0` prima di tagliare, altrimenti `substring(0, -1)` solleverebbe un'eccezione.

#### Esempio — Le iniziali di un nome

```java
public class Iniziali {
    public static void main(String[] args) {
        String full = "Ada Lovelace";
        int space = full.indexOf(' ');
        String initials = "" + full.charAt(0) + full.charAt(space + 1);
        System.out.println(initials);
    }
}
```

L'output è `AL`. `indexOf(' ')` trova lo spazio (posizione 3); il carattere dopo (posizione 4) è la `'L'` di "Lovelace". L'espressione parte da `""` proprio per quanto detto nella sezione 3.1.2: `full.charAt(0) + full.charAt(space + 1)` da sola sommerebbe due `char` come numeri (65 + 76 = 141).

## 3.3 Sequenze di escape e Unicode

### 3.3.1 Le sequenze di escape

Come stampare la frase `"Java" refers to a language.`, con le virgolette comprese? Se scriviamo `System.out.println(""Java" refers...");` il compilatore vede una stringa vuota `""` seguita da `Java`, e si confonde. Bisogna dirgli che quelle virgolette non chiudono il letterale ma fanno **parte del testo**. Si usa il carattere **backslash** `\` davanti: una **sequenza di escape** è un backslash seguito da un carattere, e **rappresenta un solo carattere**, anche se nel sorgente ne servono due.

```java
System.out.println("\"Java\" refers to a language.");
```

Le sequenze di escape principali sono:

| Sequenza | Carattere rappresentato |
|---|---|
| `\"` | virgolette doppie |
| `\'` | apice singolo |
| `\\` | backslash |
| `\n` | a capo (*newline*, "line feed") |
| `\r` | ritorno carrello (*carriage return*) |
| `\t` | tabulazione orizzontale |
| `\b` | backspace |
| `\f` | avanzamento pagina (*form feed*) |

> [!NOTE]
> **Approfondimento esterno — Le sequenze di escape**
> La documentazione di `String.translateEscapes()` elenca tutte le sequenze riconosciute in un letterale: `\b` (backspace, `U+0008`), `\t` (tabulazione, `U+0009`), `\n` (a capo, `U+000A`), `\f` (form feed, `U+000C`), `\r` (ritorno carrello, `U+000D`), `\s` (spazio, `U+0020`), `\"`, `\'`, `\\`, oltre alle sequenze ottali da `\0` a `\377`. La stessa pagina precisa che le sequenze Unicode come `\u2022` **non** sono sequenze di escape in senso stretto: le traduce il compilatore quando legge il sorgente.
> *Fonte:* [String.translateEscapes() (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html#translateEscapes())

```java
public class Escape {
    public static void main(String[] args) {
        System.out.println("\"Java\" refers to a language.");
        System.out.println("abc\\def");
        System.out.println("new\nline");
        System.out.println("col1\tcol2");
        char singleQuote = '\'';
        System.out.println(singleQuote);
        System.out.println("It's fine without escape");
        char doubleQuote = '"';
        System.out.println(doubleQuote);
        System.out.println("a\nb".length());
        System.out.println("C:\\dati\\file.txt");
    }
}
```

L'output è (il carattere di tabulazione è reso con uno spazio largo):

```text
"Java" refers to a language.
abc\def
new
line
col1	col2
'
It's fine without escape
"
3
C:\dati\file.txt
```

Spiegazione. Il backslash è il carattere che *introduce* un escape, quindi per stamparne uno vero bisogna raddoppiarlo: `"abc\\def"` stampa `abc\def`, e un percorso come `C:\dati` si scrive `"C:\\dati"`. `\n` manda a capo, e infatti `"new\nline"` occupa due righe. Dentro un letterale `String` l'apice singolo non ha bisogno di escape (`"It's fine"`), così come nei letterali `char` le virgolette doppie non ne hanno bisogno (`'"'`); servono invece `'\''` per il carattere apice e `\"` per le virgolette dentro una stringa. L'ultima riga conferma che ogni sequenza è **un carattere**: `"a\nb"` è fatta di tre caratteri (`a`, a capo, `b`), non di quattro.

Non confondere `\n` con `println`: `println` stampa il testo **e poi** va a capo, mentre `\n` è un carattere che si può mettere ovunque nel testo, anche con `print`.

### 3.3.2 Unicode

Per rappresentare i caratteri come numeri serve un **codice**. Molti linguaggi usano ASCII, che copre l'alfabeto inglese, le cifre e i simboli più comuni. Java usa invece **Unicode**, un codice molto più ampio che **include ASCII** e contiene anche lettere di molti altri alfabeti (accentate, greche, cirilliche, ideogrammi…). Per questo un `char` occupa 16 bit ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.2.4). Un carattere si può scrivere anche tramite il suo codice con la forma `\uXXXX` (quattro cifre esadecimali): `"\u0041"` è la stringa `"A"`, e `"\u00e8"` è `"è"`.

Per i programmi di questo corso basta ricordare che i caratteri accentati si possono usare normalmente; se il terminale non è configurato per la stessa codifica del programma, possono comparire stampati male, ma il programma è corretto.

## 3.4 Confrontare stringhe

### 3.4.1 `==` contro `equals`

Abbiamo già visto ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.7.2) che `==` va bene per interi e caratteri e non per i numeri in virgola mobile. Per gli **oggetti**, e quindi per le stringhe, c'è un altro problema: `s1 == s2` non confronta il testo, ma controlla se le due variabili si riferiscono **allo stesso oggetto**, cioè alla stessa posizione di memoria. Due stringhe con lo stesso identico contenuto ma create separatamente sono due oggetti diversi, e per `==` sono diverse.

Per confrontare il **contenuto** si usa il metodo `equals`:

```text
public boolean equals(Object anObject)
public boolean equalsIgnoreCase(String anotherString)
```

`s1.equals(s2)` (o `s2.equals(s1)`) è vero se le due stringhe hanno gli stessi caratteri nello stesso ordine. `equalsIgnoreCase` fa lo stesso **ignorando la differenza fra maiuscole e minuscole**: `"Hello".equalsIgnoreCase("hello")` è `true`, mentre `"Hello".equals("hello")` è `false`.

```java
public class Uguaglianza {
    public static void main(String[] args) {
        String s1 = new String("Java");
        String s2 = new String("Java");
        System.out.println(s1 == s2);                          // false: due oggetti distinti
        System.out.println(s1.equals(s2));                     // true: stesso contenuto
        System.out.println("Hello".equalsIgnoreCase("hello")); // true
        System.out.println("Hello".equals("hello"));           // false
        String a = "Java";
        String b = "Java";
        System.out.println(a == b);                            // true, ma non ci si può contare
        String nothing = null;
        System.out.println("Java".equals(nothing));            // false, nessun errore
    }
}
```

L'output è:

```text
false
true
true
false
true
false
```

Il caso più insidioso è quello centrale: `a == b` dà `true` perché il compilatore può far condividere agli stessi letterali un solo oggetto, e quindi, con i letterali, `==` *sembra* funzionare. Non è una garanzia su cui basarsi: appena una delle due stringhe nasce da un'altra strada (`new String(...)`, una lettura da tastiera o da file, una concatenazione fatta a runtime) il confronto con `==` diventa falso anche con testo uguale. **Per confrontare il contenuto di due stringhe si usa sempre `equals`.**

> [!WARNING]
> **Attenzione — `equals` e il valore `null`**
> L'ultima riga dell'esempio mostra un'abitudine utile: scrivere il **letterale per primo**, `"Java".equals(nothing)`. Se `nothing` è `null`, il confronto dà semplicemente `false`. Scritto al contrario, `nothing.equals("Java")`, chiamerebbe un metodo su `null` e solleverebbe `NullPointerException`. Quando una stringa potrebbe essere `null`, chiama `equals` sul letterale o su una stringa di cui sei certo.

### 3.4.2 L'ordine lessicografico e `compareTo`

Per sapere se una stringa viene **prima** o **dopo** un'altra si usa l'**ordine lessicografico**. È simile all'ordine alfabetico del dizionario, ma si basa sull'ordine dei caratteri nel codice Unicode. Ne derivano due conseguenze: **tutte le cifre vengono prima di tutte le lettere**, e **tutte le lettere maiuscole vengono prima di tutte le minuscole** (la `'Z'` ha codice 90, la `'a'` codice 97). Di conseguenza `"Zebra"` precede `"apple"`.

Il metodo che confronta è:

```text
public int compareTo(String anotherString)
public int compareToIgnoreCase(String str)
```

`s1.compareTo(s2)` restituisce un `int` con questo significato: **negativo** se `s1` precede `s2`, **zero** se sono uguali, **positivo** se `s1` segue `s2`. `compareToIgnoreCase` fa lo stesso ignorando maiuscole e minuscole.

> [!NOTE]
> **Approfondimento esterno — Cosa restituisce esattamente `compareTo`**
> La documentazione definisce il valore così: se le due stringhe differiscono in una posizione, e `k` è la **prima** posizione in cui differiscono, il risultato è `this.charAt(k) - anotherString.charAt(k)`, cioè la differenza dei due codici. Se una stringa è un **prefisso** dell'altra (nessuna posizione differisce), il risultato è `this.length() - anotherString.length()`. Il risultato è `0` esattamente quando `equals` darebbe `true`.
> *Fonte:* [String.compareTo(String) (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html#compareTo(java.lang.String))

```java
public class Ordine {
    public static void main(String[] args) {
        System.out.println("apple".compareTo("banana"));          // -1  ('a' - 'b')
        System.out.println("banana".compareTo("apple"));          // 1
        System.out.println("apple".compareTo("apple"));           // 0
        System.out.println("Hello".compareTo("Help"));            // -4  ('l' - 'p')
        System.out.println("abc".compareTo("abcde"));             // -2  (3 - 5)
        System.out.println("Zebra".compareTo("apple"));           // -7  ('Z' - 'a')
        System.out.println("Zebra".compareToIgnoreCase("apple")); // 25  ('z' - 'a')
        String first = "mela";
        String second = "pera";
        if (first.compareTo(second) < 0) {
            System.out.println(first + " viene prima di " + second);
        }
    }
}
```

L'output è:

```text
-1
1
0
-4
-2
-7
25
mela viene prima di pera
```

Il valore esatto dipende dalle lettere coinvolte, perciò **non** si confronta mai il risultato con un numero preciso: né `== 1` né `== -1`. Si guarda solo il **segno**, con `< 0`, `== 0`, `> 0`, come nell'ultimo `if`. Per ordinare una raccolta di stringhe questo metodo viene usato automaticamente dalla libreria: la classe `String` implementa l'interfaccia `Comparable` ([Capitolo 10](10-classi-astratte-e-interfacce.md)) proprio grazie a `compareTo`.

Se si vuole un ordine "da dizionario" che ignori la differenza tra maiuscole e minuscole, si usa `compareToIgnoreCase`; altrimenti si possono portare entrambe le stringhe alla stessa forma con `toLowerCase()` (o `toUpperCase()`) prima di chiamare `compareTo`. Gli operatori `<` e `>` **non** si possono applicare alle stringhe: `"a" < "b"` non compila.

## 3.5 Dividere una stringa con `split`

Spesso un dato arriva come una riga di testo con più campi separati da un carattere: una riga di un file CSV (*comma-separated values*, valori separati da virgola), una frase da scomporre in parole. Il metodo che taglia una stringa in pezzi è:

```text
public String[] split(String regex)
```

Restituisce un **array di stringhe** (un array è una sequenza di valori dello stesso tipo, [Capitolo 5](05-array-e-matrici.md)): i pezzi di testo compresi tra due separatori. L'argomento è il separatore, ma attenzione: è una **espressione regolare** (*regular expression*, "regex"), cioè un modello di testo. Per i separatori semplici come `","` o `" "` si comporta come ci si aspetta, ma alcuni caratteri hanno un significato speciale (sotto). Per ora basta il caso semplice:

```java
import java.util.Arrays;

public class Dividere {
    public static void main(String[] args) {
        String line = "7001,12,2.50,CHAIR";
        String[] parts = line.split(",");
        System.out.println(parts.length);              // 4
        System.out.println(parts[3]);                  // CHAIR
        System.out.println(Arrays.toString(parts));    // [7001, 12, 2.50, CHAIR]
        int quantity = Integer.parseInt(parts[1].trim());
        double price = Double.parseDouble(parts[2].trim());
        System.out.println(quantity * price);          // 30.0
    }
}
```

L'output è:

```text
4
CHAIR
[7001, 12, 2.50, CHAIR]
30.0
```

`line.split(",")` dà un array di 4 elementi, accessibili con gli indici `parts[0]`…`parts[3]`. La riga con `Arrays.toString` serve solo a stamparlo in modo leggibile (la classe `Arrays` è del [Capitolo 5](05-array-e-matrici.md)). Per usare i pezzi come numeri bisogna convertirli: `split` restituisce sempre stringhe, e `Integer.parseInt` / `Double.parseDouble` ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.6.4) le trasformano in numeri. Il `trim()` davanti serve a togliere eventuali spazi attorno al pezzo, che farebbero sollevare `NumberFormatException`.

### 3.5.1 Casi particolari di `split`

Il comportamento di `split` ha alcuni casi che conviene conoscere a memoria, perché sono quelli che l'esame e i test nascosti mettono alla prova.

```java
import java.util.Arrays;

public class CasiSplit {
    public static void main(String[] args) {
        System.out.println(Arrays.toString(",a,,b,,".split(",")));        // [, a, , b]
        System.out.println(Arrays.toString("a,b,,".split(",", -1)));      // [a, b, , ]
        System.out.println(Arrays.toString("  a  b ".split(" ")));        // [, , a, , b]
        System.out.println(Arrays.toString("  a  b ".trim().split(" +")));// [a, b]
        System.out.println("".split(",").length);                         // 1
        System.out.println(Arrays.toString("a.b.c".split(".")));          // []
        System.out.println(Arrays.toString("a.b.c".split("\\.")));        // [a, b, c]
        System.out.println(Arrays.toString("a|b".split("\\|")));          // [a, b]
    }
}
```

L'output è:

```text
[, a, , b]
[a, b, , ]
[, , a, , b]
[a, b]
1
[]
[a, b, c]
[a, b]
```

Punto per punto.

- **Separatori consecutivi producono elementi vuoti.** Tra due virgole di fila non c'è niente, e `split` restituisce la stringa vuota `""` in quella posizione. Così `",a,,b,,".split(",")` ha un elemento vuoto iniziale e uno in mezzo.
- **Gli elementi vuoti in coda vengono scartati.** Dopo `"b"` ci sono altre due virgole, ma i pezzi vuoti finali non compaiono nel risultato: l'array è `[, a, , b]` e non ha elementi dopo `b`. Se si vogliono conservare, esiste la versione `public String[] split(String regex, int limit)` con `limit` negativo (per esempio `-1`), come nella seconda riga.
- **Con spazi multipli o in testa si ottengono elementi vuoti.** `"  a  b ".split(" ")` dà due elementi vuoti iniziali e uno in mezzo. Per dire "uno o più spazi" si usa il modello `" +"` (il `+` significa "uno o più della cosa precedente"); e per togliere gli spazi in testa si fa prima `trim()`. La terza e la quarta riga mostrano il prima e il dopo. Un altro modello molto usato per "uno o più spazi bianchi di qualunque tipo" è `"\\s+"`.
- **La stringa vuota produce un array di un elemento** (la stringa vuota stessa), non un array vuoto: `"".split(",").length` è `1`.
- **Alcuni caratteri sono "speciali" nelle espressioni regolari**, per esempio `.` (qualunque carattere) e `|` (alternativa). Per usarli come semplici separatori vanno preceduti da `\\`: `split("\\.")`, `split("\\|")`. Il backslash è doppio perché ne serve uno solo per l'espressione regolare, ma in un letterale Java ogni backslash va raddoppiato (sezione 3.3.1). Scrivere `split(".")` è un errore logico: compila, ma ogni carattere è un separatore e tutti i pezzi risultano vuoti e vengono scartati (risultato `[]`).

> [!NOTE]
> **Approfondimento esterno — `split` e le espressioni regolari**
> `String.split(String regex)` equivale a `split(regex, 0)`: il risultato **non contiene** le stringhe vuote finali, e il metodo solleva `PatternSyntaxException` se l'espressione regolare è scritta male. Con un `limit` negativo il modello viene applicato quante volte possibile e le stringhe vuote finali vengono **conservate**. I modelli di base usati sopra sono descritti nella classe `Pattern`: `.` è "qualunque carattere", `\s` è "un carattere di spazio bianco", il quantificatore `+` significa "una o più volte"; e, come dice la documentazione, in un letterale Java i backslash di un'espressione regolare vanno **raddoppiati**.
> *Fonte:* [String.split(String) (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html#split(java.lang.String)) e [Class Pattern (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/regex/Pattern.html)

## 3.6 L'output su console

### 3.6.1 `print` e `println`

`System.out` è un oggetto che fa parte di Java e rappresenta lo schermo (l'*output standard*). Ne abbiamo già usato il metodo `println`; ne esistono due varianti principali:

```text
public void println(...)   // stampa il valore e poi va a capo
public void print(...)     // stampa il valore e basta, senza andare a capo
public void println()      // senza argomenti: stampa solo un a capo
```

Entrambi esistono per ogni tipo primitivo, per `String` e per un oggetto qualsiasi, così `System.out.println(5)`, `System.out.println('c')`, `System.out.println(2.5)`, `System.out.println(true)` funzionano tutti. Con `print` si può costruire una riga a pezzi, terminandola con un `println`:

```java
public class StampaRiga {
    public static void main(String[] args) {
        System.out.print("One, two,");
        System.out.print(" buckle my shoe.");
        System.out.println(" Three, four,");
        System.out.println(" shut the door.");
        System.out.println();
        System.out.println('a' + 1);
        System.out.println((char) ('a' + 1));
    }
}
```

L'output è:

```text
One, two, buckle my shoe. Three, four,
 shut the door.

98
b
```

I primi tre `print`/`println` finiscono sulla stessa riga: solo il terzo manda a capo. Il quarto stampa una riga, e `println()` da solo stampa una riga vuota. Le ultime due righe ripropongono una trappola dei caratteri: `'a' + 1` è un `int` (98), che `println` stampa come numero; per ottenere il carattere successivo ad `'a'` serve il cast a `char` ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.6.3).

> [!IMPORTANT]
> **Nota del docente — Il formato dell'output è la specifica**
> Nella prova scritta l'output atteso è nella traccia e il test lo confronta con quello del programma: uno spazio in più, un a capo mancante, una virgola al posto del punto, e il confronto fallisce. Quindi **conta ogni carattere**: dove va `print` e dove `println`, dove vanno gli spazi, quante cifre decimali. Un `double` concatenato mostra sempre almeno una cifra decimale (`24.0`, non `24`), e questo si vede subito nell'output.

### 3.6.2 Formattare "a mano"

Spesso un numero va mostrato in un formato preciso, per esempio un importo in dollari con due cifre dopo la virgola. Senza strumenti di formattazione lo si costruisce a mano, ragionando in questo modo: si ricavano separatamente la parte intera (i dollari) e i centesimi, si stampa il simbolo del dollaro, i dollari, il punto, e poi i centesimi **sempre con due cifre** (quindi con uno zero davanti se sono meno di 10). Bisogna anche gestire il caso negativo e arrotondare, perché con i `double` un risultato come `19.99 * 100` non è esattamente `1999`.

#### Esempio — Un importo in dollari

```java
public class Denaro {
    static String dollars(double amount) {
        String sign = "";
        if (amount < 0) {
            sign = "-";
            amount = -amount;                         // lavoriamo sul valore positivo
        }
        long totalCents = (long) (amount * 100 + 0.5);  // arrotonda al centesimo
        long units = totalCents / 100;                  // parte intera
        long cents = totalCents % 100;                  // centesimi
        String pad = cents < 10 ? "0" : "";             // zero davanti se serve
        return sign + "$" + units + "." + pad + cents;
    }

    public static void main(String[] args) {
        System.out.println(dollars(9.5));
        System.out.println(dollars(19.99));
        System.out.println(dollars(0.05));
        System.out.println(dollars(-3.2));
        System.out.println(dollars(2.999));
    }
}
```

L'output è:

```text
$9.50
$19.99
$0.05
-$3.20
$3.00
```

Riga per riga del metodo. Se l'importo è negativo memorizziamo il segno in una stringa e lavoriamo sul valore opposto, così le divisioni non danno risultati strani. `amount * 100 + 0.5` porta l'importo in centesimi e aggiunge mezzo centesimo: il cast a `long` **tronca** ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.6.3), e aggiungere `0.5` prima di troncare equivale ad arrotondare al più vicino (`2.999` diventa 300 centesimi, cioè `$3.00`). La divisione `/ 100` tra interi dà i dollari, il resto `% 100` i centesimi. Infine `cents < 10 ? "0" : ""` (l'operatore condizionale, sezione 2.7.5 del Capitolo 2) aggiunge lo zero iniziale: `0.05` è `$0.05` e non `$0.5`.

Questo lavoro è istruttivo, ma Java offre uno strumento che lo fa in una riga: la formattazione con `printf` e `String.format`.

### 3.6.3 `printf` e `String.format`

Il metodo `printf` stampa un testo costruito a partire da una **stringa di formato** con dei segnaposto, che vengono sostituiti dai valori che seguono:

```text
public PrintStream printf(String format, Object... args)
public PrintStream printf(Locale l, String format, Object... args)
public static String format(String format, Object... args)       // in String
public static String format(Locale l, String format, Object... args)
```

Le due `printf` (della classe `PrintStream`, di cui `System.out` è un'istanza) **stampano**; le due `format` (della classe `String`) **restituiscono** la stringa formattata senza stamparla. I puntini `Object...` significano che dopo la stringa di formato si può passare un numero qualunque di valori. Ogni segnaposto nella stringa di formato ha la forma:

```text
%[indice$][flag][larghezza][.precisione]conversione
```

dove solo la **conversione** (un carattere) e il `%` iniziale sono obbligatori.

> [!NOTE]
> **Approfondimento esterno — La sintassi della stringa di formato**
> La classe `java.util.Formatter` descrive la sintassi usata da `printf` e `String.format`. Le conversioni più utili:
>
> | Conversione | Argomento | Risultato |
> |---|---|---|
> | `%d` | intero (`byte`, `short`, `int`, `long`) | numero decimale |
> | `%f` | virgola mobile (`float`, `double`) | numero decimale con parte frazionaria |
> | `%e` | virgola mobile | notazione scientifica |
> | `%x` | intero | esadecimale |
> | `%s` | qualunque (usa `toString()`) | testo |
> | `%c` | carattere | un carattere |
> | `%b` | qualunque (`boolean` o altro) | `true` o `false` |
> | `%n` | nessuno | il separatore di riga della piattaforma |
> | `%%` | nessuno | un simbolo `%` |
>
> La **larghezza** è il numero minimo di caratteri (l'output viene riempito con spazi a sinistra). La **precisione** con `%f` è il numero di cifre dopo la virgola. I **flag** più usati sono `-` (allinea a sinistra), `0` (riempie con zeri), `+` (mostra sempre il segno), `,` (separatore delle migliaia). Il metodo lancia `IllegalFormatException` (non controllata) se la stringa di formato è scritta male, se un segnaposto non è compatibile con l'argomento, o se mancano argomenti. **La localizzazione** (`Locale`) decide, tra l'altro, il simbolo decimale e il separatore delle migliaia: se non si passa un `Locale`, vale quello predefinito della macchina.
> *Fonte:* [Class Formatter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Formatter.html), [PrintStream.printf (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/PrintStream.html#printf(java.lang.String,java.lang.Object...)) e [String.format (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html#format(java.lang.String,java.lang.Object...))

```java
import java.util.Locale;

public class Formato {
    public static void main(String[] args) {
        double price = 3.14159;
        int qty = 42;
        System.out.printf("%.2f%n", price);                         // locale predefinito
        System.out.printf(Locale.US, "%.2f%n", price);              // sempre con il punto
        System.out.printf("%5d|%-5d|%05d%n", qty, qty, qty);
        System.out.printf("%s ha %d anni%n", "Ada", 36);
        String s = String.format(Locale.US, "%8.3f|%,d|%x|%c|%b|%%", 2.5, 1234567, 255, 'z', true);
        System.out.println(s);
        System.out.printf("senza a capo");
        System.out.println(" <- la riga continua");
    }
}
```

Su un computer con le impostazioni italiane l'output è:

```text
3,14
3.14
   42|42   |00042
Ada ha 36 anni
   2.500|1,234,567|ff|z|true|%
senza a capo <- la riga continua
```

Spiegazione. `%.2f` stampa il numero con due cifre dopo la virgola, **arrotondando** (`3.14159` diventa `3.14`). Nella prima riga il risultato è `3,14` con la **virgola** perché il locale predefinito è italiano; con `Locale.US` si ottiene sempre il **punto**. È la differenza che rompe il confronto con il test nascosto quando la traccia mostra, per esempio, `18.50`: su un computer con impostazioni italiane `printf("%.2f")` stampa `18,50`. Se l'output atteso usa il punto, si passa `Locale.US` come primo argomento. Nella terza riga `%5d` riempie a larghezza 5 con spazi a sinistra, `%-5d` allinea a sinistra e `%05d` riempie con zeri. `%n` manda a capo (come `println`: `printf` **non** va a capo da solo), e `%%` stampa un vero `%`.

> [!WARNING]
> **Attenzione — `printf` non va a capo**
> A differenza di `println`, `printf` stampa esattamente ciò che c'è nella stringa di formato. Se vuoi andare a capo devi scrivere `%n` (o `\n`) alla fine. Una dimenticanza fa sì che l'output successivo finisca sulla stessa riga.

## 3.7 L'input da tastiera con `Scanner`

### 3.7.1 Leggere dalla tastiera

Per leggere ciò che l'utente digita si usa la classe `Scanner`, che sta nel package `java.util`. Un **package** è una libreria di classi; poiché `java.util` non è importato in automatico (a differenza di `java.lang`), bisogna dichiararlo all'inizio del file. Si procede in tre passi: si importa la classe, si crea un oggetto `Scanner` collegato all'input standard `System.in`, e si chiamano i suoi metodi per leggere i dati.

```java
import java.util.Scanner;

public class Anagrafica {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        System.out.println("Enter your first name and age:");
        String name = keyboard.next();
        int age = keyboard.nextInt();
        System.out.println("Hello " + name + ", next year you will be " + (age + 1));
    }
}
```

Una possibile esecuzione, in cui la seconda riga è ciò che digita l'utente:

```text
Enter your first name and age:
Ada 36
Hello Ada, next year you will be 37
```

Riga per riga. `import java.util.Scanner;` rende disponibile la classe. `new Scanner(System.in)` crea lo scanner e lo collega alla tastiera; `keyboard` è il nome che gli diamo. `keyboard.next()` legge la **prossima parola** (fino al primo spazio) come `String`; `keyboard.nextInt()` legge la prossima parola e la interpreta come `int`. L'utente può scrivere i due valori sulla stessa riga separati da spazio, come sopra, oppure su due righe: per `Scanner` è lo stesso, perché gli spazi e gli a capo sono entrambi **separatori**.

> [!NOTE]
> **Definizione — Token e delimitatori**
> Lo `Scanner` divide l'input in pezzi chiamati **token**, separati da **delimitatori**. Per impostazione predefinita i delimitatori sono i **caratteri di spazio bianco** (spazio, tabulazione, a capo). `next()`, `nextInt()`, `nextDouble()`… leggono ciascuno **un token** e lo convertono nel tipo richiesto.

### 3.7.2 I metodi di `Scanner`

Questi sono i metodi di lettura (la tabella riporta il tipo restituito):

| Metodo | Cosa legge | Tipo restituito |
|---|---|---|
| `next()` | il prossimo token (fino al primo delimitatore, escluso) | `String` |
| `nextLine()` | **il resto della riga corrente**; l'a capo viene letto e scartato, non fa parte del risultato | `String` |
| `nextInt()` | il prossimo token come intero | `int` |
| `nextLong()` | il prossimo token come intero lungo | `long` |
| `nextShort()` | il prossimo token come intero corto | `short` |
| `nextByte()` | il prossimo token come intero a 8 bit | `byte` |
| `nextDouble()` | il prossimo token come numero in virgola mobile | `double` |
| `nextFloat()` | il prossimo token come numero in virgola mobile | `float` |
| `nextBoolean()` | il prossimo token come valore di verità: le parole `true` o `false`, con qualunque combinazione di maiuscole e minuscole | `boolean` |
| `useDelimiter(String pattern)` | cambia il delimitatore (sezione 3.7.4) | `Scanner` |

Tutti questi metodi sono dichiarati senza `throws`: le eccezioni che possono sollevare non sono controllate (sezione 3.7.5), quindi non servono `try`/`catch` per compilare.

### 3.7.3 La trappola di `nextLine` dopo `nextInt`

Questa è la fonte di errore più comune con `Scanner`, e merita una sezione a sé. Il punto è che `nextLine()` legge **il resto della riga corrente**, *anche se è vuoto*. `nextInt()`, invece, si ferma subito dopo l'ultima cifra del numero, **senza consumare l'a capo** che segue. Ecco cosa succede quando si mescolano i due:

```java
import java.util.Scanner;

public class Trappola {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        int n = keyboard.nextInt();
        String s1 = keyboard.nextLine();
        String s2 = keyboard.nextLine();
        System.out.println("n  = " + n);
        System.out.println("s1 = [" + s1 + "]");
        System.out.println("s2 = [" + s2 + "]");
    }
}
```

Con questo input:

```text
42
and don't you
forget it.
```

l'output è:

```text
n  = 42
s1 = []
s2 = [and don't you]
```

`nextInt()` legge `42` e si ferma subito dopo il `2`: l'a capo che chiude la prima riga resta nell'input. Il primo `nextLine()` legge "il resto della riga" a partire da lì, che è **vuoto**: restituisce quindi la stringa vuota (e consuma l'a capo). Solo il secondo `nextLine()` legge la riga successiva. Chi si aspettava `s1 = "and don't you"` ha letto una riga "fantasma".

Ci sono due rimedi. Il primo è chiamare `nextLine()` una volta in più **dopo** `nextInt()`, per buttare via il resto della prima riga:

```java
int n = keyboard.nextInt();
keyboard.nextLine();                    // consuma l'a capo rimasto dopo il numero
String s = keyboard.nextLine();         // ora legge la riga vera
```

Il secondo è leggere sempre **righe intere** con `nextLine()` e convertire a mano, con `Integer.parseInt` ([Capitolo 2](02-tipi-variabili-operatori.md), sezione 2.6.4):

```java
int n = Integer.parseInt(keyboard.nextLine().trim());
String s = keyboard.nextLine();
```

> [!CAUTION]
> **Errore tipico — Stessa trappola con `nextDouble`, `next`, `nextBoolean`…**
> Tutti i metodi che leggono un token (non solo `nextInt`) lasciano nell'input l'a capo finale della riga. Quindi qualunque `nextLine()` che segua una lettura di token sulla stessa riga restituisce il resto di *quella* riga, di solito vuoto. La regola: ogni volta che passi da una lettura "a token" a una lettura "a riga", ricordati dell'a capo rimasto.

### 3.7.4 Altri delimitatori

Con `useDelimiter` si cambia ciò che separa un token dall'altro. Dopo `keyboard.useDelimiter("##")` il separatore è **solo** la sequenza `##`: gli spazi e gli a capo non separano più nulla, e diventano parte dei token. Questo è il caso semplice del metodo (la documentazione ne descrive di più generali, basati sulle espressioni regolari).

```java
import java.util.Scanner;

public class Delimitatori {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        keyboard.useDelimiter("##");
        String first = keyboard.next();
        String second = keyboard.next();
        System.out.println("[" + first + "]");
        System.out.println("[" + second + "]");
    }
}
```

Con l'input `one two##three four` (senza a capo finale) l'output è:

```text
[one two]
[three four]
```

I due token contengono uno spazio al loro interno, cosa impossibile con il delimitatore predefinito. Se l'input terminasse con un a capo, quell'a capo farebbe parte dell'ultimo token.

### 3.7.5 Input sbagliato e fine dell'input

Che succede se il programma chiede un `int` e l'utente scrive `abc`? Se il token non ha la forma del tipo richiesto, `nextInt()` solleva `InputMismatchException`. Se l'input è finito, ogni metodo di lettura solleva `NoSuchElementException`; `InputMismatchException` è una sua sottoclasse, e tutte e due sono eccezioni **non controllate** (sono sottoclassi di `RuntimeException`).

Per evitare l'eccezione si **controlla prima**, con i metodi `hasNext…`, che rispondono `true` o `false` **senza consumare input**:

```text
public boolean hasNext()
public boolean hasNextInt()
public boolean hasNextLine()
```

`hasNextInt()` dice se il prossimo token si può leggere come `int`; `hasNext()` se c'è ancora un token; `hasNextLine()` se c'è ancora una riga. Il ciclo `while` è del [Capitolo 4](04-strutture-di-controllo.md); qui lo leggiamo come "finché la condizione è vera".

#### Esempio — Sommare i numeri fino al primo non numero

```java
import java.util.Scanner;

public class Somma {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        int sum = 0;
        while (keyboard.hasNextInt()) {         // finché il prossimo token è un intero
            sum += keyboard.nextInt();
        }
        System.out.println("Sum = " + sum);
    }
}
```

Con l'input

```text
3 4
5 x 6
```

l'output è `Sum = 12`: il ciclo legge 3, 4 e 5, poi trova `x`, che non è un intero, e si ferma (il `6` non viene mai letto).

#### Esempio — Richiedere di nuovo un numero finché è valido

```java
import java.util.Scanner;

public class NumeroValido {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        System.out.print("Enter a whole number: ");
        while (!keyboard.hasNextInt()) {
            keyboard.next();                    // scarta il token sbagliato
            System.out.print("Not a number, try again: ");
        }
        int n = keyboard.nextInt();
        System.out.println("You entered " + n);
    }
}
```

Con l'input `abc xyz 7` (anche su più righe) l'output è:

```text
Enter a whole number: Not a number, try again: Not a number, try again: You entered 7
```

Il passaggio decisivo è `keyboard.next()` dentro il ciclo. Quando `hasNextInt()` è falso, il token sbagliato **resta nell'input**: un metodo di lettura che fallisce non consuma ciò che non ha saputo convertire. Se il ciclo non lo scartasse, controllerebbe all'infinito sempre lo stesso token e non terminerebbe mai.

> [!NOTE]
> **Approfondimento esterno — Le eccezioni e il controllo di `Scanner`**
> Per `nextInt()` la documentazione dichiara: `InputMismatchException` se il prossimo token non ha la forma di un intero o supera i limiti del tipo; `NoSuchElementException` se l'input è terminato; `IllegalStateException` se lo scanner è stato chiuso. `InputMismatchException` è una sottoclasse di `NoSuchElementException`. I metodi `hasNextInt()`, `hasNext()` e `hasNextLine()` non avanzano nell'input.
> *Fonte:* [Class Scanner (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Scanner.html) e [InputMismatchException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/InputMismatchException.html)

### 3.7.6 Numeri decimali e impostazioni locali

C'è un'ultima insidia, legata all'ambiente in cui il programma gira. Lo `Scanner` interpreta i numeri in base al **locale** del computer: su un sistema con impostazioni italiane il separatore decimale è la **virgola**, quindi `nextDouble()` accetta `3,5` e **rifiuta** `3.5` (solleva `InputMismatchException`); su un sistema con impostazioni inglesi accade il contrario. Per rendere il programma indipendente dal computer si fissa il locale dello scanner con `useLocale`:

```java
import java.util.Locale;
import java.util.Scanner;

public class Prezzo {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        keyboard.useLocale(Locale.US);             // il separatore decimale è il punto
        double price = keyboard.nextDouble();
        System.out.println(price * 2);
    }
}
```

Con l'input `3.5` l'output è `7.0` su qualunque computer. Senza la riga `useLocale`, la stessa esecuzione su un computer con impostazioni italiane termina con `InputMismatchException`. È lo stesso meccanismo che abbiamo incontrato con `printf` nella sezione 3.6.3: **un numero con la virgola decimale dipende dal locale**, sia in lettura sia in scrittura.

### 3.7.7 Chiudere lo scanner

Un oggetto `Scanner` può essere chiuso con il metodo `public void close()`. Dopo la chiusura qualunque tentativo di lettura solleva `IllegalStateException`. Nei programmi che leggono dalla tastiera non è obbligatorio chiamarlo; va però ricordato che chiudere uno `Scanner` creato su `System.in` chiude anche l'input standard sottostante: se se ne crea un secondo dopo, non potrà più leggere nulla. In generale si crea **un solo** `Scanner` su `System.in` per programma e lo si usa ovunque. Con i file (nel [Capitolo 14](14-file-di-testo.md)) la chiusura diventerà invece un passo importante.

## Errori tipici

> [!CAUTION]
> **Errore tipico — Confrontare stringhe con `==`**
> ```java
> String a = new String("ciao");
> String b = new String("ciao");
> if (a == b) {                  // ERRORE LOGICO: false, anche se il testo è uguale
>     System.out.println("uguali");
> }
> ```
> `==` confronta i **riferimenti**, cioè se le due variabili indicano lo stesso oggetto, non il testo. Il programma compila e non dà errori, ma il ramo non viene eseguito. Forma corretta: `a.equals(b)`. Ancora peggio: con i letterali il confronto può dare `true` per caso e nascondere l'errore, che salta fuori solo quando una delle stringhe arriva da una lettura.

> [!CAUTION]
> **Errore tipico — Usare `<` e `>` su stringhe**
> ```java
> if ("apple" < "banana") { }    // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `bad operand types for binary operator '<'`: gli operatori relazionali valgono solo per i tipi numerici (e `char`). Forma corretta: `"apple".compareTo("banana") < 0`.

> [!CAUTION]
> **Errore tipico — Dimenticare di salvare il risultato di un metodo di `String`**
> ```java
> String name = "  Ada ";
> name.trim();                   // ERRORE LOGICO: il risultato viene scartato
> name.toUpperCase();            // idem
> System.out.println("[" + name + "]");   // stampa [  Ada ]
> ```
> Le stringhe sono immutabili: `trim()` e `toUpperCase()` restituiscono una **nuova** stringa e lasciano `name` com'è. Forma corretta: `name = name.trim().toUpperCase();`, che riassegna il risultato alla variabile.

> [!CAUTION]
> **Errore tipico — `length` senza parentesi e `s[0]` su una stringa**
> ```java
> String s = "ciao";
> int n = s.length;              // ERRORE DI COMPILAZIONE: cannot find symbol
> char c = s[0];                 // ERRORE DI COMPILAZIONE: array required, but String found
> ```
> Su una stringa `length` è un **metodo**, quindi `s.length()`; e una stringa non è un array, quindi il carattere in posizione 0 è `s.charAt(0)`. Per gli array vale il contrario: `a.length` senza parentesi (Capitolo 5).

> [!CAUTION]
> **Errore tipico — Uscire dai limiti di una stringa**
> ```java
> String s = "ciao";
> char last = s.charAt(s.length());       // ERRORE A RUNTIME: StringIndexOutOfBoundsException
> String part = s.substring(2, 9);        // ERRORE A RUNTIME: StringIndexOutOfBoundsException
> ```
> Gli indici validi per `charAt` vanno da `0` a `s.length() - 1`; per `substring(inizio, fine)` servono `0 <= inizio <= fine <= s.length()`. Il programma compila e si ferma solo quando esegue quella riga. Forma corretta: `s.charAt(s.length() - 1)` e `s.substring(2)`, oppure un controllo sulla lunghezza prima dell'accesso. Un ciclo con `i <= s.length()` al posto di `i < s.length()` produce lo stesso errore all'ultimo giro.

> [!CAUTION]
> **Errore tipico — Chiamare un metodo su una stringa `null`**
> ```java
> String s = null;
> int n = s.length();                     // ERRORE A RUNTIME: NullPointerException
> if (s.equals("ciao")) { }               // ERRORE A RUNTIME: NullPointerException
> ```
> `null` significa "nessun oggetto", e su nessun oggetto non si può chiamare alcun metodo. Forma corretta: controllare prima (`if (s != null && s.equals("ciao"))`) oppure mettere il letterale per primo: `"ciao".equals(s)`. Attenzione a non confondere `null` con la stringa vuota `""`, che è un oggetto vero e su cui i metodi funzionano.

> [!CAUTION]
> **Errore tipico — `'a'` e `"a"` non sono la stessa cosa**
> ```java
> char c = "a";                  // ERRORE DI COMPILAZIONE
> String s = 'a';                // ERRORE DI COMPILAZIONE
> ```
> I messaggi sono `incompatible types: String cannot be converted to char` e `incompatible types: char cannot be converted to String`. Gli apici singoli indicano un `char`, le virgolette doppie una `String`. Forme corrette: `char c = 'a';` e `String s = "a";` (oppure `String.valueOf('a')`).

> [!CAUTION]
> **Errore tipico — Un `+` che somma invece di concatenare**
> ```java
> int a = 3, b = 4;
> System.out.println("Somma: " + a + b);       // ERRORE LOGICO: stampa Somma: 34
> System.out.println(a + b + " è la somma");   // stampa 7 è la somma (corretto qui)
> System.out.println('x' + 'y' + "z");         // ERRORE LOGICO: stampa 241z
> ```
> Dopo un testo, ogni `+` concatena: `"Somma: " + a + b` accoda prima `3` e poi `4`. Forma corretta: `"Somma: " + (a + b)`. Per i `char`, partire da una stringa (`"" + 'x' + 'y' + "z"`).

> [!CAUTION]
> **Errore tipico — Sequenze di escape sbagliate**
> ```java
> String path = "C:\dati\file.txt";      // ERRORE DI COMPILAZIONE: illegal escape character
> String quote = "Disse "ciao"";         // ERRORE DI COMPILAZIONE: ';' expected
> ```
> Un backslash inizia sempre una sequenza di escape, e `\d` non esiste; le virgolette nel mezzo chiudono la stringa. Forme corrette: `"C:\\dati\\file.txt"` e `"Disse \"ciao\""`. Spezzare un letterale su due righe è un altro errore di compilazione (`unclosed string literal`): per andare a capo nel sorgente si chiude il letterale e si usa `+`.

> [!CAUTION]
> **Errore tipico — `split` con un carattere speciale**
> ```java
> String[] a = "a.b.c".split(".");       // ERRORE LOGICO: array vuoto
> String[] b = "a|b".split("|");         // ERRORE LOGICO: [a, |, b]
> ```
> L'argomento di `split` è un'espressione regolare e `.` e `|` hanno un significato speciale. Il programma compila e restituisce un risultato sbagliato. Forma corretta: `"a.b.c".split("\\.")` e `"a|b".split("\\|")`.

> [!CAUTION]
> **Errore tipico — Dare per scontato il numero di pezzi di `split`**
> ```java
> String[] w = "a  b".split(" ");        // ERRORE LOGICO: 3 elementi, non 2 (uno è "")
> int n = Integer.parseInt(" 12".trim()); // corretto: trim() prima di parseInt
> ```
> Due spazi di fila generano un elemento vuoto, e un pezzo con spazi attorno fa sollevare `NumberFormatException` se passato così com'è a `parseInt`. Forma corretta: `"a  b".split(" +")` per uno o più spazi, e `trim()` sul pezzo prima di convertirlo.

> [!CAUTION]
> **Errore tipico — `nextLine()` dopo `nextInt()`**
> ```java
> int n = keyboard.nextInt();
> String s = keyboard.nextLine();        // ERRORE LOGICO: s è "" (il resto della prima riga)
> ```
> `nextInt()` non consuma l'a capo che segue il numero, quindi `nextLine()` restituisce una stringa vuota. Forma corretta: una chiamata `keyboard.nextLine();` in più subito dopo `nextInt()`, oppure leggere righe intere e convertire con `Integer.parseInt`. Vedi la sezione 3.7.3.

> [!CAUTION]
> **Errore tipico — Dimenticare l'`import` di `Scanner`**
> ```java
> public class P {
>     public static void main(String[] args) {
>         Scanner keyboard = new Scanner(System.in);   // ERRORE DI COMPILAZIONE
>     }
> }
> ```
> Il compilatore risponde `cannot find symbol` (due volte: sulla classe `Scanner` come tipo e sul costruttore). `Scanner` sta in `java.util`, che non è importato in automatico. Forma corretta: aggiungere `import java.util.Scanner;` prima della classe.

> [!CAUTION]
> **Errore tipico — Un segnaposto di `printf` incompatibile o un output dipendente dal locale**
> ```java
> System.out.printf("%d%n", 3.5);          // ERRORE A RUNTIME: IllegalFormatConversionException
> System.out.printf("%.2f", 3.14159);      // ERRORE LOGICO: niente a capo e, in italiano, "3,14"
> ```
> `%d` vuole un intero e riceve un `double`; la forma corretta è `%f` (o `%.2f`). E con `%.2f` senza `Locale` il simbolo decimale dipende dal computer, e senza `%n` la riga non termina. Forma corretta, se l'output atteso usa il punto: `System.out.printf(Locale.US, "%.2f%n", 3.14159);` con `import java.util.Locale;`.

> [!CAUTION]
> **Errore tipico — `nextDouble()` e il separatore decimale**
> ```java
> double d = keyboard.nextDouble();       // ERRORE A RUNTIME con "3.5" su un computer italiano
> ```
> Con impostazioni italiane, `3.5` non è un numero valido per lo scanner e viene sollevata `InputMismatchException`. Forma corretta: `keyboard.useLocale(Locale.US);` prima della lettura, se l'input usa il punto.

## Riassunto

Una stringa è una sequenza di caratteri rappresentata dalla classe `String`: non un tipo primitivo, ma un **oggetto** con dei metodi. Si scrive con un letterale tra virgolette doppie, si unisce con `+` (che concatena o somma a seconda dei tipi, procedendo da sinistra), si misura con `length()` e si scorre con `charAt(i)`, con indici da 0. Una volta creata non cambia mai (immutabilità): i metodi che sembrano modificarla ne restituiscono una nuova, che va salvata. Per **confrontare** il contenuto si usa `equals` (mai `==`, che confronta i riferimenti), per l'ordine `compareTo` guardandone solo il segno; per **tagliare** si usano `substring`, `indexOf` e `split`, che lavora con espressioni regolari. Per **stampare** si usano `print`, `println` e, per i formati precisi, `printf` o `String.format`, tenendo presente che il simbolo decimale dipende dal locale; per **leggere** dalla tastiera si usa `Scanner`, che divide l'input in token e che ha la trappola di `nextLine` dopo una lettura a token.

**Concetti chiave**

- **`String` è un oggetto.** Ha metodi da chiamare con il punto; una variabile `String` può valere `null` (nessun oggetto), da non confondere con la stringa vuota `""`.
- **Concatenazione `+`.** Se un operando è una stringa, l'altro viene convertito in testo; la valutazione va da sinistra a destra, quindi `"a" + 1 + 2` dà `a12` e `1 + 2 + "a"` dà `3a`.
- **Indici da 0.** Il primo carattere è in posizione 0, l'ultimo in `length() - 1`; fuori da questo intervallo `charAt` e `substring` sollevano `StringIndexOutOfBoundsException`.
- **Immutabilità.** `toUpperCase`, `trim`, `replace`, `substring` restituiscono una stringa nuova: se non si assegna il risultato, non succede nulla.
- **`equals` e non `==`.** `==` confronta se due variabili indicano lo stesso oggetto; `equals` confronta il contenuto. Il letterale va messo per primo per evitare `NullPointerException`.
- **`compareTo` e l'ordine lessicografico.** Segno negativo, zero o positivo; ordine di Unicode (cifre prima delle lettere, maiuscole prima delle minuscole); non si confronta mai con `1` o `-1`.
- **`split`.** Taglia una stringa con un'espressione regolare; separatori consecutivi producono elementi vuoti, gli elementi vuoti finali vengono scartati, i caratteri speciali (`.`, `|`) vanno preceduti da `\\`.
- **Escape e Unicode.** `\"`, `\\`, `\n`, `\t`, `\'` sono un solo carattere; Java usa Unicode, quindi un `char` può rappresentare anche lettere accentate o di altri alfabeti.
- **`print`, `println`, `printf`.** `println` va a capo, `print` e `printf` no (`%n` per andare a capo con `printf`); `%d`, `%f`, `%s`, `%c`, `%b` sono le conversioni di base.
- **Il locale.** Il simbolo decimale di `printf("%.2f")` e di `Scanner.nextDouble()` dipende dalle impostazioni del computer: `Locale.US` e `useLocale(Locale.US)` fissano il punto.
- **`Scanner`.** Legge token separati da spazi bianchi; `nextLine()` legge il resto della riga corrente e, dopo una lettura a token, restituisce di solito una stringa vuota; i metodi `hasNext…` permettono di controllare l'input prima di leggerlo.

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `String` | `length` | `int length()` | — |
| `String` | `charAt` | `char charAt(int index)` | `StringIndexOutOfBoundsException` |
| `String` | `substring` | `String substring(int beginIndex)`, `String substring(int beginIndex, int endIndex)` | `StringIndexOutOfBoundsException` |
| `String` | `indexOf`, `lastIndexOf` | `int indexOf(String str)`, `int indexOf(int ch)`, `int indexOf(int ch, int fromIndex)`, `int lastIndexOf(int ch)` | — |
| `String` | `contains`, `startsWith`, `endsWith` | `boolean contains(CharSequence s)`, `boolean startsWith(String prefix)`, `boolean endsWith(String suffix)` | — |
| `String` | `toUpperCase`, `toLowerCase`, `trim` | `String toUpperCase()`, `String toLowerCase()`, `String trim()` | — |
| `String` | `replace` | `String replace(char oldChar, char newChar)`, `String replace(CharSequence target, CharSequence replacement)` | — |
| `String` | `isEmpty` | `boolean isEmpty()` | — |
| `String` | `equals`, `equalsIgnoreCase` | `boolean equals(Object anObject)`, `boolean equalsIgnoreCase(String anotherString)` | — |
| `String` | `compareTo`, `compareToIgnoreCase` | `int compareTo(String anotherString)`, `int compareToIgnoreCase(String str)` | — |
| `String` | `split` | `String[] split(String regex)`, `String[] split(String regex, int limit)` | `PatternSyntaxException` |
| `String` | `valueOf` (statico) | `static String valueOf(int i)` e le altre versioni per ogni tipo | — |
| `String` | `format` (statico) | `static String format(String format, Object... args)`, `static String format(Locale l, String format, Object... args)` | `IllegalFormatException` |
| `PrintStream` (`System.out`) | `print`, `println` | `void print(String s)`, `void println(String x)`, `void println()` e le versioni per ogni tipo | — |
| `PrintStream` (`System.out`) | `printf` | `PrintStream printf(String format, Object... args)`, `PrintStream printf(Locale l, String format, Object... args)` | `IllegalFormatException` |
| `Scanner` (`java.util`) | costruttore | `Scanner(InputStream source)` | — |
| `Scanner` | `next`, `nextLine` | `String next()`, `String nextLine()` | `NoSuchElementException`, `IllegalStateException` |
| `Scanner` | `nextInt`, `nextDouble` | `int nextInt()`, `double nextDouble()` | `InputMismatchException`, `NoSuchElementException`, `IllegalStateException` |
| `Scanner` | `hasNext`, `hasNextInt`, `hasNextLine` | `boolean hasNext()`, `boolean hasNextInt()`, `boolean hasNextLine()` | `IllegalStateException` |
| `Scanner` | `useDelimiter`, `useLocale` | `Scanner useDelimiter(String pattern)`, `Scanner useLocale(Locale locale)` | — |
| `Scanner` | `close` | `void close()` | — |
