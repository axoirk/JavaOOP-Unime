# Esercizio 4: Variabili di Classe e Costanti / Exercise 4: Class Variables and Constants

---

## 🇮🇹 Italiano

### Obiettivo
Comprendere la profonda differenza tra la memoria d'istanza (che appartiene al singolo oggetto) e la memoria di classe (che appartiene alla classe nella sua interezza ed è condivisa), imparando a implementare contatori globali e costanti universali.

### Requisiti del task
1. **Creare la Classe `GestioneBancaria`:**
    - Definisci una costante pubblica e inalterabile (`static final`) chiamata `TASSO_INTERESSE_MAX` e impostala a `5.0` (rappresenta il 5%).
    - Definisci una variabile privata e statica chiamata `totaleContiAperti` (inizializzata a `0`), che terrà traccia di quanti conti bancari vengono aperti in tutta la filiale.
    - Implementa un metodo statico `getTotaleConti()` per restituire il valore del contatore.

2. **Creare la Classe `ContoBancario`:**
    - Aggiungi variabili d'istanza per `titolare` (Stringa), `saldo` (double) e `tassoInteresse` (double).
    - Nel costruttore, oltre ad assegnare il titolare e un saldo iniziale, **incrementa il contatore statico** della classe `GestioneBancaria`.
    - Aggiungi un metodo `impostaTassoInteresse(double nuovoTasso)`. Questo metodo deve verificare che il `nuovoTasso` non superi la costante globale `GestioneBancaria.TASSO_INTERESSE_MAX`. Se lo supera, blocca l'assegnazione, imposta il tasso al valore massimo consentito e stampa un "Warning" in console per l'operatore.

3. **Classe `Main`:**
    - Istanzia 3 conti bancari per clienti diversi.
    - Prova a impostare a uno dei conti un tasso di interesse anomalo (es. 8.5) per testare il blocco di sicurezza (la costante).
    - Stampa a schermo il numero totale di conti aperti invocando il metodo statico della classe `GestioneBancaria`, dimostrando che lo stato globale è stato aggiornato correttamente dalle singole istanze.

### Esempio di Output
```
Numero attuale conti creati: 0
Numero attuale conti creati: 1
Impossibile modificare tasso interesse: Valore superiore da quello definito.
Numero attuale conti creati: 3
Titolare Conto: Mario Rossi
Saldo sul Conto: €599,99
Tasso interesse: 3,90
...
```

---

## 🇬🇧 English

### Objective
Understand the profound difference between instance memory (which belongs to a single object) and class memory (which belongs to the class as a whole and is shared), learning how to implement global counters and universal constants.

### Task Requirements
1. **Create the `GestioneBancaria` Class:**
    - Define a public and immutable constant (`static final`) named `TASSO_INTERESSE_MAX` and set it to `5.0` (representing 5%).
    - Define a private static variable named `totaleContiAperti` (initialized to `0`), which will track how many bank accounts are opened across the entire branch.
    - Implement a static method `getTotaleConti()` to return the counter's value.

2. **Create the `ContoBancario` Class:**
    - Add instance variables for `titolare` (String), `saldo` (double), and `tassoInteresse` (double).
    - In the constructor, in addition to assigning the holder and an initial balance, **increment the static counter** of the `GestioneBancaria` class.
    - Add a method `impostaTassoInteresse(double nuovoTasso)`. This method must verify that `nuovoTasso` does not exceed the global constant `GestioneBancaria.TASSO_INTERESSE_MAX`. If it does, block the assignment, set the rate to the maximum allowed value, and print a "Warning" to the console.

3. **`Main` Class:**
    - Instantiate 3 bank accounts for different customers.
    - Try to set an anomalous interest rate (e.g., 8.5) for one of the accounts to test the security lock (the constant).
    - Print the total number of open accounts by invoking the static method of the `GestioneBancaria` class, demonstrating that the global state was correctly updated by individual instances.

### Sample Output
```
Current bank accounts created: 0
Current bank accounts created: 1
Impossible to modify interest rate: Value higher than the maximum allowed.
Current bank accounts created: 3
Account Holder: Mario Rossi
Balance: €599.99
Interest Rate: 3.90
...
```

### Concepts Covered
- `static` modifier
- `final` modifier for defining Constants
- Sharing global state between instances
- Class methods vs Instance methods