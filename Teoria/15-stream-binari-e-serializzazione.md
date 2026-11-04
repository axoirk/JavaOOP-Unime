---
materia: Programmazione a Oggetti
capitolo: 15
titolo: Stream binari e serializzazione
livello_syllabus: 4
stato: completo
slide: ["Savitch cap. 14 slide 28-54"]
appelli: [EXAM3]
fonti_esterne: 10
aggiornato: 2026-11-04
tags: [appunti, java, programmazione-a-oggetti]
---

# Capitolo 15 — Stream binari e serializzazione

## Di cosa parla questo capitolo

Nel [Capitolo 14](14-file-di-testo.md) abbiamo salvato dati sotto forma di **testo**: ogni numero diventava una sequenza di cifre, ogni riga un pezzo di carattere leggibile. È comodo, ma ha due limiti. Il primo: per riavere un numero bisogna ricostruirlo dalle cifre, e per riavere un oggetto bisogna scrivere a mano il codice che lo scompone in campi (come facevamo con i file CSV) e poi quello che lo ricompone. Il secondo: un oggetto con riferimenti ad altri oggetti, o una lista intera, non ha una rappresentazione testuale ovvia.

Java offre una strada più diretta. I **flussi binari** scrivono i valori nella loro forma interna, byte dopo byte, e li rileggono senza passare per i caratteri. E la **serializzazione** va oltre: trasforma un **oggetto intero**, con tutto ciò che contiene, in una sequenza di byte, e da quei byte ricostruisce un oggetto equivalente. Con due righe si salva un oggetto su un file, e con altre due lo si riavvia a nuova vita, anche in un altro programma.

In questo capitolo vedremo:

- come **scrivere e leggere valori primitivi e stringhe** in un file binario (`writeInt`, `writeDouble`, `writeUTF` e i metodi corrispondenti per la lettura), e perché si devono rileggere **nello stesso ordine** in cui sono stati scritti;
- come si riconosce la **fine del file** in un flusso binario, che non ha un `hasNext` e non restituisce `null`, ma lancia una `EOFException`;
- che cos'è la **serializzazione**, l'interfaccia `Serializable` e i metodi `writeObject` e `readObject`;
- quali **regole** deve rispettare una classe per essere serializzabile (campi, superclasse, `static`, `transient`) e che cos'è la **costante di versione** `serialVersionUID`;
- come serializzare **array e collezioni**, come scrivere **più oggetti** in uno stesso file e perché non si può usare `ObjectOutputStream` per aggiungere in coda;
- perché lo stesso flusso funziona su un file come su una connessione di rete, e perché **la destinazione** va scelta con cura;
- gli **scheletri** da saper scrivere a memoria e gli errori che compilatore o test nascosto puniscono.

Il capitolo si appoggia ai precedenti. La distinzione tra flussi di byte e flussi di caratteri, l'idea di **avvolgere** un flusso in un altro, il buffer e il `close` sono nel [Capitolo 14](14-file-di-testo.md), e qui li useremo senza rispiegarli. Le **eccezioni controllate** e lo schema di chiusura nel `finally` sono nel [Capitolo 13](13-eccezioni.md). L'identità di un oggetto e il fatto che un oggetto ricostruito sia un oggetto nuovo sono nel [Capitolo 8](08-riferimenti-e-memoria.md) (sezione 8.4.5). Le interfacce vuote come `Serializable` e quelle con metodi, come `Comparable`, sono nel [Capitolo 10](10-classi-astratte-e-interfacce.md). Il capitolo sulla rete ([Capitolo 19](19-networking.md)) riprenderà tutto ciò che qui impariamo per spedire oggetti da un programma a un altro.

> [!IMPORTANT]
> **Nota per l'esame — Serializzazione e flussi binari**
> La serializzazione è uno degli argomenti tipici del secondo esercizio della prova scritta (13 punti), spesso **combinata** con un'altra API: un oggetto serializzato viaggia su un socket. All'esame il docente guarda la **struttura letterale** richiesta dalla traccia: una classe con la costante di versione, le variabili d'istanza `private`, la conversione in byte e la ricostruzione con il `readObject` e il cast, la gestione del fallimento. Sapere separatamente la serializzazione e i socket non basta: bisogna saperli comporre, e scegliere con cura **quale flusso** si avvolge (il file o la connessione). Per questo il capitolo insiste sulle forme esatte: firme, eccezioni da dichiarare, `import`.

---

## 15.1 Dal testo ai byte

### 15.1.1 Perché un file binario

Ricordiamo la distinzione del [Capitolo 14](14-file-di-testo.md) (sezione 14.1.3): un file di testo è una sequenza di caratteri leggibile da un editor; tutti gli altri file sono binari. Un dato scritto in un file di testo e lo stesso dato scritto in un file binario hanno costi diversi.

Prendiamo l'intero `12345`. In un file di testo occupa **cinque caratteri**, quelli delle cinque cifre. In un file binario scritto con `writeInt` occupa **quattro byte**, esattamente quanti ne occupa un `int` in memoria, e rileggerlo non richiede nessuna analisi di cifre: i quattro byte tornano a essere l'`int`. Lo stesso vale per un `double`: sempre otto byte, qualunque sia il valore, mentre in testo `3.0` e `3.14159265358979` hanno lunghezze molto diverse.

| | File di testo | File binario |
|---|---|---|
| Come è scritto un `int` | le cifre, come caratteri | i 4 byte dell'`int` |
| Leggibile da una persona con un editor | sì | no |
| Per rileggere un valore | si ricostruisce dai caratteri (`parseInt`, `nextInt`) | si legge direttamente (`readInt`) |
| Il tipo del valore | non è scritto: lo decide chi legge | non è scritto: lo decide chi legge |

L'ultima riga è la più importante per il seguito. **Né il testo né i byte dicono di che tipo sia un valore.** Quattro byte possono essere un `int`, un `float`, due `char` o parte di un `double`: chi rilegge deve **sapere** in che ordine e con quali tipi i dati sono stati scritti. È l'origine della regola d'oro di questo capitolo: *si legge nello stesso ordine e con gli stessi tipi con cui si è scritto* (sezione 15.3).

### 15.1.2 Le classi del capitolo

Le classi dei flussi binari sono le gemelle di quelle del capitolo precedente. Dove i flussi di caratteri hanno `Reader` e `Writer`, i flussi di byte hanno `InputStream` e `OutputStream` (sezione 14.1.4). Quello che cambia rispetto ai testi è il livello a cui si lavora, e lo sappiamo già: le classi si **avvolgono** l'una nell'altra.

| Classe | Package | Che cosa sa fare | Su che cosa si appoggia |
|---|---|---|---|
| `FileOutputStream` / `FileInputStream` | `java.io` | scrivere / leggere **byte** di un file | direttamente il file |
| `ObjectOutputStream` / `ObjectInputStream` | `java.io` | scrivere / leggere **primitivi, stringhe e oggetti** | un altro flusso di byte, passato al costruttore |
| `DataOutputStream` / `DataInputStream` | `java.io` | scrivere / leggere **primitivi e stringhe** (non oggetti) | un altro flusso di byte, passato al costruttore |

Il file vero e proprio è sempre in mano a `FileOutputStream` o `FileInputStream`, che però sanno scrivere solo byte uno alla volta. Chi vuole scrivere un `int` o un oggetto **avvolge** quel flusso in un `ObjectOutputStream` (o `DataOutputStream`), che sa tradurre i valori in byte. Il costruttore di `ObjectOutputStream` **non accetta un nome di file**: accetta un flusso di byte, e lo si costruisce a parte.

```java
// ERRATO come schema: il costruttore non prende una String
// ObjectOutputStream out = new ObjectOutputStream("punteggi.dat");

// Corretto: si apre il file con FileOutputStream e lo si avvolge
// ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("punteggi.dat"));
```

Come per i file di testo, si legge l'espressione dall'**interno verso l'esterno**: `new FileOutputStream("punteggi.dat")` apre (o crea) il file, e `new ObjectOutputStream(...)` gli aggiunge la capacità di scrivere valori e oggetti.

Nel resto del capitolo useremo soprattutto `ObjectOutputStream` e `ObjectInputStream`, perché sono quelli che servono per la serializzazione, e perché sanno scrivere e leggere anche i primitivi e le stringhe con gli stessi metodi di `DataOutputStream` e `DataInputStream`. Questi ultimi, più semplici, sono presentati nell'approfondimento della sezione 15.2.5.

---

## 15.2 Scrivere valori in un file binario

### 15.2.1 Aprire il file e scrivere

Il primo programma scrive tre numeri interi in un file binario. È lo schema più semplice: aprire, scrivere con `writeInt`, chiudere.

```java
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;

public class ScriviPunteggi {
    public static void main(String[] args) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("punteggi.dat"));
        out.writeInt(18);
        out.writeInt(25);
        out.writeInt(30);
        out.close();
        System.out.println("Scritti 3 numeri.");
    }
}
```

L'output sul terminale è:

```text
Scritti 3 numeri.
```

Il file `punteggi.dat` non è leggibile in un editor: contiene byte, non caratteri. Vediamo il programma riga per riga.

- `new FileOutputStream("punteggi.dat")` apre il file in scrittura. Come `PrintWriter` e `FileWriter` ([Capitolo 14](14-file-di-testo.md)), se il file esiste **lo svuota** subito; se non esiste lo crea. Il costruttore dichiara `FileNotFoundException`.
- `new ObjectOutputStream(...)` avvolge il flusso. Il suo costruttore dichiara `IOException`, perché scrive subito sul flusso un'**intestazione** (*header*) che serve a chi leggerà, per riconoscere che si tratta di un flusso di questo tipo.
- `writeInt(18)` scrive i quattro byte dell'intero. Non c'è un `println`: un flusso binario non scrive righe, scrive valori. Non c'è nessun separatore tra un valore e il successivo, perché non serve: ognuno occupa un numero fisso di byte e chi legge sa quanti ne deve prendere.
- `close()` svuota il buffer e chiude il file: senza di esso il file resta incompleto, come per i file di testo (sezione 14.2.2).

Poiché `FileNotFoundException` è una sottoclasse di `IOException` ([Capitolo 13](13-eccezioni.md)), il solo `throws IOException` sul `main` le copre entrambe.

> [!NOTE]
> **Definizione — Il costruttore di `ObjectOutputStream`**
> `public ObjectOutputStream(OutputStream out) throws IOException`. Crea un flusso che scrive sull'`OutputStream` ricevuto. Non esiste un costruttore che accetti il nome di un file.

### 15.2.2 I metodi di scrittura

`ObjectOutputStream` ha un metodo per ogni tipo primitivo. Tutti dichiarano `IOException` (che per la scrittura non possiamo ignorare) e hanno il nome `write` seguito dal nome del tipo.

| Metodo | Firma | Scrive |
|---|---|---|
| `writeInt` | `void writeInt(int val)` | un `int`, quattro byte |
| `writeLong` | `void writeLong(long val)` | un `long`, otto byte |
| `writeDouble` | `void writeDouble(double val)` | un `double`, otto byte |
| `writeFloat` | `void writeFloat(float val)` | un `float`, quattro byte |
| `writeBoolean` | `void writeBoolean(boolean val)` | un `boolean`, un byte |
| `writeChar` | `void writeChar(int val)` | un `char`, due byte (il parametro è un `int`) |
| `writeShort` / `writeByte` | `void writeShort(int val)` / `void writeByte(int val)` | uno `short` (due byte) / un `byte` |
| `writeUTF` | `void writeUTF(String str)` | una **stringa** |
| `writeObject` | `final void writeObject(Object obj)` | un **oggetto** (sezione 15.5) |

Notiamo la regola generale: **per ogni tipo, un metodo**. Se si vuole salvare un `int` si usa `writeInt`; non si può passare un `int` a un generico `write` e lasciare che Java scelga. E quando il tipo è una stringa o un oggetto, si usano metodi diversi (`writeUTF` e `writeObject`).

### 15.2.3 Scrivere le stringhe: `writeUTF`

Una stringa ha lunghezza variabile, quindi chi legge non sa in anticipo quanti byte prendere. `writeUTF(String)` risolve il problema scrivendo **prima la lunghezza** e poi i caratteri, in un formato chiamato *UTF-8 modificato*. Dal punto di vista di chi usa il metodo conta una cosa sola: quello che si scrive con `writeUTF` si rilegge con `readUTF`, e `readUTF` sa da solo quanti byte leggere. Le stringhe scritte occupano un numero di byte che dipende dalla loro lunghezza: la stringa `"Marta"`, per esempio, occupa 2 byte per la lunghezza e 5 per i caratteri, cioè 7 byte in tutto.

```java
// scrive una stringa: la lunghezza viene scritta in automatico
out.writeUTF("Marta");
```

Questa è la differenza di fondo tra `writeInt`, che usa sempre lo stesso numero di byte, e `writeUTF`, che ne usa un numero variabile in base alla stringa.

### 15.2.4 Un programma con tipi diversi

Il file può contenere valori di tipi diversi, uno dopo l'altro, nell'ordine che scegliamo. Lo scriviamo e lo rileggiamo in uno stesso programma, con due metodi.

```java
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class ScheDati {
    static void scrivi(String nomeFile) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(nomeFile));
        out.writeUTF("Marta");        // String
        out.writeInt(34);             // int
        out.writeDouble(1.68);        // double
        out.writeBoolean(true);       // boolean
        out.close();
    }

    static void leggi(String nomeFile) throws IOException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(nomeFile));
        String nome = in.readUTF();       // stesso ordine della scrittura
        int eta = in.readInt();
        double altezza = in.readDouble();
        boolean iscritta = in.readBoolean();
        in.close();
        System.out.println(nome + " " + eta + " " + altezza + " " + iscritta);
    }

    public static void main(String[] args) throws IOException {
        scrivi("scheda.dat");
        leggi("scheda.dat");
        System.out.println("Byte nel file: " + new File("scheda.dat").length());
    }
}
```

L'output è:

```text
Marta 34 1.68 true
Byte nel file: 26
```

I dati utili sono 20 byte (7 + 4 + 8 + 1): gli altri 6 sono l'intestazione e le informazioni di controllo che `ObjectOutputStream` aggiunge. Il confronto con i 20 byte esatti di `DataOutputStream` è nell'approfondimento seguente.

### 15.2.5 `DataOutputStream` e `DataInputStream`

`ObjectOutputStream` scrive i primitivi con i metodi dell'interfaccia `DataOutput`. Chi vuole solo salvare valori primitivi e stringhe, senza oggetti, può usare le classi più semplici che realizzano quell'interfaccia direttamente.

> [!NOTE]
> **Approfondimento esterno — `DataOutputStream` e `DataInputStream`**
> La documentazione ufficiale descrive `DataOutputStream` così: «*lets an application write primitive Java data types to an output stream in a portable way. An application can then use a data input stream to read the data back in*». Il costruttore è `public DataOutputStream(OutputStream out)` e **non dichiara eccezioni**. I metodi di scrittura sono `final` e dichiarano `IOException`: `writeInt(int v)` scrive «*four bytes, high byte first*», `writeDouble(double v)` scrive un valore di 8 byte, `writeUTF(String str)` dichiara anche la `UTFDataFormatException` (sottoclasse di `IOException`) se la stringa in UTF-8 modificato superasse i 65535 byte.
> `DataInputStream` ha il costruttore `public DataInputStream(InputStream in)` (nessuna eccezione) e i metodi `final String readUTF()`, `int readInt()`, `double readDouble()`, `boolean readBoolean()`, `long readLong()`, tutti con `throws IOException`; la documentazione precisa che ciascuno lancia `EOFException` se il flusso finisce prima di aver letto tutti i byte necessari.
> `ObjectOutput` e `ObjectInput` sono descritte come le interfacce che **estendono** `DataOutput` e `DataInput` «*to include writing of objects*»: per questo `ObjectOutputStream` ha gli stessi metodi di `DataOutputStream`, più `writeObject`.
>
> *Fonte:* [DataOutputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/DataOutputStream.html), [DataInputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/DataInputStream.html) e [ObjectOutput (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectOutput.html)

Il programma della sezione precedente, riscritto con `DataOutputStream` e `DataInputStream`, ha la stessa forma:

```java
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class ScheDatiData {
    public static void main(String[] args) throws IOException {
        DataOutputStream out = new DataOutputStream(new FileOutputStream("scheda2.dat"));
        out.writeUTF("Marta");
        out.writeInt(34);
        out.writeDouble(1.68);
        out.writeBoolean(true);
        out.close();

        DataInputStream in = new DataInputStream(new FileInputStream("scheda2.dat"));
        System.out.println(in.readUTF() + " " + in.readInt() + " " + in.readDouble() + " " + in.readBoolean());
        in.close();
        System.out.println("Byte nel file: " + new File("scheda2.dat").length());
    }
}
```

```text
Marta 34 1.68 true
Byte nel file: 20
```

Il file di `DataOutputStream` pesa esattamente i 20 byte dei dati, perché non ha intestazione. Questa è anche una **differenza di compatibilità**: un file scritto con `DataOutputStream` non ha l'intestazione che `ObjectInputStream` si aspetta, e non si può rileggere con quest'ultimo (e viceversa). Chi scrive e chi legge devono usare la **stessa famiglia** di classi.

> [!WARNING]
> **Attenzione — Se la traccia dice "file binario"**
> La parola «binario» non dice quale famiglia usare. Il caso tipico di un file di record (per esempio una stringa, un intero e un `double` per ogni riga) si risolve con `DataOutputStream`/`DataInputStream` o con `ObjectOutputStream`/`ObjectInputStream`, purché si **scrivano e leggano gli stessi campi nello stesso ordine**. Se invece la traccia chiede di salvare un **oggetto**, serve `ObjectOutputStream` con `writeObject` (sezione 15.5): `DataOutputStream` non sa scrivere oggetti.

---

## 15.3 Leggere un file binario

### 15.3.1 `ObjectInputStream` e i metodi di lettura

La lettura è la strada inversa: si apre il file con `FileInputStream` e lo si avvolge in un `ObjectInputStream`. Per ogni metodo `writeXxx` c'è il metodo `readXxx` corrispondente.

| Per leggere | Metodo | Firma |
|---|---|---|
| un `int` | `readInt` | `int readInt()` |
| un `long` | `readLong` | `long readLong()` |
| un `double` | `readDouble` | `double readDouble()` |
| un `float` | `readFloat` | `float readFloat()` |
| un `boolean` | `readBoolean` | `boolean readBoolean()` |
| un `char` | `readChar` | `char readChar()` |
| una `String` | `readUTF` | `String readUTF()` |
| un oggetto | `readObject` | `final Object readObject()` |

Tutti dichiarano `IOException`; `readObject` dichiara anche `ClassNotFoundException` (sezione 15.5.3). Il costruttore è `public ObjectInputStream(InputStream in) throws IOException` e `new FileInputStream(String)` dichiara `FileNotFoundException`, come i costruttori di scrittura.

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class Punteggi {
    static void scrivi(String nomeFile) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(nomeFile));
        out.writeInt(18);
        out.writeInt(25);
        out.writeInt(30);
        out.close();
    }

    static void leggi(String nomeFile) throws IOException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(nomeFile));
        int a = in.readInt();
        int b = in.readInt();
        int c = in.readInt();
        in.close();
        System.out.println(a + " " + b + " " + c);
        System.out.println("Somma: " + (a + b + c));
    }

    public static void main(String[] args) throws IOException {
        scrivi("punteggi.dat");
        leggi("punteggi.dat");
    }
}
```

L'output è:

```text
18 25 30
Somma: 73
```

### 15.3.2 La regola d'oro: stesso ordine, stessi tipi

Il file non porta con sé i tipi: sono 25 byte e nessuno dice dove finisce il primo valore e comincia il secondo. Per questo la lettura deve **ripercorrere esattamente la scrittura**: se il file contiene, nell'ordine, una stringa, un intero e un `double`, si chiamano `readUTF`, `readInt`, `readDouble`, in quest'ordine. Se i tipi o l'ordine non coincidono, **Java non se ne accorge** e restituisce valori sbagliati: non c'è nessuna eccezione, il programma va avanti con numeri senza senso (errore tipico 1, in fondo al capitolo).

La stessa regola impone una cosa che spesso si dimentica: quando un record ha più campi, **si leggono tutti anche quelli che non servono**. Se ogni record è `(nome, età, altezza)` e interessa solo l'altezza, si leggono comunque nome ed età (e si scartano), perché altrimenti la lettura successiva parte da un punto sbagliato del record.

### 15.3.3 Che cosa può andare storto in apertura

L'apertura può lanciare:

- `FileNotFoundException`, da `new FileInputStream(...)`: il file non esiste, è una cartella o non è leggibile (sezione 14.2.4);
- `StreamCorruptedException`, da `new ObjectInputStream(...)`: il file esiste ma **non inizia con l'intestazione** attesa, perché non è stato scritto da un `ObjectOutputStream`. È ciò che accade se si prova a leggere come flusso di oggetti un file di testo, oppure un file scritto con `DataOutputStream` (sezione 15.2.5). L'eccezione è un'`IOException`, e il messaggio dice qual è la sequenza di byte trovata: per un file di testo che comincia con `ciao mondo` è `invalid stream header: 6369616F`, cioè i codici dei primi quattro caratteri;
- `EOFException`, sempre dal costruttore, se il file è **vuoto**: non c'è nemmeno l'intestazione da leggere.

> [!NOTE]
> **Approfondimento esterno — Il costruttore di `ObjectInputStream`**
> La documentazione ufficiale descrive `public ObjectInputStream(InputStream in) throws IOException` e precisa che il costruttore «*will block until the corresponding ObjectOutputStream has written and flushed the header*» (cioè **si ferma ad aspettare** che dall'altra parte arrivi l'intestazione scritta e svuotata da un `ObjectOutputStream`). Dichiara `StreamCorruptedException` («*if the stream header is incorrect*») e `IOException` («*if an I/O error occurs while reading stream header*»). Per un file l'attesa non si nota, perché l'intestazione è già lì; la rivedremo parlando di rete (sezione 15.11).
>
> *Fonte:* [ObjectInputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectInputStream.html)

---

## 15.4 La fine del file: `EOFException`

### 15.4.1 Il problema

Negli esempi precedenti sapevamo **quanti** valori c'erano nel file: tre numeri, quattro campi. In un programma vero spesso non lo si sa: il file contiene tutti i valori che un programma precedente ha voluto salvare, e chi legge deve continuare **finché ce ne sono**. Con i file di testo il problema aveva due soluzioni: `hasNextLine()` del `Scanner` e `readLine() == null` del `BufferedReader` (sezione 14.4).

I flussi binari non offrono né l'una né l'altra. Non c'è un metodo `hasNext` e nessun metodo di lettura restituisce `null` o `-1` per dire «è finito», perché *qualsiasi* sequenza di byte è un valore possibile: `-1` è un `int` legittimo e un `readDouble` non ha un valore speciale da restituire. Java sceglie un'altra strada: quando si prova a leggere e i dati sono finiti, il metodo **lancia un'eccezione**.

> [!NOTE]
> **Definizione — `EOFException`**
> `EOFException` è una sottoclasse di `IOException` (dunque **controllata**). Segnala che la fine del file (*end of file*) o del flusso è stata raggiunta **durante una lettura**. Tutti i metodi `readInt`, `readDouble`, `readUTF`, `readObject` la lanciano se non ci sono più byte da leggere.

> [!NOTE]
> **Approfondimento esterno — `EOFException` e fine del flusso**
> La documentazione ufficiale di `EOFException` dice: «*Signals that an end of file or end of stream has been reached unexpectedly during input. This exception is mainly used by data input streams to signal end of stream. Note that many other input operations return a special value on end of stream rather than throwing an exception.*» La documentazione di `ObjectInputStream` aggiunge che, alla fine dei dati, «*bytewise reads will return -1 as the byte read or number of bytes read, and primitive reads will throw EOFExceptions*»: le letture di byte restituiscono `-1`, le letture di primitivi lanciano `EOFException`.
>
> *Fonte:* [EOFException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/EOFException.html) e [ObjectInputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectInputStream.html)

### 15.4.2 Il ciclo di lettura fino alla fine

Poiché la fine arriva come eccezione, la usiamo come **uscita dal ciclo**: si legge in un ciclo infinito `while (true)` e si cattura `EOFException` fuori dal ciclo. Qui l'eccezione non è un errore ma il modo normale di terminare.

```java
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class LeggiFinoAllaFine {
    static void scrivi(String nomeFile) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(nomeFile));
        int[] valori = {4, 8, 15, 16, 23, 42};
        for (int i = 0; i < valori.length; i++) {
            out.writeInt(valori[i]);
        }
        out.close();
    }

    static void leggiTutti(String nomeFile) throws IOException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(nomeFile));
        int somma = 0;
        int quanti = 0;
        try {
            while (true) {                       // quanti sono? non si sa: si legge finché ce ne sono
                int n = in.readInt();
                somma += n;
                quanti++;
            }
        } catch (EOFException e) {
            System.out.println("Fine del file.");  // uscita normale dal ciclo
        } finally {
            in.close();
        }
        System.out.println("Letti " + quanti + " numeri, somma " + somma);
    }

    public static void main(String[] args) throws IOException {
        scrivi("numeri.dat");
        leggiTutti("numeri.dat");
    }
}
```

L'output è:

```text
Fine del file.
Letti 6 numeri, somma 108
```

Riga per riga. `while (true)` non ha una condizione di uscita: l'unica via d'uscita è l'eccezione. Dopo il sesto `readInt` riuscito, il settimo trova il file finito e lancia `EOFException`; l'esecuzione salta fuori dal ciclo e va nel `catch`, che stampa il messaggio e lascia il blocco. Il `finally` chiude il flusso. Le istruzioni dopo il `try` (la stampa finale) continuano a eseguirsi, perché l'eccezione è stata **gestita**.

Notiamo tre dettagli di forma, tutti importanti per la lettura letterale di una traccia.

1. **Il `try` racchiude l'intero ciclo**, non solo la lettura dentro il ciclo. Se il `try`/`catch` fosse dentro il corpo del `while (true)`, dopo l'eccezione il ciclo ricomincerebbe, e leggerebbe ancora, e ancora, e ancora, con un'eccezione a ogni giro.
2. **`EOFException` è un'`IOException`**: se nello stesso `try` si gestiscono entrambe, il `catch (EOFException)` va **prima**; altrimenti il compilatore rifiuta il programma, perché l'eccezione specifica non potrebbe mai essere raggiunta (errore tipico 3, e [Capitolo 13](13-eccezioni.md), sezione 13.4).
3. **Il flusso si chiude comunque**: nel `finally`, non nel `catch`. La chiusura non deve dipendere dal modo in cui si esce dal ciclo.

### 15.4.3 File vuoto, valori in più o in meno

Se il file è stato scritto da un `ObjectOutputStream` che è stato chiuso senza scrivere alcun valore, contiene la sola intestazione: `new ObjectInputStream(...)` riesce, e il primo `readInt` lancia subito `EOFException`. Il ciclo termina senza aver letto nulla (nel nostro programma `quanti` rimane 0). Se invece il file è **completamente vuoto** (zero byte), non c'è nemmeno l'intestazione, e a lanciare `EOFException` è già il costruttore, come visto nella sezione 15.3.3. In entrambi i casi la fine è segnalata allo stesso modo.

Una conseguenza meno ovvia riguarda i file di **record**. Se ogni record è formato da due valori, per esempio un identificativo e un punteggio, il ciclo legge una coppia alla volta. Se il file contiene per errore un numero **dispari** di valori, l'ultimo `readInt` della coppia lancia `EOFException` **a metà record**, e il `catch` la tratta come una fine normale: l'ultimo valore viene scartato senza nessun avviso.

```java
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class RecordIncompleto {
    public static void main(String[] args) throws IOException {
        DataOutputStream out = new DataOutputStream(new FileOutputStream("coppie.dat"));
        out.writeInt(5);
        out.writeInt(6);
        out.writeInt(7);                       // il record dispari: manca la seconda metà
        out.close();

        DataInputStream in = new DataInputStream(new FileInputStream("coppie.dat"));
        try {
            while (true) {
                int id = in.readInt();
                int punti = in.readInt();      // qui il terzo giro lancia EOFException
                System.out.println(id + " -> " + punti);
            }
        } catch (EOFException e) {
            System.out.println("Fine.");
        } finally {
            in.close();
        }
    }
}
```

```text
5 -> 6
Fine.
```

Il `7` è stato letto ma mai stampato. In un programma vero questo è un file corrotto; l'eccezione non lo segnala, perché per Java è una fine come un'altra.

### 15.4.4 Il valore sentinella

Con i file di testo si usava a volte un **valore sentinella** (un valore speciale, per esempio `-1`, che segna la fine dei dati). Con un file binario si può fare lo stesso, ma la sentinella è **solo un dato in più**: va letta anch'essa, e **non sostituisce** `EOFException`. Se il file non contiene la sentinella (per un errore di chi lo ha scritto), il ciclo che aspetta solo `-1` lancia comunque `EOFException`.

Il ciclo robusto prevede entrambe le uscite: la sentinella e la fine del file.

```java
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class ConSentinella {
    public static void main(String[] args) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("dati.dat"));
        out.writeInt(10);
        out.writeInt(20);
        out.writeInt(-1);                   // sentinella: segna la fine dei dati utili
        out.close();

        ObjectInputStream in = new ObjectInputStream(new FileInputStream("dati.dat"));
        int somma = 0;
        try {
            int n = in.readInt();
            while (n != -1) {               // prima uscita: la sentinella
                somma += n;
                n = in.readInt();
            }
        } catch (EOFException e) {          // seconda uscita: il file finisce senza sentinella
            System.out.println("Il file e' finito prima della sentinella.");
        } finally {
            in.close();
        }
        System.out.println("Somma: " + somma);
    }
}
```

```text
Somma: 30
```

### 15.4.5 Tre modi di dire «è finito»

Ogni famiglia di flussi ha la sua convenzione per segnalare la fine, ed è utile avere la tabella a portata di mano, perché all'esame il ciclo giusto dipende dal flusso.

| Flusso | Come segnala la fine | Come si scrive il ciclo |
|---|---|---|
| `Scanner` su un file | `hasNextLine()` restituisce `false` | `while (in.hasNextLine())` |
| `BufferedReader.readLine()` | restituisce `null` | `while ((riga = in.readLine()) != null)` |
| `read()` / `read(byte[])` su un `InputStream` | restituiscono `-1` | `while ((n = in.read()) != -1)` |
| `readInt`, `readDouble`, `readUTF`, `readObject` | **lanciano** `EOFException` | `try { while (true) { ... } } catch (EOFException e) { }` |

Un errore tipico è mischiare le convenzioni: scrivere `while ((x = in.readObject()) != null)` (errore tipico 2), che non termina mai in modo pulito, perché `readObject` non restituisce `null` alla fine: lancia `EOFException`.

### 15.4.6 Esempio svolto: raddoppiare i numeri di un file

Un problema classico mette insieme lettura e scrittura binarie: leggere tutti i numeri di un file, raddoppiarli e scrivere i risultati in un secondo file. Le due aperture e la chiusura nel `finally` seguono lo schema del [Capitolo 14](14-file-di-testo.md) (sezione 14.6).

```java
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class Raddoppia {
    static void raddoppia(String nomeIn, String nomeOut) throws IOException {
        ObjectInputStream in = null;
        ObjectOutputStream out = null;
        try {
            in = new ObjectInputStream(new FileInputStream(nomeIn));
            out = new ObjectOutputStream(new FileOutputStream(nomeOut));
            try {
                while (true) {
                    int n = in.readInt();
                    out.writeInt(n * 2);
                }
            } catch (EOFException e) {
                // fine dei dati: uscita normale dal ciclo
            }
        } finally {
            if (in != null) {
                in.close();
            }
            if (out != null) {
                out.close();
            }
        }
    }

    static void scrivi(String nomeFile, int[] valori) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(nomeFile));
        for (int i = 0; i < valori.length; i++) {
            out.writeInt(valori[i]);
        }
        out.close();
    }

    static void stampa(String nomeFile) throws IOException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(nomeFile));
        StringBuilder sb = new StringBuilder();
        try {
            while (true) {
                sb.append(in.readInt()).append(' ');
            }
        } catch (EOFException e) {
            // fine
        } finally {
            in.close();
        }
        System.out.println(sb.toString().trim());
    }

    public static void main(String[] args) throws IOException {
        scrivi("origine.dat", new int[] {1, 2, 3, 4, 5});
        raddoppia("origine.dat", "doppi.dat");
        stampa("doppi.dat");
    }
}
```

```text
2 4 6 8 10
```

Il `catch (EOFException)` sta **dentro** il `try` più grande, intorno al ciclo: le aperture e il `finally` sono quelli dello schema a quattro passi. Il `finally` più esterno chiude entrambi i flussi con la guardia `!= null`: se la seconda apertura fallisse, `out` sarebbe ancora `null` e `in` verrebbe comunque chiuso. (Il metodo `stampa` usa `StringBuilder` solo per mettere i numeri su una riga: è un accessorio di questo esempio.)

---

## 15.5 Serializzare un oggetto

### 15.5.1 Il problema

I valori primitivi e le stringhe si salvano con i metodi della sezione 15.2. Un **oggetto** però è più complicato: ha più campi, di tipi diversi, e quei campi possono essere a loro volta oggetti. Per salvare, per esempio, un `Libro` con titolo e numero di pagine, si potrebbero scrivere i campi uno per uno (`writeUTF(titolo)`, `writeInt(pagine)`) e, in lettura, ricostruire l'oggetto con il costruttore. Funziona, ma è un lavoro da rifare per ogni classe e fragile: se si aggiunge un campo, vanno cambiate sia la scrittura sia la lettura, e nello stesso ordine.

Java risolve il problema con un meccanismo generale.

> [!NOTE]
> **Definizione — Serializzazione**
> La **serializzazione** (*serialization*) è il processo che rappresenta un oggetto come una **sequenza di byte**, che si può scrivere su un file o inviare su una rete. La **deserializzazione** è il processo inverso: dai byte si ricostruisce un oggetto con gli stessi valori. È possibile per ogni classe che realizzi l'interfaccia `Serializable`.

Il codice di conversione non lo scriviamo noi: lo esegue la macchina virtuale, esaminando la classe dell'oggetto e i suoi campi, compresi quelli `private`.

### 15.5.2 L'interfaccia `Serializable`

`Serializable` è un'interfaccia particolarissima: **non ha nessun metodo**. Realizzarla (`implements Serializable`) non obbliga a scrivere codice: è soltanto un'etichetta con cui la classe dichiara «i miei oggetti possono essere convertiti in byte».

> [!NOTE]
> **Definizione — `java.io.Serializable`**
> `public interface Serializable`, nel package `java.io`. È un'interfaccia **vuota** (un'interfaccia *marcatore*, o *marker interface*): dichiarare `implements Serializable` autorizza la macchina virtuale a convertire gli oggetti della classe in una sequenza di byte. Non c'è nessun metodo da implementare.

> [!NOTE]
> **Approfondimento esterno — `Serializable` nella documentazione**
> La documentazione ufficiale dice che la serializzabilità di una classe è abilitata dal fatto che essa realizzi l'interfaccia `java.io.Serializable`, e precisa: «*Classes that do not implement this interface will not have any of their state serialized or deserialized. All subtypes of a serializable class are themselves serializable.*» In italiano: una classe che non realizza `Serializable` **non** ha il suo stato né scritto né letto, e **tutte le sottoclassi** di una classe serializzabile sono a loro volta serializzabili.
>
> *Fonte:* [Serializable (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/Serializable.html)

Il [Capitolo 10](10-classi-astratte-e-interfacce.md) ha mostrato che una classe può realizzare quante interfacce vuole; qui è la stessa sintassi, con la particolarità che non c'è nulla da implementare.

```java
// una classe serializzabile: si aggiunge solo "implements Serializable"
class Libro implements java.io.Serializable {
    private String titolo;
    private int pagine;
    // ... costruttore, metodi ...
}
```

### 15.5.3 `writeObject` e `readObject`

Per scrivere l'oggetto si usa `writeObject`, per rileggerlo `readObject`. Il secondo restituisce un `Object`, quindi serve un **cast** verso il tipo reale (sezione 9.5).

> [!NOTE]
> **Approfondimento esterno — `writeObject` e `readObject`**
> La documentazione ufficiale riporta le firme `public final void writeObject(Object obj) throws IOException` e `public final Object readObject() throws IOException, ClassNotFoundException`. Per `writeObject` elenca tra le cause `NotSerializableException` («*Some object to be serialized does not implement the java.io.Serializable interface*») e `InvalidClassException`. Per `readObject` elenca `ClassNotFoundException` («*Class of a serialized object cannot be found*»), `InvalidClassException`, `StreamCorruptedException` («*Control information in the stream is inconsistent*») e `OptionalDataException` («*Primitive data was found in the stream instead of objects*»).
>
> *Fonte:* [ObjectOutputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectOutputStream.html) e [ObjectInputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectInputStream.html)

La differenza tra le due firme è importante per l'esame: `readObject` dichiara **due** eccezioni controllate, `IOException` e `ClassNotFoundException`. La seconda **non è una `IOException`**: se un `try`/`catch` gestisce solo l'una, l'altra va gestita a parte, oppure dichiarata con `throws` (errore tipico 7). `ClassNotFoundException` indica che i byte descrivono un oggetto di una classe che la macchina virtuale in esecuzione non conosce: succede quando chi legge non ha a disposizione la classe con cui l'oggetto è stato scritto.

Un esempio completo salva un oggetto e lo rilegge, in un solo programma con due metodi. Per ora la classe non dichiara la costante di versione: la sezione 15.8 spiega perché in un programma vero va dichiarata.

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Libro implements Serializable {
    private String titolo;
    private int pagine;

    public Libro(String titolo, int pagine) {
        this.titolo = titolo;
        this.pagine = pagine;
    }

    public String getTitolo() { return titolo; }
    public int getPagine() { return pagine; }

    @Override
    public String toString() {
        return "Libro[" + titolo + ", " + pagine + " pagine]";
    }
}

public class SalvaLibro {
    static void salva(Libro l, String nomeFile) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(nomeFile));
        out.writeObject(l);               // l'oggetto intero diventa byte
        out.close();
    }

    static Libro carica(String nomeFile) throws IOException, ClassNotFoundException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(nomeFile));
        Libro l = (Libro) in.readObject(); // readObject restituisce Object: serve il cast
        in.close();
        return l;
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Libro a = new Libro("Algoritmi", 320);
        salva(a, "libro.dat");
        Libro b = carica("libro.dat");
        System.out.println(b);
        System.out.println(a == b);
        System.out.println(a.getTitolo().equals(b.getTitolo()) && a.getPagine() == b.getPagine());
    }
}
```

L'output è:

```text
Libro[Algoritmi, 320 pagine]
false
true
```

Riga per riga. La classe `Libro` dichiara `implements Serializable` e basta: nessuna riga in più per la conversione. In `salva`, `writeObject(l)` converte l'oggetto in byte e li scrive nel file. In `carica`, `readObject()` legge i byte e costruisce un oggetto; poiché il tipo di ritorno è `Object`, il cast `(Libro)` è obbligatorio. In `main` creiamo `a`, lo salviamo, lo ricarichiamo in `b` e confrontiamo.

I due confronti finali dicono qualcosa di profondo. `a == b` è `false`: i due riferimenti indicano **oggetti diversi**. Ma i campi coincidono. Lo avevamo anticipato nel [Capitolo 8](08-riferimenti-e-memoria.md) (sezione 8.4.5): un oggetto letto da un file o ricevuto dalla rete è un **oggetto nuovo**, costruito leggendo i byte, con gli stessi valori dell'originale ma un'altra identità. Il confronto di identità non può dire altro; per sapere se due oggetti sono «uguali nel contenuto» serve `equals`.

### 15.5.4 Il costruttore non viene richiamato

Un punto che spiega molti comportamenti inattesi: quando `readObject` ricostruisce un oggetto di una classe serializzabile, **non esegue il suo costruttore**. I campi vengono riempiti direttamente con i valori letti dai byte. Il costruttore (con le sue stampe, i suoi controlli e i suoi valori iniziali) è stato eseguito una sola volta, quando l'oggetto è stato creato la prima volta, ed è eseguito di nuovo solo se l'oggetto viene creato con `new`.

### 15.5.5 Il cast e `ClassCastException`

Il cast di `readObject` ha le stesse regole di ogni cast ([Capitolo 9](09-ereditarieta-e-polimorfismo.md)): se l'oggetto letto non è del tipo indicato, il programma lancia `ClassCastException`. È un errore di chi legge: il file contiene un oggetto di una classe diversa da quella attesa (per esempio si è letto `(Libro)` un file che contiene un `String`).

---

## 15.6 Che cosa rende serializzabile una classe

`implements Serializable` è il passo necessario, ma non sempre sufficiente. Il compilatore non controlla nulla: tutti i problemi si scoprono **a tempo di esecuzione**, quando `writeObject` o `readObject` vengono eseguiti, con un'eccezione.

Le condizioni che una classe deve soddisfare sono tre.

1. La classe **realizza `Serializable`**. Altrimenti `writeObject` lancia `NotSerializableException`.
2. Ogni **variabile d'istanza di un tipo classe** deve essere a sua volta di una classe serializzabile (o essere `transient`, sezione 15.6.3). Un oggetto contiene altri oggetti, e per convertirlo in byte bisogna poter convertire anche loro. Le classi della libreria che usiamo di solito lo sono già: `String`, i wrapper come `Integer` e `Double`, gli array, e le collezioni `ArrayList`, `LinkedList`, `HashMap`, `TreeMap`.
3. La **superclasse** diretta, se esiste, è serializzabile, **oppure** ha un costruttore senza parametri accessibile (sezione 15.6.2).

### 15.6.1 Un campo non serializzabile

Il caso più frequente è una classe serializzabile che contiene un oggetto di una classe che non lo è. Nell'esempio, `Ordine` è serializzabile ma contiene un `Cliente` che non lo è.

```java
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Cliente {                       // NON serializzabile
    String nome = "Anna";
}

class Ordine implements Serializable {  // serializzabile, ma contiene un Cliente
    int numero = 7;
    Cliente cliente = new Cliente();
}

public class CampoNonSerializzabile {
    public static void main(String[] args) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("ordine.dat"));
        try {
            out.writeObject(new Ordine());
        } catch (IOException e) {
            System.out.println("Errore: " + e);
        } finally {
            out.close();
        }
    }
}
```

```text
Errore: java.io.NotSerializableException: Cliente
```

Il messaggio dell'eccezione è il **nome della classe** che non è serializzabile: ci dice dove cercare. La catena si interrompe al primo anello debole: basta *un* campo di una classe non serializzabile per far fallire l'intero oggetto. Le due soluzioni sono far realizzare `Serializable` anche a `Cliente`, oppure dichiarare il campo `transient` (sezione 15.6.3), se non serve salvarlo.

> [!NOTE]
> **Approfondimento esterno — Le eccezioni della serializzazione**
> `NotSerializableException` è descritta come «*Thrown when an instance is required to have a Serializable interface. The serialization runtime or the class of the instance can throw this exception. The argument should be the name of the class.*». È una sottoclasse di `ObjectStreamException`, che a sua volta è una sottoclasse di `IOException`: anche `InvalidClassException`, `StreamCorruptedException` e `OptionalDataException` lo sono. Per questo un `catch (IOException e)` le prende tutte, mentre `ClassNotFoundException`, che non è una `IOException`, no.
>
> *Fonte:* [NotSerializableException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/NotSerializableException.html) e [ObjectStreamException (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectStreamException.html)

### 15.6.2 La superclasse

Se una classe `Fattura` serializzabile **estende** una classe `Documento` che **non** è serializzabile, i campi di `Documento` non vengono salvati: quando si ricostruisce l'oggetto, quella parte è reinizializzata eseguendo il **costruttore senza parametri** di `Documento`. Vediamo che cosa succede.

> [!NOTE]
> **Approfondimento esterno — Superclasse non serializzabile**
> La documentazione ufficiale di `Serializable` precisa: «*During deserialization, the fields of non-serializable superclasses will be initialized using the no-arg constructor of the first (bottommost) non-serializable superclass. This constructor must be accessible to the subclass that is being deserialized. It is an error to declare a class Serializable if this is not the case; the error will be detected at runtime.*»
>
> *Fonte:* [Serializable (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/Serializable.html)

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Documento {                         // NON serializzabile
    String autore = "anonimo";
    Documento() {
        System.out.println("Documento()");
    }
}

class Fattura extends Documento implements Serializable {
    double importo;
    Fattura(double importo) {
        System.out.println("Fattura()");
        this.importo = importo;
    }
}

public class SuperclasseNonSerializzabile {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Fattura f = new Fattura(250.0);       // stampa Documento() e Fattura()
        f.autore = "Rossi";

        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("fattura.dat"));
        out.writeObject(f);
        out.close();

        System.out.println("--- lettura ---");
        ObjectInputStream in = new ObjectInputStream(new FileInputStream("fattura.dat"));
        Fattura g = (Fattura) in.readObject(); // stampa Documento(), non Fattura()
        in.close();
        System.out.println(g.autore + " " + g.importo);
    }
}
```

L'output è:

```text
Documento()
Fattura()
--- lettura ---
Documento()
anonimo 250.0
```

Seguiamo l'esecuzione. Con `new Fattura(250.0)` parte prima il costruttore della superclasse (stampa `Documento()`, [Capitolo 9](09-ereditarieta-e-polimorfismo.md), sezione 9.3) e poi quello della sottoclasse (stampa `Fattura()`). Poi `f.autore = "Rossi"`. In lettura, `readObject` ricostruisce l'oggetto senza eseguire il costruttore di `Fattura` (sezione 15.5.4), ma poiché `Documento` non è serializzabile, il suo costruttore **viene** eseguito: appare di nuovo la stampa `Documento()`, e il campo `autore` torna al valore del costruttore, `"anonimo"`, **non** `"Rossi"`. Il campo `importo` è invece quello salvato: `250.0`.

Se `Documento` non avesse un costruttore senza parametri (per esempio solo `Documento(String autore)`), la lettura fallirebbe. Per evitare tutte queste complicazioni, nella pratica basta rendere serializzabile anche la superclasse, e tutta la catena è salvata.

### 15.6.3 I campi `static` e i campi `transient`

Due categorie di campi **non** vengono salvate.

I campi **`static`** appartengono alla classe, non a un oggetto ([Capitolo 7](07-classi-e-oggetti.md), sezione 7.4): non sono parte dello stato dell'oggetto, quindi la serializzazione li ignora. Dopo la lettura, un campo `static` ha il valore che ha in quel momento la classe, non quello di quando l'oggetto fu scritto.

I campi **`transient`** sono quelli che il programmatore esclude volontariamente. La parola chiave `transient` si mette tra i modificatori del campo, e significa «questo campo non fa parte dello stato persistente dell'oggetto». Si usa per un dato che non ha senso salvare (una password in chiaro, un valore calcolato che si può ricalcolare, un oggetto non serializzabile).

> [!NOTE]
> **Approfondimento esterno — Campi `transient` e `static`**
> La documentazione ufficiale di `ObjectInputStream` dice: «*Fields declared as transient or static are ignored by the deserialization process.*» Per i campi non letti precisa che la memoria dell'oggetto è «*allocated for the object and initialized to zero (NULL)*»: un campo escluso riprende dunque il **valore predefinito** del suo tipo.
>
> *Fonte:* [ObjectInputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectInputStream.html)

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Sessione implements Serializable {
    String utente;
    transient String token;          // non viene salvato
    transient int tentativi;         // non viene salvato
    transient boolean attiva;        // non viene salvato
    static int aperte = 0;           // non fa parte dell'oggetto

    Sessione(String utente, String token) {
        this.utente = utente;
        this.token = token;
        this.tentativi = 3;
        this.attiva = true;
    }
}

public class CampiEsclusi {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Sessione s = new Sessione("anna", "abc123");
        Sessione.aperte = 5;

        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("sessione.dat"));
        out.writeObject(s);
        out.close();

        Sessione.aperte = 99;        // la classe cambia dopo la scrittura

        ObjectInputStream in = new ObjectInputStream(new FileInputStream("sessione.dat"));
        Sessione r = (Sessione) in.readObject();
        in.close();

        System.out.println(r.utente + " " + r.token + " " + r.tentativi + " " + r.attiva);
        System.out.println("aperte = " + Sessione.aperte);
    }
}
```

L'output è:

```text
anna null 0 false
aperte = 99
```

Il campo `utente` è tornato com'era (`"anna"`). I tre campi `transient` hanno il valore predefinito del loro tipo: `null` per l'oggetto `String`, `0` per l'`int`, `false` per il `boolean`. Il campo `static` `aperte` vale `99`, cioè il valore attuale della classe, non il `5` di quando l'oggetto fu scritto. Per rispondere in modo sintetico alla domanda «a che cosa serve `transient`»: serve a **escludere un campo dalla serializzazione**; il campo, dopo la lettura, ha il valore predefinito del suo tipo.

---

## 15.7 Lo stesso oggetto scritto due volte

La macchina virtuale tiene traccia, dentro **un singolo** `ObjectOutputStream`, degli oggetti che ha già scritto, assegnando a ciascuno un **numero d'ordine** (il *serial number* della terminologia del corso). Se lo stesso oggetto viene passato di nuovo a `writeObject`, **non viene riscritto**: nel flusso finisce solo quel numero d'ordine, un riferimento all'oggetto già scritto. È una scelta sensata: evita di duplicare oggetti condivisi e permette di salvare strutture con riferimenti circolari. Ma ha una conseguenza che sorprende.

> [!NOTE]
> **Approfondimento esterno — Riferimenti multipli allo stesso oggetto**
> La documentazione ufficiale di `ObjectOutputStream` dice che «*Multiple references to a single object are encoded using a reference sharing mechanism so that graphs of objects can be restored to the same shape as when the original was written*». Il metodo `public void reset() throws IOException` «*will disregard the state of any objects already written to the stream*»: gli oggetti scritti prima «*will be written to the stream again*».
>
> *Fonte:* [ObjectOutputStream (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/ObjectOutputStream.html)

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Segnalino implements Serializable {
    int valore;
    Segnalino(int valore) { this.valore = valore; }
}

public class DueVolte {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Segnalino s = new Segnalino(1);

        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("due.dat"));
        out.writeObject(s);
        s.valore = 2;                    // modifica DOPO la prima scrittura
        out.writeObject(s);              // stesso oggetto: scrive solo il numero d'ordine
        out.close();

        ObjectInputStream in = new ObjectInputStream(new FileInputStream("due.dat"));
        Segnalino a = (Segnalino) in.readObject();
        Segnalino b = (Segnalino) in.readObject();
        in.close();

        System.out.println(a.valore + " " + b.valore);
        System.out.println(a == b);
    }
}
```

```text
1 1
true
```

Il valore `2` non è mai stato scritto: la seconda `writeObject` ha scritto solo il riferimento al primo oggetto, che conteneva ancora `1`. In lettura, `a` e `b` sono **lo stesso oggetto** (`a == b` è `true`). Il caso tipico in cui questo diventa una trappola è un ciclo che scrive lo **stesso oggetto** modificato a ogni giro. Le vie d'uscita sono due: creare un oggetto **nuovo** a ogni scrittura, oppure chiamare `reset()` tra una scrittura e l'altra.

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Segnalino implements Serializable {
    int valore;
    Segnalino(int valore) { this.valore = valore; }
}

public class DueVolteReset {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Segnalino s = new Segnalino(1);

        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("reset.dat"));
        out.writeObject(s);
        s.valore = 2;
        out.reset();                     // dimentica gli oggetti già scritti
        out.writeObject(s);              // ora l'oggetto viene riscritto con il valore nuovo
        out.close();

        ObjectInputStream in = new ObjectInputStream(new FileInputStream("reset.dat"));
        Segnalino a = (Segnalino) in.readObject();
        Segnalino b = (Segnalino) in.readObject();
        in.close();

        System.out.println(a.valore + " " + b.valore);
    }
}
```

```text
1 2
```

---

## 15.8 La costante di versione: `serialVersionUID`

### 15.8.1 Il problema delle versioni

Un oggetto serializzato su un file vive molto più a lungo del programma che lo ha scritto. Supponiamo di salvare dei `Libro` oggi, e fra un mese di aggiungere un campo alla classe `Libro`. Se il programma nuovo prova a leggere il vecchio file, i byte descrivono una classe con **meno campi** di quella attuale: la lettura è davvero sicura?

Per rispondere a questa domanda, ogni classe serializzabile ha un **numero di versione**, il `serialVersionUID`. Quando si scrive un oggetto, il numero viene scritto insieme ai dati. Quando si legge, la macchina virtuale **confronta** il numero scritto nel file con quello della classe attuale: se coincidono procede, altrimenti rifiuta la lettura con `InvalidClassException`. È una protezione contro la lettura di dati scritti da una versione della classe incompatibile con quella attuale.

> [!NOTE]
> **Approfondimento esterno — `serialVersionUID`**
> La documentazione ufficiale di `Serializable` dice che una classe serializzabile può dichiarare esplicitamente il proprio `serialVersionUID` «*by declaring a field named "serialVersionUID" that must be static, final, and of type long*»: `ANY-ACCESS-MODIFIER static final long serialVersionUID = 42L;`. Se il numero letto dal flusso e quello della classe locale sono diversi, «*deserialization will result in an InvalidClassException*».
> Se la classe **non** lo dichiara, il numero viene **calcolato** dal sistema in base alla struttura della classe, e questo calcolo «*is highly sensitive to class details that may vary depending on compiler implementations, and can thus result in unexpected InvalidClassExceptions during deserialization*». Per questo «*it is strongly recommended that all serializable classes other than enum types explicitly declare serialVersionUID values*», e si consiglia il modificatore `private` («*since such declarations apply only to the immediately declaring class*»).
>
> *Fonte:* [Serializable (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/Serializable.html)

### 15.8.2 La dichiarazione esatta

La forma da saper scrivere a memoria è questa:

```java
private static final long serialVersionUID = 1L;
```

Ogni parola ha il suo ruolo, e un errore **non è segnalato dal compilatore**: sia `static`, sia `final`, sia `long` sono richiesti, e il **nome** deve essere esatto, con la `S`, la `V` e la `UID` maiuscole. Un nome scritto in modo diverso (`serialversionuid`, `serialVersionUid`, `serialVersionID`) è semplicemente un altro campo, perfettamente legale, che la serializzazione ignora: il numero di versione tornerebbe a essere calcolato in automatico, ma nessun errore avvertirebbe dello scambio. Per lo stesso motivo conviene scrivere sempre il suffisso `L` (`1L`): il valore `1` senza suffisso è un `int`, che Java converte automaticamente in `long`, quindi compila, ma la forma con `L` rende evidente il tipo.

Il valore del numero è una scelta di chi scrive la classe: `1L` va benissimo. Che cosa conta è che resti **lo stesso** finché la classe è compatibile con i dati già scritti, e **cambi** quando le modifiche rendono incompatibili i dati vecchi.

### 15.8.3 Un esempio di `InvalidClassException`

Una classe con la costante dichiarata si serializza normalmente:

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Ricetta implements Serializable {
    private static final long serialVersionUID = 1L;

    private String nome;
    private int minuti;

    public Ricetta(String nome, int minuti) {
        this.nome = nome;
        this.minuti = minuti;
    }

    @Override
    public String toString() {
        return "Ricetta[" + nome + ", " + minuti + " min]";
    }
}

public class ConVersione {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("ricetta.dat"));
        out.writeObject(new Ricetta("Focaccia", 40));
        out.close();

        ObjectInputStream in = new ObjectInputStream(new FileInputStream("ricetta.dat"));
        System.out.println((Ricetta) in.readObject());
        in.close();
    }
}
```

```text
Ricetta[Focaccia, 40 min]
```

Se ora si cambia la costante nella classe (da `1L` a `2L`), si ricompila e si **rilegge lo stesso file** senza riscriverlo, la lettura fallisce con un messaggio che riporta i due numeri:

```text
java.io.InvalidClassException: Ricetta; local class incompatible: stream classdesc serialVersionUID = 1, local class serialVersionUID = 2
```

L'eccezione dice il nome della classe e i due numeri a confronto: quello nei dati (`stream classdesc`) e quello della classe locale. Senza una costante dichiarata, lo stesso errore si presenta alla minima modifica della classe, con due numeri lunghi e privi di significato, calcolati dal sistema.

---

## 15.9 Array e collezioni in un colpo solo

Un array è un oggetto ([Capitolo 5](05-array-e-matrici.md), [Capitolo 8](08-riferimenti-e-memoria.md)), e come tale si serializza con **un solo** `writeObject`, purché il tipo degli elementi sia serializzabile. Lo stesso vale per le collezioni della libreria (`ArrayList`, `LinkedList`, `HashMap`, `TreeMap`; [Capitolo 12](12-generics-e-collezioni.md)). In lettura si usa un solo `readObject` e il cast verso il tipo array o collezione.

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;

class Libro implements Serializable {
    private String titolo;
    private int pagine;

    public Libro(String titolo, int pagine) {
        this.titolo = titolo;
        this.pagine = pagine;
    }

    @Override
    public String toString() {
        return titolo + " (" + pagine + ")";
    }
}

public class ArrayECollezioni {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Libro[] scaffale = { new Libro("Algoritmi", 320), new Libro("Reti", 410) };
        ArrayList<String> tag = new ArrayList<>();
        tag.add("java");
        tag.add("oggetti");

        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("scaffale.dat"));
        out.writeObject(scaffale);        // un solo writeObject per l'intero array
        out.writeObject(tag);             // e uno per la lista
        out.close();

        ObjectInputStream in = new ObjectInputStream(new FileInputStream("scaffale.dat"));
        Libro[] letto = (Libro[]) in.readObject();     // cast verso il tipo array
        ArrayList<?> lista = (ArrayList<?>) in.readObject();
        in.close();

        System.out.println(letto.length + " libri, il secondo e' " + letto[1]);
        System.out.println(lista);
    }
}
```

```text
2 libri, il secondo e' Reti (410)
[java, oggetti]
```

Due osservazioni. Prima di tutto, il tipo dell'array nel cast è il tipo **reale** (`Libro[]`), non `Object[]`. Poi, il cast verso una collezione generica ha un problema: a runtime l'informazione sul tipo degli elementi non esiste più ([Capitolo 12](12-generics-e-collezioni.md), sezione 12.2), per cui il compilatore **non può controllare** un cast come `(ArrayList<String>) in.readObject()`. Se lo si scrive, la compilazione riesce, ma `javac` stampa una nota (`Note: ... uses unchecked or unsafe operations.`): non è un errore, e il programma funziona. Nell'esempio abbiamo usato `ArrayList<?>` (una lista di tipo ignoto, di cui si possono comunque stampare e leggere gli elementi come `Object`) per evitare la nota.

---

## 15.10 Più oggetti in un file

### 15.10.1 Scrivere e rileggere più oggetti, fino alla fine

Un programma che salva molti oggetti ha due alternative. La prima è scrivere un solo oggetto di tipo collezione che li contiene tutti (sezione 15.9). La seconda è scrivere **un `writeObject` per oggetto**, uno dopo l'altro, e rileggerli con il ciclo della sezione 15.4: `while (true)` con `catch (EOFException)`. Poiché `readObject` dichiara anche `ClassNotFoundException`, che non è una `IOException`, qui il `catch` per essa va aggiunto.

```java
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;

class Libro implements Serializable {
    private String titolo;
    private int pagine;

    public Libro(String titolo, int pagine) {
        this.titolo = titolo;
        this.pagine = pagine;
    }

    public int getPagine() { return pagine; }

    @Override
    public String toString() {
        return titolo + " (" + pagine + ")";
    }
}

public class PiuOggetti {
    static void scrivi(String nomeFile) throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(nomeFile));
        out.writeObject(new Libro("Algoritmi", 320));   // un writeObject per oggetto
        out.writeObject(new Libro("Reti", 410));
        out.writeObject(new Libro("Database", 280));
        out.close();
    }

    static ArrayList<Libro> leggi(String nomeFile) throws IOException {
        ArrayList<Libro> libri = new ArrayList<>();
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(nomeFile));
        try {
            while (true) {
                Libro l = (Libro) in.readObject();
                libri.add(l);
            }
        } catch (EOFException e) {
            // fine del file: uscita normale
        } catch (ClassNotFoundException e) {
            System.out.println("Classe sconosciuta: " + e.getMessage());
        } finally {
            in.close();
        }
        return libri;
    }

    public static void main(String[] args) throws IOException {
        scrivi("libri.dat");
        ArrayList<Libro> libri = leggi("libri.dat");
        int totale = 0;
        for (int i = 0; i < libri.size(); i++) {
            System.out.println(libri.get(i));
            totale += libri.get(i).getPagine();
        }
        System.out.println("Pagine totali: " + totale);
    }
}
```

```text
Algoritmi (320)
Reti (410)
Database (280)
Pagine totali: 1010
```

Il ciclo è lo stesso del caso dei primitivi, con due differenze di forma. La prima: `readObject` restituisce un `Object`, quindi **il cast** `(Libro)` è dentro il ciclo. La seconda: il `catch` per `EOFException` **non** è l'unico, perché va gestita anche `ClassNotFoundException`. Il `catch (EOFException)` e il `catch (ClassNotFoundException)` non sono in relazione di sottoclasse, quindi si possono mettere in qualunque ordine; se si volesse aggiungere un `catch (IOException)` generico, andrebbe **dopo** `EOFException`.

Una variante frequente, quando si conosce il numero di oggetti in anticipo, è scrivere **prima il numero** con `writeInt` e poi gli oggetti, e rileggere con un ciclo `for` senza bisogno di `EOFException`: lo stesso flusso accetta infatti primitivi e oggetti mescolati, purché si rilegga nello stesso ordine.

### 15.10.2 Aggiungere in coda: con `ObjectOutputStream` non si può

Con i file di testo, aggiungere in coda è facile: si apre il file con `new FileWriter(nome, true)` (sezione 14.3). Si potrebbe pensare di fare lo stesso con `new ObjectOutputStream(new FileOutputStream(nome, true))`. Il programma compila, la scrittura riesce, ma il file diventa **illeggibile**.

La ragione è l'intestazione: ogni nuovo `ObjectOutputStream` ne scrive una all'inizio del suo flusso, e un `ObjectInputStream` si aspetta di trovarla **una sola volta**, all'inizio del file. Con l'apertura in coda, il file contiene due intestazioni, una a metà.

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class CodaErrata {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        ObjectOutputStream out1 = new ObjectOutputStream(new FileOutputStream("coda.dat"));
        out1.writeObject("uno");
        out1.close();

        ObjectOutputStream out2 = new ObjectOutputStream(new FileOutputStream("coda.dat", true));
        out2.writeObject("due");                 // seconda intestazione in mezzo al file
        out2.close();

        ObjectInputStream in = new ObjectInputStream(new FileInputStream("coda.dat"));
        try {
            System.out.println(in.readObject());
            System.out.println(in.readObject());
        } catch (IOException e) {
            System.out.println("Errore: " + e);
        } finally {
            in.close();
        }
    }
}
```

```text
uno
Errore: java.io.StreamCorruptedException: invalid type code: AC
```

La prima lettura riesce, la seconda trova i byte della seconda intestazione dove si aspettava un oggetto, e lancia `StreamCorruptedException`. Le soluzioni sono due. La prima: **rileggere tutto, aggiungere il nuovo oggetto alla lista e riscrivere l'intero file** con un solo `ObjectOutputStream`. La seconda: usare, per un file di record da aggiornare in coda, `DataOutputStream` con `new FileOutputStream(nome, true)`, che non scrive nessuna intestazione e quindi si può aprire in coda quante volte si vuole (e si rilegge con `DataInputStream`, sezione 15.4).

---

## 15.11 Lo stesso flusso, un altro mezzo

### 15.11.1 La destinazione la decide il flusso avvolto

Un `ObjectOutputStream` non sa che cosa ci sia dietro: sa soltanto convertire un oggetto in byte e passarli al flusso di byte che gli è stato dato nel costruttore. Sarà **quel flusso** a decidere dove vanno a finire. Se è un `FileOutputStream`, i byte finiscono sul disco. Se è il flusso di uscita di una connessione di rete, finiscono sulla rete, verso un altro programma, che li legge con un `ObjectInputStream` avvolto attorno al flusso di ingresso della connessione.

```java
// i byte finiscono su DISCO
ObjectOutputStream suFile = new ObjectOutputStream(new FileOutputStream("dati.dat"));

// i byte finiscono IN RETE, verso il programma all'altro capo del socket
ObjectOutputStream suRete = new ObjectOutputStream(socket.getOutputStream());
```

Le due righe sono quasi identiche, e questa somiglianza è la trappola. Se una traccia dice «**invia** l'oggetto al server» e noi costruiamo l'`ObjectOutputStream` attorno a un `FileOutputStream`, abbiamo scritto un programma che serializza perfettamente ma **non comunica con nessuno**: ha risolto un problema diverso da quello richiesto. Il verbo della traccia dice quale flusso avvolgere: «salva», «scrivi su file» chiedono un file; «invia», «trasmetti», «spedisci sulla connessione» chiedono il flusso della connessione. Come si ottengono `socket.getOutputStream()` e `socket.getInputStream()` è argomento del [Capitolo 19](19-networking.md); qui ci interessa il principio: **tutto ciò che sappiamo su `writeObject` e `readObject` vale invariato**, cambia solo ciò che si avvolge.

| | Serializzazione su **file** | Serializzazione su **rete** |
|---|---|---|
| Flusso avvolto in scrittura | `new FileOutputStream(nome)` | `socket.getOutputStream()` |
| Flusso avvolto in lettura | `new FileInputStream(nome)` | `socket.getInputStream()` |
| Chi apre il canale | nessuno: basta il nome | il client apre il socket verso il server, il server accetta |
| Quando si legge | quando si vuole, anche dopo giorni | subito: dall'altra parte c'è qualcuno che aspetta |
| Se si sbaglia mezzo | compare un file nella cartella | non arriva niente al destinatario |

### 15.11.2 Due avvertenze sull'apertura dei flussi in rete

Sul file l'intestazione è già scritta quando si legge; in rete no, e due conseguenze vanno anticipate, perché sono nella documentazione dei costruttori.

- **L'intestazione e il blocco.** Il costruttore di `ObjectOutputStream` scrive subito l'intestazione, e quello di `ObjectInputStream` **si ferma ad aspettarla** (approfondimento della sezione 15.3.3). La documentazione del costruttore di `ObjectOutputStream` suggerisce a chi scrive di svuotare subito il flusso (`flush()`), perché gli `ObjectInputStream` che ricevono non restino bloccati nella lettura dell'intestazione. Per questo, in un programma di rete, l'`ObjectOutputStream` si apre **per primo**, e si fa `flush()` dopo ogni invio: se i due programmi aprissero entrambi per primo il flusso di ingresso, resterebbero bloccati ad aspettarsi a vicenda.
- **La classe deve esistere dall'altra parte.** Chi legge deve avere la **stessa classe**, con lo stesso nome e la stessa costante di versione: altrimenti `ClassNotFoundException` o `InvalidClassException` (sezione 15.8).

I dettagli del socket sono nel [Capitolo 19](19-networking.md).

---

## 15.12 Le eccezioni della serializzazione

Riassumiamo le eccezioni che incontriamo, con la causa e il punto in cui si presentano. Tutte, tranne `ClassNotFoundException`, sono sottoclassi di `IOException`.

| Eccezione | Superclasse | Quando | Dove si manifesta |
|---|---|---|---|
| `FileNotFoundException` | `IOException` | il file non si può aprire | `new FileInputStream(...)`, `new FileOutputStream(...)` |
| `EOFException` | `IOException` | i dati sono finiti durante una lettura (anche file vuoto) | `readInt`, `readUTF`, `readObject`, `new ObjectInputStream(...)` |
| `StreamCorruptedException` | `ObjectStreamException` | intestazione o controllo del flusso non validi: file non scritto da `ObjectOutputStream` | `new ObjectInputStream(...)`, `readObject` |
| `OptionalDataException` | `ObjectStreamException` | si legge un oggetto ma nel flusso c'è un dato primitivo | `readObject` |
| `NotSerializableException` | `ObjectStreamException` | si scrive un oggetto (o un campo) di una classe non serializzabile | `writeObject` |
| `InvalidClassException` | `ObjectStreamException` | `serialVersionUID` diverso, costruttore mancante in una superclasse non serializzabile, … | `readObject`, talvolta `writeObject` |
| `ClassNotFoundException` | `ReflectiveOperationException` (non è una `IOException`) | la classe dell'oggetto letto non è disponibile | `readObject` |
| `ClassCastException` | `RuntimeException` | il cast di `readObject` verso un tipo sbagliato | dopo `readObject` (non controllata) |

La gerarchia ha due conseguenze pratiche. Un `catch (IOException e)` cattura tutte le eccezioni della tabella **tranne** le ultime due: va quindi accompagnato da un `catch (ClassNotFoundException e)` quando si usa `readObject`. E nei blocchi `catch` in sequenza, `EOFException` e le altre sottoclassi vanno **prima** della superclasse `IOException`.

---

## 15.13 Dalla traccia al codice

Le tracce d'esame sulla serializzazione sono scarne: indicano il comportamento e il formato dell'output, e lasciano a chi scrive il compito di trovare le strutture giuste. Vediamo come si traducono le frasi tipiche.

| La traccia dice… | Si scrive… |
|---|---|
| «la classe deve poter essere convertita in una sequenza di byte e ricostruita» | `implements Serializable` (e nessun metodo da aggiungere) |
| «dichiarare una costante di versione per la serializzazione di tipo `long` pari a 1» | `private static final long serialVersionUID = 1L;` (nome esatto) |
| «tutte le variabili d'istanza devono essere private» | `private` su ogni campo, con i metodi di lettura richiesti |
| «il costruttore riceve nell'ordine il nome e il cognome» | l'**ordine dei parametri** è parte della consegna: `(String nome, String cognome)` |
| «la sua rappresentazione testuale è nella forma `X[a b]`» | `toString()` con `public` e `@Override`, stringa **identica** (spazi, parentesi) |
| «salva su file», «scrivi in un file binario» | `ObjectOutputStream` attorno a `FileOutputStream` |
| «invia al server», «trasmetti sulla connessione» | `ObjectOutputStream` attorno al flusso di uscita del socket |
| «ricostruisci l'oggetto e restituiscilo» | `(Tipo) in.readObject()` con il **cast**, e `return` |
| «leggi tutti gli oggetti fino alla fine» | ciclo `while (true)` con `catch (EOFException)` (sezione 15.10) |
| «in caso di fallimento restituisci `null`» | un `catch` che restituisce `null`, per **tutte** le eccezioni del tipo di operazione |
| «aggiungi un record in coda al file» | non con `ObjectOutputStream`; con `DataOutputStream` e `true` (sezione 15.10.2) |

---

## Come esce all'esame

La serializzazione è comparsa in un appello ufficiale.

**Appello dell'8 luglio 2026 (EXAM3) — Esercizio 3, 13 punti: serializzazione di oggetti su socket.** La traccia presentava un server già in ascolto (che non andava scritto), con indirizzo e porta noti, il quale riceve un oggetto, lo rimanda indietro identico sulla stessa connessione e chiude. Chiedeva due classi.

1. Una classe di dati con **nome e cognome**, costruttore con i due valori **in quest'ordine**, metodi di lettura, **variabili d'istanza tutte private**, la capacità di essere **convertita in byte e ricostruita altrove**, una **costante di versione** di tipo `long` pari a `1`, e una rappresentazione testuale nella forma indicata dalla traccia.
2. Una classe `Client` con un metodo che riceve un oggetto della prima classe e ne restituisce uno: instaura la connessione verso le coordinate date, **trasmette l'oggetto ricevuto come parametro**, **attende** quello che il server rimanda indietro, lo **ricostruisce** e lo restituisce al chiamante. In caso di **fallimento** della comunicazione il metodo restituisce `null`.

L'output atteso, indicato nella traccia, era la rappresentazione testuale dell'oggetto restituito.

I concetti del capitolo che servivano sono `Serializable` (sezione 15.5), il `serialVersionUID` nella forma esatta (sezione 15.8), `writeObject` e `readObject` con il cast (sezione 15.5.3) e la scelta della destinazione (sezione 15.11), insieme al socket ([Capitolo 19](19-networking.md)) e alla gestione dei fallimenti con `try`/`catch` ([Capitolo 13](13-eccezioni.md)). I vincoli letterali erano numerosi: l'ordine dei parametri del costruttore, il modificatore `private` su tutti i campi, il tipo `long` e il valore della costante, il formato esatto del `toString`, il comportamento `null` in caso di errore, e il fatto che l'oggetto dovesse **viaggiare sulla connessione**, non su un file.

---

## Scheletri da esame

Sono i frammenti minimi da saper scrivere a memoria, su un editor senza aiuti. Ciascuno è una classe che si compila da sola.

### Scheletro 1 — Scrivere valori primitivi e stringhe in un file binario

*Quando si usa:* «scrivi in un file binario il nome, l'età e …»; la traccia può imporre la chiusura nel `finally`.

```java
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;

public class ScheletroScritturaBinaria {
    static void scrivi(String nomeFile, String nome, int eta, double altezza) throws IOException {
        ObjectOutputStream out = null;                          // fuori dal try, a null
        try {
            out = new ObjectOutputStream(new FileOutputStream(nomeFile));
            out.writeUTF(nome);                                 // un metodo per tipo
            out.writeInt(eta);
            out.writeDouble(altezza);
        } finally {
            if (out != null) {                                  // guardia: l'apertura potrebbe aver fallito
                out.close();                                    // svuota il buffer e chiude
            }
        }
    }
}
```

- **Eccezioni:** `new FileOutputStream(String)` dichiara `FileNotFoundException`; `new ObjectOutputStream(...)`, i metodi `write...` e `close()` dichiarano `IOException`: il `throws IOException` le copre tutte.
- **Import necessari:** `java.io.FileOutputStream`, `java.io.IOException`, `java.io.ObjectOutputStream`.
- **Variante:** con `DataOutputStream` il costruttore non dichiara eccezioni, i metodi di scrittura sì (`IOException`); `import java.io.DataOutputStream`.

### Scheletro 2 — Leggere valori da un file binario fino alla fine

*Quando si usa:* «leggi tutti i record del file …»; la fine del file si riconosce da `EOFException`.

```java
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;

public class ScheletroLetturaBinaria {
    static int sommaEta(String nomeFile) throws IOException {
        ObjectInputStream in = null;
        int somma = 0;
        try {
            in = new ObjectInputStream(new FileInputStream(nomeFile));
            try {
                while (true) {                                  // finché ce ne sono
                    String nome = in.readUTF();                 // si leggono TUTTI i campi del record,
                    int eta = in.readInt();                     // nello stesso ordine della scrittura
                    double altezza = in.readDouble();
                    somma += eta;
                }
            } catch (EOFException e) {
                // fine del file: uscita normale dal ciclo
            }
        } finally {
            if (in != null) {
                in.close();
            }
        }
        return somma;
    }
}
```

- **Eccezioni:** `new FileInputStream(String)` dichiara `FileNotFoundException`; `new ObjectInputStream(...)`, i metodi `read...` e `close()` dichiarano `IOException`. `EOFException` è una `IOException`: il `catch` specifico sta **dentro**, intorno al ciclo, e il `throws IOException` copre il resto.
- **Import necessari:** `java.io.EOFException`, `java.io.FileInputStream`, `java.io.IOException`, `java.io.ObjectInputStream`.
- **Ordine dei catch:** se nello stesso `try` si volesse anche `catch (IOException e)`, quello di `EOFException` va **prima**.

### Scheletro 3 — Serializzare e deserializzare un oggetto

*Quando si usa:* «salva l'oggetto su file» e «ricarica l'oggetto dal file».

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Voce implements Serializable {                              // la classe da salvare
    private static final long serialVersionUID = 1L;
    private String testo;

    public Voce(String testo) {
        this.testo = testo;
    }

    public String getTesto() {
        return testo;
    }
}

public class ScheletroOggetto {
    static void salva(Voce v, String nomeFile) throws IOException {
        ObjectOutputStream out = null;
        try {
            out = new ObjectOutputStream(new FileOutputStream(nomeFile));
            out.writeObject(v);                                  // l'oggetto intero
        } finally {
            if (out != null) {
                out.close();
            }
        }
    }

    static Voce carica(String nomeFile) throws IOException, ClassNotFoundException {
        ObjectInputStream in = null;
        try {
            in = new ObjectInputStream(new FileInputStream(nomeFile));
            return (Voce) in.readObject();                       // cast: readObject restituisce Object
        } finally {
            if (in != null) {
                in.close();
            }
        }
    }
}
```

- **Eccezioni:** `writeObject` dichiara `IOException` (e può lanciare `NotSerializableException`, che ne è una sottoclasse); `readObject` dichiara `IOException` **e** `ClassNotFoundException`. Il metodo `carica` le dichiara entrambe nel `throws`.
- **Import necessari:** `java.io.FileInputStream`, `java.io.FileOutputStream`, `java.io.IOException`, `java.io.ObjectInputStream`, `java.io.ObjectOutputStream`, `java.io.Serializable`.
- **`return` nel `try`:** il `finally` viene eseguito comunque prima che il metodo ritorni, quindi il flusso si chiude.

### Scheletro 4 — Leggere più oggetti fino alla fine del file

*Quando si usa:* «rileggi tutti gli oggetti scritti nel file».

```java
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.ArrayList;

public class ScheletroPiuOggetti {
    static ArrayList<Voce> caricaTutte(String nomeFile) throws IOException {
        ArrayList<Voce> voci = new ArrayList<>();
        ObjectInputStream in = null;
        try {
            in = new ObjectInputStream(new FileInputStream(nomeFile));
            while (true) {
                Voce v = (Voce) in.readObject();                 // cast dentro il ciclo
                voci.add(v);
            }
        } catch (EOFException e) {
            // fine del file: uscita normale
        } catch (ClassNotFoundException e) {
            System.out.println("Classe sconosciuta");           // readObject la dichiara a parte
        } finally {
            if (in != null) {
                in.close();
            }
        }
        return voci;
    }
}

class Voce implements java.io.Serializable {
    private static final long serialVersionUID = 1L;
    private String testo;

    public Voce(String testo) {
        this.testo = testo;
    }
}
```

- **Eccezioni:** `EOFException` ha il suo `catch`; `ClassNotFoundException` non è una `IOException` e ha un `catch` a parte; il resto delle `IOException` si propaga con `throws IOException`.
- **Import necessari:** `java.io.EOFException`, `java.io.FileInputStream`, `java.io.IOException`, `java.io.ObjectInputStream`, `java.util.ArrayList`.
- **`readObject` non restituisce `null` alla fine del file:** lancia `EOFException`. Un ciclo `while ((v = ...readObject()) != null)` è sbagliato.

### Scheletro 5 — La classe di dati serializzabile completa

*Quando si usa:* «definire la classe …, i cui oggetti devono poter essere convertiti in byte e ricostruiti, con costante di versione e rappresentazione testuale …». È la parte di classe di un esercizio di serializzazione.

```java
import java.io.Serializable;

class Contatto implements Serializable {
    private static final long serialVersionUID = 1L;            // nome esatto, tipo long

    private String nome;                                        // tutte le variabili private
    private String telefono;

    public Contatto(String nome, String telefono) {             // ordine dei parametri: come la traccia
        this.nome = nome;
        this.telefono = telefono;
    }

    public String getNome() {
        return nome;
    }

    public String getTelefono() {
        return telefono;
    }

    @Override
    public String toString() {                                  // formato identico a quello richiesto
        return "Contatto[" + nome + " " + telefono + "]";
    }
}

public class ScheletroClasseDati {
    public static void main(String[] args) {
        System.out.println(new Contatto("Anna", "0901234"));
    }
}
```

- **Che cosa controllare:** `implements Serializable` (nessun metodo da aggiungere), `private static final long serialVersionUID` con il nome scritto esattamente così, campi `private`, ordine dei parametri del costruttore uguale alla traccia, `toString` con `public`, stringa identica a quella dell'output atteso (spazi e parentesi comprese).
- **Import necessari:** `java.io.Serializable`.

---

## Errori tipici

> [!CAUTION]
> **Errore 1 — Leggere con un ordine o un tipo diversi da quelli di scrittura**
> Il file non contiene i tipi, solo i byte: se si leggono con un metodo sbagliato, Java non se ne accorge e restituisce numeri senza senso, **senza nessuna eccezione**.
>
> ```java
> // ERRATO: si scrive un int e poi un double, si legge un double e poi un int
> import java.io.FileInputStream;
> import java.io.FileOutputStream;
> import java.io.IOException;
> import java.io.ObjectInputStream;
> import java.io.ObjectOutputStream;
>
> public class OrdineSbagliato {
>     public static void main(String[] args) throws IOException {
>         ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("m.dat"));
>         out.writeInt(5);
>         out.writeDouble(2.5);
>         out.close();
>
>         ObjectInputStream in = new ObjectInputStream(new FileInputStream("m.dat"));
>         double d = in.readDouble();          // ma il primo valore è un int
>         int i = in.readInt();                // e il secondo è un double
>         in.close();
>         System.out.println(d + " " + i);
>     }
> }
> ```
>
> Il programma compila e stampa due valori privi di significato (sulla macchina di prova `1.1140607419E-313 0`), anziché `5` e `2.5`. La forma corretta rilegge **nello stesso ordine e con gli stessi tipi**: prima `readInt()`, poi `readDouble()`.

> [!CAUTION]
> **Errore 2 — Aspettarsi `null` o `-1` alla fine del file**
> `readObject`, `readInt`, `readUTF` non restituiscono un valore speciale alla fine: lanciano `EOFException`. Un ciclo che aspetta `null` non termina in modo pulito.
>
> ```java
> // ERRATO: readObject non restituisce null a fine file
> import java.io.FileInputStream;
> import java.io.IOException;
> import java.io.ObjectInputStream;
>
> public class AttesaNull {
>     public static void main(String[] args) throws IOException, ClassNotFoundException {
>         ObjectInputStream in = new ObjectInputStream(new FileInputStream("libri.dat"));
>         Object x;
>         while ((x = in.readObject()) != null) {   // al termine lancia EOFException
>             System.out.println(x);
>         }
>         in.close();
>     }
> }
> ```
>
> Compila, ma quando i dati finiscono il programma termina con `Exception in thread "main" java.io.EOFException`. Il ciclo corretto è `while (true)` con `catch (EOFException e)` fuori dal ciclo (sezione 15.4).

> [!CAUTION]
> **Errore 3 — `catch (IOException)` prima di `catch (EOFException)`**
> `EOFException` è una sottoclasse di `IOException`: il `catch` più specifico va **per primo**. Nell'ordine inverso il compilatore rifiuta il codice.
>
> ```java
> // ERRATO: il catch di EOFException non può mai essere raggiunto
> try {
>     while (true) {
>         System.out.println(in.readInt());
>     }
> } catch (IOException e) {
>     System.out.println("errore");
> } catch (EOFException e) {              // error: exception EOFException has already been caught
>     System.out.println("fine");
> }
> ```
>
> L'ordine corretto è `catch (EOFException e)` e poi, se serve, `catch (IOException e)`.

> [!CAUTION]
> **Errore 4 — La classe non realizza `Serializable`**
> Il compilatore non controlla: l'errore si presenta a runtime, alla prima `writeObject`.
>
> ```java
> // ERRATO: manca "implements Serializable"
> import java.io.FileOutputStream;
> import java.io.IOException;
> import java.io.ObjectOutputStream;
>
> class Biglietto {                          // manca implements Serializable
>     int numero = 12;
> }
>
> public class SenzaMarcatore {
>     public static void main(String[] args) throws IOException {
>         ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("b.dat"));
>         out.writeObject(new Biglietto());  // NotSerializableException: Biglietto
>         out.close();
>     }
> }
> ```
>
> Il programma compila e fallisce con `java.io.NotSerializableException: Biglietto`. Si corregge con `class Biglietto implements Serializable`.

> [!CAUTION]
> **Errore 5 — Un campo di una classe non serializzabile**
> `implements Serializable` sulla classe esterna non basta: ogni campo di tipo classe deve essere serializzabile. L'eccezione riporta il nome della classe che manca (sezione 15.6.1).
>
> ```java
> // ERRATO: Cliente non è serializzabile
> class Cliente { String nome = "Anna"; }
> class Ordine implements java.io.Serializable {
>     Cliente cliente = new Cliente();       // NotSerializableException: Cliente
> }
> ```
>
> Le correzioni sono due: far realizzare `Serializable` a `Cliente`, oppure dichiarare il campo `transient` se non serve salvarlo.

> [!CAUTION]
> **Errore 6 — Dimenticare il cast su `readObject`**
> `readObject` restituisce `Object`. L'assegnazione diretta a una variabile di tipo `Libro` non compila.
>
> ```java
> // ERRATO: manca il cast
> Libro l = in.readObject();      // error: incompatible types: Object cannot be converted to Libro
> ```
>
> Si scrive `Libro l = (Libro) in.readObject();`. Con il cast, il compilatore accetta e il controllo del tipo vero avviene a runtime (`ClassCastException` se l'oggetto letto è di un'altra classe).

> [!CAUTION]
> **Errore 7 — Non gestire `ClassNotFoundException`**
> `readObject` dichiara **due** eccezioni controllate. Se il metodo dichiara solo `throws IOException`, il compilatore protesta.
>
> ```java
> // ERRATO: manca ClassNotFoundException
> static Libro carica(String nome) throws IOException {
>     ObjectInputStream in = new ObjectInputStream(new FileInputStream(nome));
>     return (Libro) in.readObject();   // error: unreported exception ClassNotFoundException;
>                                       // must be caught or declared to be thrown
> }
> ```
>
> La si dichiara (`throws IOException, ClassNotFoundException`) oppure la si cattura con un `catch` a parte: non basta `catch (IOException e)`, perché `ClassNotFoundException` non è una sua sottoclasse.

> [!CAUTION]
> **Errore 8 — Passare un nome di file a `ObjectOutputStream`**
> Il costruttore accetta un **flusso di byte**, non una stringa.
>
> ```java
> // ERRATO: il costruttore non prende una String
> ObjectOutputStream out = new ObjectOutputStream("dati.dat");
> // error: incompatible types: String cannot be converted to OutputStream
> ```
>
> La forma corretta è `new ObjectOutputStream(new FileOutputStream("dati.dat"))` (sezione 15.1.2). Lo stesso vale per `ObjectInputStream` e `FileInputStream`.

> [!CAUTION]
> **Errore 9 — Non chiudere il flusso di scrittura**
> I dati passano per un buffer: senza `close()` (o `flush()`) restano in memoria e il file è incompleto o vuoto di dati.
>
> ```java
> // ERRATO: manca close(): il file contiene solo l'intestazione
> import java.io.EOFException;
> import java.io.FileInputStream;
> import java.io.FileOutputStream;
> import java.io.IOException;
> import java.io.ObjectInputStream;
> import java.io.ObjectOutputStream;
>
> public class SenzaClose {
>     public static void main(String[] args) throws IOException {
>         ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("s.dat"));
>         out.writeInt(42);                  // resta nel buffer
>         // out.close() dimenticata
>
>         ObjectInputStream in = new ObjectInputStream(new FileInputStream("s.dat"));
>         try {
>             System.out.println(in.readInt());
>         } catch (EOFException e) {
>             System.out.println("nessun dato nel file");
>         }
>     }
> }
> ```
>
> Il programma stampa `nessun dato nel file`. Con `close()` (o con `flush()`) il valore `42` verrebbe scritto davvero. Per `ObjectInputStream` e `DataInputStream` non c'è un buffer da svuotare, ma il flusso va chiuso comunque (sezione 14.2.2).

> [!CAUTION]
> **Errore 10 — Aprire un `ObjectOutputStream` in coda**
> Il file diventa illeggibile, perché ogni `ObjectOutputStream` scrive la propria intestazione (sezione 15.10.2).
>
> ```java
> // ERRATO: compila e scrive, ma il file poi non si rilegge
> ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("coda.dat", true));
> ```
>
> Alla lettura: `StreamCorruptedException: invalid type code: AC`. Si rilegge tutto, si aggiunge e si riscrive l'intero file; oppure si usa `DataOutputStream` con `true`.

> [!CAUTION]
> **Errore 11 — Riscrivere lo stesso oggetto modificato**
> Dentro un singolo `ObjectOutputStream`, un oggetto già scritto non viene riscritto: nel flusso va solo un riferimento al primo (sezione 15.7).
>
> ```java
> // ERRATO: si legge due volte il valore della prima scrittura
> Segnalino s = new Segnalino(1);
> out.writeObject(s);
> s.valore = 2;
> out.writeObject(s);        // scrive solo il riferimento: nel file ci sono due "1"
> ```
>
> Si crea un oggetto nuovo a ogni scrittura (`new Segnalino(2)`), oppure si chiama `out.reset()` tra le due scritture.

> [!CAUTION]
> **Errore 12 — Il nome della costante di versione scritto male**
> Il compilatore non segnala nulla: un nome sbagliato è un campo qualsiasi.
>
> ```java
> // ERRATO: ciascuna di queste righe, da sola, non è la costante di versione
> private static final long serialversionuid = 1L;   // minuscole
> private static final long serialVersionUid = 1L;   // "Uid"
> private static final int  serialVersionUID = 1;    // il tipo deve essere long
> private long serialVersionUID = 1L;                // mancano static e final
> ```
>
> La forma esatta è `private static final long serialVersionUID = 1L;` (sezione 15.8.2). In una traccia che la richiede, un nome diverso significa **non averla dichiarata**.

> [!CAUTION]
> **Errore 13 — Leggere con `ObjectInputStream` un file che non è stato scritto da `ObjectOutputStream`**
> Un file di testo, o un file di `DataOutputStream`, non ha l'intestazione attesa.
>
> ```java
> // ERRATO: "note.txt" è un file di testo
> ObjectInputStream in = new ObjectInputStream(new FileInputStream("note.txt"));
> // java.io.StreamCorruptedException: invalid stream header: 6369616F
> ```
>
> Chi legge deve usare la **stessa famiglia** con cui il file è stato scritto: testo con `Scanner`/`BufferedReader`, valori con `Data*` o `Object*`, oggetti con `Object*`.

> [!CAUTION]
> **Errore 14 — Serializzare sul flusso sbagliato**
> Quando la traccia dice «invia», avvolgere un `FileOutputStream` produce un programma che serializza correttamente e non comunica con nessuno.
>
> ```java
> // ERRATO se la traccia dice "invia al server": i byte finiscono su un file locale
> ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("copia.dat"));
> out.writeObject(persona);
>
> // Corretto: i byte finiscono sulla connessione
> ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
> out.writeObject(persona);
> out.flush();
> ```
>
> Il verbo della traccia decide il flusso (sezione 15.11). Il codice non dà errori in nessuno dei due casi: è il comportamento richiesto a non essere rispettato.

> [!CAUTION]
> **Errore 15 — Contare su un campo `transient` dopo la lettura**
> Un campo `transient` non viene salvato: dopo `readObject` ha il valore predefinito del tipo (sezione 15.6.3).
>
> ```java
> // ERRATO: il token serve ancora dopo la lettura
> class Sessione implements java.io.Serializable {
>     String utente;
>     transient String token;     // dopo readObject: null
> }
> ```
>
> Se un dato deve sopravvivere alla serializzazione, non va dichiarato `transient`. Se invece va escluso, il programma deve **ricalcolarlo** dopo la lettura.

---

## Riassunto

Un file di testo salva i dati come caratteri; un **flusso binario** li salva come byte, nella forma interna dei tipi. Per scrivere si avvolge un `FileOutputStream` in un `ObjectOutputStream` (o in un `DataOutputStream`), che ha un metodo per ogni tipo (`writeInt`, `writeDouble`, `writeBoolean`, `writeUTF` per le stringhe); per leggere si avvolge un `FileInputStream` in un `ObjectInputStream`, con i metodi corrispondenti. Il file **non porta i tipi**: si rilegge nello stesso ordine e con gli stessi tipi con cui si è scritto. Non esiste un `hasNext` né un valore speciale per la fine: ogni lettura **lancia `EOFException`**, e con essa si esce da un ciclo `while (true)`.

La **serializzazione** salva un oggetto intero: la classe realizza l'interfaccia vuota `Serializable`, e `writeObject`/`readObject` convertono l'oggetto in byte e viceversa, con il cast in lettura. La classe deve avere tutti i campi serializzabili (o `transient`), una superclasse serializzabile o con costruttore senza parametri, e i campi `static` e `transient` non vengono salvati. La costante `private static final long serialVersionUID` fissa la versione della classe: senza di essa, o con un valore diverso da quello dei dati, la lettura può fallire con `InvalidClassException`. Un oggetto già scritto in uno stesso flusso non viene riscritto (serve `reset()`), e `ObjectOutputStream` non si può aprire in coda. Lo stesso flusso funziona su un file e su una connessione di rete: la **destinazione** la decide il flusso avvolto.

### Concetti chiave

- **Flusso binario**: scrive i valori come byte, nella forma interna; più compatto del testo ma non leggibile con un editor; non porta i tipi.
- **`ObjectOutputStream` / `ObjectInputStream`**: avvolgono un flusso di byte; sanno scrivere e leggere primitivi, stringhe (`writeUTF`/`readUTF`) e oggetti (`writeObject`/`readObject`); costruttori che dichiarano `IOException` e non accettano un nome di file.
- **`DataOutputStream` / `DataInputStream`**: stessi metodi per primitivi e stringhe, ma niente oggetti e niente intestazione; non intercambiabili con `Object*`.
- **Stesso ordine e stessi tipi**: la lettura ripercorre la scrittura; un errore non dà eccezione ma valori sbagliati; si leggono tutti i campi di un record.
- **`EOFException`**: fine del file, lanciata da `readInt`, `readUTF`, `readObject`; sottoclasse di `IOException`; si cattura fuori dal ciclo `while (true)`, prima di `IOException`; `readObject` non restituisce `null`.
- **Serializzazione**: rappresentare un oggetto come sequenza di byte e ricostruirlo; l'oggetto ricostruito è un oggetto nuovo (`==` è `false`) e il suo costruttore non viene richiamato.
- **`Serializable`**: interfaccia vuota (marcatore); nessun metodo da implementare; i problemi si scoprono a runtime (`NotSerializableException`).
- **Requisiti**: campi di classi serializzabili, superclasse serializzabile o con costruttore senza parametri; `static` e `transient` non vengono salvati; i campi `transient` riprendono `null`/`0`/`false`.
- **`serialVersionUID`**: `private static final long`, nome esatto; confrontato in lettura (`InvalidClassException` se diverso).
- **Numero d'ordine degli oggetti**: lo stesso oggetto scritto due volte nello stesso flusso viene scritto solo la prima volta; `reset()` per riscriverlo.
- **Array e collezioni**: un solo `writeObject` e un solo `readObject` con cast al tipo reale.
- **Più oggetti**: un `writeObject` per oggetto e ciclo fino a `EOFException`; con `ObjectOutputStream` non si aggiunge in coda (seconda intestazione): `StreamCorruptedException`.
- **Il flusso avvolto decide la destinazione**: file o rete; il verbo della traccia («salva» o «invia») sceglie.

### API essenziali

| Classe | Costruttore / metodo | Eccezioni dichiarate |
|---|---|---|
| `FileOutputStream` | `FileOutputStream(String name)`, `FileOutputStream(String name, boolean append)` | `FileNotFoundException` |
| `FileInputStream` | `FileInputStream(String name)` | `FileNotFoundException` |
| `ObjectOutputStream` | `ObjectOutputStream(OutputStream out)` | `IOException` |
| `ObjectOutputStream` | `void writeInt(int val)`, `writeLong`, `writeDouble`, `writeBoolean`, `writeUTF(String str)` | `IOException` |
| `ObjectOutputStream` | `final void writeObject(Object obj)` | `IOException` (`NotSerializableException`, `InvalidClassException`) |
| `ObjectOutputStream` | `void reset()`, `void flush()`, `void close()` | `IOException` |
| `ObjectInputStream` | `ObjectInputStream(InputStream in)` | `IOException` (`StreamCorruptedException`, `EOFException`) |
| `ObjectInputStream` | `int readInt()`, `long readLong()`, `double readDouble()`, `boolean readBoolean()`, `String readUTF()` | `IOException` (`EOFException`) |
| `ObjectInputStream` | `final Object readObject()` | `IOException`, `ClassNotFoundException` |
| `ObjectInputStream` | `void close()` | `IOException` |
| `DataOutputStream` | `DataOutputStream(OutputStream out)`, `final void writeInt(int v)`, `writeDouble`, `writeUTF(String str)` | costruttore: nessuna; metodi: `IOException` |
| `DataInputStream` | `DataInputStream(InputStream in)`, `final int readInt()`, `readDouble`, `String readUTF()` | costruttore: nessuna; metodi: `IOException` (`EOFException`) |
| `EOFException` | sottoclasse di `IOException`: fine dei dati durante una lettura | controllata |
| `Serializable` | interfaccia vuota; `private static final long serialVersionUID` | — |
