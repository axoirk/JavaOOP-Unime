# Esercizio 4

---

### Descrizione
Programma che calcola la **media di una serie di voti** inseriti dall'utente, usando un ciclo `while` controllato da un valore sentinella.

L'utente inserisce un voto alla volta (numero ≥ 0).  
Quando inserisce un **numero negativo**, il ciclo termina e viene stampata la media dei voti inseriti.

#### Logica
1. Viene inizializzata la somma e un contatore a `0`.
2. Il ciclo `while` continua finché il valore inserito è ≥ 0.
3. Ogni numero valido viene sommato e il contatore viene incrementato.
4. Al termine vengono stampati: somma totale, contatore e media.

### Concetti trattati
- Ciclo `while` con valore sentinella
- Accumulatore e contatore
- Calcolo della media
- Cast da `int` a `float` per la divisione
- Output formattato con `System.out.printf`

### Esempio di esecuzione
```
Inserisci un valore:
8
Valore sommato: 8
Inserisci un valore:
6
Valore sommato: 6
Inserisci un valore:
-1
Risultati:
Totale Somma: 14
Stato Contatore: 2
Media: 7,00
```

