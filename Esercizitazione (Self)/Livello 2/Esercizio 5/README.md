# Esercizio 5 – Inner Classes e Linked List / Inner Classes and Linked List

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio introduce l'uso delle **classi interne (inner classes)** per implementare una struttura dati classica: la **lista concatenata (Linked List)** di stringhe.

Il programma:
- Definisce una classe `StringLinkedList` che gestisce la lista.
- Utilizza una classe interna privata `ListNode` per rappresentare i singoli nodi della lista.
- Implementa metodi per l'inserimento in testa (`addHead`) e in coda (`addTail`).
- Utilizza la **reflection** nel `Main` per ispezionare la struttura interna della lista senza violarne l'incapsulamento.

### Obiettivo didattico
- Comprendere l'utilità delle classi interne per raggruppare componenti logici privati.
- Apprendere il funzionamento dei puntatori e dei collegamenti tra nodi.
- Gestione della memoria dinamica e dei riferimenti in Java.

### Esempio di Output
```text
==== Stato iniziale ====
Contenuto lista: []

==== Dopo addHead("Pane") ====
Contenuto lista: [Pane]

==== Dopo addHead("Latte") ====
Contenuto lista: [Latte, Pane]

==== Dopo addTail("Uova") ====
Contenuto lista: [Latte, Pane, Uova]

==== Dopo addTail("Burro") ====
Contenuto lista: [Latte, Pane, Uova, Burro]
```

---

## 🇬🇧 English

### Description
This exercise introduces the use of **inner classes** to implement a classic data structure: a **Linked List** of strings.

The program:
- Defines a `StringLinkedList` class to manage the list.
- Uses a private inner class `ListNode` to represent individual nodes.
- Implements methods for inserting at the beginning (`addHead`) and at the end (`addTail`).
- Uses **reflection** in the `Main` class to inspect the list's internal structure without violating encapsulation.

### Learning Objective
- Understand the purpose of inner classes for grouping private logical components.
- Learn how pointers and links between nodes work.
- Manage dynamic memory and references in Java.

### Output Example
```text
==== Initial State ====
List content: []

==== After addHead("Bread") ====
List content: [Bread]

==== After addHead("Milk") ====
List content: [Milk, Bread]

==== After addTail("Eggs") ====
List content: [Milk, Bread, Eggs]

==== After addTail("Butter") ====
List content: [Milk, Bread, Eggs, Butter]
```
