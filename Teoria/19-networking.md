---
materia: Programmazione a Oggetti
capitolo: 19
titolo: Networking
livello_syllabus: 6
stato: completo
slide: ["Client-Server.pdf pagine 1-26", "Savitch cap. 14 slide 55-58"]
appelli: [EXAM2, EXAM3, EXAM4]
fonti_esterne: 8
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 19 — Networking

## Di cosa parla questo capitolo

Fino a qui ogni programma che abbiamo scritto viveva da solo: leggeva dalla tastiera o da un file, calcolava, stampava. Molti programmi veri, però, **parlano con altri programmi**: il browser chiede una pagina a un server, un'applicazione di messaggistica spedisce un testo a un'altra, un programma d'esame trasmette un oggetto a un server già in ascolto e ne aspetta la risposta. Questo capitolo spiega come si scrivono, in Java, i due programmi che si parlano.

La buona notizia è che quasi tutto quello che serve lo sappiamo già. Parlare con un altro programma attraverso una rete significa **scrivere byte su un flusso** e **leggere byte da un flusso**, esattamente come con un file ([Capitolo 14](14-file-di-testo.md) e [Capitolo 15](15-stream-binari-e-serializzazione.md)). Cambia una cosa sola: il flusso non porta a un file ma a un altro programma, e per ottenerlo bisogna prima **stabilire un contatto**. Di questo si occupano le classi del package `java.net`.

In questo capitolo vedremo:

- che cosa sono **client**, **server**, **indirizzo** e **porta**, e quali sono i due modi di comunicare, **TCP** e **UDP** (paragrafo 19.1);
- i **socket TCP**: `ServerSocket` e `accept` per il server, `Socket` per il client, i due flussi di ogni socket, e tre applicazioni complete (paragrafo 19.2);
- come un server serve **più client contemporaneamente**, con un thread per ciascuno (paragrafo 19.3);
- come far viaggiare **oggetti serializzati** su una connessione, e l'ordine in cui vanno aperti i flussi (paragrafo 19.4);
- i **datagrammi UDP**: `DatagramSocket`, `DatagramPacket`, `InetAddress` (paragrafo 19.5);
- come leggere una **pagina web** con `URL` (paragrafo 19.6);
- le **eccezioni della rete** e il comportamento richiesto «in caso di fallimento» (paragrafo 19.7);
- come tradurre le parole di una traccia in codice (paragrafo 19.8);
- gli **scheletri** da saper scrivere a memoria e gli **errori tipici**.

Il capitolo si appoggia su molti precedenti. `PrintWriter`, `BufferedReader` e `Scanner`, l'idea di **avvolgere** un flusso in un altro e il ruolo di `close` sono nel [Capitolo 14](14-file-di-testo.md). `ObjectOutputStream`, `ObjectInputStream` e `Serializable` sono nel [Capitolo 15](15-stream-binari-e-serializzazione.md), che ha già anticipato (sezione 15.11) la scelta del flusso da avvolgere. Le eccezioni controllate e lo schema di chiusura nel `finally` sono nel [Capitolo 13](13-eccezioni.md). Per il server a più client servono i thread del [Capitolo 17](17-thread.md) e, appena si condividono dati, la sincronizzazione del [Capitolo 18](18-sincronizzazione.md).

> [!IMPORTANT]
> **Nota per l'esame — Rete**
> Un esercizio da 13 punti della prova scritta ha chiesto più volte un **client**: di solito il server è già in ascolto e *non va scritto*, le sue coordinate (indirizzo e porta) sono date nella traccia, e si chiede un metodo che apra la comunicazione, trasmetta un dato, attenda la risposta e la restituisca, oppure restituisca `null` «in caso di fallimento». Il dato può essere un testo su TCP, un oggetto serializzato su TCP, un testo su UDP. Sapere le forme esatte è la differenza tra un esercizio che si esegue al primo tentativo e uno che si blocca in silenzio (un client che aspetta una risposta che non arriverà *non stampa nulla* e consuma comunque un'esecuzione). Per questo il capitolo insiste su tre cose: quale flusso avvolgere, in che ordine aprirli, e che cosa fare quando qualcosa va storto.

---

## 19.1 Due programmi che si parlano

### 19.1.1 Client e server

Quando due programmi comunicano in rete, quasi sempre i loro ruoli non sono simmetrici. Uno **aspetta** di essere contattato e offre un servizio; l'altro **cerca** il primo e gli chiede qualcosa.

> [!NOTE]
> **Definizione — Server e client**
> Il **server** è il programma che resta *in ascolto* su una certa porta e offre un servizio. Il **client** è il programma che prende l'iniziativa: si collega al server e gli invia le sue richieste. Il server deve essere già in funzione quando il client tenta di collegarsi.

> [!TIP]
> **Intuizione — Il servizio clienti telefonico**
> Il server somiglia a un ufficio con un numero di telefono: sta lì, a disposizione, e non chiama mai nessuno. Il client è la persona che compone il numero. Se l'ufficio non è aperto (il server non è stato avviato), la telefonata non va a buon fine. L'analogia funziona fino a un certo punto: un vero server può parlare con moltissimi clienti, e lo vedremo nel paragrafo 19.3.

Nella programmazione, «client» e «server» sono ruoli del **programma**, non del computer: i due programmi possono girare su macchine diverse oppure, come negli esempi di questo capitolo, sulla **stessa** macchina.

### 19.1.2 Indirizzo e porta

Perché un client trovi un server servono due informazioni.

- L'**indirizzo** del computer su cui il server gira. Può essere un indirizzo numerico (come `192.168.1.20`, detto indirizzo IP) oppure un nome (come `www.example.com`). Per parlare con un programma che gira sulla **stessa macchina** esiste l'indirizzo speciale `127.0.0.1`, con il nome corrispondente `localhost`.
- La **porta** (*port*): un numero intero da **0 a 65535** che identifica *quale* programma, tra i tanti che girano su quel computer, deve ricevere il contatto.

Un computer ospita molti servizi insieme; l'indirizzo dice a quale computer rivolgersi, la porta dice a quale servizio. Il server dichiara all'avvio «sono io ad ascoltare sulla porta 5555», e il client scrive nel proprio codice «voglio parlare con l'indirizzo 127.0.0.1, porta 5555». La coppia indirizzo-porta è un **socket** nel senso più ampio del termine (la parola ha però anche un significato più preciso in Java, che incontreremo nel paragrafo 19.2).

Due precisazioni. Primo: su una stessa macchina una porta può essere occupata da **un solo** programma alla volta. Se un secondo programma chiede la stessa porta riceve un errore (paragrafo 19.7). Secondo: il client non sceglie la propria porta; il sistema gliene assegna una libera in automatico, e il server la vede arrivare insieme al contatto.

### 19.1.3 Due modi di comunicare: TCP e UDP

Esistono due protocolli di comunicazione, con caratteristiche opposte, e Java li gestisce con due famiglie di classi diverse.

| | **TCP** (con connessione) | **UDP** (senza connessione) |
|---|---|---|
| Come funziona | Si stabilisce **una connessione** tra client e server; i dati scorrono nel canale come un flusso continuo | Non c'è connessione: ogni pacchetto viaggia per conto suo, anche per percorsi diversi |
| Ordine | I dati arrivano **nell'ordine** in cui sono partiti | Nessuna garanzia di ordine |
| Perdite | Affidabile: la probabilità di perdere dati è bassa | I pacchetti possono **perdersi** o arrivare **duplicati** |
| Classi Java | `Socket`, `ServerSocket` | `DatagramSocket`, `DatagramPacket` |
| Quando si sceglie | Quando i dati devono arrivare tutti e in ordine | Quando il controllo degli errori e l'affidabilità del TCP non servono |

Il prezzo dell'affidabilità del TCP è il lavoro in più: stabilire la connessione e controllare che tutto arrivi. UDP evita questo lavoro ed è quindi **più efficiente**, a patto di accettare che qualcosa possa andare perso. Per questo si usa quando conta la rapidità più della completezza (pensa a una videochiamata, in cui un pezzo di immagine perso è meglio di un'immagine in ritardo).

Per un'applicazione che scambia messaggi di testo e oggetti, come quelle d'esame, TCP è la scelta naturale; UDP compare quando la traccia dice esplicitamente «protocollo UDP» o parla di «datagramma».

### 19.1.4 Le classi di `java.net`

Le classi di questo capitolo stanno quasi tutte nel package `java.net`; i flussi, come sappiamo, in `java.io`. Un programma di rete ha quindi quasi sempre due gruppi di `import`:

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
```

| Classe | A cosa serve | Paragrafo |
|---|---|---|
| `ServerSocket` | il server: si mette in ascolto su una porta e accetta i client | 19.2.2 |
| `Socket` | un'estremità di una connessione TCP; il client la crea per collegarsi | 19.2.3 |
| `DatagramSocket` | un'estremità di una comunicazione UDP | 19.5.2 |
| `DatagramPacket` | un pacchetto UDP: dati, lunghezza, indirizzo e porta | 19.5.3 |
| `InetAddress` | un indirizzo di rete | 19.5.4 |
| `URL` | l'indirizzo di una risorsa su Internet, da cui leggere | 19.6 |

---

## 19.2 Socket TCP

### 19.2.1 L'idea: un socket a ciascuna estremità

Con TCP, la comunicazione si costruisce così. Il server crea un `ServerSocket` e si mette in ascolto su una porta. Il client crea un `Socket` indicando indirizzo e porta del server. Quando il contatto riesce, **entrambi** i programmi si ritrovano in mano un oggetto `Socket`: il client ha il proprio, e il server ne ottiene uno nuovo, dedicato a quel client, dal metodo `accept` (paragrafo 19.2.2).

Ogni `Socket` ha **due flussi**: uno di **ingresso**, da cui si leggono i dati che arrivano dall'altra parte, e uno di **uscita**, su cui si scrivono i dati da spedire. Il collegamento è incrociato: ciò che si scrive nel flusso di uscita di un socket compare nel flusso di ingresso dell'altro.

```text
        SERVER                                         CLIENT
   +----------------+                            +----------------+
   |  Socket (S1)   |                            |  Socket (S2)   |
   |                |                            |                |
   |  ingresso  <---+----------------------------+---  uscita     |
   |  uscita    ----+--------------------------->+-->  ingresso   |
   +----------------+                            +----------------+
```

Il disegno si legge così: quello che il client scrive sul suo flusso di uscita lo legge il server dal suo flusso di ingresso, e viceversa. Dopo che i due socket sono stati ottenuti, **non c'è più differenza di principio tra client e server**: entrambi leggono e scrivono su flussi, e sta al programmatore decidere chi parla per primo. Questo punto è cruciale: due programmi che *leggono entrambi* per primi restano in attesa l'uno dell'altro per sempre.

### 19.2.2 Il server: `ServerSocket` e `accept`

Il server crea un oggetto `ServerSocket` passando la porta su cui ascoltare, poi chiama `accept` per aspettare un client.

```java
ServerSocket server = new ServerSocket(9090);     // ascolta sulla porta 9090
Socket socket = server.accept();                  // si ferma finche' arriva un client
```

La prima riga **registra il servizio**: da questo momento il sistema sa che i contatti diretti alla porta 9090 sono per questo programma. La seconda riga è **bloccante**: il programma si ferma lì, senza consumare processore, finché un client si collega. Quando accade, `accept` restituisce un nuovo `Socket`, il canale con *quel* client. Il `ServerSocket` resta a disposizione per accettare altri client; il `Socket` restituito serve a parlare con quello appena arrivato.

> [!NOTE]
> **Definizione — `ServerSocket` e `accept`**
> `public ServerSocket(int port) throws IOException` crea un socket di ascolto legato alla porta indicata.
> `public Socket accept() throws IOException` attende una connessione e la accetta, restituendo il `Socket` per comunicare con quel client. Il metodo **blocca** finché una connessione non arriva.
> Se la porta è già occupata, il costruttore lancia una `IOException` (precisamente `BindException`, paragrafo 19.7).

Esiste anche il costruttore con due argomenti, `ServerSocket(int port, int backlog)`: il secondo numero è la lunghezza della **coda** dei client che hanno bussato ma non sono ancora stati accettati. Nel costruttore a un solo argomento la coda è lunga 50. In tutto il capitolo useremo la forma con la sola porta.

> [!NOTE]
> **Approfondimento esterno — `ServerSocket` e `accept`**
> La documentazione ufficiale precisa che `ServerSocket(int port)` «*Creates a server socket, bound to the specified port*», che una porta 0 significa «*the port number is automatically allocated, typically from an ephemeral port range*» (cioè sceglie il sistema una porta libera) e che «*The maximum queue length for incoming connection indications (a request to connect) is set to 50. If a connection indication arrives when the queue is full, the connection is refused*». Dichiara `throws IOException` e `IllegalArgumentException` («*if the port parameter is outside the specified range of valid port values, which is between 0 and 65535, inclusive*»). Per `accept` scrive: «*Listens for a connection to be made to this socket and accepts it. The method blocks until a connection is made*».
>
> *Fonte:* [ServerSocket (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/ServerSocket.html)

### 19.2.3 Il client: `Socket`

Il client crea un `Socket` passando l'indirizzo del server e la porta:

```java
Socket socket = new Socket("localhost", 9090);    // si collega al server
```

Il costruttore **non ritorna** finché la connessione non è stabilita (o fallita): se tutto va bene, al ritorno il client ha già un canale aperto verso il server. Il primo argomento è il nome o l'indirizzo numerico (una `String`: `"localhost"`, `"127.0.0.1"`, `"www.example.com"`), il secondo la porta.

> [!NOTE]
> **Definizione — `Socket` (costruttore)**
> `public Socket(String host, int port) throws UnknownHostException, IOException` crea un socket TCP e lo collega alla porta indicata dell'host indicato.
> `UnknownHostException` (un'`IOException`) segnala che l'indirizzo non si risolve; un server non in ascolto produce una `ConnectException` (paragrafo 19.7). Una porta fuori da 0-65535 lancia `IllegalArgumentException`, non controllata.

> [!NOTE]
> **Approfondimento esterno — `Socket(String, int)`**
> La documentazione ufficiale descrive `public Socket(String host, int port) throws UnknownHostException, IOException` così: «*Creates a stream socket and connects it to the specified port number on the named host*». Se `host` è `null` equivale all'indirizzo di *loopback* (la macchina stessa). Tra le eccezioni elenca `UnknownHostException` («*if the IP address of the host could not be determined*»), `IOException` («*if an I/O error occurs when creating the socket*») e `IllegalArgumentException` («*if the port parameter is outside the specified range of valid port values, which is between 0 and 65535, inclusive*»).
>
> *Fonte:* [Socket (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/Socket.html)

### 19.2.4 I flussi del socket

Ora che i due programmi hanno un `Socket` ciascuno, serve il modo di scrivere e leggere. Il socket offre due metodi:

```java
InputStream  entrata = socket.getInputStream();    // da qui si legge
OutputStream uscita  = socket.getOutputStream();   // qui si scrive
```

Sono flussi di **byte**: `InputStream` e `OutputStream` sono le classi astratte di base dei flussi di byte ([Capitolo 14](14-file-di-testo.md)). Per scambiarsi testo li **avvolgiamo** negli stessi oggetti che già conosciamo per i file:

```java
PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
```

La prima riga costruisce un `PrintWriter` sul flusso di uscita. Il secondo argomento, `true`, è il punto più delicato dell'intero capitolo: attiva lo **svuotamento automatico** (*autoflush*). Un `PrintWriter` accumula i caratteri in un buffer e li spedisce solo quando il buffer si riempie o viene svuotato. Su un file non importa quando i dati partono; su una **connessione di rete** sì, perché l'altro programma sta aspettando e non può rispondere a ciò che non ha ricevuto. Con `true`, ogni `println` svuota il buffer, e il testo parte subito.

La seconda riga costruisce un `BufferedReader` sul flusso di ingresso: `socket.getInputStream()` produce byte, `InputStreamReader` li traduce in caratteri, `BufferedReader` aggiunge `readLine`. È la stessa catena a tre anelli che già usiamo per leggere un file di testo, con il socket al posto di `FileReader` ([Capitolo 14](14-file-di-testo.md), sezione 14.4.2). In alternativa si può avvolgere il flusso di ingresso direttamente in uno `Scanner`:

```java
Scanner in = new Scanner(socket.getInputStream());
String riga = in.nextLine();
```

I due modi sono equivalenti per leggere righe; useremo `BufferedReader` perché è quello dei materiali del corso.

La lettura merita attenzione: `in.readLine()` **blocca** finché una riga completa (terminata da un a capo) non è arrivata. Se l'altro programma chiude la connessione, `readLine` restituisce `null`, esattamente come alla fine di un file.

> [!NOTE]
> **Approfondimento esterno — `PrintWriter` con *autoflush* e `readLine`**
> La documentazione ufficiale descrive `public PrintWriter(OutputStream out, boolean autoFlush)` come «*Creates a new PrintWriter from an existing OutputStream*» e spiega l'argomento: «*if true, the println, printf, or format methods will flush the output buffer*». Il `print` semplice, quindi, **non** svuota il buffer nemmeno con `autoFlush` a `true`. Per `BufferedReader.readLine()` scrive che una riga è terminata da un a capo, da un ritorno carrello o dalla fine del flusso, e che restituisce «*null if the end of the stream has been reached without reading any characters*»; dichiara `throws IOException`.
>
> *Fonte:* [PrintWriter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/PrintWriter.html) e [BufferedReader (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/BufferedReader.html)

### 19.2.5 Chiudere la connessione

Quando la conversazione è finita bisogna chiudere il socket con `close()`, che dichiara `throws IOException`. Chiudere il socket chiude anche i suoi due flussi; ed è vero anche il contrario: chiudere il flusso di uscita ottenuto da `getOutputStream()` chiude il socket. Va quindi chiuso **una volta sola**, e per lo stesso motivo visto per i file ([Capitolo 13](13-eccezioni.md), sezione 13.5.3) la chiusura va in un blocco `finally`, così da avvenire anche se qualcosa lancia un'eccezione a metà conversazione.

Quando il socket è creato *prima* del `try`, lo schema è semplice:

```java
Socket socket = new Socket("localhost", 9090);    // se questo fallisce, non c'e' nulla da chiudere
try {
    // ... conversazione ...
} finally {
    socket.close();                               // sempre, anche con un'eccezione
}
```

Se invece la creazione del socket sta *dentro* il `try` (perché le sue eccezioni devono essere catturate insieme alle altre), la variabile va dichiarata prima, inizializzata a `null`, e la chiusura nel `finally` è protetta da un controllo `!= null`: lo vedremo nel metodo del paragrafo 19.4.4 e negli scheletri.

> [!NOTE]
> **Approfondimento esterno — Chiusura di un `Socket`**
> La documentazione ufficiale di `Socket.close()` dice: «*Closing this socket will also close the socket's InputStream and OutputStream*»; il metodo dichiara `throws IOException`. Per `getOutputStream()` aggiunge: «*Closing the returned OutputStream will close the associated socket*». I due metodi `getInputStream()` e `getOutputStream()` dichiarano entrambi `throws IOException`.
>
> *Fonte:* [Socket (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/Socket.html)

Anche `ServerSocket` ha un `close()`, da chiamare quando il server smette di accettare client.

### 19.2.6 Prima applicazione: il saluto

Mettiamo insieme i pezzi con l'applicazione più semplice possibile. Il server aspetta un client, gli manda una riga di saluto e termina. Il client si collega, legge la riga e la stampa.

#### Esempio — Server del saluto

```java
import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerSaluto {
    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(9101);       // il servizio "abita" sulla porta 9101
        System.out.println("Server in ascolto");
        try {
            Socket socket = server.accept();                // si ferma qui finche' non arriva un client
            try {
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                out.println("Ciao dal server");             // una riga verso il client
            } finally {
                socket.close();                             // chiude la connessione con questo client
            }
        } finally {
            server.close();                                 // smette di ascoltare
        }
    }
}
```

Riga per riga. L'`import` di `ServerSocket` e `Socket` viene da `java.net`, quello di `PrintWriter` e `IOException` da `java.io`. Il `main` dichiara `throws IOException` perché `new ServerSocket`, `accept`, `getOutputStream` e `close` possono lanciarla. La riga `new ServerSocket(9101)` apre l'ascolto; la stampa serve solo a noi per vedere che il server è partito. `accept()` blocca. Dopo l'arrivo del client, `getOutputStream()` dà il flusso verso di lui, `new PrintWriter(..., true)` lo avvolge con lo svuotamento automatico, e `println` spedisce la riga. I due `finally` annidati chiudono prima il socket del client e poi il socket di ascolto.

#### Esempio — Client del saluto

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class ClienteSaluto {
    public static void main(String[] args) throws IOException {
        Socket socket = new Socket("localhost", 9101);      // si connette al server
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String risposta = in.readLine();                // legge una riga
            System.out.println("Dal server: " + risposta);
        } finally {
            socket.close();
        }
    }
}
```

Il client usa la stessa porta, 9101, che il server ha dichiarato: se i due numeri non coincidono, la connessione non riesce. Il costruttore `new Socket("localhost", 9101)` ritorna quando il contatto è avvenuto; `readLine` aspetta la riga del server.

Per provare i due programmi si avvia **prima il server**, in un terminale, e poi il client, in un altro. Il server stampa:

```text
Server in ascolto
```

e il client:

```text
Dal server: Ciao dal server
```

Se si avvia il client per primo, o con una porta diversa, il client termina con `java.net.ConnectException: Connection refused` (paragrafo 19.7).

### 19.2.7 Seconda applicazione: il ripetitore

Un server che dice una frase sola è poco utile. Complichiamo un poco: il client invia più righe, il server risponde a ciascuna ripetendola con un prefisso, e la conversazione termina quando il client invia la riga `#`, che fa da **valore sentinella** ([Capitolo 4](04-strutture-di-controllo.md), sezione 4.6). Qui nasce il punto che distingue un programma di rete da uno su file: i due programmi devono **concordare un protocollo**, cioè un accordo su chi parla, in che formato (qui: una riga per messaggio) e come ci si saluta (qui: `#`).

#### Esempio — Il server ripetitore

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerRipetitore {
    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(9102);
        System.out.println("Server in ascolto");
        Socket socket = server.accept();
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        String riga = in.readLine();
        while (riga != null && !riga.equals("#")) {         // null: il client ha chiuso senza dire "#"
            out.println("Dal server: " + riga);
            riga = in.readLine();
        }
        out.println("Dal server: chiusura");
        socket.close();
        server.close();
    }
}
```

Il ciclo legge una riga alla volta. La condizione ha **due** parti: `riga != null` e `!riga.equals("#")`. La prima protegge dal caso in cui il client chiuda la connessione senza inviare `#`: `readLine` restituisce allora `null`, e chiamare `riga.equals(...)` su `null` lancerebbe una `NullPointerException` ([Capitolo 8](08-riferimenti-e-memoria.md), sezione 8.3). Grazie al corto circuito di `&&`, se `riga` è `null` la seconda parte non viene valutata. Si può anche scrivere `!"#".equals(riga)`, che è sicura anche con `riga` nulla perché il metodo è chiamato sulla costante.

#### Esempio — Il client del ripetitore

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ClienteRipetitore {
    public static void main(String[] args) throws IOException {
        String[] messaggi = {"uno", "due", "#"};
        Socket socket = new Socket("localhost", 9102);
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        for (String m : messaggi) {
            out.println(m);                                 // invia
            System.out.println(in.readLine());              // attende e stampa la risposta
        }
        socket.close();
    }
}
```

Il client alterna **un invio e una lettura** per ogni messaggio: è il suo lato del protocollo. Ricordiamo che al `#` il server risponde comunque con una riga (`Dal server: chiusura`), per cui il client, che dopo ogni invio legge una riga, non resta mai in attesa. Se il server non rispondesse al `#`, la terza `readLine` del client aspetterebbe all'infinito (o fino alla chiusura della connessione). **Il numero di scritture di un lato deve corrispondere al numero di letture dell'altro**: è la regola d'oro dei protocolli semplici.

Output del client:

```text
Dal server: uno
Dal server: due
Dal server: chiusura
```

### 19.2.8 Servire più client, uno dopo l'altro

I due server visti finora servono **un solo client** e poi terminano. Un vero server resta in funzione e accetta client uno dopo l'altro: basta mettere `accept` in un ciclo infinito.

#### Esempio — Server che serve un client dopo l'altro

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerSequenziale {
    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(9107);
        System.out.println("Server in ascolto");
        while (true) {                                          // non finisce mai
            Socket socket = server.accept();                    // aspetta il prossimo client
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String riga = in.readLine();
            while (riga != null && !riga.equals("#")) {
                out.println("Dal server: " + riga);
                riga = in.readLine();
            }
            socket.close();                                     // finito con questo client
        }
    }
}
```

La struttura è a due cicli annidati: quello **esterno** accetta un client dopo l'altro, quello **interno** conversa con il client corrente fino al `#`. Un server così non termina da solo: si ferma solo se lo si interrompe dall'esterno.

C'è però un limite serio: mentre il server converso con un client, **non sta eseguendo `accept`**, e gli altri client devono aspettare nella coda. Se il primo client è lento (o si dimentica di inviare `#`), tutti gli altri restano fermi. Il paragrafo 19.3 risolve il problema.

### 19.2.9 Terza applicazione: due client che si scrivono

La terza applicazione del corso fa comunicare **due client attraverso il server**. Il server aspetta due client, poi inoltra i messaggi dall'uno all'altro, finché uno dei due invia `#`. Il server fa da centralino: nessun client conosce l'altro.

#### Esempio — Il server che inoltra tra due client

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerDueClient {
    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(9103);
        Socket s1 = server.accept();                        // primo client
        PrintWriter out1 = new PrintWriter(s1.getOutputStream(), true);
        BufferedReader in1 = new BufferedReader(new InputStreamReader(s1.getInputStream()));
        out1.println("Connesso");
        Socket s2 = server.accept();                        // secondo client
        PrintWriter out2 = new PrintWriter(s2.getOutputStream(), true);
        BufferedReader in2 = new BufferedReader(new InputStreamReader(s2.getInputStream()));
        out2.println("Connesso");

        boolean fine = false;
        while (!fine) {
            String m1 = in1.readLine();                     // si ferma finche' parla il client 1
            out2.println(m1);                               // lo gira al client 2
            String m2 = in2.readLine();                     // poi si ferma finche' parla il client 2
            out1.println(m2);                               // lo gira al client 1
            fine = "#".equals(m1) || "#".equals(m2);
        }
        s1.close();
        s2.close();
        server.close();
    }
}
```

Il server apre due coppie di flussi, una per client, e a ogni giro del ciclo fa quattro cose: legge dal client 1, inoltra al client 2, legge dal client 2, inoltra al client 1. Il ciclo termina quando uno dei due messaggi è `#`.

#### Esempio — Il client della conversazione a due

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ClienteDue {
    public static void main(String[] args) throws IOException {
        String nome = args[0];
        Socket socket = new Socket("localhost", 9103);
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        System.out.println(nome + " riceve: " + in.readLine());   // "Connesso"
        String[] messaggi = {"ciao da " + nome, "#"};
        for (String m : messaggi) {
            out.println(m);
            System.out.println(nome + " riceve: " + in.readLine());
        }
        socket.close();
    }
}
```

Il nome del client arriva dalla riga di comando (`args[0]`, [Capitolo 5](05-array-e-matrici.md)). Avviando il server e poi due client, `java ClienteDue Anna` e `java ClienteDue Bruno`, l'output di Anna è:

```text
Anna riceve: Connesso
Anna riceve: ciao da Bruno
Anna riceve: #
```

e quello di Bruno:

```text
Bruno riceve: Connesso
Bruno riceve: ciao da Anna
Bruno riceve: #
```

(Se i due client sono avviati in terminali diversi, le righe di uno non si mescolano con quelle dell'altro.)

> [!WARNING]
> **Attenzione — I turni sono rigidi**
> Questo server legge **prima** dal client 1 e **poi** dal client 2, sempre in quell'ordine. Se il client 2 ha qualcosa da dire mentre il server aspetta una riga dal client 1, il messaggio resta fermo finché il client 1 non parla. È un limite di tutti i programmi che hanno *un solo punto di lettura* e leggono in modo bloccante. La soluzione generale è un thread per ogni direzione (paragrafo 19.3): ciascun thread si ferma a leggere dal *suo* client, senza bloccare l'altro.

---
## 19.3 Un thread per ogni client

### 19.3.1 Il problema

Nel server sequenziale del paragrafo 19.2.8 il thread principale fa tutto: accetta, conversa, riaccetta. Mentre conversa con un client, gli altri aspettano. Ma sappiamo già come fare due cose contemporaneamente: con i **thread** ([Capitolo 17](17-thread.md)). L'idea è dividere il lavoro in due ruoli:

- il thread principale fa **solo** `accept`, in un ciclo infinito;
- per ogni client accettato avvia un **nuovo thread** che si occupa di quella conversazione, e torna subito ad `accept`.

Così un client lento o distratto blocca solo il proprio thread, non il server.

### 19.3.2 Il codice

La conversazione con un singolo client diventa il corpo di `run` di un `Runnable`, a cui si passa il `Socket` nel costruttore.

#### Esempio — Server con un thread per client

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

class GestoreClient implements Runnable {
    private Socket socket;

    GestoreClient(Socket socket) {
        this.socket = socket;
    }

    public void run() {
        try {
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String riga = in.readLine();
            while (riga != null && !riga.equals("#")) {
                out.println("Dal server: " + riga);
                riga = in.readLine();
            }
            socket.close();
        } catch (IOException e) {
            System.out.println("Client perso: " + e.getMessage());
        }
    }
}

public class ServerMultiplo {
    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(9104);
        System.out.println("Server in ascolto");
        while (true) {
            Socket socket = server.accept();                // un nuovo client
            new Thread(new GestoreClient(socket)).start();  // servito da un thread suo
        }
    }
}
```

Ci sono due classi: `GestoreClient`, senza modificatore, che realizza `Runnable` e contiene la conversazione; `ServerMultiplo`, con il `main`, che accetta e avvia. Il metodo `run` **non può** dichiarare `throws IOException` (la firma di `Runnable.run` non lo ammette, [Capitolo 17](17-thread.md)), per cui l'`IOException` viene catturata dentro `run` con un `try`/`catch`. Il thread principale non chiama mai `join`: non gli interessa aspettare i gestori, il suo compito è accettare.

Proviamo a collegare due client: il primo si collega e poi resta fermo per tre secondi prima di scrivere, il secondo si collega mezzo secondo dopo e scrive subito. Con il server sequenziale il secondo dovrebbe attendere la fine del primo; con i thread viene servito subito:

```text
Veloce: Dal server: ciao da Veloce
Lento: Dal server: ciao da Lento
```

La riga di `Veloce` compare per prima benché il suo client sia partito dopo: mentre `Lento` dormiva, il suo thread era fermo in `readLine`, e il thread principale era già tornato su `accept` per accogliere `Veloce`.

> [!WARNING]
> **Attenzione — Dati condivisi tra i gestori**
> Questo gestore lavora solo sul proprio socket e sulle proprie variabili locali, quindi i thread non si pestano i piedi. Se invece i gestori modificassero **uno stesso oggetto** (un contatore dei messaggi, un elenco dei client collegati), si ricadrebbe nella race condition del [Capitolo 18](18-sincronizzazione.md): l'oggetto condiviso va protetto con `synchronized`.

Questo schema (`accept` in un ciclo, un thread per client) è la forma di quasi tutti i server veri. Nelle tre tracce di rete degli appelli ufficiali il server era sempre fornito e non andava scritto: conviene però saperlo leggere, e saperlo scrivere per provare il proprio client in locale.

---

## 19.4 Oggetti sulla connessione

### 19.4.1 Perché non basta il testo

Le righe di testo vanno bene per messaggi semplici. Ma se due programmi devono scambiarsi un **oggetto** con più campi (un ordine, una persona, un biglietto), convertirlo in testo, spedirlo e riconvertirlo a mano è lungo e fragile. Abbiamo già lo strumento giusto: la **serializzazione** ([Capitolo 15](15-stream-binari-e-serializzazione.md)). `ObjectOutputStream.writeObject` trasforma un oggetto in byte, `ObjectInputStream.readObject` lo ricostruisce, e gli stessi byte possono viaggiare su una connessione di rete. Come ha anticipato la sezione 15.11, cambia solo il flusso che si avvolge: invece di un `FileOutputStream`, il flusso di uscita del socket.

```java
// scrittura: i byte finiscono IN RETE
ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
// lettura: i byte arrivano DALLA RETE
ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
```

Le due righe sono quasi uguali a quelle per il file; l'unica differenza è ciò che sta tra le parentesi del costruttore. Su un file l'ordine con cui si aprono i flussi non conta; **in rete sì**, ed è la fonte del guaio più sottile del capitolo.

### 19.4.2 L'ordine di apertura dei flussi

Ricordiamo dal [Capitolo 15](15-stream-binari-e-serializzazione.md) (sezioni 15.3.3 e 15.11.2) due fatti. Il costruttore di `ObjectOutputStream` **scrive subito** un'intestazione sul flusso. Il costruttore di `ObjectInputStream` **legge** quell'intestazione, e se non è ancora arrivata **si ferma ad aspettarla**.

Ora immaginiamo che client e server aprano entrambi per primo il flusso di **ingresso**:

```text
client:  new ObjectInputStream(...)   --> aspetta l'intestazione del server
server:  new ObjectInputStream(...)   --> aspetta l'intestazione del client
```

Nessuno dei due ha ancora aperto il flusso di uscita, quindi nessuno ha scritto l'intestazione che l'altro attende: restano **bloccati per sempre**, senza stampare nulla né lanciare eccezioni. È un'attesa circolare, della stessa famiglia dello stallo del [Capitolo 18](18-sincronizzazione.md).

La regola che evita il problema è una sola:

> [!IMPORTANT]
> **Nota per l'esame — Prima l'uscita, poi `flush`, poi l'ingresso**
> Su ogni estremità di una connessione che scambia oggetti si apre **prima** l'`ObjectOutputStream`, si chiama subito `flush()` (che spedisce l'intestazione), e **solo dopo** si apre l'`ObjectInputStream`. Se entrambi i programmi seguono la regola, nessuno aspetta un'intestazione che non è stata ancora spedita. Dopo ogni `writeObject` si fa `flush()`, perché i dati escano dal buffer e non restino fermi mentre l'altro li attende.

### 19.4.3 Un esempio completo: spedire un oggetto e riaverlo

Vediamo un programma completo. Il server riceve un oggetto, lo stampa e lo rimanda indietro identico; il client lo spedisce e stampa quello che torna. L'oggetto è un `Biglietto` con una destinazione e un numero di posto.

#### Esempio — La classe `Biglietto` e il client

```java
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.net.Socket;

class Biglietto implements Serializable {
    private static final long serialVersionUID = 1L;
    private String destinazione;
    private int posto;

    public Biglietto(String destinazione, int posto) {
        this.destinazione = destinazione;
        this.posto = posto;
    }

    public String getDestinazione() { return destinazione; }
    public int getPosto() { return posto; }

    public String toString() {
        return "Biglietto[" + destinazione + ", posto " + posto + "]";
    }
}

public class ClienteBiglietti {
    private String host;
    private int porta;

    public ClienteBiglietti(String host, int porta) {
        this.host = host;
        this.porta = porta;
    }

    public Biglietto invia(Biglietto b) {
        Socket socket = null;
        try {
            socket = new Socket(host, porta);                                    // 1. connessione
            ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
            out.flush();                                                         // 2. spedisce l'intestazione
            ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
            out.writeObject(b);                                                  // 3. invio
            out.flush();
            return (Biglietto) in.readObject();                                  // 4. risposta, con il cast
        } catch (IOException e) {
            return null;
        } catch (ClassNotFoundException e) {
            return null;
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    // niente da fare: si e' gia' in chiusura
                }
            }
        }
    }

    public static void main(String[] args) {
        ClienteBiglietti c = new ClienteBiglietti("127.0.0.1", Integer.parseInt(args[0]));
        System.out.println(c.invia(new Biglietto("Roma", 12)));
    }
}
```

#### Esempio — Il server che rimanda indietro l'oggetto

```java
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerOggetti {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        ServerSocket server = new ServerSocket(9105);
        System.out.println("Server in ascolto");
        Socket socket = server.accept();
        ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());   // PRIMA l'uscita...
        out.flush();                                                                // ...e si svuota l'intestazione
        ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
        Biglietto b = (Biglietto) in.readObject();
        System.out.println("Server ha ricevuto: " + b);
        out.writeObject(b);                                                         // lo rimanda identico
        out.flush();
        socket.close();
        server.close();
    }
}
```

Il server usa la classe `Biglietto` del file precedente (nello stesso programma compilato: `javac *.java`). Il `main` del client riceve la porta dalla riga di comando, qui `9105`. Avviato prima il server e poi il client, il server stampa

```text
Server in ascolto
Server ha ricevuto: Biglietto[Roma, posto 12]
```

e il client:

```text
Biglietto[Roma, posto 12]
```

Il `toString` del client mostra che l'oggetto ricostruito ha gli stessi valori di quello spedito; come ricordato nel [Capitolo 8](08-riferimenti-e-memoria.md) (sezione 8.4.5), è però un **oggetto nuovo**: un `==` con l'originale darebbe `false`.

### 19.4.4 Il metodo client: struttura e fallimento

Il metodo `invia` ha la forma che una traccia d'esame chiede quasi alla lettera. Rileggiamolo in funzione dei suoi quattro momenti.

1. **Connessione.** `new Socket(host, porta)` può lanciare `UnknownHostException` o `IOException`. È dentro il `try`, perché ogni suo fallimento deve produrre `null`.
2. **Apertura dei flussi nell'ordine giusto.** Uscita, `flush`, ingresso (paragrafo 19.4.2).
3. **Invio e attesa.** `writeObject` e `flush`; poi `readObject`, che **blocca** finché il server non risponde e che dichiara due eccezioni **controllate**: `IOException` e `ClassNotFoundException` ([Capitolo 15](15-stream-binari-e-serializzazione.md), sezione 15.12). Il cast `(Biglietto)` è obbligatorio perché `readObject` restituisce `Object`.
4. **Fallimento e chiusura.** Qualunque eccezione porta a `return null;`, come chiede la traccia; la chiusura del socket è nel `finally`, protetta da `socket != null` (se `new Socket` fallisce, la variabile è rimasta `null`) e circondata da un proprio `try`/`catch`, perché anche `close` dichiara `IOException`.

Due note di struttura. La variabile `socket` è dichiarata **prima** del `try` perché il `finally` deve poterla vedere: una variabile dichiarata dentro il `try` non esiste nel `finally` ([Capitolo 13](13-eccezioni.md)). E i due `catch` sono separati perché `IOException` e `ClassNotFoundException` non sono in relazione tra loro: nessuna delle due è sottoclasse dell'altra.

Il `return (Biglietto) in.readObject();` dentro il `try` non salta il `finally`: Java esegue comunque il `finally` prima di restituire il valore, quindi il socket viene chiuso anche in caso di successo.

### 19.4.5 Testo e oggetti non si mescolano

Una connessione ha due estremità, e **entrambe** devono usare lo stesso tipo di flusso. Se un lato scrive righe con un `PrintWriter` e l'altro prova a leggerle con un `ObjectInputStream`, la lettura dell'intestazione fallisce:

```text
java.io.StreamCorruptedException: invalid stream header: 6369616F
```

Il numero esadecimale `6369616F` è il codice dei byte `c`, `i`, `a`, `o`: il lettore si aspettava l'intestazione di serializzazione e ha trovato la parola `ciao`. Il protocollo (testo o oggetti, quanti messaggi, in che ordine) è un accordo tra i due programmi: se la traccia dice che il server «riceve un oggetto e lo rimanda indietro», il client deve parlare per oggetti; se dice «messaggio testuale», per righe.

---

## 19.5 Datagrammi UDP

### 19.5.1 Un altro modo di comunicare

Con UDP non c'è nessuna connessione e nessun flusso. Un programma impacchetta i dati in un **pacchetto** (*datagram*), ci scrive sopra l'indirizzo e la porta del destinatario, e lo **spedisce**. Il destinatario, se è in ascolto, **riceve** il pacchetto. Non c'è `accept`, non c'è un canale che resti aperto, non c'è un `Socket` per client.

> [!TIP]
> **Intuizione — La lettera nella cassetta**
> TCP somiglia a una telefonata: si compone il numero, si stabilisce un collegamento, si parla in continuazione. UDP somiglia alle lettere: ciascuna è una busta chiusa con il suo indirizzo, si imbuca e si spera che arrivi. Due lettere spedite una dopo l'altra possono arrivare in ordine invertito, o una può non arrivare. L'analogia ha un limite: la posta in genere avvisa se non riesce a consegnare, UDP no.

### 19.5.2 `DatagramSocket`

Le due estremità di una comunicazione UDP usano un oggetto `DatagramSocket`, che serve sia per spedire sia per ricevere. Ci sono due modi di crearlo:

```java
DatagramSocket serverSocket = new DatagramSocket(9106);   // server: porta fissa, nota ai client
DatagramSocket clientSocket = new DatagramSocket();       // client: porta scelta dal sistema
```

Il **server** deve dichiarare la propria porta, per essere trovato; il **client** non ne ha bisogno, perché è lui a cercare il server, e il sistema gli assegna una porta libera qualsiasi. Entrambi i costruttori dichiarano `throws SocketException`, che è una sottoclasse di `IOException`.

> [!NOTE]
> **Definizione — `DatagramSocket`**
> `public DatagramSocket(int port) throws SocketException` crea un socket UDP legato alla porta indicata.
> `public DatagramSocket() throws SocketException` ne crea uno legato a una porta libera qualsiasi.
> `public void send(DatagramPacket p) throws IOException` spedisce un pacchetto.
> `public void receive(DatagramPacket p) throws IOException` attende un pacchetto e ne riempie `p`.
> `public void close()` chiude il socket (non dichiara eccezioni).

Un `DatagramSocket` è **un'estremità**: un server UDP usa un solo `DatagramSocket` per ricevere i pacchetti di tutti i client, a differenza del TCP dove ogni client ha il suo `Socket`.

### 19.5.3 `DatagramPacket`

Un `DatagramPacket` è il pacchetto: contiene quattro informazioni.

- il **contenuto**, un array di `byte`;
- la **lunghezza** dei dati;
- l'**indirizzo IP** del computer a cui il pacchetto è destinato, oppure da cui è arrivato;
- la **porta** di quel computer.

Il pacchetto si costruisce in due modi, a seconda dell'uso.

```java
// per RICEVERE: un contenitore vuoto, con la sua capacita'
byte[] buffer = new byte[1024];
DatagramPacket inArrivo = new DatagramPacket(buffer, buffer.length);

// per SPEDIRE: dati gia' pronti + a chi mandarli
byte[] dati = "ciao".getBytes();
DatagramPacket inPartenza = new DatagramPacket(dati, dati.length, indirizzo, porta);
```

Nel pacchetto **da ricevere** non si scrivono indirizzo e porta: li compila `receive` nel momento in cui il pacchetto arriva, scrivendovi chi ha spedito. Nel pacchetto **da spedire** bisogna invece indicarli: sono la «busta» del destinatario. Si recuperano con `getAddress()` e `getPort()`.

> [!NOTE]
> **Definizione — `DatagramPacket`**
> `public DatagramPacket(byte[] buf, int length)`: pacchetto per ricevere, di capacità `length`.
> `public DatagramPacket(byte[] buf, int length, InetAddress address, int port)`: pacchetto per spedire `length` byte verso l'indirizzo e la porta indicati.
> `public byte[] getData()`, `public int getLength()`, `public InetAddress getAddress()`, `public int getPort()`.
> I costruttori non dichiarano eccezioni controllate.

### 19.5.4 `InetAddress`: l'indirizzo del destinatario

Il pacchetto da spedire vuole un indirizzo di tipo `InetAddress`, non una `String`. La classe `InetAddress` rappresenta un indirizzo di rete e **non ha costruttori pubblici**: non si scrive `new InetAddress(...)`. Per ottenerne uno si usa il metodo statico `getByName`:

```java
InetAddress indirizzo = InetAddress.getByName("127.0.0.1");
InetAddress locale = InetAddress.getByName("localhost");
```

`getByName` accetta sia un indirizzo numerico sia un nome di macchina. Dichiara `throws UnknownHostException`, una sottoclasse di `IOException`, che viene lanciata quando il nome non si risolve in un indirizzo. Con un indirizzo numerico scritto per esteso, come `"127.0.0.1"`, il metodo controlla soltanto che il formato sia valido.

Per capire che cosa si ottiene, stampiamo qualche valore. Un `InetAddress` stampato con `println` mostra il nome della macchina (se noto) e l'indirizzo numerico separati da una barra; `getHostAddress()` restituisce solo l'indirizzo, come `String`:

```java
import java.net.InetAddress;

public class ProvaIndirizzo {
    public static void main(String[] args) throws Exception {
        System.out.println(InetAddress.getByName("127.0.0.1"));
        System.out.println(InetAddress.getByName("127.0.0.1").getHostAddress());
        System.out.println(InetAddress.getByName("localhost"));
    }
}
```

```text
/127.0.0.1
127.0.0.1
localhost/127.0.0.1
```

> [!NOTE]
> **Approfondimento esterno — `InetAddress.getByName`**
> La documentazione ufficiale descrive `public static InetAddress getByName(String host) throws UnknownHostException` come «*Determines the IP address of a host, given the host's name*» e precisa che il nome può essere «*a machine name, such as "www.example.com", or a textual representation of its IP address. If a literal IP address is supplied, only the validity of the address format is checked*». Tra le eccezioni elenca `UnknownHostException` («*if no IP address for the host could be found*»).
>
> *Fonte:* [InetAddress (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/InetAddress.html)

### 19.5.5 Spedire e ricevere

Il ciclo di vita di uno scambio UDP si riduce a due metodi.

**Spedire** (lato che parla): si prepara il pacchetto con dati, indirizzo e porta del destinatario e si chiama `send`.

```java
byte[] dati = messaggio.getBytes();                                  // testo -> byte
DatagramPacket pacchetto = new DatagramPacket(dati, dati.length, indirizzo, porta);
socket.send(pacchetto);
```

**Ricevere** (lato che ascolta): si prepara un pacchetto vuoto con un buffer abbastanza grande e si chiama `receive`, che **blocca** finché non arriva un pacchetto e poi riempie il buffer, la lunghezza, l'indirizzo e la porta del mittente.

```java
byte[] buffer = new byte[1024];
DatagramPacket pacchetto = new DatagramPacket(buffer, buffer.length);
socket.receive(pacchetto);                                           // si ferma qui
```

Un server UDP che deve **rispondere** al mittente usa proprio ciò che `receive` ha scritto nel pacchetto ricevuto: `pacchetto.getAddress()` e `pacchetto.getPort()` dicono chi ha scritto, e sono l'indirizzo e la porta da mettere sul pacchetto di risposta. Non serve conoscere in anticipo i client.

### 19.5.6 Da testo a byte e ritorno

Un pacchetto trasporta `byte`, quindi un testo va convertito. Per **spedire**: `messaggio.getBytes()` restituisce l'array di byte della `String`. Per **ricevere**: si ricostruisce la `String` dai byte.

Qui sta la trappola più frequente. L'array che si dà a `receive` è lungo, per esempio, 1024 posti, ma il messaggio arrivato può essere di soli 4 byte (`ciao`): gli altri 1020 posti restano a zero. Il metodo `getData()` restituisce **l'intero array**, non solo la parte riempita. Se si scrive

```java
String testo = new String(pacchetto.getData());                    // SBAGLIATO: 1024 caratteri
```

si ottiene una stringa di 1024 caratteri, in cui dopo `ciao` ci sono 1020 caratteri nulli. La parte valida è lunga `getLength()` byte, e va indicata esplicitamente:

```java
String testo = new String(pacchetto.getData(), 0, pacchetto.getLength());   // CORRETTO
```

Il costruttore `String(byte[], int, int)` prende i byte a partire dalla posizione `0` per `getLength()` byte. Con `ciao` in un buffer da 1024, la prima forma produce una stringa di lunghezza 1024, la seconda una di lunghezza 4 (verificato nell'esecuzione).

> [!NOTE]
> **Approfondimento esterno — `DatagramPacket`: dati, lunghezza, buffer troppo piccolo**
> La documentazione ufficiale dice che `getData()` «*Returns the data buffer. The data received or the data to be sent starts from the offset in the buffer, and runs for length long*» e che `getLength()` «*Returns the length of the data to be sent or the length of the data received*». Per `DatagramSocket.receive` scrive: «*When this method returns, the DatagramPacket's buffer is filled with the data received. The datagram packet also contains the sender's IP address, and the port number on the sender's machine. This method blocks until a datagram is received. The length field of the datagram packet object contains the length of the received message. If the message is longer than the packet's length, the message is truncated*». Il costruttore di invio richiede che «*The length argument must be less than or equal to buf.length*» e lancia `IllegalArgumentException` se non lo è.
>
> *Fonte:* [DatagramPacket (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/DatagramPacket.html) e [DatagramSocket (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/DatagramSocket.html)

Una seconda trappola è il buffer **troppo piccolo**: se arriva un messaggio più lungo del buffer, il messaggio viene **troncato** senza alcun errore. Con un buffer da 4 byte e il messaggio `ciao mondo`, `receive` restituisce normalmente e il pacchetto contiene soltanto `ciao`. Il buffer va quindi dimensionato sul messaggio più lungo atteso.

> [!NOTE]
> **Approfondimento esterno — Conversione testo-byte e *charset***
> La documentazione ufficiale precisa che `String.getBytes()` «*Encodes this String into a sequence of bytes using the platform's default charset*»: la conversione dipende dalla piattaforma. Per i testi d'esame, in caratteri ASCII e accentati comuni, `getBytes()` e `new String(byte[], int, int)` sono sufficienti; chi volesse una conversione indipendente dalla macchina usa le versioni con il *charset* esplicito.
>
> *Fonte:* [String (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html)

### 19.5.7 Un esempio completo: richiesta e risposta

Un server UDP riceve un testo e risponde al mittente con lo stesso testo preceduto da `Ricevuto: `. Il client invia un messaggio e restituisce la risposta, oppure `null` se qualcosa va storto.

#### Esempio — Il server UDP

```java
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class ServerDatagram {
    public static void main(String[] args) throws Exception {
        DatagramSocket socket = new DatagramSocket(9106);
        System.out.println("Server UDP in ascolto");
        byte[] buffer = new byte[1024];
        while (true) {
            DatagramPacket richiesta = new DatagramPacket(buffer, buffer.length);
            socket.receive(richiesta);                                   // bloccante
            String testo = new String(richiesta.getData(), 0, richiesta.getLength());
            System.out.println("Server ha ricevuto: " + testo);

            InetAddress indirizzo = richiesta.getAddress();              // chi ha scritto
            int porta = richiesta.getPort();
            byte[] dati = ("Ricevuto: " + testo).getBytes();
            DatagramPacket risposta = new DatagramPacket(dati, dati.length, indirizzo, porta);
            socket.send(risposta);
        }
    }
}
```

Il `main` dichiara `throws Exception`, comodo per un programma di prova; il server non termina da solo (ciclo infinito). A ogni giro costruisce un pacchetto vuoto, attende, ricostruisce il testo con `getLength()`, legge indirizzo e porta del mittente, prepara la risposta e la spedisce **a quel mittente**.

#### Esempio — Il client UDP

```java
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class ClienteDatagram {
    private String host;
    private int porta;

    public ClienteDatagram(String host, int porta) {
        this.host = host;
        this.porta = porta;
    }

    public String chiedi(String messaggio) {
        DatagramSocket socket = null;
        try {
            socket = new DatagramSocket();                               // porta locale scelta dal sistema
            InetAddress indirizzo = InetAddress.getByName(host);
            byte[] dati = messaggio.getBytes();
            socket.send(new DatagramPacket(dati, dati.length, indirizzo, porta));

            byte[] buffer = new byte[1024];
            DatagramPacket risposta = new DatagramPacket(buffer, buffer.length);
            socket.receive(risposta);                                    // attende la risposta
            return new String(risposta.getData(), 0, risposta.getLength());
        } catch (IOException e) {
            return null;
        } finally {
            if (socket != null) {
                socket.close();
            }
        }
    }

    public static void main(String[] args) {
        ClienteDatagram c = new ClienteDatagram("127.0.0.1", 9106);
        System.out.println(c.chiedi("ciao"));
    }
}
```

Il metodo `chiedi` ha la stessa struttura del metodo `invia` del paragrafo 19.4.4: socket dichiarato fuori dal `try`, tutto il lavoro dentro, `return null;` nel `catch`, chiusura nel `finally` protetta da `!= null`. Due differenze: `DatagramSocket.close()` **non dichiara** eccezioni, quindi nel `finally` basta la chiamata, senza altro `try`/`catch`; e `InetAddress.getByName` lancia `UnknownHostException`, che è una `IOException` e ricade quindi nello stesso `catch`.

Con il server in funzione, il client stampa:

```text
Ricevuto: ciao
```

e il server:

```text
Server UDP in ascolto
Server ha ricevuto: ciao
```

### 19.5.8 Quello che UDP non garantisce

L'esempio funziona perché abbiamo provato client e server sulla stessa macchina, con un server in ascolto. In generale UDP non offre le garanzie del TCP, e tre conseguenze vanno tenute presenti.

- **Perdita e ordine.** Un pacchetto può non arrivare, o arrivare dopo uno spedito più tardi. Un programma serio deve prevederlo; i programmi d'esame, con un solo pacchetto di richiesta e uno di risposta, di solito no.
- **Nessun avviso se il server non c'è.** `send` non fallisce se non c'è nessuno in ascolto: il pacchetto va semplicemente perso. A quel punto `receive` **resta in attesa per sempre**, senza lanciare nulla. Un client UDP il cui server non è avviato si blocca in silenzio.
- **Il messaggio deve stare nel buffer.** Altrimenti viene troncato (paragrafo 19.5.6).

---

## 19.6 Leggere una pagina web con `URL`

Nel [Capitolo 14](14-file-di-testo.md) abbiamo visto che `Scanner` funziona con qualunque sorgente di dati. Una pagina web è una sorgente come un'altra: la classe `URL` rappresenta l'indirizzo di una risorsa su Internet, e il suo metodo `openStream()` apre una connessione e restituisce un `InputStream` da cui leggere i byte della risorsa.

```java
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.Scanner;

public class Pagina {
    public static void main(String[] args) throws IOException {
        URL sito = new URL(args[0]);
        Scanner in = new Scanner(new InputStreamReader(sito.openStream()));
        int n = 0;
        while (in.hasNextLine() && n < 3) {
            System.out.println(in.nextLine());
            n++;
        }
        in.close();
    }
}
```

Il programma riceve l'indirizzo dalla riga di comando, apre il flusso e stampa le prime tre righe. È la stessa struttura che usiamo per un file: `Scanner`, `hasNextLine`, `nextLine`, `close` ([Capitolo 14](14-file-di-testo.md), sezione 14.4.1); cambia solo l'origine, che viene dall'`URL` invece che da un `File`. Con un indirizzo `http://...` si legge una pagina vera; con un indirizzo `file:///` si legge un file locale, e questo permette di provare il programma anche senza rete. Se `/tmp/pagina.txt` contiene

```text
prima riga
seconda riga
terza riga
quarta
```

l'esecuzione con `java Pagina file:///tmp/pagina.txt` stampa

```text
prima riga
seconda riga
terza riga
```

Il costruttore `new URL(String)` dichiara `throws MalformedURLException`, quando il testo non è un indirizzo valido (per esempio manca il protocollo `http:`); `openStream()` dichiara `throws IOException`. `MalformedURLException` è una sottoclasse di `IOException`, per cui basta il `throws IOException` del `main`.

> [!NOTE]
> **Approfondimento esterno — `URL(String)` e `openStream`**
> La documentazione ufficiale descrive `public URL(String spec) throws MalformedURLException` come «*Creates a URL object from the String representation*», con `MalformedURLException` lanciata «*if no protocol is specified, or an unknown protocol is found, or spec is null, or the parsed URL fails to comply with the specific syntax of the associated protocol*». Per `public final InputStream openStream() throws IOException` scrive: «*Opens a connection to this URL and returns an InputStream for reading from that connection*».
>
> *Fonte:* [URL (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/URL.html)

---

## 19.7 Le eccezioni della rete

### 19.7.1 La famiglia di `IOException`

Quasi tutto ciò che può andare storto in rete è un'`IOException` o una sua sottoclasse. Le incontriamo nell'ordine in cui possono capitare.

| Eccezione | Superclasse | Quando succede | Messaggio verificato |
|---|---|---|---|
| `UnknownHostException` | `IOException` | il nome della macchina non si risolve in un indirizzo | `java.net.UnknownHostException: nome.inesistente.invalid` |
| `ConnectException` | `SocketException` | nessun server in ascolto su quella porta (o rifiuto) | `java.net.ConnectException: Connection refused` |
| `BindException` | `SocketException` | la porta del server è già occupata da un altro programma | `java.net.BindException: Address already in use` |
| `SocketException` | `IOException` | problema generico di socket (per esempio socket chiuso) | — |
| `MalformedURLException` | `IOException` | un `URL` costruito con un testo non valido | — |
| `IllegalArgumentException` | `RuntimeException` | una porta fuori dall'intervallo 0-65535, o un pacchetto UDP senza indirizzo | `java.lang.IllegalArgumentException: port out of range:70000` e `java.lang.IllegalArgumentException: Address not set` |

Le prime cinque sono **controllate** ([Capitolo 13](13-eccezioni.md)) perché discendono da `IOException`: il compilatore pretende che vengano catturate o dichiarate. La sesta, `IllegalArgumentException`, è **non controllata**: il compilatore non la richiede e un `catch (IOException e)` **non la prende**.

### 19.7.2 Quale `catch` scrivere

Una traccia d'esame di solito dice «in caso di fallimento della comunicazione il metodo restituisce `null`». È una richiesta ampia: *qualunque* guasto deve portare a `null`. Catturare una singola sottoclasse (per esempio solo `ConnectException`) lascia scoperti gli altri guasti. La scelta più sicura è catturare `IOException`, che li comprende tutti, e `return null;`. Se il codice contiene anche `readObject`, serve in aggiunta un `catch (ClassNotFoundException e)`, che non è una `IOException`.

L'ordine dei `catch` va rispettato ([Capitolo 13](13-eccezioni.md)): una sottoclasse prima della superclasse. Se si vogliono distinguere i casi, `catch (ConnectException e)` va scritto **prima** di `catch (IOException e)`; il contrario non compila, perché il secondo `catch` renderebbe irraggiungibile il primo.

L'`IllegalArgumentException` di una porta non valida è un errore del *programmatore* (una porta come `70000` è un numero sbagliato scritto nel codice), non un guasto di rete: non si cattura, si corregge il numero.

---

## 19.8 Dalla traccia al codice

Le tracce di rete usano un lessico ricorrente, ed ogni espressione corrisponde a una scelta precisa nel codice. La tabella aiuta a decodificarlo.

| La traccia dice… | Si scrive… |
|---|---|
| «un server è già in ascolto e non va scritto» | solo il **client**: niente `ServerSocket`, niente `accept` |
| «coordinate note a priori: host e porta» | l'indirizzo e la porta vanno nel codice o nel costruttore (`new Socket(host, porta)`) |
| «instaura una connessione verso il server» (TCP) | `new Socket(host, porta)` |
| «apre una comunicazione sul protocollo UDP» | `new DatagramSocket()` + `DatagramPacket` + `send`/`receive` |
| «trasmette un messaggio testuale» | `PrintWriter(socket.getOutputStream(), true)` e `println` |
| «trasmette l'oggetto» / «invia» | `ObjectOutputStream` sul **flusso del socket**, `writeObject`, `flush` |
| «attende la risposta» | una lettura che blocca: `readLine`, `readObject` o `receive` |
| «la ricostruisce» (oggetto) | `readObject` e il cast alla classe |
| «la ricostruisce in forma testuale» (UDP) | `new String(p.getData(), 0, p.getLength())` |
| «la restituisce al chiamante» | `return` del valore letto |
| «non sono richiesti costrutti per la ricezione» | **non** aprire il flusso di ingresso e non leggere |
| «in caso di fallimento restituisce `null`» | `catch (IOException e) { return null; }` (e `ClassNotFoundException` se c'è `readObject`) |
| «le variabili d'istanza devono essere private» | `private String host; private int porta;` |
| «il costruttore riceve nell'ordine l'host e la porta» | `public Classe(String host, int porta)`, quell'ordine |

Due letture della traccia sono più delicate delle altre. La prima è la differenza tra **costruttore** e **metodo**: in una delle tracce la connessione veniva stabilita *nel costruttore* («al momento dell'istanza, instauri una connessione»), in altre *nel metodo* («il metodo instaura la connessione»). Fa differenza: nel secondo caso il costruttore si limita a memorizzare host e porta, come nei nostri `ClienteBiglietti` e `ClienteDatagram`. La seconda è **cosa non fare**: se la traccia dice che non servono costrutti per la ricezione, aprire comunque un `BufferedReader` e chiamare `readLine` rende il client dipendente da una risposta che il server non invierà, e lo blocca.

---
## Come esce all'esame

Tre appelli ufficiali hanno proposto un esercizio di rete, tutti nel ruolo di **client** verso un server fornito dalla traccia.

### EXAM2 — Esercizio 2 (13 punti): client TCP che invia un messaggio

- **Cosa chiedeva la traccia.** Una classe `Client` con un costruttore `public Client(String ip, int porta)` che, **al momento dell'istanza**, instaura una connessione verso il server in ascolto su indirizzo e porta dati e **trasmette** un messaggio testuale arbitrario. La traccia precisava che **non erano richiesti costrutti per la ricezione della risposta**.
- **Concetti del capitolo necessari.** `new Socket(host, porta)` (paragrafo 19.2.3), il flusso di uscita avvolto in un `PrintWriter` con *autoflush* (19.2.4), la gestione delle eccezioni controllate (19.7), la chiusura nel `finally` ([Capitolo 13](13-eccezioni.md)).
- **Vincoli letterali imposti.** La firma esatta del costruttore, con `String` e `int` in quell'ordine; la connessione e l'invio **dentro il costruttore**, non in un metodo a parte; nessuna lettura della risposta.

### EXAM3 — Esercizio 3 (13 punti): oggetto serializzato su socket

- **Cosa chiedeva la traccia.** Un server già in ascolto (non da scrivere) che riceve un oggetto, lo rimanda indietro identico sulla stessa connessione e chiude, su indirizzo `127.0.0.1` e porta `5555`. Si chiedeva una classe `Persona` serializzabile (costruttore con nome e cognome nell'ordine, variabili `private`, costante di versione `long` pari a `1`, `toString` nella forma `Persona[Mario Rossi]`) e una classe `Client` con un metodo `invia` che riceve una persona e ne restituisce una: instaura la connessione, **trasmette l'oggetto ricevuto come parametro**, **attende** quello che il server rimanda, lo **ricostruisce** e lo restituisce. In caso di **fallimento** della comunicazione il metodo restituisce `null`.
- **Concetti del capitolo necessari.** Le sezioni 19.4.2-19.4.4 (ordine di apertura dei flussi, struttura del metodo, `null` sul fallimento), `writeObject`/`readObject` con il cast e il `serialVersionUID` ([Capitolo 15](15-stream-binari-e-serializzazione.md), sezioni 15.5 e 15.8), la scelta del flusso del socket al posto del file (sezione 15.11).
- **Vincoli letterali imposti.** Il costruttore con l'ordine dei parametri; tutte le variabili d'istanza `private`; il tipo `long` e il valore `1` della costante; il formato esatto del `toString`; l'oggetto che viaggia **sulla connessione** (non su un file); il valore `null` come esito del fallimento.

### EXAM4 — Esercizio 2 (13 punti): client UDP con risposta

- **Cosa chiedeva la traccia.** Un server UDP già in ascolto su `127.0.0.1`, porta `6666`, che risponde al mittente con un prefisso seguito dal testo ricevuto. Si chiedeva una classe `ClientUDP` con costruttore (host testuale, porta intera, variabili `private`) e un metodo `inviaMessaggio` che riceve un messaggio testuale e restituisce una stringa: apre una comunicazione sul protocollo UDP, **trasmette** il messaggio, **attende** la risposta, la **ricostruisce in forma testuale** e la restituisce; in caso di fallimento restituisce `null`.
- **Concetti del capitolo necessari.** `DatagramSocket`, `DatagramPacket` e `InetAddress` (paragrafi 19.5.2-19.5.4), `send` e `receive` (19.5.5), la conversione tra testo e byte con `getLength()` (19.5.6), il `return null` sul fallimento (19.7.2).
- **Vincoli letterali imposti.** Il costruttore con host e porta nell'ordine indicato; le variabili `private`; il nome esatto del metodo e il tipo di ritorno `String`; la risposta ricostruita con la sola parte valida del buffer, perché l'output atteso mostra il testo senza caratteri in più.

Il filo comune è chiaro: il **server non si scrive**, il **client è un metodo con struttura fissa** (connetti, invia, attendi, ricostruisci, restituisci, `null` se fallisce), e il punteggio dipende dall'aderenza alle firme, all'ordine dei parametri e ai tipi di ritorno indicati.

---

## Scheletri da esame

Questi frammenti sono i minimi da saper scrivere a memoria su un editor senza aiuti. Ciascuno compila così com'è.

### Scheletro 1 — Server TCP che accetta un client

**Quando si usa.** La traccia chiede di scrivere anche il server, o si deve provare un client in locale.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerBase {
    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(5555);           // porta di ascolto
        try {
            Socket socket = server.accept();                    // bloccante: aspetta un client
            try {
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);   // true: autoflush
                String riga = in.readLine();                    // legge una riga (null se il client chiude)
                out.println("Ricevuto: " + riga);               // risponde
            } finally {
                socket.close();
            }
        } finally {
            server.close();
        }
    }
}
```

**Eccezioni e import.** Sei `import` (`BufferedReader`, `IOException`, `InputStreamReader`, `PrintWriter` da `java.io`; `ServerSocket`, `Socket` da `java.net`). `IOException` (controllata) da `ServerSocket`, `accept`, `getInputStream`, `getOutputStream`, `readLine`, `close`: dichiarata con `throws` sul `main`.

### Scheletro 2 — Client TCP che invia un messaggio (senza ricezione)

**Quando si usa.** «Instaura una connessione verso il server e trasmette un messaggio»; la traccia non chiede la risposta.

```java
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class ClienteInvio {
    private String host;
    private int porta;

    public ClienteInvio(String host, int porta) {
        this.host = host;
        this.porta = porta;
    }

    public void invia(String messaggio) {
        Socket socket = null;
        try {
            socket = new Socket(host, porta);                              // connessione
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            out.println(messaggio);                                        // invio, nessuna lettura
        } catch (IOException e) {
            System.out.println("Comunicazione fallita");
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    // niente da fare
                }
            }
        }
    }
}
```

**Variante: connessione e invio nel costruttore.** Se la traccia dice che la connessione avviene «al momento dell'istanza», il lavoro sta nel costruttore, che non restituisce nulla e quindi gestisce l'eccezione al suo interno:

```java
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class ClienteIstanza {
    public ClienteIstanza(String ip, int porta) {
        Socket socket = null;
        try {
            socket = new Socket(ip, porta);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            out.println("messaggio");
        } catch (IOException e) {
            System.out.println("Comunicazione fallita");
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    // niente da fare
                }
            }
        }
    }
}
```

**Eccezioni e import.** `java.io.IOException`, `java.io.PrintWriter`, `java.net.Socket`. `IOException` catturata dentro il metodo (o il costruttore): la firma resta quella richiesta, senza `throws`. Il parametro che arriva come `String ip` va a `new Socket(String, int)`.

### Scheletro 3 — Client TCP con risposta testuale

**Quando si usa.** «Trasmette il messaggio, attende la risposta e la restituisce»; `null` se fallisce.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ClienteTesto {
    private String host;
    private int porta;

    public ClienteTesto(String host, int porta) {
        this.host = host;
        this.porta = porta;
    }

    public String chiedi(String messaggio) {
        Socket socket = null;
        try {
            socket = new Socket(host, porta);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out.println(messaggio);                            // invio
            return in.readLine();                              // attende e restituisce la risposta
        } catch (IOException e) {
            return null;                                       // qualunque guasto: null
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    // niente da fare
                }
            }
        }
    }
}
```

**Eccezioni e import.** Cinque `import`. Un unico `catch (IOException e)` copre `UnknownHostException`, `ConnectException` e gli errori di lettura. Il `return` dentro il `try` non salta il `finally`.

### Scheletro 4 — Client TCP che invia un oggetto e legge la risposta

**Quando si usa.** «Trasmette l'oggetto, attende l'oggetto che il server rimanda, lo ricostruisce e lo restituisce»; `null` se fallisce.

```java
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.net.Socket;

class Prenotazione implements Serializable {
    private static final long serialVersionUID = 1L;           // tipo long, valore richiesto
    private String cliente;
    private int notti;

    public Prenotazione(String cliente, int notti) {
        this.cliente = cliente;
        this.notti = notti;
    }

    public String toString() {
        return "Prenotazione[" + cliente + ", " + notti + "]";
    }
}

public class ClientePrenotazioni {
    public Prenotazione invia(Prenotazione p) {
        Socket socket = null;
        try {
            socket = new Socket("127.0.0.1", 5555);
            ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
            out.flush();                                       // PRIMA l'uscita e il flush...
            ObjectInputStream in = new ObjectInputStream(socket.getInputStream());   // ...poi l'ingresso
            out.writeObject(p);
            out.flush();
            return (Prenotazione) in.readObject();             // cast obbligatorio
        } catch (IOException e) {
            return null;
        } catch (ClassNotFoundException e) {
            return null;
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    // niente da fare
                }
            }
        }
    }
}
```

**Eccezioni e import.** Cinque `import`. `IOException` e `ClassNotFoundException` (entrambe controllate) in due `catch` separati. La classe da spedire realizza `Serializable` e dichiara `serialVersionUID`.

### Scheletro 5 — Client UDP: richiesta e risposta

**Quando si usa.** «Apre una comunicazione sul protocollo UDP, trasmette il messaggio e ne attende la risposta».

```java
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class ClienteUdp {
    private String host;
    private int porta;

    public ClienteUdp(String host, int porta) {
        this.host = host;
        this.porta = porta;
    }

    public String invia(String messaggio) {
        DatagramSocket socket = null;
        try {
            socket = new DatagramSocket();                                   // porta locale libera
            InetAddress indirizzo = InetAddress.getByName(host);
            byte[] dati = messaggio.getBytes();                              // testo -> byte
            socket.send(new DatagramPacket(dati, dati.length, indirizzo, porta));

            byte[] buffer = new byte[1024];
            DatagramPacket risposta = new DatagramPacket(buffer, buffer.length);
            socket.receive(risposta);                                        // bloccante
            return new String(risposta.getData(), 0, risposta.getLength()); // solo la parte valida
        } catch (IOException e) {
            return null;
        } finally {
            if (socket != null) {
                socket.close();                                              // non dichiara eccezioni
            }
        }
    }
}
```

**Eccezioni e import.** Quattro `import` (`IOException` da `java.io`; `DatagramPacket`, `DatagramSocket`, `InetAddress` da `java.net`). `SocketException`, `UnknownHostException` e `IOException` sono tutte `IOException`: un solo `catch`.

### Scheletro 6 — Server UDP che risponde al mittente

**Quando si usa.** Per provare un client UDP in locale, o se la traccia chiede il server.

```java
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class ServerUdp {
    public static void main(String[] args) throws Exception {
        DatagramSocket socket = new DatagramSocket(6666);                    // porta fissa
        byte[] buffer = new byte[1024];
        while (true) {
            DatagramPacket richiesta = new DatagramPacket(buffer, buffer.length);
            socket.receive(richiesta);                                       // bloccante
            String testo = new String(richiesta.getData(), 0, richiesta.getLength());
            byte[] dati = ("Ricevuto: " + testo).getBytes();
            socket.send(new DatagramPacket(dati, dati.length,
                    richiesta.getAddress(), richiesta.getPort()));           // al mittente
        }
    }
}
```

**Eccezioni e import.** Due `import`. `main` dichiara `throws Exception` per brevità; le eccezioni vere sono `SocketException` (costruttore) e `IOException` (`receive`, `send`).

### Scheletro 7 — Server TCP con un thread per client

**Quando si usa.** Il server deve servire più client insieme.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

class Servente implements Runnable {
    private Socket socket;

    Servente(Socket socket) {
        this.socket = socket;
    }

    public void run() {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            String riga = in.readLine();
            while (riga != null) {
                out.println("Ricevuto: " + riga);
                riga = in.readLine();
            }
            socket.close();
        } catch (IOException e) {
            System.out.println("Client perso");
        }
    }
}

public class ServerTanti {
    public static void main(String[] args) throws IOException {
        ServerSocket server = new ServerSocket(5555);
        while (true) {
            Socket socket = server.accept();
            new Thread(new Servente(socket)).start();      // un thread per client
        }
    }
}
```

**Eccezioni e import.** Sei `import`. In `run` l'`IOException` va catturata (la firma di `Runnable.run` non ammette `throws`). Il `main` la dichiara.

---

## Errori tipici

> [!CAUTION]
> **Errore tipico — `PrintWriter` senza *autoflush***
> ```java
> // ERRORE logico: compila ed esegue, ma il testo non parte
> PrintWriter out = new PrintWriter(socket.getOutputStream());
> out.println("ciao");
> String risposta = in.readLine();       // aspetta per sempre
> ```
> Il `println` mette il testo nel buffer del `PrintWriter`, ma senza `autoFlush` il buffer non viene svuotato: i caratteri non partono, l'altro programma non riceve nulla, e il `readLine` che attende la risposta non termina mai. Il programma si blocca senza stampare niente (verificato). Forma corretta: `new PrintWriter(socket.getOutputStream(), true)`, oppure `out.flush()` dopo ogni invio.

> [!CAUTION]
> **Errore tipico — `print` al posto di `println` verso un `readLine`**
> ```java
> // ERRORE logico: nessun a capo, readLine dall'altra parte non finisce
> PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
> out.print("ciao");
> ```
> Con l'*autoflush* attivo, `println`, `printf` e `format` svuotano il buffer, ma `print` **no** (così dice la documentazione). E anche se il testo partisse, `readLine` dall'altra parte attende un a capo che non arriva. Forma corretta: `out.println("ciao");`.

> [!CAUTION]
> **Errore tipico — `readLine` restituisce `null` e non lo si controlla**
> ```java
> // ERRORE a runtime: NullPointerException se il client chiude la connessione
> String riga = in.readLine();
> while (!riga.equals("#")) {
>     out.println("Dal server: " + riga);
>     riga = in.readLine();
> }
> ```
> Quando l'altro lato chiude la connessione, `readLine` restituisce `null` e `riga.equals(...)` lancia `NullPointerException`. Forma corretta: `while (riga != null && !riga.equals("#"))`, oppure `!"#".equals(riga)`.

> [!CAUTION]
> **Errore tipico — Il client parte prima del server, o con la porta sbagliata**
> ```text
> java.net.ConnectException: Connection refused
> ```
> Il client chiede un contatto a una porta su cui nessuno ascolta. Il compilatore non lo vede: è un problema di esecuzione. In un metodo con `catch (IOException e) { return null; }` l'effetto è un `null` inatteso. Il server va avviato **prima** del client, e le due porte devono coincidere.

> [!CAUTION]
> **Errore tipico — Due programmi sulla stessa porta**
> ```java
> // ERRORE a runtime: il secondo ServerSocket sulla stessa porta
> ServerSocket a = new ServerSocket(5555);
> ServerSocket b = new ServerSocket(5555);
> ```
> Una porta appartiene a un solo programma alla volta: il secondo costruttore lancia `java.net.BindException: Address already in use`. Succede anche se si rilancia un server senza aver terminato la copia precedente, o se un client UDP apre un `DatagramSocket(porta)` con la stessa porta di un server che gira sulla stessa macchina: il client deve usare `new DatagramSocket()`, senza porta.

> [!CAUTION]
> **Errore tipico — `ObjectInputStream` aperto per primo da entrambi**
> ```java
> // ERRORE logico: stallo, nessun output
> ObjectInputStream in = new ObjectInputStream(socket.getInputStream());     // aspetta l'intestazione
> ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream()); // mai raggiunto
> ```
> Il costruttore di `ObjectInputStream` attende l'intestazione scritta dal costruttore di `ObjectOutputStream` dell'altro lato; se entrambi i lati cominciano dall'ingresso, nessuno scrive la propria intestazione e i due restano fermi per sempre (verificato: il programma non stampa nulla). Forma corretta: prima `ObjectOutputStream` e `flush()`, poi `ObjectInputStream`.

> [!CAUTION]
> **Errore tipico — Manca il `catch` di `ClassNotFoundException`**
> ```java
> // ERRORE di compilazione
> try {
>     Object o = in.readObject();
> } catch (IOException e) {
>     return null;
> }
> ```
> Il compilatore segnala `error: unreported exception ClassNotFoundException; must be caught or declared to be thrown`: `readObject` dichiara due eccezioni controllate, e `ClassNotFoundException` non è una `IOException`. Un errore di compilazione consuma comunque un'esecuzione. Forma corretta: aggiungere `catch (ClassNotFoundException e) { return null; }`.

> [!CAUTION]
> **Errore tipico — Salvare su file invece di inviare in rete**
> ```java
> // ERRORE di aderenza: la traccia dice "invia al server"
> ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("dati.bin"));
> ```
> Il codice serializza correttamente, ma i byte finiscono su un file locale e non raggiungono nessuno. Il verbo della traccia sceglie il flusso: «invia», «trasmette» chiedono `socket.getOutputStream()`. Forma corretta: `new ObjectOutputStream(socket.getOutputStream())`.

> [!CAUTION]
> **Errore tipico — Mescolare testo e oggetti sulla stessa connessione**
> ```java
> // ERRORE a runtime: un lato scrive righe, l'altro legge oggetti
> out.println("ciao");                                         // lato A: PrintWriter
> ObjectInputStream in = new ObjectInputStream(...);           // lato B: attende un'intestazione
> ```
> L'altro lato non trova l'intestazione di serializzazione e lancia `java.io.StreamCorruptedException: invalid stream header: 6369616F` (i byte della parola `ciao`). Forma corretta: i due lati usano lo stesso tipo di flusso.

> [!CAUTION]
> **Errore tipico — `new String(pacchetto.getData())` senza la lunghezza**
> ```java
> // ERRORE logico: la stringa contiene tutto il buffer
> String testo = new String(pacchetto.getData());
> ```
> `getData()` restituisce l'intero buffer, per esempio 1024 byte, e la parte non riempita contiene zeri. Con `ciao` si ottiene una stringa di 1024 caratteri (verificato) e un confronto con l'output atteso fallisce. Forma corretta: `new String(pacchetto.getData(), 0, pacchetto.getLength())`.

> [!CAUTION]
> **Errore tipico — Buffer UDP troppo piccolo**
> ```java
> // ERRORE logico: il messaggio viene troncato senza errori
> byte[] buffer = new byte[4];
> DatagramPacket p = new DatagramPacket(buffer, buffer.length);
> socket.receive(p);                    // arriva "ciao mondo": p contiene solo "ciao"
> ```
> Se il messaggio è più lungo del buffer, `receive` lo taglia e non segnala nulla (verificato: `ciao` e lunghezza `4`). Forma corretta: un buffer almeno pari al messaggio più lungo atteso, per esempio `new byte[1024]`.

> [!CAUTION]
> **Errore tipico — Pacchetto da spedire senza indirizzo e porta**
> ```java
> // ERRORE a runtime: IllegalArgumentException
> byte[] dati = "ciao".getBytes();
> socket.send(new DatagramPacket(dati, dati.length));    // il costruttore di ricezione
> ```
> Il costruttore a due argomenti crea un pacchetto per **ricevere**; spedirlo lancia `java.lang.IllegalArgumentException: Address not set` (verificato), che non è una `IOException` e un `catch (IOException e)` non la prende. Forma corretta: `new DatagramPacket(dati, dati.length, indirizzo, porta)`.

> [!CAUTION]
> **Errore tipico — Un solo `catch` troppo specifico**
> ```java
> // ERRORE logico: la traccia vuole null in caso di QUALUNQUE fallimento
> try {
>     // ... connessione, invio, risposta ...
> } catch (ConnectException e) {
>     return null;
> }
> ```
> Un host inesistente produce `UnknownHostException`, un guasto in lettura una `SocketException` o una `IOException`: nessuna è una `ConnectException`. Il compilatore stesso protesta per l'eccezione controllata non gestita. Forma corretta: `catch (IOException e)`, che le comprende tutte.

> [!CAUTION]
> **Errore tipico — Leggere la risposta quando non è richiesta**
> ```java
> // ERRORE di aderenza e di esecuzione: la traccia non chiede la ricezione
> out.println(messaggio);
> String risposta = in.readLine();       // il server non risponde: il client si blocca
> ```
> Se la traccia dice che non servono costrutti per la ricezione, il server non è tenuto a rispondere: la lettura aspetta all'infinito (o fino alla chiusura della connessione) e il programma non termina. Forma corretta: nessun `BufferedReader` e nessun `readLine`.

> [!CAUTION]
> **Errore tipico — Chiudere il socket nel `try` invece che nel `finally`**
> ```java
> // ERRORE logico: se readLine lancia, close non viene eseguito
> try {
>     socket = new Socket(host, porta);
>     // ... uso del socket ...
>     socket.close();
> } catch (IOException e) {
>     return null;
> }
> ```
> Se qualcosa lancia prima di `close`, il socket resta aperto. Se la traccia impone un `finally`, la chiusura fuori da esso è anche un errore di aderenza. Forma corretta: la chiusura nel `finally`, con il controllo `socket != null` ([Capitolo 13](13-eccezioni.md), sezione 13.5.3).

> [!CAUTION]
> **Errore tipico — Scrivere il server quando la traccia dice che esiste già**
> ```java
> // ERRORE di aderenza: la traccia fornisce il server in ascolto
> ServerSocket server = new ServerSocket(5555);
> Socket socket = server.accept();
> ```
> Un `ServerSocket` nel client occupa la porta che il server vero sta già usando (`BindException`) o, se il server non gira, aspetta un client che non arriverà. Il client apre un `Socket` verso quella porta: `new Socket(host, porta)`.

---

## Riassunto

Due programmi in rete si parlano con un **client** che cerca e un **server** che ascolta, identificati da un **indirizzo** e da una **porta** (0-65535). Esistono due protocolli: **TCP** crea una connessione affidabile e ordinata, e in Java usa `ServerSocket` (il server, con `accept` che blocca e restituisce un `Socket` per ogni client) e `Socket` (il client, `new Socket(host, porta)`); **UDP** non ha connessione e spedisce pacchetti indipendenti con `DatagramSocket` e `DatagramPacket`. Con TCP ogni socket ha due flussi, `getInputStream()` e `getOutputStream()`, che si avvolgono come i flussi dei file: `PrintWriter(…, true)` e `BufferedReader(new InputStreamReader(…))` per il testo, `ObjectOutputStream` e `ObjectInputStream` per gli oggetti. Il protocollo (chi scrive, chi legge, in che formato) è un accordo tra i due programmi: due lati che leggono per primi restano bloccati. Un server che deve servire più client avvia un thread per ciascuno. Quasi ogni guasto di rete è un'`IOException`, e le tracce d'esame chiedono di restituire `null` in caso di fallimento.

**Concetti chiave**

- **Client e server**: il server ascolta su una porta, il client si collega. Il server va avviato prima.
- **Indirizzo e porta**: l'indirizzo identifica il computer (`127.0.0.1` o `localhost` per la macchina stessa), la porta (0-65535) identifica il servizio; una porta è di un solo programma alla volta.
- **TCP e UDP**: TCP con connessione, flusso continuo, ordine garantito; UDP senza connessione, pacchetti che possono perdersi, arrivare in disordine o duplicati, ma più efficiente.
- **`ServerSocket` e `accept`**: `accept` blocca e restituisce un `Socket` dedicato al client.
- **`Socket`**: un'estremità della connessione; ha un flusso di ingresso e uno di uscita, collegati in modo incrociato.
- **Flussi del socket**: `PrintWriter(…, true)` (con *autoflush*, altrimenti il testo non parte), `BufferedReader` con `readLine` (blocca; `null` a connessione chiusa); chiudere il socket nel `finally`.
- **Server a più client**: `accept` in un ciclo e un thread per ogni `Socket`; i dati condivisi si proteggono con `synchronized`.
- **Oggetti su socket**: stesso `writeObject`/`readObject` dei file, ma sul flusso del socket; si apre prima l'`ObjectOutputStream` e si fa `flush`, poi l'`ObjectInputStream`; `readObject` dichiara anche `ClassNotFoundException`.
- **Datagrammi**: `DatagramSocket` (server con porta, client senza), `DatagramPacket` (dati, lunghezza, indirizzo, porta), `InetAddress.getByName`, `send`, `receive` (blocca); il testo si ricostruisce con `getLength()`, il buffer deve bastare.
- **`URL` e `openStream`**: leggere una pagina web con `Scanner` come un file.
- **Eccezioni**: `UnknownHostException`, `ConnectException`, `BindException`, `SocketException` sono `IOException`; un `catch (IOException)` copre il fallimento; `IllegalArgumentException` non è controllata.
- **Dalla traccia al codice**: «server già in ascolto» significa solo client; «invia» sceglie il flusso del socket; «in caso di fallimento restituisce `null`»; la firma e l'ordine dei parametri alla lettera.

**API essenziali**

| Classe | Elemento | Firma | Eccezioni |
|---|---|---|---|
| `ServerSocket` | costruttore | `public ServerSocket(int port) throws IOException` | `IOException` (`BindException` se occupata); `IllegalArgumentException` |
| `ServerSocket` | `accept` | `public Socket accept() throws IOException` | `IOException`; blocca |
| `ServerSocket` | `close` | `public void close() throws IOException` | `IOException` |
| `Socket` | costruttore | `public Socket(String host, int port) throws UnknownHostException, IOException` | `UnknownHostException`, `IOException` (`ConnectException`); `IllegalArgumentException` |
| `Socket` | `getInputStream` | `public InputStream getInputStream() throws IOException` | `IOException` |
| `Socket` | `getOutputStream` | `public OutputStream getOutputStream() throws IOException` | `IOException` |
| `Socket` | `close` | `public void close() throws IOException` | `IOException`; chiude anche i flussi |
| `PrintWriter` | costruttore | `public PrintWriter(OutputStream out, boolean autoFlush)` | — |
| `BufferedReader` | `readLine` | `public String readLine() throws IOException` | `IOException`; `null` a fine flusso |
| `DatagramSocket` | costruttori | `public DatagramSocket(int port) throws SocketException`, `public DatagramSocket() throws SocketException` | `SocketException` |
| `DatagramSocket` | `send` / `receive` | `public void send(DatagramPacket p) throws IOException`, `public void receive(DatagramPacket p) throws IOException` | `IOException`; `receive` blocca |
| `DatagramSocket` | `close` | `public void close()` | — |
| `DatagramPacket` | costruttori | `public DatagramPacket(byte[] buf, int length)`, `public DatagramPacket(byte[] buf, int length, InetAddress address, int port)` | `IllegalArgumentException` |
| `DatagramPacket` | lettura | `public byte[] getData()`, `public int getLength()`, `public InetAddress getAddress()`, `public int getPort()` | — |
| `InetAddress` | `getByName` | `public static InetAddress getByName(String host) throws UnknownHostException` | `UnknownHostException` |
| `InetAddress` | `getHostAddress` | `public String getHostAddress()` | — |
| `URL` | costruttore | `public URL(String spec) throws MalformedURLException` | `MalformedURLException` |
| `URL` | `openStream` | `public final InputStream openStream() throws IOException` | `IOException` |
| `String` | `getBytes` | `public byte[] getBytes()` | — |
