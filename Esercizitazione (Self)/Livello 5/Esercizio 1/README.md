# Esercizio 1: Creazione Thread / Exercise 1: Thread Creation

---

## 🇮🇹 Italiano

### Obiettivo
Implementare l'interfaccia `Runnable` per avviare attività in parallelo e comprendere la differenza tra i metodi `start()` e `run()`.

### Requisiti del task
1. **Definizione dei Task:**
   - Creare due classi diverse, ad esempio `Coffee` e `Tea`, entrambe che implementano l'interfaccia `java.lang.Runnable`.
2. **Implementazione di `run()`:**
   - Nel metodo `run()` di ciascuna classe, stampare un messaggio ripetuto (es. "Sto preparando il caffè..." e "Sto preparando il tè...") all'interno di un ciclo.
3. **Classe Main:**
   - Istanziare gli oggetti `Coffee` e `Tea`.
   - Passarli ai costruttori di due oggetti `Thread` distinti.
   - Avviarli entrambi in parallelo usando il metodo `start()`.
   - Osservare l'alternanza dell'output in console, che dimostra l'esecuzione concorrente.

### Concetti trattati
- Interfaccia `Runnable`
- Composizione del Thread (passare un Runnable al costruttore)
- Metodo `start()` vs `run()`
- Esecuzione concorrente (Interleaving)

### Esempio di Output
```text
Sto preparando il caffè...
Sto preparando il tè...
Sto preparando il caffè...
Sto preparando il caffè...
Sto preparando il tè...
```

---

## 🇬🇧 English

### Objective
Implement the `Runnable` interface to start parallel activities and understand the difference between the `start()` and `run()` methods.

### Task Requirements
1. **Task Definition:**
   - Create two different classes, for example, `Coffee` and `Tea`, both implementing the `java.lang.Runnable` interface.
2. **Implementing `run()`:**
   - In the `run()` method of each class, print a repeated message (e.g., "I am preparing coffee..." and "I am preparing tea...") within a loop.
3. **Main Class:**
   - Instantiate the `Coffee` and `Tea` objects.
   - Pass them to the constructors of two distinct `Thread` objects.
   - Start both in parallel using the `start()` method.
   - Observe the interleaving of the output in the console, which demonstrates concurrent execution.

### Concepts Covered
- `Runnable` interface
- Thread composition (passing a Runnable to the constructor)
- `start()` vs `run()` method
- Concurrent execution (Interleaving)

### Sample Output
```text
I am preparing coffee...
I am preparing tea...
I am preparing coffee...
I am preparing coffee...
I am preparing tea...
```
