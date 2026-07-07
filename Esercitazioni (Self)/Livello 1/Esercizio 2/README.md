# Esercizio 2

---

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

