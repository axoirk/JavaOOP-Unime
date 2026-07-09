# Report Valutazione - Appello Ufficiale 1

**Studente:** Mirko
**Voto Finale Proposto:** 30/30

---

## 📝 Dettaglio Valutazione Esercizi

### Esercizio 1 (Polimorfismo Base)
* **Punteggio:** 5/5
* **Esito:** Impeccabile.
* **Note:** Hai strutturato perfettamente la classe astratta `Animale` e implementato in modo pulito l'override del metodo `verso()` nelle classi derivate `Cane` e `Gatto`. Sintassi da manuale.

### Esercizio 2 (Gestione Avanzata Eccezioni)
* **Punteggio:** 12/13
* **Esito:** Molto buono, architettura esatta ma piccolo refuso testuale.
* **Note / Correzioni:** 
  Hai utilizzato correttamente tutte le 5 parole chiave richieste (`try`, `catch`, `finally`, `throw`, `throws`). La gestione dei tre rami condizionali (`0`, `1`, `2`) e la corretta cattura dell'`IOException` con il rilancio della `RuntimeException` dimostrano un'ottima comprensione del meccanismo delle eccezioni in Java.
  Ti ho tolto 1 punto puramente formale: hai stampato la stringa `"eccezzione"` con la doppia zeta, invece della corretta dicitura `"eccezione"` richiesta dalla traccia. All'esame, i bot automatici effettuano controlli stringati (literal-match), quindi una virgola o una lettera di troppo fanno fallire il test d'ufficio! Ricordati di fare sempre copia e incolla del testo esatto.

### Esercizio 3 (Ereditarietà, Thread e Information Hiding)
* **Punteggio:** 13/13
* **Esito:** Perfetto.
* **Note / Correzioni:**
  Ottima esecuzione. Hai esteso `Persona`, implementato l'interfaccia `Runnable` e gestito brillantemente i costruttori in overload. L'uso di `Math.pow` per l'elevamento a potenza all'interno del metodo `run()` è corretto, così come la rigorosa applicazione dell'Information Hiding attraverso l'uso di variabili private e relativi metodi getter/setter. 

---

## 🎯 Giudizio Finale
Voto finale: **30/30**.
L'esame è superato con un voto eccellente. L'architettura del codice è solidissima e l'implementazione dei concetti avanzati (Thread, Eccezioni, Polimorfismo) è stata padroneggiata in scioltezza. Fai solo un pizzico di attenzione in più ai dettagli di "spelling" per i print a schermo! Ottimo lavoro.
