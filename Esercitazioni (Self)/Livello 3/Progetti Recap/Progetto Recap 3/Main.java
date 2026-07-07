public class Main {
	public static void main(String[] args) {
		
		Computer pc1 = new Computer(10, 100.0);
		Computer pc2 = new Computer(7, 128.00);
		
		try {
			pc1.avvia();
			pc2.avvia(); // ERRORE: Scritto start() invece di avvia()
		
		} catch (RuntimeException e) {
			System.out.println(e.getMessage());
		} finally {
			// ERRORE: Mettendo il rilascio risorse nel 'catch', venivano rilasciate SOLO in caso di errore.
			// FIX CORRETTO: Utilizzo del blocco 'finally' per garantire l'esecuzione sempre e comunque.
			System.out.println("Risorse hardware rilasciate."); 
		}
	}
}