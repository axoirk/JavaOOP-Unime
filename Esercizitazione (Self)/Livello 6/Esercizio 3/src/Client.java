import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Client {
    public static void main(String[] args) throws IOException {
        try (DatagramSocket clientSocket = new DatagramSocket()){ // Inizializzazione socket
            String message = "Ciao! Sto inviando un messaggio tramite protocollo UDP!";
            byte[] data = message.getBytes(); // Trasformiamo il messaggio lettibile in bytes

            // Inizialzziamo il pachetto, passando come paramenti il messaggio in byets, il peso del pacchetto, e la sua destinazione definiendo host e porta.
            DatagramPacket packet = new DatagramPacket(data, data.length, InetAddress.getByName("127.0.0.1"), 9000);
            clientSocket.send(packet); // Inviamo il pacchetto
            System.out.println("[Client UDP] Pacchetto inviato.");


        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
