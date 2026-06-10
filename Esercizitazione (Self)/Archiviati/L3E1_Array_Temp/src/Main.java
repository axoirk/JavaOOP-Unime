import java.util.Scanner;

/**
 * Esercizio su array monodimensionali.
 * Salva 7 temperature, le attraversa e ne calcola la media settimanale.
 */
public class Main {
    public static void main(String[] args) {
        double[] temperature = new double[7];
        double summ = 0;
        Scanner scanner = new Scanner(System.in);

        // Primo passaggio: popolamento dell'array.
        for (int i =  0; i <= temperature.length - 1; i++) {
            System.out.printf("Inserisci temperatura del giorno %d: ", i + 1 );
            temperature[i] = scanner.nextDouble();
        }

        // Secondo passaggio: riduzione (somma) degli elementi.
        for(int k = 0; k < temperature.length; k++){
            summ += temperature[k];
        }

        System.out.printf("La media della temperatura settimanale è: %.2f", summ / temperature.length);
    }
}
