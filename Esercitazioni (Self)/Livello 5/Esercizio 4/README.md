# Esercizio 4: La Sincronizzazione

---

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

