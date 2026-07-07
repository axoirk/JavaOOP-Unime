import java.io.Serializable;

public class Species implements Serializable {
    public String nome;
    public String specie;

    public Species(String nome, String specie) {
        this.nome = nome;
        this.specie = specie;
    }
}
