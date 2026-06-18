# Esercizio 5: Serializzazione di Oggetti / Exercise 5: Object Serialization

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio introduce il concetto di **serializzazione** e **deserializzazione** degli oggetti in Java.

Il programma:
- crea un'istanza della classe `Species` con dei dati fittizi;
- serializza (salva) questo oggetto all'interno di un file binario chiamato `save.ser`;
- successivamente, legge il file `save.ser` per deserializzare (ricostruire) l'oggetto;
- stampa a schermo i valori degli attributi dell'oggetto appena caricato per verificarne la correttezza.

### Obiettivo didattico
L'obiettivo è consolidare:
- l'uso di `ObjectOutputStream` e `FileOutputStream` per il salvataggio di oggetti;
- l'uso di `ObjectInputStream` e `FileInputStream` per il caricamento di oggetti;
- l'implementazione dell'interfaccia marker `Serializable`;
- la gestione dettagliata e specifica di molteplici eccezioni (`FileNotFoundException`, `EOFException`, `ClassNotFoundException`, `IOException`).

### Struttura e comportamento del codice
Flusso principale:
1. Istanziazione dell'oggetto `Species`.
2. Apertura dello stream di output verso `save.ser` tramite blocco `try-with-resources`.
3. Scrittura dell'oggetto utilizzando il metodo `writeObject()`.
4. Apertura dello stream di input dal file `save.ser` sempre con `try-with-resources`.
5. Lettura dell'oggetto con `readObject()` ed esecuzione di un cast esplicito a `(Species)`.
6. Stampa delle proprietà dell'oggetto ripristinato.

### File
| File | Descrizione |
|------|-------------|
| `Main.java` | Esegue la scrittura e la successiva lettura dell'oggetto, gestendo le possibili eccezioni. |
| `Species.java` | Definisce la struttura dell'oggetto da salvare. Implementa `Serializable`. |
| `save.ser` | File binario generato contenente i byte dell'oggetto serializzato. |

### Concetti trattati
- Serializzazione e Deserializzazione
- Interfaccia `Serializable`
- Flussi di I/O per dati binari (`ObjectOutputStream`, `ObjectInputStream`)
- Casting di oggetti durante la lettura
- Multi-catch block per la gestione di errori specifici di I/O e reflection

### Approfondimento: La Serializzazione e l'interfaccia Serializable
La **Serializzazione** in Java è il processo che converte lo stato di un oggetto in una sequenza di byte. Questa sequenza può essere salvata su un disco, inviata su una rete o salvata in un database. L'operazione inversa, che ricrea l'oggetto in memoria partendo dalla sequenza di byte, è detta **Deserializzazione**.

Per poter serializzare un oggetto, la sua classe deve dichiarare di implementare l'interfaccia `java.io.Serializable`:
```java
public class Species implements Serializable { ... }
```
`Serializable` è una **marker interface** (interfaccia marcatore): non contiene alcun metodo da implementare. Serve esclusivamente a segnalare alla JVM (Java Virtual Machine) che gli oggetti di questa classe sono autorizzati ad essere convertiti in byte. Se si tenta di passare al metodo `writeObject()` un oggetto la cui classe non implementa `Serializable`, Java lancerà una `NotSerializableException`.

Un punto di attenzione sulla deserializzazione è il metodo `readObject()`. Questo metodo restituisce un riferimento generico di tipo `Object`, motivo per cui è sempre necessario effettuare un **cast** (es: `(Species) in.readObject()`) verso la classe originaria. Questo passaggio è strettamente controllato da Java, che lancia una `ClassNotFoundException` se la classe dell'oggetto letto non è presente a runtime.

### Esempio di esecuzione
```
Oggetto salvato correttamente in save.ser
Nome Specie caricato: Pietra di marte
Tipo Specie caricato: Pietre
```

---

## 🇬🇧 English

### Description
This exercise introduces the concept of object **serialization** and **deserialization** in Java.

The program:
- creates an instance of the `Species` class with dummy data;
- serializes (saves) this object into a binary file named `save.ser`;
- subsequently, reads the `save.ser` file to deserialize (reconstruct) the object;
- prints the loaded object's attribute values to the screen to verify correctness.

### Learning objective
The goal is to strengthen:
- the use of `ObjectOutputStream` and `FileOutputStream` to save objects;
- the use of `ObjectInputStream` and `FileInputStream` to load objects;
- the implementation of the `Serializable` marker interface;
- the detailed and specific handling of multiple exceptions (`FileNotFoundException`, `EOFException`, `ClassNotFoundException`, `IOException`).

### Code flow and behavior
Main flow:
1. Instantiation of the `Species` object.
2. Opening the output stream to `save.ser` via a `try-with-resources` block.
3. Writing the object using the `writeObject()` method.
4. Opening the input stream from the `save.ser` file, again using `try-with-resources`.
5. Reading the object with `readObject()` and performing an explicit cast to `(Species)`.
6. Printing the properties of the restored object.

### Files
| File | Description |
|------|-------------|
| `Main.java` | Executes the writing and subsequent reading of the object, handling possible exceptions. |
| `Species.java` | Defines the structure of the object to be saved. Implements `Serializable`. |
| `save.ser` | Generated binary file containing the bytes of the serialized object. |

### Concepts covered
- Serialization and Deserialization
- `Serializable` interface
- I/O streams for binary data (`ObjectOutputStream`, `ObjectInputStream`)
- Object casting during reading
- Multi-catch blocks for specific I/O and reflection error handling

### In-depth: Serialization and the Serializable interface
**Serialization** in Java is the process of converting an object's state into a byte stream. This sequence can be saved to a disk, sent over a network, or stored in a database. The reverse operation, recreating the object in memory from the byte stream, is called **Deserialization**.

To serialize an object, its class must declare that it implements the `java.io.Serializable` interface:
```java
public class Species implements Serializable { ... }
```
`Serializable` is a **marker interface**: it does not contain any methods to implement. It serves exclusively to signal to the JVM (Java Virtual Machine) that objects of this class are permitted to be converted into bytes. If you attempt to pass an object whose class does not implement `Serializable` to the `writeObject()` method, Java will throw a `NotSerializableException`.

A key point to note about deserialization is the `readObject()` method. This method returns a generic reference of type `Object`, which is why it is always necessary to perform a **cast** (e.g., `(Species) in.readObject()`) back to the original class. This step is strictly monitored by Java, which will throw a `ClassNotFoundException` if the class of the read object is not present at runtime.

### Sample run
```
Oggetto salvato correttamente in save.ser
Nome Specie caricato: Pietra di marte
Tipo Specie caricato: Pietre
```