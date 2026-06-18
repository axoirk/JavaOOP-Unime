# Esercizio 3: Interfacce Grafiche (Swing) / Exercise 3: Graphical User Interfaces (Swing)

---

## 🇮🇹 Italiano

### Obiettivo
Abbandonare l'interazione via terminale (console) e creare la prima finestra grafica (GUI) utilizzando il framework Java Swing, familiarizzando con i componenti di base.

### Requisiti del task
1. **Setup della Finestra (`JFrame`):**
    - Crea una classe `FinestraBase`.
    - Istanzia un oggetto `JFrame` dandogli un titolo (es. "La Mia Prima GUI").
    - Imposta il comportamento di chiusura affinché l'applicazione termini realmente alla chiusura della finestra (`setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)`).
    - Imposta una dimensione fissa (es. 400x300 pixel).
2. **Creazione dei Componenti:**
    - Crea un pannello contenitore `JPanel`.
    - Crea un'etichetta testuale `JLabel` con un messaggio di benvenuto.
    - Crea un pulsante `JButton` con il testo "Questo è un pulsante!".
3. **Assemblaggio:**
    - Aggiungi la `JLabel` e il `JButton` all'interno del `JPanel`.
    - Aggiungi il `JPanel` al `JFrame` principale.
    - Rendi la finestra visibile (`setVisible(true)`).

### Concetti trattati
- Framework `javax.swing`
- Componenti primari: `JFrame`, `JPanel`, `JLabel`, `JButton`
- Ciclo di vita base di una finestra Java

### Esempio di Output
*Eseguendo il programma, apparirà una finestra di 400x300 pixel con titolo "La mia prima GUI". All'interno, disposti in riga (FlowLayout predefinito di JPanel), appariranno l'etichetta "Benvenuto nella mia prima GUI!" e un pulsante cliccabile.*

---

## 🇬🇧 English

### Objective
Move away from terminal interaction (console) and create your first graphical user interface (GUI) using the Java Swing framework, becoming familiar with basic components.

### Task Requirements
1. **Window Setup (`JFrame`):**
    - Create a `FinestraBase` class.
    - Instantiate a `JFrame` object and give it a title (e.g., "My First GUI").
    - Set the default close operation so the application actually terminates when the window is closed (`setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)`).
    - Set a fixed size (e.g., 400x300 pixels).
2. **Component Creation:**
    - Create a `JPanel` container.
    - Create a `JLabel` with a welcome message.
    - Create a `JButton` with the text "Questo è un pulsante!".
3. **Assembly:**
    - Add the `JLabel` and the `JButton` to the `JPanel`.
    - Add the `JPanel` to the main `JFrame`.
    - Make the window visible (`setVisible(true)`).

### Concepts Covered
- `javax.swing` framework
- Primary components: `JFrame`, `JPanel`, `JLabel`, `JButton`
- Basic lifecycle of a Java window

### Output Example
*Running the program will open a 400x300 pixel window titled "La mia prima GUI". Inside, arranged in a row (default FlowLayout of JPanel), you will see the label "Benvenuto nella mia prima GUI!" and a clickable button.*
