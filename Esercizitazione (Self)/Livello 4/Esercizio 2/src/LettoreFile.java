import java.io.*;
import java.util.Scanner;

public class LettoreFile {
    private int index_line = 1;
    File file;

    public LettoreFile(String fileName) {
        file = new File(fileName);
        try (Scanner reader = new Scanner(file)) {
            while(reader.hasNextLine()) {
                String line = reader.nextLine();
                System.out.println("Riga " + index_line + " : " + line);
                index_line++;
            }
        } catch (FileNotFoundException e) {
            System.out.println("Impossibile trovare il file dichiarato.");
            e.printStackTrace();
        }
    }
}
