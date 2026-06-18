/**
 * Esercizio sull'algoritmo Selection Sort.
 * Mostra generazione dati, stampa e ordinamento in-place di un array.
 */
public class Main {
    public  static void  printArray(int[] arr){
        for (int i = 0; i < arr.length; i++){
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        int space = 10;
        int[] array = new int[space];

        for (int i = 0; i < array.length; i++) {
            array[i] = (int)(Math.random() * 30 + 1);
        }

        printArray(array);

       // Selection Sort: ad ogni iterazione posiziona il minimo nella cella corrente.
       for (int k = 0; k < space - 1; k++) {
           int minIndex = k;
           for (int j = k + 1; j < space; j++) {
               if (array[j] < array[minIndex]) {
                   minIndex = j;
               }
           }
           int temp = array[k];
           array[k] = array[minIndex];
           array[minIndex] = temp;
       }
        printArray(array);
    }
}
