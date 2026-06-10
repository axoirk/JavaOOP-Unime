/**
 * Eccezione checked personalizzata per segnalare divisione non valida per zero.
 */
public class DivideByZeroException extends Exception{
    public DivideByZeroException(){
        super("Non puoi dividere per zero!");
    }
}
