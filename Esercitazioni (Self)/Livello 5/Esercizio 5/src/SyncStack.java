public class SyncStack {
    private final Object[] queue = new Object[5];

    private int in = 0;
    private int out = 0;
    private int count = 0;

    // [ERRORE ORIGINALE]: Restituivi un boolean e gestivi wait() e notify() nel RunnableStack.
    // [SOLUZIONE]: wait() e notify() vanno chiamati ALL'INTERNO della classe della risorsa condivisa,
    // nei metodi che hanno la keyword 'synchronized'.
    public synchronized void send(Object obj) throws InterruptedException {
        // [ERRORE ORIGINALE]: Usavi un if per controllare se era pieno. Quando si usa wait(),
        // si deve SEMPRE usare un ciclo while per ricontrollare la condizione al risveglio.
        while (count == queue.length) {
            System.out.println("Stack pieno. Il produttore si sospende...");
            wait(); // Sospende il thread che esegue questo metodo (Produttore)
        }

        queue[in] = obj;
        in = (in + 1) % queue.length;
        count++;
        System.out.println("Inserito: " + obj);

        // [ERRORE ORIGINALE]: Non c'era notify() qui. 
        // [SOLUZIONE]: Ora che abbiamo inserito qualcosa, notifichiamo (risvegliamo) il consumatore.
        notify();
    }

    public synchronized Object receive() throws InterruptedException {
        // Anche qui, aspettiamo che ci sia almeno un elemento
        while (count == 0) {
            System.out.println("Stack vuoto. Il consumatore si sospende...");
            wait(); // Sospende il thread che esegue questo metodo (Consumatore)
        }

        Object obj = queue[out];
        queue[out] = null;
        out = (out + 1) % queue.length;
        count--;
        System.out.println("Prelevato: " + obj);

        // [SOLUZIONE]: Ora che abbiamo prelevato, c'è un posto libero. Notifichiamo il produttore.
        notify();

        return obj;
    }
}
