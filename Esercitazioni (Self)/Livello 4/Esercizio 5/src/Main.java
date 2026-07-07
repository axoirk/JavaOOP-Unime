import java.io.*;

public class Main {
    public static void main(String[] args) {
        Species specie = new Species("Pietra di marte", "Pietre");

        // --- WRITE ---
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("save.ser"))) {
            out.writeObject(specie);
            System.out.println("Oggetto salvato correttamente in save.ser");

        } catch (FileNotFoundException e) {
            System.err.println("Errore in scrittura: Impossibile creare o aprire il file 'save.ser'.");
            e.printStackTrace();
        } catch (IOException e) {
            System.err.println("Errore di I/O durante la scrittura dell'oggetto.");
            e.printStackTrace();
        }

        // --- READ ---
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("save.ser"))) {

            Species loadedSpecie = (Species) in.readObject();

            System.out.println("Nome Specie caricato: " + loadedSpecie.nome);
            System.out.println("Tipo Specie caricato: " + loadedSpecie.specie);

        } catch (FileNotFoundException e) {
            System.err.println("Errore in lettura: Nessun file di salvataggio trovato.");

        } catch (EOFException e) {
            System.err.println("Errore in lettura: Raggiunta inaspettatamente la fine del file (file corrotto).");

        } catch (ClassNotFoundException e) {
            System.err.println("Errore in lettura: La classe 'Species' non è presente in questo progetto.");

        } catch (IOException e) {
            System.err.println("Errore generico di I/O durante la lettura.");
            e.printStackTrace();
        }
    }
}