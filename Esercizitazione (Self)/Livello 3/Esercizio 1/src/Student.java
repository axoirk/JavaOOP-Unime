/**
 * Sottoclasse di Person che aggiunge la matricola.
 * Mostra l'override del metodo writeOutput con riuso di super.
 */
public class Student extends Person {
    private Integer matricola;

    public Student(String name, Integer matricola) {
        super(name);
        this.matricola = matricola;
    }

    @Override
    public void writeOutput() {
        // Prima stampa la parte comune ereditata.
        super.writeOutput();
        // Poi completa l'output con il dato specifico dello studente.
        System.out.printf("Matricola: %d%n", this.matricola);
    }

    public Integer getMatricola() {
        return matricola;
    }

    public void setMatricola(Integer matricola) {
        this.matricola = matricola;
    }
}
