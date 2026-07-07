public class Transazione {
	private int saldo;
	
	Transazione(int saldo) {
		this.saldo = saldo;
	}
	
	// ERRORE: Se lanciavi un'eccezione Checked, dovevi dichiararlo con la keyword 'throws'.
	// FIX CORRETTO: Aggiunta di 'throws SaldoInsufficienteException' alla firma del metodo.
	public void eseguiTransazione(int importo) throws SaldoInsufficienteException {
		if (this.saldo < importo) { 
			throw new SaldoInsufficienteException("Errore di Transazione: Saldo Insufficiente per elaborare " + importo + "."); 
		
		} else {
			System.out.println("Tentativo di transazione con importo " + importo + ".");
			this.saldo -= importo;
		}
	}
}