# 03. Flussi di Esecuzione, Strutture di Controllo e Scope

## L'Architettura del Controllo di Flusso

Per default, la Java Virtual Machine esegue le istruzioni all'interno di un metodo seguendo un rigido ordine sequenziale top-down: dalla prima riga verso l'ultima. Tuttavia, la capacità decisionale di un software (l'intelligenza algoritmica) nasce dalla possibilità di alterare dinamicamente questo scorrere del tempo in base a valutazioni logiche o al presentarsi di specifiche condizioni ambientali. 

Queste "deviazioni" del flusso sequenziale si governano tramite le **Strutture di Controllo**, che si dividono classicamente in due famiglie: Costrutti Condizionali (ramificazioni) e Costrutti Iterativi (cicli).

## Costrutti Condizionali: Prendere Decisioni

### Il costrutto `if - else if - else`
È il fondamento della logica booleana. Valuta un'espressione logica incapsulata tra parentesi tonde e, se e solo se questa espressione risulta `true` (vera), esegue il blocco di codice successivo. La sua forza risiede nell'esclusione reciproca: solo un ramo del costrutto verrà eseguito, scartando i restanti.

```java
int votoEsame = 28;

if (votoEsame >= 18) {
    // Questo blocco viene eseguito se la condizione è vera.
    System.out.println("Esame superato con successo!");
    
    if (votoEsame == 30) {
        // Ramificazione annidata (nested) per affinare la logica
        System.out.println("Lode accademica meritata.");
    }
} else {
    // Il ramo 'else' funge da "catch-all" (rete di salvataggio).
    // Si attiva solo se tutte le precedenti condizioni erano false.
    System.out.println("Bocciato. Ritenta al prossimo appello.");
}
```

### Il costrutto `switch` e il rischio di Fall-Through
Quando le scelte non si basano su "range" di valori (come maggiore o minore), ma sull'uguaglianza rigorosa e predefinita di una singola variabile (ad esempio un menù di scelta), l'uso di una cascata di `if-else` risulta prolisso, difficile da leggere e computazionalmente non ottimizzato. 

Lo `switch` risolve questo problema. Sotto il cofano, il compilatore Java trasforma lo `switch` in una *Jump Table* (Tabella dei Salti), permettendo alla JVM di calcolare e saltare direttamente al blocco di codice corretto senza dover valutare sequenzialmente tutte le alternative precedenti (rendendolo, in teoria, un'operazione dal tempo costante O(1)).

> **Nota del Docente (Sindrome da Fall-Through):**
> A differenza di molti linguaggi moderni, in Java i rami `case` dello `switch` non si "fermano" da soli. Una volta che la JVM trova il `case` corrispondente, inizia a eseguire il codice ma **continua a precipitare in basso** eseguendo anche il codice dei `case` sottostanti, ignorando le loro "etichette". Questo comportamento anomalo si chiama *Fall-Through*. Per arginarlo, il programmatore deve inserire volontariamente l'istruzione `break;` per forzare l'uscita anticipata.

## Costrutti Iterativi: Il Potere della Ripetizione

Le macchine trionfano dove l'uomo cede alla fatica: l'esecuzione ripetitiva e ciclica. In base alla tipologia di informazione nota prima dell'avvio del ciclo, si sceglie il costrutto più appropriato.

### Il Ciclo `for` (Iterazione Definita)
Ideale, e quasi obbligatorio, quando il numero esatto di iterazioni è stabilito a monte o quando si deve scorrere longitudinalmente un array o una lista. Concentra in una sola riga tutta l'impalcatura amministrativa: Inizializzazione, Condizione di Uscita e Aggiornamento della variabile di controllo.

```java
// Struttura: for(inizializzazione; condizione; step di aggiornamento)
for (int i = 0; i < 5; i++) {
    System.out.println("Iterazione numero: " + i);
}
// NOTA BENE: Sebbene si contino 5 iterazioni, l'output sarà 0, 1, 2, 3, 4. 
// L'informatica è "Zero-Indexed" (inizia da zero).
```

### I Cicli `while` e `do-while` (Iterazione Indefinita)
Strumenti d'elezione quando la fine del ciclo non dipende da un contatore, ma dal verificarsi di un evento asincrono (es. la pressione di un tasto da parte dell'utente, l'arrivo della fine di un file, o la generazione di un numero casuale).

La netta e insormontabile differenza tra i due risiede nel momento in cui viene posta la domanda (la valutazione della condizione):
- Il **`while`** esegue il test **in testa** (pre-condizione). Potrebbe tranquillamente non eseguire MAI il suo blocco di codice se la condizione è falsa fin dall'inizio.
- Il **`do-while`** esegue il test **in coda** (post-condizione). Ha una garanzia fondamentale: *il blocco di codice verrà eseguito ALMENO una volta*, a prescindere dal valore della condizione.

## Teoria dello Scope (La Visibilità delle Variabili)

Una variabile non vive per sempre, e non è accessibile ovunque. Lo **Scope (Ambito di Visibilità)** definisce lo spazio semantico all'interno del quale una variabile esiste ed è raggiungibile dal codice. 

In Java, la regola aurea dello Scope si poggia sulle **parentesi graffe `{ }`**. 

> **Regola Aurea dello Scope:**
> Una variabile è visibile dal momento esatto in cui viene dichiarata, fino alla parentesi graffa di chiusura del blocco (`}`) in cui la dichiarazione è avvenuta. Una volta raggiunta quella parentesi, la variabile viene distrutta (poiché il relativo Stack Frame si svuota) e smette di esistere.

```java
public class TeoriaScope {
    public static void main(String[] args) {
        
        int contatoreEsterno = 100; // Vive per tutta la durata del metodo main
        
        for (int i = 0; i < 3; i++) {
            // La variabile 'i' nasce qui e muore ad ogni chiusura di ciclo
            // Posso leggere variabili esterne (Scope gerarchico esterno-interno)
            int risultato = contatoreEsterno + i; 
            System.out.println(risultato);
        } // Qui muoiono 'i' e 'risultato'
        
        // ERRORE ACCADEMICO FATALE:
        // Il compilatore rifiuterà categoricamente il codice seguente, 
        // poiché 'i' non esiste più nello Stack Memory.
        // System.out.println("L'ultimo valore di i è: " + i);
    }
}
```

Questa rigidità dello Scope non è una limitazione, ma una prassi difensiva vitale. Evita che i programmatori "inquinino" lo spazio dei nomi globale (Namespace Pollution), riduce l'occupazione della memoria liberando le variabili appena non servono più e impedisce interferenze involontarie tra porzioni di codice disconnesse.