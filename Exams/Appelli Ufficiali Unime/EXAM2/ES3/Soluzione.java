// Inserisci qui la tua classe Buffer:



// ==========================================
// CODICE PRE-FORNITO DAL DOCENTE
// ==========================================

class Produttore implements Runnable {
    private Buffer buffer;
    
    public Produttore(Buffer b) {
        this.buffer = b;
    }
    
    @Override
    public void run() {
        try {
            for(int i = 1; i <= 5; i++) {
                buffer.inserisci(i);
                System.out.println("Prodotto: " + i);
                Thread.sleep(100);
            }
        } catch(InterruptedException e) {}
    }
}

class Consumatore implements Runnable {
    private Buffer buffer;
    
    public Consumatore(Buffer b) {
        this.buffer = b;
    }
    
    @Override
    public void run() {
        try {
            for(int i = 1; i <= 5; i++) {
                int val = buffer.estrai();
                System.out.println("Consumato: " + val);
                Thread.sleep(150);
            }
        } catch(InterruptedException e) {}
    }
}
