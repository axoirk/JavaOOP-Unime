// ERRORE: Estendere RuntimeException crea un'eccezione Unchecked (nessun obbligo di try-catch).
// FIX CORRETTO: Estendere Exception crea un'eccezione Checked (che obbliga il compilatore al controllo).
public class SaldoInsufficienteException extends Exception {

	public SaldoInsufficienteException(String message){
		super(message);
	}
	
	public SaldoInsufficienteException(){
		super();
	} 
}