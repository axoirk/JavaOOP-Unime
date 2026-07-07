import java.util.Scanner;

/**
 * Esercizio sul costrutto switch con enum.
 * Converte l'input testuale in un valore MovieRating e stampa il messaggio associato.
 */
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Inserisci una valutazione: (A, B, C, D, F): ");
        String input = scanner.nextLine();

        char voteChar = input.toUpperCase().charAt(0);

        switch (voteChar) {
            case 'A':
                System.out.println("Hai inserito una valutazione ECCELLENTE");
                break;
            case 'B':
                System.out.println("Hai inserito una valutazione MOLTO BUONO");
                break;
            case 'C':
                System.out.println("Hai inserito una valutazione SUFFICIENTE");
                break;
            case 'D':
                System.out.println("Hai inserito una valutazione SCARSO");
                break;
            case 'F':
                System.out.println("Hai inserito una valutazione INSUFFICIENTE");
                break;
            default:
                System.out.println("Valutazione Non Valida");
                break;
        }

        scanner.close();
    }
}
