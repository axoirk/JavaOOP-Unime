/**
 * Classe di prova per classi astratte e polimorfismo.
 * L'array e' tipizzato con la superclasse astratta, ma contiene sottoclassi diverse.
 */
public class Main {
    public static void main(String[] args) {

        ShapeBase[] shapes = new ShapeBase[8];

        // Associazione dinamica: a runtime ogni elemento e' Rectangle o Triangle.
        for (int i = 0; i < shapes.length; i++) {
            shapes[i] = (i % 2 == 0) ? new Triangle() : new Rectangle();
        }

        for (ShapeBase shape : shapes) {
            shape.drawHere();
        }
    }
}
