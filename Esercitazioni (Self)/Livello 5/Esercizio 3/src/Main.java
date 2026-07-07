public class Main {
    public static void main(String[] args) {
        RunnableThread task = new RunnableThread();

        Thread t1 = new Thread(task, "Thread-1");
        Thread t2 = new Thread(task, "Thread-2");

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            System.out.println("[Main] Thread interrotto. Termino...");
            e.printStackTrace();
        }

        System.out.println("[Main] Tutti i thread hanno finito. Programma terminato.");
    }
}
