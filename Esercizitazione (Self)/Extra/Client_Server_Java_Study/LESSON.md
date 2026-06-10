# Lezione: Architettura Client-Server in Java

## 1. Introduzione all'Architettura Client-Server
L'architettura Client-Server è un modello fondamentale nel computing distribuito. I compiti sono suddivisi tra i fornitori di una risorsa o servizio, chiamati **Server**, e i richiedenti di tale servizio, chiamati **Client**.
- **Il Server:** È un processo che attende passivamente e rimane in ascolto su uno specifico indirizzo di rete e una determinata porta, pronto a soddisfare le richieste in arrivo.
- **Il Client:** È un processo che inizia attivamente la comunicazione inviando una richiesta di connessione al Server per usufruire di un servizio.

## 2. Concetti Chiave di Rete
Per far sì che due applicazioni comunichino su una rete, è necessario definire delle coordinate precise:
- **Indirizzo IP:** È l'identificativo numerico univoco del dispositivo di rete (host) su cui è in esecuzione il programma (es. `127.0.0.1` indica "localhost", ovvero la macchina locale, o un IP pubblico in Internet).
- **Porta:** È un numero logico a 16 bit che identifica un processo o un servizio specifico all'interno di un host (es. 80 per HTTP, 8080 comunemente per test).
- **Socket:** Rappresenta l'astrazione software di un endpoint (una terminazione) di rete. È attraverso i Socket che avviene il flusso di dati bidirezionale.
- **Protocolli (TCP vs UDP):** 
  - **TCP (Transmission Control Protocol):** Orientato alla connessione, garantisce la consegna affidabile e ordinata dei dati. In Java è gestito tramite la classe `Socket`.
  - **UDP (User Datagram Protocol):** Non orientato alla connessione (datagram-based), veloce ma senza garanzie di consegna.

### 2.1 Approfondimento (Rifresco su Reti)
Se si possiede una base di networking, è utile ricordare un paio di dinamiche fondamentali che avvengono "dietro le quinte" quando realizzi algoritmi in Java tra Client-Server:
* **Three-way Handshake:** Quando in Java crei un `new Socket("ip", porta)`, a livello di sistema operativo viene iniziato l'Handshake TCP (SYN -> SYN/ACK -> ACK). Il costruttore in Java si blocca per la durata di questo scambio; se l'handshake fallisce (server irraggiungibile), viene sollevata una `ConnectException`.
* **Indirizzo di Loopback (`127.0.0.1`):** I pacchetti diretti a questo IP non raggiungono mai la scheda di rete fisica, ma vengono processati internamente dal kernel. È per questo che per i test su singola macchina (localhost) il tutto risulta estremamente rapido e protetto dai firewall esterni.
* **Buffer del SO vs Buffer Java:** I dati non partono "un carattere alla volta" verso la scheda di rete. Quando scrivi in uno Stream Java, i dati si accumulano prima in un buffer del linguaggio, per poi essere trasferiti al buffer della Socket del Sistema Operativo. Se non forzi l'invio (tramite `flush()` manuale o usando `true` nell'istanziazione di `PrintWriter`), rischi che i messaggi rimangano fermi nella memoria e l'altro endpoint rimanga bloccato in attesa.

## 3. Le Classi Java per la Rete
Il pacchetto standard per la programmazione di rete in Java è `java.net`.

### `java.net.ServerSocket` (Lato Server)
Questa classe permette al server di "mettersi in ascolto" di richieste in ingresso.
- **Creazione:** Si istanzia specificando il numero della porta su cui restare in ascolto.
- **Accettazione:** Il metodo `accept()` è bloccante: sospende l'esecuzione finché un client non si connette, restituendo poi un oggetto `Socket` dedicato a quella specifica comunicazione.

### `java.net.Socket` (Lato Client e Server)
Una volta stabilita la connessione, entrambi gli endpoint comunicano tramite oggetti `Socket`.
- Sul **Client**, il socket viene creato specificando IP e porta del Server, tentando immediatamente la connessione.
- Sul **Server**, viene restituito dal metodo `accept()`.

La comunicazione vera e propria avviene poi estraendo i **flussi di dati (Streams)** dal pacchetto `java.io`, convertendo i byte in testo tramite `BufferedReader` e `PrintWriter` (o alternativamente `Scanner` e `PrintStream`).

## 4. Esempi Pratici e Flusso di Esecuzione Sequenziale

Per comprendere esattamente "chi aspetta chi", leggi attentamente i commenti cronologici (STEP) nei due listati sottostanti. Si suppone che il Server venga avviato per primo.

### Esempio: Il Server Base

```java
import java.io.*;
import java.net.*;

public class SimpleServer {
    public static void main(String[] args) {
        int port = 8080;
        
        // STEP 1: Il Server si riserva la porta 8080 a livello di Sistema Operativo.
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Server in ascolto sulla porta " + port);
            
            // STEP 2: Il metodo accept() viene chiamato. 
            // ATTENZIONE: Il thread principale del Server si BLOCCA qui.
            // Il codice sottostante non viene eseguito finché un Client non inizia l'handshake.
            try (Socket clientSocket = serverSocket.accept(); 
                 // STEP 4: (Raggiunto solo dopo la connessione del Client). 
                 // Inizializzazione degli stream di lettura (in) e scrittura (out).
                 BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                 PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) { // "true" imposta l'autoFlush!
                 
                System.out.println("Client connesso dal seguente IP: " + clientSocket.getInetAddress());
                
                // STEP 5: Il Server si BLOCCA di nuovo su in.readLine().
                // È in attesa che il Client invii del testo e prema "Invio" (\n o \r).
                String clientMessage = in.readLine();
                
                // STEP 8: Il Server ha ricevuto il messaggio e prosegue l'esecuzione.
                System.out.println("Messaggio ricevuto dal Client: " + clientMessage);
                
                // STEP 9: Il Server scrive sullo stream di output.
                // Grazie all'autoFlush=true impostato sopra, il messaggio parte immediatamente verso il Client.
                out.println("Ciao Client, ho ricevuto il tuo messaggio!");
                
                // STEP 11: Il blocco try-with-resources termina. 
                // Il socket del Client e i flussi di rete vengono chiusi (viene inviato un FIN TCP).
            } catch (IOException e) {
                System.err.println("Errore durante la comunicazione con il client: " + e.getMessage());
            }
            
        } catch (IOException e) {
            System.err.println("Impossibile avviare il server. Porta già in uso? " + e.getMessage());
        }
    }
}
```

### Esempio: Il Client Base

```java
import java.io.*;
import java.net.*;

public class SimpleClient {
    public static void main(String[] args) {
        String host = "127.0.0.1";
        int port = 8080;
        
        // STEP 3: Il costruttore di Socket avvia l'handshake verso il Server.
        // Se il Server non sta eseguendo l'accept() sulla porta 8080, solleva ConnectException.
        try (Socket socket = new Socket(host, port);
             // Creazione dei flussi in e out speculari a quelli del Server.
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
             
            System.out.println("Connessione stabilita con il server.");
            
            // STEP 6: Il Client scrive nel flusso di output. 
            // Grazie al metodo println, viene aggiunto il carattere "A capo" che sblocca il readLine() del Server (STEP 5).
            out.println("Buongiorno, Server! Questo è un messaggio di test.");
            
            // STEP 7: Subito dopo aver inviato, il Client si BLOCCA su readLine(), 
            // in attesa di ricevere la risposta dal Server.
            String response = in.readLine();
            
            // STEP 10: Ricevuta la risposta dal Server (generata allo STEP 9), il Client si sblocca e stampa a video.
            System.out.println("Risposta dal server: " + response);
            
            // STEP 12: Il try-with-resources termina. 
            // Anche la socket del lato Client e i suoi stream vengono chiusi in modo sicuro.
        } catch (UnknownHostException e) {
            System.err.println("Host sconosciuto: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Errore di I/O (connessione rifiutata o interrotta): " + e.getMessage());
        }
    }
}
```

### 4.1 Esempio: Server e Client in UDP (Datagrammi)
A differenza del TCP, in UDP non c'è una fase di connessione iniziale bloccante. Il Client si limita a preparare un "pacco postale" (Datagramma) e a spedirlo a un indirizzo e una porta. Il Server ascolta passivamente sulla porta e legge i pacchi in arrivo, indipendentemente dal mittente. In UDP **non esistono flussi I/O (`InputStream`/`OutputStream`)**, si scambiano solo array di byte puri.

**Server UDP:**
```java
import java.net.*;

public class UDPServer {
    public static void main(String[] args) {
        int port = 9090;
        try (DatagramSocket socket = new DatagramSocket(port)) {
            System.out.println("Server UDP in ascolto sulla porta " + port);
            
            // Creiamo un buffer (array di byte) per accogliere i dati in ingresso
            byte[] buffer = new byte[1024];
            
            // Il DatagramPacket funziona come un contenitore vuoto in cui il socket scaricherà i dati
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            
            // Il Server si BLOCCA qui, attendendo che arrivi un pacchetto da un qualsiasi mittente
            socket.receive(packet);
            
            // Estraiamo la stringa dai byte ricevuti
            String receivedMessage = new String(packet.getData(), 0, packet.getLength());
            System.out.println("Ricevuto: " + receivedMessage + " da " + packet.getAddress());
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

**Client UDP:**
```java
import java.net.*;

public class UDPClient {
    public static void main(String[] args) {
        String host = "127.0.0.1";
        int port = 9090;
        
        try (DatagramSocket socket = new DatagramSocket()) { // Nessuna connessione nel costruttore!
            
            String message = "Ciao Server UDP!";
            byte[] data = message.getBytes(); // Convertiamo il testo in byte crudi
            
            InetAddress address = InetAddress.getByName(host);
            
            // Creiamo il pacco postale inserendo: dati, lunghezza, indirizzo e porta del destinatario
            DatagramPacket packet = new DatagramPacket(data, data.length, address, port);
            
            // Spediamo il pacchetto. È un'operazione "fire-and-forget" (lancia e dimentica)
            socket.send(packet);
            System.out.println("Datagramma inviato.");
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 5. Best Practices e Gestione Avanzata (Multithreading e Concorrenza)

Nella programmazione di rete le probabilità di fallimento (connessione caduta a metà invio, rete occupata, host irraggiungibile) sono alte, e Java ci costringe a gestire le *Checked Exceptions*.

- **Gestione delle Risorse:** Le risorse di rete e gli Stream consumano porte a livello hardware e file descriptor nel Kernel. Devono **sempre** essere chiuse. Il costrutto `try-with-resources` usato negli esempi sopra garantisce la chiusura automatica anche se viene sollevata un'eccezione, risolvendo storici problemi di *Resource Leak*.
- **La Trappola del "Deadlock Distribuito":** Un errore comune tra i principianti è far bloccare contemporaneamente Client e Server in lettura (`readLine()`). Se entrambi aspettano che l'altro scriva qualcosa prima di agire, il programma rimarrà congelato all'infinito. Lo scambio di dati (il Protocollo Applicativo che inventi) deve sempre definire una chiara alternanza: chi invia per primo e chi aspetta.
- **Server Concorrenti (Multithreading):** Il server dell'esempio al punto 4 è un **Server Iterativo**: gestisce un solo Client alla volta. Se l'esecuzione all'interno del blocco in cui si processa la logica impiega 10 secondi, tutti gli altri Client dovranno attendere 10 secondi in coda prima che venga chiamato un nuovo `accept()`. 
  - La **soluzione enterprise** prevede di inserire il `serverSocket.accept()` all'interno di un ciclo `while(true)`. 
  - Appena si connette un Client e si ottiene l'oggetto `Socket`, esso viene "consegnato" in input al costruttore di una nuova istanza di un `Thread` (o di un oggetto che implementa `Runnable`).
  - Questo Thread secondario prenderà in carico i flussi I/O e la comunicazione, mentre il thread principale del `main` tornerà a loopare verso l'inizio, per rimettersi istantaneamente a fare da sentinella, in ascolto (con l'`accept()`) pronto per i prossimi Client.