import java.util.ArrayList;


public class Scuola {

		private class Studente {
			private String nome;
			private int age;
			
			Studente(String nome, int age) {
				this.nome = nome;
				this.age = age;
			}
			
			public String getNome() {
				return nome;
			}
			
			public int getAge() {
				return age;
			}
		}
		
		private ArrayList<Studente> studenti = new ArrayList<>();
		
		
		public void aggiungiStudente(String nome, int age) {
			Studente studente = new Studente(nome, age);
			studenti.add(studente);
		}
		
		public void mostraStudenti(){
			for(Studente studente : studenti) {
				System.out.printf("Studente: %s, Età: %d\n", studente.getNome(), studente.getAge());
			}
		}	
	
}