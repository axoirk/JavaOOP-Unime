# Esercizio 2 (13 Punti) - Gestione Avanzata Eccezioni (Le 5 Keywords)

**Regole Appello:** 30 minuti totali per 3 esercizi. Max 5 esecuzioni per esercizio. Tutte le classi nello stesso file (Main.java).

Definire un metodo che accetta un parametro `int` e gestire i seguenti casi:
* Se `0`: lanciare una `Exception` generica e stampare "eccezione generica".
* Se `1`: lanciare una `IOException`, catturarla, rilanciare una `RuntimeException` e stampare "eccezione runtime".
* Se `2`: stampare "no eccezioni".

**Vincolo Architetturale:** Si devono obbligatoriamente utilizzare **tutte e 5 le parole chiave** della gestione delle eccezioni (`try`, `catch`, `finally`, `throw`, `throws`).