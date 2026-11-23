# Esercizio 3 (13 Punti) - Comunicazione di Rete su Protocollo UDP


Un server UDP è già in ascolto e non va scritto: riceve un datagramma, risponde al mittente con `RISPOSTA: ` seguito dal testo ricevuto, e resta in ascolto. Le sue coordinate sono note a priori:

```text
host   127.0.0.1
porta  6666
```

1. Definire la classe `ClientUDP`, il cui costruttore riceve nell'ordine l'host (testuale) e la porta (intero). Le variabili d'istanza devono essere private.
2. Definire il metodo `inviaMessaggio`, che riceve un messaggio (testuale) e restituisce una stringa.
3. Il metodo apre una comunicazione con il server sul protocollo UDP, gli trasmette il messaggio ricevuto come parametro, attende la risposta che il server rimanda indietro, la ricostruisce in forma testuale e la restituisce al chiamante.
4. La conversione del testo in byte, e quella della risposta da byte a testo, usano la codifica `UTF-8`.
5. In caso di fallimento della comunicazione il metodo restituisce `null`.

## Output atteso

Costruendo `new ClientUDP("127.0.0.1", 6666)` e invocando `inviaMessaggio("ciao")`, poi `inviaMessaggio("perché è già così")`:

```text
RISPOSTA: ciao
RISPOSTA: perché è già così
```
