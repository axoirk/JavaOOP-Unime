/**
 * Classe di test per confrontare i tre costruttori sovraccaricati di Pet.
 */
public class Main {
    public static void  main(String[] args){
        // Tre creazioni con firme differenti: (), (String), (String, Integer, Double).
        Pet dog = new Pet();
        Pet cat = new Pet("Arturo");
        Pet lizard = new Pet("Tom", 10, 5.0);

        dog.setAge(10);
        dog.setName("Johnny");
        dog.setWeight(50.1);

        dog.showInfo();
        cat.showInfo();
        lizard.showInfo();

        cat.setWeight(10.5);
        cat.setAge(5);

        cat.showInfo();

        lizard.bark();
        dog.bark();
        cat.bark();
    }
}
