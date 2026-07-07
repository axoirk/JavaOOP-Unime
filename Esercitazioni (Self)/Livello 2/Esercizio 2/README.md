# Esercizio 2

---

### Descrizione
Programma che approfondisce l'**overloading dei costruttori** in Java, mostrando come inizializzare lo stesso tipo di oggetto in modi diversi.

Viene definita una classe `Pet` con attributi:
- nome (`name`)
- eta (`age`)
- peso (`weight`)

Sono presenti tre costruttori:
- costruttore di default `Pet()`
- costruttore con solo nome `Pet(String name)` (imposta eta e peso a 0)
- costruttore completo `Pet(String name, Integer age, Double weight)`

Nel `Main` vengono creati tre oggetti con firme diverse, poi modificati con setter e utilizzati con i metodi:
- `showInfo()`
- `bark()`

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Crea tre oggetti `Pet` con costruttori diversi, aggiorna alcuni valori e richiama i metodi di output |
| `Pet.java` | Definisce attributi, costruttori overloadati, metodi di comportamento e getter/setter |

### Concetti trattati
- Overloading dei costruttori
- Inizializzazione oggetti con firme diverse
- Incapsulamento tramite attributi `private` e getter/setter
- Uso di `this` nei costruttori
- Invocazione di metodi su oggetti
- Output formattato con `System.out.printf`

### Esempio di esecuzione
```
Ciao! Il mio nome e Johnny, ho 10 anni, e peso 50.10 KG
Ciao! Il mio nome e Arturo, ho 0 anni, e peso 0.00 KG
Ciao! Il mio nome e Tom, ho 10 anni, e peso 5.00 KG
Ciao! Il mio nome e Arturo, ho 5 anni, e peso 10.50 KG
Woff Woff! Sono Tom e sto abbagliando
...
```

