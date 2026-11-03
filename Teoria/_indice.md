---
materia: Programmazione a Oggetti
aggiornato: 2026-11-03
---

# Programmazione a Oggetti (Java) — Appunti di teoria

Questi appunti coprono il programma del corso di *Programmazione a Oggetti* (Università di Messina, Informatica, secondo anno). Sono pensati per chi incontra Java per la prima volta e deve arrivare all'esame scritto sapendo scrivere a memoria, su un editor senza aiuti, il codice degli argomenti che escono più spesso.

I capitoli seguono l'ordine dei sette livelli del programma: dalle basi del linguaggio (livello 1) alla programmazione a oggetti (livelli 2 e 3), poi file e interfacce grafiche (4), thread e concorrenza (5), rete e XML (6), e infine l'ecosistema di strumenti attorno a Java (7). Ogni capitolo si regge da solo, ma rimanda ai precedenti quando ne usa i concetti.

Ogni capitolo ha la stessa struttura: un'introduzione che dice di cosa parla, la teoria divisa in sezioni numerate, una sezione **Come esce all'esame** (solo se l'argomento è comparso in un appello), gli **Scheletri da esame** (i frammenti minimi da saper scrivere a memoria), gli **Errori tipici** e un **Riassunto** finale.

I riquadri colorati hanno un significato fisso:

| Riquadro | Contenuto |
|---|---|
| `NOTE` | una definizione, oppure un *Approfondimento esterno* tratto dalla documentazione ufficiale Oracle (con il link alla pagina) |
| `TIP` | un'intuizione o un'analogia |
| `IMPORTANT` | un punto che il docente sottolinea o che pesa all'esame |
| `WARNING` | un caso limite o una cosa da non confondere |
| `CAUTION` | un errore tipico, con la forma sbagliata e quella corretta |

## L'esame scritto in breve

La prova scritta si svolge su Moodle, in un'area di testo che ha la comodità di un blocco note: niente controllo della sintassi, niente completamento automatico. Tutte le classi di un esercizio vanno scritte in un unico file. Un pulsante *Esegui* compila il codice e ne confronta l'output con un test che non si vede, mentre l'output atteso è riportato nella traccia. Ogni esercizio ammette al massimo cinque esecuzioni, e anche un errore di compilazione ne consuma una.

Si hanno 45 minuti per tre esercizi, da gestire liberamente, per 31 punti in tutto: un esercizio da 5 punti e due da 13. Gli argomenti tipici sono la logica e la programmazione a oggetti di base; le API principali di Java (eccezioni, file, serializzazione, socket TCP e UDP, XML, JDBC, collezioni); i thread e la concorrenza.

Il docente non valuta soltanto se il programma funziona, ma se rispetta **alla lettera** la struttura richiesta: nomi di classi e metodi, firme, blocchi imposti (per esempio una stampa che deve stare in un `finally`), formato dell'output. Un programma che produce l'output giusto con una struttura diversa da quella chiesta perde punti. Per questo il codice di questi appunti è scritto con le firme esatte delle API, le eccezioni da dichiarare e gli `import` espliciti.

## Capitoli

| # | Capitolo | Livello | Stato | Appelli in cui compare |
|---|---|---|---|---|
| 01 | [Java e la JVM](01-java-e-la-jvm.md) | 1 | completo | EXAM2, EXAM4 |
| 02 | [Tipi primitivi, variabili e operatori](02-tipi-variabili-operatori.md) | 1 | completo | EXAM2, EXAM4 |
| 03 | [Stringhe e input/output da console](03-stringhe-e-console.md) | 1 | completo | — |
| 04 | [Strutture di controllo](04-strutture-di-controllo.md) | 1 | da fare | — |
| 05 | [Array e matrici](05-array-e-matrici.md) | 1 | da fare | EXAM2 |
| 06 | [Metodi](06-metodi.md) | 1-2 | da fare | EXAM2, EXAM4 |
| 07 | [Classi e oggetti](07-classi-e-oggetti.md) | 2 | da fare | EXAM1, EXAM3, EXAM4 |
| 08 | [Riferimenti e memoria](08-riferimenti-e-memoria.md) | 2 | da fare | EXAM3 |
| 09 | [Ereditarietà e polimorfismo](09-ereditarieta-e-polimorfismo.md) | 2-3 | da fare | EXAM1 |
| 10 | [Classi astratte e interfacce](10-classi-astratte-e-interfacce.md) | 3 | da fare | EXAM1, EXAM3 |
| 11 | [Classi annidate, interne e anonime](11-classi-annidate.md) | 2-3 | da fare | EXAM4 |
| 12 | [Generics e collezioni](12-generics-e-collezioni.md) | 2-3 | da fare | — |
| 13 | [Eccezioni](13-eccezioni.md) | 3 | da fare | EXAM1, EXAM3 |
| 14 | [File di testo](14-file-di-testo.md) | 4 | da fare | — |
| 15 | [Stream binari e serializzazione](15-stream-binari-e-serializzazione.md) | 4 | da fare | EXAM3 |
| 16 | [Interfacce grafiche](16-interfacce-grafiche.md) | 4 | da fare | — |
| 17 | [Thread](17-thread.md) | 5 | da fare | EXAM1 |
| 18 | [Sincronizzazione](18-sincronizzazione.md) | 5 | da fare | EXAM2 |
| 19 | [Networking](19-networking.md) | 6 | da fare | EXAM2, EXAM3, EXAM4 |
| 20 | [XML in Java](20-xml.md) | 6 | da fare | — |
| 21 | [JDBC](21-jdbc.md) | 7 | da fare | — |
| 22 | [Ecosistema: Maven, Spring Boot, NoSQL](22-ecosistema.md) | 7 | da fare | — |

Gli appelli sono indicati con una sigla. EXAM3 è l'appello dell'8 luglio 2026 ed EXAM4 quello dell'8 settembre 2026; EXAM1 ed EXAM2 sono tracce di appelli precedenti, ricostruite.

## Mappa argomento → capitolo

| Argomento tipico d'esame | Dove |
|---|---|
| Un metodo statico dentro una classe, conversioni numeriche | cap. 01, §1.10; cap. 06; cap. 02, §2.8 |
| Divisione intera e cast | cap. 02, §2.5.2 e §2.6.3 |
| Confrontare due stringhe (`equals`, `compareTo`) | cap. 03, §3.4 |
| Spezzare una riga di testo in campi con `split` | cap. 03, §3.5 |
| Formattare l'output con `printf` e `String.format`, simbolo decimale e `Locale` | cap. 03, §3.6.3 |
| Classe con campi privati, getter e setter, costruttori in overload | cap. 07 |
| Sottoclasse con `super(...)` e override | cap. 09 |
| Classe astratta o interfaccia implementata da più classi | cap. 10 |
| Classe interna non statica che modifica lo stato della classe esterna | cap. 11 |
| Le cinque parole chiave delle eccezioni, stampa nel `finally` | cap. 13 |
| Eccezione personalizzata controllata o non controllata | cap. 13 |
| Leggere un file di testo riga per riga fino alla fine | cap. 14 |
| Scrivere in coda a un file | cap. 14 |
| Leggere dati binari o oggetti fino a `EOFException` | cap. 15 |
| `Serializable` e `serialVersionUID` | cap. 15 |
| Thread con `Runnable`, `start` e `join` | cap. 17 |
| Dividere un array tra più thread | cap. 17 |
| Mutua esclusione con `synchronized` | cap. 18 |
| Buffer condiviso con `wait` e `notifyAll` (produttore/consumatore) | cap. 18 |
| Client TCP che invia un messaggio | cap. 19 |
| Inviare un oggetto serializzato su un socket e leggere la risposta | cap. 19, cap. 15 |
| Client UDP che invia un datagramma e attende la risposta | cap. 19 |
| Caricare un documento XML con DOM e leggere gli elementi | cap. 20 |
| Query con `PreparedStatement` e lettura del `ResultSet` | cap. 21 |

La colonna *Dove* indicherà anche la sezione esatta man mano che i capitoli vengono scritti.
