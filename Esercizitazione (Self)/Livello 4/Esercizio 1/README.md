# Esercizio 1 – Scrivere e Leggere File di Testo / Writing and Reading Text Files

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio affronta le basi della manipolazione dei file di testo in Java, coprendo sia la scrittura che la lettura dei dati.

Il programma:
- richiede all'utente di inserire parole da tastiera finché non viene digitato "EXIT";
- salva ogni parola inserita all'interno di un file di testo chiamato `out.txt`;
- una volta terminato l'inserimento, riapre il file `out.txt`;
- legge il file riga per riga e stampa il contenuto formattato sulla console.

### Obiettivo didattico
L'obiettivo è consolidare:
- l'uso di `PrintWriter` per scrivere stringhe di testo in un file;
- l'uso di `Scanner` combinato con `File` per leggere i dati da un file;
- la corretta gestione delle eccezioni di I/O (`IOException`);
- l'implementazione del blocco `try-with-resources` per la chiusura automatica degli stream.

### Struttura e comportamento del codice
Flusso principale:
1. Creazione di uno stream di scrittura (`PrintWriter`) verso `out.txt`.
2. Ciclo di input interattivo tramite `Scanner` da `System.in`.
3. Scrittura continua sul file finché l'utente non inserisce "EXIT".
4. Chiusura automatica dello stream di scrittura.
5. Creazione di un nuovo `Scanner` per leggere dal file `out.txt`.
6. Ciclo di lettura che termina quando `hasNextLine()` restituisce `false`.
7. Stampa di ogni riga letta su console.

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Contiene la logica per la scrittura interattiva su file e la successiva lettura e stampa. |
| `out.txt` | File generato dinamicamente durante l'esecuzione del programma. |

### Concetti trattati
- Gestione I/O (Input/Output) sui file
- Classi `PrintWriter`, `Scanner` e `File`
- Gestione delle eccezioni (`try-catch`)
- `try-with-resources`
- Cicli `while` per l'elaborazione di stream di lunghezza indefinita

### Approfondimento: Il blocco Try-With-Resources
In questo esercizio viene utilizzato il costrutto `try-with-resources`, introdotto in Java 7. 
Prima di questo costrutto, ogni risorsa aperta (come un file, un database, o un socket) doveva essere chiusa manualmente nel blocco `finally` usando il metodo `close()`. Se si dimenticava di chiudere la risorsa, si rischiava un **memory leak** (perdita di memoria) o il blocco del file da parte del sistema operativo.

La sintassi del `try-with-resources` è la seguente:
```java
try (Risorsa res = new Risorsa()) {
    // utilizzo della risorsa
} catch (Eccezione e) {
    // gestione errore
}
```
In questo modo, la classe istanziata all'interno delle parentesi tonde del `try` (che deve implementare l'interfaccia `AutoCloseable`) **viene chiusa automaticamente** al termine del blocco `try`, indipendentemente dal fatto che venga lanciata un'eccezione o meno. Nel nostro codice, questo ci esenta dal dover chiamare esplicitamente `writer.close()` o `reader.close()`, rendendo il codice più pulito e sicuro.

### Esempio di esecuzione
```
Ciao
mondo
questo
è
un
test
EXIT
Riga file: Ciao
Riga file: mondo
Riga file: questo
Riga file: è
Riga file: un
Riga file: test
```

---

## 🇬🇧 English

### Description
This exercise covers the basics of text file manipulation in Java, demonstrating both writing and reading data.

The program:
- prompts the user to enter words from the keyboard until "EXIT" is typed;
- saves each entered word into a text file named `out.txt`;
- once input is complete, reopens the `out.txt` file;
- reads the file line by line and prints its content to the console.

### Learning objective
The goal is to strengthen:
- the use of `PrintWriter` to write strings of text to a file;
- the use of `Scanner` combined with `File` to read data from a file;
- proper I/O exception handling (`IOException`);
- the implementation of the `try-with-resources` statement for automatic stream closure.

### Code flow and behavior
Main flow:
1. Creation of a writing stream (`PrintWriter`) directed to `out.txt`.
2. Interactive input loop via `Scanner` from `System.in`.
3. Continuous writing to the file until the user inputs "EXIT".
4. Automatic closure of the writing stream.
5. Creation of a new `Scanner` to read from the `out.txt` file.
6. Reading loop that terminates when `hasNextLine()` returns `false`.
7. Printing of each read line to the console.

### Files
| File | Description |
|------|-------------|
| `Main.java` | Contains the logic for interactive file writing followed by reading and printing. |
| `out.txt` | Dynamically generated file during program execution. |

### Concepts covered
- File I/O (Input/Output) management
- `PrintWriter`, `Scanner`, and `File` classes
- Exception handling (`try-catch`)
- `try-with-resources`
- `while` loops for processing streams of unknown length

### In-depth: The Try-With-Resources statement
This exercise utilizes the `try-with-resources` construct, introduced in Java 7. 
Before this construct, every opened resource (such as a file, a database connection, or a socket) had to be manually closed in a `finally` block using the `close()` method. Forgetting to close a resource could lead to a **memory leak** or the file remaining locked by the operating system.

The syntax for `try-with-resources` is as follows:
```java
try (Resource res = new Resource()) {
    // using the resource
} catch (Exception e) {
    // error handling
}
```
By doing this, the class instantiated within the parentheses of the `try` block (which must implement the `AutoCloseable` interface) is **automatically closed** at the end of the `try` block, regardless of whether an exception is thrown or not. In our code, this frees us from having to explicitly call `writer.close()` or `reader.close()`, making the code cleaner and safer.

### Sample run
```
Hello
world
this
is
a
test
EXIT
Riga file: Hello
Riga file: world
Riga file: this
Riga file: is
Riga file: a
Riga file: test
```