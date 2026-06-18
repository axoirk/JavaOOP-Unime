public class GestioneBancaria {
    public static final double TASSO_INTERESSE_MAX = 5.0;
    private static int totaleContiAperti = 0;


    public static void incrementConti() {
        GestioneBancaria.totaleContiAperti++;
    }

    public static int getTotaleConti() {
        return GestioneBancaria.totaleContiAperti;
    }
}
