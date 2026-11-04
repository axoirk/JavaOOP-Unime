## 🤖 REGOLE DI GENERAZIONE PER L'AI (MOCK EXAMS) — v2

*Direttiva pubblica e rigorosa per permettere a qualsiasi AI di generare simulazioni d'esame Java OOP strutturate, standardizzate e fedeli alle condizioni reali dell'appello.*

> **Principio guida:** una simulazione ha valore solo se riproduce i **vincoli** dell'appello, non solo i suoi argomenti. Un esercizio giusto svolto in condizioni comode non misura nulla.

---

### 0. Ambiente di Svolgimento (Fedeltà alle Condizioni Reali)

L'appello si svolge dentro una pagina **Moodle**, in un'area di scrittura di livello "blocco note": nessun controllo di sintassi, nessun completamento automatico, nessuna segnalazione di errore mentre si scrive. È presente un pulsante **Esegui** che compila il codice e lo confronta con un test **non visibile** allo studente.

La simulazione deve replicare queste condizioni:

- **Un solo file per esercizio.** Tutte le classi richieste vanno dichiarate nello stesso file `Soluzione.java`. Non è ammessa la suddivisione in più file.
- **Editor cieco.** Lo studente scrive in un editor di testo semplice, privo di analisi del codice: l'editor di riferimento è quello nella pagina di `Exams/aula.py`, accanto alla traccia: colorazione della sintassi, ma nessun controllo e nessun suggerimento. Per il singolo esercizio con `esegui.sh` sono ammessi `nano` e TextEdit in modalità testo semplice. L'uso di un IDE con analisi statica (IntelliJ, VS Code con estensioni Java, Eclipse) durante la prova **invalida la simulazione**.
- **Esecuzione contingentata.** L'esecuzione avviene solo tramite `Exams/aula.py` (aula d'esame in browser: tracce, cronometro, Esegui, consegna) oppure, per il singolo esercizio, tramite `Exams/esegui.sh`. Entrambi replicano il pulsante Esegui e contano i tentativi sullo stesso file `.esecuzioni`.
- **Riquadro dei test.** Dopo un Esegui lo studente vede il verdetto, l'elenco delle verifiche con il loro esito e, su quelle fallite, il valore atteso e quello prodotto — come il riquadro dei test di Moodle. Gli errori del compilatore sono mostrati integralmente.
- **Limite di 5 esecuzioni per esercizio.** Oltre la quinta, ogni esecuzione produce una penalità sul punteggio. Un errore di compilazione consuma un'esecuzione esattamente come un'esecuzione riuscita. Il tetto è per esercizio e non si travasa: l'ora complessiva è gestibile liberamente, le esecuzioni no.

### 0.1 Inizializzazione Ambiente (Preparazione Cartelle)

- Le simulazioni vivono in `Exams/Simulazioni/`: `Prove/` contiene la serie attiva, `Archivio/` le serie chiuse, una cartella ciascuna (`Serie_1/`, `Serie_2/`, …; non si alimentano più). Quando una serie si chiude, le sue `SIM_N` passano in `Archivio/Serie_<n+1>/` e la nuova riparte da `SIM_1`. Se `Prove/` non esiste, **va creata** (es. `mkdir -p "Exams/Simulazioni/Prove/SIM_X/ES1"`).
- Ogni simulazione risiede in una sottocartella numerata progressivamente dentro la serie (`SIM_1`, `SIM_2`, …) contenente `ES1`, `ES2`, `ES3`. La struttura degli argomenti e la scala di difficoltà sono in `Exams/Simulazioni/GUIDA_PUBBLICA.md`.
- In ogni cartella esercizio l'AI deposita: `README.md` (traccia), `Soluzione.java` (con i soli `import`), `Main.class` (tester compilato).

---

### 1. Struttura Punteggi, Difficoltà e Argomenti

Totale **31 punti**, **45 minuti** complessivi per i tre esercizi. Il tempo è gestibile liberamente: lo studente può passare da un esercizio all'altro quando vuole.

- **Esercizio 1 (5 punti) — Riscaldamento.** Due nature, da alternare. *Problem solving:* un metodo **statico** che risolve un calcolo matematico o un problema di logica generale — conversioni, ricorsione, manipolazione di array e stringhe (all'appello EXAM2 era `public static int converti(int km)`). *Progettazione OOP elementare:* classi che implementano un'interfaccia o estendono una classe astratta, con information hiding.
- **Esercizio 2 (13 punti) — Core Java e API built-in.** File I/O (testo, binario, serializzazione), Networking (`Socket`, `ServerSocket`), parsing XML, JDBC, uso avanzato di Collections e `Comparable`. Variare costantemente.
- **Esercizio 3 (13 punti) — L'esercizio difficile.** **Non è per forza sui thread.** Nell'unico appello sostenuto era serializzazione di oggetti su socket. Il terzo esercizio è quello complesso da 13 punti, e attinge a: thread e concorrenza (`Thread`/`Runnable`, `synchronized`, `wait`/`notifyAll`, `join()`, Produttore/Consumatore, information hiding su risorsa condivisa), oppure serializzazione, oppure networking, **spesso in combinazione tra loro**.

> **Livello di difficoltà.** Ogni simulazione ha un livello da 1 a 5, scelto per la singola prova (§12). La struttura sopra non cambia: cambia la complessità di ciò che si chiede.

> **Regola di composizione.** Gli argomenti si presentano combinati, non isolati. Almeno una traccia ES3 su tre deve richiedere di comporre due aree distinte (es. serializzazione *attraverso* un socket, thread che scrivono *su file*, `Comparable` applicato a oggetti letti *da XML*). Saper fare le due cose separatamente non basta: è esattamente il punto in cui l'appello reale è stato perso.

---

### 2. Stile della Traccia (Scarna, ma con l'Output Atteso)

La traccia risiede in `README.md` e imita il registro delle tracce d'appello: **italiano piano e diretto**, frasi brevi, terminologia standard chiamata con il suo nome — *serializzabile*, `serialVersionUID`, *thread*, *mutua esclusione*, *array*, `ArrayList`. Asciutta, non contorta: le perifrasi che evitano di nominare le cose («convertibile in una sequenza di byte», «flusso di esecuzione indipendente», «intero a 64 bit») rendono la traccia più difficile del vero e vanno evitate.

Il confine è netto: **si nominano i concetti, non si regalano le soluzioni**. «Garantendo la mutua esclusione» è il linguaggio dell'appello reale ed è ammesso; `public synchronized void deposita(int importo)` no. Un buon riferimento è `Exams/ESAMI_PASSATI.MD`: le tracce vere si leggono al primo colpo.

**Cosa la traccia DEVE contenere:**
- Nomi di classi e metodi richiesti, **case-sensitive**, e i tipi di ritorno.
- I **vincoli architetturali** espliciti (es. "usare tutte e cinque le parole chiave della gestione delle eccezioni", "tutte le variabili d'istanza devono essere private").
- L'**output atteso**, in un blocco ```text. All'appello reale lo studente conosce l'output che il test invisibile pretende: ometterlo renderebbe la simulazione più difficile del vero, non più fedele.

**Cosa la traccia NON deve MAI contenere:**
- **Le regole d'appello.** Niente intestazioni con durata, numero di esecuzioni o «tutte le classi nello stesso file»: sono condizioni note e già ricordate dall'aula. La traccia contiene l'esercizio, punto.
- **Nessun suggerimento sintattico.** Mai firme complete che contengano keyword risolutive (`synchronized`, `throws`, `extends`, `implements`, `static`). Solo nome e tipo di ritorno.
- **Nessun aiuto logico, nessun promemoria.** Anche se lo studente ha sbagliato ripetutamente lo stesso concetto nelle simulazioni precedenti, la traccia non contiene mai formule del tipo "ricordati di…", "attenzione a…". Lo studente deve arrivarci da solo.
- **Nessun riferimento alla pesatura del §6.** Lo studente non deve sapere che una certa area viene proposta più spesso.

---

### 3. Varianti di Traccia

Il docente utilizza entrambe le modalità seguenti. L'AI ne sceglie una a ogni generazione, in base a quale delle due ha esercitato di meno di recente — non secondo una rotazione fissa:

- **Variante A — Foglio bianco.** `Soluzione.java` contiene solo gli `import` pre-inseriti dall'AI. Lo studente scrive tutto.
- **Variante B — Classi parziali fornite.** `Soluzione.java` contiene una o più classi **già completamente implementate**, e lo studente deve realizzare la classe mancante **deducendone le firme dalle invocazioni presenti nel codice fornito**. La traccia descrive i requisiti della classe mancante ma non ne espone i metodi.

In entrambe le varianti: nessuna classe pre-impostata vuota, nessuna firma scheletro, nessun `TODO`.

**Import, in entrambe le varianti.** All'appello reale gli `import` dei package necessari sono sempre già predisposti quando servono, indipendentemente dalla variante: non è una parte dell'esercizio su cui lo studente viene valutato. In Variante B questo significa aggiungere in cima a `Soluzione.java` gli `import` richiesti anche dalla classe che lo studente deve ancora scrivere (dedotti dai requisiti della traccia, es. `java.io.*` per una classe serializzabile, `java.net.*` per una connessione di rete), non solo quelli della classe già fornita.

---

### 4. Test "Black Box" (Invisibile)

- Per ogni esercizio l'AI genera un `Main.java` con test automatici robusti, lo compila per produrre `Main.class`, e successivamente **elimina definitivamente il sorgente `Main.java`**.
- Lo studente possiede solo `Soluzione.java` e avvia il tester tramite `esegui.sh`.
- Il tester deve verificare l'**output**, non l'implementazione: è così che funziona il test di Moodle.
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

---

### 5. Varietà e Anti-Ripetizione

Le simulazioni generate, lo storico dei punteggi e il registro delle prove sono **materiale personale e locale**: non sono tracciati da git e su un clone non esistono. L'AI **non può** fare affidamento sulla loro presenza, e quando mancano lo dice invece di inventarsi una continuità.

Prima di generare, l'AI deve leggere lo **storico locale** (`Exams/STORICO_SIMULAZIONI.md`, se presente) e le tracce delle prove già presenti, e comporre la simulazione **su quella base**, non su uno schema deciso in anticipo. Nessuna prova futura va fissata prima di generarla: argomenti, variante e natura di ES1 si decidono al momento, guardando cosa è stato davvero fatto.

Criteri, in ordine:

1. **Terreno nuovo per primo.** Sotto-argomenti mai proposti, o proposti e andati male, prima di quelli già solidi.
2. **Copertura completa nel medio periodo.** Ogni argomento del §9 va toccato almeno una volta; nessuna area sparisce dal giro.
3. **Un argomento può tornare, la traccia no.** Rivedere un concetto già visto è legittimo e spesso utile, ma con una formulazione diversa: altro scenario, altri nomi, altri vincoli architetturali, altra forma dei dati. Riproporre la stessa traccia non misura niente.
4. **Mai lo stesso sotto-argomento due volte di fila** nella stessa posizione (ES1, ES2 o ES3).

Al termine della correzione, l'AI **aggiunge una riga** allo storico: è ciò che rende possibile la scelta successiva.

---

### 6. Pesatura degli Argomenti sulle Lacune

Il generatore concentra le tracce di **ES2 ed ES3** sulle aree in cui lo storico mostra punteggi non pieni. Priorità attuali, in ordine, fondate sull'esito reale dell'appello (16/31):

1. **Serializzazione di oggetti attraverso uno stream di rete.** È l'errore che ha azzerato un esercizio da 13 punti: `ObjectOutputStream` costruito su `FileOutputStream` invece che su `socket.getOutputStream()`. Priorità assoluta finché non è automatico. Include `serialVersionUID` come `static final long`, `implements Serializable`, e il ciclo completo scrittura → invio → rilettura → deserializzazione con cast.
2. **Dati e I/O** — eccezioni custom (checked/unchecked), file di testo, file binari, serializzazione su file.
3. **Rete e Dati Avanzati** — `Socket` e `ServerSocket`, `URL`, parsing XML (DOM/SAX), CSV, JDBC.

Circa il **60% delle tracce** deve ricadere in queste aree. La priorità decade quando lo storico registra punteggio pieno su quell'area in **due simulazioni consecutive**.

Aree già dimostrate solide (OOP avanzata, interfacce, `Runnable` base): frequenza ridotta, ma **mai azzerata** — il primo esercizio le usa e vanno mantenute calde.

Questa regola è interna al generatore: **non compare mai nella traccia** e non viene comunicata allo studente.

---

### 7. Rubrica di Correzione

Il docente **non valuta soltanto se il programma funziona**: valuta se lo studente ha costruito *esattamente la struttura richiesta*, e non concede parziali a chi risolve il problema sbagliato.

**Casi di calibrazione reali** (dall'appello sostenuto, esito 16/31). Il correttore deve replicare questa severità:

| Caso | Cosa era richiesto | Cosa è stato consegnato | Penalità |
|---|---|---|---|
| **Stampe fuori dal `finally`** | Le stampe delle varie condizioni dentro il blocco `finally` | Codice compilante, output corretto, stampe collocate altrove | **3-5 punti**, a programma perfettamente funzionante |
| **Serializzazione sul mezzo sbagliato** | Oggetto `Persona` serializzato **sullo stream del socket** e rispedito indietro | `ObjectOutputStream` costruito su `FileOutputStream`: serializzazione su file | **Esercizio sostanzialmente azzerato**, pur essendo la serializzazione in sé corretta |
| **Interfaccia elementare** | Implementare un'interfaccia su una classe | Corretto | 5/5, nessun rilievo |

Il secondo caso fissa il principio più duro: **risolvere correttamente il problema sbagliato non vale un parziale.** Se la traccia dice "invia al server", una soluzione che scrive su disco non prende punti per la parte di serializzazione fatta bene.

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

---

### 8. Esecuzioni e Penalità

Alla consegna lo studente dichiara il numero di esecuzioni effettuate per esercizio (`aula.py` ed `esegui.sh` lo registrano automaticamente; `aula.py` produce inoltre `Consegna_<SIM>_<data>.md` con esecuzioni, tempi, output di ogni run e codice consegnato, senza punteggio). Il report applica la penalità per ogni esecuzione oltre la quinta e la riporta esplicitamente. Senza questo passaggio il vincolo più duro dell'appello resta puramente decorativo.

---

### 9. Argomenti del Syllabus (Bacino da cui Attingere)

- **Basi e Sintassi:** `Scanner`, primitive, cicli, array primitivi, manipolazione stringhe (`split`, `charAt`).
- **Fondamenti OOP:** classi, oggetti, metodi, information hiding, `ArrayList`, `HashMap`.
- **OOP Avanzata:** ereditarietà, polimorfismo, classi astratte, interfacce, override, ordinamento personalizzato (`Comparable`).
- **Dati e I/O:** eccezioni custom (checked/unchecked), lettura e scrittura di file di testo (`FileReader`/`BufferedReader`), file binari, serializzazione.
- **Thread e Concorrenza:** `Thread`, `Runnable`, `synchronized`, lock intrinsechi, `wait()`, `notifyAll()`, `join()`, interruzioni, deadlock, Produttore/Consumatore.
- **Rete e Dati Avanzati:** `Socket` e `ServerSocket`, stream di rete, parsing XML (DOM/SAX), stringhe CSV, JDBC di base.

---

### 10. Fase di Supervisione in Aula (Q&A Pre-Consegna)

Durante la simulazione l'AI assume il ruolo di un severo **professore in aula**.

Lo studente può porre domande in caso di blocco. L'AI accoglie il dubbio ma **non fornisce mai soluzioni esplicite, codice, o suggerimenti palesi**. Le risposte stimolano il ragionamento senza consegnare la risposta. Nessuna deroga, nemmeno a tempo quasi scaduto.

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
