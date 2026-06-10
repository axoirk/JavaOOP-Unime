import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;

/**
 * Classe di test per la lista concatenata custom.
 * Usa reflection per ispezionare i nodi senza cambiare la visibilita' interna.
 */
public class Main {

    public static void main(String[] args) {
        StringLinkedList list = new StringLinkedList();

        runTest("Stato iniziale", list);

        list.addHead("Pane");
        runTest("Dopo addHead(\"Pane\")", list);

        list.addHead("Latte");
        runTest("Dopo addHead(\"Latte\")", list);

        list.addTail("Uova");
        runTest("Dopo addTail(\"Uova\")", list);

        list.addTail("Burro");
        runTest("Dopo addTail(\"Burro\")", list);
    }

    private static void runTest(String title, StringLinkedList list) {
        System.out.println("==== " + title + " ====");
        System.out.println("Contenuto lista: " + snapshot(list));
        System.out.println();
    }

    // Costruisce una vista leggibile della lista attraversando i nodi via reflection.
    private static List<String> snapshot(StringLinkedList list) {
        List<String> values = new ArrayList<>();
        try {
            Field headField = StringLinkedList.class.getDeclaredField("head");
            headField.setAccessible(true);
            Object current = headField.get(list);

            while (current != null) {
                Class<?> nodeClass = current.getClass();
                Field dataField = nodeClass.getDeclaredField("data");
                Field linkField = nodeClass.getDeclaredField("link");
                dataField.setAccessible(true);
                linkField.setAccessible(true);

                values.add((String) dataField.get(current));
                current = linkField.get(current);
            }
        } catch (ReflectiveOperationException e) {
            throw new RuntimeException("Errore durante l'ispezione della lista", e);
        }
        return values;
    }
}
