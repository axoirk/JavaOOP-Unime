# Esercizio 3 (13 Punti) - Ereditarietà, Thread e Information Hiding

**Regole Appello:** 30 minuti totali per 3 esercizi. Max 5 esecuzioni per esercizio. Tutte le classi nello stesso file (Main.java).

Data una classe `Persona` con costruttore `(String nome, String cognome)` (già fornita nel file):
1. Definire una sottoclasse `Studente` che implementa l'interfaccia `Runnable`.
2. Definire in `Studente` due costruttori in overload:
   * Il primo accetta: `nome`, `cognome`, `matricola` (int).
   * Il secondo accetta: `matricola` (int), `cds` (String). 
3. Fare l'override del metodo `run()`: dovrà elevare la `matricola` al quadrato e sovrascriverne il valore.
4. **Vincolo Architetturale:** Usare rigorosamente l'Information Hiding (tutte le variabili d'istanza devono essere `private` e bisogna definire i relativi metodi `get` e `set`).