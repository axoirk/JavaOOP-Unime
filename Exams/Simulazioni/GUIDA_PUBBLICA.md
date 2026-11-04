# Guida alle Simulazioni d'Esame

Come è fatta una simulazione, come cresce la difficoltà, come si genera e come si corregge.

Vale insieme a **`Exams/REGOLE_GENERAZIONE_AI.MD`**, che resta la specifica su ambiente, stile
della traccia, tester black-box e rubrica di correzione: qui c'è solo ciò che quella non dice.

```text
Exams/Simulazioni/
├── GUIDA_PUBBLICA.md   questo file
├── Prove/              la serie attiva: SIM_1, SIM_2, … (locali, non versionate)
└── Archivio/           una cartella per serie chiusa: Serie_1/, Serie_2/, … (locali, non versionate)
```

> **Nota sui file locali.** Le simulazioni generate, lo storico dei punteggi e il registro delle
> prove sono dati personali di chi studia: restano sul disco e non entrano nel repository. Questa
> guida descrive il **meccanismo**; i risultati di chi lo usa sono affar suo.

---

## 1. Struttura fissa di ogni prova

Tre esercizi, **31 punti**, **45 minuti** complessivi gestibili liberamente. La ripartizione degli
argomenti non cambia mai da una simulazione all'altra: è la struttura ricorrente degli appelli reali.

| | Punti | Area | Cosa ci sta dentro |
|---|---|---|---|
| **ES1** | 5 | **Basi e fondamenti OOP**, oppure **problem solving** | Due nature possibili, da alternare. *OOP:* classi elementari, costruttori, information hiding, interfacce, classi astratte, ereditarietà, polimorfismo, override. *Problem solving:* un metodo **statico** che risolve un calcolo o un problema di logica — conversioni, ricorsione, cifre di un numero, manipolazione di array e stringhe |
| **ES2** | 13 | **Argomenti specifici** | Eccezioni custom, file di testo, file binari, serializzazione, `Socket`/`ServerSocket`, `URL`, XML (DOM/SAX), CSV, JDBC, Collections e `Comparable` |
| **ES3** | 13 | **Thread e mutua esclusione** | `Thread`/`Runnable`, `join()`, `synchronized`, lock intrinsechi, `wait`/`notifyAll`, produttore-consumatore, terminazione pulita, deadlock |

### Riscontro sugli appelli reali

| Appello | ES1 | ES2 | ES3 |
|---|---|---|---|
| EXAM1 (ricostruito) | Classi astratte, polimorfismo | Eccezioni, le 5 keyword | Ereditarietà + `Runnable` + information hiding |
| EXAM2 (ricostruito) | Metodo statico, conversione km → m | Networking, `Socket` client | `wait`/`notify`, buffer condiviso |
| EXAM3 (sostenuto) | Interfaccia su una classe | Eccezioni, le 5 keyword | **Serializzazione su socket** |
| EXAM4 (sostenuto) | **Inner class non statica** | **UDP, richiesta e risposta** | Metodo statico, conversione km → m |

**L'eccezione che vale la pena ricordare:** agli appelli veri l'esercizio da 13 punti non è sempre
sui thread — è stato serializzazione attraverso socket, ed è stato UDP. Lo schema ES1/ES2/ES3 qui
sopra è la norma, non una legge: dal livello 4 in poi l'ES3 può essere un esercizio di
**composizione** (oggetti serializzati che viaggiano sulla rete, thread che scrivono su file)
invece che di pura concorrenza.

---

## 2. Scala di difficoltà

La scala va da 1 a 5. Si parte dal livello 1 e si sale per merito; in più, per una singola
simulazione, si può **scegliere il livello** (regola 4 di "Regole di avanzamento"). Ogni livello
**eredita** gli argomenti dei precedenti: salire non toglie nulla, aggiunge.

### Livello 1 — rimettere le mani sulla sintassi
- **ES1** — una classe elementare con costruttore e information hiding più un'interfaccia con un solo metodo; oppure un metodo statico che risolve un calcolo diretto (conversione, somma, massimo, conteggio su una stringa).
- **ES2** — eccezione custom (controllata o non controllata) e file di testo: `BufferedReader`, `FileWriter`.
- **ES3** — mutua esclusione elementare su una risorsa condivisa: `synchronized`, nessuna attesa fra thread.

### Livello 2 — la struttura richiesta, non solo il risultato
- **ES1** — classi astratte, ereditarietà con `super()`, override, polimorfismo su array di tipo base; oppure un metodo statico con logica a più passaggi (ricorsione, cifre di un numero, ricerca in un array).
- **ES2** — file binari (`DataOutputStream`), serializzazione su file, Collections e `Comparable`. Compaiono i **vincoli architetturali** sulla collocazione delle istruzioni (blocco `finally`, chiusura del flusso, ordine delle operazioni).
- **ES3** — coordinamento con `join()`, suddivisione del carico fra thread, terminazione ordinata.

### Livello 3 — le API che l'appello pretende
- **ES1** — interfacce multiple, `Comparable`, classi astratte con stato; oppure un metodo statico che combina algoritmo e struttura dati.
- **ES2** — `Socket` e `ServerSocket`, `URL`, parsing XML (DOM o SAX), CSV, JDBC di base.
- **ES3** — `wait`/`notifyAll`, produttore-consumatore, buffer limitato, attesa dentro un `while` e non dentro un `if`.

### Livello 4 — composizione, cioè l'appello vero
- **ES2 ed ES3 combinano due aree in un solo esercizio:** serializzazione *attraverso* un socket, thread che scrivono *su file*, oggetti letti *da XML* e poi ordinati, client e server che si scambiano oggetti mentre più thread lavorano.
- Le tracce diventano più scarne: più deduzione dalle invocazioni, meno enunciati espliciti.
- È il livello dell'appello reale. **Ci si arriva, non ci si parte.**

### Livello 5 — oltre l'appello
- Stesse aree e stessa scarnezza del livello 4, con il margine in più per arrivare all'esame preparati.
- **ES1** — un algoritmo che usa una struttura dati, oppure una gerarchia di più classi con polimorfismo, con casi limite non elencati nella traccia ma deducibili dall'esempio.
- **ES2 ed ES3** — composizione di due aree con **almeno due vincoli architetturali** per esercizio (collocazione nel `finally`, ordine delle operazioni, blocco `synchronized`, ciclo di `start` separato da quello di `join`), più classi da scrivere e firme da dedurre anche per eccezioni e interfacce. ES3 può unire due meccanismi, ad esempio `wait`/`notifyAll` con `join()`, o un trasferimento fra due risorse in cui il deadlock va evitato.
- La complessità cresce, l'ambiguità no: la traccia resta chiara e con l'output atteso.

---

## 3. Regole di avanzamento

1. **Si sale di livello** dopo **due simulazioni consecutive dello stesso livello** chiuse a **≥ 26/31**, con **nessun esercizio sotto la metà** dei suoi punti. Un 28/31 ottenuto azzerando ES3 non promuove.
2. **Si scende di un livello** dopo **due simulazioni consecutive sotto 16/31**, la soglia di non superamento dell'appello.
3. **La lacuna prioritaria pesa più del livello.** Finché lo storico locale non registra due punteggi pieni consecutivi su un argomento identificato come lacuna critica, quell'argomento rientra nel giro **anche ai livelli bassi**, nella forma più semplice che il livello consente.
4. **Il livello si può scegliere per la singola simulazione** (1-5). Senza indicazione vale il livello consigliato da queste regole. Una prova svolta a un livello diverso da quello registrato è registrata con il suo livello, ma **non conta per la salita o la discesa** e non le interrompe.

---

## 4. Come si decide una nuova simulazione

Non esiste un calendario di argomenti deciso in anticipo, e **nessuna prova futura è già scritta**.
La composizione si decide al momento della generazione, guardando cosa è stato fatto davvero.

Prima di generare, l'agente:

1. legge lo **storico locale** — punteggi, copertura per sotto-argomento, prove recenti;
2. guarda le tracce già presenti in `Prove/` e in `Archivio/Serie_*/` e, se serve un riscontro sulle formulazioni, quelle degli appelli reali;
3. sceglie una composizione che **copra terreno nuovo**: sotto-argomenti mai toccati, o toccati male, prima di quelli già solidi;
4. tiene calde le aree già dimostrate solide, senza ripetere la stessa formulazione due volte di fila.

Cosa varia da una prova all'altra, per scelta ragionata e non per rotazione fissa:

- **la natura di ES1** — progettazione OOP oppure problem solving su metodo statico;
- **la variante** — foglio bianco, oppure classi già implementate di cui dedurre le firme;
- **il sotto-argomento** di ES2 e di ES3 dentro le rispettive aree;
- **la formulazione.** Un argomento già visto può tornare, ma con una traccia diversa: altro scenario, altri nomi, altri vincoli architetturali, altra forma dei dati. Rivedere `wait`/`notify` su un problema che non somiglia al precedente è ripasso; riproporre la stessa traccia è tempo perso.

Obiettivo nel medio periodo: **ogni argomento del syllabus va toccato almeno una volta**, e le aree
in cui lo storico mostra punteggi non pieni vanno toccate più spesso.

### Generazione in parallelo, non in sequenza

La decisione sopra — livello, variante, natura di ES1, sotto-argomento di ES2 ed ES3 — resta un
**unico passaggio del thread principale**: richiede la vista d'insieme su storico e
anti-ripetizione, e non si divide. Una volta assegnato un argomento a ciascun esercizio, però,
**scrivere la traccia è indipendente esercizio per esercizio**: farlo in sequenza allunga l'attesa
senza motivo.

Il thread principale:

1. decide livello, variante e argomento di ES1/ES2/ES3 come sopra;
2. lancia **tre subagent in parallelo**, uno per esercizio, ciascuno con:
   - il proprio argomento assegnato e la variante (A o B);
   - lo **stralcio già estratto** di §1-§3 di `Exams/REGOLE_GENERAZIONE_AI.MD`, copiato nel brief e non come rimando al file — il subagent non deve rileggere l'intero documento;
   - l'esempio di formulazione più vicino tra le tracce già presenti;
   - ogni direttiva di sessione attiva (§11 di `REGOLE_GENERAZIONE_AI.MD`).

   Il subagent ha accesso solo a `Read`/`Write`/`Bash` sui path della propria cartella esercizio,
   non a `Grep`/`Glob` liberi sul resto del repository. Scrive `README.md`, compila una soluzione
   di riferimento e un tester (`Main.java`) nel formato `[OK]`/`[KO]` di §4, **verifica che la
   soluzione di riferimento superi il tester**, poi cancella `Main.java` lasciando solo
   `Main.class`, e scrive `Soluzione.java` nella forma che la variante richiede (solo import per
   la A, classi già fornite per la B);
3. appena i tre risultati rientrano, il thread principale controlla la coerenza d'insieme — nessuna traccia rivela per errore la formulazione di un'altra, nessun conflitto di nomi fra esercizi — e consegna la simulazione pronta.

> Il brief autosufficiente non è un dettaglio di stile: ogni file che il subagent deve aprire da
> solo per trovare la regola che gli serve è un giro di lettura ripetuto tre volte in parallelo,
> sulla stessa manciata di righe che il thread principale ha già letto una volta.

---

## 5. Come si svolge una prova

```bash
python3 Exams/aula.py "Exams/Simulazioni/Prove/SIM_1"
```

Apre la pagina d'aula: tracce con l'editor del codice accanto a ciascuna, cronometro da 45 minuti, **Esegui** per
esercizio (cinque, oltre è penalità), **Consegna**. Alla consegna — manuale o allo scadere del
tempo — nasce `Consegna_SIM_N_<data>.md` con i dati grezzi: esecuzioni, tempi, output, codice
consegnato. **Nessun punteggio:** la correzione è un passaggio separato.

Il codice si scrive **solo** nell'editor della pagina (colorazione, nessun controllo), **un file per
esercizio**, salvato da solo in `ESn/Soluzione.java`. Un IDE con
analisi statica invalida la prova: misurerebbe qualcosa che all'appello non hai.

In pausa e dopo la consegna l'editor diventa di sola lettura.

---

## 6. Come si corregge una prova (in parallelo, non in sequenza)

Anche la correzione è indipendente esercizio per esercizio. Il thread principale:

1. legge **una sola volta** `Consegna_SIM_N_<data>.md` — codice consegnato e output delle esecuzioni in aula per tutti e tre gli esercizi;
2. lancia **tre subagent in parallelo**, uno per esercizio, ciascuno con il **path assoluto** del proprio `Soluzione.java` consegnato e del proprio `Main.class`: non gli si chiede di cercarli. Accesso solo a `Read`/`Bash` (compilazione ed esecuzione) e `Write` sulla propria `_solutions/ESn/`, niente esplorazione libera. Ciascuno:
   - compila ed esegue il codice consegnato contro il tester nascosto di quel solo esercizio — **obbligatorio anche se l'ultima esecuzione in aula era fallita** (§7 delle regole);
   - applica la **rubrica a quattro assi** e restituisce **in formato fisso** — punteggio per asse più una riga di motivazione per asse, non un paragrafo discorsivo;
   - scrive su disco `Soluzione.java` (verificata contro il tester) e `Note.md` nel path **assoluto** `<path della simulazione>/_solutions/ESn/`. Mai un path relativo: il subagent lavora con la cartella dell'esercizio come working directory, e un path relativo lì finisce annidato dentro `ESn/_solutions/ESn/` invece che a fianco di `ES1`/`ES2`/`ES3`;
3. appena i tre risultati rientrano, assembla `Report_Esame_N.md` **incollando** le righe asse-per-asse di ciascun subagent, non riscrivendole, e aggiorna lo storico locale — l'unico passaggio ancora sequenziale, perché richiede la vista d'insieme sui tre esercizi.

> Il formato fisso in output non è burocrazia: un report lungo scritto dal subagent e poi riscritto
> dal thread principale raddoppia i token di correzione senza aggiungere severità al giudizio.

---

## 7. Cosa produce una correzione

| File | Contenuto |
|---|---|
| `Report_Esame_N.md` | Punteggio per esercizio ed esito, con l'asse della rubrica a cui è imputata ogni penalità |
| `_solutions/ESn/Soluzione.java` | La soluzione corretta, **compilata e verificata contro il tester**, con un commento nel punto esatto di ogni errore realmente commesso |
| `_solutions/ESn/Note.md` | Punteggio, l'errore in linguaggio piano, perché il codice va fatto così, cosa ricordare |
| riga nello storico locale | Argomenti, punteggi, esecuzioni consumate, ambiente, variante — la memoria dell'anti-ripetizione |

Le note si ancorano a ciò che è stato **effettivamente scritto**, non a errori generici: chi ha
sbagliato la divisione intera legge una nota sulla divisione intera, non un trattato sui tipi
numerici.
