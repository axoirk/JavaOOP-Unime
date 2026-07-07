# Esercizio 2: Lettura File (Reader)

---

### Obiettivo
Imparare a leggere dati in modo persistente dal file system utilizzando le classi del pacchetto `java.io`, affrontando la gestione delle eccezioni legate all'Input/Output.

### Requisiti del task
1. **Preparazione del File:**
    - Assicurati di avere un file di testo (es. `out.txt`) nella cartella principale del progetto. Puoi usare il file generato dall'Esercizio 1.
2. **Creazione della classe `LettoreFile`:**
    - Importa le classi necessarie (`java.io.File`, `java.io.FileNotFoundException`, e `java.util.Scanner`).
    - Crea un oggetto `File` passando al costruttore il percorso o il nome del tuo file di testo.
    - Istanzia un oggetto `Scanner` passando l'oggetto `File` come sorgente.
3. **Gestione Eccezioni e Lettura:**
    - Poiché la lettura da file può generare una `FileNotFoundException`, avvolgi l'istanziazione dello `Scanner` in un blocco `try-with-resources`.
    - All'interno del `try`, usa un ciclo `while` basato sul metodo `hasNextLine()`.
    - Ad ogni iterazione, leggi la riga successiva con `nextLine()` e stampala a schermo con l'indice della riga.

### Concetti trattati
- Classe `File`
- Classe `Scanner` applicata ai file
- Gestione delle Checked Exceptions (`FileNotFoundException`)
- Cicli basati su controlli booleani (`hasNextLine`)

### Esempio di Output
```text
Riga 1 : Ciao
Riga 2 : mondo
Riga 3 : questo
Riga 4 : è
Riga 5 : un
Riga 6 : test
```

