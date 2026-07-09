// Inserisci qui la tua soluzione:
abstract class Animale {
	public abstract String verso();
}

class Cane extends Animale {
	@Override
	public String verso() {
		return "bau";
	}

}

class Gatto extends Animale {
	@Override
	public String verso() {
		return "miao";
	}
}