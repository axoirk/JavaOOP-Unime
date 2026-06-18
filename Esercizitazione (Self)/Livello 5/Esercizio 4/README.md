# Esercizio 4: La Sincronizzazione / Exercise 4: Synchronization

---

## 🇮🇹 Italiano

### Obiettivo
Comprendere il fenomeno delle Race Condition e imparare a risolverle utilizzando i meccanismi di mutua esclusione forniti dalla JVM.

### Requisiti del task
1. **Creazione del Conflitto (Race Condition):**
   - Creare una situazione in cui due o più thread provano ad incrementare contemporaneamente un **contatore condiviso** (variabile nell'Heap).
   - Osservare come, senza protezione, il valore finale del contatore sia errato o imprevedibile (non deterministico).
2. **Risoluzione (Sincronizzazione):**
   - Risolvere il problema utilizzando la parola chiave `synchronized` sul metodo di incremento o tramite un blocco sincronizzato.
3. **Verifica:**
   - Garantire che il risultato finale corrisponda esattamente alla somma degli incrementi previsti da tutti i thread.

### Concetti trattati
- Race Condition e inconsistenza dei dati
- Memoria condivisa (Heap)
- Parola chiave `synchronized`
- Atomicità delle operazioni e Lock (Monitor)

### Esempio di Output
```text
[Senza sincronizzazione] Valore atteso: 20000, Valore ottenuto: 18432 (ERRORE)
[Con sincronizzazione] Valore atteso: 20000, Valore ottenuto: 20000 (OK)
```

---

## 🇬🇧 English

### Objective
Understand the phenomenon of Race Conditions and learn how to resolve them using the mutual exclusion mechanisms provided by the JVM.

### Task Requirements
1. **Creating Conflict (Race Condition):**
   - Create a situation where two or more threads try to simultaneously increment a **shared counter** (a variable in the Heap).
   - Observe how, without protection, the final value of the counter is incorrect or unpredictable (non-deterministic).
2. **Resolution (Synchronization):**
   - Resolve the issue using the `synchronized` keyword on the increment method or through a synchronized block.
3. **Verification:**
   - Ensure that the final result exactly matches the sum of increments expected from all threads.

### Concepts Covered
- Race Condition and data inconsistency
- Shared memory (Heap)
- `synchronized` keyword
- Atomicity of operations and Lock (Monitor)

### Sample Output
```text
[Without synchronization] Expected value: 20000, Obtained value: 18432 (ERROR)
[With synchronization] Expected value: 20000, Obtained value: 20000 (OK)
```
