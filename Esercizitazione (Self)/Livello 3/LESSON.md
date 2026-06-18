# Livello 3: OOP Avanzata e Gestione degli Errori

## 1. Ereditarietà e Relazione Gerarchica

### Teoria Fondamentale: La Relazione "IS-A"
L'**Ereditarietà** permette di creare nuove classi basandosi su classi esistenti, ereditandone metodi e variabili. Si stabilisce una relazione di tipo **"is-a" (è un)**.

**Esempio Teorico: Il Mondo Animale**
Un `Cane` *è un* `Animale`. Un `Gatto` *è un* `Animale`.
In questa gerarchia, `Animale` è la **Superclasse** (più generica), mentre `Cane` e `Gatto` sono le **Sottoclassi** (più specifiche).

### Sintassi ed Esempi di Codice
```java
// SUPERCLASSE
public class Animale {
    protected String nome;

    public Animale(String nome) {
        this.nome = nome;
    }

    public void emettiSuono() {
        System.out.println("L'animale emette un suono generico.");
    }
}

// SOTTOCLASSE
public class Cane extends Animale {
    public Cane(String nome) {
        // Chiamata al costruttore della superclasse
        super(nome);
    }

    @Override
    public void emettiSuono() {
        System.out.println(nome + " dice: Bau Bau!");
    }
}
```

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
