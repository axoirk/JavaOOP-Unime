public class Main {
	public static void main(String[] args) {
		Scuola scuola = new Scuola();
		
		scuola.aggiungiStudente("Alice", 16);
		scuola.aggiungiStudente("Bob", 17);
		
		scuola.mostraStudenti();
	}
}