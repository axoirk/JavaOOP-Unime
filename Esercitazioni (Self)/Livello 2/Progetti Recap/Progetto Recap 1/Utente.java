public class Utente{
	private String username;
	private String email;
	
	Utente(String username, String email) {
		this.username = username;
		this.email = email;
	}
	
	Utente(){};
	
	public void setUsername(String newUsername){
		username = newUsername;
	}
	
	public void setEmail(String newEmail){
		email = newEmail;
	}
	
	public String getUsername(){
		return username;
	}
	
	public String getEmail(){
		return email;
	}
	
	public void printInfo(){
		System.out.printf("Utente: %s, Email: %s\n", username, email);
	}
}