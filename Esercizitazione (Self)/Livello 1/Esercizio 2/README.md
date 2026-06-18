# Esercizio 2

---

## 🇮🇹 Italiano

### Descrizione
Programma che calcola l'**Indice di Massa Corporea (BMI)** dell'utente e ne fornisce una valutazione.

L'utente inserisce il proprio **peso in kg** e l'**altezza in cm**.  
Il programma calcola il BMI con la formula:

```
BMI = peso / (altezza_in_metri)²
```

In base al valore ottenuto viene stampato uno dei tre messaggi:
- **Sottopeso** → BMI < 20.1
- **Normopeso** → 20.1 ≤ BMI ≤ 25.0
- **Sovrappeso** → BMI > 25.0

### Concetti trattati
- Input con `Scanner` (tipi `float` e `int`)
- Calcolo con `Math.pow`
- Struttura condizionale `if / else if`
- Output formattato con `System.out.printf`

### Esempio di esecuzione
```
SISTEMA CALCOLO BMI.
Inserisci Peso (KG) e Altezza (cm):
70
175
Sei normopeso! BMI: 22,86
```

---

## 🇬🇧 English

### Description
A program that calculates the user's **Body Mass Index (BMI)** and provides a classification.

The user enters their **weight in kg** and **height in cm**.  
The program computes the BMI using the formula:

```
BMI = weight / (height_in_metres)²
```

Based on the result, one of three messages is printed:
- **Underweight** → BMI < 20.1
- **Normal weight** → 20.1 ≤ BMI ≤ 25.0
- **Overweight** → BMI > 25.0

### Concepts covered
- Input with `Scanner` (`float` and `int` types)
- Computation with `Math.pow`
- Conditional structure `if / else if`
- Formatted output with `System.out.printf`

### Sample run
```
SISTEMA CALCOLO BMI.
Inserisci Peso (KG) e Altezza (cm):
70
175
Sei normopeso! BMI: 22,86
```
