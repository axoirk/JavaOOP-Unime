public class Computer extends Dispositivo {
	private double storage;
	
	Computer(int RAM, double Storage){
		super(RAM);
		// ERRORE: Il parametro era 'Storage' con la maiuscola, ma hai assegnato 'storage' con la minuscola (variabile vuota).
		// FIX CORRETTO: this.storage = Storage;
		this.storage = Storage;
	}
	
	@Override
	public void avvia(){
		super.avvia();
		
		System.out.println("Computer avviato con successo.");
	}
}