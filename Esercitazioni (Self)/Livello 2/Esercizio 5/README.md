# Esercizio 5 – Inner Classes e Linked List

---

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

