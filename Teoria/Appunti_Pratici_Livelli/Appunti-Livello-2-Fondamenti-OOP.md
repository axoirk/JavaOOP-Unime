# Livello 2: Fondamenti OOP (Programmazione Orientata agli Oggetti)

## 1. Classe vs Oggetto e Incapsulamento

### Teoria Fondamentale: Astrazione e Information Hiding
La Programmazione Orientata agli Oggetti (OOP) modella il software come un insieme di entità autonome (Oggetti) che interagiscono tra loro.
- **Classe**: Il blueprint (progetto) che definisce attributi e metodi.
- **Oggetto**: L'istanza concreta creata in memoria (Heap).
- **Incapsulamento**: Protezione dello stato interno tramite modificatori di accesso (`private`) e metodi pubblici (`getter`/`setter`).

### Esempio: Gestione di un Libro
```java
public class Libro {
    private String titolo;
    private String autore;
    private int pagine;

    // Costruttore
    public Libro(String titolo, String autore, int pagine) {
        this.titolo = titolo;
        this.autore = autore;
        setPagine(pagine); // Validazione tramite setter
    }

    // Getter e Setter con validazione
    public void setPagine(int pagine) {
        if (pagine > 0) {
            this.pagine = pagine;
        } else {
            System.out.println("Errore: il numero di pagine deve essere positivo.");
        }
    }

    public void mostraDettagli() {
        System.out.println("Libro: " + titolo + " | Autore: " + autore + " | Pagine: " + pagine);
    }
}
```

---

## 2. Variabili di Classe (Static) e Costanti

### Teoria Fondamentale: Stato Condiviso
- **`static`**: Una variabile o un metodo marcato come statico appartiene alla Classe, non alle singole istanze. Viene condiviso da tutti gli oggetti.
- **`final`**: Definisce una costante il cui valore non può essere cambiato dopo l'assegnazione.

### Esempio: Registro Cittadini
```java
public class Cittadino {
    // Variabile statica per contare la popolazione totale
    private static int popolazioneTotale = 0;
    
    // Costante universale
    public static final String SPECIE = "Homo Sapiens";

    private String nome;

    public Cittadino(String nome) {
        this.nome = nome;
        popolazioneTotale++; // Incremento condiviso
    }

    public static int getPopolazione() {
        return popolazioneTotale;
    }
}
```

---

## 3. Collezioni Dinamiche (ArrayList)

### Teoria Fondamentale: Liste Ridimensionabili
`ArrayList` è una classe del framework Collections che implementa un array dinamico. A differenza degli array primitivi, può cambiare dimensione a runtime e offre metodi pronti all'uso come `add()`, `remove()`, `size()` e `contains()`.

### Esempio: Registro Partecipanti
```java
import java.util.ArrayList;

public class Registro {
    public static void main(String[] args) {
        ArrayList<String> partecipanti = new ArrayList<>();

        partecipanti.add("Marco");
        partecipanti.add("Giulia");
        partecipanti.add("Antonio");

        System.out.println("Numero iscritti: " + partecipanti.size());
        
        // Rimozione
        partecipanti.remove("Antonio");

        // Iterazione con for-each
        for (String p : partecipanti) {
            System.out.println("Partecipante: " + p);
        }
    }
}
```

---

## 4. Inner Classes (Classi Interne)

### Teoria Fondamentale: Relazioni di Composizione
Una Inner Class è definita all'interno di un'altra classe. Viene usata per raggruppare classi che sono logicamente legate solo alla classe esterna, migliorando l'incapsulamento.

### Esempio: Smartwatch e Batteria
```java
public class Smartwatch {
    private String marca;
    private Batteria batteria;

    public Smartwatch(String marca) {
        this.marca = marca;
        this.batteria = new Batteria();
    }

    // Classe Interna Privata
    private class Batteria {
        private int percentuale = 100;
        
        public void scarica() {
            percentuale -= 10;
        }
    }
    
    public void usa() {
        batteria.scarica();
        System.out.println(marca + " in uso...");
    }
}
```

---

## 5. Mappe (Map, HashMap, TreeMap)

### Teoria Fondamentale: Strutture Chiave-Valore
In Java, l'interfaccia `Map` (come ad esempio `HashMap`, `TreeMap`) rappresenta una struttura dati del framework *Collections* che memorizza coppie di **Chiave-Valore** (Key-Value). A differenza delle liste (come `ArrayList`), i dati non sono indicizzati da un numero sequenziale, ma da una chiave univoca che permette di recuperare il valore associato in modo efficiente.

- **`HashMap`**: È l'implementazione più utilizzata. L'accesso e l'inserimento sono estremamente veloci, ma non garantisce alcun ordine specifico degli elementi inseriti.
- **`TreeMap`**: Mantiene le chiavi sempre ordinate (es. in ordine alfabetico o numerico naturale), ma le operazioni di inserimento/ricerca sono leggermente più lente rispetto all'`HashMap`.

### Esempio: Registro Voti (Mappa String -> Integer)
```java
import java.util.HashMap;
import java.util.Map;

public class RegistroVoti {
    public static void main(String[] args) {
        // Creazione di una mappa con Chiave=String (Nome) e Valore=Integer (Voto)
        Map<String, Integer> voti = new HashMap<>();

        // 1. Inserimento elementi (put)
        voti.put("Marco", 28);
        voti.put("Giulia", 30);
        voti.put("Antonio", 24);
        voti.put("Luca", 18);

        // 2. Lettura singola di un elemento (get)
        // Legge il valore associato alla chiave, restituisce null se non esiste
        Integer votoMarco = voti.get("Marco");
        System.out.println("Voto di Marco: " + votoMarco);

        // 3. Estrazione di un elemento (remove)
        // Rimuove la coppia dalla mappa e restituisce il valore che è stato appena eliminato
        Integer votoAntonio = voti.remove("Antonio");
        System.out.println("Antonio rimosso. Il suo voto era: " + votoAntonio);

        // 4. Verifica esistenza (containsKey / containsValue)
        if (voti.containsKey("Giulia")) {
            System.out.println("Giulia è presente nel registro.");
        }

        // 5. Lettura di tutte le chiavi (keySet) o di tutti i valori (values)
        System.out.println("\nSolo i Nomi (Chiavi): " + voti.keySet());
        System.out.println("Solo i Voti (Valori): " + voti.values());

        // 6. Iterazione completa su Coppie Chiave-Valore (entrySet)
        System.out.println("\n--- Elenco Voti Aggiornato ---");
        for (Map.Entry<String, Integer> entry : voti.entrySet()) {
            System.out.println("Studente: " + entry.getKey() + " | Voto: " + entry.getValue());
        }
    }
}
```
