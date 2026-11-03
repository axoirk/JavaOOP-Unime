---
materia: Programmazione a Oggetti
capitolo: 7
titolo: Classi e oggetti
livello_syllabus: 2
stato: completo
slide: ["Savitch cap. 8 slide 4-38", "Savitch cap. 9 slide 3-14, 31-32, 46-52", "Lect2 (Classes, Methods, Constructor, public vs. private, Packages)"]
appelli: [EXAM1, EXAM3, EXAM4]
fonti_esterne: 3
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 7 — Classi e oggetti

## Di cosa parla questo capitolo

Nei capitoli precedenti abbiamo lavorato con valori sparsi: un `int` qui, una `String` là, qualche array. Ogni volta che i dati di un problema "stanno insieme" (le caratteristiche di un'automobile, il saldo e il titolare di un conto, il nome e la matricola di uno studente) ci siamo dovuti arrangiare con più variabili separate e con metodi che le ricevono tutte come parametri. Funziona finché il programma è piccolo; poi nessuno sa più quali variabili appartengano a quale entità, e chiunque può modificarle in qualunque momento. La programmazione a oggetti risolve il problema in modo radicale: **raggruppa i dati e le operazioni che li riguardano in un'unica unità**, la **classe**, e fa vivere ogni entità del problema come un **oggetto** costruito su quel modello.

Il capitolo riprende i metodi del [Capitolo 6 — Metodi](06-metodi.md) (qui diventano metodi *d'istanza*, che lavorano sui dati di un oggetto) e le variabili di classe e le costanti `static` che vi abbiamo già incontrato. Usa i tipi del [Capitolo 2 — Tipi primitivi, variabili e operatori](02-tipi-variabili-operatori.md) per i campi e gli array del [Capitolo 5 — Array e matrici](05-array-e-matrici.md) come stato interno. Chiude i punti lasciati aperti nei capitoli precedenti: che cosa sia davvero un `enum`, che cosa sia un package e perché le classi dell'esame stanno tutte in un solo file.

Alla fine del capitolo saprai definire una classe con **campi** e **metodi**, creare oggetti con `new` e usarli con l'operatore punto, scrivere uno o più **costruttori** (compreso il caso in cui due costruttori si chiamano a vicenda con `this(...)`), proteggere lo stato con l'**information hiding** (`private` per i campi, `public` per i metodi che formano l'interfaccia, accessor e mutator con controllo dei valori), distinguere un membro d'istanza da uno `static`, scrivere un `enum` con campi e costruttore, organizzare le classi in **package** con `import`, e tradurre in codice la traccia di un esercizio che chiede "una classe con queste variabili d'istanza private, questo costruttore e questi metodi".

> [!IMPORTANT]
> **Classi e prove scritte**
> Classi con campi privati, costruttori e metodi `get`/`set` compaiono in tre delle tracce ufficiali degli appelli, in ognuna con un peso diverso: come tutto l'esercizio da 5 punti, come unico requisito architetturale di un esercizio da 13, come primo mattone di un esercizio che poi si estende con ereditarietà, classi annidate o thread. Il docente valuta l'**aderenza letterale**: la traccia dice "tutte le variabili d'istanza private", "il costruttore riceve nell'ordine la base e l'altezza", "due costruttori in overload", e ogni parola è verificabile nel codice. Le sezioni 7.2 e 7.3 e gli scheletri in fondo servono a questo. Vedi la sezione "Come esce all'esame".

## 7.1 Classi e oggetti

### 7.1.1 Il problema: dati che appartengono insieme

Immaginiamo di dover descrivere un'automobile: ha un modello, una velocità attuale, una quantità di carburante nel serbatoio. Con gli strumenti dei capitoli precedenti scriveremmo tre variabili, e per descrivere due automobili ne scriveremmo sei:

```java
public class SenzaClassi {
    public static void main(String[] args) {
        String modello1 = "Berlina";
        int velocita1 = 50;
        double carburante1 = 40.0;

        String modello2 = "Utilitaria";
        int velocita2 = 0;
        double carburante2 = 25.5;

        velocita1 = velocita1 + 20;                    // accelera la prima
        System.out.println(modello1 + ": " + velocita1 + " km/h");
        System.out.println(modello2 + ": " + velocita2 + " km/h");
    }
}
```

```text
Berlina: 70 km/h
Utilitaria: 0 km/h
```

Il programma è corretto, ma ha tre difetti che crescono con le dimensioni del problema. Il primo: nulla dice che `modello1`, `velocita1` e `carburante1` siano parti della *stessa* automobile; lo sappiamo solo noi, dai numeri nei nomi. Il secondo: con cento automobili servirebbero trecento variabili, e non si potrebbe scrivere un ciclo su di esse (lo stesso problema che ci ha portato agli array nel Capitolo 5, ma qui gli elementi sono di tipo diverso). Il terzo: se vogliamo un metodo `stampa` che mostri un'automobile, dovrà ricevere tre parametri, e chi lo chiama dovrà ricordarsi di passarli nell'ordine giusto.

La soluzione è definire **un nuovo tipo**, `Automobile`, che contiene tutti e tre i dati e sa fare le operazioni che li riguardano.

### 7.1.2 Classe e oggetto

> [!NOTE]
> **Definizione — Classe e oggetto**
> Una **classe** (*class*) è un modello che descrive un tipo di entità: elenca i **dati** che ogni entità di quel tipo possiede (i *campi*, o *variabili d'istanza*) e le **operazioni** che sa eseguire (i *metodi*). Un **oggetto** (*object*, o **istanza**, *instance*) è una singola entità concreta costruita secondo il modello di una classe, con i propri valori dei dati. Un programma Java è un insieme di oggetti che interagiscono tra loro.

> [!TIP]
> **Intuizione — Lo stampo e i biscotti**
> La classe è lo stampo per i biscotti; gli oggetti sono i biscotti. Lo stampo definisce la forma, ma non si mangia: per avere un biscotto bisogna usarlo. Dallo stesso stampo escono quanti biscotti si vuole, ciascuno con la sua farcitura (i valori dei dati), e cambiare la farcitura di un biscotto non cambia gli altri. L'analogia ha un limite: lo stampo dei biscotti è un oggetto fisico a parte, mentre in Java la classe è una *descrizione* che esiste nel codice, e che il programma legge quando deve costruire un oggetto.

La distinzione fra classe e oggetto è la prima da avere chiara. `Automobile` è una classe: dice che ogni automobile ha un modello, una velocità e un carburante, e che può accelerare. La "Berlina a 70 km/h con 40 litri" e la "Utilitaria ferma con 25,5 litri" sono due oggetti, due **istanze** della classe `Automobile`. Ogni oggetto ha la **propria copia** dei dati; i metodi invece sono scritti una volta sola, nella classe, e funzionano su qualunque oggetto.

I progettisti disegnano le classi con un **diagramma delle classi UML** (*Unified Modeling Language*), che ha la forma di un rettangolo diviso in tre parti: il nome della classe, i dati, le operazioni. Per la nostra automobile:

```text
+-------------------------------+
| Automobile                    |
+-------------------------------+
| modello: String               |
| velocita: int                 |
| carburante: double            |
+-------------------------------+
| stampa(): void                |
| accelera(delta: int): void    |
| autonomia(): double           |
+-------------------------------+
```

Il diagramma contiene più della semplice interfaccia (mostra anche i dati) e meno dell'implementazione (non mostra il corpo dei metodi). Di solito si disegna **prima** di scrivere la classe, come progetto. Più avanti (sezione 7.3.8) vedremo i segni `+` e `-` davanti ai membri, che indicano `public` e `private`.

### 7.1.3 Definire una classe: campi e metodi d'istanza

Una classe si scrive con la parola chiave `class`, il nome (per convenzione con l'iniziale maiuscola) e il **corpo** tra graffe. Nel corpo ci sono i **campi** (*fields*), cioè le variabili dichiarate direttamente nella classe e fuori da ogni metodo, e i **metodi**.

```java
class Automobile {
    public String modello;                 // campi: ogni oggetto ha la sua copia
    public int velocita;
    public double carburante;

    public void stampa() {                 // metodo d'istanza: lavora sui campi di un oggetto
        System.out.println(modello + ": " + velocita + " km/h, " + carburante + " litri");
    }

    public void accelera(int delta) {
        velocita = velocita + delta;       // modifica il campo dell'oggetto su cui è chiamato
    }

    public double autonomia() {            // metodo che restituisce un valore
        return carburante * 15.0;          // supponendo 15 km con un litro
    }
}
```

Vale tutto ciò che sappiamo dal Capitolo 6 sulle intestazioni dei metodi: tipo di ritorno, nome, parametri, `return`. Due differenze rispetto ai metodi `static` che conoscevamo. La prima: non c'è la parola `static`, quindi questi sono **metodi d'istanza** (*instance methods*): per usarli serve un oggetto. La seconda: nel corpo di un metodo d'istanza si possono usare i campi **per nome**, senza scrivere altro: `velocita` in `accelera` è il campo `velocita` *dell'oggetto su cui il metodo è stato chiamato*. È questo che permette a `accelera(20)` di dare risultati diversi su automobili diverse, pur essendo scritto una volta sola.

La parola `public` davanti a ogni membro significa "accessibile da qualunque altra classe". Per ora la usiamo ovunque; nella sezione 7.3 vedremo perché quasi sempre i campi *non* devono essere pubblici.

### 7.1.4 Creare e usare oggetti: `new` e l'operatore punto

Dichiarare una variabile di tipo `Automobile` non crea nessuna automobile: crea solo una "casella" capace di indicare un oggetto (come vedremo nel [Capitolo 8 — Riferimenti e memoria](08-riferimenti-e-memoria.md)). L'oggetto si crea con l'operatore **`new`** seguito dal nome della classe e da una coppia di parentesi:

```java
public class ProvaAutomobile {
    public static void main(String[] args) {
        Automobile a = new Automobile();       // crea un oggetto e lo assegna alla variabile a
        a.modello = "Berlina";                 // operatore punto: oggetto.campo
        a.velocita = 50;
        a.carburante = 40.0;

        Automobile b = new Automobile();       // un secondo oggetto, indipendente dal primo
        b.modello = "Utilitaria";
        b.carburante = 25.5;

        a.accelera(20);                        // operatore punto: oggetto.metodo(argomenti)
        a.stampa();
        b.stampa();
        System.out.println("Autonomia di " + a.modello + ": " + a.autonomia() + " km");
    }
}
```

Questo `main` usa la classe `Automobile` appena scritta: nello stesso file le due classi si affiancano, come negli esempi del capitolo 6.

```text
Berlina: 70 km/h, 40.0 litri
Utilitaria: 0 km/h, 25.5 litri
Autonomia di Berlina: 600.0 km
```

Seguiamo l'esecuzione. `new Automobile()` costruisce un oggetto nuovo e ne restituisce il riferimento, che viene assegnato ad `a`; la stessa istruzione scritta una seconda volta, con `b`, costruisce un oggetto distinto. L'**operatore punto** collega un oggetto a un suo membro: `a.modello` è il campo `modello` dell'oggetto `a`, `a.accelera(20)` chiama il metodo `accelera` con `a` come oggetto su cui lavorare. Dopo `a.accelera(20)` la velocità di `a` è `50 + 20 = 70`, mentre `b.velocita` non è stata toccata e vale ancora il valore predefinito 0 (lo vediamo tra poco). Le due automobili sono **indipendenti**: modificare una non cambia l'altra. L'autonomia di `a` è `40.0 · 15.0 = 600.0`.

Riassumendo la regola d'accesso: per un membro **non statico** si scrive `nomeOggetto.membro`; per un membro `static` si scrive `NomeClasse.membro` (Capitolo 6, sezione 6.4). Dentro la classe stessa, un metodo d'istanza usa gli altri membri semplicemente per nome.

### 7.1.5 I valori predefiniti dei campi

Nel `main` precedente non abbiamo mai assegnato `b.velocita`, eppure `b.stampa()` ha mostrato `0 km/h` e non un errore. È una differenza importante tra variabili locali e campi. Una variabile **locale** non inizializzata non si può usare: il compilatore rifiuta il programma (Capitolo 2, sezione 2.1.3). Un **campo**, invece, riceve automaticamente un **valore predefinito** (*default value*) alla creazione dell'oggetto, che dipende dal tipo.

| Tipo del campo | Valore predefinito |
|---|---|
| `byte`, `short`, `int`, `long` | `0` |
| `float`, `double` | `0.0` |
| `boolean` | `false` |
| `char` | il carattere di codice 0 (`'\u0000'`) |
| qualunque classe (`String`, `Automobile`…) e array | `null` |

```java
class Valori {
    int intero;
    double reale;
    boolean vero;
    char carattere;
    String testo;
}

public class ProvaValori {
    public static void main(String[] args) {
        Valori v = new Valori();
        System.out.println(v.intero);
        System.out.println(v.reale);
        System.out.println(v.vero);
        System.out.println((int) v.carattere);      // il carattere 0 non si vede: stampiamo il suo codice
        System.out.println(v.testo);
    }
}
```

```text
0
0.0
false
0
null
```

Il valore `null` significa "nessun oggetto": una variabile di tipo classe che vale `null` non indica niente, e chiamare un metodo su di essa fa terminare il programma con una `NullPointerException` (se ne parla nel Capitolo 8). Per questo un campo `String` mai assegnato non è una stringa vuota, ma `null`: `testo.length()` fallirebbe.

> [!WARNING]
> **Attenzione — I valori predefiniti sono una rete di sicurezza, non uno stile**
> Che i campi partano da `0`, `false` o `null` non significa che sia sensato lasciarli così: un'automobile con modello `null` e velocità 0 è un oggetto privo di significato. Il punto di una classe ben progettata è che l'oggetto nasca già in uno stato valido: se ne occupano i costruttori (sezione 7.2).

### 7.1.6 La parola chiave `this`

Dentro un metodo d'istanza l'oggetto su cui il metodo è stato chiamato non ha un nome: nel metodo `accelera` abbiamo scritto `velocita`, non `a.velocita`. Quell'oggetto "implicito" si può comunque nominare con la parola chiave **`this`**, che significa "l'oggetto che sta eseguendo questo metodo".

> [!NOTE]
> **Definizione — `this`**
> Dentro un metodo d'istanza o un costruttore, **`this`** è un riferimento all'oggetto su cui il metodo è stato chiamato (o che il costruttore sta costruendo). `this.velocita` è il campo `velocita` di quell'oggetto; `this.accelera(5)` è la chiamata del metodo `accelera` sullo stesso oggetto.

Le due righe seguenti, dentro `accelera`, sono perfettamente equivalenti:

```java
velocita = velocita + delta;
this.velocita = this.velocita + delta;
```

Scrivere `this.` è facoltativo finché non c'è ambiguità, ed è il caso più comune. Diventa **indispensabile** quando un parametro ha lo stesso nome di un campo: nel corpo del metodo il nome semplice indica sempre il parametro (il più "vicino"), e il campo resta nascosto. È l'*ombreggiamento* (*shadowing*), e lo vedremo meglio nella sezione 7.1.8, perché è la ragione per cui quasi ogni costruttore e ogni `set` contiene `this.`.

`this` ha anche altri usi, che incontreremo: chiamare un altro costruttore della stessa classe (`this(...)`, sezione 7.2.5) e, nelle classi annidate, indicare l'oggetto della classe esterna (Capitolo 11).

### 7.1.7 Metodi che chiamano metodi, metodi che restituiscono un `boolean`

Un metodo può chiamare gli altri metodi della propria classe, per nome e senza nessun prefisso: l'oggetto su cui lavora è lo stesso. Per vederlo scriviamo una classe `Specie` che raccoglie i dati di una specie animale protetta (nome, popolazione, tasso annuo di crescita), con un metodo che ne ricava un altro.

```java
class Specie {
    public String nome;
    public int popolazione;
    public double tassoCrescita;                 // 0.05 vuol dire +5% all'anno

    public int popolazionePrevista(int anni) {
        double previsione = popolazione;
        for (int i = 0; i < anni; i++) {
            previsione = previsione + previsione * tassoCrescita;
        }
        return (int) previsione;                 // il cast tronca i decimali (Capitolo 2)
    }

    public boolean piuNumerosaDi(Specie altra) { // metodo che restituisce un boolean
        return popolazione > altra.popolazione;  // this.popolazione contro altra.popolazione
    }

    public void stampaPrevisione(int anni) {
        System.out.println(nome + " tra " + anni + " anni: " + popolazionePrevista(anni));   // chiama un altro metodo
    }
}

public class ProvaSpecie {
    public static void main(String[] args) {
        Specie lupo = new Specie();
        lupo.nome = "Lupo";
        lupo.popolazione = 1000;
        lupo.tassoCrescita = 0.10;

        Specie orso = new Specie();
        orso.nome = "Orso";
        orso.popolazione = 400;
        orso.tassoCrescita = 0.50;

        lupo.stampaPrevisione(2);
        orso.stampaPrevisione(2);
        System.out.println(lupo.piuNumerosaDi(orso));
        System.out.println(orso.piuNumerosaDi(lupo));
    }
}
```

```text
Lupo tra 2 anni: 1210
Orso tra 2 anni: 900
true
false
```

`stampaPrevisione` chiama `popolazionePrevista(anni)` senza scrivere `lupo.` o `orso.`: il metodo viene eseguito sullo stesso oggetto che ha eseguito `stampaPrevisione`. Per il lupo i conti sono `1000 → 1100 → 1210`; per l'orso `400 → 600 → 900`.

Il metodo `piuNumerosaDi` mostra due cose. Primo, un metodo può restituire un `boolean`: basta dichiarare `boolean` come tipo di ritorno e usare un'espressione booleana nel `return`. Secondo, un metodo d'istanza può ricevere come parametro **un altro oggetto della stessa classe** e leggerne i campi: dentro `lupo.piuNumerosaDi(orso)`, `popolazione` è `lupo.popolazione` (l'oggetto su cui si chiama il metodo) e `altra.popolazione` è `orso.popolazione` (l'oggetto passato come argomento). È una situazione comune: l'accesso ai campi di un altro oggetto della *stessa* classe è sempre ammesso, anche se i campi fossero `private` (sezione 7.3).

### 7.1.8 Campo, parametro, variabile locale: chi vede chi

In una classe convivono tre tipi di variabili, che si distinguono per **dove sono dichiarate**, quanto **vivono** e chi le **vede**.

| Tipo | Dove si dichiara | Quando esiste | Valore iniziale |
|---|---|---|---|
| **Campo** (variabile d'istanza) | nella classe, fuori dai metodi, senza `static` | finché esiste l'oggetto a cui appartiene | predefinito (`0`, `false`, `null`) |
| **Variabile di classe** (`static`) | nella classe, fuori dai metodi, con `static` | per tutta l'esecuzione del programma, una sola copia | predefinito |
| **Parametro** | nell'intestazione del metodo o del costruttore | durante la chiamata | l'argomento passato |
| **Variabile locale** | dentro un metodo o un blocco | dalla dichiarazione alla `}` del blocco | **nessuno**: va assegnata prima dell'uso |

I campi e le variabili di classe sono **membri** della classe: si possono usare in tutti i suoi metodi. Negli esempi che seguono compare già la parola `private` davanti ai campi: vuol dire che solo il codice della classe può usarli, e la spiegheremo nella sezione 7.3. Parametri e variabili locali appartengono al singolo metodo (Capitolo 6, sezioni 6.2 e 6.3).

Quando un parametro (o una variabile locale) ha lo stesso nome di un campo, il nome semplice indica il parametro: il campo è *nascosto* (ombreggiato) e per raggiungerlo si usa `this.`.

```java
class Termometro {
    private double gradi;

    public void impostaErrato(double gradi) {
        gradi = gradi;                  // assegna il parametro a se stesso: il campo non cambia
    }

    public void impostaGiusto(double gradi) {
        this.gradi = gradi;             // campo a sinistra, parametro a destra
    }

    public double leggi() {
        return gradi;
    }
}

public class ProvaOmbra {
    public static void main(String[] args) {
        Termometro t = new Termometro();
        t.impostaErrato(21.5);
        System.out.println(t.leggi());
        t.impostaGiusto(21.5);
        System.out.println(t.leggi());
    }
}
```

```text
0.0
21.5
```

`impostaErrato` compila senza proteste (assegnare una variabile a se stessa è legale) ma non fa nulla: a sinistra e a destra dell'`=` c'è il parametro. Il campo resta a `0.0`, il valore predefinito. `impostaGiusto` scrive `this.gradi` a sinistra: ora il compilatore sa che parliamo del campo. Se invece parametro e campo hanno nomi diversi (`double g` e `gradi`) l'ambiguità non esiste e `this.` si può omettere, ma l'abitudine più diffusa è di dare lo **stesso nome** ai due e scrivere sempre `this.campo = campo;`.

### 7.1.9 Dove stanno le classi: un file o più file

Nell'uso normale di Java **ogni classe sta in un file proprio**, che si chiama come la classe e ha estensione `.java`: `Automobile` in `Automobile.java`, `Specie` in `Specie.java`. Ogni file si può compilare da solo; le classi di un programma stanno di solito nella stessa cartella, così il compilatore le trova. Compilando `ProvaAutomobile.java` il compilatore cerca da sé `Automobile.java` nella stessa cartella e la compila a sua volta.

```text
Automobile.java        ->  class Automobile { ... }
ProvaAutomobile.java   ->  public class ProvaAutomobile { ... main ... }
```

Negli esempi di questi appunti e nelle prove d'esame le cose vanno diversamente: **tutte le classi stanno nello stesso file**, e al più una è `public`, quella che ha il `main` e dà il nome al file (Capitolo 1, sezione 1.10). Le altre classi si scrivono **senza modificatore** davanti a `class`, come abbiamo fatto con `Automobile`. Il significato di una classe senza modificatore (visibile solo nel proprio package) lo vediamo nella sezione 7.3.6. La scelta di un file solo ha una ragione pratica: la pagina d'esame ha un'unica area di testo.

## 7.2 I costruttori

### 7.2.1 Il problema: l'oggetto nasce con valori predefiniti

Nell'esempio con `Automobile` per ottenere un'automobile completa abbiamo scritto quattro righe: `new`, e poi tre assegnazioni ai campi. Se ci dimentichiamo una delle tre, l'oggetto esiste ma è incompleto (modello `null`, carburante zero) e nessuno ce lo segnala. Sarebbe meglio che un oggetto **non potesse nascere** senza i suoi dati essenziali: è ciò che fa un costruttore.

### 7.2.2 Definire un costruttore

> [!NOTE]
> **Definizione — Costruttore**
> Un **costruttore** (*constructor*) è un metodo speciale che viene eseguito **quando un oggetto viene creato con `new`**, e serve a inizializzarne i campi. Ha **lo stesso nome della classe** e **nessun tipo di ritorno**, nemmeno `void`. Può avere parametri, con i quali si specificano i valori iniziali.

La forma generale è:

```text
modificatore NomeClasse(tipo parametro1, tipo parametro2, ...) {
    corpo
}
```

dove il modificatore di accesso è di norma `public`. Ecco `Automobile` con un costruttore:

```java
class Automobile {
    public String modello;
    public int velocita;
    public double carburante;

    public Automobile(String modello, double carburante) {     // costruttore
        this.modello = modello;                                // campo = parametro
        this.carburante = carburante;
        this.velocita = 0;                                     // un'automobile nuova parte ferma
    }

    public void stampa() {
        System.out.println(modello + ": " + velocita + " km/h, " + carburante + " litri");
    }
}

public class ProvaCostruttore {
    public static void main(String[] args) {
        Automobile a = new Automobile("Berlina", 40.0);        // gli argomenti vanno al costruttore
        Automobile b = new Automobile("Utilitaria", 25.5);
        a.stampa();
        b.stampa();
    }
}
```

```text
Berlina: 0 km/h, 40.0 litri
Utilitaria: 0 km/h, 25.5 litri
```

Le parentesi di `new Automobile("Berlina", 40.0)` non sono più vuote: gli argomenti vengono passati al costruttore, che li copia nei campi (con `this.` per via dell'ombreggiamento). Una volta definito questo costruttore, **non si può più scrivere `new Automobile()` senza argomenti**: l'unico modo di creare un'automobile è fornire modello e carburante, ed è esattamente ciò che volevamo. Il compilatore controlla numero e tipo degli argomenti come per ogni metodo.

Tre osservazioni sulla forma.

- Il costruttore si chiama **come la classe**, maiuscole comprese. Un metodo con un nome diverso non è un costruttore.
- Il costruttore **non ha tipo di ritorno**. Se per distrazione si scrive `public void Automobile(...)`, quello non è più un costruttore ma un normale metodo che per caso si chiama come la classe: il programma compila, e gli oggetti nascono senza essere inizializzati (vedi gli errori tipici in fondo).
- Un costruttore **non si chiama** come un metodo (`a.Automobile(...)` è un errore): viene eseguito solo da `new`.

Con un esempio dal materiale del corso: una classe `Sfera` con un raggio, un valore predefinito e un metodo che calcola il volume.

```java
class Sfera {
    private double raggio;
    public static final double RAGGIO_PREDEFINITO = 1.0;

    public Sfera() {                                // costruttore senza parametri
        this.raggio = RAGGIO_PREDEFINITO;
    }

    public Sfera(double raggio) {                   // costruttore con un parametro
        this.raggio = raggio;
    }

    public double getRaggio() {
        return raggio;
    }

    public double getVolume() {
        return 4 * Math.PI * raggio * raggio * raggio / 3;
    }
}

public class ProvaSfera {
    public static void main(String[] args) {
        Sfera piccola = new Sfera();
        Sfera grande = new Sfera(19.1);
        System.out.println("Raggio " + piccola.getRaggio() + ": volume " + (float) piccola.getVolume());
        System.out.println("Raggio " + grande.getRaggio() + ": volume " + (float) grande.getVolume());
    }
}
```

```text
Raggio 1.0: volume 4.1887903
Raggio 19.1: volume 29186.95
```

Qui i costruttori sono **due**: `new Sfera()` usa il raggio predefinito (costante `static final` della classe), `new Sfera(19.1)` quello indicato. Il cast `(float)` accorcia le cifre stampate. Il campo `raggio` è dichiarato `private`: significa che solo i metodi della classe `Sfera` possono leggerlo o scriverlo, e dal `main` si arriva al valore soltanto con `getRaggio()` (ne parliamo a fondo nella sezione 7.3). Vediamo subito come Java sceglie tra più costruttori.

### 7.2.3 Il costruttore di default

Finora le classi del capitolo (`Automobile` prima della 7.2.2, `Specie`, `Valori`) non avevano nessun costruttore, e `new Automobile()` funzionava. Come? Se una classe **non dichiara alcun costruttore**, il compilatore ne aggiunge uno da sé: senza parametri, con il corpo vuoto, e con lo stesso modificatore di accesso della classe. È il **costruttore di default** (*default constructor*), e fa sì che `new NomeClasse()` esista sempre. Quello che fa è lasciare i campi ai valori predefiniti della sezione 7.1.5.

La regola ha però un rovescio, tra i più frequenti all'esame:

> [!WARNING]
> **Attenzione — Il costruttore di default sparisce**
> Appena la classe dichiara **almeno un costruttore**, il compilatore **non aggiunge più** quello di default. Se dopo aver scritto `Automobile(String modello, double carburante)` si scrive `new Automobile()`, il programma non compila: `constructor Automobile in class Automobile cannot be applied to given types`. Se serve anche la forma senza argomenti, va scritta a mano, come costruttore esplicito.

Questo è anche il motivo per cui un costruttore senza parametri e con il corpo vuoto, come `public Automobile() { }`, a volte si scrive esplicitamente: è l'unico modo di avere sia la forma con argomenti sia quella senza.

### 7.2.4 Più costruttori: l'overloading

Una classe può avere **più costruttori**, purché differiscano per numero o tipo dei parametri, cioè per **firma** (*signature*): è l'overloading dei metodi (Capitolo 6, sezione 6.7) applicato ai costruttori. Al momento della creazione Java sceglie il costruttore la cui firma corrisponde agli argomenti di `new`. Un esempio con una classe `Animale`, con quattro costruttori che offrono quattro modi di crearne uno.

```java
class Animale {
    private String nome;
    private int eta;
    private double peso;

    public Animale() {                                      // senza parametri
        this.nome = "senza nome";
        this.eta = 0;
        this.peso = 0.0;
    }

    public Animale(String nome, int eta, double peso) {     // tre parametri
        this.nome = nome;
        this.eta = eta;
        this.peso = peso;
    }

    public Animale(String nome) {                           // solo il nome
        this.nome = nome;
        this.eta = 0;
        this.peso = 0.0;
    }

    public Animale(double peso) {                           // solo il peso
        this.nome = "senza nome";
        this.eta = 0;
        this.peso = peso;
    }

    public String descrizione() {
        return nome + ", " + eta + " anni, " + peso + " kg";
    }
}

public class ProvaAnimale {
    public static void main(String[] args) {
        Animale a = new Animale();
        Animale b = new Animale("Rex", 3, 18.5);
        Animale c = new Animale("Micio");
        Animale d = new Animale(4.2);
        System.out.println(a.descrizione());
        System.out.println(b.descrizione());
        System.out.println(c.descrizione());
        System.out.println(d.descrizione());
    }
}
```

```text
senza nome, 0 anni, 0.0 kg
Rex, 3 anni, 18.5 kg
Micio, 0 anni, 0.0 kg
senza nome, 0 anni, 4.2 kg
```

Ogni `new` corrisponde a un costruttore diverso: `new Animale()` al primo, `new Animale("Rex", 3, 18.5)` al secondo (tre argomenti nell'ordine `String`, `int`, `double`), `new Animale("Micio")` al terzo (un solo `String`), `new Animale(4.2)` al quarto (un solo `double`). L'**ordine** dei parametri fa parte della firma: `Animale(String, int)` e `Animale(int, String)` sono due costruttori diversi, e chi li chiama deve rispettare l'ordine che la traccia prescrive. Due costruttori con la **stessa** sequenza di tipi non sono ammessi, qualunque nome si dia ai parametri: `Animale(String a)` e `Animale(String b)` darebbero l'errore `constructor Animale(String) is already defined in class Animale`.

I costruttori della classe `Animale` fanno tutti lo stesso lavoro con piccole variazioni, e il codice si ripete. Le due sezioni seguenti mostrano come evitarlo.

### 7.2.5 Costruttori che riusano codice: un metodo ausiliario e `this(...)`

**Primo modo: un metodo ausiliario.** Il lavoro comune si mette in un metodo `set`, che i costruttori chiamano:

```java
class Animale2 {
    private String nome;
    private int eta;
    private double peso;

    public Animale2() {
        set("senza nome", 0, 0.0);                        // chiama il metodo ausiliario
    }

    public Animale2(String nome) {
        set(nome, 0, 0.0);
    }

    public Animale2(String nome, int eta, double peso) {
        set(nome, eta, peso);
    }

    public void set(String nome, int eta, double peso) {
        this.nome = nome;
        this.eta = eta;
        this.peso = peso;
    }

    public String descrizione() {
        return nome + ", " + eta + " anni, " + peso + " kg";
    }
}

public class ProvaAnimale2 {
    public static void main(String[] args) {
        System.out.println(new Animale2().descrizione());
        System.out.println(new Animale2("Micio").descrizione());
        System.out.println(new Animale2("Rex", 3, 18.5).descrizione());
    }
}
```

```text
senza nome, 0 anni, 0.0 kg
Micio, 0 anni, 0.0 kg
Rex, 3 anni, 18.5 kg
```

Il lavoro vero è scritto una sola volta, in `set`, e se un giorno servisse un controllo sull'età lo si metterebbe in un punto solo. Un costruttore può dunque chiamare i metodi della propria classe come qualunque altro metodo.

**Secondo modo: `this(...)`.** Un costruttore può chiamarne un altro della **stessa classe** scrivendo `this(argomenti)`. È la forma più compatta: il costruttore "completo" fa il lavoro, e gli altri lo richiamano passandogli i valori di ripiego.

```java
class Animale3 {
    private String nome;
    private int eta;
    private double peso;

    public Animale3(String nome, int eta, double peso) {   // costruttore completo
        this.nome = nome;
        this.eta = eta;
        this.peso = peso;
    }

    public Animale3() {
        this("senza nome", 0, 0.0);                        // chiama il costruttore a tre parametri
    }

    public Animale3(String nome) {
        this(nome, 0, 0.0);                                // idem, con il nome ricevuto
    }

    public String descrizione() {
        return nome + ", " + eta + " anni, " + peso + " kg";
    }
}

public class ProvaAnimale3 {
    public static void main(String[] args) {
        System.out.println(new Animale3().descrizione());
        System.out.println(new Animale3("Micio").descrizione());
        System.out.println(new Animale3("Rex", 3, 18.5).descrizione());
    }
}
```

```text
senza nome, 0 anni, 0.0 kg
Micio, 0 anni, 0.0 kg
Rex, 3 anni, 18.5 kg
```

`this("senza nome", 0, 0.0)` non crea un nuovo oggetto: *prosegue* la costruzione dell'oggetto corrente passando la parola al costruttore con tre parametri, che ne riempie i campi; poi l'esecuzione torna al costruttore chiamante. Quale costruttore viene scelto lo decide, come sempre, la firma degli argomenti.

> [!WARNING]
> **Attenzione — `this(...)` deve essere la prima istruzione**
> La chiamata `this(...)` è ammessa **solo come prima istruzione** del costruttore. Scrivere un'altra istruzione prima è un errore di compilazione (con JDK 11: `call to this must be first statement in constructor`; le versioni più recenti, che sperimentano una regola più libera, possono dare un messaggio diverso). Due costruttori che si chiamano a vicenda con `this(...)` sono un altro errore: `recursive constructor invocation`.

### 7.2.6 Overloading e conversione automatica dei costruttori

Un caso già visto nel Capitolo 6 (sezione 6.7.3) si ripresenta con i costruttori, ed è facile da trascurare. Riprendiamo `Animale` con un costruttore che riceve l'**età** (un `int`) e uno che riceve il **peso** (un `double`):

```java
class Cucciolo {
    private int eta;
    private double peso;

    public Cucciolo(int eta) {                      // età in anni
        this.eta = eta;
    }

    public Cucciolo(double peso) {                  // peso in kg
        this.peso = peso;
    }

    public String descrizione() {
        return eta + " anni, " + peso + " kg";
    }
}

public class ProvaCucciolo {
    public static void main(String[] args) {
        System.out.println(new Cucciolo(2).descrizione());
        System.out.println(new Cucciolo(2.0).descrizione());
        System.out.println(new Cucciolo((double) 2).descrizione());
    }
}
```

```text
2 anni, 0.0 kg
0 anni, 2.0 kg
0 anni, 2.0 kg
```

`new Cucciolo(2)` sceglie il costruttore con `int`, perché `2` è un `int`, **anche se l'autore pensava a un peso di due chili**. Prima il compilatore cerca una firma che corrisponda esattamente agli argomenti, e solo se non la trova prova le conversioni automatiche (da `int` a `double`). Per ottenere il costruttore con `double` bisogna passare un valore `double`: `2.0`, oppure `(double) 2`. Moralità: due costruttori con parametri numerici di tipo diverso e significato diverso sono una trappola; un buon progetto li evita, per esempio con un unico costruttore con entrambi i parametri.

### 7.2.7 Che cosa accade quando si scrive `new`

Mettiamo in fila gli eventi di `Automobile a = new Automobile("Berlina", 40.0);`, dall'inizio alla fine.

1. Java **alloca** (riserva) spazio per un nuovo oggetto `Automobile`, con tutti i campi ai valori predefiniti (`null`, `0`, `0.0`).
2. Esegue il **costruttore** scelto in base alla firma, che assegna ai campi i valori voluti.
3. `new` **restituisce il riferimento** all'oggetto creato, e l'assegnazione lo mette nella variabile `a`.

L'ordine spiega due fatti già visti: nel costruttore i campi esistono già e si possono leggere (hanno i valori predefiniti), e la variabile `a` non è assegnata finché il costruttore non è terminato. Dove viene memorizzato davvero l'oggetto, e che cosa significa "riferimento", è il tema del [Capitolo 8 — Riferimenti e memoria](08-riferimenti-e-memoria.md).

## 7.3 Information hiding e incapsulamento

### 7.3.1 Il problema: lo stato alla mercé di tutti

Finora tutti i campi erano `public`. Guardiamo che cosa succede con una classe che rappresenta un rettangolo:

```java
class RettangoloAperto {
    public double larghezza;
    public double altezza;

    public double area() {
        return larghezza * altezza;
    }
}

public class ProvaAperto {
    public static void main(String[] args) {
        RettangoloAperto r = new RettangoloAperto();
        r.larghezza = 4;
        r.altezza = 3;
        System.out.println(r.area());

        r.larghezza = -4;                    // nessuno lo impedisce
        System.out.println(r.area());
    }
}
```

```text
12.0
-12.0
```

Il programma ha prodotto un'area negativa, e il rettangolo "con larghezza -4" è un oggetto che non ha senso nel mondo reale. La classe non può difendersi: chiunque, da qualunque punto del programma, può scrivere in `larghezza` qualunque valore. In un programma di migliaia di righe, trovare *chi* ha messo `-4` è un incubo.

C'è un secondo problema, meno evidente. Se domani decidessimo di rappresentare il rettangolo con due lati `lato1` e `lato2`, ogni riga di ogni altra classe che scrive `r.larghezza` smetterebbe di compilare, e dovremmo correggerle tutte.

La soluzione è la stessa per entrambi i problemi: **nascondere i campi** e far passare ogni accesso da metodi scritti dalla classe, che possono controllare i valori e che restano gli stessi anche se i campi cambiano.

> [!NOTE]
> **Definizione — Information hiding e incapsulamento**
> L'**information hiding** (*occultamento dell'informazione*) consiste nel progettare una classe in modo che chi la usa debba sapere **che cosa** fanno i suoi metodi, ma non **come** lo fanno: i dettagli interni restano nascosti. Si chiama anche **astrazione**. L'**incapsulamento** (*encapsulation*) è la tecnica con cui lo si ottiene: la classe si divide in una **interfaccia** pubblica (che cosa si può fare) e in una **implementazione** privata (come lo si fa), e i dati si possono toccare solo attraverso l'interfaccia.

### 7.3.2 `public` e `private`

Gli strumenti sono due **modificatori di accesso** (*access modifiers*), da scrivere davanti a campi, metodi e costruttori:

- un membro **`public`** è accessibile da qualunque altra classe, per nome;
- un membro **`private`** è accessibile **solo dal codice scritto dentro la stessa classe**, cioè tra le sue graffe.

La regola di progetto che ne segue: **i campi sono `private`**; i metodi che formano l'interfaccia della classe, cioè le operazioni che gli altri possono chiedere, sono `public`. Riscriviamo il rettangolo così:

```java
class Rettangolo {
    private double larghezza;                 // nascosti: solo i metodi di Rettangolo li vedono
    private double altezza;

    public void setDimensioni(double larghezza, double altezza) {
        if (larghezza > 0 && altezza > 0) {   // l'unico modo di cambiare le dimensioni
            this.larghezza = larghezza;
            this.altezza = altezza;
        } else {
            System.out.println("Dimensioni rifiutate");
        }
    }

    public double area() {
        return larghezza * altezza;
    }
}

public class ProvaRettangolo {
    public static void main(String[] args) {
        Rettangolo r = new Rettangolo();
        r.setDimensioni(4, 3);
        System.out.println(r.area());
        r.setDimensioni(-4, 3);               // rifiutata: lo stato resta quello di prima
        System.out.println(r.area());
    }
}
```

```text
12.0
Dimensioni rifiutate
12.0
```

Ora l'unica porta d'ingresso è `setDimensioni`, e la classe la usa per **controllare** i valori: le dimensioni non positive vengono rifiutate e il rettangolo conserva uno stato valido. Il vantaggio è che il controllo sta in un punto solo, dentro la classe, e nessun altro può aggirarlo.

Provare a saltare la porta è un errore di compilazione:

> [!CAUTION]
> **Errore tipico — Accedere a un membro `private` da un'altra classe**
> ```java
> public class ProvaPrivato {
>     public static void main(String[] args) {
>         Rettangolo r = new Rettangolo();
>         r.larghezza = 6;                  // ERRORE DI COMPILAZIONE
>     }
> }
> ```
> Il compilatore risponde `larghezza has private access in Rettangolo`. Il campo è privato e il `main` sta in un'altra classe. Si corregge passando dai metodi pubblici della classe (`setDimensioni`), non rendendo il campo `public`.

Un'avvertenza che spesso sorprende: `private` limita l'accesso alla **classe**, non all'**oggetto**. Nel metodo `piuNumerosaDi(Specie altra)` della sezione 7.1.7 avremmo potuto dichiarare i campi `private` e continuare a scrivere `altra.popolazione`: il metodo è scritto dentro la classe `Specie`, quindi può leggere i campi privati di *qualunque* oggetto `Specie`, non solo di `this`.

### 7.3.3 Accessor e mutator

Quando i campi sono privati, il resto del programma ha comunque bisogno di leggerli e, in certi casi, di cambiarli. Per questo la classe offre due famiglie di metodi pubblici:

- i metodi **accessor** (*accessor methods*, o *getter*), che **restituiscono** il valore di un campo; per convenzione si chiamano `get` seguito dal nome del campo con l'iniziale maiuscola (`getNome`);
- i metodi **mutator** (*mutator methods*, o *setter*), che **modificano** il valore di un campo; si chiamano `set` seguito dal nome del campo (`setNome`).

Ecco una classe `Acquisto` che li usa, con un mutator che controlla i valori:

```java
class Acquisto {
    private String articolo;
    private int quantita;
    private double prezzoUnitario;

    public Acquisto(String articolo, int quantita, double prezzoUnitario) {
        this.articolo = articolo;
        setQuantita(quantita);                       // il costruttore riusa i mutator, quindi i controlli
        setPrezzoUnitario(prezzoUnitario);
    }

    public String getArticolo() {                    // accessor
        return articolo;
    }

    public void setArticolo(String articolo) {       // mutator
        this.articolo = articolo;
    }

    public int getQuantita() {
        return quantita;
    }

    public void setQuantita(int quantita) {
        if (quantita > 0) {
            this.quantita = quantita;
        } else {
            System.out.println("Quantita rifiutata: " + quantita);
        }
    }

    public double getPrezzoUnitario() {
        return prezzoUnitario;
    }

    public void setPrezzoUnitario(double prezzoUnitario) {
        if (prezzoUnitario >= 0) {
            this.prezzoUnitario = prezzoUnitario;
        } else {
            System.out.println("Prezzo rifiutato: " + prezzoUnitario);
        }
    }

    public double getTotale() {                      // metodo calcolato: non corrisponde a un campo
        return quantita * prezzoUnitario;
    }
}

public class ProvaAcquisto {
    public static void main(String[] args) {
        Acquisto a = new Acquisto("Quaderno", 3, 2.5);
        System.out.println(a.getArticolo() + ": " + a.getTotale());
        a.setQuantita(-1);                           // rifiutata
        a.setPrezzoUnitario(3.0);
        System.out.println(a.getArticolo() + ": " + a.getTotale());
    }
}
```

```text
Quaderno: 7.5
Quantita rifiutata: -1
Quaderno: 9.0
```

Osserviamo quattro cose.

- Ogni campo ha il suo accessor e il suo mutator, con i nomi costruiti con la regola `get`/`set` + nome del campo con l'iniziale maiuscola: `articolo → getArticolo`, `setArticolo`; `prezzoUnitario → getPrezzoUnitario`, `setPrezzoUnitario`. All'esame il nome è verificato alla lettera: `getprezzo`, `GetPrezzo` o `prezzoGet` non sono quello che la traccia chiede.
- Il tipo del parametro del mutator è il tipo del campo, e il tipo di ritorno dell'accessor è il tipo del campo.
- I mutator **controllano** i valori. Quando il valore non è ammesso, qui il metodo stampa un messaggio e lascia lo stato com'era (nel [Capitolo 13 — Eccezioni](13-eccezioni.md) vedremo il modo più corretto: lanciare un'eccezione).
- Il costruttore chiama i mutator invece di assegnare direttamente i campi: in questo modo i controlli valgono **anche alla creazione**, senza ripetere il codice. Per `articolo` invece il mutator non controlla niente, e l'assegnazione diretta è equivalente.

`getTotale` è un accessor "calcolato": restituisce un valore ricavato dai campi, e non esiste nessun campo `totale`. È un esempio del fatto che l'interfaccia di una classe può essere diversa dalla sua struttura interna, ed è proprio l'idea dell'information hiding.

> [!IMPORTANT]
> **Nota del docente — Non tutti i campi hanno un setter**
> Quando la traccia dice "tutte le variabili d'istanza private e i relativi metodi `get` e `set`", ogni campo ha **entrambi** i metodi, con i nomi regolari. Se la traccia chiede soltanto i `get`, scrivere anche i `set` è un'aggiunta non richiesta. Ci sono campi che non devono cambiare dopo la creazione (un codice, una matricola): per quelli si scrive solo l'accessor, e si dichiara il campo `final` (sezione 7.4.2).

### 7.3.4 Interfaccia e implementazione

Il nome *incapsulamento* nasce da un'immagine: guidiamo un'automobile conoscendo il pedale del freno, l'acceleratore e il volante, cioè **che cosa** fanno, ma non vediamo gli ingranaggi che realizzano il lavoro, cioè **come** lo fanno. Il guidatore usa l'interfaccia, il meccanico conosce l'implementazione. Una classe ben incapsulata si divide nello stesso modo:

- l'**interfaccia della classe** (*class interface*) è l'insieme delle intestazioni dei metodi pubblici, con un commento che dice che cosa fanno. È ciò che deve leggere chi **usa** la classe;
- l'**implementazione della classe** (*class implementation*) comprende i campi privati e il corpo di tutti i metodi, pubblici e privati. È ciò che interessa a chi **scrive** la classe.

Le regole di progetto per una classe ben incapsulata sono sei.

1. Premettere alla definizione un commento su come usare la classe.
2. Dichiarare **tutti i campi `private`**.
3. Fornire metodi `public` di accesso ai dati (accessor) e di manipolazione (mutator, e le altre operazioni).
4. Scrivere, prima di ogni metodo pubblico, un commento che spieghi **completamente come usarlo**.
5. Dichiarare `private` i **metodi ausiliari**, quelli che servono solo dentro la classe.
6. Descrivere con commenti, nel corpo, i dettagli di implementazione.

Un **metodo ausiliario** (*helper method*) è un metodo di servizio che la classe usa per sé: nessun altro deve poterlo chiamare, quindi lo si dichiara `private`. Per esempio un arrotondamento a due decimali:

```java
class Fattura {
    private double imponibile;
    private double aliquota;                              // 0.22 per il 22%

    public Fattura(double imponibile, double aliquota) {
        this.imponibile = imponibile;
        this.aliquota = aliquota;
    }

    public double totale() {
        return arrotonda(imponibile + imponibile * aliquota);   // usa il metodo ausiliario
    }

    private double arrotonda(double x) {                  // privato: dettaglio interno
        return Math.round(x * 100) / 100.0;
    }
}

public class ProvaFattura {
    public static void main(String[] args) {
        Fattura f = new Fattura(10.0, 0.22);
        System.out.println(f.totale());
    }
}
```

```text
12.2
```

`totale()` appartiene all'interfaccia; `arrotonda` no, e chiamare `f.arrotonda(1.234)` dal `main` darebbe l'errore `arrotonda(double) has private access in Fattura`.

Il vantaggio dell'interfaccia stabile si vede quando cambia l'implementazione. Una classe `Durata` che conserva minuti e secondi in due campi, e una versione che conserva un solo numero di secondi, si usano **allo stesso modo**:

```java
class Durata {                                           // versione 1: due campi
    private int minuti;
    private int secondi;

    public void setDurata(int minuti, int secondi) {
        this.minuti = minuti;
        this.secondi = secondi;
    }

    public int getMinuti() {
        return minuti;
    }

    public int getSecondi() {
        return secondi;
    }
}

class DurataCompatta {                                   // versione 2: un solo campo
    private int totaleSecondi;

    public void setDurata(int minuti, int secondi) {
        this.totaleSecondi = minuti * 60 + secondi;
    }

    public int getMinuti() {
        return totaleSecondi / 60;
    }

    public int getSecondi() {
        return totaleSecondi % 60;
    }
}

public class ProvaDurata {
    public static void main(String[] args) {
        Durata d1 = new Durata();
        d1.setDurata(3, 25);
        System.out.println(d1.getMinuti() + " min " + d1.getSecondi() + " s");

        DurataCompatta d2 = new DurataCompatta();
        d2.setDurata(3, 25);
        System.out.println(d2.getMinuti() + " min " + d2.getSecondi() + " s");
    }
}
```

```text
3 min 25 s
3 min 25 s
```

Le istruzioni del `main` sono identiche e i risultati anche, benché dentro le due classi i dati siano organizzati in modo diverso. Chi usa `Durata` non si accorgerebbe del passaggio alla seconda versione: è per questo che i campi si nascondono.

### 7.3.5 Precondizioni, postcondizioni e `javadoc`

Il commento che accompagna un metodo pubblico deve dire a chi lo usa **che cosa deve essere vero prima** di chiamarlo e **che cosa sarà vero dopo**. Si chiamano:

- **precondizione** (*precondition*): ciò che deve valere prima della chiamata, affinché il metodo funzioni;
- **postcondizione** (*postcondition*): ciò che il metodo garantisce dopo l'esecuzione (il valore restituito, o gli effetti sullo stato).

```java
/** Un conto con un saldo in euro. */
class Conto {
    private double saldo;

    public Conto(double saldoIniziale) {
        this.saldo = saldoIniziale;
    }

    /**
     * Preleva una somma dal conto.
     * Precondizione: l'importo è positivo e non supera il saldo.
     * Postcondizione: il saldo è diminuito dell'importo prelevato.
     *
     * @param importo la somma da prelevare
     */
    public void preleva(double importo) {
        saldo = saldo - importo;
    }

    /**
     * Restituisce il saldo attuale.
     *
     * @return il saldo in euro
     */
    public double getSaldo() {
        return saldo;
    }
}
```

I commenti tra `/**` e `*/` sono **commenti di documentazione**: l'utilità `javadoc`, fornita con il JDK, li legge e produce automaticamente la documentazione della classe in formato HTML. Per impostazione predefinita include i commenti di documentazione e le intestazioni dei membri **pubblici** (e `protected`), non quelli privati: è il modo di ottenere l'*interfaccia* della classe senza leggerne il codice. Un commento `/** ... */` va messo immediatamente prima del metodo o della classe a cui si riferisce; la forma `@param` e `@return` è quella riconosciuta dallo strumento per descrivere un parametro e il valore restituito. Ci sono molte pagine di documentazione che si leggono così: la Javadoc di Oracle citata in questi appunti è prodotta con lo stesso strumento.

In una prova scritta `javadoc` non si usa, ma i commenti pre/postcondizione sono un buon modo di ragionare sul metodo prima di scriverlo: la precondizione dice che cosa si può dare per scontato, la postcondizione dice che cosa il codice deve ottenere.

### 7.3.6 I quattro livelli di accesso

Oltre a `public` e `private`, esistono altri due livelli, in tutto quattro:

| Modificatore | Stessa classe | Stesso package | Sottoclassi, in un altro package | Qualunque classe |
|---|---|---|---|---|
| `private` | sì | no | no | no |
| *(nessun modificatore)*, o **package-private** | sì | sì | no | no |
| `protected` | sì | sì | sì | no |
| `public` | sì | sì | sì | sì |

Il livello **senza modificatore** (a volte detto di *package*) è quello che si ottiene semplicemente non scrivendo niente: il membro è visibile alle classi dello **stesso package** (sezione 7.6) e a nessun'altra. È ciò che accade alle classi senza `public` negli esempi in un file solo: tutte stanno nello stesso package, quindi si vedono tra loro. Il livello **`protected`** è un'estensione del livello di package: il membro è visibile nello stesso package *e* nelle **sottoclassi** (classi che estendono quella in cui il membro è dichiarato, argomento del [Capitolo 9 — Ereditarietà e polimorfismo](09-ereditarieta-e-polimorfismo.md)), anche se stanno in un altro package.

Per le **classi** i livelli ammessi sono solo due: `public` e quello di package. Una classe `private` o `protected` al primo livello è un errore di compilazione (`modifier private not allowed here`); i livelli `private` e `protected` si applicano ai membri.

> [!TIP]
> **Intuizione — Casa, condominio, famiglia, strada**
> `private` è la stanza chiusa a chiave: ci entra solo chi abita la casa (la classe). Il livello di package è il portone del condominio: lo aprono tutti i condomini (le classi dello stesso package). `protected` aggiunge i parenti stretti (le sottoclassi), anche se abitano in un altro condominio. `public` è il marciapiede: passa chiunque.

In pratica, per l'esame, la regola è semplice: **campi `private`, metodi e costruttori usati dall'esterno `public`**. `protected` si incontra con l'ereditarietà, e il livello di package è ciò che hanno per forza le classi di un file unico quando non si scrive `public`.

### 7.3.7 La perdita di riservatezza (*privacy leak*)

Rendere `private` un campo non basta, se il campo è di **tipo classe** o è un array e il suo valore esce dalla classe così com'è. Una variabile di tipo classe non contiene l'oggetto, ma un **riferimento** ad esso (se ne parla nel [Capitolo 8 — Riferimenti e memoria](08-riferimenti-e-memoria.md)); copiare la variabile copia il riferimento, non l'oggetto, e il risultato è che **due variabili indicano lo stesso oggetto**. Lo avevamo già visto con gli array (Capitolo 5, sezione 5.5.5). Con un oggetto accade lo stesso. Definiamo un punto con coordinate private e un segmento che ne contiene due:

```java
class Punto {
    private int x;
    private int y;

    public Punto(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public void setX(int x) {
        this.x = x;
    }
}

class Segmento {
    private Punto inizio;
    private Punto fine;

    public Segmento(Punto inizio, Punto fine) {
        this.inizio = inizio;                     // memorizza il riferimento ricevuto
        this.fine = fine;
    }

    public Punto getInizio() {
        return inizio;                            // restituisce il riferimento interno
    }

    public int lunghezzaOrizzontale() {
        return fine.getX() - inizio.getX();
    }
}

public class ProvaLeak {
    public static void main(String[] args) {
        Punto p = new Punto(0, 0);
        Punto q = new Punto(10, 0);
        Segmento s = new Segmento(p, q);
        System.out.println(s.lunghezzaOrizzontale());

        s.getInizio().setX(8);                    // modifica il segmento senza passare da un suo metodo
        System.out.println(s.lunghezzaOrizzontale());

        p.setX(-5);                               // anche p, rimasto al chiamante, è lo stesso oggetto
        System.out.println(s.lunghezzaOrizzontale());
    }
}
```

```text
10
2
15
```

I campi `inizio` e `fine` sono `private`, eppure il segmento è stato modificato tre volte senza usare nessun suo metodo. La prima volta in uscita: `getInizio()` ha restituito il riferimento al **vero** `Punto` interno, e `setX(8)` lo ha cambiato (lunghezza `10 - 8 = 2`). La seconda in ingresso: il costruttore ha memorizzato il riferimento ricevuto, quindi `p` e `s.inizio` sono lo stesso oggetto, e `p.setX(-5)` ha cambiato il segmento (lunghezza `10 - (-5) = 15`).

La cura è la **copia difensiva** (*defensive copy*): la classe non memorizza né restituisce mai il riferimento ricevuto o posseduto, ma ne fa una **copia** e la tiene (o la restituisce) al suo posto.

```java
class Segmento2 {
    private Punto inizio;
    private Punto fine;

    public Segmento2(Punto inizio, Punto fine) {
        this.inizio = new Punto(inizio.getX(), inizio.getY());    // copia del punto ricevuto
        this.fine = new Punto(fine.getX(), fine.getY());
    }

    public Punto getInizio() {
        return new Punto(inizio.getX(), inizio.getY());           // copia: l'originale non esce
    }

    public int lunghezzaOrizzontale() {
        return fine.getX() - inizio.getX();
    }
}
```

Con `Segmento2` il `main` precedente stamperebbe sempre `10`: `getInizio().setX(8)` e `p.setX(-5)` agiscono su copie e non toccano lo stato del segmento. Il problema si pone solo con campi di tipo **mutabile**: una `String` non ha metodi che la modifichino, quindi restituire un campo `String` non è una perdita di riservatezza. Le copie difensive e il modello dei riferimenti sono ripresi nel Capitolo 8.

### 7.3.8 I segni `+` e `-` nel diagramma delle classi

Nel diagramma UML la visibilità dei membri si indica con un segno davanti al nome: **`+`** per `public`, **`-`** per `private`. Il diagramma della classe `Acquisto` della sezione 7.3.3 diventa:

```text
+--------------------------------------------+
| Acquisto                                   |
+--------------------------------------------+
| - articolo: String                         |
| - quantita: int                            |
| - prezzoUnitario: double                   |
+--------------------------------------------+
| + Acquisto(String, int, double)            |
| + getArticolo(): String                    |
| + setArticolo(articolo: String): void      |
| + getQuantita(): int                       |
| + setQuantita(quantita: int): void         |
| + getPrezzoUnitario(): double              |
| + setPrezzoUnitario(prezzo: double): void  |
| + getTotale(): double                      |
+--------------------------------------------+
```

Una classe ben incapsulata ha nel diagramma una colonna di `-` per i dati e una di `+` per le operazioni.

## 7.4 Membri statici nelle classi con oggetti

I membri `static` (variabili di classe, costanti di classe, metodi statici) sono stati presentati nel [Capitolo 6](06-metodi.md), sezione 6.4. Qui li usiamo dentro classi che hanno anche oggetti, e vediamo la loro funzione principale: tenere traccia di qualcosa che **riguarda la classe nel suo complesso** e non un oggetto in particolare.

### 7.4.1 Contare gli oggetti creati

Come facciamo a sapere quanti oggetti di una classe sono stati creati? Un campo d'istanza non va bene, perché ogni oggetto ha il proprio e nessuno conosce gli altri. Serve un dato **condiviso**: una variabile `static`, che esiste in un'unica copia per la classe. Il posto giusto per incrementarla è il costruttore, perché viene eseguito a ogni creazione.

```java
class Ordine {
    private static int creati = 0;                // una sola copia, condivisa da tutti gli oggetti
    private int numero;                           // campo d'istanza: uno per oggetto

    public Ordine() {
        creati = creati + 1;                      // a ogni creazione il contatore comune sale
        this.numero = creati;                     // il numero dell'oggetto = il suo ordine di creazione
    }

    public int getNumero() {
        return numero;
    }

    public static int getCreati() {               // metodo statico: legge un dato di classe
        return creati;
    }
}

public class ProvaOrdine {
    public static void main(String[] args) {
        System.out.println("Creati: " + Ordine.getCreati());
        Ordine a = new Ordine();
        Ordine b = new Ordine();
        Ordine c = new Ordine();
        System.out.println(a.getNumero() + " " + b.getNumero() + " " + c.getNumero());
        System.out.println("Creati: " + Ordine.getCreati());
    }
}
```

```text
Creati: 0
1 2 3
Creati: 3
```

Seguiamo l'esecuzione. Prima di qualunque `new` il contatore vale 0 (il valore con cui è inizializzato): per questo la prima stampa mostra `Creati: 0`, anche se non esiste ancora nessun oggetto. Ogni `new Ordine()` esegue il costruttore, che incrementa `creati` e copia il nuovo valore nel campo `numero` dell'oggetto: il primo oggetto ottiene 1, il secondo 2, il terzo 3. Alla fine `creati` vale 3, e `Ordine.getCreati()` lo restituisce.

Il metodo `getCreati` è `static` perché non riguarda un oggetto e si vuole poterlo chiamare **anche prima** di crearne uno, come abbiamo fatto nella prima riga del `main`. La regola del Capitolo 6 vale ancora: un metodo statico non può usare direttamente i campi d'istanza (`numero`), perché non sa su quale oggetto lavorare. In un metodo statico non esiste nemmeno `this`.

### 7.4.2 Costanti di classe e campi `final`

La parola `final` davanti a una variabile la rende **non modificabile dopo la prima assegnazione**. Se la variabile è anche `static`, abbiamo una **costante di classe** (`public static final double RAGGIO_PREDEFINITO = 1.0;` nella classe `Sfera`), per convenzione con nome in maiuscolo.

Un campo **d'istanza** può essere `final`: ogni oggetto ha la sua copia, che riceve il valore una volta sola, nel costruttore (o nella dichiarazione), e non può più cambiare. È lo strumento giusto per un dato che non deve mutare dopo la nascita dell'oggetto, come il numero d'ordine.

```java
class OrdineFisso {
    private static int creati = 0;
    private final int numero;                     // assegnato una sola volta

    public OrdineFisso() {
        creati = creati + 1;
        numero = creati;                          // prima (e unica) assegnazione: nel costruttore
    }

    public int getNumero() {
        return numero;
    }
}

public class ProvaFinal {
    public static void main(String[] args) {
        OrdineFisso a = new OrdineFisso();
        OrdineFisso b = new OrdineFisso();
        System.out.println(a.getNumero() + " " + b.getNumero());
    }
}
```

```text
1 2
```

Per un campo `final` si scrive il solo `get`, e non il `set`: è l'unico modo in cui la classe può garantire che il valore non cambi. Tentare di riassegnarlo in un altro metodo è un errore di compilazione: `cannot assign a value to final variable numero`.

La parola `final` si usa anche davanti a un metodo e a una classe, con effetti legati all'ereditarietà (un metodo `final` non si può ridefinire in una sottoclasse, una classe `final` non si può estendere): ne riparliamo con l'ereditarietà nel Capitolo 9.

## 7.5 Le enumerazioni come classi

Nel [Capitolo 4 — Strutture di controllo](04-strutture-di-controllo.md), sezione 4.4, abbiamo usato l'`enum` come un elenco di costanti. Adesso possiamo dire che cos'è davvero: **un `enum` è una classe** con un numero **fisso e finito di oggetti**, quelli elencati nella dichiarazione. Non si possono creare altri oggetti con `new`: le costanti dell'elenco sono le sole istanze che esistono. Come ogni classe, un `enum` può avere campi, un costruttore e metodi.

```java
enum Suit {
    CLUBS("nero"), DIAMONDS("rosso"), HEARTS("rosso"), SPADES("nero");   // elenco delle costanti, con argomenti

    private final String colore;                  // campo d'istanza: ogni costante ha il proprio

    Suit(String colore) {                         // costruttore, eseguito una volta per costante
        this.colore = colore;
    }

    public String getColore() {
        return colore;
    }

    public boolean isRosso() {
        return colore.equals("rosso");
    }
}

public class ProvaSuit {
    public static void main(String[] args) {
        for (Suit s : Suit.values()) {
            System.out.println(s + " -> " + s.getColore() + ", rosso: " + s.isRosso());
        }
    }
}
```

```text
CLUBS -> nero, rosso: false
DIAMONDS -> rosso, rosso: true
HEARTS -> rosso, rosso: true
SPADES -> nero, rosso: false
```

Il codice si legge nell'ordine seguente.

1. **L'elenco delle costanti viene per primo** e se dopo ci sono altri membri si chiude con il **punto e virgola**. Ogni costante può avere argomenti tra parentesi: `CLUBS("nero")` crea l'oggetto `CLUBS` chiamando il costruttore con l'argomento `"nero"`.
2. Il **costruttore** `Suit(String colore)` ha il nome della classe e nessun tipo di ritorno, come ogni costruttore. Non si dichiara `public`: nei `enum` il costruttore è sempre privato, scritto o no, e si esegue una sola volta per costante, quando la classe viene caricata. Nessun codice può chiamarlo con `new Suit(...)`: l'insieme delle costanti è chiuso.
3. I **campi** e i **metodi** si scrivono come in una classe qualunque: `getColore` e `isRosso` lavorano sul campo `colore` della costante su cui sono chiamati.
4. `Suit.values()` restituisce un array con tutte le costanti, nell'ordine di dichiarazione (Capitolo 4, sezione 4.4.3): il `for` le percorre e `System.out.println(s + ...)` stampa il nome della costante.

Perché le costanti di un `enum` si confrontano con `==` e non con `equals`? Perché ciascuna è **un unico oggetto**: `Suit.HEARTS` indica sempre lo stesso oggetto, in tutto il programma, e due variabili che valgono `Suit.HEARTS` sono alla lettera due nomi dello stesso oggetto.

> [!NOTE]
> **Approfondimento esterno — Il costruttore di `java.lang.Enum`**
> Ogni `enum` estende implicitamente la classe `java.lang.Enum`. La Javadoc della classe riporta il suo unico costruttore, `protected Enum(String name, int ordinal)`, e dice: "Sole constructor. Programmers cannot invoke this constructor. It is for use by code emitted by the compiler in response to enum class declarations." In altre parole, i nomi e gli ordinali delle costanti (`name()`, `ordinal()` del Capitolo 4) sono assegnati dal compilatore, non dal programmatore, e il costruttore che si scrive in un `enum` aggiunge soltanto i *propri* campi.
>
> *Fonte:* [java.lang.Enum (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Enum.html)

## 7.6 I package

### 7.6.1 Che cos'è un package

Quando i programmi crescono, le classi diventano centinaia, e due problemi si presentano. Il primo è di ordine: serve un modo di raggrupparle per argomento, come si fa con i file nelle cartelle. Il secondo è di nomi: due programmatori diversi possono, senza saperlo, chiamare `Punto` o `Data` due classi diverse, e se i programmi si incontrano il compilatore non sa quale sia quale. Il **package** risolve entrambi.

> [!NOTE]
> **Definizione — Package**
> Un **package** è una raccolta di classi raggruppate sotto un nome, e corrisponde a una **cartella** nel file system. Ogni classe del package sta in un file proprio e inizia con la riga `package nomePackage;`, che deve essere la **prima istruzione del file** (sono ammessi solo commenti prima).

Il nome del package dice al compilatore **in quale cartella** stanno le classi: i punti del nome diventano i separatori delle cartelle, e la ricerca parte dalla cartella di base (la cartella corrente, per default). Il package `negozio` sta nella cartella `negozio`; il package `negozio.magazzino` nella sottocartella `negozio/magazzino`. Per convenzione i nomi dei package si scrivono in minuscolo.

Costruiamo un programma con due package, `negozio` e `app`:

```text
progetto/
├── negozio/
│   └── Articolo.java        (package negozio)
└── app/
    └── Vendita.java         (package app, contiene il main)
```

```java
// File: negozio/Articolo.java
package negozio;

public class Articolo {
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
}
```

```java
// File: app/Vendita.java
package app;

import negozio.Articolo;                          // da qui in poi basta scrivere Articolo

public class Vendita {
    public static void main(String[] args) {
        Articolo a = new Articolo("Penna", 1.5);
        System.out.println(a.getNome() + " costa " + a.getPrezzo());
    }
}
```

```text
Penna costa 1.5
```

Dalla cartella `progetto` si compila con `javac negozio/Articolo.java app/Vendita.java` e si esegue con `java app.Vendita`: il comando `java` vuole il nome **completo** della classe (`app.Vendita`), con il package davanti, perché cerca il file `app/Vendita.class`. Due osservazioni su ciò che abbiamo scritto:

- la classe `Articolo`, il suo costruttore e i suoi metodi sono dichiarati `public`: stanno in un package diverso da quello di `Vendita`, e senza `public` (livello di package, sezione 7.3.6) `Vendita` non potrebbe usarli;
- `Vendita` ha bisogno dell'`import`, perché `Articolo` è in un altro package. Le classi dello **stesso** package si vedono per nome, senza `import`.

### 7.6.2 `import`, nomi completi e conflitti di nome

L'istruzione `import` l'abbiamo già incontrata nel [Capitolo 1](01-java-e-la-jvm.md), sezione 1.5.4: permette di scrivere il nome **breve** di una classe di un altro package invece del **nome completo** (*fully qualified name*), formato dal nome del package, un punto e il nome della classe (`java.util.Scanner`). Lo stesso `import` vale per le classi scritte da noi, come `import negozio.Articolo;`. Le istruzioni `import` stanno dopo la riga `package` (se c'è) e prima della definizione della classe. Il package `java.lang` è importato implicitamente.

I package risolvono anche il problema dei **conflitti di nome** (*name clashes*): due classi con lo stesso nome breve ma in package diversi non entrano in conflitto, perché il nome completo le distingue. Un caso reale nella libreria standard: esistono sia `java.util.Date` sia `java.sql.Date`.

> [!NOTE]
> **Approfondimento esterno — Due classi `Date`**
> La Javadoc descrive `java.util.Date` così: "The class `Date` represents a specific instant in time, with millisecond precision." La classe `java.sql.Date`, dichiarata `public class Date extends java.util.Date`, è descritta come "A thin wrapper around a millisecond value that allows JDBC to identify this as an SQL `DATE` value." Sono dunque due classi diverse che si chiamano alla stessa maniera (la seconda si usa con le basi di dati, [Capitolo 21](21-jdbc.md)), e in un programma che le usa entrambe la distinzione si fa con il nome completo.
>
> *Fonte:* [java.util.Date](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Date.html) e [java.sql.Date](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/Date.html) (Java SE 17)

Per usarle nello stesso file si importa al più una delle due, e l'altra si scrive con il nome completo:

```java
import java.util.Date;                            // importata: nome breve Date

public class DueDate {
    public static void main(String[] args) {
        Date a = new Date(0L);                    // java.util.Date
        java.sql.Date b = new java.sql.Date(0L);  // nome completo: nessuna ambiguità
        System.out.println(a.getTime());
        System.out.println(b.getTime());
    }
}
```

```text
0
0
```

Il valore `0L` è un istante di partenza (l'origine dei tempi di Java, il 1° gennaio 1970); `getTime()` restituisce i millisecondi trascorsi dall'origine, e vale `0` per entrambe. Importarle **tutte e due** produrrebbe un errore di compilazione: `a type with the same simple name is already defined by the single-type-import of Date`.

### 7.6.3 Package e prove scritte

All'appello il codice si scrive in **un solo file**, senza package: le classi stanno tutte nello stesso package (quello anonimo) e si vedono per nome, quindi non servono né la riga `package` né gli `import` per le classi dell'esercizio. Gli `import` servono invece per le classi della libreria fuori da `java.lang` (`Scanner`, `ArrayList`, `File`…). Una riga `package` aggiunta per abitudine a un file d'esame può impedire l'esecuzione: con `package app;` in cima, il comando `java Vendita` risponde `Error: Could not find or load main class Vendita` (il nome completo è `app.Vendita`).

## 7.7 Collaudare una classe

Scritta una classe, bisogna provarla. Il metodo più semplice è un **collaudo** (*test*) scritto in Java: un programma, di solito un `main`, che crea oggetti, chiama i metodi e controlla che i risultati siano quelli attesi. L'idea è di collaudare ogni **unità** (un metodo, una classe) separatamente (*unit testing*): l'insieme dei collaudi di una classe si chiama *test suite*, e rieseguirlo dopo ogni modifica per verificare che nulla sia stato rotto si chiama *regression testing* (collaudo di regressione).

```java
class Cassa {
    private int totale;

    public void incassa(int importo) {
        totale = totale + importo;
    }

    public int getTotale() {
        return totale;
    }
}

public class CollaudoCassa {
    public static void main(String[] args) {
        Cassa c = new Cassa();
        controlla("cassa nuova", 0, c.getTotale());

        c.incassa(30);
        c.incassa(12);
        controlla("dopo due incassi", 42, c.getTotale());
    }

    static void controlla(String prova, int atteso, int ottenuto) {
        if (atteso == ottenuto) {
            System.out.println("OK   " + prova);
        } else {
            System.out.println("FAIL " + prova + ": atteso " + atteso + ", ottenuto " + ottenuto);
        }
    }
}
```

```text
OK   cassa nuova
OK   dopo due incassi
```

Il metodo `controlla` confronta il valore atteso con quello ottenuto e stampa un esito. Il collaudo copre il caso più semplice (la cassa appena creata) e un caso con due operazioni: pochi casi scelti bene, compresi quelli limite (zero, valori negativi, un solo elemento), valgono più di molti casi simili.

> [!WARNING]
> **Attenzione — Stampare un oggetto non mostra i suoi dati**
> Se si prova a stampare un oggetto con `System.out.println(c)`, il risultato non è il contenuto dei campi ma qualcosa come `Cassa@1b6d3586` (il nome della classe, una `@` e un numero esadecimale). È il comportamento predefinito di ogni oggetto. Per stampare i dati bisogna scrivere un metodo `toString` nella propria classe, e se ne parla nel [Capitolo 9 — Ereditarietà e polimorfismo](09-ereditarieta-e-polimorfismo.md). Finché non c'è, si stampa chiamando gli accessor (`c.getTotale()`).

> [!NOTE]
> **Approfondimento esterno — `Object.toString`**
> La Javadoc di `java.lang.Object` descrive il metodo `public String toString()`, che "returns a string representation of the object". Per la classe `Object` quella stringa è formata da "the name of the class of which the object is an instance, the at-sign character `@`, and the unsigned hexadecimal representation of the hash code of the object", cioè `getClass().getName() + '@' + Integer.toHexString(hashCode())`. Poiché ogni classe estende `Object` (Capitolo 9), questo è il comportamento di tutte le classi che non ridefiniscono `toString`.
>
> *Fonte:* [java.lang.Object#toString (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#toString())

## 7.8 Dal testo della traccia alla classe

Nelle prove la classe da scrivere è descritta a parole, con un linguaggio ricorrente. Conviene imparare a **tradurlo** nel codice, un pezzo per volta, perché ogni pezzo è un punto di aderenza letterale.

| La traccia dice | Nel codice |
|---|---|
| "Definire la classe `Nome`" | `class Nome { ... }` con **esattamente** quel nome |
| "testuale" | tipo `String` |
| "numero con la virgola" | tipo `double` |
| "intero" | tipo `int` |
| "booleano" | tipo `boolean` |
| "il costruttore riceve nell'ordine *a*, *b*, *c*" | un costruttore con tre parametri **in quell'ordine**, e con i tipi corrispondenti |
| "tutte le variabili d'istanza devono essere private" | **ogni** campo `private`, nessuna eccezione |
| "i relativi metodi `get` e `set`" | un `getX` e un `setX` per ogni campo, con i nomi regolari (sezione 7.3.3) |
| "due costruttori in overload" | due costruttori con firme diverse (sezione 7.2.4) |
| "il metodo `nome` che non riceve parametri e restituisce una stringa" | `public String nome() { ... }` |
| "restituisce un booleano … `true` se …, altrimenti `false`" | tipo di ritorno `boolean` e un `return true`/`return false` su ogni percorso |
| "sovrascrive il valore" | un'assegnazione al campo: il campo contiene il nuovo valore |

Un esempio completo, con una traccia nuova scritta nello stile degli appelli.

#### Esempio — Una classe da una traccia

*La traccia.* Definire la classe `Tessera`, il cui costruttore riceve nell'ordine il codice (testuale), il saldo iniziale (numero con la virgola) e il nome del titolare (testuale). Tutte le variabili d'istanza devono essere private. Definire il metodo `ricarica`, che riceve un importo (numero con la virgola) e restituisce un booleano: se l'importo non è positivo restituisce `false`; altrimenti somma l'importo al saldo e restituisce `true`. Definire il metodo `descrizione`, che non riceve parametri e restituisce una stringa nella forma `"tessera " + codice + ": " + saldo + " euro"`. Con `new Tessera("T-7", 10.0, "Anna")` e le ricariche `-5.0` e `15.5` si ottiene:

```text
tessera T-7: 10.0 euro
false
tessera T-7: 10.0 euro
true
tessera T-7: 25.5 euro
```

*La traduzione.* Dalla traccia si ricavano nell'ordine: tre campi privati (`String codice`, `double saldo`, `String titolare`); un costruttore a tre parametri *nell'ordine dato*; un metodo `ricarica` con parametro `double` e ritorno `boolean`; un metodo `descrizione` senza parametri con ritorno `String`. Il testo non chiede `get` né `set`, quindi non si scrivono.

```java
class Tessera {
    private String codice;                               // tutte private, come richiesto
    private double saldo;
    private String titolare;

    public Tessera(String codice, double saldo, String titolare) {    // ordine: codice, saldo, titolare
        this.codice = codice;
        this.saldo = saldo;
        this.titolare = titolare;
    }

    public boolean ricarica(double importo) {
        if (importo <= 0) {
            return false;                                // importo non positivo: nessuna modifica
        }
        saldo = saldo + importo;                         // sovrascrive il saldo
        return true;
    }

    public String descrizione() {
        return "tessera " + codice + ": " + saldo + " euro";
    }
}

public class ProvaTessera {
    public static void main(String[] args) {
        Tessera t = new Tessera("T-7", 10.0, "Anna");
        System.out.println(t.descrizione());
        System.out.println(t.ricarica(-5.0));
        System.out.println(t.descrizione());
        System.out.println(t.ricarica(15.5));
        System.out.println(t.descrizione());
    }
}
```

```text
tessera T-7: 10.0 euro
false
tessera T-7: 10.0 euro
true
tessera T-7: 25.5 euro
```

L'output coincide con quello richiesto. Notiamo che il campo `titolare` non viene mai letto: la traccia lo vuole nel costruttore, quindi esiste e si memorizza, anche se nessun metodo lo usa. Togliere un campo "inutile" sarebbe uno scostamento dalla traccia.

## Come esce all'esame

**EXAM1 — Esercizio 3 (13 punti), ereditarietà, thread e information hiding.** La traccia forniva già una classe `Persona`, con un costruttore `(String nome, String cognome)`, e chiedeva di scrivere una sottoclasse `Studente` che realizza `Runnable`. Per questo capitolo contano tre requisiti: **due costruttori in overload** di `Studente`, il primo con parametri `nome`, `cognome`, `matricola` (intero), il secondo con `matricola` (intero) e `cds` (testuale); un metodo `run` che eleva la `matricola` al quadrato e ne **sovrascrive** il valore; e il **vincolo architetturale** "usare rigorosamente l'information hiding: tutte le variabili d'istanza `private` e i relativi metodi `get` e `set`". I concetti del capitolo che servivano sono i costruttori con firme diverse e parametri nell'ordine richiesto (sezioni 7.2.2 e 7.2.4), i campi privati con accessor e mutator regolari (7.3.2 e 7.3.3) e l'uso di `this` per distinguere campo e parametro (7.1.8). Il secondo costruttore non riceve né nome né cognome, e come inizializzare la parte ereditata da `Persona` è un tema del [Capitolo 9](09-ereditarieta-e-polimorfismo.md); `Runnable` e `run` sono nel [Capitolo 17](17-thread.md). Vincoli letterali: i **nomi** dei campi e dei metodi (`matricola`, `cds`), l'**ordine** dei parametri dei due costruttori, `private` su **tutti** i campi, un `get` e un `set` per ciascuno.

**Appello dell'8 luglio 2026 (EXAM3) — Esercizio 1 (5 punti), OOP di base con interfacce.** La traccia chiedeva un'interfaccia `Figura` con un metodo `area` che restituisce un numero con la virgola, una classe `Rettangolo` "il cui costruttore riceve nell'ordine la base e l'altezza", una classe `Quadrato` "il cui costruttore riceve la misura del lato", entrambe realizzazioni di `Figura`, con "tutte le variabili d'istanza private". L'output atteso mostrava l'area di `Rettangolo(3.0, 4.0)` (`12.0`) e di `Quadrato(3.0)` (`9.0`). Del capitolo servono il costruttore con parametri **nell'ordine dato** (7.2.2), i campi privati (7.3.2) e un metodo senza parametri che restituisce un `double` calcolato dai campi (7.1.3); l'interfaccia e il suo uso "attraverso il tipo `Figura`" sono nel [Capitolo 10](10-classi-astratte-e-interfacce.md). Vincoli letterali: i nomi delle classi e del metodo, l'ordine base/altezza, `private` su tutti i campi.

**Appello dell'8 settembre 2026 (EXAM4) — Esercizio 1 (13 punti), classi annidate e information hiding.** La traccia chiedeva una classe `Asta` con un costruttore che riceve nell'ordine "il codice dell'asta (testuale), la quota di partenza (numero con la virgola) e il nome del miglior offerente (testuale)", con "tutte le variabili d'istanza rigorosamente private, nel rispetto dell'information hiding", e dentro di essa una classe annidata **non statica** `Offerta`, anch'essa con campi privati, con due metodi: `stato`, che restituisce una stringa in un formato imposto, e `aggiungiOfferta`, che restituisce un `boolean` e, se l'importo non è inferiore alla quota attuale, aggiorna quota e miglior offerente e restituisce `true`. Del capitolo servono il costruttore a tre parametri nell'ordine prescritto, i campi privati (sezioni 7.2 e 7.3), un metodo che restituisce un `boolean` e **modifica lo stato** (7.1.7 e lo scheletro "Un metodo che modifica lo stato e restituisce un booleano") e la traduzione di "testuale" e "numero con la virgola" in `String` e `double` (7.8). La struttura annidata è nel [Capitolo 11](11-classi-annidate.md). Vincoli letterali: l'**ordine** dei parametri del costruttore, `private` sui campi di **entrambe** le classi, e la stringa restituita da `stato`, con i suoi spazi e la sua punteggiatura, da copiare carattere per carattere dalla traccia.

## Scheletri da esame

### Una classe con campi privati, costruttore, `get` e `set`

*Quando si usa:* la traccia chiede una classe con "variabili d'istanza private" e i relativi `get` e `set`. Quasi ogni esercizio sulle classi parte da qui.

```java
class Corso {
    private String nome;                                   // ogni campo private
    private int crediti;

    public Corso(String nome, int crediti) {               // parametri nell'ordine della traccia
        this.nome = nome;                                  // this: campo a sinistra, parametro a destra
        this.crediti = crediti;
    }

    public String getNome() {                              // get + nome del campo con l'iniziale maiuscola
        return nome;
    }

    public void setNome(String nome) {                     // set + nome del campo, parametro dello stesso tipo
        this.nome = nome;
    }

    public int getCrediti() {
        return crediti;
    }

    public void setCrediti(int crediti) {
        this.crediti = crediti;
    }
}

public class ProvaCorso {
    public static void main(String[] args) {
        Corso c = new Corso("Programmazione a Oggetti", 9);
        c.setCrediti(c.getCrediti() + 3);
        System.out.println(c.getNome() + ": " + c.getCrediti() + " crediti");
    }
}
```

```text
Programmazione a Oggetti: 12 crediti
```

Nessun `import`, nessuna eccezione da dichiarare. Il `main` di prova di solito non va scritto: la classe di collaudo c'è già e chiama i metodi. I nomi (classe, campi, metodi) e l'ordine dei parametri si copiano dalla traccia senza cambiarli.

### Costruttori in overload, uno che richiama l'altro

*Quando si usa:* la traccia chiede "due costruttori in overload" con parametri diversi.

```java
class Atleta {
    private String nome;
    private String cognome;
    private int numero;
    private String squadra;

    public Atleta(String nome, String cognome, int numero) {     // primo: nome, cognome, numero
        this.nome = nome;
        this.cognome = cognome;
        this.numero = numero;
        this.squadra = "nessuna";
    }

    public Atleta(int numero, String squadra) {                  // secondo: numero, squadra (firma diversa)
        this("sconosciuto", "sconosciuto", numero);              // riusa il primo: prima istruzione
        this.squadra = squadra;
    }

    public String descrizione() {
        return nome + " " + cognome + " #" + numero + " (" + squadra + ")";
    }
}

public class ProvaAtleta {
    public static void main(String[] args) {
        System.out.println(new Atleta("Carla", "Bianchi", 7).descrizione());
        System.out.println(new Atleta(10, "Messina").descrizione());
    }
}
```

```text
Carla Bianchi #7 (nessuna)
sconosciuto sconosciuto #10 (Messina)
```

Nessun `import`, nessuna eccezione. Le due firme `(String, String, int)` e `(int, String)` sono diverse per numero e tipo dei parametri, quindi `new` sceglie senza ambiguità. `this(...)` deve essere la **prima** istruzione del costruttore; dopo si può assegnare il resto.

### Un contatore di oggetti e una costante di classe

*Quando si usa:* la traccia chiede di "contare quanti oggetti sono stati creati" o di dare a ogni oggetto un numero progressivo.

```java
class Pratica {
    public static final String PREFISSO = "PR-";             // costante di classe
    private static int contatore = 0;                        // una sola copia per la classe

    private final String codice;                             // uno per oggetto, assegnato una volta

    public Pratica() {
        contatore++;                                         // il costruttore incrementa il contatore comune
        this.codice = PREFISSO + contatore;
    }

    public String getCodice() {
        return codice;
    }

    public static int getContatore() {                       // statico: si chiama sulla classe
        return contatore;
    }
}

public class ProvaPratica {
    public static void main(String[] args) {
        new Pratica();
        Pratica p = new Pratica();
        System.out.println(p.getCodice());
        System.out.println(Pratica.getContatore() + " pratiche");
    }
}
```

```text
PR-2
2 pratiche
```

Nessun `import`, nessuna eccezione. Il contatore deve essere `static`: se fosse un campo d'istanza ogni oggetto ne avrebbe uno suo, sempre a `1`. Un campo `final` si assegna nel costruttore e non ha `set`.

### Un metodo che modifica lo stato e restituisce un booleano

*Quando si usa:* la traccia dice "restituisce `false` se …, altrimenti aggiorna … e restituisce `true`".

```java
class Serbatoio {
    private double capacita;
    private double livello;

    public Serbatoio(double capacita) {
        this.capacita = capacita;
        this.livello = 0;
    }

    public boolean rifornisci(double litri) {
        if (litri <= 0 || livello + litri > capacita) {
            return false;                                    // caso rifiutato: lo stato non cambia
        }
        livello = livello + litri;                           // caso accettato: sovrascrive il livello
        return true;                                         // return su ogni percorso
    }

    public String stato() {
        return "livello " + livello + " su " + capacita;
    }
}

public class ProvaSerbatoio {
    public static void main(String[] args) {
        Serbatoio s = new Serbatoio(50.0);
        System.out.println(s.rifornisci(30.0));
        System.out.println(s.rifornisci(30.0));
        System.out.println(s.stato());
    }
}
```

```text
true
false
livello 30.0 su 50.0
```

Nessun `import`, nessuna eccezione. La condizione di rifiuto si scrive per prima e si conclude con `return false`; il ramo normale modifica lo stato e termina con `return true`. Il confronto tra importo e limite va letto con attenzione nella traccia (`<` o `<=`, `>` o `>=`).

### Un `enum` con un campo e un costruttore

*Quando si usa:* i valori ammessi sono pochi e fissi e ciascuno porta con sé un dato.

```java
enum Taglia {
    S(36), M(40), L(44);                                     // le costanti chiamano il costruttore; ';' obbligatorio

    private final int misura;                                // campo privato, uno per costante

    Taglia(int misura) {                                     // costruttore: nome dell'enum, nessun public
        this.misura = misura;
    }

    public int getMisura() {
        return misura;
    }
}

public class ProvaTaglia {
    public static void main(String[] args) {
        for (Taglia t : Taglia.values()) {
            System.out.println(t + " = " + t.getMisura());
        }
    }
}
```

```text
S = 36
M = 40
L = 44
```

Nessun `import`, nessuna eccezione. L'elenco delle costanti viene prima di ogni altro membro e termina con `;` se seguono campi o metodi. Il costruttore di un `enum` non si dichiara `public` e non si chiama mai con `new`.

## Errori tipici

Alcuni errori sono già discussi nel testo: accedere a un membro `private` da un'altra classe (sezione 7.3.2), dimenticare che il costruttore di default sparisce (7.2.3), dare a un parametro lo stesso nome di un campo e scrivere `x = x` senza `this` (7.1.8), `this(...)` non come prima istruzione (7.2.5), la perdita di riservatezza (7.3.7), la riassegnazione di un campo `final` (7.4.2), i due `import` di `Date` (7.6.2) e la riga `package` in un file d'esame (7.6.3). Seguono gli altri.

> [!CAUTION]
> **Errore tipico — Un costruttore con `void`**
> ```java
> class Persona {
>     private String nome;
>     public void Persona(String nome) {          // con void non è un costruttore: è un metodo
>         this.nome = nome;
>     }
> }
> // nel main:
> Persona p = new Persona("Anna");                // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `constructor Persona in class Persona cannot be applied to given types`. Poiché `Persona(String)` con `void` è un normale metodo, la classe è rimasta **senza costruttori** e ha ricevuto quello di default, senza parametri. Peggio ancora: `new Persona()` compilerebbe, creando un oggetto con `nome` a `null` senza alcun avviso. Forma corretta: `public Persona(String nome) { ... }`, senza tipo di ritorno.

> [!CAUTION]
> **Errore tipico — Chiamare un metodo d'istanza sulla classe**
> ```java
> class Automobile {
>     public void stampa() { System.out.println("auto"); }
> }
> // nel main:
> Automobile.stampa();                            // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `non-static method stampa() cannot be referenced from a static context`. Un metodo d'istanza lavora su un oggetto e non si può chiamare con il nome della classe. Forma corretta: `new Automobile().stampa();`, oppure una variabile `Automobile a = new Automobile(); a.stampa();`. Se invece il metodo non usa nessun dato dell'oggetto, può essere dichiarato `static`.

> [!CAUTION]
> **Errore tipico — Un campo d'istanza usato da un metodo statico**
> ```java
> public class Conteggio {
>     private int totale = 0;                     // campo d'istanza
>     public static void main(String[] args) {
>         totale = totale + 1;                    // ERRORE DI COMPILAZIONE
>     }
> }
> ```
> Il compilatore risponde `non-static variable totale cannot be referenced from a static context`. Il `main` è statico, quindi non lavora su nessun oggetto e il campo `totale` non appartiene a nessuno. Forma corretta: creare un oggetto e usare il campo attraverso di esso (o dichiarare il campo `static`, se un dato per tutta la classe è davvero ciò che serve).

> [!CAUTION]
> **Errore tipico — Dichiarare una variabile ma non creare l'oggetto**
> ```java
> Automobile a;
> a.stampa();                                     // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `variable a might not have been initialized`: la variabile esiste ma non contiene nessun oggetto. Forma corretta: `Automobile a = new Automobile();`. Se la variabile fosse un **campo** di una classe, il compilatore non protesterebbe e il programma terminerebbe in esecuzione con una `NullPointerException`, perché il campo vale `null` finché non gli si assegna un oggetto (Capitolo 8).

> [!CAUTION]
> **Errore tipico — Argomenti del costruttore in ordine o tipo sbagliato**
> ```java
> // classe: public Tessera(String codice, double saldo, String titolare)
> Tessera t = new Tessera(10.0, "T-7", "Anna");   // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `incompatible types: double cannot be converted to String`, indicando il primo argomento che non ha il tipo richiesto (se la classe avesse più costruttori, direbbe `no suitable constructor found for Tessera(double,String,String)` e li elencherebbe). Il costruttore vuole `(String, double, String)` e non `(double, String, String)`. Peggio sarebbe un errore silenzioso: se due parametri consecutivi avessero lo **stesso tipo** (due `String`, due `double`), scambiarli **compilerebbe** e il programma darebbe risultati sbagliati. Per questo l'ordine della traccia si segue alla lettera.

> [!CAUTION]
> **Errore tipico — Una variabile locale al posto del campo**
> ```java
> class Automobile {
>     private int velocita;
>     public Automobile() {
>         int velocita = 50;                      // nuova variabile locale: il campo non cambia
>     }
>     public int getVelocita() {
>         return velocita;                        // restituisce il campo: vale ancora 0
>     }
> }
> ```
> Il programma compila e `new Automobile().getVelocita()` restituisce `0` invece di `50`. Scrivendo il **tipo** davanti al nome (`int velocita = 50;`) si dichiara una variabile locale che nasconde il campo e sparisce alla fine del costruttore. Forma corretta: `velocita = 50;` oppure `this.velocita = 50;`, senza il tipo.

> [!CAUTION]
> **Errore tipico — Un contatore d'istanza al posto di un contatore di classe**
> ```java
> class Pratica {
>     private int contatore = 0;                  // manca static: uno per ogni oggetto
>     private int numero;
>     public Pratica() {
>         contatore = contatore + 1;
>         numero = contatore;                     // vale sempre 1
>     }
> }
> ```
> Compila e non segnala niente, ma ogni oggetto ha il **proprio** `contatore`, che parte da 0 e arriva a 1: tutte le pratiche ottengono il numero 1. Forma corretta: `private static int contatore = 0;`.

> [!CAUTION]
> **Errore tipico — Il costruttore salta i controlli del mutator**
> ```java
> class Corso {
>     private int crediti;
>     public Corso(int crediti) {
>         this.crediti = crediti;                 // assegna direttamente: nessun controllo
>     }
>     public void setCrediti(int crediti) {
>         if (crediti > 0) {
>             this.crediti = crediti;
>         }
>     }
> }
> ```
> `new Corso(-9)` crea un corso con crediti negativi, anche se `setCrediti(-9)` lo rifiuterebbe. Il controllo vale solo per la strada che lo contiene. Forma corretta: il costruttore chiama il mutator (`setCrediti(crediti);`), come nella classe `Acquisto` della sezione 7.3.3, così il controllo è scritto una volta e vale ovunque.

> [!CAUTION]
> **Errore tipico — Nomi dei metodi che non seguono la regola `get`/`set`**
> ```java
> class Corso {
>     private String nome;
>     public String getnome() {                   // iniziale minuscola: non è getNome
>         return nome;
>     }
> }
> // nel main:
> System.out.println(c.getNome());                // ERRORE DI COMPILAZIONE
> ```
> Il compilatore risponde `cannot find symbol`, perché Java distingue maiuscole e minuscole e `getnome` non è `getNome`. All'esame il caso più insidioso è quello in cui il codice di collaudo chiama `getNome()` e il metodo scritto ha un altro nome: non compila, e l'esecuzione è persa. Forma corretta: `get` o `set`, poi il nome del campo con l'**iniziale maiuscola** e il resto come nel campo.

> [!CAUTION]
> **Errore tipico — Un campo non `private` quando la traccia lo impone**
> ```java
> class Corso {
>     private String nome;
>     int crediti;                                // nessun modificatore: visibile a tutto il package
>     public int bonus;                           // pubblico
> }
> ```
> Il codice compila e funziona, ma viola il vincolo "tutte le variabili d'istanza private": il test nascosto non lo vede, mentre la correzione sì (aderenza letterale). Con `int crediti;` il campo ha il livello di package, che è facile da lasciare per distrazione perché non si scrive nulla. Forma corretta: `private` davanti a **ogni** campo.

> [!CAUTION]
> **Errore tipico — Un `enum` con il costruttore pubblico, istanziato con `new` o senza `;`**
> ```java
> enum Taglia {
>     S(36), M(40)                                // ERRORE: manca il ';' prima del primo membro
>     private final int misura;
>     public Taglia(int misura) {                 // ERRORE: public non ammesso
>         this.misura = misura;
>     }
> }
> // nel main:
> Taglia t = new Taglia(44);                      // ERRORE: un enum non si istanzia
> ```
> Il compilatore segnala per primo l'errore di sintassi (con JDK 22 `',', '}', or ';' expected` alla riga `private final int misura;`, perché dopo l'elenco delle costanti manca il punto e virgola). Corretto quello, compaiono `modifier public not allowed here` per il costruttore e `enum classes may not be instantiated` per il `new` (con JDK 11: `enum types may not be instantiated`). Forma corretta: l'elenco termina con `;` quando seguono altri membri, il costruttore non ha modificatore (è sempre privato), e i soli oggetti sono le costanti dell'elenco.

> [!CAUTION]
> **Errore tipico — Una classe con un nome diverso da quello della traccia**
> ```java
> class Rettangolo {                              // la traccia chiedeva "Rettangolo"
>     private double base;
>     public Rettangolo(double base, double altezza) { ... }
> }
> // il collaudo chiama: new Rettangle(3.0, 4.0)     // ERRORE DI COMPILAZIONE
> ```
> Se il codice di collaudo usa `Rettangle` e la classe si chiama `Rettangolo`, il compilatore risponde `cannot find symbol` e tutto l'esercizio non si compila. Nomi di classi, di metodi e di campi vanno copiati dalla traccia carattere per carattere, accenti e maiuscole compresi.

## Riassunto

Una **classe** è un modello che raggruppa i **dati** (campi, o variabili d'istanza) e le **operazioni** (metodi) di un tipo di entità; un **oggetto** è una sua istanza, con la propria copia dei dati. Gli oggetti si creano con `new` e si usano con l'operatore punto. I campi non inizializzati ricevono un valore predefinito (`0`, `false`, `null`), a differenza delle variabili locali. Dentro un metodo d'istanza `this` indica l'oggetto su cui il metodo è stato chiamato, ed è indispensabile quando un parametro ha lo stesso nome di un campo. Il **costruttore** ha il nome della classe e nessun tipo di ritorno, si esegue a ogni `new` e inizializza l'oggetto; una classe può averne più d'uno (overloading), e uno può richiamare l'altro con `this(...)` come prima istruzione; se non se ne scrive nessuno il compilatore ne aggiunge uno senza parametri, che sparisce appena se ne scrive uno. L'**information hiding** si realizza con i campi `private` e i metodi `public` che formano l'interfaccia: accessor (`getX`) e mutator (`setX`, con il controllo dei valori), mentre i metodi ausiliari restano privati; restituire o memorizzare un riferimento a un oggetto mutabile fa perdere la riservatezza, e si evita con la copia difensiva. I membri `static` appartengono alla classe (contatori, costanti); `final` impedisce la riassegnazione. Un `enum` è una classe con un numero fisso di oggetti, che può avere campi, un costruttore (privato) e metodi. I **package** raggruppano le classi in cartelle, risolvono i conflitti di nome e si usano con `import`; il livello di accesso senza modificatore e `protected` completano i quattro livelli. All'esame le classi stanno in un solo file, e la traccia va tradotta alla lettera.

**Concetti chiave**

- **Classe e oggetto.** La classe è il modello, l'oggetto la singola istanza; ogni oggetto ha la sua copia dei campi, i metodi sono scritti una volta sola.
- **Campo e metodo d'istanza.** Un campo è una variabile della classe fuori dai metodi; un metodo d'istanza lavora sui campi dell'oggetto su cui è chiamato.
- **`new` e operatore punto.** `new Classe(argomenti)` crea l'oggetto; `oggetto.membro` accede a campi e metodi.
- **Valori predefiniti.** `0`, `0.0`, `false`, carattere 0, `null`; valgono per i campi, non per le variabili locali.
- **`this`.** L'oggetto corrente; `this.campo = parametro;` risolve l'ombreggiamento.
- **Costruttore.** Stesso nome della classe, nessun tipo di ritorno, eseguito da `new`; con `void` diventa un metodo.
- **Costruttore di default.** Esiste solo se non si scrive nessun costruttore.
- **Overloading dei costruttori.** Firme diverse per numero, tipo e ordine dei parametri; `this(...)` richiama un altro costruttore della stessa classe, come prima istruzione.
- **Information hiding.** Campi `private`, metodi `public`; l'interfaccia dice che cosa si può fare, l'implementazione come.
- **Accessor e mutator.** `getNome` / `setNome`, con il tipo del campo; il mutator controlla i valori e il costruttore dovrebbe passare da lui.
- **Metodi ausiliari.** I metodi di servizio si dichiarano `private`.
- **Livelli di accesso.** `private`, nessun modificatore (package), `protected`, `public`.
- **Privacy leak.** Un campo privato che contiene un oggetto mutabile può essere modificato da fuori se il suo riferimento esce dalla classe; si cura con la copia.
- **`static` e `final`.** Variabile di classe condivisa; contatore di istanze; costante di classe `static final`; campo `final` assegnato una volta sola.
- **`enum` come classe.** Un numero fisso di oggetti, elencati per primi, con campi e costruttore privato; le costanti si confrontano con `==`.
- **Package e `import`.** Una cartella di classi; `package` come prima riga, `import` dopo; il nome completo risolve i conflitti.
- **Collaudo.** Un `main` che chiama i metodi e confronta atteso e ottenuto, ripetuto dopo ogni modifica.
- **Dalla traccia al codice.** Nomi, ordine dei parametri, `private` su ogni campo, `get` e `set` regolari, formati di output: tutto alla lettera.

**Sintassi essenziale**

| Elemento | Forma |
|---|---|
| Classe | `class Nome { campi, costruttori, metodi }` (senza `public` se non contiene il `main`) |
| Campo | `private Tipo nome;` |
| Costruttore | `public Nome(Tipo p1, Tipo p2) { this.p1 = p1; ... }` (nessun tipo di ritorno) |
| Costruttore che ne richiama un altro | `this(arg1, arg2);` (prima istruzione) |
| Creazione di un oggetto | `Nome x = new Nome(arg1, arg2);` |
| Accesso a un membro | `x.campo`, `x.metodo(args)`; `Nome.membroStatico` |
| Accessor e mutator | `public Tipo getNome() { return nome; }` / `public void setNome(Tipo nome) { this.nome = nome; }` |
| Variabile di classe, costante | `private static int n = 0;` / `public static final double MAX = 1.0;` |
| Campo assegnato una volta | `private final Tipo nome;` (nel costruttore) |
| Enum con campo | `enum E { A(1), B(2); private final int v; E(int v) { this.v = v; } }` |
| Package e import | `package nome;` (prima riga) / `import nome.Classe;` |

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `Enum` (ogni `enum`) | `values` | `static E[] values()` (generato dal compilatore) | — |
| `Enum` (ogni `enum`) | `name` | `String name()` | — |
| `Enum` (ogni `enum`) | `ordinal` | `int ordinal()` | — |
| `Object` | `toString` | `String toString()` (predefinito: nome della classe, `@`, hash esadecimale) | — |
