public class Circle implements Measurable {
    private double raggio;

    public Circle(double raggio) {
        this.raggio = raggio;
    }

    @Override
    public double getArea() {
        return Math.PI * Math.pow(this.raggio, 2);

    }

    @Override
    public double getPerimeter() {
        return 2 * Math.PI * this.raggio;
    }
}
