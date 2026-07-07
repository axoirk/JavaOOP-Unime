# Esercizio 2 (13 Punti) - Core Java (I/O e Checked Exceptions)

**Regole Appello:** 30 minuti totali per l'intero esame. Max 5 esecuzioni per esercizio. Tutte le classi nello stesso file (Soluzione.java).

Definire una classe `LettoreFile`. Implementare un metodo statico `public static void leggiEScrivi(String pathOrigine, String pathDestinazione)`. Il metodo deve leggere ESCLUSIVAMENTE la prima riga di testo presente nel file indicato da `pathOrigine` e scriverla nel file indicato da `pathDestinazione`. 

Inoltre, il metodo DEVE dichiarare esplicitamente nella propria firma il possibile lancio di `IOException`, demandando rigorosamente la cattura dell'eccezione al codice chiamante.