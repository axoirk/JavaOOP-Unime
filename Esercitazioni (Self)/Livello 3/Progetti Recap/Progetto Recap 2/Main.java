public class Main{
	public static void main(String[] args) {
		Transazione transazione = new Transazione(1200);
		
		try {
			transazione.eseguiTransazione(1000);
			transazione.eseguiTransazione(1000);
		// ERRORE: Catturavi RuntimeException.
		// FIX CORRETTO: Ora devi catturare specificatamente SaldoInsufficienteException (o genericamente Exception).
		} catch (SaldoInsufficienteException e) {
			System.out.println(e.getMessage());
		}
	}
}