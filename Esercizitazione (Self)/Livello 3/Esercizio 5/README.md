# Esercizio 5 – Gestione delle Eccezioni / Exception Handling

---

## 🇮🇹 Italiano

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

---

## 🇬🇧 English

### Description
This exercise introduces robust error handling in Java through the use of **exceptions**.

The program:
- Defines a custom exception named `DivideByZeroException`.
- Uses `try-catch` blocks to intercept potential errors during execution (such as invalid input or division by zero).
- Uses the `throw` keyword to explicitly raise an exception when an application error condition is detected.
- Handles user input via the `Scanner` class.

### Learning Objective
- Understand the exception propagation mechanism.
- Create and use custom exceptions.
- Write safe and resilient code against runtime errors.

### Output Example
```text
Inserisci un numeratore:
10
Inserisci un denominatore:
0
Attenzione: divisione per zero non consentita!
```
