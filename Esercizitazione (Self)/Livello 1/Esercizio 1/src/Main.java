import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Acquisizione di un double digitato dall'utente.
        System.out.println("Inserisci un numero il tuo peso in KG (ex: 60.5): ");
        double weight = scanner.nextDouble();

        System.out.println("Inserisci la tua altezza in M (ex: 1,80): ");
        double high = scanner.nextDouble();


        // Output formattato con placeholder %d per interi.
        System.out.printf("Il numero BMI é %.2f", weight / (high * high));
    }
}
