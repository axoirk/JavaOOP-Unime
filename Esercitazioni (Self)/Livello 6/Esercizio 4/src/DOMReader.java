
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;


public class DOMReader  {
    public File fileXML;

    public DOMReader(String fileXML) {
        this.fileXML = new File(fileXML);
    }

    public void read() throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setIgnoringComments(true);

        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(fileXML);

        doc.getDocumentElement().normalize();
        NodeList studenti = doc.getElementsByTagName("studente");

        for (int i = 0; i < studenti.getLength(); i++) {
            String name;
            String surname;
            String id_student;

            Node nodo = studenti.item(i);

            if (nodo.getNodeType() == Node.ELEMENT_NODE) {
                Element studente = (Element) nodo;

                name = studente.getElementsByTagName("nome").item(0).getTextContent();
                surname = studente.getElementsByTagName("cognome").item(0).getTextContent();
                id_student = studente.getElementsByTagName("matricola").item(0).getTextContent();

                System.out.printf("Nome: %s %s, Matricola: %s\n", name, surname, id_student);
            }
        }
    }
}
