# Livello 6: Java in Rete e Manipolazione XML

## 1. Java Networking: Comunicazione Client-Server

### Basi del Networking: Le Classi "Eroe"
Prima di implementare un sistema distribuito in Java, è essenziale comprendere le coordinate che permettono a due programmi di trovarsi e parlare attraverso una rete. Per semplificare un argomento così complesso, usiamo delle metafore quotidiane per descrivere le classi fondamentali del pacchetto `java.net`.

#### Il Protocollo TCP (La Telefonata Sicura)
Il TCP è orientato alla connessione: garantisce che i dati arrivino integri e nello stesso ordine.
1.  **`ServerSocket` (Il Centralinista):** Immaginalo come un centralinista seduto in un ufficio. Non chiama nessuno, resta solo in attesa che il telefono squilli sulla sua scrivania (la **Porta** di rete). Il suo unico compito è rispondere (metodo `accept()`) e "passare la chiamata" creando un canale dedicato.
2.  **`Socket` (Il Telefono):** È il dispositivo con cui parliamo fisicamente. Una volta stabilita la connessione, sia il Client che il Server usano un oggetto `Socket` per scambiarsi flussi di dati usando gli Stream di I/O (microfono e altoparlante).

#### Il Protocollo UDP (L'Aeroplanino di Carta / Posta Rapida)
L'UDP non ha connessione: è veloce ma non garantisce che il messaggio arrivi a destinazione.
1.  **`DatagramSocket` (La Cassetta delle Lettere):** Non c'è una chiamata attiva. È solo una fessura dove puoi imbucare buste (pacchetti) o riceverle. Non sai se il destinatario è in casa o se leggerà mai il messaggio.
2.  **`DatagramPacket` (La Busta):** Contiene i dati (un array di byte) e l'indirizzo scritto sopra (IP e Porta). Senza la "busta", non puoi spedire nulla con UDP.

---

### Implementazione TCP: Esempi di Connessione e Scambio Dati

#### Caso A: Connessione Semplice (Solo "Bussare")
In questo scenario, il Client si limita a stabilire il contatto e il Server lo rileva. Non c'è scambio di testi.

```java
// LATO SERVER (Il Centralinista)
// Apre l'ufficio sulla porta 5000
ServerSocket centralino = new ServerSocket(5000); 
System.out.println("In attesa di chiamate...");

// Il programma si blocca qui finché qualcuno non bussa
Socket chiamata = centralino.accept(); 
System.out.println("Qualcuno ha chiamato!");
chiamata.close();

// LATO CLIENT (Il Chiamante)
// Chiama il numero 5000 all'indirizzo locale
Socket telefono = new Socket("localhost", 5000); 
System.out.println("Ho effettuato la chiamata al server.");
telefono.close();
```

#### Caso B: Scambio di Informazioni (Botta e Risposta)
Qui usiamo i decoratori `PrintWriter` e `BufferedReader` per inviare e leggere testo.

```java
// LATO SERVER: Riceve un messaggio e risponde
try (ServerSocket server = new ServerSocket(5000);
     Socket client = server.accept();
     // autoFlush=true nel PrintWriter assicura che il messaggio parta subito
     PrintWriter out = new PrintWriter(client.getOutputStream(), true);
     BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()))) {
    
    // Ascolta cosa dice il client
    String messaggioRicevuto = in.readLine(); 
    System.out.println("Il client dice: " + messaggioRicevuto);
    
    // Risponde al client
    out.println("Ciao Client! Ho ricevuto forte e chiaro!"); 
}

// LATO CLIENT: Invia un messaggio e aspetta la risposta
try (Socket socket = new Socket("localhost", 5000);
     PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
     BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
    
    // Parla per primo
    out.println("Buongiorno Server!"); 
    
    // Si blocca in attesa della risposta del Server
    String risposta = in.readLine(); 
    System.out.println("Risposta del server: " + risposta);
}
```

---

### Implementazione UDP: Esempi di Invio Rapido

L'UDP non usa Stream (flussi), ma lavora direttamente con i **byte**. Non ci sono `BufferedReader` o `PrintWriter`.

#### Invio di un Segnale Rapido
```java
// RICEVITORE (Server UDP)
try (DatagramSocket cassetta = new DatagramSocket(6000)) {
    // Prepara un sacco vuoto per la posta in arrivo
    byte[] buffer = new byte[1024]; 
    DatagramPacket bustaInArrivo = new DatagramPacket(buffer, buffer.length);
    
    System.out.println("In attesa di posta...");
    // Aspetta che cada una busta nella cassetta
    cassetta.receive(bustaInArrivo); 
    
    // Estrae il testo dai byte ricevuti
    String messaggio = new String(bustaInArrivo.getData(), 0, bustaInArrivo.getLength());
    System.out.println("Posta ricevuta: " + messaggio);
}

// MITTENTE (Client UDP)
try (DatagramSocket cassetta = new DatagramSocket()) {
    String testo = "Avviso UDP veloce!";
    // Trasformiamo il testo in byte (formato obbligatorio per UDP)
    byte[] dati = testo.getBytes(); 
    
    // Prepariamo la busta scrivendoci sopra i dati, l'IP e la porta del destinatario
    DatagramPacket bustaDaSpedire = new DatagramPacket(dati, dati.length, 
                                              InetAddress.getByName("localhost"), 6000);
    
    // Spediamo la busta nel vuoto (fire-and-forget)
    cassetta.send(bustaDaSpedire); 
    System.out.println("Segnale inviato.");
}
```

---

### Tabella Comparativa: TCP vs UDP

| Caratteristica | TCP (La Telefonata) | UDP (L'Aeroplanino) |
| :--- | :--- | :--- |
| **Protocollo** | Orientato alla connessione | Senza connessione (Stateless) |
| **Affidabilità** | Alta (ritrasmette i dati persi) | Bassa (best-effort) |
| **Ordine** | Garantito | Casuale |
| **Velocità** | Minore (overhead di controllo) | Massima (leggero e rapido) |
| **Uso ideale** | File, Email, Chat, Web | Video streaming, Gaming online, VoIP |

---

### La Classe `URL` e `HttpURLConnection`: Interfacciarsi con il Web e API REST
Oltre ai Socket a basso livello, Java fornisce la classe `java.net.URL` e la sua evoluzione `java.net.HttpURLConnection` per interagire con risorse Web e servizi **RESTful**.

Mentre `URL.openStream()` è sufficiente per scaricare il contenuto grezzo di una pagina, `HttpURLConnection` è lo strumento necessario per gestire richieste moderne. Esso permette di impostare i metodi HTTP (GET, POST, PUT, DELETE), gestire gli Header (come il `Content-Type`) e, soprattutto, analizzare i **Codici di Stato HTTP**.

#### I Codici di Stato HTTP (Status Codes)
Nelle architetture REST, il server comunica l'esito della richiesta tramite un codice numerico. Saperli interpretare è vitale per gestire i diversi scenari di errore:
-   **2xx (Successo):** Es. `200 OK` (operazione riuscita), `201 Created` (risorsa creata con successo).
-   **3xx (Redirezione):** Es. `301 Moved Permanently` (l'indirizzo è cambiato).
-   **4xx (Errore Client):** Es. `400 Bad Request` (sintassi errata), `401 Unauthorized` (mancano le credenziali), `404 Not Found` (la risorsa non esiste).
-   **5xx (Errore Server):** Es. `500 Internal Server Error` (il server è andato in crash).

#### Gestione Avanzata degli Errori
Un client robusto verifica sempre il `ResponseCode` prima di tentare la lettura dei dati. Se il server restituisce un errore, il flusso di dati standard (`getInputStream`) viene chiuso e l'eventuale spiegazione dell'errore (es. un JSON che spiega perché il login è fallito) viene spostata nel cosiddetto **Error Stream**.

*Esempio: Richiesta API con gestione dei casi d'errore*
```java
import java.io.*;
import java.net.*;
import java.util.Scanner;

public class ClientRestEvoluto {
    public static void main(String[] args) {
        try {
            URL url = new URL("https://api.esempio.it/dati");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(5000); // Timeout di 5 secondi

            int status = conn.getResponseCode();
            
            if (status == HttpURLConnection.HTTP_OK) { // Caso 200
                try (Scanner sc = new Scanner(conn.getInputStream())) {
                    System.out.println("Dati Ricevuti:");
                    while (sc.hasNextLine()) System.out.println(sc.nextLine());
                }
            } 
            else if (status == HttpURLConnection.HTTP_NOT_FOUND) { // Caso 404
                System.err.println("[ERRORE 404] La risorsa richiesta è inesistente.");
            } 
            else if (status >= 500) { // Caso 5xx
                System.err.println("[ERRORE SERVER] Il sistema remoto è temporaneamente fuori servizio.");
            } 
            else {
                // Lettura del messaggio di errore dettagliato dal server tramite getErrorStream()
                try (Scanner errSc = new Scanner(conn.getErrorStream())) {
                    System.err.print("Errore generico (" + status + "): ");
                    while (errSc.hasNextLine()) System.err.println(errSc.nextLine());
                }
            }
            conn.disconnect();
            
        } catch (SocketTimeoutException e) {
            System.err.println("Errore: Il server non ha risposto in tempo.");
        } catch (IOException e) {
            System.err.println("Errore di connessione o URL errato.");
        }
    }
}
```

---

## 2. Elaborazione XML in Java: SAX e DOM

### Teoria Avanzata: Il Conflitto tra Memoria e Navigazione
Scegliere tra SAX e DOM non è una questione di preferenza, ma di **ingegneria dei dati**. In Java, entrambi passano per **JAXP (Java API for XML Processing)**, un layer che isola il programmatore dal parser specifico (es. Apache Xerces).

- **SAX (Simple API for XML)**: È un parser **Push**. È il parser che "spinge" i dati verso la tua applicazione man mano che li legge. Non puoi fermarlo, non puoi tornare indietro. È perfetto per flussi di dati (streaming).
- **DOM (Document Object Model)**: È un parser **Object-based**. Trasforma il testo in un albero di oggetti. È l'ideale quando devi modificare il file (aggiungere nodi) o quando le informazioni sono correlate tra loro in punti diversi del documento.

---

### Lo Standard SAX: L'algoritmo basato su Eventi
L'implementazione di SAX richiede la creazione di un **Handler** (un ricettore). Il segreto per un'estrazione dati corretta in SAX è l'uso di uno **Stato** (booleani) e di un **Accumulatore** (`StringBuilder`).

#### Classi e Metodi Essenziali (SAX)
- `SAXParserFactory`: La fabbrica che genera il parser.
- `SAXParser`: Il motore che esegue la scansione.
- `DefaultHandler`: La classe base da estendere per ricevere gli eventi.
- **Metodi Callback:**
    - `startElement(...)`: Chiamato all'apertura del tag (es. `<studente>`). Qui si leggono gli **Attributi**.
    - `characters(...)`: Chiamato per il testo. **Attenzione:** Può essere chiamato più volte per lo stesso tag!
    - `endElement(...)`: Chiamato alla chiusura (es. `</studente>`). Qui si salvano i dati accumulati.

#### Algoritmo di Estrazione Dati (SAX)
```java
public class MioHandler extends DefaultHandler {
    private StringBuilder buffer = new StringBuilder();
    private Persona p;

    @Override
    public void startElement(String uri, String localName, String qName, Attributes atts) {
        buffer.setLength(0); // Svuota il buffer per il nuovo testo
        if (qName.equals("persona")) {
            p = new Persona();
            p.setId(atts.getValue("id")); // Legge l'attributo
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        buffer.append(ch, start, length); // Accumula i frammenti di testo
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.equals("nome")) p.setNome(buffer.toString());
        if (qName.equals("persona")) lista.add(p); // Oggetto completo
    }
}
```

---

### Lo Standard DOM: L'approccio ad Albero (Document Object Model)
A differenza di SAX, il DOM non si limita a leggere: esso **ricostruisce**. Immagina di smontare un mobile e rimontarlo identico dentro la tua RAM. Una volta completato il parsing, l'intero file XML esiste nella memoria Heap come una gerarchia di oggetti legati tra loro.

#### La Gerarchia dei Nodi
Nel DOM, tutto è un **Nodo** (`org.w3c.dom.Node`). Esistono 12 tipi di nodi, ma i più importanti per un programmatore Java sono:
1.  **Document**: La radice dell'albero, il punto di partenza per ogni ricerca.
2.  **Element**: Rappresenta i tag (es. `<studente>`). Può avere figli e attributi.
3.  **Attr**: Rappresenta un attributo (es. `id="101"`).
4.  **Text**: Contiene il testo puro all'interno dei tag. Spesso sottovalutato, è un nodo a tutti gli effetti.

#### Classi e Metodi Chiave (JAXP)
-   **`DocumentBuilderFactory`**: Il "Centro di Comando". Qui decidi se il parser deve ignorare i commenti, essere consapevole dei Namespace o validare il file tramite uno Schema/DTD.
-   **`DocumentBuilder`**: L'operaio che esegue fisicamente il `parse()`.
-   **`NodeList`**: Non è una lista Java standard (non è un'ArrayList), ma un array live di nodi. Si scorre con un indice (`item(i)`) e `.getLength()`.

#### Algoritmo di Manipolazione e Navigazione (DOM)
L'eleganza del DOM sta nella possibilità di **creare** o **modificare** il file in memoria prima di salvarlo.

```java
import javax.xml.parsers.*;
import org.w3c.dom.*;
import java.io.File;

public class GestoreDOM {
    public static void main(String[] args) throws Exception {
        // 1. Configurazione Factory
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setIgnoringComments(true); // Esempio di configurazione avanzata
        
        // 2. Costruzione dell'albero
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new File("studenti.xml"));
        
        // FONDAMENTALE: Normalizza i nodi di testo (unisce frammenti adiacenti)
        doc.getDocumentElement().normalize();

        // 3. Navigazione Selettiva
        NodeList studenti = doc.getElementsByTagName("studente");
        
        for (int i = 0; i < studenti.getLength(); i++) {
            Node nodo = studenti.item(i);
            
            if (nodo.getNodeType() == Node.ELEMENT_NODE) {
                Element studente = (Element) nodo;
                
                // Estrazione dati mirata
                String matricola = studente.getAttribute("matricola");
                String nome = studente.getElementsByTagName("nome").item(0).getTextContent();
                
                System.out.println("Matricola: " + matricola + " - Nome: " + nome);
                
                // 4. Esempio di MANIPOLAZIONE (Modifica in memoria)
                // Aggiungiamo un nuovo tag <stato> a ogni studente
                Element stato = doc.createElement("stato");
                stato.appendChild(doc.createTextNode("Attivo"));
                studente.appendChild(stato);
            }
        }
    }
}
```

---

### Quando scegliere SAX vs DOM? (In sintesi)
| Criterio | SAX | DOM |
| :--- | :--- | :--- |
| **Occupazione RAM** | Minima (indipendente dal file) | Alta (molto superiore al file) |
| **Velocità** | Elevatissima (una sola passata) | Più lenta (costruzione albero) |
| **Navigazione** | Solo in avanti (Forward-only) | Bidirezionale (Padri/Figli/Fratelli) |
| **Modifica** | Impossibile (sola lettura) | Facile (puoi aggiungere/rimuovere nodi) |
| **Complessità** | Alta (gestione manuale degli stati) | Bassa (API intuitiva ad oggetti) |

