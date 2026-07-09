// Inserisci qui la tua soluzione:

class Studente extends Persona implements Runnable {
	private int matricola;
	private String cds;
	
	public Studente(String nome, String cognome, int matricola) {
		super(nome, cognome);
		this.matricola = matricola;
	}
	
	public Studente(int matricola, String cds) {
		this.matricola = matricola;
		this.cds = cds;
	}
	
	
	@Override
	public void run() {
		matricola = (int) Math.pow(matricola, 2);
	}
	
	public int getMatricola() {
		return matricola;
	}
	
	public String getCds() {
		return cds;
	}
	
	public void setMatricola(int matricola) {
		this.matricola = matricola;
	}
	
	public void setCds(String cds) {
		this.cds = cds;
	}
}



// ==========================================
// CODICE PRE-FORNITO DAL DOCENTE
// ==========================================

class Persona {
    private String nome;
    private String cognome;

    public Persona() {}
    
    public Persona(String nome, String cognome) {
        this.nome = nome;
        this.cognome = cognome;
    }

    public String getNome() { return nome; }
    public String getCognome() { return cognome; }
    public void setNome(String nome) { this.nome = nome; }
    public void setCognome(String cognome) { this.cognome = cognome; }
}


