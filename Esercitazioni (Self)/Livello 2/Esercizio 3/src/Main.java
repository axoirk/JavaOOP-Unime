/**
 * Programma dimostrativo per verificare il comportamento dei setter di Purchase.
 * Include casi validi e un caso non valido per il controllo sul prezzo.
 */
public class Main {
    public static void main(String[] args) {
        // Caso 1: inizializzazione valida
        Purchase ipad = new Purchase();
        ipad.setName("iPad Pro");
        ipad.setPrice(1299.99);
        ipad.setAmount(5);
        printPurchase("Caso 1 - Valido", ipad);

        // Caso 2: altro oggetto valido
        Purchase iphone = new Purchase();
        iphone.setName("iPhone 16");
        iphone.setPrice(999.90);
        iphone.setAmount(8);
        printPurchase("Caso 2 - Valido", iphone);

        // Caso 3: test validazione prezzo negativo
        Purchase mouse = new Purchase();
        mouse.setName("Magic Mouse");
        mouse.setPrice(89.99);
        mouse.setAmount(20);
        System.out.println("\nTentativo di assegnare prezzo negativo a " + mouse.getName() + "...");
        mouse.setPrice(-10.0); // Deve essere rifiutato dal controllo nel setter
        printPurchase("Caso 3 - Dopo prezzo negativo", mouse);

        // Caso 4: prezzo zero (valido, non negativo)
        Purchase promo = new Purchase();
        promo.setName("Cover Promo");
        promo.setPrice(0.0);
        promo.setAmount(50);
        printPurchase("Caso 4 - Prezzo zero", promo);
    }

    // Metodo di supporto per stampare sempre lo stesso formato di output.
    private static void printPurchase(String titolo, Purchase purchase) {
        System.out.printf("\n%s\nNome: %s\nPrezzo: %.2f\nQuantita: %d\n",
                titolo,
                purchase.getName(),
                purchase.getPrice(),
                purchase.getAmount());
    }
}
