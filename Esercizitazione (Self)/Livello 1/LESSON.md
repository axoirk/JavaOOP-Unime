# Livello 1: Le Basi Assolute

## 1. Input/Output e Variabili

### Teoria Fondamentale
In Java, l'interazione con l'utente avviene tramite i flussi standard (Standard Streams). La classe `Scanner` (presente nel package `java.util`) funge da interprete del flusso di byte in ingresso (tipicamente `System.in`, la tastiera), trasformandolo in tipi primitivi. 

> **Definizione Accademica (Variabile e Stato):**
> Una variabile è un'astrazione della cella di memoria RAM. Essa è caratterizzata da un **tipo**, un **nome (identificatore)** e un **valore** (che definisce il suo *stato*). In Java, essendo fortemente tipizzato (strongly typed), il tipo determina lo spazio allocato e le operazioni consentite.

Il **Type Casting** è il processo di conversione di un tipo di dato in un altro.
- **Casting Implicito (Widening):** Avviene automaticamente quando si passa da un tipo più "piccolo" a uno più "grande" (es. `int` → `double`), senza perdita di precisione.
- **Casting Esplicito (Narrowing):** Richiede l'intervento del programmatore per "forzare" la conversione (es. `double` → `int`), con possibile troncamento dei dati.

### Sintassi ed Esempi di Codice
```java
import java.util.Scanner; // Import obbligatorio per l'I/O

public class BasiAssolute {
    public static void main(String[] args) {
        // 1. Inizializzazione dello Scanner
        Scanner input = new Scanner(System.in);
        
        // 2. Output standard
        System.out.print("Inserisci la tua età: ");
        
        // 3. Lettura di un intero
        int eta = input.nextInt(); 
        
        // Risoluzione del problema del buffer (consuma il carattere di newline '\n')
        input.nextLine(); 
        
        System.out.print("Inserisci il tuo nome: ");
        String nome = input.nextLine();
        
        // 4. Type Casting Esplicito
        double piGreco = 3.14159;
        int piGrecoIntero = (int) piGreco; // Troncamento: diventa 3
        
        System.out.println("Nome: " + nome + " | Età: " + eta);
        
        // Chiusura dello Scanner per rilasciare le risorse
        input.close(); 
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Il problema del buffer (Newline lasciato in sospeso):** Quando usi `nextInt()` o `nextDouble()`, lo Scanner legge il numero ma lascia nel buffer il carattere di 'A Capo' (`\n`). Se subito dopo chiami `nextLine()`, questo leggerà stringa vuota! *Soluzione:* Inserire sempre un `input.nextLine();` a vuoto dopo un `nextInt()` se si deve leggere una stringa.
- **Memory Leak e `close()`:** Ricorda sempre di invocare `.close()` sugli oggetti che manipolano stream (come Scanner) per evitare di esaurire i file descriptor (Memory Leak).
- **`System.out.print` vs `System.out.println`:** Il primo stampa sulla stessa riga, il secondo aggiunge un fine riga.

---

## 2. Strutture di Controllo Condizionali

### Teoria Fondamentale
Le strutture condizionali permettono al flusso di esecuzione di bifurcare (branching) in base a espressioni booleane. L'istruzione `if-else` valuta espressioni logiche sequenziali, mentre lo `switch` crea un salto diretto (jump table) basato sul valore esatto di una variabile.

> **Nota del Docente (Le Enumerazioni):**
> Le `enum` sono tipi speciali introdotti per raggruppare un set predefinito di costanti (es. i giorni della settimana). Abbinate al costrutto `switch`, migliorano nettamente la leggibilità del codice e garantiscono la **Type Safety**, impedendo l'assegnazione di valori non validi.

| Caratteristica | `if-else if` | `switch` |
| --- | --- | --- |
| **Condizioni** | Qualsiasi espressione booleana (range, maggiore/minore) | Valori esatti, Stringhe (da Java 7) ed Enum |
| **Prestazioni** | Valutazione lineare (O(N) nel caso peggiore) | Ottimizzato dal compilatore (Jump Table) |
| **Leggibilità** | Minore in caso di molte opzioni | Maggiore per scelte multiple fisse |

### Sintassi ed Esempi di Codice
```java
public class CostruttiCondizionali {
    
    // Definizione di un'Enumerazione
    public enum Giorno { LUNEDI, MERCOLEDI, VENERDI, DOMENICA }
    
    public static void main(String[] args) {
        Giorno oggi = Giorno.MERCOLEDI;
        
        // Costrutto Switch applicato a una Enum
        switch (oggi) {
            case LUNEDI:
            case MERCOLEDI:
            case VENERDI:
                System.out.println("Giorno di lezione all'Università.");
                break; // FONDAMENTALE: Evita il Fall-through
                
            case DOMENICA:
                System.out.println("Giorno di riposo.");
                break;
                
            default:
                System.out.println("Studio individuale.");
                // Nel default il break è opzionale ma consigliato
                break; 
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Sindrome del Fall-Through:** Omettere il `break` in un `case` dello `switch` fa sì che vengano eseguiti anche tutti i `case` successivi indiscriminatamente. *A volte è desiderato (come nel raggruppamento dei giorni feriali sopra), ma il 90% delle volte è un bug grave.*
- **Errore di assegnazione nell'`if`:** Scrivere `if (a = 5)` (singolo uguale) in linguaggi derivati dal C causa enormi bug; in Java causa errore di compilazione a meno che `a` non sia booleano, offrendo maggiore sicurezza nativa.

---

## 3. Cicli e Iterazioni

### Teoria Fondamentale
L'iterazione permette di ripetere un blocco di istruzioni. La scelta del costrutto ciclico dipende dalla natura del problema:

> **Definizione Accademica (Il Valore Sentinella):**
> Un valore sentinella (es. `-1` in input) è una flag usata per terminare un ciclo la cui lunghezza non è nota a priori. Consente all'utente di segnalare esplicitamente "fine dei dati".

| Costrutto | Quando utilizzarlo | Controllo |
| --- | --- | --- |
| `for` | Il numero di iterazioni è **noto a priori** (es. iterare su un array). | Inizializzazione, condizione e incremento compatti. |
| `while` | Il numero di iterazioni **non è noto** (es. ciclo con valore sentinella). | Controllo in Testa (potrebbe eseguire 0 iterazioni). |
| `do-while`| Simile al while, ma deve eseguire il blocco **almeno una volta**. | Controllo in Coda. |

### Sintassi ed Esempi di Codice
```java
import java.util.Scanner;

public class Iterazioni {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int inputUtente;
        int somma = 0;
        
        // Ciclo WHILE con Valore Sentinella (-1)
        System.out.println("Inserisci numeri per sommarli (-1 per terminare):");
        inputUtente = scanner.nextInt();
        
        while (inputUtente != -1) {
            // Operatore di assegnazione combinata (somma += x equivale a somma = somma + x)
            somma += inputUtente; 
            System.out.print("Prossimo numero: ");
            inputUtente = scanner.nextInt();
        }
        
        System.out.println("La somma totale è: " + somma);
        
        // Ciclo DO-WHILE
        int counter = 0;
        do {
            System.out.println("Esecuzione numero: " + counter);
            counter++; // Operatore aritmetico post-incremento
        } while (counter < 0); // Esegue comunque una volta!
        
        scanner.close();
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Off-by-One Error:** Errore logico comunissimo nel `for`. Partendo da `i = 0`, la condizione deve essere strettamente minore (`i < lunghezza`), non minore/uguale (`i <= lunghezza`), altrimenti si genera una `IndexOutOfBoundsException`.
- **Infinite Loop (Cicli Infiniti):** Dimenticarsi di aggiornare la variabile di controllo nel corpo di un `while` causerà il blocco del programma in un ciclo infinito.
- **Variabili Ombra (Shadowing):** Dichiarare una variabile `int i = 0;` fuori dal ciclo e poi un `for(int i = 0; ...)` all'interno genera un conflitto di visibilità e shadowing non consentito in Java (il compilatore si arrabbia).