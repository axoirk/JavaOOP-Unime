# Esercizio 3

---

## 🇮🇹 Italiano

### Descrizione
Programma che introduce **incapsulamento** e **controllo dei dati in ingresso** tramite metodi setter.

La classe `Purchase` contiene attributi `private`:
- nome (`name`)
- prezzo (`price`)
- quantita (`amount`)

L'accesso avviene tramite getter e setter pubblici. In particolare, `setPrice(Double price)` valida il valore:
- se negativo, stampa un avviso e rifiuta l'assegnazione
- se zero o positivo, aggiorna il prezzo

Nel `Main` vengono eseguiti piu casi di test (valori validi, prezzo negativo, prezzo zero) e viene stampato lo stato dell'oggetto dopo ogni scenario.

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Crea diversi oggetti `Purchase`, prova i casi di validazione e stampa i risultati |
| `Purchase.java` | Definisce attributi incapsulati, getter/setter e validazione del prezzo nel setter |

### Concetti trattati
- Information Hiding (attributi `private`)
- Getter e setter per accesso controllato
- Validazione dell'input nel mutatore (`setPrice`)
- Gestione di casi validi e non validi
- Output formattato con `System.out.printf`

### Esempio di esecuzione
```
Caso 1 - Valido
Nome: iPad Pro
Prezzo: 1299.99
Quantita: 5

Tentativo di assegnare prezzo negativo a Magic Mouse...
Il prezzo inserito risulta negativo (minore di 0)
...
```

---

## 🇬🇧 English

### Description
A program that introduces **encapsulation** and **input validation** through setter methods.

The `Purchase` class defines `private` fields:
- name (`name`)
- price (`price`)
- quantity (`amount`)

Data access is provided through public getters and setters. In particular, `setPrice(Double price)` validates the value:
- if it is negative, it prints a warning and rejects the assignment
- if it is zero or positive, it updates the price

In `Main`, multiple scenarios are executed (valid values, negative price, zero price), and the object state is printed after each case.

### Files
| File | Description |
|------|-------------|
| `Main.java` | Creates multiple `Purchase` objects, runs validation scenarios, and prints results |
| `Purchase.java` | Defines encapsulated fields, getters/setters, and price validation in the setter |

### Concepts covered
- Information hiding with `private` fields
- Getters and setters for controlled access
- Input validation in a mutator (`setPrice`)
- Handling valid and invalid scenarios
- Formatted output with `System.out.printf`

### Sample run
```
Caso 1 - Valido
Nome: iPad Pro
Prezzo: 1299.99
Quantita: 5

Tentativo di assegnare prezzo negativo a Magic Mouse...
Il prezzo inserito risulta negativo (minore di 0)
...
```
