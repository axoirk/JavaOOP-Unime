# Q&A per l'esame orale — Programmazione a Oggetti (Java)

Domande e risposte per il colloquio orale, nell'ordine dei capitoli di `Teoria/`. Ogni risposta finisce con il link al paragrafo degli appunti da cui è presa: se una risposta non ti torna, apri quello.

**Come si usa:**

1. la **Parte A** contiene i temi già chiesti agli orali: si studia per prima;
2. la **Parte B** copre tutto il programma, capitolo per capitolo;
3. la **Parte C** raccoglie i confronti rapidi, quelli del tipo «che differenza c'è tra…».

Ogni risposta è divisa in tre parti:

- **Risposta**: quello che si dice a voce, in 20-40 secondi;
- **Se insiste**: il dettaglio in più, da dare se il professore chiede di approfondire;
- **Esempio**: da dettare o scrivere alla lavagna quando serve.

Un buon metodo per l'orale: definizione, poi **perché esiste** (quale problema risolve), poi un esempio. Il professore valuta più la precisione dei termini che la lunghezza.

---

## Indice

- [Parte A — Temi già chiesti agli orali](#parte-a--temi-già-chiesti-agli-orali)
- [Parte B — Tutto il programma, per capitolo](#parte-b--tutto-il-programma-per-capitolo)
  - [1-2. Java, JVM, tipi](#1-2-java-jvm-tipi)
  - [3-6. Stringhe, controllo, array, metodi](#3-6-stringhe-controllo-array-metodi)
  - [7-8. Classi, oggetti, riferimenti](#7-8-classi-oggetti-riferimenti)
  - [9-11. Ereditarietà, astrazione, classi annidate](#9-11-ereditarietà-astrazione-classi-annidate)
  - [12. Generics e collezioni](#12-generics-e-collezioni)
  - [13. Eccezioni](#13-eccezioni)
  - [14-15. File, stream binari, serializzazione](#14-15-file-stream-binari-serializzazione)
  - [16. Interfacce grafiche](#16-interfacce-grafiche)
  - [17-18. Thread e sincronizzazione](#17-18-thread-e-sincronizzazione)
  - [19. Networking](#19-networking)
  - [20. XML](#20-xml)
  - [21. JDBC](#21-jdbc)
  - [22. Ecosistema: Maven, Spring Boot, NoSQL](#22-ecosistema-maven-spring-boot-nosql)
- [Parte C — Confronti rapidi](#parte-c--confronti-rapidi)

---

## Parte A — Temi già chiesti agli orali

Domande fatte agli appelli precedenti: socket UDP; overloading e overriding; eccezioni nell'overloading e nell'overriding; JDBC; package; scope delle variabili; `final`; classi astratte; `Serializable`; file binari; `super`.

### A1. Che differenza c'è tra overloading e overriding?

**Risposta.** L'**overloading** è avere più metodi con lo **stesso nome ma parametri diversi**, per numero, tipo o ordine. Possono stare nella stessa classe o fra superclasse e sottoclasse. Quale metodo chiamare lo decide il **compilatore**, guardando i tipi dichiarati degli argomenti: è una scelta statica, a tempo di compilazione.

L'**overriding** è la **riscrittura**, in una sottoclasse, di un metodo ereditato, con la **stessa firma**. Quale versione eseguire lo decide la **JVM durante l'esecuzione**, guardando la classe effettiva dell'oggetto: è il **binding dinamico**, la base del polimorfismo.

**Se insiste.**

- Il **tipo di ritorno da solo non distingue** due overload: due metodi che differiscono solo per il ritorno non compilano.
- Non esiste un'annotazione `@Overload`. `@Override` invece si usa, e fa controllare al compilatore che stai davvero riscrivendo qualcosa.
- Regole dell'override:
  - il tipo di ritorno deve essere uguale o un **sottotipo** (ritorno covariante);
  - la visibilità **non può restringersi**: un `public` riscritto senza `public` dà l'errore *attempting to assign weaker access privileges*;
  - non si riscrivono i metodi `final`, né quelli `private` (non si ereditano), né quelli `static` (vengono solo nascosti).
- I **costruttori** si sovraccaricano, ma non si riscrivono, perché non si ereditano.

**Esempio.**
```java
class Persona { public void scrivi() { ... } }
class Studente extends Persona {
    @Override public void scrivi() { super.scrivi(); ... }   // overriding: stessa firma
    public void scrivi(String intestazione) { ... }           // overloading: parametro diverso
}
```
→ [cap. 9, §9.4.4 Overriding e overloading](09-ereditarieta-e-polimorfismo.md#944-overriding-e-overloading) · [cap. 6, §6.7 L'overloading](06-metodi.md#67-loverloading) · [§6.7.4 Il tipo di ritorno non distingue](06-metodi.md#674-il-tipo-di-ritorno-non-distingue) · [§9.4.5 Visibilità del metodo riscritto](09-ereditarieta-e-polimorfismo.md#945-la-visibilità-di-un-metodo-riscritto)

### A2. Come si comportano le eccezioni nell'overloading e nell'overriding?

**Risposta.**

- **Overloading:** **nessun vincolo**. I metodi in overload sono metodi diversi, e ognuno dichiara le eccezioni che vuole. La clausola `throws` **non fa parte della firma**, quindi due metodi che differiscono solo per il `throws` non sono un overload: è una duplicazione, e non compila.
- **Overriding:** sulle **eccezioni controllate** vale la regola «**restringere sì, allargare mai**». Il metodo riscritto può:
  - dichiarare le **stesse** eccezioni;
  - dichiararne **sottoclassi** più specifiche (per esempio `FileNotFoundException` al posto di `IOException`);
  - dichiararne **meno**, oppure **nessuna**.

  Non può dichiarare eccezioni controllate **nuove** o **più generiche**. Le **non controllate** (`RuntimeException` e sottoclassi) non hanno vincoli.

**Se insiste: il perché.** È il **principio di sostituzione** (Liskov). Un client che usa un riferimento di tipo `Base` ha scritto `catch (IOException e)`. Se una sottoclasse potesse lanciare `Exception` o `SQLException`, chiamando il metodo attraverso il riferimento `Base` uscirebbe un'eccezione che quel `catch` non prende. Il polimorfismo non sarebbe più sicuro per i tipi.

**Esempio.**
```java
class Base    { public void connetti() throws IOException { } }
class Ok1 extends Base { @Override public void connetti() throws FileNotFoundException { } } // più specifica: ok
class Ok2 extends Base { @Override public void connetti() { } }                              // nessuna: ok
class No  extends Base { @Override public void connetti() throws Exception { } }             // NON compila
// errore: overridden method does not throw Exception
```
→ [cap. 13, §13.3.3 `throws` e l'ereditarietà: la regola di overriding](13-eccezioni.md#1333-throws-e-lereditarietà-la-regola-di-overriding) · [§13.2.4 Checked contro unchecked](13-eccezioni.md#1324-checked-contro-unchecked-la-regola-doro-del-compilatore)

### A3. Qual è lo scope delle variabili: istanza, classe, parametri, locali?

**Risposta.**

| Variabile | Dove si dichiara | Quante copie | Quanto vive | Valore iniziale |
|---|---|---|---|---|
| **d'istanza** (campo) | nella classe, senza `static` | **una per oggetto** | quanto l'oggetto (nello heap) | predefinito: `0`, `false`, `null` |
| **di classe** (`static`) | nella classe, con `static` | **una sola**, condivisa da tutti gli oggetti | dal caricamento della classe alla fine del programma | predefinito |
| **parametro** | nella firma del metodo | una per ogni chiamata | per la durata della chiamata (nello stack) | il valore passato dal chiamante |
| **locale** | dentro un metodo o un blocco | una per ogni chiamata | **dalla dichiarazione alla `}`** del blocco (nello stack) | **nessuno**: va assegnata prima dell'uso |

**Se insiste.**

- Se usi una locale non assegnata, il compilatore dà *variable might not have been initialized*.
- Un parametro o una locale con lo stesso nome di un campo **nasconde** il campo (*shadowing*). Per raggiungere il campo si scrive `this.nome = nome`.
- Java passa sempre **per valore**: un parametro è una copia. Se è un riferimento si copia l'indirizzo, quindi il metodo può modificare l'oggetto ma non sostituirlo per il chiamante.
- Un metodo `static` non vede i campi d'istanza, perché non ha un `this`.
- I campi `static` si usano con il nome della classe: `Biglietto.emessi`.

→ [cap. 6, §6.2 Variabili locali e blocchi](06-metodi.md#62-variabili-locali-e-blocchi) · [cap. 4, §4.1.3 Visibilità in un blocco](04-strutture-di-controllo.md#413-la-visibilità-delle-variabili-in-un-blocco) · [cap. 6, §6.3.2 Passaggio per valore](06-metodi.md#632-il-passaggio-per-valore) · [§6.4.2 Variabili di classe e costanti](06-metodi.md#642-variabili-di-classe-e-costanti) · [cap. 7, §7.4.1 Contare gli oggetti creati](07-classi-e-oggetti.md#741-contare-gli-oggetti-creati) · [cap. 8, §8.7.1 Quanto vive una variabile locale](08-riferimenti-e-memoria.md#871-quanto-vive-una-variabile-locale)

### A4. A cosa serve `final`?

**Risposta.** `final` vuol dire «**non si può più cambiare**», e il significato preciso dipende da dove lo metti:

- **su una variabile o un campo**: si assegna **una volta sola**. Un campo `final` va assegnato nella dichiarazione o nel costruttore. `static final` è una **costante di classe**, scritta in maiuscolo (`MAX_POSTI`);
- **su un metodo**: **non si può riscrivere** nelle sottoclassi;
- **su una classe**: **non si può estendere**. `String` è `final`.

**Se insiste.**

- Un **riferimento** `final` non può puntare a un altro oggetto, ma l'oggetto stesso resta **modificabile**: `final int[] v` permette `v[0] = 5`, ma non `v = new int[3]`.
- `abstract final` è una contraddizione: `abstract` chiede di essere riscritto o esteso, `final` lo vieta.
- Errori del compilatore:
  - metodo `final` riscritto: *overridden method is final*;
  - classe `final` estesa: *cannot inherit from final*.
- Anche `Object.getClass()` è `final`.

→ [cap. 7, §7.4.2 Costanti di classe e campi `final`](07-classi-e-oggetti.md#742-costanti-di-classe-e-campi-final) · [cap. 9, §9.4.6 `final` davanti a metodi e classi](09-ereditarieta-e-polimorfismo.md#946-final-davanti-a-metodi-e-classi) · [cap. 2, §2.4 Costanti con nome](02-tipi-variabili-operatori.md#24-le-costanti-con-nome)

### A5. Che cos'è una classe astratta?

**Risposta.** È una classe dichiarata `abstract` che **non si può istanziare**: serve come base comune per le sottoclassi. Può contenere **metodi astratti**, cioè dichiarati senza corpo, che le sottoclassi concrete **devono** implementare. Ma è una classe vera: ha anche campi, costruttori e metodi completi. Si usa quando le classi hanno una relazione «**è un**» e condividono codice, ma la base non sa implementare un comportamento. Per esempio `Animale` ha `verso()`, ma solo `Cane` e `Gatto` sanno quale sia.

**Se insiste: le regole.**

- `new Animale()` dà l'errore *is abstract; cannot be instantiated*.
- Una classe astratta però è un **tipo**: `Animale a = new Cane();` è lecito, e così un array `Animale[]`.
- Un metodo astratto non ha corpo e finisce con `;`. Con le graffe si ottiene *abstract methods cannot have a body*.
- Una classe con anche un solo metodo astratto deve essere `abstract`.
- Una sottoclasse concreta implementa **tutti** i metodi astratti, altrimenti deve essere a sua volta `abstract`.
- I costruttori della classe astratta esistono e si chiamano con `super(...)`.
- Un metodo concreto della classe astratta può chiamare quello astratto: a runtime viene eseguita la versione della sottoclasse (pattern *template method*).

**Esempio** (quello dello scritto di oggi).
```java
abstract class Animale {
    private String nome;
    public Animale(String nome) { this.nome = nome; }
    public String getNome() { return nome; }
    public abstract String verso();
}
class Cane extends Animale {
    public Cane(String nome) { super(nome); }
    @Override public String verso() { return "bau"; }
}
// Animale a = new Cane("Fido"); a.verso();  -> "bau"  (binding dinamico)
```
→ [cap. 10, §10.1 Classi astratte](10-classi-astratte-e-interfacce.md#101-classi-astratte) · [§10.1.3 Le regole](10-classi-astratte-e-interfacce.md#1013-le-regole) · [§10.1.5 Metodo completo che chiama quello astratto](10-classi-astratte-e-interfacce.md#1015-il-metodo-completo-che-chiama-quello-astratto) · [§10.3 Classe astratta o interfaccia?](10-classi-astratte-e-interfacce.md#103-classe-astratta-o-interfaccia)

### A6. A cosa serve la parola chiave `super`?

**Risposta.** `super` è il riferimento alla **parte di superclasse** dell'oggetto corrente. Ha tre usi:

1. **`super(...)`** chiama il **costruttore della superclasse**, perché i costruttori non si ereditano. Deve essere la **prima istruzione** del costruttore.
2. **`super.metodo()`** chiama la versione **della superclasse** di un metodo che la sottoclasse ha riscritto. Serve a estendere un comportamento invece di riscriverlo da capo.
3. **`super.campo`** raggiunge un campo della superclasse nascosto da uno con lo stesso nome, purché non sia `private`.

**Se insiste.**

- Se non scrivi `super(...)`, il compilatore inserisce da solo `super()`, senza argomenti. Se la superclasse ha solo costruttori con parametri, non compila. È il caso di EXAM1, dove serviva `super(null, null)` nel secondo costruttore.
- `this(...)` e `super(...)` non stanno nello stesso costruttore: entrambi vogliono la prima riga.
- `super` non si usa in un metodo `static`.
- Non si concatena: `super.super.metodo()` non esiste.
- `super().metodo()` è un errore classico: `super(...)` è una chiamata al costruttore, non un oggetto.

→ [cap. 9, §9.3.1 I costruttori non si ereditano: `super(...)`](09-ereditarieta-e-polimorfismo.md#931-i-costruttori-non-si-ereditano-super) · [§9.3.2 Se non si scrive `super(...)`](09-ereditarieta-e-polimorfismo.md#932-se-non-si-scrive-super) · [§9.3.3 `this(...)` e `super(...)` non si sommano](09-ereditarieta-e-polimorfismo.md#933-this-e-super-non-si-sommano) · [§9.4.3 `super.metodo()`](09-ereditarieta-e-polimorfismo.md#943-richiamare-la-versione-della-superclasse-supermetodo)

### A7. Che cos'è l'interfaccia `Serializable`?

**Risposta.** La **serializzazione** trasforma un oggetto, **con tutti gli oggetti a cui punta**, in una sequenza di byte. Quei byte si possono salvare su file o spedire in rete, e la **deserializzazione** ricostruisce l'oggetto. `Serializable` è un'interfaccia **marcatore**: **non ha metodi**, e dichiara soltanto che gli oggetti della classe si possono serializzare. Si scrive con `ObjectOutputStream.writeObject(o)` e si legge con `(Tipo) ObjectInputStream.readObject()`, con il cast obbligatorio.

**Se insiste.**

- **Cosa non si salva**:
  - i campi **`static`**, perché appartengono alla classe e non all'oggetto;
  - i campi **`transient`**, esclusi di proposito (una password, un valore ricalcolabile).

  Alla lettura riprendono il valore predefinito: `0` o `null`.
- **`serialVersionUID`** (`private static final long serialVersionUID = 1L;`) è il numero di versione della classe. Se fra scrittura e lettura non coincide si ottiene `InvalidClassException`. Se non lo dichiari, Java lo calcola dalla struttura della classe, e cambia a ogni modifica.
- **Grafo di oggetti**: se un campo punta a un oggetto non serializzabile si ottiene `NotSerializableException`.
- **Lo stesso oggetto scritto due volte** nello stesso stream non viene riscritto: si salva un riferimento a quello già scritto.
- **Superclasse non serializzabile**: i suoi campi non vengono salvati, e alla lettura viene chiamato il suo **costruttore senza parametri**, che deve esistere.
- `readObject` lancia anche **`ClassNotFoundException`**, se la classe non è disponibile in chi legge.
- In un file serializzato **non si aggiunge in coda**: un secondo `ObjectOutputStream` scrive una seconda intestazione e il file diventa illeggibile.
- Lo stesso meccanismo funziona su file (`FileOutputStream`) e su socket (`socket.getOutputStream()`): è l'EXAM3.

→ [cap. 15, §15.5 Serializzare un oggetto](15-stream-binari-e-serializzazione.md#155-serializzare-un-oggetto) · [§15.6 Che cosa rende serializzabile una classe](15-stream-binari-e-serializzazione.md#156-che-cosa-rende-serializzabile-una-classe) · [§15.6.3 `static` e `transient`](15-stream-binari-e-serializzazione.md#1563-i-campi-static-e-i-campi-transient) · [§15.7 Lo stesso oggetto scritto due volte](15-stream-binari-e-serializzazione.md#157-lo-stesso-oggetto-scritto-due-volte) · [§15.8 `serialVersionUID`](15-stream-binari-e-serializzazione.md#158-la-costante-di-versione-serialversionuid) · [§15.10.2 Aggiungere in coda non si può](15-stream-binari-e-serializzazione.md#15102-aggiungere-in-coda-con-objectoutputstream-non-si-può) · [§15.12 Le eccezioni](15-stream-binari-e-serializzazione.md#1512-le-eccezioni-della-serializzazione)

### A8. Che cosa sono i file binari, e come si leggono e scrivono?

**Risposta.**

- Un **file di testo** contiene caratteri leggibili. Si gestisce con i flussi di **caratteri**: `Reader` e `Writer`, cioè `FileReader`, `BufferedReader`, `FileWriter` e `PrintWriter`.
- Un **file binario** contiene i valori **così come stanno in memoria**: un `int` occupa sempre 4 byte. Si gestisce con i flussi di **byte**, `InputStream` e `OutputStream`.
- Il binario è **più compatto e più veloce**, e non richiede conversioni testo↔numero. In cambio non si legge con un editor.
- Per i tipi primitivi si usano `DataOutputStream` (`writeInt`, `writeDouble`, `writeUTF`) e `DataInputStream` (`readInt`, …), avvolti intorno a `FileOutputStream` e `FileInputStream`.

**Se insiste.**

- Si rilegge **nello stesso ordine e con gli stessi tipi** della scrittura: il file non sa cosa contiene.
- La **fine del file** si riconosce dall'**`EOFException`**: si legge in un `while (true)` e si esce nel `catch (EOFException e)`. `readInt` non restituisce un valore speciale a fine file.
- `new FileOutputStream("f.dat", true)` scrive **in coda**. Senza `true` il file viene cancellato.
- I flussi si **avvolgono** uno nell'altro, ognuno aggiunge una funzione: è il pattern *decorator*.
- Si chiude nel `finally`, con il controllo `!= null`, oppure con try-with-resources.
- Eccezioni da conoscere: `FileNotFoundException` (sottoclasse di `IOException`), `EOFException` e `IOException`.

**Esempio.**
```java
DataOutputStream out = new DataOutputStream(new FileOutputStream("passi.dat", true));
out.writeUTF(giorno); out.writeInt(passi);
// lettura: while (true) { in.readUTF(); tot += in.readInt(); }  catch (EOFException e) { fine }
```
→ [cap. 14, §14.1.3 File di testo e file binari](14-file-di-testo.md#1413-file-di-testo-e-file-binari) · [§14.1.4 Flussi di caratteri e di byte](14-file-di-testo.md#1414-flussi-di-caratteri-e-flussi-di-byte) · [§14.1.5 Avvolgere un flusso](14-file-di-testo.md#1415-avvolgere-un-flusso-in-un-altro) · [cap. 15, §15.1 Dal testo ai byte](15-stream-binari-e-serializzazione.md#151-dal-testo-ai-byte) · [§15.2 Scrivere](15-stream-binari-e-serializzazione.md#152-scrivere-valori-in-un-file-binario) · [§15.3 Leggere](15-stream-binari-e-serializzazione.md#153-leggere-un-file-binario) · [§15.4 `EOFException`](15-stream-binari-e-serializzazione.md#154-la-fine-del-file-eofexception)

### A9. Come funzionano i socket UDP?

**Risposta.** UDP è un protocollo **senza connessione**: non c'è un `accept`, né un canale aperto fra le due parti. Si spediscono **datagrammi**, pacchetti indipendenti con dentro l'indirizzo e la porta del destinatario. **Non garantisce** né che arrivino, né l'ordine, né che non arrivino doppi; in cambio è **leggero e veloce**. Si usa dove una perdita è tollerabile: DNS, streaming, VoIP, giochi.

In Java servono tre classi:

- **`DatagramSocket`**, il punto di invio e ricezione. Il client lo crea senza porta, il server sulla sua porta: `new DatagramSocket(porta)`;
- **`DatagramPacket`**, la «busta». In invio si crea con `(byte[] dati, lunghezza, InetAddress, porta)`, in ricezione con `(byte[] buffer, lunghezza)`;
- **`InetAddress`**, l'indirizzo, che si ottiene con `InetAddress.getByName("host")`. Non si crea con `new`.

**Se insiste.**

- `send(p)` spedisce. `receive(p)` è **bloccante**: aspetta finché non arriva un pacchetto.
- Il testo si converte in byte con `s.getBytes()`. Al ritorno si usa `new String(p.getData(), 0, p.getLength())`, perché il buffer è più grande dei byte arrivati.
- Il server risponde al mittente leggendo **`p.getAddress()` e `p.getPort()`** dal pacchetto ricevuto.
- Se il messaggio supera il buffer, la parte in eccesso viene **troncata**.
- Si chiude con `ds.close()` nel `finally`.
- Le eccezioni sono `SocketException`, `UnknownHostException` e `IOException`.

**Esempio** (EXAM4 e lo scritto di oggi).
```java
DatagramSocket ds = new DatagramSocket();
byte[] dati = messaggio.getBytes();
ds.send(new DatagramPacket(dati, dati.length, InetAddress.getByName(host), porta));
byte[] buf = new byte[1024];
DatagramPacket r = new DatagramPacket(buf, buf.length);
ds.receive(r);                                        // bloccante
return new String(r.getData(), 0, r.getLength());
```
→ [cap. 19, §19.5 Datagrammi UDP](19-networking.md#195-datagrammi-udp) · [§19.1.3 TCP e UDP](19-networking.md#1913-due-modi-di-comunicare-tcp-e-udp) · [§19.7 Le eccezioni della rete](19-networking.md#197-le-eccezioni-della-rete)

### A10. Che cos'è JDBC e come si usa?

**Risposta.** JDBC (*Java Database Connectivity*) è l'**API standard** di Java per accedere ai **database relazionali**. Il codice è lo stesso per qualunque DBMS: cambia solo il **driver**, il traduttore fornito dal produttore come file JAR, che converte le chiamate JDBC nel protocollo di quel database. Le classi stanno in `java.sql`, mentre `javax.sql` contiene le parti opzionali (`DataSource`, i pool di connessioni).

L'architettura va dal programma all'**API JDBC**, poi al **`DriverManager`**, poi al **driver**, poi al **database**.

I **sei passi**:

1. avere il **driver** nel classpath;
2. aprire la **connessione** con `Connection c = DriverManager.getConnection(url, utente, password)`, dove l'URL è del tipo `jdbc:mysql://localhost:3306/nomedb`;
3. creare un **`Statement`** con `c.createStatement()`, oppure un **`PreparedStatement`** con `c.prepareStatement(sql)`;
4. **eseguire** il comando:
   - `executeQuery(sql)` per una **SELECT**, che restituisce un **`ResultSet`**;
   - `executeUpdate(sql)` per **INSERT, UPDATE, DELETE e CREATE**, che restituisce un **`int`**, il numero di righe toccate;
5. **scorrere** il risultato con `while (rs.next())`, leggendo le colonne con `rs.getString("nome")` o `rs.getInt(1)`;
6. **chiudere in ordine inverso**: prima il `ResultSet`, poi lo statement, poi la `Connection`. Si fa nel `finally` o con try-with-resources.

**Se insiste.**

- **I quattro tipi di driver**:
  - **I**, ponte JDBC-ODBC: storico e inefficiente, non c'è più nei JDK attuali;
  - **II**, API nativa: richiede una libreria nativa sul client;
  - **III**, middleware: un server intermedio con un protocollo di rete;
  - **IV**, *thin driver* tutto Java: parla direttamente il protocollo del database, ed è quello usato oggi.
- **`ResultSet`** è un **cursore**: parte **prima** della prima riga, e `next()` avanza e restituisce `false` alla fine. **Le colonne si contano da 1.** Il `ResultSet` è legato alla connessione: se chiudi la connessione, non puoi più leggerlo.
- **`PreparedStatement`** usa i segnaposto **`?`**, impostati con `ps.setString(1, valore)` e `ps.setInt(2, n)`. Ha due vantaggi:
  - è **precompilato**, quindi più veloce se lo ripeti;
  - è **sicuro contro la SQL injection**, perché i valori non vengono incollati nella stringa SQL.

  I `?` sostituiscono solo **valori**, non nomi di tabelle o colonne.
- **`SQLException`** è controllata: va catturata o dichiarata.
- Un tempo il driver si caricava con `Class.forName("com.mysql.cj.jdbc.Driver")`. Oggi lo carica da solo il JAR.
- Cenni: metadati (`DatabaseMetaData`, `ResultSetMetaData`), `RowSet`, `CallableStatement` per le procedure memorizzate, `DataSource` e pool di connessioni.

**Esempio.**
```java
Connection c = null; PreparedStatement ps = null; ResultSet rs = null;
try {
    c = DriverManager.getConnection(url, user, pwd);
    ps = c.prepareStatement("SELECT titolo FROM libri WHERE autore = ?");
    ps.setString(1, autore);
    rs = ps.executeQuery();
    while (rs.next()) lista.add(rs.getString("titolo"));
} catch (SQLException e) { ... }
finally { /* chiusura in ordine inverso: rs, ps, c, ciascuna con il suo controllo != null */ }
```
→ [cap. 21, §21.2 Che cos'è JDBC](21-jdbc.md#212-che-cosè-jdbc) · [§21.2.4 I quattro tipi di driver](21-jdbc.md#2124-i-quattro-tipi-di-driver) · [§21.3 La catena di oggetti](21-jdbc.md#213-la-catena-di-oggetti) · [§21.4 La connessione](21-jdbc.md#214-la-connessione) · [§21.5.2 `executeUpdate` e `executeQuery`](21-jdbc.md#2152-executeupdate-e-executequery) · [§21.6 `ResultSet`](21-jdbc.md#216-leggere-i-risultati-resultset) · [§21.7 `PreparedStatement`](21-jdbc.md#217-preparedstatement-comandi-con-parametri) · [§21.7.6 `Statement` o `PreparedStatement`?](21-jdbc.md#2176-statement-o-preparedstatement) · [§21.8 Chiudere le risorse](21-jdbc.md#218-chiudere-le-risorse) · [§21.10 Cenni](21-jdbc.md#2110-cenni-metadati-rowset-procedure-memorizzate-pool-di-connessioni)

### A11. Che cos'è un package?

**Risposta.** Un package è un **gruppo di classi con un nome**, e corrisponde a una **cartella**: il package `negozio.magazzino` sta in `negozio/magazzino/`. Serve a due cose:

- **ordinare** le classi per argomento;
- **evitare i conflitti di nome**: `java.util.Date` e `java.sql.Date` convivono perché il **nome completo** (*fully qualified name*) le distingue.

La riga `package nome;` è la **prima istruzione** del file. Seguono gli `import`, poi la classe.

**Se insiste.**

- Con `import` si scrive il nome breve di una classe di un altro package. Le classi dello **stesso** package si vedono senza `import`, e **`java.lang`** è importato in automatico.
- `import java.util.*;` importa tutte le classi del package, ma non i sottopackage.
- Se due classi hanno lo stesso nome breve, se ne importa una e l'altra si scrive per esteso.
- Il package definisce anche un **livello di accesso**: un membro **senza modificatore** è visibile solo dentro il suo package. I livelli, dal più aperto, sono `public` > `protected` > package > `private`.
- Una classe in un package si esegue con il nome completo: `java app.Vendita`.
- Per convenzione i nomi dei package si scrivono in minuscolo, spesso con il dominio rovesciato (`it.unime.progetto`).
- All'esame scritto non si mette nessuna riga `package`: le classi stanno nel package anonimo.

→ [cap. 7, §7.6 I package](07-classi-e-oggetti.md#76-i-package) · [cap. 1, §1.5 Anatomia di un primo programma (package e `import`)](01-java-e-la-jvm.md#15-anatomia-di-un-primo-programma) · [cap. 7, §7.3.6 I quattro livelli di accesso](07-classi-e-oggetti.md#736-i-quattro-livelli-di-accesso)

---

## Parte B — Tutto il programma, per capitolo

### 1-2. Java, JVM, tipi

**B0. Quali sono i principi della programmazione a oggetti?** *(È la domanda d'apertura più classica.)*
Un programma è una **collezione di oggetti che interagiscono**. Ogni oggetto ha uno **stato**, i campi, e un **comportamento**, i metodi; gli oggetti dello stesso tipo appartengono alla stessa **classe**. I principi sono tre:

- **Incapsulamento** (*information hiding*): dati e metodi chiusi in una capsula. Chi usa la classe sa *come usarla*, non *come funziona dentro*: il guidatore conosce i pedali, non il motore.
- **Ereditarietà**: le classi formano una gerarchia. Quelle in basso ereditano dalle superiori e si specializzano, aggiungendo solo il nuovo.
- **Polimorfismo**: lo stesso nome di metodo produce comportamenti diversi a seconda della classe dell'oggetto che lo esegue.

**Se insiste.** Molti testi aggiungono l'**astrazione**: si modella solo ciò che serve, separando l'interfaccia dall'implementazione, con classi astratte e interfacce.
→ [cap. 1, §1.8 Uno sguardo alla programmazione a oggetti](01-java-e-la-jvm.md#18-uno-sguardo-alla-programmazione-a-oggetti) · [cap. 7, §7.3.4 Interfaccia e implementazione](07-classi-e-oggetti.md#734-interfaccia-e-implementazione)

**B1. Che cos'è il bytecode e perché Java è portabile?**
`javac` non compila nel linguaggio macchina di un processore, ma nel **bytecode**, il linguaggio di un computer ipotetico: la **JVM**. Su ogni macchina reale una JVM esegue il bytecode, interpretandolo o compilandolo al volo con il **JIT** (*Just-In-Time*). Lo stesso `.class` gira ovunque ci sia una JVM, senza ricompilare: *write once, run anywhere*. Ogni classe produce un `.class`, il **class loader** le carica quando servono, e l'esecuzione parte da `public static void main(String[] args)`.
→ [cap. 1, §1.3 Bytecode e JVM](01-java-e-la-jvm.md#13-il-bytecode-e-la-java-virtual-machine) · [§1.4 `javac` e `java`](01-java-e-la-jvm.md#14-compilare-ed-eseguire-javac-e-java)

**B2. Come è organizzata la memoria della JVM?**
- Ogni thread ha il suo **stack**, con le variabili locali e i parametri dei metodi in corso, e il suo **program counter**.
- Lo **heap** è unico e condiviso fra i thread: contiene gli **oggetti** e gli array creati con `new`, e il **garbage collector** lo ripulisce.
- La **method area** contiene le classi caricate: campi, metodi, bytecode e campi `static`.

→ [cap. 1, §1.9 La JVM in memoria](01-java-e-la-jvm.md#19-la-jvm-in-memoria) · [cap. 8, §8.7.4 Un solo heap, più stack](08-riferimenti-e-memoria.md#874-un-solo-heap-più-stack)

**B3. Che differenza c'è fra tipi primitivi e tipi riferimento?**
- Gli **8 primitivi** (`byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`) contengono **direttamente il valore** e non hanno metodi.
- I **tipi riferimento** (classi, array, `String`, interfacce) contengono l'**indirizzo** di un oggetto che sta nello heap, oppure `null`.
- L'assegnamento copia il valore nel primo caso e il **riferimento** nel secondo: due variabili possono indicare lo stesso oggetto.

→ [cap. 2, §2.2 I tipi primitivi](02-tipi-variabili-operatori.md#22-i-tipi-primitivi) · [cap. 8, §8.1 Variabili e oggetti](08-riferimenti-e-memoria.md#81-variabili-e-oggetti-due-cose-diverse) · [§8.2 L'assegnamento copia il riferimento](08-riferimenti-e-memoria.md#82-lassegnamento-copia-il-riferimento)

**B4. Che cosa sono la conversione implicita, la promozione e il cast?**
- **Conversione implicita**: verso un tipo più ampio, senza perdita, avviene da sola (`int` → `double`).
- **Cast**: verso un tipo più stretto serve esplicitamente (`(int) 3.7`, che vale 3: tronca, non arrotonda).
- **Promozione**: in un'espressione con tipi misti si promuove al tipo più ampio.
- Trappola: `5 / 2` vale `2`, perché è una divisione intera. `(double) a / b` è giusto, `(double) (a / b)` è sbagliato.
- Da testo a numero: `Integer.parseInt(s)`, che lancia `NumberFormatException`.

→ [cap. 2, §2.6 Le conversioni tra tipi](02-tipi-variabili-operatori.md#26-le-conversioni-tra-tipi)

**B4b. Quali tipi di errore esistono?**
- **Di sintassi**: li trova il **compilatore**, per esempio un `;` mancante o un tipo sbagliato.
- **Di esecuzione**: li trova la **JVM** mentre il programma gira, e sono le eccezioni, come una divisione per zero fra interi.
- **Logici**: il programma gira ma dà un risultato sbagliato. Li rivela solo un **collaudo** con risultati noti.

Strumenti utili: seguire il programma a mano (*tracing*) e le **asserzioni** (`assert condizione;`, attive solo con `java -ea`).
→ [cap. 1, §1.7.3 Tre tipi di errore](01-java-e-la-jvm.md#173-tre-tipi-di-errore) · [cap. 4, §4.7.2 Le asserzioni](04-strutture-di-controllo.md#472-le-asserzioni)

### 3-6. Stringhe, controllo, array, metodi

**B5. Perché le stringhe si confrontano con `equals` e non con `==`?**
`String` è una **classe**: `==` confronta i **riferimenti** (stesso oggetto?), `equals` il **contenuto**. Due stringhe uguali create in modo diverso (`new`, `split`, input) sono oggetti distinti, quindi `==` dà `false`. Le stringhe sono **immutabili**: ogni «modifica» (`toUpperCase`, `+`) crea una stringa nuova. Per costruirne una pezzo per pezzo si usa `StringBuilder`.
→ [cap. 3, §3.4 Confrontare stringhe](03-stringhe-e-console.md#34-confrontare-stringhe) · [§3.1 La classe `String`](03-stringhe-e-console.md#31-la-classe-string) · [cap. 8, §8.4 `==` e `equals`](08-riferimenti-e-memoria.md#84-uguali-o-identici--e-equals)

**B5b. Come si legge l'input da tastiera?**
Con `Scanner sc = new Scanner(System.in);` e poi `nextInt()`, `nextDouble()`, `next()` (una parola) o `nextLine()` (una riga intera).

- **Trappola**: `nextLine()` subito dopo `nextInt()` restituisce una riga vuota, perché legge l'a capo rimasto nel buffer. Serve un `nextLine()` in più per consumarlo.
- Un input del tipo sbagliato lancia `InputMismatchException`.
- In uscita: `System.out.println` e `printf`/`String.format` per i formati, per esempio `%02d` o `%.2f`.

→ [cap. 3, §3.7 L'input con `Scanner`](03-stringhe-e-console.md#37-linput-da-tastiera-con-scanner) · [§3.7.3 La trappola di `nextLine`](03-stringhe-e-console.md#373-la-trappola-di-nextline-dopo-nextint) · [§3.6 L'output su console](03-stringhe-e-console.md#36-loutput-su-console)

**B6. Che differenza c'è fra `switch` e una catena di `if-else`?**
- `switch` confronta **una** espressione con valori costanti: interi, `char`, `String`, `enum`. Senza `break` si **prosegue** nel `case` successivo (*fall-through*).
- `if-else` valuta condizioni booleane qualsiasi, anche intervalli e condizioni composte.
- Un'**enum** è un tipo con un insieme fisso di valori, ed è una classe a tutti gli effetti.

→ [cap. 4, §4.3 `switch`](04-strutture-di-controllo.md#43-listruzione-switch) · [§4.4 Le enumerazioni](04-strutture-di-controllo.md#44-le-enumerazioni) · [cap. 7, §7.5 Enum come classi](07-classi-e-oggetti.md#75-le-enumerazioni-come-classi)

**B7. Che differenza c'è fra un array e un `ArrayList`?**
- L'**array** ha **dimensione fissa**, contiene primitivi o riferimenti, e la lunghezza è il campo `length`. Gli array sono oggetti.
- L'**`ArrayList`** **cresce da solo** e contiene **solo oggetti**: per gli `int` serve `Integer`, grazie all'autoboxing. La lunghezza si legge con `size()`, gli elementi con `get(i)` e `add(x)`.

Da ricordare: `v.length`, `s.length()`, `lista.size()`.
→ [cap. 5, §5.1 Che cos'è un array](05-array-e-matrici.md#51-che-cosè-un-array) · [§5.4 Gli array sono oggetti](05-array-e-matrici.md#54-gli-array-sono-oggetti) · [§5.9 Array o ArrayList?](05-array-e-matrici.md#59-array-o-arraylist)

**B8. Che differenza c'è fra metodi `static` e metodi d'istanza?**
- Un metodo **`static`** appartiene alla **classe**: si chiama con `Classe.metodo()`, senza oggetto. Non ha `this` e non vede i campi d'istanza.
- Un metodo **d'istanza** lavora su un oggetto preciso: si chiama con `oggetto.metodo()` e vede i suoi campi.
- `main` è `static` perché la JVM lo chiama prima che esista qualunque oggetto.

→ [cap. 6, §6.4 Metodi statici e d'istanza](06-metodi.md#64-metodi-statici-e-metodi-distanza)

**B9. Java passa i parametri per valore o per riferimento?**
**Sempre per valore.** Con un primitivo si copia il numero. Con un oggetto si copia il **riferimento**: il metodo può **modificare** l'oggetto (`p.setNome(...)` si vede fuori), ma se assegna al parametro un altro oggetto, il chiamante non se ne accorge. Per questo un metodo `swap(a, b)` su due oggetti non funziona.
→ [cap. 6, §6.3.2 Passaggio per valore](06-metodi.md#632-il-passaggio-per-valore) · [cap. 8, §8.5 Oggetti e parametri](08-riferimenti-e-memoria.md#85-oggetti-e-parametri-dei-metodi)

**B10. Che cosa sono le classi wrapper e l'autoboxing?**
Ogni primitivo ha una classe corrispondente: `Integer`, `Double`, `Character`, `Boolean`… Servono dove è ammesso solo un oggetto, come nelle collezioni. **Boxing e unboxing** sono automatici (`Integer x = 5; int y = x;`). Le wrapper offrono anche metodi statici come `Integer.parseInt`. Trappola: due `Integer` si confrontano con `equals`, non con `==`.
→ [cap. 6, §6.6 Le classi wrapper](06-metodi.md#66-le-classi-wrapper)

**B11. Che cos'è la ricorsione?**
È un metodo che **chiama sé stesso** su un problema più piccolo. Servono un **caso base**, che si risolve senza ricorsione, e un passo che si avvicina al caso base. Se il caso base manca, le chiamate non finiscono più e si ottiene `StackOverflowError`, perché ogni chiamata occupa un pezzo di stack.
→ [cap. 6, §6.9 La ricorsione](06-metodi.md#69-la-ricorsione)

### 7-8. Classi, oggetti, riferimenti

**B12. Che differenza c'è fra classe e oggetto?**
La **classe** è il modello: dichiara i **campi** (lo stato) e i **metodi** (il comportamento). L'**oggetto** è un'**istanza** concreta, creata con `new`: ha i suoi valori dei campi e vive nello heap.
→ [cap. 7, §7.1 Classi e oggetti](07-classi-e-oggetti.md#71-classi-e-oggetti)

**B13. Che cos'è un costruttore?**
Un metodo speciale che **ha lo stesso nome della classe**, **non ha un tipo di ritorno** (nemmeno `void`) e inizializza l'oggetto al momento della `new`.

- Se non ne scrivi nessuno, Java fornisce il **costruttore di default**, senza parametri. Appena ne scrivi uno, quello di default **sparisce**.
- I costruttori si **sovraccaricano**, e uno può chiamarne un altro con **`this(...)`**, come prima istruzione.
- Che cosa succede con `new`: si alloca l'oggetto, i campi prendono i valori predefiniti, poi si esegue il costruttore.

→ [cap. 7, §7.2 I costruttori](07-classi-e-oggetti.md#72-i-costruttori) · [§7.2.3 Il costruttore di default](07-classi-e-oggetti.md#723-il-costruttore-di-default) · [§7.2.5 `this(...)`](07-classi-e-oggetti.md#725-costruttori-che-riusano-codice-un-metodo-ausiliario-e-this) · [§7.2.7 Che cosa accade con `new`](07-classi-e-oggetti.md#727-che-cosa-accade-quando-si-scrive-new)

**B14. A cosa serve `this`?**
È il riferimento all'**oggetto corrente**. Ha due usi:

- **`this.campo`**, per distinguere un campo da un parametro con lo stesso nome;
- **`this(...)`**, per chiamare un altro costruttore della stessa classe.

Nelle classi interne, **`Esterna.this`** indica l'oggetto esterno. In un metodo `static`, `this` non esiste.
→ [cap. 7, §7.2.2 Definire un costruttore](07-classi-e-oggetti.md#722-definire-un-costruttore) · [cap. 11, §11.2.4 `this` e `Esterna.this`](11-classi-annidate.md#1124-this-e-esternathis)

**B15. Che cosa sono l'information hiding e l'incapsulamento?**
Si **nasconde lo stato** dell'oggetto, con i campi `private`, e lo si espone solo attraverso **metodi pubblici**: i getter (*accessor*) e i setter (*mutator*), che possono **validare** i dati. Così l'oggetto resta sempre coerente e l'implementazione si può cambiare senza toccare chi la usa. L'**interfaccia** di una classe (quello che si vede) è separata dalla sua **implementazione**.

**Se insiste.** Il *privacy leak*: un getter che restituisce un riferimento a un oggetto modificabile interno permette di cambiarlo dall'esterno. Si risolve restituendo una copia.
→ [cap. 7, §7.3 Information hiding e incapsulamento](07-classi-e-oggetti.md#73-information-hiding-e-incapsulamento) · [§7.3.7 Privacy leak](07-classi-e-oggetti.md#737-la-perdita-di-riservatezza-privacy-leak)

**B16. Quali sono i quattro livelli di accesso?**

| Modificatore | Stessa classe | Stesso package | Sottoclasse (altro package) | Ovunque |
|---|---|---|---|---|
| `private` | sì | no | no | no |
| (nessuno) = package | sì | sì | no | no |
| `protected` | sì | sì | sì | no |
| `public` | sì | sì | sì | sì |

→ [cap. 7, §7.3.6 I quattro livelli di accesso](07-classi-e-oggetti.md#736-i-quattro-livelli-di-accesso) · [cap. 9, §9.2 `private` e `protected`](09-ereditarieta-e-polimorfismo.md#92-che-cosa-vede-la-sottoclasse-private-e-protected)

**B17. A cosa serve `static` su un campo?**
Il campo appartiene alla **classe**, e ne esiste **una sola copia** condivisa da tutti gli oggetti. L'esempio classico è il **contatore** degli oggetti creati: `private static int emessi`, incrementato nel costruttore. `static final` è una costante.
→ [cap. 7, §7.4 Membri statici](07-classi-e-oggetti.md#74-membri-statici-nelle-classi-con-oggetti)

**B18. Che differenza c'è fra `==` ed `equals`, e perché `equals` va con `hashCode`?**
- `==` sui riferimenti dice se sono **lo stesso oggetto**.
- `equals` dice se hanno **lo stesso contenuto**, ma solo se la classe lo riscrive: quello di `Object` equivale a `==`.
- Si riscrive con la firma esatta `public boolean equals(Object o)`, con un controllo del tipo e un cast.
- **`hashCode` va riscritto insieme a `equals`**: oggetti uguali devono avere lo stesso hash, altrimenti `HashSet` e `HashMap` non li trovano.

→ [cap. 8, §8.4 `==` e `equals`](08-riferimenti-e-memoria.md#84-uguali-o-identici--e-equals) · [cap. 9, §9.7.3 `equals(Object)`](09-ereditarieta-e-polimorfismo.md#973-equalsobject-il-confronto-sul-contenuto-in-forma-definitiva) · [§9.7.4 `hashCode`](09-ereditarieta-e-polimorfismo.md#974-hashcode-va-riscritto-insieme-a-equals)

**B19. Che cos'è `null`, e quando si ottiene una `NullPointerException`?**
`null` è il riferimento che **non indica nessun oggetto**. Chiamare un metodo o leggere un campo attraverso `null` lancia una `NullPointerException`, che è non controllata.
→ [cap. 8, §8.3 `null`](08-riferimenti-e-memoria.md#83-null-la-variabile-che-non-indica-niente)

**B20. Che cos'è il garbage collector?**
In Java la memoria non si libera a mano. Quando un oggetto diventa **irraggiungibile**, cioè nessuna catena di riferimenti partendo da una variabile viva arriva a lui, il **garbage collector** lo elimina dallo heap, in un momento deciso dalla JVM. Questo evita i *dangling pointer* e la maggior parte dei *memory leak*.
→ [cap. 8, §8.7 Vita e morte degli oggetti](08-riferimenti-e-memoria.md#87-vita-e-morte-degli-oggetti) · [§8.7.3 Il garbage collector](08-riferimenti-e-memoria.md#873-il-garbage-collector)

**B21. Che differenza c'è fra copia superficiale e copia profonda?**
- `b = a` copia **il riferimento**: c'è un solo oggetto.
- Un **costruttore di copia** crea un oggetto nuovo. Se copia solo i riferimenti dei campi oggetto, la copia è **superficiale**, e i due oggetti condividono le parti interne.
- Una copia **profonda** copia anche gli oggetti interni.

→ [cap. 8, §8.6 Copiare un oggetto](08-riferimenti-e-memoria.md#86-copiare-un-oggetto)

### 9-11. Ereditarietà, astrazione, classi annidate

**B22. Che cos'è l'ereditarietà? Java ha l'ereditarietà multipla?**
Con `extends` una sottoclasse **eredita** campi e metodi della superclasse, ne aggiunge altri e ne riscrive alcuni. Esprime la relazione «**è un**» e serve a **riusare** il codice. Java ha **ereditarietà singola** fra classi (una sola superclasse), ma una classe può **implementare più interfacce**.

**Se insiste.**

- I membri `private` vengono ereditati come stato, ma la sottoclasse **non li può nominare**: passa dai getter, oppure si usa `protected`.
- I costruttori **non** si ereditano.
- Tutte le classi discendono da **`Object`**.

→ [cap. 9, §9.1 Ereditarietà](09-ereditarieta-e-polimorfismo.md#91-ereditarietà-riusare-una-classe-esistente) · [§9.1.5 Una sola superclasse](09-ereditarieta-e-polimorfismo.md#915-una-sola-superclasse) · [§9.2.1 I membri privati non si nominano](09-ereditarieta-e-polimorfismo.md#921-i-membri-privati-non-si-nominano)

**B23. Che cosa sono il polimorfismo e il binding dinamico?**
Una variabile di tipo superclasse (o interfaccia) può indicare oggetti di **qualunque sottoclasse**: `Animale a = new Gatto();`. Quando chiami un metodo riscritto, la **JVM sceglie a runtime** la versione della **classe dell'oggetto**, non del tipo della variabile: è il **binding dinamico**.

Il compilatore controlla soltanto che il metodo esista nel **tipo della variabile**. Per questo `a.metodoSoloDelGatto()` non compila senza un **cast verso il basso** `(Gatto) a`, che a runtime può fallire con `ClassCastException`; si controlla prima con `instanceof`.

Il vantaggio: un ciclo su un `Animale[]` funziona con qualunque animale, anche con quelli aggiunti in futuro.
→ [cap. 9, §9.6 Polimorfismo e binding dinamico](09-ereditarieta-e-polimorfismo.md#96-polimorfismo-e-binding-dinamico) · [§9.6.4 Compilatore contro JVM](09-ereditarieta-e-polimorfismo.md#964-che-cosa-decide-il-compilatore-e-che-cosa-decide-la-jvm) · [§9.5 «È un» e «ha un», cast verso il basso](09-ereditarieta-e-polimorfismo.md#95-compatibilità-di-tipo-è-un-e-ha-un)

**B24. Che differenza c'è fra «è un» e «ha un»?**
- **Ereditarietà**, «è un»: uno `Studente` è una `Persona`.
- **Composizione**, «ha un»: un'`Auto` ha un `Motore`, cioè ha un campo di quel tipo.

Si usa l'ereditarietà solo quando la relazione «è un» è vera.
→ [cap. 9, §9.5 Compatibilità di tipo](09-ereditarieta-e-polimorfismo.md#95-compatibilità-di-tipo-è-un-e-ha-un)

**B25. Che cos'è la classe `Object`, e quali metodi si riscrivono?**
È l'**antenata di tutte le classi**. Si riscrivono:

- **`toString()`**, chiamato quando concateni o stampi un oggetto: la versione di `Object` stampa `Classe@hash`;
- **`equals(Object)`**;
- **`hashCode()`**.

Sono metodi `public`, quindi anche la riscrittura deve essere `public`.
→ [cap. 9, §9.7 La classe `Object`](09-ereditarieta-e-polimorfismo.md#97-la-classe-object)

**B26. Che cos'è un'interfaccia?**
È un **contratto**: dichiara metodi **senza corpo**, implicitamente `public abstract`, e **costanti**, implicitamente `public static final`. Una classe la realizza con **`implements`**, e deve implementarne tutti i metodi come `public`. Una classe implementa **più interfacce**, e un'interfaccia può **estenderne** altre. Non si istanzia, ma è un **tipo**: `Figura f = new Quadrato(2);`. Esempi: `Runnable`, `Comparable`, `Serializable`, `ActionListener`.

**Se insiste (fuori dalle dispense).** Da Java 8 un'interfaccia può avere anche metodi `default` e `static` con corpo. Basta citarlo.
→ [cap. 10, §10.2 Interfacce](10-classi-astratte-e-interfacce.md#102-interfacce) · [§10.2.6 Più interfacce, `extends` insieme a `implements`](10-classi-astratte-e-interfacce.md#1026-più-interfacce-e-extends-insieme-a-implements)

**B27. Quando si usa una classe astratta e quando un'interfaccia?**

| | Classe astratta | Interfaccia |
|---|---|---|
| Si usa con | `extends`, **una sola** | `implements`, **quante si vuole** |
| Metodi con corpo | sì | no (nel programma del corso) |
| Campi d'istanza e costruttori | sì | no, solo costanti |
| Esprime | «**è un**», con codice in comune | «**sa fare**», un'abilità |

Si usa la **classe astratta** quando le classi sono parenti e condividono stato e codice. Si usa l'**interfaccia** quando classi senza parentela devono avere la stessa capacità.
→ [cap. 10, §10.3 Classe astratta o interfaccia?](10-classi-astratte-e-interfacce.md#103-classe-astratta-o-interfaccia)

**B28. Come si ordinano gli oggetti con `Comparable`?**
La classe implementa `Comparable<T>` e il metodo `public int compareTo(T altro)`, che restituisce un numero **negativo, zero o positivo** se `this` viene prima, è uguale o viene dopo. Poi si usa `Arrays.sort(array)` o `Collections.sort(lista)`. Un **`Comparator`** invece è un criterio d'ordine esterno alla classe, utile quando servono più ordinamenti.
→ [cap. 10, §10.4 `Comparable`](10-classi-astratte-e-interfacce.md#104-linterfaccia-comparable-ordinare-gli-oggetti) · [cap. 12, §12.6.5 `Comparator`](12-generics-e-collezioni.md#1265-ordinare-comparable-comparator-collectionssort)

**B29. Che cos'è una classe interna, non statica?**
È una classe dichiarata **dentro** un'altra, senza `static`. Ogni suo oggetto è **legato a un oggetto della classe esterna** e ne vede **tutti i membri, anche quelli privati**; vale anche il contrario.

- Si crea con **`esterna.new Interna(...)`**.
- Da dentro, l'oggetto esterno è **`Esterna.this`**.
- **Annidare non è ereditare**: `class Offerta extends Asta` è un'altra cosa (errore di EXAM4).

Si usa per un tipo che ha senso solo insieme all'esterna: il nodo di una lista, l'offerta di un'asta.
→ [cap. 11, §11.2 La classe interna](11-classi-annidate.md#112-la-classe-interna) · [§11.2.3 `esterna.new`](11-classi-annidate.md#1123-creare-un-oggetto-interno-new-e-esternanew) · [§11.2.6 Annidare non è ereditare](11-classi-annidate.md#1126-annidare-non-è-ereditare)

**B30. Che differenza c'è fra classe interna, annidata statica e anonima?**
- **Annidata statica** (`static class`): **non** è legata a un oggetto esterno, si crea con `new Esterna.Annidata()` e vede solo i membri `static` dell'esterna. Esempi della libreria: `Map.Entry`, `Thread.State`.
- **Anonima**: `new Tipo() { ... }`, una classe senza nome usata una volta sola, che estende una classe o implementa un'interfaccia sul momento. È il caso tipico di `Runnable` e degli `ActionListener`. Vede le variabili locali solo se sono *effectively final*.

→ [cap. 11, §11.4 Classe annidata statica](11-classi-annidate.md#114-la-classe-annidata-statica) · [§11.4.3 Interna o statica](11-classi-annidate.md#1143-interna-o-statica-come-si-sceglie) · [§11.5 Classe anonima](11-classi-annidate.md#115-la-classe-anonima)

### 12. Generics e collezioni

**B31. Che cosa sono i generics, e a cosa servono?**
Sono classi **parametriche rispetto a un tipo**: `ArrayList<String>` è una lista di sole stringhe. Il compilatore **controlla i tipi** in fase di compilazione e il cast non serve più. Senza parametro (*raw type*) si rischia una `ClassCastException` a runtime. Una classe generica si scrive `class Scatola<T> { private T contenuto; ... }`. Il parametro deve essere un tipo riferimento: si scrive `Integer`, non `int`.
→ [cap. 12, §12.2 Generics](12-generics-e-collezioni.md#122-classi-parametriche-e-generics)

**B32. Quali sono le collezioni principali?**
- **`List`** è ordinata e ammette duplicati: `ArrayList` ha accesso per indice veloce, `LinkedList` inserimenti e cancellazioni veloci.
- **`Set`** non ammette duplicati: `HashSet` non ha ordine, `TreeSet` è ordinato.
- **`Map`** associa chiavi e valori: `HashMap`, `TreeMap`.
- Si scorrono con il **for-each** oppure con un **`Iterator`** (`hasNext()`, `next()`, `remove()`).

→ [cap. 12, §12.6 Le collezioni della libreria](12-generics-e-collezioni.md#126-le-collezioni-della-libreria) · [§12.4 Gli iteratori](12-generics-e-collezioni.md#124-gli-iteratori) · [§12.3 Le liste concatenate](12-generics-e-collezioni.md#123-le-liste-concatenate)

**B32b. Che cosa sono la lista concatenata, la pila e l'albero?**
- **Lista concatenata**: una sequenza di **nodi**, ognuno con un dato e il riferimento al successivo. La lista tiene solo il riferimento alla **testa**. Inserire e togliere in testa è immediato, ma per arrivare all'elemento *i* bisogna scorrere la lista. Il nodo si scrive di solito come **classe interna privata**.
- **Pila** (*stack*): l'ultimo che entra è il primo che esce, **LIFO**. Le operazioni sono `push` e `pop`.
- **Coda** (*queue*): **FIFO**, il primo che entra è il primo che esce. È il buffer di produttore e consumatore.
- **Albero binario**: ogni nodo ha al più due figli. In un albero **di ricerca** i valori minori stanno a sinistra e i maggiori a destra, quindi la ricerca è veloce.

→ [cap. 12, §12.3.2 Il nodo e la lista](12-generics-e-collezioni.md#1232-il-nodo-e-la-lista) · [§12.5 Pila e albero](12-generics-e-collezioni.md#125-altre-strutture-collegate-la-pila-e-lalbero) · [cap. 11, §11.3 Il nodo come classe interna privata](11-classi-annidate.md#113-il-nodo-di-lista-come-classe-interna-privata)

### 13. Eccezioni

**B33. Che cos'è un'eccezione, e perché esiste?**
È un **oggetto** che rappresenta un errore e **interrompe il flusso normale**, risalendo le chiamate finché un `catch` non la gestisce. Serve a **separare il codice dell'errore da quello normale**, invece di restituire valori speciali come `-1`. Se nessuno la cattura, il programma termina e stampa lo *stack trace*.
→ [cap. 13, §13.1 L'idea di fondo](13-eccezioni.md#131-lidea-di-fondo-separare-lerrore-dal-flusso-normale)

**B34. Com'è fatta la gerarchia delle eccezioni?**
- `Throwable` è la radice. Da lei discendono:
  - **`Error`**: guasti gravi della JVM (`OutOfMemoryError`, `StackOverflowError`), che non si gestiscono;
  - **`Exception`**: gli errori dell'applicazione.
- Dentro `Exception`, le **`RuntimeException`** sono **non controllate**: `NullPointerException`, `ArithmeticException`, `ArrayIndexOutOfBoundsException`, `NumberFormatException`, `ClassCastException`. Tutte le altre sono **controllate**: `IOException`, `SQLException`, `InterruptedException`, `ClassNotFoundException`.
- Metodi di `Throwable`: `getMessage()`, `toString()`, `printStackTrace()`, `getCause()`.

→ [cap. 13, §13.2 La gerarchia](13-eccezioni.md#132-la-gerarchia-delle-eccezioni-throwable-error-exception)

**B35. Che differenza c'è fra eccezioni controllate e non controllate?**
- Le **controllate** (*checked*) obbligano a una scelta, controllata dal compilatore: **catturarle** con `try/catch` oppure **dichiararle** con `throws`. Rappresentano problemi esterni e prevedibili: un file che manca, la rete giù.
- Le **non controllate** (*unchecked*, `RuntimeException`) non hanno obbligo: di solito sono errori di programmazione, da correggere nel codice.

→ [cap. 13, §13.2.4 Checked contro unchecked](13-eccezioni.md#1324-checked-contro-unchecked-la-regola-doro-del-compilatore)

**B36. Quali sono le cinque parole chiave delle eccezioni?**
1. **`try`**: racchiude il codice che può fallire.
2. **`catch`**: la gestisce. Se ce ne sono più di uno, va **prima la più specifica**: una sottoclasse dopo la sua superclasse dà l'errore *exception has already been caught*.
3. **`finally`**: si esegue **sempre**, con o senza eccezione, anche dopo un `return`. Serve a chiudere le risorse.
4. **`throw`**: **crea e lancia** un'eccezione (`throw new X("msg")`). È un'istruzione.
5. **`throws`**: nella **firma**, **dichiara** che il metodo può lanciarla e lascia la gestione al chiamante (*passing the buck*).

**Se insiste.** Un'eccezione si può catturare e **rilanciarne** un'altra, anche convertendo una controllata in una non controllata: `catch (NumberFormatException e) { throw new ValoreErratoException(...); }`.
→ [cap. 13, §13.3 `throw` contro `throws`](13-eccezioni.md#133-lanciare-e-dichiarare-throw-contro-throws) · [§13.4 `catch` multipli e propagazione](13-eccezioni.md#134-catturare-le-eccezioni-blocchi-catch-multipli-e-propagazione) · [§13.5 `finally`](13-eccezioni.md#135-il-blocco-finally-lesecuzione-garantita-e-la-gestione-delle-risorse) · [§13.7 Le cinque parole chiave in sinergia](13-eccezioni.md#137-le-cinque-parole-chiave-in-sinergia)

**B37. Come si scrive un'eccezione personalizzata?**
Si scrive una classe che **estende `Exception`**, se deve essere controllata, oppure **`RuntimeException`**, se non controllata, con un costruttore che passa il messaggio: `super(msg)`. Una specializzazione estende la **base personalizzata**, non `Exception`, così un solo `catch` della base le prende tutte.
```java
class SaldoInsufficienteException extends Exception {
    public SaldoInsufficienteException(String msg) { super(msg); }
}
```
→ [cap. 13, §13.6 Definire le proprie eccezioni](13-eccezioni.md#136-definire-le-proprie-eccezioni-classi-personalizzate)

**B38. Che cos'è il try-with-resources?**
`try (BufferedReader br = new BufferedReader(...)) { ... }` **chiude da solo** la risorsa alla fine del blocco, anche in caso di eccezione. Funziona con ogni classe che implementa **`AutoCloseable`**. Sostituisce lo schema con `finally`, `!= null` e `close()`.
→ [cap. 13, §13.5.4 `AutoCloseable` e try-with-resources](13-eccezioni.md#1354-approfondimento-esterno-autocloseable-e-il-try-with-resources) · [cap. 21, §21.8.3](21-jdbc.md#2183-try-with-resources-la-forma-alternativa)

### 14-15. File, stream binari, serializzazione

**B39. Che cos'è uno stream, e perché i flussi si avvolgono uno nell'altro?**
Uno **stream** è un flusso **sequenziale** di dati, in ingresso (*input*) o in uscita (*output*), da o verso un file, un socket o la console. I flussi si **avvolgono**: quello interno sa dove leggere (`FileReader`), quello esterno aggiunge una funzione, come il buffer e la lettura per righe di `BufferedReader`. È il pattern *decorator*.
→ [cap. 14, §14.1 Flussi e file](14-file-di-testo.md#141-flussi-e-file) · [§14.1.5 Avvolgere un flusso](14-file-di-testo.md#1415-avvolgere-un-flusso-in-un-altro)

**B40. Come si scrive e si legge un file di testo?**
- **Scrittura**: `PrintWriter` su `FileWriter`. Con `new FileWriter(nome, true)` si scrive **in coda**.
- **Lettura**: `BufferedReader` su `FileReader`, con `while ((riga = br.readLine()) != null)`: `readLine` restituisce `null` a fine file.
- Per scomporre le righe CSV si usa `split(";")`.
- Si chiude nel `finally`. Se non chiudi un writer, il buffer può non essere scritto e il file resta vuoto.
- La classe **`File`** rappresenta un percorso: `exists()`, `delete()`, `length()`.

→ [cap. 14, §14.2 Scrivere](14-file-di-testo.md#142-scrivere-un-file-di-testo) · [§14.3 In coda](14-file-di-testo.md#143-aggiungere-in-coda-a-un-file) · [§14.4 Leggere](14-file-di-testo.md#144-leggere-un-file-di-testo) · [§14.5 `File`](14-file-di-testo.md#145-la-classe-file)

**B41. Come si salvano più oggetti in un file?**
Si salva **una collezione** (`ArrayList<Tessera>`) con un solo `writeObject`, e la si rilegge con un cast. Funziona se `ArrayList` e gli elementi sono serializzabili. In alternativa si scrivono più oggetti e si rileggono fino all'`EOFException`.
→ [cap. 15, §15.9 Array e collezioni in un colpo solo](15-stream-binari-e-serializzazione.md#159-array-e-collezioni-in-un-colpo-solo) · [§15.10 Più oggetti in un file](15-stream-binari-e-serializzazione.md#1510-più-oggetti-in-un-file)

### 16. Interfacce grafiche

**B42. Come si costruisce una finestra Swing, e come si gestiscono gli eventi?**
- Si parte da un **`JFrame`**, la finestra, a cui si aggiungono componenti: `JLabel`, `JButton`, `JTextField`, `JTextArea`, raggruppati in `JPanel`.
- Un **layout manager** li dispone: `FlowLayout`, `BorderLayout`, `GridLayout`.
- **Eventi**: il modello è a **delega**, uno schema *observer*. Un oggetto che implementa **`ActionListener`** (il metodo `actionPerformed(ActionEvent e)`) si registra sul bottone con `addActionListener`. Al clic, Swing chiama `actionPerformed`.
- Spesso il listener è una classe interna o anonima.
- Per chiudere il programma insieme alla finestra: `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)`.
- **JavaFX** è il successore di Swing: basta un cenno.

→ [cap. 16, §16.2 `JFrame` e `JLabel`](16-interfacce-grafiche.md#162-la-prima-finestra-jframe-e-jlabel) · [§16.3 Layout manager](16-interfacce-grafiche.md#163-disporre-i-componenti-i-layout-manager) · [§16.4 Pulsanti ed eventi](16-interfacce-grafiche.md#164-pulsanti-ed-eventi) · [§16.7 JavaFX](16-interfacce-grafiche.md#167-cenni-a-javafx)

### 17-18. Thread e sincronizzazione

**B43. Che cos'è un thread, e come si crea?**
Un **thread** è un flusso di esecuzione indipendente dentro lo stesso programma. Ha il suo **stack**, ma **condivide lo heap** con gli altri thread. Si crea in due modi:

1. **estendendo `Thread`** e riscrivendo `run()`;
2. **implementando `Runnable`** e passando l'oggetto a `new Thread(r)`. È il modo preferito, perché la classe resta libera di estendere un'altra classe e il compito resta separato dal meccanismo che lo esegue.

In entrambi i casi si avvia con **`start()`**, non con `run()`.
→ [cap. 17, §17.3 Creare un thread: due modi](17-thread.md#173-creare-un-thread-due-modi) · [§17.3.3 Quale scegliere](17-thread.md#1733-quale-dei-due-modi-scegliere)

**B44. Che differenza c'è fra chiamare `start()` e chiamare `run()`?**
`start()` crea il **nuovo thread**, che poi esegue `run()` in parallelo. Chiamare `run()` direttamente è una normale chiamata di metodo, eseguita **nel thread corrente**: nessun parallelismo. `start()` due volte sullo stesso thread lancia `IllegalThreadStateException`.
→ [cap. 17, §17.2 `Thread`, `run` e `start`](17-thread.md#172-la-classe-thread-run-e-start)

**B45. Qual è il ciclo di vita di un thread?**
- **new**: creato, ma non ancora avviato;
- **runnable**: dopo `start()`, pronto per l'esecuzione; **running** quando lo scheduler lo sceglie;
- **blocked**: in attesa di `sleep`, `wait`, `join`, I/O o di un lock;
- **dead**: `run()` è finito.

Nella Javadoc gli stati sono `Thread.State`: `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, `TERMINATED`, letti con `getState()`. Per **fermare** un thread si usa una **variabile sentinella `volatile`** controllata nel ciclo di `run`. `stop()` è deprecato.
→ [cap. 17, §17.4 Ciclo di vita](17-thread.md#174-il-ciclo-di-vita-di-un-thread) · [§17.4.4 La variabile sentinella](17-thread.md#1744-fermare-un-thread-la-variabile-sentinella)

**B46. Quali metodi controllano un thread?**
- `sleep(ms)` è statico e mette in pausa il thread **corrente**; lancia `InterruptedException`, che è controllata.
- **`join()`** fa **aspettare la fine** di un altro thread: il risultato si legge **dopo** il `join`.
- `isAlive()`, `yield()` (cede il turno), `setPriority()`, `getName()`, `Thread.currentThread()`.
- Si fanno **due cicli**: nel primo partono tutti i thread con `start`, nel secondo si aspettano tutti con `join`. Con `start` e `join` nello stesso ciclo, i thread girano uno alla volta.

→ [cap. 17, §17.5 I metodi che controllano un thread](17-thread.md#175-i-metodi-che-controllano-un-thread) · [§17.5.4 `join` e `isAlive`](17-thread.md#1754-attendere-un-altro-thread-join-e-isalive) · [§17.6 Più thread insieme](17-thread.md#176-più-thread-che-lavorano-insieme)

**B47. Che cos'è una race condition, e come si evita con `synchronized`?**
Due thread che modificano lo stesso dato possono **intrecciarsi**: `count++` è fatto di tre passi (leggi, somma, scrivi), e un aggiornamento va perso. La parte di codice che tocca il dato condiviso è la **sezione critica**, e va eseguita in **mutua esclusione**.

In Java **ogni oggetto ha un lock** (*monitor*):

- un metodo `synchronized` prende il lock di **`this`**: un solo thread alla volta può eseguire i metodi sincronizzati **di quell'oggetto**;
- un metodo `static synchronized` prende il lock della **classe**, e serve per i dati `static`;
- un blocco `synchronized (oggetto) { ... }` prende il lock di un oggetto scelto, per tenerlo il meno possibile.

**Se insiste.** Il lock è **dell'oggetto, non del metodo**. Un lock d'istanza non protegge un campo `static` condiviso da oggetti diversi. `synchronized` garantisce anche la **visibilità** delle modifiche fra i thread.
→ [cap. 18, §18.1 Il problema: dati condivisi](18-sincronizzazione.md#181-il-problema-dati-condivisi) · [§18.2 Mutua esclusione e lock](18-sincronizzazione.md#182-mutua-esclusione-e-lock) · [§18.3 Metodi `synchronized`](18-sincronizzazione.md#183-i-metodi-synchronized) · [§18.3.4 `static synchronized`](18-sincronizzazione.md#1834-i-metodi-static-synchronized) · [§18.4 Blocchi `synchronized`](18-sincronizzazione.md#184-i-blocchi-synchronized)

**B48. Che cos'è un deadlock?**
È uno **stallo**: due o più thread si aspettano **a vicenda**, perché ognuno tiene un lock che serve all'altro, e nessuno procede più. Il caso tipico: A prende il lock 1 e poi chiede il 2, mentre B prende il 2 e chiede l'1. Si evita prendendo i lock **sempre nello stesso ordine**.
→ [cap. 18, §18.5 Il deadlock](18-sincronizzazione.md#185-il-deadlock)

**B49. Come funzionano `wait` e `notify`, e che differenza c'è con `sleep`?**
`wait()`, `notify()` e `notifyAll()` sono metodi di **`Object`** e si chiamano **solo dentro codice `synchronized`**, altrimenti si ottiene `IllegalMonitorStateException`.

- `wait()` **rilascia il lock** e sospende il thread finché qualcuno non chiama `notify` o `notifyAll`.
- `wait` va sempre dentro un **`while`** che ricontrolla la condizione, per i risvegli spuri e perché un altro thread può arrivare prima.
- **`sleep` invece non rilascia il lock**: aspetta un tempo, non un evento.

L'esempio classico è **produttore e consumatore** su un buffer limitato: il produttore aspetta se il buffer è pieno, il consumatore se è vuoto.
→ [cap. 18, §18.6 `wait` e `notify`](18-sincronizzazione.md#186-coordinare-i-thread-wait-e-notify) · [§18.6.5 Perché `wait` va in un `while`](18-sincronizzazione.md#1865-perché-wait-va-sempre-in-un-while) · [§18.6.7 `sleep` contro `wait`](18-sincronizzazione.md#1867-sleep-contro-wait) · [§18.7 Produttore e consumatore](18-sincronizzazione.md#187-produttore-e-consumatore)

**B50. A cosa serve `volatile`?**
Garantisce che una variabile modificata da un thread sia **vista subito** dagli altri: senza `volatile`, un thread può continuare a leggere una copia vecchia. Si usa per la sentinella che ferma un thread. **Non** rende atomico `count++`: per quello serve `synchronized`.
→ [cap. 17, §17.4.4 La sentinella](17-thread.md#1744-fermare-un-thread-la-variabile-sentinella) · [cap. 18, §18.3.6 `synchronized` e visibilità](18-sincronizzazione.md#1836-synchronized-e-visibilità)

### 19. Networking

**B51. Che cosa sono client, server, indirizzo e porta?**
- Il **server** resta in ascolto su una **porta** nota; il **client** si collega all'indirizzo IP e alla porta del server.
- L'indirizzo individua la macchina, la porta il programma su quella macchina. Le porte vanno da 0 a 65535, e quelle sotto 1024 sono riservate.
- `localhost` / `127.0.0.1` è la macchina stessa.
- Le classi stanno in `java.net`.

→ [cap. 19, §19.1 Due programmi che si parlano](19-networking.md#191-due-programmi-che-si-parlano)

**B52. Che differenza c'è fra TCP e UDP?**

| | TCP | UDP |
|---|---|---|
| Connessione | sì: prima si apre una connessione, poi si comunica | no: pacchetti indipendenti |
| Affidabilità | consegna garantita, **in ordine**, senza duplicati | nessuna garanzia |
| Dati | **flusso** continuo di byte | **datagrammi** separati |
| Velocità | più lento: controlli, conferme | più veloce e leggero |
| Classi Java | `ServerSocket`, `Socket` | `DatagramSocket`, `DatagramPacket`, `InetAddress` |
| Usi | web, email, trasferimento di file, chat | DNS, streaming, VoIP, giochi |

→ [cap. 19, §19.1.3 TCP e UDP](19-networking.md#1913-due-modi-di-comunicare-tcp-e-udp) · [§19.5.8 Quello che UDP non garantisce](19-networking.md#195-datagrammi-udp)

**B53. Come si comunica con i socket TCP?**
- **Server**: `ServerSocket ss = new ServerSocket(porta);` poi `Socket s = ss.accept();`. `accept` è **bloccante** e restituisce un `Socket` collegato al client.
- **Client**: `new Socket(host, porta)`.
- Da qui i due lati sono **simmetrici**: si usano `s.getInputStream()` e `s.getOutputStream()`, avvolti in `BufferedReader` e `PrintWriter(…, true)`, dove `true` attiva l'**autoflush**.
- Si chiude il socket nel `finally`.
- Per servire **più client insieme**, un **thread per ogni client** dopo l'`accept`.

→ [cap. 19, §19.2 Socket TCP](19-networking.md#192-socket-tcp) · [§19.3 Un thread per ogni client](19-networking.md#193-un-thread-per-ogni-client)

**B54. Come si spedisce un oggetto su un socket?**
L'oggetto deve essere **`Serializable`**. Si usano `ObjectOutputStream` sul `getOutputStream()` del socket e `ObjectInputStream` sul `getInputStream()`. L'**ordine conta**: prima si crea l'output e si fa `flush()`, poi l'input, su **entrambi i lati**. Il costruttore di `ObjectInputStream` aspetta l'intestazione dell'altro lato: se entrambi aprono prima l'input, si bloccano a vicenda. Testo e oggetti non si mescolano sullo stesso socket.
→ [cap. 19, §19.4 Oggetti sulla connessione](19-networking.md#194-oggetti-sulla-connessione) · [§19.4.2 Ordine di apertura dei flussi](19-networking.md#1942-lordine-di-apertura-dei-flussi) · [cap. 15, §15.11 Lo stesso flusso, un altro mezzo](15-stream-binari-e-serializzazione.md#1511-lo-stesso-flusso-un-altro-mezzo)

**B55. Come si legge una pagina web?**
`URL url = new URL(indirizzo);` poi `url.openStream()`, avvolto in `BufferedReader(new InputStreamReader(...))`, letto riga per riga. Lancia `MalformedURLException`, sottoclasse di `IOException`.
→ [cap. 19, §19.6 Leggere una pagina web con `URL`](19-networking.md#196-leggere-una-pagina-web-con-url)

**B56. Quali eccezioni lancia la rete?**
Fanno tutte parte della famiglia di **`IOException`**:

- `UnknownHostException`: host sconosciuto;
- `ConnectException`: nessuno in ascolto;
- `SocketException`;
- `SocketTimeoutException`;
- `MalformedURLException`.

→ [cap. 19, §19.7 Le eccezioni della rete](19-networking.md#197-le-eccezioni-della-rete)

### 20. XML

**B57. Che cos'è XML?**
È un linguaggio di **marcatura** per descrivere dati strutturati con **tag** definiti dall'utente: `<film sala="1"><titolo>…</titolo></film>`.

- È **ben formato** se ha **un solo elemento radice**, tag chiusi e annidati correttamente, attributi tra virgolette e rispetta maiuscole e minuscole.
- È **valido** se rispetta anche uno schema (DTD o XSD).
- Gli **elementi** contengono testo o altri elementi; gli **attributi** stanno nel tag di apertura.

→ [cap. 20, §20.1 Che cos'è un documento XML](20-xml.md#201-che-cosè-un-documento-xml)

**B58. Che differenza c'è fra DOM e SAX?**
- **DOM** carica **tutto il documento in memoria come albero** di nodi: si naviga avanti e indietro e si può modificare, ma pesa con i file grandi.
- **SAX** è **a eventi**, a *callback*: il parser legge in sequenza e chiama i metodi di un `DefaultHandler` (`startElement`, `characters`, `endElement`). Usa poca memoria e va bene per file enormi, ma si legge solo in avanti e non si modifica.
- Entrambi fanno parte di **JAXP** e si creano con le **factory**: `DocumentBuilderFactory` e `SAXParserFactory`.
- Altre librerie da conoscere solo di nome: JDOM, DOM4J, JAXB.

**Codice DOM.**
```java
Document doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(new File(f));
doc.getDocumentElement().normalize();
NodeList nodi = doc.getElementsByTagName("film");
Element e = (Element) nodi.item(i);  e.getAttribute("sala");
e.getElementsByTagName("titolo").item(0).getTextContent();
```
→ [cap. 20, §20.2 Eventi e oggetti](20-xml.md#202-due-modi-di-leggere-eventi-e-oggetti) · [§20.3 JAXP e le factory](20-xml.md#203-jaxp-e-le-factory) · [§20.4 DOM](20-xml.md#204-dom-leggere-e-costruire-lalbero) · [§20.5 SAX](20-xml.md#205-sax-lasciare-che-sia-il-parser-a-chiamare-noi) · [§20.6 DOM o SAX?](20-xml.md#206-dom-o-sax) · [§20.7 Altre librerie](20-xml.md#207-altre-librerie)

**B58b. Come si costruisce e si salva un documento con DOM?**
- Si parte da un documento vuoto: `Document doc = builder.newDocument();`.
- Si creano i nodi con `doc.createElement("film")` e `doc.createTextNode("…")`, e si impostano gli attributi con `e.setAttribute("sala", "1")`.
- Si attaccano con `appendChild`: prima la radice al documento, poi i figli.
- Per salvare su file si usa un `Transformer`, che fa parte di JAXP.
- Da sapere: in un DOM **gli spazi bianchi fra i tag sono anch'essi nodi** (nodi di testo). Per questo si naviga con `getElementsByTagName` e si chiama `normalize()`.

→ [cap. 20, §20.4.8 Costruire e modificare](20-xml.md#2048-costruire-e-modificare-un-documento) · [§20.4.9 Salvare un documento](20-xml.md#2049-salvare-un-documento-un-cenno) · [§20.4.4 Gli spazi bianchi sono nodi](20-xml.md#2044-gli-spazi-bianchi-sono-nodi)

### 21. JDBC

La risposta completa è la [A10](#a10-che-cosè-jdbc-e-come-si-usa). Qui solo le domande collegate.

**B59. Che cos'è un database relazionale, e quale SQL serve sapere?**
I dati stanno in **tabelle**: le **righe** sono i record e le **colonne** i campi, con una **chiave primaria** che identifica ogni riga. Il SQL minimo: `CREATE TABLE`, `INSERT INTO … VALUES`, `SELECT … FROM … WHERE`, `UPDATE … SET … WHERE`, `DELETE FROM … WHERE`.
→ [cap. 21, §21.1 Un database relazionale](21-jdbc.md#211-un-database-relazionale-in-breve)

**B60. Che differenza c'è fra `executeQuery` ed `executeUpdate`?**
- `executeQuery` si usa per una **SELECT** e restituisce un `ResultSet`.
- `executeUpdate` si usa per **INSERT, UPDATE, DELETE e CREATE** e restituisce un **`int`**: le righe modificate, oppure 0 per i comandi che non toccano righe, come `CREATE`.

Usare `executeQuery` con un `UPDATE` lancia una `SQLException`.
→ [cap. 21, §21.5.2](21-jdbc.md#2152-executeupdate-e-executequery)

**B60b. Come si gestiscono i valori `NULL` e i cursori scorrevoli?**
- **Valori `NULL`**:
  - `getString` restituisce `null`;
  - `getInt` e `getDouble` restituiscono **`0`** (`getBoolean` restituisce `false`), quindi uno `0` può voler dire «zero» oppure «assente». Si distingue chiamando **`wasNull()` subito dopo** la lettura.
- **Cursori scorrevoli**: il cursore predefinito va **solo in avanti** ed è di sola lettura. Con `createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY)` si può anche tornare indietro e saltare: `previous()`, `first()`, `last()`, `absolute(n)`.
- Per leggere **una sola riga** si usa `if (rs.next())` invece del `while`.

→ [cap. 21, §21.6.5 Valori `NULL`](21-jdbc.md#2165-valori-null) · [§21.6.6 Cursori scorrevoli](21-jdbc.md#2166-cursori-scorrevoli) · [§21.6.3 Una sola riga](21-jdbc.md#2163-una-sola-riga-o-un-solo-valore)

**B61. Perché `PreparedStatement` invece di `Statement`?**
- **Sicurezza**: blocca la **SQL injection**. Con `Statement` e la concatenazione, un input come `' OR '1'='1` cambia il significato della query; con `?` resta un valore.
- **Prestazioni**: la query è **precompilata** una volta e si riusa cambiando solo i parametri.
- **Leggibilità**: niente apici e concatenazioni.

Se un `?` resta senza valore, si ottiene una `SQLException`.
→ [cap. 21, §21.7 `PreparedStatement`](21-jdbc.md#217-preparedstatement-comandi-con-parametri) · [§21.7.6 `Statement` o `PreparedStatement`?](21-jdbc.md#2176-statement-o-preparedstatement)

**B62. Perché si chiude la connessione, e in che ordine?**
Ogni connessione occupa **risorse sul server** del database, che ne accetta un numero limitato. Si chiude **in ordine inverso** rispetto all'apertura (`ResultSet`, poi statement, poi `Connection`), nel `finally` con il controllo `!= null` oppure con try-with-resources. Chiudere lo statement chiude anche il suo `ResultSet`.
→ [cap. 21, §21.4.6 Perché chiudere](21-jdbc.md#2146-perché-chiudere-la-connessione) · [§21.8 Chiudere le risorse](21-jdbc.md#218-chiudere-le-risorse)

**B63. Come si trasformano le righe di un `ResultSet` in oggetti?**
Per ogni riga del `ResultSet` si crea un oggetto Java, con `new Libro(rs.getString("titolo"), rs.getInt("anno"))`, e lo si aggiunge a un `ArrayList<Libro>`. È il passaggio dal modello **relazionale** al modello **a oggetti**.
→ [cap. 21, §21.9 Dalle righe agli oggetti](21-jdbc.md#219-dalle-righe-agli-oggetti)

### 22. Ecosistema: Maven, Spring Boot, NoSQL

**B64. Che cos'è Maven, e a cosa serve il `pom.xml`?**
Maven è uno strumento di **build automation** e di **gestione delle dipendenze**:

- impone una **struttura standard** del progetto (`src/main/java`, `src/test/java`);
- **scarica da solo le librerie** dichiarate, dal *repository* centrale verso quello locale `~/.m2`;
- compila, collauda e impacchetta il progetto in un JAR.

Il **`pom.xml`** (*Project Object Model*) descrive il progetto:

- le **coordinate** `groupId`, `artifactId`, `version`;
- le **dipendenze**;
- i **plugin**.

**Se insiste.**

- Il **ciclo di vita** passa per le **fasi** `validate`, `compile`, `test`, `package`, `verify`, `install`, `deploy`. Lanciarne una esegue anche tutte quelle precedenti.
- I comandi di tutti i giorni sono `mvn clean install` e `mvn package`.
- I **plugin** eseguono i **goal**.
- Gli **archetipi** sono modelli di progetto.

→ [cap. 22, §22.2 Maven](22-ecosistema.md#222-maven) · [§22.2.4 `pom.xml`](22-ecosistema.md#2224-il-file-pomxml) · [§22.2.8 Ciclo di vita e fasi](22-ecosistema.md#2228-il-ciclo-di-vita-e-le-fasi)

**B65. Che cos'è Spring Boot?**
È un framework per creare applicazioni Java, tipicamente **servizi web REST**, con una configurazione minima e un server integrato.

- **`@SpringBootApplication`** marca la classe principale.
- **`@RestController`** e **`@GetMapping("/percorso")`** espongono un metodo come risposta HTTP; il valore restituito diventa il corpo della risposta, spesso in JSON.
- Si basa su **inversione del controllo** e **iniezione delle dipendenze**: il framework crea gli oggetti (*bean*) e li collega fra loro.

→ [cap. 22, §22.3 Spring Boot](22-ecosistema.md#223-spring-boot) · [§22.3.7 IoC, DI, bean](22-ecosistema.md#2237-inversione-del-controllo-iniezione-delle-dipendenze-bean)

**B66. Che cosa sono i database NoSQL?**
Sono database **non relazionali**, senza tabelle rigide:

- **a documenti**, come **MongoDB**, con documenti in stile JSON;
- **per serie temporali**, come **InfluxDB**, con misure indicizzate per tempo, tipiche dei sensori e del monitoraggio.

Si scelgono per la flessibilità dello schema e per la scalabilità.
→ [cap. 22, §22.4 I database NoSQL](22-ecosistema.md#224-i-database-nosql)

---

## Parte C — Confronti rapidi

Le domande del tipo «che differenza c'è tra…» si chiudono con una frase.

| Confronto | La differenza in una riga | Appunti |
|---|---|---|
| overloading / overriding | stesso nome e parametri diversi, scelto dal compilatore / stessa firma in una sottoclasse, scelto dalla JVM | [§9.4.4](09-ereditarieta-e-polimorfismo.md#944-overriding-e-overloading) |
| `throw` / `throws` | istruzione che lancia / clausola della firma che dichiara | [§13.3](13-eccezioni.md#133-lanciare-e-dichiarare-throw-contro-throws) |
| checked / unchecked | obbligo di catturare o dichiarare / nessun obbligo (`RuntimeException`) | [§13.2.4](13-eccezioni.md#1324-checked-contro-unchecked-la-regola-doro-del-compilatore) |
| `final` / `finally` / `finalize` | non modificabile / blocco sempre eseguito / vecchio metodo chiamato dal garbage collector, deprecato | [§9.4.6](09-ereditarieta-e-polimorfismo.md#946-final-davanti-a-metodi-e-classi) · [§13.5](13-eccezioni.md#135-il-blocco-finally-lesecuzione-garantita-e-la-gestione-delle-risorse) |
| classe astratta / interfaccia | «è un», con stato e codice, se ne estende una / «sa fare», contratto, se ne implementano molte | [§10.3](10-classi-astratte-e-interfacce.md#103-classe-astratta-o-interfaccia) |
| `this` / `super` | l'oggetto corrente / la sua parte di superclasse | [§9.3](09-ereditarieta-e-polimorfismo.md#93-i-costruttori-nelle-classi-derivate) |
| `this(...)` / `super(...)` | altro costruttore della stessa classe / costruttore della superclasse; entrambi in prima riga, mai insieme | [§9.3.3](09-ereditarieta-e-polimorfismo.md#933-this-e-super-non-si-sommano) |
| `static` / d'istanza | uno per la classe / uno per ogni oggetto | [§7.4](07-classi-e-oggetti.md#74-membri-statici-nelle-classi-con-oggetti) |
| `==` / `equals` | stesso oggetto / stesso contenuto | [§8.4](08-riferimenti-e-memoria.md#84-uguali-o-identici--e-equals) |
| stack / heap | locali e parametri, uno per thread / oggetti, condiviso | [§1.9](01-java-e-la-jvm.md#19-la-jvm-in-memoria) |
| array / `ArrayList` | dimensione fissa, anche primitivi / cresce, solo oggetti | [§5.9](05-array-e-matrici.md#59-array-o-arraylist) |
| testo / binario | caratteri, `Reader` e `Writer` / byte, `InputStream` e `OutputStream` | [§14.1.3](14-file-di-testo.md#1413-file-di-testo-e-file-binari) |
| `transient` / `static` nella serializzazione | escluso di proposito / non fa parte dell'oggetto: nessuno dei due viene salvato | [§15.6.3](15-stream-binari-e-serializzazione.md#1563-i-campi-static-e-i-campi-transient) |
| `Thread` / `Runnable` | si estende la classe / si implementa l'interfaccia, preferito | [§17.3.3](17-thread.md#1733-quale-dei-due-modi-scegliere) |
| `start()` / `run()` | nuovo thread / chiamata normale nel thread corrente | [§17.2](17-thread.md#172-la-classe-thread-run-e-start) |
| `sleep` / `wait` | tiene il lock e aspetta un tempo / rilascia il lock e aspetta una `notify` | [§18.6.7](18-sincronizzazione.md#1867-sleep-contro-wait) |
| `notify` / `notifyAll` | sveglia un thread / li sveglia tutti, più sicuro | [§18.6.4](18-sincronizzazione.md#1864-notify-e-notifyall) |
| lock d'istanza / di classe | `synchronized` protegge `this` / `static synchronized` protegge la classe | [§18.3.4](18-sincronizzazione.md#1834-i-metodi-static-synchronized) |
| TCP / UDP | connessione, affidabile, flusso / senza connessione, nessuna garanzia, datagrammi | [§19.1.3](19-networking.md#1913-due-modi-di-comunicare-tcp-e-udp) |
| `ServerSocket` / `Socket` | aspetta i client con `accept` / un capo della connessione | [§19.2](19-networking.md#192-socket-tcp) |
| DOM / SAX | albero in memoria, modificabile / eventi in sequenza, poca memoria | [§20.6](20-xml.md#206-dom-o-sax) |
| `Statement` / `PreparedStatement` | SQL concatenato / segnaposto `?`, precompilato, contro la SQL injection | [§21.7.6](21-jdbc.md#2176-statement-o-preparedstatement) |
| `executeQuery` / `executeUpdate` | SELECT e `ResultSet` / INSERT, UPDATE, DELETE e `int` | [§21.5.2](21-jdbc.md#2152-executeupdate-e-executequery) |
| classe interna / annidata statica | legata a un oggetto esterno, `esterna.new` / indipendente, `new Esterna.X()` | [§11.4.3](11-classi-annidate.md#1143-interna-o-statica-come-si-sceglie) |
| `Comparable` / `Comparator` | ordine naturale, dentro la classe / criterio esterno, più criteri | [§12.6.5](12-generics-e-collezioni.md#1265-ordinare-comparable-comparator-collectionssort) |
| `List` / `Set` / `Map` | ordinata con duplicati / senza duplicati / coppie chiave-valore | [§12.6](12-generics-e-collezioni.md#126-le-collezioni-della-libreria) |
