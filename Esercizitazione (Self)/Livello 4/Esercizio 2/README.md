# Esercizio 2: Lettura File (Reader) / Exercise 2: File Reading (Reader)

---

## 🇮🇹 Italiano

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

---

## 🇬🇧 English

### Objective
Learn how to read data persistently from the file system using the `java.io` package classes, handling Input/Output exceptions.

### Task Requirements
1. **File Preparation:**
    - Ensure you have a text file (e.g., `out.txt`) in the project's root folder. You can use the file generated in Exercise 1.
2. **Creating the `LettoreFile` Class:**
    - Import the necessary classes (`java.io.File`, `java.io.FileNotFoundException`, and `java.util.Scanner`).
    - Create a `File` object by passing the path or name of your text file to the constructor.
    - Instantiate a `Scanner` object by passing the `File` object as the source.
3. **Exception Handling and Reading:**
    - Since reading from a file can throw a `FileNotFoundException`, wrap the `Scanner` instantiation in a `try-with-resources` block.
    - Inside the `try` block, use a `while` loop based on the `hasNextLine()` method.
    - In each iteration, read the next line with `nextLine()` and print it to the screen along with the line index.

### Concepts Covered
- `File` class
- `Scanner` class applied to files
- Handling Checked Exceptions (`FileNotFoundException`)
- Boolean-based loops (`hasNextLine`)

### Output Example
```text
Riga 1 : Hello
Riga 2 : world
Riga 3 : this
Riga 4 : is
Riga 5 : a
Riga 6 : test
```
