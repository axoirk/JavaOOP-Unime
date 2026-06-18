public class Pellicola implements Comparable<Pellicola> {
    private String titolo, regista;
    private int annoUscita;

    public Pellicola(String titolo, String regista, int annoUscita) {
        this.titolo = titolo;
        this.regista = regista;
        this.annoUscita = annoUscita;
    }

    @Override
    public String toString() {
        return String.format("%s (%d) - %s", this.titolo, this.annoUscita, this.regista);
    }
    @Override
    public int compareTo(Pellicola altraPellicola) {
        return Integer.compare(this.annoUscita, altraPellicola.annoUscita);
    }
}
