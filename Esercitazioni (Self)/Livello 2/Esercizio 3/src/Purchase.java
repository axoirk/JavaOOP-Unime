/**
 * Classe per l'esercizio su incapsulamento e validazione.
 * I campi sono private e vengono gestiti solo tramite getter/setter.
 */
public class Purchase {
    private String name;
    private Double price;
    private Integer amount;


    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        // Regola di dominio: il prezzo non può essere negativo.
        if (price < 0) {
            System.out.println("Il prezzo inserito risulta negativo (minore di 0)");
            return;
        }

        this.price = price;
    }

    public Integer getAmount() {
        return amount;
    }

    public void setAmount(Integer amount) {
        this.amount = amount;
    }
}
