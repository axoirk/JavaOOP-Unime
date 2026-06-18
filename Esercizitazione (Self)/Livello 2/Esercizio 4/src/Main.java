public class Main {
    public static void main(String[] args) {

        System.out.println("Numero attuale conti creati: " + GestioneBancaria.getTotaleConti());
        ContoBancario conto1 = new ContoBancario("Mario Rossi", 599.99, 3.9);

        System.out.println("Numero attuale conti creati: " + GestioneBancaria.getTotaleConti());

        ContoBancario conto2 = new ContoBancario("Mirko Fiorini", 195.45, 16);
        ContoBancario conto3 = new ContoBancario("Luca Scamazza", 10.99, 1);

        System.out.println("Numero attuale conti creati: " + GestioneBancaria.getTotaleConti());

        conto1.printContoInfo();
        conto2.printContoInfo();
        conto3.printContoInfo();

    }
}
