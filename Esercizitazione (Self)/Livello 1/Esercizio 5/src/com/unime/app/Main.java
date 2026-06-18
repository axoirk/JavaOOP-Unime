import java.util.Scanner;

/**
 * Esercizio sul ciclo for a numero fisso di iterazioni.
 * Simula una crescita settimanale per 10 settimane.
 */
public class Main {
    public static void main(String[] args){

        System.out.println("Inserisci il numero di insetti, e il tasso di crescita settimanale.");
        Scanner scanner = new Scanner(System.in);

        Integer n = scanner.nextInt();
        Integer raddoppio = scanner.nextInt();

        // Il for rappresenta una simulazione temporale a passi settimanali.
        for (int i = 1; i <= 10; i++) {
            n *= raddoppio;
            System.out.printf("Settimana %d\nNumero attuale insetti: %d\n\n", i, n);
        }

        System.out.printf("I tuoi insetti sono diventati in totale: " + n);
    }
}
