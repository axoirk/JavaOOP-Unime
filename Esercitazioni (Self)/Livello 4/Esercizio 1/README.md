# Esercizio 1: Scrivere e Leggere File di Testo

---

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

