# Livello 1: Le Basi della Programmazione e Sintassi

## 1. Input/Output e Variabili

### Teoria Fondamentale: Tipi di Dato e Flussi di Sistema
In Java, l'interazione con l'utente avviene tramite i flussi standard (Standard Streams). La classe `Scanner` (presente nel package `java.util`) funge da interprete del flusso di byte in ingresso (tipicamente `System.in`, la tastiera). Mentre il flusso di base vede solo byte crudi, lo `Scanner` li "tokenizza", ovvero li scompone e li converte automaticamente in tipi primitivi Java (`int`, `double`, `String`, ecc.) basandosi su delimitatori (di default gli spazi bianchi o gli 'a capo').

> **Definizione Accademica (Variabile e Stato):**
> Una variabile è un'astrazione della cella di memoria RAM. Essa è caratterizzata da un **tipo**, un **nome (identificatore)** e un **valore**. Java è un linguaggio **fortemente tipizzato** (strongly typed) e **staticamente tipizzato**.

### Esempio: Calcolo dell'Area di un Cerchio
In questo esempio, chiediamo all'utente il raggio di un cerchio e calcoliamo l'area, dimostrando l'uso di `Scanner` e `double`.

```java
import java.util.Scanner;

public class CalcoloArea {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Inserisci il raggio del cerchio: ");
        double raggio = input.nextDouble();
        
        // Uso della costante Math.PI e del metodo Math.pow per l'elevamento a potenza
        double area = Math.PI * Math.pow(raggio, 2);
        
        System.out.printf("L'area del cerchio con raggio %.2f è: %.2f\n", raggio, area);
        
        input.close();
    }
}
```

---

## 2. Strutture di Controllo Condizionali

### Teoria Fondamentale: Biforcazione Algoritmica
Le strutture condizionali permettono al flusso di esecuzione di biforcarsi basandosi sulla valutazione di espressioni logico-booleane. 
L'istruzione **`if-else`** gestisce intervalli o condizioni complesse, mentre lo **`switch`** è ottimizzato per il confronto di una singola variabile con più valori costanti (Jump Table).

### Esempio: Classificazione Temperature e Stagioni
Usiamo un `if-else` per classificare il clima e uno `switch` per stampare un messaggio in base alla stagione.

```java
public class Clima {
    public enum Stagione { PRIMAVERA, ESTATE, AUTUNNO, INVERNO }

    public static void main(String[] args) {
        double temperatura = 25.5;

        // 1. Controllo IF-ELSE
        if (temperatura < 10) {
            System.out.println("Clima Rigido");
        } else if (temperatura <= 25) {
            System.out.println("Clima Temperato");
        } else {
            System.out.println("Clima Caldo");
        }

        // 2. Costrutto SWITCH con Enum
        Stagione attuale = Stagione.ESTATE;
        switch (attuale) {
            case ESTATE:
                System.out.println("Tempo di vacanze!");
                break;
            case INVERNO:
                System.out.println("Tempo di sciare!");
                break;
            default:
                System.out.println("Goditi il paesaggio.");
                break;
        }
    }
}
```

---

## 3. I Cicli (Iterazioni)

### Teoria Fondamentale: Cicli Definiti e Indefiniti
- **`for`**: Ideale quando conosciamo a priori il numero di iterazioni.
- **`while`**: Ideale quando il ciclo continua finché una condizione è vera (es. valore sentinella).
- **`do-while`**: Garantisce almeno un'esecuzione del blocco di codice.

### Esempio: Calcolo del Fattoriale e Inserimento Validato
```java
import java.util.Scanner;

public class Iterazioni {
    public static void main(String[] args) {
        // 1. Ciclo FOR per il Fattoriale
        int n = 5;
        long fattoriale = 1;
        for (int i = 1; i <= n; i++) {
            fattoriale *= i;
        }
        System.out.println("Il fattoriale di " + n + " è: " + fattoriale);

        // 2. Ciclo WHILE per validazione input
        Scanner sc = new Scanner(System.in);
        int scelta;
        
        System.out.println("Scegli un numero tra 1 e 3:");
        scelta = sc.nextInt();
        
        while (scelta < 1 || scelta > 3) {
            System.out.println("Errore! Scegli un numero VALIDO (1-3):");
            scelta = sc.nextInt();
        }
        
        System.out.println("Hai scelto l'opzione: " + scelta);
        sc.close();
    }
}
```

---

## 4. I Packages

### Teoria Fondamentale: Organizzazione in Namespace
I package evitano conflitti di nomi e riflettono la struttura delle cartelle sul disco. La direttiva `package` deve essere la prima riga del file.

### Esempio: Geometria e Applicazione
**File: `it/unime/geo/Rettangolo.java`**
```java
package it.unime.geo;

public class Rettangolo {
    public double calcolaArea(double b, double h) {
        return b * h;
    }
}
```

**File: `it/unime/main/App.java`**
```java
package it.unime.main;
import it.unime.geo.Rettangolo;

public class App {
    public static void main(String[] args) {
        Rettangolo r = new Rettangolo();
        System.out.println("Area: " + r.calcolaArea(5, 10));
    }
}
```

---

## 5. Array Primitivi (Essenziali)

### Teoria Fondamentale: Memoria Contigua e Indici
Un array è un contenitore di dimensione fissa che ospita elementi dello stesso tipo in memoria contigua. L'accesso avviene tramite indice (0-based).

### Esempio: Gestione Inventario
```java
public class Inventario {
    public static void main(String[] args) {
        // Dichiarazione e inizializzazione di un array di interi
        int[] scorte = {150, 20, 45, 12, 80};
        String[] prodotti = {"Bulloni", "Viti", "Chiodi", "Dadi", "Rondelle"};

        System.out.println("Stato Magazzino:");
        for (int i = 0; i < prodotti.length; i++) {
            System.out.println(prodotti[i] + ": " + scorte[i] + " unità");
        }
    }
}
```
