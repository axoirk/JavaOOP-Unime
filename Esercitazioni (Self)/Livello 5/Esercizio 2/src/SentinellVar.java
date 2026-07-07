public class SentinellVar {
    private static volatile boolean state = true;

    public static void stop() {
        state = false;
    }

    public static boolean getState() {
        return state;
    }
}
