// IMPLEMENTA QUI LA CLASSE PASSCONDIVISO
class PassCondiviso {
    
}

// ==========================================
// CODICE PRE-FORNITO DAL DOCENTE
// ==========================================
class Cuoco implements Runnable {
    private PassCondiviso pass;
    public Cuoco(PassCondiviso pass) { this.pass = pass; }
    
    @Override
    public void run() {
        String[] piatti = {"Pasta", "Bistecca", "Dolce"};
        try {
            for (String piatto : piatti) {
                System.out.println("[Cuoco] Prepara: " + piatto);
                pass.posa(piatto);
                Thread.sleep(50);
            }
        } catch (InterruptedException e) { e.printStackTrace(); }
    }
}

class Cameriere implements Runnable {
    private PassCondiviso pass;
    public Cameriere(PassCondiviso pass) { this.pass = pass; }
    
    @Override
    public void run() {
        try {
            for (int i = 0; i < 3; i++) {
                String piatto = pass.ritira();
                System.out.println("[Cameriere] Serve al tavolo: " + piatto);
                Thread.sleep(100);
            }
        } catch (InterruptedException e) { e.printStackTrace(); }
    }
}
