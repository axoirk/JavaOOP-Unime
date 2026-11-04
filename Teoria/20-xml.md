---
materia: Programmazione a Oggetti
capitolo: 20
titolo: XML in Java
livello_syllabus: 6
stato: completo
slide: ["2.04.XML-Java.pdf pagine 1-42"]
appelli: []
fonti_esterne: 9
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 20 — XML in Java

## Di cosa parla questo capitolo

Un programma che salva i propri dati su un file ha un problema: deve decidere **come** scriverli, e chiunque voglia rileggerli deve conoscere quella scelta. Nel [Capitolo 14](14-file-di-testo.md) abbiamo scritto righe di testo con campi separati da virgole; nel [Capitolo 15](15-stream-binari-e-serializzazione.md) abbiamo scritto oggetti in un formato binario che solo Java sa leggere. **XML** (*eXtensible Markup Language*) è una risposta diversa: un formato di testo **standard**, leggibile da una persona e da programmi scritti in qualunque linguaggio, in cui i dati portano con sé la propria struttura, perché ogni valore è racchiuso in un'etichetta che ne dice il significato.

Leggere un file XML a mano, riga per riga, sarebbe un incubo: bisognerebbe riconoscere le etichette, abbinare apertura e chiusura, gestire i caratteri speciali. Per questo esistono i **parser** (*analizzatori sintattici*), programmi che fanno questo lavoro e restituiscono all'applicazione il contenuto già scomposto. Java ne include due famiglie, che si differenziano per il **modo** in cui consegnano i dati: **DOM**, che costruisce in memoria un albero di oggetti, e **SAX**, che avvisa il programma man mano che incontra le parti del documento.

In questo capitolo vedremo:

- che cosa è un **documento XML**, quando è **ben formato** e che cosa fa un parser (paragrafo 20.1);
- i **due modelli** di lettura, a eventi e a oggetti, e come scegliere (paragrafo 20.2);
- **JAXP** e le **factory** con cui si ottiene un parser (paragrafo 20.3);
- **DOM**: l'albero dei nodi, come caricare un documento, come leggerlo, come costruirne o modificarne uno, come salvarlo (paragrafo 20.4);
- **SAX**: il modello a **callback**, la classe `DefaultHandler`, i metodi `startElement`, `characters`, `endElement` (paragrafo 20.5);
- un confronto per **scegliere** tra i due (paragrafo 20.6) e un cenno alle altre librerie (paragrafo 20.7);
- come **tradurre le parole di una traccia** in codice (paragrafo 20.8);
- gli **scheletri** da saper scrivere a memoria e gli **errori tipici**.

Il capitolo si appoggia sui precedenti. I parser sono oggetti e interfacce ([Capitolo 10](10-classi-astratte-e-interfacce.md)); i `DefaultHandler` si scrivono **estendendo una classe** e **riscrivendo** i suoi metodi ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)); le eccezioni che i parser dichiarano sono **controllate** ([Capitolo 13](13-eccezioni.md)); un documento si legge da un `File` ([Capitolo 14](14-file-di-testo.md)); i dati letti si raccolgono tipicamente in una `List` ([Capitolo 12](12-generics-e-collezioni.md)) e i numeri si convertono con `Integer.parseInt` o `Double.parseDouble` ([Capitolo 6](06-metodi.md)).

> [!IMPORTANT]
> **Nota per l'esame — XML**
> L'XML fa parte dell'area «Core Java API» del secondo esercizio della prova scritta (13 punti), insieme a file, serializzazione, socket, JDBC e collezioni. Il caso tipico è il **caricamento di un documento con DOM** e la lettura dei suoi elementi: si ottiene un `Document`, si cerca una lista di nodi per nome del tag, si scorre la lista, si leggono attributi e testo, si costruiscono oggetti. Le difficoltà sono due, e sono entrambe di **precisione**: i nomi dei metodi (`getElementsByTagName`, `getTextContent`, `getLength`) vanno scritti al carattere, perché non si possono dedurre per analogia, e le **eccezioni controllate** dei parser vanno dichiarate o catturate, altrimenti il programma non compila e l'esecuzione è persa. Il capitolo insiste su queste due cose.

---

## 20.1 Che cos'è un documento XML

### 20.1.1 Un esempio: un catalogo di prodotti

Cominciamo da un documento concreto, che useremo in tutto il capitolo. Descrive un catalogo di tre prodotti, ciascuno con un codice, un nome e un prezzo.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalogo>
  <prodotto codice="A10">
    <nome>Lampada</nome>
    <prezzo>24.50</prezzo>
  </prodotto>
  <prodotto codice="B20">
    <nome>Tavolo</nome>
    <prezzo>120.00</prezzo>
  </prodotto>
  <prodotto codice="C30">
    <nome>Sedia</nome>
    <prezzo>35.90</prezzo>
  </prodotto>
</catalogo>
```

La prima riga, la **dichiarazione XML**, dice che il file è XML, di quale versione e con quale codifica di caratteri. Poi viene il contenuto vero e proprio, fatto di pochi ingredienti:

- un **elemento** è una coppia di etichette, una di apertura (`<nome>`) e una di chiusura (`</nome>`), con ciò che sta in mezzo. Le etichette si chiamano anche **tag**; il nome dentro il tag (`nome`) è il **nome del tag**. Un elemento può contenere testo (`<nome>Lampada</nome>`), altri elementi (`<prodotto>...</prodotto>` contiene un `nome` e un `prezzo`) o entrambi;
- un **attributo** è una coppia nome-valore scritta *dentro* il tag di apertura: `codice="A10"` è un attributo dell'elemento `prodotto`, con valore `A10` (sempre tra virgolette);
- un elemento che non contiene nulla si può scrivere con **un solo tag**, che si apre e si chiude insieme: `<riga articolo="matita"/>`;
- il **testo** è il contenuto «scritto in chiaro» di un elemento, come `Lampada` o `24.50`;
- l'elemento più esterno, qui `catalogo`, che contiene tutti gli altri, è la **radice** (*root*): in un documento ce n'è una sola.

Gli elementi contenuti in un altro si chiamano suoi **figli**, e l'elemento che li contiene è il loro **padre**. Così `prodotto` è figlio di `catalogo`, e `nome` e `prezzo` sono figli di `prodotto` e fratelli tra loro. L'insieme di queste relazioni forma un **albero**:

```text
catalogo
├── prodotto  (codice="A10")
│   ├── nome     "Lampada"
│   └── prezzo   "24.50"
├── prodotto  (codice="B20")
│   ├── nome     "Tavolo"
│   └── prezzo   "120.00"
└── prodotto  (codice="C30")
    ├── nome     "Sedia"
    └── prezzo   "35.90"
```

Le etichette dicono **che cosa** è ogni dato: chi legge il documento capisce che `24.50` è un prezzo senza bisogno di una legenda. È la differenza con il file di testo con campi separati da virgole del [Capitolo 14](14-file-di-testo.md), dove il significato di ogni colonna sta solo nella testa di chi ha scritto il programma.

### 20.1.2 Quando un documento è «ben formato»

Il formato è rigoroso, e un documento che lo viola non è XML. Le regole fondamentali sono poche.

- Esiste **una sola radice**, che contiene tutto il resto.
- Ogni tag di apertura ha il suo tag di chiusura, e gli elementi sono **annidati correttamente**: si chiude per primo l'ultimo elemento aperto. `<a><b></b></a>` va bene, `<a><b></a></b>` no.
- I valori degli attributi stanno **tra virgolette**.
- Alcuni caratteri hanno un significato speciale e nel testo non si possono scrivere direttamente: in particolare `&` e `<`. Si scrivono come `&amp;` e `&lt;`.

Un documento che rispetta queste regole è detto **ben formato** (*well-formed*). Il parser lo controlla e, se trova una violazione, **si rifiuta di proseguire** lanciando un'eccezione. Con il nostro parser, per esempio, il testo `<a><b></a>` produce

```text
org.xml.sax.SAXParseException: The element type "b" must be terminated by the matching end-tag "</b>".
```

e il testo `<a>5 & 6</a>` produce

```text
org.xml.sax.SAXParseException: The entity name must immediately follow the '&' in the entity reference.
```

Esiste un livello di controllo ulteriore, la **validità**: un documento è **valido** se, oltre a essere ben formato, rispetta le regole di struttura dichiarate in un documento di descrizione (un DTD o un XML Schema), che stabilisce per esempio che un `prodotto` deve avere un `nome` e un `prezzo`. I parser che eseguono questo controllo si chiamano **validanti**. In questo capitolo ci occupiamo del solo controllo di buona formazione.

### 20.1.3 Che cosa fa un parser

Un **parser** XML ha due compiti: **scomporre** il documento nelle sue parti (elementi, attributi, testo) e **controllare** che sia ben formato (ed eventualmente valido). La validazione è un'operazione computazionalmente costosa, e per questo i parser permettono di scegliere se attivarla o no (paragrafo 20.3).

Per un'applicazione che vuole leggere XML, il parser è oggi uno strumento standard: il JDK ne contiene uno nelle sue librerie di base, a partire dalla specifica **JAXP** (*Java API for XML Processing*, paragrafo 20.3). Non c'è nulla da installare: basta usare le classi giuste.

---

## 20.2 Due modi di leggere: eventi e oggetti

Dal punto di vista di chi scrive il programma, un parser può consegnare i dati in due modi molto diversi. Conviene capirli bene prima di vedere il codice, perché da questa scelta dipende tutto il resto.

### 20.2.1 Il modello a oggetti: DOM

Nel primo modo il parser legge **l'intero documento** e lo ricostruisce in memoria come un **albero di oggetti**: un oggetto per ogni elemento, uno per ogni attributo, uno per ogni pezzo di testo, collegati tra loro come nel disegno del paragrafo 20.1.1. Al programma viene consegnato un solo oggetto, che rappresenta il documento intero, e da lì il programma **naviga** l'albero a piacere: scende ai figli, risale al padre, passa ai fratelli, cerca elementi per nome, torna indietro, aggiunge o toglie nodi. Questo modello si chiama **DOM** (*Document Object Model*) ed è uno standard del W3C, usato in molti linguaggi con le stesse interfacce.

```text
   file XML                 parser               memoria del programma
 +----------------+                              +--------------------+
 | <a i="1">      |    ---> legge tutto --->     |  albero di oggetti |
 |   Ciao         |                              |  (Document, Element|
 | </a>           |                              |   Attr, Text ...)  |
 +----------------+                              +--------------------+
                                                           |
                               il programma naviga e modifica l'albero
```

Il vantaggio è la **comodità**: tutto il documento è lì, a portata di mano, e si può muovere in qualunque direzione. Il prezzo è la **memoria**: l'albero dell'intero documento sta in RAM, e per file molto grandi può non starci.

### 20.2.2 Il modello a eventi: SAX

Nel secondo modo il parser **non costruisce nulla**: percorre il documento dall'inizio alla fine, una volta sola, e ogni volta che incontra qualcosa di significativo **avvisa** il programma chiamando uno dei suoi metodi. È il modello dei **callback**: il programma scrive in anticipo alcuni metodi («quando incontri l'apertura di un elemento, esegui questo»), il parser li chiama al momento giusto, passando come argomenti le informazioni sull'evento (il nome dell'elemento, i suoi attributi, il testo trovato). Questo modello si chiama **SAX** (*Simple API for XML*).

```text
   <?xml ...?>
   <a i="1"> Ciao </a>
        |
        v   il parser percorre il file e "chiama" i metodi del programma:
   startDocument()
   startElement("a", attributi: i="1")
   characters(" Ciao ")
   endElement("a")
   endDocument()
```

Il vantaggio è l'**economia**: non si tiene in memoria nulla di più di quanto il programma decide di ricordare, per cui si possono leggere documenti enormi. Il prezzo è la **scomodità**: il programma vede ogni cosa **una volta sola, in ordine**, e non può tornare indietro. Se una risposta dipende da due punti lontani del documento, deve ricordarsi da solo ciò che ha visto. Le analogie con la vita quotidiana aiutano: DOM somiglia a stampare un libro e tenerlo sulla scrivania, per sfogliarlo come si vuole; SAX somiglia a farselo leggere ad alta voce da qualcuno, senza possibilità di chiedere di rileggere. L'analogia ha un limite: nel SAX il lettore non si ferma mai ad aspettarci, siamo noi a dover tenere il passo.

### 20.2.3 Il confronto in breve

| | **DOM** (oggetti) | **SAX** (eventi) |
|---|---|---|
| Che cosa consegna | un albero completo in memoria | una sequenza di notifiche, una alla volta |
| Memoria | tutto il documento | quasi niente |
| Navigazione | libera, in ogni direzione | solo in avanti, una volta |
| Modifica del documento | sì (aggiunge, toglie, cambia nodi) | no, sola lettura |
| Semplicità di scrittura | alta: si naviga a oggetti | più bassa: serve ricordare lo «stato» |
| Adatto a | documenti piccoli o medi, ricerche, modifiche | documenti grandi, letture sequenziali |

I parser più diffusi supportano entrambi i modelli, e spesso un parser DOM è costruito sopra un parser SAX: il DOM non è altro che un programma SAX che, a ogni evento, aggiunge un nodo all'albero.

---

## 20.3 JAXP e le factory

### 20.3.1 I package

Le classi per elaborare XML sono tutte nel JDK, raccolte sotto il nome **JAXP**. Per usarle serve sapere in quali package stanno, perché gli `import` fanno parte del codice che si scrive all'esame.

| Package | Contenuto |
|---|---|
| `javax.xml.parsers` | le classi per **creare** i parser: `DocumentBuilderFactory`, `DocumentBuilder`, `SAXParserFactory`, `SAXParser` e l'eccezione `ParserConfigurationException` |
| `org.w3c.dom` | le interfacce del **DOM**: `Document`, `Element`, `Node`, `NodeList`, `Attr`, `Text` |
| `org.xml.sax` | le interfacce del **SAX**: `Attributes`, `XMLReader`, `ContentHandler`, `SAXException` |
| `org.xml.sax.helpers` | `DefaultHandler`, la classe da estendere per scrivere un gestore SAX |
| `javax.xml.transform` (e sottopackage) | la trasformazione e il salvataggio di un documento (paragrafo 20.4.8) |

JAXP permette di lavorare **indipendentemente dall'effettivo parser** presente nel sistema: il programma usa le sole interfacce standard, e la libreria sceglie l'implementazione. Per ottenere questa indipendenza si usa il **pattern factory**.

### 20.3.2 Il pattern factory

Per ottenere un parser non si scrive `new`. Si chiede a una **fabbrica** (*factory*) di costruirlo. Per ciascuno dei due modelli ci sono due classi: una fabbrica e il parser che essa produce.

| Modello | Fabbrica | Parser prodotto |
|---|---|---|
| DOM | `DocumentBuilderFactory` | `DocumentBuilder` |
| SAX | `SAXParserFactory` | `SAXParser` |

Le fabbriche sono classi **astratte** (non si istanziano con `new`, [Capitolo 10](10-classi-astratte-e-interfacce.md)) e hanno un metodo **statico** `newInstance()` che restituisce un oggetto di una classe concreta scelta dalla libreria. A quel punto la fabbrica produce il parser:

```java
DocumentBuilderFactory fabbrica = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = fabbrica.newDocumentBuilder();       // parser DOM

SAXParserFactory spf = SAXParserFactory.newInstance();
SAXParser saxParser = spf.newSAXParser();                       // parser SAX
```

Il nome del metodo si scrive `newInstance` (con la **n**, non `newIstance` come in italiano), e si chiama sulla **classe**, perché è statico.

> [!NOTE]
> **Approfondimento esterno — `DocumentBuilderFactory` e `DocumentBuilder`**
> La documentazione ufficiale descrive `public static DocumentBuilderFactory newInstance()` come «*Obtains a new instance of a DocumentBuilderFactory*». Il metodo `public abstract DocumentBuilder newDocumentBuilder() throws ParserConfigurationException` «*Creates a new instance of a DocumentBuilder using the currently configured parameters*» e lancia `ParserConfigurationException` «*if a DocumentBuilder cannot be created which satisfies the configuration requested*». Per leggere un documento, `DocumentBuilder` offre diverse forme di `parse`, tutte con `throws SAXException, IOException` e tutte con `IllegalArgumentException` se l'argomento è `null`: `parse(File f)`, `parse(InputStream is)`, `parse(InputSource is)` e `parse(String uri)`.
>
> *Fonte:* [DocumentBuilderFactory (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/javax/xml/parsers/DocumentBuilderFactory.html) e [DocumentBuilder (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/javax/xml/parsers/DocumentBuilder.html)

### 20.3.3 Le eccezioni dei parser

Le eccezioni che si incontrano nell'elaborazione di XML sono tutte **controllate** ([Capitolo 13](13-eccezioni.md)): il compilatore pretende che siano catturate o dichiarate. Sono tre, e vanno conosciute per nome perché compaiono nella clausola `throws`.

| Eccezione | Package | Quando |
|---|---|---|
| `ParserConfigurationException` | `javax.xml.parsers` | `newDocumentBuilder()` o `newSAXParser()` non riescono a creare il parser richiesto |
| `SAXException` | `org.xml.sax` | il documento **non è ben formato** (il parser lancia la sottoclasse `SAXParseException`) |
| `IOException` | `java.io` | il file non c'è o non si legge |

Chi scrive un metodo che usa un parser ha due strade: dichiarare le tre con `throws ParserConfigurationException, SAXException, IOException`, oppure catturarle con un `try`/`catch`. Se la traccia dà la firma di un metodo senza `throws`, le eccezioni vanno catturate dentro. Tutte e tre le classi sono sottoclassi di `Exception`, per cui in un esercizio di fretta si può anche catturare `Exception`, a patto che la traccia non richieda altro.

### 20.3.4 Opzioni del parser

Le fabbriche permettono di configurare il parser prima di crearlo. Due opzioni compaiono nella documentazione e conviene riconoscerle:

- `setValidating(boolean)`: se `true`, il parser controlla anche la **validità** del documento, oltre alla buona formazione;
- `setNamespaceAware(boolean)`: se `true`, il parser tratta correttamente i **namespace** (i prefissi dei nomi, come `a:b`). Per i documenti senza prefissi, il caso comune, non cambia nulla nel risultato del DOM, ma influisce sui nomi forniti a SAX (paragrafo 20.5.5).

Entrambe sono metodi delle fabbriche, da chiamare **prima** di `newDocumentBuilder()` o `newSAXParser()`. Se si vuole reagire agli errori del documento in modo personalizzato, si scrive una classe che realizza l'interfaccia `ErrorHandler` di SAX (metodi `warning`, `error` e `fatalError`) e la si registra sul parser DOM con `setErrorHandler`. Nei casi d'esame i valori predefiniti bastano.

---

## 20.4 DOM: leggere e costruire l'albero

### 20.4.1 I nodi e i loro tipi

Nel DOM **tutto è un nodo**. L'interfaccia `Node` (package `org.w3c.dom`) è la radice di una piccola gerarchia di interfacce, una per ogni tipo di cosa che può comparire in un documento. Le più importanti sono quattro.

| Interfaccia | Che cosa rappresenta | Costante di `getNodeType()` |
|---|---|---|
| `Document` | l'intero documento; è il punto di partenza di ogni ricerca | `Node.DOCUMENT_NODE` |
| `Element` | un elemento (un tag): ha un nome, può avere figli e attributi | `Node.ELEMENT_NODE` |
| `Attr` | un attributo (`codice="A10"`) | `Node.ATTRIBUTE_NODE` |
| `Text` | un pezzo di testo | `Node.TEXT_NODE` |

Un punto che sorprende chi comincia: il **testo** di un elemento **non è** una proprietà dell'elemento, ma un **nodo figlio** a sé, di tipo `Text`. Nel disegno dell'albero del paragrafo 20.1.1, `Lampada` non sta «dentro» il nodo `nome`: è il nodo di testo figlio del nodo `nome`. Per questo, per leggere il testo, ci sono due strade (paragrafo 20.4.5): scendere al figlio, oppure usare un metodo che lo cerca per noi. Esistono anche altri tipi di nodo, tra cui i commenti (`Comment`, `Node.COMMENT_NODE`).

Ogni nodo ha un **nome** e un **valore**, il cui significato dipende dal tipo. La tabella, ricavata dalla documentazione, è importante perché spiega un errore tipico (paragrafo 20.4.5):

| Tipo di nodo | `getNodeName()` | `getNodeValue()` |
|---|---|---|
| `Element` | il nome del tag (come `getTagName()`) | **`null`** |
| `Attr` | il nome dell'attributo | il valore dell'attributo |
| `Text` | la costante `"#text"` | il contenuto del testo |
| `Comment` | la costante `"#comment"` | il contenuto del commento |
| `Document` | la costante `"#document"` | `null` |

> [!NOTE]
> **Approfondimento esterno — `Node`: nome e valore secondo il tipo**
> La documentazione ufficiale di `Node` riporta una tabella che, per ogni tipo di nodo, indica che cosa restituiscono `nodeName`, `nodeValue` e `attributes`. Per un `Element`, `nodeName` è «*same as Element.tagName*» e `nodeValue` è `null`; per un `Text`, `nodeName` è `"#text"` e `nodeValue` è «*same as CharacterData.data, the content of the text node*»; per un `Document`, `nodeName` è `"#document"` e `nodeValue` è `null`.
>
> *Fonte:* [Node (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/Node.html)

### 20.4.2 Caricare un documento

Il caricamento ha sempre gli stessi tre passi: una fabbrica, un `DocumentBuilder`, e `parse`, che restituisce il `Document`.

```java
DocumentBuilderFactory fabbrica = DocumentBuilderFactory.newInstance();   // 1. la fabbrica
DocumentBuilder builder = fabbrica.newDocumentBuilder();                  // 2. il parser DOM
Document doc = builder.parse(new File("catalogo.xml"));                   // 3. l'albero in memoria
```

`parse` esiste in più forme, a seconda di dove si trova il documento:

| Forma | Sorgente |
|---|---|
| `parse(File f)` | un file su disco: la forma più usata |
| `parse(InputStream is)` | un flusso di byte (per esempio quello di un socket, [Capitolo 19](19-networking.md)) |
| `parse(InputSource is)` | un `InputSource` (package `org.xml.sax`), che può avvolgere un `Reader` |
| `parse(String uri)` | un indirizzo (URI) in forma di stringa, **non** il testo del documento |

L'ultima merita attenzione: la `String` che si passa a `parse(String)` è un **indirizzo** da cui leggere, non il documento stesso. Se si ha il testo XML in una stringa (per esempio per provare un programma senza creare un file), bisogna avvolgerlo in un `Reader` e in un `InputSource`:

```java
String testo = "<a><b>uno</b><b>due</b></a>";
Document doc = builder.parse(new InputSource(new StringReader(testo)));
```

`StringReader` (package `java.io`) è un `Reader` che legge da una `String`; `InputSource` viene da `org.xml.sax`. In alternativa si può passare per i byte: `builder.parse(new ByteArrayInputStream(testo.getBytes()))`.

Le tre eccezioni da gestire sono quelle del paragrafo 20.3.3: `ParserConfigurationException` dal secondo passo, `SAXException` e `IOException` dal terzo.

### 20.4.3 Navigare: la radice e le liste di nodi

Con il `Document` in mano si comincia dalla radice:

```java
Element radice = doc.getDocumentElement();     // l'elemento <catalogo>
radice.normalize();                            // unisce nodi di testo adiacenti
```

Il metodo si chiama `getDocumentElement` (**singolare**, e non `getDocumentElements`). Restituisce l'`Element` radice. Il metodo `normalize()` fonde i nodi di testo adiacenti e rimuove quelli vuoti, rendendo l'albero nella forma «naturale»; è buona pratica chiamarlo subito dopo il caricamento.

Per raggiungere gli altri elementi esistono due strade.

**Per nome del tag**, con `getElementsByTagName`: restituisce **tutti** gli elementi discendenti con quel nome, in ordine di documento. Si può chiamare sul `Document` (cerca in tutto il documento) o su un `Element` (cerca solo tra i suoi discendenti). Il nome speciale `"*"` equivale a «qualunque elemento».

```java
NodeList prodotti = doc.getElementsByTagName("prodotto");   // i tre <prodotto>
```

**Per parentela**, con `getChildNodes`, che restituisce tutti i **figli** diretti di un nodo.

Entrambi i metodi restituiscono un oggetto `NodeList`. Non è una lista come quelle di `java.util` ([Capitolo 12](12-generics-e-collezioni.md)): non è una `List`, non ha `size()` né `get(i)`, non si usa nel for-each. Ha esattamente due metodi:

| Metodo | Significato |
|---|---|
| `int getLength()` | il numero di nodi nella lista |
| `Node item(int index)` | il nodo in posizione `index` (da `0` a `getLength() - 1`) |

Si scorre quindi con un ciclo `for` a indice, come un array, ma chiamando **`getLength()` con le parentesi**: non è il campo `length` degli array ([Capitolo 5](05-array-e-matrici.md)), né il metodo `size()` delle liste.

```java
for (int i = 0; i < prodotti.getLength(); i++) {
    Node nodo = prodotti.item(i);
    // ... uso di nodo ...
}
```

Il tipo di ritorno di `item` è `Node`, l'interfaccia più generica. Per usare i metodi specifici degli elementi (gli attributi, la ricerca per tag) serve un **cast** a `Element`, come per ogni valore restituito con un tipo più generale ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)): `Element e = (Element) nodo;`. Attenzione: il cast è a `Element` (singolare, di `org.w3c.dom`), non a `Elements`.

> [!NOTE]
> **Approfondimento esterno — `getElementsByTagName` e `getDocumentElement`**
> La documentazione ufficiale di `Document.getElementsByTagName(String tagname)` dice: «*Returns a NodeList of all the Elements in document order with a given tag name and are contained in the document*»; «*The special value "*" matches all tags*» e per XML «*the tagname parameter is case-sensitive*» (maiuscole e minuscole contano). Analogamente `Element.getElementsByTagName(String name)` restituisce i discendenti dell'elemento. `Document.getDocumentElement()` è «*a convenience attribute that allows direct access to the child node that is the document element of the document*». `NodeList.getLength()` è «*The number of nodes in the list. The range of valid child node indices is 0 to length-1 inclusive*».
>
> *Fonte:* [Document (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/Document.html), [Element (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/Element.html) e [NodeList (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/NodeList.html)

### 20.4.4 Gli spazi bianchi sono nodi

Ecco una trappola che coglie quasi tutti la prima volta. Il file del paragrafo 20.1.1 è «indentato»: tra un `<prodotto>` e il successivo ci sono un a capo e qualche spazio. Per il parser, quegli spazi e quegli a capo **sono testo**, e quindi **nodi di tipo `Text`**. Proviamo a elencare i figli diretti della radice:

```java
import java.io.File;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class ProvaSpazi {
    public static void main(String[] args) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance().newDocumentBuilder()
                .parse(new File("catalogo.xml"));
        Element radice = doc.getDocumentElement();
        System.out.println("Radice: " + radice.getNodeName());
        NodeList figli = radice.getChildNodes();
        System.out.println("Figli della radice: " + figli.getLength());
        for (int i = 0; i < figli.getLength(); i++) {
            Node n = figli.item(i);
            System.out.println(i + ": " + n.getNodeName() + " tipo " + n.getNodeType());
        }
    }
}
```

Il programma dichiara `throws Exception` per brevità, ed elenca i figli della radice con il loro nome e il codice del tipo. L'uscita è:

```text
Radice: catalogo
Figli della radice: 7
0: #text tipo 3
1: prodotto tipo 1
2: #text tipo 3
3: prodotto tipo 1
4: #text tipo 3
5: prodotto tipo 1
6: #text tipo 3
```

La radice ha **sette** figli, non tre: i tre `prodotto` (tipo 1, `ELEMENT_NODE`) sono intervallati da quattro nodi `#text` (tipo 3, `TEXT_NODE`) che contengono solo spazi e a capo. Un programma che scorre `getChildNodes()` e tratta ogni figlio come un prodotto trova, ogni due elementi, un nodo di testo che non è un elemento, e al primo cast a `Element` si imbatte in una `ClassCastException`, oppure ottiene valori vuoti.

Esistono due rimedi, e va saputo scegliere.

1. **Usare `getElementsByTagName`**, che restituisce solo elementi con il nome richiesto e ignora i nodi di testo. È la soluzione più semplice, ed è quella che useremo.
2. **Filtrare per tipo** scorrendo `getChildNodes()` e tenendo solo i nodi con `n.getNodeType() == Node.ELEMENT_NODE`.

Nei documenti senza indentazione (`<catalogo><prodotto>...</prodotto></catalogo>` su una riga) i nodi di spazio non ci sono, ma non si può contare su questo: un programma che funziona su un file compatto si rompe su uno indentato. Con `getElementsByTagName` il problema non si pone.

### 20.4.5 Leggere attributi e testo

Dato un `Element` (il cast descritto sopra), si leggono attributi e testo così.

**Un attributo** si legge con `getAttribute(String name)`, che restituisce una `String`: il valore dell'attributo, oppure la **stringa vuota** se l'attributo non esiste (non `null`, e non un'eccezione).

```java
String codice = prodotto.getAttribute("codice");     // "A10"
String manca = prodotto.getAttribute("colore");       // "" (attributo assente)
```

**Il testo di un figlio** si può leggere in due modi.

- Con `getTextContent()`, che restituisce il testo contenuto nell'elemento e nei suoi discendenti: `e.getElementsByTagName("nome").item(0).getTextContent()` restituisce `"Lampada"`. È il modo più comodo e quello che useremo.
- Scendendo al nodo di testo: `e.getElementsByTagName("nome").item(0).getFirstChild().getNodeValue()` fa lo stesso, ma in due passi (`getFirstChild()` restituisce il nodo di testo figlio, `getNodeValue()` ne legge il contenuto).

Il `getNodeValue()` va chiamato sul **nodo di testo**, non sull'elemento. Per la tabella del paragrafo 20.4.1, un `Element` ha valore `null`; chiamare `getNodeValue()` direttamente sul nodo `nome` restituisce `null`, non `"Lampada"`. Lo mostra un breve programma, in cui `primo` è il primo elemento `nome`:

```java
Element primo = (Element) doc.getElementsByTagName("nome").item(0);
System.out.println(primo.getFirstChild().getNodeValue());    // Lampada
System.out.println(primo.getNodeValue());                     // null
System.out.println(primo.getTextContent());                   // Lampada
```

```text
Lampada
null
Lampada
```

Una precisazione su `getTextContent()`: chiamato su un elemento che contiene altri elementi (come `prodotto`) restituisce il testo di **tutti** i discendenti messi in fila, **compresi gli spazi di indentazione**. Per `<prodotto>` del nostro file restituirebbe una stringa di 25 caratteri, in cui `Lampada` e `24.50` sono circondati da a capo e spazi. Per questo il testo si legge dal **figlio foglia** (`nome`, `prezzo`), non dal contenitore.

Il testo letto è sempre una `String`. Per usarlo come numero va convertito, e la conversione può fallire ([Capitolo 6](06-metodi.md)): `Double.parseDouble("24.50")` dà `24.5`, `Integer.parseInt("12")` dà `12`, mentre una stringa non numerica lancia `NumberFormatException`.

> [!NOTE]
> **Approfondimento esterno — `getTextContent`, `getAttribute`**
> Per `Node.getTextContent()` la documentazione ufficiale scrive che «*returns the text content of this node and its descendants*» e che «*No whitespace normalization is performed*» (non c'è alcuna pulizia degli spazi). Per `Element.getAttribute(String name)` scrive che restituisce «*The Attr value as a string, or the empty string if that attribute does not have a specified or default value*».
>
> *Fonte:* [Node (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/Node.html) e [Element (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/Element.html)

### 20.4.6 Un esempio completo: leggere il catalogo

Mettiamo insieme i pezzi. Il programma carica `catalogo.xml`, stampa codice, nome e prezzo di ogni prodotto e calcola il totale dei prezzi.

#### Esempio — Leggere un documento con DOM

```java
import java.io.File;
import java.io.IOException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class LeggiCatalogo {
    public static void main(String[] args)
            throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory fabbrica = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = fabbrica.newDocumentBuilder();
        Document doc = builder.parse(new File("catalogo.xml"));
        doc.getDocumentElement().normalize();

        NodeList prodotti = doc.getElementsByTagName("prodotto");
        double totale = 0;
        for (int i = 0; i < prodotti.getLength(); i++) {
            Node nodo = prodotti.item(i);
            Element prodotto = (Element) nodo;
            String codice = prodotto.getAttribute("codice");
            String nome = prodotto.getElementsByTagName("nome").item(0).getTextContent();
            double prezzo = Double.parseDouble(
                    prodotto.getElementsByTagName("prezzo").item(0).getTextContent());
            System.out.println(codice + " " + nome + " " + prezzo);
            totale = totale + prezzo;
        }
        System.out.println("Totale: " + totale);
    }
}
```

Riga per riga. I dieci `import` sono esplicitati perché all'esame si scrivono a mano: le classi di `javax.xml.parsers`, di `org.w3c.dom` e `org.xml.sax` sono in tre package diversi, e dimenticarne uno è un errore di compilazione. Il `main` dichiara le tre eccezioni controllate del paragrafo 20.3.3. Le prime tre righe del corpo sono la sequenza fabbrica-builder-`parse`; `normalize()` pulisce l'albero. `getElementsByTagName("prodotto")` raccoglie i tre prodotti. Nel ciclo, `prodotti.item(i)` dà un `Node`, che va convertito in `Element` con il cast; da `prodotto` si leggono l'attributo `codice` e, per `nome` e `prezzo`, si cerca il figlio per tag (`getElementsByTagName(...)`) e si prende il **primo** risultato con `.item(0)`, perché ce n'è uno solo per prodotto. Il prezzo, testo, viene convertito con `Double.parseDouble`.

Con `catalogo.xml` nella cartella corrente l'uscita è:

```text
A10 Lampada 24.5
B20 Tavolo 120.0
C30 Sedia 35.9
Totale: 180.4
```

I prezzi sono stampati senza lo zero finale (`24.5`, non `24.50`) perché sono stati convertiti in `double`: a stampare è un numero, non il testo del documento.

### 20.4.7 Dal documento agli oggetti

Nei programmi veri il fine non è stampare, ma **costruire oggetti** a partire dai dati. È la composizione tipica di un esercizio: parsing DOM, creazione di oggetti, raccolta in una lista, `return`. Il metodo seguente carica il catalogo e restituisce una `List<Prodotto>`.

#### Esempio — Un metodo che restituisce una lista di oggetti

```java
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

class Prodotto {
    private String codice;
    private String nome;
    private double prezzo;

    public Prodotto(String codice, String nome, double prezzo) {
        this.codice = codice;
        this.nome = nome;
        this.prezzo = prezzo;
    }

    public double getPrezzo() { return prezzo; }

    public String toString() {
        return codice + " " + nome + " " + prezzo;
    }
}

public class CaricaProdotti {
    public static List<Prodotto> carica(String nomeFile)
            throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document doc = builder.parse(new File(nomeFile));
        List<Prodotto> lista = new ArrayList<Prodotto>();
        NodeList nodi = doc.getElementsByTagName("prodotto");
        for (int i = 0; i < nodi.getLength(); i++) {
            Element e = (Element) nodi.item(i);
            String codice = e.getAttribute("codice");
            String nome = e.getElementsByTagName("nome").item(0).getTextContent();
            double prezzo = Double.parseDouble(
                    e.getElementsByTagName("prezzo").item(0).getTextContent());
            lista.add(new Prodotto(codice, nome, prezzo));
        }
        return lista;
    }

    public static void main(String[] args) throws Exception {
        List<Prodotto> prodotti = carica("catalogo.xml");
        System.out.println(prodotti.size() + " prodotti");
        for (Prodotto p : prodotti) {
            System.out.println(p);
        }
    }
}
```

La classe `Prodotto` è un normale oggetto del [Capitolo 7](07-classi-e-oggetti.md), con campi `private` e un costruttore. Il metodo `carica` è `static`, riceve il nome del file e dichiara le tre eccezioni controllate: è il chiamante a decidere come gestirle. Per ogni nodo della lista costruisce un `Prodotto` e lo aggiunge a una `ArrayList`. Uscita:

```text
3 prodotti
A10 Lampada 24.5
B20 Tavolo 120.0
C30 Sedia 35.9
```

### 20.4.8 Costruire e modificare un documento

Il DOM non serve solo a leggere: l'albero si può **costruire da zero** o **modificare**. Le regole sono quelle di una fabbrica di oggetti: un nodo si crea chiamando un metodo `create...` del `Document` a cui appartiene, e poi si collega all'albero con `appendChild`.

| Metodo | Dove | Che cosa fa |
|---|---|---|
| `newDocument()` | `DocumentBuilder` | crea un documento vuoto |
| `createElement(String tagName)` | `Document` | crea un elemento con quel nome |
| `createTextNode(String data)` | `Document` | crea un nodo di testo |
| `setAttribute(String name, String value)` | `Element` | aggiunge (o cambia) un attributo |
| `appendChild(Node newChild)` | `Node` | aggiunge il nodo **in coda** ai figli |
| `removeChild(Node oldChild)` | `Node` | toglie un figlio |
| `insertBefore(Node newChild, Node refChild)` | `Node` | inserisce prima di un figlio dato |
| `replaceChild(Node newChild, Node oldChild)` | `Node` | sostituisce un figlio con un altro |

Costruiamo un documento che contiene un solo prodotto: l'ordine è sempre «crea, completa, collega».

```java
DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
Document doc = builder.newDocument();                    // documento vuoto

Element catalogo = doc.createElement("catalogo");        // crea la radice...
doc.appendChild(catalogo);                               // ...e la collega al documento

Element prodotto = doc.createElement("prodotto");
prodotto.setAttribute("codice", "D40");                  // attributo
Element nome = doc.createElement("nome");
nome.appendChild(doc.createTextNode("Scaffale"));        // il testo e' un nodo figlio
prodotto.appendChild(nome);
catalogo.appendChild(prodotto);
```

Si noti che il testo `Scaffale` si inserisce creando un **nodo di testo** e collegandolo come figlio dell'elemento `nome`, esattamente come l'albero lo rappresenta. Gli elementi si collegano **dal basso verso l'alto** o dall'alto verso il basso, indifferentemente, purché ogni nodo finisca come figlio di un altro e la radice come figlio del documento.

Il metodo `appendChild` dichiara `throws DOMException`, un'eccezione **non controllata**: non va né dichiarata né catturata.

> [!NOTE]
> **Approfondimento esterno — Creare e collegare nodi**
> La documentazione ufficiale descrive `Document.createElement(String tagName)` come «*Creates an element of the type specified. Note that the instance returned implements the Element interface, so attributes can be specified directly on the returned object*», `Document.createTextNode(String data)` come «*Creates a Text node given the specified string*» e `Node.appendChild(Node newChild)` come «*Adds the node newChild to the end of the list of children of this node. If the newChild is already in the tree, it is first removed*». `Element.setAttribute` «*Adds a new attribute. If an attribute with that name is already present in the element, its value is changed*».
>
> *Fonte:* [Document (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/Document.html) e [Node (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/w3c/dom/Node.html)

### 20.4.9 Salvare un documento: un cenno

Costruire un albero in memoria serve a poco se non si riesce a salvarlo. Le interfacce DOM, però, **non specificano** come si salva un documento: l'operazione è affidata alle implementazioni. In JAXP il compito si svolge con le classi del package `javax.xml.transform`, che sono pensate per «trasformare» una sorgente in una destinazione e che, usate senza istruzioni di trasformazione, si limitano a **copiare** l'albero in un'uscita.

Lo schema minimo è fisso: si ottiene un `Transformer` dalla sua fabbrica e gli si chiede di trasformare un `DOMSource` (l'albero) in uno `StreamResult` (il file).

```java
import java.io.File;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Document;

public class Salvataggio {
    public static void salva(Document doc, String nomeFile) throws TransformerException {
        Transformer t = TransformerFactory.newInstance().newTransformer();
        t.transform(new DOMSource(doc), new StreamResult(new File(nomeFile)));
    }
}
```

Il metodo `transform` dichiara `throws TransformerException`, un'eccezione **controllata**; `newTransformer()` dichiara `TransformerConfigurationException`, una sua sottoclasse. Il file prodotto contiene l'albero su una sola riga (senza indentazione) preceduto dalla dichiarazione XML:

```text
<?xml version="1.0" encoding="UTF-8" standalone="no"?><elenco><voce n="1">primo</voce></elenco>
```

È un **cenno**: lo schema va riconosciuto, ma l'esame si concentra sulla lettura.

> [!NOTE]
> **Approfondimento esterno — `javax.xml.transform`**
> La documentazione ufficiale presenta il package come quello che «*Defines the generic APIs for processing transformation instructions, and performing a transformation from source to result*». Il metodo `TransformerFactory.newTransformer()` «*Create a new Transformer that performs a copy of the Source to the Result, i.e. the "identity transform"*» e lancia `TransformerConfigurationException`. Il metodo `Transformer.transform(Source xmlSource, Result outputTarget)` dichiara `throws TransformerException`.
>
> *Fonte:* [javax.xml.transform (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/javax/xml/transform/package-summary.html) e [Transformer (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/javax/xml/transform/Transformer.html)

### 20.4.10 Muoversi nell'albero

Oltre a `getElementsByTagName`, l'interfaccia `Node` offre metodi per muoversi lungo le relazioni di parentela. Sono utili quando la struttura non si può ricavare dal solo nome dei tag.

| Metodo | Restituisce |
|---|---|
| `getParentNode()` | il nodo padre |
| `getChildNodes()` | la `NodeList` dei figli |
| `getFirstChild()`, `getLastChild()` | il primo e l'ultimo figlio |
| `getPreviousSibling()`, `getNextSibling()` | il fratello precedente e quello successivo |
| `hasChildNodes()` | `true` se ha figli |
| `getOwnerDocument()` | il `Document` a cui il nodo appartiene |
| `hasAttributes()`, `getAttributes()` | se ha attributi; la mappa degli attributi (`NamedNodeMap`) |

`getAttributes()` restituisce una `NamedNodeMap`, un insieme di nodi (qui gli attributi) individuati per **nome** e non per posizione; chi vuole solo il valore di un attributo di cui conosce il nome usa direttamente `getAttribute`. Per gli `Element` esistono inoltre `getTagName()` (il nome del tag), `hasAttribute(String name)` (esiste l'attributo?) e `removeAttribute(String name)`. Come per `getChildNodes`, tenere a mente la trappola degli spazi bianchi (paragrafo 20.4.4): `getFirstChild()` e `getNextSibling()` di un elemento in un file indentato possono restituire nodi di testo.

---

## 20.5 SAX: lasciare che sia il parser a chiamare noi

### 20.5.1 Il modello a callback

Con SAX il programma non «va a prendere» i dati: li **riceve**. Scrive una classe con alcuni metodi e la consegna al parser; il parser percorre il documento e, a ogni evento, chiama il metodo corrispondente. I metodi che il programma scrive per essere chiamati da qualcun altro si chiamano **callback** (letteralmente «richiamo»).

L'interfaccia che raccoglie i metodi degli eventi del contenuto si chiama `ContentHandler` (package `org.xml.sax`). Ha molti metodi, ma ne bastano pochi.

| Metodo | Quando il parser lo chiama |
|---|---|
| `startDocument()` | all'inizio del documento |
| `endDocument()` | alla fine del documento |
| `startElement(String uri, String localName, String qName, Attributes atts)` | all'**apertura** di un elemento: `<prodotto codice="A10">` |
| `characters(char[] ch, int start, int length)` | quando incontra **testo** |
| `endElement(String uri, String localName, String qName)` | alla **chiusura** di un elemento: `</prodotto>` |

Realizzare l'interfaccia `ContentHandler` per intero significherebbe scrivere tutti i suoi metodi, anche quelli che non servono. Per questo esiste la classe **`DefaultHandler`** (package `org.xml.sax.helpers`), che li realizza tutti con un corpo vuoto («non fare nulla»). Il programmatore la **estende** e **riscrive** (*override*, [Capitolo 9](09-ereditarieta-e-polimorfismo.md)) soltanto i metodi che gli interessano, lasciando che gli eventi degli altri siano ignorati.

> [!NOTE]
> **Definizione — Gestore SAX**
> Un **gestore** (*handler*) SAX è una classe che estende `DefaultHandler` e riscrive i metodi `startElement`, `characters`, `endElement` (e, se serve, `startDocument`, `endDocument`).
> Le firme esatte da riscrivere sono:
> `public void startElement(String uri, String localName, String qName, Attributes atts)`
> `public void characters(char[] ch, int start, int length)`
> `public void endElement(String uri, String localName, String qName)`

Il nome dei metodi, l'ordine e il **tipo** dei parametri devono coincidere con quelli di `DefaultHandler`. Se non coincidono, il metodo scritto **non** riscrive nulla: diventa un metodo diverso (un *overload*, [Capitolo 6](06-metodi.md)), e il parser continua a chiamare quello vuoto della superclasse. Il programma compila e funziona «senza fare niente». Si previene l'errore con l'annotazione `@Override` ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)) davanti al metodo: se la firma non coincide, il compilatore protesta.

Le firme dichiarano `throws SAXException` in `DefaultHandler`, ma un metodo che li riscrive **può omettere** la clausola `throws` (un override non può dichiarare eccezioni controllate in più, ma può dichiararne di meno, [Capitolo 13](13-eccezioni.md)).

### 20.5.2 Un esempio: il catalogo con SAX

Ripetiamo la lettura del catalogo del paragrafo 20.1.1, stavolta con SAX: stampiamo codice, nome e prezzo di ogni prodotto e il totale. Con SAX nulla è memorizzato dal parser, e dunque la classe deve **ricordarsi da sola** in che punto del documento si trova. Il metodo standard sono i **flag** booleani: uno per ogni elemento di cui interessa il testo, acceso quando l'elemento si apre e spento quando si chiude.

#### Esempio — Un gestore SAX con i flag

```java
import java.io.File;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

class HandlerCatalogo extends DefaultHandler {
    private boolean inNome = false;           // siamo dentro <nome> ?
    private boolean inPrezzo = false;         // siamo dentro <prezzo> ?
    private String codice = "";
    private String nome = "";
    private String prezzo = "";
    private double totale = 0;

    @Override
    public void startElement(String uri, String localName, String qName, Attributes atts) {
        if (qName.equals("prodotto")) {
            codice = atts.getValue("codice");          // legge l'attributo
        }
        if (qName.equals("nome")) {
            inNome = true;
            nome = "";
        }
        if (qName.equals("prezzo")) {
            inPrezzo = true;
            prezzo = "";
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        if (inNome) {
            nome = nome + new String(ch, start, length);
        }
        if (inPrezzo) {
            prezzo = prezzo + new String(ch, start, length);
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.equals("nome")) {
            inNome = false;
        }
        if (qName.equals("prezzo")) {
            inPrezzo = false;
        }
        if (qName.equals("prodotto")) {                // il prodotto e' completo: si usa
            System.out.println(codice + " " + nome + " " + prezzo);
            totale = totale + Double.parseDouble(prezzo);
        }
    }

    @Override
    public void endDocument() {
        System.out.println("Totale: " + totale);
    }
}

public class ContaSax {
    public static void main(String[] args) throws Exception {
        SAXParserFactory fabbrica = SAXParserFactory.newInstance();
        SAXParser parser = fabbrica.newSAXParser();
        parser.parse(new File("catalogo.xml"), new HandlerCatalogo());
    }
}
```

Per capire come lavora, seguiamo gli eventi del **primo prodotto**, dal punto di vista del gestore. Ricordiamo che gli spazi e gli a capo tra i tag sono testo anch'essi, ma non incidono perché i flag sono spenti.

| Il parser incontra… | Chiama… | Che cosa fa il gestore |
|---|---|---|
| `<prodotto codice="A10">` | `startElement` (qName `prodotto`) | legge l'attributo: `codice = "A10"` |
| `<nome>` | `startElement` (qName `nome`) | accende `inNome`, azzera `nome` |
| `Lampada` | `characters` | `inNome` è acceso: `nome = "Lampada"` |
| `</nome>` | `endElement` (qName `nome`) | spegne `inNome` |
| `<prezzo>`, `24.50`, `</prezzo>` | idem | `prezzo = "24.50"`, flag spento |
| `</prodotto>` | `endElement` (qName `prodotto`) | stampa la riga, somma il prezzo |

Quando il prodotto si chiude, il gestore ha raccolto tutti i suoi dati: è il momento giusto per **usarli** (stamparli, costruire un oggetto, aggiungerlo a una lista). Uscita:

```text
A10 Lampada 24.50
B20 Tavolo 120.00
C30 Sedia 35.90
Totale: 180.4
```

I prezzi compaiono come nel documento (`24.50`) perché qui li abbiamo stampati come **testo**, e li abbiamo convertiti in `double` solo per la somma: nell'esempio DOM del paragrafo 20.4.6 la stampa era del numero.

La classe `ContaSax` ha la parte «fissa» del SAX: fabbrica, parser, `parse`. Il metodo `SAXParser.parse(File f, DefaultHandler dh)` legge il file e chiama il gestore. Dichiara `throws SAXException, IOException`, mentre `newSAXParser()` dichiara `ParserConfigurationException` e `SAXException`: il `main` dichiara `throws Exception` per comprenderle tutte (in un metodo da consegnare sono preferibili le tre eccezioni esplicite del paragrafo 20.3.3).

> [!NOTE]
> **Approfondimento esterno — `SAXParser.parse` e `newSAXParser`**
> La documentazione ufficiale descrive `public void parse(File f, DefaultHandler dh) throws SAXException, IOException` come «*Parse the content of the file specified as XML using the specified DefaultHandler*», con `IllegalArgumentException` «*If the File object is null*». Il metodo `public abstract SAXParser newSAXParser() throws ParserConfigurationException, SAXException` della `SAXParserFactory` «*Creates a new instance of a SAXParser using the currently configured factory parameters*».
>
> *Fonte:* [SAXParser (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/javax/xml/parsers/SAXParser.html) e [SAXParserFactory (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/javax/xml/parsers/SAXParserFactory.html)

### 20.5.3 La forma con `XMLReader`

La forma più completa passa per un oggetto `XMLReader`: dal `SAXParser` si ottiene il lettore (`getXMLReader()`), gli si registra il gestore con `setContentHandler(...)` e si avvia la lettura con `parse(...)`.

```java
SAXParserFactory spf = SAXParserFactory.newInstance();
SAXParser saxParser = spf.newSAXParser();
XMLReader xmlReader = saxParser.getXMLReader();
xmlReader.setContentHandler(new HandlerCatalogo());
xmlReader.parse("catalogo.xml");
```

`XMLReader` si importa da `org.xml.sax`. `XMLReader.parse(String systemId)` riceve il nome (o l'indirizzo) del documento da leggere e dichiara `throws IOException, SAXException`. Le due forme sono equivalenti: con lo stesso gestore producono lo stesso risultato. La prima (`parser.parse(file, gestore)`) è più breve; la seconda permette di registrare più gestori (per esempio uno per gli errori) prima di avviare la lettura.

Sull'`XMLReader` l'interfaccia dei gestori è divisa in quattro parti, di cui `ContentHandler` è la più usata: `ContentHandler` (gli eventi del contenuto), `ErrorHandler` (errori e avvertimenti), `DTDHandler` ed `EntityResolver` (casi avanzati, dichiarazioni e riferimenti a entità esterne). Se un gestore non viene registrato, il comportamento predefinito è **ignorare** gli eventi corrispondenti.

### 20.5.4 `characters` può arrivare a pezzi

Nell'esempio abbiamo scritto `nome = nome + new String(ch, start, length)` e non semplicemente `nome = new String(ch, start, length)`. La differenza, che sembra pedanteria, è un punto del contratto di SAX.

Il parametro `ch` di `characters` è un array di caratteri **condiviso dal parser**; il testo che interessa è solo la parte da `start` per `length` caratteri, ed è questa che `new String(ch, start, length)` copia. E non è detto che l'intero testo di un elemento arrivi in **un'unica** chiamata: la documentazione dice che il parser **può** consegnare il testo contiguo in una sola chiamata, **oppure** spezzarlo in più. Con testi brevi quasi mai succede, ma un programma corretto non deve contarci. La forma sicura è **accumulare**: azzerare la stringa all'apertura dell'elemento (`nome = ""`) e **aggiungere** (`+`) a ogni chiamata, e usare il valore completo solo alla chiusura.

> [!NOTE]
> **Approfondimento esterno — `ContentHandler.characters`**
> La documentazione ufficiale di `characters(char[] ch, int start, int length)` dice: «*The Parser will call this method to report each chunk of character data. SAX parsers may return all contiguous character data in a single chunk, or they may split it into several chunks*» e aggiunge che «*The application must not attempt to read from the array outside of the specified range*».
>
> *Fonte:* [ContentHandler (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/xml/sax/ContentHandler.html)

### 20.5.5 `qName` e `localName`

Un'ultima sottigliezza riguarda i **nomi** degli elementi. `startElement` e `endElement` ricevono tre nomi: `uri`, `localName` e `qName`. Per i documenti senza prefissi (il nostro caso) conviene sapere che:

- `qName` (*qualified name*) è il nome del tag così come scritto nel documento: per `<prodotto>` vale `"prodotto"`. **Sempre disponibile** nella configurazione predefinita.
- `localName` è il nome «senza prefisso», e viene fornito **solo se il parser tratta i namespace**. Nella configurazione predefinita di `SAXParserFactory` il parser non li tratta, e `localName` è la **stringa vuota**.

Lo si verifica con un breve programma, che stampa i nomi del documento `<a><b>x</b></a>` con e senza `setNamespaceAware(true)`:

```text
nsAware=false localName=[] qName=[a]
nsAware=false localName=[] qName=[b]
nsAware=true localName=[a] qName=[a]
nsAware=true localName=[b] qName=[b]
```

Un confronto `localName.equals("prodotto")` nella configurazione predefinita è quindi **sempre falso**, e il gestore non reagisce mai. Per questo negli esempi di questo capitolo si confronta **`qName`**. In alternativa si può chiamare `spf.setNamespaceAware(true)` prima di `newSAXParser()`, e allora anche `localName` è valorizzato.

> [!NOTE]
> **Approfondimento esterno — I nomi in `startElement`**
> La documentazione ufficiale di `DefaultHandler.startElement` descrive i parametri: `uri` è «*the Namespace URI, or the empty string if the element has no Namespace URI or if Namespace processing is not being performed*»; `localName` è «*the local name (without prefix), or the empty string if Namespace processing is not being performed*»; `qName` è «*the qualified name (with prefix), or the empty string if qualified names are not available*». `Attributes.getValue(String qName)` restituisce «*The attribute value as a string, or null if the attribute is not in the list or if qualified names are not available*».
>
> *Fonte:* [DefaultHandler (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/xml/sax/helpers/DefaultHandler.html) e [Attributes (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/org/xml/sax/Attributes.html)

### 20.5.6 Gli attributi con `Attributes`

L'ultimo parametro di `startElement` è un oggetto `Attributes`, che contiene gli attributi dell'elemento appena aperto. Quello che si fa quasi sempre è leggere un attributo di cui si conosce il nome:

```java
String codice = atts.getValue("codice");     // null se l'attributo non c'e'
```

Diversamente da `Element.getAttribute` del DOM, che restituisce la stringa vuota se manca l'attributo, `Attributes.getValue` restituisce **`null`**. Gli attributi si leggono **solo dentro `startElement`**: l'oggetto `Attributes` non è più valido dopo il ritorno del metodo, quindi l'eventuale valore da riusare va copiato in un campo del gestore, come abbiamo fatto con `codice`.

---

## 20.6 DOM o SAX?

La scelta si riduce a una domanda: il programma ha bisogno di **muoversi** nel documento, oppure di **passarci sopra una volta sola**?

- Si sceglie **DOM** quando il documento è di dimensioni ragionevoli e serve libertà: cercare un elemento per nome, rileggere più volte, mettere in relazione parti lontane, **modificare** o costruire il documento. È la scelta predefinita nei programmi d'esame, perché il codice è più corto e più facile da scrivere a memoria: fabbrica, builder, `parse`, `getElementsByTagName`, ciclo.
- Si sceglie **SAX** quando il documento è molto grande, o quando basta un passaggio in avanti per estrarre ciò che serve (contare, sommare, filtrare). Non si modifica nulla: è sola lettura. Il prezzo è la gestione dello stato con i flag.

Se un esercizio chiede di *modificare* il documento (aggiungere un nodo, cambiare un valore), la risposta è DOM. Se chiede di leggere «senza caricare tutto in memoria», la risposta è SAX.

---

## 20.7 Altre librerie

Oltre a DOM e SAX del JDK esistono librerie esterne per lavorare con XML: **JDOM** (una variante di DOM, più vicina allo stile della programmazione a oggetti), **DOM4J** (simile a JDOM, con più funzionalità), e **JAXB** (*Java Architecture for XML Binding*, che associa un documento XML a classi Java specifiche, in modo da leggere, scrivere e manipolare documenti validi). Non fanno parte del JDK e non servono per l'esame: ne basta conoscere i nomi.

---

## 20.8 Dalla traccia al codice

Quando una traccia chiede di elaborare un documento XML, le sue espressioni corrispondono a scelte precise nel codice. La tabella ricapitola i nomi che **vanno scritti al carattere**, perché un nome inventato per analogia è un errore di compilazione.

| La traccia (o il programma) vuole… | Si scrive esattamente… | Attenzione |
|---|---|---|
| ottenere la fabbrica | `DocumentBuilderFactory.newInstance()` | `newInstance` con la **n**; è `static` |
| ottenere il parser DOM | `fabbrica.newDocumentBuilder()` | dichiara `ParserConfigurationException` |
| leggere un file | `builder.parse(new File("a.xml"))` | restituisce un `Document`; dichiara `SAXException` e `IOException` |
| l'elemento radice | `doc.getDocumentElement()` | **singolare**; poi `.normalize()` |
| tutti i tag con un nome | `doc.getElementsByTagName("prodotto")` | `Elements` plurale, `By` con la maiuscola; restituisce una `NodeList` |
| la lunghezza della lista | `lista.getLength()` | **metodo** con le parentesi: né `length` né `size()` |
| l'elemento i-esimo | `lista.item(i)` | `item`, non `items` né `get`; restituisce un `Node` |
| passare da `Node` a `Element` | `(Element) nodo` | cast a `Element` (singolare) |
| un attributo | `e.getAttribute("codice")` | `String`, vuota se manca |
| il testo di un elemento | `e.getTextContent()` | non `getTextContext`, non `getText` |
| il nome del tag | `e.getTagName()` oppure `e.getNodeName()` | non `getName()`: non esiste |
| il tipo del nodo | `n.getNodeType() == Node.ELEMENT_NODE` | per saltare i nodi di testo |
| creare un elemento | `doc.createElement("x")` | il metodo è del `Document`, non dell'`Element` |
| creare un testo | `doc.createTextNode("t")` | e poi `appendChild` |
| ottenere la fabbrica SAX | `SAXParserFactory.newInstance()` | |
| leggere con SAX | `parser.parse(new File("a.xml"), gestore)` | il gestore estende `DefaultHandler` |
| l'attributo in SAX | `atts.getValue("codice")` | `null` se manca |

Due raccomandazioni di metodo. La prima: prima di scrivere, decidere **DOM o SAX** dalle parole della traccia (paragrafo 20.6). La seconda: la struttura dell'esercizio è quasi sempre la stessa, in questo ordine, e conviene scriverla di seguito senza pensarci: *fabbrica, builder, `parse`, lista per tag, ciclo, cast a `Element`, lettura di attributi e testo, conversione in numero, oggetto, aggiunta alla lista, `return`*.

---

## Scheletri da esame

Questi frammenti sono i minimi da saper scrivere a memoria su un editor senza aiuti. Ciascuno compila così com'è. Gli scheletri 1-4 usano questo documento, `corsi.xml`:

```xml
<corsi>
  <corso id="1"><titolo>Fisica</titolo><ore>60</ore></corso>
  <corso id="2"><titolo>Chimica</titolo><ore>45</ore></corso>
</corsi>
```

### Scheletro 1 — Caricare un documento con DOM e leggere gli elementi per tag

**Quando si usa.** «Carica il documento XML e stampa/leggi gli elementi».

```java
import java.io.File;
import java.io.IOException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class LeggiCorsi {
    public static void main(String[] args)
            throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document doc = builder.parse(new File("corsi.xml"));      // l'albero in memoria
        NodeList corsi = doc.getElementsByTagName("corso");       // tutti i <corso>
        for (int i = 0; i < corsi.getLength(); i++) {             // getLength() con le parentesi
            Element c = (Element) corsi.item(i);                  // item(i) e cast a Element
            String id = c.getAttribute("id");                     // attributo: String
            String titolo = c.getElementsByTagName("titolo").item(0).getTextContent();
            System.out.println(id + ": " + titolo);
        }
    }
}
```

```text
1: Fisica
2: Chimica
```

**Eccezioni e import.** Nove `import`, da quattro gruppi: `java.io` (`File`, `IOException`), `javax.xml.parsers` (`DocumentBuilder`, `DocumentBuilderFactory`, `ParserConfigurationException`), `org.w3c.dom` (`Document`, `Element`, `NodeList`) e `org.xml.sax` (`SAXException`). Le tre eccezioni controllate sono dichiarate con `throws`.

### Scheletro 2 — Un metodo che restituisce una lista di oggetti, `null` se fallisce

**Quando si usa.** «Il metodo carica il file e restituisce la lista; in caso di errore restituisce `null`». La firma non ha `throws`: le eccezioni si catturano dentro.

```java
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

class Corso {
    private int id;
    private String titolo;
    private int ore;

    public Corso(int id, String titolo, int ore) {
        this.id = id;
        this.titolo = titolo;
        this.ore = ore;
    }

    public String toString() {
        return id + " " + titolo + " " + ore;
    }
}

public class CaricaCorsi {
    public static List<Corso> carica(String nomeFile) {
        try {
            DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
            Document doc = builder.parse(new File(nomeFile));
            List<Corso> lista = new ArrayList<Corso>();
            NodeList nodi = doc.getElementsByTagName("corso");
            for (int i = 0; i < nodi.getLength(); i++) {
                Element e = (Element) nodi.item(i);
                int id = Integer.parseInt(e.getAttribute("id"));          // attributo -> int
                String titolo = e.getElementsByTagName("titolo").item(0).getTextContent();
                int ore = Integer.parseInt(
                        e.getElementsByTagName("ore").item(0).getTextContent());
                lista.add(new Corso(id, titolo, ore));
            }
            return lista;
        } catch (ParserConfigurationException e) {
            return null;
        } catch (SAXException e) {
            return null;
        } catch (IOException e) {
            return null;
        }
    }
}
```

**Eccezioni e import.** Undici `import`. Tre `catch` separati, uno per ogni eccezione controllata. `Integer.parseInt` può lanciare `NumberFormatException`, **non controllata**: non è tra i `catch` perché la traccia parla di fallimento della lettura, ma se la traccia chiede di coprire anche i valori non numerici va aggiunto un `catch (NumberFormatException e)`.

### Scheletro 3 — Un documento in una stringa, con elementi senza contenuto

**Quando si usa.** Il testo XML è già in una `String` (per esempio una costante nella traccia). Un elemento senza figli e senza testo si può scrivere con un solo tag, `<riga .../>`.

```java
import java.io.IOException;
import java.io.StringReader;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

public class LeggiOrdine {
    public static int totaleQuantita(String xml)
            throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xml)));   // testo, non indirizzo
        NodeList righe = doc.getElementsByTagName("riga");
        int totale = 0;
        for (int i = 0; i < righe.getLength(); i++) {
            Element r = (Element) righe.item(i);
            totale = totale + Integer.parseInt(r.getAttribute("quantita"));
        }
        return totale;
    }

    public static void main(String[] args) throws Exception {
        String xml = "<ordine><riga articolo=\"matita\" quantita=\"3\"/>"
                   + "<riga articolo=\"penna\" quantita=\"4\"/></ordine>";
        System.out.println(totaleQuantita(xml));
    }
}
```

```text
7
```

**Eccezioni e import.** Dieci `import`, tra cui `StringReader` (da `java.io`) e `InputSource` (da `org.xml.sax`). Il documento passa per `parse(InputSource)`, non per `parse(String)`, che vuole un indirizzo.

### Scheletro 4 — Costruire un documento DOM e salvarlo su file

**Quando si usa.** «Crea un documento XML con questi dati e salvalo».

```java
import java.io.File;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class ScriviCorsi {
    public static void scrivi(String[] titoli, String nomeFile)
            throws ParserConfigurationException, TransformerException {
        Document doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().newDocument();
        Element radice = doc.createElement("corsi");
        doc.appendChild(radice);                                       // radice collegata al documento
        for (int i = 0; i < titoli.length; i++) {
            Element corso = doc.createElement("corso");
            corso.setAttribute("id", String.valueOf(i + 1));
            Element titolo = doc.createElement("titolo");
            titolo.appendChild(doc.createTextNode(titoli[i]));         // il testo e' un nodo figlio
            corso.appendChild(titolo);
            radice.appendChild(corso);
        }
        Transformer t = TransformerFactory.newInstance().newTransformer();
        t.transform(new DOMSource(doc), new StreamResult(new File(nomeFile)));
    }
}
```

**Eccezioni e import.** Dieci `import`. Due eccezioni controllate: `ParserConfigurationException` (da `newDocumentBuilder()`) e `TransformerException` (da `transform`). `appendChild` e `setAttribute` dichiarano `DOMException`, non controllata.

### Scheletro 5 — Un gestore SAX con i flag

**Quando si usa.** «Leggi il documento con SAX» o «senza caricarlo tutto in memoria».

```java
import java.io.File;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

class HandlerCorsi extends DefaultHandler {
    private boolean inTitolo = false;                    // flag: siamo dentro <titolo>
    private String id = "";
    private String titolo = "";

    @Override
    public void startElement(String uri, String localName, String qName, Attributes atts) {
        if (qName.equals("corso")) {
            id = atts.getValue("id");                    // attributo, solo qui
        }
        if (qName.equals("titolo")) {
            inTitolo = true;
            titolo = "";                                 // azzera prima di accumulare
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        if (inTitolo) {
            titolo = titolo + new String(ch, start, length);   // accumula, non sostituisce
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.equals("titolo")) {
            inTitolo = false;                            // spegne il flag
        }
        if (qName.equals("corso")) {
            System.out.println(id + ": " + titolo);      // il corso e' completo
        }
    }
}

public class LeggiCorsiSax {
    public static void main(String[] args) throws Exception {
        SAXParser parser = SAXParserFactory.newInstance().newSAXParser();
        parser.parse(new File("corsi.xml"), new HandlerCorsi());
    }
}
```

```text
1: Fisica
2: Chimica
```

**Eccezioni e import.** Cinque `import`. Confronto sempre su `qName`. `@Override` facoltativo, ma se la firma è sbagliata il compilatore lo segnala. `main` dichiara `throws Exception` per brevità (le vere sono `ParserConfigurationException`, `SAXException`, `IOException`).

---

## Errori tipici

> [!CAUTION]
> **Errore tipico — Nomi di metodi inventati per analogia**
> ```java
> // ERRORE di compilazione: nessuno di questi metodi esiste
> DocumentBuilderFactory f = DocumentBuilderFactory.newIstance();      // newInstance
> NodeList l = doc.getElementByTagName("corso");                        // getElementsByTagName
> String s = e.getTextContext();                                        // getTextContent
> Node n = l.items(0);                                                  // item
> String t = e.getName();                                               // getTagName / getNodeName
> Element r = doc.getDocumentElements();                                // getDocumentElement
> ```
> Ogni riga produce `error: cannot find symbol`, e un errore di compilazione consuma comunque un'esecuzione. I nomi vanno memorizzati al carattere (tabella del paragrafo 20.8): `newInstance` con la **n**, `getElementsByTagName` con `Elements` plurale e `By` maiuscola, `getTextContent`, `item`, `getTagName`, `getDocumentElement` singolare.

> [!CAUTION]
> **Errore tipico — `length` o `size()` su una `NodeList`**
> ```java
> // ERRORE di compilazione
> for (int i = 0; i < corsi.length; i++) { ... }        // length e' degli array
> for (int i = 0; i < corsi.size(); i++) { ... }        // size() e' delle List
> ```
> `NodeList` non è un array né una `List`: ha il solo metodo `getLength()` (`error: cannot find symbol`). Forma corretta: `corsi.getLength()`, con le parentesi, e `corsi.item(i)` per l'elemento.

> [!CAUTION]
> **Errore tipico — Eccezioni controllate non gestite**
> ```java
> // ERRORE di compilazione
> public static void main(String[] args) {
>     DocumentBuilder b = DocumentBuilderFactory.newInstance().newDocumentBuilder();
>     Document d = b.parse(new File("corsi.xml"));
> }
> ```
> Il compilatore segnala `error: unreported exception ParserConfigurationException; must be caught or declared to be thrown` e, corretto quello, `unreported exception SAXException` e `IOException`. Sono tre eccezioni controllate. Forma corretta: `throws ParserConfigurationException, SAXException, IOException` sul metodo, oppure tre `catch` (o `catch (Exception e)`) se la firma non ha `throws`.

> [!CAUTION]
> **Errore tipico — Chiamare un metodo di `Element` su un `Node`**
> ```java
> // ERRORE di compilazione: item restituisce Node
> String id = corsi.item(i).getAttribute("id");
> ```
> `item(i)` restituisce un `Node`, e `getAttribute` è un metodo di `Element` (`error: cannot find symbol`). Forma corretta: il cast, `((Element) corsi.item(i)).getAttribute("id")`, oppure `Element c = (Element) corsi.item(i); c.getAttribute("id")`.

> [!CAUTION]
> **Errore tipico — Trattare ogni figlio come un elemento**
> ```java
> // ERRORE a runtime: i figli includono i nodi di testo (spazi, a capo)
> NodeList figli = doc.getDocumentElement().getChildNodes();
> for (int i = 0; i < figli.getLength(); i++) {
>     Element c = (Element) figli.item(i);              // ClassCastException al primo giro
> }
> ```
> In un file indentato, tra un elemento e il successivo c'è un nodo di testo con gli spazi (paragrafo 20.4.4). Il cast di un nodo di testo a `Element` lancia `ClassCastException`. Forma corretta: usare `getElementsByTagName("corso")`, oppure filtrare i nodi con `getNodeType() == Node.ELEMENT_NODE` prima del cast.

> [!CAUTION]
> **Errore tipico — `getNodeValue()` su un elemento**
> ```java
> // ERRORE logico: stampa "null"
> Element titolo = (Element) c.getElementsByTagName("titolo").item(0);
> System.out.println(titolo.getNodeValue());          // null
> ```
> Il valore di un `Element` è `null` (tabella del paragrafo 20.4.1): il testo è un nodo figlio. Forma corretta: `titolo.getTextContent()`, oppure `titolo.getFirstChild().getNodeValue()`.

> [!CAUTION]
> **Errore tipico — Passare il testo XML a `parse(String)`**
> ```java
> // ERRORE a runtime: parse(String) vuole un indirizzo
> Document d = builder.parse("<a>testo</a>");
> ```
> Il programma compila ma lancia `java.net.MalformedURLException: no protocol: <a>testo</a>`, perché la stringa è interpretata come indirizzo da aprire. Forma corretta: `builder.parse(new InputSource(new StringReader(xml)))`.

> [!CAUTION]
> **Errore tipico — Dimenticare che `getAttribute` restituisce una stringa, vuota se manca**
> ```java
> // ERRORE a runtime se l'attributo non c'e' o ha un altro nome
> int id = Integer.parseInt(e.getAttribute("codice"));      // l'attributo si chiama "id"
> ```
> `getAttribute` con un nome inesistente restituisce `""` senza lanciare nulla, e `Integer.parseInt("")` lancia `java.lang.NumberFormatException: For input string: ""`. Forma corretta: il nome esatto dell'attributo come scritto nel documento (le maiuscole contano), e la conversione `Integer.parseInt(...)` o `Double.parseDouble(...)` perché il valore è sempre una `String`.

> [!CAUTION]
> **Errore tipico — Creare un nodo e non collegarlo**
> ```java
> // ERRORE logico: l'elemento esiste ma non fa parte del documento
> Element extra = doc.createElement("extra");
> // manca radice.appendChild(extra);
> ```
> `createElement` crea il nodo ma non lo inserisce nell'albero: `doc.getElementsByTagName("extra").getLength()` vale `0` (verificato). Forma corretta: `radice.appendChild(extra)`.

> [!CAUTION]
> **Errore tipico — SAX: confronto su `localName`**
> ```java
> // ERRORE logico: con la configurazione predefinita localName e' ""
> public void startElement(String uri, String localName, String qName, Attributes atts) {
>     if (localName.equals("corso")) { ... }        // mai vero
> }
> ```
> Il parser non tratta i namespace, e `localName` è la stringa vuota (paragrafo 20.5.5): l'`if` non scatta mai e il programma non stampa nulla. Forma corretta: `qName.equals("corso")`.

> [!CAUTION]
> **Errore tipico — SAX: firma sbagliata del metodo da riscrivere**
> ```java
> // ERRORE di compilazione con @Override; senza, il metodo non viene mai chiamato
> @Override
> public void startElement(String uri, String qName, Attributes atts) { ... }
> ```
> Manca un parametro: non è una riscrittura di `startElement`. Con `@Override` il compilatore dice `error: method does not override or implement a method from a supertype`; senza `@Override` il metodo è un overload e il parser continua a chiamare quello vuoto, senza alcun errore. Forma corretta: `startElement(String uri, String localName, String qName, Attributes atts)`.

> [!CAUTION]
> **Errore tipico — SAX: testo letto fuori dai flag, o flag mai spento**
> ```java
> // ERRORE logico: characters riceve anche gli spazi tra i tag
> public void characters(char[] ch, int start, int length) {
>     titolo = new String(ch, start, length);        // senza controllare il flag
> }
> ```
> `characters` viene chiamato per **tutto** il testo, compresi gli spazi e gli a capo tra un tag e l'altro: senza il flag `inTitolo`, `titolo` viene sovrascritto da quegli spazi. Allo stesso modo, un flag acceso in `startElement` e **mai spento** in `endElement` raccoglie anche il testo degli elementi seguenti. Forma corretta: flag acceso all'apertura, spento alla chiusura, e `characters` che accumula solo quando il flag è acceso.

> [!CAUTION]
> **Errore tipico — Documento non ben formato**
> ```text
> org.xml.sax.SAXParseException: The element type "b" must be terminated by the matching end-tag "</b>".
> ```
> Un tag non chiuso, una chiusura nell'ordine sbagliato, un `&` non scritto come `&amp;`, un file vuoto (`Premature end of file.`): il parser si rifiuta di proseguire e lancia `SAXParseException`, che è una `SAXException`. Il parser predefinito stampa inoltre `[Fatal Error]` su `System.err`. La correzione è nel documento, non nel codice.

> [!CAUTION]
> **Errore tipico — File non trovato**
> ```text
> java.io.FileNotFoundException: .../corsi.xml (No such file or directory)
> ```
> `new File("corsi.xml")` è un percorso **relativo alla cartella da cui si lancia il programma** ([Capitolo 14](14-file-di-testo.md), sezione 14.5). Se il file è altrove, `parse` lancia `FileNotFoundException`, una `IOException`. Forma corretta: avviare il programma dalla cartella giusta, o indicare un percorso completo.

> [!CAUTION]
> **Errore tipico — `import` mancanti**
> ```java
> // ERRORE di compilazione: solo org.w3c.dom e' importato
> import org.w3c.dom.*;
> public class Prova {
>     DocumentBuilder b;       // cannot find symbol
> }
> ```
> `DocumentBuilder` e `DocumentBuilderFactory` sono in `javax.xml.parsers`, `SAXException` in `org.xml.sax`, `File` e `IOException` in `java.io`: ogni gruppo ha il suo `import`. Forma corretta: un `import` per ciascuna classe usata, come negli scheletri.

---

## Riassunto

Un documento **XML** è un testo strutturato: **elementi** annidati (`<nome>...</nome>`) con **attributi** (`codice="A10"`) e **testo**, con una sola **radice**; se rispetta le regole è **ben formato**. Un **parser** lo scompone e ne controlla la forma. Java ne mette a disposizione due modelli tramite **JAXP**: **DOM** costruisce in memoria un **albero di nodi** (`Document`, `Element`, `Attr`, `Text`) che si può navigare e modificare liberamente, a prezzo della memoria; **SAX** percorre il documento una volta sola e **chiama** i metodi di un gestore (`startElement`, `characters`, `endElement`), a prezzo di dover ricordare lo stato con dei flag. Entrambi si ottengono da una **fabbrica** (`DocumentBuilderFactory.newInstance()`, `SAXParserFactory.newInstance()`). Con DOM la sequenza è sempre la stessa: fabbrica, `DocumentBuilder`, `parse(File)`, `getElementsByTagName`, ciclo su `NodeList` con `getLength()` e `item(i)`, cast a `Element`, lettura di `getAttribute` e `getTextContent`. Le eccezioni dei parser sono **controllate** e vanno dichiarate o catturate; i nomi dei metodi vanno scritti al carattere.

**Concetti chiave**

- **Documento ben formato**: una radice, tag chiusi e annidati correttamente, attributi tra virgolette, `&` scritto `&amp;`. Un documento malformato lancia `SAXParseException`.
- **Parser e JAXP**: scompone e controlla il documento; i package sono `javax.xml.parsers`, `org.w3c.dom`, `org.xml.sax`, `org.xml.sax.helpers`.
- **Pattern factory**: `newInstance()` è `static` e restituisce la fabbrica; la fabbrica produce `DocumentBuilder` o `SAXParser`.
- **DOM**: l'intero documento diventa un albero in memoria; navigazione libera, modifica possibile, memoria alta.
- **SAX**: eventi a callback, una sola passata in avanti, sola lettura, memoria minima.
- **Nodi**: il testo è un nodo `Text` figlio dell'elemento; `getNodeValue()` di un `Element` è `null`.
- **`getElementsByTagName`**: restituisce una `NodeList` di elementi, ignorando i nodi di spazi; `getChildNodes()` invece include anche i nodi `#text`.
- **`NodeList`**: `getLength()` e `item(int)`, non una `List`.
- **Lettura**: `getAttribute` (stringa, vuota se manca) e `getTextContent`; il testo si converte con `parseInt` o `parseDouble`.
- **Costruzione**: `createElement`, `createTextNode`, `setAttribute`, `appendChild`; un nodo creato va collegato. Il salvataggio passa per `Transformer`.
- **Gestore SAX**: estende `DefaultHandler`, riscrive con la firma esatta `startElement`, `characters`, `endElement`; flag acceso e spento; `characters` si accumula; si confronta `qName`.
- **Scelta**: DOM per documenti piccoli e per modificare; SAX per documenti grandi e letture sequenziali.

**API essenziali**

| Classe | Elemento | Firma | Eccezioni |
|---|---|---|---|
| `DocumentBuilderFactory` | `newInstance` | `public static DocumentBuilderFactory newInstance()` | — |
| `DocumentBuilderFactory` | `newDocumentBuilder` | `public abstract DocumentBuilder newDocumentBuilder() throws ParserConfigurationException` | `ParserConfigurationException` |
| `DocumentBuilder` | `parse` | `public Document parse(File f)` / `parse(InputStream is)` / `parse(InputSource is)` / `parse(String uri)` | `SAXException`, `IOException` |
| `DocumentBuilder` | `newDocument` | `public abstract Document newDocument()` | — |
| `Document` | `getDocumentElement` | `Element getDocumentElement()` | — |
| `Document` / `Element` | `getElementsByTagName` | `NodeList getElementsByTagName(String name)` | — |
| `Document` | `createElement` | `Element createElement(String tagName) throws DOMException` | `DOMException` (non controllata) |
| `Document` | `createTextNode` | `Text createTextNode(String data)` | — |
| `NodeList` | `getLength`, `item` | `int getLength()`, `Node item(int index)` | — |
| `Node` | `getTextContent`, `getNodeValue` | `String getTextContent()`, `String getNodeValue()` | `DOMException` |
| `Node` | `appendChild`, `removeChild` | `Node appendChild(Node newChild)`, `Node removeChild(Node oldChild)` | `DOMException` |
| `Node` | `getNodeType`, `getNodeName` | `short getNodeType()`, `String getNodeName()` | — |
| `Element` | `getAttribute`, `setAttribute` | `String getAttribute(String name)`, `void setAttribute(String name, String value)` | `DOMException` (`setAttribute`) |
| `SAXParserFactory` | `newSAXParser` | `public abstract SAXParser newSAXParser() throws ParserConfigurationException, SAXException` | `ParserConfigurationException`, `SAXException` |
| `SAXParser` | `parse` | `public void parse(File f, DefaultHandler dh) throws SAXException, IOException` | `SAXException`, `IOException` |
| `DefaultHandler` | `startElement` | `public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException` | `SAXException` |
| `DefaultHandler` | `characters` | `public void characters(char[] ch, int start, int length) throws SAXException` | `SAXException` |
| `DefaultHandler` | `endElement` | `public void endElement(String uri, String localName, String qName) throws SAXException` | `SAXException` |
| `Attributes` | `getValue` | `String getValue(String qName)` | — (`null` se manca) |
| `TransformerFactory` / `Transformer` | `newTransformer`, `transform` | `Transformer newTransformer()`, `void transform(Source xmlSource, Result outputTarget)` | `TransformerConfigurationException`, `TransformerException` |
