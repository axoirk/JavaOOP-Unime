import java.util.Scanner;
import java.util.ArrayList;

/**
 * Esercizio su collezioni dinamiche con ArrayList.
 * Dimostra inserimento in loop e lettura con for-each.
 */
public class Main {
    public static void main(String[] args) {
        ArrayList<String> list = new ArrayList<String>();
        Scanner input = new Scanner(System.in);
        String oggetto_lista = "";

        System.out.println("Inserisci un oggetto nella lista della spesa: ");
        // Sentinella testuale: STOP termina l'inserimento.
        while (!oggetto_lista.equals("STOP")) {
            oggetto_lista = input.nextLine();

            if (oggetto_lista.equals("STOP")) {
                break;
            }
            list.add(oggetto_lista);
            System.out.println("Oggetto aggiunto alla lista della spesa.\nPer terminare l'inserimento digitare \"STOP\"");

        }

        System.out.println("Lista della spesa: ");
        // for-each: iterazione diretta sugli elementi della collezione.
        for(String obj : list) {
            System.out.println(obj);
        }
    }
}
