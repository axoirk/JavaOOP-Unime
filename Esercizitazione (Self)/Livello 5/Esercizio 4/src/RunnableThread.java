public class RunnableThread implements Runnable {

    SharedCounter counter;

    RunnableThread(SharedCounter counter) {
        this.counter = counter;
    }
    public void increment() {
        counter.incrementCounter();

    }

    public synchronized void sIncrement() {
        counter.incrementCounter();
    }

    @Override
    public void run() {
        for(int i = 0; i < counter.ATTEMPT_COUNTER / counter.n_threads; i++) {
            if(counter.isSyncronized()) {
                sIncrement(); // Con synchronized, applichiamo un lock in modo che 1 thread alla volta può accedere al metodo, e gli altri stanno in attesa finchè non si leva il lock
            } else {
                increment(); // Creando un Race-Condition
            }
        }
    }
}
