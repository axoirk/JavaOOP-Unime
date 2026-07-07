package org.esame.analisi;

public class Analisi {
	public int analizza(char[] input) {
		int vocals = 0;
	
		for(int i = 0; i < input.length; i++) {
			if(input[i] == '#') break;
				
			switch(input[i]) {
				case 'a':
					vocals++;
					break;
				case 'e':
					vocals++;
					break;
				case 'i':
					vocals++;
					break;
				case 'o':
					vocals++;
					break;
				case 'u':
					vocals++;
					break;
				default:
					break;
			}
		}
		
		return vocals;
	}
}