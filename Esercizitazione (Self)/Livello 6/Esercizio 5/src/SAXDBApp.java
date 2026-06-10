import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public class SAXDBApp extends DefaultHandler {
    private boolean isFirst = false;
    private boolean isLast = false;

    private StringBuilder FirtsName  = new StringBuilder();
    private StringBuilder LastName = new StringBuilder();
    private StringBuilder idNumBuffer = new StringBuilder();

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
        if (qName.equals("person")) {
            String id = attributes.getValue("idnum");

            if (id != null) idNumBuffer.append(id);
        }

        if(qName.equals("first")) isFirst = true;
        if(qName.equals("last")) isLast = true;
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        if (isFirst) FirtsName.append(new String(ch, start, length));
        if (isLast) LastName.append(new String(ch, start, length));
    }

    @Override
    public void endElement(String uri, String localName, String qName) throws SAXException {
        if(qName.equals("first")) isFirst = false;
        if(qName.equals("last")) isLast = false;

        if(qName.equals("person")) {
            System.out.println("Informazioni Persona: " + FirtsName + " " + LastName + " (" + idNumBuffer + ")" );
            FirtsName.setLength(0);
            LastName.setLength(0);
            idNumBuffer.setLength(0);
        }
    }
}
