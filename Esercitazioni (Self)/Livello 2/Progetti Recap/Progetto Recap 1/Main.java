public class Main{
	public static void main(String[] args) {
		Utente utente1 = new Utente("mario88", "mario@email.com");
		Utente utente2 = new Utente();
		
		utente2.setUsername("luigi42");
		utente2.setEmail("luigi@email.com");
		
		utente1.printInfo();
		utente2.printInfo();
	}
}