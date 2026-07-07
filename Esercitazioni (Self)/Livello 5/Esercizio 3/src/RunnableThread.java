public class RunnableThread implements Runnable {
    public final int MAX_TASK = 5;
    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        System.out.printf("[%s] Avvio lavoro...\n", threadName);

        int n_task = 0;
        while (n_task < MAX_TASK) {
            int rand = (int)(Math.random() * 5001);
            System.out.printf("[%s] Applico operazione N.%d ...\n", threadName, n_task);
            try {
                System.out.printf("[%s] Mi riposo per %d ms...\n", threadName, rand);
                Thread.sleep(rand);
                n_task++;
            } catch (InterruptedException e) {
                System.out.printf("[%s] Thread interrotto. Sospendo...\n", threadName);
            }
        }

        System.out.printf("[%s] Operazione completata.\n", threadName);
    }
}
