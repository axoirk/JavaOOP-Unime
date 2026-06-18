import java.io.BufferedReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {
    public static void main(String[] args) throws IOException {
        Socket server = new Socket("127.0.0.1", 9000);
        try {
            PrintWriter out = new PrintWriter(new OutputStreamWriter(server.getOutputStream()), true);
            out.println("Ciao dal Client TCP!");

        } catch (Exception e) {
            System.out.printf(e.getMessage(), e.getStackTrace());
        } finally {
            server.close();
        }
    }
}
