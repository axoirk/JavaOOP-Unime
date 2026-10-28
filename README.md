# JavaOOP-Unime

Repository personale di studio per **Programmazione a Oggetti (Java)** — Università degli Studi di Messina, corso di laurea in Informatica.

Non è un'applicazione e non ha un build system a livello di root: è **materiale di studio**. Appunti in Markdown, esercizi svolti a mano, e un apparato per simulare l'appello nelle stesse condizioni in cui si svolge davvero.

La lingua del repository è l'italiano — tracce, appunti, report e commit.

---

## Indice

- [Le tre aree](#le-tre-aree)
- [Struttura](#struttura)
- [`Teoria/` — gli appunti](#teoria--gli-appunti)
- [`Esercitazioni (Self)/` — il percorso a 7 livelli](#esercitazioni-self--il-percorso-a-7-livelli)
- [`Exams/` — appelli reali e simulazioni](#exams--appelli-reali-e-simulazioni)
- [Compilare ed eseguire](#compilare-ed-eseguire)
- [L'aula d'esame](#laula-desame)
- [Perché tutto questo: le regole d'appello](#perché-tutto-questo-le-regole-dappello)
- [Cosa non trovi qui](#cosa-non-trovi-qui)
- [Licenza](#licenza)

---

## Le tre aree

| Area | Cosa contiene | A cosa serve |
|---|---|---|
| **`Teoria/`** | Appunti in Markdown, ~3 500 righe | Studiare e ripassare la teoria, con gli esempi già compilati e verificati |
| **`Esercitazioni (Self)/`** | Esercizi Java scritti dallo studente, organizzati su 7 livelli | Fare pratica in ordine crescente di difficoltà |
| **`Exams/`** | Tracce d'appello reali, tester black-box, e gli strumenti per simulare l'esame | Prepararsi alla prova, non solo alla materia |

---

## Struttura

```text
JavaOOP-Unime/
│
├── Teoria/
│   ├── Fondamenti_e_Pilastri_OOP/       teoria trasversale, 01 → 06
│   ├── Appunti_Pratici_Livelli/         un file per Livello 1-7
│   └── Extra/                           approfondimenti (client-server)
│
├── Esercitazioni (Self)/
│   ├── Livello 1/ … Livello 7/
│   │   ├── Esercizio 1/ … Esercizio N/  un progetto indipendente ciascuno
│   │   └── Progetti Recap/              esercizi di sintesi del livello
│   ├── Extra/                           progetti fuori percorso
│   └── Q&A.MD                           domande e risposte per l'orale, per livello
│
├── Exams/
│   ├── Appelli Ufficiali Unime/
│   │   ├── EXAM1/  EXAM2/               appelli ricostruiti
│   │   ├── EXAM3/  EXAM4/               appelli realmente sostenuti
│   │   └── …/ESn/                       README (traccia) · Soluzione.java · Main.class (tester)
│   ├── Simulazioni/GUIDA_PUBBLICA.md    come è fatta, si genera e si corregge una simulazione
│   ├── ESAMI_PASSATI.MD                 tracce testuali degli appelli reali + regole d'appello
│   ├── REGOLE_GENERAZIONE_AI.MD         specifica per generare una simulazione fedele
│   ├── aula.py                          aula d'esame in browser: tracce, cronometro, Esegui, consegna
│   └── esegui.sh                        replica il pulsante Esegui sul singolo esercizio
│
├── CLAUDE.md                            istruzioni per gli agenti che lavorano sul repository
└── LICENSE                              MIT
```

---

## `Teoria/` — gli appunti

Due collezioni complementari, più un documento di controllo.

### `Fondamenti_e_Pilastri_OOP/` — la teoria trasversale
Sei file numerati che si leggono in ordine: architettura e JVM, sintassi e memoria, strutture di controllo, i pilastri OOP, costruttori e ciclo di vita, OOP avanzata. È il "perché" del linguaggio, indipendente dal programma del corso.

### `Appunti_Pratici_Livelli/` — un file per livello
Segue il Syllabus a sette livelli, uno a uno. Ogni file è autosufficiente: teoria, esempi di codice, e una sezione **Errori Comuni** che raccoglie gli sbagli realmente commessi, non quelli ipotetici.

| File | Argomenti |
|---|---|
| `Livello 1` | Sintassi, `Scanner`, primitive, cicli, array, stringhe |
| `Livello 2` | Classi e oggetti, information hiding, `privacy leak`, `equals`/`hashCode`/`toString`, `static`, `ArrayList`, `HashMap`, wrapper e autoboxing, `Iterator`, classi annidate |
| `Livello 3` | Ereditarietà, `super`, classi astratte, interfacce, `Comparable`, eccezioni (le 5 keyword, custom, `throws` e override) |
| `Livello 4` | `File`, stream e Decorator, file di testo, file binari, **serializzazione su file e attraverso socket**, Swing, JavaFX |
| `Livello 5` | Processi e thread, `Runnable`, `synchronized`, `wait`/`notifyAll`, produttore/consumatore, `join()`, deadlock |
| `Livello 6` | TCP (`Socket`/`ServerSocket`), **UDP richiesta e risposta**, `URL` e HTTP, XML con SAX e DOM |
| `Livello 7` | Maven, JDBC, NoSQL, Spring Boot |

Gli esempi di codice sono **compilati ed eseguiti** prima di entrare negli appunti, quelli di rete e concorrenza compresi.

---

## `Esercitazioni (Self)/` — il percorso a 7 livelli

Esercizi scritti dallo studente, uno per cartella, ciascuno con il proprio `README.md` che contiene la traccia (titolo, descrizione, obiettivo didattico, esempio di output).

| Livello | Tema |
|---|---|
| **1** | Basi e sintassi |
| **2** | Fondamenti OOP |
| **3** | OOP avanzata ed eccezioni |
| **4** | I/O, file, `Serializable`, Swing |
| **5** | JVM e thread |
| **6** | Networking e XML |
| **7** | Maven, JDBC, NoSQL, Spring |

Ogni livello chiude con **`Progetti Recap/`**: esercizi più grandi che mettono insieme gli argomenti del livello. `Q&A.MD` raccoglie le domande dell'orale ordinate per livello.

---

## `Exams/` — appelli reali e simulazioni

La parte più specifica del repository, e la ragione per cui esiste in questa forma.

### Appelli ufficiali

Quattro appelli in `Appelli Ufficiali Unime/`. **EXAM3 ed EXAM4 sono stati realmente sostenuti**; EXAM1 ed EXAM2 sono ricostruzioni. Ogni esercizio è una cartella:

| File | Cos'è |
|---|---|
| `README.md` | La traccia, nello stile scarno dell'appello, con l'**output atteso** |
| `Soluzione.java` | Il foglio di partenza: solo gli `import`. È il file che compili |
| `Main.class` | Il **tester black-box**, già compilato. Il sorgente non esiste, come all'appello |

I tester non verificano solo l'output: verificano **il modo**. Alcuni leggono la classe per riflessione (una classe annidata è davvero non statica?), altri contengono il server e contano le connessioni ricevute — così una soluzione che serializza su file invece che sulla rete fallisce anche se l'oggetto "torna indietro" corretto.

### Simulazioni

`Simulazioni/GUIDA_PUBBLICA.md` descrive struttura, scala di difficoltà a quattro livelli, regole di avanzamento e il procedimento di generazione e correzione. `REGOLE_GENERAZIONE_AI.MD` è la specifica vincolante: ambiente, stile della traccia, tester black-box, rubrica di correzione a quattro assi.

Le simulazioni generate e i punteggi sono materiale personale e **non stanno nel repository** (vedi [Cosa non trovi qui](#cosa-non-trovi-qui)).

---

## Compilare ed eseguire

Non c'è un task runner: si compila a mano, dalla cartella dell'esercizio. Tre layout, tre modi.

**Progetti con `src/`** (Livelli 1-6, nati in IntelliJ):
```bash
javac -d out/production src/*.java
java -cp out/production Main
```

**Progetti "flat"** (Progetti Recap, Exams — `.java` e `.class` nella stessa cartella):
```bash
javac *.java
java Main
```

**Livello 7** (Maven):
```bash
mvn clean install
mvn exec:java -Dexec.mainClass="org.esercizio.unime.App"
```

Non ci sono test unitari: nessun JUnit configurato. L'unico meccanismo di verifica è il tester black-box degli esami.

---

## L'aula d'esame

Due strumenti in Python e shell, senza dipendenze, che riproducono le condizioni della prova.

### `aula.py` — la prova completa

```bash
python3 Exams/aula.py "Exams/Simulazioni/Prove/SIM_1"
python3 Exams/aula.py "Exams/Appelli Ufficiali Unime/EXAM4"    # rifare un appello vero
python3 Exams/aula.py <cartella> --durata 45 --riparti --porta 8765
```

Apre una pagina locale con le tre tracce, l'editor del codice sotto ciascuna (sola colorazione Java, salvato in `ESn/Soluzione.java`), il cronometro, un **Esegui** per esercizio e il pulsante **Consegna**. Dopo un Esegui mostra il verdetto e le verifiche una per una, con atteso e ottenuto su quelle fallite — come il riquadro dei test di Moodle.

Alla consegna — manuale o allo scadere del tempo, che blocca le esecuzioni — genera `Consegna_<SIM>_<data>.md` con i **soli dati grezzi**: esecuzioni, tempi, output, codice consegnato. Nessun punteggio: la correzione è un passaggio separato.

### `esegui.sh` — il singolo esercizio

```bash
./Exams/esegui.sh "Exams/Appelli Ufficiali Unime/EXAM4/ES2"
./Exams/esegui.sh <cartella> --stato     # esecuzioni consumate
./Exams/esegui.sh <cartella> --reset     # azzera il contatore
```

Replica il pulsante Esegui e conta i tentativi. I due strumenti condividono il contatore, quindi si possono alternare.

---

## Perché tutto questo: le regole d'appello

L'esame si svolge dentro una pagina **Moodle**, in un'area di scrittura di livello blocco note: nessun controllo di sintassi, nessun completamento, nessuna segnalazione di errore mentre scrivi.

| Vincolo | Valore |
|---|---|
| Tempo | **45 minuti** totali per 3 esercizi, gestibili liberamente |
| Punteggio | **31 punti** (5 + 13 + 13) |
| File | **Tutte le classi di un esercizio in un unico file** |
| Esecuzioni | **Massimo 5 per esercizio**; oltre, penalità. Un errore di compilazione ne consuma una come un successo |
| Test | Invisibile. L'output atteso è però indicato nella traccia |

E il criterio di correzione che conta più di tutti: **il docente non valuta soltanto se il programma funziona, ma se hai costruito esattamente la struttura richiesta.** Caso reale: codice compilante con output corretto, penalizzato di 3-5 punti perché le stampe non erano dentro il blocco `finally` che la traccia imponeva.

È il motivo per cui gli appunti hanno una sezione "Errori Comuni" e i tester controllano il modo: **l'asse a rischio più alto è l'aderenza letterale, non la correttezza.**

---

## Cosa non trovi qui

Alcune cose esistono in locale ma sono deliberatamente fuori dal repository. Prima di dire "non c'è", tieni presente che:

| Escluso | Perché |
|---|---|
| `java_lessons/` | Materiale del professore: non ridistribuibile |
| `Exams/Simulazioni/Prove/`, `Archivio/` | Simulazioni generate, usa e getta |
| `Exams/STORICO_SIMULAZIONI.md` | Storico dei punteggi: dato personale |
| `Exams/Simulazioni/GUIDA.md` | Guida personale, contiene il registro delle prove |
| `SYLLABUS.MD`, `REPORT.MD` | Documenti di regia del percorso |

La linea è netta: **la logica è pubblica, i risultati di chi la usa no.** Le regole di generazione, la guida alle simulazioni e gli strumenti dell'aula stanno nel repository; punteggi e prove svolte restano sul disco.

I file `.class` invece **sono committati di proposito** in `Progetti Recap` e in `Exams`: i tester black-box devono essere distribuibili già compilati.

---

## Licenza

[MIT](LICENSE) — © 2026 devmirkoo. Materiale pensato per uso didattico personale.

> **Nota.** Appunti, tracce di simulazione e strumenti d'aula sono stati costruiti con l'assistenza di modelli linguistici, a partire dal materiale del corso e dagli errori realmente commessi agli appelli. Le tracce degli appelli ufficiali sono ricostruzioni: struttura e vincoli sono quelli reali, i dettagli operativi sono dichiarati come tali nel README di ogni cartella.
