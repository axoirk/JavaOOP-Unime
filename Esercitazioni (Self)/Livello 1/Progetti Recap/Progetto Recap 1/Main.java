public class Main{
	public static void main(String[] args) {
		int anno = 2024;
		
		boolean annoBisestile = false;
		
		if ((anno % 4 == 0 && anno % 100 != 0) || anno % 400 == 0 ) annoBisestile = true;
		
		if (annoBisestile) {
			System.out.printf("L'anno %d, è bisestile", anno);
		} else {
			System.out.printf("L'anno %d, NON è bisestile", anno);
		}
	}
}