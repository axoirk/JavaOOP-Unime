# Lacune emerse dalle simulazioni ↔ appunti

Secondo giro di `MAPPA_LACUNE.md`. Quello confrontava gli **appelli** con gli appunti (fino all'8 settembre);
questo confronta **tutte le simulazioni corrette** — le 11 della Serie 1, le 9 corrette della Serie 2 e le 2 della
Serie 3 — con gli appunti come sono oggi. Gli **appelli ufficiali** (i due sostenuti e i due ricostruiti) sono in §6. Serve a te: per ogni errore che si è ripetuto dice **dove rileggere**
oppure **che negli appunti non c'è niente da rileggere**.

Aggiornato al **31 ottobre 2026**. **Gli appunti sono stati riscritti lo stesso giorno** sui punti qui sotto: la tabella in §8 dice dove
è finita ogni lacuna. Le sezioni 2-6 descrivono lo stato *prima* della riscrittura. Fonti: i `Report_Esame_*.md` e i `Note.md` di `Exams/Simulazioni/` (locali, non
versionati), `Exams/STORICO_SIMULAZIONI.md`, `Exams/ESAMI_PASSATI.MD`, `Report_EXAM1/2/4.md` (per EXAM3 non c'è
un report: ci sono solo il README e `ESAMI_PASSATI.MD`), i sette file di `Appunti_Pratici_Livelli/` e i sei di
`Fondamenti_e_Pilastri_OOP/`. Il confronto con gli appunti è fatto cercando le parole chiave in tutti i file e
leggendo i passaggi che comparivano: "non c'è" significa "non l'ho trovato", non una garanzia assoluta.

Legenda: 🔴 assente negli appunti · 🟠 presente ma incompleto (manca la forma che serve in prova) · 🟢 presente e
corretto, l'errore è di applicazione, non di teoria.

---

## 1. Le prove, in una tabella

La Serie 1 è su altre regole (30 minuti, spesso con aiuti, in parte in IDE): i voti sono su 30 e **non si confrontano**
con gli altri. Restano utili per gli errori.

| Prova | Totale | Errore che ha pesato di più |
|---|---|---|
| S1 EXAM_1 | 19/30 | `wait()` senza `notifyAll`, `if` al posto di `while`; `readLine()` chiamato due volte |
| S1 EXAM_2 | 26/30 | `input.length()` su `null`; `if` invece di `while` attorno a `wait()` |
| S1 EXAM_3 | 20/30 | `charAt(0)` su riga vuota; `setSalarioBase()` usato come getter; `salariobase` ≠ `salarioBase` |
| S1 EXAM_4 | 27/30 | `getValore()` non `synchronized`; `"Errore di rete."` invece di `"Errore di Rete"` |
| S1 EXAM_5 | 21/30 | stringhe diverse dalla traccia; `notify()` fuori da `synchronized`; `throws` richiesto ma gestito con `try` |
| S1 EXAM_6 | 24/30 | `numbers.size()==0 \|\| numbers==null` (ordine); `throw NullPointerException;` senza `new`; `wait` in `if` |
| S1 EXAM_7 | 27/30 | sentinella senza `volatile`; stampa nel `finally` invece che nel `catch` |
| S1 EXAM_8 | 26/30 | `compareTo` decrescente con i segni invertiti |
| S1 EXAM_9 | 19/30 | `content[i]` su una `String`; contare gli spazi senza `+1`; `this.start()` nel costruttore |
| S1 EXAM_10 | 25/30 | `wait()` in `if`; `throws NumberFormatException` richiesto e omesso |
| S1 SIM_EXAM_11 | **5/31** | ES2 e ES3 a zero: foglio bianco su un `DataOutputStream`; serializzazione su stream di caratteri |
| S2 SIM_1 | 15/31 | ES2 non compila: cast `(double)` su `String`, `exists()` su `FileReader`; media con divisione intera |
| S2 SIM_2 | 21/31 | `readObject()` confrontato con `null` a fine file; flussi dichiarati dentro il `try` e chiusi nel `finally` |
| S2 SIM_3 | 5/31 | `Operario` per `Operaio`; `ricevi` senza `ServerSocket`; ES3 mai provato |
| S2 SIM_4 | 14,5/31 | serializzazione al posto del binario; `finally` che chiude `null`; deadlock AB-BA |
| S2 SIM_5 | 17,5/31 | ES2 mai eseguito; `serializableUID` al posto di `serialVersionUID` |
| S2 SIM_6 | 25,3/31 | `==` tra `String`; costruttore che assegna il campo a sé stesso; `serialversionUID` |
| S2 SIM_7 | 23/31 | eccezioni senza messaggio; buffer LIFO invece di FIFO |
| S2 SIM_8 | 26,5/31 | 7 nomi di API DOM inventati; `public` in un file con più classi |
| S2 SIM_9 | 22/31 | `start()` e `join()` nello stesso ciclo; `getCounter()` su un `Thread` |
| S2 SIM_10 | — | interrotta, mai consegnata |
| S3 SIM_1 | 14,25/31 | `throws` e nomi dei metodi non dedotti dalle classi fornite; `Map.getValue` |
| **S3 SIM_2** | **9,75/31** | ES2 mai compilato; ES3 al minuto 39; `EOFException`, `finally`, `int[][]`, `start`/`join` |

Dove stai bene, e vale la pena dirlo: **serializzazione su rete** (13/13 e 12,5/13 consecutivi, SIM_8-9),
**`synchronized`** (13/13 più volte), **`wait`/`notifyAll` in `while`** (nella Serie 1 `if` al posto di `while` quattro volte; nelle
prove della Serie 2 che lo richiedevano, SIM_2 e SIM_7, è sempre corretto), interfacce e classi astratte (5/5 quasi sempre).

---

## 2. Cosa non è negli appunti (🔴 e 🟠): rileggi qui, e poi esercitati

Ordinati per quante volte l'errore è tornato e per quanto è costato. Per ognuno: cosa è successo, cosa dicono oggi
gli appunti, che cosa manca.

### 2.1 🔴 Fine file: `EOFException` (e perché `readObject()` non dà `null`)

- **Errori:** S2 SIM_2 (`while ((x = (Libro) ois.readObject()) != null)`, lettura azzerata); S3 SIM_2 (`// non ricordo`
  proprio su `temperaturaMassima`); SIM_EXAM_11 (ES2 foglio bianco). In S2 SIM_4 invece la lettura fino a fine file è
  uscita giusta: c'è chi la sa, ma non è fissata.
- **Appunti:** la parola `EOFException` **non compare in nessun file**. L4 mostra `DataInputStream` e
  `ObjectInputStream` che leggono **un solo record**, senza ciclo (`Appunti-Livello-4`, §"File binario" righe 263-272;
  riga 207 per l'oggetto). La fine file è spiegata solo per i file di testo (`readLine() != null`, L4 riga 107) e per i
  socket di testo (L6 riga 88).
- **Manca:** il ciclo di lettura di *quanti record ci sono, non lo so*:

```java
try {
    while (true) {                    // nessun hasNext(): si legge finché il flusso non finisce
        in.readUTF(); in.readInt(); double t = in.readDouble();
    }
} catch (EOFException fine) {         // fine file = eccezione, non null, non -1
    // uscita normale dal ciclo
}
```

  Stessa idea con `readObject()` (che dichiara anche `ClassNotFoundException`). `readLine()` dà `null`; `read()`
  dà `-1`; `readUTF`/`readInt`/`readDouble`/`readObject` **lanciano** `EOFException`. Sono tre convenzioni diverse.

### 2.2 🔴 Aprire un file in scrittura lo svuota: append e controlli prima di aprire

- **Errori:** S3 SIM_2 ES2: `new FileOutputStream(path)` senza `true` (non accoda) e controllo dell'ora **dopo**
  l'apertura (la misurazione rifiutata lascia comunque il file vuoto).
- **Appunti:** L4 riga 85-86 mostra l'append **solo con `FileWriter(path, true)`**. Per `FileOutputStream` (quello che
  si usa col binario) non c'è, e non c'è mai scritto che `new FileOutputStream(path)` / `new FileWriter(path)` **tronca
  il file nel momento in cui lo apri**, prima di qualunque `write`.
- **Manca:** due regole. `FileOutputStream(path, true)` accoda. **Si valida prima di aprire il flusso**, mai dentro
  il `try` dopo l'apertura, quando la traccia dice "il file resta invariato".

### 2.3 🟠 `finally` scritto a mano per chiudere i flussi

- **Errori:** S2 SIM_2 (flussi dichiarati dentro il `try`, `cannot find symbol` nel `finally`); S2 SIM_3 (stesso);
  S2 SIM_4 (`ois.close()` su `null` dentro il `finally` sovrascrive il `return` del `catch`); S3 SIM_2 (try-with-resources
  al posto del `finally` richiesto: requisito azzerato, 2 punti).
- **Appunti:** L3 §5 spiega `finally` con una divisione per zero e dice che il try-with-resources "non lo sostituisce
  agli occhi del correttore" (riga 374). **Non c'è nessun esempio di `finally` che chiude un flusso.** Quindi la forma
  che la traccia pretende ("la chiusura dei flussi deve avvenire nel blocco `finally`") non l'hai mai vista scritta.
- **Manca:** la forma, che è sempre questa:

```java
DataOutputStream out = null;                       // 1. dichiarato FUORI dal try
try {
    out = new DataOutputStream(new FileOutputStream(path, true));   // 2. assegnato dentro
    out.writeUTF(nome);
} finally {
    if (out != null) {                             // 3. se l'apertura è fallita, out è ancora null
        out.close();                               // 4. close() dichiara IOException: il metodo ha throws IOException
    }
}
```

  Tre errori compilano o girano male in tre modi diversi: variabile dentro il `try` (non compila), `close()` senza
  controllo `null` (`NullPointerException` che copre l'eccezione vera), `close()` senza `throws IOException` (non compila).

### 2.4 🔴 Deduzione delle firme dal codice fornito (variante B)

- **Errori:** SIM_EXAM_11 (`getValore()` `int` al posto di `double`); S2 SIM_4 (`leggiProdotti` invece di `leggi`);
  S3 SIM_1 ES2 (`throws` mancanti: erano nei `catch` di `Promemoria`), ES3 (`getSchedeNulle()` invece di `nulle()`,
  `totale()` assente). È il pattern che ha prodotto i due zero-compilazione di S3 SIM_1.
- **Appunti:** la parola "dedurre" non compare. Nessun appunto spiega **come si legge il codice di un altro** per
  ricavarne le firme.
- **Manca:** la tabella di lettura. Tutto quello che serve sta già nel codice fornito:

| Nel codice fornito vedi | Ne ricavi |
|---|---|
| `x.nome(a, b)` | il **nome esatto** del metodo, il numero e il tipo dei parametri |
| `double s = x.nome()` | il **tipo di ritorno** (e `int` non basta: `lossy conversion`) |
| `new X(a, b)` | la firma del **costruttore**, nell'ordine dato |
| `catch (E e)` attorno alla chiamata | il metodo **dichiara `throws E`** (controllata: ha senso solo se può lanciarla) |
| `x.nome()` usato come istruzione | probabilmente `void` |
| il campo usato in un'espressione | il tipo (`somma += x.get()` con `somma` `double` → `get` restituisce numero) |

  Regola: **il nome si copia, non si "adatta"**. Prima di scrivere il corpo di un metodo dedotto, rileggi la riga
  che lo chiama.

### 2.5 🟠 Eccezioni controllate delle API: quali metodi le lanciano

- **Errori:** SIM_EXAM_1 (`throw new InterruptedException(e)`); S2 SIM_1 (`new FileReader()` fuori dal `try`);
  S2 SIM_2 ES3: cinque run in tutto, due sulle eccezioni controllate (`unreported exception InterruptedException`,
  poi `exception ... is never thrown in body of try`); S2 SIM_4 (`close()`);
  S3 SIM_1 ES2 (cinque run su `unreported exception`); S3 SIM_2 ES2 (`throws OraNonValidaException` dove serviva
  `IOException`).
- **Appunti:** gli esempi ci sono (L5 §3 con `InterruptedException`; L4 con `IOException`; L4 riga 338 con
  `ClassNotFoundException`), ma **nessuna tabella**, e i due messaggi del compilatore (`unreported exception X; must be
  caught or declared to be thrown`, `exception X is never thrown in body of corresponding try statement`) **non
  compaiono**.
- **Manca:** una tabella che dica chi lancia cosa, da sapere a memoria:

| Chiamata | Eccezione controllata |
|---|---|
| `Thread.sleep`, `wait`, `join` | `InterruptedException` |
| `new FileReader/FileInputStream/FileOutputStream/PrintWriter(path)` | `FileNotFoundException` (è una `IOException`) |
| `readLine`, `write*`, `read*`, `close` su flussi | `IOException` |
| `readUTF/readInt/...` a fine file | `EOFException` (sottoclasse di `IOException`) |
| `readObject` | `IOException` **e** `ClassNotFoundException` |
| `new Socket`, `accept`, `getInputStream` | `IOException` |
| `parse`, `newDocumentBuilder` (DOM) | `ParserConfigurationException`, `SAXException`, `IOException` |

  E le due letture degli errori: **`unreported exception`** = manca `throws` o `catch`; **`is never thrown in body of
  try`** = hai scritto un `catch` per un'eccezione che nel `try` nessuno lancia. Se il codice fornito ha un `catch (E)`,
  vedi 2.4: il `throws E` è dall'altra parte.

### 2.6 🟠 `Runnable` + `Thread`: due array, e `join()` su una matrice

- **Errori:** S2 SIM_9 (`ArrayList<Thread>` poi `getCounter()`, `start()`+`join()` nello stesso `for`, partizionamento
  con `while`); S3 SIM_2 (un solo `Thread` creato, niente `start`/`join`, `int[]` al posto di `int[][]`).
- **Appunti:** L5 §3 spiega bene "un ciclo che avvia, un ciclo che aspetta" e l'array del **tipo concreto**, ma sempre
  con `extends Thread`. La forma che hai scelto tu tutte le volte è `implements Runnable` + `new Thread(...)`: lì i due
  oggetti (il lavoro e il thread) sono **due** e vanno tenuti in **due array paralleli**. Non è nei file. Non ci sono
  neanche array bidimensionali (vedi 2.7).
- **Manca:**

```java
Reparto[] reparti = new Reparto[righe.length];
Thread[]  thread  = new Thread[righe.length];
for (int i = 0; i < righe.length; i++) {          // ciclo 1: crea e AVVIA tutti
    reparti[i] = new Reparto(righe[i], min, max);
    thread[i]  = new Thread(reparti[i]);
    thread[i].start();
}
for (int i = 0; i < righe.length; i++) {          // ciclo 2: aspetta, poi legge il parziale
    try { thread[i].join(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    parziali[i] = reparti[i].getFuori();          // getFuori sta su Reparto, non su Thread
}
```

  Per il partizionamento di un array fra `n` thread: `passo = lunghezza / n`; l'ultimo prende il resto
  (`fine = (i == n-1) ? lunghezza : (i+1)*passo`); un `for` su `i`, non un `while` su un indice (con `n = 1` il
  `while` non gira mai: SIM_9).

### 2.7 🔴 Array bidimensionali

- **Errori:** S3 SIM_2 ES3 (`esamina(int[] ...)` al posto di `int[][]`: il tester non trova il metodo).
- **Appunti:** `int[][]`, "matrice" e "righe di lunghezza diversa" **non compaiono mai**. L1 arriva solo agli array
  monodimensionali (§5).
- **Manca:** `int[][] m = new int[3][]; m[0] = new int[]{8,12,25,10};` — una matrice è **un array di array**; `m.length` è
  il numero di righe; `m[i].length` la lunghezza **di quella riga** (può essere 0, e può essere diversa dalle altre);
  `for (int[] riga : m)`.

### 2.8 🔴 Formattare un `double`: `18.5`, non `18.50` né `18,50`

- **Errori:** S3 SIM_2 ES2 (`String.format("%.2f")` dove la traccia mostrava `18.5`; con locale italiano stampa
  `18,50`). Collegato: S1 EXAM_4, 5, 7, 10 e S3 SIM_1 (stringhe diverse dalla traccia di una lettera o di un punto).
- **Appunti:** L1 riga 27 ha un `printf("%.2f")` e basta. Non c'è scritto che `"" + 18.5` e `String.valueOf(18.5)` danno
  `18.5` (la forma di `Double.toString`) e `%.2f` **sempre** due decimali, con la **virgola** su una JVM in locale
  italiano.
- **Manca:** regola: se l'esempio della traccia mostra `18.5` o `24.0`, il valore si concatena; `%.2f` solo se la
  traccia mostra due decimali. Nel dubbio il confronto è con l'**esempio di output** della traccia, carattere per carattere.

### 2.9 🟠 Un unico file: `public` e classi annidate `private`

- **Errori:** S2 SIM_8 (`public class Biblioteca` in un file che ne ha già una: `class X is public, should be declared in
  a file named X.java`); S3 SIM_2 ES1 (`private class Lettore`, mentre la traccia usa `p.new Lettore()` dal `main`).
- **Appunti:** L2 §4 ha un esempio di inner class `private` (`Smartwatch`/`Batteria`, righe 340-372) senza dire che
  **fuori dalla classe esterna non si può fare `p.new Batteria()`**. La sezione "Errori comuni" (riga 399) non lo
  elenca. La regola dell'appello "tutte le classi in un unico file, senza `public`" non compare in nessun appunto
  (è solo in `CLAUDE.md` e nelle regole d'esame).
- **Manca:** due righe. All'appello nessuna classe è `public` (il file ne può avere al più una, col nome del file). Una
  inner class che la traccia **crea dal main** (`p.new Lettore()`) non va dichiarata `private`: senza modificatore, o
  `public`.

### 2.10 🔴 Valori iniziali e casi limite negli algoritmi su array e stringhe

- **Errori:** S2 SIM_2 (`int max = 0` sbaglia sui negativi; `if (length > 1) ... else return 0` scarta l'array di un
  elemento); S2 SIM_1 (`summ / i` fra `int`: divisione intera, 27,0 al posto di 27,5); S1 EXAM_2, EXAM_6 (`null`
  controllato dopo `.size()`; vuoto confuso con `null`); S1 EXAM_3 (`charAt(0)` su riga vuota); S1 EXAM_9 (spazi contati,
  parole = spazi + 1); S3 SIM_1 (`length() == 0` non rifiuta `"   "`).
- **Appunti:** non trovo né la divisione intera (`(double)` non compare), né `StringIndexOutOfBoundsException`, né
  `Integer.MIN_VALUE` / "parti dal primo elemento", né l'ordine dei controlli `null`. `Fondamenti/02` spiega cos'è
  `null` e la `NullPointerException`, non come si scrive il controllo.
- **Manca:** una lista breve di casi da controllare prima di consegnare un metodo che lavora su dati: **`null`**
  (sempre per primo: `a == null || a.size() == 0`), **vuoto**, **un elemento**, **tutti uguali**, **tutti negativi**,
  **soli spazi** (`trim().isEmpty()`), **riga vuota** (`startsWith` invece di `charAt(0)`), e: due `int` che si
  dividono danno un `int`, anche se lo metti in un `double`.

### 2.11 🟢→🟠 `readLine()` chiamato due volte consuma due righe

- **Errore:** S1 EXAM_1 (`if (reader.readLine() != null) riga = reader.readLine();`).
- **Appunti:** il ciclo giusto c'è (L4 riga 107). Manca il "perché": **ogni** chiamata avanza di una riga, quindi
  `readLine()` si chiama una volta sola e si guarda il risultato.

---

## 3. Cosa è negli appunti (🟢): non serve rileggere la teoria, serve fissarla

Qui l'errore è tornato **nonostante** gli appunti. Rileggere non basta: serve scrivere a memoria la forma, senza guardare.

| Errore | Dove è tornato | Dove sta negli appunti | Stato |
|---|---|---|---|
| `wait()` dentro un `if` | S1 EXAM_1, 2, 6, 10 | L5 §2 (tre ragioni del `while`) | **risolto**: `while` corretto in S1 EXAM_8 e nelle due prove S2 che lo richiedevano (SIM_2, SIM_7) |
| `start()` e `join()` nello stesso `for` | S2 SIM_9 | L5 §3, righe 389-399 | in S3 SIM_2 non c'era nemmeno lo `start` → vedi 2.6 |
| `volatile` sulla sentinella | S1 EXAM_7 | L5 righe 145-152 | non ricomparso |
| `compareTo` decrescente | S1 EXAM_8 | L3 §"Regole matematiche" | non ricomparso |
| `==` tra `String` | S2 SIM_6 | L2 riga 114 | non ricomparso |
| Campo mai assegnato (`capienza = capienza`; parametro con nome diverso dal campo) | S2 SIM_6 | L5 riga 473, `Fondamenti/05` §Shadowing | non ricomparso |
| `serialVersionUID` scritto esatto | S2 SIM_5, SIM_6 | L4, §Serializzazione attraverso la rete | **risolto** (SIM_8-9) |
| Serializzazione sul mezzo giusto (socket, non file) | EXAM3, S1 SIM 11, S2 SIM_3 | L4 §Serializzazione attraverso la Rete | **risolto** (SIM_5, 6, 8, 9) |
| `ServerSocket`/`accept()` per ricevere | S2 SIM_3 | L6 | risolto dalle prove successive |
| `String` non è un array (`content[i]`) | S1 EXAM_9 | L1 §6, riga 179 | non ricomparso |
| Getter non `synchronized` | S1 EXAM_4 | L5 riga 322 | non ricomparso |
| `start()` nel costruttore del thread | S1 EXAM_3, EXAM_9 | L5 righe 44-49 | **gli appunti insegnano il contrario**: presentano `this.start()` nel costruttore come "pattern elegante". Il correttore l'ha penalizzato due volte; la regola "il chiamante decide quando fare `start()`" non è scritta |
| LIFO contro FIFO | S2 SIM_7 | L5 riga 379 | non ricomparso |
| Deadlock AB-BA | S2 SIM_4 | L5 riga 476 (una riga) | solo nominato: manca l'esempio con i lock presi **in ordine di id** su entrambi gli oggetti. È l'unico punto 🟠 di concorrenza che non ho messo in §2 perché è comparso una volta sola |
| Throw: `new`, messaggio nel costruttore | S1 EXAM_6, S2 SIM_7 | L3 §5 | non ricomparso |
| Nomi di API DOM | S2 SIM_8 | L6 §DOM (righe 400-421) | gli esempi ci sono tutti; l'errore è stato aver inventato i nomi per analogia. Vedi §4 |

**Una nota sull'esempio di L5.** `Appunti-Livello-5-JVM-Thread.md` righe 44-49 presenta come "pattern elegante" un thread
che chiama `this.start()` nel costruttore. Gli errori S1 EXAM_3 e S1 EXAM_9 sono entrambi questo (avvio doppio, e il
thread che gira prima che l'oggetto sia completo). Se vuoi correggere un appunto per primo, è questo: **non
fidarti di quel paragrafo**.

---

## 4. Cosa non è teoria: le tre abitudini che costano più punti

Queste non si leggono. Hanno prodotto più zeri di tutte le lacune sopra messe insieme.

### 4.1 Il compilatore usato tardi

| Prova | Primo run sull'esercizio che poi è andato a zero o quasi |
|---|---|
| **Appello EXAM4 (08/09, sostenuto)** | secondo il tuo racconto: errori che il primo Esegui avrebbe mostrato in tutti e tre gli esercizi (stima 14,5/31, il file consegnato non c'è) |
| S1 SIM_EXAM_11 | ES2: zero run, ES3: zero run |
| S2 SIM_1 | ES2: minuto 26 su 31 (diciotto minuti di scrittura al buio) |
| S2 SIM_3 | ES3: zero run |
| S2 SIM_5 | ES2: zero run |
| S3 SIM_1 | ES3: minuto 33 |
| S3 SIM_2 | ES2: zero run; ES3: minuto 39 su 39:36 consegnati |

Nelle prove in cui questo è successo, il punteggio medio è **sotto 15/31**. Su ES1 invece si bruciano 4-5 run per
refusi (S3 SIM_2: quattro su cinque). Il compilatore è l'unico controllo che hai: va usato **sulla prima classe scritta**,
anche mezza, per un run solo.

### 4.2 I refusi da blocco note

Li ha trovati tutti il compilatore o il tester, nessuno la rilettura. Sono sempre le stesse otto famiglie:

| Famiglia | Esempi veri |
|---|---|
| Manca una parola o un segno | `private Lettore {` senza `class` · `prossimo {` senza `()` · `oos.flush;` · `)` dopo `ora` · `+` in `"..." misura` · `;` finale · tipo di ritorno di `getFuori()` · `new` in `throw NullPointerException;` |
| `,` al posto di `;` | `for (i = 0; i < n, i++)` |
| Virgolette non chiuse | `return "Fine Playlist;` |
| Nome di API sbagliato per una lettera | `getOutpustStream` · `ObjectOuputStream` · `readline` · `writeDobule` · `InterruptedExpcetion` · `RuntimeExcpetion` · `newIstance` |
| Nome di classe o metodo diverso dalla traccia | `Operario`/`Operaio` · `aggiung`/`aggiungi` · `calcoloTassa`/`calcolaTassa` · `Analizztore` · `leggiProdotti`/`leggi` |
| Maiuscole | `Public` · `salariobase` · `serialversionUID` · `Fine Playlist` |
| Variabile locale | usata senza valore iniziale (`might not have been initialized`) · metodo senza `return` finale (`missing return`) · nome diverso tra dichiarazione e uso (`riga`/`line`, `count`/`counter`) |
| Nome inventato per analogia | `exists()` su `FileReader` · `Map.getValue` · `Collection.sort` · `getElementByTagName` · `Integer.parseInt` su un `char` |

**Controllo di 60 secondi, prima di ogni Esegui:** (1) ogni metodo ha tipo di ritorno e `()`; (2) ogni `for` ha due `;`;
(3) ogni stringa ha due virgolette; (4) ogni nome **che compare nella traccia** (classe, metodo, messaggio, formato)
è copiato, non riscritto; (5) ogni nome di API lo scrivi come lo scriveresti in un esempio che hai davanti — se non
ricordi l'iniziale `get`/`set`/`is`, apri la riga che l'ha già usato.

### 4.3 Le stringhe e i formati della traccia

S1 EXAM_4, 5, 7, 10; S3 SIM_1 (`voce vuota` in minuscolo); S3 SIM_2 (`18.5`). Sono **sempre** una lettera, un punto,
una maiuscola: `Errore di Rete` ≠ `Errore di rete.`. La traccia mostra l'output atteso: confrontalo **carattere per
carattere**, non a occhio.

---

## 5. Cosa rileggere, nell'ordine

1. **L4** `Appunti-Livello-4-Dati-IO-GUI.md` §"File binario" (righe 248-285): poi scrivi a mano, senza guardare, il ciclo
   di lettura con `EOFException` (2.1), l'apertura in append (2.2) e il `finally` con `if (x != null) x.close()` (2.3).
2. **L3** `Appunti-Livello-3-OOP-Avanzata.md` §5 (righe 215-340): aggiungi alla riga "try-with-resources" la forma
   `finally` della 2.3, e la tabella di 2.5.
3. **L5** `Appunti-Livello-5-JVM-Thread.md` §3 (righe 380-440): riscrivi lo schema `Runnable` + `Thread[]` di 2.6 su una
   **matrice** (2.7), senza guardare. Salta (o riscrivi) il paragrafo di riga 44-49: `start()` nel costruttore è il
   pattern che è stato penalizzato.
4. **L1** `Appunti-Livello-1-Basi-Programmazione.md` §5-6: aggiungi `int[][]`, la divisione fra interi e
   `trim().isEmpty()`, `startsWith` invece di `charAt(0)` (2.7, 2.10).
5. **L2** `Appunti-Livello-2-Fondamenti-OOP.md` §4, "Errori comuni" (riga 399): aggiungi `private class` e `public` in
   un file solo (2.9).
6. **Rete (§6):** L6 §UDP (righe 109-246) e client TCP di testo (righe 50-71), riscritti a memoria; poi la regola del
   file di sole classi (aggiungila a 4.2).
7. **Il metodo, non la teoria:** tabella di 2.4 per la variante B (leggi sempre il codice fornito prima di scrivere
   una riga); controllo di 4.2; primo run entro cinque minuti da quando apri un esercizio (4.1).

Fin qui sono **sette letture**, di cui quattro riguardano un solo pezzo (I/O binario e `finally`). Se hai un'ora sola:
fai 1, 3, 4.2 e UDP (6).

---

## 6. Gli appelli ufficiali

Due sostenuti (EXAM3 08/07: **16/31**, riserva, rifiutata; EXAM4 08/09: **14,5/31 stimato**, scritto non superato) e due
ricostruiti e svolti a casa in IDE (EXAM1 30/30, EXAM2 29/30: **non confrontabili**, ma gli errori sì).
`MAPPA_LACUNE.md` (§2-§4) aveva già confrontato questi errori con gli appunti e riempito i buchi. Qui li ricontrollo
con gli appunti **di oggi**.

| Appello | Errore | Negli appunti oggi | Poi, nelle simulazioni |
|---|---|---|---|
| EXAM3 ES3 (azzerato) | `ObjectOutputStream` su `FileOutputStream`, non sul socket | 🟢 L4 §Serializzazione attraverso la Rete | **risolto**: 13/13 e 12,5/13 (SIM_8-9) |
| EXAM3 ES2 (−3/−5) | stampe fuori dal `finally` | 🟢 L3 §5, "perché le tracce lo impongono" | rispettato in S2 SIM_7; **tornato** in S3 SIM_2 come `close()` fuori dal `finally` (2.3) |
| EXAM4 ES1 (8/13) | `extends Asta` al posto dell'annidamento | 🟢 L2 §4 (riscritta dopo l'appello) | **messo alla prova una volta sola**, in S3 SIM_2 ES1: struttura giusta, ma `private class` (2.9) |
| EXAM4 ES2 (4/13) | `new InetAddress(host, porta)`; niente `receive()` | 🟢 L6 §UDP, righe 109-246 (richiesta/risposta, `getByName`, `getLength`) | **mai riproposto in nessuna simulazione** |
| EXAM4 ES3 (2,5/5) | metodo statico scritto fuori da qualsiasi classe | 🔴 nessuna riga dice che un metodo non può stare al primo livello del file | mai riproposto come errore; in S3 SIM_2 `Playlist` è scritta bene |
| EXAM1 ES2 (12/13) | `"eccezzione"` invece di `"eccezione"` | non è teoria (stringhe della traccia, §4.3) | tornato più volte |
| EXAM2 ES3 (11/13) | `wait()` dentro un getter | 🟢 L5 riga 469 | non ricomparso |

Tre cose che emergono mettendoli insieme, e che le simulazioni da sole non mostrano:

**1. UDP è il buco più grosso, ed è teoria già scritta ma mai provata.** L'appunto c'è, completo (L6, richiesta/risposta con
`getAddress()`/`getPort()`). Ma `STORICO_SIMULAZIONI.md` non ha neanche una riga UDP nella copertura, e nessuno dei report che ho letto (Serie 1, 2 e 3)
l'ha mai proposto. Cioè: dopo l'appello in cui hai perso 9 punti su UDP non hai mai scritto un `ClientUDP`
sotto cronometro, se non rifacendo EXAM4 a mano. Il TCP **di testo** (EXAM2 ES2) è stato provato solo nella Serie 1
(EXAM_4 client 12/13, EXAM_7 server 13/13, settembre e prima); da allora in Serie 2-3 la rete è stata solo
serializzazione TCP. Negli appelli la rete è stata l'esercizio grosso in **tre appelli su quattro**
(EXAM2 socket di testo, EXAM3 serializzazione, EXAM4 UDP): la forma si cambia ogni volta.

**2. Il metodo statico fuori da una classe è 🔴.** Sono 2,5 punti su 5 persi per non scrivere `class X {`. Negli appunti
non c'è la regola (un file Java contiene solo classi, interfacce ed enum; metodi e campi stanno **dentro**). L1 mostra
sempre metodi dentro classi, ma non lo dice. Aggiungila alla 4.2: "prima riga di ogni esercizio: `class X {`".

**3. Il profilo degli appelli e quello delle simulazioni sono lo stesso.** Il report di EXAM4 lo dice: *nessun
esercizio perso per non saper risolvere il problema*, tutti persi per forma e completezza, e tutti e tre
errori che il primo Esegui avrebbe mostrato. È la 4.1: la lacuna dominante non è un argomento, è il momento in cui
premi Esegui.

**Cosa dare per chiuso:** serializzazione su rete, inner class (teoria), `finally` sulle stampe, `wait` nel getter.

**Cosa fare, in ordine:** (a) UDP: riscrivi `ClientUDP.inviaMessaggio` a memoria (L6 §UDP, poi `aula.py` su EXAM4 ES2);
(b) client TCP di testo con `PrintWriter(socket.getOutputStream(), true)` (L6 righe 50-71): non provato dalla Serie 1;
(c) regola del file di sole classi.

---

## 7. Cosa questa analisi non copre

- **EXAM3 non ha un report:** il quadro dell'appello di luglio viene da `ESAMI_PASSATI.MD` e dal README, non da una
  correzione riga per riga. EXAM4 è una **stima** ricostruita dal racconto, margine ±2 punti.
- **Non ho letto le soluzioni complete**, solo i report e le note: dove un report è sintetico (S2 SIM_5-9 hanno quattro
  righe per esercizio) mi fido dell'attribuzione degli errori fatta in correzione.
- **JDBC, CSV, SAX, UDP, `URL`** non sono mai comparsi nelle simulazioni. `MAPPA_LACUNE.md` §4 li elenca come scoperti
  o a bassa priorità e il quadro non è cambiato.
- **Gli appunti non sono stati modificati.** Se vuoi che aggiunga le sezioni mancanti (2.1-2.3, 2.5-2.10) agli
  appunti dei livelli 1, 3, 4 e 5, è un passaggio a parte.

---

## 8. Dove sono finite le lacune (riscrittura del 31 ottobre)

Ogni esempio di codice aggiunto è stato **compilato ed eseguito** prima di entrare negli appunti, e i blocchi sono stati
ricompilati estraendoli dai file finali. I messaggi del compilatore citati sono quelli veri, copiati dall'output.

| Lacuna | Dove | Cosa c'è ora |
|---|---|---|
| 2.1 `EOFException` | L4 §2, "Un file di record…" | ciclo `while (true)` + `catch (EOFException)` per `Data*Stream` e `readObject`; tabella delle tre convenzioni di fine flusso (`null`, `-1`, eccezione) |
| 2.2 Apertura che svuota, append | L4 §2 (dopo la lettura di testo) e `Registro` | `FileWriter/PrintWriter/FileOutputStream` troncano all'apertura; `true` per accodare; validare prima di aprire |
| 2.3 `finally` a mano | L3 §5, "`finally` che chiude i flussi a mano" | i quattro passi (fuori dal `try`, `null`, `if != null`, `throws IOException`), la variante "mai propagare", errori e conseguenze |
| 2.4 Dedurre le firme | L2 §6 | tabella "cosa vedi → cosa ne ricavi", esempio `Promemoria`/`Diario`, tre regole (nome copiato, `catch` = `throws`, messaggi dalla traccia) |
| 2.5 Eccezioni controllate delle API | L3 §5, "Quali metodi lanciano quali eccezioni" | tabella completa (verificata con `javac`), lettura dei due messaggi (`unreported…`, `is never thrown…`), `InterruptedException` quando non si può dichiarare |
| 2.6 `Runnable` + `Thread[]` | L5 §3, "Con `Runnable` i due oggetti sono due" | `Reparto[]` + `Thread[]` su una matrice, cinque punti da ricordare |
| 2.6 partizionamento | L5 §3, "Partizionare… il `for`, non il `while`" | formula con resto all'ultimo blocco, caso `n = 1`, estremo escluso |
| 2.7 `int[][]` | L1 §5 | matrici come array di array, righe di lunghezza diversa, `m[i].length`, parametro `int[][]` |
| 2.8 Formato di un `double` | L1 §7 | tabella `"" + t` / `%.2f` / `Locale.US` / `Math.round`; `%.2f` dà `18,50` |
| 2.9 `public` e `private class` | L1 §9 e L2 §4 | regole di forma dell'appello; `private` e `esterna.new Interna()`; due voci nuove in "Errori comuni" |
| 2.10 Casi limite | L1 §8 | tabella (`null` per primo, vuoto, un elemento, tutti negativi, soli spazi, riga vuota, estremi), `split` e i suoi trucchi |
| 2.10 Divisione intera, `parseInt` | L1 §7 | `(double) somma / n`, perché il cast va sul primo operando, parse al posto del cast |
| 2.11 `readLine()` una volta | L4 §2 | nota dopo l'esempio di lettura |
| §3 `start()` nel costruttore | L5 §1, Esempi 1B e 2B | **riscritti**: l'esempio sbagliato è marcato `SBAGLIATO`, accanto la forma corretta e le tre ragioni |
| §3 Deadlock AB-BA | L5 §5 | `Conto` con `id` progressivo `static`, lock annidati in ordine di `id`, provato 3 volte |
| §6 UDP: `null` su errore | L6 §1, "Trappole UDP" | tutti i fallimenti sono `IOException`; `setSoTimeout`; verificato su host inesistente e porta senza server |
| §6 Metodo fuori dalla classe | L1 §9 | regola "in un file solo classi" con i due messaggi (Java recenti e precedenti) |
| `Map.getValue`, mappa non popolata | L2 §5 | tabella dei nomi esatti di `Map`, `getValue` solo su `Map.Entry`, `Urna` che popola la mappa nel costruttore |
| Nomi inventati dell'API DOM | L6 §2, "I nomi esatti dell'API DOM" | tabella lettera per lettera, esempio completo XML → oggetti → `Collections.sort` |
| Refusi da blocco note | L1 §9 | tabella dei messaggi del compilatore e checklist di 60 secondi |

**Non toccato:** il metodo (primo Esegui entro cinque minuti, §4.1) compare in L1 §9 come regola 4, ma resta un'abitudine
da allenare, non un argomento da leggere. UDP e client TCP di testo restano da **riscrivere a memoria** sotto
cronometro (§6): gli appunti li avevano già, la lacuna era la pratica.

