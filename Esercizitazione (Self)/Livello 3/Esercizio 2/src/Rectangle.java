/**
 * Implementazione concreta di ShapeBase.
 * Disegna un rettangolo con bordo usando caratteri '*'.
 */
public class Rectangle extends ShapeBase {
    private final int BASE = 10;
    private final int HEIGHT = 5;

    @Override
    public void drawHere() {
        // Riga superiore del rettangolo.
        System.out.println("*".repeat(BASE));
        for (int i = 0; i < HEIGHT; i++) {
            String spazi = " ".repeat(Math.max(0, BASE - 2));
            System.out.println("*" + spazi + "*");
        }

        if (HEIGHT >= 0) {
            System.out.println("*".repeat(BASE));
        }

        System.out.println("\n" + "-".repeat(10));
    }
}
