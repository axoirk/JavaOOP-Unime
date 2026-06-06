/*
Esercizio 1: Scrivere e Leggere File di Testo.
Obiettivo: Salvare permanentemente stringhe di testo.
Come fare: Per scrivere: usa la classe PrintWriter passandole il nome di un file (es. "out.txt").
Inserisci le chiamate al metodo println() dentro un blocco try-catch per catturare eventuali errori e, molto importante, usa il metodo close() alla fine per svuotare il buffer e rilasciare il file.
Per leggere: usa la classe Scanner passandole un oggetto File("out.txt") e cicla finché hasNextLine() è vero per stampare il contenuto su console.
* */

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        // Writing file
        try (PrintWriter writer = new PrintWriter("out.txt")) {


            Scanner input = new Scanner(System.in);
                while (input.hasNext()) {
                    String word = input.next();
                    if (word.equals("EXIT")) break;
                    writer.println(word);
                }

                // writer.close(); -- Non c'è bisogno di definire la chiamata close, in quanto abbiamo concesso la gestione di salvare e chiudere il file direttamente al try-catch, utilizzando il try-with-resources

        } catch (IOException e) {
            System.out.println("An error occurred while writing.");
            e.printStackTrace();
            return;
        }

        // Reading file
        try (Scanner reader = new Scanner(new File("out.txt"))) {

            while(reader.hasNextLine()) {
                System.out.println("Riga file: " + reader.nextLine());
            }

        } catch (IOException e) {
            System.out.println("An error occurred while reading.");
            e.printStackTrace();
        }
    }
}
