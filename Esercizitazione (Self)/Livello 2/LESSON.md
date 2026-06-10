# Livello 2: La Programmazione Orientata agli Oggetti - OOP

## 1. Classi, Oggetti e Incapsulamento

### Teoria Fondamentale: Astrazione e Information Hiding
Il paradigma Object-Oriented (OOP) nasce per risolvere la crisi del software degli anni '70 e '80, dove enormi basi di codice procedurale (tutto globale, funzioni slegate dai dati) diventavano impossibili da mantenere. La OOP modella il dominio del problema creando entità autonome e coese (Oggetti) che comunicano scambiandosi messaggi.

> **Definizione Accademica (Classe vs Oggetto):**
> Una **Classe** è il "progetto" ingegneristico o *blueprint* a livello concettuale. Non esiste fisicamente in esecuzione se non come metadato, ma definisce la struttura dei dati (le *variabili d'istanza* o *stato*) e i comportamenti consentiti (i *metodi*). 
> Un **Oggetto** è una specifica istanza creata a runtime nella memoria *Heap*. Ogni oggetto possiede una propria copia indipendente delle variabili d'istanza definite dalla classe, garantendo l'isolamento dello stato.

L'**Incapsulamento (Information Hiding)** è il principio supremo di sicurezza della OOP. Sancisce che lo stato interno di un oggetto non deve **mai** essere manipolabile dall'esterno in modo diretto. Si applica la regola della "Scatola Nera": i dati sono marcati come `private` (invisibili all'esterno) e vi si accede esclusivamente tramite un'interfaccia pubblica di metodi `public` (i famosi pattern Getter/Setter). Questo permette alla classe di fungere da "Dogana", applicando regole di validazione ed evitando che il software entri in stati logici incoerenti (es. impostare un'età negativa).

L'**Overloading (Sovraccarico dei Metodi)** consente a una classe di avere più metodi (inclusi i Costruttori) con lo *stesso identico nome*, purché la loro "firma" sia diversa (ossia cambi il numero o il tipo di parametri passati). Il compilatore capisce quale metodo invocare basandosi sugli argomenti forniti a tempo di compilazione (Static Binding).

### Sintassi ed Esempi di Codice
```java
public class Studente Universitario {
    // 1. Information Hiding: Nessuno fuori da questa classe può toccare questi campi.
    private String matricola;
    private int eta;
    private double mediaVoti;
    
    // 2. Costruttore di Default (Senza argomenti)
    // Se non lo si scrive e si usa un altro costruttore, Java NON lo genererà in automatico.
    public StudenteUniversitario() {
        this.matricola = "Non Assegnata";
        this.eta = 18;
        this.mediaVoti = 18.0;
    }
    
    // 3. Costruttore con Overloading e Costructor Injection
    // La keyword 'this' risolve l'ambiguità (Shadowing) tra il parametro e la variabile d'istanza.
    public StudenteUniversitario(String matricola, int eta) {
        this.matricola = matricola;
        // Deleghiamo l'assegnazione al Setter per sfruttare la sua logica di validazione!
        setEta(eta); 
        this.mediaVoti = 18.0; 
    }
    
    // 4. Pattern Getter: Lettura sicura (Read-Only per il mondo esterno)
    public String getMatricola() {
        return this.matricola;
    }
    
    // 5. Pattern Setter: Scrittura validata (Mutazione controllata)
    public void setEta(int eta) {
        // La "Dogana" algoritmica
        if (eta >= 16 && eta <= 120) {
            this.eta = eta;
        } else {
            System.err.println("Errore di Dominio: Età fuori dal range accademico consentito.");
            // Non si blocca l'esecuzione, ma si evita di corrompere lo stato!
            // In contesti enterprise, qui si lancerebbe una IllegalArgumentException.
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Bypassare i Setter nel Costruttore:** Errore classico di design. Se scrivi logica di validazione dentro `setEta()`, non scrivere `this.eta = eta;` dentro il costruttore, altrimenti permetterai la creazione di un oggetto corrotto già alla nascita. Usa sempre `setEta(eta)` nel costruttore!
- **Riferimento `this` Dimenticato:** Omettere `this` quando un parametro ha lo stesso nome di una variabile d'istanza (`eta = eta;`) fa sì che il parametro riassegni il valore a se stesso, lasciando lo stato dell'oggetto miseramente vuoto o a `null`.
- **Restituire riferimenti interni modificabili (Privacy Leak):** Se un Getter restituisce un oggetto mutabile (es. un `Date` o un `ArrayList` interno), chi chiama il getter può svuotare la lista o cambiare la data distruggendo l'incapsulamento dall'esterno. Accademicamente, si risolve restituendo una *Defensive Copy* (copia difensiva: `return new ArrayList<>(questaLista);`).

---

## 2. Ereditarietà e Relazione Gerarchica

### Teoria Fondamentale: La Relazione "IS-A"
Mentre le classi incapsulano i dati, l'Ereditarietà permette di riutilizzarli e specializzarli, abbattendo la ridondanza di codice. L'ereditarietà instaura una rigida relazione gerarchica di tipo **"is-a" (è un/una)** tra una Superclasse (Classe Base o Padre) e una Sottoclasse (Classe Derivata o Figlia). 
Esempio: Una `Motocicletta` *è un* `Veicolo`.

Quando si usa la keyword `extends`, la figlia assorbe passivamente tutto il patrimonio genetico (metodi e campi visibili) del padre. Tuttavia, l'ereditarietà in Java è **strettamente singola**: una classe può avere un solo padre diretto. Questo design previene il collasso semantico noto in C++ come "Problema del Diamante" (ovvero ereditare due metodi identici da due padri diversi, generando ambiguità).

> **Dietro le Quinte (La Catena dei Costruttori):**
> Gli oggetti non nascono nel vuoto. Quando istanzi una figlia, in memoria Heap viene creato prima il nucleo del padre, e poi l'estensione della figlia attorno ad esso. Per questo motivo, il costruttore della figlia **deve obbligatoriamente chiamare il costruttore del padre** come primissima operazione, usando la keyword `super()`. Se non lo fai, Java inserisce invisibilmente un `super()` vuoto. Se il padre non ha un costruttore vuoto, il tuo codice esploderà in fase di compilazione.

| Modificatore | Visibilità in Classe | Nel Package | Nelle Sottoclassi | Ovunque |
| --- | --- | --- | --- | --- |
| `private` | ✅ Sì | ❌ No | ❌ No | ❌ No |
| *(default)* | ✅ Sì | ✅ Sì | ❌ No | ❌ No |
| `protected` | ✅ Sì | ✅ Sì | ✅ Sì | ❌ No |
| `public` | ✅ Sì | ✅ Sì | ✅ Sì | ✅ Sì |

### Sintassi ed Esempi di Codice
```java
// SUPERCLASSE (Base)
public class Lavoratore {
    // 'protected' permette alle classi figlie di manipolare direttamente la variabile,
    // mantenendola inaccessibile al mondo esterno (Information Hiding preservato parzialmente).
    protected double stipendioBase; 
    private String nome;
    
    public Lavoratore(String nome, double stipendioBase) {
        this.nome = nome;
        this.stipendioBase = stipendioBase;
    }
    
    public void calcolaPaga() {
        System.out.println("Paga del lavoratore " + nome + ": €" + stipendioBase);
    }
}

// SOTTOCLASSE (Derivata)
public class Manager extends Lavoratore {
    private double bonusProduzione;
    
    public Manager(String nome, double stipendioBase, double bonusProduzione) {
        // 1. CHIAMATA A SUPER(): Deve essere rigorosamente la PRIMA riga eseguibile!
        // Inizializza l'anima "Lavoratore" che risiede dentro al Manager.
        super(nome, stipendioBase); 
        this.bonusProduzione = bonusProduzione;
    }
    
    // 2. OVERRIDING (Riscrittura del metodo)
    // Usiamo l'annotazione @Override per chiedere al compilatore di vigilare sulle firme.
    @Override
    public void calcolaPaga() {
        double pagaTotale = stipendioBase + bonusProduzione; // Uso variabile protected
        System.out.println("Paga del MANAGER: €" + pagaTotale + " (Bonus incluso)");
        
        // Se volessimo riutilizzare il comportamento originale del padre senza sovrascriverlo del tutto:
        // super.calcolaPaga();
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Errore di Firma nell'Overriding:** Se per sovrascrivere `calcolaPaga()` scrivi `public void calcolaPaga(int ore)`, stai commettendo un errore letale: hai appena fatto *Overloading* (creato un nuovo metodo), e non *Overriding*. A runtime, il polimorfismo invocherà il vecchio metodo del padre. Usa **sempre** `@Override`: se sbagli firma, il compilatore lancerà un errore impedendoti di procedere.
- **Dimenticare il `super` con padri complessi:** Se la classe `Veicolo` ha solo il costruttore `Veicolo(String marca)`, la figlia `Automobile` non compilerà finché non scrivi esplicitamente `super("Fiat")` nella prima riga del suo costruttore.
- **Rompere l'Information Hiding con `protected`:** L'abuso di `protected` per evitare di scrivere i getter spezza l'incapsulamento tra classi del medesimo package. Usalo saggiamente, preferendo di base `private` ovunque sia possibile.

---

## 3. Classi Astratte e Polimorfismo (Il Cuore della OOP)

### Teoria Fondamentale: Late Binding e V-Table
Il **Polimorfismo** (dal greco "molte forme") è il concetto più sublime e potente dell'ingegneria del software orientata agli oggetti. Si poggia su una regola d'oro del compilatore: **"Un riferimento di una Superclasse può puntare e governare un'istanza di una Sottoclasse"**. In breve: un puntatore di tipo `Animale` può agganciare in memoria Heap un oggetto fisico `Cane`.

Ma cosa succede se invochiamo un metodo? 
> **Definizione Accademica (Dynamic Method Dispatch / Late Binding):**
> Quando invochi `animale.faiVerso()`, il compilatore non sa se farà "Miao" o "Bau". Il collegamento tra il nome del metodo e la funzione fisica in memoria viene risolto solo al volo, in frazioni di secondo, a *tempo di esecuzione* (Runtime). La JVM ispeziona la natura nuda e reale dell'oggetto che risiede nell'Heap (es. scorge che è un `Cane`) e invoca spietatamente il metodo `faiVerso()` sovrascritto dalla classe `Cane`, ignorando totalmente il tipo del riferimento. 
> Per farlo velocemente, la JVM usa sotto il cofano una struttura in C++ chiamata **V-Table (Virtual Method Table)**, un array di puntatori a funzione.

Le **Classi Astratte (`abstract`)** estremizzano questo concetto. Rappresentano "concetti platonici" (es. la `FormaGeometrica`), troppo astratti per avere senso compiuto nel mondo reale. Esse:
- Non possono essere istanziate con la keyword `new`.
- Servono unicamente da scheletro per le figlie.
- Possono contenere **Metodi Astratti**: metodi privi di corpo (es. `public abstract double calcolaArea();`). Questi si comportano come contratti dittatoriali: obbligano il programmatore che scriverà le Sottoclassi (es. `Cerchio`) a fornire materialmente il codice per quel metodo, pena la non compilabilità.

### Sintassi ed Esempi di Codice: Upcasting, Downcasting e `instanceof`
```java
// CLASSE ASTRATTA: Non istanziabile. Modella un concetto.
public abstract class Animale {
    private String razza;
    
    public Animale(String razza) { this.razza = razza; }
    
    // Contratto vincolante: ogni figlio dovrà sapere come muoversi!
    public abstract void muoviti();
}

public class Uccello extends Animale {
    public Uccello() { super("Volatile"); }
    
    @Override
    public void muoviti() { System.out.println("Volo sbattendo le ali!"); }
    
    public void becca() { System.out.println("Becco i semi."); }
}

public class Pesce extends Animale {
    public Pesce() { super("Acquatico"); }
    
    @Override
    public void muoviti() { System.out.println("Nuoto muovendo le pinne!"); }
}

public class PolimorfismoAvanzato {
    public static void main(String[] args) {
        
        // 1. UPCASTING (Implicito e Sicuro al 100%)
        // Un riferimento 'padre' punta a un oggetto 'figlio'.
        Animale pet1 = new Uccello();
        Animale pet2 = new Pesce();
        
        // 2. POLIMORFISMO IN AZIONE (Late Binding)
        // Stessa riga di codice, risultati magicamente diversi in base all'Heap.
        pet1.muoviti(); // Stampa "Volo sbattendo le ali!"
        pet2.muoviti(); // Stampa "Nuoto muovendo le pinne!"
        
        // ERRORE ACCADEMICO! Il compilatore valuta il TIPO DEL RIFERIMENTO (Animale).
        // Animale non ha un metodo becca(), anche se in memoria c'è un Uccello.
        // pet1.becca(); // <-- NON COMPILA!
        
        // 3. DOWNCASTING E SICUREZZA (instanceof)
        // Per recuperare le funzionalità specifiche di 'Uccello', dobbiamo fare Downcasting (restringimento).
        // Il Downcasting è pericoloso: se 'pet1' fosse un Pesce, la JVM crasherebbe con ClassCastException!
        // Dobbiamo usare 'instanceof' per verificare la vera natura prima di castare.
        if (pet1 instanceof Uccello) {
            Uccello u = (Uccello) pet1; // Downcast esplicito
            u.becca(); // Ora possiamo invocare becca() in sicurezza.
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **`new Animale()` fallisce:** Tentare di allocare memoria per una classe marcata come `abstract` genera errore. Solo le classi concrete possono popolare l'Heap.
- **Dimenticare l'implementazione astratta:** Se un `Cerchio extends FormaGeometrica` ma tu non scrivi l'override per `calcolaArea()`, il compilatore rifiuterà la classe `Cerchio` dicendoti che deve essere dichiarata anch'essa `abstract`. Le figlie concrete devono onorare tutti i contratti!
- **ClassCastException nel Downcasting:** Scrivere `Pesce p = (Pesce) pet1;` è un gravissimo azzardo (Downcasting Cieco). Siccome `pet1` nasconde un `Uccello`, a runtime la JVM lancerà `ClassCastException` mandando in crash l'applicazione. Non fidarti mai del cast tra oggetti senza prima aver interpellato l'operatore di guardia `instanceof`.

---

> ⚠️ **SEGNALAZIONE: ARGOMENTI MANCANTI E DA SPOSTARE RISPETTO AL NUOVO SYLLABUS**
> In base alla nuova organizzazione a 7 livelli, in questo file mancano i seguenti argomenti (che appartengono al Livello 2):
> - **Variabili di Classe (Static) e Costanti:** L'uso della keyword `static` per variabili condivise e `static final` per le costanti.
> - **Inner Classes (Classi Interne):** La definizione e l'utilità delle classi private annidate all'interno di classi esterne per nascondere la logica interna.
> 
> *Nota Strutturale:* La teoria su **Ereditarietà**, **Polimorfismo** e **Classi Astratte** (attualmente presente qui) andrebbe formalmente spostata nel file `LESSON.md` del **Livello 3**.