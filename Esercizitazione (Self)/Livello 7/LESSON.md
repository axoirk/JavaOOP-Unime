# Appunti su Apache Maven

## 1. Cos'è Apache Maven?
**Apache Maven** (termine yiddish che significa *"accumulatore di conoscenza"*) è uno strumento open source sviluppato dalla Apache Software Foundation per l'automazione della build, la gestione e la comprensione dei progetti software, principalmente (ma non esclusivamente) per l'ecosistema **Java**.

A differenza di strumenti procedurali più vecchi come Apache Ant (in cui bisognava specificare passo-passo *come* compilare il codice), Maven adotta un approccio **dichiarativo** basato sul concetto di **POM (Project Object Model)**. Si descrive *cosa* è il progetto, di quali librerie ha bisogno per funzionare e quali plugin utilizzare: al resto penserà il motore di Maven.

## 2. Perché si utilizza? I Vantaggi Principali
Maven risolve molti dei problemi storici dello sviluppo software offrendo vantaggi enormi che lo hanno reso lo standard di fatto:

* **Convention over Configuration (Convenzioni piuttosto che configurazione):** Maven impone una struttura di directory predefinita (ad es. `src/main/java` per il codice sorgente, `src/test/java` per i test, `target/` per l'output). Rispettando queste regole, non è necessario scrivere complessi script di compilazione. Questo abbatte i tempi di inserimento per i nuovi sviluppatori: chiunque conosca Maven saprà esattamente dove trovare i file in un nuovo progetto.
* **Gestione Automatica delle Dipendenze:** Invece di cercare manualmente in rete i file `.jar`, scaricarli e aggiungerli al progetto (rischiando problemi di versioning o di file mancanti), basta "dichiararli". Maven li scaricherà in automatico da server remoti, gestendo persino le **dipendenze transitive** (ovvero, scaricherà le librerie necessarie alle librerie che hai richiesto).
* **Standardizzazione e Automazione:** Automatizza processi di compilazione, esecuzione di unit test, creazione di archivi distribuibili (es. JAR, WAR) e rilascio, garantendo che il processo sia standard e ripetibile su qualsiasi macchina o server di Continuous Integration.
* **Generazione di Documentazione e Siti:** Sfruttando le informazioni definite nel progetto, genera report, metriche di codice e documentazione Javadoc sotto forma di sito web.

## 3. Architettura e Componenti Chiave

* **Goal:** Una singola funzione o comando eseguibile (es. la compilazione).
* **Plug-in:** Raccolte di Goal. Maven stesso è essenzialmente un framework vuoto; tutto il lavoro reale (compilazione, test, pacchettizzazione) viene delegato a specifici plugin (es. `maven-compiler-plugin`, `maven-surefire-plugin` per i test).
* **Repository:** L'infrastruttura dove Maven archivia e va a cercare le librerie (artefatti). Esistono principalmente tre tipi:
  * **Centrale / Remoto:** Server esterni (come il *Maven Central Repository*) da cui Maven scarica le librerie pubbliche di terze parti se non le possiede già.
  * **Locale:** Una cache sul tuo computer (solitamente la cartella `~/.m2/repository`). Quando Maven scarica una libreria remota, la salva qui per non doverla riscaricare in futuro.

## 4. Il Ciclo di Vita della Build (Build Lifecycle) e le Fasi
Il comportamento di esecuzione di Maven ruota attorno ai "Cicli di vita". Ne esistono 3 predefiniti:
1. **default (o build):** gestisce il deployment e la creazione vera e propria dell'artefatto.
2. **clean:** gestisce la pulizia del progetto dai vecchi file compilati (cartella `target/`).
3. **site:** gestisce la generazione della documentazione del progetto.

### Le Fasi del Default Lifecycle
Ogni ciclo è composto da una sequenza ben definita di **Fasi (Phases)**.
**La Regola Fondamentale di Maven:** *Invocare una specifica fase significa chiedere a Maven di eseguire prima e in ordine sequenziale tutte le fasi che la precedono nel ciclo di vita.*

Le fasi principali e più usate sono:
1. **`validate`**: Controlla che la struttura del progetto sia corretta e le informazioni necessarie siano presenti.
2. **`compile`**: Compila il codice sorgente (es. traduce i file `.java` in file `.class` all'interno della cartella `target/classes`).
3. **`test`**: Esegue i test automatizzati (Unit Tests con framework come JUnit). Se un test fallisce, l'intera esecuzione di Maven si interrompe (evitando di produrre pacchetti corrotti).
4. **`package`**: Impacchetta il codice appena compilato e testato in un formato distribuibile (es. archivio `.jar` per un'app desktop o `.war` per un'app web).
5. **`verify`**: Esegue controlli di qualità e test di integrazione sul pacchetto generato.
6. **`install`**: Installa l'artefatto nel **Repository Locale**, rendendolo disponibile come dipendenza per altri tuoi progetti locali.
7. **`deploy`**: Carica l'artefatto finale in un **Repository Remoto** (es. aziendale, come Nexus o Artifactory) per condividerlo con colleghi e altri team.

## 5. Il Cuore del Progetto: La struttura del POM (Project Object Model)
Tutte le direttive per Maven risiedono in un singolo file XML denominato **`pom.xml`**, localizzato nella root del progetto.
Ogni POM eredita di default configurazioni base e strutture standard da un file interno invisibile chiamato **Super POM**.

### Le Coordinate GAV
Per essere valido, ogni progetto deve definire le proprie *coordinate* univoche, conosciute come **GAV**:
* **`<groupId>`**: Identifica l'azienda, il team o il gruppo che gestisce il progetto (es. `com.universita.oop`). Spesso segue il nome a dominio invertito.
* **`<artifactId>`**: Il nome specifico del modulo o progetto (es. `sistema-gestionale`).
* **`<version>`**: La versione dell'artefatto corrente (es. `1.0.0-SNAPSHOT` dove "SNAPSHOT" indica che è in fase di sviluppo attivo).

### Gestione delle Dipendenze: Scope e Transitività
Le dipendenze esterne vengono dichiarate nel nodo `<dependencies>`. Due concetti avanzati molto importanti sono:
* **Dipendenze Transitive ed Esclusioni:** Maven scarica automaticamente l'albero completo delle dipendenze (librerie richieste dalle tue librerie). In caso di conflitti (versioni multiple della stessa libreria in rami diversi), Maven usa la regola della *"nearest definition"* (vince la dipendenza più vicina alla radice dell'albero). Si possono anche usare i tag `<exclusions>` per impedire il download di specifiche librerie transitive indesiderate.
* **Dependency Scopes (`<scope>`):** Regolano la visibilità di una libreria nelle varie fasi della build:
  * `compile` (default): La dipendenza è sempre presente in tutti i classpath e viene inclusa nel pacchetto.
  * `provided`: Richiesta per la compilazione, ma non impacchettata perché si assume che l'ambiente di esecuzione (es. un server Tomcat) la fornirà a runtime (es. Servlet API).
  * `runtime`: Non è richiesta per la compilazione, ma è fondamentale durante l'esecuzione (es. un driver JDBC per MySQL).
  * `test`: La libreria è visibile e necessaria solo per la compilazione e l'esecuzione della fase di test (es. JUnit o Mockito).

### Il tag `<build>` e la configurazione dei Plugin
Mentre le dipendenze aggiungono librerie al progetto, il blocco `<build>` serve a modificare il processo di compilazione e impacchettamento configurando i plugin di Maven:
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.8.1</version>
            <configuration>
                <source>11</source> <!-- Specifica la versione di Java per il codice sorgente -->
                <target>11</target> <!-- Specifica la versione del bytecode generato -->
            </configuration>
        </plugin>
    </plugins>
</build>
```
* **Distribuzione e Fat JAR (Maven Assembly Plugin):** Spesso si ha la necessità di distribuire l'applicativo non come semplice libreria, ma come eseguibile stand-alone (`java -jar ...`) che contenga al suo interno anche tutte le dipendenze esterne. Questo "mega-pacchetto" viene chiamato in gergo **Fat JAR** (o Uber JAR). Per realizzarlo, è necessario istruire Maven aggiungendo ai plugin il `maven-assembly-plugin`, indicandogli il descrittore `jar-with-dependencies` e specificando qual è la tua classe principale (`<mainClass>`).

### Strutture Avanzate del POM (Enterprise Features)
* **Ereditarietà (Inheritance):** Più progetti possono dichiarare un tag `<parent>` per ereditare versioni di dipendenze e plugin da un POM genitore. Perfetto per garantire che tutti i microservizi di un'azienda usino la stessa versione delle librerie.
* **Aggregazione (Multi-Module):** Un POM "Padre" (con `<packaging>pom</packaging>`) può includere un tag `<modules>` che elenca vari sotto-progetti. Lanciando Maven sul POM Padre, si attiverà la build automatica e concatenata di tutti i sottomoduli. Maven analizza internamente queste correlazioni tramite il suo motore chiamato **Reactor**, che stabilisce dinamicamente qual è l'ordine corretto in cui compilare i moduli in base alle loro interdipendenze.
* **Profili (Profiles):** Tramite il nodo `<profiles>` è possibile creare configurazioni condizionali che si attivano solo in determinati contesti (es. un profilo per l'ambiente di "Sviluppo" che usa un database in memoria, e uno per "Produzione" che usa Oracle). Si richiamano da riga di comando con l'opzione `-P nome-profilo`.

## 6. Utilizzo Pratico e Comandi Principali

### Generazione del progetto tramite Archetipi (Archetypes)
Per avviare un nuovo progetto non si creano le cartelle a mano. Maven fornisce gli **Archetipi**, ovvero dei *template* (modelli) preconfezionati di progetti.
Eseguendo da terminale `mvn archetype:generate`, Maven genererà automaticamente per te l'intero albero delle directory e un `pom.xml` di base.

### Comandi (CLI) più comuni
I comandi Maven (CLI) si costruiscono passando a `mvn` le fasi o i goal desiderati:
* `mvn clean`: Rimuove la cartella `/target`, assicurando che la successiva compilazione sia pulita e riparta da zero (evitando conflitti con vecchi file compilati).
* `mvn compile`: Traduce il codice sorgente senza fare altro.
* `mvn test`: Esegue gli unit test. Include intrinsecamente le fasi precedenti (quindi compila i sorgenti, compila i test, ed esegue i test).
* `mvn clean install`: **Il comando più celebre**. Esegue una pulizia del workspace, ricompila, testa, genera l'artefatto e lo salva nella cache locale (Repository Locale), rendendolo pronto all'uso per altri tuoi progetti.

### Lavorare con IntelliJ IDEA
Se utilizzi **IntelliJ IDEA**, è utile sapere che l'integrazione con Maven è nativa, permettendoti di gestire i progetti in totale facilità senza utilizzare obbligatoriamente la CLI:
* **Archetipi da UI:** Invece di usare `mvn archetype:generate` da terminale, andando su *File > New > Project*, puoi selezionare il generatore **"Maven Archetype"**, scegliere dalla lista il template che desideri (es. `maven-archetype-quickstart`) e l'IDE preparerà tutto in autonomia.
* **Aggiornamento delle Dipendenze:** Quando scrivi o modifichi un blocco `<dependency>` nel `pom.xml`, IntelliJ mostra un'icona "M" flottante per effettuare il *Load Maven Changes* (sincronizzazione). Cliccandola, avvierà il download dei JAR automaticamente.
* **Pannello Maven:** C'è un pannello "Maven" laterale molto utile (di solito a destra) con l'albero di tutti i tuoi *Lifecycle*. Con un semplice doppio click su `clean`, `install` o `package` avvierai i comandi di build.
* **Progetti Multi-Modulo:** IntelliJ facilita l'aggregazione di moduli. Creando un nuovo sottomodulo (*New > Module* su un progetto esistente), IntelliJ andrà a impostare automaticamente le relazioni: aggiungerà il tag `<modules>` nel `pom.xml` genitore, e preparerà il tag `<parent>` nel `pom.xml` del figlio.

---

## 7. JDBC: L'Architettura di Connessione ai Database Relazionali

### Teoria Fondamentale e Architettura
**JDBC (Java Database Connectivity)** è una libreria standard (`java.sql` e `javax.sql`) che permette ai programmi Java di connettersi ai database ed eseguire comandi SQL, astraendo i dettagli specifici di ogni vendor dietro un'API comune. Architetturalmente, JDBC si divide in due strati: l'**API JDBC** (usata dallo sviluppatore) e il **JDBC Driver Manager** (il motore che comunica fisicamente con i driver dei database).

### I Quattro Tipi di Driver JDBC
La connessione fisica dipende dal driver scelto. La teoria categorizza i driver in 4 classi architetturali:
1.  **Type I (JDBC-ODBC Bridge):** Mappa le chiamate JDBC all'accesso API ODBC. Soluzione obsoleta, inefficace e limitata alle sole capacità dell'ODBC sottostante.
2.  **Type II (Native API Driver):** Comunica interfacciandosi direttamente con le API native (C/C++) del database. Più veloce del Type I, ma lega il codice alla macchina fisica.
3.  **Type III (Network Protocol / Middleware):** Le chiamate passano tramite un protocollo di rete verso un *middleware server* che le traduce per il DB. Ottimo per architetture enterprise complesse.
4.  **Type IV (Thin Driver / All-Java):** Scritto interamente in Java, comunica direttamente col protocollo nativo del database. È il più efficiente, indipendente dalla piattaforma e non richiede librerie native (es. MySQL Connector/J).

### Classi Core e Workflow Operativo
Il ciclo di vita di una connessione JDBC segue passaggi rigorosi:
1.  **Il DriverManager:** Classe non istanziabile (metodi statici) che rintraccia i driver registrati. La chiamata `DriverManager.getConnection(url, user, password)` valuta la URL (es. `jdbc:mysql://localhost:3306/db`) e restituisce una sessione.
2.  **La Connection:** Rappresenta una sessione attiva. Avendo i database un limite di sessioni parallele, non chiudere una connessione genera *resource leak* critici.
3.  **Gli Statement (L'Esecuzione):**
    -   `Statement`: Per query semplici e statiche. Produce un ResultSet *forward-only* e *read-only*.
    -   `PreparedStatement`: **Il più importante**. Viene pre-compilato e messo in cache sul database, ottimizzando i tempi di esecuzione e prevenendo attacchi di **SQL Injection** tramite l'uso di placeholder (`?`).
    -   `CallableStatement`: Usato per invocare *Stored Procedures* residenti direttamente nel database.
4.  **Il ResultSet (I Dati):** Sfrutta il concetto di "Cursor". Alla creazione, il cursore è posizionato *prima* della prima riga. Il metodo `next()` sposta il cursore in avanti. **Attenzione:** in JDBC gli indici delle colonne partono da `1`, non da `0`.

#### Gestione Avanzata (RowSets e MetaData)
-   **RowSets:** A differenza del `ResultSet`, che richiede una connessione sempre aperta col database, i **RowSet** (introdotti nelle API javax.sql) possono essere **disconnessi**. Permettono di estrarre i dati, chiudere la connessione e continuare a manipolare i record localmente.
-   **MetaData:** JDBC permette di interrogare la struttura del database stesso. Usando `DatabaseMetaData` o `ResultSetMetaData`, si possono scoprire i nomi delle colonne, i tipi di dato e persino la versione del database a cui si è connessi senza scrivere query SQL specifiche.

*Esempio Teorico: Gestione Inventario (PreparedStatement e Finally)*
```java
String url = "jdbc:mysql://localhost:3306/magazzino";
// L'uso del try-with-resources garantisce la sacralità del '.close()' per evitare resource leak
try (Connection conn = DriverManager.getConnection(url, "admin", "admin123");
     PreparedStatement pstmt = conn.prepareStatement("SELECT nome, quantita FROM Prodotti WHERE categoria = ?")) {
    
    pstmt.setString(1, "Elettronica"); // Valorizzazione sicura del placeholder
    
    try (ResultSet rs = pstmt.executeQuery()) {
        while (rs.next()) {
            // Estrazione tramite nome colonna o indice (che in JDBC parte da 1)
            System.out.println(rs.getString("nome") + " - Qta: " + rs.getInt(2));
        }
    }
} catch (SQLException e) { 
    System.err.println("Errore di connessione o sintassi SQL: " + e.getMessage()); 
}
```

---

## 8. Il Paradigma NoSQL e i Database Documentali

### Oltre il Relazionale: L'assenza di Schema
Mentre i database SQL impongono uno schema rigido (tabelle, colonne, tipi di dato definiti a priori), i database **NoSQL** nascono per gestire strutture dati dinamiche, scalabili e non relazionali.

Due categorie principali nel panorama NoSQL sono:
1.  **Database Documentali (es. MongoDB):** Memorizzano le informazioni sotto forma di documenti simili al JSON (BSON). Non esistono "tabelle", ma **Collection**, e non esistono "righe", ma **Documenti**.
2.  **Time Series Database (es. InfluxDB):** Ottimizzati per gestire enormi volumi di dati legati al tempo (timestamp come chiave primaria), utili per IoT o telemetria. Strutturati in *Measurements* (la categoria), *Tags* (metadati indicizzati per la ricerca veloce) e *Fields* (i valori reali non indicizzati).

### L'Approccio Documentale (MongoDB in Java)
In MongoDB, l'assenza di schema (*schema-less*) permette di aggiungere campi a un documento "al volo" al momento dell'inserimento, rendendolo perfetto per salvare oggetti la cui struttura varia nel tempo o a seconda del contesto. Un documento ha sempre un campo obbligatorio `_id` che funge da chiave primaria.

L'interfacciamento in Java (tramite librerie come `mongo-java-driver`) prevede:
-   L'apertura di un `MongoClient`.
-   La selezione di un `MongoDatabase` e di una `MongoCollection`.
-   La manipolazione tramite l'oggetto `Document` nativo (che mappa essenzialmente un dizionario Chiave-Valore).

*Esempio Teorico: Inserimento Dati non Strutturati*
```java
// Connessione al server locale
try (MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017")) {
    // Selezione del DB e della Collection
    MongoDatabase database = mongoClient.getDatabase("unime_db");
    MongoCollection<Document> collection = database.getCollection("studenti");

    // Creazione di un documento dinamico
    Document studente = new Document("nome", "Mario")
                            .append("cognome", "Rossi")
                            // Possiamo inserire liste e strutture annidate!
                            .append("esami_superati", Arrays.asList("OOP", "Sistemi Operativi"));
    
    // Inserimento fire-and-forget
    collection.insertOne(studente);
    System.out.println("Documento NoSQL inserito con successo!");
}
```

---

## 9. Architetture Web con Spring Boot e REST

### Cos'è Spring Boot?
Spring Boot è l'evoluzione del framework Spring, progettata per creare applicazioni **stand-alone** e pronte per la produzione con configurazione minima. Sfrutta il concetto di **Inversion of Control (IoC)** per gestire i componenti dell'applicazione (Bean).

### Servizi RESTful
Il modello **REST (Representational State Transfer)** è lo standard per la comunicazione tra sistemi via HTTP.
-   **Risorse:** Tutto è una risorsa identificata da un URL (es. `/api/libri`).
-   **Verbi HTTP:** Si usano i metodi standard: `GET` (leggere), `POST` (creare), `PUT` (aggiornare), `DELETE` (eliminare).

### Annotazioni Chiave
-   **`@SpringBootApplication`:** Abilita la configurazione automatica.
-   **`@RestController`:** Segnala che la classe gestirà richieste web e restituirà dati (solitamente JSON).
-   **`@GetMapping("/percorso")`:** Mappa una funzione a una specifica richiesta GET.

*Esempio Teorico: Controller per un Catalogo (Spring)*
```java
@RestController
@RequestMapping("/api/catalogo")
public class CatalogoController {

    @GetMapping("/saluto")
    public String sayHello(@RequestParam(value = "nome", defaultValue = "Ospite") String nome) {
        return "Benvenuto nel catalogo, " + nome + "!";
    }
}
```

