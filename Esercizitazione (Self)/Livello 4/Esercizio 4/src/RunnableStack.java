// [ERRORE ORIGINALE]: "public class RunnableStack extends SyncStack" 
// Non si usa l'ereditarietà in questo caso, perché un task Runnable NON È uno Stack.
// [SOLUZIONE]: Si usa la composizione. Il Runnable *contiene* un riferimento al SyncStack condiviso.
public class RunnableStack implements Runnable {

    private SyncStack stack;
    private boolean isProducer;

    // Costruttore per passare l'oggetto condiviso
    public RunnableStack(SyncStack stack, boolean isProducer) {
        this.stack = stack;
        this.isProducer = isProducer;
    }

    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        System.out.println("Avviato Thread: " + threadName);
        
        try {
            // [ERRORE ORIGINALE]: Usavi "synchronized (this)" qui attorno a tutto il ciclo di esecuzione.
            // Sbagliato per due motivi: "this" era diverso per ogni thread (non si bloccavano a vicenda),
            // e bloccare l'intero ciclo avrebbe impedito all'altro thread di lavorare per sempre.
            // La sincronizzazione è ora interamente gestita nei metodi send() e receive() di SyncStack.
            
            if (isProducer) {
                int valoreGenerato = 1;
                while (true) {
                    stack.send(valoreGenerato++);
                    Thread.sleep(500); // Pausa per far leggere l'output a schermo
                }
            } else {
                // [ERRORE ORIGINALE]: Il consumatore faceva una sola richiesta senza un loop "while(true)".
                // [SOLUZIONE]: Aggiunto il loop per farlo consumare continuamente.
                while (true) {
                    stack.receive();
                    Thread.sleep(1500); // Pausa più lunga (consuma più lentamente di quanto l'altro produce)
                }
            }
        } catch (InterruptedException e) {
            System.out.println("Thread " + threadName + " interrotto.");
        }
    }
}