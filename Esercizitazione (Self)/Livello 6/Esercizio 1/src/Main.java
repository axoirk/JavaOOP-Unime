import java.io.IOException;
import java.net.URL;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        try {
            URL indirizzo = new URL("https://www.wikipedia.org/");
            Scanner webScanner = new Scanner(indirizzo.openStream());
            while(webScanner.hasNextLine()) {
                System.out.println(webScanner.nextLine());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
