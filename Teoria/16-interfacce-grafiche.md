---
materia: Programmazione a Oggetti
capitolo: 16
titolo: Interfacce grafiche
livello_syllabus: 4
stato: completo
slide: ["Savitch cap. 16 slide 3-42", "JavaFX (Deitel cap. 12) slide 7-98"]
appelli: []
fonti_esterne: 13
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 16 — Interfacce grafiche

## Di cosa parla questo capitolo

Fino a qui i nostri programmi hanno parlato con l'utente attraverso la console: il programma scrive righe di testo, l'utente risponde digitando righe di testo, e a comandare è sempre il programma, che decide quando fare la prossima domanda. Le applicazioni che usiamo ogni giorno funzionano in modo diverso: mostrano **finestre**, **pulsanti**, **caselle di testo**, e restano in attesa che sia l'utente a fare qualcosa. Un clic su un pulsante, e solo allora, mette in moto un pezzo di codice.

Questo cambia il modo di pensare un programma. Non c'è più un unico flusso che parte dal `main` e arriva in fondo: ci sono **componenti** disposti sullo schermo e **frammenti di codice** che vengono eseguiti quando succede qualcosa. Per scrivere un programma così bastano tre idee, e il capitolo è costruito attorno a loro:

1. come si **costruisce e si mostra una finestra**, e come si dispongono i componenti al suo interno (i *layout manager*);
2. come si **reagisce a un evento**, per esempio al clic su un pulsante, scrivendo un *listener* (*ascoltatore*);
3. come si **legge e si scrive testo** nei componenti, e quindi come si trasformano in numeri le stringhe digitate dall'utente, con tutti i problemi che questa conversione si porta dietro.

In questo capitolo vedremo:

- che cos'è una **interfaccia grafica** (GUI) e che cosa significa **programmazione a eventi**;
- le classi **`JFrame`** e **`JLabel`**, il **content pane**, `setVisible` e i modi per **chiudere** una finestra (`setDefaultCloseOperation`, `WindowAdapter`);
- i tre **layout manager** principali: `BorderLayout`, `FlowLayout`, `GridLayout`;
- **`JButton`**, l'interfaccia **`ActionListener`** e il metodo `actionPerformed`, con le tre forme in cui si scrive un listener (classe della finestra, classe interna, classe anonima);
- lo schema **model–view–controller** (MVC);
- i **pannelli** (`JPanel`) e la **gerarchia** delle classi di Swing;
- **`JTextField`** e **`JTextArea`**, la conversione tra stringhe e numeri e la **`NumberFormatException`**;
- un **cenno a JavaFX**: `Stage`, `Scene`, FXML, controller;
- gli **scheletri** da saper scrivere a memoria e gli errori tipici.

Il capitolo usa quasi tutto ciò che abbiamo studiato prima. Le classi che **estendono** `JFrame` sono l'ereditarietà del [Capitolo 9](09-ereditarieta-e-polimorfismo.md); un listener è una classe che **realizza un'interfaccia** ([Capitolo 10](10-classi-astratte-e-interfacce.md)); le classi interne e anonime dei listener sono nel [Capitolo 11](11-classi-annidate.md); `NumberFormatException` è un'eccezione del [Capitolo 13](13-eccezioni.md); la conversione di una stringa in numero con `parseInt` è nel [Capitolo 2](02-tipi-variabili-operatori.md) e nel [Capitolo 6](06-metodi.md); salvare il contenuto di una casella di testo in un file riprende il [Capitolo 14](14-file-di-testo.md).

> [!IMPORTANT]
> **Nota per l'esame — Interfacce grafiche**
> L'interfaccia grafica fa parte del programma del corso (livello 4), ma negli appelli ufficiali raccolti finora non compare un esercizio con finestre e pulsanti. Gli appunti la trattano comunque per intero, con la stessa cura per le **firme esatte** e per gli `import`, perché è un argomento d'orale e perché il meccanismo degli eventi, le interfacce e le classi anonime che qui si usano tornano in altri capitoli, come `Runnable` nel [Capitolo 17](17-thread.md) e i gestori di eventi di rete.

---

## 16.1 Dalla console alla finestra

### 16.1.1 Che cos'è una GUI

Una **interfaccia grafica** (*Graphical User Interface*, in sigla **GUI**, che si pronuncia "gui") è la parte di un programma con cui l'utente interagisce attraverso elementi visivi invece che attraverso la console. I suoi ingredienti più comuni sono:

- la **finestra** (*window*): una porzione dello schermo in cui il programma disegna ciò che vuole;
- il **menu**: un elenco di scelte;
- il **pulsante** (*button*): un'area su cui si fa clic per scegliere qualcosa.

Un elemento come un pulsante o una casella di testo si chiama **componente** (nelle librerie di Java anche *widget* o *controllo*, in altri sistemi). Una GUI è un insieme di componenti dentro una finestra.

### 16.1.2 Programmazione a eventi

Nei programmi da console il codice dice: "adesso leggo un numero; poi lo elaboro; poi stampo". La GUI funziona al contrario: il programma prepara la finestra e poi **aspetta**. Quando l'utente fa qualcosa, il sistema segnala che è successo qualcosa. Quel "qualcosa" si chiama **evento**.

> [!NOTE]
> **Definizione — Evento, sorgente, listener**
> Un **evento** (*event*) è un **oggetto** che rappresenta un'azione, per esempio il clic su un pulsante. Il componente su cui l'azione avviene è la **sorgente** dell'evento; si dice che la sorgente **genera** o "lancia" (*fires*) l'evento. L'oggetto che deve reagire si chiama **ascoltatore** (*listener*): è registrato presso la sorgente, e quando l'evento si verifica la sorgente invoca un suo metodo, passandogli l'evento. Un programma organizzato così si dice guidato dagli eventi (*event-driven*).

Il meccanismo ha tre passi, che ritroveremo identici in tutto il capitolo:

1. si **crea** il componente (la sorgente) e il listener;
2. si **registra** il listener presso la sorgente, con un metodo il cui nome comincia per `add` e finisce per `Listener`;
3. quando l'evento si verifica, la sorgente **chiama** il metodo del listener.

Dal punto di vista del `main`, tutto questo ha una conseguenza sorprendente: il `main` costruisce la finestra, la mostra e **finisce**; ma il programma non termina, perché resta una finestra aperta che aspetta eventi. Nelle prossime sezioni vedremo anche come si fa a chiuderlo davvero.

### 16.1.3 Le librerie: Swing e AWT, e gli import

Java ha due famiglie di classi per le finestre. La più vecchia, **AWT** (*Abstract Window Toolkit*), vive nel package `java.awt`. La più recente, **Swing**, vive nel package `javax.swing` ed è costruita sopra AWT: le sue classi ereditano da quelle di AWT (lo vedremo nella gerarchia della sezione 16.5.2) e hanno quasi sempre un nome che comincia per `J`: `JFrame`, `JLabel`, `JButton`. In questo capitolo scriviamo programmi con Swing.

I package che servono sono tre, e sono **distinti**:

| Package | Che cosa contiene | Esempi |
|---|---|---|
| `javax.swing` | i componenti Swing | `JFrame`, `JLabel`, `JButton`, `JPanel`, `JTextField`, `JTextArea` |
| `java.awt` | colori, layout manager, classi di AWT | `Color`, `Container`, `BorderLayout`, `FlowLayout`, `GridLayout` |
| `java.awt.event` | gli **eventi** e i **listener** | `ActionEvent`, `ActionListener`, `WindowEvent`, `WindowAdapter` |

Un `import` di un package **non** importa i sotto-package: `import java.awt.*;` non fa conoscere `ActionListener`, che sta in `java.awt.event`. Come negli altri capitoli useremo `import` espliciti, uno per classe, così si vede sempre da dove arriva ogni nome.

### 16.1.4 Le dimensioni si misurano in pixel

Lo schermo è una griglia di puntini, detti **pixel**. Con Swing sia la **dimensione** sia la **posizione** degli oggetti sullo schermo si misurano in pixel. La **risoluzione** di uno schermo è il numero di pixel che sa mostrare. Una finestra di 300 pixel di larghezza e 150 di altezza si ottiene con `setSize(300, 150)`; la larghezza viene sempre prima dell'altezza.

---

## 16.2 La prima finestra: `JFrame` e `JLabel`

### 16.2.1 Il programma minimo

Una finestra con un titolo e una riga di testo si costruisce con due classi. **`JFrame`** (`javax.swing`) è la finestra vera e propria, con la barra del titolo e i pulsanti di chiusura. **`JLabel`** (`javax.swing`) è una **etichetta**: un componente che mostra un breve testo e non reagisce a nessun evento dell'utente.

```java
import javax.swing.JFrame;
import javax.swing.JLabel;

public class PrimaFinestra {
    public static void main(String[] args) {
        JFrame finestra = new JFrame("La mia prima finestra"); // titolo nella barra
        finestra.setSize(300, 150);                             // larghezza, altezza in pixel
        finestra.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // il pulsante di chiusura termina il programma
        JLabel etichetta = new JLabel("Ciao dal mondo grafico!");
        finestra.add(etichetta);                                // l'etichetta va dentro la finestra
        finestra.setVisible(true);                              // solo ora la finestra appare
    }
}
```

All'esecuzione si apre una finestra larga 300 pixel e alta 150, con il titolo "La mia prima finestra" nella barra e, in alto, la scritta "Ciao dal mondo grafico!". La console resta vuota. Chiudendo la finestra con il pulsante della barra il programma termina.

Vediamo il programma riga per riga.

- `new JFrame("La mia prima finestra")` crea l'oggetto finestra. Il costruttore con una `String` imposta il titolo. Esiste anche il costruttore senza argomenti, `new JFrame()`, e il titolo si può impostare dopo con `setTitle(String)`. Subito dopo la creazione la finestra è **invisibile**: esiste come oggetto, ma non è sullo schermo.
- `setSize(300, 150)` dà alla finestra la sua dimensione in pixel. Se si dimentica, la finestra ha dimensione 0 per 0 (lo vedremo tra gli errori tipici).
- `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)` decide che cosa succede quando l'utente preme il pulsante di chiusura della finestra (sezione 16.2.4).
- `new JLabel("...")` crea l'etichetta con il suo testo.
- `finestra.add(etichetta)` aggiunge l'etichetta alla finestra. Dietro le quinte l'aggiunta avviene sul *content pane* della finestra (sezione 16.2.2).
- `finestra.setVisible(true)` rende la finestra visibile.

> [!NOTE]
> **Approfondimento esterno — `JFrame`: costruttori, visibilità e `add`**
> La documentazione Java SE 17 descrive `JFrame` come una versione estesa di `java.awt.Frame` che aggiunge il supporto ai componenti di Swing. I costruttori `JFrame()` e `JFrame(String title)` costruiscono una finestra **inizialmente invisibile**; entrambi dichiarano `HeadlessException`, un'eccezione **non controllata** (sottoclasse di `RuntimeException`) che viene lanciata se il programma gira in un ambiente senza schermo, tastiera e mouse. I metodi `add`, `remove` e `setLayout` di `JFrame` sono ridefiniti in modo da **delegare** le chiamate al *content pane*: `frame.add(child)` aggiunge `child` al content pane.
>
> *Fonte:* [JFrame (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/JFrame.html)

### 16.2.2 Il content pane e il colore di sfondo

Una finestra `JFrame` non è un contenitore semplice. È fatta a strati, e lo strato su cui si appoggiano i componenti del programma si chiama **content pane** (*pannello del contenuto*): è la superficie interna della finestra, quella sotto la barra del titolo. Quando scriviamo `finestra.add(etichetta)` la chiamata viene girata al content pane. Si può anche farlo esplicitamente: il metodo `getContentPane()` restituisce un oggetto di tipo `Container` (package `java.awt`) che rappresenta il content pane, ed è la forma esplicita che si incontra più spesso nei programmi.

```java
Container contentPane = finestra.getContentPane(); // il pannello interno della finestra
contentPane.add(etichetta);                        // equivale a finestra.add(etichetta)
```

La forma esplicita serve soprattutto quando si deve agire sul content pane in sé, per esempio per cambiarne il colore. Il programma seguente ha una finestra dallo sfondo blu. È scritto come una **classe derivata da `JFrame`**: lo studieremo meglio nella sezione 16.2.5, per ora basta notare che il costruttore `super("...")` imposta il titolo e che tutto il lavoro si fa nel costruttore.

```java
import java.awt.Color;
import java.awt.Container;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class FinestraColorata extends JFrame {
    public FinestraColorata() {
        super("Finestra colorata");                  // costruttore di JFrame con il titolo
        setSize(300, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        Container contentPane = getContentPane();    // il pannello interno
        contentPane.setBackground(Color.BLUE);       // colore di sfondo
        contentPane.add(new JLabel("Sfondo blu"));
    }

    public static void main(String[] args) {
        FinestraColorata finestra = new FinestraColorata();
        finestra.setVisible(true);
    }
}
```

I colori sono oggetti della classe `Color` (package `java.awt`). La classe offre costanti statiche già pronte: `Color.BLACK`, `Color.BLUE`, `Color.CYAN`, `Color.DARK_GRAY`, `Color.GRAY`, `Color.GREEN`, `Color.LIGHT_GRAY`, `Color.MAGENTA`, `Color.ORANGE`, `Color.PINK`, `Color.RED`, `Color.WHITE`, `Color.YELLOW`. Il metodo `setBackground(Color)` imposta il colore di sfondo di un componente.

> [!WARNING]
> **Attenzione — Il colore va sul content pane**
> Chiamare `setBackground(Color.BLUE)` sulla finestra stessa **non cambia** quello che si vede: i componenti stanno sul content pane, che ha il suo sfondo e copre quello della finestra. Il colore va impostato su `getContentPane()` (o su un pannello, sezione 16.5.1). Lo abbiamo verificato dipingendo il content pane su un'immagine: dopo `finestra.setBackground(Color.BLUE)` il suo colore è rimasto grigio chiaro, mentre dopo `getContentPane().setBackground(Color.BLUE)` è diventato blu.

> [!WARNING]
> **Attenzione — Aggiungere dopo la visualizzazione**
> Quando si aggiunge un componente a un contenitore che è già sullo schermo, la gerarchia va ricontrollata: la documentazione di `Container.add` avverte che, se il contenitore è già stato visualizzato, "la gerarchia deve essere validata" (`validate()`, oppure `revalidate()` su un `JComponent`) perché il nuovo componente appaia. Nei programmi di questo capitolo costruiamo tutta l'interfaccia **prima** di chiamare `setVisible(true)`, e il problema non si pone.

### 16.2.3 `setVisible`

Il metodo `setVisible(boolean)` mostra o nasconde un componente: `true` lo rende visibile, `false` lo nasconde. Non è una prerogativa delle finestre: ogni componente può essere reso visibile o invisibile, e il metodo si chiama **sull'oggetto** da mostrare o nascondere (`finestra.setVisible(true)`, `etichetta.setVisible(false)`).

Per una finestra l'ordine conta per chiarezza, non per correttezza: l'abitudine sana è costruire tutto (titolo, dimensione, componenti) e chiamare `setVisible(true)` come **ultima** istruzione, in modo che l'utente non veda la finestra comporsi a pezzi.

> [!CAUTION]
> **Errore tipico — Dimenticare `setVisible(true)`**
> ```java
> // ERRORE: manca setVisible(true)
> import javax.swing.JFrame;
>
> public class FinestraInvisibile {
>     public static void main(String[] args) {
>         JFrame finestra = new JFrame("Dove sono?");
>         finestra.setSize(300, 150);
>     }
> }
> ```
> Il programma compila ed esegue **senza errori e senza alcun effetto visibile**: la finestra non appare e, poiché non c'è nessuna finestra mostrata, il programma termina subito. Forma corretta: aggiungere `finestra.setVisible(true);` in fondo al `main` (o al costruttore del chiamante).

### 16.2.4 Chiudere la finestra

La barra del titolo di una finestra ha un pulsante di chiusura, ma **non è un `JButton`**: è un elemento della finestra stessa, e non lo si aggiunge né lo si programma come un pulsante normale. Che cosa fa il programma quando l'utente lo preme? Per capirlo dobbiamo distinguere tre cose: **nascondere** la finestra, **liberare** le sue risorse (`dispose`) e **terminare** il programma.

Il comportamento è deciso da `setDefaultCloseOperation(int operation)` di `JFrame`, che accetta una di quattro costanti definite in `WindowConstants` (e quindi usabili come `JFrame.NOME`):

| Costante | Che cosa succede alla chiusura |
|---|---|
| `JFrame.DO_NOTHING_ON_CLOSE` | niente: il programma deve gestire la chiusura da sé con un `WindowListener` |
| `JFrame.HIDE_ON_CLOSE` | la finestra viene **nascosta** (è il valore **predefinito**) |
| `JFrame.DISPOSE_ON_CLOSE` | la finestra viene nascosta e le sue risorse vengono liberate |
| `JFrame.EXIT_ON_CLOSE` | il programma **termina** con `System.exit`; da usare solo nelle applicazioni |

La riga della tabella che più sorprende è la seconda. Con il valore predefinito, il pulsante di chiusura **fa sparire la finestra, ma non termina il programma**: la finestra nascosta continua a esistere come oggetto e la JVM resta in vita. Lo abbiamo verificato eseguendo un programma, simulando la chiusura: dopo l'evento la finestra non è più visibile ma ancora "mostrabile", e il processo non finisce. Chi vuole che la chiusura della finestra chiuda il programma deve chiedere `EXIT_ON_CLOSE`, che è l'impostazione che abbiamo usato negli esempi.

> [!NOTE]
> **Approfondimento esterno — `setDefaultCloseOperation`**
> La documentazione descrive le quattro scelte così: `DO_NOTHING_ON_CLOSE` non fa nulla e richiede che il programma gestisca l'operazione nel metodo `windowClosing` di un `WindowListener` registrato; `HIDE_ON_CLOSE` nasconde automaticamente la finestra dopo aver invocato gli eventuali `WindowListener`; `DISPOSE_ON_CLOSE` la nasconde e ne libera le risorse; `EXIT_ON_CLOSE` esce dall'applicazione con il metodo `System.exit`, da usare **solo nelle applicazioni**. "Il valore è `HIDE_ON_CLOSE` per impostazione predefinita." Inoltre, quando l'ultima finestra visualizzabile della JVM viene liberata, la JVM può terminare.
>
> *Fonte:* [JFrame.setDefaultCloseOperation (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/JFrame.html#setDefaultCloseOperation(int))

**La chiusura con un listener di finestra.**

Prima di `setDefaultCloseOperation`, e ancora oggi in molti programmi, la chiusura si gestiva con un **listener di finestra**. La finestra è anch'essa una sorgente di eventi: quando l'utente tenta di chiuderla, genera un `WindowEvent` e chiama il metodo `windowClosing` dei `WindowListener` registrati con `addWindowListener`.

Qui nasce un problema pratico. `WindowListener` (package `java.awt.event`) è un'interfaccia con **sette** metodi, tutti `public abstract`:

| Metodo | Quando viene chiamato |
|---|---|
| `windowOpened(WindowEvent e)` | la finestra viene aperta per la prima volta |
| `windowClosing(WindowEvent e)` | l'utente tenta di chiudere la finestra dal menu di sistema |
| `windowClosed(WindowEvent e)` | la finestra è stata chiusa con `dispose` |
| `windowIconified(WindowEvent e)` | la finestra viene ridotta a icona |
| `windowDeiconified(WindowEvent e)` | la finestra torna da icona a normale |
| `windowActivated(WindowEvent e)` | la finestra diventa quella attiva |
| `windowDeactivated(WindowEvent e)` | la finestra non è più quella attiva |

Una classe che *implementa* l'interfaccia ([Capitolo 10](10-classi-astratte-e-interfacce.md)) deve definirli **tutti e sette**, anche se noi ne vogliamo soltanto uno. Per evitare sei metodi vuoti, la libreria offre la classe astratta **`WindowAdapter`**: realizza `WindowListener` (e altri due listener di finestra) con **tutti i metodi vuoti**. Basta *estendere* `WindowAdapter` e ridefinire solo il metodo che interessa. Un *adapter* ("adattatore") è una classe di comodo di questo tipo: esiste per non dover scrivere i metodi che non servono.

```java
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class ChiusuraConAdapter {
    public static void main(String[] args) {
        JFrame finestra = new JFrame("Chiusura con listener");
        finestra.setSize(300, 100);
        finestra.add(new JLabel("Chiudimi"));
        finestra.addWindowListener(new ChiudiTutto()); // registrazione del listener
        finestra.setVisible(true);
    }
}

// Estende l'adapter: ridefinisce un solo metodo dei sette
class ChiudiTutto extends WindowAdapter {
    public void windowClosing(WindowEvent e) {
        System.out.println("Chiusura richiesta");
        System.exit(0); // termina il programma
    }
}
```

Alla chiusura della finestra la console mostra:

```text
Chiusura richiesta
```

e il programma termina. Notiamo due cose. La classe `ChiudiTutto` non è `public`, perché in un file c'è una sola classe pubblica (quella col `main`). E il metodo `windowClosing` è `public`: la sua firma è ereditata da un'interfaccia, i cui metodi sono sempre pubblici, e una ridefinizione non può essere meno accessibile.

> [!NOTE]
> **Approfondimento esterno — `WindowAdapter`**
> `WindowAdapter` è una classe astratta di comodo per ricevere eventi di finestra: **i suoi metodi sono vuoti**. Esiste per semplificare la creazione di listener: si estende la classe e si ridefiniscono i metodi degli eventi che interessano. Se si implementasse direttamente `WindowListener`, bisognerebbe definire tutti i suoi metodi.
>
> *Fonte:* [WindowAdapter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/awt/event/WindowAdapter.html)

Le due strade equivalgono, per il caso più comune: `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)` è più breve e va preferita quando basta uscire; il `WindowAdapter` serve quando alla chiusura bisogna **fare qualcosa** (stampare, salvare, chiedere conferma) prima di uscire.

### 16.2.5 Una finestra come classe derivata da `JFrame`

Nei primi esempi abbiamo creato un `JFrame` nel `main` e l'abbiamo configurato dall'esterno. Il modo più usato di organizzare un programma grafico è un altro: definire una **classe che estende `JFrame`**, in cui il costruttore fa tutta la configurazione. Questa scelta usa due meccanismi:

- **ereditarietà**: la nostra finestra *è un* `JFrame` (una sua specializzazione), quindi eredita tutti i suoi metodi (`setSize`, `add`, `setVisible`, `getContentPane`…) e li chiama senza scriverne il nome dell'oggetto;
- **contenimento**: la finestra *contiene* altri oggetti Swing (etichette, pulsanti, pannelli), che aggiunge a sé.

Il primo esempio di questo stile è `FinestraColorata` (sezione 16.2.2). Rivediamo i punti importanti, perché sono la struttura di quasi ogni programma grafico del capitolo:

```java
import javax.swing.JFrame;
import javax.swing.JLabel;

public class Saluto extends JFrame {            // ereditarietà: Saluto "è un" JFrame
    public Saluto() {
        super("Saluto");                          // titolo, tramite il costruttore di JFrame
        setSize(250, 100);                        // metodi ereditati, chiamati senza oggetto
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        add(new JLabel("Buongiorno!"));           // contenimento: la finestra contiene l'etichetta
    }

    public static void main(String[] args) {
        Saluto finestra = new Saluto();           // costruisce tutto
        finestra.setVisible(true);                // mostra
    }
}
```

Il `main` è breve: crea l'oggetto e lo rende visibile. Si può anche separare in due classi la finestra e il programma che la usa. In un esercizio d'esame, dove tutto sta in un file con una sola classe pubblica, il `main` si mette di solito nella stessa classe della finestra, come qui, oppure in una classe a parte non pubblica.

> [!TIP]
> **Intuizione — Ereditare o contenere**
> Si eredita da `JFrame` quando la finestra *è* una finestra con comportamenti propri (reagisce a eventi, ha campi propri). Si contiene un `JFrame` in un campo quando serve solo "una finestra" come strumento. Con l'ereditarietà il codice è più compatto perché si scrive `setSize(...)` invece di `finestra.setSize(...)`; con il contenimento si dichiara chiaramente che la finestra è un oggetto separato. In questo capitolo usiamo l'ereditarietà.

### 16.2.6 I metodi di `JFrame` che servono

La tabella raccoglie i metodi che abbiamo già usato o useremo. La colonna centrale dice in quale classe sono dichiarati: `JFrame` eredita da `Frame`, `Window`, `Container` e `Component` (sezione 16.5.2), e molti metodi "di `JFrame`" sono in realtà ereditati.

| Metodo | Dichiarato in | Che cosa fa |
|---|---|---|
| `JFrame()` , `JFrame(String title)` | `JFrame` | costruisce una finestra inizialmente invisibile |
| `void setTitle(String title)` | `Frame` | imposta il titolo nella barra |
| `void setSize(int width, int height)` | `Component` | imposta larghezza e altezza **in pixel** |
| `void pack()` | `Window` | dimensiona la finestra in modo da contenere i componenti alle loro dimensioni preferite |
| `void setVisible(boolean b)` | `Window` | mostra (`true`) o nasconde (`false`) |
| `void setDefaultCloseOperation(int operation)` | `JFrame` | cosa fare alla chiusura (sezione 16.2.4) |
| `Container getContentPane()` | `JFrame` | il pannello interno su cui stanno i componenti |
| `Component add(Component comp)` , `void add(Component comp, Object constraints)` | `Container` | aggiunge un componente (con vincolo di posizione nel secondo caso) |
| `void setLayout(LayoutManager mgr)` | `JFrame` | cambia il layout manager del content pane (sezione 16.3) |
| `void setBackground(Color c)` | `Component` | colore di sfondo (sulla finestra non si vede: sezione 16.2.2) |
| `void addWindowListener(WindowListener l)` | `Window` | registra un listener di finestra |
| `void dispose()` | `Window` | libera le risorse della finestra |
| `void setResizable(boolean resizable)` | `Frame` | permette o vieta il ridimensionamento |

Il metodo `pack()` merita una parola. Invece di fissare con `setSize` una dimensione arbitraria, si può lasciare che sia la finestra a calcolarsi la dimensione minima per contenere i componenti, ciascuno nella sua dimensione preferita; è utile quando non si sa quanto spazio serve.

> [!NOTE]
> **Approfondimento esterno — `Window.pack()`**
> `pack()` fa in modo che la finestra venga dimensionata per adattarsi alla dimensione preferita e ai layout dei suoi sottocomponenti. Se la finestra non è ancora "displayable" (cioè non ha ancora le risorse native), viene resa tale prima di calcolare la dimensione. La finestra viene validata dopo il calcolo.
>
> *Fonte:* [Window.pack() (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/awt/Window.html#pack())

### 16.2.7 Un avvertimento sui thread

C'è un punto della documentazione che i programmi di questo capitolo non rispettano alla lettera, e che è giusto conoscere. In questi esempi la finestra si crea e si mostra direttamente nel `main`, che è la forma più semplice e la più diffusa negli esercizi didattici. La documentazione di Swing, però, dice che Swing "in generale non è *thread safe*": tutti i componenti e le classi collegate devono essere usati nel *thread di distribuzione degli eventi* (*event dispatching thread*), quello in cui girano i listener. Il `main` **non** gira in quel thread. Per costruire e mostrare la GUI la documentazione raccomanda quindi di passare il controllo a quel thread con `SwingUtilities.invokeLater(Runnable)`.

> [!NOTE]
> **Approfondimento esterno — La politica dei thread di Swing**
> "In generale Swing non è thread safe. Tutti i componenti Swing e le classi collegate, salvo diversa indicazione, devono essere usati nell'*event dispatching thread*." Gli eventi generati da un'azione dell'utente (come il clic su un `JButton`) vengono già distribuiti in quel thread, quindi la maggior parte dei programmatori non ne è toccata; l'effetto si sente nella **costruzione e visualizzazione** dell'applicazione, perché `main` non è invocato nell'event dispatching thread. Il modo preferito per passare il controllo è `invokeLater`, che pianifica l'esecuzione di un `Runnable` in quel thread.
>
> *Fonte:* [javax.swing — Swing's Threading Policy (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/package-summary.html)

La forma consigliata dalla documentazione usa una classe anonima che realizza `Runnable` ([Capitolo 10](10-classi-astratte-e-interfacce.md), sezione 10.5, e [Capitolo 11](11-classi-annidate.md), sezione 11.5):

```java
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingUtilities;

public class AvvioConsigliato {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                // Questo codice gira nell'event dispatching thread
                JFrame finestra = new JFrame("Avvio consigliato");
                finestra.setSize(300, 100);
                finestra.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                finestra.add(new JLabel("Costruita nel thread degli eventi"));
                finestra.setVisible(true);
            }
        });
    }
}
```

Il `main` consegna un `Runnable` a `invokeLater`; Swing lo eseguirà quando potrà, nel thread giusto. Che cosa sia un thread, e come due thread possano disturbarsi, si vedrà nel [Capitolo 17](17-thread.md) e nel [Capitolo 18](18-sincronizzazione.md): per ora basta sapere che esiste un modo ufficiale di avviare un programma Swing, e che gli esempi seguenti usano la forma più semplice.

---

## 16.3 Disporre i componenti: i layout manager

### 16.3.1 Chi decide dove va un componente

Aggiungere un componente a un contenitore con `add` non dice **dove** apparirà. In una GUI scritta a mano in Java non si indicano coordinate: si sceglie un **layout manager** (*gestore della disposizione*), un oggetto che dispone i componenti del contenitore secondo una regola e li riposiziona quando la finestra cambia dimensione. Quando si costruisce una GUI con un contenitore Swing, quindi, ci sono **tre tipi di oggetti** di cui occuparsi:

1. il **contenitore** stesso (per esempio il content pane della finestra o un pannello);
2. i **componenti** che si aggiungono al contenitore (etichette, pulsanti, campi di testo…);
3. il **layout manager**, che posiziona i componenti nel contenitore.

Un layout manager si imposta con `setLayout(LayoutManager)` sul contenitore: `setLayout(new FlowLayout())`. I tre più usati sono in `java.awt` e li vediamo uno per uno.

### 16.3.2 `BorderLayout`: cinque regioni

`BorderLayout` divide il contenitore in **cinque regioni**: `NORTH` (in alto), `SOUTH` (in basso), `EAST` (a destra), `WEST` (a sinistra) e `CENTER` (al centro). Ogni regione è identificata da una **costante** di `BorderLayout` (`BorderLayout.NORTH`, ecc., di tipo `String`), e il componente si aggiunge **specificando la regione** come secondo argomento di `add`:

```text
+---------------------------------------+
|                NORTH                  |
+--------+---------------------+--------+
|        |                     |        |
|  WEST  |       CENTER        |  EAST  |
|        |                     |        |
+--------+---------------------+--------+
|                SOUTH                  |
+---------------------------------------+
```

Il programma seguente riempie le cinque regioni con cinque pulsanti.

```java
import java.awt.BorderLayout;
import javax.swing.JButton;
import javax.swing.JFrame;

public class DemoBorder {
    public static void main(String[] args) {
        JFrame finestra = new JFrame("BorderLayout");
        finestra.setSize(400, 300);
        finestra.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        finestra.add(new JButton("Nord"), BorderLayout.NORTH);
        finestra.add(new JButton("Sud"), BorderLayout.SOUTH);
        finestra.add(new JButton("Est"), BorderLayout.EAST);
        finestra.add(new JButton("Ovest"), BorderLayout.WEST);
        finestra.add(new JButton("Centro"), BorderLayout.CENTER);
        finestra.setVisible(true);
    }
}
```

Non abbiamo chiamato `setLayout`: il layout predefinito del content pane di una `JFrame` **è già** `BorderLayout`. Come i componenti si distribuiscono lo abbiamo misurato su una finestra di 400 per 300 pixel (l'area utile è 400 per 272, perché la barra del titolo ne occupa una parte):

- i pulsanti `NORTH` e `SOUTH` occupano **tutta la larghezza** e hanno l'altezza che serve loro (29 pixel);
- `WEST` ed `EAST` occupano tutta l'altezza rimasta, ciascuno con la propria larghezza (75 pixel);
- `CENTER` prende **tutto lo spazio che avanza**, sia in larghezza sia in altezza (250 per 214 pixel).

Per questo il centro è la regione "importante": quando la finestra si ingrandisce, a crescere è il centro. Le altre regioni si adattano al contenuto.

Tre regole da ricordare:

- ogni regione contiene **al massimo un componente**. Se se ne aggiunge un secondo nella stessa regione, quello nuovo **sostituisce** il precedente nella disposizione (e il primo non si vede più). Se serve più di un elemento in una regione, si mette un pannello nella regione e gli elementi nel pannello (sezione 16.5.1);
- `add(componente)` **senza regione**, in un `BorderLayout`, aggiunge il componente al `CENTER`. È questo il motivo per cui nei primi esempi un'etichetta aggiunta con un solo argomento riempiva la finestra;
- se il nome della regione non esiste (per esempio `"Nord"` al posto di `BorderLayout.NORTH`) si ottiene a runtime una `IllegalArgumentException` con il messaggio `cannot add to layout: unknown constraint: Nord`. Usare sempre le **costanti**, non le stringhe scritte a mano.

> [!NOTE]
> **Approfondimento esterno — `BorderLayout`**
> Un `BorderLayout` dispone un contenitore ordinando i componenti in cinque regioni: `NORTH`, `SOUTH`, `EAST`, `WEST` e `CENTER`. **Ogni regione può contenere al più un componente** ed è identificata da una costante corrispondente. I componenti sono disposti secondo le loro dimensioni preferite e i vincoli della dimensione del contenitore: i componenti `NORTH` e `SOUTH` possono essere allargati in orizzontale, quelli `EAST` e `WEST` in verticale, e il componente `CENTER` può allargarsi in entrambe le direzioni per riempire lo spazio rimasto. Il costruttore `BorderLayout()` non lascia spazi tra i componenti; `BorderLayout(int hgap, int vgap)` imposta lo spazio orizzontale e verticale.
>
> *Fonte:* [BorderLayout (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/awt/BorderLayout.html)

### 16.3.3 `FlowLayout`: in fila, a capo quando finisce lo spazio

`FlowLayout` dispone i componenti **uno dopo l'altro**, da sinistra a destra, nell'ordine in cui sono stati aggiunti, come le parole di un paragrafo. Quando la riga è piena, si va a capo. Ogni componente conserva la sua dimensione preferita. È il layout predefinito di `JPanel`.

I costruttori principali sono `FlowLayout()` (allineamento al centro, spazio di 5 pixel tra i componenti sia in orizzontale sia in verticale), `FlowLayout(int align)` con l'allineamento (`FlowLayout.LEFT`, `FlowLayout.CENTER`, `FlowLayout.RIGHT`) e `FlowLayout(int align, int hgap, int vgap)`.

```java
import java.awt.FlowLayout;
import javax.swing.JButton;
import javax.swing.JFrame;

public class DemoFlow {
    public static void main(String[] args) {
        JFrame finestra = new JFrame("FlowLayout");
        finestra.setSize(300, 100);
        finestra.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        finestra.setLayout(new FlowLayout());      // il predefinito del content pane è BorderLayout
        finestra.add(new JButton("Uno"));
        finestra.add(new JButton("Due"));
        finestra.add(new JButton("Tre"));
        finestra.setVisible(true);
    }
}
```

Qui il `setLayout` è necessario, perché senza di esso i tre pulsanti andrebbero tutti nel `CENTER` del `BorderLayout` del content pane, e ne resterebbe visibile uno solo. I tre pulsanti compaiono in fila, centrati, nell'ordine "Uno", "Due", "Tre". Se la finestra viene stretta fino a non contenerli tutti, l'ultimo scende su una seconda riga.

> [!NOTE]
> **Approfondimento esterno — `FlowLayout` e `JPanel`**
> `FlowLayout()` costruisce un layout con allineamento al centro e spazio predefinito di 5 unità, orizzontale e verticale, tra i componenti; `FlowLayout(int align)` fa lo stesso con l'allineamento indicato. Il costruttore `JPanel()` crea un pannello con un `FlowLayout`: è il layout predefinito dei pannelli.
>
> *Fonte:* [FlowLayout (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/awt/FlowLayout.html) — [JPanel (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/JPanel.html)

### 16.3.4 `GridLayout`: una griglia di celle uguali

`GridLayout` divide il contenitore in una **griglia** di righe e colonne e assegna a **tutti** i componenti celle della **stessa dimensione**. I componenti riempiono la griglia **per righe**, da sinistra a destra e dall'alto in basso, nell'ordine di inserimento. È ideale per tastierini numerici e scacchiere.

Il costruttore è `GridLayout(int rows, int cols)`; la versione `GridLayout(int rows, int cols, int hgap, int vgap)` aggiunge gli spazi tra le celle.

```java
import java.awt.GridLayout;
import javax.swing.JButton;
import javax.swing.JFrame;

public class DemoGrid {
    public static void main(String[] args) {
        JFrame finestra = new JFrame("GridLayout");
        finestra.setSize(300, 100);
        finestra.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        finestra.setLayout(new GridLayout(2, 3));       // 2 righe, 3 colonne
        for (int i = 1; i <= 6; i++) {
            finestra.add(new JButton("" + i));          // "" + i: l'int diventa stringa
        }
        finestra.setVisible(true);
    }
}
```

I sei pulsanti si dispongono così, riempiendo la prima riga e poi la seconda:

```text
+-------+-------+-------+
|   1   |   2   |   3   |
+-------+-------+-------+
|   4   |   5   |   6   |
+-------+-------+-------+
```

Su un contenitore di 300 pixel di larghezza e 100 di altezza, ogni cella misura 100 per 50 pixel (lo abbiamo controllato leggendo le posizioni dei componenti). Le celle hanno tutte la stessa dimensione, a prescindere dal contenuto.

Il valore `0` ha un significato speciale: la documentazione dice che **uno solo** tra `rows` e `cols` può essere zero, e allora ci possono essere "quante righe" (o "quante colonne") servono. `new GridLayout(0, 3)` significa "3 colonne e tutte le righe necessarie".

> [!NOTE]
> **Approfondimento esterno — `GridLayout(int rows, int cols)`**
> Crea un layout a griglia con il numero di righe e colonne indicato; a **tutti i componenti** del layout viene data la stessa dimensione. Uno solo tra `rows` e `cols` può essere zero, con il significato di "un numero qualsiasi di oggetti in una riga (o in una colonna)".
>
> *Fonte:* [GridLayout (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/awt/GridLayout.html)

### 16.3.5 Quale layout scegliere

| Layout | Regola | Predefinito di | Quando |
|---|---|---|---|
| `BorderLayout` | cinque regioni, una per componente; il centro prende lo spazio rimasto | content pane di `JFrame` | struttura generale della finestra (barra in alto, area principale, comandi in basso) |
| `FlowLayout` | in fila da sinistra a destra, a capo se non c'è spazio | `JPanel` | gruppi di pulsanti, righe di comandi |
| `GridLayout` | celle uguali per righe e colonne | — | tastierini, tabelle di componenti simili, moduli etichetta-campo |

Nei programmi veri i tre layout si **combinano** annidando pannelli (sezione 16.5.1): una finestra con `BorderLayout`, un pannello a `FlowLayout` nella regione `SOUTH` con i pulsanti e un pannello a `GridLayout` nel `CENTER` con i campi.

---

## 16.4 Pulsanti ed eventi

### 16.4.1 `JButton`

`JButton` (package `javax.swing`) è il pulsante. Si crea con il testo da mostrare, `new JButton("Salva")`, e si aggiunge a un contenitore con `add`, come abbiamo fatto nelle sezioni precedenti. Da solo un pulsante non fa nulla: si disegna, si può premere, ma il programma non lo sa. Per reagire occorre un listener.

Ricordiamo che il pulsante di chiusura della barra del titolo **non è un `JButton`** (sezione 16.2.4): non possiamo registrargli un `ActionListener`.

### 16.4.2 `ActionListener` e `actionPerformed`

Un pulsante, quando viene premuto, genera un **evento di azione** (*action event*), un oggetto della classe `ActionEvent` (package `java.awt.event`). Gli eventi di azione si gestiscono con i **listener di azione**, cioè con oggetti che realizzano l'interfaccia `ActionListener`.

> [!NOTE]
> **Definizione — `ActionListener`**
> `ActionListener` (package `java.awt.event`) è un'interfaccia con un solo metodo:
> `void actionPerformed(ActionEvent e)`.
> Una classe che vuole ricevere gli eventi di azione di un componente **realizza** l'interfaccia (`implements ActionListener`), **definisce** `actionPerformed` e registra un suo oggetto presso il componente con `addActionListener`. Quando l'evento si verifica, il componente chiama `actionPerformed` di quell'oggetto, passando l'`ActionEvent`.

I passi per far reagire un pulsante sono dunque tre:

1. nell'intestazione della classe che ascolterà si aggiunge `implements ActionListener`;
2. si definisce il metodo **`public void actionPerformed(ActionEvent e)`**, che contiene il codice da eseguire a ogni clic;
3. si registra il listener con **`pulsante.addActionListener(listener)`**.

Il metodo deve essere `public` perché in un'interfaccia i metodi sono pubblici e una ridefinizione non può essere meno accessibile ([Capitolo 10](10-classi-astratte-e-interfacce.md)).

Il primo esempio è una finestra con due pulsanti che cambiano il colore dello sfondo, come un semaforo. È la forma più diretta: la **finestra stessa** è il listener, quindi realizza `ActionListener` e passa `this` ad `addActionListener`.

```java
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;

public class Semaforo extends JFrame implements ActionListener {
    public Semaforo() {
        super("Semaforo");
        setSize(300, 120);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        getContentPane().setBackground(Color.GRAY);
        setLayout(new FlowLayout());

        JButton pulsanteRosso = new JButton("Rosso");
        JButton pulsanteVerde = new JButton("Verde");
        pulsanteRosso.addActionListener(this);  // this: la finestra ascolta i clic
        pulsanteVerde.addActionListener(this);
        add(pulsanteRosso);
        add(pulsanteVerde);
    }

    // Chiamato a ogni clic su uno dei due pulsanti
    public void actionPerformed(ActionEvent e) {
        String comando = e.getActionCommand();      // il testo del pulsante premuto
        if (comando.equals("Rosso")) {
            getContentPane().setBackground(Color.RED);
        } else if (comando.equals("Verde")) {
            getContentPane().setBackground(Color.GREEN);
        }
        System.out.println("Comando: " + comando);
    }

    public static void main(String[] args) {
        Semaforo finestra = new Semaforo();
        finestra.setVisible(true);
    }
}
```

All'apertura la finestra ha lo sfondo grigio e due pulsanti in fila. Se l'utente preme "Rosso" e poi "Verde", lo sfondo diventa prima rosso, poi verde, e la console mostra:

```text
Comando: Rosso
Comando: Verde
```

Vediamo il programma passo per passo.

- `class Semaforo extends JFrame implements ActionListener`: la classe estende una finestra e realizza l'interfaccia. L'ordine è sempre `extends` e poi `implements` ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)).
- `pulsanteRosso.addActionListener(this)`: `this` è la finestra, che è un `ActionListener` perché realizza l'interfaccia. Da questo momento i clic del pulsante raggiungono `actionPerformed`.
- `e.getActionCommand()` restituisce una `String` che identifica il comando. Per un `JButton` il comando predefinito è il **testo** del pulsante (lo abbiamo verificato: un `JButton("Ciao")` ha comando `"Ciao"`). Si confrontano stringhe con `equals`, mai con `==` ([Capitolo 3](03-stringhe-e-console.md)).
- Il metodo `main` costruisce la finestra e la mostra, e **finisce**. I clic arrivano dopo, quando la finestra è già sullo schermo: è la programmazione a eventi.

> [!NOTE]
> **Approfondimento esterno — `ActionListener`, `addActionListener` e `getActionCommand`**
> `ActionListener` è l'interfaccia per ricevere eventi di azione. La classe interessata a elaborare un evento di azione la realizza, e l'oggetto creato con quella classe viene registrato presso un componente con il suo metodo `addActionListener`. Quando l'evento di azione si verifica, viene invocato il metodo `actionPerformed(ActionEvent e)` dell'oggetto. `AbstractButton` (la superclasse di `JButton`) ha `addActionListener(ActionListener l)`. `ActionEvent.getActionCommand()` "restituisce la stringa di comando associata a questa azione"; permette a un componente di specificare uno fra più comandi a seconda del proprio stato.
>
> *Fonte:* [ActionListener (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/awt/event/ActionListener.html) — [ActionEvent.getActionCommand (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/awt/event/ActionEvent.html#getActionCommand())

**In una frase.**

In una frase: si scrive una classe che realizza `ActionListener` e definisce `actionPerformed(ActionEvent e)`; se ne registra un oggetto sul pulsante con `addActionListener`; quando il pulsante viene premuto, Swing chiama `actionPerformed` di quell'oggetto, che contiene la reazione.

### 16.4.3 Capire quale pulsante è stato premuto

Quando un solo listener ascolta più pulsanti, `actionPerformed` deve capire **chi** ha generato l'evento. Ci sono due strade, che abbiamo già incontrato o che sono a portata di mano:

- **per comando**: `e.getActionCommand()` restituisce il comando, che per un `JButton` è il suo testo. È la strada del semaforo, comoda ma fragile: se si cambia il testo del pulsante bisogna cambiare anche il confronto;
- **per sorgente**: `e.getSource()` (ereditato da `EventObject`) restituisce l'**oggetto** che ha generato l'evento, di tipo `Object`. Lo si confronta con `==` con i pulsanti memorizzati in campi: `if (e.getSource() == pulsanteRosso)`. Qui `==` è corretto, perché vogliamo sapere se è **lo stesso oggetto** ([Capitolo 8](08-riferimenti-e-memoria.md)). Richiede che i pulsanti siano campi della classe e non variabili locali del costruttore.

### 16.4.4 Dove si scrive il listener: tre forme

Nel semaforo il listener è la finestra, ma non è l'unica possibilità, né la migliore quando i pulsanti sono tanti e hanno compiti diversi: un unico `actionPerformed` con una lunga catena di `if` diventa difficile da leggere. Le alternative sono i due tipi di classe annidata del [Capitolo 11](11-classi-annidate.md).

1. **La finestra è il listener** (`implements ActionListener`, `addActionListener(this)`). Compatta, adatta a pochi pulsanti. Tutti i pulsanti condividono un solo `actionPerformed`.
2. **Una classe interna** (non statica) per ogni compito. Ogni pulsante ha il suo listener, con il suo `actionPerformed`, e la classe interna accede ai campi della finestra, anche `private`, senza nulla da dichiarare ([Capitolo 11](11-classi-annidate.md), sezione 11.2).
3. **Una classe anonima**: si dichiara e si crea il listener nello stesso punto, `new ActionListener() { ... }`, quando serve una volta sola ([Capitolo 11](11-classi-annidate.md), sezione 11.5).

L'esempio seguente fa lavorare le ultime due forme in un solo programma: una finestra con un contatore e due pulsanti. Per "+1" usa una classe interna, per "Azzera" una classe anonima.

```java
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

public class FinestraContatore extends JFrame {
    private int valore = 0;                                   // dato (modello)
    private JLabel visualizzatore = new JLabel("Valore: 0", SwingConstants.CENTER);

    // Classe interna: vede i campi privati della finestra
    private class AscoltaPiuUno implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            valore++;
            visualizzatore.setText("Valore: " + valore);
        }
    }

    public FinestraContatore() {
        super("Contatore");
        setSize(250, 120);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        add(visualizzatore, BorderLayout.CENTER);

        JButton piuUno = new JButton("+1");
        piuUno.addActionListener(new AscoltaPiuUno());        // listener = oggetto della classe interna

        JButton azzera = new JButton("Azzera");
        azzera.addActionListener(new ActionListener() {       // listener = classe anonima
            public void actionPerformed(ActionEvent e) {
                valore = 0;
                visualizzatore.setText("Valore: 0");
            }
        });

        JPanel comandi = new JPanel(new FlowLayout());
        comandi.add(piuUno);
        comandi.add(azzera);
        add(comandi, BorderLayout.SOUTH);
    }

    public static void main(String[] args) {
        FinestraContatore finestra = new FinestraContatore();
        finestra.setVisible(true);
    }
}
```

La finestra mostra al centro "Valore: 0" e in basso i due pulsanti. Premendo tre volte "+1" la scritta diventa "Valore: 3"; premendo "Azzera" torna "Valore: 0". Osserviamo:

- `AscoltaPiuUno` è dichiarata **dentro** `FinestraContatore`, `private` perché nessun altro ne ha bisogno, e modifica `valore` e `visualizzatore` come se fossero suoi;
- la classe anonima fa lo stesso: `new ActionListener() { ... }` dichiara una classe senza nome che realizza l'interfaccia e ne crea subito un oggetto. Il punto e virgola dopo la parentesi chiusa appartiene alla chiamata `addActionListener(...)`;
- il costruttore `new JPanel(new FlowLayout())` crea un pannello con quel layout (sezione 16.5.1).

> [!WARNING]
> **Attenzione — Le variabili locali usate da una classe anonima**
> Una classe anonima (o locale) può usare le **variabili locali** del metodo in cui è dichiarata solo se sono `final` o *effettivamente* `final`, cioè mai riassegnate dopo l'inizializzazione ([Capitolo 11](11-classi-annidate.md), sezione 11.5). I **campi** della classe esterna (come `valore` e `visualizzatore` qui) non hanno questo limite.

### 16.4.5 Il modello MVC

L'esempio del contatore contiene, in piccolo, un'organizzazione che si chiama **model–view–controller** (*modello–vista–controllore*, in sigla **MVC**) e che separa tre ruoli:

> [!NOTE]
> **Definizione — Model–View–Controller**
> Nello schema MVC un'applicazione separa tre parti. Il **modello** (*model*) contiene i **dati** dell'applicazione. La **vista** (*view*) li **presenta** all'utente, cioè è la GUI. Il **controllore** (*controller*) contiene la **logica** che elabora gli input: quando l'utente fa qualcosa, il controllore modifica il modello con il nuovo input, e quando il modello cambia, il controllore aggiorna la vista perché mostri i dati cambiati. In un'applicazione semplice, modello e controllore sono spesso riuniti in una sola classe.

Nel contatore il modello è il campo `valore`, la vista è l'etichetta `visualizzatore` con i pulsanti, il controllore sono i due listener: ciascuno cambia `valore` (aggiorna il modello) e poi riscrive l'etichetta (aggiorna la vista). Il ciclo si può rappresentare così:

```text
   utente --clic--> [ VISTA: pulsanti, etichetta ]
                          |  evento
                          v
                    [ CONTROLLORE: actionPerformed ]
                     |                         ^
          modifica   v                         | aggiorna
                    [ MODELLO: i dati ] -------+
```

Il vantaggio della separazione è che il modello può essere scritto e provato **senza nessuna GUI**. Rifacciamo il contatore con il modello in una classe a sé, `Contatore`, che non conosce Swing:

```java
import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

// MODELLO: solo dati e operazioni, nessun riferimento a Swing
class Contatore {
    private int valore;

    public void incrementa() {
        valore++;
    }

    public void azzera() {
        valore = 0;
    }

    public int getValore() {
        return valore;
    }
}

// VISTA e CONTROLLORE
public class ContatoreMvc extends JFrame implements ActionListener {
    private Contatore modello = new Contatore();
    private JLabel vista = new JLabel("Valore: 0", SwingConstants.CENTER);
    private JButton piu = new JButton("+1");
    private JButton zero = new JButton("Azzera");

    public ContatoreMvc() {
        super("Contatore MVC");
        setSize(250, 120);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        piu.addActionListener(this);
        zero.addActionListener(this);
        add(vista, BorderLayout.CENTER);
        add(piu, BorderLayout.WEST);
        add(zero, BorderLayout.EAST);
    }

    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == piu) {
            modello.incrementa();                       // aggiorna il modello
        } else if (e.getSource() == zero) {
            modello.azzera();
        }
        vista.setText("Valore: " + modello.getValore()); // aggiorna la vista dal modello
    }

    public static void main(String[] args) {
        ContatoreMvc finestra = new ContatoreMvc();
        finestra.setVisible(true);
    }
}
```

Il comportamento è identico al precedente. La differenza è nel progetto: `Contatore` si può provare con un `main` di prova, e la finestra si può cambiare (altri pulsanti, un altro layout) senza toccare i dati. Notiamo che qui, per distinguere i due pulsanti, usiamo `e.getSource() == piu` (sezione 16.4.3) invece del testo.

---

## 16.5 Pannelli e gerarchia delle classi

### 16.5.1 `JPanel`: un contenitore dentro un contenitore

Un **pannello** (`JPanel`, package `javax.swing`) è un **contenitore** usato per raggruppare componenti dentro un contenitore più grande. Ha un colore di sfondo, ha un suo layout manager, e a sua volta si aggiunge alla finestra come se fosse un componente.

La struttura tipica è questa: si crea il pannello, vi si aggiungono i componenti con `add`, e il pannello stesso si aggiunge al content pane con `add`, indicando eventualmente la regione:

```java
JPanel pannelloPulsanti = new JPanel();
pannelloPulsanti.add(pulsanteAvvia);                 // il pulsante va nel pannello
contentPane.add(pannelloPulsanti, BorderLayout.SOUTH); // il pannello va nel content pane
```

I costruttori utili sono `JPanel()`, che crea un pannello con un `FlowLayout`, e `JPanel(LayoutManager layout)`, che crea un pannello con il layout indicato. Il pannello serve a risolvere il limite di `BorderLayout` (un componente per regione): nella regione si mette un pannello, e nel pannello tutti i componenti che si vogliono.

```java
import java.awt.BorderLayout;
import java.awt.Color;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

public class FinestraConPannello extends JFrame {
    public FinestraConPannello() {
        super("Pannello di comandi");
        setSize(300, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel comandi = new JPanel();              // FlowLayout predefinito
        comandi.setBackground(Color.LIGHT_GRAY);    // un pannello ha il suo colore
        comandi.add(new JButton("Avvia"));
        comandi.add(new JButton("Ferma"));

        add(new JLabel("Area principale", SwingConstants.CENTER), BorderLayout.CENTER);
        add(comandi, BorderLayout.SOUTH);           // il pannello occupa una sola regione
    }

    public static void main(String[] args) {
        FinestraConPannello finestra = new FinestraConPannello();
        finestra.setVisible(true);
    }
}
```

La finestra ha, in alto, la scritta "Area principale" al centro e, in basso, una barra grigio chiaro con i due pulsanti "Avvia" e "Ferma" affiancati. Nella regione `SOUTH` c'è **un componente**, il pannello, anche se il pannello ne contiene due.

### 16.5.2 La gerarchia delle classi di Swing

Le classi che abbiamo incontrato non sono slegate: stanno in una gerarchia di ereditarietà ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)). Ricostruirla dalla documentazione serve a capire perché metodi come `setBackground`, `setSize` o `add` si trovano ovunque.

```text
Object
 └── Component                        (java.awt)   ogni cosa che sta sullo schermo
      └── Container                   (java.awt)   un componente che può contenerne altri
           ├── Window                 (java.awt)
           │    └── Frame             (java.awt)
           │         └── JFrame       (javax.swing)   la finestra
           └── JComponent             (javax.swing)   base dei componenti Swing
                ├── JPanel                           pannello
                ├── JLabel                           etichetta
                ├── AbstractButton
                │    └── JButton                     pulsante
                └── JTextComponent   (javax.swing.text)
                     ├── JTextField                  testo su una riga
                     └── JTextArea                   testo su più righe
```

Da questo schema si ricavano le due categorie con cui si classificano le classi di Swing:

- una **classe contenitore** (*container class*) è una discendente di `Container`: può contenere altri componenti e ha `add`. Lo sono `JFrame` (via `Window`), `JPanel` e in realtà anche tutti i `JComponent`, perché `JComponent` estende `Container`;
- una **classe componente** è una discendente di `JComponent`: `JPanel`, `JLabel`, `JButton`, `JTextField`, `JTextArea`.

`JPanel` è dunque al tempo stesso componente (si aggiunge a un contenitore) e contenitore (vi si aggiungono componenti). `JFrame` è un contenitore ma **non** un `JComponent`: discende da `Window`, ed è per questo che il suo `setBackground` ha il comportamento particolare della sezione 16.2.2.

La gerarchia riporta in primo piano il polimorfismo ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)): `add(Component comp)` accetta **qualunque** componente, perché ogni `JButton`, `JLabel` o `JPanel` *è un* `Component`. Per questo si può passare un pulsante, un'etichetta o un pannello allo stesso metodo `add`.

---

## 16.6 Testo e numeri: `JLabel`, `JTextField`, `JTextArea`

### 16.6.1 `JLabel`: un testo da mostrare

`JLabel` mostra un breve testo (o un'immagine, o entrambi) e **non reagisce** agli eventi dell'utente. Si crea con `new JLabel("testo")`; il costruttore `new JLabel("testo", SwingConstants.CENTER)` aggiunge l'allineamento orizzontale (`SwingConstants`, package `javax.swing`). Il testo si legge con `getText()` e si cambia con `setText(String)`: lo abbiamo fatto nel contatore. Un uso classico è l'**etichetta di un campo di testo**: un `JLabel` messo accanto a un campo per dire all'utente che cosa scrivervi.

> [!NOTE]
> **Approfondimento esterno — `JLabel`**
> `JLabel` è un'area di visualizzazione per un breve testo o per un'immagine, o per entrambi. Un'etichetta **non reagisce agli eventi di input**: di conseguenza non può ottenere il focus della tastiera.
>
> *Fonte:* [JLabel (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/JLabel.html)

### 16.6.2 `JTextField`: una riga di testo

`JTextField` (package `javax.swing`) è una casella in cui l'utente scrive **una riga** di testo; serve sia per l'ingresso sia, se non è modificabile, per mostrare un'uscita. I costruttori principali sono:

| Costruttore | Significato |
|---|---|
| `JTextField()` | casella vuota |
| `JTextField(int columns)` | casella vuota con una larghezza di `columns` colonne |
| `JTextField(String text)` | casella con un testo iniziale |
| `JTextField(String text, int columns)` | testo iniziale e larghezza |

Il numero di **colonne** serve a calcolare la **larghezza preferita**: una casella di 10 colonne è larga abbastanza da contenere circa 10 caratteri. I metodi che servono sono quelli di `JTextComponent`, la superclasse comune a `JTextField` e a `JTextArea`:

| Metodo | Firma | Che cosa fa |
|---|---|---|
| `getText` | `String getText()` | restituisce il testo contenuto, **sempre come stringa** |
| `setText` | `void setText(String t)` | sostituisce il testo |
| `setEditable` | `void setEditable(boolean b)` | `false`: l'utente non può modificare il testo (utile per le caselle di uscita) |

> [!NOTE]
> **Approfondimento esterno — `JTextField` e `JTextComponent`**
> `JTextField` è un componente leggero che permette di modificare **una riga di testo**. `JTextField(int columns)` costruisce una casella vuota con il numero di colonne indicato; le colonne servono a calcolare la larghezza preferita (se sono zero, la larghezza preferita è quella che risulta naturalmente dal componente). `getText()` della superclasse `JTextComponent` restituisce il testo contenuto; `setText(String t)` imposta il testo; `setEditable(boolean b)` stabilisce se il componente può essere modificato.
>
> *Fonte:* [JTextField (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/JTextField.html) — [JTextComponent (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/text/JTextComponent.html)

### 16.6.3 `JTextArea`: più righe

`JTextArea` (package `javax.swing`) è l'area di testo su **più righe**. I costruttori sono `JTextArea()`, `JTextArea(String text)`, `JTextArea(int rows, int columns)` e `JTextArea(String text, int rows, int columns)`; righe e colonne fissano le dimensioni preferite (con valori negativi si ha `IllegalArgumentException`). Oltre a `getText`, `setText` e `setEditable` ha `void append(String str)`, che aggiunge testo **in fondo** a quello presente, e `void setLineWrap(boolean wrap)`, che attiva l'andata a capo automatica delle righe troppo lunghe. Una `JTextArea` contiene testo scritto dall'utente o prodotto dal programma.

Un esempio che unisce quanto visto: un piccolo blocco note con un'area di testo e due pulsanti, "Salva" per scrivere il contenuto in un file e "Svuota" per cancellarlo. Il salvataggio usa `PrintWriter` come nel [Capitolo 14](14-file-di-testo.md), con la chiusura nel `finally`.

```java
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextArea;

public class BloccoNote extends JFrame implements ActionListener {
    private JTextArea testo = new JTextArea(8, 30);   // 8 righe, 30 colonne

    public BloccoNote() {
        super("Blocco note");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JButton salva = new JButton("Salva");
        JButton svuota = new JButton("Svuota");
        salva.addActionListener(this);
        svuota.addActionListener(this);

        JPanel comandi = new JPanel(new FlowLayout());
        comandi.add(salva);
        comandi.add(svuota);

        add(testo, BorderLayout.CENTER);
        add(comandi, BorderLayout.SOUTH);
        pack();                                         // dimensione calcolata dai componenti
    }

    public void actionPerformed(ActionEvent e) {
        if (e.getActionCommand().equals("Salva")) {
            PrintWriter out = null;
            try {
                out = new PrintWriter("appunti.txt");  // dichiara FileNotFoundException
                out.print(testo.getText());
                System.out.println("Salvato");
            } catch (FileNotFoundException ex) {
                System.out.println("Impossibile salvare");
            } finally {
                if (out != null) {
                    out.close();
                }
            }
        } else if (e.getActionCommand().equals("Svuota")) {
            testo.setText("");                          // area vuota
        }
    }

    public static void main(String[] args) {
        BloccoNote finestra = new BloccoNote();
        finestra.setVisible(true);
    }
}
```

Se l'utente scrive del testo e preme "Salva", la console mostra:

```text
Salvato
```

e nella cartella di lavoro compare il file `appunti.txt` con il testo digitato. Il bottone "Svuota" lascia l'area vuota. Il programma usa `pack()` invece di `setSize`: la finestra si dimensiona sull'area di testo di 8 righe per 30 colonne e sulla barra dei pulsanti. L'eccezione `FileNotFoundException` è **controllata** ([Capitolo 13](13-eccezioni.md)) e `actionPerformed` non può dichiarare `throws`, perché la firma ereditata dall'interfaccia non lo prevede: l'unica strada è gestirla dentro il metodo con un `try`/`catch`.

> [!NOTE]
> **Approfondimento esterno — `JTextArea`**
> `JTextArea` è un'area che mostra testo semplice su **più righe**. Il costruttore `JTextArea(int rows, int columns)` costruisce un'area vuota con il numero di righe e colonne indicato, e dichiara `IllegalArgumentException` se uno dei due è negativo. `append(String str)` aggiunge il testo indicato in fondo al documento. `setLineWrap(boolean wrap)` imposta la politica di andata a capo.
>
> *Fonte:* [JTextArea (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/javax/swing/JTextArea.html)

### 16.6.4 Numeri come stringhe

Qui c'è il punto che crea più errori nei primi programmi grafici. Con Swing **tutto ciò che entra o esce dallo schermo è una stringa**. Se l'utente scrive `25` in una casella, `getText()` restituisce la `String` `"25"`, non l'`int` 25; e se il programma vuole mostrare un risultato numerico, deve prima convertirlo in `String`. La conversione è compito del programmatore, in entrambe le direzioni:

| Direzione | Come |
|---|---|
| Da stringa a `int` | `Integer.parseInt(campo.getText())` |
| Da stringa a `double` | `Double.parseDouble(campo.getText())` |
| Da numero a stringa | `String.valueOf(numero)`, oppure `"" + numero`, oppure `Integer.toString(n)` |

Questa è la differenza con le variabili che abbiamo sempre usato: `int somma = campoA.getText() + campoB.getText();` non somma nulla, perché `+` tra due stringhe le **concatena** (`"2"` + `"3"` fa `"23"`) e l'assegnazione a un `int` non compila. La conversione con `parseInt` (e `parseDouble`, per i `double`) è nel [Capitolo 6](06-metodi.md), sezione 6.6.

### 16.6.5 Quando la stringa non è un numero: `NumberFormatException`

Cosa succede se l'utente scrive `ciao` dove ci si aspettava un numero, o lascia la casella vuota? `Integer.parseInt("ciao")` lancia una **`NumberFormatException`**, che è una sottoclasse non controllata di `IllegalArgumentException` ([Capitolo 13](13-eccezioni.md)). Siccome è non controllata il compilatore non obbliga a gestirla, e un programma che non lo fa funziona **finché l'utente digita numeri validi**: è il caso di un programma di somma scritto senza alcuna protezione.

La versione che gestisce il caso va scritta con `try`/`catch`: il blocco `try` contiene le conversioni e il calcolo, il `catch (NumberFormatException ex)` mostra un messaggio invece di far fallire il listener.

```java
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

public class Somma extends JFrame implements ActionListener {
    private JTextField campoA = new JTextField(8);
    private JTextField campoB = new JTextField(8);
    private JTextField campoRisultato = new JTextField(8);

    public Somma() {
        super("Somma");
        setSize(300, 160);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridLayout(4, 2, 5, 5));      // 4 righe, 2 colonne, 5 pixel di spazio

        campoRisultato.setEditable(false);           // è un'uscita: l'utente non la modifica
        JButton calcola = new JButton("Somma");
        calcola.addActionListener(this);

        add(new JLabel("Primo numero:"));
        add(campoA);
        add(new JLabel("Secondo numero:"));
        add(campoB);
        add(new JLabel("Risultato:"));
        add(campoRisultato);
        add(new JLabel(""));                         // cella vuota per allineare il pulsante
        add(calcola);
    }

    public void actionPerformed(ActionEvent e) {
        try {
            int a = Integer.parseInt(campoA.getText());    // String -> int
            int b = Integer.parseInt(campoB.getText());
            campoRisultato.setText(String.valueOf(a + b)); // int -> String
        } catch (NumberFormatException ex) {
            campoRisultato.setText("Dato errato");
        }
    }

    public static void main(String[] args) {
        Somma finestra = new Somma();
        finestra.setVisible(true);
    }
}
```

La finestra ha quattro righe di due colonne: etichetta e campo per i due addendi, etichetta e campo (non modificabile) per il risultato, e in fondo il pulsante "Somma". Con `12` e `30` nei due campi il risultato è `42`. Con `12` e `ciao`, oppure con un campo vuoto, il campo del risultato mostra `Dato errato` e il programma continua a funzionare.

Due osservazioni sul comportamento che abbiamo verificato:

- se la `NumberFormatException` non viene catturata, **il programma non si ferma**: la finestra resta aperta e risponde ancora, ma l'eccezione viene stampata in console e la reazione si interrompe a metà. Per questo l'utente non vede nulla cambiare, e chi guarda solo la finestra non capisce che cosa è successo. Gestire l'eccezione serve a dare un riscontro;
- `Integer.parseInt` **non toglie gli spazi**: `Integer.parseInt(" 12 ")` lancia `NumberFormatException` con messaggio `For input string: " 12 "`. Chi digita uno spazio per sbaglio manda in errore un input che sembra corretto. Se vogliamo tollerare gli spazi si usa `campoA.getText().trim()`, `String.trim()` che elimina gli spazi all'inizio e alla fine.

> [!NOTE]
> **Approfondimento esterno — `Integer.parseInt` e `NumberFormatException`**
> `Integer.parseInt(String s)` interpreta l'argomento come un intero decimale con segno. I caratteri della stringa devono essere **tutte cifre decimali**, salvo il primo, che può essere il segno meno `-` oppure il segno più `+`; nessun altro carattere, spazi compresi, è ammesso. Se la stringa non contiene un intero valido, lancia `NumberFormatException`. `NumberFormatException` è "lanciata per indicare che l'applicazione ha tentato di convertire una stringa in uno dei tipi numerici, ma la stringa non ha il formato appropriato"; estende `IllegalArgumentException`.
>
> *Fonte:* [Integer.parseInt (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Integer.html#parseInt(java.lang.String)) — [NumberFormatException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/NumberFormatException.html)

---

## 16.7 Cenni a JavaFX

Swing non è l'unica libreria grafica di Java. **JavaFX** è la libreria che Java propone come API per interfacce grafiche, grafica e multimedia "del futuro". Per l'esame non occorre saperla scrivere a memoria; serve conoscere le idee, che sono molto vicine a quelle di Swing con nomi diversi. Questa sezione ne dà un quadro.

> [!WARNING]
> **Attenzione — JavaFX non è nella JDK 17 standard**
> Le classi di JavaFX (package `javafx.*`) non fanno parte dei moduli della JDK usata per questi appunti e non compaiono nella Javadoc Oracle di Java SE 17: per compilare e lanciare un programma JavaFX bisogna aggiungere le librerie JavaFX al percorso di compilazione e di esecuzione (come fanno gli ambienti di sviluppo, o uno strumento come Maven, [Capitolo 22](22-ecosistema.md)). Gli esempi di questa sezione sono stati compilati con le librerie JavaFX 17.

### 16.7.1 Le parti di una finestra JavaFX

Una finestra JavaFX è fatta di pezzi con nomi precisi.

- I **controlli** (*controls*) sono i componenti della GUI: `Label` (mostra testo), `TextField` (riceve testo), `Button` (avvia un'azione). Stanno nel package `javafx.scene.control`.
- Lo **stage** (*palcoscenico*) è la finestra in cui la GUI viene mostrata: è un oggetto della classe `Stage` (package `javafx.stage`).
- Lo stage contiene una **scena** (*scene*), oggetto della classe `Scene` (package `javafx.scene`), che definisce la GUI come un **grafo della scena** (*scene graph*): un **albero** di elementi visivi (controlli, forme, immagini, testo).
- Ogni elemento del grafo della scena è un **nodo** (*node*), istanza di una sottoclasse di `Node`. Tutti i nodi, tranne il primo (il **nodo radice**, *root node*), hanno un solo genitore.
- I nodi che hanno figli sono in genere **contenitori di layout** (*layout containers*), che dispongono i figli nella scena. Ne vediamo due: `VBox`, che li dispone **in verticale**, dall'alto in basso, e `GridPane`, che li dispone in una griglia di righe e colonne.

Il parallelo con Swing è diretto:

| Swing | JavaFX | Note |
|---|---|---|
| `JFrame` | `Stage` | la finestra |
| content pane / pannello | `Scene` + nodo radice | la superficie della GUI |
| `JLabel`, `JTextField`, `JButton` | `Label`, `TextField`, `Button` | i controlli |
| `BorderLayout`, `FlowLayout`, `GridLayout` | contenitori come `VBox`, `GridPane` | disposizione dei figli |
| `ActionListener.actionPerformed(ActionEvent)` | `EventHandler<ActionEvent>.handle(ActionEvent)` | reazione al clic |

### 16.7.2 Scene Builder e FXML

In JavaFX l'aspetto della GUI si può descrivere **senza scrivere codice Java**. **Scene Builder** è uno strumento visivo autonomo (si può usare anche dentro vari ambienti di sviluppo): si trascinano i componenti da una libreria su un'area di disegno e se ne impostano le proprietà. Lo strumento genera un file **FXML** (*FX Markup Language*): un **vocabolario XML** per definire e disporre i controlli JavaFX ([Capitolo 20](20-xml.md)). Il codice FXML è separato dalla logica del programma, che sta nei sorgenti Java: questa separazione dell'interfaccia dall'implementazione facilita correzione, modifica e manutenzione. È lo schema MVC della sezione 16.4.5: l'FXML è la vista, la classe Java con la logica è il controllore.

Un FXML minimo per una finestra con un'etichetta centrata in un `VBox`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.Label?>
<?import javafx.scene.layout.VBox?>

<VBox alignment="CENTER" prefWidth="450" prefHeight="300"
      xmlns="http://javafx.com/javafx" xmlns:fx="http://javafx.com/fxml">
   <children>
      <Label text="Benvenuti in JavaFX!"/>
   </children>
</VBox>
```

L'elemento radice è il `VBox`, che è il nodo radice del grafo della scena. L'attributo `alignment="CENTER"` centra i figli (in orizzontale e in verticale), e `prefWidth` e `prefHeight` sono la larghezza e l'altezza **preferite** del nodo radice, che la scena usa per dimensionare la finestra all'avvio. L'unico figlio, nell'elemento `children`, è l'etichetta. Ogni valore di proprietà che si imposta su un oggetto JavaFX serve a impostare una variabile d'istanza dell'oggetto quando JavaFX lo crea a runtime.

### 16.7.3 L'avvio: `Application`, `launch` e `start`

Il punto di partenza di un programma JavaFX è una sottoclasse di **`Application`** (package `javafx.application`). Il meccanismo è questo:

1. il `main` chiama il metodo statico `Application.launch(args)`, che inizializza JavaFX;
2. JavaFX crea **un oggetto** della nostra sottoclasse e ne chiama il metodo **`start(Stage stage)`**, passando lo `Stage` della finestra;
3. `start` crea la GUI, la aggancia a una `Scene` e mette la scena sullo stage.

Un programma completo, senza FXML, con la stessa etichetta centrata:

```java
import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class Benvenuto extends Application {
    @Override
    public void start(Stage stage) {
        Label etichetta = new Label("Benvenuti in JavaFX!");
        VBox radice = new VBox(etichetta);       // il nodo radice contiene l'etichetta
        radice.setAlignment(Pos.CENTER);
        Scene scena = new Scene(radice, 450, 300); // la scena ha per radice il VBox
        stage.setTitle("Benvenuto");               // titolo nella barra
        stage.setScene(scena);                     // la scena va sullo stage
        stage.show();                              // la finestra appare
    }

    public static void main(String[] args) {
        Application.launch(args);
    }
}
```

Il `main` non crea nessuna finestra: delega a `launch`. È `start` a costruire e mostrare. Confrontiamolo con Swing: in Swing creavamo il `JFrame` nel `main` e lo mostravamo con `setVisible(true)`; in JavaFX la finestra è lo `Stage` che il sistema ci **consegna**, e si mostra con `show()`.

### 16.7.4 Caricare un FXML: controller, `fx:id` e `@FXML`

Con un FXML, la classe `Application` non costruisce i controlli a mano ma **carica il file**. Il metodo statico `FXMLLoader.load(...)` (package `javafx.fxml`) legge l'FXML, crea il grafo della scena e restituisce un riferimento `Parent` (package `javafx.scene`) al nodo radice. Poi si procede come prima: si crea la `Scene` con la radice, si imposta il titolo, si mette la scena sullo stage, si chiama `show`.

Il codice che reagisce agli eventi sta in una classe a parte, il **controller** (*controllore*), che l'FXML nomina con l'attributo `fx:controller`. Il legame tra FXML e controller si basa su tre elementi:

- **`fx:id`**: un nome assegnato a un controllo nell'FXML, per poterlo manipolare dal codice. La variabile del controller che lo riferisce deve avere **esattamente lo stesso nome**;
- **`@FXML`**: un'annotazione ([Capitolo 9](09-ereditarieta-e-polimorfismo.md), sezione 9.4.2, per le annotazioni) del package `javafx.fxml`, che si mette davanti alle variabili d'istanza del controller che devono riferire i controlli dell'FXML, e ai metodi che possono rispondere agli eventi dei controlli. Quando `FXMLLoader` carica il file, **inizializza** ciascuna variabile `@FXML` in modo che riferisca il componente corrispondente;
- **`onAction="#nomeMetodo"`**: nell'FXML, l'attributo che collega l'azione del pulsante a un metodo del controller.

Costruiamo un esempio completo: un campo di testo, un pulsante e un'etichetta che mostra un saluto.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.Button?>
<?import javafx.scene.control.Label?>
<?import javafx.scene.control.TextField?>
<?import javafx.scene.layout.VBox?>

<VBox alignment="CENTER" spacing="10" prefWidth="300" prefHeight="200"
      xmlns="http://javafx.com/javafx" xmlns:fx="http://javafx.com/fxml"
      fx:controller="SalutoController">
   <children>
      <TextField fx:id="campoNome"/>
      <Button text="Saluta" onAction="#salutaPremuto"/>
      <Label fx:id="etichettaSaluto"/>
   </children>
</VBox>
```

Questo file, salvato come `Saluto.fxml`, descrive tre controlli in verticale. Il `TextField` e il `Label` hanno un `fx:id` perché il codice li manipolerà; il `Button` non ha `fx:id` perché non serve riferirlo, ma ha `onAction="#salutaPremuto"`: quando viene premuto, il metodo `salutaPremuto` del controller sarà chiamato. L'attributo `fx:controller` indica la classe del controller.

```java
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

public class SalutoController {
    @FXML private TextField campoNome;      // stesso nome dell'fx:id
    @FXML private Label etichettaSaluto;    // stesso nome dell'fx:id

    @FXML
    private void salutaPremuto(ActionEvent evento) {  // collegato da onAction="#salutaPremuto"
        etichettaSaluto.setText("Ciao, " + campoNome.getText() + "!");
    }

    @FXML
    public void initialize() {              // chiamato dopo il caricamento, senza parametri
        etichettaSaluto.setText("Scrivi il tuo nome");
    }
}
```

Il controller non estende nulla e non implementa nessuna interfaccia. Il metodo `initialize()`, senza parametri, ha un ruolo speciale: quando `FXMLLoader` crea l'oggetto del controller, se trova un metodo `initialize` senza parametri lo chiama; serve a configurare il controller prima che la GUI sia mostrata.

Non resta che l'applicazione che carica l'FXML:

```java
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class SalutoApp extends Application {
    @Override
    public void start(Stage stage) throws Exception {
        Parent radice = FXMLLoader.load(getClass().getResource("Saluto.fxml")); // legge l'FXML
        Scene scena = new Scene(radice);          // dimensione = quella preferita della radice
        stage.setTitle("Saluto");
        stage.setScene(scena);
        stage.show();
    }

    public static void main(String[] args) {
        Application.launch(args);
    }
}
```

Quando `FXMLLoader.load` legge il file fa quattro cose: restituisce la radice del grafo; **crea un oggetto** del controller nominato nell'FXML; inizializza le variabili `@FXML` dei controlli con `fx:id`; **registra** i gestori di evento specificati nell'FXML, cioè fa sì che il clic sul pulsante chiami `salutaPremuto`. Il file `Saluto.fxml` deve trovarsi nella stessa cartella delle classi compilate, perché `getResource` lo cerca accanto alla classe.

Un gestore di evento di JavaFX è un oggetto che realizza l'interfaccia `EventHandler<ActionEvent>` (package `javafx.event`), il cui unico metodo `handle(ActionEvent)` restituisce `void`. È l'equivalente di `ActionListener`: quando carica l'FXML, `FXMLLoader` crea un oggetto con quell'interfaccia il cui `handle` chiama il metodo che abbiamo indicato con `onAction`.

### 16.7.5 Eventi che si registrano a mano: `ChangeListener`

Non tutti i controlli permettono di scrivere nell'FXML il nome del gestore. Molti controlli hanno **proprietà** (per esempio il valore di un cursore, `Slider`) che generano un evento quando cambiano; per reagire bisogna registrare a mano un oggetto che realizza **`ChangeListener`** (package `javafx.beans.value`), un'interfaccia generica specializzata con il tipo della proprietà. La proprietà del valore di uno `Slider` è un `DoubleProperty`, che è un `ObservableValue<Number>` e ha il metodo `addListener` per registrare un `ChangeListener<Number>`.

Si usa quasi sempre una **classe anonima** ([Capitolo 11](11-classi-annidate.md), sezione 11.5), perché il gestore serve una volta sola. Il metodo da definire è `changed`, che riceve il valore osservabile, il vecchio valore e il nuovo:

```java
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;

public class CursoreController {
    @FXML private Slider cursore;
    @FXML private Label etichettaValore;

    @FXML
    public void initialize() {
        cursore.valueProperty().addListener(new ChangeListener<Number>() {
            @Override
            public void changed(ObservableValue<? extends Number> osservato,
                                Number vecchio, Number nuovo) {
                etichettaValore.setText("Valore: " + nuovo.intValue()); // il nuovo valore
            }
        });
    }
}
```

La lettura è la stessa della sezione 16.4.4: `new ChangeListener<Number>() { ... }` dichiara e crea nello stesso punto una classe anonima che realizza l'interfaccia. Come in Swing, la classe anonima può usare i campi della classe esterna e le variabili locali solo se `final` o effettivamente `final`.

---

## Scheletri da esame

Gli scheletri seguenti sono i frammenti da saper scrivere a memoria su un editor senza aiuti. Il programma del corso li richiede così: una finestra con `JFrame` ed `JLabel`; un pulsante con `ActionListener`; una calcolatrice con `JTextField`, che gestisca la `NumberFormatException`.

### Scheletro 1 — Finestra con un'etichetta e chiusura del programma

*Quando si usa:* è la base di ogni programma grafico: una finestra con titolo e dimensione, che termina il programma alla chiusura.

```java
import javax.swing.JFrame;
import javax.swing.JLabel;

public class Benvenuto extends JFrame {
    public Benvenuto() {
        super("Benvenuto");                                   // titolo
        setSize(300, 120);                                    // larghezza, altezza
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);       // la chiusura termina il programma
        add(new JLabel("Benvenuto nel programma"));           // testo
    }

    public static void main(String[] args) {
        Benvenuto finestra = new Benvenuto();
        finestra.setVisible(true);                            // per ultimo
    }
}
```

Import: `javax.swing.JFrame`, `javax.swing.JLabel`. Nessuna eccezione da dichiarare (`HeadlessException` è non controllata).

### Scheletro 2 — Pulsante con `ActionListener` che modifica un'etichetta

*Quando si usa:* ogni volta che un clic deve cambiare qualcosa nella finestra. Si ricordano tre cose: `implements ActionListener`, `actionPerformed` pubblico, `addActionListener(this)`.

```java
import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

public class ContaClic extends JFrame implements ActionListener {   // 1. implements
    private int clic = 0;
    private JLabel etichetta = new JLabel("Clic: 0", SwingConstants.CENTER);

    public ContaClic() {
        super("Conta clic");
        setSize(250, 120);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        JButton pulsante = new JButton("Premi");
        pulsante.addActionListener(this);                             // 3. registrazione
        add(etichetta, BorderLayout.CENTER);
        add(pulsante, BorderLayout.SOUTH);
    }

    public void actionPerformed(ActionEvent e) {                      // 2. public, parametro ActionEvent
        clic++;
        etichetta.setText("Clic: " + clic);
    }

    public static void main(String[] args) {
        ContaClic finestra = new ContaClic();
        finestra.setVisible(true);
    }
}
```

Import: `java.awt.event.ActionEvent` e `java.awt.event.ActionListener` (da `java.awt.event`, non da `javax.swing`), più le classi Swing e `java.awt.BorderLayout`. Nessuna eccezione da dichiarare.

### Scheletro 3 — Calcolatrice con `JTextField` e `NumberFormatException`

*Quando si usa:* quando l'utente scrive numeri in caselle e il programma li usa. Le conversioni e il calcolo stanno nel `try`; il `catch` della `NumberFormatException` mostra un messaggio.

```java
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

public class Prodotto extends JFrame implements ActionListener {
    private JTextField campoA = new JTextField(6);
    private JTextField campoB = new JTextField(6);
    private JTextField campoRisultato = new JTextField(6);

    public Prodotto() {
        super("Prodotto");
        setSize(260, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridLayout(4, 2, 5, 5));
        campoRisultato.setEditable(false);                  // campo di sola uscita
        JButton calcola = new JButton("Moltiplica");
        calcola.addActionListener(this);
        add(new JLabel("A:"));
        add(campoA);
        add(new JLabel("B:"));
        add(campoB);
        add(new JLabel("Risultato:"));
        add(campoRisultato);
        add(new JLabel(""));
        add(calcola);
    }

    public void actionPerformed(ActionEvent e) {
        try {
            int a = Integer.parseInt(campoA.getText());     // da String a int
            int b = Integer.parseInt(campoB.getText());
            campoRisultato.setText(String.valueOf(a * b));  // da int a String
        } catch (NumberFormatException ex) {
            campoRisultato.setText("Dato errato");
        }
    }

    public static void main(String[] args) {
        Prodotto finestra = new Prodotto();
        finestra.setVisible(true);
    }
}
```

Import: come lo scheletro 2 più `java.awt.GridLayout` e `javax.swing.JTextField`. `NumberFormatException` è in `java.lang` (nessun `import`) ed è non controllata: il `catch` è facoltativo per il compilatore, ma necessario per il comportamento.

### Scheletro 4 — Chiusura con `WindowAdapter`

*Quando si usa:* quando alla chiusura della finestra bisogna fare qualcosa (stampare, salvare) prima di uscire; altrimenti basta `EXIT_ON_CLOSE`.

```java
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class ConArrivederci {
    public static void main(String[] args) {
        JFrame finestra = new JFrame("Arrivederci");
        finestra.setSize(250, 100);
        finestra.add(new JLabel("Chiudimi"));
        finestra.addWindowListener(new Saluta());            // registra il listener di finestra
        finestra.setVisible(true);
    }
}

class Saluta extends WindowAdapter {                        // extends, non implements
    public void windowClosing(WindowEvent e) {              // public; nome e parametro esatti
        System.out.println("Arrivederci");
        System.exit(0);                                      // senza di questa il programma non termina
    }
}
```

Import: `java.awt.event.WindowAdapter` e `java.awt.event.WindowEvent`. Nessuna eccezione da dichiarare.

---

## Errori tipici

> [!CAUTION]
> **Errore tipico — Chiudere la finestra non termina il programma**
> ```java
> // ERRORE: manca setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
> import javax.swing.JFrame;
>
> public class SenzaUscita {
>     public static void main(String[] args) {
>         JFrame finestra = new JFrame("Prova");
>         finestra.setSize(200, 100);
>         finestra.setVisible(true);
>     }
> }
> ```
> Il programma compila e la finestra appare. Ma il pulsante di chiusura la **nasconde soltanto** (il valore predefinito è `HIDE_ON_CLOSE`): il processo resta in esecuzione senza finestra, e il terminale non torna disponibile. Forma corretta: `finestra.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);` oppure un `WindowAdapter` con `System.exit(0)`.

> [!CAUTION]
> **Errore tipico — Dimenticare `setSize` (o `pack`)**
> ```java
> // ERRORE: la finestra non ha dimensione
> JFrame finestra = new JFrame("Prova");
> finestra.add(new JLabel("Ciao"));
> finestra.setVisible(true);
> ```
> Una `JFrame` appena creata ha dimensione **0 per 0**: lo abbiamo verificato. La finestra si apre ridotta alla sola barra del titolo, o non si vede quasi per niente. Forma corretta: `finestra.setSize(300, 150);` oppure `finestra.pack();` prima di `setVisible(true)`.

> [!CAUTION]
> **Errore tipico — Non registrare il listener**
> ```java
> // ERRORE: il pulsante non è mai collegato al listener
> JButton pulsante = new JButton("Premi");
> add(pulsante);               // manca pulsante.addActionListener(this);
> ```
> Il programma compila ed esegue; il pulsante si disegna e si può premere, ma **non succede nulla**, senza alcun messaggio d'errore. È l'errore più difficile da vedere perché non produce segnali: rileggere ogni pulsante verificando che abbia la sua riga `addActionListener`.

> [!CAUTION]
> **Errore tipico — Dichiarare `implements ActionListener` e non definire `actionPerformed`**
> ```java
> // ERRORE: manca actionPerformed
> public class Finestra extends JFrame implements ActionListener {
>     // ...
> }
> ```
> L'interfaccia ha un metodo astratto: la classe che la realizza deve definirlo, altrimenti non compila, con un messaggio come `Finestra is not abstract and does not override abstract method actionPerformed(ActionEvent) in ActionListener`. Forma corretta: aggiungere `public void actionPerformed(ActionEvent e) { ... }`.

> [!CAUTION]
> **Errore tipico — `actionPerformed` senza `public`, o con la firma sbagliata**
> ```java
> // ERRORE 1: senza public
> void actionPerformed(ActionEvent e) { ... }
> // ERRORE 2: parametro diverso da ActionEvent
> public void actionPerformed(String comando) { ... }
> ```
> Nel primo caso il compilatore segnala `actionPerformed(ActionEvent) in Finestra cannot implement actionPerformed(ActionEvent) in ActionListener; attempting to assign weaker access privileges; was public`: i metodi di un'interfaccia sono pubblici e la ridefinizione non può esserlo meno. Nel secondo caso si è scritto un metodo **diverso** (un overloading, non un override) e la classe resta senza il metodo richiesto: stesso errore del caso precedente. Forma corretta: esattamente `public void actionPerformed(ActionEvent e)`. Mettere `@Override` davanti al metodo ([Capitolo 9](09-ereditarieta-e-polimorfismo.md), sezione 9.4.2) fa emergere subito l'errore di firma, con il messaggio `actionPerformed(String) in Finestra does not override or implement a method from a supertype`.

> [!CAUTION]
> **Errore tipico — Importare `javax.swing.*` e non `java.awt.event`**
> ```java
> // ERRORE: mancano gli import dei tipi di evento
> import javax.swing.JButton;
> import javax.swing.JFrame;
>
> public class Finestra extends JFrame implements ActionListener { ... }
> ```
> I tipi `ActionListener` e `ActionEvent` non sono in `javax.swing`: sono in `java.awt.event`. Senza l'import corretto si ha `cannot find symbol` su `ActionListener` e `ActionEvent`. Un `import java.awt.*;` non basta, perché non include i sotto-package. Forma corretta: `import java.awt.event.ActionEvent;` e `import java.awt.event.ActionListener;`.

> [!CAUTION]
> **Errore tipico — Una stringa scritta a mano come regione di `BorderLayout`**
> ```java
> // ERRORE a runtime: la regione non esiste
> add(new JButton("Ok"), "Nord");
> ```
> Il programma compila (il secondo argomento di `add` è un `Object`), ma all'esecuzione lancia `java.lang.IllegalArgumentException: cannot add to layout: unknown constraint: Nord`. Forma corretta: `add(new JButton("Ok"), BorderLayout.NORTH);`, con la costante.

> [!CAUTION]
> **Errore tipico — Due componenti nella stessa regione, o niente `setLayout`**
> ```java
> // ERRORE: tutti finiscono nel CENTER del BorderLayout
> add(new JButton("Uno"));
> add(new JButton("Due"));
> add(new JButton("Tre"));
> ```
> Senza una regione ogni `add` mette il componente nel `CENTER` e **ogni nuovo componente sostituisce il precedente**: si vede soltanto l'ultimo. Forma corretta: scegliere un layout adatto con `setLayout(new FlowLayout())` (o `GridLayout`), oppure assegnare regioni diverse, oppure raggruppare i pulsanti in un `JPanel` e aggiungere il pannello a una regione.

> [!CAUTION]
> **Errore tipico — Trattare `getText()` come un numero**
> ```java
> // ERRORE di compilazione: String non è int
> int a = campoA.getText();
> int somma = campoA.getText() + campoB.getText();
> ```
> `getText()` restituisce una `String`: `int a = campoA.getText();` non compila (`incompatible types: String cannot be converted to int`). Peggio, se la variabile fosse una `String`, `campoA.getText() + campoB.getText()` **concatenerebbe** `"2"` e `"3"` in `"23"`. Forma corretta: `int a = Integer.parseInt(campoA.getText());`.

> [!CAUTION]
> **Errore tipico — Non gestire la `NumberFormatException`**
> ```java
> // ERRORE logico: campo vuoto, lettere o spazi mandano in errore il listener
> public void actionPerformed(ActionEvent e) {
>     int a = Integer.parseInt(campoA.getText());
>     campoRisultato.setText(String.valueOf(a * 2));
> }
> ```
> Compila, e funziona con input corretti. Con `ciao`, con la casella vuota o con `" 12 "` (gli spazi non sono ammessi), `parseInt` lancia `NumberFormatException`. L'eccezione non ferma il programma né la finestra, ma interrompe il metodo e viene stampata in console: l'utente non vede nessun cambiamento e nessuna spiegazione. Forma corretta: racchiudere conversione e calcolo in un `try` con `catch (NumberFormatException ex)` che scrive un messaggio nel campo di uscita.

> [!CAUTION]
> **Errore tipico — Usare in una classe anonima una variabile locale che cambia**
> ```java
> // ERRORE di compilazione: la variabile locale non è effettivamente final
> int contatore = 0;
> pulsante.addActionListener(new ActionListener() {
>     public void actionPerformed(ActionEvent e) {
>         contatore++;                     // modifica di una variabile locale del metodo esterno
>     }
> });
> ```
> Il compilatore rifiuta il programma: `local variables referenced from an inner class must be final or effectively final`. Una variabile locale catturata da una classe anonima non può essere riassegnata. Forma corretta: dichiarare `contatore` come **campo** della classe esterna (i campi non hanno questo limite), come nel contatore della sezione 16.4.4.

> [!CAUTION]
> **Errore tipico — Impostare il colore sulla finestra invece che sul content pane**
> ```java
> // ERRORE: non si vede alcun cambiamento
> finestra.setBackground(Color.BLUE);
> ```
> Il colore della finestra è coperto dal content pane. Forma corretta: `finestra.getContentPane().setBackground(Color.BLUE);` (sezione 16.2.2).

> [!CAUTION]
> **Errore tipico — Confondere i listener con `==` sulle stringhe del comando**
> ```java
> // ERRORE: == confronta i riferimenti, non il contenuto
> if (e.getActionCommand() == "Rosso") { ... }
> ```
> `getActionCommand()` restituisce una `String`. Con `==` si confronta se è lo **stesso oggetto**, non se il testo coincide, e il confronto può dare `false` anche con testo uguale ([Capitolo 3](03-stringhe-e-console.md) e [Capitolo 8](08-riferimenti-e-memoria.md)). Forma corretta: `e.getActionCommand().equals("Rosso")`.

---

## Riassunto

Una interfaccia grafica sposta il programma dalla console alla **finestra**: invece di un flusso che chiede e legge, c'è un insieme di **componenti** disposti sullo schermo e di frammenti di codice che partono quando l'utente agisce. Si costruisce una finestra con `JFrame`, le si dà un titolo e una dimensione in pixel, si aggiungono i componenti al suo **content pane**, si decide cosa succede alla chiusura (`EXIT_ON_CLOSE`, oppure un `WindowAdapter`) e si chiama `setVisible(true)`. La disposizione dei componenti è affidata a un **layout manager**: `BorderLayout` per la struttura generale, `FlowLayout` per le file di comandi, `GridLayout` per le griglie, combinati annidando **pannelli** (`JPanel`). La reazione all'utente segue lo schema degli **eventi**: un componente (la sorgente) genera un evento e chiama il metodo di un **listener** registrato; per i pulsanti è `ActionListener.actionPerformed(ActionEvent)`, scritto nella finestra stessa, in una classe interna o in una classe anonima. Il testo si legge e si scrive con `JTextField` e `JTextArea` ma è **sempre una stringa**: per usarlo come numero lo si converte con `parseInt`, e la `NumberFormatException` che ne può derivare va gestita. Lo schema **MVC** separa i dati, la loro presentazione e la logica che li collega. JavaFX riprende le stesse idee con nomi diversi (`Stage`, `Scene`, nodi, controller, `EventHandler`) e in più descrive l'interfaccia in un file FXML.

**Concetti chiave**

- **GUI ed evento**: la GUI è un insieme di componenti in una finestra; un evento è un oggetto che rappresenta un'azione dell'utente, generato da una sorgente e gestito da un listener.
- **`JFrame` e content pane**: la finestra; i componenti si aggiungono al suo content pane (`add` vi delega). `setSize` in pixel, `setVisible(true)` per mostrarla, sempre come ultima istruzione.
- **Chiusura**: il comportamento predefinito è nascondere la finestra, non terminare il programma. Per terminarlo: `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)` o un `WindowAdapter` con `windowClosing`.
- **`WindowAdapter`**: classe di comodo con metodi vuoti, per ridefinire solo il metodo di `WindowListener` che interessa.
- **Finestra come classe derivata**: `class X extends JFrame`, con il costruttore che configura tutto e il `main` che crea e mostra.
- **Layout manager**: `BorderLayout` (cinque regioni, un componente per regione, `add(c)` senza regione va al centro), `FlowLayout` (in fila, a capo; predefinito di `JPanel`), `GridLayout(rows, cols)` (celle uguali, per righe).
- **`JButton` e `ActionListener`**: `implements ActionListener`, `public void actionPerformed(ActionEvent e)`, `addActionListener`.
- **Quale pulsante**: `e.getActionCommand()` (testo, confronto con `equals`) oppure `e.getSource()` (oggetto, confronto con `==`).
- **Tre forme del listener**: la finestra stessa, una classe interna, una classe anonima (variabili locali `final` di fatto).
- **MVC**: modello (dati), vista (GUI), controllore (logica che collega i due).
- **`JPanel` e gerarchia**: il pannello raggruppa componenti; `JFrame` discende da `Window`, i componenti Swing da `JComponent`, tutti da `Container` e `Component`.
- **`JLabel`, `JTextField`, `JTextArea`**: testo non modificabile, una riga, più righe; `getText`, `setText`, `setEditable`, `append`.
- **Numeri e stringhe**: ciò che entra e esce è `String`; `Integer.parseInt` / `Double.parseDouble` per entrare, `String.valueOf` per uscire; `NumberFormatException` per input non valido (anche spazi o campo vuoto).
- **JavaFX**: `Application.launch` → `start(Stage)`, `Scene` e grafo della scena, FXML scritto con Scene Builder, controller con `@FXML` e `fx:id`, `EventHandler<ActionEvent>`, `ChangeListener`.

**API essenziali**

| Classe | Metodo | Firma | Eccezioni |
|---|---|---|---|
| `JFrame` | costruttore | `JFrame()` , `JFrame(String title)` | `HeadlessException` (non controllata) |
| `JFrame` | `setDefaultCloseOperation` | `void setDefaultCloseOperation(int operation)` | — |
| `JFrame` | `getContentPane` | `Container getContentPane()` | — |
| `Component` | `setSize`, `setVisible`, `setBackground` | `void setSize(int, int)`, `void setVisible(boolean)`, `void setBackground(Color)` | — |
| `Container` | `add`, `setLayout` | `Component add(Component)`, `void add(Component, Object)`, `void setLayout(LayoutManager)` | — |
| `Window` | `pack`, `addWindowListener`, `dispose` | `void pack()`, `void addWindowListener(WindowListener)`, `void dispose()` | — |
| `JButton` | costruttore | `JButton(String text)` | — |
| `AbstractButton` | `addActionListener` | `void addActionListener(ActionListener l)` | — |
| `ActionListener` | `actionPerformed` | `void actionPerformed(ActionEvent e)` | — |
| `ActionEvent` | `getActionCommand` | `String getActionCommand()` | — |
| `JLabel` | costruttori, `setText` | `JLabel(String)`, `JLabel(String, int)`, `void setText(String)` | — |
| `JTextField` | costruttore | `JTextField(int columns)`, `JTextField(String, int)` | — |
| `JTextComponent` | `getText`, `setText`, `setEditable` | `String getText()`, `void setText(String)`, `void setEditable(boolean)` | — |
| `JTextArea` | costruttore, `append` | `JTextArea(int rows, int columns)`, `void append(String)` | `IllegalArgumentException` (righe o colonne negative) |
| `JPanel` | costruttori | `JPanel()`, `JPanel(LayoutManager)` | — |
| `BorderLayout` | costanti | `NORTH`, `SOUTH`, `EAST`, `WEST`, `CENTER` (`String`) | — |
| `FlowLayout` | costruttori | `FlowLayout()`, `FlowLayout(int align)`, `FlowLayout(int, int, int)` | — |
| `GridLayout` | costruttori | `GridLayout(int rows, int cols)`, `GridLayout(int, int, int, int)` | — |
| `Integer` | `parseInt` | `static int parseInt(String s)` | `NumberFormatException` (non controllata) |
