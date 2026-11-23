# Esercizio 2 (13 Punti) - Gestione delle Eccezioni (Le 5 Parole Chiave)


1. Definire la classe `Automobile`, con il metodo `guida`, che riceve un parametro intero `n` e non restituisce nulla.
2. Il comportamento richiesto, in base al valore ricevuto:
   - `0`: viene lanciata un'eccezione controllata, che il metodo non gestisce: deve gestirla chi ha invocato il metodo; il messaggio è `eccezione`;
   - `1`: viene lanciata una `IOException`, che il metodo cattura; il blocco `catch` lancia a sua volta un'eccezione non controllata, la quale raggiunge il chiamante; il messaggio è `eccezione in run time`;
   - `2`: nessuna eccezione, il metodo non fa nulla; il messaggio è `nessuna eccezione`.
3. Il messaggio di ciascun caso va stampato in console.
4. **Vincolo architetturale:** vanno obbligatoriamente utilizzate **tutte e cinque le parole chiave** della gestione delle eccezioni (`try`, `catch`, `finally`, `throw`, `throws`).

## Output atteso

```text
guida(0)  ->  eccezione               (l'eccezione controllata raggiunge il chiamante)
guida(1)  ->  eccezione in run time   (l'eccezione non controllata raggiunge il chiamante)
guida(2)  ->  nessuna eccezione
```
