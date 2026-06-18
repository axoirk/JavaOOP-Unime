public class Main {
    public static void main(String[] args) {
        RunnableThread work1 = new RunnableThread();
        RunnableThread work2 = new RunnableThread();

        Thread t1 = new Thread(work1, "Lavoratore 1");
        Thread t2 = new Thread(work2, "Lavoratore 2");

        t1.start();
        t2.start();

        // let work for some seconds the threads before sending the stop signal
        try {
            Thread.sleep(2000); 
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("[Main] Inviando segnale di arresto...");
        SentinellVar.stop(); // set to false
    }
}
