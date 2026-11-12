# EXAM4 — Appello del 8 settembre 2026

Secondo appello **realmente sostenuto**, dopo EXAM3.

| Esercizio | Argomento |
|---|---|
| ES1 | `Asta` con inner class **non statica** `Offerta` |
| ES2 | `ClientUDP`: invio di un datagramma e attesa della risposta |
| ES3 | Metodo statico di conversione km → metri, dentro una classe |

Tre argomenti che sembrano facili e non lo sono: `extends` non rende una classe annidata, su UDP
inviare non è ricevere, e un metodo non può stare al primo livello di un file.

## Ricostruzione della traccia

Le tracce qui dentro sono **ricostruite** dal testo riportato a memoria. Struttura, vincoli
architetturali e argomenti sono quelli reali; i dettagli operativi indispensabili al tester
sono stati fissati dove l'originale era implicito:

- **ES1** — l'ordine dei parametri, i valori dell'esempio e la formula esatta della stringa di
  `stato()` (riprodotta alla lettera, spazi mancanti compresi, come nel testo originale).
- **ES2** — host, porta e forma della risposta del server. Nell'originale il server rimandava
  indietro il messaggio identico; qui risponde `RISPOSTA: ` seguito dal testo, perché un'eco
  perfetta non permetterebbe al tester di distinguere un client che riceve davvero da uno che
  restituisce il proprio parametro senza mai chiamare `receive()`.
- **ES3** — nome della classe (`Convertitore`) e del metodo (`converti`), presi dalla forma già
  vista all'Esame 2, e tipi `int`.

Le cartelle seguono l'ordine in cui gli esercizi comparivano in aula: il metodo statico da 5 punti
era l'ultimo dei tre (ES3), non il primo come a luglio. `aula.py` legge i punti dal titolo del README.

## Cosa contiene ogni cartella

| File | Cosa è |
|---|---|
| `README.md` | La traccia |
| `Soluzione.java` | Il foglio di partenza: solo gli `import`. È il file che compili |
| `Main.class` | Il tester black-box, già compilato. Il sorgente non esiste, come all'appello |

## Rifarlo come una prova vera

```bash
python3 Exams/aula.py "Exams/Appelli Ufficiali Unime/EXAM4"
```

Cronometro, cinque esecuzioni per esercizio, consegna e report. Per ripartire da zero dopo un
tentativo: `--riparti`.

## I tester che mordono

Nessuno dei tre verifica solo l'output: verificano **il modo**, che è l'asse decisivo.

- **ES1** legge la classe per riflessione e controlla quattro vincoli prima ancora di eseguire
  qualcosa: `Offerta` annidata dentro `Asta`, **non statica**, **non discendente di `Asta`**, e
  senza nessun campo dichiarato di tipo `Asta`. Una `Offerta` statica fallisce anche
  all'istanziazione, perché il tester la costruisce con `asta.new Offerta(...)`.
- **ES2** contiene il server UDP dentro il tester e **conta i datagrammi che gli arrivano
  davvero**. Un client che restituisce il proprio parametro senza chiamare `receive()` fallisce,
  perché la risposta del server è distinguibile dal messaggio inviato. Ogni chiamata è protetta
  da un timeout, così un client che resta appeso in `receive()` produce un `[KO]` e non un
  blocco. Verifica inoltre che un host irraggiungibile porti a `null` senza toccare il server.
- **ES3** controlla per riflessione che `converti` sia davvero `static`, oltre ai quattro valori.
