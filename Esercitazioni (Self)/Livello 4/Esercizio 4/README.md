# Esercizio 4: Layout e Action Listener

---

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

