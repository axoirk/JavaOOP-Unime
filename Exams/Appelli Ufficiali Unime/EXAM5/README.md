# EXAM5 — Appello del 23 novembre 2026

Terzo appello **realmente sostenuto**, dopo EXAM3 ed EXAM4. Superato: tre esercizi su tre con
test verde, voto finale 30 e lode.

| Esercizio | Argomento | Già visto in |
|---|---|---|
| ES1 | Classe astratta `Animale`, sottoclassi `Cane` e `Gatto` con il loro verso | EXAM1 ES1 |
| ES2 | Le cinque parole chiave delle eccezioni, sul metodo `guida` di `Automobile` | EXAM1 ES2, EXAM3 ES2 |
| ES3 | `ClientUDP`: invio di un datagramma e attesa della risposta, in `UTF-8` | EXAM4 ES2 |

Tutti e tre gli esercizi venivano da appelli precedenti, non uno solo come negli appelli di luglio
e settembre.

## Ricostruzione della traccia

Le tracce sono **ricostruite** dal testo riportato a memoria subito dopo la prova. Argomenti, nomi
delle classi e dei metodi e vincoli sono quelli reali; i dettagli che servono al tester sono stati
fissati dove il ricordo era incompleto:

- **ES2**: la forma esatta dei tre messaggi (`eccezione`, `eccezione in run time`,
  `nessuna eccezione`) e il caso `n == 0` reso con un'eccezione controllata generica.
- **ES3**: host, porta, forma della risposta del server e il ritorno `null` in caso di fallimento,
  presi da EXAM4 ES2, da cui l'esercizio è riciclato. La novità reale è la codifica `UTF-8` nella
  conversione tra testo e byte. Come in EXAM4, il server risponde con `RISPOSTA: ` seguito dal
  testo e non con un'eco perfetta: altrimenti il tester non distinguerebbe un client che riceve
  davvero da uno che restituisce il proprio parametro.

## Cosa contiene ogni cartella

| File | Cosa è |
|---|---|
| `README.md` | La traccia |
| `Soluzione.java` | Il foglio di partenza: solo gli `import`. È il file che compili |
| `Main.class` | Il tester black-box, già compilato. Il sorgente non esiste, come all'appello |

## Rifarlo come una prova vera

```bash
python3 Exams/aula.py "Exams/Appelli Ufficiali Unime/EXAM5"
```

Cronometro, cinque esecuzioni per esercizio, consegna e report. Per ripartire da zero dopo un
tentativo: `--riparti`.

## Cosa verificano i tester

- **ES1** controlla per riflessione che `Animale` sia astratta, che `verso` sia astratto e restituisca
  una stringa, che `Cane` e `Gatto` ne siano sottoclassi, e invoca `verso` attraverso il metodo di
  `Animale`.
- **ES2** cattura la console e l'eccezione che esce da `guida` per ciascun caso: con `0` deve uscire
  un'eccezione controllata, con `1` una non controllata, con `2` nessuna. Controlla per riflessione
  che `guida` dichiari un'eccezione controllata e legge il sorgente per le cinque parole chiave.
  Accetta `guida` sia d'istanza sia statico, perché la traccia non lo fissa.
- **ES3** contiene il server UDP e conta i datagrammi che riceve davvero. Il messaggio con le lettere
  accentate scopre un client che ricostruisce la risposta dall'intero buffer invece che dai soli byte
  ricevuti: il tester mostra i caratteri nulli in coda, che altrimenti renderebbero atteso e ottenuto
  identici a vista. Legge il sorgente per la codifica `UTF-8`, protegge ogni chiamata con un timeout
  e verifica che un host irraggiungibile porti a `null` senza toccare il server.
