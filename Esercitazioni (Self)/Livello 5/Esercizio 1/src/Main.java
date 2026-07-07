/*
sercizio 3: Thread Base e Parallelismo Fittizio.
Obiettivo: Far eseguire a Java due compiti simultaneamente.
Come fare: Crea due classi, Coffee e Tea, ed entrambe devono implements Runnable o extends Thread.
Nel metodo obbligatorio run(), crea un ciclo infinito while(true) che stampa un messaggio e invoca Thread.sleep(1000) per mettere in pausa il thread per 1 secondo (catturando la potenziale InterruptedException).
Nel main, crea le due istanze e chiama il metodo start() su entrambe per avviare l'esecuzione in parallelo.
* */
public class Main {
    public static void main(String[] args) {
        Coffee runnableCoffee = new Coffee();
        Tea runnableTea = new Tea();

        Thread tC = new Thread(runnableCoffee);
        Thread tT = new Thread(runnableTea);

        tC.start();
        tT.start();
    }
}
