# Livello 3: OOP Avanzata e Gestione degli Errori

## 1. Ereditarietà e L'Uso della Keyword `super`

### Cos'è l'Ereditarietà? (La Relazione "IS-A")
L'**Ereditarietà** è il meccanismo che permette di creare una nuova classe (Sottoclasse) basata su una classe già esistente (Superclasse). 
- **Teoria:** Pensa all'ereditarietà in biologia. Un *Cane* eredita le caratteristiche base di un *Animale* (respirare, mangiare), ma poi aggiunge comportamenti propri (abbaiare, scodinzolare). Si dice che c'è una relazione **"is-a" (è un)**: il Cane *è un* Animale.
- **Perché usarla:** Per evitare di fare copia-incolla dello stesso codice in mille classi diverse. Se tutte le entità (Studenti, Professori, Segretari) hanno un `nome` e una `dataDiNascita`, scrivi quelle variabili e i getter/setter una sola volta in una Superclasse `Persona`.

---

### Lo scoglio principale: Che cos'è `super` e quando si usa?
La parola chiave `super` è semplicemente un **riferimento alla classe padre**. È come se dicessi a Java: *"Non guardare me (la classe in cui ti trovi ora), ma guarda la classe da cui ho ereditato."*

Si usa principalmente in due contesti fondamentali. Non bisogna confonderli:

#### Caso A: `super(...)` - Costruire le fondamenta (Il Costruttore)
**Teoria:** Quando crei un oggetto `Cane`, in memoria deve prima essere costruita la sua parte di `Animale` (le sue "fondamenta"). Se la classe padre ha un costruttore che *pretende* dei parametri (es. il `nome`), la sottoclasse è **obbligata** a fornirglieli. 
**Regola d'oro:** Lo si fa invocando `super(parametro)` come **primissima istruzione obbligatoria** nel costruttore della sottoclasse.

**Esempio Pratico:**
```java
public class Animale {
    protected String nome;

    // Costruttore del Padre: pretende un nome per nascere
    public Animale(String nome) {
        this.nome = nome;
    }
}

public class Cane extends Animale {
    private String razza;

    // Costruttore del Figlio: richiede nome e razza
    public Cane(String nome, String razza) {
        // 1. DEVI chiamare il costruttore del padre e passargli il nome. 
        // Se non metti super(), il compilatore si arrabbia!
        super(nome); 
        
        // 2. Solo DOPO aver costruito l'Animale, gestisci i dati specifici del Cane
        this.razza = razza;
    }
}
```

#### Caso B: `super.nomeMetodo()` - Aggiungere funzionalità, non cancellarle
**Teoria:** Spesso, in una sottoclasse, fai l'**Override** (sovrascrivi) di un metodo del padre perché vuoi cambiarne il comportamento. Ma cosa succede se vuoi *aggiungere* qualcosa al comportamento originale, senza buttare via il codice che il padre aveva già scritto? 
Usi `super.metodo()` per dire: *"Esegui la logica base che aveva scritto mio padre, e subito dopo ci aggiungo io il resto"*.

**Esempio Pratico:**
```java
public class Dipendente {
    public void lavora() {
        System.out.println("Timbra il cartellino e inizia a lavorare.");
    }
}

public class Manager extends Dipendente {
    
    @Override
    public void lavora() {
        // Voglio che il Manager timbri il cartellino come tutti i dipendenti...
        super.lavora(); 
        
        // ...ma poi fa il suo lavoro specifico!
        System.out.println("Organizza una riunione con il team.");
    }
}
```
In questo caso, chiamando `manager.lavora()`, stamperai ENTRAMBE le frasi. Se non avessi messo `super.lavora()`, il Manager avrebbe solo organizzato la riunione senza timbrare il cartellino!

---

## 2. Classi Astratte e Polimorfismo

### Teoria Fondamentale
Una **Classe Astratta** è una classe che non può essere istanziata direttamente. Serve come modello per altre classi. Può contenere **metodi astratti** (senza corpo) che le sottoclassi *devono* implementare.

Il **Polimorfismo** permette a un riferimento di una superclasse di puntare a un oggetto di una sottoclasse, decidendo quale metodo eseguire solo a tempo di esecuzione (Runtime).

### Esempio: Calcolo Volumi (Classi Astratte)
```java
public abstract class Solido {
    public abstract double calcolaVolume();
}

public class Cubo extends Solido {
    private double lato;
    public Cubo(double l) { this.lato = l; }

    @Override
    public double calcolaVolume() {
        return Math.pow(lato, 3);
    }
}
```

---

## 3. Le Interfacce (`interface`)

### Teoria Fondamentale: Il Ruolo dei Dispositivi
Un'**Interfaccia** definisce un contratto di comportamento. Mentre l'ereditarietà definisce *cosa un oggetto è*, l'interfaccia definisce *cosa un oggetto sa fare*.

**Esempio Teorico: Dispositivi Elettronici**
Molti dispositivi diversi possono essere "accesi" o "spenti". Non importa se è una `Lampadina`, un `Computer` o un `Tostapane`: se implementano l'interfaccia `Accendibile`, garantiscono la presenza dei metodi `accendi()` e `spegni()`.

### Sintassi ed Esempi di Codice
```java
public interface Accendibile {
    void accendi(); // implicitamente public abstract
    void spegni();
}

public class Televisore implements Accendibile {
    @Override
    public void accendi() {
        System.out.println("TV Accesa: Benvenuti!");
    }

    @Override
    public void spegni() {
        System.out.println("TV Spenta: Arrivederci.");
    }
}
```

---

## 4. Gestione delle Eccezioni

### Teoria Fondamentale
Le eccezioni sono eventi anomali che interrompono il normale flusso del programma. Java usa un sistema basato su oggetti per gestire questi errori.

- **Checked Exceptions**: Errori che il compilatore ci obbliga a gestire (es. apertura di un file inesistente).
- **Unchecked Exceptions**: Errori logici (es. divisione per zero, puntatore nullo) che derivano da `RuntimeException`.

### Sintassi: Try-Catch-Finally
```java
try {
    // Codice che potrebbe generare un errore
    int risultato = 10 / 0;
} catch (ArithmeticException e) {
    // Gestione dell'errore
    System.err.println("Errore: Divisione per zero!");
} finally {
    // Codice eseguito sempre
    System.out.println("Pulizia risorse.");
}
```
