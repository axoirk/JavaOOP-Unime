/**
 * Implementazione concreta di ShapeBase.
 * Disegna un triangolo isoscele centrato usando cicli annidati.
 */
public class Triangle extends ShapeBase {
    private final int HEIGHT = 5;

    @Override
    public void drawHere() {
        for (int i = 1; i <= HEIGHT; i++) {
            // Spazi iniziali per centrare la riga corrente.
            for (int j = HEIGHT; j > i; j--) {
                System.out.print(" ");
            }

            // Numero dispari di asterischi per ogni livello del triangolo.
            for (int k = 1; k <= (2 * i - 1); k++) {
                System.out.print("*");
            }
            System.out.println();
        }

        System.out.println("\n" + "-".repeat(10));
    }
}
