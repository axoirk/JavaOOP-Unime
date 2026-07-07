/**
 * Classe di avvio per osservare il polimorfismo:
 * una reference Person puo' puntare anche a un oggetto Student.
 */
public class Main {
    public static void main(String[] args) {
        Person persona = new Person("Giulia");
        Person studente = new Student("Marco", 12345);

        persona.writeOutput();
        studente.writeOutput();
    }
}
