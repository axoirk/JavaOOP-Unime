# Esercizio 3: Interfacce Grafiche (Swing)

---

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

