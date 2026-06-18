import java.util.ArrayList;
import java.util.Collections;

public class Main {
    public static void main(String[] args) {
        ArrayList<Pellicola> pellicole = new ArrayList<>();

        Pellicola pellicola1 = new Pellicola("Inception", "Christopher Nolan", 2010);
        Pellicola pellicola2 = new Pellicola("Pulp Fiction", "Quentin Tarantino", 1994);
        Pellicola pellicola3 = new Pellicola("Il Padrino", "Francis Ford Coppola", 1972);
        Pellicola pellicola4 = new Pellicola("Interstellar", "Christopher Nolan", 2014);
        Pellicola pellicola5 = new Pellicola("La Città Incantata", "Hayao Miyazaki", 2001);

        pellicole.add(pellicola1);
        pellicole.add(pellicola2);
        pellicole.add(pellicola3);
        pellicole.add(pellicola4);
        pellicole.add(pellicola5);

        System.out.println("Pellicole PRIMA DEL SORTING:\n");
        for (Pellicola pellicola : pellicole) {
            System.out.println(pellicola.toString());
        }

        Collections.sort(pellicole);

        System.out.println("Pellicole DOPO DEL SORTING:\n");
        for (Pellicola pellicola : pellicole) {
            System.out.println(pellicola.toString());
        }
    }
}
