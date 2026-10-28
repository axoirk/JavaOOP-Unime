#!/usr/bin/env bash
#
# esegui.sh — replica il pulsante "Esegui" di Moodle durante l'appello.
#
# Compila Soluzione.java, lancia il tester invisibile (Main.class) e conta
# le esecuzioni. All'appello il limite è 5 per esercizio: oltre, penalità.
# Un errore di compilazione consuma un'esecuzione esattamente come un successo.
# Come su Moodle si compila da zero: i .class dei run precedenti vengono
# cancellati (resta solo il tester, Main.class e le sue classi interne).
#
# Uso:
#   ./esegui.sh [cartella_esercizio]      esegue (default: cartella corrente)
#   ./esegui.sh [cartella] --reset        azzera il contatore
#   ./esegui.sh [cartella] --stato        mostra il contatore senza eseguire

set -u

LIMITE=5
DIR="."
AZIONE="esegui"

for arg in "$@"; do
	case "$arg" in
		--reset) AZIONE="reset" ;;
		--stato) AZIONE="stato" ;;
		-h|--help) sed -n '3,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
		*) DIR="$arg" ;;
	esac
done

cd "$DIR" 2>/dev/null || { echo "Cartella non trovata: $DIR" >&2; exit 1; }

ESERCIZIO="$(basename "$PWD")"
CONTATORE=".esecuzioni"
[ -f "$CONTATORE" ] || echo 0 > "$CONTATORE"
N="$(cat "$CONTATORE")"

case "$AZIONE" in
	reset)
		echo 0 > "$CONTATORE"
		echo "[$ESERCIZIO] contatore azzerato."
		exit 0
		;;
	stato)
		echo "[$ESERCIZIO] esecuzioni consumate: $N / $LIMITE"
		exit 0
		;;
esac

[ -f "Soluzione.java" ] || { echo "Nessun Soluzione.java in $PWD" >&2; exit 1; }
[ -f "Main.class" ] || { echo "Nessun Main.class (tester) in $PWD" >&2; exit 1; }

N=$((N + 1))
echo "$N" > "$CONTATORE"

echo "──────────────────────────────────────────────"
printf ' %s — esecuzione %d di %d\n' "$ESERCIZIO" "$N" "$LIMITE"
if [ "$N" -gt "$LIMITE" ]; then
	printf ' ⚠  OLTRE IL LIMITE: %d esecuzione/i in eccesso. Penalità sul punteggio.\n' "$((N - LIMITE))"
fi
echo "──────────────────────────────────────────────"

find . -maxdepth 1 -name '*.class' ! -name 'Main.class' ! -name 'Main$*.class' -delete

if ! javac Soluzione.java; then
	echo "──────────────────────────────────────────────"
	echo " ERRORE DI COMPILAZIONE — esecuzione consumata comunque."
	printf ' Esecuzioni: %d / %d\n' "$N" "$LIMITE"
	exit 1
fi

java -cp . Main
ESITO=$?

echo "──────────────────────────────────────────────"
printf ' Esecuzioni: %d / %d\n' "$N" "$LIMITE"
exit "$ESITO"
