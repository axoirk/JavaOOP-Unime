/**
 * Classe usata per esercitare l'overloading dei costruttori.
 * Consente diverse strategie di inizializzazione dello stesso tipo oggetto.
 */
public class Pet {

    private String name;
    private Integer age;
    private Double weight;

    // Costruttore di default: lascia i campi non inizializzati esplicitamente.
    public Pet(){};

    // Costruttore parziale: inizializza solo il nome e assegna default agli altri campi.
    public Pet(String name) {
        this.name = name;
        this.age = 0;
        this.weight = 0.0;
    }

    // Costruttore completo: inizializza tutti gli attributi dell'oggetto.
    public Pet(String name, Integer age, Double weight) {
        this.name = name;
        this.age = age;
        this.weight = weight;
    }

    public void showInfo(){
        System.out.printf("Ciao! Il mio nome è %s, ho %d anni, e peso %.2f KG\n", this.name, this.age, this.weight);
    }

    public void bark(){
        System.out.printf("Woff Woff! Sono %s e sto abbagliando\n", this.name);
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public void setWeight(Double weight) {
        this.weight = weight;
    }

    public String getName() {
        return name;
    }

    public Integer getAge() {
        return age;
    }

    public Double getWeight() {
        return weight;
    }
}
