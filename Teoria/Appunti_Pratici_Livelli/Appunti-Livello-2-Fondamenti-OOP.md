# Livello 2: Fondamenti OOP (Programmazione Orientata agli Oggetti)

## 1. Classe vs Oggetto e Incapsulamento

### Teoria Fondamentale: Astrazione e Information Hiding
La Programmazione Orientata agli Oggetti (OOP) modella il software come un insieme di entità autonome (Oggetti) che interagiscono tra loro.
- **Classe**: Il blueprint (progetto) che definisce attributi e metodi.
- **Oggetto**: L'istanza concreta creata in memoria (Heap).
- **Incapsulamento**: Protezione dello stato interno tramite modificatori di accesso (`private`) e metodi pubblici (`getter`/`setter`).

### Esempio: Gestione di un Libro
```java
public class Libro {
    private String titolo;
    private String autore;
    private int pagine;

    // Costruttore
    public Libro(String titolo, String autore, int pagine) {
        this.titolo = titolo;
        this.autore = autore;
        setPagine(pagine); // Validazione tramite setter
    }

    // Getter e Setter con validazione
    public void setPagine(int pagine) {
        if (pagine > 0) {
            this.pagine = pagine;
        } else {
            System.out.println("Errore: il numero di pagine deve essere positivo.");
        }
    }

    public void mostraDettagli() {
        System.out.println("Libro: " + titolo + " | Autore: " + autore + " | Pagine: " + pagine);
    }
}
```

### Il Privacy Leak: quando `private` non basta
Rendere un campo `private` protegge il **riferimento**, non l'**oggetto puntato**. Se un getter restituisce un campo di tipo classe (un array, una `ArrayList`, un oggetto qualunque), il chiamante riceve l'indirizzo dell'oggetto vero e da lì può modificarlo, scavalcando ogni setter con validazione.

```java
public class Squadra {
    private String nome;
    private ArrayList<String> giocatori;

    // FUGA DI PRIVACY: restituisce il riferimento alla lista interna.
    public ArrayList<String> getGiocatori() {
        return giocatori;
    }
}

// Dall'esterno:
Squadra s = new Squadra("Messina");
s.getGiocatori().clear();     // ha appena svuotato lo stato interno di s
```

Il campo era `private`, i setter validavano, e l'incapsulamento è stato aggirato lo stesso. Le difese, in ordine di frequenza d'uso:

```java
// 1. Restituire una COPIA (difesa più comune)
public ArrayList<String> getGiocatori() {
    return new ArrayList<>(giocatori);
}

// 2. Restituire una vista non modificabile
public List<String> getGiocatori() {
    return Collections.unmodifiableList(giocatori);
}

// 3. Non restituire affatto la struttura: esporre solo ciò che serve
public int numeroGiocatori()      { return giocatori.size(); }
public String giocatore(int i)    { return giocatori.get(i); }
```

Lo stesso vale **in entrata**: un costruttore o un setter che si limita ad assegnare un array ricevuto dall'esterno lascia al chiamante un riferimento vivo sullo stato interno. La difesa è simmetrica: copiare in ingresso.

> **Perché conta all'esame.** "Rispettare rigorosamente l'information hiding" è un vincolo che ricorre in quasi tutte le tracce. Con i tipi primitivi (`int`, `double`) e con le `String` — che sono **immutabili**, quindi non modificabili da chi le riceve — bastano `private` più getter. Con array, liste e oggetti mutabili, un getter ingenuo è una falla.

### I metodi ereditati da `Object`: `toString`, `equals`, `hashCode`
Ogni classe Java discende da `Object` e ne eredita tre metodi che quasi sempre vanno riscritti.

**`toString()`** — definisce come l'oggetto si stampa. Senza override, `System.out.println(oggetto)` produce qualcosa come `Persona@1b6d3586` (nome della classe e codice hash), praticamente inutile. Viene invocato **automaticamente** dentro le concatenazioni di stringhe e da `println`: è per questo che le tracce lo chiedono indicando "la sua rappresentazione testuale è nella forma …".

```java
@Override
public String toString() {
    return "Persona[" + nome + " " + cognome + "]";
}
```

**`equals(Object)`** — definisce quando due oggetti sono "uguali". Senza override, `equals` confronta gli **indirizzi**, esattamente come `==`: due oggetti con gli stessi valori risultano diversi.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;                       // stessa istanza
    if (o == null || getClass() != o.getClass()) return false;
    Persona altra = (Persona) o;                      // cast dopo il controllo di tipo
    return nome.equals(altra.nome) && cognome.equals(altra.cognome);
}
```

**`hashCode()`** — va riscritto **insieme** a `equals`: il contratto Java impone che due oggetti uguali secondo `equals` restituiscano lo stesso `hashCode`. Chi non lo rispetta ottiene una classe che si comporta in modo scorretto dentro `HashMap` e `HashSet` (l'oggetto viene inserito e poi non si ritrova più).

```java
@Override
public int hashCode() {
    return Objects.hash(nome, cognome);   // java.util.Objects
}
```

> **`==` contro `.equals()` sulle `String`.** `==` confronta i riferimenti, `.equals()` il contenuto. Due stringhe con lo stesso testo possono stare in due oggetti diversi (tipico quando una arriva da input o da un file), e `==` restituisce `false` mentre il testo è identico. **Sulle stringhe si usa sempre `.equals()`.**

---

## 2. Variabili di Classe (Static) e Costanti

### Teoria Fondamentale: Stato Condiviso
- **`static`**: Una variabile o un metodo marcato come statico appartiene alla Classe, non alle singole istanze. Viene condiviso da tutti gli oggetti.
- **`final`**: Definisce una costante il cui valore non può essere cambiato dopo l'assegnazione.

### Esempio: Registro Cittadini
```java
public class Cittadino {
    // Variabile statica per contare la popolazione totale
    private static int popolazioneTotale = 0;
    
    // Costante universale
    public static final String SPECIE = "Homo Sapiens";

    private String nome;

    public Cittadino(String nome) {
        this.nome = nome;
        popolazioneTotale++; // Incremento condiviso
    }

    public static int getPopolazione() {
        return popolazioneTotale;
    }
}
```

---

## 3. Collezioni Dinamiche (ArrayList)

### Teoria Fondamentale: Liste Ridimensionabili
`ArrayList` è una classe del framework Collections che implementa un array dinamico. A differenza degli array primitivi, può cambiare dimensione a runtime e offre metodi pronti all'uso come `add()`, `remove()`, `size()` e `contains()`.

### Esempio: Registro Partecipanti
```java
import java.util.ArrayList;

public class Registro {
    public static void main(String[] args) {
        ArrayList<String> partecipanti = new ArrayList<>();

        partecipanti.add("Marco");
        partecipanti.add("Giulia");
        partecipanti.add("Antonio");

        System.out.println("Numero iscritti: " + partecipanti.size());
        
        // Rimozione
        partecipanti.remove("Antonio");

        // Iterazione con for-each
        for (String p : partecipanti) {
            System.out.println("Partecipante: " + p);
        }
    }
}
```

### Wrapper e Autoboxing: perché `ArrayList<int>` non esiste
Le collezioni Java memorizzano **solo oggetti**, mai tipi primitivi. Per ogni primitivo esiste quindi una classe involucro (*wrapper*):

| Primitivo | `int` | `double` | `char` | `boolean` | `long` | `float` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Wrapper | `Integer` | `Double` | `Character` | `Boolean` | `Long` | `Float` |

`ArrayList<int>` **non compila**: si scrive `ArrayList<Integer>`. La conversione avanti e indietro però è automatica, e si chiama *autoboxing* (primitivo → wrapper) e *unboxing* (wrapper → primitivo):

```java
ArrayList<Integer> numeri = new ArrayList<>();
numeri.add(5);                  // autoboxing: 5 diventa Integer.valueOf(5)
int primo = numeri.get(0);      // unboxing: l'Integer torna int
int somma = numeri.get(0) + 3;  // unboxing automatico dentro l'espressione
```

I wrapper portano con sé i metodi di conversione più usati, tutti statici:

```java
int n = Integer.parseInt("42");        // String -> int   (NumberFormatException se non è un numero)
double d = Double.parseDouble("3.14");
String s = String.valueOf(42);         // int -> String
```

> **Due trappole.** `Integer.parseInt` lancia una `NumberFormatException` (unchecked) su input non numerico: va prevista quando i dati arrivano da file, rete o utente. E su due `Integer` va usato `.equals()`, non `==`: sopra il valore 127 la cache dei wrapper non interviene e il confronto per riferimento fallisce anche a valori identici.

### Iterare una collezione: `for-each`, `Iterator`, `Iterable`
Ci sono tre modi di scorrere una collezione, e conviene sapere che sono lo stesso meccanismo.

```java
// 1. for-each: la forma da usare quasi sempre
for (String p : partecipanti) {
    System.out.println(p);
}

// 2. Iterator esplicito: l'unico modo per rimuovere durante la scansione
Iterator<String> it = partecipanti.iterator();
while (it.hasNext()) {
    String p = it.next();
    if (p.startsWith("A")) {
        it.remove();          // rimozione sicura
    }
}

// 3. indice: possibile su List, non su Set
for (int i = 0; i < partecipanti.size(); i++) { ... }
```

Il `for-each` **è** un `Iterator`: il compilatore lo riscrive nella forma 2. Funziona su qualunque tipo che implementi l'interfaccia `Iterable`, cioè su tutte le collezioni e sugli array.

> **`ConcurrentModificationException`.** Modificare la collezione (`add`/`remove` sulla lista) mentre la si sta scorrendo con un `for-each` provoca questa eccezione a runtime. È la ragione per cui `Iterator` espone `remove()`: rimuovere attraverso l'iteratore è l'unico modo sicuro di cancellare elementi durante la scansione.

---

## 4. Classi Annidate (Nested Classes) e Inner Classes

### Teoria Fondamentale: annidare non è ereditare
Una **classe annidata** è una classe dichiarata dentro il corpo di un'altra classe. È un meccanismo di **incapsulamento e di scope**, non di ereditarietà: serve a dire che un tipo ha senso solo dentro un altro tipo.

È il punto in cui si sbaglia più spesso, perché due costrutti diversi rispondono a due domande diverse:

| | La domanda | La sintassi |
| :--- | :--- | :--- |
| **Ereditarietà** | `Offerta` **è una** `Asta`? (relazione IS-A) | `class Offerta extends Asta` |
| **Classe annidata** | `Offerta` **vive dentro** una `Asta`? (relazione di appartenenza) | `class Offerta` scritta dentro il corpo di `Asta` |

Un'offerta non *è* un'asta: *appartiene* a un'asta. Scrivere `extends` per ottenere l'annidamento è un errore doppio — concettuale e di compilazione (vedi "Errori comuni" a fine sezione).

### Le quattro forme di classe annidata
```java
class Esterna {
    class Membro { }               // 1. INNER CLASS (membro, NON statica)
    static class Statica { }       // 2. STATIC NESTED CLASS
    void metodo() {
        class Locale { }           // 3. CLASSE LOCALE (visibile solo nel metodo)
        Runnable r = new Runnable() {   // 4. CLASSE ANONIMA (definita e istanziata in un colpo)
            public void run() { }
        };
    }
}
```
Nel linguaggio della materia, **"inner class" indica solo la forma 1**: classe membro **senza** `static`. Le altre tre sono classi annidate, ma non "inner" in senso stretto.

### Il privilegio dell'inner class: il riferimento implicito all'oggetto esterno
È l'unica cosa che davvero distingue una inner class da una classe qualunque, ed è tutta la ragione per cui esiste.

**Ogni oggetto di una inner class porta con sé, in modo invisibile e automatico, un riferimento all'oggetto della classe esterna che l'ha creato.** Non lo dichiari tu: c'è già, la JVM lo inserisce come campo nascosto (lo vedresti come `this$0` ispezionando il bytecode).

Conseguenze pratiche, tutte e tre importanti:

1. Dentro l'inner class puoi **leggere e scrivere i campi privati dell'oggetto esterno** chiamandoli per nome, come fossero tuoi. Non servono getter, non serve passare niente al costruttore.
2. Se un nome è ambiguo (stesso identificatore nell'interna e nell'esterna), l'oggetto esterno si nomina esplicitamente con `Esterna.this.campo`.
3. **Non può esistere un oggetto interno senza un oggetto esterno.** Perciò dall'esterno non si scrive `new Esterna.Interna(...)`, ma:

```java
Esterna e = new Esterna();
Esterna.Interna i = e.new Interna();   // sintassi 'oggetto.new': dice QUALE esterna
```

La sintassi `e.new` esiste esattamente per fornire quell'oggetto esterno. Dentro la classe esterna, invece, `new Interna()` basta: l'oggetto esterno è `this`, implicito.

### Esempio 1: inner class che manipola lo stato dell'oggetto esterno
Un'asta con le sue offerte. `Offerta` è annidata e non statica, quindi può aggiornare direttamente `quota` e `nomeMigliorOfferente`, che sono privati di `Asta`.

```java
class Asta {
    // Information hiding: nessuno tocca questi campi dall'esterno.
    private String codiceAsta;
    private double quota;
    private String nomeMigliorOfferente;

    public Asta(String codiceAsta, double quota, String nomeMigliorOfferente) {
        this.codiceAsta = codiceAsta;
        this.quota = quota;
        this.nomeMigliorOfferente = nomeMigliorOfferente;
    }

    // INNER CLASS: dentro il corpo di Asta e SENZA static. Nient'altro serve.
    // Niente extends, e nessun campo 'private Asta asta;' dichiarato a mano:
    // sarebbe rifare peggio ciò che il linguaggio fa già da solo.
    public class Offerta {
        private String nomeOfferente;
        private double quotaOfferta;

        public Offerta(String nomeOfferente, double quotaOfferta) {
            this.nomeOfferente = nomeOfferente;
            this.quotaOfferta = quotaOfferta;
        }

        // 'quota' e 'nomeMigliorOfferente' sono campi PRIVATI di Asta,
        // eppure qui si leggono per nome: è il riferimento implicito all'oggetto esterno.
        public String stato() {
            return "Asta " + codiceAsta + " a " + quota + " euro, miglior offerente " + nomeMigliorOfferente;
        }

        public boolean aggiungiOfferta(double importo) {
            if (importo < quota) {
                return false;                       // offerta troppo bassa: rifiutata
            }
            quota = importo;                        // scrive nell'oggetto Asta esterno
            nomeMigliorOfferente = nomeOfferente;   // idem
            return true;
        }
    }
}

// Uso dall'esterno
class Banditore {
    public static void main(String[] args) {
        Asta asta = new Asta("A-100", 100.0, "nessuno");

        Asta.Offerta mario = asta.new Offerta("Mario", 150.0);   // NON new Asta.Offerta(...)
        System.out.println(mario.aggiungiOfferta(50.0));         // false: sotto la quota
        System.out.println(mario.aggiungiOfferta(150.0));        // true: quota aggiornata

        // Una seconda offerta sulla STESSA asta vede lo stato già aggiornato:
        Asta.Offerta luca = asta.new Offerta("Luca", 150.0);
        System.out.println(luca.stato());   // Asta A-100 a 150.0 euro, miglior offerente Mario
    }
}
```

### Esempio 2: inner class privata come dettaglio implementativo
L'altro uso classico: nascondere del tutto un tipo di supporto che al mondo esterno non deve nemmeno essere visibile.

```java
public class Smartwatch {
    private String marca;
    private Batteria batteria;

    public Smartwatch(String marca) {
        this.marca = marca;
        this.batteria = new Batteria();   // dentro Asta/Smartwatch basta 'new Interna()'
    }

    // Classe interna PRIVATA: esiste solo per Smartwatch, invisibile fuori da qui.
    private class Batteria {
        private int percentuale = 100;

        public void scarica() {
            percentuale -= 10;
            if (percentuale <= 20) {
                // Legge un campo privato dell'oggetto Smartwatch esterno.
                System.out.println(marca + ": batteria quasi scarica.");
            }
        }
    }

    public void usa() {
        batteria.scarica();
        System.out.println(marca + " in uso...");
    }
}
```

> **Attenzione: `private` e `esterna.new Interna()`.** Qui la inner class è `private` perché **nessuno fuori da `Smartwatch` deve crearla**: la crea `Smartwatch` stesso con `new Batteria()`. Se invece la traccia (o il suo esempio di output) crea la classe annidata **da fuori**, con `p.new Lettore()` nel `main`, la classe **non può essere `private`**: `Playlist.Lettore has private access in Playlist` e il programma non compila. Regola: leggi *chi* crea la classe annidata. Se è la classe esterna, `private` va bene; se è il `main` o un'altra classe, nessun modificatore (o `public`).

### Quando invece serve `static`
Una **static nested class** è annidata solo per organizzazione: **non** ha il riferimento all'oggetto esterno, quindi non può toccarne i campi d'istanza, e si istanzia come una classe normale.

```java
class Mappa {
    private int scala;

    static class Punto {          // static: nessun legame con una specifica Mappa
        private int x, y;
        Punto(int x, int y) { this.x = x; this.y = y; }
        // int errore() { return scala; }   // NON COMPILA: 'scala' è d'istanza
    }
}

Mappa.Punto p = new Mappa.Punto(3, 4);   // niente 'oggetto.new': non serve un'esterna
```

Regola di scelta: **se la classe annidata deve lavorare sui dati dell'oggetto esterno, è inner (non statica); se è solo un tipo di supporto autonomo, è static nested.**

| | Inner class (`class X`) | Static nested (`static class X`) |
| :--- | :--- | :--- |
| Riferimento all'oggetto esterno | **Sì**, implicito | No |
| Accede ai campi d'istanza privati dell'esterna | **Sì** | No (solo ai `static`) |
| Come si istanzia dall'esterno | `esterna.new X()` | `new Esterna.X()` |
| Può esistere senza un oggetto esterno | No | Sì |

### Errori Comuni
- **`class Offerta extends Asta` per "renderla interna".** `extends` non c'entra con l'annidamento. Oltre a essere concettualmente sbagliato, spesso **non compila**: il costruttore della sottoclasse invoca implicitamente `super()`, cioè un costruttore senza argomenti della classe esterna che di solito non esiste. Il messaggio è `constructor Asta in class Asta cannot be applied to given types; required: ... found: no arguments`.
- **Mettere `static` quando la traccia chiede una inner class.** Sembra innocuo e compila, ma spegne l'unica funzione del costrutto: la classe non vede più i campi d'istanza dell'esterna, e `esterna.new X()` smette di funzionare.
- **Dichiarare a mano `private Asta asta;` dentro la classe interna.** È il segno che non si sta usando il riferimento implicito. Funziona, ma raddoppia lo stato e tradisce il senso dell'esercizio: molte tracce lo vietano esplicitamente.
- **`new Esterna.Interna(...)` su una inner class non statica.** Non compila: manca l'istanza esterna. Serve `esterna.new Interna(...)`.
- **Dimenticare che l'inner class vede i campi *privati* dell'esterna e viceversa.** È legale e voluto: l'incapsulamento in Java è a livello di *classe di primo livello*, non di singola classe annidata.
- **`private class Lettore` quando la traccia fa `p.new Lettore()` dal `main`.** Compila solo se il `main` sta dentro la classe esterna; altrimenti `Lettore has private access`. La traccia non chiede `private`: non aggiungerlo. Un tester già compilato non se ne accorge, ma un test scritto in sorgente sì.
- **`public` su una classe annidata o su una seconda classe dello stesso file.** All'appello tutte le classi stanno in un solo file: nessuna è `public` (Livello 1 §9).

---

## 5. Mappe (Map, HashMap, TreeMap)

### Teoria Fondamentale: Strutture Chiave-Valore
In Java, l'interfaccia `Map` (come ad esempio `HashMap`, `TreeMap`) rappresenta una struttura dati del framework *Collections* che memorizza coppie di **Chiave-Valore** (Key-Value). A differenza delle liste (come `ArrayList`), i dati non sono indicizzati da un numero sequenziale, ma da una chiave univoca che permette di recuperare il valore associato in modo efficiente.

- **`HashMap`**: È l'implementazione più utilizzata. L'accesso e l'inserimento sono estremamente veloci, ma non garantisce alcun ordine specifico degli elementi inseriti.
- **`TreeMap`**: Mantiene le chiavi sempre ordinate (es. in ordine alfabetico o numerico naturale), ma le operazioni di inserimento/ricerca sono leggermente più lente rispetto all'`HashMap`.

### Esempio: Registro Voti (Mappa String -> Integer)
```java
import java.util.HashMap;
import java.util.Map;

public class RegistroVoti {
    public static void main(String[] args) {
        // Creazione di una mappa con Chiave=String (Nome) e Valore=Integer (Voto)
        Map<String, Integer> voti = new HashMap<>();

        // 1. Inserimento elementi (put)
        voti.put("Marco", 28);
        voti.put("Giulia", 30);
        voti.put("Antonio", 24);
        voti.put("Luca", 18);

        // 2. Lettura singola di un elemento (get)
        // Legge il valore associato alla chiave, restituisce null se non esiste
        Integer votoMarco = voti.get("Marco");
        System.out.println("Voto di Marco: " + votoMarco);

        // 3. Estrazione di un elemento (remove)
        // Rimuove la coppia dalla mappa e restituisce il valore che è stato appena eliminato
        Integer votoAntonio = voti.remove("Antonio");
        System.out.println("Antonio rimosso. Il suo voto era: " + votoAntonio);

        // 4. Verifica esistenza (containsKey / containsValue)
        if (voti.containsKey("Giulia")) {
            System.out.println("Giulia è presente nel registro.");
        }

        // 5. Lettura di tutte le chiavi (keySet) o di tutti i valori (values)
        System.out.println("\nSolo i Nomi (Chiavi): " + voti.keySet());
        System.out.println("Solo i Voti (Valori): " + voti.values());

        // 6. Iterazione completa su Coppie Chiave-Valore (entrySet)
        System.out.println("\n--- Elenco Voti Aggiornato ---");
        for (Map.Entry<String, Integer> entry : voti.entrySet()) {
            System.out.println("Studente: " + entry.getKey() + " | Voto: " + entry.getValue());
        }
    }
}
```

### I nomi esatti dell'API di `Map` (e perché `getValue` non c'è)
`Map` ha pochi metodi e vanno scritti **esatti**. Il più inventato per analogia è `getValue`, che **non appartiene a `Map`**: è un metodo di `Map.Entry`, cioè della coppia che ottieni iterando `entrySet()`.

| Voglio | Scrivo | Nota |
|---|---|---|
| inserire o sovrascrivere | `m.put(chiave, valore)` | restituisce il valore precedente o `null` |
| leggere un valore | `m.get(chiave)` | `null` se la chiave non c'è: con `int` fa **unboxing di `null`** (`NullPointerException`) |
| leggere con un default | `m.getOrDefault(chiave, 0)` | niente `null` da controllare |
| esiste la chiave? | `m.containsKey(chiave)` | |
| contare occorrenze | `m.put(k, m.get(k) + 1)` oppure `m.merge(k, 1, Integer::sum)` | la chiave deve già esserci, o usa `merge` |
| quanti elementi | `m.size()` | non `length` e non `length()` |
| tutte le chiavi / i valori | `m.keySet()` / `m.values()` | |
| scorrere le coppie | `for (Map.Entry<K, V> e : m.entrySet())` poi `e.getKey()`, `e.getValue()` | `getValue` **solo** qui |

**Dichiarare una mappa non la popola.** Un campo `private Map<String, Integer> voti = new HashMap<>();` è una mappa **vuota**: `containsKey` è sempre `false`. Se la traccia dà l'elenco dei candidati (o dei prodotti) nel costruttore, è il **costruttore** che deve fare `put(nome, 0)` per ognuno, altrimenti ogni operazione successiva "non trova" niente.

```java
import java.util.*;

class Urna {
    private Map<String, Integer> voti = new HashMap<>();
    private int nulle = 0;

    public Urna(String[] candidati) {
        for (String c : candidati) {
            voti.put(c, 0);                  // la mappa si POPOLA nel costruttore: dichiararla non basta
        }
    }

    public void vota(String candidato) {
        if (voti.containsKey(candidato)) {
            voti.put(candidato, voti.get(candidato) + 1);   // get sulla MAPPA; getValue è di Map.Entry
        } else {
            nulle++;
        }
    }

    public int voti(String candidato) { return voti.getOrDefault(candidato, 0); }
    public int nulle() { return nulle; }
    public int totale() {
        int t = nulle;
        for (int v : voti.values()) t += v;
        return t;
    }
}
```

Le chiavi `String` si confrontano per **contenuto** (`equals`), non con `==`: la mappa lo fa da sola, ma se confronti a mano due nomi, `.equals()`.

---

## 6. Leggere il codice fornito: dedurre le firme (variante B)

In molte tracce una o più classi sono **già scritte** e a te ne manca una: *"le firme dei metodi vanno dedotte dalle invocazioni"*. Non c'è niente da inventare: il codice fornito contiene **tutto** ciò che serve. Gli errori più cari di questa variante sono nomi di metodo "adattati" (`leggiProdotti` al posto di `leggi`, `getSchedeNulle` al posto di `nulle`) e un `throws` che manca.

### Come si legge una riga di codice fornito
| Nel codice fornito vedi | Ne ricavi |
|---|---|
| `x.nome(a, b)` | il **nome esatto** del metodo, il numero e il tipo dei parametri |
| `double s = x.nome()` | il **tipo di ritorno** (con `int` avresti `possible lossy conversion`) |
| `somma += x.get()` con `somma` `double` | `get()` restituisce un numero; il tipo più largo è `double` |
| `x.nome()` usato come istruzione | probabilmente `void` |
| `new X(a, b)` | la firma del **costruttore**, nell'ordine in cui compaiono gli argomenti |
| `catch (E e)` attorno alla chiamata | il metodo dichiara **`throws E`**: un `catch` di un'eccezione controllata ha senso solo se il `try` può lanciarla |
| `catch (E1 e) {...} catch (E2 e) {...}` | `throws E1, E2` (o la superclasse comune) |
| `x.metodo()` dentro un `main` che non ha `throws` né `try` | il metodo **non** dichiara eccezioni controllate |
| `static` nella chiamata (`Classe.metodo()`) | il metodo è `static` |
| `ArrayList<String> r = x.leggi();` | tipo di ritorno `ArrayList<String>` (o un tipo compatibile con quello a sinistra) |

### Esempio completo
```java
// Codice FORNITO dalla traccia: da qui si leggono le firme.
class Promemoria {
    public static void main(String[] args) {
        Diario diario = new Diario("note.txt");                  // costruttore (String)
        try {
            diario.aggiungi("comprare il pane");                 // aggiungi(String), void
            java.util.ArrayList<String> tutte = diario.leggi();  // leggi() restituisce ArrayList<String>
            System.out.println(tutte.size());
        } catch (VoceVuotaException e) {                         // aggiungi dichiara throws VoceVuotaException
            System.out.println(e.getMessage());
        } catch (java.io.IOException e) {                        // ... e throws IOException
            System.out.println("errore");
        }
    }
}

// Quello che DEVI scrivere, ricavato riga per riga:
class VoceVuotaException extends Exception {                     // catch + checked => extends Exception
    public VoceVuotaException(String m) { super(m); }
}

class Diario {
    private String percorso;
    public Diario(String percorso) { this.percorso = percorso; }
    public void aggiungi(String testo) throws VoceVuotaException, java.io.IOException {
        if (testo.trim().isEmpty()) throw new VoceVuotaException("voce vuota");
    }
    public java.util.ArrayList<String> leggi() throws java.io.IOException { return new java.util.ArrayList<>(); }
}
```

### Tre regole di metodo
1. **Il nome si copia.** Prima di scrivere il corpo di un metodo dedotto, rileggi la riga che lo chiama e ricopia il nome; non "migliorarlo", non tradurlo, non usare un sinonimo. Un nome diverso non funziona in nessun caso: con le classi nello stesso file è `cannot find symbol`, con un test già compilato è `NoSuchMethodError` a runtime.
2. **I `catch` sono la tua lista di `throws`.** Se il codice fornito cattura `IOException`, il tuo metodo deve poterla lanciare. Se hai un errore `unreported exception` e continui a cambiare il corpo del metodo, stai guardando nel posto sbagliato: il rimedio è sulla **firma** (`throws`), non su un altro `throw` (Livello 3 §5).
3. **Il messaggio e il formato stanno nella traccia, non nel codice fornito.** Il codice fornito ti dice come si **chiama** il metodo, non che cosa deve stampare o con quale messaggio rifiutare: quello lo dice la descrizione (`voce vuota` in minuscolo è un requisito).

