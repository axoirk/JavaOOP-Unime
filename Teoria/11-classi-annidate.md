---
materia: Programmazione a Oggetti
capitolo: 11
titolo: Classi annidate, interne e anonime
livello_syllabus: 2-3
stato: completo
slide: ["Savitch cap. 15 slide 13-16", "JavaFX slide 96-98"]
appelli: [EXAM4]
fonti_esterne: 2
aggiornato: 2026-11-03
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 11 — Classi annidate, interne e anonime

## Di cosa parla questo capitolo

Fin qui ogni classe che abbiamo scritto stava per conto suo: una classe `Libro`, una classe `Rettangolo`, una classe `Tariffa`, ciascuna con il proprio nome e la propria vita. Ma capita spesso che una classe abbia senso **solo dentro un'altra**. Il nodo di una lista concatenata serve esclusivamente alla lista che lo contiene; un rubinetto serve esclusivamente al serbatoio a cui è collegato; un gestore di eventi serve a una finestra sola, e in un punto solo. Lasciare queste classi in giro, visibili a tutti, ha due inconvenienti: chiunque può usarle e rovinare lo stato dell'oggetto a cui appartengono (è la **perdita di riservatezza** del [Capitolo 7](07-classi-e-oggetti.md), sezione 7.3.7), e il programma si riempie di nomi che hanno un significato solo locale.

Java permette di **dichiarare una classe dentro il corpo di un'altra**. Ne esistono tre forme, e sono il tema del capitolo. La **classe interna** (*inner class*) è legata a un oggetto della classe esterna e ne vede i campi privati senza bisogno di *getter*. La **classe annidata statica** (*static nested class*) è solo una questione di organizzazione e di nome: vive dentro l'altra ma non è legata a nessun suo oggetto. La **classe anonima** (*anonymous class*) è una classe senza nome, scritta e istanziata in un solo punto, tipicamente per realizzare al volo un'interfaccia o una classe astratta del [Capitolo 10](10-classi-astratte-e-interfacce.md).

Alla fine saprai scrivere una classe interna e crearne gli oggetti con la sintassi giusta (`new` oppure `esterna.new`), sapere quando serve `Esterna.this`, scegliere tra classe interna e classe annidata statica, nascondere il nodo di una lista dentro la lista, scrivere una classe anonima che realizza un'interfaccia, e leggere una traccia d'esame che impone una di queste strutture senza perdere punti per un dettaglio di forma.

> [!IMPORTANT]
> **Nota per l'esame — Qui la struttura è il voto**
> Le tracce che usano classi annidate sono brevi e fatte di vincoli verificabili alla lettera: "classe annidata **non statica**", "tutte le variabili d'istanza **private**", "dentro la classe annidata **non va dichiarato** nessun riferimento alla classe esterna". Un programma che stampa l'output giusto ma ha messo `static`, o ha dichiarato a mano un campo che riferisce l'esterna, viola la traccia anche se funziona. Per questo il capitolo insiste sulla **sintassi esatta** e sul legame tra la traccia e il codice (sezione 11.6). Vedi anche "Come esce all'esame" e gli scheletri.

## 11.1 Perché mettere una classe dentro un'altra

### 11.1.1 Il problema: un tipo di supporto che tutti possono vedere

Per capire che cosa si guadagna, partiamo da una classe che ha bisogno di un tipo di supporto. Una lista di stringhe è fatta di **nodi**: ogni nodo contiene una stringa e un riferimento al nodo successivo (le liste concatenate vere e proprie sono nel [Capitolo 12](12-generics-e-collezioni.md); qui ci interessa solo *dove* scrivere la classe del nodo). La soluzione più ovvia è una classe `Nodo` per conto suo, accanto alla classe `ListaDiStringhe`:

```java
class Nodo {
    private String dato;
    private Nodo successivo;

    public Nodo(String dato, Nodo successivo) {
        this.dato = dato;
        this.successivo = successivo;
    }

    public String getDato() {
        return dato;
    }

    public Nodo getSuccessivo() {
        return successivo;
    }

    public void setSuccessivo(Nodo successivo) {
        this.successivo = successivo;
    }
}

class ListaDiStringhe {
    private Nodo testa;                       // il primo nodo; null = lista vuota

    public void aggiungiInTesta(String s) {
        testa = new Nodo(s, testa);           // il nuovo nodo punta al vecchio primo
    }

    public Nodo primo() {                     // comodo per chi vuole percorrere la lista
        return testa;
    }

    public int dimensione() {
        int n = 0;
        for (Nodo c = testa; c != null; c = c.getSuccessivo()) {
            n++;
        }
        return n;
    }
}

public class ProvaPerdita {
    public static void main(String[] args) {
        ListaDiStringhe lista = new ListaDiStringhe();
        lista.aggiungiInTesta("c");
        lista.aggiungiInTesta("b");
        lista.aggiungiInTesta("a");
        System.out.println("Elementi: " + lista.dimensione());

        lista.primo().setSuccessivo(null);    // chi ha il nodo può staccare il resto della lista
        System.out.println("Elementi: " + lista.dimensione());
    }
}
```

```text
Elementi: 3
Elementi: 1
```

Vediamo che cosa è successo. I campi di `Nodo` e il campo `testa` sono privati, e a prima vista tutto è al sicuro. Ma `ListaDiStringhe` ha un metodo `primo()` che **restituisce un riferimento a un `Nodo`**, e `Nodo` ha un metodo `setSuccessivo` pubblico. Il codice di `main`, che con la lista non ha niente a che fare, ottiene il primo nodo e gli cambia il successivo: tre elementi diventano uno, senza che la lista se ne accorga. È esattamente la perdita di riservatezza del Capitolo 7: un campo privato (qui `testa`) è protetto solo finché nessun metodo pubblico ne consegna a un estraneo il riferimento.

Si può correggere togliendo `primo()`. Ma il problema resta più in generale: la classe `Nodo` è visibile a tutto il programma, chiunque può scrivere `new Nodo("x", null)`, costruire catene di nodi e passarle a chi le accetta, e un domani basterà un altro metodo della lista che riceva o restituisca un nodo per riaprire la falla. Quello che vorremmo è che **il tipo `Nodo` non esistesse fuori da `ListaDiStringhe`**: non perché nessuno lo usi per distrazione, ma perché il compilatore lo vieti.

### 11.1.2 Classi annidate: le definizioni

La soluzione di Java è dichiarare `Nodo` *dentro* `ListaDiStringhe`.

> [!NOTE]
> **Definizione — Classe annidata**
> Una **classe annidata** (*nested class*) è una classe dichiarata nel corpo di un'altra classe, detta **classe esterna** (*outer class*). Una classe annidata **non** è una sottoclasse: la relazione è di appartenenza, non di ereditarietà.

Le forme che incontreremo sono tre, e conviene fissare subito i nomi:

| Forma | Come si riconosce | Legata a un oggetto dell'esterna? |
|---|---|---|
| **Classe interna** (*inner class*) | `class X { ... }` nel corpo dell'esterna, **senza** `static` | Sì: ogni oggetto interno appartiene a un oggetto esterno |
| **Classe annidata statica** (*static nested class*) | `static class X { ... }` nel corpo dell'esterna | No |
| **Classe anonima** (*anonymous class*, nel corso *anonymous inner class*) | `new Tipo() { ... }` dentro un metodo, senza nome | Sì, se creata in un metodo d'istanza |

Nell'uso corrente, e nelle tracce d'esame, "classe annidata non statica" e "classe interna" sono la stessa cosa. Le prossime tre sezioni le trattano una per volta, partendo dalla più importante.

## 11.2 La classe interna

### 11.2.1 Dichiarazione e accesso reciproco ai membri privati

Una **classe interna** si dichiara scrivendo una normale definizione di classe dentro il corpo di un'altra, senza `static`. Il suo nome è locale alla classe esterna: nel resto del programma si scrive `Esterna.Interna`. Il punto più importante è questo: **i metodi della classe interna e quelli della classe esterna possono usare i metodi e le variabili d'istanza gli uni degli altri, anche quando sono `private`.**

Facciamo l'esempio di un serbatoio d'acqua con i suoi rubinetti. Il serbatoio ha un nome e una quantità di litri, entrambi privati. Ogni rubinetto, quando viene aperto, versa nel serbatoio una quantità fissa di litri.

```java
class Serbatoio {
    private String nome;
    private int litri;
    private Rubinetto principale;

    public Serbatoio(String nome) {
        this.nome = nome;
        this.litri = 0;
        this.principale = new Rubinetto(5);          // dentro l'esterna basta new Rubinetto(...)
    }

    public class Rubinetto {                         // classe interna: nel corpo di Serbatoio, senza static
        private int portata;

        public Rubinetto(int portata) {
            this.portata = portata;
        }

        public void apri() {
            litri += portata;                        // litri è un campo PRIVATO di Serbatoio
        }

        public String descrizione() {
            return "rubinetto da " + portata + " litri su " + nome;   // nome: campo di Serbatoio
        }
    }

    public Rubinetto getPrincipale() {
        return principale;
    }

    public String stato() {
        return nome + ": " + litri + " litri, portata principale " + principale.portata;
        //                                                    portata è PRIVATO di Rubinetto
    }
}

public class ProvaSerbatoio {
    public static void main(String[] args) {
        Serbatoio s = new Serbatoio("Nord");
        s.getPrincipale().apri();                              // +5 litri

        Serbatoio.Rubinetto extra = s.new Rubinetto(2);        // un secondo rubinetto sullo STESSO serbatoio
        extra.apri();
        extra.apri();                                          // +2 +2 litri

        System.out.println(s.stato());
        System.out.println(extra.descrizione());

        Serbatoio t = new Serbatoio("Sud");
        Serbatoio.Rubinetto altro = t.new Rubinetto(3);
        altro.apri();
        System.out.println(t.stato());
        System.out.println(s.stato());
    }
}
```

```text
Nord: 9 litri, portata principale 5
rubinetto da 2 litri su Nord
Sud: 3 litri, portata principale 5
Nord: 9 litri, portata principale 5
```

Leggiamo il programma dall'alto.

- `class Serbatoio`: la classe esterna. I tre campi sono `private`, come ci ha insegnato l'incapsulamento.
- `private Rubinetto principale;`: dentro la classe esterna il tipo si scrive semplicemente `Rubinetto`, senza il prefisso `Serbatoio.`.
- Nel costruttore `new Rubinetto(5)` crea il rubinetto principale. Per ora accettiamo che dentro la classe esterna si scriva così; la sezione 11.2.3 spiega che cosa c'è dietro.
- `public class Rubinetto { ... }` è la classe interna. Ha un campo privato `portata` e un costruttore, come ogni classe. Non c'è `static`.
- In `apri()` la riga `litri += portata;` modifica `litri`, che **non è un campo di `Rubinetto`** ma del serbatoio a cui il rubinetto appartiene, ed è privato. Non c'è nessun *getter*, nessun *setter* e nessun riferimento passato al costruttore: il nome `litri` basta.
- In `descrizione()` lo stesso accade con `nome`.
- Il verso opposto: nel metodo `stato()` della classe esterna l'espressione `principale.portata` legge il campo `portata`, privato di `Rubinetto`. È legale: per Java, la classe esterna e le sue classi annidate fanno parte della stessa unità e si vedono a vicenda.
- Nel `main`, `s.getPrincipale().apri()` apre il rubinetto principale di `s`: i litri passano da 0 a 5. `s.new Rubinetto(2)` crea un secondo rubinetto, **sullo stesso serbatoio `s`**; due aperture versano 4 litri, che sommati ai 5 danno 9. Il rubinetto `altro`, invece, appartiene a `t`: versa 3 litri nel serbatoio Sud, e `s` non cambia. La sezione seguente spiega il perché.

Un'osservazione pratica: quando compili, `javac` produce **un file `.class` per ogni classe**, annidate comprese. Per questo programma compaiono `Serbatoio.class`, `Serbatoio$Rubinetto.class` e `ProvaSerbatoio.class`: il nome di una classe annidata è quello dell'esterna, un simbolo `$` e il nome della annidata.

### 11.2.2 Il legame con l'oggetto esterno

Che cosa rende una classe interna diversa da una classe qualsiasi che per caso sta nello stesso file? Il fatto che **ogni oggetto di una classe interna è legato a un oggetto della classe esterna**: quello che lo ha creato. Quando il rubinetto `altro` scrive `litri += portata`, il nome `litri` non è ambiguo, perché si riferisce al campo `litri` dell'oggetto `Serbatoio` a cui `altro` appartiene, cioè `t`.

> [!TIP]
> **Intuizione — Un rubinetto non esiste da solo**
> Pensa a un rubinetto vero: non ha senso senza l'impianto a cui è collegato. Quando lo apri, l'acqua esce da *quel* serbatoio, non da un serbatoio qualunque. Allo stesso modo ogni oggetto `Rubinetto` porta con sé, in modo invisibile, l'indicazione di quale `Serbatoio` è il suo, e quando il codice dice `litri` Java sa di quale oggetto parla. L'analogia ha un limite: un rubinetto vero si può smontare e rimontare altrove, mentre il collegamento di un oggetto interno al suo oggetto esterno è fissato al momento della creazione e non cambia mai.

Nell'esempio, dopo le istruzioni del `main`, la situazione nella memoria è questa (ogni freccia va dall'oggetto interno al suo oggetto esterno):

```text
 s.principale (portata 5) --\
                             +--> Serbatoio "Nord"  (litri = 9)
 extra (portata 2) ---------/

 altro (portata 3) ----------> Serbatoio "Sud"   (litri = 3)
```

Le due frecce che arrivano a "Nord" sono il motivo per cui i litri si sommano; la terza va a "Sud", ed è il motivo per cui `t` e `s` restano indipendenti. Il collegamento è **implicito**: non si dichiara nessun campo, non si passa nessun argomento. Ed è un'informazione da ricordare, perché una traccia può proibire di scriverlo a mano (sezione 11.6): dentro la classe interna l'oggetto esterno c'è già, e ci si arriva con il nome dei suoi membri oppure con `Esterna.this` (sezione 11.2.4).

### 11.2.3 Creare un oggetto interno: `new` e `esterna.new`

Poiché un oggetto interno ha bisogno di un oggetto esterno, per crearlo bisogna **dire quale**. La sintassi cambia a seconda di *dove* ci si trova.

> [!NOTE]
> **Definizione — Creazione di un oggetto di una classe interna**
> - **Dentro un metodo d'istanza o un costruttore della classe esterna** (e quindi anche dentro un'altra classe interna della stessa esterna) basta `new Interna(...)`: l'oggetto esterno è `this`, cioè l'oggetto su cui il metodo sta lavorando.
> - **Da fuori**, o da un metodo `static` dell'esterna, si scrive `riferimentoEsterna.new Interna(...)`, dove `riferimentoEsterna` è una variabile che indica un oggetto della classe esterna. Il tipo si scrive `Esterna.Interna`.

```java
class Serbatoio {
    private int litri;

    public class Rubinetto {
        private int portata;

        public Rubinetto(int portata) {
            this.portata = portata;
        }

        public void apri() {
            litri += portata;
        }
    }

    public Rubinetto nuovoRubinetto(int portata) {
        return new Rubinetto(portata);                   // 1) dentro l'esterna: new Interna(...)
    }

    public int getLitri() {
        return litri;
    }
}

public class ProvaCreazione {
    public static void main(String[] args) {
        Serbatoio s = new Serbatoio();

        Serbatoio.Rubinetto a = s.nuovoRubinetto(2);     // 1) lo crea un metodo dell'esterna
        Serbatoio.Rubinetto b = s.new Rubinetto(3);      // 2) da fuori: esterna.new Interna(...)

        a.apri();
        b.apri();
        System.out.println(s.getLitri());
    }
}
```

```text
5
```

Nel `main` ci sono due modi di ottenere un rubinetto di `s`. Il primo passa per un metodo della classe esterna, `nuovoRubinetto`, che scrive `new Rubinetto(portata)` e quindi usa implicitamente `this` come oggetto esterno. Il secondo, `s.new Rubinetto(3)`, dice esplicitamente: "crea un `Rubinetto` appartenente a `s`". Le due strade producono lo stesso tipo di oggetto. Si noti anche la dichiarazione della variabile: `Serbatoio.Rubinetto`, con il nome dell'esterna davanti, perché fuori da `Serbatoio` il nome corto `Rubinetto` non esiste.

> [!WARNING]
> **Attenzione — `new Esterna.Interna()` non basta, e `new Interna()` in un `main` statico nemmeno**
> Due errori molto frequenti, perché la forma sembra naturale:
> ```java
> Serbatoio.Rubinetto r = new Serbatoio.Rubinetto(3);   // ERRORE: quale serbatoio?
> ```
> Il compilatore risponde `an enclosing instance that contains Serbatoio.Rubinetto is required`: manca l'oggetto esterno. Forma corretta: `s.new Rubinetto(3)`.
>
> Lo stesso accade se il `main` è scritto *dentro* la classe esterna e prova a creare l'interna senza un oggetto:
> ```java
> public class Serbatoio {
>     class Rubinetto { }
>     public static void main(String[] args) {
>         Rubinetto r = new Rubinetto();                  // ERRORE
>     }
> }
> ```
> `main` è `static`: non c'è nessun `this`, quindi nessun oggetto esterno implicito. Il compilatore risponde `non-static variable this cannot be referenced from a static context`. Forma corretta: creare prima un `Serbatoio s = new Serbatoio();` e poi scrivere `s.new Rubinetto()`.

### 11.2.4 `this` e `Esterna.this`

Dentro la classe interna la parola `this` indica l'**oggetto interno**: quello su cui il metodo sta lavorando. Come si fa a indicare l'oggetto esterno quando serve nominarlo esplicitamente? Si scrive `Esterna.this`. Serve soprattutto quando i due oggetti hanno un campo con lo stesso nome: il nome non qualificato, dentro la classe interna, vale per il campo dell'interna, che *nasconde* quello dell'esterna.

```java
class Serbatoio {
    private String nome;

    public Serbatoio(String nome) {
        this.nome = nome;
    }

    public class Rubinetto {
        private String nome;                                     // stesso nome del campo dell'esterna

        public Rubinetto(String nome) {
            this.nome = nome;                                    // this.nome: il campo di Rubinetto
        }

        public String descrizione() {
            return nome + " su " + Serbatoio.this.nome;          // nome = Rubinetto; Serbatoio.this.nome = Serbatoio
        }
    }
}

public class ProvaEsternaThis {
    public static void main(String[] args) {
        Serbatoio s = new Serbatoio("Nord");
        Serbatoio.Rubinetto r = s.new Rubinetto("R1");
        System.out.println(r.descrizione());
    }
}
```

```text
R1 su Nord
```

Nel costruttore di `Rubinetto` il parametro `nome` e il campo `nome` hanno lo stesso nome, e `this.nome` indica il campo (come nel [Capitolo 7](07-classi-e-oggetti.md), sezione 7.1.6). In `descrizione()` il nome semplice `nome` è il campo di `Rubinetto`, e per arrivare a quello del serbatoio si scrive `Serbatoio.this.nome`: la forma `NomeDellaEsterna.this` significa "l'oggetto della classe esterna a cui appartengo". Funziona allo stesso modo per i metodi (`Serbatoio.this.stato()`).

> [!WARNING]
> **Attenzione — Il campo omonimo nasconde quello dell'esterna, in silenzio**
> Se la classe interna dichiara un campo con lo stesso nome di un campo dell'esterna, il nome semplice indica *sempre* quello dell'interna, senza nessun avviso. Il programma compila e fa una cosa diversa da quella voluta: un metodo che crede di aggiornare il serbatoio sta aggiornando solo il proprio campo. Se non serve l'omonimia, si evita scegliendo nomi diversi; se serve, si qualifica con `Esterna.this`.

### 11.2.5 La visibilità della classe interna

Una classe interna è un **membro** della classe esterna, come un campo o un metodo, e quindi può avere un modificatore di accesso: `public`, `private` oppure nessuno (accesso di package, come nel [Capitolo 7](07-classi-e-oggetti.md), sezione 7.6). Con `private` il nome della classe interna è visibile **soltanto dentro la classe esterna**: nessun altro codice può dichiarare una variabile di quel tipo né creare un oggetto di quella classe. È ciò che serve a nascondere un tipo di supporto, come vedremo con il nodo (sezione 11.3).

```java
public class Cisterna {
    private int livello;

    private class Valvola {                       // private: solo Cisterna può nominarla
        private int apertura;

        Valvola(int apertura) {
            this.apertura = apertura;
        }

        void regola() {
            livello += apertura;
        }
    }

    public static void main(String[] args) {
        Cisterna c = new Cisterna();
        Valvola v = c.new Valvola(4);             // il main è dentro Cisterna: può nominare Valvola
        v.regola();
        v.regola();
        System.out.println(c.livello);
    }
}
```

```text
8
```

Qui il `main` si trova nella stessa classe `Cisterna`, quindi vede la classe privata `Valvola`. Ma attenzione: la visibilità conta **dal punto di vista di chi crea l'oggetto**.

> [!WARNING]
> **Attenzione — `private` e un `main` fuori dalla classe esterna**
> ```java
> class Serbatoio {
>     private class Rubinetto { }
> }
>
> public class Prova {
>     public static void main(String[] args) {
>         Serbatoio s = new Serbatoio();
>         Serbatoio.Rubinetto r = s.new Rubinetto();    // ERRORE
>     }
> }
> ```
> Il compilatore risponde `Serbatoio.Rubinetto has private access in Serbatoio`. Una classe interna `private` non può essere creata da altre classi, `main` compreso. Se la traccia dice che l'oggetto interno si crea "dall'esterno", cioè da un `main` che sta in un'altra classe, la classe interna **non** deve essere `private` (né il suo costruttore): si lascia senza modificatore, oppure `public`.

### 11.2.6 Annidare non è ereditare

Un'ultima precisazione, perché è un equivoco che ritorna: **mettere una classe dentro un'altra non crea nessuna relazione di ereditarietà**. Sono due strumenti che rispondono a due domande diverse.

| Domanda | Strumento | Sintassi |
|---|---|---|
| "Un `Rubinetto` **è un** `Serbatoio`?" (relazione "è un") | ereditarietà | `class Rubinetto extends Serbatoio` |
| "Un `Rubinetto` **appartiene a** un `Serbatoio`?" | classe interna | `class Rubinetto { ... }` scritta nel corpo di `Serbatoio` |

Un rubinetto non è un serbatoio: appartiene a un serbatoio. Scrivere `extends` per ottenere l'annidamento è sbagliato, e spesso non compila nemmeno.

> [!WARNING]
> **Attenzione — `extends` al posto dell'annidamento**
> ```java
> class Serbatoio {
>     private int litri;
>     Serbatoio(int litri) { this.litri = litri; }
>
>     class Rubinetto extends Serbatoio {        // ERRORE di progetto, e qui anche di compilazione
>         Rubinetto() { }
>     }
> }
> ```
> Il costruttore di una sottoclasse chiama implicitamente `super()`, cioè un costruttore senza parametri di `Serbatoio` che qui non esiste: il compilatore risponde `constructor Serbatoio in class Serbatoio cannot be applied to given types` (come nel [Capitolo 9](09-ereditarieta-e-polimorfismo.md), sezione 9.3). Se invece `Serbatoio` avesse un costruttore senza parametri, il codice **compilerebbe** e sarebbe ancora più insidioso: ogni `Rubinetto` sarebbe a sua volta un `Serbatoio`, con **una propria copia** dei campi ereditati, e un metodo che crede di modificare "il serbatoio" modificherebbe solo la copia del rubinetto. Per far lavorare un rubinetto sul serbatoio a cui appartiene serve la classe interna, che ha il collegamento all'oggetto esterno, non l'ereditarietà.

## 11.3 Il nodo di lista come classe interna privata

Torniamo al problema da cui siamo partiti. Per impedire che la classe `Nodo` sia usata dal resto del programma, la dichiariamo **classe interna `private`** di `ListaDiStringhe`. È la soluzione tipica al problema della perdita di riservatezza nelle strutture concatenate: il tipo `Nodo` esiste solo dentro la lista, e nessun metodo pubblico può restituirlo o riceverlo, perché nessuno fuori dalla lista può nemmeno scriverne il nome.

```java
class ListaDiStringhe {

    private class Nodo {                         // classe interna PRIVATA: invisibile fuori da ListaDiStringhe
        private String dato;
        private Nodo successivo;

        Nodo(String dato, Nodo successivo) {
            this.dato = dato;
            this.successivo = successivo;
        }
    }

    private Nodo testa;                          // il primo nodo; null = lista vuota

    public void aggiungiInTesta(String s) {
        testa = new Nodo(s, testa);              // il nuovo nodo punta al vecchio primo
    }

    public void aggiungiInCoda(String s) {
        Nodo nuovo = new Nodo(s, null);
        if (testa == null) {                     // lista vuota: il nuovo nodo è anche il primo
            testa = nuovo;
            return;
        }
        Nodo corrente = testa;
        while (corrente.successivo != null) {    // si scorre fino all'ultimo nodo
            corrente = corrente.successivo;      // campo privato di Nodo, letto per nome
        }
        corrente.successivo = nuovo;
    }

    public boolean contiene(String s) {
        Nodo corrente = testa;
        while (corrente != null) {
            if (corrente.dato.equals(s)) {       // confronto sul contenuto, non con ==
                return true;
            }
            corrente = corrente.successivo;
        }
        return false;
    }

    public int dimensione() {
        int n = 0;
        for (Nodo c = testa; c != null; c = c.successivo) {
            n++;
        }
        return n;
    }

    public String toString() {
        String r = "[";
        for (Nodo c = testa; c != null; c = c.successivo) {
            r += c.dato;
            if (c.successivo != null) {
                r += ", ";
            }
        }
        return r + "]";
    }
}

public class ProvaLista {
    public static void main(String[] args) {
        ListaDiStringhe l = new ListaDiStringhe();
        l.aggiungiInTesta("b");
        l.aggiungiInTesta("a");
        l.aggiungiInCoda("c");

        System.out.println(l);
        System.out.println(l.dimensione());
        System.out.println(l.contiene("b"));
        System.out.println(l.contiene("z"));
    }
}
```

```text
[a, b, c]
3
true
false
```

Leggiamo i punti essenziali.

- `private class Nodo`: la classe interna è privata. I suoi campi `dato` e `successivo` sono privati anch'essi, ma la classe esterna li usa direttamente (`corrente.successivo`, `corrente.dato`) senza nessun *getter* o *setter*, per il principio della sezione 11.2.1. I metodi `getSuccessivo` e simili, che nella versione a classe separata della sezione 11.1.1 erano la porta della falla, qui **non servono più**: l'unico codice che vede i nodi è la lista.
- `testa` è l'unico campo della lista: il riferimento al primo nodo.
- `aggiungiInTesta` crea un nodo che ha come successivo il vecchio primo, e lo mette in `testa`. `new Nodo(...)` si scrive senza prefisso, perché siamo in un metodo d'istanza dell'esterna (sezione 11.2.3).
- `aggiungiInCoda` tratta a parte la lista vuota (`testa == null`), altrimenti percorre la catena fino all'ultimo nodo, quello con `successivo == null`, e vi aggancia il nuovo.
- `contiene`, `dimensione` e `toString` percorrono la catena con un riferimento che avanza di nodo in nodo; `contiene` confronta con `equals`, come nel [Capitolo 8](08-riferimenti-e-memoria.md), sezione 8.4. Quando il riferimento `corrente` diventa `null` la catena è finita.

Il vantaggio è che il tipo `Nodo` ora è inaccessibile dal resto del programma.

> [!WARNING]
> **Attenzione — Fuori dalla lista il nodo non si nomina**
> ```java
> public class Prova {
>     public static void main(String[] args) {
>         ListaDiStringhe l = new ListaDiStringhe();
>         ListaDiStringhe.Nodo n = null;       // ERRORE
>     }
> }
> ```
> Il compilatore risponde `ListaDiStringhe.Nodo has private access in ListaDiStringhe`. È proprio ciò che volevamo: non c'è modo di dichiarare un nodo fuori dalla lista, e quindi nessun metodo pubblico della lista potrebbe mai restituirne uno senza che il programma smetta di compilare.

Le liste concatenate complete (iteratori, versione generica, eccezioni) sono nel [Capitolo 12](12-generics-e-collezioni.md); questo schema, con il nodo nascosto dentro la lista, è quello che vi si riprende.

## 11.4 La classe annidata statica

### 11.4.1 Quando il legame con l'esterna non serve

Non tutte le classi annidate hanno bisogno di un oggetto esterno. Il nodo della sezione precedente, per esempio, non usa mai i campi della lista (come `testa`): si limita a contenere un dato e un riferimento al nodo seguente. Per una classe che vive dentro un'altra solo per **organizzazione** (il nome, il raggruppamento) e non per accedere ai dati di un oggetto esterno, Java offre la **classe annidata statica**, dichiarata con `static`.

> [!NOTE]
> **Definizione — Classe annidata statica**
> Una **classe annidata statica** (*static nested class*) è una classe dichiarata nel corpo di un'altra con il modificatore `static`. Non è legata a nessun oggetto della classe esterna: può esistere e si crea senza di esso. Non può usare per nome i campi e i metodi **d'istanza** dell'esterna, ma può usare quelli `static`, anche se `private`.

### 11.4.2 Come si scrive e come si crea

```java
class Griglia {
    private static int totaleCoordinate = 0;           // contatore di classe, privato
    private int righe;
    private int colonne;

    public Griglia(int righe, int colonne) {
        this.righe = righe;
        this.colonne = colonne;
    }

    public static int getTotaleCoordinate() {
        return totaleCoordinate;
    }

    public static class Coordinata {                   // annidata STATICA
        private int riga;
        private int colonna;

        public Coordinata(int riga, int colonna) {
            this.riga = riga;
            this.colonna = colonna;
            totaleCoordinate++;                        // campo static dell'esterna: si può, anche se private
        }

        public boolean dentro(Griglia g) {             // un oggetto Griglia va passato: da sola non lo ha
            return riga >= 0 && riga < g.righe && colonna >= 0 && colonna < g.colonne;
        }

        public String toString() {
            return "(" + riga + "," + colonna + ")";
        }
    }
}

public class ProvaGriglia {
    public static void main(String[] args) {
        Griglia g = new Griglia(3, 4);

        Griglia.Coordinata a = new Griglia.Coordinata(2, 3);   // niente "oggetto.new": basta il nome qualificato
        Griglia.Coordinata b = new Griglia.Coordinata(3, 0);

        System.out.println(a + " dentro: " + a.dentro(g));
        System.out.println(b + " dentro: " + b.dentro(g));
        System.out.println(Griglia.getTotaleCoordinate());
    }
}
```

```text
(2,3) dentro: true
(3,0) dentro: false
2
```

Le differenze rispetto alla classe interna si vedono tutte in questo esempio:

- **Creazione.** Si scrive `new Griglia.Coordinata(2, 3)`, con il nome qualificato e senza nessun oggetto `Griglia` davanti: ne creiamo due `Coordinata` senza che sia stata creata alcuna `Griglia` per loro. Il `new Interna()` della sezione 11.2.3 qui sarebbe sbagliato, e `g.new Coordinata(...)` anche.
- **Accesso ai membri `static`.** `totaleCoordinate++` nel costruttore di `Coordinata` modifica un campo `static` e `private` della classe esterna: permesso, perché un campo di classe non appartiene a nessun oggetto.
- **Nessun accesso diretto ai campi d'istanza.** Dentro `Coordinata` il nome `righe` non è utilizzabile da solo: non esiste una `Griglia` a cui riferirlo. Per questo `dentro` riceve la griglia come parametro e scrive `g.righe`. Con un oggetto in mano l'accesso è permesso, anche se `righe` è privato (vale la stessa regola della sezione 11.2.1: la esterna e le sue annidate si vedono a vicenda).

> [!WARNING]
> **Attenzione — Nominare un campo d'istanza dell'esterna da una classe statica**
> ```java
> class Griglia {
>     private int righe = 3;
>     static class Coordinata {
>         int numeroRighe() { return righe; }        // ERRORE
>     }
> }
> ```
> Il compilatore risponde `non-static variable righe cannot be referenced from a static context`. È lo stesso errore che si ottiene usando un campo d'istanza da un metodo `static` (Capitolo 6, sezione 6.4): una classe annidata statica non ha un oggetto esterno a cui riferirsi.

Anche **`enum` e `interface`** si possono dichiarare dentro una classe, e le loro dichiarazioni annidate si comportano come le classi annidate statiche: non servono oggetti esterni. Un'`enum` del [Capitolo 7](07-classi-e-oggetti.md), sezione 7.5, che serve a una sola classe si può scrivere nel suo corpo e usare con il nome qualificato:

```java
class Semaforo {
    enum Colore { ROSSO, GIALLO, VERDE }
}

public class ProvaEnumAnnidata {
    public static void main(String[] args) {
        Semaforo.Colore c = Semaforo.Colore.VERDE;
        System.out.println(c);
    }
}
```

```text
VERDE
```

### 11.4.3 Interna o statica: come si sceglie

La scelta dipende da una sola domanda: **la classe annidata deve lavorare sui dati di un oggetto della classe esterna?** Se sì, è una classe interna. Se è soltanto un tipo di supporto autonomo, può essere statica.

| | Classe interna (`class X`) | Classe annidata statica (`static class X`) |
|---|---|---|
| Legata a un oggetto esterno | **Sì**, implicitamente | No |
| Usa per nome i campi e i metodi d'istanza dell'esterna | **Sì**, anche i privati | No (solo con un oggetto in mano) |
| Usa per nome i campi e i metodi `static` dell'esterna | Sì | Sì |
| Come si crea dall'esterno | `esterna.new X(...)` | `new Esterna.X(...)` |
| Può esistere senza un oggetto esterno | No | Sì |
| `Esterna.this` | Disponibile | Non utilizzabile (errore: `non-static variable this cannot be referenced from a static context`) |

> [!WARNING]
> **Attenzione — `static` non è un dettaglio**
> Aggiungere o togliere `static` cambia il significato della classe. Un `static` in più spegne l'unica funzione della classe interna (vedere l'oggetto esterno) e cambia la sintassi di creazione. Un `static` in meno, dove non servirebbe, è accettato dal compilatore ma dice una cosa diversa da quello che si voleva. Il nodo di lista della sezione 11.3 non usa mai l'oggetto esterno, quindi funzionerebbe identico come `private static class Nodo`; quando però una traccia chiede una classe **non statica**, `static` va omesso.

### 11.4.4 Le classi annidate nella libreria standard

Il meccanismo non è solo una curiosità del linguaggio: la libreria di Java lo usa spesso, quasi sempre nella forma statica.

> [!NOTE]
> **Approfondimento esterno — `Map.Entry` e `Thread.State`**
> Nella Javadoc di Java 17 l'interfaccia che rappresenta una coppia chiave-valore è dichiarata `public static interface Map.Entry<K,V>`, e la pagina riporta "Enclosing interface: `Map`": `Entry` è un'interfaccia annidata dentro `Map`, e fuori da essa si scrive `Map.Entry`. Allo stesso modo `Thread.State`, l'insieme degli stati di un thread (`NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, `TERMINATED`), è dichiarato `public static enum Thread.State`, e il metodo `public Thread.State getState()` della classe `Thread` ne restituisce un valore. Il nome qualificato con il punto è lo stesso `Esterna.Annidata` visto in questo capitolo. `Map` è nel [Capitolo 12](12-generics-e-collezioni.md) e i thread nel [Capitolo 17](17-thread.md).
>
> *Fonte:* [java.util.Map.Entry](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Map.Entry.html), [java.lang.Thread.State](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.State.html), [java.lang.Thread#getState](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.html#getState())

```java
public class ProvaThreadState {
    public static void main(String[] args) {
        Thread t = new Thread();                 // creato, non ancora avviato
        Thread.State stato = t.getState();       // il tipo è annidato in Thread
        System.out.println(stato);
    }
}
```

```text
NEW
```

## 11.5 La classe anonima

### 11.5.1 Il problema: una classe usata una volta sola

Nel [Capitolo 10](10-classi-astratte-e-interfacce.md) abbiamo scritto classi che realizzano un'interfaccia: `Corridore implements Runnable`, `Rettangolo implements Figura`, e così via. Ogni volta abbiamo dato alla classe un nome, scritto la sua intestazione, creato un oggetto. Ma a volte serve un oggetto di questo tipo **in un solo punto del programma**, e dare un nome a una classe che si userà una volta soltanto è un lavoro inutile: si pensi a un gestore di eventi di un pulsante, o a un `Runnable` che un thread eseguirà una volta. Per questi casi Java permette di **scrivere la classe e creare l'oggetto nello stesso punto, senza dare un nome alla classe**.

### 11.5.2 `new Tipo() { ... }`

> [!NOTE]
> **Definizione — Classe anonima**
> Una **classe anonima** (*anonymous class*) è una classe senza nome, il cui corpo viene scritto proprio nell'espressione che ne crea un oggetto:
> ```java
> new NomeDiInterfacciaOClasse() {
>     // corpo: i metodi che realizzano l'interfaccia o riscrivono la classe
> }
> ```
> Dopo `new` non c'è il nome di una classe da istanziare, ma quello di un'**interfaccia** (che la classe anonima realizza) o di una **classe** (che la classe anonima estende). L'espressione ha come valore un riferimento all'oggetto creato, e si può assegnare a una variabile del tipo dell'interfaccia o della classe.

Come sempre nel corso, partiamo dall'equivalente con il nome e poi lo accorciamo. Abbiamo un'interfaccia `Saluto` e vogliamo due modi di salutare.

```java
interface Saluto {
    String saluta(String nome);
}

class SalutoFormale implements Saluto {                       // la solita classe con il nome
    public String saluta(String nome) {
        return "Buongiorno, " + nome;
    }
}

public class ProvaAnonima {
    public static void main(String[] args) {
        Saluto formale = new SalutoFormale();                 // una classe con il nome: va dichiarata a parte

        Saluto informale = new Saluto() {                     // classe anonima: nessun nome, corpo subito dopo
            public String saluta(String nome) {
                return "Ciao " + nome;
            }
        };                                                    // il ; chiude l'ISTRUZIONE di dichiarazione

        System.out.println(formale.saluta("Marta"));
        System.out.println(informale.saluta("Marta"));
    }
}
```

```text
Buongiorno, Marta
Ciao Marta
```

Guardiamo la dichiarazione di `informale` riga per riga.

- `Saluto informale = ...`: la variabile ha il tipo dell'interfaccia, come per qualunque oggetto di una classe che la realizza (Capitolo 10, sezione 10.2.4).
- `new Saluto() { ... }`: dopo `new` c'è `Saluto`, che è un'interfaccia e non si potrebbe istanziare da sola. Le parentesi tonde vuote sono quelle del "costruttore", e le parentesi graffe aprono il corpo della classe anonima. Tutto ciò che sta tra le graffe è il corpo di una classe che realizza `Saluto`.
- `public String saluta(String nome) { ... }`: il metodo che l'interfaccia richiede, **con `public`**, come in ogni realizzazione di un metodo d'interfaccia.
- `};`: la graffa chiude il corpo della classe, il punto e virgola chiude l'istruzione `Saluto informale = ...;`. Dimenticarlo è un errore di compilazione frequente.

La classe anonima non ha un nome, e questo ha delle conseguenze pratiche. Non si può creare un secondo oggetto della stessa classe (non c'è nome da scrivere dopo `new`). Non si può dichiarare un costruttore, perché un costruttore ha il nome della classe. Il compilatore le dà comunque un nome interno, che compare nei file generati: la prima classe anonima di `ProvaAnonima` produce il file `ProvaAnonima$1.class`, la seconda `ProvaAnonima$2.class`, e così via.

> [!NOTE]
> **Approfondimento esterno — `Class#getSimpleName` e `Class#isAnonymousClass`**
> `public String getSimpleName()` della classe `java.lang.Class` "returns the simple name of the underlying class as given in the source code. An empty string is returned if the underlying class is anonymous". Il metodo `public boolean isAnonymousClass()` restituisce `true` se e solo se la classe è anonima. `public String getName()` restituisce invece il *binary name* della classe: per una classe annidata il nome dell'esterna, un `$` e il nome della annidata, e per una anonima il nome dell'esterna e un numero progressivo scelto dal compilatore. Sono metodi d'istanza di `Class` e si ottengono con `oggetto.getClass()`.
>
> *Fonte:* [java.lang.Class#getSimpleName](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Class.html#getSimpleName()), [java.lang.Class#isAnonymousClass](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Class.html#isAnonymousClass()), [java.lang.Class#getName](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Class.html#getName())

```java
public class ProvaNomi {
    public static void main(String[] args) {
        Runnable r = new Runnable() {
            public void run() { }
        };
        System.out.println(r.getClass().getName());
        System.out.println("[" + r.getClass().getSimpleName() + "]");
        System.out.println(r.getClass().isAnonymousClass());
    }
}
```

```text
ProvaNomi$1
[]
true
```

### 11.5.3 Che cosa vede la classe anonima

Una classe anonima scritta dentro un metodo d'istanza si comporta, rispetto all'esterna, come una classe interna: vede i campi e i metodi d'istanza dell'oggetto su cui il metodo sta lavorando, privati compresi, e anche quelli `static`. Ma vede anche le **variabili locali e i parametri** del metodo in cui è scritta, con una restrizione precisa.

> [!IMPORTANT]
> **Nota per l'esame — Le variabili locali e `final`**
> Una classe anonima può usare le variabili locali (e i parametri) del metodo in cui è dichiarata solo se sono dichiarate `final`, oppure sono **`final` di fatto** (*effectively final*): cioè se, pur senza la parola `final`, nel metodo **non viene mai assegnato loro un nuovo valore** dopo l'inizializzazione. Una variabile che cambia valore da qualche parte del metodo non può essere usata dalla classe anonima.

```java
interface Saluto {
    String saluta(String nome);
}

class Registratore {
    private int chiamate = 0;                              // campo dell'oggetto esterno

    public Saluto creaSaluto(String prefisso) {            // prefisso: un parametro, mai riassegnato
        return new Saluto() {
            public String saluta(String nome) {
                chiamate++;                                // modifica il campo di Registratore
                return prefisso + " " + nome;              // legge il parametro del metodo
            }
        };
    }

    public int getChiamate() {
        return chiamate;
    }
}

public class ProvaCattura {
    public static void main(String[] args) {
        Registratore r = new Registratore();
        Saluto a = r.creaSaluto("Ciao");
        Saluto b = r.creaSaluto("Salve");

        System.out.println(a.saluta("Marta"));
        System.out.println(b.saluta("Luca"));
        System.out.println(r.getChiamate());
    }
}
```

```text
Ciao Marta
Salve Luca
2
```

Il metodo `creaSaluto` restituisce un oggetto anonimo che realizza `Saluto`. Dentro `saluta`:

- `chiamate++` modifica il campo `chiamate` dell'oggetto `Registratore` su cui è stato chiamato `creaSaluto`. Per questo, dopo le due chiamate, `r.getChiamate()` vale 2: i due saluti, `a` e `b`, appartengono entrambi a `r`.
- `prefisso` è il parametro di `creaSaluto`. L'oggetto anonimo conserva il valore di `prefisso` anche dopo che `creaSaluto` è terminato (`a` ricorda `"Ciao"`, `b` ricorda `"Salve"`): per poter garantire che quel valore non cambi mai, il compilatore pretende che sia `final` di fatto.

> [!WARNING]
> **Attenzione — Una variabile locale riassegnata non si usa nella classe anonima**
> ```java
> public static void main(String[] args) {
>     int n = 1;
>     Runnable r = new Runnable() {
>         public void run() { System.out.println(n); }     // ERRORE
>     };
>     n = 2;                                                // questa riga rende n non "final di fatto"
> }
> ```
> Il compilatore risponde `local variables referenced from an inner class must be final or effectively final`. La riga con l'errore è quella che *usa* `n` nella classe anonima, ma la causa è l'assegnamento `n = 2` altrove. Rimedio: non riassegnare la variabile, oppure copiarne il valore in una variabile nuova (`final int copia = n;`) e usare quella.

Allo stesso modo, una classe anonima scritta in un metodo `static` (come `main`) non ha un oggetto esterno, quindi non può nominare i campi d'istanza della classe che la contiene: il compilatore risponde `non-static variable x cannot be referenced from a static context`.

### 11.5.4 Classi anonime di classi astratte

La classe anonima non si limita alle interfacce: può **estendere una classe**, anche astratta, e in tal caso le parentesi dopo il nome possono contenere gli argomenti per il costruttore della superclasse. Con una classe astratta, la classe anonima è proprio la sottoclasse concreta che realizza i metodi astratti.

```java
abstract class Sconto {
    protected double percentuale;

    Sconto(double percentuale) {
        this.percentuale = percentuale;
    }

    public abstract double applica(double prezzo);
}

public class ProvaScontoAnonimo {
    public static void main(String[] args) {
        Sconto meta = new Sconto(50.0) {                   // 50.0 va al costruttore di Sconto
            public double applica(double prezzo) {
                return prezzo * (100.0 - percentuale) / 100.0;   // percentuale è protected: la vede
            }
        };

        System.out.println(meta.applica(80.0));
    }
}
```

```text
40.0
```

`new Sconto(50.0) { ... }` fa due cose in una: dichiara una sottoclasse anonima di `Sconto` che realizza `applica`, e ne crea un oggetto passando `50.0` al costruttore `Sconto(double)`. Senza il corpo tra graffe, `new Sconto(50.0)` sarebbe un errore (la classe è astratta, Capitolo 10, sezione 10.1.3).

### 11.5.5 Dove le si incontra

Il caso d'uso tipico è un oggetto a cui basta dare un comportamento una volta sola.

```java
public class ProvaRunnableAnonimo {
    public static void main(String[] args) {
        Runnable lavoro = new Runnable() {
            public void run() {
                System.out.println("lavoro eseguito");
            }
        };
        lavoro.run();            // qui run() è chiamato come un metodo qualsiasi: nessun thread parte
    }
}
```

```text
lavoro eseguito
```

È la forma in cui si scrive di solito il `Runnable` da passare a un `Thread` (`new Thread(new Runnable() { ... })`, [Capitolo 17](17-thread.md)), ed è anche il modo in cui, nelle interfacce grafiche, si scrive al volo il gestore di un evento: un gestore che serve a un solo pulsante e a un solo punto del codice, che realizza l'interfaccia dell'ascoltatore e legge i campi della finestra che lo contiene ([Capitolo 16](16-interfacce-grafiche.md)). In entrambi i casi la classe anonima è comoda perché sta accanto al codice che la usa e può leggere i campi dell'oggetto esterno senza passaggi intermedi. Quando però il comportamento serve in più punti, o è lungo, conviene dargli un nome e scriverlo come classe vera.

## 11.6 Leggere una traccia con classi annidate

Una traccia che chiede una classe annidata è fatta di frasi corte, ciascuna delle quali si traduce in una scelta di codice. Per non perdere punti conviene leggere ogni frase come un vincolo e chiedersi: **che cosa cambia nel codice se la rispetto, e che cosa se non la rispetto?**

| La traccia dice… | Nel codice significa… |
|---|---|
| "dentro la classe `X` definire una classe annidata `Y`" | `class Y` scritta **nel corpo** di `X`, non accanto e non con `extends` |
| "classe annidata **non statica**" | `class Y`, **senza** `static` (classe interna) |
| "classe annidata **statica**" | `static class Y` |
| "nessun riferimento a `X` dichiarato in `Y`" | in `Y` non ci sono campi di tipo `X`, né parametri `X` nei costruttori: `Y` usa i campi di `X` **per nome** |
| "il costruttore di `Y` riceve nell'ordine …" | i parametri nell'ordine indicato, con i tipi dedotti dalla descrizione ("testuale" = `String`, "numero con la virgola" = `double`) |
| "tutte le variabili d'istanza private" | `private` sui campi di **tutte** le classi dell'esercizio, interne comprese |
| "da `x` si costruisce un `Y`" (o simile) | `x.new Y(...)` dal `main`: quindi `Y` e il suo costruttore **non** `private` |
| "restituisce una stringa nella forma …" | la stringa esatta, con gli spazi e la punteggiatura della traccia, ottenuta con `return` (non `println`) |

Due precisazioni sulla forma, che nascono dalle regole dell'esame (un solo file, una sola classe `public`):

- La regola della classe `public` vale per le classi di **primo livello**. Una classe annidata è un membro, e può avere qualunque modificatore d'accesso: scrivere `public class Y` nel corpo di `X` non viola la regola del file.
- Il test nascosto usa le classi dall'**esterno**, con le righe di uso mostrate nell'output atteso: tutto ciò che la traccia nomina e che il test deve poter chiamare (classi, costruttori, metodi richiesti) non deve essere `private`. Il `private` si mette dove la traccia lo chiede, cioè sulle variabili d'istanza.

## Come esce all'esame

**EXAM4 — Esercizio 1 (13 punti), classi annidate e information hiding.** La traccia chiedeva una classe `Asta`, il cui costruttore riceve nell'ordine il codice dell'asta (testuale), la quota di partenza (numero con la virgola) e il nome del miglior offerente (testuale), con tutte le variabili d'istanza "rigorosamente private". Dentro `Asta` andava definita una classe annidata **non statica** `Offerta`, il cui costruttore riceve nell'ordine il nome dell'offerente e la quota offerta, anch'essa con tutte le variabili d'istanza private. Dentro `Offerta` due metodi: `stato`, senza parametri, che restituisce una stringa in un formato imposto (`"prezzo asta attuale: " + quota + "euro. miglior offerente" + nomeMigliorOfferente`), e `aggiungiOfferta`, che riceve un importo e restituisce un `boolean`: se l'importo è minore della quota attuale dell'asta restituisce `false`; altrimenti sovrascrive la quota attuale dell'asta e il nome del miglior offerente e restituisce `true`. Due **vincoli architetturali** espliciti: `Offerta` non deve essere statica, e dentro `Offerta` non va dichiarato nessun riferimento a un oggetto `Asta`. L'output atteso mostrava lo stato dell'asta (100.0, "nessuno"), poi `false` per un'offerta di 50.0, lo stesso stato, poi `true` per un'offerta di 150.0 e lo stato aggiornato (150.0, "Mario"), con un'offerta costruita "da" un'asta.

Del capitolo servono: la classe interna senza `static` (sezione 11.2.1), il collegamento implicito all'oggetto esterno che permette a `aggiungiOfferta` di **modificare i campi privati** dell'asta per nome, senza campo `Asta` dichiarato (sezioni 11.2.1 e 11.2.2), e la creazione dell'offerta "da" un'asta con `asta.new Offerta(...)` (sezione 11.2.3). Dal [Capitolo 7](07-classi-e-oggetti.md): i campi privati, l'ordine dei parametri del costruttore e la traduzione di "testuale" e "numero con la virgola" in `String` e `double`; dal [Capitolo 6](06-metodi.md) e dal Capitolo 7, un metodo che modifica lo stato e restituisce un `boolean`. Vincoli letterali da copiare dalla traccia: i nomi `Asta`, `Offerta`, `stato`, `aggiungiOfferta`; l'**ordine** dei parametri dei due costruttori; `private` su tutte le variabili d'istanza di entrambe le classi; `Offerta` non statica e senza riferimento ad `Asta`; la stringa di `stato`, con "euro. miglior offerente" **senza spazi** dopo il numero e prima del nome, esattamente come scritta.

## Scheletri da esame

### Una classe interna non statica che modifica i campi privati dell'esterna

*Quando si usa:* la traccia chiede una classe annidata **non statica** i cui metodi leggono e aggiornano lo stato della classe che la contiene, e vieta di dichiarare un riferimento alla classe esterna. Si veda la sezione 11.2.

```java
class Salvadanaio {
    private String proprietario;
    private double totale;

    public Salvadanaio(String proprietario, double totale) {
        this.proprietario = proprietario;
        this.totale = totale;
    }

    class Versamento {                                       // senza static, e nessun campo di tipo Salvadanaio
        private String nome;
        private double importo;

        public Versamento(String nome, double importo) {     // ordine dei parametri come da traccia
            this.nome = nome;
            this.importo = importo;
        }

        public String stato() {
            return "saldo " + totale + " di " + proprietario;      // campi dell'esterna, per nome
        }

        public boolean deposita(double somma) {
            if (somma < importo) {
                return false;                                // rifiutato: lo stato non cambia
            }
            totale = totale + somma;                         // modifica il campo privato dell'esterna
            proprietario = nome;
            return true;
        }
    }
}

public class ProvaSalvadanaio {
    public static void main(String[] args) {
        Salvadanaio s = new Salvadanaio("Anna", 100.0);
        Salvadanaio.Versamento v = s.new Versamento("Marco", 20.0);   // esterna.new Interna(...)

        System.out.println(v.stato());
        System.out.println(v.deposita(5.0));
        System.out.println(v.deposita(50.0));
        System.out.println(v.stato());
    }
}
```

```text
saldo 100.0 di Anna
false
true
saldo 150.0 di Marco
```

Non servono `import` né eccezioni. Punti da controllare: la classe interna sta **dentro** il corpo di quella esterna, **senza** `static`; i campi di entrambe sono `private`; la classe interna e il suo costruttore **non** sono `private`, perché il `main` li crea da fuori con `s.new Versamento(...)`; nessun campo `Salvadanaio` dentro `Versamento`; la stringa di `stato` è **restituita** (`return`) e con gli spazi della traccia.

### Il nodo come classe interna privata di una lista

*Quando si usa:* la traccia chiede una lista (o altra struttura concatenata) il cui nodo non deve essere visibile dall'esterno. Si veda la sezione 11.3.

```java
class ListaDiNumeri {
    private class Nodo {                         // privata: invisibile fuori dalla lista
        private int dato;
        private Nodo successivo;

        Nodo(int dato, Nodo successivo) {
            this.dato = dato;
            this.successivo = successivo;
        }
    }

    private Nodo testa;                          // null = lista vuota

    public void aggiungiInTesta(int n) {
        testa = new Nodo(n, testa);
    }

    public int somma() {
        int s = 0;
        for (Nodo c = testa; c != null; c = c.successivo) {   // si arriva ai campi privati di Nodo per nome
            s += c.dato;
        }
        return s;
    }
}

public class ProvaListaDiNumeri {
    public static void main(String[] args) {
        ListaDiNumeri l = new ListaDiNumeri();
        l.aggiungiInTesta(3);
        l.aggiungiInTesta(4);
        l.aggiungiInTesta(5);
        System.out.println(l.somma());
    }
}
```

```text
12
```

Non servono `import` né eccezioni. Punti da controllare: `private class Nodo` **dentro** la lista; nessun metodo pubblico della lista restituisce o riceve un `Nodo`; il percorso termina quando il riferimento è `null`.

### Una classe annidata statica, creata senza oggetto esterno

*Quando si usa:* la traccia chiede una classe annidata `static`, oppure un tipo di supporto che deve essere creato e usato senza un oggetto della classe esterna. Si veda la sezione 11.4.

```java
class Percorso {
    private static int creati = 0;                         // contatore di classe

    public static int getCreati() {
        return creati;
    }

    public static class Tappa {                            // static: nessun oggetto Percorso richiesto
        private String luogo;
        private int minuti;

        public Tappa(String luogo, int minuti) {
            this.luogo = luogo;
            this.minuti = minuti;
            creati++;                                      // campo static dell'esterna: permesso
        }

        public String toString() {
            return luogo + " (" + minuti + " min)";
        }
    }
}

public class ProvaPercorso {
    public static void main(String[] args) {
        Percorso.Tappa t = new Percorso.Tappa("Stazione", 15);   // nome qualificato, niente "oggetto.new"
        System.out.println(t);
        System.out.println(Percorso.getCreati());
    }
}
```

```text
Stazione (15 min)
1
```

Non servono `import` né eccezioni. Punti da controllare: `static class` nel corpo dell'esterna; si crea con `new Esterna.Annidata(...)`, **non** con `oggetto.new`; la classe statica non nomina i campi d'istanza dell'esterna.

### Una classe anonima che realizza un'interfaccia

*Quando si usa:* serve un oggetto che realizza un'interfaccia (o riscrive un metodo di una classe) in un solo punto del codice, senza dichiarare una classe con il nome. Si veda la sezione 11.5.

```java
interface Operazione {
    int applica(int x);
}

public class ProvaAnonimaScheletro {
    public static void main(String[] args) {
        int fattore = 3;                                   // non riassegnato: "final di fatto"

        Operazione triplica = new Operazione() {           // new Interfaccia() { corpo }
            public int applica(int x) {                    // public, come ogni realizzazione di interfaccia
                return x * fattore;
            }
        };                                                 // il ; chiude la dichiarazione della variabile

        System.out.println(triplica.applica(7));
    }
}
```

```text
21
```

Non servono `import` né eccezioni. Punti da controllare: `new Interfaccia() { ... }` con le parentesi tonde; il metodo `public` con lo stesso tipo di ritorno dell'interfaccia; il punto e virgola dopo la graffa di chiusura; le variabili locali usate nel corpo non vengono riassegnate.

## Errori tipici

Alcuni errori sono già discussi nel testo: `new Esterna.Interna()` senza oggetto esterno e `new Interna()` da un metodo `static` (sezione 11.2.3), l'omonimia di un campo con quello dell'esterna (sezione 11.2.4), `private` con un `main` fuori dall'esterna (sezione 11.2.5), `extends` al posto dell'annidamento (sezione 11.2.6), il campo d'istanza nominato da una classe statica (sezione 11.4.2), la variabile locale riassegnata (sezione 11.5.3). Seguono gli altri.

> [!CAUTION]
> **Errore tipico — Dichiarare a mano il riferimento all'oggetto esterno**
> ```java
> class Serbatoio {
>     private int litri;
>
>     class Rubinetto {
>         private Serbatoio serbatoio;                    // INUTILE, e vietato da molte tracce
>         Rubinetto(Serbatoio serbatoio) { this.serbatoio = serbatoio; }
>         void apri(int l) { serbatoio.litri += l; }
>     }
> }
> ```
> Il codice compila e funziona, ma raddoppia ciò che il linguaggio già fa: ogni oggetto interno ha già, in modo implicito, il suo oggetto esterno (sezione 11.2.2). Una traccia che dice "dentro la classe annidata non va dichiarato nessun riferimento alla classe esterna" è violata alla lettera, e l'aderenza alla traccia è ciò che il docente valuta. Forma corretta: nessun campo e nessun parametro `Serbatoio`; `void apri(int l) { litri += l; }`.

> [!CAUTION]
> **Errore tipico — `static` quando la traccia chiede una classe non statica**
> ```java
> class Serbatoio {
>     private int litri;
>     static class Rubinetto {                  // ERRORE
>         void apri(int l) { litri += l; }      // non compila
>     }
> }
> ```
> Il compilatore risponde `non-static variable litri cannot be referenced from a static context`, perché la classe statica non ha un oggetto esterno. Anche quando, aggiungendo un campo `Serbatoio` a mano, il programma torna a compilare, la traccia chiedeva una classe **non statica**: `static` va tolto, non aggirato.

> [!CAUTION]
> **Errore tipico — Creare l'interna dal `main` esterno con la sintassi della statica**
> ```java
> Serbatoio s = new Serbatoio();
> Serbatoio.Rubinetto r = new Serbatoio.Rubinetto(3);    // ERRORE
> ```
> La forma `new Esterna.Interna(...)` è quella delle classi annidate **statiche**. Per una classe interna serve l'oggetto esterno: `s.new Rubinetto(3)`. Il messaggio è `an enclosing instance that contains Serbatoio.Rubinetto is required`. Regola per ricordarla: se la classe interna ha bisogno di un oggetto esterno, quell'oggetto si scrive *davanti* a `new`.

> [!CAUTION]
> **Errore tipico — Il punto e virgola dopo la classe anonima**
> ```java
> Runnable r = new Runnable() {
>     public void run() { }
> }                                    // ERRORE: manca il ;
> System.out.println("fatto");
> ```
> Il compilatore risponde `';' expected`. La classe anonima fa parte di un'**espressione** (`new ... { ... }`), e l'istruzione che la contiene, `Runnable r = ...;`, termina con il punto e virgola dopo la graffa di chiusura.

> [!CAUTION]
> **Errore tipico — Il metodo della classe anonima senza `public`**
> ```java
> Runnable r = new Runnable() {
>     void run() { }                   // ERRORE: manca public
> };
> ```
> Il compilatore risponde `run() in <anonymous ...> cannot implement run() in Runnable` seguito da `attempting to assign weaker access privileges; was public`. I metodi di un'interfaccia sono pubblici, e chi li realizza, anche in una classe anonima, deve dichiararli `public` (Capitolo 10, sezione 10.2.3).

> [!CAUTION]
> **Errore tipico — Una classe anonima scritta come se avesse un nome**
> ```java
> Saluto s = new Saluto() {
>     public Saluto() { }              // ERRORE: un costruttore non ha nome da usare
>     public String saluta(String nome) { return nome; }
> };
> ```
> La classe anonima non ha nome, quindi non può dichiarare un costruttore: il compilatore risponde `invalid method declaration; return type required`. Quel che serve passare alla superclasse si mette tra le tonde dopo `new` (sezione 11.5.4); l'inizializzazione di un campo si fa direttamente alla sua dichiarazione.

> [!CAUTION]
> **Errore tipico — Riscrivere la stringa di una traccia a memoria**
> Quando la traccia impone il formato di una stringa (`"prezzo asta attuale: " + quota + "euro. miglior offerente" + nome`), il test nascosto la confronta carattere per carattere: uno spazio in più o in meno, un punto al posto di due punti, una maiuscola dove non c'è, e l'esecuzione è persa anche se la logica è giusta. Vale per tutte le tracce, ma è particolarmente insidioso nelle classi annidate perché la stringa sta nel metodo di una classe interna, dentro un blocco più lungo. Forma corretta: copiare il testo dalla traccia, tra virgolette, **letteralmente**, e concatenare i valori con `+` senza aggiungere spazi che la traccia non mostra.

## Riassunto

Una classe può essere dichiarata nel corpo di un'altra: è una **classe annidata**, e il rapporto con la classe esterna è di appartenenza, non di ereditarietà. Il motivo principale è l'**incapsulamento**: un tipo di supporto, come il nodo di una lista, può essere nascosto dentro la classe che lo usa, evitando la perdita di riservatezza che si avrebbe lasciandolo visibile a tutto il programma. Le forme sono tre. La **classe interna** (senza `static`) è legata a un oggetto della classe esterna: vede per nome i suoi campi e metodi, privati compresi (e viceversa l'esterna vede i membri privati dell'interna), si crea con `new Interna()` dentro la esterna o con `esterna.new Interna()` da fuori, e può nominare esplicitamente l'oggetto esterno con `Esterna.this`. La **classe annidata statica** non è legata a nessun oggetto, usa solo i membri `static` dell'esterna e si crea con `new Esterna.Annidata()`. La **classe anonima** è una classe senza nome, scritta e istanziata nello stesso punto con `new Tipo() { ... }` per realizzare un'interfaccia o estendere una classe; vede i membri dell'esterna e le variabili locali del metodo che sono `final` di fatto.

**Concetti chiave**

- **Classe annidata.** Classe dichiarata nel corpo di un'altra (l'esterna); non è una sottoclasse.
- **Classe interna.** Classe annidata senza `static`; ogni suo oggetto appartiene a un oggetto della classe esterna, in modo implicito.
- **Accesso reciproco.** L'interna usa per nome i membri dell'esterna, anche privati; l'esterna usa i membri privati dell'interna.
- **Creazione di un oggetto interno.** `new Interna(...)` dentro un metodo d'istanza dell'esterna; `esterna.new Interna(...)` dal resto del programma e dai metodi `static`; il tipo si scrive `Esterna.Interna`.
- **`Esterna.this`.** L'oggetto esterno a cui appartiene l'oggetto interno; serve quando un nome è nascosto da un campo omonimo dell'interna.
- **Interna `private`.** Visibile solo nell'esterna: nasconde un tipo di supporto, come il nodo di una lista; non può essere creata da altre classi.
- **Annidare non è ereditare.** `extends` non produce un annidamento; la relazione "appartiene a" si esprime con la classe interna.
- **Classe annidata statica.** Dichiarata con `static`; non ha oggetto esterno; usa i membri `static` dell'esterna e, con un oggetto in mano, anche quelli d'istanza; si crea con `new Esterna.Annidata(...)`.
- **Come si sceglie.** Interna se deve lavorare sui dati di un oggetto della esterna; statica se è solo un tipo di supporto autonomo.
- **Classe anonima.** Senza nome, corpo scritto subito dopo `new Tipo()`; realizza un'interfaccia o estende una classe; non ha costruttori propri; la dichiarazione che la contiene finisce con `;`.
- **Variabili locali nella classe anonima.** Utilizzabili solo se `final` o `final` di fatto (mai riassegnate).
- **File generati.** Ogni classe annidata produce un file `Esterna$Annidata.class`; le anonime `Esterna$1.class`, `Esterna$2.class`.
- **In una traccia.** "Non statica" = senza `static`; "nessun riferimento all'esterna" = nessun campo `Esterna`, si usano i nomi dei campi; "da `x` si costruisce" = `x.new Y(...)`, quindi né classe né costruttore `private`.

**Sintassi essenziale**

| Elemento | Forma |
|---|---|
| Classe interna | `class Esterna { class Interna { ... } }` |
| Classe interna privata | `class Esterna { private class Interna { ... } }` |
| Tipo di una classe annidata fuori dall'esterna | `Esterna.Interna x;` |
| Crea oggetto interno (dentro l'esterna, metodo d'istanza) | `Interna i = new Interna(...);` |
| Crea oggetto interno (da fuori, o da un metodo `static`) | `Esterna.Interna i = e.new Interna(...);` |
| L'oggetto esterno, dentro l'interna | `Esterna.this` |
| Classe annidata statica | `class Esterna { static class Annidata { ... } }` |
| Crea oggetto di una annidata statica | `Esterna.Annidata a = new Esterna.Annidata(...);` |
| Classe anonima da un'interfaccia | `Interfaccia x = new Interfaccia() { public ... metodo(...) { ... } };` |
| Classe anonima da una classe (astratta) | `Classe x = new Classe(argomenti) { ... };` |
| Nome del file `.class` generato | `Esterna$Interna.class`, `Esterna$1.class` |

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `Object` (`java.lang`) | `getClass` | `public final Class<?> getClass()` | — |
| `Class<T>` (`java.lang`) | `getName` | `public String getName()` | — |
| `Class<T>` (`java.lang`) | `getSimpleName` | `public String getSimpleName()` (stringa vuota se la classe è anonima) | — |
| `Class<T>` (`java.lang`) | `isAnonymousClass` | `public boolean isAnonymousClass()` | — |
| `Thread` (`java.lang`) | `getState` | `public Thread.State getState()` (Capitolo 17) | — |
