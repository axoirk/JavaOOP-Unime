# Livello 2: La Programmazione Orientata agli Oggetti - OOP

## 1. Classi, Oggetti e Incapsulamento

### Teoria Fondamentale
Il paradigma Object-Oriented modella il dominio del problema creando entità (Oggetti) che comunicano tra loro. 

> **Definizione Accademica (Classe vs Oggetto):**
> Una **Classe** è il "progetto" o *blueprint* a livello concettuale: definisce la struttura dei dati (variabili d'istanza) e i comportamenti (metodi). Un **Oggetto** è una specifica istanza creata a runtime in memoria heap, partendo da quella classe.

L'**Incapsulamento (Information Hiding)** è il principio secondo il quale lo stato interno di un oggetto non deve essere manipolabile dall'esterno in modo incontrollato. I dati sono marcati come `private` ed esposti tramite metodi `public` (Pattern Getter/Setter), che si occupano della validazione.

L'**Overloading (Sovraccarico dei Metodi)** consente a una classe di avere più metodi (inclusi i Costruttori) con lo *stesso nome*, purché abbiano firme diverse (diverso numero o tipo di parametri).

### Sintassi ed Esempi di Codice
```java
public class Studente {
    // Variabili d'istanza incapsulate (Information Hiding)
    private String nome;
    private int eta;
    
    // Costruttore 1 (Vuoto / Default)
    public Studente() {
        this.nome = "Sconosciuto";
        this.eta = 18;
    }
    
    // Costruttore 2 (Overloading con parametri)
    public Studente(String nome, int eta) {
        this.nome = nome;
        setEta(eta); // Uso il setter per la validazione!
    }
    
    // Getter
    public String getNome() {
        return this.nome;
    }
    
    // Setter con validazione dello stato
    public void setEta(int eta) {
        if (eta > 0 && eta <= 120) {
            this.eta = eta;
        } else {
            System.out.println("Errore: Età non valida.");
            this.eta = 18; // Fallback di default
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Bypassare i Setter nel Costruttore:** Errore classico. Nei costruttori bisogna invocare i metodi Setter per evitare di duplicare la logica di validazione e rischiare stati inconsistenti.
- **Riferimento `this`:** È una best practice accademica usare sempre `this.variabile` per risolvere ambiguità di shadowing quando i parametri hanno lo stesso nome delle variabili d'istanza.
- **Dimenticare i Costruttori:** Se non scrivi costruttori, Java ne inserisce uno vuoto di default. Ma se ne scrivi almeno uno (es. con parametri), quello vuoto non è più generato e, se necessario, dovrai scriverlo tu.

---

## 2. Ereditarietà

### Teoria Fondamentale
L'ereditarietà instaura una relazione forte di tipo **"is-a" (è-un)** tra una Sottoclasse (figlia) e una Superclasse (madre). 

> **Nota del Docente (Visibilità `protected`):**
> Il modificatore `protected` indica che una variabile d'istanza è invisibile al mondo esterno, ma è visibile (ereditata direttamente) dalle sottoclassi e dalle classi dello stesso package.

L'**Overriding** è la riscrittura di un metodo della superclasse all'interno della sottoclasse. Mantieni esattamente la stessa firma, ma modifichi il comportamento interno.

| Modificatore | Visibilità in Classe | Nel Package | In Sottoclasse | Mondo Esterno |
| --- | --- | --- | --- | --- |
| `private` | ✅ Sì | ❌ No | ❌ No | ❌ No |
| `(default)` | ✅ Sì | ✅ Sì | ❌ No | ❌ No |
| `protected` | ✅ Sì | ✅ Sì | ✅ Sì | ❌ No |
| `public` | ✅ Sì | ✅ Sì | ✅ Sì | ✅ Sì |

### Sintassi ed Esempi di Codice
```java
// Superclasse
public class Persona {
    protected String codiceFiscale; // Visibile alle sottoclassi
    
    public Persona(String codiceFiscale) {
        this.codiceFiscale = codiceFiscale;
    }
    
    public void stampaIdentita() {
        System.out.println("Persona generica con CF: " + codiceFiscale);
    }
}

// Sottoclasse
public class Docente extends Persona {
    private String dipartimento;
    
    public Docente(String codiceFiscale, String dipartimento) {
        // Chiamata OBBLIGATORIA al costruttore della superclasse
        super(codiceFiscale); 
        this.dipartimento = dipartimento;
    }
    
    // Method Overriding
    @Override
    public void stampaIdentita() {
        // Uso 'super' per invocare il metodo della superclasse prima del codice aggiuntivo
        super.stampaIdentita(); 
        System.out.println("Docente del dipartimento: " + dipartimento);
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Errore di Firma nell'Overriding:** Se sbagli anche solo una maiuscola, stai facendo *Overloading*, non Overriding. Il compilatore non ti avviserà a meno che tu non usi l'annotazione `@Override`, che genera un errore se non stai effettivamente sovrascrivendo nulla. Usala SEMPRE!
- **Posizione del `super()`:** La chiamata a `super(...)` all'interno del costruttore figlio deve essere **rigorosamente la prima riga di codice**. Inserirla dopo genera un errore di sintassi.

---

## 3. Classi Astratte e Polimorfismo

### Teoria Fondamentale
Le classi astratte fungono da "contratti parziali". Possono contenere variabili e metodi implementati, ma anche **metodi astratti** (metodi privi di corpo). Non possono essere istanziate direttamente tramite `new`.

> **Definizione Accademica (Polimorfismo e Associazione Dinamica):**
> Il **Polimorfismo** (dal greco "molte forme") è l'abilità di una variabile riferimento di tipo Superclasse di puntare a un'istanza di una Sottoclasse. 
> Grazie all'**Associazione Dinamica (Late Binding)**, quando invochi un metodo sovrascritto, la JVM decide *a tempo di esecuzione* quale versione del metodo eseguire (quella della figlia), basandosi sul tipo dell'oggetto effettivo in memoria (heap), e non sul tipo del riferimento.

### Sintassi ed Esempi di Codice
```java
// Classe Astratta
public abstract class Animale {
    private String nome;
    
    public Animale(String nome) {
        this.nome = nome;
    }
    
    // Metodo astratto: niente corpo, solo la firma. Obbliga i figli a implementarlo!
    public abstract void emettiVerso();
    
    public String getNome() { return nome; }
}

public class Cane extends Animale {
    public Cane(String nome) { super(nome); }
    
    @Override
    public void emettiVerso() {
        System.out.println("Bau! Sono " + getNome());
    }
}

public class Gatto extends Animale {
    public Gatto(String nome) { super(nome); }
    
    @Override
    public void emettiVerso() {
        System.out.println("Miao! Sono " + getNome());
    }
}

public class TestPolimorfismo {
    public static void main(String[] args) {
        // Array Polimorfico (riferimenti della Superclasse)
        Animale[] zoo = new Animale[2];
        
        zoo[0] = new Cane("Fido"); // Upcasting implicito
        zoo[1] = new Gatto("Silvestro");
        
        for (Animale a : zoo) {
            // Late Binding: invoca la versione specifica di Cane o Gatto a Runtime
            a.emettiVerso(); 
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **`new Animale()` fallisce:** Istanziare direttamente una classe astratta causa errore a tempo di compilazione. Serve sempre una classe concreta (figlia) per l'istanza.
- **Dimenticare l'implementazione:** Se una classe eredita da un'astratta e non implementa *tutti* i metodi astratti, essa stessa deve essere dichiarata a sua volta astratta, altrimenti si spacca la compilazione.
- **Sottotipo e Supertipo:** Puoi sempre assegnare una figlia a un riferimento padre (es. `Animale a = new Cane();`), ma mai viceversa (`Cane c = new Animale();` genera ClassCastException).