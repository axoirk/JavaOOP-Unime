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

> ⚠️ **SEGNALAZIONE: ARGOMENTI MANCANTI E DA SPOSTARE RISPETTO AL NUOVO SYLLABUS**
> In base alla nuova organizzazione a 7 livelli:
> - **Questo intero file (Apache Maven) appartiene concettualmente al Livello 7.**
> - **Manca del tutto la teoria del Livello 5** (Thread, Programmazione concorrente, Runnable, Identificazione Thread, join/sleep/yield, Sincronizzazione e Comunicazione wait/notify). Attualmente, questa teoria risiede erroneamente all'interno del file `LESSON.md` del Livello 4.
