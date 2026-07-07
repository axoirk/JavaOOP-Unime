# Esercizio 1

---

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

