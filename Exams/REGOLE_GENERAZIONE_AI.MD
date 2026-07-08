## 🤖 REGOLE DI GENERAZIONE PER L'AI (MOCK EXAMS)
*Questa sezione serve come direttiva rigorosa per l'AI nella generazione di futuri esami.*

1. **Struttura Punteggi, Difficoltà e Argomenti:**
   - **Esercizio 1 (5 Punti):** Riscaldamento. Si può testare l'algoritmica di base, la matematica o la logica semplice (if/else, array). Tuttavia, è possibile (e consigliato) esplorare anche la progettazione OOP elementare/principiante: ad esempio, chiedere di realizzare semplici classi che implementino un'interfaccia o estendano una classe astratta compiendo operazioni molto basilari.
   - **Esercizio 2 (13 Punti):** Core Java e API built-in. L'obiettivo è testare concetti avanzati o intermedi della libreria standard. Oltre a Eccezioni e File I/O, estendere lo spettro ad altri argomenti chiavi: **Networking (Socket, ServerSocket)**, API per parsare file **XML**, connessioni a DB con **JDBC**, o utilizzi avanzati delle **Collections**. L'AI deve argomentare bene i test e variare queste tematiche.
   - **Esercizio 3 (13 Punti):** Thread e Concorrenza. **ATTENZIONE:** Non sempre riguarda la mutua esclusione (Wait/Notify o risorse condivise). Spesso si richiede semplicemente di implementare la logica base di un Thread (estendere `Thread` o implementare `Runnable`), applicare l'Information Hiding (get/set), polimorfismo e overriding di `run()`. Variare le simulazioni tra problemi di sincronizzazione e problemi di ereditarietà/Thread di base.
   
2. **Stile della Traccia (Povera e senza aiuti):** Formale, accademico ed estremamente scarno.
   - **NESSUN SUGGERIMENTO SINTATTICO:** Mai fornire firme complete di metodi contenenti keyword risolutive (come `synchronized`, `throws`, `extends`, ecc.).
   - Quando si descrive un metodo da implementare, limitarsi al nome (CaseSensitive) e al tipo di ritorno (es. int, String o void). Ad esempio: dire "creare un metodo entra che non ritorna nulla", e NON "creare un metodo public synchronized void entra()".
   - **NESSUN AIUTO LOGICO (NO REMINDER):** Anche se lo studente continua a sbagliare determinati concetti tra una simulazione e l'altra, la traccia NON deve mai contenere suggerimenti del tipo "Ricordati di fare questo..." o "Attento a...". Lo studente deve capirlo e arrivarci totalmente da solo.
   
3. **Ambiente di Sviluppo (IDE Moodle2):**
   - L'esame si svolge in un singolo file per esercizio (`Soluzione.java`). 
   - I file dello studente non devono contenere classi pre-impostate, firme di metodi o `TODO`. Tuttavia, l'AI **deve pre-inserire gli `import` necessari** in cima al file `Soluzione.java` (es. `import java.net.*;`, `import java.io.*;`, ecc.), per agevolare lo studente nel ricordare i package corretti.
   - Nell'esercizio 3, nel caso di code condivise, i Worker pre-forniti vanno lasciati nello stesso file ma in sola lettura, e lo studente deduce le firme da solo.
   
4. **Test "Black Box" (Invisibili):** 
   - Il `Main.java` con i test deve essere pre-compilato in `.class` e il suo file sorgente `.java` **eliminato definitivamente**. Lo studente avrà solo `Soluzione.java` per scrivere, ed eseguirà `java Main` per avviare il tester invisibile compilato dall'AI.
   
5. **Varietà e Imprevedibilità delle Tracce:** 
   - L'AI deve scansionare lo storico delle simulazioni passate e assicurarsi di generare sfide **sempre nuove per TUTTI E 3 gli esercizi**. Evitare assolutamente la ripetitività:
     * Nell'ES1, se prima c'era una classe astratta, ora proporre manipolazione di array o stringhe.
     * Nell'ES2, se prima c'era l'I/O, ora proporre Networking, XML o Database.
     * Nell'ES3, se prima c'era Mutua Esclusione, ora proporre Ereditarietà e Information Hiding sui Thread.
   - Ogni singola traccia deve garantire che lo studente esca dalla propria "comfort zone".

6. **Ispirazione dalle Esercitazioni (Self):**
   - L'AI è autorizzata e caldamente invitata, prima di generare una nuova simulazione, a spulciare la directory `Esercitazioni (Self)` (e il relativo `SYLLABUS.MD`) per vedere esattamente quali concetti pratici ha affrontato lo studente nei 7 livelli di apprendimento. 
   - Questo permette di trarre ispirazione da esercizi reali fatti in passato per inventare tracce sempre originali, pertinenti e tarate sul programma effettivo.

7. **Tempistiche:** 30 minuti totali per l'intero esame, gestibili liberamente.

8. **Fase di Supervisione in Aula (Q&A Pre-Consegna):**
   - Durante lo svolgimento della simulazione (prima della richiesta formale di correzione), l'AI deve immedesimarsi nel ruolo di un professore che sorveglia l'aula.
   - Lo studente può porre domande in caso di dubbi sulla traccia o blocchi logici. L'AI risponderà accogliendo i dubbi, ma **non fornirà MAI soluzioni esplicite, aiuti diretti o suggerimenti palesi**. Le risposte devono stimolare il ragionamento senza regalare la soluzione (nessun "suggerimento velato" troppo ovvio).
