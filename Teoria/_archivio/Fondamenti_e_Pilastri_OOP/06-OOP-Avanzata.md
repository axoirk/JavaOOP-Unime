# 06. OOP Avanzata: Ereditarietà, Polimorfismo e Astrazione

L'Incapsulamento protegge il singolo oggetto. Ma quando i software scalano verso architetture enterprise (come i gestionali bancari o i motori grafici), è necessario orchestrare decine di classi diverse evitando ridondanze. Qui entrano in gioco l'Ereditarietà e l'ultimo, definitivo pilastro: il Polimorfismo.

## Il Secondo Pilastro: L'Ereditarietà

L'Ereditarietà è un meccanismo che permette a una nuova classe di assorbire l'intero patrimonio genetico (stato e comportamento) di una classe preesistente, per poi espanderlo o modificarlo. Formalizza una fortissima relazione gerarchica del tipo **"is-a" (è-un)**.

Si utilizza la parola chiave **`extends`** per indicare che la classe derivata (*Sottoclasse* o *Figlia*) estende la classe base (*Superclasse* o *Padre*).

> **L'ereditarietà in Java è strettamente SINGOLA.**
> A differenza del C++, in Java una classe può avere una e una sola Superclasse diretta. Questo previene il famigerato "Problema del Diamante" (ambiguità su quale metodo ereditare in presenza di padri multipli). 

```java
// SUPERCLASSE (Base)
public class Veicolo {
    protected String marca; // 'protected' lo rende visibile ai figli
    
    public Veicolo(String marca) {
        this.marca = marca;
    }
    
    public void muovi() {
        System.out.println("Il veicolo si sta muovendo.");
    }
}

// SOTTOCLASSE (Derivata)
public class Motocicletta extends Veicolo {
    private boolean haSidecar;
    
    public Motocicletta(String marca, boolean haSidecar) {
        // La keyword 'super' invoca obbligatoriamente il costruttore del Padre
        super(marca); 
        this.haSidecar = haSidecar;
    }
}
```

### Overloading vs Overriding: La Guerra dei Metodi
Non bisogna confondere i due concetti più omofoni della OOP:
- L'**Overloading (Sovraccarico):** Si ha nella *stessa classe*. Definisco più metodi con lo stesso identico nome, ma con **parametri diversi**. Utile per fornire opzioni alternative (es. `stampa(int x)` e `stampa(String s)`).
- L'**Overriding (Riscrittura):** Si ha *tra padre e figlio*. La Sottoclasse decide di ribellarsi al Padre ereditato, fornendo una propria implementazione a un metodo. Affinché sia valido, la "firma" del metodo (nome, parametri e tipo di ritorno) deve essere **assolutamente identica** a quella del Padre. Si decora accademica mente con l'annotazione `@Override` per forzare il compilatore a controllare l'assenza di refusi.

## Il Terzo Pilastro: Il Polimorfismo e il Late Binding

Il Polimorfismo (dal greco, "capacità di assumere molte forme") è il concetto più sublime e intellettualmente potente della OOP. Permette di trattare oggetti di natura diversa come se appartenessero allo stesso tipo, delegando l'esecuzione dell'azione corretta al motore di esecuzione.

Si basa su un principio chimico di Java: **Un riferimento di tipo Superclasse può puntare tranquillamente a un'istanza (oggetto) di una qualsiasi Sottoclasse.** 
Un riferimento `Veicolo` può puntare a un oggetto fisico `Motocicletta` creato nell'Heap.

```java
public class SistemaTraffico {
    public static void main(String[] args) {
        // Array Polimorfico: Il contenitore è "generico", il contenuto è "specifico".
        Veicolo[] garage = new Veicolo[2];
        
        garage[0] = new Veicolo("Ford");
        garage[1] = new Motocicletta("Ducati", false); // Magia Polimorfica!
        
        // Iterazione cieca
        for (Veicolo v : garage) {
            // Quale metodo 'muovi()' verrà eseguito? 
            // Quello del Veicolo o quello (sovrascritto) della Motocicletta?
            v.muovi(); 
        }
    }
}
```

### L'Associazione Dinamica (Late Binding)
Come fa la JVM a sapere quale versione del metodo `muovi()` eseguire nel ciclo? Usa l'**Associazione Dinamica**. 
In fase di compilazione, il codice sembra invocare il metodo della classe padre (il riferimento è `Veicolo`). Ma *a tempo di esecuzione* (runtime), la JVM scarta il tipo del riferimento e guarda la vera, nuda natura dell'oggetto stivato nell'Heap. Se nell'Heap trova una Motocicletta, eseguirà implacabilmente il metodo sovrascritto dalla Motocicletta, anche se l'etichetta esterna dice "Veicolo". Questo permette di scrivere codice generico che non ha bisogno di conoscere l'esatto tipo degli oggetti in anticipo.

## L'Astrazione Formale: Classi Astratte e Interfacce

A volte una Superclasse è un concetto così vago e teorico (es. la classe *FormaGeometrica*) che non ha alcun senso permettere a qualcuno di istanziarla (creare una "FormaGeometrica" senza specificare se sia un cerchio o un quadrato è illogico).

1. **Classi Astratte (`abstract class`):** Sono classi incomplete. Non possono mai essere istanziate con `new`. Servono unicamente come fondamenta (scheletri) per le sottoclassi. Possono contenere **metodi astratti** (metodi scritti a metà, privi di parentesi graffe e corpo), che obbligano come una dittatura le classi figlie a implementarli, garantendo che ogni forma geometrica creata in futuro avrà per forza un metodo `calcolaArea()`.

2. **Interfacce (`interface`):** Rappresentano il livello massimo di astrazione. Un'interfaccia non è una classe, è un **Contratto di Comportamento puro**. Non può avere stato interno (niente variabili d'istanza) e definisce solo firme di metodi pubblici. 
Poiché in Java l'ereditarietà (extends) è singola, le interfacce risolvono il problema permettendo l'**implementazione multipla** (`implements`). Una classe può ereditare da un solo padre, ma può firmare infiniti contratti (interfacce), assorbendo così abilità trasversali (es. un'Auto `extends Veicolo` ma contemporaneamente `implements Assicurabile, Rottamabile`).