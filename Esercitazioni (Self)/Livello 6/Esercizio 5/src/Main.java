/*
Esercizio 5: Event-Based XML Parsing (SAX).
Obiettivo: Intercettare eventi durante la lettura di un file XML.
Come fare: Crea un piccolo file person.xml. Nel codice Java, usa SAXParserFactory per ottenere un parser SAX.
Crea una classe SAXDBApp che estenda DefaultHandler e fai l'override di startElement(), endElement() e characters().
Nella logica dei metodi, usa dei booleani (es. InFirst, InLast) per capire quando stai leggendo un certo tag e stampa il valore estratto dal documento XML alla chiusura del tag
* */

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import java.io.File;

public class Main {
    public static void main (String[] args) {

        try {
            SAXParserFactory factory = SAXParserFactory.newInstance();
            SAXParser saxParser = factory.newSAXParser();
            SAXDBApp handler = new SAXDBApp();
            saxParser.parse(new File("person.xml"), handler);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
