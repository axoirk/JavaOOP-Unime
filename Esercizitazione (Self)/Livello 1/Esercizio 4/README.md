# Esercizio 4

---

## 🇮🇹 Italiano

### Descrizione
Programma che calcola la **media di una serie di voti** inseriti dall'utente, usando un ciclo `while` controllato da un valore sentinella.

L'utente inserisce un voto alla volta (numero ≥ 0).  
Quando inserisce un **numero negativo**, il ciclo termina e viene stampata la media dei voti inseriti.

#### Logica
1. Viene inizializzata la somma e un contatore a `0`.
2. Il ciclo `while` continua finché il valore inserito è ≥ 0.
3. Ogni numero valido viene sommato e il contatore viene incrementato.
4. Al termine vengono stampati: somma totale, contatore e media.

### Concetti trattati
- Ciclo `while` con valore sentinella
- Accumulatore e contatore
- Calcolo della media
- Cast da `int` a `float` per la divisione
- Output formattato con `System.out.printf`

### Esempio di esecuzione
```
Inserisci un valore:
8
Valore sommato: 8
Inserisci un valore:
6
Valore sommato: 6
Inserisci un valore:
-1
Risultati:
Totale Somma: 14
Stato Contatore: 2
Media: 7,00
```

---

## 🇬🇧 English

### Description
A program that calculates the **average of a series of grades** entered by the user, using a `while` loop controlled by a sentinel value.

The user enters one grade at a time (number ≥ 0).  
When a **negative number** is entered, the loop ends and the average of the collected grades is printed.

#### Logic
1. Sum and counter are initialised to `0`.
2. The `while` loop continues as long as the input is ≥ 0.
3. Each valid number is added to the sum and the counter is incremented.
4. At the end, total sum, counter, and average are printed.

### Concepts covered
- `while` loop with sentinel value
- Accumulator and counter
- Average calculation
- Cast from `int` to `float` for division
- Formatted output with `System.out.printf`

### Sample run
```
Inserisci un valore:
8
Valore sommato: 8
Inserisci un valore:
6
Valore sommato: 6
Inserisci un valore:
-1
Risultati:
Totale Somma: 14
Stato Contatore: 2
Media: 7,00
```
