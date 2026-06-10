# Livello 3: Array, Eccezioni e Strutture Dati

## 1. Array Primitivi e Algoritmi di Ordinamento

### Teoria Fondamentale: Memoria Contigua e Big-O
L'Array è la struttura dati più primordiale offerta da Java. La sua natura ingegneristica è rigorosa: alloca un blocco di memoria **strettamente contiguo** (tutti i blocchi sono fisicamente adiacenti nell'Heap). Questa scelta garantisce un tempo di accesso istantaneo e matematicamente calcolabile, $O(1)$, per qualsiasi indice.
Il grande compromesso di questa rigidità è l'immutabilità dimensionale: una volta istanziato con `new int[5]`, l'array non potrà mai espandersi né contrarsi.

> **Definizione Accademica (Selection Sort e Complessità):**
> Il Selection Sort (Ordinamento per Selezione) è un algoritmo didattico in loco. Logicamente, taglia l'array in due sezioni: una porzione "già ordinata" a sinistra e una "non ordinata" a destra. Ad ogni iterazione (passo), scandaglia la porzione destra alla ricerca del minimo assoluto e lo scambia (Swap) con l'elemento all'estrema sinistra della porzione non ordinata.
> Essendo composto da due cicli annidati che scorrono interamente i dati, la sua complessità temporale (Big-O) è pari a **$O(N^2)$**. Su array giganteschi risulta catastroficamente lento rispetto ad algoritmi logaritmici come Merge o Quick Sort.

### Sintassi ed Esempi di Codice: Lo Swap Sicuro
```java
public class OrdinamentoAccademico {
    public static void main(String[] args) {
        int[] array = {64, 25, 12, 22, 11}; // Inizializzazione inline
        
        // --- Algoritmo Selection Sort ---
        for (int i = 0; i < array.length - 1; i++) {
            int indiceMinimo = i; // Assumiamo che il minimo sia all'inizio del sotto-array
            
            // Ciclo interno: Ricerca lineare del vero minimo
            for (int j = i + 1; j < array.length; j++) {
                if (array[j] < array[indiceMinimo]) {
                    indiceMinimo = j; // Aggiorna la "coordinata" del minimo
                }
            }
            
            // Swap (Scambio in Loco): L'uso del bicchiere vuoto (temp)
            // Senza 'temp', sovrascriveremmo distruggendo uno dei due dati.
            int temp = array[indiceMinimo];
            array[indiceMinimo] = array[i];
            array[i] = temp;
        }
        
        // Stampa dell'array (Iterazione basata sull'indice)
        System.out.print("Array ordinato: ");
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i] + " ");
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Lo `Swap` Impossibile senza `temp`:** Molti studenti provano a scambiare le variabili scrivendo `a = b; b = a;`. Questo cancella irrimediabilmente il valore originale di `a`. Lo swap richiede matematicamente l'uso di una variabile tampone temporanea per proteggere il dato durante il travaso.
- **`NullPointerException` in Array di Oggetti:** Creare un array di stringhe `String[] nomi = new String[5];` alloca le 5 celle, ma al loro interno troverai solo il vuoto cosmico (`null`). Devi istanziare manualmente gli oggetti cella per cella (`nomi[0] = new String("Mario")`) prima di poterne invocare i metodi come `.length()`.

---

## 2. Architettura delle Eccezioni e Call Stack Unwinding

### Teoria Fondamentale: Checked vs Unchecked
Nel C, gli errori venivano gestiti in modo grezzo: i metodi restituivano codici numerici speciali (es. `-1` per indicare fallimento). Java rivoluziona questo aspetto trasformando l'errore in un **Oggetto** a sé stante: l'Eccezione (`Exception`). Questo oggetto contiene il messaggio d'errore e l'intera traccia (Stack Trace) delle funzioni che hanno causato il problema.

Quando si solleva un'eccezione, Java innesca il meccanismo di **Call Stack Unwinding** (Srotolamento dello Stack). Il metodo che fallisce "salta" in aria e muore prematuramente, l'eccezione viene passata al metodo chiamante, e se neanche lui ha previsto un salvataggio (`try-catch`), salta anche lui in aria, in una reazione a catena che distrugge il programma fino al `main()`.

Le eccezioni si dividono in due filosofie diametralmente opposte:
1. **Checked Exceptions:** (Es. `IOException`). Derivano da `Exception`. Sono anomalie prevedibili che dipendono da forze esterne al codice (es. disco rotto o server irraggiungibile). Il compilatore Java non compila il codice finché non implementi una rete di salvataggio (`try-catch`) obbligatoria.
2. **Unchecked Exceptions (Runtime):** (Es. `NullPointerException`, `IndexOutOfBoundsException`). Derivano da `RuntimeException`. Sono anomalie scatenate interamente da **bug logici** scritti dal programmatore. Il compilatore non ti obbliga a intercettarle, perché dovresti risolvere il bug alla radice, non nasconderlo sotto un tappeto.

> **Nota del Docente (`throw` vs `throws`):**
> Sono concetti radicalmente diversi. 
> `throw` è l'azione armata: **lancia fisicamente** l'oggetto bomba (es. `throw new Exception();`).
> `throws` è la burocrazia: è una dichiarazione posta nella firma del metodo per scaricare la responsabilità, dicendo al mondo "Attenzione, questo metodo può esplodere. Maneggiare con cura!".

### Sintassi ed Esempi di Codice: La Rete di Sicurezza
```java
// Definizione di un'eccezione custom (Fortemente Consigliato per architetture complesse)
public class SaldoInsufficienteException extends Exception {
    public SaldoInsufficienteException(String message) {
        super(message); // Delegare il messaggio alla superclasse per lo Stack Trace
    }
}

public class ContoBancario {
    private double saldo = 100.0;
    
    // Il metodo avvisa burocraticamente la JVM: "Potrei lanciare questa anomalia!" (throws)
    public void preleva(double importo) throws SaldoInsufficienteException {
        if (importo > saldo) {
            // L'anomalia viene istanziata nell'Heap e lanciata violentemente contro il flusso (throw)
            throw new SaldoInsufficienteException("Cassa vuota: hai solo €" + saldo);
        }
        saldo -= importo; // Questa riga non verrà MAI eseguita se c'è l'eccezione.
    }
    
    public static void main(String[] args) {
        ContoBancario conto = new ContoBancario();
        
        // Rete di salvataggio strutturale
        try {
            // Seleziona il pezzo di codice da proteggere (Zona Minata)
            conto.preleva(150.0);
            System.out.println("Soldi erogati."); // Ignorata se salta il try!
            
        } catch (SaldoInsufficienteException e) {
            // Qui si attutisce la caduta. L'oggetto 'e' contiene la bomba disinnescata.
            System.err.println("OPERAZIONE FALLITA: " + e.getMessage());
            
        } finally {
            // Questo blocco è sacro. Viene eseguito IN OGNI CASO (sia successo, sia catastrofe).
            // Usato accademicamente per chiudere risorse come database o file aperti nel 'try'.
            System.out.println("Disconnessione dal database bancario completata.");
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **L'Abominio del Catch Vuoto:** Scrivere `catch (Exception e) {}` per spegnere l'errore del compilatore senza intraprendere alcuna azione correttiva. È l'equivalente di staccare la sirena dell'allarme antincendio mentre la casa brucia: i bug verranno soppressi e saranno introvabili.
- **Inversione della Gerarchia nel Catch:** I blocchi `catch` multipli sono valutati top-down. Se catturi `Exception` (il padre di tutti) per primo, qualsiasi blocco `catch` sottostante (es. `IOException`) non verrà mai raggiunto e il codice non compilerà per "Unreachable Code". I `catch` vanno sempre posizionati **dal più specifico al più generico**.

---

## 3. Collezioni Dinamiche, ArrayList e Autoboxing

### Teoria Fondamentale: Il Ridimensionamento Invisibile
A differenza degli array primitivi, l'`ArrayList` (del framework Java Collections) è un'astrazione dinamica. Sotto il cofano non vi è alcuna stregoneria: l'ArrayList avvolge semplicemente un array primitivo `Object[]`. 

Quando invochi `add()` e superi la *Capacity* massima (lo spazio interno reale), l'ArrayList crea segretamente nell'Heap un nuovo array gigantesco (solitamente raddoppiandone la capienza), riversa tutti i vecchi dati nel nuovo array, abbandona il vecchio array in pasto al Garbage Collector e ti permette di inserire il nuovo elemento.

> **Definizione Accademica (Generics e Type Erasure):**
> Fino a Java 5, le liste contenevano genericamente oggetti `Object`, costringendo a pericolosi cast in uscita. I Generics (le parentesi angolari `<T>`) impongono un vincolo matematico a compile-time (Type Safety). 
> *Dietro le quinte (Type Erasure):* Durante la compilazione in Bytecode, Java "cancella" le informazioni sui Generics per retrocompatibilità. La JVM continua a vedere solo liste di `Object`, ma il compilatore ha inserito per noi tutti i cast sicuri invisibilmente.

### Sintassi ed Esempi di Codice: Wrapper e Foreach
```java
import java.util.ArrayList;

public class UtilizzoCollezioni {
    public static void main(String[] args) {
        
        // ArrayList<int> è illegale! I Generics accettano SOLO Riferimenti (Oggetti).
        // Usiamo le Classi Wrapper: Integer, Double, Boolean.
        // Il meccanismo che trasforma un int in un Integer si chiama AUTOBOXING.
        ArrayList<Integer> votiAccademici = new ArrayList<>();
        
        // Autoboxing: Java trasforma silenziosamente '28' in 'new Integer(28)'
        votiAccademici.add(28); 
        votiAccademici.add(30);
        votiAccademici.add(18);
        
        votiAccademici.remove(Integer.valueOf(18)); // Rimuove per valore l'oggetto Integer
        // votiAccademici.remove(1); // Rimuoverebbe l'oggetto per INDICE (il '30')
        
        // Enhanced For Loop (Sintassi Moderna For-Each)
        // Auto-Unboxing: Java trasforma silenziosamente 'Integer' in 'int'
        int somma = 0;
        for (int voto : votiAccademici) {
            somma += voto;
        }
        
        // Notare la differenza: l'array ha .length come variabile, la lista ha .size() come metodo!
        System.out.println("Media: " + (somma / votiAccademici.size()));
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Confondere `remove(int index)` con `remove(Object o)` negli ArrayList di interi:** Passare un `int` a `remove` indicherà sempre la rimozione per indice. Se vuoi rimuovere l'elemento che vale numericamente 5, devi passargli un oggetto Wrapper per fargli capire l'intento logico: `remove(Integer.valueOf(5))`.
- **Modificare la Lista durante l'Iterazione:** Se cerchi di usare un `remove()` dentro a un ciclo `for-each` sulla stessa lista, Java lancerà un'atroce `ConcurrentModificationException`. Il ciclo for-each è bloccato in lettura. Se devi snellire una lista iterando, usa un `Iterator` manuale e il suo metodo `iterator.remove()`.

---

## 4. Strutture Dati Custom (Linked List e Privacy Leak)

### Teoria Fondamentale: Nodi, Link e Garbage Collection
La Lista Concatenata (Linked List) stravolge il concetto contiguo dell'array. I dati non sono adiacenti. Vengono inglobati all'interno di "scatole" chiamate Nodi. Oltre al dato, ogni Nodo contiene un puntatore fisico (`next`) all'indirizzo di memoria del Nodo successivo.

Per mantenere il controllo, la classe centrale possiede solo un puntatore chiamato `head` (Testa), che mira dritto al primo nodo.
L'inserimento in testa ($O(1)$) è istantaneo: si staccano e riattaccano due puntatori. Tuttavia, trovare l'ultimo elemento impone uno scorrimento iterativo lungo tutta la catena saltando di memoria in memoria ($O(N)$).

> **Definizione Accademica (Inner Class e Privacy Leak):**
> Se il nodo `ListNode` fosse una classe pubblica standard, chiunque potrebbe istanziare nodi liberi o alterare i puntatori `next` della tua lista, spezzando la catena (Privacy Leak). 
> La soluzione accademica definitiva è dichiarare la classe Nodo come **`private class` (Inner Class)** all'interno della Lista Concatenata stessa. Questo sigilla tecnologicamente e logicamente i nodi dal mondo esterno.

### Sintassi ed Esempi di Codice: Sviluppo da Zero
```java
import java.util.Iterator;
import java.util.NoSuchElementException;

// Implementiamo Iterable per sbloccare la sintassi 'for-each'
public class ListaConcatenataCustom implements Iterable<String> {
    
    // INNER CLASS PRIVATA: Massima blindatura (Information Hiding architettonico)
    private class ListNode {
        String data;
        ListNode next; // Il "gancio" verso il prossimo nodo
        
        public ListNode(String data, ListNode next) {
            this.data = data;
            this.next = next;
        }
    }
    
    // Il sacro puntatore in cima alla lista
    private ListNode head;
    
    public ListaConcatenataCustom() {
        head = null; // Stato di lista vuota
    }
    
    // Inserimento Rapido in Testa (O(1))
    public void addFirst(String data) {
        // Logica brillante in un'unica riga: 
        // 1. Si crea un nodo in Heap.
        // 2. Il suo 'next' punta all'attuale 'head'.
        // 3. 'head' viene eletto a puntare sul nodo appena creato.
        head = new ListNode(data, head);
    }
    
    // Implementazione del Pattern Iterator
    @Override
    public Iterator<String> iterator() {
        return new Iterator<String>() {
            // Puntatore mobile usato per "passeggiare" sulla catena senza rovinare 'head'
            private ListNode current = head;
            
            @Override
            public boolean hasNext() {
                return current != null; // Se current sbatte su 'null', siamo alla fine!
            }
            
            @Override
            public String next() {
                if (!hasNext()) throw new NoSuchElementException();
                String val = current.data; // Estrae il dato
                current = current.next;    // Esegue il salto al nodo successivo
                return val;
            }
        };
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Perdere la Testa (Orphan Node):** Attenzione a non assegnare mai per sbaglio `head = head.next;` per scorrere la lista! Facendo così, perdi il riferimento al primissimo nodo. Di conseguenza, il Garbage Collector giudicherà il primo nodo come *Unreachable* e lo distruggerà per sempre. Per leggere una lista, si istanzia sempre un puntatore temporaneo (come `ListNode current = head;`) per preservare le ancore vitali.
- **Crash da Elemento Nullo (`NullPointerException` sulla coda):** Il nodo che chiude la lista avrà sempre il puntatore `next` impostato a `null`. Accedere avventatamente a `current.next.data` in prossimità della chiusura causerà inevitabilmente lo schianto del sistema. L'uso metodico del costrutto `while(current != null)` è vitale.

---

> ⚠️ **SEGNALAZIONE: ARGOMENTI MANCANTI E DA SPOSTARE RISPETTO AL NUOVO SYLLABUS**
> In base alla nuova organizzazione a 7 livelli, in questo file mancano i seguenti argomenti (che appartengono al Livello 3):
> - **Le Interfacce:** Dichiarazione (`interface`) e implementazione (`implements`), oltre alle differenze architetturali chiave rispetto alle classi astratte.
> - **Estensione di Interfacce e Comparable:** L'implementazione dell'interfaccia standard `Comparable` e del metodo `compareTo()` per l'ordinamento degli oggetti.
> - La teoria completa su **Ereditarietà, Polimorfismo e Classi Astratte** (attualmente è scritta nel file del Livello 2).
> 
> *Nota Strutturale:* Le strutture dati (`Array`, `ArrayList`, `LinkedList`) qui trattate restano propedeutiche e molto utili, ma non compaiono esplicitamente come requirement primari del Livello 3 nel nuovo piano di studi.