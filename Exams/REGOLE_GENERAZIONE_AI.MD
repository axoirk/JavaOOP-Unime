## 🤖 REGOLE DI GENERAZIONE PER L'AI (MOCK EXAMS) — v2

*Direttiva pubblica e rigorosa per permettere a qualsiasi AI di generare simulazioni d'esame Java OOP strutturate, standardizzate e fedeli alle condizioni reali dell'appello.*

> **Principio guida:** una simulazione ha valore solo se riproduce i **vincoli** dell'appello, non solo i suoi argomenti. Un esercizio giusto svolto in condizioni comode non misura nulla.

---

### 0. Ambiente di Svolgimento (Fedeltà alle Condizioni Reali)

L'appello si svolge dentro una pagina **Moodle**, in un'area di scrittura di livello "blocco note": nessun controllo di sintassi, nessun completamento automatico, nessuna segnalazione di errore mentre si scrive. È presente un pulsante **Esegui** che compila il codice e lo confronta con un test **non visibile** allo studente.

La simulazione deve replicare queste condizioni:

- **Un solo file per esercizio.** Tutte le classi richieste vanno dichiarate nello stesso file `Soluzione.java`. Non è ammessa la suddivisione in più file.
- **Editor cieco.** Lo studente scrive in un editor di testo semplice, privo di analisi del codice: l'editor di riferimento è quello nella pagina di `Exams/aula.py`, accanto alla traccia: colorazione della sintassi, numeri di riga, chiusura automatica delle parentesi e rientro automatico a capo, ma nessun controllo e nessun suggerimento. **Differenza nota rispetto a Moodle:** l'appello reale è un blocco note senza completamento; le parentesi e il rientro automatici di `aula.py` rendono meno probabile una graffa dimenticata, quindi quell'errore può sottostimare la sua frequenza reale. **Altra differenza nota:** il tester può segnalare un vincolo architetturale esplicito violato (§4), un segnale che a Moodle potrebbe non esserci: la rubrica (§7) resta quella che pesa la struttura. Per il singolo esercizio con `esegui.sh` sono ammessi `nano` e TextEdit in modalità testo semplice. L'uso di un IDE con analisi statica (IntelliJ, VS Code con estensioni Java, Eclipse) durante la prova **invalida la simulazione**.
- **Esecuzione contingentata.** L'esecuzione avviene solo tramite `Exams/aula.py` (aula d'esame in browser: tracce, cronometro, Esegui, consegna) oppure, per il singolo esercizio, tramite `Exams/esegui.sh`. Entrambi replicano il pulsante Esegui e contano i tentativi sullo stesso file `.esecuzioni`.
- **Riquadro dei test.** Dopo un Esegui lo studente vede il verdetto, l'elenco delle verifiche con il loro esito e, su quelle fallite, il valore atteso e quello prodotto — come il riquadro dei test di Moodle. Gli errori del compilatore sono mostrati integralmente. *(Confermato dall'utente il 12/11/2026: a Moodle lo studente vede davvero l'elenco dei test con esito e confronto.)*
- **Limite di 5 esecuzioni per esercizio.** Oltre la quinta, ogni esecuzione produce una penalità sul punteggio. Un errore di compilazione consuma un'esecuzione esattamente come un'esecuzione riuscita. Il tetto è per esercizio e non si travasa: l'ora complessiva è gestibile liberamente, le esecuzioni no.

### 0.1 Inizializzazione Ambiente (Preparazione Cartelle)

- Le simulazioni vivono in `Exams/Simulazioni/`: `Prove/` contiene la serie attiva, `Archivio/` le serie chiuse, una cartella ciascuna (`Serie_1/`, `Serie_2/`, …; non si alimentano più). Quando una serie si chiude, le sue `SIM_N` passano in `Archivio/Serie_<n+1>/` e la nuova riparte da `SIM_1`. Se `Prove/` non esiste, **va creata** (es. `mkdir -p "Exams/Simulazioni/Prove/SIM_X/ES1"`).
- Ogni simulazione risiede in una sottocartella numerata progressivamente dentro la serie (`SIM_1`, `SIM_2`, …) contenente `ES1`, `ES2`, `ES3`. La struttura degli argomenti e la scala di difficoltà sono in `Exams/Simulazioni/GUIDA_PUBBLICA.md`.
- In ogni cartella esercizio l'AI deposita: `README.md` (traccia), `Soluzione.java` (con i soli `import`, o in Variante B anche le classi fornite), `Main.class` (tester compilato). Il titolo del README dichiara i punti (`# Esercizio 2 (13 Punti) — ...`): `aula.py` li legge da lì.
- **Ordine in aula.** I ruoli restano fissi (ES1 5 punti, ES2 e ES3 13), ma l'ordine in cui compaiono è variabile, come agli appelli (EXAM1-3: il 5 per primo; EXAM4: per ultimo). Il file facoltativo `ordine.txt` nella cartella della prova (es. `ES2 ES3 ES1`) dice a `aula.py` l'ordine delle schede; senza file, o se non è valido, l'ordine è `ES1 ES2 ES3` (così erano tutte le prove fino a S3/SIM_13). È valida qualunque permutazione. Il generatore mette l'esercizio da 5 punti per ultimo quando non lo è stato in nessuna delle tre prove precedenti (circa una su quattro), mai in due di fila, e annota ordine e riciclo nella riga del registro della `GUIDA.md` locale (testo libero). Le schede di `aula.py` mostrano il nome della cartella (ES1, ES2, ES3): il numero nel titolo del README è il ruolo, non la posizione, e il file di consegna riporta l'ordine usato.

---

### 1. Struttura Punteggi, Difficoltà e Argomenti

Totale **31 punti**, **45 minuti** complessivi per i tre esercizi. Il tempo è gestibile liberamente: lo studente può passare da un esercizio all'altro quando vuole.

- **Esercizio 1 (5 punti) — Riscaldamento.** Due nature, da alternare. *Problem solving:* un metodo **statico** che risolve un calcolo matematico o un problema di logica generale — conversioni, cifre di un numero, manipolazione di array e stringhe, nei limiti del tetto di logica qui sotto (all'appello EXAM2 era `public static int converti(int km)`). *Progettazione OOP elementare:* classi che implementano un'interfaccia o estendono una classe astratta, con information hiding.
- **Esercizio 2 (13 punti) — Core Java e API built-in.** File I/O (testo, binario, serializzazione), Networking (`Socket`, `ServerSocket`), parsing XML, JDBC, uso avanzato di Collections e `Comparable`. Variare costantemente.
- **Esercizio 3 (13 punti) — L'esercizio difficile.** **Non è per forza sui thread.** Agli appelli sostenuti era serializzazione di oggetti su socket (luglio); a settembre nessuno dei tre esercizi era sui thread. *Per scelta di progetto*, ai Livelli 1-3 l'ES3 resta sui thread e sulla concorrenza (con le classi annidate da 13 punti dal Livello 3): rete e serializzazione da 13 punti compaiono nei livelli alti, e in forma elementare in ES2 (§6). Il terzo esercizio è quello complesso da 13 punti, e attinge a: thread e concorrenza (`Thread`/`Runnable`, `synchronized`, `wait`/`notifyAll`, `join()`, Produttore/Consumatore, information hiding su risorsa condivisa), oppure serializzazione, oppure networking, **spesso in combinazione tra loro**.

> **Livello di difficoltà.** Ogni simulazione ha un livello da 1 a 5, scelto per la singola prova (§12). La struttura sopra non cambia: cambia la complessità di ciò che si chiede.

> **Regola di composizione (dal Livello 4, come in §12).** Gli argomenti si presentano combinati, non isolati. Dal Livello 4, almeno una traccia ES3 su tre deve richiedere di comporre due aree distinte (es. serializzazione *attraverso* un socket, thread che scrivono *su file*, `Comparable` applicato a oggetti letti *da XML*). Saper fare le due cose separatamente non basta: è esattamente il punto in cui l'appello reale è stato perso.

> **Tetto di logica (Livelli 1 e 2, ES1 ed ES2; ES3 invariato).** La simulazione serve a conoscere la sintassi, il codice e le classi che possono uscire all'esame, non a risolvere algoritmi. Le tracce vere di ES1 sono state `converti(km)`, un'interfaccia e una classe astratta: nessuna logica lunga. La difficoltà sta nella *struttura richiesta* e nell'API, non nell'algoritmo.
> - **ES1, problem solving.** Un metodo (al massimo due, indipendenti) la cui logica è una formula o una conversione diretta, oppure **un solo ciclo semplice** con al più un `if` (somma, massimo, conteggio, una trasformazione su una stringa o su un array, la somma delle cifre di un numero). **Vietati:** cicli annidati, ricorsione, due fasi in cascata (il risultato di un ciclo che alimenta un secondo ciclo, come la radice digitale), proprietà da scoprire con un ragionamento matematico, più casi limite non mostrati dall'esempio. Controllo prima di consegnare: la soluzione di riferimento di ogni metodo sta in una decina di righe e si scrive senza pensare a un algoritmo.
> - **ES2.** Il formato dei dati ha un solo separatore e al più una trasformazione per campo; niente parsing a più rami. I casi limite del tester sono soltanto quelli che la traccia o l'esempio permettono di dedurre (§2). Il peso dell'esercizio sta nei vincoli architetturali (eccezioni, `finally`, flussi, firme dedotte), non nella logica interna.
> - **ES1, progettazione OOP.** Il tetto vale anche qui: ogni metodo contiene una formula o un solo ciclo semplice con al più un `if` (una media, un massimo, un confronto). La difficoltà sta nelle classi, nei costruttori, nell'information hiding, non nel calcolo dentro i metodi; niente casi limite non mostrati dall'esempio (parità, insieme vuoto) a meno che la traccia li dica.
> - Ricorsione, cicli annidati e algoritmi a più fasi si riservano ai Livelli 3 e superiori, nella sola forma di ES1 che li ammette (guida §2). **Tutti e tre gli esercizi, riciclo compreso, rispettano il tetto e il livello della prova.**

> **Varietà di classi e API (Livelli 1 e 2, ES1 ed ES2).** Visto che la logica resta semplice, a variare tra una prova e l'altra sono le **classi e i metodi della libreria** che la traccia fa usare, ognuno in una forma elementare: `String` (`charAt`, `substring`, `indexOf`, `split`, `trim`, `equals`, `compareTo`), `Math`, classi wrapper (`Integer.parseInt`, `Character`), `StringBuilder`, array e `Arrays`, `ArrayList`, `Scanner`, `File`, flussi di testo e binari. Le API usate si annotano nella nota della prova nello storico (§5, terreno nuovo per primo): una prova non ripete la stessa famiglia di API della precedente. In Variante B contano di più la sintassi e le firme: più classi fornite da leggere, costruttori, `static`, tipi di ritorno, `import`, da dedurre dalle invocazioni.

---

### 2. Stile della Traccia (Scarna, ma con l'Output Atteso)

La traccia risiede in `README.md` e imita il registro delle tracce d'appello: **italiano piano e diretto**, frasi brevi, terminologia standard chiamata con il suo nome — *serializzabile*, `serialVersionUID`, *thread*, *mutua esclusione*, *array*, `ArrayList`. Asciutta, non contorta: le perifrasi che evitano di nominare le cose («convertibile in una sequenza di byte», «flusso di esecuzione indipendente», «intero a 64 bit») rendono la traccia più difficile del vero e vanno evitate.

Il confine è netto: **si nominano i concetti e i vincoli, non si regalano le soluzioni**. «Garantendo la mutua esclusione» è il linguaggio dell'appello reale ed è ammesso; `public synchronized void deposita(int importo)` no.

**Vincolo contro soluzione.** Le tracce vere nominano le parole che sono il *vincolo* del compito: la firma completa del metodo statico di ES1 (`public static int converti(int km)`, EXAM2), «tutte e cinque le parole chiave (`try`, `catch`, `finally`, `throw`, `throws`)», «classe astratta», «classe annidata non statica», `Runnable`, `serialVersionUID`. Questo è ammesso. Resta vietata la parola che è la *soluzione* di un punto: `synchronized` sul metodo, `throws` o `extends` su una firma che lo studente deve dedurre, e `static` su un campo o metodo che la traccia non fissa già. La differenza: se la parola è il requisito esplicito dell'esercizio la si scrive, se è il modo di soddisfarlo la si lascia trovare. Un buon riferimento è `Exams/ESAMI_PASSATI.MD`: le tracce vere si leggono al primo colpo.

**Scheletro del README (come EXAM3 ed EXAM4).** Titolo con i punti (`# Esercizio N (X Punti) — Titolo`), l'enunciato, i requisiti in elenco numerato, il blocco `## Output atteso`. **Niente sezioni «Descrizione» né «Obiettivo didattico»**: l'appello non le ha, e l'obiettivo didattico nomina il concetto da applicare, cioè il suggerimento che §2 vieta. In Variante B è ammessa la nota sulle firme da dedurre. Ciò che il codice fornito fissa già (una chiamata `Biglietto.emessi()` mostra che il metodo è `static`) non si ripete in traccia.

**Cosa la traccia DEVE contenere:**
- Nomi di classi e metodi richiesti, **case-sensitive**, e i tipi di ritorno.
- I **vincoli architetturali** espliciti (es. "usare tutte e cinque le parole chiave della gestione delle eccezioni", "tutte le variabili d'istanza devono essere private").
- L'**output atteso**, in un blocco ```text. All'appello reale lo studente conosce l'output che il test invisibile pretende: ometterlo renderebbe la simulazione più difficile del vero, non più fedele.
- **La formula matematica, negli ES1 di problem solving il cui calcolo è una formula specifica o complessa** (distanza tra due punti, indice di massa corporea, interesse composto, area di un triangolo con tre lati, e simili: espressioni che si conoscono solo se le si è studiate, con radici, potenze, costanti o più termini). Va riportata nella traccia, accanto al requisito del metodo, **in notazione matematica e non in codice**: testo semplice con simboli (`d = √((x₂ − x₁)² + (y₂ − y₁)²)`, `|a − b|`), una riga per formula, con gli stessi nomi dei parametri della traccia. Serve a togliere dalla prova la memoria della formula, che non è ciò che l'esercizio misura: resta allo studente tradurla in Java, con i tipi, l'ordine dei parametri e le API giuste. **Non si riporta** per le operazioni elementari: conversione di unità (km → m), somma, differenza, prodotto, quoziente e resto, media aritmetica, percentuale semplice, area di rettangolo o quadrato. Non si riporta nemmeno nessuna riga di codice (`Math.sqrt`, `*`, `/`, un cast), nessun promemoria su come tradurla («attenzione alla divisione intera») e nessuna formula per gli esercizi che non calcolano una grandezza (conteggi su stringhe e array, cifre di un numero, scansioni). Il km → m riciclato da un appello resta quindi identico all'originale (§5.1). Il discrimine è uno: se lo studente può scrivere il calcolo leggendo soltanto la traccia, la formula non serve.

**Cosa la traccia NON deve MAI contenere:**
- **Le regole d'appello.** Niente intestazioni con durata, numero di esecuzioni o «tutte le classi nello stesso file»: sono condizioni note e già ricordate dall'aula. La traccia contiene l'esercizio, punto.
- **Nessun suggerimento sintattico.** Mai firme che contengano keyword risolutive (`synchronized`, `throws`, `extends`, `implements`) né `static` su ciò che la traccia non fissa. Si danno nome e tipo di ritorno; la firma completa è ammessa solo per il metodo statico di ES1 e solo se coincide con il vincolo dell'esercizio (vedi *Vincolo contro soluzione*).
- **Nessun aiuto logico, nessun promemoria.** (La formula matematica del problema, descritta sopra, è il dato dell'esercizio e non un aiuto: fa eccezione.) Anche se lo studente ha sbagliato ripetutamente lo stesso concetto nelle simulazioni precedenti, la traccia non contiene mai formule del tipo "ricordati di…", "attenzione a…". Lo studente deve arrivarci da solo.
- **Nessun riferimento alla pesatura del §6.** Lo studente non deve sapere che una certa area viene proposta più spesso.
- **Nessun obbligo di usare ciò che non sta nel materiale del docente.** Una traccia non può richiedere, esplicitamente o in pratica (un requisito che si soddisfa solo con quel metodo), una classe, un metodo o una tecnica che il materiale del corso (`java_lessons/`, riportato in `Teoria/`) non mostra. Gli approfondimenti marcati «fuori programma» in `Teoria/` sono esclusi per definizione. Prima di fissare un tema si cerca la parola risolutiva nel materiale; se manca, si cambia tema. Caso reale: SIM_22 ES3 richiedeva di fermare un thread senza attendere il periodo, cioè `Thread.interrupt()`, che le dispense non contengono; i punti sono stati restituiti.

---

### 3. Varianti di Traccia

Il docente utilizza entrambe le modalità seguenti. L'AI ne sceglie una a ogni generazione, in base a quale delle due ha esercitato di meno di recente — non secondo una rotazione fissa:

- **Variante A — Foglio bianco.** `Soluzione.java` contiene solo gli `import` pre-inseriti dall'AI. Lo studente scrive tutto.
- **Variante B — Classi parziali fornite.** `Soluzione.java` contiene una o più classi **già completamente implementate**, e lo studente deve realizzare la classe mancante **deducendone le firme dalle invocazioni presenti nel codice fornito**. La traccia descrive i requisiti della classe mancante ma non ne espone i metodi.

In entrambe le varianti: nessuna firma scheletro, nessun `TODO`. **Eccezione, come in EXAM2 ES3:** in Variante B può esserci la sola classe da scrivere preimpostata e vuota (`class Buffer { }`), quando la traccia dice che è vuota; resta vietato ogni scheletro di metodi. Negli starter sono ammessi solo commenti di collocazione che non nominano classi, metodi o keyword da scrivere (es. `// codice fornito`). **Classificazione:** è Variante B solo se il codice fornito *invoca* la classe da scrivere (le firme si deducono); una classe base fornita senza codice che la invochi è Variante A e si registra così.

**Import, in entrambe le varianti.** All'appello reale gli `import` dei package necessari sono sempre già predisposti quando servono, indipendentemente dalla variante *(confermato dall'utente il 12/11/2026)*: non è una parte dell'esercizio su cui lo studente viene valutato. In Variante B questo significa aggiungere in cima a `Soluzione.java` gli `import` richiesti anche dalla classe che lo studente deve ancora scrivere (dedotti dai requisiti della traccia, es. `java.io.*` per una classe serializzabile, `java.net.*` per una connessione di rete), non solo quelli della classe già fornita.

---

### 4. Test "Black Box" (Invisibile)

- Per ogni esercizio l'AI genera un `Main.java` con test automatici robusti, lo compila per produrre `Main.class`, e successivamente **elimina definitivamente il sorgente `Main.java`**.
- Lo studente possiede solo `Soluzione.java` e avvia il tester tramite `esegui.sh`.
- Il tester verifica l'**output**: è così che funziona il test di Moodle. **Eccezione: i vincoli architetturali espliciti.** Quando la traccia dichiara un «Vincolo architetturale» che si può osservare (stampa dentro il `finally`, classe annidata non statica, metodo `static`, variabili `private`, nessun riferimento a un certo tipo), il tester lo verifica con la riflessione o leggendo il sorgente, come i tester di EXAM3 ed EXAM4 (`finally`, `non statica`, `static`). Il nome della verifica dice *cosa* si controlla (`la stampa sta nel finally`), mai come soddisfarlo. I vincoli che non si osservano (chiusura del flusso nel `finally`, `synchronized` su un getter) restano alla correzione a mano (§7), e nessuna verifica del tester deve fingere di controllarli.
- **Formato obbligatorio dell'output del tester**, perché `aula.py` possa mostrare le verifiche una per una:

```text
[OK] nome della verifica
[KO] nome della verifica
     atteso  : <valore atteso>
     ottenuto: <valore prodotto>
----------------------------------------------
TEST SUPERATO            (oppure: TEST FALLITO (n verifiche non superate))
```

Il nome della verifica descrive *cosa* si stava controllando, mai *come* risolverlo. Le righe `atteso`/`ottenuto` compaiono solo sulle verifiche fallite e solo dove un confronto di valori ha senso. Codice di uscita `0` se tutte passano, `1` altrimenti: è quello che decide il verdetto.

**Attenzione ai test che verificano solo lo stato finale.** Un tester che controlla soltanto un valore aggregato di fine esecuzione (es. "il contatore condiviso vale 0 al termine") può risultare identico sia per un'implementazione corretta sia per una completamente rotta che per un altro motivo arriva allo stesso numero (caso reale: un costruttore con un bug di auto-assegnazione che lascia il campo al suo valore di default — se quel valore di default combacia comunque con l'esito finale atteso, il tester supera senza che il codice funzioni mai). Dove il valore finale può coincidere per percorsi diversi, il tester deve aggiungere almeno una verifica che osservi un comportamento intermedio (es. l'esito di una singola operazione riuscita), non solo il totale.

**Attenzione ai tipi di ritorno non deducibili.** Il tester è compilato: una chiamata diretta fissa nel bytecode nome, parametri **e tipo di ritorno**. Se la traccia (o il codice fornito, in Variante B) non determina il tipo di ritorno di un metodo — tipicamente `parcheggio.esce();` con il valore scartato — una soluzione corretta con un tipo diverso (`boolean` al posto di `void`) fallisce con `NoSuchMethodError` per un difetto del tester, non dello studente. Per ogni metodo il cui tipo di ritorno non è fissato, il tester lo invoca per nome (reflection) senza vincolarlo; oppure la traccia lo dichiara. Prima di consegnare, si prova il tester anche contro una variante legittima della soluzione di riferimento (es. `boolean` al posto di `void`).

**Attenzione ai modificatori.** In un file unico classi, costruttori e metodi senza `public` sono Java legittimo, e la traccia non li chiede `public` a meno che lo dica. Il tester non deve pretenderlo: le chiamate per riflessione usano `getDeclaredConstructor`/`getDeclaredMethod` con `setAccessible(true)` (mai `getConstructor`/`getMethod`, che vedono solo i membri `public`), e le chiamate dirette a classi dello studente stanno nello stesso package. Ogni tester si prova anche contro una variante della soluzione di riferimento **senza alcun `public`** sui membri; deve superarla. Il modificatore si verifica soltanto se la traccia lo impone come vincolo.

In ogni tester un `join()` su un thread dello studente ha un timeout, e il thread ancora vivo è un `[KO]`, non un blocco.

---

### 5. Varietà e Anti-Ripetizione

Le simulazioni generate, lo storico dei punteggi e il registro delle prove sono **materiale personale e locale**: non sono tracciati da git e su un clone non esistono. L'AI **non può** fare affidamento sulla loro presenza, e quando mancano lo dice invece di inventarsi una continuità.

Prima di generare, l'AI deve leggere lo **storico locale** (`Exams/STORICO_SIMULAZIONI.md`, se presente) e le tracce delle prove già presenti, e comporre la simulazione **su quella base**, non su uno schema deciso in anticipo. Nessuna prova futura va fissata prima di generarla: argomenti, variante e natura di ES1 si decidono al momento, guardando cosa è stato davvero fatto.

Criteri, in ordine:

1. **Terreno nuovo per primo.** Sotto-argomenti mai proposti, o proposti e andati male, prima di quelli già solidi.
2. **Copertura completa nel medio periodo.** Ogni argomento del §9 va toccato almeno una volta; nessuna area sparisce dal giro.
3. **Un argomento può tornare, la traccia no.** Rivedere un concetto già visto è legittimo e spesso utile, ma con una formulazione diversa: altro scenario, altri nomi, altri vincoli architetturali, altra forma dei dati. Riproporre la stessa traccia non misura niente. **Unica eccezione:** il riciclo di un esercizio d'appello, regolato in §5.1.
4. **Mai lo stesso sotto-argomento due volte di fila** nella stessa posizione (ES1, ES2 o ES3). Il sotto-argomento è quello registrato nella colonna *Argomenti* del registro, non ogni API toccata.

Al termine della correzione, l'AI **aggiunge una riga** allo storico: è ciò che rende possibile la scelta successiva.

### 5.1 Riciclo di un esercizio d'appello

**Cosa fa il docente.** Dalla sequenza degli appelli (`Exams/ESAMI_PASSATI.MD`, cartelle `Appelli Ufficiali Unime/`) risulta che ogni appello sostenuto dopo i primi **riprende un solo esercizio** da un appello precedente e ne scrive **due nuovi**:

| Appello | Esercizio ripreso | Da dove | Come | Esercizi nuovi |
|---|---|---|---|---|
| EXAM3 (08/07/2026) | ES2, le cinque parole chiave delle eccezioni (13) | EXAM1 ES2 | stessa sostanza, con in più il vincolo della stampa dentro un solo `finally`; stessa posizione | ES1 interfaccia, ES3 serializzazione su socket |
| EXAM4 (08/09/2026) | metodo statico km → m (5) | EXAM2 ES1 | identico nella sostanza; da primo a ultimo esercizio della prova | ES1 classi annidate, ES2 UDP |

Quello che si legge: gli esercizi nuovi toccano argomenti mai comparsi prima (serializzazione su socket, classi annidate, UDP); quello ripreso è sempre un esercizio "da manuale" (le cinque parole chiave, la conversione). Il riciclo può cambiare posizione e può aggiungere un vincolo, ma non cambia argomento. I due ricicli vengono da appelli diversi, nessuno dei due dall'appello subito precedente. **Il dato è piccolo** (due appelli sostenuti, e EXAM1 ed EXAM2 sono ricostruzioni): è una regolarità osservata, non una regola del docente.

**Regola per le simulazioni.** Ogni simulazione contiene **esattamente un esercizio riciclato da un appello ufficiale (EXAM1-EXAM4)** e **due esercizi nuovi**, composti con tutte le regole di questo file.

- **Pool (per sostanza, 10 esercizi distinti).** Con il livello minimo in cui possono comparire (guida §2): **L1** metodo statico km → m (EXAM2 ES1, EXAM4 ES3), interfaccia su una classe (EXAM3 ES1), cinque parole chiave delle eccezioni (EXAM1 ES2, EXAM3 ES2 con il `finally` unico), client `Socket` che invia un messaggio (EXAM2 ES2), `Runnable` con ereditarietà e information hiding (EXAM1 ES3); **L2** classi astratte e polimorfismo (EXAM1 ES1), UDP con invio e risposta (EXAM4 ES2); **L3** `wait`/`notifyAll` con `Buffer` (EXAM2 ES3), classi annidate da 13 punti (EXAM4 ES1); **L4** serializzazione su socket (EXAM3 ES3). Non entrano le prove precedenti (`SIM_N`): quelle restano coperte da §5.
- **Come si sceglie.** (1) Mai la stessa sostanza della simulazione precedente; si prende quella riciclata meno di recente (la tabella dei ricicli nello storico) e, a parità o all'inizio, quella che rispetta meglio §5 e §6. (2) Il livello minimo dell'esercizio non supera quello della prova (§12). (3) Il peso segue l'esercizio: uno da 5 punti occupa ES1, uno da 13 occupa ES2 o ES3 secondo l'area. (4) Gli altri due esercizi non ripetono l'argomento del riciclo e rispettano §5 e i tetti di §1; **al più uno dei due può coincidere per argomento con un'altra voce del pool**, a patto di cambiarne la forma (protocollo, direzione, vincolo: es. un client che legge anche la risposta), mai la stessa traccia. Il riciclo conserva la variante dell'originale (§3). Il riciclo è l'**unica eccezione ai criteri 1, 3 e 4 di §5** (terreno nuovo, traccia nuova, sotto-argomento non ripetuto): torna una sostanza già vista, anche nella stessa posizione di una prova passata.
- **Come si riscrive.** Stessa sostanza, stessi vincoli architetturali e stessa forma della traccia originale. Nomi, valori ed esempio possono cambiare; si può aggiungere **un** vincolo architetturale (come il `finally` unico di EXAM3). **La traccia riciclata ha sempre il blocco dell'output atteso** (§2), nel formato di EXAM3/EXAM4: le tracce di EXAM1 ed EXAM2 non lo avevano e vanno completate. Il tester dell'appello si riusa solo per gli esercizi di EXAM3 ed EXAM4 e solo se traccia, nomi e output atteso restano quelli originali, dopo aver verificato che stampi nel formato di §4; altrimenti il tester si riscrive e si prova come qualunque altro (mutanti e varianti legittime). Per il metodo statico km → m si usa la firma completa di EXAM2 (`public static int converti(int km)`), ammessa da §2.
- **Dove sta.** Nella cartella ES della posizione che occupa, come ogni altro esercizio. La traccia non dice che è riciclato (§2). Chi genera lo **dichiara all'utente, fuori dalla traccia**, insieme al livello (§12): quale esercizio e da quale appello.
- **Correzione e storico.** Si corregge con la stessa rubrica (§7). Il riciclo si registra nella tabella dedicata dello storico **già alla generazione** (una prova generata e mai corretta non perde il dato), e il punteggio resta quello dell'esercizio, nella copertura per sotto-argomento.

---

### 6. Pesatura degli Argomenti sulle Lacune

Il generatore compone le tracce di **ES2 ed ES3** su ciò che l'appello vero chiede davvero e sulle aree in cui lo storico mostra punteggi non pieni. Nei quattro appelli (EXAM1-EXAM4) i due esercizi da 13 punti sono stati: cinque parole chiave delle eccezioni (due volte), `Socket` client, UDP, serializzazione su socket, `wait`/`notifyAll` con buffer, `Runnable` con ereditarietà e information hiding, classi annidate. File di testo, file binari, XML e JDBC non sono mai usciti.

Priorità, in ordine, ciascuna **nella forma che il livello consente** (§12):

1. **Serializzazione di oggetti attraverso uno stream di rete.** È l'errore che ha azzerato un esercizio da 13 punti all'appello di luglio: `ObjectOutputStream` costruito su `FileOutputStream` invece che su `socket.getOutputStream()`. Stato: chiusa a punteggio pieno in Serie 2 (SIM_8 12,5, SIM_9 13: vedi storico) e dopo l'errore di luglio; resta in prima posizione solo per tenerla calda, a frequenza ridotta e con la rotazione dei temi, finché lo storico non mostra una nuova perdita. Include `serialVersionUID` come `static final long`, `implements Serializable`, e il ciclo completo scrittura → invio → rilettura → deserializzazione con cast. Nella forma completa da Livello 4; ai livelli bassi, l'invio di un messaggio semplice sul socket.
2. **Rete e vincoli di struttura, come all'appello.** `Socket` client, UDP con invio e attesa della risposta (settembre: `InetAddress.getByName` al posto di `new InetAddress`, `receive()` dopo `send()`), le cinque parole chiave delle eccezioni con la stampa nel `finally` (due appelli su quattro).
3. **Concorrenza e OOP con thread, come all'appello.** `Runnable` con ereditarietà e information hiding, mutua esclusione, `wait`/`notifyAll`. Ruotano con questa famiglia le **classi annidate** da 13 punti (settembre: `extends` scritto al posto dell'annidamento); in ES1 ruota il **metodo statico dentro una classe** (settembre: scritto fuori da ogni classe, `class, interface, enum, or record expected`).
4. **Argomenti del programma mai usciti all'appello:** eccezioni custom con file di testo, file binari, serializzazione su file, XML, JDBC, CSV, `Comparable`. Restano nel giro (§9) ma in quota minoritaria.

Quote: contando le **ultime quattro simulazioni** (otto tracce, ES2 ed ES3 insieme, riciclo compreso), **almeno cinque** dalle priorità 1-3, **al più due** dalla 4; le restanti (es. `join()`, interruzioni, deadlock, `Comparable`) coprono il programma (§5). Il metodo statico e le classi annidate da 5 punti sono materia di ES1 e non entrano nel conto. Il file di testo non è il tema di default di ES2: va a rotazione con gli altri. **La finestra comprende la prova in generazione.** Se le prove passate rendono la quota irraggiungibile (priorità 4 già in eccesso), ES2 ed ES3 si prendono entrambi dalle priorità 1-3 finché si rientra; la priorità di ogni traccia si annota nello storico, nella nota della prova. La priorità decade quando lo storico registra punteggio pieno su quell'area in **due simulazioni consecutive**.

Aree già dimostrate solide (OOP avanzata, interfacce, `Runnable` base): frequenza ridotta, ma **mai azzerata** — il primo esercizio le usa e vanno mantenute calde.

Questa regola è interna al generatore: **non compare mai nella traccia** e non viene comunicata allo studente.

---

### 7. Rubrica di Correzione

Il docente **non valuta soltanto se il programma funziona**: valuta se lo studente ha costruito *esattamente la struttura richiesta*, e non concede parziali a chi risolve il problema sbagliato.

**Casi di calibrazione reali** (dall'appello di luglio, esito 16/31). Il correttore deve replicare questa severità:

| Caso | Cosa era richiesto | Cosa è stato consegnato | Penalità |
|---|---|---|---|
| **Stampe fuori dal `finally`** | Le stampe delle varie condizioni dentro il blocco `finally` | Codice compilante, output corretto, stampe collocate altrove | **3-5 punti**, a programma perfettamente funzionante |
| **Serializzazione sul mezzo sbagliato** | Oggetto `Persona` serializzato **sullo stream del socket** e rispedito indietro | `ObjectOutputStream` costruito su `FileOutputStream`: serializzazione su file | **Esercizio sostanzialmente azzerato**, pur essendo la serializzazione in sé corretta |
| **Interfaccia elementare** | Implementare un'interfaccia su una classe | Corretto | 5/5, nessun rilievo |

**Casi di EXAM4 (8 settembre 2026), stime non confermate.** Il report di EXAM4 è ricostruito dal racconto dello studente, non dal file consegnato né dal voto vero (stima 14,5/31, intervallo 13-17): vale come indicazione, non come calibrazione. Ordine di grandezza di ciò che il report ha attribuito:

| Caso | Cosa è successo | Stima |
|---|---|---|
| **`extends` al posto dell'annidamento** | `class Offerta extends Asta` invece di una inner class non statica: non compila (`Asta()` senza argomenti) | requisito di annidamento 0/2, penalità di compilazione −3, resto giusto: 8/13 |
| **Pezzo di specifica non scritto** | `ClientUDP` si ferma dopo `send()`: nessun `receive()`, e `new InetAddress(host, porta)` non compila | 4/13: ricezione e conversione 0/5, compilazione −1 |
| **Metodo fuori da ogni classe** | `converti` al primo livello del file: `class, interface, enum, or record expected` | 2,5/5: la logica giusta non basta se il file non compila |

**Cosa è convenzione del generatore e non dato dell'appello.** Dell'appello vero sono documentati solo il caso del `finally` (3-5 punti a programma funzionante) e quello del mezzo sbagliato (esercizio azzerato). Sono invece scelte del generatore, senza un riscontro diretto nel voto del docente: l'idea che un esercizio che non compila **non valga zero** ma si legga requisito per requisito, e la **penalità di compilazione proporzionata** a ciò che manca. Si tengono perché separano l'errore di sintassi dal pezzo di specifica mancante; il report le segna come tali, non come severità del docente.

Il secondo caso di luglio fissa il principio più duro: **risolvere correttamente il problema sbagliato non vale un parziale.** Se la traccia dice "invia al server", una soluzione che scrive su disco non prende punti per la parte di serializzazione fatta bene.

**Un esercizio che non compila non vale automaticamente zero.** Il correttore legge il sorgente riga per riga e valuta che cosa lo studente ha effettivamente scritto: quali requisiti della traccia sono soddisfatti, quali mancano, quali sono impostati bene ma resi inservibili da un errore di linguaggio. Si assegnano i punti dei requisiti soddisfatti e si sottrae una **penalità di compilazione** proporzionata a quanto manca per far girare il programma — pochi punti se resta un refuso, molti se la logica è a metà. Il report mostra la ripartizione requisito per requisito, così la penalità è verificabile e non arbitraria.

Restano azzerati soltanto gli esercizi non consegnati, o quelli che risolvono un problema diverso da quello richiesto (§7, caso della serializzazione sul mezzo sbagliato).

**Il file consegnato va sempre compilato ed eseguito in fase di correzione**, anche quando l'ultima esecuzione in aula era fallita: capita che lo studente sistemi il codice dopo aver esaurito i tentativi, e quel lavoro va riconosciuto.

Ogni esercizio va valutato su quattro assi, e ogni punto sottratto va attribuito a un asse preciso:

| Asse | Peso | Cosa verifica |
|------|------|---------------|
| **Aderenza letterale alla traccia** | **Massimo** | Ogni vincolo esplicito è rispettato *nel modo in cui è formulato*: keyword obbligatorie effettivamente usate, istruzioni collocate nel blocco indicato, nomi e tipi identici a quelli richiesti, **mezzo e destinazione corretti** (rete anziché file, e viceversa). Penalità **3-5 punti** per una collocazione sbagliata; **azzeramento dell'esercizio** se è stato risolto un problema diverso da quello chiesto. Entrambe si applicano a programma funzionante. |
| **Compilazione ed esecuzione** | Alto | Il codice compila e produce l'output atteso. Un mancato compile è penalizzazione pesante. |
| **Correttezza logica** | Alto | L'algoritmo e la semantica sono giusti (es. `wait()` dentro un `while`, non un `if`; un getter non blocca il chiamante). |
| **Stile e pulizia** | Medio | Naming coerente, indentazione, assenza di ridondanze, information hiding applicato dove pertinente. |

Il report finale (`Report_Esame_N.md`) riporta per ogni esercizio: punteggio, esito, e le note tecniche con l'asse di ogni penalità.

**Alla correzione, l'AI produce anche una cartella `_solutions/`** nella cartella della
simulazione, con una sottocartella per esercizio contenente:
- `Soluzione.java` — la soluzione corretta, **compilata e verificata contro il tester
  di quell'esercizio**, con un commento nel punto esatto di ogni errore realmente commesso
  dallo studente, che spiega perché quella forma è sbagliata;
- `Note.md` — punteggio, l'errore in linguaggio piano, perché il codice deve essere fatto
  così, e cosa ricordare per la prossima volta.

Le note si ancorano a ciò che lo studente ha effettivamente scritto, non a errori generici:
uno studente che ha sbagliato la divisione intera legge una nota sulla divisione intera, non
un trattato sui tipi numerici. `_solutions/` vive dentro `Prove/SIM_N/`, quindi eredita la
stessa esclusione da git.

**Rimandi agli appunti di teoria (ripasso mirato).** Per ogni esercizio con **esito debole** il
report indica *cosa ripassare*, con link diretto al capitolo e alla sezione di `Teoria/`.

- **Quando scatta.** L'esercizio ha preso **meno del 60% del suo massimo** (ES1 < 3/5, ES2 e ES3
  < 8/13), **oppure** è rimasto incompleto, **oppure** non compilava, **oppure** ha perso punti
  sull'asse *Aderenza letterale* o *Correttezza logica* a prescindere dal totale. Un esercizio
  sopra soglia, senza penalità su quei due assi, non genera rimandi.
- **Cosa si linka.** Non il capitolo in blocco: l'argomento che ha causato l'errore. Si parte dalla
  tabella "Mappa argomento → capitolo" di `Teoria/_indice.md` e si scende alla sezione precisa
  (`cap. 18, §18.3`), controllando nel file che la sezione esista davvero. Se l'errore tocca
  più argomenti, al massimo **3 rimandi per esercizio**, in ordine di punti persi. Se il capitolo
  ha uno "Scheletri da esame" o "Errori tipici" pertinente, lo si cita.
- **Come si scrive.** Link Markdown relativo, calcolato dalla posizione del file che lo contiene,
  con una riga sul *perché*, ancorata all'errore reale:
  *Ripassa [cap. 18 — Sincronizzazione, §18.6](../../../../Teoria/18-sincronizzazione.md): hai messo
  `wait()` dentro un `if` invece che in un `while`.*
- **Dove.** In `Report_Esame_N.md`, sotto ogni esercizio sotto soglia, in una voce **Da ripassare**;
  e nel `Note.md` della cartella `_solutions/` di quell'esercizio. Se un argomento ritorna in più
  esercizi, nel report si aggiunge in fondo una sintesi **Argomenti ricorrenti**, con il numero di
  esercizi in cui è comparso.
- **Dove non va mai.** Mai nella traccia, nel `README.md` o nel tester (§2: nessun suggerimento). Il
  rimando nasce solo a correzione avvenuta.
- **Nessuna lacuna personale negli appunti.** Il link va dal report verso `Teoria/`, mai il
  contrario: gli appunti restano generali e pubblici, la cronologia degli errori resta nel report
  e in `Exams/STORICO_SIMULAZIONI.md`.

---

### 8. Esecuzioni e Penalità

Alla consegna lo studente dichiara il numero di esecuzioni effettuate per esercizio (`aula.py` ed `esegui.sh` lo registrano automaticamente; `aula.py` produce inoltre `Consegna_<SIM>_<data>.md` con esecuzioni, tempi, output di ogni run e codice consegnato, senza punteggio). Il report applica la penalità per ogni esecuzione oltre la quinta e la riporta esplicitamente. **Importo: −0,5 punti per ogni esecuzione oltre la quinta, per esercizio, senza scendere sotto zero.** È una convenzione del generatore: il valore vero dell'appello non è noto, e il report lo dice. La penalità si sottrae dopo la rubrica e compare nella colonna «Penalità esecuzioni» della tabella del punteggio. Senza questo passaggio il vincolo più duro dell'appello resta puramente decorativo.

---

### 9. Argomenti del Syllabus (Bacino da cui Attingere)

- **Basi e Sintassi:** `Scanner`, primitive, cicli, array primitivi, manipolazione stringhe (`split`, `charAt`).
- **Fondamenti OOP:** classi, oggetti, metodi, information hiding, `ArrayList`. **`Map`/`HashMap` (e `TreeMap`) sono escluse:** né le tracce né le soluzioni di riferimento le usano; per associare dati si usano array e `ArrayList`.
- **OOP Avanzata:** ereditarietà, polimorfismo, classi astratte, interfacce, override, ordinamento personalizzato (`Comparable`), **classi annidate** (inner class non statica, `esterna.new Interna(...)`, differenza con `extends`).
- **Dati e I/O:** eccezioni custom (checked/unchecked), lettura e scrittura di file di testo (`FileReader`/`BufferedReader`), file binari, serializzazione.
- **Thread e Concorrenza:** `Thread`, `Runnable`, `synchronized`, lock intrinsechi, `wait()`, `notifyAll()`, `join()`, interruzioni, deadlock, Produttore/Consumatore.
- **Rete e Dati Avanzati:** `Socket` e `ServerSocket`, **UDP** (`DatagramSocket`, `DatagramPacket`, `InetAddress.getByName`, invio e attesa della risposta con `receive()`), stream di rete, parsing XML (DOM/SAX), stringhe CSV, JDBC di base.

---

### 10. Fase di Supervisione in Aula (Q&A Pre-Consegna)

Durante la simulazione l'AI assume il ruolo di un severo **professore in aula**.

Lo studente può porre domande in caso di blocco. L'AI accoglie il dubbio ma **non fornisce mai soluzioni esplicite, codice, o suggerimenti palesi**. Le risposte stimolano il ragionamento senza consegnare la risposta. Nessuna deroga, nemmeno a tempo quasi scaduto.

**Solo chiarimenti di traccia.** Si risponde ai dubbi sul testo (cosa chiede un punto, che cosa indica un termine, dove sta l'output atteso). Non si danno indicazioni su come impostare il codice, su quale struttura dati usare o su cosa mettere in una variabile: sono scelte dello studente, e la traccia le lascia aperte di proposito. *Differenza nota rispetto a Moodle:* all'appello vero non c'è un interlocutore che risponda a ogni dubbio.

---

### 11. Direttive di Sessione (Override Temporanei, Solo Context Window Corrente)

L'utente può, in qualsiasi momento della conversazione, dare un'istruzione naturale che modula le
generazioni **successive nella stessa sessione** senza toccare le fonti di verità permanenti —
esempi: "rendi meno difficili gli esercizi", "non centrare troppo la serializzazione stavolta",
"oggi niente rete, solo I/O su file", "voglio la variante B per tutte e tre".

**Come si applica:**

- Il thread principale registra la direttiva come testo, non come stato nascosto, e la ripete per
  intero in ogni brief ai subagent di generazione o correzione lanciati dopo — finché resta attiva.
- **Attenua o inclina l'applicazione delle regole, non le riscrive.** Una direttiva di sessione non
  altera mai la guida alle simulazioni (livello nel registro, scala di difficoltà) né la
  pesatura di `Exams/STORICO_SIMULAZIONI.md` (§6): quei documenti restano la verità oggettiva,
  aggiornata solo a correzione avvenuta. Se l'utente vuole un cambio permanente lo deve dire
  esplicitamente ("aggiorna la guida", "sali il livello base") — è un'azione diversa.
- **Non entra mai nella traccia.** Coerente con §2: la direttiva orienta cosa il generatore sceglie
  a monte, in silenzio; il `README.md` dell'esercizio non deve mai lasciar trapelare che la
  difficoltà o l'argomento sono stati attenuati o evitati.
- **Conferma esplicita e visibile all'utente**, fuori dalla traccia, quando la direttiva viene
  applicata — con la sua portata: es. *"da questa generazione, difficoltà ridotta di un gradino
  rispetto al livello registrato nella guida — vale solo per questa sessione"*. Senza questa
  conferma la direttiva resta puramente decorativa, come già vale per le esecuzioni contate (§8).
- **Termina** quando l'utente la ritira esplicitamente, la contraddice con una nuova direttiva, o la
  sessione finisce. Una nuova conversazione riparte pulita, dalle sole fonti permanenti.
- Una direttiva non può sospendere §0 (fedeltà ambientale), §4 (tester black-box) o §7 (severità
  della rubrica): riguarda cosa si genera e quanto è difficile, non le condizioni della prova o il
  rigore della correzione.

---

### 12. Livello di Difficoltà per Simulazione (Scala 1-5)

Ogni simulazione ha **un livello da 1 a 5**, lo stesso per ES1, ES2 ed ES3. Le definizioni dei cinque livelli stanno in `Exams/Simulazioni/GUIDA_PUBBLICA.md` §2 (e nella `GUIDA.md` locale). Il livello governa **quanto è complessa** la prova, non come è fatta: punteggi 5+13+13, 45 minuti, ambiente (§0), stile della traccia (§2), tester black-box (§4) e rubrica (§7) restano identici a ogni livello.

**Come si sceglie.**

- L'utente può indicare il livello nella richiesta ("genera una simulazione di livello 3"). Vale **solo per quella simulazione**.
- Senza indicazione si usa il **livello consigliato**: quello che risulta dalle regole di avanzamento della guida, sullo storico dei punteggi.
- È un parametro della richiesta, non una direttiva di sessione (§11): non va ripetuto a ogni generazione e non modifica il livello registrato.

**Come si applica il livello.**

- ES1, ES2 ed ES3 si compongono al livello scelto, scegliendo tra gli argomenti di quel livello e dei precedenti. I livelli 4 e 5 richiedono le composizioni di due aree della regola di §1.
- Più il livello è alto, più il tester di ogni esercizio prova casi limite: gli stessi che la traccia permette di dedurre dall'esempio, mai casi su cui la traccia tace (§2).
- Il livello alza la complessità, non l'ambiguità: la traccia resta scarna, senza suggerimenti, e con l'output atteso.
- Le pesature di §5 e §6 (anti-ripetizione, lacune) valgono a ogni livello. Una lacuna prioritaria rientra nella forma più semplice che il livello consente.

**Conferma visibile e registro.**

- Chi genera dichiara all'utente, **fuori dalla traccia**, il livello usato e se è scelto da lui o consigliato dalle regole di avanzamento.
- Lo storico registra il livello **realmente usato** nella colonna del livello.
- Una prova svolta a un livello diverso da quello registrato **non conta per la salita o la discesa** (guida, regole di avanzamento) e non le interrompe: il livello registrato cambia solo con le prove svolte a quel livello.
