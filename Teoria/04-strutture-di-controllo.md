---
materia: Programmazione a Oggetti
capitolo: 4
titolo: Strutture di controllo
livello_syllabus: 1
stato: completo
slide: ["Savitch cap. 3 slide 4-69", "Savitch cap. 4 slide 1-49", "Savitch cap. 5 slide 29"]
appelli: []
fonti_esterne: 4
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 4 — Strutture di controllo

## Di cosa parla questo capitolo

Finora i nostri programmi hanno eseguito le istruzioni una dopo l'altra, dalla prima all'ultima, sempre nello stesso ordine. Un programma così sa fare calcoli, ma non sa **decidere** ("se il saldo è negativo, avvisa") e non sa **ripetere** ("per ognuno dei dieci valori, fai questo"). Le **strutture di controllo** (*control flow*) sono gli strumenti con cui il programmatore cambia l'ordine di esecuzione: le **ramificazioni** scelgono quale strada percorrere (`if`, `switch`), i **cicli** ripetono un gruppo di istruzioni (`while`, `do-while`, `for`).

Il capitolo si appoggia sui valori di verità e sugli operatori logici del [Capitolo 2 — Tipi primitivi, variabili e operatori](02-tipi-variabili-operatori.md) (sezione 2.7): ogni condizione che incontreremo è un'espressione booleana. Riprende anche il `main` e le stampe del [Capitolo 1 — Java e la JVM](01-java-e-la-jvm.md), e il confronto tra stringhe del [Capitolo 3 — Stringhe e input/output da console](03-stringhe-e-console.md), che qui useremo nelle condizioni.

Alla fine del capitolo saprai scegliere e scrivere la struttura giusta per un problema (una scelta tra intervalli, una scelta tra valori esatti, una ripetizione con numero di giri noto o ignoto), prevedere a mano cosa fa un ciclo, evitare gli errori classici (`=` al posto di `==`, `break` dimenticato, ciclo che non finisce, ciclo che gira una volta di troppo) e usare le **enumerazioni** (`enum`), che si usano proprio insieme a `switch` e ai cicli. Vedrai infine come si traduce il testo di un esercizio in una struttura di controllo.

> [!NOTE]
> **Sull'uso nei programmi d'esame**
> Nelle tracce delle prove scritte descritte nell'[indice](_indice.md) questo capitolo non è mai l'argomento dichiarato dell'esercizio: è lo **strumento** con cui si risolve ogni esercizio. Un metodo statico che deve restituire un risultato calcolato, una classe che deve contare, cercare o filtrare, un thread che ripete un'operazione: sotto c'è sempre un `if` o un ciclo. Per questo gli esempi di fine capitolo (sezione 4.9) hanno la forma di piccoli esercizi con output atteso.

## 4.1 Il flusso di controllo

### 4.1.1 Sequenza, scelte, ripetizioni

Il **flusso di controllo** (*flow of control*) è l'ordine in cui un programma esegue le sue azioni. Per impostazione predefinita è **sequenziale**: si parte dalla prima istruzione del `main` e si scende, una riga alla volta. Le strutture di controllo sono di due famiglie:

- un'**istruzione di ramificazione** (*branching statement*) sceglie tra due o più azioni possibili: in Java sono `if`/`else` e `switch`;
- un'**istruzione di ciclo** (*loop statement*) ripete un'azione finché non si verifica una condizione di arresto: in Java sono `while`, `do-while` e `for`.

> [!TIP]
> **Intuizione — Il bivio e il giro in tondo**
> Una ramificazione è un bivio: a un certo punto si guarda un cartello (la condizione) e si prende una strada o l'altra; poi le strade si ricongiungono e il programma prosegue. Un ciclo è una rotonda: si resta a girare finché la condizione di uscita non è soddisfatta. L'analogia ha un limite: nella rotonda si può girare senza mai uscire (un **ciclo infinito**), e nei programmi è un errore frequente (sezione 4.6.5).

Tutte queste istruzioni usano **condizioni**, cioè espressioni booleane: `time < limit`, `score >= 60`, `n % 2 == 0`, o una combinazione con `&&`, `||` e `!` (sezione 2.7). Se la condizione dà `true` si compie l'azione, altrimenti no.

### 4.1.2 Istruzioni composte e blocchi

In Java, ovunque la sintassi chiede "un'istruzione" se ne può scrivere **una sola**. Per eseguirne più di una si racchiudono tra parentesi graffe: l'insieme così ottenuto si chiama **istruzione composta** (*compound statement*) e vale come un'istruzione sola.

```text
{
    Istruzione_1;
    Istruzione_2;
    ...
}
```

Un'istruzione composta può essere usata ovunque possa stare un'istruzione. Per esempio, nel corpo di un `if`:

```text
if (total > 10)
{
    sum = sum + total;
    total = 0;
}
```

Senza le graffe il corpo del `if` sarebbe soltanto `sum = sum + total;`, e `total = 0;` verrebbe eseguita sempre. È l'origine di un errore tipico (vedi gli errori tipici in fondo al capitolo). Per questo conviene **mettere sempre le graffe**, anche quando il corpo è una riga sola: costa due caratteri e toglie un'intera categoria di errori. Gli esempi di questo capitolo le mettono quasi sempre; dove le omettiamo è per mostrare proprio cosa succede.

### 4.1.3 La visibilità delle variabili in un blocco

Quando una variabile è dichiarata dentro un'istruzione composta, l'istruzione composta prende il nome di **blocco** (*block*), e la variabile è **locale al blocco**. La regola è semplice:

> [!NOTE]
> **Definizione — Ambito (scope) di una variabile locale**
> L'**ambito** (*scope*) di una variabile locale va **dalla sua dichiarazione fino alla parentesi graffa `}` che chiude il blocco in cui è dichiarata**. Fuori da quel punto il nome non esiste. Una variabile dichiarata *fuori* dal blocco, prima del blocco, è invece visibile sia fuori sia dentro.

Vediamolo con un programma:

```java
public class Blocchi {
    public static void main(String[] args) {
        int total = 100;                  // visibile in tutto il resto del metodo
        if (total > 50) {
            int bonus = 10;               // nasce qui, vive fino alla } che chiude il blocco
            total = total + bonus;        // dentro il blocco si vedono anche le variabili esterne
            System.out.println("bonus = " + bonus);
        }
        System.out.println("total = " + total);
        // System.out.println(bonus);     // errore: bonus non esiste più qui
    }
}
```

`total` è dichiarata nel corpo del `main`, quindi è visibile ovunque dopo la sua dichiarazione, anche dentro il blocco del `if`. `bonus` è dichiarata dentro il blocco: la si può usare solo tra la sua dichiarazione e la `}` del `if`. Se togliessimo il commento alla penultima riga, il compilatore risponderebbe `cannot find symbol`. Dentro il blocco `bonus` vale 10 e `total` diventa 110. L'output è:

```text
bonus = 10
total = 110
```

Tre conseguenze pratiche. Primo, **una variabile si dichiara il più vicino possibile al punto in cui serve**, nel blocco più piccolo che la contiene. Secondo, **non si può dichiarare nel blocco interno una variabile con lo stesso nome di una già visibile** nel blocco esterno: `int total = 5;` dentro il `if` sarebbe un errore di compilazione (`variable total is already defined`). Terzo, una variabile dichiarata nell'intestazione di un `for` (sezione 4.5.3) vive solo per il ciclo.

## 4.2 L'istruzione if-else

### 4.2.1 La forma di base

L'istruzione `if-else` sceglie tra **due** azioni in base a una condizione. Sintassi:

```text
if (Espressione_booleana)
    Istruzione_1
else
    Istruzione_2
```

L'espressione tra parentesi tonde **deve** essere di tipo `boolean`; le parentesi sono obbligatorie. Se vale `true` si esegue `Istruzione_1`, altrimenti `Istruzione_2`; poi il programma continua con l'istruzione successiva. `Istruzione_1` e `Istruzione_2` sono istruzioni singole oppure blocchi tra graffe (sezione 4.1.2).

### 4.2.2 Omettere il ramo else

Il ramo `else` è facoltativo. Se manca e la condizione è falsa, non si esegue niente e il programma prosegue.

```java
public class SenzaElse {
    public static void main(String[] args) {
        int age = 15;
        if (age < 18) {
            System.out.println("Tariffa ridotta");
        } else {
            System.out.println("Tariffa intera");
        }

        int count = 5;
        int total = 20;
        if (count < 3) {              // la condizione è falsa: il blocco viene saltato
            total = 0;
            count = 0;
        }
        System.out.println(total + " " + count);
    }
}
```

Nella prima parte `age < 18` è vera, quindi si stampa il ramo `if` e il ramo `else` viene ignorato. Nella seconda, `count < 3` è falsa (5 non è minore di 3) e non c'è un `else`: il blocco con i due azzeramenti viene saltato e `total` e `count` restano come prima. L'output è:

```text
Tariffa ridotta
20 5
```

### 4.2.3 if annidati ed else pendente

Un `if-else` può contenere qualunque tipo di istruzione, quindi anche un altro `if-else`: si parla di istruzioni **annidate** (*nested*). Si può annidare nel ramo `if`, nel ramo `else` o in entrambi:

```text
if (Condizione_1)
    if (Condizione_2)
        Istruzione_1
    else
        Istruzione_2
else
    if (Condizione_3)
        Istruzione_3
    else
        Istruzione_4
```

Qui nasce un'ambiguità: se in una sequenza di `if` e `else` senza graffe il numero di `else` è minore di quello degli `if`, a quale `if` appartiene ciascun `else`? La regola del linguaggio è:

> [!NOTE]
> **Definizione — Regola dell'else pendente**
> Ogni `else` si accoppia con **l'`if` più vicino che non ha ancora un `else`**. L'indentazione serve a *far leggere* all'uomo l'accoppiamento, ma al compilatore non importa: conta solo la regola. Le graffe permettono di raggruppare le istruzioni come le parentesi in un'espressione e di forzare un accoppiamento diverso.

Il caso classico sono due scritture quasi identiche che fanno cose diverse. Nel programma seguente `a > b` è falso, quindi il comportamento dipende da quale `if` "possiede" l'`else`:

```java
public class ElsePendente {
    public static void main(String[] args) {
        int a = 1;
        int b = 2;
        int c = 3;
        int d = 1;
        String e = "e invariato";
        String g = "g invariato";

        // Prima forma: le graffe fanno dell'if interno un blocco a sé.
        // L'else resta agganciato all'if esterno.
        if (a > b) {
            if (c > d)
                e = "e cambiato";
        } else
            g = "g cambiato";
        System.out.println(e + ", " + g);

        e = "e invariato";
        g = "g invariato";

        // Seconda forma: senza graffe l'else si aggancia all'if più vicino, quello interno.
        if (a > b)
            if (c > d)
                e = "e cambiato";
            else
                g = "g cambiato";
        System.out.println(e + ", " + g);
    }
}
```

Nella prima forma le graffe chiudono l'`if (c > d)`, quindi l'`else` si lega a `if (a > b)`: poiché `a > b` è falso, si esegue l'`else` e `g` cambia. Nella seconda forma non ci sono graffe e l'`else` si lega all'`if (c > d)` più vicino; ma `a > b` è falso e quindi l'intero `if` interno, con il suo `else`, viene saltato: non cambia nulla. L'output è:

```text
e invariato, g cambiato
e invariato, g invariato
```

Se vuoi che l'`else` appartenga all'`if` esterno, **metti le graffe**.

### 4.2.4 Scelte multiple con else if

Quando le alternative sono più di due, si concatenano gli `if` nel ramo `else`. Il risultato si scrive in questa forma, che è solo un modo ordinato di annidare:

```text
if (Condizione_1)
    Istruzione_1
else if (Condizione_2)
    Istruzione_2
else if (Condizione_3)
    Istruzione_3
else
    Istruzione_di_default
```

Le condizioni sono valutate **in ordine, dall'alto in basso**. Appena una è vera si esegue la sua istruzione e **tutte le altre si saltano**, anche se fossero vere. L'`else` finale, che raccoglie tutti i casi rimasti, è facoltativo ma di solito conviene metterlo. Un classico è la conversione di un punteggio in una fascia:

```java
public class Fasce {
    static char grade(int score) {
        if (score >= 90) {
            return 'A';
        } else if (score >= 80) {
            return 'B';
        } else if (score >= 70) {
            return 'C';
        } else if (score >= 60) {
            return 'D';
        } else {
            return 'F';
        }
    }

    public static void main(String[] args) {
        System.out.println(grade(95));
        System.out.println(grade(90));
        System.out.println(grade(72));
        System.out.println(grade(60));
        System.out.println(grade(10));
    }
}
```

`grade` è un metodo statico che riceve un `int` e restituisce un `char`; l'istruzione `return` termina il metodo e consegna il valore a chi l'ha chiamato (i metodi sono il tema del Capitolo 6). Con 95 la prima condizione è vera e il metodo restituisce `'A'` senza guardare le altre. Con 72 le prime due condizioni sono false e la terza vera: `'C'`. Con 10 nessuna condizione è vera e scatta l'`else`: `'F'`. L'output è:

```text
A
A
C
D
F
```

Si noti che nelle condizioni successive alla prima non serve riscrivere il limite superiore. Si potrebbe scrivere `else if ((score >= 80) && (score < 90))`, ma è ridondante: se si arriva a quel punto, vuol dire che `score >= 90` era falso, quindi `score < 90` è già garantito. Scrivere il controllo due volte non è un errore, ma allunga il codice e aumenta le occasioni di sbagliarsi.

> [!WARNING]
> **Attenzione — L'ordine delle condizioni conta**
> Con una catena di `else if` le condizioni **si sovrappongono** (un punteggio di 95 è anche `>= 60`), e vince la prima che risulta vera. Quindi vanno scritte dalla più restrittiva alla meno restrittiva. Se nella funzione sopra mettessimo per prima `score >= 60`, ogni punteggio da 60 in su darebbe `'D'` e le altre fasce non sarebbero mai raggiunte. Il compilatore non segnala nulla: è un errore logico.

### 4.2.5 Un caso completo: l'indice di massa corporea

Riuniamo quanto visto in un esempio con calcolo e classificazione. L'**indice di massa corporea** (*Body Mass Index*, BMI) serve a stimare il rischio di problemi legati al peso. Si calcola come

$$\text{BMI} = \frac{\text{massa in kg}}{(\text{altezza in m})^2}$$

cioè la massa in chilogrammi divisa per il **quadrato** dell'altezza in metri. La valutazione è: sotto 18,5 sottopeso; da 18,5 incluso a 25 escluso normopeso; da 25 a 30 escluso sovrappeso; da 30 in su obeso.

L'algoritmo è: partire da altezza in piedi e pollici e peso in libbre; convertire in metri e chilogrammi (1 pollice = 0,0254 metri; 1 kg corrisponde a circa 2,2 libbre); calcolare il BMI; stampare la classe di rischio con una catena di `if`. Mettiamo i dati direttamente nel programma, così il risultato è sempre lo stesso:

```java
import java.util.Locale;

public class Bmi {
    static String classifica(double bmi) {
        if (bmi < 18.5) {
            return "sottopeso";
        } else if (bmi < 25) {
            return "normopeso";
        } else if (bmi < 30) {
            return "sovrappeso";
        } else {
            return "obeso";
        }
    }

    public static void main(String[] args) {
        int feet = 5;
        int inches = 9;
        double pounds = 150;

        double meters = (feet * 12 + inches) * 0.0254;   // 1 pollice = 0.0254 metri
        double kilograms = pounds / 2.2;                 // 1 kg = 2.2 libbre (valore approssimato)
        double bmi = kilograms / (meters * meters);

        System.out.printf(Locale.US, "BMI = %.1f -> %s%n", bmi, classifica(bmi));
        System.out.println(classifica(18.5));
        System.out.println(classifica(24.99));
        System.out.println(classifica(30));
    }
}
```

Riga per riga. `classifica` usa una catena di quattro rami con la sola condizione sul limite superiore, perché i limiti inferiori sono garantiti dai rami precedenti. In `main`, `feet * 12 + inches` converte 5 piedi e 9 pollici in 69 pollici; moltiplicando per 0,0254 si ottengono 1,7526 m. `pounds / 2.2` dà circa 68,18 kg. Il BMI è `68,18 / (1,7526 · 1,7526)`, circa 22,2. La stampa con `printf` e `Locale.US` (sezione 3.6.3) fissa il punto decimale. Le tre chiamate successive controllano i **valori di confine**: 18,5 è già normopeso (la condizione `bmi < 18.5` è falsa), 24,99 è ancora normopeso, 30 è già obeso. L'output è:

```text
BMI = 22.2 -> normopeso
normopeso
normopeso
obeso
```

> [!TIP]
> **Intuizione — Collauda sempre i confini**
> Gli errori nelle catene di `if` stanno quasi sempre sui valori di confine, dove si confondono `<` e `<=`. Quando scrivi una catena, prova sempre i valori esattamente uguali ai limiti e quelli immediatamente accanto.

### 4.2.6 Scrivere bene le condizioni

Le condizioni usano gli operatori di confronto e logici del [Capitolo 2](02-tipi-variabili-operatori.md). Ricapitoliamo i punti che contano di più dentro un `if`.

- **`==` per interi e caratteri.** `a == 3` con `a` intero è corretto.
- **Mai `==` tra numeri in virgola mobile.** I `double` sono approssimati (sezione 2.2.3): `0.1 + 0.2` non è esattamente `0.3`. Si controlla invece che la differenza sia minore di una piccola tolleranza (*epsilon*): `Math.abs(b - c) < epsilon`, dove `Math.abs` restituisce il valore assoluto.
- **Mai `==` tra stringhe e altri oggetti.** `s1 == s2` controlla soltanto se le due variabili indicano lo *stesso oggetto in memoria*. Per il contenuto si usa `s1.equals(s2)` oppure `s1.equalsIgnoreCase(s2)` (sezione 3.4).
- **Variabili booleane.** Se `isAdult` è un `boolean`, la condizione si scrive `if (isAdult)`, non `if (isAdult == true)`, e la negazione `if (!isAdult)`. Un buon nome fa leggere la condizione come una frase (sezione 2.7.1).

```java
public class Confronti {
    public static void main(String[] args) {
        int a = 3;
        System.out.println(a == 3);                      // interi: == va bene

        double x = 0.1 + 0.2;
        System.out.println(x == 0.3);                    // false: x vale 0.30000000000000004
        double epsilon = 0.000001;
        System.out.println(Math.abs(x - 0.3) < epsilon); // true: differenza trascurabile

        String s1 = new String("ciao");
        String s2 = new String("ciao");
        System.out.println(s1 == s2);                    // false: due oggetti distinti
        System.out.println(s1.equals(s2));               // true: stesso testo

        boolean isAdult = a >= 18;
        if (!isAdult) {
            System.out.println("minorenne");
        }
    }
}
```

`a == 3` è vera. `x == 0.3` è falsa perché `x` vale `0.30000000000000004`, ma la differenza `x - 0.3` è di circa `5.5e-17` e sta sotto la tolleranza: il confronto con `epsilon` dà `true`. Le due stringhe create con `new String` sono oggetti distinti con lo stesso testo: `==` dà `false` ed `equals` dà `true`. L'output è:

```text
true
false
true
false
true
minorenne
```

L'operatore condizionale `condizione ? valore1 : valore2`, che nei casi semplici sostituisce un `if-else`, è descritto nella sezione 2.7.5.

### 4.2.7 Controllare i dati in ingresso

Un programma non deve fidarsi dei dati che riceve. Se si scrive `int inches = feet * 12;` senza controllare `feet`, cosa succede se il valore è negativo? Se è irragionevole, come 100 piedi? Se è così grande da far traboccare un `int` (oltre 2 147 483 647)? Il rimedio è un `if` che lascia entrare nella parte "buona" del programma solo i valori ammessi, e gestisce a parte gli altri.

```java
public class Validazione {
    static String inInch(int feet) {
        if (feet >= 0 && feet < 10) {
            int inches = feet * 12;
            return feet + " piedi = " + inches + " pollici";
        } else {
            return feet + " non è un valore ragionevole";
        }
    }

    public static void main(String[] args) {
        System.out.println(inInch(6));
        System.out.println(inInch(-2));
        System.out.println(inInch(100));
    }
}
```

La condizione `feet >= 0 && feet < 10` è vera solo per i valori da 0 a 9; per ogni altro valore si va nell'`else`. Si noti che la variabile `inches` è dichiarata dentro il blocco del `if`: è visibile solo lì (sezione 4.1.3). L'output è:

```text
6 piedi = 72 pollici
-2 non è un valore ragionevole
100 non è un valore ragionevole
```

## 4.3 L'istruzione switch

### 4.3.1 La forma

Quando la scelta dipende dal **valore esatto** di una sola espressione ("se è 1 fai questo, se è 2 quest'altro…") la catena di `else if` diventa lunga e ripetitiva. L'istruzione `switch` è fatta per questo caso: è una ramificazione a più vie che decide in base a una sola espressione, detta **espressione di controllo** (*controlling expression*). Sintassi:

```text
switch (Espressione_di_controllo)
{
    case Etichetta_1:
        Istruzioni;
        break;
    case Etichetta_2:
        Istruzioni;
        break;
    ...
    default:
        Istruzioni;
        break;
}
```

L'esecuzione procede così. Si valuta l'espressione di controllo. Si cerca, tra le etichette dei `case`, quella uguale al valore ottenuto. Se la si trova, si esegue la lista di istruzioni che la segue. Se non c'è nessuna corrispondenza, si esegue il ramo `default`. Il ramo `default` è facoltativo, ma è consigliato metterlo, anche solo per stampare un messaggio. Ogni **etichetta** (*case label*) è una **costante** seguita da due punti, e due `case` dello stesso `switch` non possono avere la stessa etichetta.

```java
public class Giorni {
    static String nome(int day) {
        String name;
        switch (day) {
            case 1:
                name = "lunedì";
                break;
            case 2:
                name = "martedì";
                break;
            case 3:
                name = "mercoledì";
                break;
            default:
                name = "altro giorno";
                break;
        }
        return name;
    }

    public static void main(String[] args) {
        System.out.println(nome(1));
        System.out.println(nome(3));
        System.out.println(nome(7));
    }
}
```

`nome(1)` salta al `case 1`, assegna `"lunedì"` e il `break` fa uscire dallo `switch`; poi `return name;` restituisce il valore. `nome(7)` non corrisponde a nessuna etichetta e finisce nel `default`. L'output è:

```text
lunedì
mercoledì
altro giorno
```

### 4.3.2 break e fall-through

Il punto che più spesso inganna è questo: dopo aver trovato l'etichetta giusta, Java esegue le sue istruzioni **e poi continua con le istruzioni dei `case` successivi**, senza controllare le loro etichette, finché non incontra un `break` o la fine dello `switch`. Questo comportamento si chiama *fall-through* (letteralmente "cadere giù"). L'istruzione `break` interrompe lo `switch` e fa proseguire il programma dopo la `}` finale.

```java
public class Cadute {
    public static void main(String[] args) {
        int level = 2;
        System.out.println("Senza break:");
        switch (level) {
            case 1:
                System.out.println("  livello 1");
            case 2:
                System.out.println("  livello 2");
            case 3:
                System.out.println("  livello 3");
            default:
                System.out.println("  default");
        }

        System.out.println("Con break:");
        switch (level) {
            case 1:
                System.out.println("  livello 1");
                break;
            case 2:
                System.out.println("  livello 2");
                break;
            case 3:
                System.out.println("  livello 3");
                break;
            default:
                System.out.println("  default");
        }
    }
}
```

Nel primo `switch` il valore è 2: si entra nel `case 2`, si stampa "livello 2", e poiché manca il `break` si "cade" nel `case 3` e poi nel `default`, stampando anche quelli. Nel secondo, ogni ramo termina con `break` e si stampa solo il ramo scelto. L'output è:

```text
Senza break:
  livello 2
  livello 3
  default
Con break:
  livello 2
```

> [!IMPORTANT]
> **Nota del docente — `break` alla fine di ogni caso**
> L'azione di ogni caso termina di norma con `break`. Il `break` è facoltativo dal punto di vista della sintassi, ma senza di esso si eseguono anche gli altri casi. Dimenticarlo è un errore che il compilatore non vede e che cambia l'output.

Il fall-through non è soltanto un incidente da evitare: serve quando **più etichette devono portare alla stessa azione**. Basta scrivere i `case` uno sotto l'altro, senza istruzioni (e senza `break`) tra loro:

```java
public class Vocali {
    static String tipo(char c) {
        switch (c) {
            case 'a':
            case 'e':
            case 'i':
            case 'o':
            case 'u':
                return "vocale";
            case ' ':
                return "spazio";
            default:
                return "altro";
        }
    }

    public static void main(String[] args) {
        System.out.println(tipo('e'));
        System.out.println(tipo('z'));
        System.out.println(tipo(' '));
    }
}
```

Cinque etichette condividono la stessa istruzione: per `'e'` si entra nel secondo `case` e si "cade" fino al `return`. In questo programma non servono i `break`, perché ogni ramo termina con `return`, che esce dall'intero metodo. L'output è:

```text
vocale
altro
spazio
```

### 4.3.3 Quali tipi e quali etichette

L'espressione di controllo deve avere un tipo **intero o carattere** (`byte`, `short`, `int`, `char`), oppure — da Java 7 — essere una **stringa** (`String`), oppure essere un'**enumerazione** (sezione 4.4). Non sono ammessi `long`, `double`, `boolean`: `switch (l)` con `long l` è un errore di compilazione (con JDK 22, `selector type long is not allowed`).

Le etichette devono essere **costanti**: letterali (`1`, `'a'`, `"stop"`) o costanti con nome `final` inizializzate con un letterale. Una variabile qualunque come etichetta non compila (`constant expression required`), e due etichette uguali nemmeno (`duplicate case label`).

Con le stringhe il confronto è lo stesso di `equals`, quindi distingue maiuscole e minuscole:

```java
public class Comandi {
    static String esegui(String command) {
        switch (command) {
            case "start":
                return "avvio";
            case "stop":
                return "arresto";
            default:
                return "comando sconosciuto: " + command;
        }
    }

    public static void main(String[] args) {
        System.out.println(esegui("start"));
        System.out.println(esegui("stop"));
        System.out.println(esegui("Start"));
    }
}
```

`"Start"` con la S maiuscola non è uguale a `"start"` e finisce nel `default`. L'output è:

```text
avvio
arresto
comando sconosciuto: Start
```

> [!WARNING]
> **Attenzione — switch su una stringa `null`**
> Se l'espressione di controllo è una stringa `null`, lo `switch` solleva una `NullPointerException` (non finisce nel `default`). Quando la stringa può mancare, va controllata prima.

### 4.3.4 switch o catena di else if?

Sono due strumenti per due problemi diversi.

| Situazione | Strumento |
|---|---|
| La scelta dipende dall'**uguaglianza** di una sola espressione con valori **costanti** (menu, comandi, giorni, enumerazioni) | `switch` |
| La scelta dipende da **intervalli** (`x > 10 && x < 20`), da condizioni su più variabili o da confronti tra valori calcolati | `if` / `else if` |

Uno `switch` classico non può esprimere un intervallo, perché ogni etichetta è un valore singolo. Una catena di `else if` può esprimere tutto, ma quando le alternative sono "il valore è 1, è 2, è 3…" lo `switch` si legge meglio. Tutto ciò che si scrive con uno `switch` si può riscrivere con `if`/`else if` (con `==` per i numeri e `equals` per le stringhe); non è vero il contrario.

## 4.4 Le enumerazioni

### 4.4.1 Dichiarare e usare un enum

A volte una variabile deve poter assumere soltanto **pochi valori prestabiliti**: un semaforo è rosso, giallo o verde; una valutazione è alta, media o bassa. Usare i numeri 0, 1, 2 ("0 vuol dire rosso") è fragile: nessuno controlla che non si scriva 7, e il programma si legge male. Una **enumerazione** (*enumeration*, in codice `enum`) risolve il problema elencando i valori ammessi.

> [!NOTE]
> **Definizione — Enumerazione**
> Una **enumerazione** è un tipo che elenca i valori che una variabile può assumere. Si dichiara con la parola chiave `enum`, il nome del tipo e, tra graffe, le costanti separate da virgole. Per convenzione i nomi delle costanti sono in maiuscolo. Si usa una costante scrivendo `NomeEnum.COSTANTE`.

```java
enum Level { LOW, MEDIUM, HIGH }

public class Livelli {
    public static void main(String[] args) {
        Level rating;
        rating = Level.MEDIUM;
        System.out.println(rating);
        if (rating == Level.HIGH) {
            System.out.println("alto");
        } else {
            System.out.println("non alto");
        }
    }
}
```

`enum Level { LOW, MEDIUM, HIGH }` definisce un nuovo tipo, `Level`, con tre sole costanti. `Level rating;` dichiara una variabile di quel tipo; `rating = Level.MEDIUM;` le assegna una costante. Stampare un valore di enum mostra il suo nome. Per i valori di un enum si usa `==` (sono costanti uniche, non servono `equals`). Si noti la forma del file: l'`enum` è dichiarato **fuori** dalla classe pubblica, senza modificatore, nello stesso file, come si farebbe con una classe in una prova scritta. In alternativa lo si può dichiarare **dentro** la classe, come nell'esempio che segue. L'output è:

```text
MEDIUM
non alto
```

Un `enum` è in realtà una classe speciale con un numero fisso di istanze: i dettagli, cioè classi e oggetti, sono nel [Capitolo 7 — Classi e oggetti](07-classi-e-oggetti.md). Qui basta saperlo usare come tipo con valori elencati.

### 4.4.2 enum e switch

Gli enum sono il compagno naturale dello `switch`. Nelle etichette dei `case` si scrive il **nome semplice** della costante, senza il nome dell'enum davanti:

```java
public class Semafori {
    enum Light { RED, YELLOW, GREEN }

    static String azione(Light light) {
        switch (light) {
            case RED:
                return "fermati";
            case YELLOW:
                return "rallenta";
            case GREEN:
                return "passa";
            default:
                return "?";
        }
    }

    public static void main(String[] args) {
        Light now = Light.YELLOW;
        System.out.println(now);
        System.out.println(azione(now));
        System.out.println(now == Light.YELLOW);

        System.out.println(now.name() + " ha posizione " + now.ordinal());
        Light parsed = Light.valueOf("GREEN");
        System.out.println(azione(parsed));

        for (Light l : Light.values()) {
            System.out.print(l + " ");
        }
        System.out.println();
    }
}
```

Qui l'`enum` è dichiarato dentro la classe `Semafori`. Nello `switch` le etichette sono `RED`, `YELLOW`, `GREEN`, non `Light.RED`: scrivere il nome qualificato è un errore di compilazione (`an enum switch case label must be the unqualified name of an enumeration constant`). Le altre righe usano i metodi di cui parliamo ora. L'output è:

```text
YELLOW
rallenta
true
YELLOW ha posizione 1
passa
RED YELLOW GREEN 
```

### 4.4.3 Alcuni metodi degli enum

Ogni enum possiede alcuni metodi, dichiarati dalla classe base `java.lang.Enum` o generati dal compilatore. Quelli che servono sono:

| Metodo | Firma | Cosa fa |
|---|---|---|
| `values` | `static E[] values()` | restituisce un array con tutte le costanti, **nell'ordine di dichiarazione** (generato dal compilatore) |
| `valueOf` | `static E valueOf(String name)` | restituisce la costante con quel nome; solleva `IllegalArgumentException` se non esiste (generato dal compilatore) |
| `name` | `final String name()` | il nome della costante, scritto esattamente come nella dichiarazione |
| `ordinal` | `final int ordinal()` | la posizione nella dichiarazione, **a partire da zero** |
| `toString` | `String toString()` | di norma coincide con `name()`; è ciò che viene stampato |
| `compareTo` | `final int compareTo(E o)` | negativo, zero o positivo secondo l'ordine di dichiarazione |

Nell'esempio sopra `YELLOW` è la seconda costante, quindi `ordinal()` vale 1. `Light.valueOf("GREEN")` restituisce la costante `GREEN`; `Light.valueOf("PURPLE")` solleva `IllegalArgumentException` con il messaggio `No enum constant Semafori.Light.PURPLE`.

> [!NOTE]
> **Approfondimento esterno — La classe `java.lang.Enum`**
> La Javadoc descrive `Enum` come "la classe base comune di tutte le classi di enumerazione del linguaggio Java". `name()` restituisce il nome della costante "esattamente come dichiarato nella sua dichiarazione di enum"; `ordinal()` ne restituisce la posizione, "dove alla costante iniziale è assegnato l'ordinale zero"; `toString()` restituisce il nome della costante come contenuto nella dichiarazione; `compareTo` confronta secondo "l'ordine in cui le costanti sono dichiarate". I metodi sintetizzati dal compilatore (`values`, `valueOf(String)`) sono descritti nella specifica del linguaggio, sezione 8.9, a cui la Javadoc rimanda.
>
> *Fonte:* [java.lang.Enum (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Enum.html)

## 4.5 I cicli

Una porzione di programma che si ripete si chiama **ciclo** (*loop*); l'istruzione o il gruppo di istruzioni ripetuto è il **corpo** (*body*) del ciclo. Ogni passaggio nel corpo è un'**iterazione** (o "giro"). Un ciclo deve avere un modo per **finire**: la condizione prima o poi deve diventare falsa, altrimenti il programma gira per sempre (sezione 4.6.5). Java ha tre istruzioni di ciclo: `while`, `do-while`, `for`.

### 4.5.1 while

L'istruzione `while` ripete il corpo **finché una condizione booleana resta vera**. Il controllo avviene **prima** di ogni giro.

```text
while (Espressione_booleana)
    Istruzione_del_corpo
```

oppure, con più istruzioni nel corpo:

```text
while (Espressione_booleana)
{
    Prima_istruzione;
    Seconda_istruzione;
    ...
}
```

L'esecuzione è: (1) si valuta la condizione; (2) se è falsa, si salta il ciclo e si prosegue dopo; (3) se è vera, si esegue il corpo e si torna al punto 1. Il corpo contiene di norma un'azione che prima o poi rende falsa la condizione.

```java
public class Cicli {
    public static void main(String[] args) {
        int count = 1;
        while (count <= 3) {
            System.out.println("Giro " + count);
            count++;
        }
        System.out.println("Fine, count = " + count);

        int zero = 10;
        while (zero < 5) {                 // falsa subito: il corpo non gira mai
            System.out.println("mai stampato");
        }
        System.out.println("zero = " + zero);
    }
}
```

Nel primo ciclo `count` parte da 1; a ogni giro si stampa e si incrementa. Dopo il terzo giro `count` vale 4 e la condizione `count <= 3` diventa falsa: il ciclo finisce e `count` conserva il valore 4. Nel secondo ciclo la condizione è falsa fin dal primo controllo: **il corpo può non essere eseguito mai**. L'output è:

```text
Giro 1
Giro 2
Giro 3
Fine, count = 4
zero = 10
```

### 4.5.2 do-while

L'istruzione `do-while` è simile al `while`, ma controlla la condizione **dopo** ogni giro: quindi il corpo viene eseguito **almeno una volta**.

```text
do
    Istruzione_del_corpo
while (Espressione_booleana);
```

Attenzione al **punto e virgola** dopo la parentesi della condizione: nel `do-while` è obbligatorio (se manca, errore `';' expected`). L'esecuzione è: (1) si esegue il corpo; (2) si valuta la condizione; (3) se è vera si torna al punto 1, altrimenti si esce. Un `do-while` è equivalente a un `while` preceduto da una copia del corpo:

```text
Istruzioni_S1
while (Condizione)
    Istruzioni_S1
```

Un uso tipico è "fai una cosa, poi chiedi se ripetere". Per rendere gli esempi riproducibili leggiamo le risposte da una stringa invece che dalla tastiera: `new Scanner("s s n")` crea uno `Scanner` che produce i token `s`, `s`, `n`, e tutti i metodi (`next`, `nextInt`…) si usano come con `System.in`.

> [!NOTE]
> **Approfondimento esterno — `Scanner(String source)`**
> Oltre a `Scanner(InputStream source)` (sezione 3.7), la classe `java.util.Scanner` ha il costruttore `Scanner(String source)`, che "costruisce un nuovo `Scanner` che produce valori letti dalla stringa specificata". Serve a collaudare un programma senza dover digitare ogni volta l'input.
>
> *Fonte:* [java.util.Scanner (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Scanner.html)

```java
import java.util.Scanner;

public class Almeno {
    public static void main(String[] args) {
        Scanner in = new Scanner("s s n");     // al posto della tastiera: tre risposte già pronte
        int rounds = 0;
        String answer;
        do {
            rounds++;
            System.out.println("Turno " + rounds);
            answer = in.next();                // legge "s", poi "s", poi "n"
            System.out.println("Risposta: " + answer);
        } while (answer.equals("s"));
        System.out.println("Turni giocati: " + rounds);

        int x = 100;
        do {                                   // il corpo gira comunque una volta
            System.out.println("x = " + x);
        } while (x < 5);
    }
}
```

Il primo ciclo continua finché la risposta è `"s"` (si confronta con `equals`, non con `==`): gira tre volte, e il terzo giro legge `"n"` e termina. Nel secondo ciclo la condizione `x < 5` è falsa fin dall'inizio, ma il corpo viene eseguito comunque una volta, a differenza del `while`. Si noti che `answer` è dichiarata **prima** del `do`: se fosse dichiarata dentro il corpo, la condizione, che sta fuori dalle graffe, non la vedrebbe (sezione 4.1.3). L'output è:

```text
Turno 1
Risposta: s
Turno 2
Risposta: s
Turno 3
Risposta: n
Turni giocati: 3
x = 100
```

### 4.5.3 for

L'istruzione `for` esegue il corpo un numero di volte determinato da un contatore: raccoglie in un'unica riga le tre parti che in un ciclo "contato" ci sono sempre, cioè **inizializzazione**, **condizione**, **aggiornamento**.

```text
for (Inizializzazione; Condizione; Aggiornamento)
    Istruzione_del_corpo
```

Le tre parti sono separate da **due punti e virgola**. L'esecuzione è: (1) si esegue l'inizializzazione, **una sola volta**; (2) si valuta la condizione; se è falsa si esce; (3) si esegue il corpo; (4) si esegue l'aggiornamento; (5) si torna al punto 2. È quindi equivalente a:

```text
Inizializzazione;
while (Condizione)
    Corpo_che_include_l_Aggiornamento
```

```java
public class Per {
    public static void main(String[] args) {
        for (int count = 1; count < 3; count++) {
            System.out.println(count);
        }

        int sum = 0;
        for (int n = 1; n <= 10; n++) {
            sum = sum + n * n;                 // somma dei quadrati da 1 a 10
        }
        System.out.println("Somma dei quadrati: " + sum);

        for (int i = 10; i >= 0; i = i - 5) {  // conto alla rovescia di 5 in 5
            System.out.print(i + " ");
        }
        System.out.println();

        int k;
        int product;
        for (k = 1, product = 1; k <= 5; k++) {   // due inizializzazioni, separate da virgola
            product = product * k;
        }
        System.out.println("5! = " + product + ", k = " + k);

        int i = 0;                             // lo stesso ciclo, scritto con while
        while (i < 3) {
            System.out.print("w" + i + " ");
            i++;
        }
        System.out.println();
    }
}
```

Primo ciclo: `count` parte da 1; giro con 1, giro con 2; con 3 la condizione `count < 3` è falsa e il ciclo termina (quindi si stampano solo 1 e 2). Secondo: `n` va da 1 a 10 e accumula `n * n`; la somma dei quadrati è 385. Terzo: l'aggiornamento può essere qualunque assegnamento, qui `i = i - 5`; si stampa 10, 5, 0. Quarto: **l'inizializzazione può contenere più istruzioni separate da virgola**, e anche l'aggiornamento (la condizione, invece, è una sola espressione booleana, anche composta con `&&`, `||`, `!`). Qui `k` e `product` sono dichiarate prima e inizializzate nell'intestazione; alla fine `k` vale 6, perché è l'incremento a portare `k` oltre il limite. Ultimo: l'equivalente `while`, in cui `i` è dichiarata prima e aggiornata nel corpo. L'output è:

```text
1
2
Somma dei quadrati: 385
10 5 0 
5! = 120, k = 6
w0 w1 w2 
```

**Dichiarare la variabile nell'intestazione.** Nel secondo ciclo l'abbiamo scritto con `int n = 1`: la variabile è dichiarata *nell'inizializzazione* ed è **locale al ciclo**, cioè esiste soltanto durante il `for` (sezione 4.1.3). Dopo la `}` finale il nome `n` non esiste più (e si può riusare). Se invece serve il valore finale del contatore dopo il ciclo, come con `k` sopra, la variabile va dichiarata prima.

**Quale ciclo scegliere.** La regola pratica è:

| Situazione | Ciclo |
|---|---|
| Il numero di giri è **noto prima** di iniziare (da 1 a n, per ogni elemento, per `n` volte) | `for` |
| Si ripete **finché** una condizione è vera, e potrebbero servire zero giri | `while` |
| Si deve eseguire il corpo **almeno una volta** e poi decidere | `do-while` |

Tutti e tre sono equivalenti come potenza espressiva: ciò che si scrive con uno si può scrivere con un altro. La scelta riguarda la leggibilità.

### 4.5.4 for-each su un enum

Esiste una seconda forma del `for`, che scorre tutti i valori di un insieme senza usare un contatore. Con gli enum si scrive:

```text
for (TipoEnum variabile : TipoEnum.values())
    Istruzione_del_corpo
```

Si legge "per ogni `variabile` in `TipoEnum.values()`". A ogni giro `variabile` assume una costante, nell'ordine di dichiarazione. Ne abbiamo visto un esempio nel programma `Semafori`: `for (Light l : Light.values())`. Con gli array ([Capitolo 5](05-array-e-matrici.md)) e le collezioni ([Capitolo 12](12-generics-e-collezioni.md)) si scrive nello stesso modo.

### 4.5.5 Cicli annidati

Il corpo di un ciclo può contenere qualunque istruzione, quindi anche un altro ciclo. Per ogni giro del ciclo **esterno**, il ciclo **interno** viene eseguito per intero.

```java
public class Annidati {
    public static void main(String[] args) {
        for (int row = 1; row <= 4; row++) {
            for (int col = 1; col <= row; col++) {
                System.out.print("*");
            }
            System.out.println();
        }

        for (int a = 1; a <= 3; a++) {
            for (int b = 1; b <= 4; b++) {
                System.out.print(a * b + "\t");
            }
            System.out.println();
        }
    }
}
```

Nel primo blocco il ciclo interno gira `row` volte: 1 giro alla prima riga, 2 alla seconda, e così via; `println()` alla fine di ogni giro esterno va a capo. Il totale degli asterischi è 1 + 2 + 3 + 4 = 10. Nel secondo blocco i due cicli producono una tabellina: per ogni `a` si stampano i prodotti `a * b` per `b` da 1 a 4, separati da una tabulazione (`\t`). L'output è:

```text
*
**
***
****
1	2	3	4	
2	4	6	8	
3	6	9	12	
```

Il numero totale di esecuzioni del corpo interno è il **prodotto** (se i limiti sono costanti) o la **somma** (se dipendono dal contatore esterno, come nel primo blocco). Due cicli annidati con lo stesso contatore, ad esempio due `for` con `int i`, non compilano (sezione 4.1.3).

## 4.6 Progettare un ciclo

### 4.6.1 Il corpo e l'inizializzazione

Per scrivere un ciclo si parte dalle azioni che il programma deve compiere, a mano, e si cerca lo **schema che si ripete**. Quello schema sarà il corpo. Lo schema non deve per forza cominciare dalla prima azione, e alcune azioni possono servire una volta sola, dopo l'ultimo giro. Poi bisogna chiedersi: quali variabili devono avere un valore *prima* che il ciclo cominci? Spesso un contatore parte da 0 o 1 e un accumulatore da 0 (o, per un prodotto, da 1), ma non sempre: dipende da cosa succede al primo giro. Altre variabili ricevono un valore solo dentro il ciclo.

### 4.6.2 Quante volte: contatore, domanda, sentinella, flag

Il modo in cui un ciclo si ferma determina la sua forma.

1. **Numero di giri noto**: si usa un `for` con un contatore (*count-controlled loop*).
2. **Chiedere prima di ogni giro** (*ask-before-iterating*): si chiede all'utente se continuare. Va bene per pochi giri. Si usa `while` o `do-while` (sezione 4.5.2).
3. **Valore sentinella** (*sentinel value*): per liste lunghe, un valore speciale segnala la fine dei dati. Deve essere **diverso da tutti i possibili valori veri**: per un elenco di punteggi, che non sono mai negativi, può servire un numero negativo.
4. **Variabile booleana di controllo**: una `boolean` che vale `true` finché si deve continuare e viene portata a `false` quando una condizione si verifica.

Esempio con sentinella. Si leggono punteggi finché non arriva un valore negativo, poi si calcola la media:

```java
import java.util.Scanner;

public class Sentinella {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner("90 0 10 -1");   // -1 è la sentinella
        int sum = 0;
        int count = 0;
        int next = keyboard.nextInt();
        while (next >= 0) {
            sum = sum + next;
            count++;
            next = keyboard.nextInt();
        }
        System.out.println("Letti " + count + " valori, somma " + sum);
        if (count > 0) {
            System.out.println("Media: " + (double) sum / count);
        } else {
            System.out.println("Nessun valore");
        }
    }
}
```

Lo schema è sempre lo stesso: **si legge un valore prima del ciclo**, poi nel `while` lo si elabora e **si legge il successivo come ultima istruzione del corpo**. Così, quando arriva la sentinella, la condizione `next >= 0` la intercetta e il ciclo termina senza elaborarla. Dopo il ciclo l'`if (count > 0)` evita di dividere per zero nel caso di lista vuota. Il cast `(double) sum` è necessario: con due `int` la divisione sarebbe intera (sezione 2.5.2). L'output è:

```text
Letti 3 valori, somma 100
Media: 33.333333333333336
```

Esempio con variabile booleana. Si cerca il primo numero che è multiplo sia di 5 sia di 7:

```java
public class Flag {
    public static void main(String[] args) {
        boolean found = false;
        int n = 1;
        while (!found) {
            if (n % 5 == 0 && n % 7 == 0) {
                found = true;               // il ciclo termina al prossimo controllo
            } else {
                n++;
            }
        }
        System.out.println("Primo multiplo di 5 e 7: " + n);
    }
}
```

`found` parte da `false`; il ciclo gira finché `!found` è vero. Quando `n` raggiunge 35 la condizione interna è vera, `found` diventa `true` e al controllo successivo il ciclo termina; `n` non viene incrementato in quel giro, quindi vale ancora 35. L'output è:

```text
Primo multiplo di 5 e 7: 35
```

### 4.6.3 Un esempio completo: la casa e gli insetti

Mettiamo insieme costanti, ciclo e calcoli. Un'infestazione di insetti cresce del 95% ogni settimana. Ogni insetto occupa 0,002 piedi cubi. Una casa ha un volume di 500 piedi cubi e inizialmente ci sono 100 insetti. Dopo quante settimane il volume totale degli insetti supera quello della casa?

L'algoritmo, a mano: partire dalla popolazione iniziale e dal suo volume; finché il volume degli insetti non supera quello della casa, ripetere: calcolare i nuovi nati (95% della popolazione), aggiungerli, ricalcolare il volume, contare una settimana. Variabili: `GROWTH_RATE` e `ONE_BUG_VOLUME` (costanti, sezione 2.4), `houseVolume`, `population`, `totalBugVolume`, `countWeeks`, `newBugs`.

```java
public class Scarafaggi {
    public static void main(String[] args) {
        final double GROWTH_RATE = 0.95;          // crescita settimanale: 95%
        final double ONE_BUG_VOLUME = 0.002;      // volume di un insetto, in piedi cubi

        double houseVolume = 500;
        int population = 100;                     // insetti iniziali
        double totalBugVolume = population * ONE_BUG_VOLUME;
        int countWeeks = 0;

        while (totalBugVolume <= houseVolume) {
            int newBugs = (int) (population * GROWTH_RATE);
            population = population + newBugs;
            totalBugVolume = population * ONE_BUG_VOLUME;
            countWeeks++;
        }

        System.out.println("Settimane: " + countWeeks);
        System.out.println("Insetti: " + population);
        System.out.println("Volume occupato: " + totalBugVolume);
    }
}
```

La condizione `totalBugVolume <= houseVolume` significa "gli insetti non hanno ancora riempito la casa": il ciclo prosegue finché è vera. Il cast `(int)` tronca i nati alla parte intera, perché non esistono mezzi insetti. Ogni giro cambia `population`, quindi anche `totalBugVolume`: è ciò che prima o poi fa terminare il ciclo. L'output è:

```text
Settimane: 12
Insetti: 301754
Volume occupato: 603.508
```

Se il tasso di crescita fosse zero o negativo, `totalBugVolume` non supererebbe mai `houseVolume` e il ciclo non finirebbe mai (sezione 4.6.5).

### 4.6.4 break e continue

Due istruzioni modificano l'esecuzione normale di un ciclo.

- **`break`** termina **subito** il ciclo (o lo `switch`) che lo contiene e continua con l'istruzione dopo la `}`. Termina soltanto il ciclo **più interno** che lo contiene.
- **`continue`** termina **soltanto il giro corrente** e passa al successivo: in un `for` esegue l'aggiornamento e poi controlla la condizione; in un `while` o `do-while` controlla subito la condizione.

```java
public class BreakContinue {
    public static void main(String[] args) {
        for (int i = 1; i <= 10; i++) {
            if (i % 2 == 0) {
                continue;                   // salta il resto del giro: passa al prossimo i
            }
            if (i > 7) {
                break;                      // esce dal ciclo
            }
            System.out.print(i + " ");
        }
        System.out.println();

        for (int i = 1; i <= 3; i++) {      // break dentro uno switch esce solo dallo switch
            switch (i) {
                case 2:
                    System.out.println("caso 2");
                    break;
                default:
                    System.out.println("altro " + i);
            }
        }
    }
}
```

Nel primo ciclo, i numeri pari fanno scattare `continue` e non vengono stampati; quando `i` arriva a 9 (dispari e maggiore di 7) scatta `break` e il ciclo finisce: si stampano 1, 3, 5, 7. Nel secondo ciclo il `break` si trova dentro uno `switch`: interrompe lo `switch`, non il `for`, che prosegue con i valori successivi. L'output è:

```text
1 3 5 7 
altro 1
caso 2
altro 3
```

> [!WARNING]
> **Attenzione — Usare `break` e `continue` con parsimonia**
> Rendono il ciclo più difficile da leggere, perché il punto di uscita non è più solo nella condizione: vanno usati poco, o per nulla. Un ciclo che si può scrivere con una condizione chiara è quasi sempre preferibile. Hanno però senso, ad esempio, per uscire non appena si trova ciò che si cercava.

### 4.6.5 Cicli infiniti

Un ciclo che si ripete senza mai terminare è un **ciclo infinito** (*infinite loop*). Capita quando la condizione non diventa mai falsa: ad esempio nel caso degli insetti con crescita negativa, oppure quando ci si dimentica di aggiornare il contatore (`while (i < 3) { ... }` senza `i++`).

A volte però si scrive un ciclo infinito **di proposito** con la condizione `true`, e si esce con un `break` quando serve:

```java
import java.util.Scanner;

public class Infinito {
    public static void main(String[] args) {
        Scanner in = new Scanner("4 8 0 15");
        int sum = 0;
        while (true) {                      // condizione sempre vera: si esce solo con break
            int value = in.nextInt();
            if (value == 0) {
                break;
            }
            sum = sum + value;
        }
        System.out.println("Somma fino allo zero: " + sum);
    }
}
```

Il ciclo legge numeri e li somma; quando legge `0` esce con `break`. Il `15` finale non viene mai letto. Anche `for (;;)` (tutte e tre le parti vuote) è un ciclo infinito. L'output è:

```text
Somma fino allo zero: 12
```

Il compilatore sa riconoscere il caso: l'istruzione scritta dopo un `while (true)` privo di `break` è irraggiungibile e dà l'errore `unreachable statement`. Lo stesso errore si ha con le istruzioni scritte subito dopo un `break` o un `return`.

### 4.6.6 Gli errori tipici nei cicli

I bachi più frequenti nei cicli sono quattro.

- **Cicli infiniti involontari**: la condizione non diventa mai falsa (manca l'aggiornamento, è nel verso sbagliato, o è dopo un `continue`).
- **Errori di uno** (*off-by-one*): il ciclo gira una volta di troppo o di meno, di solito per `<` al posto di `<=` o per un contatore che parte da 0 invece che da 1. Per fare 3 giri partendo da 0 la condizione è `i < 3`; con `i <= 3` i giri sono 4.
- **Confronto di uguaglianza tra numeri in virgola mobile** usato per fermare un ciclo: `for (double d = 0; d != 1.0; d += 0.1)` non termina mai, perché sommando dieci volte `0.1` non si ottiene esattamente `1.0`. Si usa `<` o `<=`, oppure si conta con un intero.
- **Cicli infiniti sottili**: il ciclo termina per alcuni dati e per altri no. Ad esempio un programma che deve estinguere un debito quando la penale mensile supera il pagamento mensile: il debito non scende mai.

Prima di consegnare un ciclo conviene provarlo a mano con tre valori: il caso normale, il caso in cui il corpo non gira per niente, e il caso al confine.

## 4.7 Seguire un programma a mano e asserzioni

### 4.7.1 Tracciare le variabili

**Tracciare le variabili** (*tracing*) significa osservare come cambiano mentre il programma gira. È il modo più sicuro per capire un ciclo e per trovare un errore. Si può fare **a mano**, su carta, con una tabella: una colonna per variabile, una riga per giro. Oppure si inseriscono temporaneamente delle stampe (`System.out.println`) per vedere i valori; oppure si usa il debugger dell'ambiente di sviluppo. Alla prova scritta sull'editor semplice resta la tabella a mano.

Tracciamo il metodo `digitSum` che somma le cifre di un numero (il codice completo è nella sezione 4.9). Il ciclo è `while (n > 0) { sum = sum + n % 10; n = n / 10; }` e parte da `n = 4096`, `sum = 0`:

| Giro | `n` prima | `n % 10` | `sum` dopo | `n` dopo (`n / 10`) | `n > 0` ? |
|---|---|---|---|---|---|
| 1 | 4096 | 6 | 6 | 409 | sì |
| 2 | 409 | 9 | 15 | 40 | sì |
| 3 | 40 | 0 | 15 | 4 | sì |
| 4 | 4 | 4 | 19 | 0 | **no** |

Al quarto giro `n` diventa 0, la condizione è falsa e il ciclo termina con `sum = 19`. Se il valore iniziale fosse stato 0, il corpo non sarebbe mai stato eseguito e il metodo avrebbe restituito 0, che è la risposta giusta.

### 4.7.2 Le asserzioni

Un'**asserzione** (*assertion*) è un'affermazione sullo stato del programma che dovrebbe essere vera quando non ci sono errori. In un programma si può scrivere in un commento, per documentare il ragionamento. Java permette di scriverla come istruzione, con la parola chiave `assert`:

```text
assert Espressione_booleana;
assert Espressione_booleana : Espressione_del_messaggio;
```

Se l'espressione è `true` non succede nulla. Se è `false`, il programma si ferma con un `AssertionError`; nella seconda forma il valore dopo i due punti, convertito in stringa, diventa il messaggio dell'errore.

```java
public class Asserzioni {
    public static void main(String[] args) {
        int limit = 20;
        int n = 1;
        assert n == 1;                      // precondizione
        while (n < limit) {
            n = 2 * n;
        }
        assert n >= limit;                  // postcondizione: n è la prima potenza di 2 >= limit
        System.out.println(n);

        int k = 3;
        assert k == 1 : "k doveva valere 1, vale " + k;
        System.out.println("fine");
    }
}
```

Il ciclo raddoppia `n` finché non raggiunge `limit`: parte da 1 e passa per 2, 4, 8, 16, 32, quindi stampa 32. Le prime due asserzioni sono vere. L'ultima, invece, è falsa: `k` vale 3.

**Ma c'è un dettaglio decisivo: per impostazione predefinita le asserzioni sono disattivate**, e il programma le ignora. Lanciato con `java Asserzioni`, il programma stampa:

```text
32
fine
```

Lanciato con l'opzione `-ea` (*enable assertions*), `java -ea Asserzioni`, controlla anche le asserzioni e si ferma alla terza:

```text
32
Exception in thread "main" java.lang.AssertionError: k doveva valere 1, vale 3
	at Asserzioni.main(Asserzioni.java:13)
```

> [!NOTE]
> **Approfondimento esterno — `AssertionError` e lo stato delle asserzioni**
> La Javadoc descrive `AssertionError` come l'errore "lanciato per indicare che un'asserzione è fallita": con `assert espressione1 : espressione2`, l'espressione dopo i due punti diventa il messaggio di dettaglio (il costruttore `AssertionError(Object detailMessage)` ne usa la conversione in stringa). Lo stato di default delle asserzioni dipende dal *class loader* che carica le classi: `ClassLoader.setDefaultAssertionStatus(boolean enabled)` determina se le classi caricate avranno le asserzioni "abilitate o disabilitate per default". L'opzione `-ea` del comando `java` fa parte della documentazione degli strumenti, non della Javadoc delle API.
>
> *Fonte:* [java.lang.AssertionError (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/AssertionError.html)

> [!WARNING]
> **Attenzione — Non mettere in un `assert` ciò che il programma deve fare**
> Poiché di default le asserzioni sono spente, l'espressione di un `assert` **non viene valutata**. Se contiene un effetto collaterale, come `assert (calls++) < 10;`, il programma cambia comportamento a seconda del modo in cui è lanciato: senza `-ea` `calls` resta 0, con `-ea` diventa 1. Un'asserzione serve a controllare, mai a fare. Per validare i dati in ingresso, che deve funzionare sempre, si usa un `if` (sezione 4.2.7).

## 4.8 Terminare il programma: System.exit

Il programma normalmente finisce quando termina il `main`. A volte però si presenta una situazione che rende inutile proseguire (ad esempio un dato non valido). Il metodo `System.exit(int status)` termina subito la JVM; per convenzione lo stato `0` indica una conclusione regolare e uno stato diverso da zero indica una conclusione anomala.

```java
public class Uscita {
    public static void main(String[] args) {
        int payoff = 100;
        int numberOfWinners = 0;
        if (numberOfWinners == 0) {
            System.out.println("Errore: divisione per zero.");
            System.exit(1);
        } else {
            int oneShare = payoff / numberOfWinners;
            System.out.println("Ogni vincitore riceve " + oneShare);
        }
        System.out.println("Questa riga non viene raggiunta");
    }
}
```

Il numero di vincitori è zero, quindi il programma stampa il messaggio d'errore e chiama `System.exit(1)`. Il programma si ferma lì: la riga finale non viene mai stampata e la divisione per zero non viene mai eseguita. Dalla shell, `echo $?` subito dopo mostra lo stato `1`. L'output è:

```text
Errore: divisione per zero.
```

> [!NOTE]
> **Approfondimento esterno — `System.exit`**
> La Javadoc dichiara `public static void exit(int status)`: "termina la Java Virtual Machine attualmente in esecuzione. L'argomento serve da codice di stato; per convenzione un codice diverso da zero indica una terminazione anomala". Il metodo "non ritorna mai normalmente" e `System.exit(n)` equivale a `Runtime.getRuntime().exit(n)`. Può sollevare `SecurityException` se esiste un gestore di sicurezza che non permette l'uscita con quel codice.
>
> *Fonte:* [java.lang.System#exit(int) (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/System.html)

Nei programmi veri si preferisce, quando possibile, far terminare il programma in modo naturale (con `return` o lasciando finire il `main`) e riservare `System.exit` ai casi d'emergenza.

## 4.9 Dal testo dell'esercizio alla struttura di controllo

In una prova scritta si parte da un **testo**, non da uno schema. Il primo passo è tradurre le parole della traccia nel costrutto giusto.

| Nel testo si legge… | Struttura |
|---|---|
| "se… altrimenti", "nel caso in cui", "solo se" | `if` / `else` |
| "se… altrimenti se…", "a seconda della fascia" (intervalli) | `if` / `else if` / `else` (condizioni dalla più restrittiva) |
| "a seconda del comando/giorno/valore" (uguaglianza con costanti) | `switch` |
| "per ogni", "da 1 a n", "n volte", "per tutti i numeri fino a" | `for` |
| "finché", "fino a quando", "mentre" | `while` |
| "ripeti… e poi chiedi", "almeno una volta" | `do-while` |
| "il primo… che", "appena trovi" | ciclo con `return` o `break` (oppure con una variabile `boolean`) |
| "fino a quando si incontra il valore…" | ciclo con valore sentinella |

Il secondo passo è rispettare la **firma e l'output richiesti alla lettera**: nome della classe, nome del metodo, tipi dei parametri e del risultato, `static` se la traccia dice "senza creare un oggetto". Il terzo è pensare ai **casi limite**: valore zero, numero negativo, numero più piccolo, numero più grande.

Esempio nella forma d'esame. Supponiamo che la traccia chieda: "Definire la classe `Cifre` con due metodi statici: `digitSum`, che riceve un intero non negativo e restituisce la somma delle sue cifre decimali; `isPrime`, che riceve un intero e restituisce `true` se è primo (maggiore di 1 e divisibile solo per 1 e per se stesso). Il `main` stampa `digitSum(4096)`, `digitSum(0)` e i numeri primi da 0 a 12 su una sola riga, separati da spazio". L'output atteso:

```text
19
0
2 3 5 7 11 
```

Il testo contiene due cicli e un `if`. `digitSum` non ha un numero noto di giri (dipende dal numero di cifre), quindi serve un `while`: si prende l'ultima cifra con `n % 10`, la si somma, e si toglie con `n / 10`, finché `n` vale 0. `isPrime` ha i giri noti (i possibili divisori), quindi un `for`; si scarta subito `n < 2`, e si esce con `return false` appena si trova un divisore. Basta provare i divisori `d` fino a quando `d * d <= n`, perché se `n` ha un divisore maggiore della sua radice quadrata ne ha anche uno minore.

```java
public class Cifre {
    static int digitSum(int n) {
        int sum = 0;
        while (n > 0) {
            sum = sum + n % 10;     // ultima cifra
            n = n / 10;             // toglie l'ultima cifra
        }
        return sum;
    }

    static boolean isPrime(int n) {
        if (n < 2) {
            return false;
        }
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(digitSum(4096));
        System.out.println(digitSum(0));
        for (int n = 0; n <= 12; n++) {
            if (isPrime(n)) {
                System.out.print(n + " ");
            }
        }
        System.out.println();
    }
}
```

Per `digitSum(4096)` la traccia del ciclo è la tabella della sezione 4.7.1 e il risultato è 19; per `0` il ciclo non gira e si restituisce 0. In `isPrime(9)` il ciclo prova `d = 2` (9 % 2 = 1) e `d = 3` (9 % 3 = 0, quindi `return false`); in `isPrime(2)` e `isPrime(3)` la condizione `d * d <= n` è falsa subito (4 > 2 e 4 > 3) e il ciclo non gira, quindi si arriva a `return true`. Nel `main` il `for` esterno prova i numeri da 0 a 12 e stampa soltanto quelli per cui `isPrime` dà `true`; `print` (senza `ln`) li tiene sulla stessa riga e il `println()` finale va a capo. L'output è:

```text
19
0
2 3 5 7 11 
```

Notiamo che il testo non dice cosa fare con un numero negativo in `digitSum`: il nostro `while (n > 0)` restituirebbe 0. Una traccia vera lo specifica; quando non lo dice, non si inventano comportamenti.

## Errori tipici

> [!CAUTION]
> **Errore tipico — `=` al posto di `==` in una condizione**
> ```java
> int x = 5;
> if (x = 5) { }                 // ERRORE DI COMPILAZIONE
> boolean b = false;
> if (b = true) { }              // COMPILA, ma è un errore logico
> ```
> Con un `int` il compilatore risponde `incompatible types: int cannot be converted to boolean`, perché `x = 5` è un assegnamento che vale 5, non una condizione. Con un `boolean` invece **compila**: `b = true` assegna `true` a `b` e l'espressione vale `true`, quindi il ramo viene eseguito sempre. Forma corretta: `if (x == 5)`; per un booleano `if (b)`.

> [!CAUTION]
> **Errore tipico — Punto e virgola subito dopo `if`, `for` o `while`**
> ```java
> int total = 0;
> for (int i = 0; i < 3; i++);       // ERRORE LOGICO: il corpo è l'istruzione vuota ;
> { total++; }                       // viene eseguito una volta sola, dopo il ciclo
> System.out.println(total);         // stampa 1, non 3
> ```
> Il `;` è un'istruzione vuota: diventa il corpo del ciclo, e il blocco successivo è un'istruzione a sé. Il programma compila e stampa `1`. Con `while (j < 3);` e `j` che cambia nel blocco dopo, il programma non termina mai. Lo stesso accade con `if (x > 5);`, che esegue sempre il blocco successivo. Forma corretta: nessun `;` dopo la parentesi della condizione.

> [!CAUTION]
> **Errore tipico — Graffe mancanti: il corpo è solo la prima istruzione**
> ```java
> int n = 3;
> if (n > 2)
>     System.out.println("A");
>     System.out.println("B");       // ERRORE LOGICO: fuori dall'if, viene sempre stampata
> ```
> L'indentazione inganna l'occhio, non il compilatore: il corpo dell'`if` è soltanto la prima `println`, la seconda viene eseguita sempre. Forma corretta: mettere sempre le graffe quando le istruzioni sono più di una, e meglio sempre.

> [!CAUTION]
> **Errore tipico — Else che si aggancia all'`if` sbagliato**
> ```java
> if (a > b)
>     if (c > d)
>         e = f;
> else                               // ERRORE LOGICO: appartiene all'if (c > d), non all'if (a > b)
>     g = h;
> ```
> L'`else` si lega sempre all'`if` più vicino senza `else`, qualunque sia l'indentazione (sezione 4.2.3). Se l'intenzione era legarlo all'`if` esterno, serve un blocco: `if (a > b) { if (c > d) e = f; } else g = h;`.

> [!CAUTION]
> **Errore tipico — Condizioni di una catena nell'ordine sbagliato**
> ```java
> if (score >= 60) return 'D';
> else if (score >= 90) return 'A';  // ERRORE LOGICO: non viene mai raggiunta
> else return 'F';
> ```
> Con 95 la prima condizione è già vera, quindi il metodo restituisce `'D'`. Le condizioni di una catena vanno scritte dalla più restrittiva (`>= 90`) alla meno restrittiva (`>= 60`).

> [!CAUTION]
> **Errore tipico — Più valori confrontati con un solo `==`**
> ```java
> if (x == 1 || 2) { }               // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `bad operand types for binary operator '||'` (primo operando `boolean`, secondo `int`): ogni lato di `||` deve essere una condizione completa. Forma corretta: `if (x == 1 || x == 2)`. Lo stesso vale per `0 < x <= 100`, che va scritto `0 < x && x <= 100`.

> [!CAUTION]
> **Errore tipico — Usare una variabile fuori dal suo blocco**
> ```java
> if (x > 0) {
>     int y = 2;
> }
> System.out.println(y);             // ERRORE DI COMPILAZIONE: cannot find symbol
> for (int i = 0; i < 3; i++) { }
> System.out.println(i);             // ERRORE DI COMPILAZIONE: cannot find symbol
> ```
> `y` esiste solo dentro le graffe del `if`, e `i` solo durante il `for`. Se il valore serve dopo, la variabile va dichiarata **prima** del blocco o del ciclo.

> [!CAUTION]
> **Errore tipico — Dichiarare di nuovo una variabile già visibile**
> ```java
> int x = 1;
> if (x > 0) {
>     int x = 2;                     // ERRORE DI COMPILAZIONE
> }
> ```
> Il compilatore risponde `variable x is already defined in method main(String[])`. In un blocco interno non si può dichiarare un nome già in uso in un blocco che lo contiene. Forma corretta: un nome diverso, oppure semplicemente `x = 2;` per modificare la stessa variabile.

> [!CAUTION]
> **Errore tipico — Variabile assegnata solo in alcuni rami**
> ```java
> int n;
> int a = 2;
> if (a > 1) { n = 5; }
> System.out.println(n);             // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `variable n might not have been initialized`: se la condizione fosse falsa, `n` resterebbe senza valore (sezione 2.1.3). Forma corretta: inizializzare `n` alla dichiarazione, oppure assicurarsi che ogni ramo (anche un `else`) le assegni un valore.

> [!CAUTION]
> **Errore tipico — Dimenticare il `break` in uno `switch`**
> ```java
> switch (level) {
>     case 1: System.out.println("uno");      // ERRORE LOGICO: senza break si cade nel case 2
>     case 2: System.out.println("due");
> }
> ```
> Con `level` uguale a 1 si stampano sia "uno" sia "due" (e, se ci fossero, tutti i rami successivi, `default` compreso). Compila senza avvisi. Forma corretta: un `break;` alla fine di ogni ramo, tranne quando si vuole davvero il fall-through (sezione 4.3.2).

> [!CAUTION]
> **Errore tipico — Etichette di `switch` non valide**
> ```java
> int k = 2;
> switch (a) { case k: break; }                  // ERRORE: constant expression required
> switch (a) { case 1: break; case 1: break; }   // ERRORE: duplicate case label
> switch (longValue) { case 3: break; }          // ERRORE: selector type long is not allowed
> switch (light) { case Light.RED: break; }      // ERRORE: etichetta enum qualificata
> ```
> Le etichette devono essere costanti e diverse tra loro; l'espressione di controllo non può essere `long`, `double` o `boolean`; per un enum si scrive `case RED:`, non `case Light.RED:`. I messaggi esatti sono nelle sezioni 4.3.3 e 4.4.2.

> [!CAUTION]
> **Errore tipico — Dimenticare il `;` finale del `do-while`**
> ```java
> int i = 0;
> do { i++; } while (i < 3)          // ERRORE DI COMPILAZIONE: ';' expected
> System.out.println(i);
> ```
> A differenza di `while` e `for`, il `do-while` termina con un punto e virgola dopo la condizione. Forma corretta: `while (i < 3);`.

> [!CAUTION]
> **Errore tipico — Virgole al posto dei punti e virgola nel `for`**
> ```java
> for (int i = 0; i < n, i++) { }    // ERRORE DI COMPILAZIONE: ';' expected
> ```
> Le tre parti dell'intestazione si separano con **due punti e virgola**: `for (int i = 0; i < n; i++)`. La virgola serve solo per elencare più istruzioni *dentro* la stessa parte (`for (a = 0, b = 10; a < b; a++, b--)`).

> [!CAUTION]
> **Errore tipico — Ciclo che gira una volta di troppo (o di meno)**
> ```java
> for (int i = 0; i <= 3; i++) {     // ERRORE LOGICO: 4 giri
>     System.out.print("x");
> }
> ```
> Stampa `xxxx`, non `xxx`. Partendo da 0, per fare `n` giri la condizione è `i < n`; partendo da 1 è `i <= n`. Un `<=` al posto di `<` è anche la causa delle uscite dai limiti di una stringa o di un array all'ultimo giro (sezione 3.1.3).

> [!CAUTION]
> **Errore tipico — Ciclo che non cambia mai la condizione**
> ```java
> int i = 0;
> while (i < 10) {
>     if (i % 2 == 0) {
>         continue;                  // ERRORE LOGICO: salta anche i++ e i resta 0 per sempre
>     }
>     i++;
> }
> ```
> `continue` salta il resto del corpo, compreso l'aggiornamento: `i` resta 0 e il ciclo non termina. Nel `for` questo non succede, perché l'aggiornamento è nell'intestazione e viene eseguito comunque. Forma corretta: aggiornare prima del `continue`, oppure usare un `for`.

> [!CAUTION]
> **Errore tipico — Fermare un ciclo con un `==` tra `double`**
> ```java
> for (double d = 0; d != 1.0; d += 0.1) { }   // ERRORE LOGICO: non termina mai
> ```
> Sommando dieci volte `0.1` non si ottiene esattamente `1.0` (sezione 2.2.3), quindi `d != 1.0` resta sempre vera. Forma corretta: `d < 1.0`, o meglio un contatore intero e `d = i * 0.1`.

> [!CAUTION]
> **Errore tipico — `break` dentro uno `switch` dentro un ciclo**
> ```java
> for (int i = 0; i < 5; i++) {
>     switch (i) {
>         case 2: break;             // ERRORE LOGICO: esce dallo switch, non dal for
>         default: System.out.println(i);
>     }
> }
> ```
> `break` termina soltanto la struttura più interna che lo contiene, qui lo `switch`: il `for` continua. Per uscire dal ciclo bisogna usare `break` fuori dallo `switch`, oppure `return` in un metodo.

> [!CAUTION]
> **Errore tipico — Codice dopo un `break`, un `return` o un ciclo infinito**
> ```java
> while (true) { }
> System.out.println("mai");         // ERRORE DI COMPILAZIONE: unreachable statement
> ```
> Il compilatore rifiuta le istruzioni che non possono mai essere eseguite. Lo stesso accade scrivendo una riga subito dopo un `break` o un `return` nello stesso blocco.

> [!CAUTION]
> **Errore tipico — Effetti collaterali dentro un `assert`**
> ```java
> int calls = 0;
> assert (calls++) < 10;             // ERRORE LOGICO: con le asserzioni spente calls++ non viene eseguito
> System.out.println(calls);         // 0 senza -ea, 1 con -ea
> ```
> Un'asserzione deve solo verificare, mai modificare lo stato (sezione 4.7.2).

## Riassunto

Un programma esegue le istruzioni in sequenza, e le strutture di controllo permettono di cambiare questo ordine. Le **ramificazioni** scelgono una strada in base a una condizione booleana: `if-else` per due vie, `else if` per più vie su intervalli, `switch` per più vie su valori costanti. I **cicli** ripetono un corpo: `while` controlla prima, `do-while` dopo (almeno un giro), `for` raccoglie inizializzazione, condizione e aggiornamento per i cicli con un numero di giri noto. Le **graffe** raggruppano più istruzioni in un blocco, e una variabile dichiarata in un blocco esiste solo fino alla sua `}`. Le **enumerazioni** danno nome a un insieme chiuso di valori e si usano con `switch` e con il `for` a elenco su `values()`. Per progettare e collaudare un ciclo si ragiona su cosa si ripete, su come si inizializza e su come termina; si traccia a mano con una tabella; si controllano i casi limite; e per un controllo interno si può usare `assert`, ricordando che di default è spento.

**Concetti chiave**

- **Flusso sequenziale e di controllo.** Il flusso è sequenziale finché una ramificazione o un ciclo non lo cambia; ogni condizione è un'espressione `boolean`.
- **Blocco e visibilità.** Le graffe formano un'istruzione composta; una variabile dichiarata in un blocco vive dalla dichiarazione alla `}` e non può riusare un nome già visibile.
- **`if-else` e `else if`.** Le condizioni di una catena si valutano dall'alto e vince la prima vera; vanno scritte dalla più restrittiva. L'`else` si lega all'`if` più vicino senza `else`.
- **Confronti nelle condizioni.** `==` per interi e caratteri; tolleranza per i `double`; `equals` per le stringhe; mai `=` al posto di `==`.
- **`switch`.** Seleziona su interi, caratteri, stringhe o enum con etichette costanti e diverse; dopo l'etichetta trovata si prosegue fino a un `break` (fall-through); `default` raccoglie gli altri casi.
- **`enum`.** Tipo con costanti elencate; `values()`, `valueOf`, `name()`, `ordinal()`; nelle etichette di `switch` si scrive il nome semplice.
- **`while`, `do-while`, `for`.** Il primo può non girare mai, il secondo gira almeno una volta e vuole il `;` finale, il terzo ha tre parti separate da `;` e la variabile dichiarata nell'intestazione è locale al ciclo.
- **Come si ferma un ciclo.** Contatore, domanda all'utente, valore sentinella, variabile booleana. Un ciclo la cui condizione non cambia mai è infinito.
- **`break` e `continue`.** `break` esce dal ciclo o dallo `switch` più interno; `continue` salta al giro successivo (nel `while` salta anche l'aggiornamento se questo è nel corpo).
- **Tracing.** Una tabella a mano con una riga per giro mostra come cambiano le variabili e rivela gli errori di uno.
- **`assert`.** Verifica una condizione che deve essere vera; di default è disattivata (si attiva con `java -ea`); non deve avere effetti collaterali.
- **`System.exit(status)`.** Termina subito la JVM; stato `0` per la conclusione regolare, diverso da zero per l'anomala.

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `System` | `exit` | `static void exit(int status)` | `SecurityException` |
| `Enum` (ogni `enum`) | `name`, `ordinal`, `toString` | `final String name()`, `final int ordinal()`, `String toString()` | — |
| `Enum` (ogni `enum`) | `compareTo` | `final int compareTo(E o)` | — |
| ogni `enum` `E` | `values`, `valueOf` | `static E[] values()`, `static E valueOf(String name)` | `IllegalArgumentException` (`valueOf`) |
| `Scanner` | costruttore | `Scanner(String source)` | — |
| `Math` | `abs` | `static int abs(int a)`, `static double abs(double a)` | — |
| `AssertionError` | costruttore | `AssertionError(Object detailMessage)` | — |
