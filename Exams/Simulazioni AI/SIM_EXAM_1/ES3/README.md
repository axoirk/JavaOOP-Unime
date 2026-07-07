# Esercizio 3 (13 Punti) - Concorrenza e Sincronizzazione (Wait/Notify)

**Regole Appello:** 30 minuti totali per l'intero esame. Max 5 esecuzioni per esercizio. Tutte le classi nello stesso file (Soluzione.java).

All'interno dell'ambiente sono già fornite le classi `Cuoco` e `Cameriere`, completamente implementate. Tali classi interagiscono concorrentemente scambiandosi informazioni tramite un bancone (Pass) condiviso.

Si richiede di implementare ex-novo la classe `PassCondiviso` (attualmente vuota). Essa deve fungere da intermediario, garantendo mutua esclusione e sincronizzazione. Deve obbligatoriamente soddisfare i seguenti requisiti:
1. Mantenere lo stato di una singola comanda di tipo `String` (può ospitare 1 sola comanda alla volta).
2. Definire un metodo per posare una comanda.
3. Definire un metodo per ritirare la comanda.

*(Nota: Le firme esatte dei metodi per la classe `PassCondiviso` devono essere dedotte analizzando le invocazioni presenti nel codice fornito di Cuoco e Cameriere).*