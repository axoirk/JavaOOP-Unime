# Esercizio 2 – Selection Sort su Array / Selection Sort on Arrays

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio implementa un algoritmo classico di ordinamento: **Selection Sort**.

Il programma:
- genera un array di interi con valori casuali;
- stampa l'array prima dell'ordinamento;
- ordina i valori in modo crescente con due cicli annidati;
- ristampa l'array dopo l'ordinamento.

### Obiettivo didattico
L'obiettivo e comprendere il funzionamento passo-passo di Selection Sort:
- per ogni posizione `k`, si cerca l'indice del valore minimo nella parte destra dell'array;
- al termine della ricerca si esegue lo scambio tra `array[k]` e `array[minIndex]`;
- la porzione sinistra risulta progressivamente ordinata.

### Struttura e comportamento del codice
Flusso principale:
1. Creazione di un array di dimensione fissa (`space = 10`)
2. Riempimento con numeri casuali (`Math.random()`)
3. Stampa iniziale con `printArray(int[] arr)`
4. Ordinamento con Selection Sort
5. Stampa finale dell'array ordinato

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Contiene generazione array, funzione di stampa e implementazione completa di Selection Sort |

### Concetti trattati
- Array monodimensionali
- Metodi statici di supporto (`printArray`)
- Cicli `for` annidati
- Ricerca del minimo
- Scambio valori con variabile temporanea (`temp`)
- Complessita quadratica `O(n^2)` di Selection Sort

### Esempio di esecuzione
```
27 3 14 9 21 1 30 8 17 5
1 3 5 8 9 14 17 21 27 30
```

---

## 🇬🇧 English

### Description
This exercise implements a classic sorting algorithm: **Selection Sort**.

The program:
- generates an integer array with random values;
- prints the array before sorting;
- sorts values in ascending order using nested loops;
- prints the array again after sorting.

### Learning objective
The goal is to understand Selection Sort step by step:
- for each position `k`, find the index of the minimum value in the remaining right-side portion;
- after the scan, swap `array[k]` with `array[minIndex]`;
- the left side becomes progressively sorted.

### Code flow and behavior
Main flow:
1. Create a fixed-size array (`space = 10`)
2. Fill it with random integers (`Math.random()`)
3. Print initial content via `printArray(int[] arr)`
4. Run Selection Sort
5. Print the sorted array

### Files
| File | Description |
|------|-------------|
| `Main.java` | Contains array generation, print helper method, and complete Selection Sort implementation |

### Concepts covered
- One-dimensional arrays
- Static helper methods (`printArray`)
- Nested `for` loops
- Minimum search in subarray
- Value swap using a temporary variable (`temp`)
- Quadratic time complexity `O(n^2)` of Selection Sort

### Sample run
```
27 3 14 9 21 1 30 8 17 5
1 3 5 8 9 14 17 21 27 30
```
