# Esercizio 2

**Difficoltà:** Media 🟡
**Tempo Max:** 10 minuti
**Compilazioni Max:** 5

**Traccia:**
Creare un deposito del valore di 1000. Lanciare contemporaneamente due flussi indipendenti, entrambi programmati per estrarre il valore di 800 dal medesimo deposito. Garantire l'integrità strutturale della transazione applicando le regole di esclusione reciproca per evitare che il saldo scenda sotto zero.

**Dati in Input:**
Deposito: 1000. Thread A estrae 800. Thread B estrae 800.

**Output Atteso:**
`Flusso A preleva 800. Saldo residuo: 200`
`Flusso B tenta il prelievo ma fallisce.`
*(L'ordine di A e B può variare)*
