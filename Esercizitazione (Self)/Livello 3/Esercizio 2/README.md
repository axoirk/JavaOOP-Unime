# Esercizio 2 – Classi Astratte e Polimorfismo / Abstract Classes and Polymorphism

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio approfondisce l'uso delle **classi astratte** e del **polimorfismo dinamico** attraverso la rappresentazione di forme geometriche.

Il programma:
- Utilizza una classe astratta `ShapeBase` come modello comune per tutte le forme.
- Implementa le classi concrete `Rectangle` e `Triangle` che estendono `ShapeBase`.
- Utilizza un array di tipo `ShapeBase[]` per gestire oggetti di diverse sottoclassi in modo uniforme.
- Dimostra il **Late Binding**: il metodo `drawHere()` viene risolto a runtime in base all'oggetto effettivo puntato dal riferimento.

### Obiettivo didattico
- Definire contratti comportamentali con metodi astratti.
- Gestire collezioni eterogenee grazie al polimorfismo.
- Comprendere l'importanza dell'astrazione nel design del software.

### Esempio di Output
```text
  *
 * *
*****
*****
*   *
*****
  *
 * *
*****
*****
*   *
*****
```

---

## 🇬🇧 English

### Description
This exercise explores the use of **abstract classes** and **dynamic polymorphism** by representing geometric shapes.

The program:
- Uses an abstract class `ShapeBase` as a common template for all shapes.
- Implements concrete classes `Rectangle` and `Triangle` that extend `ShapeBase`.
- Uses an array of type `ShapeBase[]` to manage objects of different subclasses uniformly.
- Demonstrates **Late Binding**: the `drawHere()` method is resolved at runtime based on the actual object the reference points to.

### Learning Objective
- Define behavioral contracts using abstract methods.
- Manage heterogeneous collections through polymorphism.
- Understand the importance of abstraction in software design.

### Output Example
```text
  *
 * *
*****
*****
*   *
*****
  *
 * *
*****
*****
*   *
*****
```
