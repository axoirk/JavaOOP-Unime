# Esercizio 1

---

## 🇮🇹 Italiano

### Descrizione
Programma che introduce la **programmazione a oggetti** in Java tramite la creazione di una classe personalizzata.

Viene definita una classe `Automobile` con attributi come:
- velocità (`speed`)
- carburante (`fuel`)
- targa (`license`)

Nel `Main` vengono istanziati due oggetti, inizializzati con valori diversi e poi modificati richiamando i metodi:
- `accelerate(double pedalPressure)`
- `decelerate(double brakePressure)`

Dopo ogni modifica, il programma stampa lo stato aggiornato di ciascuna automobile.

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Crea due oggetti `Automobile`, imposta i valori iniziali e simula accelerazione/decelerazione |
| `Automobile.java` | Definisce attributi, costanti, metodi di comportamento e getter/setter |

### Concetti trattati
- Definizione di una classe personalizzata
- Variabili d'istanza e costanti
- Incapsulamento tramite getter e setter
- Creazione oggetti con `new`
- Invocazione di metodi su oggetti
- Output formattato con `System.out.printf`

### Esempio di esecuzione
```
Stato attuale AUTO-AD594GD
Velocità: 5,00, Benzina: 10,00
Stato attuale AUTO-LF494GF
Velocità: 5,00, Benzina: 4,60
Modifiche Valori (Accelerazione)
Stato attuale AUTO-AD594GD
Velocità: 17,00, Benzina: 9,76
...
```

---

## 🇬🇧 English

### Description
A program that introduces **object-oriented programming** in Java by creating a custom class.

An `Automobile` class is defined with attributes such as:
- speed (`speed`)
- fuel (`fuel`)
- license plate (`license`)

Inside `Main`, two objects are instantiated, initialized with different values, and then updated by calling:
- `accelerate(double pedalPressure)`
- `decelerate(double brakePressure)`

After each change, the program prints the updated state of each car.

### Files
| File | Description |
|------|-------------|
| `Main.java` | Creates two `Automobile` objects, sets initial values, and simulates acceleration/deceleration |
| `Automobile.java` | Defines attributes, constants, behavior methods, and getters/setters |

### Concepts covered
- Custom class definition
- Instance variables and constants
- Encapsulation through getters and setters
- Object creation with `new`
- Calling methods on objects
- Formatted output with `System.out.printf`

### Sample run
```
Stato attuale AUTO-AD594GD
Velocità: 5,00, Benzina: 10,00
Stato attuale AUTO-LF494GF
Velocità: 5,00, Benzina: 4,60
Modifiche Valori (Accelerazione)
Stato attuale AUTO-AD594GD
Velocità: 17,00, Benzina: 9,76
...
```
