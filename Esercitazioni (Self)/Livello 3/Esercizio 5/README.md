# Esercizio 5 – Gestione delle Eccezioni

---

### Descrizione
Questo esercizio introduce la gestione robusta degli errori in Java attraverso l'uso delle **eccezioni**.

Il programma:
- Definisce un'eccezione personalizzata `DivideByZeroException`.
- Utilizza i blocchi `try-catch` per intercettare potenziali errori durante l'esecuzione (come l'input non valido o la divisione per zero).
- Utilizza la keyword `throw` per lanciare esplicitamente un'eccezione quando viene rilevata una condizione di errore applicativo.
- Gestisce l'input dell'utente tramite la classe `Scanner`.

### Obiettivo didattico
- Comprendere il meccanismo di propagazione delle eccezioni.
- Creare e utilizzare eccezioni personalizzate.
- Scrivere codice sicuro e resiliente agli errori di runtime.

### Esempio di Output
```text
Inserisci un numeratore:
10
Inserisci un denominatore:
0
Attenzione: divisione per zero non consentita!
```

