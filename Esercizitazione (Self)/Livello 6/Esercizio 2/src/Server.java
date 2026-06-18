import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;


public class Server {
    public static void main(String[] args) throws IOException {
       ServerSocket server = new ServerSocket(9000);
        System.out.println("[Server] Server avviato e in ascolto sulla porta " + server.getLocalPort());
        try {
            while (true) {
                Socket clientSocket = server.accept();
                System.out.println("[Server] Client connesso: " + clientSocket.getInetAddress());
                try (BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()))) {
                    System.out.println("[Server] Messaggio ricevuto: " + in.readLine());
                }
            }
        } finally {
            server.close();
        }
    }
}
