# Esercizio 3: Coordinamento (join, sleep) / Exercise 3: Coordination (join, sleep)

---

## 🇮🇹 Italiano

### Obiettivo
Gestire la sincronizzazione temporale tra thread principali e secondari utilizzando i meccanismi di attesa e sospensione.

### Requisiti del task
1. **Compiti Ritardati:**
   - Creare dei thread che eseguono compiti con ritardi simulati usando `Thread.sleep()`.
2. **Sincronizzazione (Wait for all):**
   - Nella classe `Main`, fare in modo che il thread principale (main) attenda la fine dell'esecuzione di tutti i thread figli invocando su di essi il metodo `join()`.
3. **Chiusura:**
   - Stampare un messaggio finale solo dopo che tutti i thread hanno terminato il loro lavoro, garantendo l'ordine logico delle operazioni.

### Concetti trattati
- `join()`: attesa della terminazione di un thread
- `sleep()`: sospensione temporanea (messa in stato Blocked)
- Gestione di `InterruptedException`

### Esempio di Output
```text
Thread-1: Inizio operazione lunga...
Thread-2: Inizio operazione breve...
Thread-2: Operazione completata.
Thread-1: Operazione completata.
[Main]: Tutti i thread hanno finito. Programma terminato.
```

---

## 🇬🇧 English

### Objective
Manage the temporal synchronization between main and secondary threads using waiting and suspension mechanisms.

### Task Requirements
1. **Delayed Tasks:**
   - Create threads that perform tasks with simulated delays using `Thread.sleep()`.
2. **Synchronization (Wait for all):**
   - In the `Main` class, ensure that the main thread waits for all child threads to finish execution by invoking the `join()` method on them.
3. **Closure:**
   - Print a final message only after all threads have finished their work, ensuring the logical order of operations.

### Concepts Covered
- `join()`: waiting for a thread to terminate
- `sleep()`: temporary suspension (put into Blocked state)
- `InterruptedException` handling

### Sample Output
```text
Thread-1: Starting long operation...
Thread-2: Starting short operation...
Thread-2: Operation completed.
Thread-1: Operation completed.
[Main]: All threads have finished. Program terminated.
```
