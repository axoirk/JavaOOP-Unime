import java.util.Scanner;

/**
 * Esercizio su gestione eccezioni con try/catch e throw esplicito.
 */
public class Main {
    public static void main(String[] args) {
        try {
            Scanner input = new Scanner(System.in);

            System.out.println("Inserisci un numeratore:");
            int num = input.nextInt();

            System.out.println("Inserisci un denominatore:");
            int denom = input.nextInt();

            if (denom == 0) {
                // Segnalazione di un errore applicativo tramite eccezione personalizzata.
                throw new DivideByZeroException();
            }

           System.out.printf("Risultato divisione: %.2f", (double) num / denom);
        } catch (Exception e) {
            System.out.printf(e.getMessage());
        }
    }
}
