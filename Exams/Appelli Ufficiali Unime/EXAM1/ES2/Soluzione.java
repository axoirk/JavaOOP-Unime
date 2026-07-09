// Inserisci qui la tua soluzione:
import java.io.*;

class GestoreEccezioni {
	public static void esegui(int n) throws Exception {
		try {
			if(n == 0) {
				System.out.println("eccezzione generica");
				throw new Exception();
			}
			
			if(n == 1) {
				throw new IOException();
			}
			
			if(n == 2) {
				System.out.println("no eccezzioni");
			}
			
		} catch (IOException e) {
			System.out.println("eccezzione runtime");
			throw new RuntimeException();
		} finally {
			
		}
	}
}