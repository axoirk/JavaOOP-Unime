# Esercizio 4 – Lista della Spesa con ArrayList / Shopping List with ArrayList

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio usa una struttura dati dinamica (`ArrayList`) per gestire una lista della spesa inserita da tastiera.

Il programma:
- richiede all'utente di inserire oggetti uno alla volta;
- aggiunge ogni elemento in `ArrayList<String>`;
- termina l'inserimento quando viene digitato `STOP`;
- stampa infine tutti gli elementi presenti nella lista.

### Obiettivo didattico
L'obiettivo e consolidare:
- uso di `ArrayList` rispetto agli array a dimensione fissa;
- acquisizione input testuale con `Scanner`;
- gestione di una condizione di stop tramite valore sentinella (`STOP`);
- iterazione finale con ciclo `for-each`.

### Struttura e comportamento del codice
Flusso principale:
1. Inizializzazione di `ArrayList<String>` e `Scanner`
2. Richiesta del primo input utente
3. Ciclo `while` finche il valore non e `STOP`
4. Aggiunta dell'oggetto alla lista e messaggio di conferma
5. Stampa completa della lista della spesa

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Gestisce inserimento dinamico degli oggetti, condizione di stop e stampa finale della lista |

### Concetti trattati
- `ArrayList<String>`
- Input da tastiera con `Scanner`
- Ciclo `while` con sentinella
- Confronto stringhe con `.equals(...)`
- Ciclo `for-each` per stampa elementi

### Esempio di esecuzione
```
Inserisci un oggetto nella lista della spesa:
Latte
Oggetto aggiunto alla lista della spesa.
Per terminare l'inserimento digitare "STOP"
Pane
Oggetto aggiunto alla lista della spesa.
Per terminare l'inserimento digitare "STOP"
STOP
Lista della spesa:
Latte
Pane
```

---

## 🇬🇧 English

### Description
This exercise uses a dynamic data structure (`ArrayList`) to manage a shopping list entered from keyboard input.

The program:
- asks the user to enter items one by one;
- stores each item into an `ArrayList<String>`;
- ends input when `STOP` is typed;
- then prints all items currently in the list.

### Learning objective
The goal is to strengthen:
- use of `ArrayList` compared to fixed-size arrays;
- text input handling with `Scanner`;
- stop-condition handling with a sentinel value (`STOP`);
- final iteration using a `for-each` loop.

### Code flow and behavior
Main flow:
1. Initialize `ArrayList<String>` and `Scanner`
2. Prompt for user input
3. Loop with `while` until value is `STOP`
4. Add each item and print confirmation
5. Print the full shopping list

### Files
| File | Description |
|------|-------------|
| `Main.java` | Handles dynamic item input, stop condition, and final list printing |

### Concepts covered
- `ArrayList<String>`
- Keyboard input with `Scanner`
- `while` loop with sentinel value
- String comparison with `.equals(...)`
- `for-each` iteration for output

### Sample run
```
Inserisci un oggetto nella lista della spesa:
Latte
Oggetto aggiunto alla lista della spesa.
Per terminare l'inserimento digitare "STOP"
Pane
Oggetto aggiunto alla lista della spesa.
Per terminare l'inserimento digitare "STOP"
STOP
Lista della spesa:
Latte
Pane
```
