# Esercizio 3 – Divisione con Eccezione Personalizzata / Division with Custom Exception

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio introduce la gestione delle eccezioni in Java con una eccezione personalizzata.

Il programma:
- acquisisce da tastiera numeratore e denominatore;
- controlla il caso di divisione per zero;
- lancia una `DivideByZeroException` dedicata quando il denominatore e `0`;
- stampa il risultato della divisione in formato decimale quando l'input e valido.

### Obiettivo didattico
L'obiettivo e comprendere:
- differenza tra flusso normale e flusso eccezionale;
- uso di `throw` per segnalare errori applicativi;
- creazione di una classe eccezione custom che estende `Exception`;
- gestione dell'errore con blocco `try/catch` e messaggi utente.

### Struttura e comportamento del codice
Flusso principale:
1. Lettura di numeratore e denominatore con `Scanner`
2. Verifica del denominatore (`denom == 0`)
3. Lancio di `new DivideByZeroException()` in caso non valido
4. Calcolo della divisione con cast a `double`
5. Stampa del risultato (`%.2f`) oppure del messaggio di errore nel `catch`

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Gestisce input utente, controllo del denominatore, lancio eccezione e stampa risultato |
| `DivideByZeroException.java` | Definisce l'eccezione personalizzata con messaggio "Non puoi dividere per zero!" |

### Concetti trattati
- Input da tastiera con `Scanner`
- Casting numerico a `double`
- Eccezioni personalizzate (`extends Exception`)
- `throw` e `try/catch`
- Validazione di input critico (denominatore diverso da zero)

### Esempio di esecuzione
```
Inserisci un numeratore:
10
Inserisci un denominatore:
2
Risultato divisione: 5.00
```

```
Inserisci un numeratore:
10
Inserisci un denominatore:
0
Non puoi dividere per zero!
```

---

## 🇬🇧 English

### Description
This exercise introduces Java exception handling with a custom exception class.

The program:
- reads numerator and denominator from keyboard input;
- checks the division-by-zero case;
- throws a dedicated `DivideByZeroException` when denominator is `0`;
- prints the division result in decimal format when input is valid.

### Learning objective
The goal is to understand:
- the difference between normal flow and exceptional flow;
- use of `throw` to signal application errors;
- how to create a custom exception class extending `Exception`;
- error handling with `try/catch` and user-facing messages.

### Code flow and behavior
Main flow:
1. Read numerator and denominator using `Scanner`
2. Check denominator (`denom == 0`)
3. Throw `new DivideByZeroException()` when invalid
4. Compute division with `double` cast
5. Print result (`%.2f`) or error message in the `catch` block

### Files
| File | Description |
|------|-------------|
| `Main.java` | Handles user input, denominator check, exception throw, and result printing |
| `DivideByZeroException.java` | Defines the custom exception with message "Non puoi dividere per zero!" |

### Concepts covered
- Keyboard input with `Scanner`
- Numeric casting to `double`
- Custom exceptions (`extends Exception`)
- `throw` and `try/catch`
- Critical input validation (non-zero denominator)

### Sample run
```
Inserisci un numeratore:
10
Inserisci un denominatore:
2
Risultato divisione: 5.00
```

```
Inserisci un numeratore:
10
Inserisci un denominatore:
0
Non puoi dividere per zero!
```
