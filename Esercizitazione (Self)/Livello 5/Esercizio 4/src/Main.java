public class Main {
    public static void main(String[] args) {
        SharedCounter counter = new SharedCounter(200000, 2);

        RunnableThread runnableCounter = new RunnableThread(counter);

        Thread t1 = new Thread(runnableCounter, "Contatore 1");
        Thread t2 = new Thread(runnableCounter, "Contatore 2");

        Thread t3 = new Thread(runnableCounter, "Contatore 1 Sync");
        Thread t4 = new Thread(runnableCounter, "Contatore 2 Sync");

        try {
            t1.start();
            t2.start();

            t1.join();
            t2.join();

            System.out.printf("[Senza sincronizzazione] Valore atteso: %d, Valore ottenuto: %d (Possibile Race-Condition e counter non consono)\n", counter.ATTEMPT_COUNTER, counter.getCounter());

            counter.resetCounter();
            counter.setSyncronized();

            t3.start();
            t4.start();

            t3.join();
            t4.join();

            System.out.printf("[Con sincronizzazione] Valore atteso: %d, Valore ottenuto: %d (Risultato Giusto)\n", counter.ATTEMPT_COUNTER, counter.getCounter());

        } catch (InterruptedException e) {
            System.out.println("[Main] Thread interrotto. Sospendo programma...");
        }
    }
}
