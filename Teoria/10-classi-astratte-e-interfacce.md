---
materia: Programmazione a Oggetti
capitolo: 10
titolo: Classi astratte e interfacce
livello_syllabus: 3
stato: completo
slide: ["Savitch cap. 11 slide 8-29", "Multithreading p. 10", "Lect2 (parole chiave)"]
appelli: [EXAM1, EXAM3]
fonti_esterne: 3
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 10 — Classi astratte e interfacce

## Di cosa parla questo capitolo

Nel [Capitolo 9 — Ereditarietà e polimorfismo](09-ereditarieta-e-polimorfismo.md) abbiamo visto che una classe base può essere riscritta dalle sue sottoclassi, e che una variabile della classe base può indicare un oggetto di una sottoclasse. Resta però un problema che il capitolo precedente ha solo sfiorato. Alcune classi base esistono **soltanto per essere estese**: descrivono che cosa devono saper fare le sottoclassi, ma non hanno nessun modo sensato di farlo loro. Una classe `Tariffa` sa che ogni tariffa deve calcolare un costo, ma *come* lo calcola dipende dalla tariffa concreta. Che cosa si scrive nel corpo del metodo `costo` della classe base? Qualunque valore di riserva è una bugia, e nulla obbliga una sottoclasse distratta a riscriverlo.

Java risolve il problema in due modi, che sono il tema del capitolo. Le **classi astratte** (*abstract classes*) sono classi incomplete: dichiarano metodi senza corpo e obbligano le sottoclassi a scriverli. Le **interfacce** (*interfaces*) vanno oltre: sono un puro **contratto**, un elenco di intestazioni di metodi che una classe si impegna a realizzare, e permettono a classi che non hanno nessun rapporto di parentela di essere usate in modo uniforme. Dell'interfaccia vedremo poi un caso particolarmente importante, `Comparable`, che serve a dire a Java come si ordinano gli oggetti di una classe, e ne citeremo un altro, `Runnable`, che ritroveremo nel capitolo sui thread.

Alla fine saprai dichiarare una classe astratta e un'interfaccia, scrivere le classi che le realizzano con la sintassi e i modificatori che il compilatore richiede, usare un oggetto attraverso il tipo della classe astratta o dell'interfaccia, scrivere `compareTo` per ordinare un array di oggetti con `Arrays.sort`, e spiegare a voce la differenza tra classe astratta e interfaccia e quando si sceglie l'una o l'altra.

> [!IMPORTANT]
> **Nota per l'esame — Qui si perde per un dettaglio di forma**
> Le tracce che usano questi concetti sono brevi: "una classe astratta `X` con un metodo astratto `String m()`", "un'interfaccia `Y` che dichiara il metodo `area`". Il resto va dedotto, ed è lì che si consumano le esecuzioni: un metodo che realizza l'interfaccia scritto senza `public`, un metodo che deve **restituire** una stringa e la **stampa**, una classe dichiarata astratta quando la traccia chiedeva un'interfaccia. Vedi "Come esce all'esame" e gli scheletri.

## 10.1 Classi astratte

### 10.1.1 Il problema: una classe base che non sa come fare

Supponiamo di dover calcolare il costo di una telefonata o di una sosta secondo diverse **tariffe**: una tariffa fissa, che costa sempre lo stesso importo, e una tariffa a minuti, che costa un prezzo per ciascun minuto. Il modo naturale di organizzare le classi è quello del capitolo precedente: una classe base `Tariffa` con un metodo `costo(int minuti)`, e due sottoclassi che lo riscrivono. Ma che cosa scriviamo nella classe base?

```java
class Tariffa {
    public double costo(int minuti) {
        return 0;                                  // "valore di riserva": ha senso?
    }
}

class TariffaFissa extends Tariffa {
    private double importo;

    public TariffaFissa(double importo) {
        this.importo = importo;
    }

    public double costo(int minuti) {
        return importo;
    }
}

class TariffaAMinuto extends Tariffa {
    private double prezzoMinuto;

    public TariffaAMinuto(double prezzoMinuto) {
        this.prezzoMinuto = prezzoMinuto;
    }

    public double Costo(int minuti) {              // refuso: la C è maiuscola
        return prezzoMinuto * minuti;
    }
}

public class ProvaRiserva {
    public static void main(String[] args) {
        Tariffa a = new TariffaFissa(5.0);
        Tariffa b = new TariffaAMinuto(0.25);
        Tariffa c = new Tariffa();                 // e questa che tariffa sarebbe?

        System.out.println(a.costo(30));
        System.out.println(b.costo(30));           // dovrebbe essere 7.5
        System.out.println(c.costo(30));
    }
}
```

```text
5.0
0.0
0.0
```

Il programma compila e gira senza una sola protesta, e produce un risultato sbagliato. `TariffaAMinuto` contiene un refuso: il metodo si chiama `Costo`, non `costo`, quindi non riscrive niente (è un metodo nuovo, come spiegato nella sezione 9.4.2). Per la variabile `b` parte allora la versione della classe base, che restituisce `0`, e nessuno ce lo segnala. Inoltre la riga `new Tariffa()` è legale: esiste un oggetto "tariffa generica" che costa zero, cioè una cosa che nel nostro problema non ha senso.

I difetti sono due, e hanno la stessa radice. La classe base **non può** scrivere un corpo sensato per `costo`, ma il linguaggio la costringe a scriverne uno; e nulla impone alle sottoclassi di riscriverlo. Quello che vorremmo dire è: "ogni tariffa *deve* poter calcolare un costo, ma io, classe base, non so come: lo dichiaro e basta, e tocca alle sottoclassi".

### 10.1.2 `abstract`: classe e metodi astratti

La parola chiave è **`abstract`**. Si scrive davanti al metodo, che perde il corpo e termina con un punto e virgola, e anche davanti alla classe che lo contiene.

```java
abstract class Tariffa {
    public abstract double costo(int minuti);      // niente corpo: finisce con ;
}
```

> [!NOTE]
> **Definizione — Metodo astratto, classe astratta**
> Un **metodo astratto** (*abstract method*) è un metodo dichiarato con la parola chiave `abstract`, con la sola intestazione e **nessun corpo**: al posto delle parentesi graffe c'è un punto e virgola. Una **classe astratta** (*abstract class*) è una classe dichiarata con `abstract`. Una classe che contiene almeno un metodo astratto **deve** essere dichiarata astratta. Di una classe astratta **non si possono creare oggetti** con `new`; si può soltanto estenderla.

Le sottoclassi hanno ora un obbligo preciso: ogni sottoclasse che si vuole **concreta**, cioè istanziabile, deve riscrivere tutti i metodi astratti che eredita, con la stessa firma. Se non lo fa, il compilatore lo rifiuta. Riscriviamo l'esempio.

```java
abstract class Tariffa {
    public abstract double costo(int minuti);
}

class TariffaFissa extends Tariffa {
    private double importo;

    public TariffaFissa(double importo) {
        this.importo = importo;
    }

    @Override
    public double costo(int minuti) {
        return importo;
    }
}

class TariffaAMinuto extends Tariffa {
    private double prezzoMinuto;

    public TariffaAMinuto(double prezzoMinuto) {
        this.prezzoMinuto = prezzoMinuto;
    }

    @Override
    public double costo(int minuti) {
        return prezzoMinuto * minuti;
    }
}

public class ProvaAstratta {
    public static void main(String[] args) {
        Tariffa[] tariffe = new Tariffa[2];
        tariffe[0] = new TariffaFissa(5.0);
        tariffe[1] = new TariffaAMinuto(0.25);

        for (int i = 0; i < tariffe.length; i++) {
            System.out.println("30 minuti: " + tariffe[i].costo(30));
        }
    }
}
```

```text
30 minuti: 5.0
30 minuti: 7.5
```

Riga per riga. `abstract class Tariffa` dichiara la classe astratta; il suo unico membro è `public abstract double costo(int minuti);`, un'intestazione senza corpo che dice "chi mi estende deve fornire un metodo con questo nome, questo parametro e questo tipo di ritorno". `TariffaFissa` e `TariffaAMinuto` estendono `Tariffa` e ciascuna fornisce il proprio corpo; l'annotazione `@Override` (sezione 9.4.2) fa verificare al compilatore che stiamo davvero realizzando un metodo della superclasse. Nel `main`, l'array è dichiarato del tipo della classe astratta: `Tariffa[] tariffe` è un contenitore di riferimenti a `Tariffa`, e può contenere oggetti di qualunque sua sottoclasse concreta (è l'array polimorfico del Capitolo 9, sezione 9.6). Quando il ciclo chiama `tariffe[i].costo(30)`, la JVM esegue la versione della classe dell'oggetto, grazie al binding dinamico.

Che cosa è cambiato rispetto a prima? Se riscriviamo il refuso del paragrafo precedente con la classe astratta, il compilatore ci ferma:

> [!WARNING]
> **Attenzione — Il refuso adesso non passa inosservato**
> ```java
> class TariffaAMinuto extends Tariffa {
>     public double Costo(int minuti) {          // ERRORE: C maiuscola, non realizza costo
>         return 0.25 * minuti;
>     }
> }
> ```
> Il compilatore risponde `TariffaAMinuto is not abstract and does not override abstract method costo(int) in Tariffa`. Con la classe astratta, un metodo "dimenticato" o sbagliato di nome diventa un **errore di compilazione** e non un risultato errato a runtime. Se in più si scrive `@Override` sul metodo con il refuso, il compilatore aggiunge `method does not override or implement a method from a supertype`.

E la riga `new Tariffa()`? Non si compila più:

```java
Tariffa t = new Tariffa();                         // ERRORE: la classe è astratta
```

Il messaggio è `Tariffa is abstract; cannot be instantiated`. La classe astratta serve a fare da base; l'oggetto "tariffa generica" non può più esistere.

### 10.1.3 Le regole

Ricapitoliamo in un unico quadro tutto ciò che il compilatore controlla. Ogni regola è stata verificata con il compilatore, e il messaggio riportato è quello che compare.

**Non si istanziano.** `new` su una classe astratta è un errore (`... is abstract; cannot be instantiated`). Ma una classe astratta è un **tipo** a tutti gli effetti: si può usare per una variabile, per un parametro di metodo o per il tipo di un array, e queste variabili possono indicare oggetti di qualunque sottoclasse concreta. È esattamente quanto fa `Tariffa[] tariffe` nell'esempio.

**Un metodo astratto non ha corpo.** Se si mettono le graffe si ottiene `abstract methods cannot have a body`. All'inverso, un metodo normale a cui si dimentica il corpo dà `missing method body, or declare abstract`.

**Un metodo astratto sta in una classe astratta.** Se si dimentica `abstract` davanti alla classe, il compilatore risponde con lo stesso messaggio che si ottiene da una sottoclasse incompleta: `Tariffa is not abstract and does not override abstract method costo(int) in Tariffa`.

**Chi estende deve completare, oppure restare astratto.** Una sottoclasse concreta deve realizzare **tutti** i metodi astratti che eredita. Se ne realizza solo alcuni, deve essere a sua volta dichiarata astratta, e il compito passa alle sue sottoclassi. Un esempio con due metodi astratti:

```java
abstract class Documento {
    public abstract String titolo();
    public abstract int pagine();
}

abstract class Racconto extends Documento {         // realizza solo titolo: resta astratta
    public String titolo() {
        return "Senza titolo";
    }
}

class Romanzo extends Racconto {                    // concreta: realizza ciò che manca
    public int pagine() {
        return 320;
    }
}

public class ProvaCatena {
    public static void main(String[] args) {
        Documento d = new Romanzo();
        System.out.println(d.titolo() + ", " + d.pagine() + " pagine");
    }
}
```

```text
Senza titolo, 320 pagine
```

`Racconto` realizza `titolo` ma non `pagine`: se non fosse dichiarata `abstract`, il compilatore direbbe `Racconto is not abstract and does not override abstract method pagine() in Documento`. Per `Romanzo`, che è concreta, i due metodi sono entrambi realizzati: `titolo` ereditato da `Racconto`, `pagine` scritto in `Romanzo`. L'oggetto `new Romanzo()` si può assegnare a una variabile `Documento` e il binding dinamico trova il metodo giusto.

**`abstract` non si combina con `private`, `static` e `final`.** Un metodo astratto deve poter essere riscritto da una sottoclasse, cosa che `private` (non visibile), `static` (appartiene alla classe, non all'oggetto) e `final` (non riscrivibile) escludono. Il compilatore risponde `illegal combination of modifiers: abstract and private` (e così per `static` e `final`). Lo stesso vale per una **classe** `final abstract`: una classe `final` non può essere estesa, una astratta esiste solo per essere estesa.

**Una classe astratta può non avere metodi astratti.** `abstract` sulla classe è lecito anche in assenza di metodi astratti: serve a impedire che si creino oggetti di quella classe. La direzione opposta, invece, non vale: un metodo astratto richiede la classe astratta.

### 10.1.4 Una classe astratta è una classe vera

La classe astratta non è un'"interfaccia travestita". Ha tutto quello che ha una classe normale: campi, costruttori, metodi completi. Ciò che non ha è la possibilità di essere istanziata direttamente. Questo la rende preziosa: tutto ciò che è comune a **tutte** le sottoclassi si scrive una volta nella classe astratta, e solo ciò che differisce resta astratto. Completiamo `Tariffa` con un nome, un costruttore, un getter e un metodo completo `riepilogo`:

```java
abstract class Tariffa {
    private String nome;

    public Tariffa(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }

    public abstract double costo(int minuti);        // l'unica parte che differisce

    public String riepilogo(int minuti) {            // metodo completo, comune a tutte
        return nome + ": " + minuti + " minuti = " + costo(minuti);
    }
}

class TariffaFissa extends Tariffa {
    private double importo;

    public TariffaFissa(String nome, double importo) {
        super(nome);                                  // costruisce la parte Tariffa
        this.importo = importo;
    }

    @Override
    public double costo(int minuti) {
        return importo;
    }
}

class TariffaAMinuto extends Tariffa {
    private double prezzoMinuto;

    public TariffaAMinuto(String nome, double prezzoMinuto) {
        super(nome);
        this.prezzoMinuto = prezzoMinuto;
    }

    @Override
    public double costo(int minuti) {
        return prezzoMinuto * minuti;
    }
}

public class ProvaRiepilogo {
    public static void mostra(Tariffa t) {            // un parametro di tipo classe astratta
        System.out.println(t.riepilogo(30));
    }

    public static void main(String[] args) {
        Tariffa[] tariffe = {
            new TariffaFissa("Giornaliera", 5.0),
            new TariffaAMinuto("Flessibile", 0.25)
        };

        for (int i = 0; i < tariffe.length; i++) {
            mostra(tariffe[i]);
        }
    }
}
```

```text
Giornaliera: 30 minuti = 5.0
Flessibile: 30 minuti = 7.5
```

Tre cose da osservare. Primo, **la classe astratta ha un costruttore**, anche se non si può chiamare con `new`: lo richiamano le sottoclassi con `super(nome)`, come per qualunque superclasse (sezione 9.3). Il costruttore serve a inizializzare i campi comuni, qui il `nome`, che resta `private` e si legge dalle sottoclassi con `getNome()` (sezione 9.2). Secondo, `riepilogo` è un metodo **completo**, scritto una sola volta, ereditato da entrambe le sottoclassi senza che nessuna lo riscriva. Terzo, `mostra(Tariffa t)` accetta come parametro una `Tariffa`, che è astratta: va benissimo, perché a runtime il parametro sarà sempre un oggetto di una sottoclasse concreta.

### 10.1.5 Il metodo completo che chiama quello astratto

Guardiamo ancora il metodo `riepilogo`. Dentro il suo corpo c'è la chiamata `costo(minuti)`, che è una forma abbreviata di `this.costo(minuti)`, e il metodo `costo` nella classe `Tariffa` **non ha corpo**: come può `riepilogo` chiamarlo? Ricordiamo il meccanismo del Capitolo 9, sezione 9.6.3. Quando scriviamo `tariffe[1].riepilogo(30)`, la JVM trova `riepilogo` in `Tariffa` e lo esegue con `this` uguale all'oggetto `TariffaAMinuto`. All'interno, `this.costo(minuti)` viene risolto al momento dell'esecuzione sulla classe vera dell'oggetto, cioè `TariffaAMinuto`, e parte la sua versione di `costo`. Una versione di `costo` nella classe `Tariffa` non è mai richiesta, perché il compilatore ha già garantito che ogni oggetto che può arrivare lì ne ha una: non esistono oggetti di una classe astratta, e ogni sottoclasse concreta ha realizzato tutti i metodi astratti.

Questo schema ha un nome nella pratica dei programmatori: un metodo scritto una volta nella classe astratta stabilisce i **passi** di un'operazione e lascia alle sottoclassi i **dettagli** di alcuni passi. È il caso di studio delle forme geometriche con cui il docente introduce l'argomento: un metodo della classe base, `drawAt`, sposta il cursore e poi richiama `drawHere`, che è il metodo che ciascuna forma (rettangolo, triangolo) riscrive per disegnarsi; la classe base dichiara `drawHere` come astratto, perché non può sapere come disegnare una forma generica. Il metodo `drawAt` viene scritto una sola volta e funziona anche per forme che verranno scritte in futuro.

> [!TIP]
> **Intuizione — Il modulo con i campi da riempire**
> Una classe astratta somiglia a un modulo prestampato: la parte stampata (i passi comuni, i campi, i metodi completi) è già scritta, e restano dei riquadri vuoti (i metodi astratti) che chi usa il modulo deve compilare. Nessuno può "consegnare" il modulo vuoto: è per questo che la classe astratta non si istanzia. L'analogia ha un limite: un modulo si compila una volta sola, mentre ogni sottoclasse compila gli stessi riquadri a modo suo, e il programma sceglie al volo quale compilazione usare.

## 10.2 Interfacce

### 10.2.1 Il problema: la stessa abilità in classi che non si somigliano

La classe astratta è un'ottima soluzione quando le classi **sono parenti**: una tariffa fissa e una a minuti sono due tipi di tariffa. Ma consideriamo un altro problema. Vogliamo un metodo che, data una collezione di oggetti, calcoli l'area totale. Gli oggetti sono rettangoli e cerchi. Un rettangolo e un cerchio hanno qualcosa in comune, la capacità di dire la propria area, ma potrebbero stare in gerarchie completamente diverse: magari il rettangolo estende una classe `Finestra` e il cerchio una classe `Pulsante`. E in Java una classe ha **una sola superclasse** (sezione 9.1.5): non possiamo far estendere a tutte e due una classe `Misurabile`.

Il modo di dire "queste classi, qualunque sia la loro parentela, sanno fare questa cosa" è l'**interfaccia**. Il docente la introduce partendo da un insieme di comportamenti: un animale domestico deve avere un nome, saper mangiare, rispondere a un comando. Se elenchiamo le intestazioni dei metodi che realizzano questi comportamenti, otteniamo l'**interfaccia della classe** (*class interface*): ciò che si può chiedere a un oggetto. Classi diverse realizzano gli stessi comportamenti **in modo diverso**, ma tutte rispondono alla stessa interfaccia. Quando questo elenco di intestazioni viene scritto in Java con la parola chiave `interface`, diventa un **tipo** che le classi possono impegnarsi a realizzare.

> [!TIP]
> **Intuizione — La patente**
> Un'interfaccia è come la patente di guida. L'esaminatore non si chiede chi sia il candidato, quanti anni abbia o dove sia nato: gli chiede di saper fare un insieme preciso di cose (partire, fermarsi, sterzare, parcheggiare). Chiunque abbia la patente B può guidare un'auto, e un'agenzia di noleggio può affidare un'auto a chiunque sia in possesso della patente senza sapere altro. Allo stesso modo, un metodo che riceve un `Misurabile` non sa e non vuole sapere se è un rettangolo o un cerchio: sa che ha un'area. L'analogia ha un limite: la patente si prende con un esame, mentre un'interfaccia si "ottiene" scrivendo i metodi richiesti e dichiarandolo con `implements`.

### 10.2.2 Dichiarare un'interfaccia

L'interfaccia si dichiara con la parola chiave **`interface`**, al posto di `class`. Dentro mette le **intestazioni** dei metodi, ciascuna terminata da un punto e virgola, senza corpo.

```java
interface Misurabile {
    double perimetro();
    double area();
}
```

> [!NOTE]
> **Definizione — Interfaccia**
> Un'**interfaccia** (*interface*) è un componente del programma che contiene le intestazioni di un certo numero di **metodi pubblici**, e può contenere anche **costanti** con nome. Non contiene costruttori, né variabili d'istanza, né corpi di metodi. L'interfaccia è un **tipo riferimento**: si può usare come tipo di una variabile o di un parametro. Si salva in un file `.java` e il suo nome comincia, per convenzione, con la maiuscola, come quello di una classe.

Le regole, tutte verificate con il compilatore:

- **I metodi sono implicitamente `public` e `abstract`.** Non serve scrivere né l'una né l'altra parola: `double area();` equivale a `public abstract double area();`. Scrivere entrambe è lecito ma ridondante. Questa seconda regola, `public` implicito, ha una conseguenza pratica importante nella sezione 10.2.3.
- **Nessun corpo.** Un metodo con le graffe è rifiutato (`interface abstract methods cannot have body`).
- **Nessun costruttore.** Un'intestazione `Misurabile();` produce `<identifier> expected`: l'interfaccia non crea oggetti, quindi non ha niente da costruire.
- **Nessuna variabile d'istanza.** Una dichiarazione `int n;` è rifiutata (`= expected`, perché in un'interfaccia una variabile è una **costante** e quindi richiede il valore: ne parliamo nella sezione 10.2.5).
- **Non si istanzia.** `new Misurabile()` dà `Misurabile is abstract; cannot be instantiated`.

> [!IMPORTANT]
> **Nota del docente — Interfaccia e file unico**
> L'interfaccia, come la classe, vive in un file `.java`. All'esame tutte le classi di un esercizio stanno **in un unico file**, e una sola è `public`, quella con il `main`. Un'interfaccia nello stesso file si dichiara quindi **senza** `public`: scrivere `public interface Misurabile` in un file che non si chiama `Misurabile.java` dà `interface Misurabile is public, should be declared in a file named Misurabile.java`. Vale la stessa regola delle classi (Capitolo 1, "Errori tipici").

### 10.2.3 Realizzare un'interfaccia: `implements`

Una classe che vuole rispettare il contratto lo dichiara con la parola chiave **`implements`** ("realizza", "implementa") nella riga di definizione, seguita dal nome dell'interfaccia, e **definisce il corpo di ogni metodo** dell'interfaccia.

```java
interface Misurabile {
    double perimetro();
    double area();
}

class Rettangolo implements Misurabile {
    private double base;
    private double altezza;

    public Rettangolo(double base, double altezza) {
        this.base = base;
        this.altezza = altezza;
    }

    public double perimetro() {
        return 2 * (base + altezza);
    }

    public double area() {
        return base * altezza;
    }
}

class Cerchio implements Misurabile {
    private double raggio;

    public Cerchio(double raggio) {
        this.raggio = raggio;
    }

    public double perimetro() {
        return 2 * Math.PI * raggio;
    }

    public double area() {
        return Math.PI * raggio * raggio;
    }
}

public class ProvaRealizzazione {
    public static void main(String[] args) {
        Rettangolo r = new Rettangolo(3.0, 4.0);
        Cerchio c = new Cerchio(1.0);

        System.out.println("rettangolo: perimetro " + r.perimetro() + ", area " + r.area());
        System.out.println("cerchio: perimetro " + c.perimetro() + ", area " + c.area());
    }
}
```

```text
rettangolo: perimetro 14.0, area 12.0
cerchio: perimetro 6.283185307179586, area 3.141592653589793
```

`Rettangolo` e `Cerchio` non hanno niente in comune se non la riga `implements Misurabile`. Ciascuna ha i propri campi privati, il proprio costruttore, e i propri corpi per `perimetro` e `area`. Il costruttore, come sempre, riceve i parametri nell'ordine che la traccia stabilisce; i campi sono privati, come richiede l'incapsulamento (Capitolo 7). `Math.PI` è la costante `double` della libreria (Capitolo 6, sezione 6.5).

Il punto che fa perdere più tempo è il modificatore `public`. I metodi dell'interfaccia sono pubblici anche se non lo si scrive, e **chi li realizza non può renderli meno accessibili**: è la regola dell'overriding (sezione 9.4.5), applicata qui perché il metodo realizzato è la riscrittura di un metodo pubblico. Se nella classe si scrive `double area() { ... }` senza `public`, il metodo diventa visibile solo nel package (accesso predefinito) e il compilatore rifiuta:

> [!CAUTION]
> **Errore tipico — Realizzare un metodo di interfaccia senza `public`**
> ```java
> interface Pagabile {
>     double importo();
> }
>
> class Fattura implements Pagabile {
>     double importo() {                       // ERRORE: manca public
>         return 100.0;
>     }
> }
> ```
> Il compilatore risponde `importo() in Fattura cannot implement importo() in Pagabile` e, sulla riga successiva, `attempting to assign weaker access privileges; was public`. Il metodo dell'interfaccia è `public` anche se nell'interfaccia non lo si legge, e la sua realizzazione deve esserlo. Forma corretta: `public double importo()`. È tra gli errori più frequenti di chi scrive una classe che realizza un'interfaccia a mano, senza completamento automatico.

Altre due regole sulla riga `implements`:

- **Si realizzano tutti i metodi.** Una classe concreta che dichiara `implements Misurabile` senza scrivere uno dei due metodi viene rifiutata con `... is not abstract and does not override abstract method ... in Misurabile`. Come per le classi astratte, l'alternativa è dichiarare la classe `abstract` e lasciare il compito alle sue sottoclassi (sezione 10.3).
- **`implements` si usa con un'interfaccia, `extends` con una classe.** Scrivere `class D implements C` con `C` classe dà `interface expected here`; scrivere `class D extends I` con `I` interfaccia dà `no interface expected here`.

L'annotazione `@Override` si può scrivere anche sui metodi che realizzano un'interfaccia: il compilatore verifica che ci sia davvero un metodo corrispondente nell'interfaccia. All'esame, dove non c'è nessun controllo, è un modo in più per accorgersi di un refuso nel nome del metodo.

### 10.2.4 L'interfaccia come tipo

Il vantaggio dell'interfaccia sta nel suo essere un tipo. Un metodo può dichiarare un parametro di tipo `Misurabile`, e riceverà senza distinzione un rettangolo, un cerchio, o qualunque classe che realizzi il contratto, oggi o in futuro. Una variabile può avere il tipo `Misurabile` e riferirsi a un oggetto di una classe che lo realizza; un array può contenere `Misurabile`.

```java
interface Misurabile {
    double perimetro();
    double area();
}

class Rettangolo implements Misurabile {
    private double base;
    private double altezza;

    public Rettangolo(double base, double altezza) {
        this.base = base;
        this.altezza = altezza;
    }

    public double perimetro() { return 2 * (base + altezza); }
    public double area() { return base * altezza; }
}

class Cerchio implements Misurabile {
    private double raggio;

    public Cerchio(double raggio) {
        this.raggio = raggio;
    }

    public double perimetro() { return 2 * Math.PI * raggio; }
    public double area() { return Math.PI * raggio * raggio; }
}

public class ProvaInterfacciaTipo {
    public static void stampa(Misurabile m) {          // parametro di tipo interfaccia
        System.out.println("perimetro " + m.perimetro() + ", area " + m.area());
    }

    public static double areaTotale(Misurabile[] v) {  // array di tipo interfaccia
        double somma = 0;
        for (int i = 0; i < v.length; i++) {
            somma = somma + v[i].area();
        }
        return somma;
    }

    public static void main(String[] args) {
        Misurabile m = new Rettangolo(3.0, 4.0);       // variabile di tipo interfaccia
        stampa(m);

        m = new Cerchio(1.0);                          // la stessa variabile, un altro oggetto
        stampa(m);

        Misurabile[] forme = { new Rettangolo(3.0, 4.0), new Cerchio(1.0) };
        System.out.println("area totale " + areaTotale(forme));
    }
}
```

```text
perimetro 14.0, area 12.0
perimetro 6.283185307179586, area 3.141592653589793
area totale 15.141592653589793
```

Riga per riga. Le classi sono quelle di prima, con i metodi di una riga per brevità. `stampa(Misurabile m)` è scritta una sola volta e vale per qualunque oggetto che realizzi il contratto: nel corpo chiama `m.perimetro()` e `m.area()` senza sapere che cosa sia `m`. Nel `main`, la variabile `m` dichiarata `Misurabile` indica prima un `Rettangolo` e poi un `Cerchio`: l'assegnamento è lecito senza cast, come per la superclasse (sezione 9.5.1), perché ogni `Rettangolo` e ogni `Cerchio` *è un* `Misurabile`. L'array `forme` contiene riferimenti a `Misurabile`, e `areaTotale` li percorre chiamando `area()`.

Valgono le stesse due distinzioni del polimorfismo (sezione 9.6.4):

- **Il compilatore guarda il tipo dichiarato.** Attraverso una variabile `Misurabile` si possono chiamare soltanto i metodi dichiarati nell'interfaccia. Un metodo in più della classe, come `getBase()` in `Rettangolo`, non è visibile: il compilatore risponde `cannot find symbol` con `location: variable m of type Misurabile`.
- **La JVM guarda la classe dell'oggetto.** Quando `m.area()` viene eseguito, parte il metodo della classe vera dell'oggetto, `Rettangolo` o `Cerchio`: è il binding dinamico di sempre.

> [!NOTE]
> **Nota — Interfaccia e `new`**
> Un'interfaccia è un tipo, ma non è una classe da cui nascono oggetti. Una variabile `Misurabile` non può mai riferirsi a un "Misurabile generico": gli oggetti sono sempre di una classe concreta che realizza l'interfaccia. Scrivere `new Misurabile()` è un errore di compilazione.

### 10.2.5 Costanti nell'interfaccia

Un'interfaccia può contenere anche **costanti con nome**, cioè dichiarazioni di variabili con valore. Sono implicitamente `public`, `static` e `final`, anche se non si scrive niente: si leggono con il nome dell'interfaccia (`Soglie.MASSIMO`) e le classi che la realizzano le vedono con il nome semplice.

```java
interface Soglie {
    int MINIMO = 0;                                    // public static final, senza scriverlo
    int MASSIMO = 100;
}

class Sensore implements Soglie {
    public boolean valido(int lettura) {
        return lettura >= MINIMO && lettura <= MASSIMO;   // le costanti si vedono per nome
    }
}

public class ProvaCostanti {
    public static void main(String[] args) {
        Sensore s = new Sensore();

        System.out.println(s.valido(50));
        System.out.println(s.valido(150));
        System.out.println(Soglie.MASSIMO);             // con il nome dell'interfaccia
        System.out.println(Sensore.MASSIMO);            // oppure con quello di una classe che la realizza
    }
}
```

```text
true
false
100
100
```

Non si può riassegnare una costante: `Soglie.MASSIMO = 200;` dà `cannot assign a value to static final variable MASSIMO`. Nel Capitolo 7 (sezione 7.4.2) abbiamo visto che una costante di classe si scrive `static final`; qui il compilatore aggiunge le parole mancanti. Questa è l'unica forma di "dato" ammessa in un'interfaccia: le variabili d'istanza (lo stato di un oggetto) no.

### 10.2.6 Più interfacce, e `extends` insieme a `implements`

Una classe può avere una sola superclasse ma può realizzare **quante interfacce vuole**: si scrivono dopo `implements`, separate da virgole. La classe deve definire tutti i metodi di tutte le interfacce. È il modo in cui Java ottiene ciò che altri linguaggi ottengono con l'ereditarietà multipla, evitando il problema delle due superclassi con metodi contrastanti (sezione 9.1.5): un'interfaccia contiene solo intestazioni, e quindi due interfacce con la stessa intestazione non si contraddicono, la classe scrive il metodo una volta.

Se la classe ha anche una superclasse, nella riga di definizione l'ordine è fisso: **prima `extends`, poi `implements`**.

```java
interface Misurabile {
    double area();
}

interface Etichettabile {
    String etichetta();
}

class Materiale {
    private String colore;

    public Materiale(String colore) {
        this.colore = colore;
    }

    public String getColore() {
        return colore;
    }
}

class Piastrella extends Materiale implements Misurabile, Etichettabile {
    private double lato;

    public Piastrella(String colore, double lato) {
        super(colore);
        this.lato = lato;
    }

    public double area() {
        return lato * lato;
    }

    public String etichetta() {
        return "piastrella " + getColore();
    }
}

public class ProvaDueInterfacce {
    public static void main(String[] args) {
        Piastrella p = new Piastrella("blu", 0.5);

        Misurabile m = p;                               // la stessa piastrella, vista come Misurabile
        Etichettabile e = p;                            // e come Etichettabile
        Materiale base = p;                             // e come Materiale

        System.out.println(m.area());
        System.out.println(e.etichetta());
        System.out.println(base.getColore());
    }
}
```

```text
0.25
piastrella blu
blu
```

`Piastrella` ha **tre tipi** oltre al proprio: `Materiale` (la superclasse), `Misurabile` e `Etichettabile` (le interfacce). Un oggetto `Piastrella` può essere assegnato a una variabile di ciascuno di questi tipi. Ogni variabile, però, vede solo ciò che il suo tipo dichiara: `m` può chiamare `area()` ma non `etichetta()`. Se si inverte l'ordine delle clausole (`implements Misurabile extends Materiale`) il compilatore risponde `'{' expected`, come visto nel capitolo precedente.

### 10.2.7 Un'interfaccia che ne estende un'altra

Un'interfaccia può **estenderne** un'altra, con la parola `extends`: la nuova interfaccia contiene le intestazioni della prima più le proprie. Una classe che realizza la nuova deve definire **tutti** i metodi di entrambe.

```java
interface Descrivibile {
    String descrizione();
}

interface Prezzabile extends Descrivibile {         // eredita descrizione() e aggiunge prezzo()
    double prezzo();
}

class Quaderno implements Prezzabile {
    private String formato;
    private double costo;

    public Quaderno(String formato, double costo) {
        this.formato = formato;
        this.costo = costo;
    }

    public String descrizione() {                    // dall'interfaccia Descrivibile
        return "quaderno " + formato;
    }

    public double prezzo() {                         // dall'interfaccia Prezzabile
        return costo;
    }
}

public class ProvaEstensione {
    public static void main(String[] args) {
        Prezzabile p = new Quaderno("A4", 2.5);
        System.out.println(p.descrizione() + ": " + p.prezzo());

        Descrivibile d = p;                          // ogni Prezzabile è anche un Descrivibile
        System.out.println(d.descrizione());
    }
}
```

```text
quaderno A4: 2.5
quaderno A4
```

Una variabile di tipo `Prezzabile` può chiamare sia `prezzo()` sia `descrizione()`, che le arriva in eredità. Se `Quaderno` si dimenticasse di scrivere `descrizione`, il compilatore direbbe `Quaderno is not abstract and does not override abstract method descrizione() in Descrivibile`. Un'interfaccia può anche estendere più interfacce, separate da virgole (`interface C extends A, B`); anche in questo caso la regola è che chi realizza `C` realizza tutto.

## 10.3 Classe astratta o interfaccia?

Abbiamo ora due strumenti che sembrano fare lo stesso lavoro. Conviene metterli a confronto, perché le due strutture sono ciascuna la scelta giusta in un caso diverso, e la differenza è domanda d'esame orale.

| Aspetto | Classe astratta | Interfaccia |
|---|---|---|
| Parola chiave | `abstract class` | `interface` |
| Come la usa una classe | `extends` | `implements` |
| Quante se ne usano | **una sola** (ereditarietà singola) | **quante si vuole** |
| Metodi senza corpo | sì, quelli dichiarati `abstract` | tutti (sono implicitamente `abstract`) |
| Metodi con corpo | sì | no |
| Variabili d'istanza | sì | no |
| Costanti | sì | sì (implicitamente `public static final`) |
| Costruttori | sì, richiamati con `super(...)` | no |
| Si può istanziare con `new` | no | no |
| Si può usare come tipo | sì | sì |
| Relazione che esprime | "è un" (parentela tra classi) | "sa fare" (abilità, contratto) |

Come si sceglie? La domanda chiave è se le classi **condividono un'identità e del codice**.

- Si usa una **classe astratta** quando c'è una forte relazione "è un" tra le classi e queste hanno molto in comune: campi, costruttori, metodi completi. È il caso di `Tariffa`: la fissa e quella a minuti *sono* tariffe, hanno entrambe un nome, e `riepilogo` si scrive una volta sola per tutte.
- Si usa un'**interfaccia** quando si vuole stabilire un'**abilità** che classi anche completamente scollegate devono possedere, senza imporre una parentela e senza condividere codice. Rettangolo e cerchio non sono "dello stesso tipo", ma entrambi sanno calcolare l'area. Interfacce della libreria come `Runnable` e `Comparable` hanno esattamente questo ruolo.

La regola dell'ereditarietà singola dà all'interfaccia un ruolo in più: una classe che estende già una superclasse non ne può estendere un'altra, ma può sempre aggiungere interfacce. Per questo, come vedremo nel [Capitolo 17](17-thread.md), una classe che deve essere eseguita da un thread e che estende già qualcos'altro non può estendere `Thread`: realizza l'interfaccia `Runnable`.

I due strumenti si possono anche **combinare**. Una classe astratta può dichiarare `implements` di un'interfaccia senza scrivere tutti i metodi: quelli che non realizza restano astratti, e sono le sottoclassi concrete a doverli scrivere.

```java
interface Stampabile {
    String testo();
}

abstract class Documento implements Stampabile {     // non realizza testo(): resta astratta
    private String titolo;

    public Documento(String titolo) {
        this.titolo = titolo;
    }

    public void stampa() {                           // metodo completo che usa testo()
        System.out.println(titolo + " -> " + testo());
    }
}

class Lettera extends Documento {
    public Lettera(String titolo) {
        super(titolo);
    }

    public String testo() {                          // il compito lasciato alla sottoclasse
        return "Gentile cliente, la informiamo che";
    }
}

public class ProvaMista {
    public static void main(String[] args) {
        Documento d = new Lettera("Avviso");
        d.stampa();

        Stampabile s = d;                            // anche un Documento è uno Stampabile
        System.out.println(s.testo());
    }
}
```

```text
Avviso -> Gentile cliente, la informiamo che
Gentile cliente, la informiamo che
```

`Documento` porta con sé il titolo, il costruttore e il metodo `stampa` (la parte comune), mentre il contratto `testo()` arriva dall'interfaccia e resta da realizzare. Se `Lettera` non scrivesse `testo()`, il compilatore direbbe `Lettera is not abstract and does not override abstract method testo() in Stampabile`.

## 10.4 L'interfaccia `Comparable`: ordinare gli oggetti

### 10.4.1 Il problema: Java non sa come ordinare i nostri oggetti

Il Capitolo 5 ha mostrato `Arrays.sort`, che ordina un array di numeri o di stringhe. Possiamo usarlo anche su un array di oggetti nostri? Prendiamo una classe `Frutto` con il solo nome, e proviamo.

```java
import java.util.Arrays;

class Frutto {
    private String nome;

    public Frutto(String nome) {
        this.nome = nome;
    }

    public String toString() {
        return nome;
    }
}

public class ProvaSenzaOrdine {
    public static void main(String[] args) {
        Frutto[] frutti = { new Frutto("pera"), new Frutto("banana"), new Frutto("mela") };

        Arrays.sort(frutti);                           // compila... ma poi?
        System.out.println(Arrays.toString(frutti));
    }
}
```

Il programma compila, ma in esecuzione si ferma subito:

```text
Exception in thread "main" java.lang.ClassCastException: class Frutto cannot be cast to class java.lang.Comparable (Frutto is in unnamed module of loader 'app'; java.lang.Comparable is in module java.base of loader 'bootstrap')
	at java.base/java.util.ComparableTimSort.countRunAndMakeAscending(ComparableTimSort.java:320)
	...
```

La ragione è semplice: per ordinare, `Arrays.sort` deve confrontare coppie di elementi e decidere quale venga prima. Per i numeri e le stringhe lo sa fare, perché quelle classi hanno un ordine naturale. Per `Frutto` non può inventarlo: va ordinato per nome? per peso? per prezzo? Siamo noi a dover dire, nella classe, **come si confrontano due frutti**. `Arrays.sort` per farlo chiama un metodo `compareTo` sugli elementi e, non trovandolo (la classe `Frutto` non lo dichiara), la conversione a `Comparable` fallisce con `ClassCastException`.

### 10.4.2 L'interfaccia

La libreria Java definisce un'interfaccia apposta, `Comparable`, che impone un ordine agli oggetti delle classi che la realizzano. Richiede un solo metodo, `compareTo`, che confronta l'oggetto su cui è chiamato (`this`) con un altro oggetto.

> [!NOTE]
> **Approfondimento esterno — L'interfaccia `java.lang.Comparable`**
> `public interface Comparable<T>`: "This interface imposes a total ordering on the objects of each class that implements it. This ordering is referred to as the class's *natural ordering*, and the class's `compareTo` method is referred to as its *natural comparison method*." L'unico metodo ha la firma `int compareTo(T o)` e "returns a negative integer, zero, or a positive integer as this object is less than, equal to, or greater than the specified object". Lancia `NullPointerException` se l'oggetto passato è `null` e `ClassCastException` se il tipo di quell'oggetto impedisce il confronto. Chi realizza l'interfaccia deve garantire che `signum(x.compareTo(y)) == -signum(y.compareTo(x))` per ogni `x` e `y`. Si raccomanda (ma non è obbligatorio) che l'ordine naturale sia **coerente con `equals`**, cioè che `e1.compareTo(e2) == 0` valga esattamente quando `e1.equals(e2)`.
>
> *Fonte:* [java.lang.Comparable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Comparable.html)

La scrittura `Comparable<T>` merita un chiarimento. Le parentesi angolari contengono un **tipo** e dicono "confrontabile con oggetti di questo tipo": `Comparable<Frutto>` vuol dire "un `Frutto` si confronta con un altro `Frutto`" e `T` nella firma `compareTo(T o)` diventa `Frutto`. È la notazione dei *generics*, che vedremo a fondo nel [Capitolo 12](12-generics-e-collezioni.md); per usare `Comparable` basta saper scrivere `implements Comparable<NomeDellaClasse>` e un metodo `compareTo` che riceve un parametro del tipo della classe stessa. Esiste anche la forma più antica, senza parentesi angolari, in cui `compareTo` riceve un `Object`: la vediamo nella sezione 10.4.5.

### 10.4.3 Scrivere `compareTo`

Realizziamo `Comparable<Frutto>` ordinando i frutti per nome, in ordine alfabetico.

```java
import java.util.Arrays;

class Frutto implements Comparable<Frutto> {
    private String nome;

    public Frutto(String nome) {
        this.nome = nome;
    }

    @Override
    public int compareTo(Frutto altro) {              // public, parametro del tipo della classe
        return nome.compareTo(altro.nome);            // delego a String.compareTo (Capitolo 3, sezione 3.4.2)
    }

    @Override
    public String toString() {
        return nome;
    }
}

public class ProvaOrdinamento {
    public static void main(String[] args) {
        Frutto[] frutti = {
            new Frutto("pera"), new Frutto("banana"),
            new Frutto("arancia"), new Frutto("mela")
        };

        System.out.println("prima:  " + Arrays.toString(frutti));
        Arrays.sort(frutti);
        System.out.println("dopo:   " + Arrays.toString(frutti));

        System.out.println(frutti[0].compareTo(frutti[1]) < 0);   // arancia viene prima di banana
    }
}
```

```text
prima:  [pera, banana, arancia, mela]
dopo:   [arancia, banana, mela, pera]
true
```

Riga per riga. `implements Comparable<Frutto>` dichiara che i frutti hanno un ordine naturale. `compareTo(Frutto altro)` deve essere `public` (è la realizzazione di un metodo pubblico dell'interfaccia, sezione 10.2.3) e restituire un `int`. Nel corpo non c'è niente da inventare: i nomi sono stringhe, e le stringhe sanno già confrontarsi con `compareTo` (Capitolo 3, sezione 3.4.2); il metodo dei frutti si limita a **inoltrare** il confronto ai nomi. Nota che il campo `nome` di `altro` si legge direttamente (`altro.nome`) anche se è `private`, perché siamo dentro la classe `Frutto` (Capitolo 8, sezione 8.4.3). Il `main` mostra due usi: `Arrays.sort(frutti)` ora funziona e ordina l'array; e `frutti[0].compareTo(frutti[1]) < 0` dice che il primo elemento dell'array viene prima del secondo.

**Il contratto.** Il valore di ritorno ha un significato per il segno, non per il numero esatto:

- **negativo** se `this` viene *prima* dell'oggetto passato (è "minore");
- **zero** se i due sono uguali ai fini dell'ordinamento;
- **positivo** se `this` viene *dopo* (è "maggiore").

Di conseguenza, quando si usa il risultato di `compareTo` non lo si confronta mai con un numero preciso (`== 1`, `== -1`): si guarda il segno con `< 0`, `== 0`, `> 0`, come per `String.compareTo` (Capitolo 3, sezione 3.4.2). Il contratto chiede inoltre che il confronto sia **simmetrico**: se `x.compareTo(y)` è negativo, `y.compareTo(x)` deve essere positivo, e viceversa.

**Come si scrive il confronto.** Si confrontano i campi che definiscono l'ordine, nell'ordine in cui contano. Per ciascun tipo c'è il confronto giusto:

- una **stringa** si confronta con il suo `compareTo` (o `compareToIgnoreCase`, che ignora maiuscole e minuscole);
- un **`int`** si confronta con `Integer.compare(x, y)`, un **`double`** con `Double.compare(x, y)`.

> [!NOTE]
> **Approfondimento esterno — `Integer.compare` e `Double.compare`**
> `public static int compare(int x, int y)` (classe `Integer`) confronta numericamente due `int`: restituisce `0` se `x == y`, un valore minore di `0` se `x < y`, un valore maggiore di `0` se `x > y`. La classe `Double` ha il metodo analogo `public static int compare(double d1, double d2)`, con lo stesso significato per il segno del risultato. Entrambi sono metodi `static`, e non dichiarano eccezioni. Per le stringhe, `public int compareTo(String anotherString)` realizza proprio `Comparable<String>`, e `public int compareToIgnoreCase(String str)` fa lo stesso confronto ignorando le differenze tra maiuscole e minuscole.
>
> *Fonte:* [java.lang.Integer#compare](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Integer.html#compare(int,int)), [java.lang.Double#compare](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Double.html#compare(double,double))

Per ordinare in senso **decrescente** basta invertire i due operandi: `Integer.compare(altro.x, x)` al posto di `Integer.compare(x, altro.x)`. Per ordinare con **più criteri**, cioè con uno spareggio, si confronta il primo campo; se il risultato è diverso da zero lo si restituisce subito, altrimenti si passa al criterio successivo:

```java
import java.util.Arrays;

class Prodotto implements Comparable<Prodotto> {
    private String codice;
    private double prezzo;

    public Prodotto(String codice, double prezzo) {
        this.codice = codice;
        this.prezzo = prezzo;
    }

    @Override
    public int compareTo(Prodotto altro) {
        int confronto = Double.compare(prezzo, altro.prezzo);   // 1° criterio: prezzo crescente
        if (confronto != 0) {
            return confronto;                                   // i prezzi sono diversi: basta
        }
        return codice.compareTo(altro.codice);                  // spareggio: codice in ordine alfabetico
    }

    @Override
    public String toString() {
        return codice + " (" + prezzo + ")";
    }
}

public class ProvaSpareggio {
    public static void main(String[] args) {
        Prodotto[] v = {
            new Prodotto("P-30", 2.5), new Prodotto("P-10", 4.0),
            new Prodotto("P-20", 2.5), new Prodotto("P-40", 1.0)
        };

        Arrays.sort(v);
        for (int i = 0; i < v.length; i++) {
            System.out.println(v[i]);
        }
    }
}
```

```text
P-40 (1.0)
P-20 (2.5)
P-30 (2.5)
P-10 (4.0)
```

Il prodotto da 1.0 viene per primo; i due da 2.5 hanno `Double.compare` uguale a zero, quindi decide il codice (`P-20` prima di `P-30`); quello da 4.0 è ultimo. Per l'ordine **decrescente** di prezzo, mantenendo lo spareggio sul codice crescente, la prima riga diventerebbe `Double.compare(altro.prezzo, prezzo)`.

> [!CAUTION]
> **Errore tipico — Confrontare sottraendo**
> ```java
> public int compareTo(Prodotto altro) {
>     return quantita - altro.quantita;          // sembra comodo, ma può dare il segno sbagliato
> }
> ```
> Con numeri vicini ai limiti del tipo, la sottrazione **trabocca** (Capitolo 2, sezione 2.5): `Integer.MAX_VALUE - (-5)` vale `-2147483644`, un numero negativo, e l'ordinamento direbbe che il numero grande viene prima del piccolo. `Integer.compare(Integer.MAX_VALUE, -5)` restituisce invece `1`, come deve. Non esiste una ragione per preferire la sottrazione: la forma corretta, `Integer.compare(quantita, altro.quantita)`, è della stessa lunghezza.

C'è un secondo punto di attenzione: `compareTo(null)` deve lanciare `NullPointerException`, come richiede la documentazione. Non serve scrivere nulla: nel corpo di `compareTo` si accede subito a un campo dell'argomento (`altro.nome`), e se `altro` è `null` quell'accesso lancia da solo la `NullPointerException` (Capitolo 8, sezione 8.3.2).

### 10.4.4 Ordinare con `Arrays.sort`

Una volta che la classe realizza `Comparable`, tutto ciò che sa ordinare oggetti la usa senza altro lavoro. Il metodo che già conosciamo, `Arrays.sort(Object[] a)`, "ordina l'array in ordine crescente secondo l'ordinamento naturale dei suoi elementi" ed è **stabile**: a parità di confronto gli elementi mantengono l'ordine di partenza (dettagli nel Capitolo 5, sezione 5.6). Lancia `ClassCastException` se gli elementi non sono confrontabili tra loro, ed è l'errore che abbiamo visto nella sezione 10.4.1.

L'ordine naturale è **uno solo** per classe: è l'unico `compareTo` che la classe può avere. Se serve un secondo criterio (per esempio ordinare i frutti anche per lunghezza del nome) bisogna cambiare il corpo di `compareTo`, oppure usare un oggetto di confronto separato, il `Comparator`, che vediamo nel [Capitolo 12](12-generics-e-collezioni.md) insieme alle liste. Per dare un'idea, ecco la stessa classe con ordine per lunghezza del nome, mantenendo l'ordine originale a parità di lunghezza:

```java
import java.util.Arrays;

class Frutto implements Comparable<Frutto> {
    private String nome;

    public Frutto(String nome) {
        this.nome = nome;
    }

    @Override
    public int compareTo(Frutto altro) {
        return Integer.compare(nome.length(), altro.nome.length());   // per lunghezza del nome
    }

    @Override
    public String toString() {
        return nome;
    }
}

public class ProvaLunghezza {
    public static void main(String[] args) {
        Frutto[] frutti = {
            new Frutto("pera"), new Frutto("banana"), new Frutto("arancia"),
            new Frutto("mela"), new Frutto("kiwi")
        };

        Arrays.sort(frutti);
        System.out.println(Arrays.toString(frutti));
    }
}
```

```text
[pera, mela, kiwi, banana, arancia]
```

I frutti di quattro lettere (`pera`, `mela`, `kiwi`) vengono per primi, **nell'ordine in cui comparivano** nell'array (l'ordinamento è stabile); poi `banana` (sei lettere) e `arancia` (sette).

### 10.4.5 La forma con `Object`

Le slide del corso presentano `Comparable` nella sua forma più antica, quella senza parentesi angolari, in cui il metodo si chiama ancora `compareTo` ma riceve un `Object`: `public int compareTo(Object other)`. Dentro il metodo bisogna riportare l'argomento al tipo della classe con un cast (sezione 9.5.3) prima di leggerne i campi.

```java
import java.util.Arrays;

class Frutto implements Comparable {                 // senza <Frutto>
    private String nome;

    public Frutto(String nome) {
        this.nome = nome;
    }

    @Override
    public int compareTo(Object altro) {             // il parametro è un Object
        Frutto f = (Frutto) altro;                   // cast verso il basso
        return nome.compareTo(f.nome);
    }

    @Override
    public String toString() {
        return nome;
    }
}

public class ProvaFormaClassica {
    public static void main(String[] args) {
        Frutto[] frutti = { new Frutto("pera"), new Frutto("banana"), new Frutto("mela") };

        Arrays.sort(frutti);
        System.out.println(Arrays.toString(frutti));
    }
}
```

```text
[banana, mela, pera]
```

Le due forme sono **alternative**: si sceglie l'una o l'altra, mai tutte e due. Sono incompatibili nella firma: con `Comparable<Frutto>` il parametro è `Frutto`, con `Comparable` senza parentesi è `Object`. Se i due non coincidono, il compilatore lo dice con `Frutto is not abstract and does not override abstract method compareTo(...) in Comparable`, in cui il tipo tra parentesi (`Frutto` oppure `Object`) è quello che il compilatore si aspetta. La forma con `Object` ha un difetto che quella generica non ha: se si passa un oggetto di un'altra classe il cast fallisce **a runtime** con `ClassCastException`, mentre con `Comparable<Frutto>` il compilatore rifiuta il programma in fase di compilazione. Nelle tracce e nei programmi nuovi è preferibile la forma generica; la forma con `Object` serve a leggere il codice scritto con quella notazione.

## 10.5 `Runnable` e le altre interfacce della libreria

La libreria Java è piena di interfacce, e ormai sappiamo leggerle per quel che sono: un contratto che la nostra classe può firmare. Ne incontreremo diverse nei capitoli successivi: `Serializable`, che permette di scrivere un oggetto su un file (Capitolo 15); `Runnable`, che permette di far eseguire un oggetto da un thread (Capitolo 17). Di quest'ultima conviene vedere subito la forma, perché è l'altra interfaccia che compare nelle tracce d'esame.

> [!NOTE]
> **Approfondimento esterno — L'interfaccia `java.lang.Runnable`**
> `@FunctionalInterface public interface Runnable`: "The `Runnable` interface should be implemented by any class whose instances are intended to be executed by a thread. The class must define a method of no arguments called `run`." L'unico metodo ha la firma `void run()`. Un `Thread` si costruisce a partire da un `Runnable`: `public Thread(Runnable target)`, e il suo `run` è il metodo che viene eseguito all'avvio del thread.
>
> *Fonte:* [java.lang.Runnable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Runnable.html), [java.lang.Thread](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html)

```java
class Saluto implements Runnable {
    private String nome;

    public Saluto(String nome) {
        this.nome = nome;
    }

    @Override
    public void run() {                              // public: anche qui vale la regola dell'interfaccia
        System.out.println("Ciao da " + nome);
    }
}

public class ProvaRunnable {
    public static void main(String[] args) {
        Runnable r = new Saluto("Marta");            // l'interfaccia come tipo
        r.run();                                     // chiamata diretta: nessun thread qui
    }
}
```

```text
Ciao da Marta
```

Qui `run()` è chiamato direttamente, come un metodo qualsiasi: non parte nessun thread. L'esempio mostra solo il lato "interfaccia" di `Runnable`, cioè che per realizzarla basta un metodo `public void run()` e che una variabile `Runnable` può indicare qualunque oggetto di una classe che la realizza. Come si passa un `Runnable` a un `Thread` e cosa succede quando il thread parte è l'argomento del Capitolo 17. La tabella della sezione 10.3 spiega perché si sceglie `Runnable` e non `extends Thread` quando la classe ha già una superclasse: perché la superclasse è una sola, le interfacce no.

## Come esce all'esame

**EXAM1 — Esercizio 1 (5 punti), classi astratte e polimorfismo.** La traccia chiedeva di creare una classe **astratta** `Animale` con un metodo **astratto** `String verso()`, e due sottoclassi `Cane` e `Gatto` che lo realizzano restituendo rispettivamente `"bau"` e `"miao"`. Del capitolo servono: `abstract class Animale` e `public abstract String verso();` con il punto e virgola al posto del corpo (sezione 10.1.2); le sottoclassi con `extends Animale`, ciascuna con un metodo `public String verso()` che **restituisce** la stringa con `return`, senza stamparla (sezione 10.1.2 e Capitolo 9, sezioni 9.4.1 e 9.4.5); e, perché la traccia parla di "polimorfismo", l'uso degli oggetti attraverso una variabile `Animale` (sezione 10.1.2). Vincoli letterali: i nomi `Animale`, `Cane`, `Gatto`; il nome e la firma `String verso()`; le due stringhe esatte, in minuscolo; la parola `abstract` sulla classe e sul metodo.

**EXAM3 — Esercizio 1 (5 punti), OOP di base con interfacce.** La traccia chiedeva un'**interfaccia** `Figura` che dichiara il metodo `area`, il quale restituisce un numero con la virgola; una classe `Rettangolo` il cui costruttore riceve nell'ordine la base e l'altezza; una classe `Quadrato` il cui costruttore riceve la misura del lato; entrambe realizzano il contratto di `Figura`; tutte le variabili d'istanza `private`. L'output atteso mostrava l'area di `Rettangolo(3.0, 4.0)` (`12.0`) e di `Quadrato(3.0)` (`9.0`), e precisava che "gli oggetti devono poter essere raccolti e usati attraverso il tipo `Figura`". Del capitolo servono: `interface Figura { double area(); }` senza `public` sull'interfaccia (sezione 10.2.2); `implements Figura` nelle due classi (sezione 10.2.3); `public double area()` nelle due classi, perché la realizzazione di un metodo d'interfaccia deve essere pubblica (sezione 10.2.3); l'uso attraverso il tipo interfaccia, per esempio un array `Figura[]` o un parametro `Figura` (sezione 10.2.4). Del [Capitolo 7](07-classi-e-oggetti.md) servono i costruttori con i parametri nell'ordine richiesto e i campi privati. Vincoli letterali: i nomi `Figura`, `Rettangolo`, `Quadrato`, `area`; l'ordine base/altezza; `private` su tutti i campi; il formato dell'output.

**EXAM1 — Esercizio 3 (13 punti), ereditarietà, thread e information hiding.** La traccia chiedeva una sottoclasse `Studente` di una `Persona` già scritta, che "implementa l'interfaccia `Runnable`", con la riscrittura del metodo `run()`. Del capitolo servono la sezione 10.5 e la sezione 10.2.3: `run()` è la realizzazione di un metodo pubblico di un'interfaccia, quindi si scrive `public void run()`. Le altre parti della traccia (costruttori, `super(...)`, campi privati) sono nel [Capitolo 9](09-ereditarieta-e-polimorfismo.md) e nel Capitolo 7.

## Scheletri da esame

### Una classe astratta con un metodo astratto e due sottoclassi

*Quando si usa:* la traccia chiede una classe base "astratta" con un metodo che le sottoclassi realizzano ciascuna a modo proprio. Si veda la sezione 10.1.2.

```java
abstract class Strumento {
    public abstract String suono();                  // niente corpo, punto e virgola
}

class Tamburo extends Strumento {
    @Override
    public String suono() {                          // stessa firma, public, return (non println)
        return "bum";
    }
}

class Flauto extends Strumento {
    @Override
    public String suono() {
        return "fiu";
    }
}

public class ProvaStrumenti {
    public static void main(String[] args) {
        Strumento[] orchestra = { new Tamburo(), new Flauto() };   // tipo della classe astratta

        for (int i = 0; i < orchestra.length; i++) {
            System.out.println(orchestra[i].suono());
        }
    }
}
```

```text
bum
fiu
```

Non servono import né eccezioni. Punti da controllare: `abstract` **sia** sulla classe **sia** sul metodo; il metodo astratto finisce con `;`; ogni sottoclasse ha `extends` e il metodo `public` con **lo stesso** tipo di ritorno; il metodo **restituisce** il testo, non lo stampa.

### Un'interfaccia realizzata da due classi, usate attraverso il tipo interfaccia

*Quando si usa:* la traccia chiede un'interfaccia che dichiara un metodo e due classi che la realizzano, con costruttori che ricevono i parametri in un ordine dato. Si vedano le sezioni 10.2.2-10.2.4.

```java
interface Pagabile {                                 // senza public: file unico
    double importo();
}

class Fattura implements Pagabile {
    private double imponibile;
    private double maggiorazione;

    public Fattura(double imponibile, double maggiorazione) {   // ordine come da traccia
        this.imponibile = imponibile;
        this.maggiorazione = maggiorazione;
    }

    @Override
    public double importo() {                        // public: realizza un metodo d'interfaccia
        return imponibile + imponibile * maggiorazione;
    }
}

class Scontrino implements Pagabile {
    private double totale;

    public Scontrino(double totale) {
        this.totale = totale;
    }

    @Override
    public double importo() {
        return totale;
    }
}

public class ProvaPagabili {
    public static void main(String[] args) {
        Pagabile[] v = { new Fattura(100.0, 0.25), new Scontrino(15.5) };

        System.out.println("importo di Fattura(100.0, 0.25)  ->  " + v[0].importo());
        System.out.println("importo di Scontrino(15.5)       ->  " + v[1].importo());
    }
}
```

```text
importo di Fattura(100.0, 0.25)  ->  125.0
importo di Scontrino(15.5)       ->  15.5
```

Non servono import né eccezioni. Punti da controllare: `interface` senza `public` e senza corpi; `implements` nelle due classi; `public` su ogni metodo che realizza il contratto; campi `private`; l'array (o la variabile, o il parametro) del tipo **interfaccia**; la forma dell'output uguale a quella della traccia, spazi compresi.

### Una classe astratta con costruttore, e un metodo completo che usa quello astratto

*Quando si usa:* la traccia chiede una classe base con dati comuni, un comportamento comune e un punto in cui le sottoclassi differiscono. Si veda la sezione 10.1.4.

```java
abstract class Abbonamento {
    private String nome;

    public Abbonamento(String nome) {                // il costruttore c'è, anche se la classe è astratta
        this.nome = nome;
    }

    public abstract double canone();                 // la parte che differisce

    public String scheda() {                         // la parte comune
        return nome + " -> " + canone() + " al mese";
    }
}

class Mensile extends Abbonamento {
    private double importo;

    public Mensile(String nome, double importo) {
        super(nome);                                 // prima istruzione
        this.importo = importo;
    }

    @Override
    public double canone() {
        return importo;
    }
}

class Annuale extends Abbonamento {
    private double importoAnno;

    public Annuale(String nome, double importoAnno) {
        super(nome);
        this.importoAnno = importoAnno;
    }

    @Override
    public double canone() {
        return importoAnno / 12;
    }
}

public class ProvaAbbonamenti {
    public static void main(String[] args) {
        Abbonamento a = new Mensile("Base", 12.0);
        Abbonamento b = new Annuale("Plus", 120.0);

        System.out.println(a.scheda());
        System.out.println(b.scheda());
    }
}
```

```text
Base -> 12.0 al mese
Plus -> 10.0 al mese
```

Non servono import né eccezioni. Punti da controllare: la classe astratta **ha** il costruttore e le sottoclassi lo richiamano con `super(...)` come prima istruzione; `scheda()` è scritto una volta sola nella classe astratta e nessuna sottoclasse lo riscrive; le variabili dei due oggetti sono dichiarate del tipo della classe astratta.

### Una classe che realizza `Comparable` e un array ordinato con `Arrays.sort`

*Quando si usa:* la traccia chiede che gli oggetti di una classe si possano ordinare, per un campo o per più campi. Si veda la sezione 10.4.

```java
import java.util.Arrays;                             // serve per Arrays.sort

class Corridore implements Comparable<Corridore> {
    private String nome;
    private int secondi;

    public Corridore(String nome, int secondi) {
        this.nome = nome;
        this.secondi = secondi;
    }

    @Override
    public int compareTo(Corridore altro) {          // public, parametro del tipo della classe
        int confronto = Integer.compare(secondi, altro.secondi);   // 1° criterio: tempo crescente
        if (confronto != 0) {
            return confronto;
        }
        return nome.compareTo(altro.nome);           // spareggio: nome in ordine alfabetico
    }

    @Override
    public String toString() {
        return nome + " " + secondi + "s";
    }
}

public class ProvaCorridori {
    public static void main(String[] args) {
        Corridore[] gara = {
            new Corridore("Elia", 62), new Corridore("Dora", 58), new Corridore("Anna", 62)
        };

        Arrays.sort(gara);
        for (int i = 0; i < gara.length; i++) {
            System.out.println(gara[i]);
        }
    }
}
```

```text
Dora 58s
Anna 62s
Elia 62s
```

Import necessario: `java.util.Arrays`. Nessuna eccezione da dichiarare. Punti da controllare: `implements Comparable<NomeClasse>`; il metodo si chiama `compareTo` (C minuscola in `compare`, T maiuscola in `To`), è `public`, restituisce `int` e riceve **un parametro del tipo della classe**; il segno del risultato (negativo = `this` viene prima) e non un valore esatto; niente sottrazione tra i campi, ma `Integer.compare`/`Double.compare`.

## Errori tipici

Alcuni errori sono già discussi nel testo: un refuso nel nome che con la classe astratta diventa errore di compilazione (sezione 10.1.2), la realizzazione di un metodo d'interfaccia senza `public` (sezione 10.2.3), la sottrazione nel `compareTo` (sezione 10.4.3), `Arrays.sort` su una classe che non realizza `Comparable` (sezione 10.4.1). Seguono gli altri.

> [!CAUTION]
> **Errore tipico — Creare un oggetto di una classe astratta o di un'interfaccia**
> ```java
> abstract class Tariffa { public abstract double costo(int minuti); }
> interface Pagabile { double importo(); }
>
> Tariffa t = new Tariffa();                   // ERRORE
> Pagabile p = new Pagabile();                 // ERRORE
> ```
> In entrambi i casi il compilatore risponde `... is abstract; cannot be instantiated`. Né l'una né l'altra possono avere oggetti propri: gli oggetti sono sempre di una classe concreta che le estende o le realizza. Forma corretta: `Tariffa t = new TariffaFissa(5.0);` e `Pagabile p = new Fattura(100.0, 0.25);`, dove il tipo dichiarato è quello astratto e l'oggetto è quello concreto.

> [!CAUTION]
> **Errore tipico — Un corpo dove non va, o nessun corpo dove serve**
> ```java
> abstract class Tariffa {
>     public abstract double costo(int minuti) { return 0; }   // ERRORE: i metodi astratti non hanno corpo
>     public double riepilogo(int minuti);                      // ERRORE: manca il corpo
> }
> ```
> Il compilatore risponde `abstract methods cannot have a body` per la prima riga e `missing method body, or declare abstract` per la seconda. Un metodo o è `abstract` (e finisce con `;`) o ha il corpo. Nelle interfacce vale solo la prima parte: un metodo con le graffe è rifiutato con `interface abstract methods cannot have body`.

> [!CAUTION]
> **Errore tipico — Dimenticare `abstract` sulla classe**
> ```java
> class Tariffa {                                    // ERRORE: manca abstract
>     public abstract double costo(int minuti);
> }
> ```
> Il compilatore risponde `Tariffa is not abstract and does not override abstract method costo(int) in Tariffa`. Un metodo astratto richiede una classe astratta: la parola `abstract` va **sia** sul metodo **sia** sulla classe. Lo stesso messaggio compare, con il nome della sottoclasse, quando una sottoclasse concreta non realizza tutti i metodi astratti: forma corretta, scrivere i metodi mancanti oppure dichiarare astratta anche la sottoclasse.

> [!CAUTION]
> **Errore tipico — Realizzare un'interfaccia senza scrivere tutti i metodi**
> ```java
> interface Descrivibile { String descrizione(); }
> interface Prezzabile extends Descrivibile { double prezzo(); }
>
> class Quaderno implements Prezzabile {             // ERRORE: manca descrizione()
>     public double prezzo() { return 2.5; }
> }
> ```
> Il compilatore risponde `Quaderno is not abstract and does not override abstract method descrizione() in Descrivibile`. Chi realizza un'interfaccia che ne estende un'altra deve scrivere i metodi di **entrambe** (sezione 10.2.7). Lo stesso vale con `implements A, B`: tutti i metodi di tutte le interfacce.

> [!CAUTION]
> **Errore tipico — `extends` e `implements` scambiati**
> ```java
> class C { }
> interface I { }
>
> class D implements C { }                     // ERRORE: C è una classe
> class E extends I { }                        // ERRORE: I è un'interfaccia
> ```
> Il compilatore risponde `interface expected here` alla prima e `no interface expected here` alla seconda. Forma corretta: `class D extends C` e `class E implements I`. Quando una classe usa entrambe, l'ordine è fisso: prima `extends`, poi `implements`.

> [!CAUTION]
> **Errore tipico — Chiamare attraverso l'interfaccia un metodo che l'interfaccia non ha**
> ```java
> Misurabile m = new Rettangolo(3.0, 4.0);
> System.out.println(m.getBase());             // ERRORE: getBase() è di Rettangolo, non di Misurabile
> ```
> Il compilatore risponde `cannot find symbol` con `symbol: method getBase()` e `location: variable m of type Misurabile`. Attraverso una variabile si vedono solo i metodi del suo tipo dichiarato (sezione 10.2.4). Forma corretta: aggiungere `getBase()` all'interfaccia (se tutte le classi devono averlo) oppure dichiarare la variabile come `Rettangolo`.

> [!CAUTION]
> **Errore tipico — Costruttori, variabili d'istanza o corpi dentro un'interfaccia**
> ```java
> interface Pagabile {
>     Pagabile();                              // ERRORE: <identifier> expected
>     int contatore;                           // ERRORE: = expected
>     double importo() { return 0; }           // ERRORE: interface abstract methods cannot have body
> }
> ```
> Un'interfaccia contiene soltanto intestazioni di metodi e costanti con valore (sezione 10.2.2). Per un costruttore o per dei campi di stato serve una classe, anche astratta: forma corretta, spostare costruttore e campi nella classe che realizza l'interfaccia, o in una classe astratta che la realizza.

> [!CAUTION]
> **Errore tipico — `abstract` insieme a `private`, `static` o `final`**
> ```java
> abstract class A {
>     private abstract void f();                 // ERRORE: illegal combination of modifiers: abstract and private
>     public static abstract void g();           // ERRORE: ... abstract and static
>     public abstract final void h();            // ERRORE: ... abstract and final
> }
> ```
> Un metodo astratto esiste per essere riscritto: `private` lo nasconde alle sottoclassi, `static` lo lega alla classe e non all'oggetto, `final` vieta di riscriverlo. Forma corretta: `public abstract void f();` (o `protected`).

> [!CAUTION]
> **Errore tipico — Una firma di `compareTo` che non coincide con quella dell'interfaccia**
> ```java
> class Frutto implements Comparable<Frutto> {
>     public int compareTo(Object altro) { return 0; }       // ERRORE: il parametro deve essere Frutto
> }
>
> class Pera implements Comparable {
>     public int compareTo(Pera altro) { return 0; }         // ERRORE: senza <...> il parametro è Object
> }
>
> class Mela implements Comparable<Mela> {
>     int compareTo(Mela altro) { return 0; }                // ERRORE: manca public
> }
> ```
> Per `Frutto` il compilatore risponde `Frutto is not abstract and does not override abstract method compareTo(Frutto) in Comparable`, seguito da `name clash: compareTo(Object) in Frutto and compareTo(Frutto) in Comparable have the same erasure, yet neither overrides the other`. Per `Pera`: `Pera is not abstract and does not override abstract method compareTo(Object) in Comparable`. Per `Mela`: `compareTo(Mela) in Mela cannot implement compareTo(T) in Comparable` con `attempting to assign weaker access privileges; was public`. Forma corretta: il tipo del parametro coincide con quello tra parentesi angolari (`Comparable<Frutto>` con `compareTo(Frutto)`, `Comparable` senza parentesi con `compareTo(Object)`), il metodo è `public` e restituisce `int`.

> [!CAUTION]
> **Errore tipico — Stampare il testo quando la traccia chiede di restituirlo**
> ```java
> class Gatto extends Animale {
>     public String verso() {
>         System.out.println("miao");          // ERRORE: la traccia chiede che il metodo RESTITUISCA "miao"
>     }
> }
> ```
> Il compilatore risponde `missing return statement`: un metodo con tipo di ritorno `String` deve terminare con un `return` su ogni percorso (Capitolo 6, sezione 6.1.4). Anche quando riesce a compilare perché il `return` c'è, scrivere `System.out.println` *dentro* il metodo al posto di restituire la stringa fa stampare due volte, o fuori posto, e non rispetta la traccia. Forma corretta: `public String verso() { return "miao"; }` e la stampa fatta da chi chiama.

> [!CAUTION]
> **Errore tipico — Una classe dove la traccia chiede un'interfaccia (e viceversa)**
> Una traccia che dice "definire l'interfaccia `Figura`" va soddisfatta con `interface Figura`, non con `abstract class Figura`; una che dice "classe astratta `Animale`" con `abstract class`, non con un'interfaccia. Le due versioni possono produrre lo stesso output, ma il docente valuta l'**aderenza letterale** alla struttura richiesta, e le classi che le realizzano cambiano parola chiave (`implements` al posto di `extends`). Nel dubbio, la parola della traccia (*interfaccia*, *classe astratta*) decide la parola chiave.

## Riassunto

Una **classe astratta** è una classe incompleta, dichiarata con `abstract`: può avere campi, costruttori e metodi completi come ogni classe, e in più **metodi astratti**, intestazioni senza corpo che terminano con `;` e che le sottoclassi devono realizzare. Non si può istanziare con `new`, ma si usa come tipo di variabili, parametri e array; è lo strumento giusto quando le classi sono parenti ("è un") e condividono dati e codice, perché permette di scrivere una volta la parte comune e lasciare astratto solo ciò che cambia. Un'**interfaccia**, dichiarata con `interface`, è un puro contratto: contiene intestazioni di metodi (implicitamente `public abstract`) e costanti (implicitamente `public static final`), nessun costruttore, nessuna variabile d'istanza, nessun corpo. Una classe la realizza con `implements` e deve scrivere tutti i suoi metodi, **dichiarandoli `public`**; può realizzarne quante vuole, mentre estende una sola classe, e nella riga di definizione l'ordine è `extends` poi `implements`. L'interfaccia è un tipo: un parametro `Misurabile` accetta qualunque oggetto di una classe che la realizza, e il binding dinamico sceglie la versione giusta del metodo. Un'interfaccia può estendere un'altra interfaccia. Tra le interfacce della libreria, `Comparable<T>` impone a una classe il suo **ordine naturale** con un solo metodo, `public int compareTo(T altro)`, che restituisce un valore negativo, zero o positivo; con `compareTo` realizzato, `Arrays.sort` ordina l'array di oggetti, mentre senza lancia `ClassCastException`. `Runnable`, con il solo `public void run()`, è l'interfaccia che permette di far eseguire un oggetto da un thread.

**Concetti chiave**

- **Metodo astratto.** Intestazione con la parola `abstract` e nessun corpo, terminata da `;`; esiste solo in una classe astratta.
- **Classe astratta.** Dichiarata con `abstract`; non si istanzia; può avere campi, costruttori e metodi completi, oltre a quelli astratti.
- **Realizzare i metodi astratti.** Una sottoclasse concreta deve scrivere tutti i metodi astratti che eredita; altrimenti è dichiarata astratta a sua volta.
- **Classe astratta come tipo.** Si possono dichiarare variabili, parametri e array del suo tipo, che contengono oggetti delle sottoclassi concrete.
- **Modificatori vietati.** `abstract` non si combina con `private`, `static`, `final`.
- **Interfaccia.** Dichiarata con `interface`: solo intestazioni di metodi pubblici e costanti; niente costruttori, variabili d'istanza o corpi.
- **`implements`.** Dichiara che una classe realizza un'interfaccia; ne scrive tutti i metodi, con `public`.
- **Interfaccia come tipo.** Si usa per variabili, parametri e array; il compilatore ammette solo i metodi dell'interfaccia, la JVM esegue quelli della classe dell'oggetto.
- **Costanti d'interfaccia.** Implicitamente `public static final`; si leggono con `Interfaccia.NOME`.
- **Più interfacce.** Una classe può realizzarne quante vuole, separate da virgole; con una superclasse, prima `extends` poi `implements`.
- **Interfaccia che estende un'interfaccia.** Eredita le intestazioni e ne aggiunge; chi la realizza scrive tutto.
- **Classe astratta o interfaccia.** Classe astratta per una parentela "è un" con codice e dati in comune; interfaccia per un'abilità condivisa da classi qualsiasi, senza codice in comune; la classe astratta si estende una volta sola, le interfacce si possono realizzare tutte.
- **`Comparable<T>`.** Interfaccia dell'ordine naturale: `public int compareTo(T altro)` restituisce negativo, zero o positivo.
- **Come si scrive `compareTo`.** Si delegano i campi ai confronti del loro tipo (`String.compareTo`, `Integer.compare`, `Double.compare`), con uno spareggio sui campi successivi; mai la sottrazione.
- **`Arrays.sort` su oggetti.** Ordina secondo `compareTo`; senza `Comparable` lancia `ClassCastException`.
- **`Runnable`.** Interfaccia con `public void run()`, realizzata dalle classi i cui oggetti vanno eseguiti da un thread.

**Sintassi essenziale**

| Elemento | Forma |
|---|---|
| Classe astratta | `abstract class Tariffa { ... }` |
| Metodo astratto | `public abstract double costo(int minuti);` |
| Sottoclasse concreta | `class TariffaFissa extends Tariffa { public double costo(int m) { ... } }` |
| Interfaccia | `interface Misurabile { double area(); }` |
| Costante d'interfaccia | `interface Soglie { int MASSIMO = 100; }` |
| Realizzare un'interfaccia | `class Rettangolo implements Misurabile { public double area() { ... } }` |
| Più interfacce | `class P extends Materiale implements Misurabile, Etichettabile { ... }` |
| Interfaccia che ne estende un'altra | `interface Prezzabile extends Descrivibile { double prezzo(); }` |
| Variabile di tipo interfaccia | `Misurabile m = new Rettangolo(3.0, 4.0);` |
| Ordine naturale (generico) | `class Frutto implements Comparable<Frutto> { public int compareTo(Frutto altro) { ... } }` |
| Ordine naturale (forma con `Object`) | `class Frutto implements Comparable { public int compareTo(Object altro) { ... } }` |
| Ordinare un array di oggetti | `Arrays.sort(frutti);` |
| Realizzare `Runnable` | `class Saluto implements Runnable { public void run() { ... } }` |

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `Comparable<T>` (`java.lang`) | `compareTo` | `int compareTo(T o)` (interfaccia) | `NullPointerException` se `o` è `null`; `ClassCastException` se il tipo impedisce il confronto |
| `Runnable` (`java.lang`) | `run` | `void run()` (interfaccia; Capitolo 17) | — |
| `Thread` (`java.lang`) | costruttore | `public Thread(Runnable target)` (Capitolo 17) | — |
| `Arrays` (`java.util`) | `sort` | `public static void sort(Object[] a)` (elementi `Comparable`) | `ClassCastException` se gli elementi non sono confrontabili tra loro |
| `Integer` (`java.lang`) | `compare` | `public static int compare(int x, int y)` | — |
| `Double` (`java.lang`) | `compare` | `public static int compare(double d1, double d2)` | — |
| `String` (`java.lang`) | `compareTo` | `public int compareTo(String anotherString)` | — |
| `String` (`java.lang`) | `compareToIgnoreCase` | `public int compareToIgnoreCase(String str)` | — |
