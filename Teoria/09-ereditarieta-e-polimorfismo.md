---
materia: Programmazione a Oggetti
capitolo: 9
titolo: Ereditarietà e polimorfismo
livello_syllabus: 2-3
stato: completo
slide: ["Savitch cap. 10 slide 3-24", "Savitch cap. 11 slide 3-7 e 16", "Lect2 (Class Hierarchy, Classes)", "Multithreading p. 10"]
appelli: [EXAM1]
fonti_esterne: 8
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 9 — Ereditarietà e polimorfismo

## Di cosa parla questo capitolo

Nel [Capitolo 7 — Classi e oggetti](07-classi-e-oggetti.md) abbiamo imparato a scrivere una classe, e nel [Capitolo 8 — Riferimenti e memoria](08-riferimenti-e-memoria.md) a ragionare su che cosa contengono le variabili che la usano. Ora affrontiamo un problema che si presenta presto in qualunque programma di dimensioni non banali: **classi diverse che hanno molto in comune**. Uno studente è una persona, quindi ha un nome come ogni persona, ma in più ha una matricola; un tesista è uno studente che in più ha un titolo di tesi. Scrivere tre volte il campo `nome`, tre volte i metodi che lo leggono e lo cambiano, e dover correggere tre volte lo stesso errore, è uno spreco e una fonte di sbagli.

Java risolve il problema con l'**ereditarietà**: si scrive una volta la classe più generale (`Persona`) e si dichiarano le classi più specifiche (`Studente`, `Tesista`) come sue *estensioni*, che ricevono tutto ciò che la classe generale mette a disposizione e aggiungono del proprio. Da qui discendono quasi tutti gli argomenti del capitolo: come si dichiara un'estensione (`extends`), che cosa può e che cosa non può vedere (`private`, `protected`), come si costruisce l'oggetto (`super(...)`), come una sottoclasse **riscrive** un comportamento ereditato (*overriding*, `@Override`, `super.metodo()`), perché una variabile `Persona` può indicare uno `Studente` (compatibilità di tipo) e che cosa succede quando si chiama un metodo attraverso di essa (**polimorfismo** e *binding dinamico*). Il capitolo si chiude con la classe `Object`, antenata di tutte le classi, e con i tre metodi che quasi ogni classe riscrive: `toString`, `equals` (in forma definitiva, come promesso nel Capitolo 8) e `hashCode`.

Alla fine saprai dichiarare una sottoclasse e scrivere i suoi costruttori nel modo che il compilatore accetta e che la traccia chiede; saprai riscrivere un metodo senza confonderlo con un overload; saprai prevedere quale versione di un metodo viene eseguita quando una variabile ha un tipo e l'oggetto un altro; saprai scrivere `toString`, `equals(Object)` e `hashCode` per una classe tua; e saprai spiegare a voce la differenza tra overloading e overriding, perché Java non ha l'ereditarietà multipla tra classi e che cosa sia il binding dinamico.

> [!IMPORTANT]
> **Nota per l'esame — Qui si perde per un dettaglio di forma**
> Le tracce che usano l'ereditarietà sono scarne: "una sottoclasse `X` della classe `Y`, con due costruttori, che ridefinisce il metodo `m`". Nessuna dice quale costruttore della superclasse chiamare, né che il metodo ridefinito deve restare `public`. Chi ha chiari i meccanismi di questo capitolo li deduce; chi li ricorda a metà consuma le cinque esecuzioni su errori come `constructor Y in class Y cannot be applied to given types`. Vedi la sezione "Come esce all'esame" e gli scheletri.

## 9.1 Ereditarietà: riusare una classe esistente

### 9.1.1 Il problema: classi quasi uguali

Supponiamo di dover gestire le persone di un ateneo. Cominciamo con una classe `Persona`: un nome, un modo per leggerlo e cambiarlo, un metodo che lo scrive a video. Fin qui nessuna novità rispetto al Capitolo 7. Poi arrivano gli studenti. Uno studente ha tutto ciò che ha una persona (un nome, i metodi per leggerlo e cambiarlo, il modo di scriverlo) e in più una matricola. Una soluzione ingenua è copiare la classe `Persona`, chiamarla `Studente` e aggiungere il campo `matricola`. Funziona, ma ha tre difetti:

- il codice di `Persona` esiste in due copie: se in `Persona` si scopre un errore, bisogna ricordarsi di correggerlo anche in `Studente`, e prima o poi ci si dimentica;
- il compilatore non sa che uno studente è anche una persona: un metodo scritto per ricevere una `Persona` non accetta uno `Studente`, anche se ne ha tutte le proprietà;
- quando arriveranno i tesisti, i docenti, i segretari, le copie saranno cinque.

Il meccanismo che evita tutto questo è l'**ereditarietà** (*inheritance*): una classe già scritta viene usata come **punto di partenza** per scriverne un'altra, la quale ne riceve automaticamente campi e metodi e ne aggiunge di nuovi. Lo schema è lo stesso con cui in biologia si dice che un cane *eredita* da un animale le caratteristiche generali (respira, si nutre) e poi ne aggiunge di proprie (abbaia). L'analogia funziona fino a un certo punto: in Java non c'è nessun "gene" che passa a caso, c'è una regola precisa di che cosa passa e che cosa no, ed è quella che vedremo.

### 9.1.2 `extends`: classe base e classe derivata

Scriviamo la classe generale, che chiameremo **classe base** o **superclasse** (*base class*, *superclass*). È una classe come quelle del Capitolo 7: un campo privato, due costruttori, accessor e mutator, un metodo che stampa.

```java
class Persona {
    private String nome;

    public Persona() {
        nome = "Nessun nome";
    }

    public Persona(String nome) {
        this.nome = nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }

    public void scrivi() {
        System.out.println("Nome: " + nome);
    }

    public boolean haLoStessoNome(Persona altra) {
        return nome.equals(altra.nome);
    }
}
```

Ora dichiariamo `Studente` come **classe derivata** o **sottoclasse** (*derived class*, *subclass*) di `Persona`. La parola chiave è **`extends`** ("estende"), e va scritta nella riga di definizione della classe, subito dopo il nome. Dentro il corpo mettiamo **solo ciò che `Studente` aggiunge**: il campo `matricola`, i costruttori, i metodi che riguardano la matricola.

```java
class Studente extends Persona {
    private int matricola;

    public Studente() {
        super();
        matricola = 0;
    }

    public Studente(String nome, int matricola) {
        super(nome);
        this.matricola = matricola;
    }

    public void reimposta(String nome, int matricola) {
        setNome(nome);
        this.matricola = matricola;
    }

    public int getMatricola() {
        return matricola;
    }

    public void setMatricola(int matricola) {
        this.matricola = matricola;
    }
}
```

Per ora prendiamo le due righe `super(...)` come un dato di fatto: le spiegheremo nella sezione 9.3. Quello che conta qui è che `Studente` **non** contiene un campo `nome` né i metodi `getNome`, `setNome`, `scrivi`, `haLoStessoNome`, e tuttavia un oggetto `Studente` li ha. Vediamolo in un programma.

```java
public class ProvaEreditarieta {
    public static void main(String[] args) {
        Studente s = new Studente("Luisa Conti", 4001);

        s.scrivi();                                  // metodo ereditato da Persona
        s.setNome("Luisa Conti Rossi");              // anche questo
        s.scrivi();
        System.out.println(s.getNome() + " ha matricola " + s.getMatricola());
    }
}
```

```text
Nome: Luisa Conti
Nome: Luisa Conti Rossi
Luisa Conti Rossi ha matricola 4001
```

Riga per riga. `new Studente("Luisa Conti", 4001)` usa il costruttore a due parametri di `Studente`. `s.scrivi()` chiama un metodo che nella classe `Studente` non c'è: Java non lo cerca solo lì, lo cerca risalendo la catena delle classi base, e lo trova in `Persona`. Lo stesso vale per `setNome` e `getNome`. `getMatricola()`, invece, è un metodo di `Studente` stessa. Si noti che `scrivi()` scrive solo il nome: la matricola non c'è, perché il metodo è quello di `Persona`, che della matricola non sa niente. Sistemeremo questo difetto nella sezione 9.4, con l'overriding.

> [!NOTE]
> **Definizione — Classe base, classe derivata, `extends`**
> L'**ereditarietà** permette di definire una classe generale e poi una classe più specifica che ne riceve campi e metodi e ne aggiunge di nuovi. La classe generale si chiama **classe base** o **superclasse**; quella specifica **classe derivata** o **sottoclasse**. In Java la sottoclasse si dichiara con la parola chiave `extends`:
> ```java
> class Studente extends Persona { ... }
> ```
> Si dice anche che `Studente` *estende* (o *eredita da*) `Persona`.

Una precisazione di vocabolario che si ripresenta nelle tracce: "superclasse" e "classe base" sono la stessa cosa, come "sottoclasse" e "classe derivata"; **padre** e **figlia** si usano spesso a voce, ma non sono termini del linguaggio.

Le gerarchie di classi si disegnano con i **diagrammi UML** (*Unified Modeling Language*, lo stesso formato usato per il diagramma delle classi del Capitolo 7, sezione 7.3.8): ogni classe è un rettangolo e l'ereditarietà è una **freccia con la punta vuota che va dalla sottoclasse alla superclasse**. La freccia, dunque, indica "è un caso particolare di". In ASCII:

```text
   +---------------------+
   | Persona             |
   |---------------------|
   | - nome: String      |
   |---------------------|
   | + scrivi()          |
   | + getNome()         |
   +---------------------+
              ^
              |
   +---------------------+
   | Studente            |
   |---------------------|
   | - matricola: int    |
   |---------------------|
   | + getMatricola()    |
   +---------------------+
```

Nel riquadro di `Studente` non si ripetono i membri di `Persona`: sono ereditati, e la freccia lo dice già.

### 9.1.3 Che cosa passa alla sottoclasse

Possiamo ora precisare che cosa "ereditare" vuol dire. Un oggetto `Studente` è, in memoria, **un unico oggetto che contiene tutti i campi dichiarati nella sua classe e in tutte le sue classi base**. Dopo l'istruzione `Studente s = new Studente("Luisa Conti", 4001);` la situazione nello heap (Capitolo 8, sezione 8.1.3) è questa:

```text
   stack                          heap
  +-------+                  +-----------------------------+
  |   s   |----------------->| oggetto Studente            |
  +-------+                  |   nome      = "Luisa Conti" |  <- campo dichiarato in Persona
                             |   matricola = 4001          |  <- campo dichiarato in Studente
                             +-----------------------------+
```

Il campo `nome` esiste, dentro l'oggetto, anche se il codice scritto dentro `Studente` non può nominarlo (vedremo perché nella sezione 9.2). Che cosa si può usare e che cosa no, riassunto:

| Elemento della superclasse | Nella sottoclasse |
|---|---|
| Metodi `public` | ereditati: si possono chiamare su un oggetto della sottoclasse, e dentro la sottoclasse, per nome |
| Metodi `protected` | ereditati (sezione 9.2.2) |
| Campi `public` | ereditati |
| Campi e metodi `private` | **non accessibili per nome**; i campi privati esistono comunque nell'oggetto (sezione 9.2) |
| Costruttori | **non ereditati**: la sottoclasse deve scrivere i propri e richiamare quello della superclasse (sezione 9.3) |

Il compito della sottoclasse è dunque *aggiungere* e, quando serve, *riscrivere*: la sezione 9.4 spiega come.

### 9.1.4 Una sottoclasse di una sottoclasse

Una classe derivata può a sua volta essere la classe base di un'altra. Scriviamo `Tesista`, uno studente che sta preparando la tesi e ha un titolo.

```java
class Tesista extends Studente {
    private String titoloTesi;

    public Tesista() {
        super();
        titoloTesi = "Da assegnare";
    }

    public Tesista(String nome, int matricola, String titoloTesi) {
        super(nome, matricola);
        this.titoloTesi = titoloTesi;
    }

    public String getTitoloTesi() {
        return titoloTesi;
    }

    public void setTitoloTesi(String titoloTesi) {
        this.titoloTesi = titoloTesi;
    }
}
```

```java
public class ProvaGerarchia {
    public static void main(String[] args) {
        Tesista t = new Tesista("Paolo Serra", 4002, "Reti di sensori");

        t.scrivi();                                  // definito in Persona
        System.out.println(t.getMatricola());        // definito in Studente
        System.out.println(t.getTitoloTesi());       // definito in Tesista
    }
}
```

```text
Nome: Paolo Serra
4002
Reti di sensori
```

Un oggetto `Tesista` ha **tutti** i membri accessibili delle due classi che lo precedono: la catena di ereditarietà si segue verso l'alto fino in fondo. La gerarchia ha ora tre livelli:

```text
   Persona  <----  Studente  <----  Tesista
```

e ciascuna classe può essere vista come un caso particolare della precedente. Questo ci dà modo di parlare di **antenati** (superclassi dirette e indirette di una classe: per `Tesista`, `Studente` e `Persona`) e di **discendenti** (sottoclassi dirette e indirette). Alla radice di tutte le gerarchie c'è una classe che non abbiamo ancora nominato: la sezione 9.7 la presenta.

> [!TIP]
> **Intuizione — Riusare il codice, non copiarlo**
> `Tesista` è breve perché non riscrive niente: eredita da `Studente` ciò che `Studente` ha e a sua volta ciò che `Studente` ha ereditato da `Persona`. Se un giorno cambia il modo in cui `Persona` memorizza il nome, il cambiamento è in un posto solo e raggiunge subito `Studente` e `Tesista`. È questo il vantaggio per cui l'ereditarietà esiste: **un'unica copia del codice comune**.

### 9.1.5 Una sola superclasse

Una classe Java può avere **una sola** superclasse diretta: dopo `extends` si scrive un nome, non due. Questa regola si chiama **ereditarietà singola**. Altri linguaggi (per esempio C++) permettono l'ereditarietà multipla, cioè più classi base; Java l'ha esclusa per le classi, perché se due classi base avessero un metodo con lo stesso nome ma comportamenti diversi, la sottoclasse non saprebbe quale ereditare. Quello che non si può fare con le classi si ottiene in un altro modo, con le **interfacce** (Capitolo 10 — [Classi astratte e interfacce](10-classi-astratte-e-interfacce.md)): una classe può estendere una sola classe ma **implementare** quante interfacce vuole.

Un caso che incontreremo nei capitoli sui thread è questo. La classe `Thread` è una classe (si estende), `Runnable` è un'interfaccia (si implementa). Se una classe estende già qualcosa, per essere eseguita da un thread non può estendere anche `Thread`, e quindi implementa `Runnable`. Nella riga di definizione le due clausole hanno un **ordine fisso**: prima `extends`, poi `implements`.

```java
class Persona {
    private String nome;

    public Persona(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }
}

class Studente extends Persona implements Runnable {   // prima extends, poi implements
    public Studente(String nome) {
        super(nome);
    }

    public void run() {
        System.out.println(getNome() + " esegue run");
    }
}

public class ProvaOrdine {
    public static void main(String[] args) {
        Studente s = new Studente("Luisa Conti");
        s.run();                                  // chiamata diretta: nessun thread qui
    }
}
```

```text
Luisa Conti esegue run
```

Qui `Studente` ha la superclasse `Persona` e in più si impegna a fornire il metodo `run` richiesto da `Runnable`. L'interfaccia, il significato di `implements` e i thread sono rinviati ai Capitoli 10 e 17; in questo capitolo ci serve solo l'ordine delle due clausole, che si scrivono sempre così.

## 9.2 Che cosa vede la sottoclasse: `private` e `protected`

### 9.2.1 I membri privati non si nominano

Dentro `Studente` proviamo a fare la cosa più naturale: scrivere un metodo che usa direttamente il campo `nome`, come se fosse un campo di `Studente`.

> [!CAUTION]
> **Errore tipico — Usare per nome un campo `private` della superclasse**
> ```java
> class Studente extends Persona {
>     private int matricola;
>
>     public String descrizione() {
>         return nome + " " + matricola;       // ERRORE: nome è private in Persona
>     }
> }
> ```
> Il compilatore risponde `nome has private access in Persona`. Il campo esiste nell'oggetto, ma `private` significa "visibile solo dentro la classe che lo dichiara", e la sottoclasse è un'altra classe. Forma corretta: usare l'accessor ereditato, `getNome() + " " + matricola`.

Il campo c'è, ma la sottoclasse non lo può **nominare**. Lo stesso vale per i metodi `private`: un metodo privato della superclasse non può essere chiamato per nome dalla sottoclasse. La sottoclasse deve passare dai metodi pubblici della superclasse (gli accessor e i mutator del Capitolo 7, sezione 7.3.3): è esattamente per questo che `reimposta` di `Studente` ha usato `setNome(nome)` e non `this.nome = nome`.

La regola è coerente con l'*information hiding* (Capitolo 7, sezione 7.3): la classe `Persona` ha scelto di nascondere il modo in cui memorizza il nome, e questa scelta vale per **tutti** gli altri, sottoclassi comprese. Se un giorno `Persona` memorizzasse nome e cognome in un unico campo, le sottoclassi continuerebbero a funzionare, perché usano `getNome()` e non il campo.

### 9.2.2 `protected`

Esiste un livello di accesso intermedio, già incontrato nel Capitolo 7 (sezione 7.3.6): `protected`. Un membro `protected` è visibile alle **sottoclassi** (e alle classi dello stesso package). Definiamo un veicolo con una velocità `protected` e un'auto che la modifica direttamente.

```java
class Veicolo {
    protected int velocita;

    public Veicolo(int velocita) {
        this.velocita = velocita;
    }

    public int getVelocita() {
        return velocita;
    }
}

class Auto extends Veicolo {
    public Auto(int velocita) {
        super(velocita);
    }

    public void accelera(int delta) {
        velocita = velocita + delta;               // campo protected: la sottoclasse lo nomina
    }
}

public class ProvaProtected {
    public static void main(String[] args) {
        Auto a = new Auto(50);
        a.accelera(30);
        System.out.println(a.getVelocita());
    }
}
```

```text
80
```

`accelera` scrive `velocita` per nome, senza passare da `getVelocita`: con `private` non compilerebbe. È comodo, ma ha un prezzo: `protected` rompe in parte l'incapsulamento, perché ogni sottoclasse (anche una scritta in futuro da altri) può modificare il campo come vuole.

> [!WARNING]
> **Attenzione — In un file unico `protected` non protegge da nessuno**
> `protected` include il livello di package: un membro `protected` è visibile **a tutte le classi dello stesso package**, anche a quelle che non c'entrano niente con l'ereditarietà. Nelle prove scritte tutte le classi stanno nello stesso file e quindi nello stesso package (Capitolo 7, sezione 7.6): in quel contesto una classe qualunque, come `ProvaProtected`, potrebbe scrivere `a.velocita = 5;` e compilerebbe. Non fidarsi di `protected` come protezione.

> [!IMPORTANT]
> **Nota per l'esame — Il vincolo "information hiding" ha la precedenza**
> Quando una traccia chiede di "usare rigorosamente l'information hiding" o di rendere "tutte le variabili d'istanza private", il livello giusto è `private`, per **tutti** i campi, anche nelle sottoclassi. `protected` sui campi sarebbe una violazione letterale del vincolo. Le sottoclassi accedono ai dati della superclasse con i suoi metodi `get` e `set`.

## 9.3 I costruttori nelle classi derivate

### 9.3.1 I costruttori non si ereditano: `super(...)`

Nella tabella della sezione 9.1.3 i costruttori erano l'unica voce "non ereditata", e c'è una ragione. Un costruttore serve a dare i valori iniziali ai campi di *quella* classe; il costruttore di `Persona` sa inizializzare `nome`, ma non sa niente di `matricola`, quindi non basterebbe a costruire uno `Studente`. Ogni sottoclasse deve perciò avere i **propri** costruttori.

Rimane un problema. Un oggetto `Studente` contiene anche la parte di `Persona` (il campo `nome`, sezione 9.1.3), e quella parte va inizializzata. Il costruttore di `Studente` non può farlo da solo, perché `nome` è `private` (sezione 9.2.1): non può scrivere `this.nome = nome`. La parte di `Persona` può essere inizializzata soltanto da un **costruttore di `Persona`**. La regola è dunque questa: **il costruttore di una sottoclasse deve richiamare un costruttore della superclasse**, e lo fa con la parola chiave **`super`** seguita dagli argomenti tra parentesi, come in `super(nome)`. Quella chiamata sceglie *quale* costruttore della superclasse eseguire, esattamente come `new Persona("Luisa")` sceglie tra i costruttori di `Persona` guardando i parametri (Capitolo 7, sezione 7.2.4).

```java
class Studente extends Persona {
    private int matricola;

    public Studente(String nome, int matricola) {
        super(nome);                     // 1. costruisce la parte Persona, con il costruttore a un parametro
        this.matricola = matricola;      // 2. poi la parte specifica di Studente
    }
}
```

La chiamata `super(...)` deve essere la **prima istruzione** del costruttore. È una regola del linguaggio, non un'abitudine: prima si costruisce la parte ereditata, poi si completa quella della sottoclasse, perché la seconda può servirsi della prima.

> [!NOTE]
> **Definizione — `super(...)` nel costruttore**
> Nel costruttore di una sottoclasse, `super(argomenti)` richiama un costruttore della superclasse (quello i cui parametri corrispondono agli argomenti). Deve essere la **prima istruzione** del costruttore.

### 9.3.2 Se non si scrive `super(...)`

Che cosa succede se il costruttore di una sottoclasse non contiene nessuna chiamata a `super`? Java ne inserisce una **implicita**, senza argomenti: all'inizio del costruttore il compilatore aggiunge `super();`. Una sottoclasse senza alcun costruttore riceve il costruttore di default (Capitolo 7, sezione 7.2.3), e anche quello comincia con `super();`. Vediamolo in un programma che stampa una riga in ogni costruttore, con tre generazioni.

```java
class Nonno {
    public Nonno() {
        System.out.println("Costruttore di Nonno");
    }
}

class Padre extends Nonno {
    public Padre() {
        System.out.println("Costruttore di Padre");     // nessun super(): ne viene aggiunto uno implicito
    }
}

class Figlio extends Padre {
    public Figlio() {
        super();                                         // esplicito: equivale a non scriverlo
        System.out.println("Costruttore di Figlio");
    }
}

public class ProvaOrdineCostruttori {
    public static void main(String[] args) {
        System.out.println("Creo un Figlio");
        new Figlio();
    }
}
```

```text
Creo un Figlio
Costruttore di Nonno
Costruttore di Padre
Costruttore di Figlio
```

`new Figlio()` esegue il costruttore di `Figlio`, il quale come prima cosa richiama quello di `Padre` (qui con un `super()` scritto), che come prima cosa richiama quello di `Nonno` (qui con un `super()` implicito). Il costruttore di `Nonno` non richiama niente: è alla fine della catena, perché ogni classe senza `extends` ha come superclasse `Object` (sezione 9.7), il cui costruttore non stampa nulla. A questo punto la catena si "srotola" all'indietro: stampa prima `Nonno`, poi `Padre`, poi `Figlio`. **Si costruisce dall'antenato più lontano verso la classe dell'oggetto.**

Il caso importante è quello in cui la chiamata implicita **non può funzionare**. Se la superclasse ha soltanto costruttori con parametri, il costruttore senza argomenti che il compilatore tenta di richiamare non esiste.

> [!CAUTION]
> **Errore tipico — Costruttore della sottoclasse che dimentica `super(...)`**
> ```java
> class Dispositivo {
>     private String marca;
>
>     public Dispositivo(String marca) {         // l'unico costruttore ha un parametro
>         this.marca = marca;
>     }
> }
>
> class Telefono extends Dispositivo {
>     private String numero;
>
>     public Telefono(String numero) {           // ERRORE: super() implicito, ma Dispositivo() non esiste
>         this.numero = numero;
>     }
> }
> ```
> Il compilatore segnala `constructor Dispositivo in class Dispositivo cannot be applied to given types;` con le righe `required: String` e `found: no arguments`. Lo stesso errore si presenta, sulla riga della classe, se `Telefono` non scrive nessun costruttore: quello di default comincia anch'esso con `super();`. Forma corretta: `super(marca)` come prima istruzione, con un valore da passare (sezione 9.3.5).

È lo stesso fenomeno del "costruttore di default che sparisce" del Capitolo 7, visto dall'altra parte: appena una classe scrive un costruttore con parametri, il costruttore senza argomenti non esiste più, e le sue sottoclassi lo pagano.

### 9.3.3 `this(...)` e `super(...)` non si sommano

Nel Capitolo 7 (sezione 7.2.5) un costruttore poteva richiamarne un altro della **stessa** classe con `this(...)`, anch'essa come prima istruzione. Ora abbiamo due chiamate che vogliono entrambe essere la prima: in uno stesso costruttore se ne può scrivere **una sola**. Non è una limitazione che pesa, perché una catena di `this(...)` finisce sempre in un costruttore che richiama `super(...)`, esplicitamente o no.

```java
class Studente extends Persona {
    private int matricola;

    public Studente(String nome, int matricola) {
        super(nome);                         // questo è il costruttore "vero": chiama la superclasse
        this.matricola = matricola;
    }

    public Studente(String nome) {
        this(nome, 0);                       // passa dall'altro costruttore, e quindi da super(nome)
    }

    public Studente() {
        this("Nessun nome");                 // a catena: arriva a super(nome) attraverso due costruttori
    }

    public int getMatricola() {
        return matricola;
    }
}

public class ProvaCatena {
    public static void main(String[] args) {
        Studente a = new Studente("Luisa Conti", 4001);
        Studente b = new Studente("Paolo Serra");
        Studente c = new Studente();

        System.out.println(a.getNome() + " " + a.getMatricola());
        System.out.println(b.getNome() + " " + b.getMatricola());
        System.out.println(c.getNome() + " " + c.getMatricola());
    }
}
```

```text
Luisa Conti 4001
Paolo Serra 0
Nessun nome 0
```

(La classe `Persona` è quella della sezione 9.1.2.) Solo il costruttore a due parametri chiama `super(nome)`; gli altri due non lo scrivono perché non possono (hanno già un `this(...)` come prima istruzione) e non serve: arrivano al costruttore completo, e da lì alla superclasse. Il vantaggio è lo stesso del Capitolo 7: la logica di inizializzazione sta in un posto solo.

### 9.3.4 Quando il costruttore non ha i dati per la superclasse

Una situazione che le tracce amano: la superclasse ha **un solo costruttore, con parametri**, e la sottoclasse deve avere un costruttore che **non riceve** quei valori. Per esempio, `Dispositivo` si costruisce con marca e modello, e `Telefono` deve avere due costruttori, uno che li riceve e uno che riceve soltanto numero e operatore.

La regola della sezione 9.3.1 non ammette eccezioni: **il costruttore di `Telefono` deve comunque richiamare `super(marca, modello)`**, quindi bisogna passare *qualcosa*. Se la traccia non lo dice, si sceglie un valore fisso, neutro, e lo si passa come argomento.

```java
class Dispositivo {
    private String marca;
    private String modello;

    public Dispositivo(String marca, String modello) {
        this.marca = marca;
        this.modello = modello;
    }

    public String getMarca() {
        return marca;
    }

    public String getModello() {
        return modello;
    }
}

class Telefono extends Dispositivo {
    private String numero;
    private String operatore;

    public Telefono(String marca, String modello, String numero) {
        super(marca, modello);                       // i dati ci sono: si passano
        this.numero = numero;
        this.operatore = "n.d.";
    }

    public Telefono(String numero, String operatore) {
        super("sconosciuta", "sconosciuto");         // i dati non ci sono: valori fissi, ma la chiamata è obbligatoria
        this.numero = numero;
        this.operatore = operatore;
    }

    public String getNumero() {
        return numero;
    }

    public String getOperatore() {
        return operatore;
    }
}

public class ProvaDispositivi {
    public static void main(String[] args) {
        Telefono t1 = new Telefono("Acme", "X1", "3331112222");
        Telefono t2 = new Telefono("3334445555", "Rete7");

        System.out.println(t1.getMarca() + " " + t1.getModello() + " " + t1.getNumero() + " " + t1.getOperatore());
        System.out.println(t2.getMarca() + " " + t2.getModello() + " " + t2.getNumero() + " " + t2.getOperatore());
    }
}
```

```text
Acme X1 3331112222 n.d.
sconosciuta sconosciuto 3334445555 Rete7
```

I due costruttori di `Telefono` sono in overloading (Capitolo 7, sezione 7.2.4): uno ha tre parametri `String`, l'altro due, e sono distinti dal numero di parametri. Il secondo non ha marca e modello, ma li deve fornire a `Dispositivo`: `super("sconosciuta", "sconosciuto")`. Il risultato si vede nella seconda riga, dove i getter ereditati restituiscono i valori fissi.

Ci sono altri modi di uscirne, da scegliere in base a ciò che la traccia permette:

- passare `null` (`super(null, null)`): compila, ma lascia i campi senza oggetto, e un uso successivo dà una `NullPointerException` (Capitolo 8, sezione 8.3.2). Va bene solo se la traccia chiede proprio `null`;
- far passare il secondo costruttore dal primo con `this("sconosciuta", "sconosciuto", numero);`, e poi assegnare `operatore` (sezione 9.3.3): utile se si vuole evitare di ripetere la logica del primo;
- aggiungere a `Dispositivo` un costruttore senza argomenti, così la chiamata implicita funziona: **non è possibile** se la traccia fornisce già la superclasse e dice di non toccarla, come accade spesso.

> [!IMPORTANT]
> **Nota per l'esame — Il parametro che manca**
> Una traccia che dà una superclasse con un solo costruttore e chiede una sottoclasse con un costruttore dai parametri diversi *non dice* come riempire la parte ereditata: tocca allo studente accorgersi che `super(...)` è obbligatorio. Il compilatore lo ricorda con `constructor X in class X cannot be applied to given types`, ma ogni errore di compilazione consuma una delle cinque esecuzioni. Prima di scrivere un costruttore di sottoclasse, si guarda **sempre** quali costruttori ha la superclasse.

## 9.4 Riscrivere un metodo: l'overriding

### 9.4.1 Che cosa vuol dire riscrivere

Abbiamo lasciato un difetto: `scrivi()` di `Persona`, ereditato da `Studente`, stampa solo il nome, mentre uno studente ha anche una matricola. Possiamo aggiungere un metodo con un altro nome (`scriviStudente()`), ma il programma che chiama `scrivi()` su una persona dovrebbe sapere se ha davanti uno studente. La soluzione è **riscrivere** (*to override*, "ridefinire", "sovrascrivere") `scrivi` nella sottoclasse: si dichiara in `Studente` un metodo con **lo stesso nome e gli stessi parametri** di quello della superclasse. Per un oggetto di `Studente` viene usata la nuova versione.

```java
class Studente extends Persona {
    private int matricola;

    public Studente(String nome, int matricola) {
        super(nome);
        this.matricola = matricola;
    }

    public int getMatricola() {
        return matricola;
    }

    public void scrivi() {                              // stessa firma di Persona.scrivi()
        System.out.println("Nome: " + getNome());
        System.out.println("Matricola: " + matricola);
    }
}

public class ProvaRiscrittura {
    public static void main(String[] args) {
        Persona p = new Persona("Anna Verdi");
        Studente s = new Studente("Luisa Conti", 4001);

        p.scrivi();                                     // versione di Persona
        s.scrivi();                                     // versione di Studente
    }
}
```

```text
Nome: Anna Verdi
Nome: Luisa Conti
Matricola: 4001
```

(Anche qui `Persona` è quella della sezione 9.1.2.) Le due chiamate hanno lo stesso aspetto, `x.scrivi()`, ma eseguono codice diverso, perché l'oggetto è di classi diverse: la prima trova `scrivi` in `Persona`, la seconda trova in `Studente` una versione che *riscrive* quella ereditata e usa quella. Dentro la nuova versione, il nome non si legge da `nome` (privato) ma da `getNome()` (sezione 9.2.1).

> [!NOTE]
> **Definizione — Overriding**
> Una sottoclasse **riscrive** (*override*) un metodo ereditato quando dichiara un metodo con la **stessa firma**, cioè lo stesso nome e gli stessi tipi di parametri, e con lo stesso tipo di ritorno. Per gli oggetti della sottoclasse vale il metodo riscritto, non quello della superclasse.

Come si vede, la firma è tutto ciò che conta. Se il nome o i parametri differiscono, **non** si sta riscrivendo niente: si sta aggiungendo un secondo metodo (sezione 9.4.4). Se la firma è uguale ma il tipo di ritorno differisce, il compilatore rifiuta: per esempio un `int scrivi()` in `Studente` dà `scrivi() in Studente cannot override scrivi() in Persona; return type int is not compatible with void`.

### 9.4.2 L'annotazione `@Override`

Nel metodo `scrivi` di `Studente` un errore di battitura (`scrivii`) o un parametro in più non produrrebbe nessun messaggio: il compilatore vedrebbe semplicemente un secondo metodo, e `s.scrivi()` continuerebbe a eseguire quello di `Persona`, con un output sbagliato e nessuna spiegazione. Per questo Java offre l'**annotazione `@Override`**.

Un'**annotazione** (*annotation*) è un'indicazione che si scrive **prima di una dichiarazione**, comincia con `@` e non cambia ciò che il codice fa: dà al compilatore (o ad altri strumenti) un'informazione. `@Override` si mette sopra un metodo e dice: "questo metodo intende riscrivere un metodo di una superclasse". Se poi **non lo fa**, il compilatore segnala un errore.

```java
class Studente extends Persona {
    private int matricola;

    public Studente(String nome, int matricola) {
        super(nome);
        this.matricola = matricola;
    }

    @Override                                           // il compilatore controlla che si riscriva davvero
    public void scrivi() {
        System.out.println("Nome: " + getNome());
        System.out.println("Matricola: " + matricola);
    }
}
```

> [!NOTE]
> **Approfondimento esterno — `java.lang.Override`**
> La Javadoc la presenta come un'*annotation interface* con `@Target(METHOD)` e `@Retention(SOURCE)`: si applica solo ai metodi e resta nel codice sorgente, senza finire nel bytecode compilato. Dice che essa "indicates that a method declaration is intended to override a method declaration in a supertype" e che, se un metodo è annotato così, "compilers are required to generate an error message unless" il metodo riscrive o implementa davvero un metodo di una supertype, oppure ha una firma equivalente a quella di un metodo pubblico dichiarato in `Object`.
>
> *Fonte:* [java.lang.Override (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Override.html)

Vediamo che cosa cambia con un refuso:

> [!CAUTION]
> **Errore tipico — Una riscrittura sbagliata che il compilatore non vede**
> ```java
> class Studente extends Persona {
>     @Override
>     public void scrivii() {                       // ERRORE: nome sbagliato, non riscrive niente
>         System.out.println("Nome: " + getNome());
>     }
> }
> ```
> Senza `@Override` questo codice compilerebbe, e `s.scrivi()` stamperebbe la versione di `Persona`. Con `@Override` il compilatore segnala `method does not override or implement a method from a supertype`, sulla riga dell'annotazione. Forma corretta: il nome e i parametri identici a quelli della superclasse, `public void scrivi()`.

`@Override` **non è obbligatoria**: il programma funziona anche senza. Conviene però scriverla ogni volta che si riscrive un metodo, perché trasforma un errore silenzioso (output sbagliato, nessun messaggio) in un errore di compilazione con un messaggio chiaro. Non contraddice nessuna traccia: la traccia chiede le firme, non l'assenza di annotazioni.

### 9.4.3 Richiamare la versione della superclasse: `super.metodo()`

Nella nostra `Studente`, `scrivi` ripete la riga `Nome: ...` che `Persona.scrivi` già stampa. Se un giorno il formato del nome cambiasse in `Persona`, bisognerebbe ricordarsi di cambiarlo anche qui. Meglio **riusare** la versione della superclasse: la parola `super` seguita da un punto e dal nome del metodo richiama la versione **della superclasse**, anche se la sottoclasse l'ha riscritta.

```java
class Studente extends Persona {
    private int matricola;

    public Studente(String nome, int matricola) {
        super(nome);
        this.matricola = matricola;
    }

    public int getMatricola() {
        return matricola;
    }

    @Override
    public void scrivi() {
        super.scrivi();                                 // la versione di Persona: stampa il nome
        System.out.println("Matricola: " + matricola);  // e poi ciò che aggiunge Studente
    }
}

class Tesista extends Studente {
    private String titoloTesi;

    public Tesista(String nome, int matricola, String titoloTesi) {
        super(nome, matricola);
        this.titoloTesi = titoloTesi;
    }

    @Override
    public void scrivi() {
        super.scrivi();                                 // la versione di Studente (che a sua volta chiama Persona)
        System.out.println("Tesi: " + titoloTesi);
    }
}

public class ProvaSuper {
    public static void main(String[] args) {
        Tesista t = new Tesista("Paolo Serra", 4002, "Reti di sensori");
        t.scrivi();
    }
}
```

```text
Nome: Paolo Serra
Matricola: 4002
Tesi: Reti di sensori
```

`t.scrivi()` esegue la versione di `Tesista`. La sua prima istruzione, `super.scrivi()`, esegue la versione di `Studente`; la prima istruzione di questa, `super.scrivi()`, esegue quella di `Persona`. Le tre stampe escono dalla più lontana alla più vicina, perché ogni livello prima chiede al livello sopra di fare il suo e poi aggiunge il proprio. Ogni versione dice **solo** ciò che è specifico della propria classe: è il modo corretto di riscrivere un metodo quando la nuova versione *aggiunge* qualcosa a quella vecchia.

Abbiamo ora due usi di `super`, da non confondere:

| Forma | Dove si scrive | Che cosa fa |
|---|---|---|
| `super(argomenti);` | prima istruzione di un **costruttore** | richiama un costruttore della superclasse (sezione 9.3) |
| `super.metodo(argomenti)` | in un **metodo** | richiama la versione della superclasse di un metodo riscritto (sezione 9.4.3) |

Un'insidia vicina: se nel metodo `scrivi` di `Studente` si scrivesse `scrivi();` senza `super.`, il metodo chiamerebbe **se stesso**, all'infinito (Capitolo 6, sezione 6.9: una ricorsione senza caso base). Il programma terminerebbe con una `StackOverflowError`. Il prefisso `super.` è proprio ciò che dice "non questa versione, quella di sopra".

### 9.4.4 Overriding e overloading

I due termini si somigliano e si confondono in continuazione; una domanda sulla loro differenza compare in ogni esame orale. L'**overloading** (Capitolo 6, sezione 6.7) è la presenza di più metodi con lo **stesso nome e parametri diversi**; l'**overriding** è la riscrittura, in una sottoclasse, di un metodo ereditato con **la stessa firma**. Un esempio che li mostra insieme:

```java
class Studente extends Persona {
    private int matricola;

    public Studente(String nome, int matricola) {
        super(nome);
        this.matricola = matricola;
    }

    @Override
    public void scrivi() {                              // OVERRIDING: stessa firma di Persona.scrivi()
        super.scrivi();
        System.out.println("Matricola: " + matricola);
    }

    public void scrivi(String intestazione) {           // OVERLOADING: stesso nome, parametro diverso
        System.out.println(intestazione);
        scrivi();                                       // quello senza parametri, cioè quello riscritto sopra
    }
}

public class ProvaOverload {
    public static void main(String[] args) {
        Studente s = new Studente("Luisa Conti", 4001);

        s.scrivi();
        s.scrivi("--- Scheda ---");
    }
}
```

```text
Nome: Luisa Conti
Matricola: 4001
--- Scheda ---
Nome: Luisa Conti
Matricola: 4001
```

Dentro `Studente` convivono due metodi `scrivi`: quello senza parametri, che **sostituisce** (per gli studenti) quello di `Persona`, e quello con un parametro `String`, che si **aggiunge**. Nessuno dei due nasconde l'altro: la chiamata `s.scrivi()` sceglie il primo, `s.scrivi("...")` il secondo, guardando gli argomenti. Un metodo in overloading può anche stare **tra superclasse e sottoclasse**: `Studente.scrivi(String)` è un overload del `scrivi()` ereditato da `Persona`, pur essendo in classi diverse.

| | Overloading | Overriding |
|---|---|---|
| Dove | stessa classe (o classe e suoi antenati) | sottoclasse che riscrive un metodo ereditato |
| Firma | stesso nome, **parametri diversi** | **stessa firma** |
| Annotazione | nessuna | `@Override` |
| Quale metodo viene eseguito | lo sceglie il **compilatore**, a tempo di compilazione, dai tipi con cui sono *dichiarati* gli argomenti | lo sceglie la **JVM**, a tempo di esecuzione, dalla classe dell'*oggetto* (sezione 9.6) |

> [!CAUTION]
> **Errore tipico — `@Overload` non esiste**
> ```java
> class Calcolo {
>     @Overload                                     // ERRORE: nessuna annotazione si chiama così
>     public int somma(int a, int b, int c) {
>         return a + b + c;
>     }
> }
> ```
> Il compilatore risponde `cannot find symbol` con `symbol: class Overload`. Per i metodi in overloading **non c'è alcuna annotazione**: si riconoscono solo dalla firma, cioè dai parametri diversi. `@Override` serve per un'altra cosa, riscrivere un metodo della superclasse, e non ha una gemella.

### 9.4.5 La visibilità di un metodo riscritto

C'è una regola che il compilatore applica e che chi non la conosce incontra con frequenza: una riscrittura **non può essere meno accessibile** dell'originale. Se in `Persona` `scrivi` è `public`, in `Studente` non può essere dichiarato senza modificatore (livello di package) né `private`.

> [!CAUTION]
> **Errore tipico — Riscrivere un metodo pubblico senza `public`**
> ```java
> class Studente extends Persona {
>     @Override
>     void scrivi() {                               // ERRORE: manca public
>         System.out.println("Studente");
>     }
> }
> ```
> Il compilatore segnala `scrivi() in Studente cannot override scrivi() in Persona; attempting to assign weaker access privileges; was public`. La riscrittura può **allargare** l'accesso (da `protected` a `public`) ma non restringerlo. Forma corretta: `public void scrivi()`.

La regola ha una conseguenza pratica per i metodi di `Object` che si riscrivono quasi sempre (sezione 9.7): sono dichiarati `public`, quindi anche la riscrittura deve esserlo. Chi scrive `String toString()` senza `public` ottiene proprio questo errore. Vale anche per i metodi che una classe realizza per conto di un'interfaccia (Capitolo 10), compreso il `run` di `Runnable`: i metodi di un'interfaccia sono pubblici, e la loro realizzazione deve esserlo.

### 9.4.6 `final` davanti a metodi e classi

Nel Capitolo 7 (sezione 7.4.2) abbiamo usato `final` su un campo, per impedire che cambi. Davanti a un **metodo** `final` impedisce di **riscriverlo** in una sottoclasse; davanti a una **classe** impedisce di **estenderla**. Sono il modo di dire "su questa parte non si deve poter intervenire".

```java
class Contatore {
    private int valore;

    public void incrementa() {
        valore = valore + 1;
    }

    public final int getValore() {                      // final: nessuna sottoclasse può riscriverlo
        return valore;
    }
}

class ContatorePasso2 extends Contatore {
    @Override
    public void incrementa() {                          // incrementa non è final: si può riscrivere
        super.incrementa();
        super.incrementa();
    }
}

public class ProvaFinal {
    public static void main(String[] args) {
        ContatorePasso2 c = new ContatorePasso2();
        c.incrementa();
        c.incrementa();
        System.out.println(c.getValore());               // getValore è quello ereditato, senza modifiche
    }
}
```

```text
4
```

`ContatorePasso2` riscrive `incrementa` per fare due passi alla volta e usa `getValore` così com'è. Se provasse a riscrivere `getValore`, il compilatore direbbe `getValore() in ContatorePasso2 cannot override getValore() in Contatore; overridden method is final`; se qualcuno provasse a scrivere `class Altro extends X` con `X` dichiarata `final class X`, direbbe `cannot inherit from final X`.

> [!NOTE]
> **Approfondimento esterno — `final` nelle API di Java**
> Nella Javadoc si vede lo stesso modificatore usato per bloccare l'ereditarietà. Il metodo `Object.getClass()` è dichiarato `public final Class<?> getClass()`, e quindi nessuna classe può riscriverlo (lo useremo nella sezione 9.7). La classe `java.lang.String` è dichiarata `public final class String extends Object`, e per questo nessuno può scrivere una sottoclasse di `String`.
>
> *Fonte:* [java.lang.Object#getClass (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#getClass()) e [java.lang.String (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html)

Per le prove scritte `final` su metodi e classi compare di rado; è utile saperlo riconoscere quando lo si incontra in codice fornito dalla traccia, perché mette dei paletti precisi a ciò che si può riscrivere.

## 9.5 Compatibilità di tipo: "è un" e "ha un"

Nelle prossime sezioni usiamo la gerarchia completata nella sezione 9.4.3: `Persona`, `Studente` e `Tesista`, ciascuna con il proprio `scrivi`.

### 9.5.1 Uno `Studente` è una `Persona`

La parola "estende" ha un significato che va oltre il risparmio di codice: la sottoclasse **è un caso particolare** della superclasse. Uno `Studente` *è una* `Persona`; un `Tesista` *è uno* `Studente`, e quindi anche una `Persona`. Java lo prende alla lettera: **un oggetto di una classe derivata può essere usato dove si aspetta un oggetto di una qualunque classe antenata**. Si può assegnare a una variabile `Persona` e passare a un metodo che chiede una `Persona`, senza nessuna conversione scritta.

```java
public class ProvaCompatibilita {
    public static void main(String[] args) {
        Persona p = new Studente("Luisa Conti", 4001);                    // uno Studente è una Persona
        Persona q = new Tesista("Paolo Serra", 4002, "Reti di sensori");  // un Tesista è una Persona
        Studente s = new Tesista("Anna Verdi", 4003, "Basi di dati");     // un Tesista è uno Studente
        Studente r = new Studente("Luisa Conti", 4009);

        System.out.println(p.getNome());
        System.out.println(q.getNome());
        System.out.println(s.getMatricola());
        System.out.println(p.haLoStessoNome(r));    // r è uno Studente, il parametro è una Persona
    }
}
```

```text
Luisa Conti
Paolo Serra
4003
true
```

Le prime tre assegnazioni mettono a sinistra una variabile di un tipo più generale e a destra un oggetto di un tipo più specifico, e il compilatore le accetta. L'ultima riga passa a `haLoStessoNome(Persona altra)` uno `Studente`: ugualmente legittima. Si noti che questo **non è un cast**, cioè una conversione di tipo come quelle del Capitolo 2 (sezione 2.6): l'oggetto non viene trasformato in niente, resta quello che è, e semplicemente lo si guarda attraverso una variabile di un tipo più ampio. Il verso inverso (dalla variabile generale a quella specifica) richiede invece un'operazione esplicita, la sezione 9.5.3.

### 9.5.2 Due tipi: quello della variabile e quello dell'oggetto

Da questo momento una situazione come `Persona p = new Studente(...)` ha **due tipi in gioco**, e distinguerli è la chiave dell'intero polimorfismo:

- il **tipo dichiarato** della variabile, qui `Persona`, che si legge nel codice a sinistra del nome;
- la **classe dell'oggetto**, qui `Studente`, quella scritta dopo `new`.

```text
   stack                           heap
  +-------+                  +-------------------------+
  |   p   |----------------->| oggetto Studente        |
  +-------+                  |   nome      = "Luisa"   |
  tipo dichiarato: Persona   |   matricola = 4001      |
                             +-------------------------+
                             classe dell'oggetto: Studente
```

Il compilatore lavora **soltanto** sul tipo dichiarato. Quando controlla `p.qualcosa()`, si chiede: "la classe `Persona` ha un metodo `qualcosa`?". Che l'oggetto, in esecuzione, sarà in realtà uno `Studente`, per lui non esiste: il compilatore non esegue il programma.

> [!CAUTION]
> **Errore tipico — Chiamare un metodo della sottoclasse attraverso una variabile della superclasse**
> ```java
> Persona p = new Studente("Luisa Conti", 4001);
> System.out.println(p.getMatricola());         // ERRORE: Persona non ha getMatricola
> ```
> Il compilatore risponde `cannot find symbol`, con `symbol: method getMatricola()` e `location: variable p of type Persona`. L'oggetto ha la matricola, ma il tipo della variabile non permette di chiederla. Forma corretta: dichiarare la variabile `Studente`, oppure fare un cast (sezione 9.5.3).

> [!TIP]
> **Intuizione — Il telecomando e l'apparecchio**
> La variabile è un telecomando, l'oggetto è l'apparecchio. Il telecomando ha i pulsanti del *suo* tipo (`Persona`: `scrivi`, `getNome`, `setNome`...): non si può premere un pulsante che non c'è, nemmeno se l'apparecchio ne ha di più. Ma quando si preme "scrivi", ciò che avviene lo decide l'apparecchio, che è uno `Studente`. Le due metà della regola, **che cosa si può chiamare** (decide il tipo della variabile) e **che cosa succede** (decide l'oggetto), sono il tema della sezione 9.6. L'analogia ha un limite: un telecomando vero dialoga con un solo apparecchio, mentre la stessa variabile Java può, una riga dopo, indicarne un altro.

### 9.5.3 Tornare indietro: il cast verso il basso

Se si ha una variabile `Persona` e si sa che l'oggetto è uno `Studente`, per usare i suoi metodi propri bisogna dichiararlo con un **cast verso il basso** (*downcast*): il tipo tra parentesi davanti all'espressione, come per i cast numerici. Il compilatore non può sapere che l'oggetto è proprio uno `Studente`, quindi non lo concede da solo.

```java
public class ProvaCast {
    public static void main(String[] args) {
        Persona p = new Studente("Luisa Conti", 4001);

        Studente s = (Studente) p;                   // cast verso il basso: ora la variabile è di tipo Studente
        System.out.println(s.getMatricola());

        System.out.println(((Studente) p).getMatricola());   // cast senza variabile in più
    }
}
```

```text
4001
4001
```

Nella seconda forma le parentesi attorno a `(Studente) p` sono necessarie: il punto lega più forte del cast, e `(Studente) p.getMatricola()` significherebbe "il cast del risultato di `p.getMatricola()`", che non esiste. Senza il cast la prima assegnazione non compila: `Studente s = p;` dà `incompatible types: Persona cannot be converted to Studente`, **anche se** l'oggetto è proprio uno studente, perché il compilatore guarda soltanto il tipo dichiarato.

Il cast, però, è una promessa che viene verificata in esecuzione. Se l'oggetto **non** è dello tipo promesso, il programma si interrompe.

```java
public class ProvaCastSbagliato {
    public static void main(String[] args) {
        Persona q = new Persona("Anna Verdi");       // un oggetto Persona, non uno Studente

        Studente z = (Studente) q;                   // compila: il compilatore non guarda l'oggetto
        System.out.println(z.getMatricola());        // non si arriva qui
    }
}
```

```text
Exception in thread "main" java.lang.ClassCastException: class Persona cannot be cast to class Studente (Persona and Studente are in unnamed module of loader 'app')
	at ProvaCastSbagliato.main(ProvaCastSbagliato.java:5)
```

> [!NOTE]
> **Approfondimento esterno — `ClassCastException`**
> La Javadoc la descrive come l'eccezione "thrown to indicate that the code has attempted to cast an object to a subclass of which it is not an instance". È un'eccezione **non controllata** (`extends RuntimeException`): il compilatore non obbliga né a dichiararla né a gestirla (Capitolo 13).
>
> *Fonte:* [java.lang.ClassCastException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/ClassCastException.html)

Il cast verso il basso è dunque uno strumento da usare **con motivo**: serve quando davvero si deve dare una forma più specifica a un oggetto già noto, e quando se ne è certi. Nella maggior parte dei casi in cui si è tentati di usarlo c'è una soluzione migliore, che è il polimorfismo (sezione 9.6): invece di chiedersi di che sottoclasse è l'oggetto per scegliere che cosa fare, si chiama un metodo riscritto e si lascia scegliere all'oggetto. Un caso in cui il cast è invece corretto e necessario è `equals(Object)` (sezione 9.7.3).

### 9.5.4 "È un" contro "ha un"

L'ereditarietà esprime la relazione **"è un"** (*is-a*): `Studente` è una `Persona`. Esiste un'altra relazione tra classi, molto frequente, che non si scrive con `extends`: la relazione **"ha un"** (*has-a*), in cui una classe contiene, come **campo**, un oggetto di un'altra classe. Nel Capitolo 7 (sezione 7.3.7) un `Segmento` aveva due `Punto`: un segmento non è un punto, *ha* due punti.

```java
class Motore {
    private int cavalli;

    public Motore(int cavalli) {
        this.cavalli = cavalli;
    }

    public int getCavalli() {
        return cavalli;
    }
}

class Automobile {
    private Motore motore;                    // ha-un: un campo il cui tipo è un'altra classe

    public Automobile(int cavalli) {
        motore = new Motore(cavalli);
    }

    public int getCavalli() {
        return motore.getCavalli();
    }
}

public class ProvaHaUn {
    public static void main(String[] args) {
        Automobile a = new Automobile(90);
        System.out.println(a.getCavalli());
    }
}
```

```text
90
```

Per scegliere tra le due strade basta una frase di controllo: se "X è un Y" suona naturale, `X extends Y`; se suona naturale "X ha un Y", `Y` è un campo di `X`. "Un'automobile è un motore" non ha senso, e `class Automobile extends Motore` la renderebbe utilizzabile in ogni punto in cui si aspetta un motore. Usare `extends` per una relazione "ha un" è un errore di progetto, e spesso anche di compilazione (si veda la nota sulle classi annidate nel [Capitolo 11](11-classi-annidate.md)).

## 9.6 Polimorfismo e binding dinamico

### 9.6.1 Il problema: una variabile, tanti comportamenti

Mettiamo insieme le due idee della sezione precedente: una variabile di una classe base può indicare oggetti di classi derivate, e le classi derivate possono riscrivere i metodi. Costruiamo un array di `Persona` e riempiamolo con oggetti diversi: una persona, uno studente, un tesista.

```java
public class ProvaPolimorfismo {
    public static void main(String[] args) {
        Persona[] gruppo = new Persona[3];
        gruppo[0] = new Persona("Anna Verdi");
        gruppo[1] = new Studente("Luisa Conti", 4001);
        gruppo[2] = new Tesista("Paolo Serra", 4002, "Reti di sensori");

        for (int i = 0; i < gruppo.length; i++) {
            gruppo[i].scrivi();                      // la stessa istruzione, in tre iterazioni
            System.out.println("-----");
        }
    }
}
```

```text
Nome: Anna Verdi
-----
Nome: Luisa Conti
Matricola: 4001
-----
Nome: Paolo Serra
Matricola: 4002
Tesi: Reti di sensori
-----
```

Il tipo dichiarato di ogni casella è `Persona` (l'array si chiama **array polimorfico**: il contenitore è generico, il contenuto è specifico). L'istruzione `gruppo[i].scrivi()` è una sola, ma nella prima iterazione esegue il `scrivi` di `Persona`, nella seconda quello di `Studente`, nella terza quello di `Tesista`. La domanda che il compilatore non può risolvere è: *quale versione di `scrivi`?*

### 9.6.2 La risposta: binding dinamico

La risposta sta nell'**oggetto**. Quando si chiama un metodo riscritto, viene eseguita la versione della classe con cui l'oggetto è stato **creato con `new`**, non quella del tipo della variabile che lo indica. Poiché la classe dell'oggetto si conosce solo quando il programma gira (nell'array, ogni casella può contenere un oggetto diverso, e quale lo decide il programma mentre procede), la scelta avviene **a tempo di esecuzione**. Questo meccanismo si chiama **binding dinamico** o **late binding** (*associazione tardiva*): il legame tra la chiamata e il codice da eseguire viene fatto tardi, quando l'oggetto è noto.

> [!NOTE]
> **Definizione — Polimorfismo e binding dinamico**
> Il **polimorfismo** ("molte forme") è la possibilità di usare, dove si aspetta un oggetto di una classe, un oggetto di una sua sottoclasse, ciascuno col proprio comportamento. Il **binding dinamico** è il meccanismo che lo rende possibile: quando si chiama un metodo riscritto, la versione eseguita è quella della classe dell'oggetto (la classe usata con `new`), scelta dalla JVM **a tempo di esecuzione**, indipendentemente dal tipo della variabile.

Lo stesso accade se è la **stessa variabile** a cambiare oggetto.

```java
public class ProvaVariabile {
    public static void main(String[] args) {
        Persona p = new Persona("Anna Verdi");
        p.scrivi();
        System.out.println("-----");

        p = new Studente("Luisa Conti", 4001);       // la stessa variabile, un altro oggetto
        p.scrivi();                                  // il tipo dichiarato non è cambiato, il comportamento sì
    }
}
```

```text
Nome: Anna Verdi
-----
Nome: Luisa Conti
Matricola: 4001
```

Il tipo dichiarato di `p` è `Persona` per tutto il programma. A cambiare, alla riga con `new Studente(...)`, è l'oggetto indicato (si ricordi il Capitolo 8: riassegnare una variabile sposta la freccia verso un altro oggetto), e con l'oggetto cambia la versione di `scrivi` che parte.

### 9.6.3 Un metodo che ne chiama un altro, riscritto

Il binding dinamico ha una conseguenza che sorprende alla prima lettura. Un metodo della classe base può chiamare un altro metodo **che le sottoclassi riscrivono**, e a ogni chiamata partirà la versione giusta, **anche se il metodo della classe base è stato scritto, e compilato, senza conoscere nessuna sottoclasse**. Ecco un annuncio: `mostra` stampa una cornice e, in mezzo, il testo restituito da `testo`. Le sottoclassi riscrivono solo `testo`.

```java
class Annuncio {
    public String testo() {
        return "(nessun testo)";
    }

    public void mostra() {
        System.out.println("+----------+");
        System.out.println(testo());                 // quale testo()? Dipende dall'oggetto
        System.out.println("+----------+");
    }
}

class Benvenuto extends Annuncio {
    @Override
    public String testo() {
        return "Benvenuti!";
    }
}

class Chiusura extends Annuncio {
    @Override
    public String testo() {
        return "Si chiude alle 18";
    }
}

public class ProvaAnnunci {
    public static void main(String[] args) {
        Annuncio[] bacheca = { new Benvenuto(), new Chiusura(), new Annuncio() };

        for (Annuncio a : bacheca) {
            a.mostra();
        }
    }
}
```

```text
+----------+
Benvenuti!
+----------+
+----------+
Si chiude alle 18
+----------+
+----------+
(nessun testo)
+----------+
```

`mostra` è scritto una volta sola, in `Annuncio`, e non la riscrive nessuno. Dentro, la chiamata `testo()` è in realtà `this.testo()`, e `this` è l'oggetto su cui `mostra` è stato chiamato: per un `Benvenuto` è un `Benvenuto`, quindi parte la sua versione di `testo`. La classe `Annuncio` potrebbe essere compilata oggi e una nuova sottoclasse `Avviso` scritta il mese prossimo, senza che `mostra` si debba cambiare: la scelta del codice si fa all'ultimo momento, quando `mostra` gira.

Quando una versione "di riserva" come `testo()` della classe base non ha senso e si vuole che **ogni** sottoclasse la fornisca, la classe base la dichiara `abstract` e non scrive nessun corpo: è il tema del [Capitolo 10 — Classi astratte e interfacce](10-classi-astratte-e-interfacce.md).

### 9.6.4 Che cosa decide il compilatore e che cosa decide la JVM

Mettiamo insieme le due metà. Il compilatore e la JVM prendono decisioni diverse, guardando cose diverse:

| Chi decide | Quando | Guarda | Decide |
|---|---|---|---|
| Il **compilatore** | a tempo di compilazione | il tipo **dichiarato** delle variabili | se il metodo si può chiamare (il metodo esiste nel tipo dichiarato); quale tra più metodi in *overloading* usare |
| La **JVM** | a tempo di esecuzione | la **classe dell'oggetto** | quale versione di un metodo *riscritto* eseguire |

L'overloading è un'altra faccia dello stesso fatto. Con due metodi con lo stesso nome e parametri diversi, la scelta è del compilatore ed è fatta guardando il **tipo dichiarato** degli argomenti:

```java
class Stampante {
    public void stampa(Object o) {
        System.out.println("stampa(Object)");
    }

    public void stampa(String s) {
        System.out.println("stampa(String)");
    }
}

public class ProvaScelta {
    public static void main(String[] args) {
        Stampante st = new Stampante();
        Object o = "ciao";                           // dichiarato Object, contiene una stringa

        st.stampa("ciao");                           // argomento di tipo String
        st.stampa(o);                                // argomento dichiarato Object
        System.out.println(o.toString());            // toString è riscritto in String
    }
}
```

```text
stampa(String)
stampa(Object)
ciao
```

Alla seconda chiamata l'oggetto è una stringa, ma `stampa` non è riscritto: è in overloading, e il compilatore ha scelto `stampa(Object)` guardando il tipo dichiarato di `o`. L'ultima riga mostra il caso opposto: `toString` è **riscritto** da `String`, quindi la JVM esegue la versione di `String` anche se la variabile è `Object`, e si legge `ciao` (non una sigla del tipo `java.lang.String@...`). È lo stesso fenomeno che nel Capitolo 8 (sezione 8.4.3) rendeva `equals(Specie)` e `equals(Object)` due metodi diversi: il primo è un overload e lo sceglie il compilatore sul tipo dichiarato; il secondo, scritto con la firma di `Object`, è una riscrittura e lo sceglie la JVM.

### 9.6.5 A che cosa serve

Il polimorfismo permette di scrivere codice **che funziona per tutte le sottoclassi, anche per quelle che ancora non esistono**.

```java
public class ProvaGenerico {
    static void presenta(Persona p) {                // accetta qualunque Persona, e quindi qualunque sottoclasse
        System.out.println("Benvenuto/a:");
        p.scrivi();
    }

    public static void main(String[] args) {
        presenta(new Persona("Anna Verdi"));
        presenta(new Tesista("Paolo Serra", 4002, "Reti di sensori"));
    }
}
```

```text
Benvenuto/a:
Nome: Anna Verdi
Benvenuto/a:
Nome: Paolo Serra
Matricola: 4002
Tesi: Reti di sensori
```

`presenta` conosce solo `Persona` e non ha bisogno di sapere altro. Se in futuro si aggiunge una classe `Dottorando extends Studente` con un suo `scrivi`, `presenta` la gestirà senza nessuna modifica: eseguirà il `scrivi` del dottorando. Un programma senza polimorfismo, per ogni nuova classe, avrebbe una catena di `if` da aggiornare in tutti i punti in cui si distinguono i tipi.

## 9.7 La classe `Object`

### 9.7.1 L'antenata di tutte le classi

Abbiamo detto che ogni classe ha una sola superclasse, ma le nostre classi `Persona`, `Motore`, `Stampante` non hanno nessuna clausola `extends`: sembrerebbe che non abbiano superclasse. In realtà una classe **senza `extends` estende implicitamente `Object`**, una classe della libreria standard (nel package `java.lang`, importato sempre, Capitolo 7, sezione 7.6.2). Scrivere `class Persona` equivale a scrivere `class Persona extends Object`. Così ogni gerarchia, risalendo, finisce in `Object`: la gerarchia di `Tesista` è `Tesista`, `Studente`, `Persona`, `Object`.

> [!NOTE]
> **Approfondimento esterno — `java.lang.Object`**
> La Javadoc la presenta così: "Class `Object` is the root of the class hierarchy. Every class has `Object` as a superclass. All objects, including arrays, implement the methods of this class."
>
> *Fonte:* [java.lang.Object (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html)

Le conseguenze sono tre. La prima: **ogni oggetto ha i metodi di `Object`**, e le nostre classi li ereditano senza scriverli (`toString`, `equals`, `hashCode`, `getClass`, e altri che incontreremo con i thread). La seconda: per la compatibilità di tipo della sezione 9.5.1, **una variabile `Object` può indicare un oggetto di qualunque classe**, e anche un array. La terza: un metodo che dichiara un parametro di tipo `Object` accetta argomenti di qualsiasi tipo; è il caso di `System.out.println(Object)`.

```java
public class ProvaObject {
    public static void main(String[] args) {
        Object o = new Studente("Luisa Conti", 4001);
        System.out.println(o.getClass().getName());     // il nome della classe dell'oggetto

        o = "una stringa";                              // la stessa variabile può indicare una stringa
        System.out.println(o.getClass().getName());

        o = 42;                                         // e anche un intero (come Integer, Capitolo 6)
        System.out.println(o.getClass().getName());
    }
}
```

```text
Studente
java.lang.String
java.lang.Integer
```

`getClass()` è un metodo ereditato da `Object` che restituisce un oggetto di tipo `Class`, il quale rappresenta la classe dell'oggetto; `getName()` ne dà il nome. È dichiarato `public final Class<?> getClass()`: `final` (sezione 9.4.6) e quindi non riscrivibile.

Con una variabile `Object` valgono le regole della sezione 9.5.2: si possono chiamare **solo** i metodi di `Object`. Scrivere `o.scrivi()` non compila, perché `Object` non ha un metodo `scrivi`.

### 9.7.2 `toString`: come si stampa un oggetto

Il metodo `toString()`, che già conosciamo dal Capitolo 7 (sezione 7.7), restituisce una `String` che rappresenta l'oggetto. La versione di `Object` non conosce i campi delle nostre classi: restituisce il nome della classe, una `@` e un numero in esadecimale (qualcosa come `Studente@1b6d3586`), che non dice niente di utile. La Javadoc raccomanda che ogni classe lo riscriva.

> [!NOTE]
> **Approfondimento esterno — `Object.toString`**
> La Javadoc dichiara `public String toString()` e dice che restituisce "a string representation of the object". Nella nota d'uso precisa che il risultato dovrebbe essere "a concise but informative representation that is easy for a person to read" e che "it is recommended that all subclasses override this method". Per `Object` la stringa è `getClass().getName() + '@' + Integer.toHexString(hashCode())`.
>
> *Fonte:* [java.lang.Object#toString (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#toString())

La riscrittura è un normale overriding (sezione 9.4), con una cautela: il metodo **restituisce** la stringa, non la stampa, e deve essere `public` (sezione 9.4.5).

```java
class Persona {
    private String nome;

    public Persona(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }

    @Override
    public String toString() {
        return "Persona[" + nome + "]";              // restituisce, non stampa
    }
}

class Studente extends Persona {
    private int matricola;

    public Studente(String nome, int matricola) {
        super(nome);
        this.matricola = matricola;
    }

    @Override
    public String toString() {
        return "Studente[" + getNome() + ", " + matricola + "]";
    }
}

public class ProvaToString {
    public static void main(String[] args) {
        Persona p = new Persona("Anna Verdi");
        Studente s = new Studente("Luisa Conti", 4001);
        Persona q = new Studente("Paolo Serra", 4002);

        System.out.println(p);                       // println(Object) chiama toString
        System.out.println(s);
        System.out.println("Iscritto: " + s);        // anche la concatenazione la chiama
        System.out.println(q);                       // variabile Persona, oggetto Studente
    }
}
```

```text
Persona[Anna Verdi]
Studente[Luisa Conti, 4001]
Iscritto: Studente[Luisa Conti, 4001]
Studente[Paolo Serra, 4002]
```

Il perché `System.out.println(s)` usa il nostro `toString` è nella Javadoc di `PrintStream.println(Object)`: il metodo "calls at first `String.valueOf(x)` to get the printed object's string value", e `String.valueOf(Object)` restituisce `"null"` se l'argomento è `null` e altrimenti `obj.toString()`. Lo stesso fa la concatenazione `"Iscritto: " + s`. Sono i due punti in cui `toString` viene chiamato **senza che nessuno lo scriva**. L'ultima riga è binding dinamico (sezione 9.6): la variabile `q` è `Persona`, ma l'oggetto è uno `Studente`, e viene eseguito il `toString` di `Studente`.

> [!IMPORTANT]
> **Nota per l'esame — La stringa va scritta al carattere**
> Le tracce che chiedono una "rappresentazione testuale nella forma `Persona[Mario Rossi]`" vogliono esattamente quei caratteri: parentesi quadre, spazi, ordine dei campi. Un test che confronta l'output non perdona uno spazio in più. Altri tre dettagli letterali: il nome del metodo è `toString` con la `S` maiuscola; restituisce una `String` (non è `void`); è `public`.

### 9.7.3 `equals(Object)`: il confronto sul contenuto, in forma definitiva

Nel Capitolo 8 (sezione 8.4.3) abbiamo scritto `equals` con il parametro della classe, `equals(Specie altra)`, e abbiamo visto che quel metodo **non riscrive** quello di `Object`, che ha un parametro `Object`: ne è un overload, e le classi della libreria, che chiamano sempre la versione `Object`, non lo usano. Adesso sappiamo che cosa serve: un'autentica riscrittura, con la firma `public boolean equals(Object obj)`. La Javadoc di `Object.equals` fissa anche che cosa ci si aspetta da un `equals` ben fatto.

> [!NOTE]
> **Approfondimento esterno — Il contratto di `Object.equals`**
> Il metodo è dichiarato `public boolean equals(Object obj)`. La Javadoc dice che implementa una *relazione di equivalenza* sui riferimenti non nulli, cioè che è: **riflessivo** (`x.equals(x)` è `true`), **simmetrico** (`x.equals(y)` è `true` se e solo se `y.equals(x)` lo è), **transitivo** (se `x.equals(y)` e `y.equals(z)`, allora `x.equals(z)`), **coerente** (chiamate ripetute danno lo stesso risultato se i dati confrontati non cambiano). Inoltre, "for any non-null reference value `x`, `x.equals(null)` should return `false`". Nella nota d'uso aggiunge che "it is generally necessary to override the `hashCode` method whenever this method is overridden".
>
> *Fonte:* [java.lang.Object#equals (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#equals(java.lang.Object))

Il parametro è di tipo `Object`: il metodo deve poter ricevere *qualsiasi* oggetto (anche `null`, anche una stringa), e rispondere `false` quando non è del tipo giusto. Prima di leggere i campi bisogna quindi controllare di che oggetto si tratta, e poi **convertirlo** nel tipo della classe con un cast verso il basso (sezione 9.5.3), perché `Object` non ha il campo `popolazione`. Riprendiamo la classe `Specie` del Capitolo 8.

```java
class Specie {
    private String nome;
    private int popolazione;

    public Specie(String nome, int popolazione) {
        this.nome = nome;
        this.popolazione = popolazione;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;                             // 1. lo stesso oggetto: uguale per forza
        }
        if (o == null || getClass() != o.getClass()) {
            return false;                            // 2. niente, oppure un oggetto di un'altra classe
        }
        Specie altra = (Specie) o;                   // 3. ora il cast è sicuro
        return nome.equals(altra.nome)               // 4. campo String: equals
            && popolazione == altra.popolazione;     //    campo int: ==
    }
}

public class ProvaEqualsObject {
    public static void main(String[] args) {
        Specie a = new Specie("Lupo", 40);
        Specie b = new Specie("Lupo", 40);
        Specie c = new Specie("Orso", 40);
        Object o = new Specie("Lupo", 40);           // stessa cosa, ma vista come Object

        System.out.println(a == b);
        System.out.println(a.equals(b));
        System.out.println(a.equals(c));
        System.out.println(a.equals(null));
        System.out.println(a.equals(o));             // ora funziona anche con la variabile Object
        System.out.println(a.equals("Lupo"));        // un'altra classe: false, nessuna eccezione
    }
}
```

```text
false
true
false
false
true
false
```

Il metodo, riga per riga.

1. `if (this == o) return true;` Se `o` è *lo stesso oggetto* di `this`, il confronto è già deciso: un oggetto è uguale a sé stesso (riflessività). È anche una scorciatoia, che evita di leggere i campi.
2. `o == null || getClass() != o.getClass()` esclude due casi. Se `o` è `null`, la risposta deve essere `false` (e il controllo viene **per primo**: con `||`, se `o` è `null` il secondo operando non viene valutato, e non si rischia una `NullPointerException`, Capitolo 8, sezione 8.3.3). Altrimenti si confronta la classe dell'oggetto corrente con quella di `o`: `getClass()` (sezione 9.7.1) restituisce l'oggetto che rappresenta la classe, e due oggetti della stessa classe ne restituiscono lo stesso. Se differiscono (per esempio `o` è una `String`), la risposta è `false`.
3. `Specie altra = (Specie) o;` A questo punto sappiamo che `o` è una `Specie`, e il cast non può fallire. Serve per poter scrivere `altra.nome`: attraverso una variabile `Object` non si potrebbero leggere i campi.
4. L'ultima riga confronta i campi come nel Capitolo 8: `==` per i primitivi, `equals` per i riferimenti (`String`). Anche qui `nome` è leggibile da `altra.nome` perché `private` limita l'accesso al codice della classe, non al singolo oggetto (Capitolo 7, sezione 7.1.7).

Il risultato è una vera riscrittura: l'ultima chiamata del `main` con la variabile `Object` ora dà `true`, che con la versione del Capitolo 8 dava `false`.

> [!WARNING]
> **Attenzione — `instanceof` e `Objects.equals`**
> Il controllo della classe al punto 2 si può fare anche con l'operatore `instanceof`, che ammette anche gli oggetti delle sottoclassi; in questi appunti non lo trattiamo, e la forma con `getClass()` è quella da ricordare. Se un campo di tipo riferimento può essere `null`, `nome.equals(...)` lancia una `NullPointerException`: la classe `java.util.Objects` ha un metodo statico `equals(Object a, Object b)` che accetta anche `null` (la Javadoc dice che se entrambi gli argomenti sono `null` restituisce `true`, altrimenti chiama `a.equals(b)` quando `a` non è `null`). Per i campi che non possono essere `null`, come negli esempi, basta `equals` diretto.

### 9.7.4 `hashCode`: va riscritto insieme a `equals`

`Object` ha un altro metodo che entra in gioco ogni volta che si riscrive `equals`: `public int hashCode()`, che restituisce un numero intero associato all'oggetto, il suo **codice hash** (*hash code*). Serve alle strutture dati che organizzano gli oggetti per codice, come `HashMap` e `HashSet` (Capitolo 12); la Javadoc dice appunto che il metodo "is supported for the benefit of hash tables such as those provided by `HashMap`". Il numero non è importante in sé: conta la regola che lo lega a `equals`.

> [!NOTE]
> **Approfondimento esterno — Il contratto di `Object.hashCode`**
> La Javadoc stabilisce tra l'altro: "if two objects are equal according to the `equals` method, then calling the `hashCode` method on each of the two objects must produce the same integer result". Non vale l'inverso: oggetti diversi possono avere lo stesso codice (non è richiesto che ne abbiano di distinti, ma "may improve the performance of hash tables"). La versione di `Object` restituisce, per quanto praticabile, interi distinti per oggetti distinti.
>
> *Fonte:* [java.lang.Object#hashCode (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#hashCode())

Conseguenza: se una classe riscrive `equals`, due oggetti con lo stesso contenuto diventano "uguali", e **devono** quindi dare lo stesso `hashCode`. Quello di `Object`, che dipende dall'identità, darebbe due numeri diversi: contratto violato. Per scrivere `hashCode` si usano **gli stessi campi** di `equals`, e il modo più rapido è il metodo `Objects.hash`.

> [!NOTE]
> **Approfondimento esterno — `Objects.hash`**
> La classe `java.util.Objects` dichiara `public static int hash(Object... values)` ("generates a hash code for a sequence of input values", cioè una sequenza di valori di numero qualsiasi, indicata con `Object...`). La Javadoc dice che è utile "for implementing `Object.hashCode()` on objects containing multiple fields", con l'esempio `return Objects.hash(x, y, z);`.
>
> *Fonte:* [java.util.Objects#hash (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Objects.html#hash(java.lang.Object...))

```java
import java.util.Objects;

class Specie {
    private String nome;
    private int popolazione;

    public Specie(String nome, int popolazione) {
        this.nome = nome;
        this.popolazione = popolazione;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Specie altra = (Specie) o;
        return nome.equals(altra.nome) && popolazione == altra.popolazione;
    }

    @Override
    public int hashCode() {
        return Objects.hash(nome, popolazione);      // gli stessi campi di equals
    }
}

public class ProvaHashCode {
    public static void main(String[] args) {
        Specie a = new Specie("Lupo", 40);
        Specie b = new Specie("Lupo", 40);

        System.out.println(a.equals(b));
        System.out.println(a.hashCode() == b.hashCode());    // uguali per equals: stesso codice
    }
}
```

```text
true
true
```

L'`import java.util.Objects;` è necessario perché `Objects` non è nel package `java.lang`. `Objects.hash(nome, popolazione)` combina i due valori in un solo intero; il `int` `popolazione` viene convertito in oggetto automaticamente (autoboxing, Capitolo 6, sezione 6.6). Il risultato vale per due oggetti con gli stessi campi, ed è ciò che il contratto richiede.

La regola da portarsi all'esame è corta: **se si riscrive `equals`, si riscrive anche `hashCode`, con gli stessi campi.** Se la traccia chiede soltanto `equals`, aggiungere un `hashCode` coerente non contraddice la richiesta e rende la classe corretta anche per le collezioni.

## Come esce all'esame

**EXAM1 — Esercizio 1 (5 punti), classi astratte e polimorfismo.** La traccia chiedeva di creare una classe astratta `Animale` con un metodo astratto `String verso()`, e due sottoclassi `Cane` e `Gatto` che lo realizzano restituendo rispettivamente `"bau"` e `"miao"`. La parte astratta è nel [Capitolo 10](10-classi-astratte-e-interfacce.md). Di questo capitolo servono: dichiarare le due sottoclassi con `extends` (sezione 9.1.2); scrivere in ciascuna un metodo con **la stessa firma** del metodo della superclasse, cioè lo stesso nome, nessun parametro e tipo di ritorno `String` (sezione 9.4.1), dichiarato `public` perché una riscrittura non può restringere l'accesso (sezione 9.4.5); restituire la stringa con `return`, senza stamparla. Quando poi un programma usa le tre classi attraverso una variabile `Animale`, a decidere quale `verso()` parte è il binding dinamico (sezione 9.6.2). Vincoli letterali: i nomi `Animale`, `Cane`, `Gatto`; il nome e la firma `String verso()`; le due stringhe esatte, in minuscolo.

**EXAM1 — Esercizio 3 (13 punti), ereditarietà, thread e information hiding.** La traccia forniva una classe `Persona` già scritta, con un costruttore `(String nome, String cognome)`, e chiedeva una sottoclasse `Studente` che implementa l'interfaccia `Runnable`, con due costruttori in overload, il primo con `nome`, `cognome`, `matricola` e il secondo con `matricola` (intero) e `cds` (testuale); la riscrittura del metodo `run()`, che eleva la matricola al quadrato e ne sovrascrive il valore; tutte le variabili d'istanza `private` con i relativi `get` e `set`. Il capitolo serve per quattro punti, oltre a quelli del [Capitolo 7](07-classi-e-oggetti.md) (costruttori in overload, campi privati, `get` e `set`). Primo, `Studente` **estende** `Persona` e **implementa** `Runnable` con le due clausole nell'ordine `extends` poi `implements` (sezione 9.1.5). Secondo, `Persona` ha **un solo costruttore, con parametri**: ogni costruttore di `Studente` deve quindi richiamare `super(...)` come prima istruzione, e non farlo è l'errore `constructor Persona in class Persona cannot be applied to given types` (sezioni 9.3.1 e 9.3.2). Terzo, il secondo costruttore non riceve `nome` e `cognome`, ma la chiamata a `super(...)` resta obbligatoria: servono valori da passare (sezione 9.3.4). Quarto, `run()` è la riscrittura di un metodo di interfaccia, e per questo deve essere `public` (sezione 9.4.5); `Runnable` e il corpo di `run` si vedono nei Capitoli 10 e 17. Vincoli letterali: i nomi `Studente`, `matricola`, `cds`; l'**ordine** dei parametri dei due costruttori; `private` su tutti i campi, un `get` e un `set` per ciascuno; `extends Persona` e `implements Runnable`.

## Scheletri da esame

### Una sottoclasse con un campo in più, `super(...)` e un metodo riscritto che riusa quello della superclasse

*Quando si usa:* la traccia chiede una classe che estende un'altra e "ridefinisce" un metodo mantenendone il comportamento di base. Si veda la sezione 9.4.3.

```java
class Veicolo {
    private String targa;

    public Veicolo(String targa) {
        this.targa = targa;
    }

    public String getTarga() {
        return targa;
    }

    public String descrizione() {
        return "Veicolo " + targa;
    }
}

class Furgone extends Veicolo {
    private int portata;                                  // il campo in più

    public Furgone(String targa, int portata) {
        super(targa);                                     // prima istruzione: costruisce la parte Veicolo
        this.portata = portata;
    }

    public int getPortata() {
        return portata;
    }

    public void setPortata(int portata) {
        this.portata = portata;
    }

    @Override
    public String descrizione() {                         // stessa firma, public
        return super.descrizione() + ", portata " + portata;   // versione della superclasse, poi il proprio
    }
}
```

Non servono import né eccezioni. Punti da controllare: `extends` nella riga della classe; `super(...)` come **prima** istruzione del costruttore; i campi della superclasse si leggono con i suoi metodi, mai per nome; `public` nella riscrittura.

### Costruttori in overload, uno senza i dati della superclasse

*Quando si usa:* la superclasse ha un solo costruttore con parametri (spesso fornita già scritta nel file) e la sottoclasse deve avere un costruttore con parametri diversi. Si veda la sezione 9.3.4.

```java
class Attrezzo {
    private String nome;
    private int peso;

    public Attrezzo(String nome, int peso) {
        this.nome = nome;
        this.peso = peso;
    }

    public String getNome() {
        return nome;
    }

    public int getPeso() {
        return peso;
    }
}

class Trapano extends Attrezzo {
    private int giri;
    private int tensione;

    public Trapano(String nome, int peso, int giri) {     // riceve i dati della superclasse
        super(nome, peso);
        this.giri = giri;
        this.tensione = 0;
    }

    public Trapano(int giri, int tensione) {              // non li riceve: valori fissi
        super("generico", 0);                             // la chiamata è obbligatoria comunque
        this.giri = giri;
        this.tensione = tensione;
    }

    public int getGiri() {
        return giri;
    }

    public int getTensione() {
        return tensione;
    }
}
```

Non servono import né eccezioni. Il valore da passare a `super(...)` nel secondo costruttore, se la traccia non lo indica, è una scelta del programmatore; `null` compila ma lascia un campo senza oggetto. L'**ordine** dei parametri di ciascun costruttore è quello scritto nella traccia.

### Una sottoclasse che implementa `Runnable`

*Quando si usa:* la traccia chiede che una sottoclasse di una classe data realizzi anche `Runnable`. Come avviare un thread è nel Capitolo 17; qui conta la forma della classe.

```java
class Sportivo {
    private String nome;

    public Sportivo(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }
}

class Corridore extends Sportivo implements Runnable {   // prima extends, poi implements
    private int giri;

    public Corridore(String nome) {
        super(nome);
        this.giri = 0;
    }

    public int getGiri() {
        return giri;
    }

    public void setGiri(int giri) {
        this.giri = giri;
    }

    @Override
    public void run() {                                   // public, void, nessun parametro: la firma di Runnable
        giri = giri + 1;
    }
}
```

Non servono import (`Runnable` è in `java.lang`) né eccezioni. Il corpo di `run` dipende dalla traccia; la firma no.

### `toString`, `equals(Object)` e `hashCode` di una classe

*Quando si usa:* la traccia chiede una rappresentazione testuale in un formato dato e/o il confronto tra oggetti sul contenuto. Si vedano le sezioni 9.7.2, 9.7.3 e 9.7.4.

```java
import java.util.Objects;

class Corso {
    private String nome;
    private int crediti;

    public Corso(String nome, int crediti) {
        this.nome = nome;
        this.crediti = crediti;
    }

    @Override
    public String toString() {
        return "Corso[" + nome + ", " + crediti + "]";    // il formato esatto della traccia; return, non println
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;                                  // stesso oggetto
        }
        if (o == null || getClass() != o.getClass()) {
            return false;                                 // null o un'altra classe
        }
        Corso altro = (Corso) o;                          // cast sicuro dopo il controllo
        return nome.equals(altro.nome) && crediti == altro.crediti;
    }

    @Override
    public int hashCode() {
        return Objects.hash(nome, crediti);               // gli stessi campi di equals
    }
}
```

Serve l'`import java.util.Objects;` solo se si scrive `hashCode` con `Objects.hash`. Nessuna eccezione da dichiarare. I tre metodi sono tutti `public`; il parametro di `equals` è **`Object`**, non `Corso`.

### Un array polimorfico e un ciclo che chiama il metodo riscritto

*Quando si usa:* la traccia chiede di tenere insieme oggetti di classi diverse della stessa gerarchia e di far "fare il proprio verso" a ciascuno. Si veda la sezione 9.6.1.

```java
class Strumento {
    public String suona() {
        return "...";
    }
}

class Chitarra extends Strumento {
    @Override
    public String suona() {
        return "pling";
    }
}

class Tamburo extends Strumento {
    @Override
    public String suona() {
        return "bum";
    }
}

public class Orchestra {
    public static void main(String[] args) {
        Strumento[] gruppo = { new Chitarra(), new Tamburo(), new Strumento() };

        for (Strumento s : gruppo) {                      // il tipo della variabile è la superclasse
            System.out.println(s.suona());                // parte la versione dell'oggetto
        }
    }
}
```

```text
pling
bum
...
```

Non servono import né eccezioni. L'array si dichiara del tipo della **superclasse**; nessun cast serve, perché `suona` è già nella superclasse.

## Errori tipici

Alcuni errori sono già discussi nel testo: usare per nome un campo `private` della superclasse (sezione 9.2.1), dimenticare `super(...)` quando la superclasse non ha un costruttore senza argomenti (sezione 9.3.2), un refuso che non riscrive niente (sezione 9.4.2), l'annotazione `@Overload` inesistente (sezione 9.4.4), riscrivere un metodo pubblico senza `public` (sezione 9.4.5), riscrivere con un tipo di ritorno diverso (sezione 9.4.1), chiamare un metodo della sottoclasse attraverso una variabile della superclasse (sezione 9.5.2), assegnare alla variabile specifica senza cast e il `ClassCastException` di un cast sbagliato (sezione 9.5.3), riscrivere un metodo `final` o estendere una classe `final` (sezione 9.4.6), usare `extends` per una relazione "ha un" (sezione 9.5.4). Seguono gli altri.

> [!CAUTION]
> **Errore tipico — `super(...)` non è la prima istruzione**
> ```java
> class Studente extends Persona {
>     private int matricola;
>
>     public Studente(String nome, int matricola) {
>         this.matricola = matricola;           // ERRORE: prima di super(...)
>         super(nome);
>     }
> }
> ```
> Il compilatore risponde `call to super must be first statement in constructor` (con JDK 22 il messaggio è invece `statements before super() is a preview feature and is disabled by default`). Può comparire anche un secondo errore, `constructor Persona in class Persona cannot be applied to given types`: non trovando `super(...)` in testa, il compilatore ne ha inserito uno implicito senza argomenti. Lo stesso vale per `this(...)` (`call to this must be first statement in constructor`) e per chi scrive **entrambe** le chiamate nello stesso costruttore. Forma corretta: `super(nome);` come riga uno, e poi il resto; per riusare un altro costruttore della stessa classe, un `this(...)` al posto di `super(...)` (sezione 9.3.3).

> [!CAUTION]
> **Errore tipico — Due classi dopo `extends`**
> ```java
> class Tesista extends Studente, Persona {   // ERRORE: una sola superclasse
>     ...
> }
> ```
> Il compilatore risponde `'{' expected`: dopo il nome della superclasse si aspetta l'inizio del corpo (o `implements`). Java ammette una sola superclasse (sezione 9.1.5). Se serve un secondo "tipo", è un'interfaccia, e si scrive con `implements` (Capitolo 10). `Tesista extends Studente` basta già per essere anche una `Persona`.

> [!CAUTION]
> **Errore tipico — `implements` prima di `extends`**
> ```java
> class Studente implements Runnable extends Persona {   // ERRORE: ordine delle clausole
>     ...
> }
> ```
> Anche qui il compilatore risponde `'{' expected`. L'ordine è fisso: **prima `extends`, poi `implements`**. Forma corretta: `class Studente extends Persona implements Runnable`.

> [!CAUTION]
> **Errore tipico — Un metodo con parametri diversi credendo di riscrivere**
> ```java
> class Persona {
>     public void saluta() {
>         System.out.println("Ciao dalla Persona");
>     }
> }
>
> class Studente extends Persona {
>     public void saluta(String chi) {          // overload, non riscrittura: ha un parametro in più
>         System.out.println("Ciao " + chi + " dallo Studente");
>     }
> }
>
> // nel main:
> Persona p = new Studente();
> p.saluta();                                   // stampa: Ciao dalla Persona
> ```
> Il programma compila e stampa la versione di `Persona`: lo `Studente` ha **due** metodi `saluta`, quello ereditato e quello nuovo, e la chiamata `p.saluta()` senza argomenti sceglie il primo. Non c'è nessun messaggio. Forma corretta: la **stessa firma**, `public void saluta()`; e `@Override` (sezione 9.4.2) fa emergere subito l'errore.

> [!CAUTION]
> **Errore tipico — `toString` che stampa invece di restituire**
> ```java
> class Studente extends Persona {
>     public void toString() {                  // ERRORE: deve restituire una String
>         System.out.println("Studente[" + getNome() + "]");
>     }
> }
> ```
> Il compilatore risponde `toString() in Studente cannot override toString() in Object; return type void is not compatible with String`. Il metodo non deve **scrivere** niente: restituisce la stringa, e sono `println` e la concatenazione a usarla (sezione 9.7.2). Forma corretta: `public String toString() { return "Studente[" + getNome() + "]"; }`.

> [!CAUTION]
> **Errore tipico — Il metodo riscritto che richiama sé stesso**
> ```java
> class Studente extends Persona {
>     @Override
>     public void scrivi() {
>         scrivi();                              // ERRORE: richiama questa stessa versione, all'infinito
>         System.out.println("Matricola");
>     }
> }
> ```
> Il programma compila ed è corretto, sintatticamente; in esecuzione ogni chiamata ne produce un'altra senza fermarsi, e si interrompe con `Exception in thread "main" java.lang.StackOverflowError` (Capitolo 6, sezione 6.9). L'intenzione era usare la versione della superclasse. Forma corretta: `super.scrivi();` (sezione 9.4.3).

> [!CAUTION]
> **Errore tipico — `equals(Object)` che fa il cast senza controllare**
> ```java
> @Override
> public boolean equals(Object o) {
>     Specie altra = (Specie) o;                 // ERRORE: nessun controllo prima del cast
>     return nome.equals(altra.nome) && popolazione == altra.popolazione;
> }
> // nel main:
> a.equals("Lupo");                              // ClassCastException
> a.equals(null);                                // NullPointerException
> ```
> Il metodo compila, ma `equals` deve poter ricevere **qualunque** oggetto: con una stringa il cast fallisce (`java.lang.ClassCastException`), con `null` la lettura di `altra.nome` lancia una `NullPointerException`, mentre il contratto vuole `false` in entrambi i casi (sezione 9.7.3). Forma corretta: controllare prima `o == null || getClass() != o.getClass()` e restituire `false`.

> [!CAUTION]
> **Errore tipico — `equals` riscritto senza `hashCode`**
> ```java
> class Specie {
>     private String nome;
>     private int popolazione;
>     // costruttore...
>
>     @Override
>     public boolean equals(Object o) { ... }    // scritto bene, ma manca hashCode
> }
> // nel main:
> Specie a = new Specie("Lupo", 40);
> Specie b = new Specie("Lupo", 40);
> a.equals(b);                                   // true
> a.hashCode() == b.hashCode();                  // quasi sempre false
> ```
> Il programma compila e `equals` funziona, ma due oggetti uguali hanno codici hash diversi: il contratto di `hashCode` è violato (sezione 9.7.4) e una collezione che si serve del codice (Capitolo 12) potrebbe non ritrovare un oggetto che contiene. Forma corretta: aggiungere `public int hashCode() { return Objects.hash(nome, popolazione); }`, con gli stessi campi di `equals`.

> [!CAUTION]
> **Errore tipico — Ridichiarare nella sottoclasse un campo della superclasse**
> ```java
> class Persona {
>     private String nome;
>     public Persona(String nome) { this.nome = nome; }
>     public String getNome() { return nome; }
> }
>
> class Studente extends Persona {
>     private String nome;                       // un secondo campo, con lo stesso nome
>
>     public Studente(String nome) {
>         super("?");
>         this.nome = nome;                      // assegna il campo di Studente, non quello di Persona
>     }
> }
>
> // nel main:
> new Studente("Luisa").getNome();               // restituisce "?", non "Luisa"
> ```
> Non c'è nessun messaggio, perché il codice è legale. Ma l'oggetto contiene **due** campi `nome`, uno per classe (sezione 9.1.3): `getNome()`, scritto in `Persona`, legge il suo, quello assegnato con `super("?")`. Forma corretta: non ridichiarare il campo, e passare il valore al costruttore della superclasse, `super(nome)`.

## Riassunto

L'**ereditarietà** permette di scrivere una volta il codice comune a più classi e di dichiarare le classi più specifiche con `extends`: una **sottoclasse** riceve campi e metodi non privati della **superclasse** e aggiunge i propri, formando una gerarchia in cui ogni classe è un caso particolare ("è un") di quella sopra. I membri `private` restano nell'oggetto ma non si possono nominare dalla sottoclasse, che deve usare i metodi pubblici della superclasse; `protected` li apre alle sottoclassi ma rompe in parte l'incapsulamento. I costruttori non si ereditano: ogni costruttore di una sottoclasse richiama come **prima istruzione** un costruttore della superclasse con `super(...)` (se non lo scrive, Java inserisce `super()`, che non compila se la superclasse non ha un costruttore senza argomenti), così gli oggetti si costruiscono dall'antenato lontano alla classe più specifica. Una sottoclasse può **riscrivere** (*override*) un metodo ereditato dichiarandone uno con la stessa firma, non meno accessibile e con lo stesso tipo di ritorno, e con `super.metodo()` può riusare la versione della superclasse; l'annotazione `@Override` fa controllare al compilatore che si stia davvero riscrivendo. Questo è diverso dall'**overloading**, che aggiunge un metodo con lo stesso nome e parametri diversi e viene risolto dal compilatore. Poiché uno studente è una persona, una variabile della superclasse può indicare un oggetto di una sottoclasse (**compatibilità di tipo**): il compilatore controlla le chiamate sul tipo dichiarato, la JVM esegue la versione della classe dell'oggetto (**binding dinamico**), ed è questo il **polimorfismo**, che permette di scrivere codice valido per tutte le sottoclassi, anche future. Ogni classe estende, direttamente o no, `Object`, che fornisce `toString`, `equals`, `hashCode` e `getClass`: una classe riscrive `toString` per stampare i campi, `equals(Object)` per confrontare il contenuto (con il controllo della classe prima del cast) e `hashCode` con gli stessi campi.

**Concetti chiave**

- **Ereditarietà.** Una classe (la sottoclasse) riceve da un'altra (la superclasse) campi e metodi e ne aggiunge di nuovi; si dichiara con `extends`.
- **Superclasse e sottoclasse.** Sinonimi di classe base e classe derivata; ogni classe ha una sola superclasse diretta (ereditarietà singola), mentre le interfacce, che si implementano, possono essere più d'una.
- **"È un" e "ha un".** `extends` esprime "è un"; un campo il cui tipo è un'altra classe esprime "ha un".
- **Membri privati.** Esistono nell'oggetto ma non sono accessibili per nome dalla sottoclasse, che usa i metodi pubblici della superclasse.
- **`protected`.** Visibile alle sottoclassi e al package; in un file unico è visibile a tutte le classi.
- **`super(...)`.** Prima istruzione del costruttore di una sottoclasse: richiama un costruttore della superclasse; senza di essa Java aggiunge `super()`.
- **Ordine di costruzione.** Dall'antenato più lontano alla classe dell'oggetto.
- **`this(...)` e `super(...)`.** Entrambi vogliono essere la prima istruzione, quindi in un costruttore se ne scrive uno solo.
- **Overriding.** Riscrittura di un metodo ereditato con la stessa firma, accesso non ristretto, stesso tipo di ritorno; `@Override` fa verificare al compilatore.
- **`super.metodo()`.** Richiama la versione della superclasse di un metodo riscritto.
- **Overloading contro overriding.** Overloading: stesso nome, parametri diversi, scelta del compilatore sul tipo dichiarato. Overriding: stessa firma in una sottoclasse, scelta della JVM sulla classe dell'oggetto. `@Overload` non esiste.
- **`final`.** Davanti a un metodo impedisce di riscriverlo, davanti a una classe di estenderla.
- **Compatibilità di tipo.** Un oggetto di una sottoclasse si assegna a una variabile della superclasse senza cast; il verso inverso richiede un cast, verificato in esecuzione (`ClassCastException`).
- **Tipo dichiarato e classe dell'oggetto.** Il primo decide che cosa si può chiamare, la seconda quale versione di un metodo riscritto parte.
- **Polimorfismo e binding dinamico.** La versione eseguita di un metodo riscritto è quella della classe dell'oggetto, decisa a tempo di esecuzione.
- **`Object`.** Antenata di ogni classe; i suoi metodi sono ereditati da tutte.
- **`toString`.** Restituisce (non stampa) la rappresentazione testuale; `println` e la concatenazione lo chiamano da soli.
- **`equals(Object)`.** Controlla `this == o`, poi `null` e classe con `getClass()`, poi il cast e il confronto dei campi.
- **`hashCode`.** Va riscritto insieme a `equals`, con gli stessi campi (per esempio con `Objects.hash`): oggetti uguali devono dare lo stesso codice.

**Sintassi essenziale**

| Elemento | Forma |
|---|---|
| Sottoclasse | `class Studente extends Persona { ... }` |
| Sottoclasse che implementa un'interfaccia | `class Studente extends Persona implements Runnable { ... }` |
| Costruttore che richiama la superclasse | `public Studente(String nome, int m) { super(nome); this.matricola = m; }` |
| Costruttore che ne richiama un altro della stessa classe | `public Studente(String nome) { this(nome, 0); }` |
| Riscrivere un metodo | `@Override public void scrivi() { ... }` |
| Richiamare la versione della superclasse | `super.scrivi();` |
| Assegnamento verso l'alto | `Persona p = new Studente(...);` |
| Cast verso il basso | `Studente s = (Studente) p;` |
| Metodo che non si può riscrivere / classe che non si può estendere | `public final int getValore() { ... }` / `final class X { ... }` |
| Rappresentazione testuale | `@Override public String toString() { return "..."; }` |
| Confronto sul contenuto | `@Override public boolean equals(Object o) { ... }` |
| Codice hash | `@Override public int hashCode() { return Objects.hash(a, b); }` |

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `Object` (`java.lang`) | `toString` | `public String toString()` (predefinito: `NomeClasse@esadecimale`) | — |
| `Object` (`java.lang`) | `equals` | `public boolean equals(Object obj)` (predefinito: identità) | — |
| `Object` (`java.lang`) | `hashCode` | `public int hashCode()` | — |
| `Object` (`java.lang`) | `getClass` | `public final Class<?> getClass()` | — |
| `Class` (`java.lang`) | `getName` | `public String getName()` | — |
| `Objects` (`java.util`) | `hash` | `public static int hash(Object... values)` | — |
| `Objects` (`java.util`) | `equals` | `public static boolean equals(Object a, Object b)` (accetta `null`) | — |
| `Override` (`java.lang`) | — | annotazione `@Override`, solo sui metodi | errore di compilazione se il metodo non riscrive niente |
| `Runnable` (`java.lang`) | `run` | `void run()` (interfaccia; Capitoli 10 e 17) | — |
| `ClassCastException` (`java.lang`) | — | cast verso il basso su un oggetto di un'altra classe | è non controllata (`extends RuntimeException`) |
