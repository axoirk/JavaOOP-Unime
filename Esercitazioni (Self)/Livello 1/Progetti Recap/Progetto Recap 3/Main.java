package org.esame.analisi;

import org.esame.analisi.Analisi;

public class Main{
	public static void main(String[] args) {
		char[] input = {'p', 'r', 'o', 'g', 'r', 'a', 'm', 'm', 'a', 'z', 'i', 'o', 'n', 'e', '#', 'a', 'b', 'c'};
		
		Analisi analisi = new Analisi();
		
		int vocals = Analisi.analizza(input);
		System.out.println("Totale vocali:" + vocals);
	}
}