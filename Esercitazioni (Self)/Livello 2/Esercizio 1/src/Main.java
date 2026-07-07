/**
 * Driver dell'esercizio su classi e istanziazione.
 * Crea due oggetti Automobile e ne confronta l'evoluzione dello stato.
 */
public class Main {
    public static void main(String[] args){
        Automobile auto1 = new Automobile();
        Automobile auto2 = new Automobile();

        // Inizializzazione di due istanze con stato differente.
        auto1.setFuel(10.0);
        auto2.setFuel(4.6);

        auto1.setSpeed(5);
        auto2.setSpeed(5);

        auto1.setLicense("AD594GD");
        auto2.setLicense("LF494GF");

        System.out.printf("Stato attuale AUTO-%s\nVelocità: %.2f, Benzina: %.2f\n",auto1.getLicense(), auto1.getSpeed(), auto1.getFuel());
        System.out.printf("Stato attuale AUTO-%s\nVelocità: %.2f, Benzina: %.2f\n", auto2.getLicense(), auto2.getSpeed(), auto2.getFuel());

        // Invocazione dei metodi di istanza per modificare lo stato interno.
        System.out.println("Modifiche Valori (Accelerazione)");
        auto1.accelerate(2.4);
        auto2.accelerate(3.7);

        System.out.printf("Stato attuale AUTO-%s\nVelocità: %.2f, Benzina: %.2f\n",auto1.getLicense(), auto1.getSpeed(), auto1.getFuel());
        System.out.printf("Stato attuale AUTO-%s\nVelocità: %.2f, Benzina: %.2f\n", auto2.getLicense(), auto2.getSpeed(), auto2.getFuel());

        System.out.println("Modifiche Valori (Deaccelerazione)");
        auto1.decelerate(1.3);
        auto2.decelerate(3);

        System.out.printf("Stato attuale AUTO-%s\nVelocità: %.2f, Benzina: %.2f\n",auto1.getLicense(), auto1.getSpeed(), auto1.getFuel());
        System.out.printf("Stato attuale AUTO-%s\nVelocità: %.2f, Benzina: %.2f\n", auto2.getLicense(), auto2.getSpeed(), auto2.getFuel());
    }
}
