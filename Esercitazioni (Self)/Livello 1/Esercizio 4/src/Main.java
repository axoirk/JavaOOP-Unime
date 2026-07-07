import java.util.Scanner;

/**
 * Esercizio sul ciclo while con valore sentinella.
 * Continua a leggere voti finché l'utente non inserisce un numero negativo.
 */
public class Main{
    public static void main(String[] args){

        int somm = 0; int count = 0;
        Integer input = 1;

        // Il ciclo termina quando compare la sentinella (< 0).
        while (input >= 0) {
            System.out.println("Inserisci un valore:" );
            Scanner scanner = new Scanner(System.in);

            input = scanner.nextInt();

            // Accumulo progressivo per il calcolo della media finale.
            if (input >= 0) {
                somm += input;
                count++;
                System.out.println("Valore sommato: " + input);
            } else {
                break;
            }
        }

        System.out.printf("Risultati:\nTotale Somma: %d\n Stato Contatore: %d\nMedia: %.2f", somm, count, (float) somm / count);
    }
}
