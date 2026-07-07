# Esercizio 1

**Difficoltà:** Facile 🟢
**Tempo Max:** 10 minuti
**Compilazioni Max:** 5

**Traccia:**
Definire un'entità in grado di eseguire calcoli separati. L'entità deve eseguire un conteggio temporizzato (100 millisecondi di pausa) da 1 a 5, dichiarando il proprio identificativo ad ogni passo. Avviare tre entità parallele. L'infrastruttura chiamante deve attendere che tutte le entità abbiano concluso prima di dichiarare la chiusura.

**Dati in Input:**
3 istanze lanciate simultaneamente.

**Output Atteso:**
15 righe stampate con interleaving (es. `Thread-0: 1`, `Thread-1: 1`...), chiuse obbligatoriamente dall'unica riga finale:
`Gara terminata.`
