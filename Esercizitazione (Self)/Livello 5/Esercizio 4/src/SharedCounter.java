public class SharedCounter {
    // SUGGERIMENTO: Aggiungere 'volatile' per garantire la visibilità immediata tra thread
    private boolean syncronized = false; 
    private int counter = 0;

    public int ATTEMPT_COUNTER;
    public int n_threads;

    public SharedCounter(int ATTEMPT_COUNTER, int n_threads) {
        this.ATTEMPT_COUNTER = ATTEMPT_COUNTER;
        this.n_threads = n_threads;
    }

    public boolean compareCounter() {
        return counter == ATTEMPT_COUNTER;
    }

    public int getCounter() {
        return counter;
    }

    public void resetCounter() {
        counter = 0;
    }

    public void incrementCounter() {
        counter++;
    }

    public boolean isSyncronized() {
        return this.syncronized;
    }

    public void setSyncronized() {
        this.syncronized = true;
    }
}