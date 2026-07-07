public class Main{
	public static void main(String[] args) {
		int[] numeri = {34, 7, 23, 89, 2};
		
		int min = 0, max = 0;
		
		for(int i = 0; i < numeri.length; i++) {
			if (i == 0 || numeri[i] < min) min = numeri[i];
			if(numeri[i] > max) max = numeri[i];
		}
		
		System.out.printf("Max: %d, Min: %d", max, min);
	}
}