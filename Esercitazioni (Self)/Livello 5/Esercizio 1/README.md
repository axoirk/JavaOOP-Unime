# Esercizio 1: Creazione Thread

---

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

