/**
 * Classe base dell'esercizio su ereditarieta'.
 * Espone un comportamento comune (writeOutput) riutilizzabile dalle sottoclassi.
 */
public class Person {
    private String name;

    public Person(String name) {
        this.name = name;
    }

    public void writeOutput(){
        System.out.printf("Nome: %s\n", this.name);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
