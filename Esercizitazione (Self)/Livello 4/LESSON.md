# Livello 4: Dati, Input/Output e Interfacce Grafiche (GUI)

## 1. Java File Handling: La classe `File`

Prima di poter leggere o scrivere fisicamente i dati dentro un file, è fondamentale capire come Java rappresenta e gestisce file e cartelle a livello di file system. Questo è il compito della classe `java.io.File`.

### Teoria Fondamentale: Rappresentazione, non Contenuto
Un errore concettuale molto comune è pensare che un oggetto `File` in Java contenga i dati del file stesso (il testo, i byte, le immagini). **Falso.** Un oggetto `File` è semplicemente una *rappresentazione astratta di un percorso* (path) all'interno del sistema operativo. È come un cartello stradale che punta a un indirizzo: il file a quell'indirizzo potrebbe esistere, oppure no.

Tramite i metodi di questa classe possiamo compiere vere e proprie operazioni di "amministrazione", come verificare l'esistenza di un file, crearne uno nuovo (vuoto), eliminare documenti, controllare i permessi di lettura/scrittura o navigare all'interno di intere cartelle (directory).

*Esempio: Operazioni di base sul File System*
```java
import java.io.File;
import java.io.IOException;

public class GestioneFile {
    public static void main(String[] args) {
        // Creiamo un oggetto File. ATTENZIONE: Questo NON crea fisicamente il file sul disco!
        // Crea solo l'oggetto Java che "punta" a quel percorso.
        File mioFile = new File("archivio_dati.txt");
        File miaCartella = new File("CartellaDiTest");

        // 1. Gestione Cartelle (Directory)
        if (!miaCartella.exists()) {
            boolean creata = miaCartella.mkdir(); // mkdir() crea la cartella
            System.out.println("Cartella creata con successo? " + creata);
        }

        // 2. Creazione e Verifica di un File
        try {
            if (mioFile.exists()) {
                System.out.println("Il file esiste già!");
                System.out.println("Percorso assoluto: " + mioFile.getAbsolutePath());
                System.out.println("Dimensione in byte: " + mioFile.length());
                System.out.println("È leggibile? " + mioFile.canRead());
            } else {
                // createNewFile() tenta di creare fisicamente un file vuoto sul disco.
                // Può fallire (es. disco pieno, permessi negati), per questo serve il try-catch.
                boolean fileCreato = mioFile.createNewFile(); 
                if (fileCreato) {
                    System.out.println("Nuovo file vuoto creato fisicamente sul disco.");
                }
            }
        } catch (IOException e) {
            System.err.println("Errore di I/O durante la creazione: " + e.getMessage());
        }

        // 3. Eliminazione (Decommentare per testare)
        // if (mioFile.delete()) {
        //     System.out.println("Il file è stato eliminato definitivamente.");
        // }
    }
}
```

---

## 2. File I/O, Stream e Serializzazione

### Teoria Fondamentale: Il Pattern Decorator e gli Stream
L'architettura I/O (Input/Output) di Java affronta il problema universale di spostare dati dal programma verso il mondo esterno (Hard Disk, Rete, Monitor) e viceversa. Il concetto centrale su cui si fonda questa architettura è lo **Stream** (Flusso). Uno stream va inteso come un nastro trasportatore unidirezionale e continuo di dati. Esistono flussi in entrata, che "pompano" dati dall'esterno verso la RAM (`InputStream` / `Reader`), e flussi in uscita, che drenano dati dalla RAM verso una destinazione (`OutputStream` / `Writer`).

Perché non c'è una singola classe per fare tutto? Perché Java divide rigorosamente l'informazione in due regni:
1. **Byte Streams (Flussi a 8-bit):** Gestiscono i dati crudi nella loro forma nativa binaria. Sono indispensabili per manipolare immagini, file audio, eseguibili o flussi di rete grezzi. Le superclassi di riferimento sono `InputStream` e `OutputStream`.
2. **Character Streams (Flussi a 16-bit):** Sono specializzati nel trattamento del testo umano (caratteri Unicode). Riducono enormemente la fatica del programmatore, occupandosi automaticamente della codifica e decodifica dei caratteri (es. UTF-8). Le superclassi di riferimento sono `Reader` e `Writer`.

> **L'Eleganza del Pattern Decorator nell'I/O:**
> Le API di I/O di Java non offrono "classi magiche" monolitiche. Utilizzano invece un design pattern strutturale chiamato *Decorator*. L'idea è partire da uno stream "grezzo" e basilare (ad esempio `FileReader`, che interagisce col sistema operativo e legge il disco carattere per carattere in modo terribilmente lento) e "incartarlo" (decorarlo) passandolo al costruttore di uno stream di livello superiore e più intelligente (come `BufferedReader`). Quest'ultimo non legge direttamente dal disco, ma preleva pacchetti enormi di dati in blocco dallo stream grezzo, li immagazzina in una memoria temporanea (il buffer in RAM) e ti permette di estrarli riga per riga (tramite l'utilissimo metodo `readLine()`). Questo approccio azzera i colli di bottiglia fisici del disco rigido e rende il design estremamente modulare.

### Lettura e Scrittura di File di Testo (Character Streams)
Trattare file di testo è l'operazione di I/O più comune. L'approccio ortodosso e performante prevede l'uso di stream bufferizzati:
- Per **scrivere**, si combina un `FileWriter` (per l'accesso fisico al file) con un `BufferedWriter` (per le performance) o un `PrintWriter` (che fornisce metodi comodi come `println()`).
- Per **leggere**, si combina un `FileReader` con un `BufferedReader`.

*Esempio 1: Scrivere in un file di testo*
```java
import java.io.*;

public class EsempioScritturaFile {
    public static void main(String[] args) {
        // Il costrutto 'try-with-resources' (le parentesi tonde dopo il try) è imperativo in Java moderno!
        // Esso garantisce che il metodo .close() venga chiamato in automatico alla fine del blocco, 
        // chiudendo le risorse del sistema operativo anche in caso di eccezioni.
        // Il parametro 'true' in FileWriter abilita l'append mode: non sovrascrive, aggiunge in coda.
        try (PrintWriter writer = new PrintWriter(new FileWriter("documento.txt", true))) {
            writer.println("Questa è una riga scritta dal programma Java.");
            writer.println("I Character Stream gestiscono il testo in modo eccellente.");
            System.out.println("Scrittura completata con successo.");
        } catch (IOException e) {
            System.err.println("Impossibile accedere al file: " + e.getMessage());
        }
    }
}
```

*Esempio 2: Leggere da un file di testo*
```java
import java.io.*;

public class EsempioLetturaFile {
    public static void main(String[] args) {
        // Incartiamo il noioso FileReader dentro un BufferedReader ad alte prestazioni.
        try (BufferedReader reader = new BufferedReader(new FileReader("documento.txt"))) {
            String riga;
            // Leggiamo fino a quando readLine() non restituisce null (fine del file - EOF)
            while ((riga = reader.readLine()) != null) {
                System.out.println("Letto dal file: " + riga);
            }
        } catch (FileNotFoundException e) {
            System.err.println("Il file specificato non esiste!");
        } catch (IOException e) {
            System.err.println("Errore durante la lettura: " + e.getMessage());
        }
    }
}
```

### La Serializzazione degli Oggetti (Byte Streams)
E se volessimo salvare l'intero "stato" di un Oggetto in modo che persista dopo la chiusura del programma? Interviene la **Serializzazione**. Essa è un processo chimico-informatico che prende un oggetto vivo nello Heap (con tutti i suoi campi e i relativi valori) e lo "iberna", trasformandolo in una pura sequenza di byte crudi (uno Stream Binario). 

Questa sequenza di byte può essere salvata su disco con un `FileOutputStream` oppure sparata in un socket di rete. Quando ne abbiamo bisogno, possiamo "resuscitare" l'oggetto tramite il processo inverso: la **Deserializzazione**.

Affinché un oggetto sia serializzabile, la sua classe deve esplicitamente implementare l'interfaccia `java.io.Serializable`. Questa è una **Marker Interface**, ossia non contiene alcun metodo da implementare: funge puramente da "timbro" sul passaporto dell'oggetto, autorizzando la JVM a esplorare i suoi campi privati e tradurli in binario.

*Esempio 3: Serializzazione e Deserializzazione di un Prodotto*
```java
import java.io.*;

// La classe Prodotto rappresenta un esempio generico di dato serializzabile
public class Prodotto implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private String nome;
    private double prezzo;
    // 'transient' impedisce la serializzazione di dati sensibili o temporanei
    private transient String codiceFiscaleFornitore; 
    
    public Prodotto(String nome, double prezzo, String codice) { 
        this.nome = nome; 
        this.prezzo = prezzo;
        this.codiceFiscaleFornitore = codice;
    }

    @Override
    public String toString() {
        return "Prodotto: " + nome + " | Prezzo: " + prezzo + "€";
    }
}

public class GestoreMagazzino {
    public static void main(String[] args) {
        Prodotto p = new Prodotto("Smartphone", 599.99, "XYZ123");
        String file = "magazzino.dat";

        // SERIALIZZAZIONE
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(file))) {
            oos.writeObject(p); 
            System.out.println("Prodotto salvato con successo.");
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        // DESERIALIZZAZIONE
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(file))) {
            Prodotto caricato = (Prodotto) ois.readObject();
            System.out.println("Prodotto ricaricato: " + caricato);
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
```

### Best Practices & Errori Comuni
- **Il Memory Leak del Buffer non svuotato:** Se decidi di ignorare il `try-with-resources` e gestisci gli stream manualmente senza chiamare l'indispensabile metodo `.close()` (o almeno `.flush()`) su scrittori come `PrintWriter` o `BufferedWriter`, i dati rimarranno intrappolati nella RAM e il file sul disco risulterà tristemente vuoto. Il `close()` è l'atto che forza lo svuotamento fisico sul disco.
- **La Trappola della `InvalidClassException`:** Come anticipato, se serializzi un oggetto su file, poi chiudi il programma, aggiungi una nuova variabile alla sua classe e riprovi a leggere il vecchio file di salvataggio, il programma esploderà lanciando una `InvalidClassException`. La JVM, per sicurezza, ricalcola un ID basato sulla nuova struttura della classe e, vedendo che non corrisponde a quello salvato nel file, blocca la procedura temendo una compromissione dei dati. Metti *sempre* un `serialVersionUID` statico.
- **L'Errore della Path Relativa:** In un'applicazione standard, passare semplicemente `"documento.txt"` significa dire al programma di cercare il file nella sua *Current Working Directory* (la cartella da cui è stato lanciato il programma, tipicamente la root del progetto). Attenzione che non coincide necessariamente con la cartella dove si trova il file `.java` sorgente!

---

## 3. Interfacce Grafiche (GUI) con Swing

### Teoria Fondamentale: Architettura Swing e il pattern MVC
L'interazione tramite console è limitante. Java offre il framework **Swing** (`javax.swing`), basato su **AWT** (`java.awt`), per creare interfacce moderne. Swing adotta il pattern **MVC (Model-View-Controller)**:
- **Model:** I dati e la logica (es. un oggetto `Prodotto`).
- **View:** La rappresentazione visiva (es. `JFrame`, `JLabel`).
- **Controller:** Il codice che gestisce gli eventi e aggiorna il Model/View (es. `ActionListener`).

Swing è **single-threaded**. Tutte le modifiche grafiche devono avvenire nell'**EDT (Event Dispatch Thread)**. Se blocchi l'EDT con un calcolo pesante, l'interfaccia "congela".

### Componenti e Gerarchia
Un'interfaccia è una gerarchia di contenitori (`Container`) e componenti (`JComponent`):
- **`JFrame`:** La finestra principale. I componenti non vanno aggiunti direttamente al frame, ma al suo **Content Pane** (`frame.getContentPane()`), che funge da tela principale.
- **`JPanel`:** Contenitore intermedio fondamentale. Permette di raggruppare componenti (es. un pannello di bottoni) prima di inserirli nel frame.
- **Componenti Standard:** `JButton` (click), `JLabel` (testo/icone), `JTextField` (input singola riga), `JTextArea` (testo multiriga).

### I Layout Manager (Gestione dello Spazio)
Java usa i Layout Manager per disporre i componenti in modo automatico e responsivo (basato sui **pixel**):
1. **`BorderLayout`:** (Default per `JFrame`). Divide lo spazio in 5 regioni: `NORTH`, `SOUTH`, `EAST`, `WEST` e `CENTER`. Il `CENTER` è l'area più importante: si espande per occupare tutto lo spazio residuo.
2. **`FlowLayout`:** (Default per `JPanel`). Dispone i componenti in riga, uno dopo l'altro. Quando finisce lo spazio, va a capo.
3. **`GridLayout`:** Crea una griglia rigida di celle di dimensioni uguali. Ideale per tastiere numeriche o scacchiere.

---

## 4. Gestione degli Eventi e Dialoghi Utente

### Il Pattern Observer: Sorgenti e Ascoltatori
Il cuore delle GUI è la **Programmazione Guidata dagli Eventi (Event-Driven)**.
- **Event Source:** Il componente che "lancia" (fires) l'evento (es. un `JButton`).
- **Event Listener:** L'oggetto che "cattura" l'evento e reagisce. Deve implementare un'interfaccia specifica come `ActionListener`.

*Best Practice:* Invece di far implementare l'ascoltatore alla classe principale, usa **Classi Interne (Inner Classes)** o **Classi Anonime**. Questo mantiene il codice pulito e permette all'ascoltatore di accedere facilmente alle variabili private della GUI.

### Dialoghi Rapidi: `JOptionPane`
Per interagire velocemente con l'utente (mostrare errori o chiedere conferme) senza creare nuovi frame, si usa `JOptionPane`:
- `JOptionPane.showMessageDialog(parent, "Messaggio")`: Mostra un avviso.
- `JOptionPane.showConfirmDialog(...)`: Chiede "Sì/No/Annulla".

### Sintassi ed Esempio Completo (Pannello Domotico)
Questo esempio mostra come gestire più componenti e stati diversi in un'unica interfaccia.

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class PannelloDomotico extends JFrame {
    private JLabel statusLuce;
    private boolean luceAccesa = false;

    public PannelloDomotico() {
        super("Smart Home Control");
        setSize(350, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        Container contentPane = getContentPane();
        contentPane.setLayout(new BorderLayout(10, 10));

        // Intestazione
        JLabel titolo = new JLabel("Controllo Luci Soggiorno", SwingConstants.CENTER);
        titolo.setFont(new Font("Arial", Font.BOLD, 16));
        contentPane.add(titolo, BorderLayout.NORTH);

        // Centro: Stato attuale
        statusLuce = new JLabel("STATO: SPENTA", SwingConstants.CENTER);
        statusLuce.setOpaque(true);
        statusLuce.setBackground(Color.DARK_GRAY);
        statusLuce.setForeground(Color.WHITE);
        contentPane.add(statusLuce, BorderLayout.CENTER);

        // Sud: Bottoni
        JPanel pnlBottoni = new JPanel(new FlowLayout());
        JButton btnToggle = new JButton("Accendi/Spegni");
        JButton btnInfo = new JButton("Info Sistema");

        btnToggle.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                luceAccesa = !luceAccesa;
                if (luceAccesa) {
                    statusLuce.setText("STATO: ACCESA");
                    statusLuce.setBackground(Color.YELLOW);
                    statusLuce.setForeground(Color.BLACK);
                } else {
                    statusLuce.setText("STATO: SPENTA");
                    statusLuce.setBackground(Color.DARK_GRAY);
                    statusLuce.setForeground(Color.WHITE);
                }
            }
        });

        btnInfo.addActionListener(e -> {
            JOptionPane.showMessageDialog(this, "Sistema Domotico v1.0\nStato Connessione: OK");
        });

        pnlBottoni.add(btnToggle);
        pnlBottoni.add(btnInfo);
        contentPane.add(pnlBottoni, BorderLayout.SOUTH);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new PannelloDomotico().setVisible(true);
        });
    }
}
```

---

## 5. Oltre Swing: L'Evoluzione con JavaFX

### Cos'è JavaFX?
JavaFX è la piattaforma moderna che sostituisce Swing. Mentre Swing disegna i componenti via software, JavaFX sfrutta l'**accelerazione hardware (GPU)** tramite uno **Scene Graph**.

### Architettura: Stage, Scene e Node
Per capire JavaFX, usa la metafora del teatro:
1. **Stage (Palcoscenico):** Rappresenta la finestra (il `JFrame` di Swing).
2. **Scene (Scena):** Il contenuto visibile. Una finestra può cambiare scena (es. da Menu a Gioco).
3. **Node (Nodo):** Ogni elemento della UI (bottoni, immagini, layout) è un nodo nell'albero della scena.

### Separazione con FXML e CSS
A differenza di Swing, JavaFX permette di separare nettamente l'estetica dalla logica:
- **FXML:** Un file XML per definire la struttura della UI.
- **CSS:** Supporto completo ai fogli di stile per definire colori e bordi.
- **Controller:** Classe Java che gestisce solo il comportamento (metodi `@FXML`).

> **Swing vs JavaFX: Quando scegliere?**
> Scegli **Swing** per applicazioni legacy o semplici strumenti interni dove la velocità di sviluppo conta più dell'estetica. Scegli **JavaFX** per applicazioni moderne che richiedono grafiche fluide, animazioni, CSS e una separazione professionale tra UI e logica.