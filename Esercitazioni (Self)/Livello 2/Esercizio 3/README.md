# Esercizio 3

---

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

