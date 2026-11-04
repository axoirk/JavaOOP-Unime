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
| **`Teoria/`** | Appunti in Markdown, 22 capitoli | Studiare e ripassare la teoria, con gli esempi già compilati e verificati |
| **`Esercitazioni (Self)/`** | Esercizi Java scritti dallo studente, organizzati su 7 livelli | Fare pratica in ordine crescente di difficoltà |
| **`Exams/`** | Tracce d'appello reali, tester black-box, e gli strumenti per simulare l'esame | Prepararsi alla prova, non solo alla materia |

---

## Struttura

```text
JavaOOP-Unime/
│
├── Teoria/
│   ├── _indice.md                       indice dei capitoli e mappa argomento → capitolo
│   ├── 01-java-e-la-jvm.md … 22-ecosistema.md   un file per capitolo, nell'ordine del Syllabus
│   └── _archivio/                       vecchi appunti (sostituiti dai capitoli)
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

Ventidue capitoli che seguono l'ordine del Syllabus a sette livelli, dalle basi di Java all'ecosistema di strumenti. Si parte da [`Teoria/_indice.md`](Teoria/_indice.md): l'elenco dei capitoli con il livello, lo stato e gli appelli in cui compaiono, più una mappa «argomento tipico d'esame → capitolo e sezione».

Ogni capitolo ha la stessa struttura: introduzione, teoria in sezioni numerate, **Come esce all'esame** (solo se l'argomento è comparso in un appello), **Scheletri da esame** (i frammenti minimi da saper scrivere a memoria), **Errori tipici** e **Riassunto**. Il codice è compilato ed eseguito prima di entrare negli appunti, quello di rete e concorrenza compreso.

| Capitoli | Argomenti | Livello |
|---|---|---|
| 01-06 | Java e la JVM, tipi e operatori, stringhe e console, strutture di controllo, array, metodi | 1-2 |
| 07-11 | Classi e oggetti, riferimenti e memoria, ereditarietà, classi astratte e interfacce, classi annidate | 2-3 |
| 12-13 | Generics e collezioni, eccezioni | 3 |
| 14-16 | File di testo, stream binari e serializzazione, interfacce grafiche | 4 |
| 17-18 | Thread, sincronizzazione | 5 |
| 19-20 | Networking (TCP, UDP), XML in Java | 6 |
| 21-22 | JDBC, ecosistema (Maven, Spring Boot, NoSQL) | 7 |

I vecchi appunti, sostituiti da questi capitoli, restano consultabili in [`Teoria/_archivio/`](Teoria/_archivio/).

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

Apre una pagina locale con le tre tracce, l'editor del codice accanto a ciascuna (colorazione Java, parentesi chiuse in automatico, salvato in `ESn/Soluzione.java`), il cronometro, un **Esegui** per esercizio e il pulsante **Consegna**. Dopo un Esegui mostra il verdetto e le verifiche una per una, con atteso e ottenuto su quelle fallite — come il riquadro dei test di Moodle.

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
