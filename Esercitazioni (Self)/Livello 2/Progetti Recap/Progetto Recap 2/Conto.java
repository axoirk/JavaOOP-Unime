public class Conto {
	private double saldo = 0;
	
	Conto(double saldoIniziale) {
		this.saldo = saldoIniziale;
		Conto_Counter.incrementa();
	}
	
	Conto(){
		Conto_Counter.incrementa();
	}
	
	public void versamento(double soldi) {
		if (soldi > 0 ) {
			saldo += soldi;
		}
	}
	
	public double getSaldo() {
		return saldo;
	}
	
}