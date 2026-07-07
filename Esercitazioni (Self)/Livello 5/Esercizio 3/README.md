# Esercizio 3: Coordinamento (join, sleep)

---

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

