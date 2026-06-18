public class RunnableThread implements Runnable {

    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        System.out.printf("[%s] Avvio esecuzione...\n", threadName);

        while(SentinellVar.getState()) {
            try {
                System.out.printf("[%s] Elaborazione dati in corso...\n", threadName);
                Thread.sleep(500);
            } catch (InterruptedException e) {
                System.out.printf("[%s] Thread interrotto.\n", threadName);
                throw new RuntimeException(e);
            }
        }

        System.out.printf("[%s]  Segnale di arresto ricevuto: terminazione pulita.\n", threadName);
    }
}
