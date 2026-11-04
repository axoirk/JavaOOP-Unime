---
materia: Programmazione a Oggetti
capitolo: 22
titolo: "Ecosistema: Maven, Spring Boot, NoSQL"
livello_syllabus: 7
stato: completo
slide: ["Maven Java.pptx (Maven: vantaggi, componenti, comandi, struttura del pom.xml)", "Maven by Example (struttura di un progetto, POM, ciclo di vita, repository, dipendenze, archetipi, esecuzione)", "Apache Maven (fasi del ciclo di vita, POM, ereditarietà e aggregazione)", "SpringBoot.pdf (Spring Boot, annotazioni, IoC, bean)", "influxDBandJava.pptx (InfluxDB: modello dei dati)"]
appelli: []
fonti_esterne: 0
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 22 — Ecosistema: Maven, Spring Boot, NoSQL

## Di cosa parla questo capitolo

Fin qui abbiamo scritto programmi che stanno in uno o pochi file e li abbiamo compilati a mano con `javac` ([Capitolo 1](01-java-e-la-jvm.md)). Un programma vero ha bisogno di altro. Ha **molte classi** distribuite in più package ([Capitolo 7](07-classi-e-oggetti.md)); usa **librerie scritte da altri**, come il driver del database del [Capitolo 21](21-jdbc.md), e ciascuna di quelle librerie ne usa a sua volta altre; va **compilato, collaudato e impacchettato** sempre nello stesso modo, su qualsiasi computer. Fare tutto questo a mano, scaricando file `.jar` e scrivendo comandi lunghi, è noioso e fonte di errori.

L'**ecosistema** di Java è l'insieme degli strumenti che stanno attorno al linguaggio e risolvono questi problemi. In questo capitolo, che è volutamente **ridotto**, ne vediamo tre: che cosa sono, a che cosa servono, quali sono i concetti chiave e come si presenta un esempio minimo. Non ci sono scheletri da imparare a memoria, perché questo materiale non è da scrivere su un editor senza aiuti: serve a **capire come si costruisce e si fa girare un'applicazione Java reale**.

- **Maven** (paragrafo 22.2), lo strumento che costruisce il progetto: compila, gestisce le librerie, esegue i test, produce il file distribuibile.
- **Spring Boot** (paragrafo 22.3), un framework per scrivere applicazioni web: un programma Java a cui un browser si collega per chiedere pagine o dati.
- **I database NoSQL** (paragrafo 22.4), un modo di conservare i dati alternativo alle tabelle del [Capitolo 21](21-jdbc.md), con due esempi: i database a documenti (MongoDB) e quelli per serie temporali (InfluxDB).

Il capitolo riprende molto di ciò che sappiamo. Il file `pom.xml` di Maven è un documento **XML** ([Capitolo 20](20-xml.md)); le annotazioni di Spring sono annotazioni come `@Override` ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)); un server web è un'applicazione **client-server** ([Capitolo 19](19-networking.md)); i dati che l'applicazione conserva possono stare in un database relazionale ([Capitolo 21](21-jdbc.md)) oppure in uno NoSQL.

> [!IMPORTANT]
> **Nota per l'esame — Livello 7**
> Maven, Spring Boot e i database NoSQL appartengono al livello 7 del programma, l'«ecosistema» di strumenti attorno a Java. Nessun appello ufficiale finora ha proposto un esercizio su questi argomenti, e non ha senso chiedere di scriverne il codice senza aiuti: le domande tipiche sono di comprensione. A che cosa serve Maven e che ruolo ha il file `pom.xml`? Che cosa fa `@RestController`? Le risposte sono nel paragrafo 22.2.4 e nel paragrafo 22.3.5, e sono ripetute nel Riassunto.

---

## 22.1 Il problema: dal programma al progetto

### 22.1.1 Quello che `javac` da solo non fa

Immaginiamo un negozio online. Il programma ha una trentina di classi in sei package, usa il driver JDBC per parlare con il database, una libreria per formattare i testi e una per leggere i file di configurazione. Per costruirlo con i soli strumenti del [Capitolo 1](01-java-e-la-jvm.md) dovremmo:

1. cercare in rete ciascuna libreria, scaricarne il file `.jar` e metterlo in una cartella;
2. scoprire che quella libreria ne richiede altre tre, e scaricare anche quelle, nella versione giusta;
3. scrivere un comando `javac` con l'elenco di tutti i `.jar` nel *classpath* e di tutti i file sorgente;
4. rifare lo stesso per i collaudi, poi impacchettare le classi in un archivio, poi spiegare a un collega come rifare tutto sul suo computer.

Ogni passo è un'occasione di errore: una libreria nella versione sbagliata, un file dimenticato, una cartella con un nome diverso su due macchine. E ogni progetto, scritto da persone diverse, avrebbe una struttura diversa.

La soluzione è uno **strumento di costruzione** (*build tool*): un programma a cui si **descrive** il progetto (come si chiama, di quali librerie ha bisogno) e che si occupa di tutto il resto, sempre nello stesso modo.

### 22.1.2 Tre strumenti, tre problemi

| Strumento | Problema che risolve |
|---|---|
| **Maven** | costruire il progetto in modo standard e ripetibile: struttura delle cartelle, librerie, compilazione, collaudo, impacchettamento |
| **Spring Boot** | scrivere un'applicazione web con pochissima configurazione, perché sia raggiungibile da un browser o da altri programmi |
| **Database NoSQL** | conservare dati che non si adattano a righe e colonne fisse: documenti dalla struttura variabile, misurazioni che arrivano nel tempo |

I tre non sono alternativi: un'applicazione reale li usa insieme. Un progetto Spring Boot, per esempio, **è un progetto Maven**, e la libreria per parlare con un database MongoDB si aggiunge al progetto tramite Maven.

---

## 22.2 Maven

### 22.2.1 Che cos'è e perché si usa

**Apache Maven** è un progetto *open source* (il codice è libero e consultabile) sviluppato dalla Apache Software Foundation, che permette di organizzare in modo molto efficiente un progetto Java. I vantaggi che si ottengono sono quattro:

- la **standardizzazione della struttura** del progetto: le cartelle hanno sempre gli stessi nomi, quindi chi conosce Maven sa subito dove trovare ogni cosa in un progetto nuovo;
- la **compilazione, il collaudo e l'esportazione automatizzati**: con un comando solo si compila, si eseguono i test e si produce l'archivio da distribuire;
- la **gestione e il download automatico delle librerie** necessarie al progetto: si dichiara quale libreria serve, Maven la scarica;
- la **creazione automatica di un sito** di documentazione del progetto, con le informazioni raccolte.

> [!NOTE]
> **Definizione — Convenzione piuttosto che configurazione (*convention over configuration*)**
> È il principio per cui un sistema assume valori ragionevoli di partenza, in modo che funzioni senza configurazione inutile. Maven lo applica ai progetti: se non diciamo nulla, assume che il codice sorgente stia in `src/main/java`, i collaudi in `src/test`, le classi compilate in `target/classes` e che il progetto produca un archivio `.jar`. Basta mettere i file nei posti convenuti e Maven sa che cosa fare.

C'è anche una differenza di impostazione rispetto agli strumenti più vecchi (come Ant). In uno strumento **procedurale** si scrive *come* costruire: «il sorgente è in questa cartella, esegui `javac` su di essa, metti il risultato in quest'altra». Maven è **dichiarativo**: si scrive *che cosa* è il progetto, e il *come* è già stabilito dalle convenzioni e dai componenti di Maven (i *plugin*, paragrafo 22.2.7).

### 22.2.2 Installare Maven e controllare che funzioni

Maven si scarica dal sito ufficiale (`https://maven.apache.org`, pagina *download*), come archivio `.zip` o `.tar.gz`. Per installarlo basta **scompattare l'archivio** in una cartella e far sì che il computer lo trovi: si aggiunge la sua sottocartella `bin` alla variabile d'ambiente `PATH` (oppure, se si lavora in un ambiente di sviluppo, si indica all'ambiente dov'è Maven). Maven ha bisogno di una JDK, e cerca la sua posizione nella variabile d'ambiente `JAVA_HOME`.

Per controllare, si apre un terminale e si scrive:

```text
mvn -version
```

Il comando stampa la versione di Maven, la cartella dove è installato, la versione di Java in uso e il sistema operativo. Se il terminale risponde che il comando `mvn` non esiste, la cartella `bin` non è nel `PATH`.

### 22.2.3 La struttura di un progetto

Per convenzione, un progetto Maven ha questa forma:

```text
negozio/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── org/esempio/negozio/App.java
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
└── target/
```

- La cartella radice (qui `negozio`) si chiama **cartella base** del progetto e contiene il file `pom.xml`, il «cuore» del progetto (paragrafo 22.2.4).
- `src/main/java` contiene i **sorgenti Java** del programma. Dentro, le cartelle ricalcano i package ([Capitolo 7](07-classi-e-oggetti.md)): il file `App.java` che dichiara `package org.esempio.negozio;` sta in `org/esempio/negozio/`.
- `src/main/resources` contiene i file che non sono codice ma che il programma usa, come i file di configurazione.
- `src/test/java` e `src/test/resources` sono i corrispondenti per i **collaudi**, cioè il codice che controlla che il programma funzioni; non finiscono nell'archivio consegnato.
- `target` è creata da Maven: contiene tutto ciò che viene **prodotto** (le classi compilate in `target/classes`, l'archivio `.jar`). Si può cancellare in qualsiasi momento senza perdere nulla di scritto a mano, perché si rigenera.

Il sorgente `App.java` è una classe Java come tutte le altre:

```java
package org.esempio.negozio;

public class App {
    public static void main(String[] args) {
        System.out.println("Ciao dal progetto Maven!");
    }
}
```

Nessuna riga di questa classe sa di Maven: il programma è lo stesso che compileremmo a mano. Maven interviene attorno.

### 22.2.4 Il file `pom.xml`

> [!NOTE]
> **Definizione — POM (*Project Object Model*)**
> Il **POM** è la descrizione dichiarativa di un progetto Maven: scritto in un file XML chiamato `pom.xml` e posto nella cartella base, dice come si chiama il progetto, che cosa produce, di quali librerie ha bisogno e quali plugin usare. Maven lavora sempre «dentro» un POM: ogni operazione (compilare, impacchettare) legge il POM per sapere come comportarsi.

Questo è il POM più piccolo che possiamo scrivere per il nostro progetto:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>org.esempio</groupId>
  <artifactId>negozio</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
  </properties>
</project>
```

Leggiamolo dall'alto, ricordando che è un documento XML ([Capitolo 20](20-xml.md)): ogni elemento aperto va chiuso, e gli elementi sono annidati.

- La **prima riga** è la dichiarazione XML. L'elemento radice `<project>` porta gli attributi che indicano a quale schema il documento si conforma (`xmlns`, `xsi:schemaLocation`): sono parole fisse, che si ricopiano.
- `<modelVersion>` è la versione del modello di POM; vale sempre `4.0.0`.
- `<groupId>`, `<artifactId>` e `<version>` sono le **coordinate** del progetto, spiegate qui sotto.
- `<packaging>` dice che tipo di archivio produce il progetto: `jar` per un'applicazione o una libreria Java (è anche il valore predefinito), `war` per un'applicazione web destinata a un server, `pom` per un progetto che raccoglie altri progetti (paragrafo 22.2.12).
- `<properties>` raccoglie impostazioni con un nome. Qui: la codifica dei file sorgente (`UTF-8`) e la versione di Java per la compilazione (`maven.compiler.source` e `maven.compiler.target`, entrambe `17`).

**Le coordinate GAV**

Tre elementi identificano un progetto Maven in modo univoco, in tutto il mondo. Sono chiamate le **coordinate** del progetto, abbreviate **GAV** dalle iniziali:

| Elemento | Significato | Esempio |
|---|---|---|
| `groupId` | il gruppo, l'organizzazione o il team che produce il progetto; per convenzione inizia con il nome di dominio **rovesciato** | `org.esempio`, `org.apache.commons` |
| `artifactId` | il nome del progetto all'interno del gruppo | `negozio`, `commons-text` |
| `version` | la versione del progetto | `1.0-SNAPSHOT`, `1.12.0` |

Si scrivono spesso di seguito, separate da due punti: `org.esempio:negozio:1.0-SNAPSHOT`. Il suffisso `-SNAPSHOT` segnala una versione **in sviluppo**, ancora in cambiamento; una versione consegnata ha un numero fisso, come `1.0`. L'**artefatto** (*artifact*) è ciò che il progetto produce: nel nostro caso un file `negozio-1.0-SNAPSHOT.jar`, il cui nome Maven ricava dal POM (`<artifactId>-<version>.<packaging>`).

> [!TIP]
> **Intuizione — Le coordinate sono un indirizzo**
> Come un indirizzo individua una casa con città, via e numero, le coordinate individuano una libreria con gruppo, nome e versione. Per questo, quando un progetto dichiara di dipendere da un'altra libreria, gli basta citarne le coordinate: Maven sa dove andarla a prendere.

### 22.2.5 Le dipendenze

Le librerie di cui il progetto ha bisogno si dichiarano nell'elemento `<dependencies>`, una `<dependency>` per libreria, indicata con le sue coordinate. Per esempio, una libreria con funzioni di formattazione dei testi:

```xml
  <dependencies>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-text</artifactId>
      <version>1.12.0</version>
    </dependency>
  </dependencies>
```

L'elemento `<dependencies>` va dentro `<project>`, dopo `<properties>`. Un esempio dalle slide del corso è la dipendenza dal *driver* per MongoDB, che il programma Java usa per collegarsi a quel database (paragrafo 22.4.1):

```xml
  <dependencies>
    <dependency>
      <groupId>org.mongodb</groupId>
      <artifactId>mongo-java-driver</artifactId>
      <version>3.12.11</version>
    </dependency>
  </dependencies>
```

Una volta dichiarata la dipendenza, il codice può usare le classi della libreria con un normale `import`:

```java
package org.esempio.negozio;

import org.apache.commons.text.WordUtils;       // classe della libreria commons-text

public class App {
    public static void main(String[] args) {
        String titolo = "il barone rampante";
        System.out.println(WordUtils.capitalizeFully(titolo));   // iniziale maiuscola per ogni parola
    }
}
```

```text
Il Barone Rampante
```

Maven scarica la libreria (la prima volta) e la mette a disposizione del compilatore, senza che noi scriviamo un solo comando `javac` con il classpath.

**Dipendenze transitive**

Una libreria può dipendere a sua volta da altre. Quando Maven scarica una dipendenza, scarica anche il suo POM, e da lì scopre le sue dipendenze, e così via. Le dipendenze delle dipendenze si chiamano **dipendenze transitive**: se il progetto A dichiara solo le dipendenze B e C, ma B dipende da D e C da E, il progetto A ottiene tutte e quattro. Il comando `mvn dependency:tree` stampa l'albero completo delle dipendenze del progetto. Per il nostro esempio:

```text
org.esempio:negozio:jar:1.0-SNAPSHOT
\- org.apache.commons:commons-text:jar:1.12.0:compile
   \- org.apache.commons:commons-lang3:jar:3.14.0:compile
```

Noi abbiamo dichiarato soltanto `commons-text`; `commons-lang3` è arrivata perché `commons-text` ne ha bisogno. Questo è il vantaggio decisivo di Maven rispetto allo scaricare i `.jar` a mano: nessuno deve scoprire quali altre librerie servano. Chi non vuole una dipendenza transitiva può escluderla, con un apposito elemento `<exclusions>`.

**Gli *scope***

Non tutte le librerie servono in tutte le fasi. L'elemento `<scope>`, facoltativo, dice **quando** una dipendenza è visibile:

| `<scope>` | Visibile per compilare? | Visibile per eseguire? | Quando si usa |
|---|---|---|---|
| `compile` (predefinito) | sì | sì | la libreria che il codice usa direttamente |
| `provided` | sì | no (la fornisce l'ambiente) | una libreria che serve per compilare, ma che a runtime è già presente sul server dove gira l'applicazione |
| `runtime` | no | sì | una libreria che il codice non nomina, ma che serve in esecuzione: il driver JDBC |
| `test` | solo per i collaudi | solo per i collaudi | le librerie per scrivere collaudi (come JUnit) |

L'esempio tipico è proprio quello del [Capitolo 21](21-jdbc.md): il programma usa soltanto le interfacce di `java.sql`, quindi il driver di MySQL non serve per compilare ma solo per eseguire, e si dichiara con `<scope>runtime</scope>`.

```xml
    <dependency>
      <groupId>com.mysql</groupId>
      <artifactId>mysql-connector-j</artifactId>
      <version>9.1.0</version>
      <scope>runtime</scope>
    </dependency>
```

Se si usa nel codice una classe di una libreria con scope `test` o `runtime`, il compilatore non la vede: l'errore è `package ... does not exist` (paragrafo «Errori tipici»).

### 22.2.6 I repository

Le librerie vivono in **repository**: cartelle strutturate che contengono gli artefatti, con i loro POM. Ce ne sono di due tipi.

- Il **repository remoto**, un server in rete. Il principale è il *Maven Central Repository*, da cui Maven scarica le librerie pubbliche. Un'azienda può averne di propri.
- Il **repository locale**, una cartella sul nostro computer, di norma `~/.m2/repository` (la cartella `.m2` nella nostra cartella personale). Quando Maven scarica una libreria, ne tiene una copia qui: la volta successiva la trova già e non la scarica di nuovo. Funziona quindi anche da *cache*.

In entrambi i repository, un artefatto sta in un percorso ricavato dalle sue coordinate:

```text
/<groupId>/<artifactId>/<version>/<artifactId>-<version>.<packaging>
```

dove i punti del `groupId` diventano separatori di cartelle. La libreria `org.apache.commons:commons-text:1.12.0` si trova quindi in `org/apache/commons/commons-text/1.12.0/commons-text-1.12.0.jar`.

Il repository locale serve anche per condividere progetti tra loro. Se il progetto B dipende dal progetto A, che abbiamo costruito sul nostro computer, basta **installare** A nel repository locale (comando `mvn install`, paragrafo 22.2.9): quando costruisce B, Maven troverà A lì. Il comando `mvn deploy` fa lo stesso verso un repository **remoto**, per renderlo disponibile agli altri sviluppatori.

### 22.2.7 Plugin e *goal*

Per quanto sappia fare tanto, il «nucleo» di Maven non sa compilare né creare un archivio: sa solo leggere la riga di comando, leggere il POM, gestire il classpath e scaricare i plugin. Tutto il lavoro vero lo fanno i **plugin**.

> [!NOTE]
> **Definizione — Plugin e *goal***
> Un **plugin** è una raccolta di **goal** (in italiano «obiettivi»). Un **goal** è una singola azione che Maven può eseguire sul progetto: la compilazione, l'esecuzione dei test, la creazione di un `.jar`. I plugin si scaricano da un repository quando servono, come le librerie. Un goal si indica con la notazione `plugin:goal`.

I plugin che si incontrano più spesso sono questi.

| Plugin | A cosa serve | Esempi di goal |
|---|---|---|
| `clean` | cancellare ciò che è stato prodotto (la cartella `target`) | `clean:clean` |
| `compiler` | compilare i file sorgente | `compiler:compile`, `compiler:testCompile` |
| `surefire` | eseguire i collaudi | `surefire:test` |
| `jar` | creare l'archivio `.jar` | `jar:jar` |
| `install` | depositare l'archivio nel repository locale | `install:install` |
| `deploy` | depositare l'archivio nel repository remoto | `deploy:deploy` |
| `site` | generare il sito di documentazione del progetto | `site:site` |
| `archetype` | generare la struttura di un progetto da un modello | `archetype:generate` |

Un goal si può lanciare direttamente dalla riga di comando, con la forma

```text
mvn <nome-plugin>:<nome-goal> [-Dparametro=valore ...]
```

dove le opzioni `-D` passano un parametro al goal. Un esempio è `mvn archetype:generate -DgroupId=org.esempio ...`. Nella pratica, però, si lanciano raramente i goal uno per uno: si preferisce chiedere a Maven una **fase** del ciclo di vita, che esegue da sola i goal giusti (paragrafo 22.2.8).

Un plugin si può anche **configurare** nel POM, dentro l'elemento `<build>` e il suo `<plugins>`. L'esempio seguente imposta la versione di Java per il plugin `compiler`, in alternativa alle due proprietà viste prima:

```xml
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <configuration>
          <source>17</source>      <!-- versione di Java del codice sorgente -->
          <target>17</target>      <!-- versione di Java del bytecode prodotto -->
        </configuration>
      </plugin>
    </plugins>
  </build>
```

Anche un plugin è un artefatto, con le sue coordinate (`groupId`, `artifactId`, eventualmente `version`).

### 22.2.8 Il ciclo di vita e le fasi

Il modo normale di usare Maven è chiedere una **fase** di un **ciclo di vita** (*lifecycle*). Maven ha tre cicli di vita predefiniti:

- **default**: costruisce il progetto, dalla validazione fino alla consegna;
- **clean**: ripulisce ciò che è stato costruito;
- **site**: genera la documentazione del progetto.

Il ciclo `default` è una sequenza di **fasi** (*phases*) in un ordine fisso. Le più importanti, in ordine, sono:

| # | Fase | Che cosa avviene |
|---|---|---|
| 1 | `validate` | controlla che il progetto sia corretto e che le informazioni necessarie siano presenti |
| 2 | `compile` | compila il codice sorgente di `src/main/java` in `target/classes` |
| 3 | `test` | esegue i collaudi (che non finiscono nell'archivio) |
| 4 | `package` | impacchetta il codice compilato in un formato distribuibile: un `.jar`, o un `.war` per un'applicazione web, in `target` |
| 5 | `verify` | controlla che l'archivio sia valido e rispetti i criteri di qualità |
| 6 | `install` | installa l'archivio nel **repository locale** |
| 7 | `deploy` | copia l'archivio in un **repository remoto**, per condividerlo |

(Il ciclo completo ha altre fasi intermedie, per esempio per elaborare le risorse o compilare i collaudi.)

> [!IMPORTANT]
> **Nota del docente — La regola fondamentale**
> **Chiedere una fase significa eseguire, nell'ordine, tutte le fasi che la precedono.** `mvn package` compila, esegue i test e solo poi crea l'archivio; `mvn install` fa tutto questo e poi installa. Non si deve chiedere prima `compile` e poi `package`: la seconda comprende la prima.

Come fa una fase a «fare» qualcosa? Ogni fase ha dei goal **agganciati** (*bound*): quando Maven attraversa una fase, esegue i goal che vi sono agganciati. Per un progetto con `<packaging>jar</packaging>` gli agganci sono questi:

| Fase | Goal agganciato |
|---|---|
| `process-resources` | `resources:resources` (copia i file di `src/main/resources`) |
| `compile` | `compiler:compile` |
| `process-test-resources` | `resources:testResources` |
| `test-compile` | `compiler:testCompile` |
| `test` | `surefire:test` |
| `package` | `jar:jar` |
| `install` | `install:install` |
| `deploy` | `deploy:deploy` |

Si vede bene lanciando `mvn compile` sul nostro progetto: tra le righe stampate compaiono, nell'ordine, i goal agganciati alle fasi attraversate.

```text
[INFO] --- resources:3.3.1:resources (default-resources) @ negozio ---
[INFO] --- compiler:3.13.0:compile (default-compile) @ negozio ---
[INFO] BUILD SUCCESS
```

Ogni riga che comincia con `---` annuncia un goal con la forma `plugin:versione:goal`. `mvn package` ne mostra di più: dopo `compile` ci sono `resources:testResources`, `compiler:testCompile` e `surefire:test`, e per ultimo `jar:jar`, che costruisce l'archivio.

Chiedere una fase invece dei goal singoli è molto più comodo: lo stesso risultato si otterrebbe scrivendo a mano `mvn resources:resources compiler:compile resources:testResources compiler:testCompile surefire:test jar:jar`. Il ciclo di vita, uguale per tutti i progetti, è ciò che permette di passare da un progetto Maven a un altro senza conoscerne i dettagli: se sappiamo costruirne uno, li sappiamo costruire tutti.

### 22.2.9 I comandi di tutti i giorni

I comandi si scrivono in un terminale, **dalla cartella base del progetto** (quella con il `pom.xml`).

| Comando | Effetto |
|---|---|
| `mvn clean` | cancella la cartella `target`, per ripartire da zero senza vecchi file compilati |
| `mvn compile` | compila i sorgenti, e nient'altro |
| `mvn test` | compila ed esegue i collaudi |
| `mvn package` | compila, collauda e crea l'archivio in `target` |
| `mvn install` | come `package`, poi installa l'archivio nel repository locale |
| `mvn deploy` | come `install`, poi lo carica nel repository remoto |
| `mvn clean install` | prima il ciclo `clean`, poi `install`: costruisce tutto da capo (il comando più usato) |
| `mvn dependency:tree` | stampa l'albero delle dipendenze, anche transitive |
| `mvn archetype:generate` | crea un nuovo progetto da un modello (paragrafo 22.2.10) |
| `mvn exec:java -Dexec.mainClass=...` | esegue la classe indicata (paragrafo 22.2.11) |

`mvn clean install` mostra che si possono chiedere **più cose di seguito**: `clean` appartiene al ciclo `clean`, `install` al ciclo `default`. Maven le esegue in ordine, da sinistra a destra.

Il risultato di `mvn package` sul nostro progetto è un archivio `target/negozio-1.0-SNAPSHOT.jar`. Se il programma non ha dipendenze, si esegue con il comando `java` indicando l'archivio nel classpath e il nome completo della classe con il `main`:

```text
java -cp target/negozio-1.0-SNAPSHOT.jar org.esempio.negozio.App
```

### 22.2.10 Creare un progetto con un archetipo

Il progetto di partenza non si crea a mano: Maven offre gli **archetipi** (*archetype*), modelli di progetto già pronti. Il goal `archetype:generate` ne usa uno e crea l'intera struttura di cartelle con un `pom.xml` e una classe di prova.

```text
mvn archetype:generate -DgroupId=org.esempio -DartifactId=simple -DarchetypeArtifactId=maven-archetype-quickstart
```

Le opzioni `-DgroupId` e `-DartifactId` danno le coordinate al nuovo progetto; `maven-archetype-quickstart` è l'archetipo più semplice, quello che produce un programma che stampa un saluto. Se non si indica l'archetipo, `archetype:generate` mostra un elenco e chiede di sceglierne uno. Il risultato è una cartella `simple` con questa struttura:

```text
simple/pom.xml
simple/src/main/java/org/esempio/App.java
simple/src/test/java/org/esempio/AppTest.java
```

Il `pom.xml` generato contiene le coordinate scelte e una dipendenza dalla libreria JUnit, con `<scope>test</scope>`, per il collaudo d'esempio `AppTest`. Gli ambienti di sviluppo offrono la stessa operazione con un menù: invece di scrivere il comando, si sceglie «nuovo progetto Maven» e si indica l'archetipo.

### 22.2.11 Eseguire il programma, e il «fat JAR»

Un progetto con dipendenze non si esegue con il solo archivio: l'archivio prodotto da `jar:jar` contiene **soltanto le classi del progetto**, non le librerie da cui dipende. Se proviamo a lanciare il programma di prima, che usa `commons-text`, con il solo `.jar`:

```text
java -cp target/negozio-1.0-SNAPSHOT.jar org.esempio.negozio.App
Exception in thread "main" java.lang.NoClassDefFoundError: org/apache/commons/text/WordUtils
```

la JVM non trova `WordUtils`, perché la libreria non è nel classpath. Ci sono due strade.

**Primo modo: lasciare a Maven l'esecuzione.** Il plugin `exec` ha un goal `java` che esegue una classe con tutto il classpath del progetto, dipendenze comprese:

```text
mvn exec:java -Dexec.mainClass=org.esempio.negozio.App
Il Barone Rampante
```

L'opzione `-Dexec.mainClass` indica la classe con il `main`; con `-Dexec.args` si passano gli argomenti. (Maven stampa anche le sue righe `[INFO]`, che qui omettiamo.)

**Secondo modo: costruire un archivio autosufficiente.** Si chiama **fat JAR** (anche *uber JAR*): un unico `.jar` che contiene le classi del progetto *e* quelle di tutte le dipendenze, così lo si consegna a chi non ha Maven e si lancia con `java -jar`. Lo si ottiene con il plugin `assembly`, configurato nel POM con il formato predefinito `jar-with-dependencies` e con la classe principale:

```xml
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.7.1</version>
        <configuration>
          <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
          </descriptorRefs>
          <archive>
            <manifest>
              <mainClass>org.esempio.negozio.App</mainClass>   <!-- classe da avviare -->
            </manifest>
          </archive>
        </configuration>
        <executions>
          <execution>
            <phase>package</phase>      <!-- si esegue durante la fase package -->
            <goals>
              <goal>single</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
```

L'elemento `<executions>` aggancia il goal `single` del plugin alla fase `package` (come nella tabella del paragrafo 22.2.8). Dopo `mvn package`, nella cartella `target` compaiono due archivi, e quello «grasso» si esegue da solo:

```text
target/negozio-1.0-SNAPSHOT.jar                           (solo le classi del progetto)
target/negozio-1.0-SNAPSHOT-jar-with-dependencies.jar     (classi e librerie)
```

```text
java -jar target/negozio-1.0-SNAPSHOT-jar-with-dependencies.jar
Il Barone Rampante
```

### 22.2.12 Cenni: ereditarietà, aggregazione, profili

Un POM può fare di più. Tre idee, qui solo accennate.

- **Ereditarietà dei POM.** Un POM può dichiarare un **POM genitore** (*parent*) con l'elemento `<parent>` e le sue coordinate, ed eredita da esso le dipendenze, le configurazioni dei plugin e altro. Serve a far usare a più progetti le stesse versioni. È ciò che fa un progetto Spring Boot (paragrafo 22.3.3). Tutti i POM, in ultima analisi, ereditano da un **super-POM** interno a Maven, che stabilisce le convenzioni predefinite. Il comando `mvn help:effective-pom` stampa il POM «effettivo», cioè il risultato di tutte le combinazioni.
- **Aggregazione (progetti multi-modulo).** Un progetto grande si divide in sottoprogetti, ciascuno con il suo POM. Un POM «padre» con `<packaging>pom</packaging>` elenca i sottoprogetti in un elemento `<modules>`; lanciando Maven sul padre, si costruiscono tutti i moduli, nell'ordine imposto dalle loro dipendenze reciproche.
- **Profili.** Il POM può avere configurazioni alternative, i *profili*, da attivare solo in certi casi (per esempio uno per lo sviluppo e uno per la consegna).

Per l'esame basta sapere che esistono. Un esempio minimo del POM padre di un progetto multi-modulo è questo:

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.esempio</groupId>
  <artifactId>negozio-padre</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>pom</packaging>

  <modules>
    <module>negozio-core</module>
    <module>negozio-web</module>
  </modules>
</project>
```

---

## 22.3 Spring Boot

### 22.3.1 Che cos'è

Un'applicazione web è un programma **server** ([Capitolo 19](19-networking.md)) a cui un browser (o un altro programma) si collega per fare una **richiesta** e ricevere una **risposta**. Il protocollo con cui si dialoga è l'**HTTP**: il client chiede una risorsa a un indirizzo, indicando un'operazione. L'operazione più comune è `GET` («dammi questa risorsa»); altre sono `POST` (inviare nuovi dati), `PUT` (aggiornare) e `DELETE` (cancellare). La risposta contiene un **codice di stato** numerico: `200` significa «tutto bene», `404` «risorsa non trovata».

Scrivere a mano un server HTTP con i soli socket del Capitolo 19 sarebbe lunghissimo. **Spring** è un grande *framework* (cioè un'infrastruttura di classi già scritte che il programmatore completa con il proprio codice) per le applicazioni Java, e **Spring Boot** è la sua versione pensata per partire in fretta: crea applicazioni indipendenti (*stand-alone*) e pronte per l'uso, con pochissima configurazione. È molto usato per costruire i **microservizi**, cioè servizi piccoli e indipendenti che comunicano in rete.

Le caratteristiche principali, che le slide elencano, sono queste.

- **Configurazione automatica.** Spring Boot guarda quali librerie ci sono nel progetto e configura da solo ciò che serve. Per un'applicazione web, per esempio, avvia un server.
- **Basato su annotazioni.** Un'applicazione funzionante si scrive con pochissime annotazioni, come `@RestController` (paragrafo 22.3.5).
- **Gestione semplificata delle dipendenze.** Spring Boot offre gli **starter**: dipendenze «a pacchetto» (una per l'applicazione web, una per il database...) che portano con sé tutte le librerie necessarie, nelle versioni compatibili tra loro.
- **Contenitore servlet incorporato.** Il server web è *dentro* l'applicazione: la si lancia come un normale programma Java e la si prova subito, senza installare un server a parte.
- **Flessibilità**, supporto ai microservizi ed elaborazione batch.

### 22.3.2 Che cosa serve per cominciare

Una JDK installata (si controlla con `java -version`), la variabile d'ambiente `JAVA_HOME` impostata sulla cartella di installazione, e un ambiente di sviluppo a scelta (IntelliJ IDEA, Eclipse, Visual Studio Code...). Maven si può usare dall'ambiente di sviluppo o dal terminale (paragrafo 22.2).

### 22.3.3 Creare il progetto con Spring Initializr

Il progetto non si scrive da zero: lo si genera dal sito **`https://start.spring.io`**. Nella pagina si compilano le informazioni del progetto (tipo di progetto, linguaggio, versione di Java, le coordinate `groupId` e `artifactId`) e si aggiungono le **dipendenze** premendo «Add dependencies». Per un'applicazione web basta una: **Spring Web**, che porta le funzioni di base per un servizio web. Il pulsante «Generate» scarica un archivio `.zip` con lo scheletro del progetto, già strutturato secondo le convenzioni di Maven (paragrafo 22.2.3).

Un progetto Spring Boot **è** un progetto Maven. Il suo `pom.xml`, nella forma più piccola, è questo (i numeri di versione variano nel tempo: li sceglie il sito al momento della generazione):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.5</version>
  </parent>

  <groupId>com.example</groupId>
  <artifactId>demo</artifactId>
  <version>0.0.1-SNAPSHOT</version>

  <properties>
    <java.version>17</java.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
```

Riconosciamo gli ingredienti del paragrafo 22.2.

- Il `<parent>` è il POM genitore di Spring Boot (paragrafo 22.2.12): da lì il progetto eredita le versioni compatibili di tutte le librerie, per questo le dipendenze sotto non hanno `<version>`.
- La dipendenza `spring-boot-starter-web` è lo starter «Spring Web» scelto sul sito: porta con sé tutto ciò che serve per un servizio web.
- Il plugin `spring-boot-maven-plugin` fa sì che `mvn package` produca un archivio autosufficiente, come il «fat JAR» del paragrafo 22.2.11, eseguibile con `java -jar`.

### 22.3.4 La classe principale: `@SpringBootApplication`

Il sito genera anche la classe di partenza, con il `main`:

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);   // avvia l'applicazione
    }
}
```

L'**annotazione** `@SpringBootApplication` ([Capitolo 9](09-ereditarieta-e-polimorfismo.md), §9.4.2: un'indicazione che si scrive prima di una dichiarazione e che dà un'informazione al compilatore o ad altri strumenti, qui a Spring) contrassegna la classe principale. È un'annotazione «tutto in uno» che ne combina tre:

- `@Configuration`: la classe può fornire le definizioni dei componenti dell'applicazione, i *bean* (paragrafo 22.3.7);
- `@EnableAutoConfiguration`: Spring Boot deve configurare l'applicazione **in base alle librerie presenti**; con `spring-boot-starter-web` configura per esempio un server web;
- `@ComponentScan`: Spring deve **cercare** i componenti dell'applicazione (controller, servizi...) e registrarli. Per impostazione predefinita la ricerca parte dal **package della classe annotata** e comprende i suoi sotto-package.

L'ultimo punto ha una conseguenza pratica: tutte le classi dell'applicazione devono stare nel package della classe principale o in uno dei suoi sotto-package, altrimenti Spring non le trova (paragrafo «Errori tipici»). Il metodo `SpringApplication.run` avvia l'applicazione.

### 22.3.5 Il primo servizio: `@RestController` e `@GetMapping`

L'esempio delle slide è un servizio che risponde «Hello» a chi lo contatta con un browser. Si aggiunge una classe al progetto, nello stesso package:

```java
package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello(@RequestParam(value = "name", defaultValue = "World") String name) {
        return String.format("Hello %s!", name);
    }
}
```

Tre annotazioni fanno tutto il lavoro.

- **`@RestController`** comunica a Spring che la classe descrive un **punto di accesso** (*endpoint*) disponibile via web: i suoi metodi gestiscono le richieste HTTP e **il valore che restituiscono viene scritto direttamente nel corpo della risposta**, di solito in formato JSON o XML. Combina due annotazioni più semplici: `@Controller` (la classe è un controller dello schema Spring MVC, vedi sotto) e `@ResponseBody` (il valore di ritorno è la risposta, e non il nome di una pagina da mostrare). Una classe del genere ha tipicamente metodi che gestiscono le richieste `GET`, `POST`, `PUT` e `DELETE`.
- **`@GetMapping("/hello")`** dice a Spring di usare il metodo `hello()` per rispondere alle richieste `GET` che arrivano all'indirizzo `/hello`. È una versione specializzata di `@RequestMapping`, pensata per le richieste `GET`, cioè quelle che servono a recuperare dati; esistono le versioni `@PostMapping` e simili per le altre operazioni.
- **`@RequestParam`** dice a Spring di aspettarsi un **parametro** di nome `name` e di tipo `String` nella richiesta, e di passarlo al metodo. Se la richiesta non lo contiene, si usa il valore predefinito `"World"`.

> [!TIP]
> **Intuizione — Il metodo è una funzione, l'indirizzo è il suo nome**
> Possiamo pensare a `hello` come a una funzione scritta in Java e agli indirizzi web come al modo di chiamarla dal browser. L'annotazione `@GetMapping("/hello")` collega il nome `/hello` alla funzione; il parametro `name` arriva dalla parte finale dell'indirizzo, dopo il punto interrogativo; il `return` è ciò che il browser mostra.

Lo schema **MVC** (*Model–View–Controller*, [Capitolo 16](16-interfacce-grafiche.md), §16.4.5) è alla base di Spring MVC: il *controller* riceve le richieste e decide chi serve, il *modello* rappresenta i dati, la *vista* li presenta. In un servizio `REST`, la «vista» è semplicemente la risposta restituita nel corpo.

> [!NOTE]
> **Definizione — REST**
> **REST** (*Representational State Transfer*) è uno stile per far comunicare i programmi via HTTP. Ogni cosa su cui si può operare è una **risorsa**, identificata da un indirizzo (per esempio `/libro`); le operazioni sono i verbi HTTP standard (`GET` per leggere, `POST` per creare, `PUT` per aggiornare, `DELETE` per cancellare). Un servizio costruito in questo modo si dice **RESTful**.

### 22.3.6 Eseguire e provare l'applicazione

L'applicazione si lancia come un normale programma: dall'ambiente di sviluppo (eseguendo la classe principale), oppure dopo `mvn package` con il comando

```text
java -jar target/demo-0.0.1-SNAPSHOT.jar
```

All'avvio Spring Boot stampa un logo e alcune righe di informazioni, tra cui l'avvio del server sulla porta **8080**. A quel punto la si prova con un browser, aprendo gli indirizzi:

```text
http://localhost:8080/hello
http://localhost:8080/hello?name=Arturo
```

Le risposte che il browser mostra sono:

```text
Hello World!
Hello Arturo!
```

`localhost` è il nome del computer stesso, `8080` la porta, `/hello` il percorso mappato da `@GetMapping`, e `?name=Arturo` passa il parametro `name`. Senza parametro vale il valore predefinito. Un indirizzo per il quale non c'è nessun metodo, per esempio `/altro`, riceve la risposta con codice `404` (*Not Found*).

**Restituire un oggetto**

Il valore restituito non deve essere per forza una stringa. Se un metodo restituisce un oggetto, Spring lo **converte da solo in JSON** (un formato di testo per i dati, con coppie nome-valore tra parentesi graffe) usando i suoi metodi `get`. Data la classe

```java
package com.example.demo;

public class Libro {

    private final String titolo;
    private final int anno;

    public Libro(String titolo, int anno) {
        this.titolo = titolo;
        this.anno = anno;
    }

    public String getTitolo() { return titolo; }
    public int getAnno() { return anno; }
}
```

un metodo che la restituisce:

```java
package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LibroController {

    @GetMapping("/libro")
    public Libro libro() {
        return new Libro("La coscienza di Zeno", 1923);
    }
}
```

risponde, a `http://localhost:8080/libro`:

```text
{"titolo":"La coscienza di Zeno","anno":1923}
```

È la stessa idea della serializzazione del [Capitolo 15](15-stream-binari-e-serializzazione.md): trasformare un oggetto in una sequenza di dati da inviare su un flusso, qui in un formato di testo leggibile da qualunque linguaggio.

### 22.3.7 Inversione del controllo, iniezione delle dipendenze, bean

Le ultime slide introducono l'idea più importante di Spring. Partiamo da un problema che già conosciamo.

Una classe `GreetingController` ha bisogno, per lavorare, di una classe `GreetingService`. La via più semplice è che il controller **crei da solo** il servizio con `new`. Ma così il controller è legato per sempre a *quel* servizio: per provarlo con un servizio diverso, bisogna modificare il controller. Vediamolo in Java semplice, senza Spring, con un servizio che può avere due versioni:

```java
interface Servizio {
    String saluta();
}

class ServizioItaliano implements Servizio {
    public String saluta() { return "Ciao, mondo!"; }
}

class ServizioInglese implements Servizio {
    public String saluta() { return "Hello, world!"; }
}

// Il controller crea da solo la propria dipendenza: legato a ServizioItaliano.
class ControllerRigido {
    private final Servizio servizio = new ServizioItaliano();

    String risposta() { return servizio.saluta(); }
}

// Il controller riceve la dipendenza dall'esterno, nel costruttore.
class ControllerFlessibile {
    private final Servizio servizio;

    ControllerFlessibile(Servizio servizio) {
        this.servizio = servizio;
    }

    String risposta() { return servizio.saluta(); }
}

public class Principale {
    public static void main(String[] args) {
        System.out.println(new ControllerRigido().risposta());
        System.out.println(new ControllerFlessibile(new ServizioItaliano()).risposta());
        System.out.println(new ControllerFlessibile(new ServizioInglese()).risposta());
    }
}
```

```text
Ciao, mondo!
Ciao, mondo!
Hello, world!
```

Nella seconda versione il controller non dice *quale* servizio usa: lo **riceve**. Chi lo costruisce decide. Questo è il principio di cui parlano le slide.

> [!NOTE]
> **Definizione — Inversione del controllo (IoC) e iniezione delle dipendenze (DI)**
> L'**inversione del controllo** (*Inversion of Control*, **IoC**) è un principio di progettazione che sposta il controllo dell'oggetto (la sua creazione e configurazione) **dall'interno dell'oggetto stesso a un'entità esterna**, il *container*. Il container IoC di Spring crea, configura e gestisce il ciclo di vita degli oggetti che servono all'applicazione. L'**iniezione delle dipendenze** (*Dependency Injection*, **DI**) è il meccanismo con cui ciò avviene: un oggetto non crea direttamente le proprie dipendenze, le **riceve** dall'esterno, di solito come parametri del costruttore, ma anche tramite i campi o i metodi. È ciò che fa il `ControllerFlessibile`, dove il «container» siamo noi nel `main`.

In Spring, l'oggetto gestito dal container si chiama **bean**. Un bean è un componente configurato, creato e iniettato automaticamente da Spring, che ne gestisce il ciclo di vita e le dipendenze. Come si dice a Spring che una classe è un bean? Con un'annotazione sulla classe: **`@Component`**, oppure le sue varianti per ruolo, **`@Service`** (logica dell'applicazione), **`@Repository`** (accesso ai dati) e **`@Controller`** (e quindi `@RestController`). Grazie alla ricerca dei componenti (`@ComponentScan`, paragrafo 22.3.4), Spring li trova da solo e li registra nel suo contesto (`ApplicationContext`): nessuno scrive `new`.

L'esempio delle slide mette insieme tutto. Il servizio:

```java
package com.example.demo;

import org.springframework.stereotype.Service;

@Service
public class GreetingService {

    public String greet() {
        return "Hello, world!";
    }
}
```

e il controller, che riceve il servizio nel costruttore:

```java
package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingController {

    private final GreetingService greetingService;

    public GreetingController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/greet")
    public String greet() {
        return greetingService.greet();
    }
}
```

`@Service` dice a Spring che `GreetingService` è un bean, quindi Spring lo crea e lo gestisce nel suo container. Il controller dichiara nel costruttore di averne bisogno: Spring vede il parametro e **inietta** il bean (**iniezione tramite il costruttore**, l'approccio più raccomandato). Il metodo `greet()` espone l'endpoint `/greet`, che risponde `Hello, world!` quando viene chiamato. Si può anche chiedere l'iniezione con l'annotazione `@Autowired` su un campo o su un metodo, ma la forma con il costruttore è preferibile, perché l'oggetto nasce già completo, come i costruttori del [Capitolo 7](07-classi-e-oggetti.md).

Del ciclo di vita dei bean si occupa il container: crea l'oggetto, lo inizializza e lo distrugge, e permette di agganciare azioni a questi momenti con annotazioni come `@PostConstruct` (dopo la creazione) e `@PreDestroy` (prima della distruzione).

---

## 22.4 I database NoSQL

### 22.4.1 Oltre le tabelle

Il [Capitolo 21](21-jdbc.md) ha mostrato il database **relazionale**: dati in tabelle con colonne fisse e tipi dichiarati in anticipo, interrogate in SQL. È un modello molto solido, ma non è adatto a tutto. Se ogni elemento da conservare ha campi diversi dagli altri, o se i dati sono enormi flussi di misurazioni, la struttura rigida diventa un ostacolo. Per questi casi esistono i database **NoSQL** («non soltanto SQL»), che rinunciano alle tabelle fisse. Ne esistono di molti tipi; le slide del corso ne presentano due.

### 22.4.2 I database a documenti: MongoDB

In un database **a documenti** (*document database*) l'unità di dati non è la riga, ma il **documento**: una struttura simile al JSON (paragrafo 22.3.6), con campi di nome e valore, che possono contenere elenchi e altri documenti annidati. I documenti dello stesso genere si raccolgono in una **collezione** (*collection*). La differenza fondamentale con le tabelle è che **non c'è uno schema obbligatorio**: due documenti della stessa collezione possono avere campi diversi, e si può aggiungere un campo a un documento senza toccare gli altri.

**MongoDB** è il database a documenti più diffuso. Da Java vi si accede con una libreria, il *driver* `mongo-java-driver`, che si aggiunge al progetto come qualsiasi altra dipendenza Maven (paragrafo 22.2.5; la dipendenza è quella già vista nell'esempio delle slide, con `groupId` `org.mongodb`). Come per JDBC, il programma Java usa le classi del driver per collegarsi al server, scegliere il database e la collezione e inserire o leggere documenti. Il percorso del livello 7 prevede proprio questo passaggio: sostituire il database relazionale con uno documentale, aggiungendo la dipendenza al `pom.xml` e scrivendo un documento nel database.

### 22.4.3 I database per serie temporali: InfluxDB

Un **database per serie temporali** (*time series database*) è ottimizzato per dati che arrivano **nel tempo**: misurazioni di sensori, metriche di un'applicazione, contatori di un impianto. **InfluxDB** è un database di questo tipo, scritto nel linguaggio Go, usato per il monitoraggio di sistemi, le metriche applicative, i dati dei sensori dell'*Internet of Things* e l'analisi in tempo reale. I suoi dati hanno un vocabolario preciso, che conviene imparare.

| Termine | Significato |
|---|---|
| **organization** | uno spazio di lavoro per un gruppo di utenti; a un'organization appartengono bucket, utenti, dashboard e attività |
| **bucket** | il contenitore in cui sono salvati tutti i dati; combina il concetto di database e quello di **periodo di conservazione** (per quanto tempo ogni dato resta salvato); appartiene a un'organization |
| **timestamp** | l'istante a cui si riferisce ogni dato; tutti i dati hanno una colonna `_time` con l'istante (internamente in nanosecondi dall'origine dei tempi, mostrato in formato UTC) |
| **measurement** | il nome della «categoria» di dati; è un contenitore per tag, campi e timestamp, e ha un nome che descrive i dati |
| **field** (campo) | un valore misurato: ha una **chiave** (*field key*, il nome) e un **valore** (*field value*: stringa, numero decimale, intero o booleano); i campi sono obbligatori e **non indicizzati** |
| **tag** | un'informazione descrittiva (metadati): ha una chiave e un valore, memorizzati come stringhe; i tag **sono indicizzati** |

Un esempio dalle slide: una misura chiamata `census` registra il numero di api (`bees`) e di formiche (`ants`) contate in luoghi diversi da scienziati diversi. Un possibile contenuto:

| `_time` | `_measurement` | `location` (tag) | `scientist` (tag) | `bees` (campo) | `ants` (campo) |
|---|---|---|---|---|---|
| 08:00 | `census` | klamath | anderson | 23 | 30 |
| 08:00 | `census` | portland | mullen | 28 | 32 |

- `census` è il **measurement**: il nome ci dice che i campi registrano un censimento.
- `location` e `scientist` sono i **tag**: le *chiavi* sono i nomi delle colonne, i *valori* sono `klamath`, `portland`, `anderson`, `mullen`.
- `bees` e `ants` sono le *chiavi dei campi*; i numeri sono i *valori dei campi*. L'insieme delle coppie chiave-valore dei campi associate a un istante (qui `bees=23, ants=30`) si chiama **field set**.

La differenza tra tag e campi ha una conseguenza pratica. I campi non sono indicizzati: una ricerca che filtra per un valore di campo deve **scorrere tutti i valori** per trovare quelli giusti. I tag sono indicizzati, e le ricerche sui tag sono molto più veloci. Perciò i metadati che si usano di frequente per cercare (qui il luogo e lo scienziato) vanno nei tag, e i valori misurati nei campi.

---

## Errori tipici

> [!CAUTION]
> **Errore tipico — Lanciare `mvn` fuori dalla cartella del progetto**
> ```text
> [ERROR] The goal you specified requires a project to execute but there is no POM in this directory ... Please verify you invoked Maven from the correct directory.
> ```
> Maven cerca il file `pom.xml` **nella cartella corrente**. Se il terminale è in un'altra cartella (per esempio sopra quella del progetto, o dentro `src`), non trova nulla. Soluzione: spostarsi nella cartella base, quella che contiene il `pom.xml`, e rilanciare.

> [!CAUTION]
> **Errore tipico — Il `pom.xml` non è un XML ben formato**
> ```xml
> <artifactId>negozio</artifactId
> ```
> Il POM è un documento XML ([Capitolo 20](20-xml.md)): un elemento non chiuso, o chiuso male come qui (manca il `>`), lo rende illeggibile. Maven non parte e risponde `Some problems were encountered while processing the POMs` / `The build could not read 1 project`. Il compilatore Java non c'entra: l'errore è prima, nel file di descrizione. Forma corretta: `<artifactId>negozio</artifactId>`.

> [!CAUTION]
> **Errore tipico — Sorgenti nella cartella sbagliata**
> ```text
> negozio/altro/org/esempio/negozio/App.java       (sbagliato)
> negozio/src/main/java/org/esempio/negozio/App.java   (giusto)
> ```
> Maven compila **soltanto** ciò che trova in `src/main/java`. Con i sorgenti altrove, `mvn package` non segnala alcun errore: dice `No sources to compile`, finisce con `BUILD SUCCESS` e produce un archivio **senza classi**. Il programma fallirà solo al momento di eseguirlo (`ClassNotFoundException`). Se `BUILD SUCCESS` arriva troppo in fretta, conviene controllare la posizione dei file.

> [!CAUTION]
> **Errore tipico — Usare nel codice una libreria con lo scope sbagliato**
> ```xml
> <dependency>
>   <groupId>org.apache.commons</groupId>
>   <artifactId>commons-text</artifactId>
>   <version>1.12.0</version>
>   <scope>test</scope>          <!-- visibile solo ai collaudi -->
> </dependency>
> ```
> ```text
> [ERROR] App.java:[3,31] package org.apache.commons.text does not exist
> ```
> Con `test` (e con `runtime`) la libreria **non è visibile al compilatore** per il codice di `src/main/java`: l'`import` fallisce con `package ... does not exist`. Se il codice nomina le classi della libreria, lo scope deve essere `compile` (il predefinito, che si ottiene omettendo l'elemento). Lo scope `runtime` è giusto soltanto per ciò che il codice non nomina, come un driver JDBC.

> [!CAUTION]
> **Errore tipico — Eseguire l'archivio senza le dipendenze**
> ```text
> java -cp target/negozio-1.0-SNAPSHOT.jar org.esempio.negozio.App
> Exception in thread "main" java.lang.NoClassDefFoundError: org/apache/commons/text/WordUtils
> ```
> Il programma compila perché Maven aveva le librerie nel classpath, ma l'archivio prodotto da `package` contiene solo le classi del progetto. Soluzioni: `mvn exec:java -Dexec.mainClass=...`, oppure un archivio autosufficiente con il plugin `assembly` (paragrafo 22.2.11).

> [!CAUTION]
> **Errore tipico — Confondere `package`, `install` e `deploy`**
> `package` crea l'archivio in `target` e basta. `install` fa lo stesso e poi lo copia nel **repository locale**, dove altri progetti sul nostro computer possono usarlo come dipendenza. `deploy` lo carica in un **repository remoto**, e richiede un server configurato. Chi vuole soltanto l'archivio usa `package`; chi vuole condividerlo con un altro progetto locale usa `install`. Per ricostruire tutto da zero, senza residui di compilazioni precedenti, si fa precedere `clean`: `mvn clean install`.

> [!CAUTION]
> **Errore tipico — Un controller senza `@RestController`**
> ```java
> public class HelloController {            // manca @RestController
>     @GetMapping("/hello")
>     public String hello(...) { ... }
> }
> ```
> La classe compila, l'applicazione parte, ma `http://localhost:8080/hello` risponde con un errore `404` (*Not Found*): Spring non sa che la classe è un controller, e ignora l'annotazione `@GetMapping`. Forma corretta: aggiungere `@RestController` sulla classe.

> [!CAUTION]
> **Errore tipico — Una classe fuori dal package della classe principale**
> ```java
> package org.altro;                        // fuori da com.example.demo
> @RestController
> public class HelloController { ... }
> ```
> Il `@ComponentScan` parte dal package della classe annotata con `@SpringBootApplication` (qui `com.example.demo`) e scende nei suoi sotto-package. Un controller in un package non nipote è **invisibile**: nessun errore, ma l'indirizzo risponde `404`. Forma corretta: tenere le classi nel package della classe principale o in un suo sotto-package.

> [!CAUTION]
> **Errore tipico — Dimenticare `@Service` (o `@Component`) su una dipendenza iniettata**
> ```java
> public class GreetingService { ... }      // manca @Service
> ```
> Il controller chiede il servizio nel costruttore, ma Spring non sa che la classe è un bean, quindi non ne ha uno da iniettare. L'applicazione non parte:
> ```text
> APPLICATION FAILED TO START
> Parameter 0 of constructor in com.example.demo.GreetingController required a bean of type 'com.example.demo.GreetingService' that could not be found.
> ```
> Forma corretta: annotare la classe con `@Service`.

> [!CAUTION]
> **Errore tipico — Parametro obbligatorio dimenticato**
> ```java
> @GetMapping("/strict")
> public String strict(@RequestParam("name") String name) { ... }    // nessun defaultValue
> ```
> Senza `defaultValue`, il parametro è **obbligatorio**: la richiesta `http://localhost:8080/strict` (senza `?name=...`) risponde `400` (*Bad Request*). Con `defaultValue`, come in `hello`, il parametro può mancare.

---

## Riassunto

Un programma reale non è un file solo: ha molte classi, usa librerie di altri, va costruito e consegnato sempre allo stesso modo. **Maven** risolve questo problema in modo **dichiarativo** e per **convenzione**: nel file `pom.xml` si descrive il progetto (le coordinate `groupId`, `artifactId`, `version`, il tipo di archivio, le dipendenze) e Maven, che di suo non sa fare nulla, delega ai **plugin** (raccolte di *goal*) il lavoro vero, nell'ordine fissato dal **ciclo di vita**: `validate`, `compile`, `test`, `package`, `verify`, `install`, `deploy`. Chiedere una fase esegue tutte le precedenti. Le librerie si dichiarano come dipendenze, vengono scaricate dai **repository** (remoto, e locale in `~/.m2/repository`) con le loro dipendenze transitive, e hanno uno **scope** che dice quando sono visibili. Sopra Maven si appoggia **Spring Boot**, un framework che permette di scrivere applicazioni web con poche annotazioni: `@SpringBootApplication` avvia e configura, `@RestController` e `@GetMapping` espongono i metodi come indirizzi HTTP, e l'**inversione del controllo** (con l'**iniezione delle dipendenze**) sposta in un container la creazione degli oggetti, i **bean**. Quando i dati non stanno bene in tabelle fisse, esistono i **database NoSQL**: a **documenti** (MongoDB, senza schema obbligatorio, con un driver Java aggiunto come dipendenza) o per **serie temporali** (InfluxDB, con tag indicizzati e campi non indicizzati).

**Concetti chiave**

- **Maven**: strumento di costruzione dei progetti Java, dichiarativo, basato sulla convenzione piuttosto che sulla configurazione; automatizza compilazione, collaudo, impacchettamento e gestione delle librerie.
- **`pom.xml`** (*Project Object Model*): il file XML, nella cartella base, che descrive il progetto. Contiene le coordinate, il `packaging`, le proprietà, le dipendenze, la configurazione dei plugin.
- **Coordinate GAV**: `groupId` (organizzazione, dominio rovesciato), `artifactId` (nome), `version` (`-SNAPSHOT` se in sviluppo). Identificano in modo univoco un progetto, una libreria, un plugin.
- **Struttura standard**: `src/main/java`, `src/main/resources`, `src/test/java`, `src/test/resources`, `target`.
- **Dipendenze**: dichiarate con le coordinate; scaricate da Maven con quelle **transitive**; il **scope** (`compile`, `provided`, `runtime`, `test`) regola dove sono visibili.
- **Repository**: remoto (Maven Central) e locale (`~/.m2/repository`); percorso derivato dalle coordinate; `install` deposita nel locale, `deploy` nel remoto.
- **Plugin e goal**: un goal è una singola azione, un plugin ne raccoglie più d'uno; notazione `plugin:goal`. Il nucleo di Maven non compila da solo.
- **Ciclo di vita**: tre cicli (`default`, `clean`, `site`); le fasi del `default` sono in ordine fisso e chiedere una fase esegue anche le precedenti; ogni fase ha dei goal agganciati.
- **Archetipo**: modello di progetto; `mvn archetype:generate` ne crea uno da zero.
- **Fat JAR**: archivio con classi del progetto e di tutte le dipendenze, ottenuto con il plugin `assembly` (`jar-with-dependencies`); il `.jar` normale contiene solo le classi del progetto.
- **Spring Boot**: framework per applicazioni stand-alone con configurazione automatica, basato su annotazioni, con *starter* per le dipendenze e server incorporato; si genera da `start.spring.io`.
- **`@SpringBootApplication`**: annotazione della classe principale che combina `@Configuration`, `@EnableAutoConfiguration` e `@ComponentScan` (ricerca dei componenti a partire dal package della classe).
- **`@RestController`**: marca una classe che gestisce richieste HTTP e restituisce i valori nel corpo della risposta (`@Controller` + `@ResponseBody`); `@GetMapping("/percorso")` associa un metodo a un indirizzo e a `GET`; `@RequestParam` legge un parametro della richiesta (con `defaultValue`, se facoltativo).
- **IoC, DI, bean**: l'inversione del controllo sposta in un container la creazione degli oggetti; l'iniezione delle dipendenze li passa a chi ne ha bisogno (di preferenza nel costruttore); un bean è un oggetto gestito dal container, dichiarato con `@Component`, `@Service`, `@Repository` o `@Controller`.
- **NoSQL**: database senza tabelle fisse. **A documenti** (MongoDB): documenti simili a JSON in collezioni, senza schema obbligatorio. **Per serie temporali** (InfluxDB): organization, bucket, timestamp, measurement, field (non indicizzati) e tag (indicizzati).

**Elementi essenziali**

| Elemento | A cosa serve |
|---|---|
| `mvn clean` / `compile` / `test` / `package` / `install` / `deploy` | pulire, compilare, collaudare, impacchettare, installare nel repository locale, depositare nel remoto |
| `mvn clean install` | ricostruire tutto da capo e installarlo |
| `mvn archetype:generate -DgroupId=... -DartifactId=...` | creare un progetto da un archetipo |
| `mvn dependency:tree` | stampare le dipendenze, anche transitive |
| `mvn exec:java -Dexec.mainClass=...` | eseguire una classe con il classpath del progetto |
| `<dependency>` con `groupId`, `artifactId`, `version`, `scope` | dichiarare una libreria nel POM |
| `@SpringBootApplication` | classe principale: configurazione automatica e ricerca dei componenti |
| `@RestController` | classe che risponde a richieste HTTP restituendo i dati nel corpo |
| `@GetMapping("/percorso")` | metodo associato a un indirizzo e all'operazione `GET` |
| `@RequestParam(value = "nome", defaultValue = "...")` | parametro della richiesta, facoltativo se ha il valore predefinito |
| `@Service`, `@Component`, `@Repository` | classi gestite dal container come bean |
