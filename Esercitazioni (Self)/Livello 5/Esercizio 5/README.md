# Livello 5 - Esercizio 5: Comunicazione tra Thread

---

### Obiettivo
Utilizzare i metodi `wait()` e `notify()` per coordinare l'accesso a una struttura dati condivisa, risolvendo il classico problema del "Produttore-Consumatore".

### Traccia (dal Syllabus)
1.  **Creare uno Stack condiviso** (o una coda limitata) per gestire dati.
2.  Implementare un thread **"Produttore"** che inserisce dati nello stack.
3.  Implementare un thread **"Consumatore"** che estrae i dati.
4.  Utilizzare i metodi `wait()` e `notify()` (o `notifyAll()`) della JVM per coordinarli:
    -   Il produttore deve attendere se lo stack è pieno.
    -   Il consumatore deve attendere se lo stack è vuoto.
5.  Verificare che la comunicazione avvenga senza spreco di risorse (evitando il busy waiting).

### Esempio di Output
```
[Produttore] Inserito: Oggetto 1
[Produttore] Inserito: Oggetto 2
[Consumatore] Estratto: Oggetto 2
[Consumatore] Estratto: Oggetto 1
[Produttore] Inserito: Oggetto 3
...
```

