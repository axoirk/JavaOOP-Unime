// IMPLEMENTA QUI LA CLASSE BUFFER

// ==========================================
// CODICE PRE-FORNITO DAL DOCENTE
// ==========================================
class Produttore implements Runnable {
    private Buffer buffer;
    public Produttore(Buffer buffer) { this.buffer = buffer; }
    @Override
    public void run() {
        try {
            for (int i = 0; i < 5; i++) {
                buffer.inserisci(i);
                System.out.println("Prodotto: " + i + " | Elementi presenti: " + buffer.getContatore());
                Thread.sleep(100);
            }
        } catch (InterruptedException e) { e.printStackTrace(); }
    }
}

class Consumatore implements Runnable {
    private Buffer buffer;
    public Consumatore(Buffer buffer) { this.buffer = buffer; }
    @Override
    public void run() {
        try {
            for (int i = 0; i < 5; i++) {
                int val = buffer.estrai();
                System.out.println("Consumato: " + val + " | Elementi presenti: " + buffer.getContatore());
                Thread.sleep(150);
            }
        } catch (InterruptedException e) { e.printStackTrace(); }
    }
}
