# Esercizio 4: Layout e Action Listener / Exercise 4: Layout and Action Listener

---

## 🇮🇹 Italiano

### Obiettivo
Applicare il *Pattern Observer* per intercettare gli eventi dell'utente (come il click di un pulsante) e gestire la disposizione spaziale dei componenti usando i Layout Manager.

### Requisiti del task
1. **Interfaccia Grafica (View):**
    - Crea una finestra `JFrame` ("Mini Calcolatrice Somma").
    - Crea un `JPanel` e applicagli un **GridLayout** (es. 4 righe, 1 colonna).
    - Aggiungi i seguenti componenti al pannello (in ordine dall'alto verso il basso):
        1.  Un `JTextField` (Casella di testo di input) per il primo numero.
        2.  Un `JTextField` per il secondo numero.
        3.  Un `JButton` con il testo "Calcola Somma".
        4.  Una `JLabel` inizialmente impostata a "Risultato: ---".
2. **Gestione Eventi (Controller/Observer):**
    - Aggancia un "ascoltatore" al bottone invocando `addActionListener(...)`.
    - All'interno del metodo `actionPerformed`:
        - Estrai il testo digitato nei due `JTextField` usando `.getText()`.
        - Converti il testo in numeri interi (`Integer.parseInt()`).
        - Calcola la somma matematica.
        - Aggiorna il testo della `JLabel` mostrando il risultato finale.
3. **Gestione Errori (Robustezza):**
    - Usa un blocco `try-catch` attorno al parsing. Se l'utente digita delle lettere invece che numeri, il `parseInt` lancerà una `NumberFormatException`.
    - Catturala e apri una finestra di dialogo di errore usando `JOptionPane.showMessageDialog(...)`.

### Concetti trattati
- Campi di input (`JTextField`)
- `GridLayout` e posizionamento relativo
- Pattern Observer: `ActionListener` e `actionPerformed`
- Conversione di tipi (Parsing) e validazione input tramite eccezioni (`NumberFormatException`)
- Finestre di dialogo modali (`JOptionPane`)

### Esempio di Output
*Inserendo "10" nel primo campo, "20" nel secondo e cliccando su "Calcola Somma", la label si aggiornerà in "Risultato: 30". Inserendo "abc", apparirà un messaggio di errore.*

---

## 🇬🇧 English

### Objective
Apply the *Observer Pattern* to intercept user events (such as a button click) and manage the spatial arrangement of components using Layout Managers.

### Task Requirements
1. **Graphical User Interface (View):**
    - Create a `JFrame` window ("Mini Sum Calculator").
    - Create a `JPanel` and apply a **GridLayout** (e.g., 4 rows, 1 column).
    - Add the following components to the panel (in order from top to bottom):
        1.  A `JTextField` (Input text box) for the first number.
        2.  A `JTextField` for the second number.
        3.  A `JButton` with the text "Calcola Somma".
        4.  A `JLabel` initially set to "Risultato: ---".
2. **Event Handling (Controller/Observer):**
    - Attach a "listener" to the button by invoking `addActionListener(...)`.
    - Inside the `actionPerformed` method:
        - Extract the text typed in the two `JTextField` components using `.getText()`.
        - Convert the text to integers (`Integer.parseInt()`).
        - Calculate the mathematical sum.
        - Update the `JLabel` text showing the final result.
3. **Error Handling (Robustness):**
    - Use a `try-catch` block around the parsing. If the user types letters instead of numbers, `parseInt` will throw a `NumberFormatException`.
    - Catch it and open an error dialog box using `JOptionPane.showMessageDialog(...)`.

### Concepts Covered
- Input fields (`JTextField`)
- `GridLayout` and relative positioning
- Observer Pattern: `ActionListener` and `actionPerformed`
- Type conversion (Parsing) and input validation via exceptions (`NumberFormatException`)
- Modal dialog boxes (`JOptionPane`)

### Sample Output
*By entering "10" in the first field, "20" in the second, and clicking "Calcola Somma", the label will update to "Risultato: 30". If you enter "abc", an error message will appear.*
