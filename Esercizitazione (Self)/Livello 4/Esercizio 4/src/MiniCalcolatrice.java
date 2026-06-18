import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MiniCalcolatrice {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                createGUI();
            }
        });
    }

    private static void createGUI () {
        JFrame frame = new JFrame("Mini-Calcolatrice");

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setSize(300, 200);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);


        JPanel panel = new JPanel(new GridLayout(4, 1, 5, 5));

        JTextField inputFirstNumber = new JTextField();
        JTextField inputSecondNumber = new JTextField();

        JButton calcolaBtn = new JButton("Calcola somma");
        JLabel resultText = new JLabel("Risultato: ---", SwingConstants.CENTER);

        panel.add(inputFirstNumber);
        panel.add(inputSecondNumber);
        panel.add(calcolaBtn);
        panel.add(resultText);

        frame.add(panel);

        calcolaBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    int val1 = Integer.parseInt(inputFirstNumber.getText());
                    int val2 = Integer.parseInt(inputSecondNumber.getText());

                    int summ = val1 + val2;
                    resultText.setText(String.format("Risultato: %d", summ));
                } catch (NumberFormatException error) {
                    JOptionPane.showMessageDialog(frame, "Inserisci solo numeri interi validi!", "Errore", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

    }
}