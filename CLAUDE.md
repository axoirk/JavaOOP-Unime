# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Cos'è questo repository

Repository personale di studio per **Programmazione a Oggetti (Java)** — Unime, Informatica.
Non è un'applicazione: è una raccolta di appunti, esercizi e simulazioni d'esame.
**Non esiste un build system a livello di root.** Ogni cartella di esercizio è un progetto indipendente.

La lingua del repository è **l'italiano** — README, tracce, appunti, report e commit messages. Mantienila.

## Comandi

Nessun task runner. Compilazione manuale, dalla cartella dell'esercizio:

```bash
# Esercizi con layout src/ (Livelli 1-6, progetti IntelliJ)
javac -d out/production src/*.java
java -cp out/production Main

# Esercizi "flat" (Progetti Recap, Exams) — .java e .class nella stessa cartella
javac *.java
java Main

# Livello 7 (Maven)
mvn clean install       # oppure: mvn package
mvn exec:java -Dexec.mainClass="org.esercizio.unime.App"

# Simulazione completa — aula d'esame in browser: 3 tracce, cronometro, Esegui, consegna
python3 Exams/aula.py "Exams/Simulazioni/Prove/SIM_1"
python3 Exams/aula.py "Exams/Appelli Ufficiali Unime/EXAM3"   # rifare l'appello vero
python3 Exams/aula.py <cartella> --durata 45 --riparti --porta 8765

# Singolo esercizio — replica il pulsante "Esegui" di Moodle e conta i tentativi
./Exams/esegui.sh "Exams/Simulazioni/Prove/SIM_1/ES2"
./Exams/esegui.sh <cartella> --stato     # esecuzioni consumate
./Exams/esegui.sh <cartella> --reset     # azzera il contatore
```

`aula.py` (stdlib, nessuna dipendenza) apre una pagina locale con la traccia a sinistra e l'editor a
destra (colorazione Java, parentesi chiuse in automatico, salvataggio automatico in `ESn/Soluzione.java`), le tre tracce, il cronometro dei 45 minuti, un Esegui per esercizio e il pulsante Consegna.
Dopo un Esegui mostra il verdetto e l'elenco delle verifiche del tester, con atteso e ottenuto su
quelle fallite, come il riquadro dei test di Moodle; i tester devono perciò stampare nel formato
`[OK]`/`[KO]` descritto in `REGOLE_GENERAZIONE_AI.MD` §4. Alla consegna — manuale o allo scadere del tempo, che
blocca le esecuzioni — genera `Consegna_<SIM>_<data>.md` nella cartella della simulazione: dati
grezzi (esecuzioni, tempi, output, codice consegnato), **nessun punteggio**. La correzione resta
un passaggio separato, da fare sulla rubrica §7. Lo stato vive in `.aula.json` e i contatori
restano quelli di `esegui.sh` (`.esecuzioni`), quindi i due strumenti si possono alternare.

Non esistono test unitari (nessun JUnit configurato). L'unico meccanismo di test è il **tester black-box** degli esami (vedi sotto).

## Struttura

| Area | Contenuto |
|------|-----------|
| `Teoria/` | Appunti in Markdown. `Fondamenti_e_Pilastri_OOP/` (01→06, teoria trasversale) e `Appunti_Pratici_Livelli/` (un file per Livello 1-7, allineato al Syllabus). |
| `Esercitazioni (Self)/` | `Livello 1..7/Esercizio N/` + `Progetti Recap/`. Esercizi scritti dallo studente. |
| `Exams/` | `Appelli Ufficiali Unime/EXAM1..4/` (tracce, soluzioni e tester; **EXAM3 ed EXAM4 sono gli appelli davvero sostenuti**, 08/07/2026 e 08/09/2026) e `Simulazioni/`: `GUIDA_PUBBLICA.md` (tracciata) più il materiale personale non tracciato — `GUIDA.md` con il registro delle prove, `Prove/SIM_N/` (serie attiva), `Archivio/Serie_N/` (serie chiuse). |
| `java_lessons/` | Materiale del professore. **Ignorato da git — non modificare.** |

I 7 Livelli sono definiti da `Esercitazioni (Self)/SYLLABUS.MD`: 1 basi/sintassi → 2 fondamenti OOP → 3 OOP avanzata + eccezioni → 4 I/O, file, Serializable, Swing → 5 JVM e thread → 6 networking e XML → 7 Maven/JDBC/NoSQL/Spring. Ogni nuovo esercizio o file di teoria deve collocarsi in questo schema.

Documenti trasversali:
- `Esercitazioni (Self)/SYLLABUS.MD` — percorso ufficiale a 7 livelli (fonte di verità per gli argomenti).
- `Esercitazioni (Self)/REPORT.MD` — stato di avanzamento e incongruenze Syllabus ↔ Teoria ↔ esercizi.
- `Esercitazioni (Self)/Q&A.MD` — domande/risposte per l'orale, ordinate per livello.
- `Exams/ESAMI_PASSATI.MD` — tracce testuali degli appelli reali + regole d'appello.
- `Exams/REGOLE_GENERAZIONE_AI.MD` — direttiva vincolante per generare simulazioni (vedi sotto).
- `Exams/Simulazioni/GUIDA_PUBBLICA.md` — struttura fissa delle prove (ES1 basi OOP **o** problem solving su metodo statico · ES2 argomenti specifici · ES3 thread e mutua esclusione), scala di difficoltà a 4 livelli, avanzamento e criteri di composizione. La prova successiva **non è mai decisa in anticipo**: argomenti, variante e natura di ES1 si scelgono al momento della generazione, leggendo storico e tracce già proposte.
- `Exams/STORICO_SIMULAZIONI.md` — storico, copertura per sotto-argomento, curva dei punteggi. **Materiale personale: locale e non tracciato**, come `Simulazioni/GUIDA.md` (che contiene il registro delle prove) e le simulazioni stesse. È la memoria dell'anti-ripetizione, ma su un clone non esiste.

Materiale personale, presente in locale ma **non tracciato**: `Teoria/MAPPA_LACUNE.md` (confronto appelli ↔ appunti), `docs/`, i `Report_EXAM*.md` e le cartelle `_solutions/` e `_soluzione/` dentro gli appelli. Prima di dire "non è nel repository", tienilo presente.

## Convenzioni

- **Ogni cartella di esercizio contiene un `README.md`** con la traccia. Formato consolidato: titolo, Descrizione, Obiettivo didattico, Esempio di Output in blocco ```text. Crea sempre il README insieme al codice.
- I `.class` sono **committati di proposito** in `Progetti Recap` e negli `Exams` (i tester black-box devono essere distribuibili già compilati). Non ripulirli.
- I `.iml` e `out/` di IntelliJ nei Livelli 1-6 sono tracciati; i nomi dei `.iml` spesso non corrispondono alla cartella — è storico, non un bug da correggere.
- `.gitignore` di root esclude `java_lessons/`, `Exams/Simulazioni/Archivio/`, `Exams/Simulazioni/Prove/SIM_*/`, `REPORT.MD` e `SYLLABUS.MD`: questi file esistono in locale ma **non** finiscono su remote. Tienilo presente prima di dire "non è nel repository".

## Regole d'esame (vincolanti)

**Come si svolge l'appello reale.** Pagina Moodle, area di scrittura di livello blocco note: nessun controllo di sintassi, nessun completamento. Tutte le classi di un esercizio in un **unico file**. Un pulsante **Esegui** compila e confronta l'output con un test **non visibile**; l'output atteso è però indicato nella traccia. **Massimo 5 esecuzioni per esercizio**, oltre scattano penalità, e un errore di compilazione consuma un tentativo come un successo. **45 minuti totali**, 3 esercizi, 31 punti (5 + 13 + 13); il tempo è gestibile liberamente, si può passare da un esercizio all'altro. Es1 = logica/OOP base, Es2 = Core Java API (I/O, socket, XML, JDBC, Collections), Es3 = thread e concorrenza.

**Come valuta il docente.** Non solo se funziona, ma se hai costruito *esattamente* la struttura richiesta. Caso reale: codice compilante e con output corretto, penalizzato di 3-5 punti perché le stampe non erano dentro il blocco `finally` che la traccia imponeva. L'asse a rischio più alto è l'aderenza letterale, non la correttezza.

`Exams/REGOLE_GENERAZIONE_AI.MD` (v2) è la specifica da seguire alla lettera per generare una simulazione. I punti che si sbagliano più facilmente:

1. **Ambiente fedele** (§0): editor semplice, un file, esecuzione solo via `Exams/esegui.sh` che conta i tentativi. Una simulazione svolta in IntelliJ non misura ciò che l'appello misura.
2. **Traccia scarna ma con l'output atteso** (§2): mai firme con keyword risolutive (`synchronized`, `throws`, `extends`), mai reminder tipo "attento a…" nemmeno su errori già commessi. L'output atteso invece è obbligatorio — all'appello lo studente ce l'ha.
3. **Due varianti** (§3), da alternare: foglio bianco, oppure classi già implementate di cui dedurre le firme mancanti.
4. **Tester black-box** (§4): scrivi `Main.java`, compilalo, poi **cancella il sorgente** lasciando solo `Main.class`.
5. **Anti-ripetizione via `Exams/STORICO_SIMULAZIONI.md`** (§5), non scansionando `Simulazioni/Prove/`. Entrambi sono locali e gitignorati: su un clone non esistono, e in quel caso l'AI lo dice invece di simulare una continuità.
6. **Pesatura sulle lacune** (§6): ~60% delle tracce ES2 su I/O+Serializzazione e Rete+XML. Interna al generatore, mai dichiarata nella traccia.
7. **Rubrica a 4 assi** (§7) per la correzione, con `Aderenza letterale alla traccia` a peso massimo.

**Ruolo durante una simulazione:** sei il professore in aula. Rispondi ai dubbi stimolando il ragionamento, ma non fornisci mai soluzioni, codice o suggerimenti espliciti. La correzione avviene dopo, in un `Report_Esame_N.md` che attribuisce ogni punto sottratto a un asse preciso della rubrica.
