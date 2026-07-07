public class ContoBancario {
    private String titolare;
    private double saldo;
    private double tassoInteresse;

    public ContoBancario(String titolare, double saldo, double tassoInteresse) {
        this.titolare = titolare;
        this.saldo = saldo;

        this.impostaTassoInteresse(tassoInteresse);
        GestioneBancaria.incrementConti();
    }

    public void impostaTassoInteresse(double nuovoTasso) {
        if (nuovoTasso <= GestioneBancaria.TASSO_INTERESSE_MAX) {
            this.tassoInteresse = nuovoTasso;
        } else {
            System.out.println("Impossibile modificare tasso interesse: Valore superiore da quello definito.");
            this.tassoInteresse = GestioneBancaria.TASSO_INTERESSE_MAX;
        }
    }

    public void printContoInfo(){
        System.out.printf("Titolare Conto: %s\nSaldo sul Conto: €%.2f\nTasso interesse: %.2f\n\n", this.titolare, this.saldo, this.tassoInteresse);
    }
}
