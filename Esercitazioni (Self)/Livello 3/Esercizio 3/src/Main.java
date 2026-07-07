import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {

        ArrayList<Measurable> listObj = new ArrayList<>();

        Circle circle = new Circle(20.0);
        Smartphone phone = new Smartphone(30, 14.5);

        listObj.add(circle);
        listObj.add(phone);

        for (int i = 0; i < listObj.size(); i++) {

            System.out.println("L'area dell'oggetto " + listObj.get(i).getClass().getName() + " equivale a: " + listObj.get(i).getArea());
            System.out.println("Il perimetro dell'oggetto " + listObj.get(i).getClass().getName() + " equivale a: " + listObj.get(i).getPerimeter());
        }

        // FOR-EACH VERSION
//        for (Measurable obj : listObj) {
//            System.out.println("L'area dell'oggetto " + obj.getClass().getName() + " equivale a: " + obj.getArea());
//            System.out.println("Il perimetro dell'oggetto " + obj.getClass().getName() + " equivale a: " + obj.getPerimeter());
//        }
    }
}
