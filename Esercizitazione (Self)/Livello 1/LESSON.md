# Livello 1: Le Basi Assolute

## 1. Input/Output e Variabili

### Teoria Fondamentale: Tipi di Dato e Flussi di Sistema
In Java, l'interazione con l'utente avviene tramite i flussi standard (Standard Streams). La classe `Scanner` (presente nel package `java.util`) funge da interprete del flusso di byte in ingresso (tipicamente `System.in`, la tastiera). Mentre il flusso di base vede solo byte crudi, lo `Scanner` li "tokenizza", ovvero li scompone e li converte automaticamente in tipi primitivi Java (`int`, `double`, `String`, ecc.) basandosi su delimitatori (di default gli spazi bianchi o gli 'a capo').

In uscita, `System.out` rappresenta lo standard output. Al di sotto, Java utilizza un meccanismo di **Buffering**: i dati inviati a `System.out.print()` non vanno istantaneamente allo schermo, ma si accumulano in un'area di memoria (buffer). Vengono "flushati" (svuotati e stampati fisicamente) solo quando il buffer è pieno o quando si incontra un carattere speciale di ritorno a capo (innescato ad esempio da `System.out.println()`).

> **Definizione Accademica (Variabile e Stato):**
> Una variabile è un'astrazione della cella di memoria RAM. Essa è caratterizzata da un **tipo**, un **nome (identificatore)** e un **valore** (che definisce il suo *stato*). Java è un linguaggio **fortemente tipizzato** (strongly typed) e **staticamente tipizzato**. Questo significa che la natura di una variabile (se è un intero o una stringa) deve essere definita in fase di dichiarazione e non può mai mutare durante l'esecuzione del programma. Questo rigore serve a prevenire un'intera categoria di bug, i *Type Errors*, già in fase di compilazione.

Il **Type Casting** è il processo di conversione di un tipo di dato primitivo in un altro.
- **Casting Implicito (Widening):** Avviene automaticamente e in totale sicurezza quando si passa da un tipo "piccolo" a uno "grande" (es. da `int` a `double`), poiché non vi è alcun rischio di perdita di precisione o di *overflow*.
- **Casting Esplicito (Narrowing):** Richiede l'intervento esplicito del programmatore per "forzare" la conversione (es. `double` → `int`). L'ingegnere del software si assume la responsabilità di un potenziale troncamento dei dati (perdita dei decimali) o di uno sforo della capacità massima del tipo di destinazione.

### Sintassi ed Esempi di Codice
```java
import java.util.Scanner; // Import obbligatorio per usare il tokenizer di I/O

public class BasiAssolute {
    public static void main(String[] args) {
        // 1. Inizializzazione dello Scanner collegato al flusso di tastiera
        Scanner input = new Scanner(System.in);
        
        // 2. Output standard senza flush immediato
        System.out.print("Inserisci la tua età: ");
        
        // 3. Lettura tokenizzata di un intero
        int eta = input.nextInt(); 
        
        // RISOLUZIONE PROBLEMA DEL BUFFER
        // Quando digitiamo '20' e premiamo Invio, passiamo allo stream: "20\n".
        // nextInt() preleva solo "20", lasciando "\n" nel buffer.
        // Dobbiamo consumare questo 'a capo' pendente.
        input.nextLine(); 
        
        System.out.print("Inserisci il tuo nome completo: ");
        String nomeCompleto = input.nextLine(); // Legge tutto fino all'Invio
        
        // 4. Type Casting Esplicito
        double piGreco = 3.14159;
        // Forzatura accademica: perdiamo volontariamente informazione
        int piGrecoIntero = (int) piGreco; // Troncamento: la variabile conterrà 3
        
        System.out.println("Utente: " + nomeCompleto + " | Età: " + eta);
        
        // Chiusura dello Scanner per rilasciare il descrittore di file (File Descriptor)
        input.close(); 
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Il problema del buffer (Newline lasciato in sospeso):** Errore classico degli studenti al primo anno. Usando `nextInt()` o `nextDouble()`, lo Scanner legge il numero ma lascia nel buffer il carattere di 'A Capo' (`\n`). Se subito dopo si usa `nextLine()`, questo catturerà istantaneamente il `\n` residuo, leggendo una stringa vuota e saltando l'input dell'utente. *Soluzione:* Inserire sempre un `input.nextLine();` a vuoto dopo un `nextQualcosa()` se la lettura successiva richiede una stringa intera.
- **Resource Leak (Perdita di Risorse):** Lo Scanner, come i file e le connessioni di rete, alloca risorse a livello di sistema operativo. Dimenticare di chiamare `input.close()` alla fine del programma (o prima che lo Scanner esca dallo scope) genera un potenziale *Resource Leak*, un problema architetturale critico nei server in continua esecuzione.
- **`System.out.print` vs `System.out.println`:** Usare `println` è generalmente più sicuro perché forza lo svuotamento del buffer verso il monitor. `print` invece rischia di accodare il testo invisibilmente finché il buffer non raggiunge la saturazione o non riceve un flush.

---

## 2. Strutture di Controllo Condizionali

### Teoria Fondamentale: Biforcazione Algoritmica
L'esecuzione sequenziale "top-down" non basta per l'intelligenza artificiale o procedurale; il software deve prendere decisioni. Le strutture condizionali permettono al flusso di esecuzione di bifurcare (branching) basandosi sulla valutazione algebrica di espressioni logico-booleane.

L'istruzione **`if-else if-else`** è universale. Valuta le espressioni nell'esatto ordine in cui sono scritte. Se la prima condizione è vera, il suo blocco viene eseguito e le successive vengono categoricamente ignorate, garantendo la mutua esclusione. L'`else` finale agisce come blocco di "rete di salvataggio" (catch-all), eseguito solo se tutte le valutazioni precedenti falliscono.

Il costrutto **`switch`**, invece, non valuta espressioni complesse (es. `> 10`), ma verifica l'uguaglianza stretta tra una variabile di test e una lista di costanti letterali.

> **Dietro le Quinte (L'Ottimizzazione dello Switch):**
> Perché usare uno `switch` al posto di dieci `if-else`? Quando il compilatore Java incontra uno `switch` fitto di opzioni, invece di tradurlo in una noiosa serie di controlli sequenziali in Bytecode, genera spesso un'architettura chiamata **Jump Table** (Tabella dei salti). A tempo di esecuzione, la JVM non fa dieci domande, ma calcola matematicamente e *istantaneamente* (con tempo O(1)) a quale riga di codice saltare basandosi sul valore della variabile, rendendo l'esecuzione drasticamente più veloce.

### Sintassi ed Esempi di Codice: Enumerazioni e Switch
```java
public class CostruttiCondizionali {
    
    // Le Enum sono tipi di dato "stagnificati". Limitano l'universo di valori possibili.
    // Impediscono l'assegnazione accidentale di "PIPPO" a una variabile Giorno.
    public enum Giorno { LUNEDI, MERCOLEDI, VENERDI, SABATO, DOMENICA }
    
    public static void main(String[] args) {
        Giorno oggi = Giorno.MERCOLEDI;
        
        // ESEMPIO 1: Operatore Ternario (Assegnazione condizionale inline)
        // Sintassi: Condizione ? ValoreSeVero : ValoreSeFalso
        String statoUmore = (oggi == Giorno.DOMENICA) ? "Rilassato" : "Sotto Stress";
        System.out.println("Stato psicologico: " + statoUmore);
        
        // ESEMPIO 2: Costrutto Switch applicato in sinergia a una Enum
        switch (oggi) {
            case LUNEDI:
            case MERCOLEDI:
            case VENERDI:
                // Sfruttiamo il Fall-through in modo positivo: raggruppiamo i casi!
                System.out.println("Giorno di lezione intensa all'Università.");
                break; // IL BREAK È FONDAMENTALE PER FERMARE LA CASCATA!
                
            case SABATO:
            case DOMENICA:
                System.out.println("Giorno di studio autonomo e riposo.");
                break;
                
            default:
                // Il default cattura ogni valore non listato sopra. 
                // In questo caso gestisce implicitamente Martedì e Giovedì.
                System.out.println("Giornata non definita, assumiamo revisione codice.");
                break; 
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Sindrome del Fall-Through Dimenticato:** In Java, i `case` dello `switch` non sono blocchi isolati. Una volta trovata un'uguaglianza, l'esecuzione entra in quel `case` e, se non trova l'istruzione `break;`, **procede a valanga** (fall-through) eseguendo indiscriminatamente anche il codice di tutti i `case` successivi, ignorandone le etichette. Sebbene l'esempio sopra lo usi a vantaggio per raggruppare i casi, dimenticare un `break` non voluto genera bug logici letali.
- **Assegnazione al posto dell'uguaglianza nell'`if`:** Molti studenti scrivono `if (a = 5)` usando un solo segno uguale (che è l'operatore di assegnazione), sperando di testare l'uguaglianza. In C/C++ questo compila ed esegue sempre vero. Fortunatamente, il tipaggio forte di Java genera un errore di compilazione ("incompatible types: int cannot be converted to boolean"), bloccando questo disastro sul nascere.

---

## 3. Cicli e Iterazioni

### Teoria Fondamentale: Controllo in Testa vs Coda
Le macchine processano moli di dati immani ripetendo pedissequamente le stesse istruzioni. L'iterazione algoritmica è governata da tre costrutti principali in Java.

| Costrutto | Filosofia di Utilizzo | Posizione del Controllo (Test) |
| --- | --- | --- |
| **`for`** | **Iterazione Definita:** Usato quando il numero di cicli è noto a priori o quando si scandisce una struttura dati finita (Array/Lista). | In testa. L'inizializzazione, la condizione e l'aggiornamento sono compatti in una sola riga semantica. |
| **`while`** | **Iterazione Indefinita:** Usato quando il ciclo deve durare finché non si verifica un evento asincrono o finché non arriva un particolare *Valore Sentinella*. | **In Testa (Pre-condizione):** Il test viene valutato prima di entrare. Può verificarsi che il corpo non venga eseguito **mai** (0 iterazioni). |
| **`do-while`**| **Esecuzione Garantita:** Usato ad esempio per mostrare un menù all'utente. Vogliamo mostrarglielo e poi chiedergli se vuole ripetere l'azione. | **In Coda (Post-condizione):** Il blocco viene eseguito ciecamente la prima volta. Il test avviene solo in fondo. Esegue sempre il blocco **almeno 1 volta**. |

> **Dietro le Quinte (Scope e Iterazione):**
> Dichiarare la variabile contatore all'interno della definizione del `for` (es. `for (int i = 0; ... )`) non è solo comodo, ma architettonicamente perfetto. Questo forza la variabile `i` ad avere uno **Scope di Blocco**. Appena il ciclo termina, lo Stack Frame svuota la variabile `i` e la distrugge, liberando memoria e impedendo che inquini il codice sottostante.

### Sintassi ed Esempi di Codice
```java
import java.util.Scanner;

public class IterazioniAvanzate {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // --- 1. CICLO FOR (Iterazione Determinata) ---
        System.out.println("Conto alla rovescia spaziale:");
        // Inizializzazione ; Condizione di permanenza ; Step di modifica
        for (int i = 3; i > 0; i--) {
            System.out.println("T-" + i);
        }
        System.out.println("Ignizione!");
        
        // --- 2. CICLO WHILE CON VALORE SENTINELLA ---
        // Il -1 agisce da "Sentinella": un valore speciale impossibile come dato valido
        // che funge da comando occulto per far crollare la condizione.
        int inputUtente = 0;
        int somma = 0;
        
        System.out.println("\nSommatore (inserisci -1 per stampare il risultato):");
        
        // Pre-condizione: controlliamo prima di entrare.
        while (inputUtente != -1) {
            System.out.print("Numero: ");
            inputUtente = scanner.nextInt();
            
            if (inputUtente != -1) {
                // Operatore di assegnazione combinata (equivalente a somma = somma + inputUtente)
                somma += inputUtente; 
            }
        }
        System.out.println("La somma totale ammonta a: " + somma);
        
        // --- 3. CICLO DO-WHILE ---
        // Utile per menù o controlli dove l'azione va fatta prima del controllo
        int tentativi = 0;
        do {
            System.out.println("Tentativo numero " + (tentativi + 1) + " (eseguito ciecamente)");
            tentativi++;
        } while (tentativi < 0); // La condizione è falsa da subito, eppure viene eseguito una volta!
        
        scanner.close();
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Off-by-One Error:** Questo è l'errore algoritmico più pernicioso dell'informatica. Essendo Java "Zero-Indexed" (conta da 0), per ciclare un array di 5 elementi si va dall'indice 0 all'indice 4. Se si imposta la condizione del `for` su `i <= 5` (minore o uguale), all'ultimo giro il ciclo tenterà di accedere allo slot 5, causando l'implacabile crash della JVM tramite `ArrayIndexOutOfBoundsException`. Si deve usare la disuguaglianza stretta: `i < 5`.
- **Infinite Loop (Cicli Infiniti):** Dimenticarsi di inserire l'istruzione di aggiornamento (es. `i++`) nel corpo di un `while`, o aggiornare la variabile in modo che si allontani dalla condizione di uscita, bloccherà il thread in un ciclo perpetuo consumando un intero core della CPU al 100% senza scampo.
- **Variabili Ombra (Shadowing Errato):** Dichiarare una variabile int `i = 0;` fuori dal ciclo e poi rimettere `for(int i = 0; ...)` all'interno rimescolando i tipi, genera un disastro semantico di ridefinizione variabile che il compilatore blocca a difesa dell'information hiding globale.