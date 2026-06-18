import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class Server {
    public static void main(String[] args) throws IOException {
       try (DatagramSocket serverSocket = new DatagramSocket(9000)){ // Inizializziamo il socket d'ascolto
           byte[] buffer = new byte[1024]; // Inizializziamo un buffer con una capienza massima di 1024 Bytes
           DatagramPacket packet = new DatagramPacket(buffer, buffer.length);  // Inizializziamo il packet contenitore dove riceverà i dati inviati dai vari client
           System.out.println("[Server UDP] Connesso sulla porta " + serverSocket.getLocalPort());

           // Il server si mette in stato di ascolto e attende fino a quando non riceve un pacchetto. Se riceve un informazione, continua con l'esecuzione della logica
           serverSocket.receive(packet);

           // Elaboriamo il pacchetto estrando il contenuto, e dopodichè lo printiamo in console
           String message = new String(packet.getData(), 0, packet.getLength());
           System.out.println("[Server UDP] Ricevuto pacchetto: " + message);

       } catch (Exception e) {
           throw new RuntimeException(e);
       }
    }
}
