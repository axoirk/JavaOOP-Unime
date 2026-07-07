import java.util.Scanner;

/**
 * Esercizio su espressioni numeriche e selezione multipla con if/else if.
 * Calcola il BMI e classifica il risultato in fasce.
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("SISTEMA CALCOLO BMI.\nInserisci Peso (KG) e Altezza (cm):");
        Scanner input = new Scanner(System.in);

        float peso = input.nextFloat();
        int altezza = input.nextInt();

        // Formula BMI: peso / altezza^2 con conversione cm -> m.
        float bmi = (float) (peso / Math.pow((float) altezza / 100, 2));

        // Struttura condizionale per classificare il valore calcolato.
        if (bmi < 20.1) {
            System.out.printf("Sei sottopeso! BMI: %.2f\n", bmi);
        } else if (bmi >= 20.1 && bmi <= 25.0) {
            System.out.printf("Sei normopeso! BMI: %.2f\n", bmi);
        } else if (bmi > 25.0) {
            System.out.printf("Sei sovrappeso! BMI: %.2f\n", bmi);
        }

        input.close();
    }
}
