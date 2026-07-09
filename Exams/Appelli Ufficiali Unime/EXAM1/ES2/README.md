# Esercizio 2 (13 Punti) - Gestione Avanzata Eccezioni (Le 5 Keywords)

**Regole Appello:** 30 minuti totali per 3 esercizi. Max 5 esecuzioni per esercizio. Tutte le classi nello stesso file (Main.java).

Creare una classe `GestoreEccezioni` contenente un metodo `public static void esegui(int n)`. All'interno di questo metodo (o aiutandoti con altri se necessario), implementare la logica per gestire i seguenti casi basati sul parametro `n`:
* Se `0`: lanciare una `Exception` generica e assicurarsi che a schermo venga stampato "eccezione generica".
* Se `1`: lanciare una `IOException`, catturarla internamente, rilanciare una `RuntimeException` verso l'esterno e assicurarsi che venga stampato "eccezione runtime".
* Se `2`: assicurarsi che venga stampato "no eccezioni".

**Vincolo Architetturale:** Si devono obbligatoriamente utilizzare **tutte e 5 le parole chiave** della gestione delle eccezioni (`try`, `catch`, `finally`, `throw`, `throws`).