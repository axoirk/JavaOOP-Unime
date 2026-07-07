public class Dispositivo {
	private int RAM;
	
	Dispositivo(int RAM) {
		this.RAM = RAM;
	}
	
	public void avvia(){
		System.out.println("Tentativo di avvio...");
		if (RAM < 8) throw new InsufficientRamException("Errore critico: RAM Insufficiente."); //  Keyword new dimenticata
		System.out.println("Dispositivo avviato con successo");
	}
	
	
}