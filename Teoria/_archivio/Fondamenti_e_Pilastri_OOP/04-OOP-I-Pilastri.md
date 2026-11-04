# 04. I Pilastri della Programmazione Orientata agli Oggetti (OOP)

## Il Passaggio dal Procedurale agli Oggetti

Prima dell'avvento della Programmazione Orientata agli Oggetti (OOP), lo sviluppo del software era dominato dal paradigma **Procedurale** (come il linguaggio C). Nel mondo procedurale, dati (variabili) e procedure (funzioni) sono entità separate: i dati fluttuano liberamente e le funzioni vi operano sopra. Questo approccio funziona per piccoli script, ma quando i sistemi crescono fino a milioni di righe di codice, diventa impossibile tracciare chi modifica quale dato, causando bug catastrofici e incomprensibili.

La OOP rivoluziona questo approccio ispirandosi al mondo reale. In natura, non esistono "procedure" fluttuanti: esistono **Oggetti** tangibili. Una macchina (oggetto) possiede dei dati interni come il livello di carburante e lo stato del motore (il suo *Stato*), e possiede dei comportamenti intrinseci per alterare questi dati, come accelerare o frenare (il suo *Comportamento*). 

> **Definizione Accademica (Classe vs Oggetto):**
> La **Classe** è l'astrazione, il progetto ingegneristico. Non esiste fisicamente, ma definisce la struttura formale (campi d'istanza) e le capacità (metodi) che le sue creature avranno.
> L'**Oggetto (o Istanza)** è la concretizzazione di quel progetto. È un'entità fisica creata a runtime nella memoria Heap, dotata di uno stato indipendente dagli altri oggetti creati dalla stessa classe.

## Il Primo Pilastro: L'Incapsulamento (Information Hiding)

Il cardine assoluto della OOP in Java è l'**Incapsulamento**, una tecnica difensiva spesso chiamata *Information Hiding* (occultamento dell'informazione).

In un'architettura software solida, non puoi permettere che il codice esterno possa raggiungere e manipolare direttamente e liberamente le viscere (lo stato) di un tuo oggetto. Se un oggetto `ContoBancario` avesse la variabile `saldo` accessibile a tutti, qualsiasi programmatore maldestro potrebbe scrivere `conto.saldo = -50000;`, portando il sistema in uno stato illegale e inconsistente.

L'Incapsulamento risolve questo problema erigendo un muro attorno ai dati:
1. Si dichiarano le variabili di stato rigorosamente **`private`**.
2. Si fornisce accesso controllato al mondo esterno esponendo solo specifici metodi **`public`** (i famosi *Getter e Setter*).

Questa barriera permette alla classe di mantenere un controllo dittatoriale su chi legge i suoi dati e, soprattutto, di applicare **logica di validazione** prima di permetterne la modifica.

## I Modificatori di Accesso in Java

Per orchestrare questo livello di segretezza e visibilità, Java fornisce quattro modificatori di accesso. La loro scelta non è mai casuale, ma è una decisione architetturale precisa:

| Modificatore | Visibilità | Significato Architetturale |
| --- | --- | --- |
| `private` | Solo all'interno della stessa Classe | **Segreto Industriale.** Il livello di protezione massimo. Quasi tutte le variabili d'istanza devono essere private. Nessuno fuori dalle parentesi graffe della classe può vederle o toccarle. |
| `(default)` | Classe e intero Package | **Segreto di Reparto.** Se non scrivi alcun modificatore, la variabile è visibile a tutte le altre classi che risiedono nella stessa cartella (package). Usato raramente in design rigorosi. |
| `protected` | Classe, Package e Sottoclassi | **Eredità Familiare.** Visibile nel package, ma soprattutto accessibile a tutte le *classi figlie* (anche se si trovano in altri package). Strumento cardine per l'ereditarietà. |
| `public` | Ovunque (Mondo intero) | **Dominio Pubblico.** Nessuna restrizione. Si usa quasi esclusivamente per i metodi che costituiscono l'API (Application Programming Interface) della classe, ovvero i bottoni che il mondo esterno può premere per interagire con l'oggetto. |

## Il Contratto API: Getter e Setter

I metodi Getter e Setter non sono un capriccio stilistico, ma stabiliscono un **contratto** tra la classe e chi la utilizza.

```java
public class Termostato {
    
    // 1. Information Hiding: La temperatura è inaccessibile dall'esterno
    private double temperatura;
    
    // 2. Il Getter permette al mondo di 'leggere' lo stato, senza poterlo alterare
    public double getTemperatura() {
        return this.temperatura;
    }
    
    // 3. Il Setter è l'unico portale per modificare lo stato.
    // Essendo un metodo, funge da dogana: ispeziona e valida il dato in ingresso.
    public void setTemperatura(double nuovaTemperatura) {
        
        // Logica di validazione: impedisce stati fisicamente impossibili
        if (nuovaTemperatura < -273.15) {
            System.out.println("Errore Termodinamico: Zero Assoluto violato!");
            // In un contesto reale, qui lanceremmo un'eccezione
            this.temperatura = -273.15; 
        } else {
            // Assegnazione consentita
            this.temperatura = nuovaTemperatura;
        }
    }
}
```

In sintesi, l'Incapsulamento garantisce l'**integrità dello stato**. Assicura che un oggetto sia sempre in una condizione logica corretta per tutta la sua vita, rendendo il software prevedibile, sicuro e, soprattutto, a prova di manutenzione. Se in futuro la regola dello "zero assoluto" cambiasse, modificheresti solo il setter nella classe `Termostato`, e tutto il software che usa il termostato beneficerebbe automaticamente del fix, incarnando la potenza del paradigma OOP.