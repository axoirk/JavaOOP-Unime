public class Smartphone implements Measurable {
    public double height;
    public double width;

    public Smartphone(double height, double width) {
        this.height = height;
        this.width = width;
    }

    @Override
    public double getArea() {
        return height * width;
    }

    @Override
    public double getPerimeter() {
        return (2 * height) + (2 * width);
    }
}
