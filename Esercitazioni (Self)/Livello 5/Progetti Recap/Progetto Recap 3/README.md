# Esercizio 3

**Difficoltà:** Difficile 🔴
**Tempo Max:** 10 minuti
**Compilazioni Max:** 5

**Traccia:**
Strutturare un contenitore a capacità limitata (1 singolo elemento massimo). Impegnare un flusso in ingresso continuo (Produttore) e uno in uscita continua (Consumatore). Instaurare un meccanismo di risveglio condizionale tra i due flussi per evitare sovrascritture o estrazioni a vuoto.

**Dati in Input:**
Produzione dei numeri interi `1`, `2`, `3`.

**Output Atteso:**
`Prodotto: 1`
`Consumato: 1`
`Prodotto: 2`
`Consumato: 2`
`Prodotto: 3`
`Consumato: 3`
