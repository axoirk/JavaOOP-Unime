# Livello 5 - Esercizio 5: Comunicazione tra Thread / Inter-Thread Communication

---

## 🇮🇹 Italiano

### Obiettivo
Utilizzare i metodi `wait()` e `notify()` per coordinare l'accesso a una struttura dati condivisa, risolvendo il classico problema del "Produttore-Consumatore".

### Traccia (dal Syllabus)
1.  **Creare uno Stack condiviso** (o una coda limitata) per gestire dati.
2.  Implementare un thread **"Produttore"** che inserisce dati nello stack.
3.  Implementare un thread **"Consumatore"** che estrae i dati.
4.  Utilizzare i metodi `wait()` e `notify()` (o `notifyAll()`) della JVM per coordinarli:
    -   Il produttore deve attendere se lo stack è pieno.
    -   Il consumatore deve attendere se lo stack è vuoto.
5.  Verificare che la comunicazione avvenga senza spreco di risorse (evitando il busy waiting).

### Esempio di Output
```
[Produttore] Inserito: Oggetto 1
[Produttore] Inserito: Oggetto 2
[Consumatore] Estratto: Oggetto 2
[Consumatore] Estratto: Oggetto 1
[Produttore] Inserito: Oggetto 3
...
```

---

## 🇬🇧 English

### Objective
Use `wait()` and `notify()` methods to coordinate access to a shared data structure, solving the classic "Producer-Consumer" problem.

### Task (from Syllabus)
1.  **Create a shared Stack** (or a bounded queue) to manage data.
2.  Implement a **"Producer"** thread that pushes data into the stack.
3.  Implement a **"Consumer"** thread that pops data from the stack.
4.  Use JVM's `wait()` and `notify()` (or `notifyAll()`) methods to coordinate them:
    -   The producer must wait if the stack is full.
    -   The consumer must wait if the stack is empty.
5.  Verify that communication occurs without resource waste (avoiding busy waiting).

### Sample Output
```
[Producer] Pushed: Item 1
[Producer] Pushed: Item 2
[Consumer] Popped: Item 2
[Consumer] Popped: Item 1
[Producer] Pushed: Item 3
...
```

### Concepts covered
- Inter-thread communication
- `wait()` and `notify()` methods
- System Monitors
- Producer-Consumer problem
