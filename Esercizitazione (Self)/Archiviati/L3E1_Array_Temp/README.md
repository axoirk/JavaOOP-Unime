# Esercizio 1 – Media Settimanale delle Temperature / Weekly Temperature Average

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio lavora su input da tastiera e gestione di array numerici.

Il programma:
- acquisisce da utente 7 temperature giornaliere;
- memorizza i valori in un array `double[]`;
- calcola la somma totale;
- stampa la media settimanale con due cifre decimali.

### Obiettivo didattico
L'obiettivo e consolidare:
- uso di `Scanner` per input interattivo;
- popolamento progressivo di un array;
- elaborazione numerica (somma e media);
- formattazione dell'output con `System.out.printf`.

### Struttura e comportamento del codice
Flusso principale:
1. Inizializzazione array `temperature` di lunghezza 7
2. Ciclo di input: richiesta temperatura per ogni giorno
3. Ciclo di aggregazione: calcolo della somma (`summ`)
4. Calcolo media: `summ / temperature.length`
5. Stampa formattata del risultato finale

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Gestisce input delle 7 temperature, calcolo della media e output formattato |

### Concetti trattati
- Array di `double`
- Input utente con `Scanner`
- Cicli `for` per lettura ed elaborazione
- Accumulatore numerico (`summ`)
- Calcolo media aritmetica
- Output numerico formattato (`%.2f`)

### Esempio di esecuzione
```
Inserisci temperatura del giorno 1: 18.5
Inserisci temperatura del giorno 2: 20.0
...
La media della temperatura settimanale è: 19.27
```

---

## 🇬🇧 English

### Description
This exercise focuses on keyboard input and numeric array processing.

The program:
- reads 7 daily temperatures from user input;
- stores values in a `double[]` array;
- computes the total sum;
- prints the weekly average with two decimal places.

### Learning objective
The goal is to strengthen:
- interactive input handling with `Scanner`;
- progressive array population;
- numeric processing (sum and average);
- formatted output with `System.out.printf`.

### Code flow and behavior
Main flow:
1. Initialize `temperature` array with length 7
2. Input loop: request one value for each day
3. Aggregation loop: compute total sum (`summ`)
4. Average calculation: `summ / temperature.length`
5. Formatted print of final result

### Files
| File | Description |
|------|-------------|
| `Main.java` | Handles temperature input, weekly average computation, and formatted output |

### Concepts covered
- `double` arrays
- User input with `Scanner`
- `for` loops for reading and processing
- Numeric accumulator (`summ`)
- Arithmetic mean computation
- Formatted numeric output (`%.2f`)

### Sample run
```
Inserisci temperatura del giorno 1: 18.5
Inserisci temperatura del giorno 2: 20.0
...
La media della temperatura settimanale è: 19.27
```
