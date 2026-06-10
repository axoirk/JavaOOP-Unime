public class Coffee implements Runnable {
    @Override
    public void run() {
        while (true) {
            System.out.println("Sto facendo il caffe'...");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                System.out.println("Thread Coffee interrotto");
                break;
            }
        }
    }
}
