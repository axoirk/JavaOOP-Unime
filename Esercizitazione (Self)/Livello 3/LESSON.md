# Livello 3: Array, Eccezioni e Strutture Dati

## 1. Array e Ordinamento

### Teoria Fondamentale
L'Array è una struttura dati statica e contigua in memoria che ospita un numero fisso di elementi dello stesso tipo. La dimensione è inalterabile dopo la creazione. La proprietà di sola lettura `.length` ne indica la capacità.

> **Definizione Accademica (Selection Sort):**
> L'algoritmo di Ordinamento per Selezione procede dividendo l'array in due porzioni: una ordinata e una non ordinata. In ogni iterazione, cerca il minimo assoluto nella parte non ordinata e lo "scambia" (Swap) con l'elemento all'estrema sinistra.

### Sintassi ed Esempi di Codice
```java
public class Ordinamento {
    public static void main(String[] args) {
        int[] array = {64, 25, 12, 22, 11};
        
        // Selection Sort
        for (int i = 0; i < array.length - 1; i++) {
            int indiceMinimo = i;
            
            // Trova l'indice dell'elemento minimo
            for (int j = i + 1; j < array.length; j++) {
                if (array[j] < array[indiceMinimo]) {
                    indiceMinimo = j;
                }
            }
            
            // Swap: Scambio degli elementi usando una variabile temporanea
            int temp = array[indiceMinimo];
            array[indiceMinimo] = array[i];
            array[i] = temp;
        }
        
        // Stampa dell'array ordinato
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i] + " ");
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Lo `Swap` imperfetto:** Dimenticare la variabile temporanea `temp` nello Swap causa la sovrascrittura distruttiva e la perdita permanente di un dato (`a = b; b = a;` fa sì che entrambi i valori diventino `b`).
- **`NullPointerException` in Array di Oggetti:** Inizializzare un array di oggetti (`Studente[] s = new Studente[5];`) istanzia l'array, ma i suoi slot contengono tutti `null`. Non dimenticare di istanziare i singoli elementi (es. `s[0] = new Studente();`) prima di invocarne i metodi.

---

## 2. Gestione delle Eccezioni

### Teoria Fondamentale
In Java, le eccezioni sono Oggetti. Segnalano il verificarsi di un evento anomalo che interrompe il flusso normale. Si dividono in *Checked* (il compilatore obbliga a gestirle) e *Unchecked* (derivate da `RuntimeException`, non gestite obbligatoriamente).

> **Nota del Docente (`throw` vs `throws`):**
> `throw` è l'azione materiale: lancia fisicamente l'oggetto eccezione (es. `throw new Exception();`).
> `throws` è la dichiarazione nella firma del metodo: avvisa chi chiamerà il metodo che potrebbe arrivare un'eccezione, scaricando la responsabilità (es. `public void metodo() throws Exception`).

### Sintassi ed Esempi di Codice
```java
// Custom Exception
public class SaldoInsufficienteException extends Exception {
    public SaldoInsufficienteException(String message) {
        super(message); // Passa il messaggio alla superclasse Exception
    }
}

public class ContoBancario {
    private double saldo = 100.0;
    
    // 'throws' dichiara la potenziale pericolosità
    public void preleva(double importo) throws SaldoInsufficienteException {
        if (importo > saldo) {
            // 'throw' lancia materialmente l'anomalia
            throw new SaldoInsufficienteException("Errore: Vuoi prelevare " + importo + " ma hai solo " + saldo);
        }
        saldo -= importo;
    }
    
    public static void main(String[] args) {
        ContoBancario conto = new ContoBancario();
        
        // Architettura Try-Catch
        try {
            conto.preleva(150.0);
            System.out.println("Prelievo effettuato!"); // Non eseguito se c'è eccezione
        } catch (SaldoInsufficienteException e) {
            // Recupero del problema e log
            System.out.println(e.getMessage());
        } finally {
            // Blocco eseguito SEMPRE, utile per chiudere risorse aperte nel try
            System.out.println("Operazione terminata.");
        }
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Catch vuoto:** Catturare un'eccezione (`catch(Exception e) { }`) senza fare nulla (Empty Catch Block) è considerato un abominio accademico. Nasconde i bug senza risolverli.
- **Gerarchia nel Catch:** I blocchi `catch` multipli vanno sempre disposti dal più specifico (es. `IOException`) al più generico (`Exception`). Se si fa il contrario, il più specifico diventerà "Unreachable code" (Codice irraggiungibile) e il programma non compilerà.

---

## 3. Collezioni Dinamiche (ArrayList)

### Teoria Fondamentale
`ArrayList` è una struttura basata su array ridimensionabili automaticamente. Quando è saturo, raddoppia internamente lo spazio e vi riversa i dati precedenti.

> **Definizione Accademica (Generics e Type Safety):**
> I Generics (`<T>`) forzano l'ArrayList a contenere esclusivamente un determinato tipo di dato. Questo fornisce la **Type Safety** a tempo di compilazione, azzerando i rischi di `ClassCastException` in fase di iterazione.

### Sintassi ed Esempi di Codice
```java
import java.util.ArrayList;

public class TestArrayList {
    public static void main(String[] args) {
        // ArrayList con Generics (Solo String)
        ArrayList<String> studenti = new ArrayList<>();
        
        studenti.add("Alice");
        studenti.add("Bob");
        studenti.add("Carlo");
        
        studenti.remove("Bob"); // Rimuove per valore
        
        // Enhanced For Loop (Iterazione Sicura e Pulita)
        for (String studente : studenti) {
            System.out.println("Nome: " + studente);
        }
        
        System.out.println("Dimensione totale: " + studenti.size());
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Array fuori range (IndexOut):** Su un ArrayList di grandezza 3, inviare `.add(5, "Pippo")` provoca una `IndexOutOfBoundsException`. L'inserimento deve essere consequenziale o esistere precedentemente.
- **Tipi Primitivi:** L'ArrayList **NON** supporta primitivi (`int`, `double`). Devi usare le classi Wrapper (Autoboxing): `ArrayList<Integer>` o `ArrayList<Double>`.

---

## 4. Strutture Dati Custom (Linked List)

### Teoria Fondamentale
A differenza degli array contigui, la Lista Concatenata poggia su "Nodi" isolati in memoria. Ogni nodo conserva il valore utile e un riferimento (puntatore) al nodo successivo in catena.

> **Definizione Accademica (Privacy Leak e Inner Classes):**
> Affinché il mondo esterno non possa stravolgere la catena manipolando i puntatori grezzi, la classe Nodo (`ListNode`) deve essere protetta. La si implementa come classe **Inner (Interna) e Privata** dentro la LinkedList principale. Questo sigilla (information hiding) l'architettura tecnica e previene i Privacy Leak.

| Array Classico | Linked List |
| --- | --- |
| Accesso diretto veloce in lettura (O(1)) | Accesso lento, necessita scorrimento sequenziale (O(N)) |
| Inserimento in mezzo lento e costoso (shift O(N)) | Inserimento in testa/mezzo rapidissimo, si staccano 2 puntatori (O(1)) |

### Sintassi ed Esempi di Codice
```java
import java.util.Iterator;

public class ListaCustom implements Iterable<Integer> {
    
    // Inner Class Privata (nessun Privacy Leak!)
    private class ListNode {
        int dato;
        ListNode next; // Puntatore al prossimo nodo
        
        public ListNode(int dato, ListNode next) {
            this.dato = dato;
            this.next = next;
        }
    }
    
    // Testa della Lista
    private ListNode head;
    
    public ListaCustom() {
        head = null; // Inizialmente vuota
    }
    
    // Inserimento in Testa (O(1))
    public void addFirst(int dato) {
        // Il nuovo nodo punta alla vecchia testa, e diventa la nuova testa
        head = new ListNode(dato, head);
    }
    
    // Pattern Iterator 
    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<Integer>() {
            private ListNode current = head;
            
            @Override
            public boolean hasNext() {
                return current != null;
            }
            
            @Override
            public Integer next() {
                int data = current.dato;
                current = current.next; // Scorre in avanti
                return data;
            }
        };
    }
}
```

### Best Practices & Errori Comuni (Trick Accademici)
- **Perdere la Testa (Orphan Node):** Attenzione a non assegnare per sbaglio `head = head.next;` durante una lettura! Perderesti il primo nodo in eterno (e il Garbage Collector se lo porterebbe via). Usa sempre un puntatore temporaneo di scorrimento (es. `ListNode current = head;`).
- **Gestione del `null`:** In prossimità della coda, bisogna stare attenti a controllare se `.next == null` prima di invocarne parametri, per non far crollare il codice con la `NullPointerException`.