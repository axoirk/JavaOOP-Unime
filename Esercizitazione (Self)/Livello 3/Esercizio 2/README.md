# Esercizio 5 – Classe Astratta e Polimorfismo / Abstract Class and Polymorphism

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio approfondisce concetti centrali della Programmazione a Oggetti: **astrazione**, **ereditarieta** e **polimorfismo**.

Viene definita una classe astratta `ShapeBase` che dichiara il metodo astratto:
- `drawHere()`

Due classi concrete la estendono:
- `Triangle` (stampa un triangolo ASCII)
- `Rectangle` (stampa un rettangolo ASCII)

Nel `Main` viene creato un array di tipo base `ShapeBase[]` e popolato alternativamente con istanze di `Triangle` e `Rectangle`. Ogni elemento viene poi disegnato invocando lo stesso metodo `drawHere()`.

### Obiettivo didattico (OOP essenziale)
L'esercizio mostra in pratica come:
- definire un **contratto comune** tramite classe astratta;
- forzare le sottoclassi a implementare il comportamento specifico (`drawHere`);
- trattare oggetti diversi con la **stessa interfaccia** (`ShapeBase`);
- sfruttare il **dynamic dispatch**: a runtime viene eseguita l'implementazione corretta in base al tipo reale (`Triangle` o `Rectangle`);
- progettare codice estendibile (aggiungere nuove forme senza modificare la logica principale di iterazione/stampa).

### Approfondimenti essenziali (nuovi in questo esercizio)
- **Perche classe astratta e non classe concreta**: `ShapeBase` non rappresenta una forma specifica da disegnare, ma una categoria comune. Renderla astratta impedisce istanze incomplete e comunica chiaramente il ruolo architetturale della classe.
- **Sostituibilita (Liskov, in pratica)**: ogni `Triangle` o `Rectangle` puo essere usato dove e richiesto `ShapeBase`, senza cambiare il codice client. Questo rende il `Main` indipendente dai dettagli delle singole forme.
- **Polimorfismo reale, non solo sintassi**: il valore didattico e che la chiamata `shape.drawHere()` resta identica, mentre il comportamento cambia in base all'oggetto concreto. E il passaggio chiave dall'approccio procedurale a quello object-oriented.
- **Open/Closed applicato**: per aggiungere una nuova forma (es. `Diamond`) basta creare `class Diamond extends ShapeBase` e implementare `drawHere()`. La logica di iterazione esistente resta invariata.
- **Contratto minimo e coesione**: `ShapeBase` espone solo cio che tutte le forme devono garantire (`drawHere`). Questo riduce accoppiamento e mantiene alta la coesione delle classi concrete.

### Struttura e comportamento del codice
Flusso principale:
1. `ShapeBase[] shapes = new ShapeBase[8];`
2. Ciclo di inizializzazione: indice pari → `Triangle`, indice dispari → `Rectangle`
3. Ciclo di esecuzione: per ogni elemento dell'array, chiamata uniforme `shape.drawHere()`

Dettagli delle implementazioni:
- `Triangle.drawHere()` costruisce un triangolo centrato con spazi iniziali e asterischi;
- `Rectangle.drawHere()` stampa bordo superiore/inferiore e righe interne cave;
- ogni disegno termina con una linea separatrice (`----------`) per distinguere le figure in output.

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Crea un array polimorfico di `ShapeBase`, istanzia forme diverse e richiama `drawHere()` su ciascun elemento |
| `ShapeBase.java` | Classe astratta che definisce il contratto comune con il metodo astratto `drawHere()` |
| `Triangle.java` | Sottoclasse concreta che implementa `drawHere()` per disegnare un triangolo ASCII |
| `Rectangle.java` | Sottoclasse concreta che implementa `drawHere()` per disegnare un rettangolo ASCII |

### Concetti trattati (approfonditi)
- Classe astratta (`abstract class`)
- Metodo astratto (`abstract method`)
- Ereditarieta con `extends`
- Polimorfismo su tipo base (`ShapeBase`)
- Override con `@Override`
- Dynamic dispatch (binding dinamico)
- Separazione tra contratto comune e implementazioni concrete
- Estendibilita del design OOP (Open/Closed in forma pratica)

### Esempio di esecuzione
```
    *
   ***
  *****
 *******
*********

----------
**********
*        *
*        *
*        *
*        *
*        *
**********

----------
...
```

---

## 🇬🇧 English

### Description
This exercise focuses on key OOP concepts: **abstraction**, **inheritance**, and **polymorphism**.

An abstract class `ShapeBase` defines the abstract method:
- `drawHere()`

Two concrete subclasses extend it:
- `Triangle` (prints an ASCII triangle)
- `Rectangle` (prints an ASCII rectangle)

In `Main`, a `ShapeBase[]` array is created and filled alternately with `Triangle` and `Rectangle` instances. Then, each element is rendered through the same `drawHere()` call.

### Learning objective (essential OOP)
The exercise demonstrates how to:
- define a **shared contract** using an abstract class;
- force subclasses to provide concrete behavior (`drawHere`);
- handle different objects through a **single common type** (`ShapeBase`);
- rely on **dynamic dispatch** so the runtime selects the correct implementation (`Triangle` or `Rectangle`);
- build extensible code (new shapes can be added without changing the main iteration logic).

### Essential deep-dive points (new in this exercise)
- **Why an abstract class instead of a concrete one**: `ShapeBase` is not a specific drawable shape; it is a common category. Making it abstract prevents incomplete instantiation and clearly communicates architectural intent.
- **Substitutability (practical Liskov)**: every `Triangle` or `Rectangle` can be used wherever `ShapeBase` is expected, without changing client code. This keeps `Main` independent from shape-specific details.
- **Real polymorphism, not just syntax**: the key learning point is that `shape.drawHere()` stays the same call while behavior changes with the concrete runtime type.
- **Open/Closed in practice**: adding a new shape (e.g., `Diamond`) requires only `class Diamond extends ShapeBase` plus `drawHere()` implementation. Existing iteration logic remains untouched.
- **Minimal contract and cohesion**: `ShapeBase` exposes only what every shape must guarantee (`drawHere`), reducing coupling and keeping concrete classes cohesive.

### Code flow and behavior
Main flow:
1. `ShapeBase[] shapes = new ShapeBase[8];`
2. Initialization loop: even index → `Triangle`, odd index → `Rectangle`
3. Execution loop: uniform call `shape.drawHere()` for each element

Implementation details:
- `Triangle.drawHere()` prints a centered triangle using leading spaces and stars;
- `Rectangle.drawHere()` prints top/bottom borders and hollow inner lines;
- each rendered shape ends with a separator line (`----------`) for readability.

### Files
| File | Description |
|------|-------------|
| `Main.java` | Creates a polymorphic `ShapeBase` array, instantiates different shapes, and calls `drawHere()` on each element |
| `ShapeBase.java` | Abstract base class defining the shared contract through abstract `drawHere()` |
| `Triangle.java` | Concrete subclass implementing `drawHere()` to render an ASCII triangle |
| `Rectangle.java` | Concrete subclass implementing `drawHere()` to render an ASCII rectangle |

### Concepts covered (in depth)
- Abstract class (`abstract class`)
- Abstract method (`abstract method`)
- Inheritance via `extends`
- Polymorphism on base type (`ShapeBase`)
- Method overriding with `@Override`
- Dynamic dispatch (runtime binding)
- Contract vs concrete implementations
- Extensible OOP design (practical Open/Closed principle)

### Sample run
```
    *
   ***
  *****
 *******
*********

----------
**********
*        *
*        *
*        *
*        *
*        *
**********

----------
...
```
