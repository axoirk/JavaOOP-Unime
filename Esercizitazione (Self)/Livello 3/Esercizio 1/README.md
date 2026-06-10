# Esercizio 4 – Ereditarieta e Override / Inheritance and Method Overriding

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio introduce uno dei pilastri fondamentali della Programmazione a Oggetti: **l'ereditarieta**.

L'obiettivo e mostrare come una classe specializzata possa:
1. **riutilizzare** il codice della classe base,
2. **estendere** lo stato con nuovi attributi,
3. **ridefinire** il comportamento con l'override dei metodi.

Nel progetto:
- `Person` rappresenta la classe base (superclasse) con l'attributo `name`;
- `Student` rappresenta la sottoclasse che **estende** `Person` e aggiunge `matricola`;
- il metodo `writeOutput()` viene ridefinito in `Student` con `@Override`.

### Obiettivo didattico (OOP essenziale)
L'esercizio chiarisce i concetti essenziali necessari per affrontare correttamente l'OOP:
- **Generalizzazione/Specializzazione**: `Person` come concetto generale, `Student` come caso specifico;
- **Riutilizzo del codice**: con `extends` si evita duplicazione;
- **Ereditarieta dei membri**: `Student` eredita i metodi pubblici/protetti della classe padre;
- **Polimorfismo**: una variabile di tipo `Person` puo riferirsi a un oggetto `Student`;
- **Binding dinamico**: la chiamata a `writeOutput()` usa la versione effettiva dell'oggetto a runtime;
- **Uso di `super`**: `super(name)` nel costruttore e `super.writeOutput()` nel metodo override;
- **Contratto del metodo**: con `@Override` il compilatore verifica la corretta ridefinizione.

### Struttura e comportamento del codice
Il `Main` crea due riferimenti di tipo `Person`:
- un oggetto realmente `Person` (`new Person("Giulia")`);
- un oggetto realmente `Student` (`new Student("Marco", 12345)`), assegnato a un riferimento `Person`.

Quando viene invocato `writeOutput()`:
- nel primo caso esegue `Person.writeOutput()`;
- nel secondo caso esegue `Student.writeOutput()`, che:
  - richiama `super.writeOutput()` per stampare il nome,
  - poi stampa la matricola.

Questo passaggio e cruciale per comprendere il polimorfismo in Java.

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Crea oggetti `Person` e `Student`, mostra il comportamento polimorfico tramite chiamate a `writeOutput()` |
| `Person.java` | Superclasse con attributo `name`, costruttore, getter/setter e metodo base `writeOutput()` |
| `Student.java` | Sottoclasse di `Person`, aggiunge `matricola` e ridefinisce `writeOutput()` usando `@Override` e `super` |

### Concetti trattati (approfonditi)
- Ereditarieta con `extends`
- Relazione **is-a** (`Student` is-a `Person`)
- Override dei metodi e annotazione `@Override`
- Uso di `super` in costruttori e metodi
- Polimorfismo con riferimenti al tipo base
- Dynamic dispatch (selezione del metodo a runtime)
- Incapsulamento tramite attributi `private` e metodi accessor/mutator
- Progettazione orientata al riuso e alla manutenibilita

### Esempio di esecuzione
```
Nome: Giulia
Nome: Marco
Matricola: 12345
```

---

## 🇬🇧 English

### Description
This exercise introduces one of the core pillars of Object-Oriented Programming: **inheritance**.

The goal is to show how a specialized class can:
1. **reuse** base-class code,
2. **extend** the state with new attributes,
3. **redefine** behavior through method overriding.

In this project:
- `Person` is the base class (superclass) with the `name` field;
- `Student` is the subclass that **extends** `Person` and adds `matricola` (student ID);
- `writeOutput()` is overridden in `Student` using `@Override`.

### Learning objective (essential OOP)
This exercise clarifies key OOP topics required for solid foundations:
- **Generalization/Specialization**: `Person` as a general model, `Student` as a specific one;
- **Code reuse**: `extends` avoids duplication;
- **Inherited members**: `Student` inherits accessible members from `Person`;
- **Polymorphism**: a `Person` reference can point to a `Student` object;
- **Dynamic binding**: method resolution happens at runtime based on actual object type;
- **`super` usage**: `super(name)` in constructor and `super.writeOutput()` in override;
- **Method contract checking**: `@Override` lets the compiler validate overriding correctness.

### Code flow and behavior
`Main` creates two references of type `Person`:
- a real `Person` object (`new Person("Giulia")`);
- a real `Student` object (`new Student("Marco", 12345)`) assigned to a `Person` reference.

When `writeOutput()` is called:
- first call executes `Person.writeOutput()`;
- second call executes `Student.writeOutput()`, which:
  - calls `super.writeOutput()` to print the inherited name,
  - then prints the student ID.

This is the central step to understand polymorphism in Java.

### Files
| File | Description |
|------|-------------|
| `Main.java` | Creates `Person` and `Student` objects and demonstrates polymorphic calls to `writeOutput()` |
| `Person.java` | Base class with `name`, constructor, getters/setters, and base `writeOutput()` method |
| `Student.java` | Subclass of `Person`, adds `matricola` and overrides `writeOutput()` using `@Override` and `super` |

### Concepts covered (in depth)
- Inheritance with `extends`
- **is-a** relationship (`Student` is-a `Person`)
- Method overriding and `@Override`
- `super` in constructors and methods
- Polymorphism with base-type references
- Dynamic dispatch (runtime method selection)
- Encapsulation with `private` fields and accessors/mutators
- Reuse-oriented, maintainable class design

### Sample run
```
Nome: Giulia
Nome: Marco
Matricola: 12345
```
