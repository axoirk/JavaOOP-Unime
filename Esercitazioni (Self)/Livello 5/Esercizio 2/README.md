# Esercizio 2: Identificazione e Ciclo di Vita

---

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

