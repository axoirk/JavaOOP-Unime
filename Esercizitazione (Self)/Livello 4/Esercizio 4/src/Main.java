/*
Esercizio 4: Sincronizzazione (Produttore-Consumatore).
Obiettivo: Evitare conflitti quando più thread accedono alla stessa risorsa.
Come fare: Implementa una classe SyncStack che agisca da buffer condiviso (un array).
Crea due thread: uno che inserisce, uno che preleva. Modifica i metodi di inserimento e prelievo con la keyword synchronized.
Se l'array è pieno, il thread produttore deve chiamare wait() (si sospende); se inserisce un dato chiama notify().
Stessa logica inversa per il consumatore se l'array è vuoto.
*/

public class Main {
    public static void main(String[] args) {
        // [ERRORE ORIGINALE]: Creavi due istanze separate di RunnableStack (che estendeva SyncStack).
        // Questo significava che ogni thread aveva la propria coda vuota privata. Non comunicavano.
        // [SOLUZIONE]: Creiamo UN'UNICA istanza della risorsa condivisa da passare a entrambi i thread.
        SyncStack bufferCondiviso = new SyncStack();

        // Passiamo lo stesso buffer a entrambi, dicendo chi è il produttore (true) e chi il consumatore (false)
        RunnableStack produttore = new RunnableStack(bufferCondiviso, true);
        RunnableStack consumatore = new RunnableStack(bufferCondiviso, false);

        Thread t1 = new Thread(produttore, "Produttore");
        Thread t2 = new Thread(consumatore, "Consumatore");

        t1.start();
        t2.start();
    }
}
