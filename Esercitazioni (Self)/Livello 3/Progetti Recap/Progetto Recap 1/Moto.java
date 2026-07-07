public class Moto implements Veicolo {
	Moto(){};
	
	@Override
	public void accelera() {
		System.out.println("La moto accelera: Vrooooom!");
	}
}