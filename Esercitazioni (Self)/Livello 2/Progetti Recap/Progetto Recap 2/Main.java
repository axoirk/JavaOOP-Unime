public class Main{
	public static void main(String[] args) {
		Conto conto1 = new Conto();
		Conto conto2 = new Conto(500);
		
		conto1.versamento(200);
		
		System.out.println("Saldo conto 1: " + conto1.getSaldo());
		System.out.println("Saldo conto 2: " + conto2.getSaldo());
		System.out.println("Totale Conti Aperti: " + Conto_Counter.getConti());
		
	}
}