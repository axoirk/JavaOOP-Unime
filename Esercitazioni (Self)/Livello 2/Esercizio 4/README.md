# Esercizio 4: Variabili di Classe e Costanti

---

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

