# 02. Fondamenti, Sintassi e Gestione della Memoria

## Il Sistema dei Tipi in Java

Java è un linguaggio **fortemente tipizzato** (strongly typed) e **staticamente tipizzato** (statically typed). Questo significa che il programmatore è obbligato a dichiarare preventivamente la natura dei dati che una variabile conterrà e che questa natura non può mutare nel corso del programma. Il compilatore si erge a giudice spietato, rifiutando di generare il Bytecode se rileva incoerenze (ad esempio, il tentativo di inserire una stringa testuale in una variabile matematica). 

Questa rigidità, che inizialmente potrebbe sembrare un ostacolo alla creatività, è in realtà uno strumento accademico di ingegneria del software formidabile: permette di intercettare interi rami di errori semantici (i famosi *Type Errors*) in fase di compilazione, ben prima che il software venga distribuito all'utente finale.

In Java, la materia prima si divide in due macro-famiglie distinte: i **Tipi Primitivi** e i **Tipi Reference (Oggetti)**.

### I Tipi Primitivi
Sono le fondamenta atomiche dell'informazione. Non sono oggetti, non hanno metodi, e contengono direttamente e letteralmente il valore binario dell'informazione. La loro dimensione è standardizzata e immutabile su qualsiasi sistema operativo.

| Tipo Primitivo | Dimensione in Memoria | Utilità e Ruolo |
| --- | --- | --- |
| `boolean` | 1 bit (circa) | Algebra booleana, ammette solo due stati: `true` o `false`. |
| `byte` | 8 bit (1 byte) | Numeri interi estremamente piccoli (da -128 a 127). Utile per flussi binari. |
| `short` | 16 bit (2 byte) | Numeri interi piccoli. Poco utilizzato nella pratica moderna. |
| `int` | 32 bit (4 byte) | Lo standard de facto per la numerazione intera (es. contatori). |
| `long` | 64 bit (8 byte) | Numeri interi colossali (es. timestamp o ID di database globali). |
| `float` | 32 bit (4 byte) | Numeri a virgola mobile a singola precisione. |
| `double` | 64 bit (8 byte) | Numeri a virgola mobile a doppia precisione (lo standard per i decimali). |
| `char` | 16 bit (2 byte) | Un singolo carattere Unicode. Gestisce alfabeti internazionali. |

### I Tipi Reference (Riferimenti)
A differenza dei primitivi, i tipi reference non contengono i dati veri e propri. Essi contengono un "indirizzo" (un puntatore astratto) che indica alla JVM dove, nella vasta prateria della memoria, risiede l'oggetto reale e i suoi metodi. Le Stringhe, gli Array e tutte le Classi create dal programmatore sono Tipi Reference.

## Dietro le Quinte: Stack Memory e Heap Memory

La vera essenza della programmazione in Java si svela comprendendo la geografia della memoria della Java Virtual Machine. Quando un programma è in esecuzione, la JVM organizza i dati in due arene principali: lo **Stack** e l'**Heap**.

> **Definizione Accademica (Stack vs Heap):**
> Lo **Stack** è un'area di memoria piccola, velocissima e ordinata (Last In, First Out). Ospita l'esecuzione dei metodi e conserva unicamente le variabili locali di tipo primitivo e i *riferimenti* agli oggetti. 
> L'**Heap**, al contrario, è un immenso serbatoio disordinato. Qualsiasi cosa venga istanziata tramite la parola chiave `new` (inclusi gli Array) prende fisicamente forma e risiede nell'Heap.

Quando si dichiara una variabile:
- Se è **primitiva** (es. `int x = 5;`), la JVM ritaglia uno spazio nello Stack grande esattamente 32 bit e vi scrive dentro un bel '5' in binario.
- Se è di tipo **reference** (es. `Studente s = new Studente();`), avvengono due cose distinte: 
  1. L'espressione `new Studente()` ordina alla JVM di allocare memoria nell'**Heap** per ospitare un nuovo studente.
  2. La variabile `s` viene posizionata nello **Stack**, e al suo interno non c'è lo studente, ma l'indirizzo di memoria (es. `0xFE23`) che punta allo studente nell'Heap.

Questo meccanismo è il motivo per cui, in Java, passare un primitivo a un metodo significa passarlo **per valore** (viene creata una copia esatta del dato), mentre passare un oggetto significa copiare il *riferimento*: entrambi i riferimenti punteranno allo stesso identico oggetto condiviso nell'Heap.

## Il concetto di "null" e la NullPointerException

Un riferimento non è obbligato a puntare immediatamente a un oggetto. Se dichiari `Studente s;` senza instanziarlo, quella variabile è come un telecomando senza un apparecchio associato. In Java, questo concetto di "assenza di puntamento" è formalizzato dalla parola chiave `null`.

Se tenti di premere i tasti di quel telecomando (cioè invocare metodi o leggere variabili tramite un riferimento `null`), la JVM si accorgerà che l'indirizzo conduce nel vuoto cosmico, interromperà l'esecuzione brutalmente e lancerà la famigerata **NullPointerException** (NPE), considerata il tallone d'Achille della programmazione a oggetti.

```java
public class AnalisiMemoria {
    public static void main(String[] args) {
        
        // 1. Variabile Primitiva: risiede e contiene il suo valore interamente nello Stack.
        int eta = 24; 
        
        // 2. Variabile Reference instanziata
        // - "String" è un oggetto. 
        // - La variabile 'nome' risiede nello Stack e punta alla memoria Heap.
        // - L'oggetto stringa "Leonardo" risiede nell'Heap.
        String nome = new String("Leonardo"); 
        
        // 3. Variabile Reference non instanziata (Puntamento a null)
        String cognome = null; 
        
        // 4. Pericolo Accademico!
        // Cercare di invocare un metodo su un riferimento nullo causerà il crash immediato
        // del software tramite NullPointerException.
        // int lunghezza = cognome.length(); // <-- ERRORE GRAVE!
        
        // Soluzione difensiva: controllo dell'assenza di null (Null Check)
        if (cognome != null) {
            System.out.println(cognome.length());
        } else {
            System.out.println("Il riferimento 'cognome' è vuoto!");
        }
    }
}
```

La gestione rigorosa dello stato nullo e la chiara separazione tra memoria primitivo/locale (Stack) e memoria oggetti (Heap) sono requisiti ineliminabili per lo sviluppo di software mission-critical in Java.