---
materia: Programmazione a Oggetti
capitolo: 21
titolo: JDBC
livello_syllabus: 7
stato: completo
slide: ["JDBC.ppt (architettura, driver, DriverManager, Connection, Statement, ResultSet, PreparedStatement, cenni a RowSet e CallableStatement)"]
appelli: []
fonti_esterne: 10
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 21 — JDBC

## Di cosa parla questo capitolo

Nei capitoli precedenti i dati di un programma sono finiti in un **file**: righe di testo ([Capitolo 14](14-file-di-testo.md)), byte e oggetti serializzati ([Capitolo 15](15-stream-binari-e-serializzazione.md)), documenti XML ([Capitolo 20](20-xml.md)). Un file va benissimo finché i dati sono pochi e li usa un solo programma. Ma se i dati sono tanti, se devono essere cercati per criteri diversi («tutti i libri di questo autore»), se più programmi li modificano insieme, rileggere e riscrivere un intero file a ogni operazione diventa impraticabile. Per questo i dati importanti vivono in un **database relazionale**: un programma separato, il *server* del database, che li custodisce in **tabelle** e risponde a richieste scritte in un linguaggio apposito, l'**SQL**.

Il programma Java non conosce il formato interno del server e non ha bisogno di conoscerlo: **JDBC** (*Java Database Connectivity*) è la libreria standard con cui un programma Java apre una connessione con un database, gli manda comandi SQL e legge i risultati. In questo capitolo vedremo:

- che cosa è un database relazionale e quanto SQL serve per questo corso (paragrafo 21.1);
- che cosa è JDBC, come è organizzato e a che cosa servono i **driver** (paragrafo 21.2);
- la **catena di oggetti** che porta da un programma ai dati: `DriverManager`, `Connection`, `Statement`, `ResultSet` (paragrafo 21.3);
- come si **apre e si chiude una connessione**, e quali eccezioni si incontrano (paragrafo 21.4);
- come si **eseguono comandi** con `Statement` (paragrafo 21.5) e come si **leggono i risultati** con `ResultSet` (paragrafo 21.6);
- perché esiste `PreparedStatement` e perché è lo strumento da usare quando i valori vengono dal programma (paragrafo 21.7);
- come si **chiudono le risorse** nel modo imposto da una traccia d'esame (paragrafo 21.8);
- come si passa **dalle righe agli oggetti** (paragrafo 21.9);
- alcuni **cenni** su metadati, `RowSet`, procedure memorizzate e pool di connessioni (paragrafo 21.10);
- come **tradurre le parole di una traccia** in codice (paragrafo 21.11);
- gli **scheletri** da saper scrivere a memoria e gli **errori tipici**.

Il capitolo mette insieme molto di ciò che abbiamo già visto. Le interfacce `Connection`, `Statement` e `ResultSet` si usano come ogni interfaccia ([Capitolo 10](10-classi-astratte-e-interfacce.md)); le loro operazioni dichiarano un'eccezione **controllata**, `SQLException`, da gestire come tutte le altre ([Capitolo 13](13-eccezioni.md)); la chiusura delle risorse nel `finally` è lo schema in quattro passi già incontrato per i flussi e per i socket ([Capitolo 13](13-eccezioni.md), [Capitolo 14](14-file-di-testo.md), [Capitolo 19](19-networking.md)); i risultati si raccolgono in una `List` di oggetti ([Capitolo 12](12-generics-e-collezioni.md)). La dipendenza da aggiungere al progetto per avere il driver è questione di Maven, che si vede nel [Capitolo 22](22-ecosistema.md).

> [!IMPORTANT]
> **Nota per l'esame — JDBC**
> JDBC fa parte dell'area «Core Java API» del secondo esercizio della prova scritta (13 punti), insieme a file, serializzazione, socket, XML e collezioni. Il caso tipico è una **query con `PreparedStatement`** e la lettura del `ResultSet`, oppure un **inserimento o una modifica con `executeUpdate`**, dentro un metodo la cui firma è data dalla traccia. Le difficoltà sono di **precisione**: i nomi dei metodi (`prepareStatement`, `executeQuery`, `executeUpdate`, `next`, `getString`) vanno scritti al carattere; gli indici dei parametri e delle colonne partono da **1**; `SQLException` è controllata e va dichiarata o catturata; le risorse vanno chiuse, e se la traccia impone il `finally` va usato proprio quel blocco. Il capitolo insiste su queste cose.

---

## 21.1 Un database relazionale, in breve

### 21.1.1 Tabelle, righe, colonne

Un **database relazionale** organizza i dati in **tabelle**. Una tabella ha un nome e un insieme fisso di **colonne**, ciascuna con un nome e un tipo; ogni **riga** rappresenta un elemento (un libro, un cliente, un ordine) e ha un valore per ogni colonna. Una colonna, o un gruppo di colonne, è dichiarata **chiave primaria** (*primary key*): il suo valore identifica la riga in modo univoco, e il database rifiuta due righe con la stessa chiave.

In tutto il capitolo useremo una tabella `libro`, che descrive i libri di un negozio:

| id | titolo | autore | anno | prezzo |
|---|---|---|---|---|
| 1 | Il barone rampante | Calvino | 1957 | 11.9 |
| 2 | Le città invisibili | Calvino | 1972 | 10.5 |
| 3 | La coscienza di Zeno | Svevo | 1923 | 9.8 |
| 4 | Il fu Mattia Pascal | Pirandello | 1904 | 8.9 |
| 5 | Uno, nessuno e centomila | Pirandello | 1926 | 9.4 |

La colonna `id` è la chiave primaria. Una cella può anche essere vuota, cioè contenere il valore speciale `NULL` (nessun valore); ne riparleremo nel paragrafo 21.6.5.

### 21.1.2 Il minimo di SQL

Il programma Java, per dare ordini al database, scrive **stringhe SQL** (*Structured Query Language*). JDBC non traduce e non controlla queste stringhe: le consegna al database così come sono, e solo lui le interpreta. Chi scrive JDBC deve quindi saper scrivere le cinque istruzioni di base. Eccole, sulla nostra tabella:

```text
CREATE TABLE libro (id INT PRIMARY KEY, titolo VARCHAR(100), autore VARCHAR(60), anno INT, prezzo DOUBLE)
INSERT INTO libro (id, titolo, autore, anno, prezzo) VALUES (6, 'Il visconte dimezzato', 'Calvino', 1952, 9.0)
SELECT titolo, anno FROM libro WHERE autore = 'Svevo' ORDER BY anno
UPDATE libro SET prezzo = 12.5 WHERE id = 1
DELETE FROM libro WHERE anno < 1910
```

- `CREATE TABLE` crea una tabella, dichiarando nome e tipo di ogni colonna. `INT`, `DOUBLE` e `VARCHAR(n)` (testo lungo al massimo *n* caratteri) sono i tipi che ci servono.
- `INSERT INTO … VALUES …` aggiunge una riga. L'elenco delle colonne tra parentesi e l'elenco dei valori si corrispondono **nello stesso ordine**.
- `SELECT … FROM … WHERE …` **interroga** la tabella: dopo `SELECT` le colonne volute (o `*` per tutte), dopo `WHERE` la condizione che le righe devono soddisfare, con `ORDER BY` per ordinare. È l'unica istruzione che **restituisce righe**.
- `UPDATE … SET … WHERE …` modifica le righe che soddisfano la condizione. Più colonne si separano con una **virgola**: `SET prezzo = 12.5, anno = 1958`. Senza `WHERE` la modifica vale per **tutte** le righe.
- `DELETE FROM … WHERE …` elimina le righe che soddisfano la condizione. Anche qui, senza `WHERE`, si eliminano tutte.

> [!WARNING]
> **Attenzione — Il testo in SQL va tra apici singoli**
> Nelle stringhe SQL i valori di testo si scrivono tra **apici singoli** (`'Svevo'`), non tra virgolette doppie; i numeri si scrivono senza apici. Dentro una stringa Java, che ha già le sue virgolette doppie, gli apici singoli non danno fastidio: `"SELECT * FROM libro WHERE autore = 'Svevo'"`. Per scrivere un apice dentro un testo SQL lo si raddoppia (`'L''isola'`), una complicazione che il paragrafo 21.7 permette di evitare del tutto.

SQL non è l'oggetto di questo corso e non si approfondisce qui. Per i casi d'esame bastano queste cinque forme, con condizioni semplici nel `WHERE` (`=`, `<`, `>`, `AND`, `OR`, `LIKE`).

---

## 21.2 Che cos'è JDBC

### 21.2.1 Il problema: ogni database parla a modo suo

Esistono moltissimi sistemi di gestione di database (*DBMS*, *Database Management System*), prodotti da aziende diverse, e ciascuno comunica con i programmi attraverso un proprio protocollo di rete e un proprio formato. Se il programma Java dovesse conoscere i dettagli di ogni prodotto, il codice scritto per uno non servirebbe per l'altro, e cambiare database significherebbe riscrivere tutto.

JDBC risolve il problema con lo stesso schema che abbiamo incontrato per le interfacce ([Capitolo 10](10-classi-astratte-e-interfacce.md)): una **interfaccia comune**, uguale per tutti, e un'**implementazione per ciascun prodotto**, fornita dal produttore. Il programma Java usa solo l'interfaccia; le differenze tra un database e l'altro restano nascoste nell'implementazione.

> [!NOTE]
> **Definizione — JDBC**
> **JDBC** (*Java Database Connectivity*) è una libreria standard di Java che permette a un programma di collegarsi a un database e di mandargli comandi SQL. Generalizza le operazioni comuni di accesso ai dati in un insieme di classi e di metodi, e nasconde in una libreria i dettagli specifici di ciascun prodotto, così che la connessione a database diversi sia trasparente per chi programma. JDBC standardizza:
> - il modo di **stabilire la connessione** al database;
> - il modo di **inviare le interrogazioni**;
> - il modo di **creare procedure memorizzate**;
> - la **struttura dei dati** che formano il risultato di una interrogazione.

### 21.2.2 I package

Le classi e le interfacce di JDBC stanno in due package:

- `java.sql` contiene il nucleo: tutto ciò che serve per accedere a un database (`DriverManager`, `Connection`, `Statement`, `PreparedStatement`, `ResultSet`, `SQLException`, …);
- `javax.sql` contiene funzionalità opzionali per le applicazioni di grandi dimensioni: `DataSource`, i *pool* di connessioni, le transazioni distribuite (paragrafo 21.10).

Nelle versioni attuali di Java entrambi i package fanno parte dello stesso modulo, `java.sql`. In tutti gli esempi di questo capitolo gli `import` sono esplicitamente `java.sql.Connection`, `java.sql.DriverManager`, e così via.

> [!NOTE]
> **Approfondimento esterno — Il modulo `java.sql`**
> La documentazione ufficiale di Java SE 17 descrive il modulo `java.sql` come quello che «*defines the JDBC API*», cioè l'API per accedere a una sorgente di dati; i package `java.sql` e `javax.sql` stanno entrambi in questo modulo. Ogni interfaccia che incontreremo (`Connection`, `Statement`, `ResultSet`) è dichiarata in `java.sql`, e i metodi che parlano con il database dichiarano `throws SQLException`.
>
> *Fonte:* [Module java.sql (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/module-summary.html)

### 21.2.3 L'architettura: API, gestore dei driver e driver

JDBC si compone di due parti:

- l'**API JDBC**, scritta interamente in Java, che è ciò che usa il programmatore;
- il **gestore dei driver** (*JDBC Driver Manager*), che si occupa di scegliere il driver giusto e di comunicare con i **driver** specifici dei singoli prodotti, i quali parlano davvero con il database.

Un **driver** è un traduttore: converte le chiamate generiche di JDBC in chiamate specifiche per un particolare database. Esistono driver per tutti i database più diffusi, e li fornisce di solito il produttore del database sotto forma di un file **JAR** da aggiungere al progetto. La traduzione avviene sul computer del **client**, cioè dove gira il programma Java: il server del database non richiede modifiche. Il driver è l'unico pezzo che sa a che cosa assomigli quel particolare server.

La figura, a parole: in alto c'è il programma Java, che chiama l'API JDBC; sotto, il `DriverManager` sceglie il driver adatto; sotto ancora, il driver (specifico del produttore) parla con il database attraverso la rete. Il programma non vede mai gli ultimi due livelli.

### 21.2.4 I quattro tipi di driver

Il corso classifica i driver in quattro **tipi**, secondo il modo in cui arrivano al database:

| Tipo | Nome | Come funziona | Giudizio |
|---|---|---|---|
| **I** | ponte JDBC-ODBC | traduce le chiamate JDBC in chiamate **ODBC** (*Open Database Connectivity*, uno standard più vecchio, del 1992, che inserisce un livello intermedio tra applicazione e database); l'ODBC poi chiama l'API nativa del database | inefficiente (attraversa più livelli) e limitato a ciò che ODBC sa fare |
| **II** | API nativa | chiama direttamente l'API nativa del database | più efficiente del tipo I, ma dipende dall'esistenza di una libreria nativa sul computer |
| **III** | middleware | manda le chiamate, con un protocollo di rete indipendente dal database, a un *middleware* su un altro server, che poi parla con il database | adatto ad architetture complesse |
| **IV** | tutto Java (*thin driver*) | scritto interamente in Java; parla direttamente con il database nel protocollo nativo di quest'ultimo | il più efficiente e il più semplice da distribuire: serve solo una JVM |

Oggi si usa quasi sempre il **tipo IV**: basta aggiungere il JAR del produttore. Il tipo I è citato per ragioni storiche; il driver che realizzava il ponte con ODBC (`sun.jdbc.odbc.JdbcOdbcDriver`, che si trova in molti esempi vecchi) non fa più parte dei JDK attuali, e un esempio che lo nomina non funziona più.

---

## 21.3 La catena di oggetti

Per eseguire una query bisogna passare per **quattro tipi di oggetti**, ciascuno prodotto dal precedente. È la struttura da avere in testa prima di studiare i dettagli.

| Oggetto | Che cosa rappresenta | Come lo si ottiene |
|---|---|---|
| `DriverManager` | il gestore dei driver; non si crea, ha solo metodi `static` | è una classe, si usa per nome |
| `Connection` | una **sessione** aperta con il database | `DriverManager.getConnection(...)` |
| `Statement` o `PreparedStatement` | un **comando SQL** da eseguire | `connessione.createStatement()` oppure `connessione.prepareStatement(sql)` |
| `ResultSet` | le **righe** restituite da una interrogazione | `comando.executeQuery(...)` |

Insieme a questi ci sono il **driver** (il traduttore, di cui il programma non vede nulla) e i **metadati** (informazioni sulla struttura dei dati, paragrafo 21.10). In ordine di tempo, i passi per interrogare un database sono sei, e conviene saperli recitare:

1. avere il **driver** nel progetto (nel *classpath*);
2. aprire una **connessione** con `DriverManager.getConnection`;
3. creare uno **`Statement`** o un **`PreparedStatement`** dalla connessione;
4. **eseguire** il comando: `executeQuery` per una interrogazione, `executeUpdate` per una modifica;
5. **scorrere i risultati** con `ResultSet`: `while (rs.next())` e i metodi `getXxx`;
6. **chiudere** `ResultSet`, comando e connessione.

I quattro paragrafi che seguono (21.4–21.7) percorrono questa catena un anello alla volta; il paragrafo 21.8 rimette insieme la chiusura.

---

## 21.4 La connessione

### 21.4.1 Avere il driver

Perché `DriverManager` possa aprire una connessione, il driver del database deve essere **presente nel progetto**: il suo JAR deve stare nel *classpath* durante l'esecuzione. Con Maven (che vedremo nel [Capitolo 22](22-ecosistema.md)) si aggiunge una dipendenza nel `pom.xml`. Per il driver MySQL, per esempio:

```xml
<dependency>
  <groupId>com.mysql</groupId>
  <artifactId>mysql-connector-j</artifactId>
  <version>9.1.0</version>
  <scope>runtime</scope>
</dependency>
```

Il `scope` `runtime` dice che il driver non serve per **compilare** (il codice usa solo le interfacce di `java.sql`) ma serve per **eseguire**.

Il driver deve anche essere **registrato** presso il `DriverManager`, cioè il gestore deve sapere che esiste. Nei vecchi esempi lo si faceva a mano, **caricando la classe del driver per nome**:

```java
// vecchio stile: serve solo con driver antichi
try {
    Class.forName("com.mysql.cj.jdbc.Driver");        // nome completo della classe del driver
} catch (ClassNotFoundException e) {
    System.out.println("Driver non trovato");
}
```

`Class.forName(String)` chiede alla JVM di trovare, caricare e collegare la classe indicata. Il nome del driver è una stringa letterale, quindi il driver non deve esistere **al momento della compilazione**: se manca a tempo di esecuzione, il metodo lancia `ClassNotFoundException`, una eccezione **controllata** ([Capitolo 13](13-eccezioni.md)) da catturare o da dichiarare. Ogni classe driver, nel proprio codice di inizializzazione, crea un'istanza di sé e la registra presso il `DriverManager`: per questo basta nominarla, senza creare esplicitamente oggetti o chiamare `registerDriver`.

Una seconda via, ormai rara, è l'impostazione della proprietà di sistema `jdbc.drivers`, che elenca i nomi completi dei driver separati da `:`, per esempio `java -Djdbc.drivers=com.mysql.cj.jdbc.Driver MiaApp`.

> [!TIP]
> **Intuizione — Oggi il driver si trova da solo**
> Le versioni moderne dei driver si **annunciano da sole** alla JVM: basta che il loro JAR sia nel classpath, e il `DriverManager` li trova senza che il programma debba nominarli. Questo è il motivo per cui nei programmi recenti `Class.forName(...)` non compare. Se una traccia d'esame non chiede espressamente di caricare il driver, non va scritto: una riga in più è soltanto una `ClassNotFoundException` in più da gestire.

> [!NOTE]
> **Approfondimento esterno — Il caricamento dei driver in `DriverManager`**
> La documentazione ufficiale spiega che, durante la propria inizializzazione, `DriverManager` cerca i driver disponibili in due modi: tramite la proprietà di sistema `jdbc.drivers`, che contiene «*a colon separated list of fully qualified class names of JDBC drivers*», e tramite i *service provider* della classe `java.sql.Driver` caricati con il meccanismo standard di Java. Quando si chiama `getConnection`, il gestore sceglie un driver adatto tra quelli caricati. Una nota aggiunge che l'uso di un oggetto `DataSource` è il modo preferito per ottenere una connessione, ma `DriverManager` resta il caso base.
>
> *Fonte:* [DriverManager (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/DriverManager.html)

### 21.4.2 L'URL del database

Quale database vogliamo raggiungere? Lo si indica con un **URL JDBC**, una stringa con questa forma:

```text
jdbc:sottoprotocollo:sottonome
```

- `jdbc` è il **protocollo**, sempre uguale;
- il **sottoprotocollo** identifica il tipo di database, e quindi il driver da usare;
- il **sottonome** identifica la risorsa: il suo formato dipende dal driver, e può contenere il nome del server, la porta, il nome del database.

| Database | URL di esempio |
|---|---|
| ponte ODBC (storico) | `jdbc:odbc:music` |
| Cloudscape (storico) | `jdbc:cloudscape:Movies` |
| Oracle | `jdbc:oracle:thin:@nomeserver:1521:nomedatabase` |
| MySQL | `jdbc:mysql://localhost:3306/negozio` |

L'ultima riga è la forma che useremo negli esempi: il database `negozio` sta sul computer locale (`localhost`) e il server MySQL ascolta sulla porta `3306`. Il **sottoprotocollo** serve proprio per la scelta del driver: il `DriverManager` chiede a ciascun driver registrato se riconosce l'URL, e usa il primo che risponde di sì.

### 21.4.3 Aprire la connessione: `getConnection`

La connessione si apre con uno di tre metodi `static` di `DriverManager`, tutti con la stessa clausola `throws SQLException`:

```java
public static Connection getConnection(String url) throws SQLException
public static Connection getConnection(String url, String user, String password) throws SQLException
public static Connection getConnection(String url, Properties info) throws SQLException
```

La forma più comune è la seconda: URL, nome utente e password del database. La terza accetta un oggetto `java.util.Properties` (coppie nome–valore; di solito le chiavi `user` e `password`). La prima serve quando le credenziali sono già nell'URL o non servono.

Il metodo restituisce un oggetto `Connection`. Se qualcosa va storto (database irraggiungibile, credenziali errate, URL sbagliato) lancia **`SQLException`**.

> [!NOTE]
> **Approfondimento esterno — `DriverManager.getConnection`**
> La documentazione ufficiale definisce `getConnection` come «*Attempts to establish a connection to the given database URL*» e precisa che il `DriverManager` «*attempts to select an appropriate driver from the set of registered JDBC drivers*». L'URL ha la forma `jdbc:subprotocol:subname`. Tutte e tre le forme lanciano `SQLException` se si verifica un errore di accesso al database o se l'URL è `null`, e `SQLTimeoutException` (sua sottoclasse) se è stato superato il tempo massimo impostato con `setLoginTimeout`.
>
> *Fonte:* [DriverManager.getConnection (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/DriverManager.html)

### 21.4.4 `SQLException`

`SQLException` è la **eccezione di JDBC**: la lanciano quasi tutte le operazioni sul database. Appartiene al package `java.sql`, è una sottoclasse di `Exception` e quindi **controllata**: il compilatore pretende che si catturi o si dichiari ([Capitolo 13](13-eccezioni.md), paragrafo 13.2). Oltre ai metodi che ogni eccezione possiede (`getMessage`, `printStackTrace`), offre due informazioni specifiche sul database: `getSQLState()` (un codice standard di cinque caratteri) e `getErrorCode()` (un numero scelto dal produttore). Nei casi d'esame si usa quasi sempre `getMessage()`.

Se il driver non c'è nel classpath, il `DriverManager` non ha nessun driver a cui chiedere, e il messaggio dell'eccezione è:

```text
No suitable driver found for jdbc:mysql://localhost:3306/negozio
```

### 21.4.5 Un primo programma: aprire e chiudere

Proviamo la sola connessione. Il programma apre, stampa un messaggio e chiude. La struttura è quella che ci accompagnerà fino alla fine: `Connection` dichiarata **fuori** dal `try` e posta a `null`, aperta **dentro** il `try`, chiusa nel `finally` dopo il controllo `!= null` — i tre passi che conosciamo dal [Capitolo 13](13-eccezioni.md), paragrafo 13.5.3.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ProvaConnessione {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/negozio";
        Connection conn = null;                                   // fuori dal try, a null
        try {
            conn = DriverManager.getConnection(url, "root", "password");
            System.out.println("Connessione aperta");
        } catch (SQLException e) {
            System.out.println("Errore: " + e.getMessage());     // il driver spiega che cosa non va
        } finally {
            if (conn != null) {                                   // se getConnection fallisce, conn e' null
                try {
                    conn.close();                                 // close() dichiara SQLException
                } catch (SQLException e) {
                    System.out.println("Errore nella chiusura: " + e.getMessage());
                }
            }
        }
    }
}
```

```text
Connessione aperta
```

Riga per riga. `url` e le credenziali sono stringhe segnaposto: in un programma vero si adattano al proprio database. `Connection conn = null;` dichiara la variabile fuori dal `try` perché il `finally` possa vederla; `null` significa «ancora nessuna connessione». `DriverManager.getConnection(...)` può lanciare `SQLException` e viene quindi dentro il `try`. Nel `finally`, `conn != null` protegge da una `NullPointerException` ([Capitolo 8](08-riferimenti-e-memoria.md)) quando la connessione non è mai stata aperta; e siccome `close()` dichiara a sua volta `SQLException`, la chiamata ha un secondo `try`/`catch` interno.

### 21.4.6 Perché chiudere la connessione

Una connessione occupa risorse sul server del database, e ogni server ne ammette solo un numero **limitato**. Se un programma le apre e non le chiude, prima o poi il server rifiuta le nuove richieste, e può bloccarsi tutto il sistema. La connessione va chiusa **sempre**, anche quando qualcosa è andato storto.

```java
public void close() throws SQLException
```

> [!NOTE]
> **Approfondimento esterno — `Connection.close`**
> La documentazione ufficiale descrive `close()` come il metodo che rilascia «*this Connection object's database and JDBC resources immediately instead of waiting for them to be automatically released*». Chiamarlo su una connessione già chiusa non ha effetto. Dichiara `throws SQLException`, ed è dichiarato anche in `AutoCloseable`, per cui `Connection` si può usare in un `try-with-resources` (paragrafo 21.8.3). Per impostazione predefinita una connessione è in modalità *auto-commit*: ogni istruzione eseguita ha effetto definitivo sul database subito dopo la sua esecuzione.
>
> *Fonte:* [Connection (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/Connection.html)

> [!WARNING]
> **Attenzione — Le transazioni non sono nel programma**
> L'*auto-commit* ha una conseguenza pratica: ogni `INSERT`, `UPDATE` o `DELETE` diventa definitivo non appena `executeUpdate` termina, senza bisogno di un'istruzione `commit`. JDBC permette anche di raggruppare più istruzioni in una **transazione** (`setAutoCommit(false)`, `commit()`, `rollback()`), che però non fa parte degli argomenti di questo corso e non si tratta qui.

---

## 21.5 Eseguire comandi: `Statement`

### 21.5.1 Creare uno `Statement`

Una volta ottenuta la connessione, si crea l'oggetto che contiene il comando da eseguire. Il più semplice è `Statement`, per istruzioni SQL **complete** e già scritte, senza parametri:

```java
Statement stmt = conn.createStatement();                // Connection.createStatement() throws SQLException
```

`Statement` è un'**interfaccia**, quindi non si può creare con `new`: è la connessione a produrne un'istanza (lo stesso meccanismo del `DocumentBuilder` del [Capitolo 20](20-xml.md), delle *factory*). Uno `Statement` si può usare più volte per mandare comandi diversi, e va chiuso quando non serve più con `stmt.close()`, che rilascia subito le risorse; il `close()` di uno `Statement` chiude anche il suo `ResultSet` corrente.

### 21.5.2 `executeUpdate` e `executeQuery`

Due metodi di `Statement` eseguono un comando, e **non sono intercambiabili**: la scelta dipende dal fatto che il comando restituisca righe oppure no.

| Metodo | Per quali istruzioni | Che cosa restituisce |
|---|---|---|
| `int executeUpdate(String sql)` | `INSERT`, `UPDATE`, `DELETE` e istruzioni che non restituiscono nulla, come `CREATE TABLE` | il **numero di righe** toccate (0 per `CREATE TABLE`) |
| `ResultSet executeQuery(String sql)` | `SELECT` | un oggetto `ResultSet` con le **righe** del risultato, mai `null` |

Entrambi dichiarano `throws SQLException`, che il compilatore pretende di vedere gestita. Con `stmt.setQueryTimeout(int secondi)` si può fissare un'attesa massima per il risultato; se è superata, il driver lancia `SQLTimeoutException`, sottoclasse di `SQLException`.

> [!NOTE]
> **Approfondimento esterno — `Statement.executeQuery` ed `executeUpdate`**
> La documentazione ufficiale precisa che `executeQuery(String sql)` esegue un'istruzione SQL «*which returns a single ResultSet object*», e che il `ResultSet` restituito non è mai `null`. `executeUpdate(String sql)` esegue una istruzione `INSERT`, `UPDATE` o `DELETE` oppure un'istruzione che non restituisce nulla, come il DDL, e restituisce «*either (1) the row count for SQL Data Manipulation Language (DML) statements or (2) 0 for SQL statements that return nothing*». Entrambi lanciano `SQLException` se l'istruzione produce qualcosa di diverso da quanto previsto: `executeQuery` con un'istruzione che non produce un solo `ResultSet`, `executeUpdate` con un'istruzione che produce un `ResultSet`. Alla chiusura di uno `Statement` si chiude anche l'eventuale `ResultSet` corrente.
>
> *Fonte:* [Statement (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/Statement.html)

### 21.5.3 Costruire il database: `CREATE TABLE` e `INSERT`

Il programma seguente prepara la tabella `libro` del paragrafo 21.1 e vi inserisce le cinque righe. Tutti gli esempi successivi del capitolo partiranno da una tabella appena preparata così.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class CreaTabella {
    public static void main(String[] args) {
        Connection conn = null;
        Statement stmt = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            stmt = conn.createStatement();
            stmt.executeUpdate("DROP TABLE IF EXISTS libro");
            int r = stmt.executeUpdate("CREATE TABLE libro (id INT PRIMARY KEY, "
                    + "titolo VARCHAR(100), autore VARCHAR(60), anno INT, prezzo DOUBLE)");
            System.out.println("Tabella creata, righe toccate: " + r);

            int inserite = 0;
            inserite += stmt.executeUpdate("INSERT INTO libro VALUES (1, 'Il barone rampante', 'Calvino', 1957, 11.9)");
            inserite += stmt.executeUpdate("INSERT INTO libro VALUES (2, 'Le città invisibili', 'Calvino', 1972, 10.5)");
            inserite += stmt.executeUpdate("INSERT INTO libro VALUES (3, 'La coscienza di Zeno', 'Svevo', 1923, 9.8)");
            inserite += stmt.executeUpdate("INSERT INTO libro VALUES (4, 'Il fu Mattia Pascal', 'Pirandello', 1904, 8.9)");
            inserite += stmt.executeUpdate("INSERT INTO libro VALUES (5, 'Uno, nessuno e centomila', 'Pirandello', 1926, 9.4)");
            System.out.println("Righe inserite: " + inserite);
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
Tabella creata, righe toccate: 0
Righe inserite: 5
```

Notiamo tre cose. Primo: la stringa del `CREATE TABLE` è spezzata su due righe con `+`; gli spazi alla fine di ciascun pezzo (o all'inizio del successivo) sono **indispensabili**, perché il database riceve un'unica stringa. Secondo: ogni `executeUpdate` restituisce `1` per una riga inserita, e li sommiamo per contare; il `CREATE TABLE`, che non tocca righe, restituisce `0`. Terzo: nel `finally` ci sono **due** `try`/`catch` separati, uno per lo `Statement` e uno per la `Connection`: se la chiusura dello `Statement` lancia un'eccezione, la connessione deve comunque essere chiusa. È lo schema che sistematizziamo nel paragrafo 21.8.

### 21.5.4 Modificare e cancellare: `UPDATE` e `DELETE`

Modifiche e cancellazioni usano lo stesso metodo `executeUpdate`, e il valore restituito è utilissimo: dice **quante righe** sono state toccate, cioè quante soddisfacevano il `WHERE`. Un valore `0` significa «nessuna riga corrisponde».

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ModificaLibri {
    public static void main(String[] args) {
        Connection conn = null;
        Statement stmt = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            stmt = conn.createStatement();

            int aggiornate = stmt.executeUpdate("UPDATE libro SET prezzo = prezzo + 1 WHERE autore = 'Calvino'");
            System.out.println("Prezzi aumentati: " + aggiornate);

            int cancellate = stmt.executeUpdate("DELETE FROM libro WHERE anno < 1910");
            System.out.println("Libri cancellati: " + cancellate);

            int nessuna = stmt.executeUpdate("DELETE FROM libro WHERE autore = 'Nessuno'");
            System.out.println("Cancellazione senza corrispondenze: " + nessuna);

            ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM libro");
            rs.next();
            System.out.println("Libri rimasti: " + rs.getInt(1));
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
Prezzi aumentati: 2
Libri cancellati: 1
Cancellazione senza corrispondenze: 0
Libri rimasti: 4
```

L'`UPDATE` tocca i due libri di Calvino; il primo `DELETE` elimina il libro del 1904; il secondo non trova nulla e restituisce `0`, senza alcuna eccezione: **non trovare righe non è un errore**. L'ultima interrogazione, `SELECT COUNT(*)`, conta le righe e restituisce una sola riga con una sola colonna; vedremo nel prossimo paragrafo perché si legge con `rs.next()` e `rs.getInt(1)`.

> [!WARNING]
> **Attenzione — `executeQuery` per `SELECT`, `executeUpdate` per il resto**
> I due metodi non sono interscambiabili. `executeQuery("INSERT …")` e `executeUpdate("SELECT …")` **compilano** (entrambi accettano una `String`) ma, a esecuzione, lanciano `SQLException`, perché l'istruzione non produce quello che il metodo si aspetta. Una regola per non sbagliare: se il comando SQL comincia con `SELECT` serve `executeQuery`, e si usa il `ResultSet` che restituisce; in tutti gli altri casi serve `executeUpdate`, e si usa l'`int`.

---

## 21.6 Leggere i risultati: `ResultSet`

### 21.6.1 Il cursore

`executeQuery` restituisce un `ResultSet`: l'insieme delle righe prodotte dalla interrogazione, a cui si accede **una riga alla volta** attraverso un **cursore** (*cursor*). Il cursore indica la riga corrente. La caratteristica che sorprende i principianti è la sua posizione iniziale: subito dopo `executeQuery`, il cursore sta **prima della prima riga**, non sulla prima. Per portarlo sulla prima riga bisogna chiamare `next()`.

```java
boolean next() throws SQLException
```

`next()` sposta il cursore di una riga in avanti. Restituisce `true` se la nuova riga esiste, `false` se le righe sono finite (e in questo caso il cursore si trova **dopo l'ultima riga**). Il ciclo di lettura, quindi, ha sempre questa forma:

```java
ResultSet rs = stmt.executeQuery("SELECT ...");
while (rs.next()) {
    // qui il cursore e' su una riga valida: si leggono le colonne con rs.getXxx(...)
}
```

È lo stesso schema di «leggi fino a quando ce ne sono» incontrato per `readLine` fino a `null` ([Capitolo 14](14-file-di-testo.md)) e per `hasNextLine`. La differenza è che il controllo di fine e l'avanzamento sono un unico gesto: `next()`.

### 21.6.2 Leggere le colonne: `getString`, `getInt`, `getDouble`

Quando il cursore è su una riga, i metodi `getXxx` leggono il valore di una colonna di **quella** riga. Il nome del metodo indica il tipo Java che si vuole ottenere; la colonna si indica con la sua **posizione** o con il suo **nome**:

```java
String getString(int columnIndex) throws SQLException
String getString(String columnLabel) throws SQLException
int    getInt(int columnIndex) throws SQLException
int    getInt(String columnLabel) throws SQLException
double getDouble(int columnIndex) throws SQLException
double getDouble(String columnLabel) throws SQLException
```

| Tipo SQL (colonna) | Metodo | Tipo Java restituito |
|---|---|---|
| `VARCHAR`, `CHAR` | `getString` | `String` |
| `INT` | `getInt` | `int` |
| `DOUBLE` | `getDouble` | `double` |
| `FLOAT` | `getFloat` | `float` |
| `BIGINT` | `getLong` | `long` |
| `BOOLEAN` | `getBoolean` | `boolean` |
| `DATE` | `getDate` | `java.sql.Date` |

> [!IMPORTANT]
> **Nota del docente — L'indice della prima colonna è 1, non 0**
> Nel `ResultSet` le colonne si numerano da **1**: la prima colonna è la numero 1. È l'opposto degli array, delle stringhe e delle liste (da 0). Sbagliare produce una `SQLException` a esecuzione, non un errore di compilazione. La stessa regola vale per gli indici dei parametri di `PreparedStatement` (paragrafo 21.7).

La posizione dipende **dall'ordine delle colonne nel `SELECT`**, non da quello della tabella: in `SELECT titolo, anno FROM libro`, la colonna 1 è `titolo` e la 2 è `anno`. Per questo, quando il `SELECT` ha più colonne, usare il **nome** (`rs.getString("titolo")`) rende il codice più leggibile e più robusto: resta valido anche se cambia l'ordine delle colonne nell'interrogazione. Il nome di una colonna non distingue le maiuscole dalle minuscole.

Possiamo ora vedere la lettura completa. Il programma stampa tutta la tabella:

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class StampaLibri {
    public static void main(String[] args) {
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            stmt = conn.createStatement();
            rs = stmt.executeQuery("SELECT id, titolo, autore, anno, prezzo FROM libro ORDER BY id");
            while (rs.next()) {                                    // una iterazione per riga
                int id = rs.getInt("id");                          // per nome
                String titolo = rs.getString("titolo");
                String autore = rs.getString(3);                   // per posizione: la terza colonna
                int anno = rs.getInt("anno");
                double prezzo = rs.getDouble("prezzo");
                System.out.println(id + " - " + titolo + " (" + autore + ", " + anno + ") " + prezzo);
            }
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (rs != null) rs.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura del ResultSet");
            }
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
1 - Il barone rampante (Calvino, 1957) 11.9
2 - Le città invisibili (Calvino, 1972) 10.5
3 - La coscienza di Zeno (Svevo, 1923) 9.8
4 - Il fu Mattia Pascal (Pirandello, 1904) 8.9
5 - Uno, nessuno e centomila (Pirandello, 1926) 9.4
```

Il corpo del ciclo legge cinque colonne della riga corrente, usando il nome per quasi tutte e la posizione (`3`) per `autore`, a titolo dimostrativo. Il `ORDER BY id` fissa l'ordine delle righe: senza, il database è libero di restituirle nell'ordine che preferisce.

> [!NOTE]
> **Approfondimento esterno — `ResultSet.next` e `getString`**
> La documentazione ufficiale descrive `next()` così: «*A ResultSet cursor is initially positioned before the first row; the first call to the method next makes the first row the current row*». Quando restituisce `false`, il cursore è dopo l'ultima riga, e «*any invocation of a ResultSet method which requires a current row will result in a SQLException being thrown*». Per i metodi `getXxx(int columnIndex)`: «*the first column is 1, the second is 2, …*». `getString` restituisce `null` se il valore SQL è `NULL`; lancia `SQLException` se l'indice di colonna non è valido o se il `ResultSet` è chiuso.
>
> *Fonte:* [ResultSet (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/ResultSet.html)

### 21.6.3 Una sola riga, o un solo valore

Quando l'interrogazione produce al più **una** riga (per esempio una ricerca per chiave primaria) o una sola cella (`COUNT(*)`, `MAX(...)`), il `while` non serve: basta **un solo `next()`**, in un `if` se la riga potrebbe non esserci, o da solo se l'interrogazione la restituisce sempre.

```java
// al massimo una riga: se non c'e', next() restituisce false
ResultSet rs = stmt.executeQuery("SELECT titolo FROM libro WHERE id = 3");
if (rs.next()) {
    System.out.println(rs.getString("titolo"));
} else {
    System.out.println("Nessun libro con quell'id");
}

// una sola cella sempre presente: COUNT(*) restituisce sempre una riga
ResultSet conta = stmt.executeQuery("SELECT COUNT(*) FROM libro");
conta.next();                                      // porta il cursore sull'unica riga
int quanti = conta.getInt(1);                      // la colonna senza nome si legge per posizione
```

`COUNT(*)` non ha un nome di colonna comodo da scrivere, quindi si legge per **posizione**: `getInt(1)`.

### 21.6.4 Un `ResultSet` è legato alla connessione

Il `ResultSet` non è una copia dei dati: finché lo si legge, resta **collegato** allo `Statement` che lo ha prodotto e alla connessione. Quando si chiude lo `Statement`, si chiude anche il `ResultSet`; quando si chiude la connessione, tutto decade. Ne segue una regola pratica che nasce da un errore tipico (paragrafo «Errori tipici»): **tutte le letture del `ResultSet` si fanno prima di chiudere**. Non si può restituire un `ResultSet` da un metodo che chiude la connessione prima di tornare. Quando i dati devono sopravvivere alla connessione, si **copiano in oggetti** Java (paragrafo 21.9).

Un'altra conseguenza: lo stesso `Statement` può eseguire una nuova interrogazione, ma il `ResultSet` precedente viene chiuso. Se servono due risultati insieme si usano due `Statement`.

### 21.6.5 Valori `NULL`

Una cella può essere vuota, cioè contenere `NULL`. Java però non ha un «numero `NULL`»: un `int` è sempre un numero. JDBC risolve il problema così: `getString` restituisce `null`; i metodi che restituiscono un tipo primitivo (`getInt`, `getDouble`, `getBoolean`) restituiscono **`0`** (o `false`). Dal solo valore restituito, quindi, uno `0` può significare «zero» oppure «assente». Per distinguerli si chiama `wasNull()` **subito dopo** aver letto la colonna: restituisce `true` se l'ultima colonna letta era `NULL`.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ProvaNull {
    public static void main(String[] args) {
        Connection conn = null;
        Statement stmt = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            stmt = conn.createStatement();
            stmt.executeUpdate("INSERT INTO libro (id, titolo, autore) VALUES (6, 'Senza data', 'Anonimo')");
            ResultSet rs = stmt.executeQuery("SELECT anno, prezzo FROM libro WHERE id = 6");
            rs.next();
            int anno = rs.getInt("anno");                       // la colonna anno e' NULL
            boolean annoAssente = rs.wasNull();                 // subito dopo la lettura
            System.out.println("anno = " + anno + ", assente: " + annoAssente);
            System.out.println("prezzo = " + rs.getDouble("prezzo") + ", assente: " + rs.wasNull());
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
anno = 0, assente: true
prezzo = 0.0, assente: true
```

> [!NOTE]
> **Approfondimento esterno — `getInt` e `wasNull`**
> La documentazione ufficiale precisa che `getInt(int columnIndex)` restituisce «*the column value; if the value is SQL NULL, the value returned is 0*», e che `wasNull()` «*reports whether the last column read had a value of SQL NULL*»: va chiamato dopo aver letto la colonna con uno dei metodi `getXxx`, non prima.
>
> *Fonte:* [ResultSet.getInt e ResultSet.wasNull (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/ResultSet.html)

### 21.6.6 Cursori scorrevoli

Il `ResultSet` ottenuto con `createStatement()` senza argomenti ha un cursore che si muove **solo in avanti** (*forward only*) e **non è modificabile** (*read only*): le righe si leggono una volta, nell'ordine, e si può solo chiamare `next()`. Per i casi d'esame è quello che serve. Esiste però una forma più ricca di `createStatement`:

```java
Statement createStatement(int resultSetType, int resultSetConcurrency) throws SQLException
```

Il primo argomento sceglie se il cursore sia **scorrevole**, il secondo se i dati siano **modificabili**:

| Costante (in `ResultSet`) | Significato |
|---|---|
| `TYPE_FORWARD_ONLY` | solo in avanti (predefinito) |
| `TYPE_SCROLL_INSENSITIVE` | scorrevole; non vede le modifiche fatte al database dopo la lettura |
| `TYPE_SCROLL_SENSITIVE` | scorrevole; riflette le modifiche fatte al database |
| `CONCUR_READ_ONLY` | dati non modificabili (predefinito) |
| `CONCUR_UPDATABLE` | dati modificabili |

Con un cursore scorrevole si possono usare, oltre a `next()`, `previous()`, `first()`, `last()`, `beforeFirst()`, `afterLast()`, `isFirst()`, `isLast()`, `isBeforeFirst()`, `isAfterLast()`. Non tutti i driver supportano tutte le combinazioni. Esiste anche una terza forma, `createStatement(int, int, int)`, che aggiunge il terzo argomento sulla *holdability* (se il `ResultSet` resta aperto dopo una conferma di transazione): non serve per gli esercizi.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ProvaScorrevole {
    public static void main(String[] args) {
        Connection conn = null;
        Statement stmt = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            stmt = conn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
            ResultSet rs = stmt.executeQuery("SELECT titolo FROM libro ORDER BY id");
            rs.last();                                           // salta all'ultima riga
            System.out.println("Ultimo: " + rs.getString("titolo"));
            rs.previous();                                       // torna indietro di una riga
            System.out.println("Penultimo: " + rs.getString("titolo"));
            rs.first();                                          // torna alla prima
            System.out.println("Primo: " + rs.getString("titolo"));
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
Ultimo: Uno, nessuno e centomila
Penultimo: Il fu Mattia Pascal
Primo: Il barone rampante
```

---

## 21.7 `PreparedStatement`: comandi con parametri

### 21.7.1 Il problema dei valori che cambiano

Finora le stringhe SQL erano **fisse** e scritte a mano. In un programma vero, però, i valori arrivano da fuori: l'autore da cercare lo digita un utente, il prezzo da modificare è il risultato di un calcolo. Con `Statement` l'unico modo di inserirli nella stringa SQL è **concatenarli**:

```java
String autore = "Svevo";
ResultSet rs = stmt.executeQuery("SELECT titolo FROM libro WHERE autore = '" + autore + "'");
```

Funziona, ma è fragile, per due motivi.

**Primo: gli apici.** Se il valore contiene un apice (un titolo come `L'isola del tesoro`), la stringa SQL risultante è `... titolo = 'L'isola del tesoro'`, che per il database è un testo terminato troppo presto seguito da parole incomprensibili: una `SQLException` per sintassi errata. Bisognerebbe raddoppiare a mano ogni apice, dappertutto.

**Secondo, più grave: l'iniezione SQL (*SQL injection*).** Se il valore proviene da un utente, un utente malevolo può scriverci dentro SQL. Se `autore` vale `x' OR '1'='1`, la stringa diventa:

```text
SELECT titolo FROM libro WHERE autore = 'x' OR '1'='1'
```

e la condizione `'1'='1'` è sempre vera: la query restituisce **tutti** i libri, non quelli di un autore. Con un valore costruito con più cura si possono leggere dati riservati o cancellarli.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class IniezioneSql {
    // ESEMPIO DI CODICE SBAGLIATO: non va imitato
    public static void main(String[] args) throws SQLException {
        String autore = "x' OR '1'='1";                          // input di un utente malevolo
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT titolo FROM libro WHERE autore = '" + autore + "'");
        int righe = 0;
        while (rs.next()) {
            righe++;
        }
        System.out.println("Righe restituite: " + righe);
        conn.close();
    }
}
```

```text
Righe restituite: 5
```

Il programma doveva cercare un autore che non esiste, e invece restituisce tutta la tabella.

### 21.7.2 La soluzione: i segnaposto `?`

`PreparedStatement` risolve entrambi i problemi con una idea semplice: la stringa SQL si scrive **una volta**, con dei **segnaposto** (`?`) al posto dei valori che cambiano, e i valori si forniscono **dopo**, con metodi appositi che li consegnano al database **come valori**, mai come SQL. Il database non può scambiare un valore per un'istruzione, qualunque cosa contenga: gli apici vengono gestiti dal driver, e l'iniezione non è più possibile.

```java
PreparedStatement ps = conn.prepareStatement("SELECT titolo FROM libro WHERE autore = ?");
ps.setString(1, autore);                     // primo (e unico) ? = il valore di autore
ResultSet rs = ps.executeQuery();            // niente stringa: la query e' gia' dentro ps
```

I passi sono sempre tre:

1. **preparare** il comando con `conn.prepareStatement(sql)`, dove `sql` contiene i `?`;
2. **fornire i valori**, un `setXxx` per ciascun `?`;
3. **eseguire** con `executeQuery()` o `executeUpdate()` **senza argomenti**.

```java
PreparedStatement prepareStatement(String sql) throws SQLException      // in Connection
void setString(int parameterIndex, String x) throws SQLException
void setInt(int parameterIndex, int x) throws SQLException
void setDouble(int parameterIndex, double x) throws SQLException
ResultSet executeQuery() throws SQLException                            // in PreparedStatement
int executeUpdate() throws SQLException
```

L'**indice** dei `setXxx` è la posizione del `?` nella stringa SQL, contata da **1**: il primo `?` è il numero 1, il secondo il numero 2. Il metodo `setXxx` si sceglie secondo il tipo del valore: `setString` per il testo, `setInt` per un intero, `setDouble` per un reale; esistono `setLong`, `setBoolean`, `setDate` e altri.

> [!NOTE]
> **Approfondimento esterno — `PreparedStatement`**
> La documentazione ufficiale descrive `Connection.prepareStatement(String sql)` come il metodo che crea un `PreparedStatement` «*for sending parameterized SQL statements to the database*»: l'istruzione, con o senza parametri `IN`, può essere precompilata e poi eseguita più volte in modo efficiente. Per i `setXxx`, «*the first parameter is 1, the second is 2, …*»; `setString` lancia `SQLException` se l'indice non corrisponde a nessun segnaposto. `executeQuery()` e `executeUpdate()` di `PreparedStatement` non hanno argomenti, e `executeQuery()` non restituisce mai `null`. I valori impostati restano validi per le esecuzioni successive, finché non vengono sostituiti.
>
> *Fonte:* [PreparedStatement (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/PreparedStatement.html)

#### Esempio — Cercare i libri di un autore

Il programma cerca tutti i libri di un autore passato come valore. Si noti l'assenza di apici attorno al `?`: è il driver a occuparsene.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class CercaPerAutore {
    public static void main(String[] args) {
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement("SELECT titolo, anno FROM libro WHERE autore = ? ORDER BY anno");
            ps.setString(1, "Pirandello");                       // il primo ?
            rs = ps.executeQuery();                              // senza argomenti
            while (rs.next()) {
                System.out.println(rs.getString("titolo") + " (" + rs.getInt("anno") + ")");
            }
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (rs != null) rs.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura del ResultSet");
            }
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
Il fu Mattia Pascal (1904)
Uno, nessuno e centomila (1926)
```

#### Esempio — Inserire più righe con uno stesso comando

Il vantaggio della preparazione si vede quando lo stesso comando si ripete con valori diversi: la stringa SQL si prepara **una sola volta** (e il database la analizza una sola volta), poi si riempiono i parametri e si esegue ogni volta.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class InserisciLibri {
    public static void main(String[] args) {
        Connection conn = null;
        PreparedStatement ps = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement(
                    "INSERT INTO libro (id, titolo, autore, anno, prezzo) VALUES (?, ?, ?, ?, ?)");

            ps.setInt(1, 6);                                     // id: intero
            ps.setString(2, "L'isola del tesoro");               // l'apice non crea problemi
            ps.setString(3, "Stevenson");
            ps.setInt(4, 1883);
            ps.setDouble(5, 7.5);                                // prezzo: reale
            System.out.println("Inserite: " + ps.executeUpdate());

            ps.setInt(1, 7);                                     // si cambiano solo i valori
            ps.setString(2, "Il visconte dimezzato");
            ps.setString(3, "Calvino");
            ps.setInt(4, 1952);
            ps.setDouble(5, 9.0);
            System.out.println("Inserite: " + ps.executeUpdate());
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
Inserite: 1
Inserite: 1
```

### 21.7.3 I limiti dei segnaposto

Un `?` può stare solo al posto di un **valore**: un numero o un testo. Non può sostituire un nome di tabella, un nome di colonna, una parola chiave SQL o un pezzo di condizione. `SELECT * FROM ? WHERE ...` e `ORDER BY ?` non funzionano come ci si aspetta: se il nome di una tabella deve variare, la stringa SQL va costruita per concatenazione (con la certezza che il nome non venga dall'utente).

Un `?` non va neppure messo **tra apici**: `WHERE autore = '?'` non contiene un segnaposto ma il carattere punto interrogativo, e l'indice 1 non corrisponde a nulla. Il testo con caratteri jolly di `LIKE` si prepara in Java e si consegna come valore:

```java
ps = conn.prepareStatement("SELECT titolo FROM libro WHERE titolo LIKE ?");
ps.setString(1, "%rosa%");                      // % e _ nel valore, non nella stringa SQL
```

### 21.7.4 Un esempio classico, con due errori da riconoscere

L'esempio con cui `PreparedStatement` viene spesso presentato (una modifica del cognome di un autore, in una tabella `authors`) contiene due imprecisioni che conviene riconoscere, perché sono i modi tipici di sbagliare:

```text
UPDATE authors SET lastname = ? Authid = ?     -- manca la virgola; e manca un WHERE
ps.setString(2, 212);                          -- 212 e' un numero: setString vuole una String
```

Nell'`UPDATE`, due assegnazioni nel `SET` si separano con una **virgola**, e per modificare una sola riga serve un `WHERE`: la forma corretta è `UPDATE authors SET lastname = ? WHERE authid = ?`. Nel secondo `setXxx`, il valore `212` è un `int`: va con `setInt(2, 212)`; `setString(2, 212)` **non compila** (`incompatible types: int cannot be converted to String`).

Il programma completo e corretto, con i nomi della nostra tabella:

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class AggiornaTitolo {
    public static void main(String[] args) {
        Connection conn = null;
        PreparedStatement ps = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement("UPDATE libro SET titolo = ?, anno = ? WHERE id = ?");
            ps.setString(1, "Il barone rampante (ed. nuova)");   // primo ?
            ps.setInt(2, 1960);                                  // secondo ?: un intero
            ps.setInt(3, 1);                                     // terzo ?: la chiave
            int righe = ps.executeUpdate();
            System.out.println("Righe modificate: " + righe);
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        } finally {
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura dello statement");
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.out.println("Errore nella chiusura della connessione");
            }
        }
    }
}
```

```text
Righe modificate: 1
```

### 21.7.5 Se i parametri non sono impostati

Se prima dell'esecuzione manca il valore di un `?`, il driver lancia `SQLException`. I valori impostati restano validi per le esecuzioni successive, finché non vengono sostituiti; chi riusa uno stesso `PreparedStatement` deve quindi impostare **tutti** i parametri che cambiano. Il metodo `ps.clearParameters()` li azzera.

### 21.7.6 `Statement` o `PreparedStatement`?

Ricapitolando, in un esercizio la scelta è semplice: se la stringa SQL è **fissa** (`CREATE TABLE`, `SELECT COUNT(*) FROM libro`, una `DELETE` senza condizioni), `Statement` basta; **appena un valore viene dal programma** (un parametro del metodo, un campo di un oggetto), `PreparedStatement` con i `?`. Se la traccia dice «con un `PreparedStatement`», la scelta è già fatta.

---

## 21.8 Chiudere le risorse

### 21.8.1 Tre risorse, tre `close`

Una interrogazione usa tre risorse: `Connection`, `Statement` (o `PreparedStatement`) e `ResultSet`. Tutte e tre hanno un metodo `close()` che dichiara `throws SQLException`. Vanno chiuse in ordine **inverso** a quello di apertura: prima il `ResultSet`, poi lo `Statement`, infine la `Connection`. Chiudere la connessione per prima renderebbe inutilizzabili le altre due.

In pratica, la chiusura dello `Statement` chiude anche il suo `ResultSet`, e la chiusura della `Connection` rilascia tutto: per questo molti programmi chiudono solo `Statement` e `Connection`. Chiudere anche il `ResultSet` è però più chiaro, e non costa nulla.

### 21.8.2 Lo schema del `finally`

È lo schema in quattro passi del [Capitolo 13](13-eccezioni.md), paragrafo 13.5.3, applicato a tre risorse:

1. dichiarare **tutte** le variabili **fuori** dal `try`, a `null`;
2. assegnarle **dentro** il `try`, man mano che si aprono;
3. nel `finally`, controllare `!= null` prima di ogni `close`;
4. gestire l'eccezione di ogni `close()`.

Il punto 4 richiede cura: se i tre `close` sono dentro un unico `try`, un errore nel primo impedisce di eseguire gli altri due. Perciò ciascuna chiusura ha il **proprio** `try`/`catch`, come negli esempi del capitolo:

```java
} finally {
    try {
        if (rs != null) rs.close();
    } catch (SQLException e) {
        System.out.println("Errore nella chiusura del ResultSet");
    }
    try {
        if (ps != null) ps.close();
    } catch (SQLException e) {
        System.out.println("Errore nella chiusura dello statement");
    }
    try {
        if (conn != null) conn.close();
    } catch (SQLException e) {
        System.out.println("Errore nella chiusura della connessione");
    }
}
```

Si può scrivere in modo più compatto con un metodo che chiude una risorsa, ma all'esame conviene la forma esplicita: è letterale, riconoscibile, e non può essere giudicata «diversa da quella richiesta».

### 21.8.3 `try-with-resources`: la forma alternativa

`Connection`, `Statement`, `PreparedStatement` e `ResultSet` realizzano `AutoCloseable` (il loro `close()` è dichiarato in quell'interfaccia), e quindi si possono usare con il `try-with-resources` presentato nel [Capitolo 13](13-eccezioni.md), paragrafo 13.5.4: le risorse si dichiarano tra parentesi dopo `try`, e il compilatore genera la chiusura, in ordine inverso, anche in caso di eccezione.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ConTryWithResources {
    public static void main(String[] args) {
        String sql = "SELECT titolo FROM libro WHERE autore = ? ORDER BY id";
        try (Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, "Calvino");
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    System.out.println(rs.getString("titolo"));
                }
            }
        } catch (SQLException e) {
            System.out.println("Errore SQL: " + e.getMessage());
        }
    }
}
```

```text
Il barone rampante
Le città invisibili
```

È più breve, e non ha il rischio di dimenticare un `close`. Ma ricordiamo l'avviso del Capitolo 13:

> [!WARNING]
> **Attenzione — Se la traccia impone il `finally`, niente `try-with-resources`**
> Se la traccia chiede che la chiusura avvenga «nel blocco `finally`», o che le stampe stiano nel `finally`, o che si usino tutte le cinque parole chiave delle eccezioni, il `try-with-resources` **non** soddisfa la richiesta: il blocco `finally` non compare nel sorgente, e la valutazione guarda alla struttura imposta, non soltanto all'output. In quel caso va usato esclusivamente lo schema del paragrafo 21.8.2. Se la traccia non dice nulla, entrambe le forme sono valide.

---

## 21.9 Dalle righe agli oggetti

### 21.9.1 La classe e il metodo

Nei programmi veri il risultato di una interrogazione non si stampa soltanto: si trasforma in **oggetti** della classe che rappresenta i dati, da usare nel resto del programma e da restituire a chi chiama il metodo. Come nel caricamento di un documento XML ([Capitolo 20](20-xml.md), paragrafo 20.4.7) e nella lettura da file ([Capitolo 14](14-file-di-testo.md)), lo schema è sempre lo stesso: **un oggetto per ogni riga**, raccolti in una `List`.

La classe `Libro` ha un campo per ogni colonna e un costruttore che li riceve:

```java
class Libro {
    private int id;
    private String titolo;
    private String autore;
    private int anno;
    private double prezzo;

    public Libro(int id, String titolo, String autore, int anno, double prezzo) {
        this.id = id;
        this.titolo = titolo;
        this.autore = autore;
        this.anno = anno;
        this.prezzo = prezzo;
    }

    @Override
    public String toString() {
        return id + ": " + titolo + " (" + autore + ", " + anno + ")";
    }
}
```

Il metodo che interroga il database riceve il criterio di ricerca come parametro (da qui il `PreparedStatement`), riempie la lista scorrendo il `ResultSet` e la restituisce. Se qualcosa va storto restituisce `null`, una convenzione che le tracce usano spesso per dire «non è stato possibile» ([Capitolo 8](08-riferimenti-e-memoria.md), paragrafo 8.3.4). Va distinta dal caso «nessun risultato»: una lista **vuota**, non `null`.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

class Libro {
    private int id;
    private String titolo;
    private String autore;
    private int anno;
    private double prezzo;

    public Libro(int id, String titolo, String autore, int anno, double prezzo) {
        this.id = id;
        this.titolo = titolo;
        this.autore = autore;
        this.anno = anno;
        this.prezzo = prezzo;
    }

    @Override
    public String toString() {
        return id + ": " + titolo + " (" + autore + ", " + anno + ")";
    }
}

public class Negozio {
    public static List<Libro> libriDi(String autore) {
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement("SELECT id, titolo, autore, anno, prezzo FROM libro WHERE autore = ? ORDER BY id");
            ps.setString(1, autore);
            rs = ps.executeQuery();
            List<Libro> libri = new ArrayList<>();                  // lista vuota: finora nessuna riga
            while (rs.next()) {
                libri.add(new Libro(rs.getInt("id"), rs.getString("titolo"), rs.getString("autore"),
                        rs.getInt("anno"), rs.getDouble("prezzo")));
            }
            return libri;                                           // vuota se l'autore non c'e'
        } catch (SQLException e) {
            return null;                                            // non e' stato possibile
        } finally {
            try {
                if (rs != null) rs.close();
            } catch (SQLException e) {
                // chiusura fallita: non c'e' altro da fare
            }
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
            }
        }
    }

    public static void main(String[] args) {
        List<Libro> calvino = libriDi("Calvino");
        for (Libro l : calvino) {
            System.out.println(l);
        }
        System.out.println("Libri di Joyce: " + libriDi("Joyce").size());
    }
}
```

```text
1: Il barone rampante (Calvino, 1957)
2: Le città invisibili (Calvino, 1972)
Libri di Joyce: 0
```

Due punti meritano attenzione. Il `return libri;` sta **dentro** il `try`: il `finally` viene eseguito comunque prima del ritorno ([Capitolo 13](13-eccezioni.md), paragrafo 13.5.2), quindi le risorse sono chiuse. E la lista è costruita **prima** del ciclo: i dati sono già copiati in oggetti `Libro` quando il `ResultSet` viene chiuso, quindi il chiamante li può usare senza più dipendere dalla connessione.

### 21.9.2 Un metodo che modifica e restituisce un esito

Per le operazioni di scrittura, un metodo restituisce spesso un `boolean` («è andata a buon fine?») oppure il numero di righe toccate. Il metodo seguente inserisce un libro e riceve come parametri i singoli valori da scrivere:

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class Inserimento {
    public static boolean inserisci(int id, String titolo, String autore, int anno, double prezzo) {
        Connection conn = null;
        PreparedStatement ps = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement("INSERT INTO libro (id, titolo, autore, anno, prezzo) VALUES (?, ?, ?, ?, ?)");
            ps.setInt(1, id);
            ps.setString(2, titolo);
            ps.setString(3, autore);
            ps.setInt(4, anno);
            ps.setDouble(5, prezzo);
            return ps.executeUpdate() == 1;                        // true se e' stata inserita una riga
        } catch (SQLException e) {
            return false;                                          // per esempio chiave primaria duplicata
        } finally {
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("Nuovo libro: " + inserisci(8, "Il cavaliere inesistente", "Calvino", 1959, 9.5));
        System.out.println("Id duplicato: " + inserisci(1, "Doppione", "Anonimo", 2000, 1.0));
    }
}
```

```text
Nuovo libro: true
Id duplicato: false
```

Il secondo inserimento viola la chiave primaria (l'`id` 1 esiste già): il database rifiuta e `executeUpdate` lancia `SQLException`, che il metodo trasforma in `false`.

---

## 21.10 Cenni: metadati, `RowSet`, procedure memorizzate, pool di connessioni

Questo paragrafo elenca gli strumenti di JDBC che il corso nomina ma che in genere non servono per scrivere un esercizio. Basta riconoscerli.

### 21.10.1 Metadati

I **metadati** (*metadata*) sono «dati sui dati»: informazioni sulla struttura. JDBC ne conosce due tipi:

- i metadati del **database**: `DatabaseMetaData`, che si ottiene con `conn.getMetaData()` e risponde a domande come «che prodotto sei?», con `getDatabaseProductName()` e `getDatabaseProductVersion()`;
- i metadati di un **`ResultSet`**: `ResultSetMetaData`, con `rs.getMetaData()`, che descrive le colonne del risultato: `getColumnCount()` (quante sono), `getColumnName(int)` (il nome della colonna numero *n*, da 1).

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

public class StampaColonne {
    public static void main(String[] args) throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT titolo, anno FROM libro");
        ResultSetMetaData md = rs.getMetaData();                    // descrive le colonne del risultato
        for (int i = 1; i <= md.getColumnCount(); i++) {            // le colonne partono da 1
            System.out.println(i + ": " + md.getColumnName(i));
        }
        conn.close();
    }
}
```

```text
1: titolo
2: anno
```

Uno stesso programma può servire per qualunque tabella, perché si legge dalla struttura il numero e il nome delle colonne, senza conoscerli in anticipo.

> [!NOTE]
> **Approfondimento esterno — `ResultSetMetaData` e `DatabaseMetaData`**
> La documentazione ufficiale descrive `ResultSetMetaData.getColumnCount()` come il metodo che restituisce «*the number of columns in this ResultSet object*», e `getColumnName(int column)` come il metodo che restituisce il nome della colonna indicata («*the first column is 1, the second is 2, …*»). `DatabaseMetaData.getDatabaseProductName()` restituisce il nome del prodotto database e `getDatabaseProductVersion()` il suo numero di versione; tutti questi metodi dichiarano `throws SQLException`.
>
> *Fonte:* [ResultSetMetaData](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/ResultSetMetaData.html) e [DatabaseMetaData](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/DatabaseMetaData.html) (Java SE 17)

### 21.10.2 `RowSet`

Il `ResultSet` ha un limite: deve restare collegato alla sorgente dei dati. Non si può **serializzare** né spedire per rete ([Capitolo 15](15-stream-binari-e-serializzazione.md), [Capitolo 19](19-networking.md)). Il **`RowSet`** è l'interfaccia (package `javax.sql`) che supera il limite: è un insieme di righe che può anche **memorizzare i dati e scollegarsi** dal database, essere serializzato e modificato da scollegato. Ne esistono tre realizzazioni:

| Realizzazione | Caratteristiche |
|---|---|
| `CachedRowSet` | scollegato dalla sorgente, scorrevole, serializzabile |
| `JdbcRowSet` | resta collegato alla sorgente |
| `WebRowSet` | estende `CachedRowSet` e può produrre una rappresentazione del suo contenuto in **XML** |

### 21.10.3 Procedure memorizzate: `CallableStatement`

Una **procedura memorizzata** (*stored procedure*) è un sottoprogramma salvato nel database, fatto di istruzioni SQL e di costrutti di programmazione, con eventuali argomenti e valori di ritorno. Vantaggi: incapsulamento e riuso, controllo delle transazioni, standardizzazione; svantaggio: è specifica del produttore, quindi si perde l'indipendenza dal database. In JDBC la terza specie di comando, `CallableStatement`, serve per chiamarle:

```java
CallableStatement prepareCall(String sql) throws SQLException      // in Connection
```

La chiamata si scrive nella forma `{call nomeProcedura(?, ?)}`. Ogni parametro ha una modalità: `IN` (ingresso), `OUT` (uscita), `INOUT` (entrambe). Non entreremo nei dettagli.

### 21.10.4 `DataSource` e pool di connessioni

Aprire una connessione costa tempo: se un'applicazione ne apre e ne chiude migliaia, conviene tenerne un certo numero aperte e **riutilizzarle**. Questo insieme si chiama **pool di connessioni** (*connection pooling*). Lo strumento standard per ottenere connessioni da un pool, o in generale da una sorgente configurata a parte, è l'interfaccia `javax.sql.DataSource`, che la documentazione ufficiale indica come il modo preferito di connettersi a una sorgente di dati: le proprietà (server, porta) si cambiano senza modificare il codice che la usa. Per gli esercizi d'esame resta valido `DriverManager`.

> [!NOTE]
> **Approfondimento esterno — `javax.sql.DataSource`**
> La documentazione ufficiale descrive `DataSource` come «*a factory for connections to the physical data source that this DataSource object represents*» e come alternativa a `DriverManager`: «*the preferred means of getting a connection*». L'interfaccia è realizzata dal produttore del driver in tre varianti: una base, che produce una `Connection` normale; una con *connection pooling*, che produce connessioni che partecipano automaticamente al pool; una per le transazioni distribuite. Un oggetto `DataSource` è tipicamente registrato presso un servizio di nomi basato su JNDI.
>
> *Fonte:* [DataSource (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html)

### 21.10.5 Il registro di `DriverManager`

Il `DriverManager` può scrivere un registro (*log*) delle proprie operazioni: `DriverManager.setLogWriter(PrintWriter)` indica dove, e `DriverManager.println(String)` vi scrive un messaggio. Serve per diagnosticare problemi di connessione. Un `PrintWriter` si costruisce intorno a qualunque `Writer` o `OutputStream` ([Capitolo 14](14-file-di-testo.md)).

---

## 21.11 Dalla traccia al codice

Le parole di una traccia sull'accesso ai database si traducono in scelte precise. La tabella ricapitola i nomi che **vanno scritti al carattere**: un nome inventato per analogia è un errore di compilazione, e un errore di compilazione consuma comunque una delle cinque esecuzioni.

| La traccia (o il programma) vuole… | Si scrive esattamente… | Attenzione |
|---|---|---|
| aprire la connessione | `DriverManager.getConnection(url, utente, password)` | `static`, `Manager` è una parola sola; dichiara `SQLException` |
| un comando senza parametri | `conn.createStatement()` | non `getStatement`, non `createStatment` |
| un comando con parametri | `conn.prepareStatement(sql)` | `prepareStatement` (non `preparedStatement`); la stringa SQL va **qui**, non in `executeQuery` |
| segnaposto | `?` nella stringa SQL | mai tra apici; solo al posto dei valori |
| impostare un parametro | `ps.setString(1, v)`, `ps.setInt(2, n)`, `ps.setDouble(3, x)` | l'indice parte da **1**; il metodo segue il tipo |
| una interrogazione (`SELECT`) | `ResultSet rs = ps.executeQuery()` | con `PreparedStatement` **senza argomenti**; con `Statement`, la stringa |
| una modifica (`INSERT`, `UPDATE`, `DELETE`) | `int n = ps.executeUpdate()` | restituisce le righe toccate |
| scorrere le righe | `while (rs.next())` | `next()` prima di ogni lettura, anche della prima |
| leggere una colonna | `rs.getString("titolo")`, `rs.getInt(2)`, `rs.getDouble("prezzo")` | colonne da **1**; il nome non distingue maiuscole |
| una sola riga | `if (rs.next())` | `else` per il caso «non trovato» |
| «in caso di fallimento restituisce `null`» | `catch (SQLException e) { return null; }` | non confondere con lista vuota |
| «chiudi nel `finally`» | `finally { … close() … }` | ciascun `close` con la guardia `!= null` e il proprio `try`/`catch` |
| «gestisci l'errore di SQL» | `catch (SQLException e)` | l'eccezione è controllata |
| «carica il driver» | `Class.forName("nome.completo.Driver")` | solo se richiesto; dichiara `ClassNotFoundException` |

Una raccomandazione di metodo: la struttura di quasi ogni esercizio è la stessa, e conviene scriverla di seguito, in questo ordine, senza pensarci: *variabili a `null` fuori dal `try`; `getConnection`; `prepareStatement` con i `?`; i `setXxx`; `executeQuery` o `executeUpdate`; (per le interrogazioni) il `while (rs.next())` con i `getXxx` e l'aggiunta alla lista; `return`; `catch (SQLException)`; `finally` con tre chiusure protette*.

---

## Scheletri da esame

Questi frammenti sono i minimi da saper scrivere a memoria su un editor senza aiuti. Ciascuno compila così com'è, con la tabella `libro` del capitolo nello stato iniziale.

### Scheletro 1 — Interrogazione con `PreparedStatement`: una lista di risultati

**Quando si usa.** «Scrivi un metodo che, dato un autore, restituisce i suoi titoli».

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class Scheletro1 {
    public static List<String> titoliDi(String autore) {
        Connection conn = null;                                     // 1. fuori dal try, a null
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement("SELECT titolo FROM libro WHERE autore = ? ORDER BY id");
            ps.setString(1, autore);                                // indici da 1
            rs = ps.executeQuery();                                 // senza argomenti
            List<String> titoli = new ArrayList<>();
            while (rs.next()) {                                     // next() prima di ogni lettura
                titoli.add(rs.getString("titolo"));
            }
            return titoli;
        } catch (SQLException e) {
            return null;                                            // fallimento
        } finally {
            try {
                if (rs != null) rs.close();                         // 3. guardia != null
            } catch (SQLException e) {                              // 4. close() dichiara SQLException
            }
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
            }
        }
    }

    public static void main(String[] args) {
        System.out.println(titoliDi("Svevo"));
        System.out.println(titoliDi("Calvino"));
    }
}
```

```text
[La coscienza di Zeno]
[Il barone rampante, Le città invisibili]
```

**Eccezioni e import.** Sette `import`: cinque da `java.sql` e due da `java.util`. L'unica eccezione, `SQLException`, è catturata; nessun `throws` nella firma. Gli indici di `setString` partono da 1; `executeQuery()` non ha argomenti.

### Scheletro 2 — Modifica con `executeUpdate`, esito `boolean` o conteggio

**Quando si usa.** «Aumenta il prezzo dei libri di un autore e restituisci quanti ne hai modificati».

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class Scheletro2 {
    public static int aumentaPrezzi(String autore, double importo) {
        Connection conn = null;
        PreparedStatement ps = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement("UPDATE libro SET prezzo = prezzo + ? WHERE autore = ?");
            ps.setDouble(1, importo);                               // primo ?: un reale
            ps.setString(2, autore);                                // secondo ?: un testo
            return ps.executeUpdate();                              // righe modificate
        } catch (SQLException e) {
            return -1;                                              // errore: nessun conteggio valido
        } finally {
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
            }
        }
    }

    public static void main(String[] args) {
        System.out.println(aumentaPrezzi("Pirandello", 0.5));
        System.out.println(aumentaPrezzi("Joyce", 0.5));
    }
}
```

```text
2
0
```

**Eccezioni e import.** Quattro `import` da `java.sql`. `executeUpdate()` restituisce `int`: il numero di righe toccate (`0` se nessuna, non è un errore). Il valore `-1` per l'errore è una convenzione di questo esempio: un conteggio valido non è mai negativo, quindi `-1` non si confonde con un risultato.

### Scheletro 3 — Una sola riga, `if (rs.next())`, `null` se non c'è

**Quando si usa.** «Cerca il libro con quell'`id`; se non esiste restituisce `null`».

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class Scheletro3 {
    public static String titoloDi(int id) {
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            ps = conn.prepareStatement("SELECT titolo FROM libro WHERE id = ?");
            ps.setInt(1, id);                                       // la chiave e' un intero
            rs = ps.executeQuery();
            if (rs.next()) {                                        // al massimo una riga: if, non while
                return rs.getString("titolo");
            }
            return null;                                            // nessuna riga: non e' un errore
        } catch (SQLException e) {
            return null;
        } finally {
            try {
                if (rs != null) rs.close();
            } catch (SQLException e) {
            }
            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
            }
        }
    }

    public static void main(String[] args) {
        System.out.println(titoloDi(3));
        System.out.println(titoloDi(99));
    }
}
```

```text
La coscienza di Zeno
null
```

**Eccezioni e import.** Cinque `import` da `java.sql`. Il `return` dentro il `try` non salta il `finally`: la chiusura avviene comunque.

### Scheletro 4 — `Statement` semplice: contare le righe

**Quando si usa.** Comando SQL fisso e senza parametri (`COUNT(*)`): basta `Statement`.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class Scheletro4 {
    public static int contaLibri() {
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/negozio", "root", "password");
            stmt = conn.createStatement();                          // nessun parametro
            rs = stmt.executeQuery("SELECT COUNT(*) FROM libro");   // la stringa SQL va qui
            rs.next();                                              // COUNT(*) restituisce sempre una riga
            return rs.getInt(1);                                    // la colonna senza nome: per posizione
        } catch (SQLException e) {
            return -1;
        } finally {
            try {
                if (rs != null) rs.close();
            } catch (SQLException e) {
            }
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
            }
            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("Libri: " + contaLibri());
    }
}
```

```text
Libri: 5
```

**Eccezioni e import.** Cinque `import` da `java.sql`. Con `Statement` la stringa SQL è argomento di `executeQuery(String)`; con `PreparedStatement` è argomento di `prepareStatement(String)` e `executeQuery()` non ha argomenti.

---

## Errori tipici

> [!CAUTION]
> **Errore tipico — Indice delle colonne o dei parametri da zero**
> ```java
> // ERRORE a runtime: SQLException
> rs.getString(0);                         // le colonne partono da 1
> ps.setString(0, "Svevo");                // anche i parametri partono da 1
> ```
> Il compilatore non si accorge di niente, e l'esecuzione si interrompe con una `SQLException` dal messaggio dipendente dal driver. Forma corretta: `rs.getString(1)` e `ps.setString(1, "Svevo")`. Se si vuole evitare il problema alla radice, si leggono le colonne **per nome**.

> [!CAUTION]
> **Errore tipico — Leggere il `ResultSet` senza `next()`**
> ```java
> ResultSet rs = ps.executeQuery();
> String t = rs.getString("titolo");        // ERRORE a runtime: il cursore e' prima della prima riga
> ```
> Subito dopo `executeQuery` il cursore sta **prima** della prima riga: leggere una colonna lancia `SQLException`. Forma corretta: `if (rs.next()) { ... }` per una riga, `while (rs.next()) { ... }` per tutte. Anche dopo il `while`, quando `next()` ha restituito `false`, il cursore è dopo l'ultima riga e non si può più leggere.

> [!CAUTION]
> **Errore tipico — `executeQuery` per una modifica, `executeUpdate` per un `SELECT`**
> ```java
> ps = conn.prepareStatement("DELETE FROM libro WHERE id = ?");
> ps.setInt(1, 4);
> ResultSet rs = ps.executeQuery();         // ERRORE a runtime: l'istruzione non restituisce righe
> int n = ps.executeUpdate();               // giusto per DELETE; per SELECT sarebbe sbagliato
> ```
> Il metodo si sceglie dal tipo di istruzione: `SELECT` va con `executeQuery`, tutto il resto (`INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE`) con `executeUpdate`. Un errore qui compila, ma lancia `SQLException` e consuma un'esecuzione.

> [!CAUTION]
> **Errore tipico — La stringa SQL passata a `executeQuery` di un `PreparedStatement`**
> ```java
> PreparedStatement ps = conn.prepareStatement("SELECT titolo FROM libro WHERE autore = ?");
> ps.setString(1, "Svevo");
> ResultSet rs = ps.executeQuery("SELECT titolo FROM libro WHERE autore = ?");   // ERRORE
> ```
> Per un `PreparedStatement` la stringa SQL si dà **una volta sola**, a `prepareStatement`; `executeQuery()` e `executeUpdate()` non hanno argomenti. Le forme con la stringa appartengono a `Statement` e, su un `PreparedStatement`, lanciano `SQLException`. Forma corretta: `ps.executeQuery()`.

> [!CAUTION]
> **Errore tipico — Costruire l'SQL per concatenazione con valori che arrivano da fuori**
> ```java
> String sql = "SELECT titolo FROM libro WHERE autore = '" + autore + "'";   // fragile e pericoloso
> ```
> Se `autore` contiene un apice (`D'Annunzio`) la stringa non è più SQL valido (`SQLException`); se è scelto da un malintenzionato (`x' OR '1'='1`) la query restituisce tutto (paragrafo 21.7.1). Forma corretta: un `PreparedStatement` con il segnaposto e `ps.setString(1, autore)`.

> [!CAUTION]
> **Errore tipico — Il segnaposto tra apici, o al posto di un nome**
> ```java
> conn.prepareStatement("SELECT titolo FROM libro WHERE autore = '?'");   // il ? non e' piu' un segnaposto
> conn.prepareStatement("SELECT * FROM ?");                               // un ? non sostituisce un nome di tabella
> ```
> Nella prima riga `'?'` è un testo composto da un punto interrogativo: non esistono parametri, e `setString(1, ...)` lancia `SQLException`. Nella seconda, un segnaposto può stare soltanto al posto di un **valore**, mai di un nome di tabella o di colonna. Forma corretta: `autore = ?` senza apici.

> [!CAUTION]
> **Errore tipico — Il metodo `setXxx` sbagliato per il tipo**
> ```java
> ps.setString(2, 212);                    // ERRORE di compilazione: int non e' una String
> ps.setInt(1, "Svevo");                   // ERRORE di compilazione: String non e' un int
> ```
> Il metodo segue il tipo del valore: `setString` per `String`, `setInt` per `int`, `setDouble` per `double`. Il compilatore segnala `incompatible types`, e l'esecuzione è persa.

> [!CAUTION]
> **Errore tipico — SQL scritto male: la virgola dimenticata e il `WHERE` mancante**
> ```java
> conn.prepareStatement("UPDATE libro SET titolo = ? anno = ?");        // manca la virgola
> conn.prepareStatement("UPDATE libro SET prezzo = ?");                 // senza WHERE: modifica TUTTE le righe
> ```
> La prima stringa compila ma è SQL non valido: il database rifiuta con `SQLException` (e il compilatore non lo vede, perché per Java l'SQL è soltanto una `String`). La seconda è SQL valido ma modifica ogni riga della tabella. Forma corretta: `UPDATE libro SET titolo = ?, anno = ? WHERE id = ?`.

> [!CAUTION]
> **Errore tipico — Eccezioni controllate non gestite**
> ```java
> public static void main(String[] args) {
>     Connection conn = DriverManager.getConnection(URL, "root", "password");   // ERRORE di compilazione
>     Statement stmt = conn.createStatement();
> }
> ```
> `SQLException` è controllata: quasi ogni metodo di JDBC la dichiara. Il compilatore segnala `error: unreported exception SQLException; must be caught or declared to be thrown`. Forma corretta: `throws SQLException` sul metodo, oppure `try`/`catch (SQLException e)`. Se si carica anche il driver con `Class.forName`, c'è una seconda eccezione controllata, `ClassNotFoundException`, da gestire.

> [!CAUTION]
> **Errore tipico — Le risorse non vengono chiuse (o si chiude senza controllare `null`)**
> ```java
> Connection conn = DriverManager.getConnection(URL, "root", "password");
> PreparedStatement ps = conn.prepareStatement(sql);
> ...                                       // mai chiuso: la connessione resta occupata sul server
> ```
> ```java
> // altra variante: il close nel finally senza guardia
> } finally {
>     conn.close();                         // NullPointerException se getConnection e' fallita; e dichiara SQLException
> }
> ```
> La prima forma accumula connessioni aperte fino a esaurire il numero ammesso dal server. La seconda, quando `getConnection` fallisce, trova `conn == null` e lancia `NullPointerException`, che nasconde l'errore vero. Forma corretta: variabile dichiarata fuori dal `try`, a `null`; nel `finally`, `if (conn != null)` con il proprio `try`/`catch` per `SQLException` (paragrafo 21.8.2).

> [!CAUTION]
> **Errore tipico — Usare `try-with-resources` quando la traccia impone il `finally`**
> ```java
> // la traccia chiede: "chiudi la connessione nel blocco finally"
> try (Connection conn = DriverManager.getConnection(URL, "root", "password")) { ... }   // nessun finally
> ```
> Il programma funziona ma non rispetta la struttura richiesta: il blocco `finally` non compare nel sorgente, e il docente valuta l'aderenza letterale. Forma corretta: lo schema del paragrafo 21.8.2 con `finally` esplicito.

> [!CAUTION]
> **Errore tipico — Usare il `ResultSet` dopo la chiusura**
> ```java
> public static ResultSet tutti() throws SQLException {
>     Connection conn = DriverManager.getConnection(URL, "root", "password");
>     Statement stmt = conn.createStatement();
>     ResultSet rs = stmt.executeQuery("SELECT * FROM libro");
>     conn.close();                          // chiude anche il ResultSet
>     return rs;                             // il chiamante trova un ResultSet chiuso: SQLException
> }
> ```
> Il `ResultSet` dipende dallo `Statement` e dalla connessione. Un metodo che chiude la connessione non può restituire il `ResultSet`. Forma corretta: leggere le righe dentro il metodo, trasformarle in oggetti e restituire la `List` (paragrafo 21.9).

> [!CAUTION]
> **Errore tipico — Nomi di metodi e classi inventati per analogia**
> ```java
> Connection c = Driver.Manager.getConnection(url);                      // DriverManager, una sola parola
> Statement s = c.getStatement();                                        // createStatement
> PreparedStatement p = c.preparedStatement(sql);                        // prepareStatement
> ResultSet r = s.executeQuerry("SELECT ...");                           // executeQuery
> while (r.hasNext()) { ... }                                            // next(), non hasNext()
> ```
> Ogni riga produce `error: cannot find symbol`, e un errore di compilazione consuma comunque un'esecuzione. I nomi vanno memorizzati al carattere (tabella del paragrafo 21.11): `DriverManager`, `createStatement`, `prepareStatement`, `executeQuery`, `executeUpdate`, `next`.

> [!CAUTION]
> **Errore tipico — `NULL` letto come numero**
> ```java
> int anno = rs.getInt("anno");             // se la cella e' NULL restituisce 0, senza errore
> if (anno == 0) { ... }                    // 0 significa "zero" o "assente"?
> ```
> `getInt` e gli altri `getXxx` di tipo primitivo restituiscono `0` per un valore `NULL`: la confusione tra «zero» e «assente» non genera errori ma risultati sbagliati. Forma corretta: chiamare `rs.wasNull()` subito dopo la lettura se la colonna può essere `NULL` (paragrafo 21.6.5).

> [!CAUTION]
> **Errore tipico — Il driver manca dal progetto**
> ```text
> java.sql.SQLException: No suitable driver found for jdbc:mysql://localhost:3306/negozio
> ```
> Il codice è corretto, ma a tempo di esecuzione il JAR del driver non è nel classpath. Il compilatore non può accorgersene, perché il programma usa solo interfacce di `java.sql`. Soluzione: aggiungere la dipendenza al `pom.xml` (paragrafo 21.4.1) o il JAR al classpath. Se l'URL è scritto male, lo stesso messaggio compare anche con il driver presente: il sottoprotocollo (`jdbc:mysql:`) deve essere esattamente quello del driver.

> [!CAUTION]
> **Errore tipico — Importare `java.sql.*` e `java.util.*` insieme**
> ```java
> import java.sql.*;
> import java.util.*;
> ...
> Date d = new Date();                       // ERRORE: reference to Date is ambiguous
> ```
> Esistono due classi `Date`, `java.util.Date` e `java.sql.Date`; con entrambi gli `import` con `*` il nome è ambiguo (`error: reference to Date is ambiguous`). Con gli import espliciti, che usiamo in tutto il capitolo, il problema non si presenta: si importa esattamente la classe che serve.

---

## Riassunto

Un programma che deve conservare molti dati e interrogarli per criteri diversi li affida a un **database relazionale**: tabelle di righe e colonne, a cui si parla in **SQL**. **JDBC** è la libreria standard (`java.sql`) con cui Java si collega a un database, manda comandi SQL e legge i risultati, nascondendo le differenze tra prodotti dietro interfacce comuni e **driver** specifici di ogni produttore (oggi quasi sempre di tipo IV, tutto Java). Il percorso è una **catena di oggetti**: `DriverManager.getConnection(url, utente, password)` produce una `Connection`; la connessione produce uno `Statement` (`createStatement()`, per SQL fisso) o un `PreparedStatement` (`prepareStatement(sql)`, per SQL con segnaposto `?`); `executeQuery` restituisce un `ResultSet` per i `SELECT`, `executeUpdate` restituisce il numero di righe toccate per `INSERT`, `UPDATE`, `DELETE` e DDL. Il `ResultSet` si legge con un **cursore** che parte *prima* della prima riga: `while (rs.next())` e i metodi `getXxx`, con colonne e parametri numerati da **1**. Quando i valori vengono dal programma, si usa `PreparedStatement`, che evita gli errori con gli apici e l'iniezione SQL. Tutte le risorse si **chiudono** in ordine inverso, nel `finally`, con la guardia `!= null` e un `try`/`catch` per ogni `close()`. `SQLException` è controllata: va dichiarata o catturata.

**Concetti chiave**

- **JDBC**: libreria standard (`java.sql`, `javax.sql`) per accedere ai database; interfacce comuni, implementazioni dei produttori.
- **Driver**: traduttore tra chiamate JDBC e un database specifico; quattro tipi (I ponte ODBC, II API nativa, III middleware, IV tutto Java). Va nel classpath; oggi si registra da solo.
- **URL JDBC**: `jdbc:sottoprotocollo:sottonome`, per esempio `jdbc:mysql://localhost:3306/negozio`.
- **`DriverManager`**: classe con soli metodi `static`; `getConnection` in tre forme; tutte dichiarano `SQLException`.
- **`Connection`**: la sessione aperta; limitata sul server, va sempre chiusa. In *auto-commit* ogni istruzione è definitiva.
- **`Statement`**: SQL fisso. `executeQuery(String)` per i `SELECT`, `executeUpdate(String)` per il resto.
- **`PreparedStatement`**: SQL con `?`; `setString`/`setInt`/`setDouble` con indice da 1; `executeQuery()`/`executeUpdate()` senza argomenti; difende dall'iniezione SQL.
- **`ResultSet`**: cursore che parte prima della prima riga; `next()` restituisce `false` alla fine; `getXxx` per posizione (da 1) o per nome; `NULL` si legge come `null` o `0`, e `wasNull()` lo distingue.
- **Dalle righe agli oggetti**: un oggetto per riga, in una `List` restituita dal metodo; `null` per il fallimento, lista vuota per «nessun risultato».
- **Chiusura**: `ResultSet`, poi `Statement`, poi `Connection`; `finally` con guardie `null` e `try`/`catch` separati; `try-with-resources` solo se la traccia non impone il `finally`.
- **Cenni**: `DatabaseMetaData`/`ResultSetMetaData`, `RowSet` (scollegato, serializzabile), `CallableStatement` per le procedure memorizzate, `DataSource` per i pool.

**API essenziali**

| Classe | Elemento | Firma | Eccezioni |
|---|---|---|---|
| `DriverManager` | `getConnection` | `static Connection getConnection(String url, String user, String password)` (anche `(String url)` e `(String url, Properties info)`) | `SQLException` |
| `Connection` | `createStatement` | `Statement createStatement()` | `SQLException` |
| `Connection` | `prepareStatement` | `PreparedStatement prepareStatement(String sql)` | `SQLException` |
| `Connection` | `close` | `void close()` | `SQLException` |
| `Statement` | `executeQuery` | `ResultSet executeQuery(String sql)` | `SQLException` |
| `Statement` | `executeUpdate` | `int executeUpdate(String sql)` | `SQLException` |
| `Statement` / `PreparedStatement` / `ResultSet` | `close` | `void close()` | `SQLException` |
| `PreparedStatement` | `setString`, `setInt`, `setDouble` | `void setString(int parameterIndex, String x)`, `void setInt(int parameterIndex, int x)`, `void setDouble(int parameterIndex, double x)` | `SQLException` |
| `PreparedStatement` | `executeQuery`, `executeUpdate` | `ResultSet executeQuery()`, `int executeUpdate()` | `SQLException` |
| `ResultSet` | `next` | `boolean next()` | `SQLException` |
| `ResultSet` | `getString`, `getInt`, `getDouble` | `String getString(int columnIndex)` / `(String columnLabel)`; `int getInt(…)`; `double getDouble(…)` | `SQLException` |
| `ResultSet` | `wasNull` | `boolean wasNull()` | `SQLException` |
| `ResultSet` | `getMetaData` | `ResultSetMetaData getMetaData()` | `SQLException` |
| `ResultSetMetaData` | `getColumnCount`, `getColumnName` | `int getColumnCount()`, `String getColumnName(int column)` | `SQLException` |
| `SQLException` | `getMessage`, `getSQLState`, `getErrorCode` | `String getMessage()`, `String getSQLState()`, `int getErrorCode()` | — |
