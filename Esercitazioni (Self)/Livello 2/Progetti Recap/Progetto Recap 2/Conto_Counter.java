public class Conto_Counter {
	private static int n_conti = 0;
	
	public static void incrementa(){
		n_conti++;
	}
	
	public static int getConti() {
		return n_conti;
	}
}