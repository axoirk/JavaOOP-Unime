/**
 * Classe modello per introdurre variabili d'istanza, metodi e stato oggetto.
 * Simula in modo semplice accelerazione/decelerazione e consumo carburante.
 */
public class Automobile {
    // Costanti di simulazione.
    private final double MAX_POWER = 5.0;
    private final double FUEL_CONSUMPTION_RATE = 0.1;
    private final double BRAKE_POWER = 8.0;
    private final double FRICTION = 0.5;

    private double speed;
    private double fuel;
    private String license;

    // Metodi di comportamento dell'oggetto.
    public void accelerate(double pedalPressure) {
        if (this.fuel > 0) {
            // L'accelerazione cresce con la pressione sul pedale.
            double acceleration = MAX_POWER * pedalPressure;
            this.speed += acceleration;
            this.fuel -= pedalPressure * FUEL_CONSUMPTION_RATE;
            if (this.fuel < 0) this.fuel = 0;
        } else {
            System.out.println("Serbatoio vuoto!");
        }
    }

    public void decelerate(double brakePressure) {
        // La decelerazione combina freno e attrito minimo.
        double deceleration = (BRAKE_POWER * brakePressure) + FRICTION;

        this.speed -= deceleration;

        if (this.speed < 0) {
            this.speed = 0;
        }
    }

    // Accesso controllato ai campi (incapsulamento).
    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public void setFuel(double fuel) {
        this.fuel = fuel;
    }

    public void setLicense(String license) {
        this.license = license;
    }

    public String getLicense() {
        return license;
    }

    public double getFuel() {
        return fuel;
    }

    public double getSpeed() {
        return speed;
    }
}
