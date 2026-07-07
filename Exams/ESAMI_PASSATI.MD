## Dettagli e Regole Appelli
* **Tempo a disposizione:** 30 minuti totali per 3 esercizi.
* **Uso del Compilatore (IDE):** Massimo 5 esecuzioni "pulite" per esercizio. Superata questa soglia, ogni esecuzione aggiuntiva causa penalità sul punteggio.
* **Punteggio Totale:** 31 punti (5 + 13 + 13).

# 📝 TRACCIA ESAME 1

### Esercizio 1 (5 Punti) - OOP Base (Classi Astratte e Polimorfismo)
Creare una classe astratta `Animale` e definire un metodo astratto `String verso()`. Definire due sottoclassi `Cane` e `Gatto` che implementano il metodo e ritornano rispettivamente "bau" e "miao".

### Esercizio 2 (13 Punti) - Gestione Avanzata Eccezioni (Le 5 Keywords)
Definire un metodo che accetta un parametro `int` e gestire i seguenti casi:
* Se `0`: lanciare una `Exception` generica e stampare "eccezione generica".
* Se `1`: lanciare una `IOException`, catturarla, rilanciare una `RuntimeException` e stampare "eccezione runtime".
* Se `2`: stampare "no eccezioni".
* **Vincolo Architetturale:** Si devono obbligatoriamente utilizzare **tutte e 5 le parole chiave** della gestione delle eccezioni (`try`, `catch`, `finally`, `throw`, `throws`).

### Esercizio 3 (13 Punti) - Ereditarietà, Thread e Information Hiding
Data una classe `Persona` con costruttore `(String nome, String cognome)`:
1. Definire una sottoclasse `Studente` che implementa l'interfaccia `Runnable`.
2. Definire in `Studente` due costruttori in overload:
   * Il primo accetta: `nome`, `cognome`, `matricola` (int).
   * Il secondo accetta: `matricola` (int), `cds` (String). 
3. Fare l'override del metodo `run()`: dovrà elevare la `matricola` al quadrato e sovrascriverne il valore.
4. **Vincolo Architetturale:** Usare rigorosamente l'Information Hiding (tutte le variabili d'istanza devono essere `private` e bisogna definire i relativi metodi `get` e `set`).

---

### Analisi del Livello di Difficoltà
**Difficoltà Stimata:** Alta 🔴
* **Motivazione:** Non per la complessità logica (le operazioni richieste sono basilari), ma per l'estrema **pressione del tempo** (30 minuti per 3 esercizi significa circa 10 minuti a esercizio) unita alla **penalità sul compilatore**. Richiede di scrivere codice a mente, pulito e sintatticamente corretto "alla prima stesura", padroneggiando a memoria i costrutti chiave (abstract, keyword eccezioni, ereditarietà con super(), e Runnable).

# 📝 TRACCIA ESAME 2

### Esercizio 1 (5 Punti) - Logica di Base
Implementare un metodo statico con la seguente firma: `public static int converti(int km)`. Il metodo deve ricevere in input un valore espresso in chilometri (km) e restituire il suo equivalente convertito in metri.

### Esercizio 2 (13 Punti) - Networking (Socket)
Definire una classe `Client`. Essendo noti a priori un indirizzo IP (es. "127.0.0.1") e un numero di porta, instaurare una connessione di rete verso il server in ascolto su tali coordinate e trasmettere al destinatario un messaggio testuale arbitrario. Non sono richiesti costrutti per la ricezione della risposta.

### Esercizio 3 (13 Punti) - Concorrenza e Sincronizzazione (Wait/Notify)
All'interno del workspace sono già fornite le classi `Produttore` e `Consumatore`, completamente implementate. Tali classi sono progettate per interagire concorrentemente con una risorsa condivisa.

Si richiede allo studente di implementare ex-novo la classe `Buffer` (attualmente vuota), col fine di risolvere il problema della concorrenza garantendo la mutua esclusione e la corretta sincronizzazione dei thread. La classe `Buffer` deve obbligatoriamente soddisfare i seguenti requisiti:
1. Contenere una struttura dati basata su un array primitivo con dimensione massima pari a 3.
2. Definire un metodo che restituisca sotto forma di intero il numero di elementi attualmente presenti nel buffer.
3. Definire un metodo per l'inserimento di un elemento nel buffer.
4. Definire un metodo per l'estrazione e rimozione di un elemento dal buffer.

*(Nota: Le firme esatte dei metodi per la classe `Buffer` devono essere dedotte dallo studente analizzando le invocazioni presenti nel codice fornito delle classi Produttore e Consumatore).*

---

## 🤖 REGOLE DI GENERAZIONE PER L'AI (MOCK EXAMS)
*Questa sezione serve come direttiva rigorosa per l'AI nella generazione di futuri esami.*

1. **Struttura Punteggi e Difficoltà:**
   - **Esercizio 1 (5 Punti):** Riscaldamento. Algoritmica di base, matematica, o logica semplice (if/else, array, OOP molto basilare).
   - **Esercizio 2 (13 Punti):** Core Java. Implementazione di un concetto avanzato (Eccezioni, Networking, File I/O, Collezioni).
   - **Esercizio 3 (13 Punti):** Boss Finale (Thread/Concorrenza). Spesso richiede di sincronizzare l'accesso a risorse condivise (Wait/Notify, Lock).
2. **Stile della Traccia:** Formale, crudo, accademico. **Nessun aiuto o suggerimento** sui costrutti da utilizzare (es. non dire "usa la keyword synchronized", di' "garantire la mutua esclusione").
3. **Ambiente di Sviluppo (IDE Moodle2):**
   - L'esame si svolge in un singolo file per esercizio (`Soluzione.java`).
   - Nell'esercizio 3 (Thread), il codice per i Worker (es. Produttore/Consumatore) è spesso pre-fornito dal docente in sola lettura, e lo studente deve scrivere solo la classe condivisa (es. Buffer), deducendo firme e metodi dal codice dei worker.
4. **Test "Black Box" (Invisibili):** Il `Main.java` con i test deve essere pre-compilato in `.class` e il suo file sorgente `.java` eliminato. Lo studente avrà solo `Soluzione.java` per scrivere, ed eseguirà `java Main` per avviare il tester invisibile compilato dall'AI.
5. **Tempistiche:** 30 minuti totali per l'intero esame, gestibili liberamente.
