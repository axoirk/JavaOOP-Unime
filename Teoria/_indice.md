---
materia: Programmazione a Oggetti
aggiornato: 2026-11-04
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
| 04 | [Strutture di controllo](04-strutture-di-controllo.md) | 1 | completo | — |
| 05 | [Array e matrici](05-array-e-matrici.md) | 1 | completo | EXAM2 |
| 06 | [Metodi](06-metodi.md) | 1-2 | completo | EXAM2, EXAM4 |
| 07 | [Classi e oggetti](07-classi-e-oggetti.md) | 2 | completo | EXAM1, EXAM3, EXAM4 |
| 08 | [Riferimenti e memoria](08-riferimenti-e-memoria.md) | 2 | completo | EXAM3 |
| 09 | [Ereditarietà e polimorfismo](09-ereditarieta-e-polimorfismo.md) | 2-3 | completo | EXAM1 |
| 10 | [Classi astratte e interfacce](10-classi-astratte-e-interfacce.md) | 3 | completo | EXAM1, EXAM3 |
| 11 | [Classi annidate, interne e anonime](11-classi-annidate.md) | 2-3 | completo | EXAM4 |
| 12 | [Generics e collezioni](12-generics-e-collezioni.md) | 2-3 | completo | — |
| 13 | [Eccezioni](13-eccezioni.md) | 3 | completo | EXAM1, EXAM3 |
| 14 | [File di testo](14-file-di-testo.md) | 4 | completo | — |
| 15 | [Stream binari e serializzazione](15-stream-binari-e-serializzazione.md) | 4 | completo | EXAM3 |
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
| Un metodo statico dentro una classe, conversioni numeriche | cap. 01, §1.10; cap. 06, §6.1.2 e §6.4.1; cap. 02, §2.8 |
| Divisione intera e cast | cap. 02, §2.5.2 e §2.6.3 |
| Confrontare due stringhe (`equals`, `compareTo`) | cap. 03, §3.4 |
| Scegliere tra intervalli (`if` / `else if`) | cap. 04, §4.2 |
| Scegliere tra valori esatti (`switch`, `break`, enum) | cap. 04, §4.3 e §4.4 |
| Ciclo `while`, `do-while`, `for`; valore sentinella | cap. 04, §4.5 e §4.6 |
| Dal testo di un esercizio alla struttura di controllo | cap. 04, §4.9 |
| Spezzare una riga di testo in campi con `split` | cap. 03, §3.5 |
| Formattare l'output con `printf` e `String.format`, simbolo decimale e `Locale` | cap. 03, §3.6.3 |
| Dichiarare, riempire e percorrere un array; `length`; indice fuori dai limiti | cap. 05, §5.1 e §5.2 |
| Array con contatore (struttura a capacità fissa: inserimento, estrazione) | cap. 05, §5.3 e scheletro finale |
| Copiare o confrontare array (`==`, `Arrays.equals`, `copyOf`) | cap. 05, §5.4 |
| Metodi che ricevono o restituiscono array; `args` del `main` | cap. 05, §5.5 |
| Massimo, ricerca, ordinamento di un array | cap. 05, §5.6 |
| Matrici, anche con righe di lunghezza diversa | cap. 05, §5.7 |
| Array di oggetti (elementi `null` fino al `new`) | cap. 05, §5.8 |
| Un metodo con `return` su ogni percorso (`missing return statement`) | cap. 06, §6.1.4 |
| Passaggio per valore: perché un metodo non scambia due `int` | cap. 06, §6.3.2 |
| Metodo `static` contro metodo d'istanza (`static` e costanti di classe) | cap. 06, §6.4 |
| `Math.pow`, `sqrt`, `round`, `random` e i loro tipi di ritorno | cap. 06, §6.5 |
| Classi wrapper, `parseInt`, `Character.isDigit`, `Integer` con `equals` | cap. 06, §6.6 |
| Overloading e scelta del metodo | cap. 06, §6.7 |
| Metodo ricorsivo con caso base, ricerca binaria, ordinamento per fusione | cap. 06, §6.9 |
| Classe con campi privati, getter e setter, costruttori in overload | cap. 7, §7.2, §7.3.3 e scheletri finali |
| Costruttore che ne richiama un altro con `this(...)` | cap. 7, §7.2.5 |
| Il costruttore di default che sparisce | cap. 7, §7.2.3 |
| Contatore di oggetti creati, costante di classe, campo `final` | cap. 7, §7.4 |
| `enum` con campi e costruttore | cap. 7, §7.5 |
| Package, `import` e conflitti di nome | cap. 7, §7.6; cap. 1, §1.5.4 |
| Dal testo di una traccia alla classe (nomi, ordine dei parametri, `private`) | cap. 7, §7.8 |
| Perdita di riservatezza e copia difensiva | cap. 7, §7.3.7 |
| Variabile e oggetto, riferimento, alias (`q = p` non copia) | cap. 8, §8.1 e §8.2 |
| Disegnare la memoria (stack, heap) per prevedere l'output | cap. 8, §8.1.3 e §8.1.5 |
| `null`, `NullPointerException`, controllo `!= null` nell'ordine giusto | cap. 8, §8.3.2 e §8.3.3 |
| Metodo che restituisce `null` se non trova nulla | cap. 8, §8.3.4 |
| `==` contro `equals`; scrivere un confronto sul contenuto | cap. 8, §8.4 e scheletro |
| Un oggetto letto da file o da rete è un oggetto nuovo | cap. 8, §8.4.5 |
| Un metodo modifica l'oggetto ricevuto ma non può sostituirlo; scambio | cap. 8, §8.5 |
| Copia di un oggetto, costruttore di copia, copia di un array di oggetti | cap. 8, §8.6 |
| Garbage collector, oggetto irraggiungibile | cap. 8, §8.7 |
| Sottoclasse con `extends`, una sola superclasse, ordine di `extends` e `implements` | cap. 9, §9.1.2 e §9.1.5 |
| Un campo privato della superclasse non si nomina; `protected` | cap. 9, §9.2 |
| Costruttore di sottoclasse con `super(...)`, chiamata implicita, ordine di costruzione | cap. 9, §9.3.1-§9.3.2 |
| Costruttore che non ha i dati della superclasse | cap. 9, §9.3.4 e scheletro |
| Riscrivere un metodo (stessa firma, `public`), `@Override`, `super.metodo()` | cap. 9, §9.4.1-§9.4.3 e scheletro |
| Overloading contro overriding; `@Overload` non esiste | cap. 9, §9.4.4; cap. 6, §6.7 |
| Metodo o classe `final` | cap. 9, §9.4.6 |
| Una variabile della superclasse che indica un oggetto della sottoclasse; cast verso il basso | cap. 9, §9.5.1-§9.5.3 |
| "È un" contro "ha un" | cap. 9, §9.5.4 |
| Array polimorfico, binding dinamico, quale versione parte | cap. 9, §9.6 e scheletro |
| `toString` che restituisce la stringa nel formato richiesto | cap. 9, §9.7.2 e scheletro |
| `equals(Object)` e `hashCode` | cap. 9, §9.7.3-§9.7.4 e scheletro |
| Classe astratta con metodo astratto e sottoclassi (`abstract`, metodo senza corpo) | cap. 10, §10.1.2 e primo scheletro |
| Regole delle classi astratte (non si istanziano, sottoclasse incompleta, modificatori vietati) | cap. 10, §10.1.3 |
| Classe astratta con costruttore e metodo completo che chiama quello astratto | cap. 10, §10.1.4-§10.1.5 e terzo scheletro |
| Interfaccia (`interface`) realizzata da più classi con `implements`, metodi `public` | cap. 10, §10.2.2-§10.2.3 e secondo scheletro |
| Usare gli oggetti attraverso il tipo dell'interfaccia (variabile, parametro, array) | cap. 10, §10.2.4 |
| Costanti in un'interfaccia; più interfacce; interfaccia che ne estende un'altra | cap. 10, §10.2.5-§10.2.7 |
| Classe astratta contro interfaccia: quando si sceglie l'una o l'altra | cap. 10, §10.3 |
| Ordinare un array di oggetti: `Comparable`, `compareTo`, `Arrays.sort` | cap. 10, §10.4 e quarto scheletro |
| `Runnable` e il metodo `run()` come realizzazione di un'interfaccia | cap. 10, §10.5; cap. 17 |
| Classe interna non statica che modifica lo stato della classe esterna | cap. 11, §11.2.1-§11.2.2 e primo scheletro |
| Creare un oggetto interno (`esterna.new Interna(...)`, `Esterna.this`) | cap. 11, §11.2.3-§11.2.4 |
| Classe interna `private` e `main` fuori dall'esterna | cap. 11, §11.2.5 |
| Annidare non è ereditare (`extends` al posto della classe interna) | cap. 11, §11.2.6 |
| Nodo di lista nascosto dentro la lista (classe interna privata) | cap. 11, §11.3 e secondo scheletro |
| Classe annidata `static` e `new Esterna.Annidata(...)`; interna o statica | cap. 11, §11.4 e terzo scheletro |
| Classe anonima (`new Interfaccia() { ... }`), variabili `final` di fatto | cap. 11, §11.5 e quarto scheletro |
| Dalla frase della traccia (classe annidata, "non statica", nessun riferimento all'esterna) al codice | cap. 11, §11.6 |
| Contenitore che cresce da solo: `ArrayList`, metodi, `import`, solo oggetti | cap. 12, §12.1.1-§12.1.3 e primo scheletro |
| Lista di numeri (`ArrayList<Integer>`), `remove(int)` contro `remove(Object)` | cap. 12, §12.1.4 |
| Percorrere una lista (`for`, for-each); indice fuori dai limiti | cap. 12, §12.1.5-§12.1.6 |
| Copiare una lista (alias, `new ArrayList<>(a)`, `clone`) | cap. 12, §12.1.7 |
| Classe generica `Classe<T>`; `new T[]` e tipi primitivi vietati; tipo grezzo | cap. 12, §12.2 |
| Lista concatenata: nodo interno privato, aggiungere e togliere nodi | cap. 12, §12.3.2 e secondo scheletro |
| Eccezione al posto del messaggio d'errore in una struttura dati | cap. 12, §12.3.3 |
| Lista concatenata generica (`<E>`) | cap. 12, §12.3.4 |
| `Iterator`, `Iterable`, for-each su una classe scritta da noi | cap. 12, §12.4.1-§12.4.3 e secondo scheletro |
| Togliere durante la scansione, `ConcurrentModificationException` | cap. 12, §12.4.4 |
| Pila (LIFO), albero binario | cap. 12, §12.5 |
| `List`, `Set`, `Map`: variabile dichiarata con l'interfaccia | cap. 12, §12.6.1 |
| `LinkedList`: `addFirst`, `removeFirst`, `push`/`pop`, `peek`/`poll` | cap. 12, §12.6.2 |
| Insieme senza duplicati (`HashSet`, `TreeSet`); oggetti nostri con `equals`/`hashCode` | cap. 12, §12.6.3 e quinto scheletro |
| Mappa chiave-valore (`HashMap`, `TreeMap`): `put`, `get`, `getOrDefault`, `entrySet`; contare | cap. 12, §12.6.4 e terzo scheletro |
| Ordinare una lista: `Collections.sort`, `Comparator`, `List.sort` | cap. 12, §12.6.5 e quarto scheletro |
| Quale collezione scegliere | cap. 12, §12.6.6 |
| Le cinque parole chiave delle eccezioni, stampa nel `finally` | cap. 13, §13.7.2 e primo scheletro |
| Eccezione personalizzata controllata o non controllata | cap. 13, §13.6 e secondo scheletro |
| Conversione da checked a unchecked (rilancio incapsulato) | cap. 13, §13.4.3 e terzo scheletro |
| Chiusura classica dei flussi nel `finally` con guardia `null` | cap. 13, §13.5.3 e quarto scheletro |
| Checked contro unchecked, `throws` e overriding | cap. 13, §13.2.4 e §13.3.3 |
| Flusso, file di testo e file binario; flussi di byte contro flussi di caratteri | cap. 14, §14.1 |
| Scrivere righe in un file con `PrintWriter`; `close` e buffer | cap. 14, §14.2.1-§14.2.2 e primo scheletro |
| `FileNotFoundException` all'apertura; chiusura nel `finally` con guardia `null` | cap. 14, §14.2.4 e §14.2.6 |
| `FileWriter` e `BufferedWriter` (`write`, `newLine`) | cap. 14, §14.2.7 |
| Scrivere in coda a un file (`FileWriter(nome, true)`, `FileOutputStream(nome, true)`) | cap. 14, §14.3 e secondo scheletro |
| Leggere un file di testo riga per riga fino alla fine (`Scanner`, `hasNextLine`) | cap. 14, §14.4.1 e quarto scheletro |
| Leggere con `BufferedReader` fino a `readLine() == null` | cap. 14, §14.4.2-§14.4.3 e terzo scheletro |
| Leggere numeri da un file di testo | cap. 14, §14.4.5 |
| Classe `File`: esistenza, lunghezza, cancellazione, elenco di una cartella; percorsi relativi | cap. 14, §14.5 |
| Metodo che apre un flusso e due flussi chiusi insieme | cap. 14, §14.6 e sesto scheletro |
| File CSV: intestazione, `split`, conversione dei campi | cap. 14, §14.7 e quinto scheletro |
| Dalle parole della traccia (in coda, fino alla fine, nel `finally`) al codice dei file | cap. 14, §14.8 |
| Flusso binario e file binario contro file di testo; `ObjectOutputStream` attorno a `FileOutputStream` | cap. 15, §15.1 |
| Scrivere e leggere `int`, `double`, `boolean`, stringhe (`writeInt`, `writeUTF`, `readInt`, …) | cap. 15, §15.2-§15.3 e primo scheletro |
| Stesso ordine e stessi tipi in lettura e in scrittura | cap. 15, §15.3.2 |
| `DataOutputStream` / `DataInputStream` e file di record | cap. 15, §15.2.5 |
| Leggere dati binari fino a `EOFException` (ciclo `while (true)`, ordine dei `catch`) | cap. 15, §15.4 e secondo scheletro |
| Raddoppiare i numeri di un file in un altro file | cap. 15, §15.4.6 |
| Dal valore sentinella alla fine del file | cap. 15, §15.4.4 |
| Serializzare un oggetto: `Serializable`, `writeObject`, `readObject` e il cast | cap. 15, §15.5 e terzo scheletro |
| Campi non serializzabili, superclasse, `static` e `transient` | cap. 15, §15.6 |
| Lo stesso oggetto scritto due volte, `reset()` | cap. 15, §15.7 |
| `serialVersionUID` nella forma esatta, `InvalidClassException` | cap. 15, §15.8 e quinto scheletro |
| Serializzare un array o una collezione in un colpo | cap. 15, §15.9 |
| Leggere più oggetti fino alla fine del file; perché non si aggiunge in coda con `ObjectOutputStream` | cap. 15, §15.10 e quarto scheletro |
| File contro rete: quale flusso avvolgere («salva» contro «invia») | cap. 15, §15.11 |
| Le eccezioni della serializzazione (`NotSerializableException`, `StreamCorruptedException`, `ClassNotFoundException`) | cap. 15, §15.12 |
| Dalla frase della traccia (costante di versione, ordine dei parametri, formato di `toString`) al codice | cap. 15, §15.13 |
| Thread con `Runnable`, `start` e `join` | cap. 17 |
| Dividere un array tra più thread | cap. 17 |
| Mutua esclusione con `synchronized` | cap. 18 |
| Buffer condiviso con `wait` e `notifyAll` (produttore/consumatore) | cap. 18 |
| Client TCP che invia un messaggio | cap. 19 |
| Inviare un oggetto serializzato su un socket e leggere la risposta | cap. 19, cap. 15 (§15.5 e §15.11) |
| Client UDP che invia un datagramma e attende la risposta | cap. 19 |
| Caricare un documento XML con DOM e leggere gli elementi | cap. 20 |
| Query con `PreparedStatement` e lettura del `ResultSet` | cap. 21 |

La colonna *Dove* indicherà anche la sezione esatta man mano che i capitoli vengono scritti.
