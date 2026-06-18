package com.unime.app;

import java.util.Scanner;
import com.unime.math.*;

public class Main {
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        UtiliyMath utMath = new UtiliyMath();

        System.out.println("Inserisci 2 valori interi: (Suddivisi da spazio): ");

        int a = scanner.nextInt();
        int b = scanner.nextInt();

        System.out.printf("La somma dei 2 numeri equivale a: " + utMath.somma(a, b));
    }
}
