import javax.swing.*;

public class FinestraBase {
    static void main() {
        JFrame jFrame  = new JFrame("La mia prima GUI");

        jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jFrame.setSize(400, 300);

        JPanel jPanel = new JPanel();
        JLabel jLabel = new JLabel("Benvenuto nella mia prima GUI!");
        JButton jButton = new JButton("Questo è un pulsante!");

        jPanel.add(jLabel);
        jPanel.add(jButton);

        jFrame.add(jPanel);
        jFrame.setVisible(true);
    }
}
