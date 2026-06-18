# Esercizio 2: Identificazione e Ciclo di Vita / Exercise 2: Identification and Lifecycle

---

## 🇮🇹 Italiano

### Obiettivo
Gestire l'identità dei thread e la loro terminazione sicura tramite variabili sentinella.

### Requisiti del task
1. **Identificazione:**
   - Creare una classe che implementa `Runnable`.
   - Assegnare un nome specifico ai thread creati (es. "Lavoratore-1", "Lavoratore-2").
2. **Esecuzione:**
   - Nel blocco di esecuzione `run()`, stampare il nome del thread corrente usando `Thread.currentThread().getName()`.
3. **Terminazione Pulita:**
   - Implementare una logica basata su una **variabile sentinella** (es. un booleano `running`) per terminare il ciclo nel metodo `run()` in modo controllato.

### Concetti trattati
- `getName()` e identificazione dei Thread
- Ciclo di vita del Thread
- Terminazione sicura (Sentinel variable)
- `Thread.currentThread()`

### Esempio di Output
```text
[Lavoratore-1] Avvio esecuzione...
[Lavoratore-2] Avvio esecuzione...
[Lavoratore-1] Elaborazione dati in corso...
[Lavoratore-2] Elaborazione dati in corso...
[Lavoratore-1] Segnale di arresto ricevuto: terminazione pulita.
[Lavoratore-2] Segnale di arresto ricevuto: terminazione pulita.
```

---

## 🇬🇧 English

### Objective
Manage thread identity and their safe termination using sentinel variables.

### Task Requirements
1. **Identification:**
   - Create a class that implements `Runnable`.
   - Assign a specific name to the created threads (e.g., via the Thread constructor or the `setName()` method).
2. **Execution:**
   - In the `run()` execution block, print the name of the current thread using `Thread.currentThread().getName()`.
3. **Clean Termination:**
   - Implement logic based on a **sentinel variable** (e.g., a boolean `running`) to terminate the loop in the `run()` method in a controlled manner, instead of abruptly stopping it with deprecated methods.

### Concepts Covered
- `getName()` and Thread identification
- Thread lifecycle
- Safe termination (Sentinel variable)
- `Thread.currentThread()`

### Sample Output
```text
[Downloader-1] Starting execution...
[Downloader-2] Starting execution...
[Downloader-1] Work in progress...
[Downloader-2] Work in progress...
[Downloader-1] Clean termination received.
[Downloader-2] Clean termination received.
```
