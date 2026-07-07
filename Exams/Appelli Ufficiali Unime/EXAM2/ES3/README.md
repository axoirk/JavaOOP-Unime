# Esercizio 3 (13 Punti) - Concorrenza e Sincronizzazione (Wait/Notify)

**Regole Appello:** 30 minuti totali per 3 esercizi. Max 5 esecuzioni per esercizio. Tutte le classi nello stesso file (Main.java).

All'interno del workspace (nel file Main.java) sono già fornite le classi `Produttore` e `Consumatore`, completamente implementate. Tali classi sono progettate per interagire concorrentemente con una risorsa condivisa.

Si richiede allo studente di implementare ex-novo la classe `Buffer` (attualmente vuota), col fine di risolvere il problema della concorrenza garantendo la mutua esclusione e la corretta sincronizzazione dei thread. La classe `Buffer` deve obbligatoriamente soddisfare i seguenti requisiti:
1. Contenere una struttura dati basata su un array primitivo con dimensione massima pari a 3.
2. Definire un metodo che restituisca sotto forma di intero il numero di elementi attualmente presenti nel buffer.
3. Definire un metodo per l'inserimento di un elemento nel buffer.
4. Definire un metodo per l'estrazione e rimozione di un elemento dal buffer.

*(Nota: Le firme esatte dei metodi per la classe `Buffer` devono essere dedotte dallo studente analizzando le invocazioni presenti nel codice fornito delle classi Produttore e Consumatore).*