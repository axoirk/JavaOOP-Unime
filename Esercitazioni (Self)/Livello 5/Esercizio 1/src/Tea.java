public class Tea implements Runnable {
    @Override
    public void run() {
        while (true) {
            System.out.println("Sto facendo il the'...");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                System.out.println("Thread Tea interrotto");
                break;
            }
        }
    }
}
