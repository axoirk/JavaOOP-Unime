public class Main {
    public static void main(String[] args) throws Exception {
        DOMReader reader = new DOMReader("studenti.xml");
        reader.read();
    }
}
