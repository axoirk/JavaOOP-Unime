---
materia: Programmazione a Oggetti
capitolo: 18
titolo: Sincronizzazione
livello_syllabus: 5
stato: completo
slide: ["Multithreading.pdf slide 34-48"]
appelli: [EXAM2]
fonti_esterne: 7
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 18 — Sincronizzazione

## Di cosa parla questo capitolo

Nel [Capitolo 17](17-thread.md) abbiamo imparato a far partire più thread e ad aspettarli con `join`. Tutti gli esempi di quel capitolo avevano una proprietà fortunata: ogni thread lavorava su **dati suoi** (una porzione di array, un campo del proprio `Runnable`) e i risultati venivano letti solo dopo `join`. Appena due thread devono lavorare sullo **stesso dato**, la fortuna finisce: il risultato dipende da come lo scheduler li alterna, e un programma può dare un valore diverso a ogni esecuzione. Questo capitolo spiega come si rimette ordine.

Ci sono due problemi distinti, e Java ha uno strumento per ciascuno:

- **non farsi calpestare**: se due thread modificano lo stesso oggetto, bisogna fare in modo che lo facciano *uno alla volta*. È la **mutua esclusione**, e si ottiene con la parola chiave `synchronized`;
- **aspettarsi a vicenda**: se un thread può proseguire solo quando un altro ha fatto qualcosa (un dato è stato prodotto, un posto si è liberato), deve potersi *fermare in attesa* senza sprecare il processore. È il **coordinamento**, e si ottiene con i metodi `wait`, `notify` e `notifyAll`.

In questo capitolo vedremo:

- che cos'è una **race condition** e perché un'istruzione come `i = i + 1` non è sicura (paragrafo 18.1);
- che cos'è un **lock**, e come la mutua esclusione se ne serve (paragrafo 18.2);
- i **metodi `synchronized`**: che cosa bloccano, che cosa *non* bloccano, e il caso dei metodi `static` (paragrafo 18.3);
- i **blocchi `synchronized`**, con cui si protegge solo la parte che serve e si sceglie l'oggetto di cui prendere il lock (paragrafo 18.4);
- il **deadlock** (*stallo*): come due thread si possono bloccare per sempre a vicenda (paragrafo 18.5);
- **`wait`, `notify` e `notifyAll`**: la firma esatta, che cosa fanno, perché `wait` si mette sempre dentro un `while` (paragrafo 18.6);
- lo schema **produttore/consumatore**, con un buffer a capacità limitata realizzato con un array (paragrafo 18.7);
- come **dedurre le firme** dei metodi dalle chiamate di un codice già scritto, che è esattamente quello che chiede una traccia d'esame (paragrafo 18.8);
- gli **scheletri** da saper scrivere a memoria e gli **errori tipici**.

Il capitolo si appoggia sul precedente: serve sapere che cosa sono `start`, `join` e `InterruptedException` ([Capitolo 17](17-thread.md)), e che i thread condividono lo heap ([Capitolo 8](08-riferimenti-e-memoria.md)). I metodi `wait` e `notify` sono metodi della classe `Object`, vista nel [Capitolo 9](09-ereditarieta-e-polimorfismo.md); `InterruptedException` è un'eccezione controllata ([Capitolo 13](13-eccezioni.md)); il buffer del paragrafo 18.7 usa un array ([Capitolo 5](05-array-e-matrici.md)).

> [!IMPORTANT]
> **Nota per l'esame — Sincronizzazione**
> Il coordinamento tra thread con `synchronized`, `wait` e `notify` è l'argomento di uno degli esercizi grandi: la traccia fornisce di solito le classi che *usano* una risorsa condivisa (un buffer) e chiede di scrivere la classe della risorsa. Vanno rispettate alla lettera tre cose: la **mutua esclusione** (`synchronized` su ogni metodo che tocca i dati condivisi), l'attesa con **`wait` dentro un `while`**, e la **notifica** dopo ogni modifica. Un programma che *si blocca per sempre* non dà nessun output: consuma un'esecuzione senza dire nulla. Per questo conviene capire bene i meccanismi di questo capitolo, invece di provare a tentoni.

---

## 18.1 Il problema: dati condivisi

### 18.1.1 Un contatore che non conta

Cominciamo dall'esempio più semplice che mostra il guaio. Una classe `Conteggio` ha un campo intero `i` e due metodi: `incr()` che lo aumenta di uno e `decr()` che lo diminuisce di uno. Due thread lavorano sullo **stesso** oggetto `Conteggio`: il primo chiama `incr()` centomila volte, il secondo chiama `decr()` centomila volte. Se ogni incremento è seguito (prima o poi) da un decremento, alla fine il valore deve tornare a zero.

```java
class Conteggio {
    int i = 0;

    void incr() {
        i = i + 1;
    }

    void decr() {
        i = i - 1;
    }
}

class Sale implements Runnable {
    private Conteggio c;                     // lo stesso oggetto per entrambi i thread

    Sale(Conteggio c) {
        this.c = c;
    }

    public void run() {
        for (int k = 0; k < 100000; k++) {
            c.incr();
        }
    }
}

class Scende implements Runnable {
    private Conteggio c;

    Scende(Conteggio c) {
        this.c = c;
    }

    public void run() {
        for (int k = 0; k < 100000; k++) {
            c.decr();
        }
    }
}

public class SenzaMutuaEsclusione {
    public static void main(String[] args) throws InterruptedException {
        Conteggio c = new Conteggio();         // un solo oggetto...
        Thread t1 = new Thread(new Sale(c));   // ...passato a entrambi i Runnable
        Thread t2 = new Thread(new Scende(c));
        t1.start();
        t2.start();
        t1.join();                             // aspettiamo che finiscano entrambi
        t2.join();
        System.out.println("Valore finale: " + c.i);
    }
}
```

Spieghiamo il programma riga per riga. `Sale` e `Scende` sono due classi che realizzano `Runnable` ([Capitolo 17](17-thread.md), paragrafo 17.3.2); ciascuna riceve nel costruttore **lo stesso** oggetto `Conteggio` e chiama su di esso `incr()` o `decr()` centomila volte. Nel `main` si crea **un solo** `Conteggio`, lo si passa a entrambi, si avviano i due thread e si attende la fine di tutti e due con `join`, perché si vuole stampare il valore finale *dopo* che il lavoro è concluso.

Il valore atteso è `0`. Il valore che si ottiene è un altro, e **cambia a ogni esecuzione**. Tre esecuzioni consecutive su una macchina di prova hanno dato:

```text
Valore finale: -1112
Valore finale: -2553
Valore finale: -5261
```

I numeri sulla vostra macchina saranno diversi (e in qualche esecuzione fortunata potrebbe uscire anche `0`): è proprio questo il punto, perché il risultato non dipende dal programma ma da **come lo scheduler ha alternato i due thread**.

### 18.1.2 Perché `i = i + 1` non è sicuro

L'istruzione `i = i + 1` sembra una cosa sola, ma per il processore è una **sequenza di passi**:

1. **leggere** il valore corrente di `i`;
2. **calcolare** il valore più uno;
3. **riscrivere** il risultato in `i`.

Lo scheduler può togliere la CPU a un thread **tra un passo e l'altro**. Vediamo che cosa può succedere se il thread 1 (che esegue `incr`) e il thread 2 (che esegue `decr`) si alternano nel momento sbagliato, partendo da `i = 0`:

| Passo | Thread 1 (`incr`) | Thread 2 (`decr`) | Valore di `i` in memoria |
|---|---|---|---|
| 1 | legge `i` e trova 0 | | 0 |
| 2 | | legge `i` e trova 0 | 0 |
| 3 | calcola 0 + 1 e scrive 1 | | 1 |
| 4 | | calcola 0 − 1 e scrive −1 | −1 |

Un incremento e un decremento sono stati eseguiti, quindi `i` dovrebbe valere 0; invece vale −1. L'incremento del thread 1 è stato **perso**: il thread 2 aveva già letto il vecchio valore 0 e, quando ha scritto il proprio risultato, ha cancellato quello scritto dal thread 1. Il valore finale dipende dalla sequenza di esecuzione, e con centomila ripetizioni per thread questi piccoli incidenti si accumulano fino ai numeri che abbiamo visto.

> [!NOTE]
> **Definizione — Race condition e operazione atomica**
> Una **race condition** (*situazione di competizione*) si verifica quando due o più thread eseguono contemporaneamente operazioni sugli stessi dati, di cui almeno una **non è atomica**: l'ordine con cui i passi delle operazioni vengono eseguiti dai diversi thread può alterare il risultato dell'intera operazione.
> Un'operazione è **atomica** se viene eseguita *per intero* o *per niente*, senza che altri thread possano inserirsi a metà.

Notiamo che `contatore++` e `i--` non sono diversi da `i = i + 1`: anche loro sono operazioni composte da lettura, calcolo e scrittura, e quindi non atomiche. È lo stesso errore che avevamo già visto con due thread su uno stesso contatore ([Capitolo 17](17-thread.md), paragrafo 17.6.5): lì avevamo anticipato che per correggerlo non basta `volatile`, e ora vediamo che cosa serve.

> [!TIP]
> **Intuizione — Due persone che aggiornano lo stesso foglio**
> Immaginiamo un foglio con scritto un numero e due persone che devono aumentarlo o diminuirlo di uno. Ognuna legge il numero, fa il conto a mente, cancella il vecchio valore e scrive il nuovo. Se tutte e due leggono il foglio *prima* che l'altra abbia scritto, la seconda a scrivere cancella il lavoro della prima. Per evitare il pasticcio basta una regola: **una persona alla volta** può avere in mano il foglio, dalla lettura alla scrittura. È esattamente la regola che imporremo ai thread.

### 18.1.3 Quando il problema non c'è

La race condition richiede che **più thread tocchino lo stesso dato** e che almeno uno lo **modifichi**. Se queste condizioni non ci sono, non serve nessuna sincronizzazione:

- se i thread lavorano ciascuno su **dati propri** (la partizione di un array del [Capitolo 17](17-thread.md), paragrafo 17.6.2, in cui ogni thread legge solo la sua porzione e scrive solo nel proprio campo), non c'è conflitto;
- se i thread **leggono soltanto** un dato che nessuno modifica, non c'è conflitto;
- le **variabili locali** di un metodo vivono nello stack del thread che lo esegue ([Capitolo 8](08-riferimenti-e-memoria.md)) e non sono condivise.

Quando invece un oggetto sullo heap è raggiunto da più thread e almeno uno lo modifica, il programmatore deve proteggerlo. Vediamo come.

---

## 18.2 Mutua esclusione e lock

### 18.2.1 L'idea: la chiave del bagno

Per risolvere la race condition serve che l'operazione complessa (leggi, calcola, scrivi) sia effettuata **per intero da un thread alla volta**, senza che istruzioni relative alla stessa operazione, eseguite da un altro thread, si inseriscano nel mezzo. Questa proprietà si chiama **mutua esclusione** (*mutual exclusion*): se un thread sta eseguendo l'operazione, gli altri sono *esclusi* finché non ha finito.

Per realizzarla si usa un **lock** (in italiano "lucchetto" o "serratura"; il termine inglese è quello d'uso). L'analogia più chiara è la chiave di un bagno: alla toilette accede una sola persona alla volta, che una volta entrata chiude la porta a chiave; le altre persone trovano la porta chiusa e devono attendere l'uscita di chi c'è dentro. L'analogia funziona fino a un certo punto: una persona che aspetta fuori non fa nulla, mentre un thread in attesa è *sospeso* dal sistema, che non gli assegna tempo di CPU finché il lock non si libera.

> [!NOTE]
> **Definizione — Lock**
> Un **lock** è un meccanismo che garantisce che un certo codice sia eseguito da **un solo thread alla volta**. Si può pensare a una variabile booleana visibile a tutti i thread: quando un thread inizia a eseguire il codice protetto, il lock risulta "preso" e si dice che il thread ha **acquisito** il lock; finché lo possiede, nessun altro thread può entrare in quel codice, e chi lo richiede viene messo in attesa. Quando il thread esce dal codice protetto, **rilascia** il lock e uno dei thread in attesa può entrare.

Il meccanismo di schedulazione si fa carico di garantire tutto questo: nessun thread potrà accedere al codice protetto finché un altro ne possiede il lock.

### 18.2.2 In Java: ogni oggetto ha un lock

In Java il programmatore **non maneggia direttamente i lock**: l'accesso avviene "dietro le quinte", tramite la parola chiave **`synchronized`**. Il modello è questo: **ogni oggetto ha un proprio lock** (nella documentazione ufficiale si parla di *monitor* dell'oggetto, e i due termini si usano come sinonimi). Quando un thread entra in un metodo o in un blocco `synchronized`, acquisisce il lock dell'oggetto indicato; quando ne esce, lo rilascia.

La documentazione ufficiale dice con precisione quando un thread è il "proprietario" (*owner*) del monitor di un oggetto, e che il proprietario può essere uno solo:

> [!NOTE]
> **Approfondimento esterno — Il proprietario del monitor di un oggetto**
> Un thread diventa proprietario del monitor di un oggetto in uno di questi tre modi:
> - eseguendo un metodo `synchronized` di istanza di quell'oggetto;
> - eseguendo il corpo di un'istruzione `synchronized` che sincronizza su quell'oggetto;
> - per gli oggetti di tipo `Class`, eseguendo un metodo `static synchronized` di quella classe.
>
> Solo un thread alla volta può essere proprietario del monitor di un oggetto.
>
> *Fonte:* [Object.notify() — Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#notify())

Che cosa succede a un thread che trova il lock occupato? Si ferma e resta in attesa: nella terminologia del [Capitolo 17](17-thread.md), paragrafo 17.4.2, si trova nello stato **`BLOCKED`**. Quando il thread che possiede il lock esce dal codice protetto e lo rilascia, il thread in attesa acquisisce il lock, diventa proprietario ed esegue a sua volta il codice. La sequenza, vista nel tempo, è questa: il thread 1 accede al metodo e riceve il lock; esegue; nel frattempo il thread 2 prova ad accedere al metodo, non riceve il lock e viene sospeso in attesa; il thread 1 termina il metodo e rilascia il lock; il thread 2 riceve la notifica, accede al metodo e riceve il lock.

> [!NOTE]
> **Approfondimento esterno — Lo stato `BLOCKED`**
> `Thread.State.BLOCKED` è lo stato di un thread bloccato in attesa di un monitor lock. Un thread in questo stato sta aspettando un monitor lock per **entrare** in un blocco o metodo `synchronized`, oppure per **rientrarvi** dopo aver chiamato `Object.wait`.
>
> *Fonte:* [Thread.State — Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.State.html)

---

## 18.3 I metodi `synchronized`

### 18.3.1 Il modificatore `synchronized`

La forma più semplice di mutua esclusione è mettere il modificatore **`synchronized`** nella dichiarazione di un metodo.

> [!NOTE]
> **Definizione — Metodo `synchronized`**
> Il modificatore `synchronized` prescrive che il metodo a cui si applica sia eseguito da **un solo thread alla volta**:
> - quando un thread inizia a eseguire un metodo `synchronized`, viene fatto il **lock dell'oggetto** a cui appartiene il metodo (per i metodi `static`, il lock della **classe**);
> - quando il thread termina l'esecuzione del metodo, viene fatto l'**unlock**;
> - finché l'unlock non è avvenuto, gli altri thread che vogliono eseguire un metodo `synchronized` *dello stesso oggetto* si pongono in attesa.

Sintatticamente `synchronized` è un modificatore come `public` o `static` e si scrive prima del tipo di ritorno. Nel codice d'esame la forma da usare è:

```java
public synchronized void incr() {
    i = i + 1;
}
```

Il rilascio del lock è automatico: avviene quando il metodo **termina**, sia perché arriva alla fine o a un `return`, sia perché lascia il metodo un'eccezione. Il programmatore non deve (e non può) "dimenticare" di rilasciarlo.

### 18.3.2 Il contatore corretto

Correggiamo `Conteggio` aggiungendo `synchronized` ai due metodi. Tutto il resto del programma (le classi `Sale` e `Scende` e il `main`) rimane identico: cambia solo la dichiarazione dei due metodi.

```java
class Conteggio {
    int i = 0;

    synchronized void incr() {
        i = i + 1;
    }

    synchronized void decr() {
        i = i - 1;
    }
}
```

Ripetendo l'esperimento del paragrafo 18.1.1 con questa classe, l'output è sempre lo stesso:

```text
Valore finale: 0
```

Vediamo perché. Il thread 1 chiama `c.incr()`: acquisisce il lock dell'oggetto `c`. Se in quel momento il thread 2 chiama `c.decr()`, trova il lock occupato (è lo stesso oggetto `c`, e `decr` è `synchronized`) e si ferma. Quando il thread 1 finisce `incr`, rilascia il lock e il thread 2 può eseguire `decr`. Le tre operazioni leggi–calcola–scrivi di un metodo non possono più essere intrecciate con quelle dell'altro. Il valore finale non dipende più dalla sequenza di esecuzione.

Osserviamo due dettagli. Primo: `incr` e `decr` si escludono **a vicenda**, non solo ciascuno con sé stesso: hanno lo stesso lock, quello dell'oggetto `c`. Secondo: la mutua esclusione non fissa l'**ordine** in cui i thread eseguono le operazioni, ma garantisce che ciascuna venga eseguita per intero. Qui l'ordine non conta, perché somma e sottrazione di uno danno comunque 0 alla fine.

### 18.3.3 Il lock è dell'oggetto, non del metodo

Un'idea sbagliata comune è che `synchronized` "blocchi il metodo". In realtà blocca **l'oggetto**: ciò che si acquisisce è il lock dell'oggetto su cui il metodo viene eseguito. Ne seguono tre conseguenze, che conviene vedere con un esperimento. La classe `Cassetto` ha un metodo `lento()` che dura mezzo secondo e un metodo `veloce()`, entrambi `synchronized`:

```java
class Cassetto {
    private String nome;

    Cassetto(String nome) {
        this.nome = nome;
    }

    synchronized void lento() {
        System.out.println(nome + ": lento() inizia");
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
        }
        System.out.println(nome + ": lento() finisce");
    }

    synchronized void veloce() {
        System.out.println(nome + ": veloce()");
    }
}

public class ProvaCassetto {
    public static void main(String[] args) throws InterruptedException {
        final Cassetto a = new Cassetto("A");
        Cassetto b = new Cassetto("B");

        Thread t = new Thread(new Runnable() {
            public void run() {
                a.lento();
            }
        });
        t.start();
        Thread.sleep(100);          // lascia al thread il tempo di entrare in a.lento()

        b.veloce();                 // altro oggetto, altro lock: passa subito
        a.veloce();                 // stesso oggetto, stesso lock: deve aspettare
        t.join();
    }
}
```

Il `main` avvia un thread che esegue `a.lento()` (il thread possiede il lock di `a` per mezzo secondo), attende 100 millisecondi per essere sicuro che il thread sia entrato nel metodo, e poi chiama `veloce()` prima su `b` e poi su `a`. La classe anonima che realizza `Runnable` è quella del [Capitolo 11](11-classi-annidate.md); la variabile `a` è dichiarata `final` perché la classe anonima la usa. L'output è:

```text
A: lento() inizia
B: veloce()
A: lento() finisce
A: veloce()
```

`B: veloce()` compare subito, mentre `A: veloce()` compare **dopo** `A: lento() finisce`. Ne ricaviamo le tre conseguenze:

1. **Oggetti diversi, lock diversi.** `b.veloce()` non è fermato dal thread che possiede il lock di `a`: sono due oggetti, ciascuno con il suo lock. Due thread che lavorano su oggetti diversi non si disturbano.
2. **Tutti i metodi `synchronized` di uno stesso oggetto condividono lo stesso lock.** `a.veloce()` è un metodo diverso da `a.lento()`, ma poiché l'oggetto è lo stesso, deve aspettare. In un oggetto con più metodi `synchronized`, **uno solo alla volta** può essere in esecuzione, qualunque sia.
3. **Un metodo non `synchronized` non aspetta nessuno.** Se `veloce()` non fosse stato `synchronized`, `a.veloce()` sarebbe partito subito, senza guardare il lock. Il lock protegge soltanto chi lo chiede.

Dalla terza conseguenza discende una regola importante, che useremo di continuo: **tutti i metodi che leggono o modificano il dato condiviso devono essere `synchronized`**, compresi i getter. Se un metodo `incr` è sincronizzato ma un metodo `getValore` che legge `i` non lo è, il getter può leggere il valore mentre un altro thread sta a metà di un aggiornamento (e, come vedremo al paragrafo 18.3.6, può addirittura non vedere il valore aggiornato).

> [!WARNING]
> **Attenzione — Il lock non protegge i dati, protegge il codice che lo chiede**
> Il lock dell'oggetto non rende "speciale" il campo `i`: un'altra classe che accedesse direttamente a `c.i` (se il campo non è `private`) passerebbe attraverso il lock senza chiedere nulla. Per questo i dati condivisi si dichiarano `private` ([Capitolo 7](07-classi-e-oggetti.md), paragrafo 7.3) e si tocca **solo** dai metodi `synchronized` della classe. L'esempio del paragrafo 18.1 lascia `i` visibile per poterlo stampare dal `main`; nel codice vero si aggiunge un getter `synchronized`.

### 18.3.4 I metodi `static synchronized`

Un metodo `static` non appartiene a nessun oggetto: non ha un `this`. Quale lock acquisisce, allora, se è dichiarato `synchronized`? Quello della **classe**: ogni classe ha un oggetto di tipo `Class` (che la rappresenta nella JVM) e, come ogni oggetto, ha il suo lock. Se il metodo è `static synchronized`, il thread acquisisce il lock dell'oggetto `Class` della classe, che è **uno solo per tutta la classe**, indipendentemente da quante istanze ne siano state create.

La conseguenza è che i metodi `synchronized` di istanza e quelli `static synchronized` **non si escludono a vicenda**: usano due lock diversi (quello dell'istanza e quello della classe). L'esperimento lo mostra. La classe `Doppio` ha un metodo `static synchronized` che dura mezzo secondo e un metodo `synchronized` di istanza:

```java
class Doppio {
    static synchronized void sullaClasse() {
        System.out.println("classe: inizia");
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
        }
        System.out.println("classe: finisce");
    }

    synchronized void sullIstanza() {
        System.out.println("istanza: eseguito");
    }
}

public class ProvaClasse {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(new Runnable() {
            public void run() {
                Doppio.sullaClasse();
            }
        });
        t.start();
        Thread.sleep(100);               // il thread è dentro sullaClasse()
        new Doppio().sullIstanza();      // lock diverso: non aspetta
        t.join();
    }
}
```

```text
classe: inizia
istanza: eseguito
classe: finisce
```

Il metodo di istanza è stato eseguito mentre il metodo statico era ancora in corso. Se invece vogliamo che le due cose si escludano, dobbiamo far prendere a entrambi lo stesso lock: lo vedremo con i blocchi `synchronized` (paragrafo 18.4.2).

Questa è anche la ragione per cui un contatore **`static`** (condiviso da tutte le istanze) non si protegge con un metodo `synchronized` *di istanza*: due istanze diverse avrebbero due lock diversi e continuerebbero a pestarsi i piedi. Un campo `static` si protegge con un metodo `static synchronized`.

### 18.3.5 Un metodo sincronizzato può chiamarne un altro dello stesso oggetto

Poiché il lock appartiene all'oggetto, ci si può chiedere se un metodo `synchronized` possa chiamarne un altro, `synchronized` anch'esso e dello stesso oggetto: il thread possiede già il lock, quindi dovrebbe aspettare sé stesso? La risposta è no: un thread che possiede già il lock di un oggetto può entrare in un altro metodo `synchronized` dello **stesso** oggetto senza bloccarsi.

```java
class Rientro {
    synchronized void esterno() {
        System.out.println("esterno: entrato");
        interno();                                   // stesso oggetto: nessun blocco
        System.out.println("esterno: fine");
    }

    synchronized void interno() {
        System.out.println("interno: entrato");
    }
}

public class ProvaRientro {
    public static void main(String[] args) {
        new Rientro().esterno();
    }
}
```

```text
esterno: entrato
interno: entrato
esterno: fine
```

Questo è il motivo per cui possiamo scrivere liberamente metodi `synchronized` che si richiamano tra loro (per esempio un metodo che inserisce e che richiama un metodo che controlla se il buffer è pieno) senza paura di bloccarci da soli. Il pericolo di bloccarsi esiste invece quando i lock in gioco sono di **oggetti diversi**, ed è il deadlock del paragrafo 18.5.

### 18.3.6 `synchronized` e visibilità

La mutua esclusione non è l'unico effetto di `synchronized`. Nel [Capitolo 17](17-thread.md), paragrafo 17.4.4, avevamo visto che la modifica di un campo fatta da un thread non è garantita visibile agli altri, a meno di usare `volatile`. Anche `synchronized` dà questa garanzia: la documentazione ufficiale dice che il rilascio di un monitor (l'uscita da un metodo o da un blocco `synchronized`) *avviene prima* di ogni successiva acquisizione dello stesso monitor.

> [!NOTE]
> **Approfondimento esterno — `synchronized` e visibilità delle modifiche**
> Il risultato di una scrittura fatta da un thread è garantito visibile a una lettura fatta da un altro thread solo se la scrittura *happens-before* la lettura (*avviene prima*). I costrutti `synchronized` e `volatile`, e i metodi `Thread.start()` e `Thread.join()`, possono formare relazioni *happens-before*. In particolare: un *unlock* (uscita da un blocco o da un metodo `synchronized`) di un monitor *happens-before* ogni successivo *lock* (ingresso in un blocco o metodo `synchronized`) **dello stesso monitor**. E poiché la relazione è transitiva, tutte le azioni di un thread precedenti all'*unlock* avvengono prima di tutte le azioni successive di qualunque thread acquisisca quel monitor.
>
> *Fonte:* [Package java.util.concurrent — Memory Consistency Properties, Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/package-summary.html)

In pratica: se tutti gli accessi a un dato condiviso (letture comprese) avvengono dentro metodi `synchronized` *dello stesso oggetto*, ogni thread vede l'ultimo valore scritto da chi è passato prima. È un'altra ragione per sincronizzare anche i getter.

### 18.3.7 Tenere il lock il meno possibile

Un thread che possiede un lock fa aspettare tutti gli altri thread che lo vogliono. Ne segue che il codice protetto va tenuto **breve**, e in particolare che dentro un metodo `synchronized` non si dovrebbero fare attese lunghe. Il [Capitolo 17](17-thread.md), paragrafo 17.5.2, ha già ricordato che `sleep` **non rilascia i lock**: se un thread si addormenta dentro un metodo `synchronized`, tutti gli altri thread che vogliono quell'oggetto aspettano per tutta la durata del sonno. Lo verifichiamo misurando il tempo di attesa:

```java
class Sala {
    synchronized void occupa() {
        try {
            Thread.sleep(400);           // dorme TENENDO il lock
        } catch (InterruptedException e) {
        }
    }

    synchronized void entra() {
        // non fa nulla: serve solo ad acquisire il lock
    }
}

public class ProvaSonno {
    public static void main(String[] args) throws InterruptedException {
        final Sala s = new Sala();
        Thread t = new Thread(new Runnable() {
            public void run() {
                s.occupa();
            }
        });
        t.start();
        Thread.sleep(100);                           // il thread è già dentro occupa()

        long inizio = System.currentTimeMillis();
        s.entra();                                   // deve aspettare la fine del sonno
        long attesa = System.currentTimeMillis() - inizio;

        System.out.println("Attesa di almeno 250 ms: " + (attesa >= 250));
        t.join();
    }
}
```

```text
Attesa di almeno 250 ms: true
```

Il metodo `entra()` è vuoto, eppure il `main` ha dovuto attendere circa 300 millisecondi (i 400 del sonno meno i 100 trascorsi prima): è il tempo in cui il thread dormiva con il lock in mano. Come regola, in un metodo `synchronized` si lasciano soltanto le istruzioni che toccano il dato condiviso; i calcoli lunghi si fanno fuori. Per proteggere *solo una parte* di un metodo servono i blocchi `synchronized`.

---

## 18.4 I blocchi `synchronized`

### 18.4.1 La sintassi e l'equivalenza con il metodo

La parola chiave `synchronized` si può usare anche per proteggere **blocchi arbitrari** di codice, e non solo interi metodi. In questo caso occorre specificare **l'oggetto di cui acquisire il lock**, tra parentesi tonde:

```java
synchronized (oggetto) {
    // blocco di istruzioni protette dal lock di "oggetto"
}
```

Il thread acquisisce il lock di `oggetto` all'ingresso nel blocco e lo rilascia all'uscita (anche se si esce per un'eccezione). Un metodo `synchronized` è soltanto una scrittura abbreviata di un blocco che copre tutto il corpo e sincronizza su `this`: le due forme seguenti sono equivalenti.

```java
synchronized void metodo() {
    // corpo
}

void metodo() {
    synchronized (this) {
        // corpo
    }
}
```

Tra le parentesi ci deve essere un **riferimento a un oggetto**: un tipo primitivo non è ammesso (`synchronized (x)` con `int x` non compila), e un riferimento `null` lancia una `NullPointerException` a runtime.

### 18.4.2 Perché usare un blocco

Il blocco `synchronized` serve in tre situazioni.

**Proteggere solo la parte che serve.** Se un metodo fa un calcolo lungo e solo alla fine aggiorna un dato condiviso, non c'è motivo di tenere il lock per tutta la durata del calcolo (si veda il paragrafo 18.3.7): si sincronizza solo l'aggiornamento.

**Scegliere un lock diverso da `this`.** A volte il dato condiviso non è un campo della classe che sta eseguendo il codice, ma un oggetto *separato* passato a tutti i thread. In questo caso si prende il lock proprio di quell'oggetto. Vediamo un esempio: quattro thread sommano ciascuno una porzione di un array e aggiungono il proprio risultato parziale a un totale condiviso.

```java
class Totale {
    int valore = 0;                              // il dato condiviso
}

class SommaParte implements Runnable {
    private int[] dati;
    private int da;                              // primo indice (incluso)
    private int fino;                            // ultimo indice (escluso)
    private Totale totale;

    SommaParte(int[] dati, int da, int fino, Totale totale) {
        this.dati = dati;
        this.da = da;
        this.fino = fino;
        this.totale = totale;
    }

    public void run() {
        int parziale = 0;
        for (int k = da; k < fino; k++) {        // calcolo fuori dal lock
            parziale = parziale + dati[k];
        }
        synchronized (totale) {                  // lock dell'oggetto condiviso
            totale.valore = totale.valore + parziale;
        }
    }
}

public class ProvaTotale {
    public static void main(String[] args) throws InterruptedException {
        int[] dati = new int[1000];
        for (int k = 0; k < dati.length; k++) {
            dati[k] = k + 1;                     // 1, 2, ..., 1000
        }
        Totale totale = new Totale();

        Thread[] thread = new Thread[4];
        for (int k = 0; k < thread.length; k++) {
            thread[k] = new Thread(new SommaParte(dati, k * 250, (k + 1) * 250, totale));
            thread[k].start();                   // primo ciclo: avvia tutti
        }
        for (int k = 0; k < thread.length; k++) {
            thread[k].join();                    // secondo ciclo: aspetta tutti
        }
        System.out.println("Somma: " + totale.valore);
    }
}
```

Il calcolo della somma parziale, che è la parte lunga, avviene **fuori** dal blocco e quindi in parallelo vero tra i quattro thread. Solo l'istruzione `totale.valore = totale.valore + parziale`, che è il punto in cui si tocca il dato condiviso (ed è una lettura–calcolo–scrittura, quindi a rischio), è protetta, e il lock che si prende è quello dell'oggetto `Totale`, lo stesso per tutti i thread. Il `main` usa il modello *avvia tutti, poi aspetta tutti* del [Capitolo 17](17-thread.md), paragrafo 17.6.2. L'output è sempre:

```text
Somma: 500500
```

Se invece di `synchronized (totale)` avessimo scritto `synchronized (this)`, ogni thread avrebbe preso il lock del *proprio* `SommaParte` (ce n'è uno per thread): quattro lock diversi, nessuna esclusione, e il totale potrebbe uscire sbagliato. La scelta dell'oggetto non è un dettaglio: **per escludersi, i thread devono prendere lo stesso lock**.

**Far escludere un metodo statico e uno di istanza.** Per far prendere lo stesso lock a un metodo `static` e a uno di istanza si sincronizza su un oggetto comune, per esempio sull'oggetto `Class`, che si scrive `NomeClasse.class`:

```java
class Registro {
    private static int totale = 0;

    static void aggiungiStatico(int n) {
        synchronized (Registro.class) {          // lock della classe, come static synchronized
            totale = totale + n;
        }
    }

    void aggiungiIstanza(int n) {
        synchronized (Registro.class) {          // STESSO lock: i due metodi si escludono
            totale = totale + n;
        }
    }
}
```

Un metodo `static synchronized` equivale a un blocco `synchronized (NomeClasse.class)` che copre tutto il corpo.

**Usare un oggetto privato come lock.** Uno schema molto diffuso consiste nel dedicare al lock un oggetto qualunque, creato apposta e mai esposto all'esterno:

```java
class ContoCorrente {
    private final Object lock = new Object();    // serve solo come lock
    private int saldo = 0;

    void versa(int importo) {
        synchronized (lock) {
            saldo = saldo + importo;
        }
    }

    int getSaldo() {
        synchronized (lock) {
            return saldo;
        }
    }
}
```

L'oggetto `Object` ([Capitolo 9](09-ereditarieta-e-polimorfismo.md), paragrafo 9.7) non ha altro scopo che fare da chiave; il campo è `private final`, quindi nessun codice esterno può prendere lo stesso lock per interferire. Notiamo che anche il getter prende il lock, per i motivi del paragrafo 18.3.3.

### 18.4.3 Un esempio: la coda di messaggi

Un esempio classico: una coda di messaggi condivisa tra thread, con un metodo per inserire (`send`) e uno per estrarre (`receive`). Tutta la struttura dati è privata e si accede soltanto da metodi `synchronized`. Il metodo `receive` restituisce `null` se la coda è vuota.

```java
import java.util.ArrayList;

class CodaMessaggi {
    private ArrayList<Object> coda = new ArrayList<Object>();

    public synchronized void send(Object obj) {
        coda.add(obj);                           // inserisce in fondo
    }

    public synchronized Object receive() {
        if (coda.size() == 0) {
            return null;                         // nessun messaggio
        }
        return coda.remove(0);                   // toglie e restituisce il primo
    }
}

class Mittente implements Runnable {
    private CodaMessaggi coda;
    private String nome;

    Mittente(CodaMessaggi coda, String nome) {
        this.coda = coda;
        this.nome = nome;
    }

    public void run() {
        for (int k = 0; k < 1000; k++) {
            coda.send(nome + "-" + k);
        }
    }
}

public class ProvaCoda {
    public static void main(String[] args) throws InterruptedException {
        CodaMessaggi coda = new CodaMessaggi();
        Thread a = new Thread(new Mittente(coda, "A"));
        Thread b = new Thread(new Mittente(coda, "B"));
        a.start();
        b.start();
        a.join();
        b.join();

        int ricevuti = 0;
        while (coda.receive() != null) {
            ricevuti++;
        }
        System.out.println("Messaggi ricevuti: " + ricevuti);
    }
}
```

```text
Messaggi ricevuti: 2000
```

Due thread inseriscono mille messaggi ciascuno nella stessa coda; dopo i `join`, il `main` li estrae finché `receive` non restituisce `null`. Ne trova esattamente 2000. L'`ArrayList` ([Capitolo 12](12-generics-e-collezioni.md)) di per sé non è pensata per l'uso da più thread: è la sincronizzazione dei **nostri** metodi `send` e `receive` che rende la coda sicura. Questo modo di scrivere (la struttura dati è un dettaglio privato, tutti i metodi che la toccano sono `synchronized`) è il modello di tutta la sincronizzazione che incontreremo.

Notiamo che `receive` non aspetta quando la coda è vuota: restituisce `null` e basta. A volte è ciò che serve. Quando invece il thread deve *aspettare* che arrivi un messaggio, servono `wait` e `notify`, e ci arriviamo al paragrafo 18.6.

---

## 18.5 Il deadlock

### 18.5.1 Che cos'è

La mutua esclusione risolve un problema, ma ne porta con sé un altro. Un thread che possiede un lock e ne chiede un secondo, mentre un altro thread possiede il secondo e chiede il primo, resta bloccato per sempre.

> [!NOTE]
> **Definizione — Deadlock**
> Un **deadlock** (*stallo*, o *blocco critico*) è una situazione in cui due o più thread (o processi) si trovano **in attesa l'uno dell'altro**, in maniera tale che gli eventi attesi non potranno mai verificarsi.

Il linguaggio non offre mezzi particolari per prevenirlo, né regole generali e precise da seguire: si tratta di esaminare con attenzione le possibili interazioni fra thread e tenerne conto nell'implementazione delle classi. Quello che possiamo fare è imparare a riconoscere la struttura tipica di uno stallo, e per farlo studiamo un esempio completo.

### 18.5.2 Un esempio

La classe `Stallo` realizza `Runnable` e ha un campo `altro` che punta a un altro oggetto `Stallo`. Il suo metodo `run` è `synchronized`: prende il lock di `this`, si ferma mezzo secondo e poi chiama il metodo `sincronizzato()` dell'**altro** oggetto, anch'esso `synchronized`.

```java
public class Stallo implements Runnable {
    Stallo altro;                                // l'oggetto "avversario"

    public static void main(String[] args) {
        Stallo d1 = new Stallo();
        Stallo d2 = new Stallo();
        Thread t1 = new Thread(d1);              // t1 esegue d1.run()
        Thread t2 = new Thread(d2);              // t2 esegue d2.run()
        d1.altro = d2;                           // d1 e d2 si "vedono"
        d2.altro = d1;
        t1.start();
        t2.start();
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
        }
        System.out.println("Fine");
    }

    public synchronized void run() {
        try {
            Thread.sleep(500);                   // dorme TENENDO il lock di this
        } catch (InterruptedException e) {
        }
        altro.sincronizzato();                   // chiede il lock dell'altro oggetto
    }

    public synchronized void sincronizzato() {
        System.out.println("in sincronizzato");
    }
}
```

Eseguendolo, **non compare nessuna riga**: né `in sincronizzato`, né `Fine`. Il programma non termina e non segnala alcuna eccezione; resta fermo finché non lo si interrompe a mano (in un terminale con `Ctrl+C`; all'esame, con una delle cinque esecuzioni sprecata). Seguiamo i thread nel tempo:

| Istante | Thread `t1` | Thread `t2` |
|---|---|---|
| 0 | esegue `d1.run()`: acquisisce il lock di `d1` | esegue `d2.run()`: acquisisce il lock di `d2` |
| 0 - 500 ms | dorme, **tenendo** il lock di `d1` | dorme, **tenendo** il lock di `d2` |
| 500 ms | si sveglia e chiama `d2.sincronizzato()`: serve il lock di `d2`, ma lo possiede `t2` → **si blocca** | si sveglia e chiama `d1.sincronizzato()`: serve il lock di `d1`, ma lo possiede `t1` → **si blocca** |
| dopo | aspetta il lock di `d2` | aspetta il lock di `d1` |

`t1` aspetta un lock che `t2` rilascerà solo uscendo da `run`; ma `t2` non può uscire da `run` finché non ottiene il lock di `d1`, che `t1` rilascerà solo uscendo da `run`. Poiché i thread si aspettano a vicenda, nessuno dei due riprende mai l'esecuzione. Anche il `main`, che sta aspettando i due thread con `join`, resta bloccato.

L'attesa di 500 millisecondi nel metodo `run` serve per costruire l'esempio: garantisce che entrambi i thread abbiano preso il proprio lock *prima* che uno dei due chieda quello dell'altro. Senza di essa, un thread potrebbe fare in tempo a completare `run` (e a rilasciare tutto) prima che l'altro parta, e il programma potrebbe funzionare, magari per mille esecuzioni di fila, per poi bloccarsi in una esecuzione sfortunata. È ciò che rende i deadlock insidiosi: dipendono dall'ordine in cui lo scheduler alterna i thread.

Il vizio sta nella forma di `run`: **mentre tiene il lock di `this`, chiede il lock di un altro oggetto**, e l'altro oggetto fa la stessa cosa nei nostri confronti. Quando in un programma un metodo `synchronized` ne richiama uno `synchronized` di *un altro oggetto*, vale la pena chiedersi se l'altro oggetto può a sua volta richiamare il primo.

### 18.5.3 Riconoscere uno stallo

Un deadlock non lancia nessuna eccezione e non scrive nulla: il programma semplicemente si ferma. Un indizio sicuro è lo stato dei thread ([Capitolo 17](17-thread.md), paragrafo 17.4.2): i thread coinvolti si trovano in stato `BLOCKED`. Possiamo verificarlo con una variante del `main` che, invece di aspettare i thread con `join`, attende un secondo e mezzo e ne stampa lo stato:

```java
public class DiagnosiStallo implements Runnable {
    DiagnosiStallo altro;

    public static void main(String[] args) throws InterruptedException {
        DiagnosiStallo d1 = new DiagnosiStallo();
        DiagnosiStallo d2 = new DiagnosiStallo();
        Thread t1 = new Thread(d1);
        Thread t2 = new Thread(d2);
        d1.altro = d2;
        d2.altro = d1;
        t1.start();
        t2.start();
        Thread.sleep(1500);                      // abbastanza perché lo stallo si sia formato
        System.out.println("t1: " + t1.getState());
        System.out.println("t2: " + t2.getState());
        System.exit(0);                          // termina anche i due thread bloccati
    }

    public synchronized void run() {
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
        }
        altro.sincronizzato();
    }

    public synchronized void sincronizzato() {
        System.out.println("in sincronizzato");
    }
}
```

```text
t1: BLOCKED
t2: BLOCKED
```

Entrambi i thread sono `BLOCKED`, in attesa di un monitor lock che non si libererà mai. L'istruzione `System.exit(0)` ([Capitolo 4](04-strutture-di-controllo.md)) ferma la JVM anche se ci sono thread bloccati.

> [!WARNING]
> **Attenzione — Lo stallo non è solo un caso scolastico**
> Un thread non può andare in stallo da solo con un unico lock: se possiede già il lock di un oggetto e chiede ancora quello stesso oggetto, passa senza bloccarsi (paragrafo 18.3.5). Lo stallo richiede **almeno due lock** e **almeno due thread**, con richieste incrociate. In un esercizio d'esame il pericolo reale è un altro: un programma scritto male, per esempio con un `wait` che nessuno notificherà mai (paragrafo 18.6), resta fermo in modo del tutto simile e il risultato è lo stesso, nessun output.

---

## 18.6 Coordinare i thread: `wait` e `notify`

### 18.6.1 Il problema: aspettare un evento

La mutua esclusione impedisce ai thread di calpestarsi, ma non basta quando un thread, per proseguire, deve aspettare che **un altro abbia fatto qualcosa**. In un programma Java i thread sono spesso interdipendenti: per completare un'operazione, un thread può dipendere da un altro. Il caso classico sono due thread che comunicano attraverso un **buffer** condiviso:

- un thread **scrive** nel buffer e l'altro **legge** dal buffer;
- il thread che legge deve coordinarsi con quello che scrive, in modo da leggere solo quando nel buffer c'è effettivamente qualcosa; altrimenti deve **aspettare**. Quando il thread che scrive ha completato l'inserimento, deve **notificarlo** al lettore perché possa procedere;
- allo stesso modo, se il buffer è pieno, il thread che scrive deve aspettare finché il lettore non toglie qualcosa e lo notifica.

Una soluzione ingenua è l'**attesa attiva** (*busy waiting*): il thread che deve aspettare controlla la condizione in un ciclo continuo, senza fare altro.

```java
class CancelloAttivo {
    private volatile boolean aperto = false;

    void attendi() {
        while (!aperto) {
            // gira a vuoto: controlla la variabile milioni di volte al secondo
        }
    }

    void apri() {
        aperto = true;
    }
}
```

Funziona, ma è uno spreco: il thread attende occupando il processore al massimo, sottraendo CPU proprio ai thread che dovrebbero fare il lavoro di cui sta in attesa. Quello che serve è poter dire: *mi metto da parte finché qualcuno non mi avvisa che la situazione è cambiata*, e **non consumare risorse nel frattempo**. Java lo permette con due operazioni:

- un thread **aspetta** (*wait*) che si verifichi una condizione o un evento;
- un altro thread **notifica** (*notify*) a chi è in attesa che la condizione o l'evento si è verificato.

### 18.6.2 I metodi di `Object`

I metodi che realizzano queste due operazioni sono definiti nella classe **`Object`** ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)), quindi li possiede **ogni oggetto** di qualsiasi classe: non servono import e si chiamano direttamente (o con `this.`) da un metodo di istanza.

| Metodo | Firma esatta | Eccezioni |
|---|---|---|
| `wait` | `public final void wait() throws InterruptedException` | `InterruptedException` (**controllata**); `IllegalMonitorStateException` |
| `wait` con limite | `public final void wait(long timeoutMillis) throws InterruptedException` | come sopra; `IllegalArgumentException` se il tempo è negativo |
| `notify` | `public final void notify()` | `IllegalMonitorStateException` |
| `notifyAll` | `public final void notifyAll()` | `IllegalMonitorStateException` |

Sono tutti `final`: non si possono ridefinire. Due fatti di questa tabella vanno ricordati: `wait` dichiara **`InterruptedException`**, che è un'eccezione controllata ([Capitolo 13](13-eccezioni.md)) e quindi obbliga a catturarla o a dichiararla con `throws`; `notify` e `notifyAll` non la dichiarano.

Un altro vincolo, fondamentale: **`wait`, `notify` e `notifyAll` si possono chiamare solo da un thread che possiede il lock dell'oggetto** su cui li si invoca, cioè dentro un metodo o un blocco `synchronized` su quell'oggetto. Chiamarli senza possedere il lock fa lanciare a runtime una `IllegalMonitorStateException`; il codice compila comunque, perché il compilatore non controlla questo vincolo.

> [!NOTE]
> **Approfondimento esterno — `IllegalMonitorStateException`**
> È l'eccezione lanciata per indicare che un thread ha tentato di attendere sul monitor di un oggetto, o di notificare altri thread in attesa sul monitor di un oggetto, **senza possedere quel monitor**. Estende `RuntimeException`, quindi **non è controllata**.
>
> *Fonte:* [IllegalMonitorStateException — Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/IllegalMonitorStateException.html)

Vediamo l'errore in azione con il programma più piccolo possibile: un thread che chiama `wait` su un oggetto senza prima averne preso il lock.

```java
public class SenzaLock {
    public static void main(String[] args) throws InterruptedException {
        Object o = new Object();
        o.wait();                      // il main non possiede il lock di o
    }
}
```

```text
Exception in thread "main" java.lang.IllegalMonitorStateException: current thread is not owner
```

Compila senza problemi (`throws InterruptedException` basta per il compilatore) ma fallisce subito a runtime. Il tipo dell'eccezione è sempre lo stesso; il testo del messaggio dipende dalla versione del JDK (con alcune versioni più vecchie, come la 11, l'eccezione compare senza messaggio). Lo stesso errore si ottiene se si prende il lock di un oggetto e si chiama `notify` su **un altro**: `synchronized (a) { b.notify(); }`. Il lock e il metodo devono riguardare lo **stesso oggetto**.

### 18.6.3 Come funziona `wait`

La documentazione ufficiale descrive con precisione che cosa fa `wait`. Seguiamo i passi, uno per uno, con la descrizione ufficiale.

> [!NOTE]
> **Approfondimento esterno — Che cosa fa `wait`**
> Il thread corrente deve possedere il monitor dell'oggetto. Il metodo fa mettere il thread (chiamiamolo T) nel **wait set** (*insieme di attesa*) di quell'oggetto e **rilascia tutte le richieste di sincronizzazione su quell'oggetto**. Notare che vengono rilasciati *solo* i lock su questo oggetto: qualsiasi altro oggetto sul quale il thread sia sincronizzato resta bloccato mentre il thread attende.
>
> T quindi non è più considerato dallo scheduling e resta inattivo finché non accade una di queste cose: un altro thread chiama `notify` sull'oggetto e T viene scelto arbitrariamente come thread da risvegliare; un altro thread chiama `notifyAll`; un altro thread **interrompe** T; scade il tempo indicato (se è stato indicato); T viene risvegliato in modo **spurio**.
>
> T viene poi rimosso dal wait set e rimesso in condizione di essere schedulato. Compete con gli altri thread nel modo consueto per il diritto di sincronizzarsi sull'oggetto; una volta riottenuto il controllo, tutte le sue richieste di sincronizzazione sull'oggetto sono ripristinate alla situazione di quando `wait` fu chiamato. Solo allora T ritorna dalla chiamata di `wait`.
>
> *Fonte:* [Object.wait(long, int) — Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#wait(long,int))

In sintesi, quando un thread chiama `wait()` dentro un metodo `synchronized`:

1. **rilascia il lock** dell'oggetto e si mette in attesa; è questo che permette ad altri thread di entrare nell'oggetto e di fare ciò che il primo sta aspettando;
2. resta fermo, senza consumare CPU (stato `WAITING`, [Capitolo 17](17-thread.md), paragrafo 17.4.2), finché qualcuno non lo risveglia;
3. una volta risvegliato, **non riparte subito**: deve ottenere di nuovo il lock, in competizione con gli altri thread;
4. quando riottiene il lock, `wait` ritorna e il thread prosegue dall'istruzione successiva, con il lock di nuovo suo.

Vediamo un esempio completo: un `Cancello` chiuso, un thread che attende l'apertura, e il `main` che lo apre dopo un po'. Il `main` stampa anche lo stato del thread mentre aspetta.

```java
class Cancello {
    private boolean aperto = false;

    public synchronized void attendi() throws InterruptedException {
        while (!aperto) {                        // finché la condizione non è vera...
            wait();                              // ...rilascia il lock e dorme
        }
    }

    public synchronized void apri() {
        aperto = true;                           // cambia la condizione
        notifyAll();                             // e avvisa chi aspetta
    }
}

public class ProvaCancello {
    public static void main(String[] args) throws InterruptedException {
        final Cancello c = new Cancello();
        Thread t = new Thread(new Runnable() {
            public void run() {
                try {
                    System.out.println("Il thread attende il cancello");
                    c.attendi();
                    System.out.println("Il thread passa il cancello");
                } catch (InterruptedException e) {
                }
            }
        });
        t.start();
        Thread.sleep(200);                       // il thread ha il tempo di mettersi in attesa
        System.out.println("Stato del thread: " + t.getState());
        System.out.println("Il main apre il cancello");
        c.apri();
        t.join();
    }
}
```

```text
Il thread attende il cancello
Stato del thread: WAITING
Il main apre il cancello
Il thread passa il cancello
```

Il thread entra in `attendi()` (prende il lock di `c`), trova `aperto` falso e chiama `wait()`: rilascia il lock e si ferma. Il `main`, dopo 200 millisecondi, vede il thread in stato `WAITING` (il thread è in attesa di una notifica) e chiama `c.apri()`: se il thread avesse tenuto il lock durante l'attesa, `apri()` (anch'esso `synchronized`) non avrebbe mai potuto entrare. `apri()` pone `aperto` a `true` e chiama `notifyAll()`, che sveglia il thread; il thread riprende, riacquisisce il lock quando il `main` esce da `apri()`, ricontrolla `aperto`, lo trova vero, esce dal `while` e ritorna.

> [!NOTE]
> **Approfondimento esterno — Lo stato `WAITING`**
> Un thread è nello stato `WAITING` quando ha chiamato uno di questi metodi: `Object.wait` senza tempo massimo, `Thread.join` senza tempo massimo, `LockSupport.park`. Un thread in questo stato sta aspettando che un altro thread esegua una particolare azione: per esempio, un thread che ha chiamato `Object.wait()` su un oggetto aspetta che un altro thread chiami `Object.notify()` o `Object.notifyAll()` su quell'oggetto.
>
> *Fonte:* [Thread.State — Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Thread.State.html)

### 18.6.4 `notify` e `notifyAll`

Quando un thread cambia la condizione che altri aspettano, deve **notificarlo**. Ci sono due metodi:

- **`notify()`** sveglia **un solo** thread tra quelli in attesa sull'oggetto. La scelta è **arbitraria** e dipende dall'implementazione;
- **`notifyAll()`** sveglia **tutti** i thread in attesa sull'oggetto.

Ci sono due fatti da tenere presenti su entrambi.

**Il thread svegliato non riparte subito.** Il thread notificato non può proseguire finché il thread che ha chiamato `notify` non **rilascia il lock** dell'oggetto, cioè finché non esce dal metodo o dal blocco `synchronized`; dopodiché compete con gli altri thread nel modo consueto e non ha nessun privilegio o svantaggio per essere il prossimo a prendere il lock. Lo verifichiamo con un esempio: il metodo `avvisa` chiama `notifyAll`, ma poi resta nel metodo ancora per un po'.

```java
class Avviso {
    synchronized void aspetta() throws InterruptedException {
        wait();
        System.out.println("B: risvegliato, riprende");
    }

    synchronized void avvisa() throws InterruptedException {
        notifyAll();
        System.out.println("A: notifyAll fatto");
        Thread.sleep(300);                       // tiene ancora il lock
        System.out.println("A: esce dal metodo");
    }
}

public class ProvaAvviso {
    public static void main(String[] args) throws InterruptedException {
        final Avviso a = new Avviso();
        Thread b = new Thread(new Runnable() {
            public void run() {
                try {
                    a.aspetta();
                } catch (InterruptedException e) {
                }
            }
        });
        b.start();
        Thread.sleep(200);                       // b è in attesa dentro wait()
        a.avvisa();
        b.join();
    }
}
```

```text
A: notifyAll fatto
A: esce dal metodo
B: risvegliato, riprende
```

Il thread `b` viene risvegliato nel momento in cui `avvisa()` chiama `notifyAll()`, ma può ripartire solo dopo che il `main` ha lasciato il metodo, perché il lock è ancora in mano al `main`. Per questo `B: risvegliato, riprende` compare per ultimo. Se ne ricava che `notify` e `notifyAll` **non rilasciano** il lock: lo rilascia l'uscita dal blocco sincronizzato.

**Quale dei due usare.** `notify` va bene solo se tutti i thread che attendono sull'oggetto sono *equivalenti* (aspettano la stessa condizione) e ne basta uno per proseguire. Se invece sullo stesso oggetto aspettano thread di **tipi diversi**, e `notify` ne sveglia uno del tipo sbagliato, la notifica va persa. Pensiamo a un buffer: un produttore attende quando il buffer è pieno, un consumatore quando è vuoto, e tutti aspettano sullo stesso oggetto. Un consumatore che toglie un elemento e chiama `notify` rischia di svegliare un altro consumatore (che trova il buffer ancora vuoto e torna ad aspettare), mentre il produttore che aspettava un posto libero resta addormentato. Con `notifyAll` si svegliano tutti; ciascuno ricontrolla la condizione e solo chi può proseguire prosegue. **Nel dubbio si usa `notifyAll()`**: è sempre corretto, al più meno efficiente.

### 18.6.5 Perché `wait` va sempre in un `while`

Nell'esempio del cancello, `wait()` era dentro un `while (!aperto)`. Non è uno stile: è una regola. La forma standard dell'attesa è:

```java
synchronized (oggetto) {
    while (/* la condizione per proseguire NON è vera */) {
        oggetto.wait();
    }
    // qui la condizione è vera: si può agire
}
```

La condizione va **ricontrollata ad ogni risveglio**, perché `wait` non garantisce che al ritorno la condizione sia vera. Ci sono almeno tre motivi:

1. **`notifyAll` sveglia tutti.** Se tre consumatori aspettano su un buffer vuoto e viene inserito **un** elemento, tutti e tre si risvegliano e si contendono il lock. Il primo prende l'elemento; il secondo e il terzo trovano il buffer di nuovo vuoto. Con un `while` tornano ad aspettare; con un `if` proseguirebbero come se l'elemento ci fosse.
2. **Tra la notifica e la ripartenza passa del tempo**, durante il quale un altro thread può aver cambiato di nuovo lo stato.
3. **Il risveglio spurio.** Un thread può svegliarsi senza che nessuno lo abbia notificato, né interrotto, né che sia scaduto un tempo: la Javadoc lo chiama *spurious wakeup*.

> [!NOTE]
> **Approfondimento esterno — Perché controllare la condizione in un ciclo**
> Un thread può risvegliarsi senza essere stato notificato, interrotto o senza che il tempo sia scaduto: è il cosiddetto *risveglio spurio*. Anche se in pratica accade di rado, le applicazioni devono proteggersi verificando la condizione che avrebbe dovuto causare il risveglio, e continuando ad attendere se la condizione non è soddisfatta. L'approccio raccomandato per l'attesa è controllare la condizione in un ciclo `while` attorno alla chiamata di `wait`:
> ```java
> synchronized (obj) {
>     while (<condition does not hold> and <timeout not exceeded>) {
>         long timeoutMillis = ... ; // recompute timeout values
>         int nanos = ... ;
>         obj.wait(timeoutMillis, nanos);
>     }
>     ... // Perform action appropriate to condition or timeout
> }
> ```
> *Fonte:* [Object.wait(long, int) — Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html#wait(long,int))

Vediamo che cosa accade con un `if` al posto del `while`. Una `Casella` tiene il conto degli elementi presenti: `metti()` lo aumenta e notifica, `prendi()` aspetta che ce ne sia almeno uno e poi lo diminuisce. Due thread chiamano `prendi()` su una casella vuota e restano in attesa; il `main` mette **un solo** elemento.

```java
class Casella {
    private int n = 0;                           // elementi presenti

    synchronized void metti() {
        n++;
        notifyAll();                             // sveglia ENTRAMBI i lettori
    }

    synchronized void prendi() throws InterruptedException {
        if (n == 0) {                            // ERRORE: if al posto di while
            wait();
        }
        n--;
    }

    synchronized int quanti() {
        return n;
    }
}

public class ProvaIf {
    public static void main(String[] args) throws InterruptedException {
        final Casella c = new Casella();
        Runnable lettore = new Runnable() {
            public void run() {
                try {
                    c.prendi();
                } catch (InterruptedException e) {
                }
            }
        };
        Thread t1 = new Thread(lettore);
        Thread t2 = new Thread(lettore);
        t1.start();
        t2.start();
        Thread.sleep(300);                       // entrambi in attesa dentro wait()
        c.metti();                               // un solo elemento, ma due risvegli
        t1.join();
        t2.join();
        System.out.println("Elementi: " + c.quanti());
    }
}
```

```text
Elementi: -1
```

La casella ha ora **meno uno** elementi, uno stato impossibile: i due lettori si sono svegliati insieme, il primo ha preso l'elemento e il secondo, senza ricontrollare, ha proseguito come se ce ne fosse un altro. Con `while (n == 0) { wait(); }` il secondo lettore avrebbe trovato `n` uguale a 0 e sarebbe tornato ad aspettare (e il programma, con un solo elemento inserito, non sarebbe terminato: il secondo lettore avrebbe aspettato per sempre, che è il comportamento corretto per un solo elemento e due lettori).

> [!IMPORTANT]
> **Nota per l'esame — La regola del `while`**
> All'esame la forma `if (condizione) wait();` è un errore: può compilare e perfino dare l'output giusto nel caso fortunato, ma non è corretta e non rispetta l'aderenza alla struttura richiesta. L'attesa si scrive **sempre** `while (condizione) wait();`, dentro un metodo o un blocco `synchronized`.

### 18.6.6 Attendere con un tempo massimo: `wait(long)`

Esiste una versione di `wait` con un tempo massimo in millisecondi: `wait(long timeoutMillis)`. Il thread si risveglia quando lo notificano, **oppure** quando il tempo è scaduto. Al ritorno non si sa quale dei due eventi sia accaduto; perciò si controlla la condizione e si calcola il tempo che resta, come nel modello della Javadoc.

```java
class Segnale {
    private boolean arrivato = false;

    synchronized boolean attendi(long ms) throws InterruptedException {
        long fine = System.currentTimeMillis() + ms;
        long resto = ms;
        while (!arrivato && resto > 0) {         // condizione E tempo non scaduto
            wait(resto);
            resto = fine - System.currentTimeMillis();
        }
        return arrivato;                         // true: segnale arrivato; false: tempo scaduto
    }

    synchronized void invia() {
        arrivato = true;
        notifyAll();
    }
}

public class ProvaSegnale {
    public static void main(String[] args) throws InterruptedException {
        Segnale s = new Segnale();
        boolean ricevuto = s.attendi(300);       // nessuno invia: scade il tempo
        System.out.println("Segnale arrivato: " + ricevuto);
    }
}
```

```text
Segnale arrivato: false
```

Il `main` attende il segnale per 300 millisecondi; nessuno lo invia, il tempo scade, e `attendi` restituisce `false`. È una variante poco frequente nelle tracce d'esame, ma è bene sapere che esiste; la forma con `wait()` senza argomenti è quella da avere in mente.

### 18.6.7 `sleep` contro `wait`

Entrambi mettono in pausa il thread, ma sono strumenti diversi:

| | `Thread.sleep(millis)` | `wait()` |
|---|---|---|
| A quale classe appartiene | `Thread` (metodo **statico**) | `Object` (metodo **di istanza**, su un oggetto) |
| Dove si può chiamare | ovunque | solo dentro `synchronized` sull'oggetto (altrimenti `IllegalMonitorStateException`) |
| Rilascia il lock? | **no**: il thread dorme tenendo i lock che possiede | **sì**: rilascia il lock di quell'oggetto |
| Quando finisce | dopo il tempo indicato | quando un altro thread chiama `notify`/`notifyAll` (o, con `wait(long)`, quando scade il tempo) |
| Eccezione | `InterruptedException` | `InterruptedException` |
| A che cosa serve | una pausa di durata fissa | aspettare che una **condizione** cambi |

La differenza che conta: `sleep` non lascia entrare nessuno, `wait` sì. Per questo `wait` è lo strumento per il coordinamento tra thread, e `sleep` non lo è: un thread che aspetta con `sleep(1000)` un dato che "dovrebbe essere pronto entro un secondo" scrive un programma che funziona per fortuna. All'esame il coordinamento si scrive con `wait`/`notify`, non con i tempi.

---

## 18.7 Produttore e consumatore

### 18.7.1 Lo schema

Mettiamo insieme mutua esclusione e coordinamento nel problema classico: un thread **produttore** inserisce dati in un buffer condiviso, un thread **consumatore** li estrae. Il buffer ha una capacità limitata. Le regole sono due:

- il produttore, se il buffer è **pieno**, deve aspettare che il consumatore tolga qualcosa;
- il consumatore, se il buffer è **vuoto**, deve aspettare che il produttore inserisca qualcosa;
- e ciascuno, dopo aver cambiato lo stato del buffer, deve **avvisare** l'altro.

Lo schema in pseudocodice, uguale per entrambi, è:

```text
// Thread produttore: produce un dato
   while (buffer_pieno) wait()
   inserisce_il_dato()
   notify()

// Thread consumatore: consuma un dato
   while (nessun_dato) wait()
   estrae_il_dato()
   notify()
```

Ogni operazione ha la stessa forma di **quattro passi**, che dentro un metodo `synchronized` della classe buffer sono:

1. **`while (condizione di blocco) wait();`**: finché l'operazione non è possibile, attendi (rilasciando il lock);
2. **modifica** dello stato del buffer (inserisce o estrae);
3. **`notifyAll();`**: avvisa chi aspettava;
4. eventuale **`return`** del dato estratto.

Il buffer è una **classe a sé**, con campi `private`, i cui metodi `synchronized` incapsulano tutto il meccanismo. Produttore e consumatore sono due `Runnable` che chiamano semplicemente `inserisci` e `estrai` senza sapere nulla di lock e di attese: tutta la sincronizzazione sta nel buffer.

### 18.7.2 Un buffer a pila

Il primo esempio è una **pila** (*stack*) di caratteri con capienza 6: si inserisce con `push` e si estrae con `pop`, e `pop` restituisce l'ultimo carattere inserito (ultimo entrato, primo uscito, *LIFO*). La struttura è un array con un indice `cima` che conta gli elementi presenti e indica anche la prima posizione libera.

```java
class PilaSincronizzata {
    private char[] dati = new char[6];           // il buffer: array primitivo di 6 caratteri
    private int cima = 0;                        // elementi presenti = prima posizione libera

    public synchronized void push(char c) throws InterruptedException {
        while (cima == dati.length) {            // pila piena: aspetta
            wait();
        }
        dati[cima] = c;
        cima++;
        notifyAll();                             // ora c'è almeno un dato: avvisa i consumatori
    }

    public synchronized char pop() throws InterruptedException {
        while (cima == 0) {                      // pila vuota: aspetta
            wait();
        }
        cima--;
        char c = dati[cima];
        notifyAll();                             // ora c'è almeno un posto libero: avvisa i produttori
        return c;
    }
}

class ProduttorePila implements Runnable {
    private PilaSincronizzata pila;
    private int somma = 0;                       // somma dei codici dei caratteri prodotti

    ProduttorePila(PilaSincronizzata pila) {
        this.pila = pila;
    }

    public void run() {
        try {
            for (char c = 'a'; c <= 'z'; c++) {
                pila.push(c);
                somma = somma + c;
            }
        } catch (InterruptedException e) {
        }
    }

    int getSomma() {
        return somma;
    }
}

class ConsumatorePila implements Runnable {
    private PilaSincronizzata pila;
    private int somma = 0;                       // somma dei codici dei caratteri consumati

    ConsumatorePila(PilaSincronizzata pila) {
        this.pila = pila;
    }

    public void run() {
        try {
            for (int k = 0; k < 26; k++) {
                somma = somma + pila.pop();
            }
        } catch (InterruptedException e) {
        }
    }

    int getSomma() {
        return somma;
    }
}

public class ProvaPila {
    public static void main(String[] args) throws InterruptedException {
        PilaSincronizzata pila = new PilaSincronizzata();
        ProduttorePila prod = new ProduttorePila(pila);
        ConsumatorePila cons = new ConsumatorePila(pila);
        Thread tp = new Thread(prod);
        Thread tc = new Thread(cons);
        tp.start();
        tc.start();
        tp.join();
        tc.join();
        System.out.println("Somma dei caratteri prodotti: " + prod.getSomma());
        System.out.println("Somma dei caratteri consumati: " + cons.getSomma());
    }
}
```

```text
Somma dei caratteri prodotti: 2847
Somma dei caratteri consumati: 2847
```

Il produttore inserisce le 26 lettere minuscole, da `'a'` a `'z'`, in una pila che ne contiene al massimo 6: quando la pila è piena `push` si ferma in `wait()` e lascia lavorare il consumatore. Il consumatore ne estrae 26: quando la pila è vuota `pop` si ferma in `wait()`. A fine lavoro le due somme coincidono, quindi nessun carattere è stato perso o letto due volte. Notiamo diverse scelte:

- il **buffer** è un **array primitivo** con la dimensione fissata, e la sua lunghezza si legge con `dati.length` nella condizione di pieno;
- la condizione di pieno è `cima == dati.length`, quella di vuoto `cima == 0`; ciascuna sta in un **`while`**;
- si usa **`notifyAll`** perché sullo stesso oggetto possono aspettare sia produttori sia consumatori;
- `push` e `pop` dichiarano **`throws InterruptedException`**, perché dentro chiamano `wait()`; i `Runnable` che li usano catturano l'eccezione nel loro `run` (un `run` non può dichiarare `throws`, [Capitolo 17](17-thread.md), paragrafo 17.5.2);
- il `main` stampa le somme **dopo** i `join`, quando i due `Runnable` hanno finito di aggiornare `somma`: l'output è sempre lo stesso, anche se l'ordine con cui i caratteri escono dalla pila cambia da un'esecuzione all'altra.

Il motivo dell'ultimo punto è importante. L'ordine con cui produttore e consumatore si alternano è deciso dallo scheduler. Per questo i risultati che si stampano devono essere quelli che **non dipendono** da quell'ordine (una somma, un conteggio), oppure l'alternanza deve essere forzata dal programma stesso (paragrafo 18.7.4).

### 18.7.3 Un buffer a coda

Una pila restituisce per primo l'ultimo elemento inserito. Se la traccia parla di una **coda** (*FIFO*, primo entrato primo uscito), o se l'output atteso mostra gli elementi nello stesso ordine in cui sono stati prodotti, la pila è sbagliata: l'array va usato in un altro modo. Servono **due indici**: `testa`, la posizione del prossimo elemento da estrarre, e `coda`, la posizione del prossimo posto libero. Quando un indice arriva alla fine dell'array riparte da zero: l'array è usato come un **buffer circolare**, e l'avanzamento si scrive `(indice + 1) % dati.length`. Un terzo campo, `n`, conta gli elementi presenti: la condizione di pieno è `n == dati.length`, quella di vuoto `n == 0`.

Realizziamo un `Buffer` di capacità 3 con tre metodi: `inserisci` (aggiunge un intero), `estrai` (toglie e restituisce il più vecchio) e `numeroElementi` (restituisce quanti elementi ci sono).

```java
class Buffer {
    private int[] dati = new int[3];             // array primitivo, capacità massima 3
    private int testa = 0;                       // indice del prossimo elemento da estrarre
    private int coda = 0;                        // indice del prossimo posto libero
    private int n = 0;                           // elementi presenti

    public synchronized void inserisci(int x) throws InterruptedException {
        while (n == dati.length) {               // buffer pieno
            wait();
        }
        dati[coda] = x;
        coda = (coda + 1) % dati.length;         // avanza, tornando a 0 dopo l'ultimo
        n++;
        notifyAll();
    }

    public synchronized int estrai() throws InterruptedException {
        while (n == 0) {                         // buffer vuoto
            wait();
        }
        int x = dati[testa];
        testa = (testa + 1) % dati.length;
        n--;
        notifyAll();
        return x;
    }

    public synchronized int numeroElementi() {
        return n;                                // non attende: legge e basta
    }
}

class Produttore implements Runnable {
    private Buffer buffer;

    Produttore(Buffer buffer) {
        this.buffer = buffer;
    }

    public void run() {
        try {
            for (int k = 1; k <= 10; k++) {
                buffer.inserisci(k);             // produce 1, 2, ..., 10
            }
        } catch (InterruptedException e) {
        }
    }
}

class Consumatore implements Runnable {
    private Buffer buffer;
    private int somma = 0;
    private boolean ordineRispettato = true;

    Consumatore(Buffer buffer) {
        this.buffer = buffer;
    }

    public void run() {
        try {
            for (int k = 1; k <= 10; k++) {
                int x = buffer.estrai();
                if (x != k) {                    // in una coda escono nello stesso ordine
                    ordineRispettato = false;
                }
                somma = somma + x;
            }
        } catch (InterruptedException e) {
        }
    }

    int getSomma() {
        return somma;
    }

    boolean getOrdineRispettato() {
        return ordineRispettato;
    }
}

public class ProvaBuffer {
    public static void main(String[] args) throws InterruptedException {
        Buffer buffer = new Buffer();
        Produttore prod = new Produttore(buffer);
        Consumatore cons = new Consumatore(buffer);
        Thread tp = new Thread(prod);
        Thread tc = new Thread(cons);
        tp.start();
        tc.start();
        tp.join();
        tc.join();
        System.out.println("Somma consumata: " + cons.getSomma());
        System.out.println("Ordine rispettato: " + cons.getOrdineRispettato());
        System.out.println("Elementi rimasti: " + buffer.numeroElementi());
    }
}
```

```text
Somma consumata: 55
Ordine rispettato: true
Elementi rimasti: 0
```

Il produttore inserisce da 1 a 10 in un buffer che ne contiene al più 3, il consumatore li estrae; la somma è 55, gli elementi escono nell'ordine di inserimento, e alla fine il buffer è vuoto. Ecco come si muovono gli indici con una capacità 3, partendo da `testa = 0`, `coda = 0`, `n = 0`:

| Operazione | `dati` | `testa` | `coda` | `n` |
|---|---|---|---|---|
| `inserisci(1)` | `[1, _, _]` | 0 | 1 | 1 |
| `inserisci(2)` | `[1, 2, _]` | 0 | 2 | 2 |
| `estrai()` → 1 | `[_, 2, _]` | 1 | 2 | 1 |
| `inserisci(3)` | `[_, 2, 3]` | 1 | 0 | 2 |
| `inserisci(4)` | `[4, 2, 3]` | 1 | 1 | 3 |
| `inserisci(5)` | **attende** (`n == 3`) | 1 | 1 | 3 |
| `estrai()` → 2 | `[4, _, 3]` | 2 | 1 | 2 |

Notiamo l'inserimento di 3 e quello di 4. Il 3 viene scritto nell'ultima posizione (la numero 2) e `(2 + 1) % 3` riporta `coda` a 0; il 4 viene quindi scritto nella posizione 0, che il consumatore aveva liberato estraendo l'1. L'array è sempre lo stesso, ma gli indici girano su di esso. Questa struttura dà esattamente la FIFO senza spostare mai gli elementi.

> [!WARNING]
> **Attenzione — Un solo indice dà una pila, non una coda**
> Se il buffer ha un solo indice (`cima`), usato sia per inserire sia per estrarre, l'ultimo elemento inserito è il primo estratto: si ottiene la **pila** del paragrafo precedente. Il programma compila, gira e non si blocca, ma gli elementi escono in ordine inverso. Se la traccia parla di una coda, o l'output atteso li mostra nell'ordine di inserimento, questo è un errore di logica che il test nascosto punisce. La traccia dice quale delle due strutture serve: per una coda occorrono due indici (oppure, spostando ogni volta tutti gli elementi di un posto, un solo indice, ma è molto più lungo da scrivere).

### 18.7.4 Quando l'output è deterministico

Se nei metodi del buffer si stampano messaggi (per esempio `inserito 1`, `estratto 1`), con una capacità maggiore di 1 l'ordine tra le stampe del produttore e quelle del consumatore **non è prevedibile**: lo scheduler decide quanti inserimenti fa il produttore prima che il consumatore si svegli. Con una capacità di **un solo elemento** invece l'alternanza è forzata dalla struttura stessa: dopo un inserimento il buffer è pieno, e il produttore non può inserire di nuovo finché il consumatore non ha estratto; dopo un'estrazione il buffer è vuoto, e il consumatore non può estrarre di nuovo finché il produttore non ha inserito. Se le stampe stanno dentro i metodi sincronizzati, l'output è sempre lo stesso:

```java
class Buffer {
    private int[] dati = new int[1];             // capacità 1
    private int n = 0;

    public synchronized void inserisci(int x) throws InterruptedException {
        while (n == dati.length) {
            wait();
        }
        dati[0] = x;
        n++;
        System.out.println("inserito " + x);     // dentro il metodo sincronizzato
        notifyAll();
    }

    public synchronized int estrai() throws InterruptedException {
        while (n == 0) {
            wait();
        }
        int x = dati[0];
        n--;
        System.out.println("estratto " + x);
        notifyAll();
        return x;
    }
}

class Produttore implements Runnable {
    private Buffer buffer;

    Produttore(Buffer buffer) {
        this.buffer = buffer;
    }

    public void run() {
        try {
            for (int k = 1; k <= 4; k++) {
                buffer.inserisci(k);
            }
        } catch (InterruptedException e) {
        }
    }
}

class Consumatore implements Runnable {
    private Buffer buffer;

    Consumatore(Buffer buffer) {
        this.buffer = buffer;
    }

    public void run() {
        try {
            for (int k = 1; k <= 4; k++) {
                buffer.estrai();
            }
        } catch (InterruptedException e) {
        }
    }
}

public class ProvaAlternanza {
    public static void main(String[] args) throws InterruptedException {
        Buffer b = new Buffer();
        Thread p = new Thread(new Produttore(b));
        Thread c = new Thread(new Consumatore(b));
        c.start();                               // il consumatore parte per primo e attende
        p.start();
        p.join();
        c.join();
    }
}
```

```text
inserito 1
estratto 1
inserito 2
estratto 2
inserito 3
estratto 3
inserito 4
estratto 4
```

Il consumatore parte per primo, trova il buffer vuoto e attende; ma, anche partendo il produttore per primo, l'output sarebbe lo stesso. La regola pratica: **un output che alterna le stampe di due thread è prevedibile solo se la struttura del programma impone l'alternanza**. In tutti gli altri casi la traccia chiede (o dovrebbe chiedere) di stampare risultati che non dipendono dall'ordine, e le stampe si fanno nel `main` dopo i `join`.

### 18.7.5 Perché `notifyAll` e non `notify`

Nei buffer qui sopra, `inserisci` e `estrai` chiamano `notifyAll()`. Lo schema in pseudocodice scriveva `notify()`, e con un solo produttore e un solo consumatore sarebbe sufficiente. Ma sullo stesso buffer possono attendere thread di tipi diversi: se un consumatore chiama `notify` dopo aver tolto un elemento e viene svegliato un altro consumatore, il produttore che attendeva un posto libero resta addormentato, mentre il consumatore svegliato rimette subito il thread in attesa. Questo scenario non è un caso limite fantasioso: basta avere due consumatori o due produttori. Con `notifyAll` ogni thread in attesa si risveglia, ricontrolla la propria condizione nel `while` e solo chi può proseguire lo fa. È la scelta sicura, che non costa nulla in correttezza.

### 18.7.6 I metodi che non attendono

Il metodo `numeroElementi()` del buffer è `synchronized` ma **non** chiama `wait`: legge `n` e lo restituisce, senza condizione. Un getter di un oggetto condiviso non deve mai attendere (altrimenti un semplice controllo potrebbe bloccare il chiamante). È comunque `synchronized` per due motivi già visti: evita di leggere `n` mentre un altro thread lo sta aggiornando, e garantisce che il thread veda il valore più recente (paragrafo 18.3.6).

---

## 18.8 Dalla traccia al codice

### 18.8.1 Dedurre le firme dalle chiamate

Nelle tracce sulla sincronizzazione capita che le classi che *usano* la risorsa condivisa siano già scritte, e che le firme dei metodi della risorsa debbano essere **dedotte dalle chiamate**. Il codice che chiama dice molto più di quanto sembri. Supponiamo che la traccia fornisca questa classe:

```java
class Produttore implements Runnable {
    private Buffer buffer;

    Produttore(Buffer buffer) {
        this.buffer = buffer;
    }

    public void run() {
        try {
            for (int k = 1; k <= 10; k++) {
                buffer.inserisci(k);
            }
        } catch (InterruptedException e) {
        }
    }
}
```

e che `Buffer` manchi. Ogni parte della chiamata è un'informazione:

| Che cosa si vede | Che cosa se ne deduce |
|---|---|
| `buffer.inserisci(k)` con `int k` | un metodo di istanza di nome **`inserisci`**, con un parametro compatibile con `int`: `int` |
| il risultato della chiamata non viene usato | il tipo di ritorno può essere `void` |
| `int x = buffer.estrai();` | il tipo di ritorno è `int` (o un tipo che si converte in `int`); il nome è **`estrai`**, senza parametri |
| `System.out.println(buffer.numeroElementi())` | il metodo restituisce qualcosa che si può stampare; se la traccia dice "intero", è `int` |
| la chiamata è dentro un `try` con `catch (InterruptedException e)` | il metodo **deve** dichiarare `throws InterruptedException` |
| la chiamata non è in un `try` e il metodo chiamante non ha `throws` | il metodo **non deve** dichiarare `throws InterruptedException` |
| `new Buffer()` | serve un costruttore **senza parametri** (quello di default va bene) |
| `new Buffer(3)` | serve un costruttore con un parametro `int` |

Le due righe sull'eccezione sono quelle che si sbagliano più facilmente, perché decidono se il programma compila. Se il chiamante cattura `InterruptedException` ma il metodo non la dichiara, il compilatore rifiuta il `catch`:

```java
// ERRORE: il metodo non dichiara throws InterruptedException
class Buffer {
    public synchronized void inserisci(int x) {
    }
}
```

```text
Produttore.java:16: error: exception InterruptedException is never thrown in body of corresponding try statement
        } catch (InterruptedException e) {
          ^
```

Al contrario, se il chiamante non gestisce l'eccezione ma il metodo la dichiara:

```java
// ERRORE: il chiamante non gestisce l'eccezione dichiarata
class Buffer {
    public synchronized void inserisci(int x) throws InterruptedException {
        wait();
    }
}
// ... e nel chiamante:  buffer.inserisci(5);   senza try/catch
```

```text
Produttore.java:15: error: unreported exception InterruptedException; must be caught or declared to be thrown
        buffer.inserisci(5);
                        ^
```

Quindi, quando il chiamante **non** cattura `InterruptedException`, il metodo del buffer non può dichiararla, e se deve chiamare `wait()` la cattura **dentro** di sé. La forma più semplice è avvolgere la sola chiamata a `wait()` in un `try`/`catch`, lasciandola dentro il `while`:

```java
public synchronized void inserisci(int x) {      // nessun throws: la traccia non lo permette
    while (n == dati.length) {
        try {
            wait();
        } catch (InterruptedException e) {
            // l'interruzione viene ignorata: si torna a controllare la condizione
        }
    }
    dati[coda] = x;
    coda = (coda + 1) % dati.length;
    n++;
    notifyAll();
}
```

Il `catch` vuoto qui è una scelta deliberata: il programma non usa le interruzioni, e dopo di essa il `while` ricontrolla la condizione e, se serve, riprende ad attendere. Il caso più comune, però, è l'altro: il chiamante cattura l'eccezione e il metodo la dichiara con `throws`, come negli esempi di questo capitolo.

### 18.8.2 Dalle parole della traccia al codice

| La traccia dice | Che cosa si scrive |
|---|---|
| "garantire la **mutua esclusione**", "un solo thread alla volta" | `synchronized` su **ogni** metodo che legge o scrive i dati condivisi, compresi i getter |
| "struttura dati basata su un **array primitivo** con dimensione massima N" | `int[] dati = new int[N];` (non `ArrayList`, non `Queue`); la capacità si legge con `dati.length` |
| "inserimento di un elemento" | metodo con `while (n == dati.length) wait();`, scrittura, `n++`, `notifyAll();` |
| "estrazione e rimozione di un elemento" | metodo con `while (n == 0) wait();`, lettura, `n--`, `notifyAll();`, `return` dell'elemento |
| "numero di elementi presenti, sotto forma di intero" | `public synchronized int numeroElementi() { return n; }` (nome dedotto dalle chiamate) |
| "se il buffer è pieno/vuoto il thread deve attendere" | `while (condizione) wait();`, **mai** `if` |
| "i metodi vanno dedotti dalle invocazioni" | si leggono nome, argomenti, tipo del risultato e `catch` del chiamante (paragrafo 18.8.1) |
| "l'ultimo inserito è il primo estratto" | pila: un solo indice (`cima`) |
| "i dati escono nell'ordine di inserimento", "coda" | FIFO: due indici e aritmetica modulare |
| "il `main` stampa il totale alla fine" | `join` su tutti i thread **prima** della stampa |

Il filo conduttore: la sincronizzazione non è una decorazione. Ogni `synchronized`, ogni `while`, ogni `notifyAll` ha una ragione precisa, e la traccia di solito la nomina con una parola ("mutua esclusione", "attendere", "pieno", "vuoto").

---

## Come esce all'esame

### EXAM2 — Esercizio 3 (13 punti)

- **Cosa chiedeva la traccia.** All'interno del file sono già fornite le classi `Produttore` e `Consumatore`, completamente implementate, progettate per interagire concorrentemente con una risorsa condivisa. Si chiede di implementare ex novo la classe `Buffer` (che manca), in modo da risolvere il problema della concorrenza garantendo la **mutua esclusione** e la corretta **sincronizzazione** dei thread. Requisiti obbligatori: (1) una struttura dati basata su un **array primitivo** con dimensione massima pari a **3**; (2) un metodo che restituisca come intero il **numero di elementi** attualmente presenti; (3) un metodo per l'**inserimento** di un elemento; (4) un metodo per l'**estrazione e rimozione** di un elemento. Le firme esatte dei metodi vanno **dedotte** dalle invocazioni nel codice fornito.
- **Concetti del capitolo necessari.** Metodi `synchronized` (paragrafo 18.3); `wait` dentro `while` e `notifyAll` (paragrafi 18.6 e 18.7); buffer con array a capacità limitata (paragrafi 18.7.2 e 18.7.3); deduzione delle firme dalle chiamate, compreso `throws InterruptedException` (paragrafo 18.8.1).
- **Vincoli letterali imposti.** Array primitivo di dimensione 3 (non una collezione); tre metodi con le firme che le chiamate fornite impongono; mutua esclusione **e** sincronizzazione (cioè sia `synchronized` sia `wait`/`notify`); la classe si chiama `Buffer`, come usata dal codice fornito.

La traccia non dice se il buffer sia una pila o una coda: lo si capisce dalle chiamate fornite e dall'output atteso. Quello che non si deduce è l'ordine di estrazione se l'output atteso non lo mostra: in quel caso entrambe le strutture sono ammissibili, ma vale la pena scegliere la coda (FIFO), che è il comportamento naturale di un buffer tra produttore e consumatore.

---

## Scheletri da esame

Questi frammenti sono i minimi da saper scrivere a memoria su un editor senza aiuti. Ciascuno compila così com'è (con una classe di prova dove serve).

### Scheletro 1 — Un dato condiviso protetto da metodi `synchronized`

**Quando si usa.** Due o più thread modificano lo stesso oggetto (un contatore, un saldo, un totale).

```java
class Contatore {
    private int valore = 0;                          // dato condiviso: private

    public synchronized void incrementa() {          // mutua esclusione sull'oggetto
        valore = valore + 1;
    }

    public synchronized int getValore() {            // anche la lettura è sincronizzata
        return valore;
    }
}

class Incrementatore implements Runnable {
    private Contatore contatore;

    Incrementatore(Contatore contatore) {
        this.contatore = contatore;
    }

    public void run() {
        for (int k = 0; k < 100000; k++) {
            contatore.incrementa();
        }
    }
}

public class ProvaContatore {
    public static void main(String[] args) throws InterruptedException {
        Contatore c = new Contatore();               // UN solo oggetto, condiviso
        Thread t1 = new Thread(new Incrementatore(c));
        Thread t2 = new Thread(new Incrementatore(c));
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(c.getValore());           // 200000, sempre
    }
}
```

```text
200000
```

**Eccezioni e import.** Nessun import. `InterruptedException` (controllata) dal `join` nel `main`, dichiarata con `throws`. I due thread devono ricevere **lo stesso** oggetto `Contatore`.

### Scheletro 2 — Un blocco `synchronized` su un oggetto condiviso

**Quando si usa.** La parte che tocca il dato condiviso è piccola e il resto del metodo no, oppure il dato condiviso è un oggetto separato passato ai thread.

```java
class Totale {
    int valore = 0;
}

class Somma implements Runnable {
    private Totale totale;
    private int da, fino;                            // intervallo da sommare: da..fino-1

    Somma(Totale totale, int da, int fino) {
        this.totale = totale;
        this.da = da;
        this.fino = fino;
    }

    public void run() {
        int parziale = 0;
        for (int k = da; k < fino; k++) {
            parziale = parziale + k;                 // lavoro fuori dal lock
        }
        synchronized (totale) {                      // lock dell'oggetto condiviso, non di this
            totale.valore = totale.valore + parziale;
        }
    }
}

public class ProvaSomma {
    public static void main(String[] args) throws InterruptedException {
        Totale totale = new Totale();
        Thread t1 = new Thread(new Somma(totale, 0, 500));
        Thread t2 = new Thread(new Somma(totale, 500, 1000));
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(totale.valore);           // 499500
    }
}
```

```text
499500
```

**Eccezioni e import.** Nessun import. Tra le parentesi di `synchronized` ci vuole un **riferimento a un oggetto** (non un `int`); deve essere lo stesso oggetto per tutti i thread.

### Scheletro 3 — Buffer a capacità limitata (coda) con `wait` e `notifyAll`

**Quando si usa.** "Produttore e consumatore", "buffer di dimensione N", "il thread deve attendere se pieno/vuoto".

```java
class Buffer {
    private int[] dati = new int[3];                 // array primitivo, capacità 3
    private int testa = 0;                           // prossimo da estrarre
    private int coda = 0;                            // prossimo posto libero
    private int n = 0;                               // elementi presenti

    public synchronized void inserisci(int x) throws InterruptedException {
        while (n == dati.length) {                   // while, MAI if
            wait();
        }
        dati[coda] = x;
        coda = (coda + 1) % dati.length;
        n++;
        notifyAll();
    }

    public synchronized int estrai() throws InterruptedException {
        while (n == 0) {
            wait();
        }
        int x = dati[testa];
        testa = (testa + 1) % dati.length;
        n--;
        notifyAll();
        return x;
    }

    public synchronized int numeroElementi() {
        return n;
    }
}

public class ProvaSkeletro {
    public static void main(String[] args) throws InterruptedException {
        final Buffer b = new Buffer();
        Thread produttore = new Thread(new Runnable() {
            public void run() {
                try {
                    for (int k = 1; k <= 6; k++) {
                        b.inserisci(k);
                    }
                } catch (InterruptedException e) {
                }
            }
        });
        produttore.start();
        int somma = 0;
        for (int k = 1; k <= 6; k++) {
            somma = somma + b.estrai();              // il main fa da consumatore
        }
        produttore.join();
        System.out.println(somma + " " + b.numeroElementi());
    }
}
```

```text
21 0
```

**Eccezioni e import.** Nessun import. `inserisci` ed `estrai` dichiarano `throws InterruptedException` (da `wait`, controllata): chi le chiama la cattura o la dichiara. Le firme vere dipendono dalle chiamate della traccia (paragrafo 18.8.1).

### Scheletro 4 — Buffer a pila (LIFO)

**Quando si usa.** L'ultimo elemento inserito deve essere il primo estratto.

```java
class Pila {
    private char[] dati = new char[6];
    private int cima = 0;                            // elementi presenti = prima posizione libera

    public synchronized void push(char c) throws InterruptedException {
        while (cima == dati.length) {
            wait();
        }
        dati[cima] = c;
        cima++;
        notifyAll();
    }

    public synchronized char pop() throws InterruptedException {
        while (cima == 0) {
            wait();
        }
        cima--;
        char c = dati[cima];
        notifyAll();
        return c;
    }
}

public class ProvaPilaSkeletro {
    public static void main(String[] args) throws InterruptedException {
        Pila p = new Pila();
        p.push('x');
        p.push('y');
        System.out.println(p.pop() + "" + p.pop());   // yx
    }
}
```

```text
yx
```

**Eccezioni e import.** Nessun import. Un solo indice: `cima` conta gli elementi e indica la prima posizione libera. Si decrementa **prima** di leggere, perché `dati[cima]` è la prima posizione libera, non l'ultimo elemento.

### Scheletro 5 — Attesa di una condizione con una variabile di stato

**Quando si usa.** Un thread deve aspettare che un evento accada (un cancello si apre, un dato è pronto) e un altro lo segnala.

```java
class Semaforo {
    private boolean pronto = false;                  // la condizione

    public synchronized void attendi() throws InterruptedException {
        while (!pronto) {                            // finché NON è vera
            wait();
        }
    }

    public synchronized void segnala() {
        pronto = true;                               // prima cambia la condizione...
        notifyAll();                                 // ...poi avvisa
    }
}

public class ProvaSemaforo {
    public static void main(String[] args) throws InterruptedException {
        final Semaforo s = new Semaforo();
        Thread t = new Thread(new Runnable() {
            public void run() {
                try {
                    s.attendi();
                    System.out.println("via");
                } catch (InterruptedException e) {
                }
            }
        });
        t.start();
        s.segnala();                                 // funziona anche se segnala() arriva prima
        t.join();
    }
}
```

```text
via
```

**Eccezioni e import.** Nessun import. La condizione è una **variabile di stato** (`pronto`) letta e scritta solo dentro metodi `synchronized`. Poiché `wait` è dentro un `while (!pronto)`, funziona anche se il segnale arriva *prima* che il thread inizi ad attendere (il `while` trova la condizione già vera e non chiama `wait`). Senza la variabile, una notifica arrivata troppo presto andrebbe persa.

---

## Errori tipici

> [!CAUTION]
> **Errore tipico — `wait()` dentro un `if`**
> ```java
> // ERRORE logico
> public synchronized int estrai() throws InterruptedException {
>     if (n == 0) {
>         wait();
>     }
>     n--;
>     // ...
> }
> ```
> Dopo il risveglio la condizione non è ricontrollata: con più consumatori, `notifyAll` li sveglia tutti, il primo prende l'elemento e gli altri proseguono su un buffer vuoto (nel paragrafo 18.6.5 il contatore degli elementi arriva a −1). Anche un risveglio spurio basterebbe. Forma corretta: `while (n == 0) { wait(); }`.

> [!CAUTION]
> **Errore tipico — `wait`, `notify` o `notifyAll` fuori da `synchronized`**
> ```java
> // ERRORE a runtime: compila
> public void inserisci(int x) throws InterruptedException {   // manca synchronized
>     while (n == dati.length) {
>         wait();
>     }
>     // ...
> }
> ```
> Il compilatore non si accorge del problema, ma a runtime `wait()` lancia `java.lang.IllegalMonitorStateException: current thread is not owner`, perché il thread non possiede il lock. Lo stesso vale per `notify` e `notifyAll`. Forma corretta: metodo `synchronized` (o blocco `synchronized` sullo stesso oggetto su cui si chiama `wait`).

> [!CAUTION]
> **Errore tipico — Lock di un oggetto, `wait` o `notify` su un altro**
> ```java
> // ERRORE a runtime
> synchronized (a) {
>     b.notify();                  // si possiede il lock di a, non quello di b
> }
> ```
> Lancia `IllegalMonitorStateException`. Il thread deve possedere il lock dell'oggetto **su cui chiama** `wait`/`notify`/`notifyAll`. Forma corretta: `synchronized (b) { b.notify(); }`.

> [!CAUTION]
> **Errore tipico — Dimenticare di notificare**
> ```java
> // ERRORE: il consumatore non sarà mai svegliato
> public synchronized void inserisci(int x) throws InterruptedException {
>     while (n == dati.length) {
>         wait();
>     }
>     dati[coda] = x;
>     coda = (coda + 1) % dati.length;
>     n++;
>     // manca notifyAll();
> }
> ```
> Il programma compila, ma un consumatore che stava aspettando un dato resta in `wait()` per sempre, e il programma non termina: nessun output. Dopo ogni modifica dello stato del buffer (inserimento **e** estrazione) serve `notifyAll()`. Forma corretta: aggiungere `notifyAll();` prima di uscire dal metodo.

> [!CAUTION]
> **Errore tipico — `notify` quando aspettano thread di tipi diversi**
> ```java
> // ERRORE potenziale
> n--;
> notify();                        // può svegliare un altro consumatore, non il produttore
> ```
> Se su uno stesso buffer aspettano sia produttori sia consumatori, `notify` ne sveglia uno a caso: se è del tipo sbagliato, ricontrolla la condizione, torna in `wait()` e la notifica è persa; l'altro tipo resta addormentato. Forma corretta: `notifyAll();`.

> [!CAUTION]
> **Errore tipico — Sincronizzare solo alcuni metodi**
> ```java
> // ERRORE: il getter non è sincronizzato
> public synchronized void incrementa() { valore++; }
> public int getValore() { return valore; }
> ```
> Il lock protegge solo chi lo chiede. `getValore` può leggere mentre un altro thread aggiorna (e può non vedere l'ultimo valore scritto, paragrafo 18.3.6). Forma corretta: `synchronized` su **tutti** i metodi che toccano il dato condiviso, getter compreso.

> [!CAUTION]
> **Errore tipico — Un lock diverso per ogni thread**
> ```java
> // ERRORE: ogni chiamata prende un lock nuovo
> synchronized (new Object()) {
>     contatore++;
> }
> ```
> L'oggetto nuovo è diverso a ogni passaggio e per ogni thread: nessun lock è mai condiviso, quindi nessuna mutua esclusione, e il risultato è imprevedibile. Lo stesso errore, meno visibile, è `synchronized (this)` in un `Runnable` di cui esiste **un'istanza per thread**: ogni thread prende il lock della *propria* istanza (paragrafo 18.4.2). Forma corretta: sincronizzare su **un oggetto condiviso** da tutti i thread.

> [!CAUTION]
> **Errore tipico — Contatore `static` e metodo `synchronized` di istanza**
> ```java
> // ERRORE: il campo è condiviso da tutte le istanze, il lock no
> class Conta {
>     static int totale = 0;
>     synchronized void aggiungi() { totale++; }   // lock dell'istanza
> }
> ```
> Due thread che usano due oggetti `Conta` diversi prendono due lock diversi e modificano lo stesso `totale` senza esclusione. Forma corretta: `static synchronized void aggiungi()`, che prende il lock della classe (paragrafo 18.3.4).

> [!CAUTION]
> **Errore tipico — `synchronized` sul costruttore**
> ```java
> // ERRORE di compilazione
> class Conto {
>     synchronized Conto() { }
> }
> ```
> ```text
> Conto.java:2: error: modifier synchronized not allowed here
> ```
> I costruttori non possono essere `synchronized`. Un oggetto in costruzione non è raggiungibile da altri thread finché il costruttore non termina. Forma corretta: togliere il modificatore.

> [!CAUTION]
> **Errore tipico — `synchronized` su un tipo primitivo**
> ```java
> // ERRORE di compilazione
> int x = 5;
> synchronized (x) { }
> ```
> ```text
> error: unexpected type
>   required: reference
>   found:    int
> ```
> Il lock è sempre di un **oggetto**. Forma corretta: un riferimento (`Object`, `this`, un oggetto condiviso).

> [!CAUTION]
> **Errore tipico — `synchronized` sul metodo `run` di un `Runnable` condiviso**
> ```java
> // ERRORE logico: i thread vengono eseguiti uno dopo l'altro
> class Lavoro implements Runnable {
>     public synchronized void run() {          // lock di this
>         // tutto il lavoro...
>     }
> }
> // main: Lavoro l = new Lavoro(); new Thread(l).start(); new Thread(l).start();
> ```
> I due thread condividono lo stesso oggetto `l`, quindi lo stesso lock: il secondo resta bloccato finché il primo non esce da `run`. Il programma è corretto ma **non è più parallelo**. Forma corretta: sincronizzare solo il codice che tocca il dato condiviso, non tutto il `run`.

> [!CAUTION]
> **Errore tipico — Dormire dentro un metodo sincronizzato**
> ```java
> // ERRORE di prestazioni (e fonte di stallo)
> public synchronized void elabora() throws InterruptedException {
>     Thread.sleep(2000);               // dorme tenendo il lock
>     // ...
> }
> ```
> `sleep` non rilascia il lock (paragrafo 18.3.7): tutti gli altri thread che vogliono l'oggetto aspettano. Se serve attendere un evento, si usa `wait()` (che il lock lo rilascia). Forma corretta: attese fuori dal codice sincronizzato, oppure `wait`.

> [!CAUTION]
> **Errore tipico — Usare `sleep` al posto della sincronizzazione**
> ```java
> // ERRORE logico
> t.start();
> Thread.sleep(2000);                   // "speriamo che t abbia finito"
> System.out.println(risultato);
> ```
> Funziona per fortuna e fallisce sulla macchina del test. Il programma deve **dipendere dagli eventi**, non dal tempo: `t.join()` per attendere un thread, `wait`/`notifyAll` per attendere una condizione.

> [!CAUTION]
> **Errore tipico — Condizioni di attesa scambiate o capacità non assegnata**
> ```java
> // ERRORE: il produttore aspetta quando il buffer è vuoto
> while (n == 0) { wait(); }            // dentro inserisci
> ```
> Con le condizioni scambiate, il primo `inserisci` su un buffer vuoto attende un'estrazione che non può avvenire se il consumatore sta a sua volta aspettando un dato: **stallo**, nessun output. Un errore affine: se la capacità è un campo `capienza` letto dal costruttore e il parametro non viene assegnato al campo (manca `this.capienza = capienza;`), la capacità resta 0: `n == capienza` è subito vero e il produttore attende per sempre. Forma corretta: **inserisci** attende se **pieno** (`n == dati.length`); **estrai** attende se **vuoto** (`n == 0`).

> [!CAUTION]
> **Errore tipico — Metodo `synchronized` che richiama un altro oggetto in modo incrociato**
> ```java
> // ERRORE: rischio di stallo
> public synchronized void run() {
>     altro.sincronizzato();        // tiene il lock di this e chiede quello di altro
> }
> ```
> Se `altro` fa la stessa cosa nei nostri confronti, i due thread si bloccano a vicenda (paragrafo 18.5). Il programma non dà errori né output. Forma corretta: non tenere un lock mentre se ne chiede uno su un altro oggetto che può a sua volta chiamarci; in un esercizio d'esame basta evitare chiamate incrociate tra metodi sincronizzati di due oggetti.

> [!CAUTION]
> **Errore tipico — Struttura sbagliata rispetto alla traccia (pila al posto della coda, collezione al posto dell'array)**
> ```java
> // ERRORE di aderenza: la traccia chiede un ARRAY PRIMITIVO di 3 posti
> private ArrayList<Integer> dati = new ArrayList<Integer>();
> ```
> Il programma può dare l'output giusto, ma la traccia imponeva una struttura precisa (array primitivo, dimensione 3, due metodi con certe proprietà). Lo stesso vale per la pila al posto della coda e per le stampe fuori dal punto prescritto. Forma corretta: seguire alla lettera la struttura richiesta.

---

## Riassunto

Quando più thread toccano **lo stesso dato** e almeno uno lo modifica, un'operazione che sembra unica (`i = i + 1`) è in realtà una sequenza di passi (leggi, calcola, scrivi) e i thread possono intrecciarli: è la **race condition**, il cui risultato cambia a ogni esecuzione. La cura è la **mutua esclusione**: far eseguire l'operazione a un thread alla volta, con un **lock**. In Java ogni oggetto ha il suo lock, che si prende con **`synchronized`**: sui metodi (lock dell'oggetto, o della classe se `static`) o su un blocco (`synchronized (oggetto)`, per proteggere solo la parte che serve e scegliere l'oggetto). Il lock è dell'oggetto, non del metodo, e protegge solo chi lo chiede: tutti i metodi che toccano il dato condiviso devono essere sincronizzati. Il prezzo è il **deadlock**: due thread che si aspettano a vicenda, ciascuno con il lock che serve all'altro. Quando un thread deve aspettare che *un altro faccia qualcosa*, la mutua esclusione non basta: si usano `wait`, `notify` e `notifyAll` di `Object`, sempre dentro un `synchronized` sullo stesso oggetto. `wait` rilascia il lock e mette il thread in attesa; la condizione va controllata in un **`while`**, perché al risveglio potrebbe non essere vera (altri thread, risvegli spuri); dopo ogni modifica si chiama `notifyAll`. Mettendo tutto insieme si ottiene lo schema **produttore/consumatore**: un buffer con array a capacità limitata, i cui metodi `inserisci` ed `estrai` sono `synchronized`, attendono in un `while` e notificano con `notifyAll`.

**Concetti chiave**

- **Race condition**: più thread operano sugli stessi dati con almeno un'operazione non atomica; il risultato dipende dall'ordine dei passi. `i++`, `i = i + 1` non sono atomiche.
- **Mutua esclusione e lock**: un'operazione complessa eseguita per intero da un thread alla volta; si ottiene con il lock (monitor) dell'oggetto.
- **`synchronized` su metodo**: lock di `this` (o dell'oggetto `Class` se il metodo è `static`); rilascio automatico all'uscita; tutti i metodi sincronizzati di uno stesso oggetto si escludono a vicenda.
- **Il lock è dell'oggetto**: oggetti diversi hanno lock diversi; un metodo non sincronizzato non aspetta nessuno; metodo di istanza e metodo `static` usano lock diversi.
- **Blocco `synchronized (oggetto)`**: protegge solo una parte del codice; vuole un riferimento a un oggetto; `synchronized void m()` equivale a un blocco su `this`.
- **Visibilità**: uscire da un blocco sincronizzato rende visibili agli altri thread le modifiche fatte; per questo anche le letture si sincronizzano.
- **Deadlock**: attesa circolare di lock tra thread; nessuna eccezione, nessun output; i thread sono `BLOCKED`.
- **`wait`**: rilascia il lock dell'oggetto e mette il thread in attesa; `throws InterruptedException` (controllata); solo dentro `synchronized` sullo stesso oggetto.
- **`notify` / `notifyAll`**: risvegliano uno / tutti i thread in attesa; il risvegliato riparte solo quando chi ha notificato esce dal blocco sincronizzato; nel dubbio `notifyAll`.
- **`while`, non `if`**: la condizione si ricontrolla a ogni risveglio (più thread svegliati, risvegli spuri).
- **`sleep` contro `wait`**: `sleep` non rilascia i lock, `wait` sì; `sleep` per le pause, `wait` per aspettare una condizione.
- **Buffer limitato**: array primitivo + contatore (e indici); inserisci attende se pieno, estrai attende se vuoto; coda (FIFO) con due indici e `%`, pila (LIFO) con uno.
- **Firme dedotte dalle chiamate**: nome, argomenti, tipo del risultato e `catch (InterruptedException)` del chiamante determinano la firma, compreso `throws`.

**API essenziali**

| Classe | Elemento | Firma | Eccezioni |
|---|---|---|---|
| — | modificatore `synchronized` | `synchronized` su metodo, oppure `synchronized (oggetto) { ... }` | `NullPointerException` se `oggetto` è `null` |
| `Object` | `wait` | `public final void wait() throws InterruptedException` | `InterruptedException` (controllata); `IllegalMonitorStateException` |
| `Object` | `wait` con limite | `public final void wait(long timeoutMillis) throws InterruptedException` | come sopra; `IllegalArgumentException` se negativo |
| `Object` | `notify` | `public final void notify()` | `IllegalMonitorStateException` |
| `Object` | `notifyAll` | `public final void notifyAll()` | `IllegalMonitorStateException` |
| `Thread` | `sleep` | `public static void sleep(long millis) throws InterruptedException` | `InterruptedException` (controllata); non rilascia i lock |
| `Thread` | `join` | `public final void join() throws InterruptedException` | `InterruptedException` (controllata) |
| `Thread` | `getState` | `public Thread.State getState()` | — (`BLOCKED`, `WAITING`, `TIMED_WAITING`, ...) |
| `IllegalMonitorStateException` | — | `class IllegalMonitorStateException extends RuntimeException` | non controllata |
