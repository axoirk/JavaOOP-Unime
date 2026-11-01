#!/usr/bin/env python3
"""aula.py — replica in locale la pagina d'esame Moodle per una simulazione.

Apre una finestra del browser con le tre tracce, il cronometro dei
45 minuti complessivi e il pulsante Esegui per esercizio (max 5 esecuzioni, oltre
scatta la penalita'). Il codice si scrive nella pagina stessa, accanto alla
traccia: un editor con colorazione della sintassi Java, numeri di riga,
parentesi chiuse in automatico e rientro a capo (nessun completamento,
nessun controllo degli errori). Cmd+Invio esegue, Esc esce dall'editor. Ogni modifica
viene salvata in ESn/Soluzione.java, che resta il file compilato, quello
riportato nella consegna e quello usato da esegui.sh.

Dopo un Esegui la pagina elenca le singole verifiche del tester con il loro
esito e, su quelle fallite, il valore atteso e quello prodotto — come il
riquadro dei test di Moodle. Il report di consegna, generato alla consegna
manuale o allo scadere del tempo, conserva l'output integrale di ogni run.

Il pulsante Pausa ferma il cronometro e sospende le esecuzioni; la pausa
sopravvive alla chiusura della finestra e non viene conteggiata nel tempo
di prova. Chiudere il server senza mettere in pausa, invece, lascia
l'orologio in corsa: il tempo e' quello reale. In pausa, e dopo la
consegna, l'editor diventa di sola lettura.

Uso:
    python3 Exams/aula.py "Exams/Simulazioni/Prove/SIM_1"
    python3 Exams/aula.py <cartella> --durata 45      minuti (default 45)
    python3 Exams/aula.py <cartella> --riparti        azzera prova e contatori
    python3 Exams/aula.py <cartella> --porta 8765
"""

import html
import json
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ESERCIZI = ["ES1", "ES2", "ES3"]
PUNTI = {"ES1": 5, "ES2": 13, "ES3": 13}
LIMITE_ESECUZIONI = 5
TIMEOUT_RUN = 30

stato_lock = threading.Lock()


# --------------------------------------------------------------------------
# Stato della prova
# --------------------------------------------------------------------------

class Prova:

    def __init__(self, cartella: Path, durata_min: int, riparti: bool):
        self.cartella = cartella
        self.fase = None    # "compilazione" o "esecuzione" mentre un Esegui e' in corso
        self.file_stato = cartella / ".aula.json"
        if riparti and self.file_stato.exists():
            self.file_stato.unlink()
        if self.file_stato.exists():
            self.dati = json.loads(self.file_stato.read_text())
        else:
            self.dati = {
                "simulazione": cartella.name,
                "inizio": time.time(),
                "durata": durata_min * 60,
                "consegnato": False,
                "consegna_ts": None,
                "pausa_da": None,
                "pausa_totale": 0.0,
                "motivo_consegna": None,
                "report": None,
                "esecuzioni": {e: [] for e in ESERCIZI},
            }
            self.salva()
        self.dati.setdefault("pausa_da", None)
        self.dati.setdefault("pausa_totale", 0.0)
        if riparti:
            for e in ESERCIZI:
                contatore = cartella / e / ".esecuzioni"
                if contatore.exists():
                    contatore.write_text("0\n")

    def salva(self):
        self.file_stato.write_text(json.dumps(self.dati, indent=1, ensure_ascii=False))

    # -- tempo ------------------------------------------------------------

    def trascorso(self) -> float:
        if self.dati["consegnato"] and self.dati["consegna_ts"]:
            adesso = self.dati["consegna_ts"]
        else:
            # In pausa l'orologio resta fermo all'istante in cui si e' premuto Pausa.
            adesso = self.dati["pausa_da"] or time.time()
        return adesso - self.dati["inizio"] - self.dati["pausa_totale"]

    def in_pausa(self) -> bool:
        return self.dati["pausa_da"] is not None and not self.dati["consegnato"]

    def commuta_pausa(self) -> bool:
        if self.dati["consegnato"]:
            return False
        if self.dati["pausa_da"] is None:
            self.dati["pausa_da"] = time.time()
        else:
            self.dati["pausa_totale"] += time.time() - self.dati["pausa_da"]
            self.dati["pausa_da"] = None
        self.salva()
        return self.in_pausa()

    def rimanente(self) -> float:
        return max(0.0, self.dati["durata"] - self.trascorso())

    def scaduto(self) -> bool:
        return self.rimanente() <= 0

    # -- esecuzioni -------------------------------------------------------

    def numero_esecuzioni(self, es: str) -> int:
        """Legge .esecuzioni, il contatore condiviso con esegui.sh."""
        contatore = self.cartella / es / ".esecuzioni"
        return int(contatore.read_text().strip() or 0) if contatore.exists() else 0

    def leggi_codice(self, es: str) -> str:
        return (self.cartella / es / "Soluzione.java").read_text()

    def scrivi_codice(self, es: str, codice: str):
        percorso = self.cartella / es / "Soluzione.java"
        provvisorio = percorso.with_suffix(".tmp")
        provvisorio.write_text(codice)
        os.replace(provvisorio, percorso)   # javac puo' leggerlo mentre si salva

    def esegui(self, es: str) -> dict:
        """Gira senza stato_lock: durante una run di 30 secondi il cronometro,
        il salvataggio e la pausa devono continuare a rispondere. Il chiamante
        imposta self.fase, che impedisce una seconda run e la consegna."""
        cartella_es = self.cartella / es
        n = self.numero_esecuzioni(es) + 1
        codice = self.leggi_codice(es)
        avvio = time.time()

        # Come su Moodle si compila da zero: un .class rimasto da un run
        # precedente farebbe compilare codice che non esiste piu'.
        for vecchio in cartella_es.glob("*.class"):
            if vecchio.name != "Main.class" and not vecchio.name.startswith("Main$"):
                vecchio.unlink()

        compila = subprocess.run(
            ["javac", "Soluzione.java"],
            cwd=cartella_es, capture_output=True, text=True)

        if compila.returncode != 0:
            esito = "COMPILAZIONE"
            uscita = compila.stderr.strip() or compila.stdout.strip()
        else:
            self.fase = "esecuzione"
            try:
                run = subprocess.run(
                    ["java", "-cp", ".", "Main"],
                    cwd=cartella_es, capture_output=True, text=True,
                    timeout=TIMEOUT_RUN)
                esito = "SUPERATO" if run.returncode == 0 else "FALLITO"
                uscita = (run.stdout + run.stderr).strip()
            except subprocess.TimeoutExpired:
                esito = "BLOCCO"
                uscita = f"Nessuna risposta entro {TIMEOUT_RUN} secondi: esecuzione interrotta."

        voce = {
            "n": n,
            "istante": round(self.trascorso(), 1),
            "durata": round(time.time() - avvio, 2),
            "esito": esito,
            "oltre_limite": n > LIMITE_ESECUZIONI,
            "uscita": uscita,
            "verifiche": analizza_verifiche(uscita) if esito in ("SUPERATO", "FALLITO") else [],
            "errori_compilatore": compila.stderr.strip() if compila.returncode != 0 else "",
            "codice": codice,
        }
        with stato_lock:
            self.dati["esecuzioni"][es].append(voce)
            self.salva()
            (cartella_es / ".esecuzioni").write_text(f"{n}\n")
        return voce

    # -- consegna ---------------------------------------------------------

    def consegna(self, motivo: str) -> str:
        if self.dati["consegnato"]:
            return self.dati["report"]
        self.dati["consegnato"] = True
        limite = self.dati["inizio"] + self.dati["durata"] + self.dati["pausa_totale"]
        self.dati["consegna_ts"] = min(time.time(), limite) \
            if motivo == "tempo scaduto" else time.time()
        if self.dati["pausa_da"] is not None:      # consegna a prova in pausa
            self.dati["pausa_totale"] += time.time() - self.dati["pausa_da"]
            self.dati["pausa_da"] = None
        self.dati["motivo_consegna"] = motivo
        percorso = self.scrivi_report(motivo)
        self.dati["report"] = percorso
        self.salva()
        return percorso

    def scrivi_report(self, motivo: str) -> str:
        marca = time.strftime("%Y%m%d-%H%M", time.localtime())
        nome = f"Consegna_{self.cartella.name}_{marca}.md"
        destinazione = self.cartella / nome
        trascorso = self.trascorso()

        r = []
        r.append(f"# Consegna — {self.cartella.name}\n")
        r.append("Dati grezzi della prova. **Nessun punteggio**: la correzione va svolta "
                 "a parte, secondo la rubrica a quattro assi di `Exams/REGOLE_GENERAZIONE_AI.MD` §7.\n")
        r.append("## Prova\n")
        r.append(f"- **Data:** {time.strftime('%d/%m/%Y %H:%M', time.localtime(self.dati['inizio']))}")
        r.append(f"- **Durata concessa:** {int(self.dati['durata'] // 60)} minuti")
        r.append(f"- **Tempo impiegato:** {formatta(trascorso)}")
        r.append(f"- **Motivo della consegna:** {motivo}")
        if self.dati["pausa_totale"] > 0:
            r.append(f"- **Tempo in pausa (non conteggiato):** {formatta(self.dati['pausa_totale'])}")
        r.append("- **Ambiente:** editor nella pagina, colorazione della sintassi e parentesi automatiche "
                 "(nessuna analisi del codice), un solo file per esercizio\n")

        r.append("## Esecuzioni\n")
        r.append("| Esercizio | Punti | Esecuzioni | Oltre il limite | Esito ultima |")
        r.append("|---|---|---|---|---|")
        for es in ESERCIZI:
            voci = self.dati["esecuzioni"][es]
            n = self.numero_esecuzioni(es)    # comprende i run fatti con esegui.sh
            oltre = max(0, n - LIMITE_ESECUZIONI)
            ultima = voci[-1]["esito"] if voci else "—"
            r.append(f"| {es} | {PUNTI[es]} | {n} / {LIMITE_ESECUZIONI} | "
                     f"{oltre if oltre else '—'} | {ultima} |")
        r.append("")

        for es in ESERCIZI:
            r.append(f"## {es}\n")
            voci = self.dati["esecuzioni"][es]
            if not voci:
                r.append("Nessuna esecuzione registrata.\n")
            for v in voci:
                penalita = " · **oltre il limite**" if v["oltre_limite"] else ""
                r.append(f"### Esecuzione {v['n']} — {v['esito']} "
                         f"(al minuto {formatta(v['istante'])}){penalita}\n")
                r.append("```text")
                r.append(v["uscita"] or "(nessun output)")
                r.append("```\n")
            sorgente = self.cartella / es / "Soluzione.java"
            r.append(f"### Codice consegnato\n")
            r.append("```java")
            r.append(sorgente.read_text().rstrip() if sorgente.exists() else "(file assente)")
            r.append("```\n")

        destinazione.write_text("\n".join(r))
        return str(destinazione)


def analizza_verifiche(uscita: str) -> list:
    """Estrae le singole verifiche dall'output del tester.

    Convenzione dei tester (vedi REGOLE_GENERAZIONE_AI.MD §4):
        [OK] nome della verifica
        [KO] nome della verifica
             atteso  : ...
             ottenuto: ...
    Un tester che non la rispetta produce una lista vuota: la pagina mostra
    allora l'output grezzo.
    """
    verifiche = []
    for riga in uscita.split("\n"):
        nuda = riga.strip()
        if nuda.startswith("[OK]") or nuda.startswith("[KO]"):
            verifiche.append({
                "nome": nuda[4:].strip(),
                "superata": nuda.startswith("[OK]"),
                "atteso": None,
                "ottenuto": None,
            })
        elif verifiche and riga.startswith(" ") and ":" in nuda:
            campo, _, valore = nuda.partition(":")
            campo = campo.strip().lower()
            if campo in ("atteso", "ottenuto"):
                verifiche[-1][campo] = valore.strip()
    return verifiche


def risposta_esito(voce: dict) -> dict:
    """Cio' che la pagina riceve di una run, subito dopo Esegui o a una ricarica."""
    return {
        "n": voce["n"],
        "esito": voce["esito"],
        "oltre_limite": voce["oltre_limite"],
        "errori_compilatore": voce["errori_compilatore"],
        "verifiche": voce["verifiche"],
        "uscita": output_residuo(voce),
        "codice": voce.get("codice"),
    }


def output_residuo(voce: dict) -> str:
    """Output da mostrare oltre a verdetto, verifiche ed errori del compilatore:
    su un test fallito resta cio' che ha stampato il programma, eccezioni comprese."""
    if voce["esito"] == "COMPILAZIONE" or voce["esito"] == "SUPERATO" and voce["verifiche"]:
        return ""
    if not voce["verifiche"]:
        return voce["uscita"]
    gia_mostrate = ("[OK]", "[KO]", "atteso", "ottenuto", "---", "TEST SUPERATO", "TEST FALLITO")
    return "\n".join(r for r in voce["uscita"].split("\n")
                     if not r.strip().startswith(gia_mostrate)).strip()


def formatta(secondi: float) -> str:
    secondi = int(secondi)
    return f"{secondi // 60:02d}:{secondi % 60:02d}"


# --------------------------------------------------------------------------
# Traccia: markdown minimale -> HTML
# --------------------------------------------------------------------------

def markdown(testo: str) -> str:
    fuori = []
    in_codice = False
    in_lista = False
    for riga in testo.split("\n"):
        if riga.startswith("```"):
            if in_codice:
                fuori.append("</code></pre>")
            else:
                if in_lista:
                    fuori.append("</ol>")
                    in_lista = False
                fuori.append("<pre><code>")
            in_codice = not in_codice
            continue
        if in_codice:
            fuori.append(html.escape(riga))
            continue

        riga_s = riga.strip()
        if not riga_s:
            if in_lista:
                fuori.append("</ol>")
                in_lista = False
            continue

        voce = re.match(r"^(\d+)\.\s+(.*)$", riga_s)
        if voce:
            if not in_lista:
                fuori.append(f'<ol start="{voce.group(1)}">')
                in_lista = True
            fuori.append(f"<li>{inline(voce.group(2))}</li>")
            continue
        if in_lista and riga[0] in " \t" and riga_s.startswith(("- ", "* ")):
            voce_ol = fuori[-1].removesuffix("</li>")
            fuori[-1] = f"{voce_ol}<p class='trattino'>{inline(riga_s[2:])}</p></li>"
            continue
        if in_lista:
            fuori.append("</ol>")
            in_lista = False

        if riga_s.startswith("### "):
            fuori.append(f"<h3>{inline(riga_s[4:])}</h3>")
        elif riga_s.startswith("## "):
            fuori.append(f"<h2>{inline(riga_s[3:])}</h2>")
        elif riga_s.startswith("# "):
            fuori.append(f"<h1>{inline(riga_s[2:])}</h1>")
        elif riga_s.startswith(("- ", "* ")):
            fuori.append(f"<p class='trattino'>{inline(riga_s[2:])}</p>")
        else:
            fuori.append(f"<p>{inline(riga_s)}</p>")
    if in_lista:
        fuori.append("</ol>")
    if in_codice:
        fuori.append("</code></pre>")
    return "\n".join(fuori)


def inline(testo: str) -> str:
    testo = html.escape(testo)
    testo = re.sub(r"`([^`]+)`", r"<code>\1</code>", testo)
    testo = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", testo)
    return testo


# --------------------------------------------------------------------------
# Pagina
# --------------------------------------------------------------------------

PAGINA = r"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aula — __NOME__</title>
<link rel="icon" href="data:,">
<style>
  :root {
    --sfondo: #14161a; --pannello: #1b1e24; --bordo: #2c313a;
    --testo: #e6e8ec; --tenue: #9aa2b1; --accento: #6ea8fe;
    --ok: #5fd08a; --ko: #ff6b6b; --attenzione: #ffb454;
    --codice: #0f1115;
    --mono: ui-monospace, SFMono-Regular, Menlo, monospace;
    color-scheme: dark;
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body { margin: 0; display: flex; flex-direction: column; overflow: hidden;
         background: var(--sfondo); color: var(--testo);
         font: 14px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
  button { font: inherit; }
  :focus-visible { outline: 2px solid var(--accento); outline-offset: 2px; }
  .sr { position: absolute; width: 1px; height: 1px; overflow: hidden;
        clip-path: inset(50%); white-space: nowrap; }

  header { display: flex; align-items: center; gap: 10px; padding: 10px 18px; flex: none;
           background: var(--pannello); border-bottom: 1px solid var(--bordo); }
  header .titolo { font-weight: 600; letter-spacing: .2px; margin-right: 8px; }
  .spazio { flex: 1; }
  #stato-consegna { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  #cronometro { font: 600 22px/1 var(--mono); margin-left: 8px;
                padding: 6px 12px; border: 1px solid var(--bordo); border-radius: 8px; }
  #cronometro.allarme { color: var(--attenzione); border-color: var(--attenzione); }
  #cronometro.scaduto { color: var(--ko); border-color: var(--ko); }
  #cronometro.pausa { color: var(--tenue); border-style: dashed; }

  #chiusura { display: flex; gap: 32px; align-items: flex-start; justify-content: space-between;
              flex: none; margin: 10px 18px 0; padding: 14px 18px; border-radius: 8px;
              background: var(--pannello); border: 1px solid var(--tenue); }
  #chiusura[hidden] { display: none; }
  #chiusura h2 { margin: 0 0 4px; font-size: 19px; color: var(--testo); letter-spacing: 0;
                 text-transform: none; line-height: 1.3; }
  #chiusura p { margin: 0 0 4px; }
  #chiusura .percorso { color: var(--tenue); font: 12.5px var(--mono); overflow-wrap: anywhere; }
  #chiusura table { border-collapse: collapse; flex: none; font-size: 13px;
                    font-variant-numeric: tabular-nums; }
  #chiusura th, #chiusura td { padding: 3px 14px 3px 0; text-align: left; font-weight: 400; }
  #chiusura thead th { color: var(--tenue); font-size: 12px; }
  #chiusura tbody th { font-weight: 600; }

  main { flex: 1; min-height: 0; display: grid; gap: 16px; padding: 10px 18px 16px;
         grid-template-columns: minmax(340px, 38fr) minmax(0, 62fr);
         grid-template-rows: minmax(0, 1fr); }
  .colonna, .lavoro { display: flex; flex-direction: column; min-width: 0; min-height: 0; }

  .tab { display: flex; gap: 6px; flex: none; }
  .tab button { background: transparent; color: var(--tenue); border: 1px solid transparent;
                border-bottom: none; padding: 8px 12px; border-radius: 8px 8px 0 0;
                cursor: pointer; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .tab button:hover { color: var(--testo); }
  .tab button.attivo { background: var(--pannello); color: var(--testo);
                       border-color: var(--bordo); }
  .tab button .conta { color: var(--tenue); font-size: 12px; margin-left: 8px; }
  .esito-tab { font-size: 12px; font-weight: 600; margin-left: 8px; }
  .esito-tab:empty { display: none; }
  .esito-tab.superato { color: var(--ok); }
  .esito-tab.fallito, .esito-tab.blocco, .esito-tab.non-eseguito { color: var(--ko); }
  .esito-tab.compilazione { color: var(--attenzione); }
  .esito-tab.vecchio, .esito-tab.in-corso { color: var(--tenue); font-weight: 400; }
  #traccia { flex: 1; min-height: 0; overflow-y: auto; background: var(--pannello);
             border: 1px solid var(--bordo); border-radius: 0 8px 8px 8px; padding: 18px 22px; }
  h1 { font-size: 19px; line-height: 1.3; margin: 0 0 14px; }
  h2 { font-size: 13px; margin: 20px 0 8px; color: var(--tenue);
       text-transform: uppercase; letter-spacing: .6px; }
  h3 { font-size: 14px; margin: 16px 0 6px; }
  pre { background: var(--codice); border: 1px solid var(--bordo); border-radius: 6px;
        padding: 12px 14px; overflow-x: auto; }
  code { font-family: var(--mono); font-size: 13px; }
  p code, li code { background: var(--codice); padding: 1px 5px; border-radius: 4px; }
  ol { padding-left: 22px; } li { margin-bottom: 6px; }
  li p { margin: 6px 0 0; }
  .trattino { margin-left: 14px; }

  .barra { display: flex; align-items: center; gap: 12px; flex: none; min-height: 42px;
           margin-bottom: 8px; }
  .barra h2 { margin: 0; }
  #salvataggio { color: var(--tenue); font-size: 12px; }
  #salvataggio.sporco { color: var(--attenzione); }
  .contatore { color: var(--tenue); font-size: 13px; white-space: nowrap;
               font-variant-numeric: tabular-nums; }
  .contatore b { color: var(--testo); font-weight: 600; }
  .contatore b.ultima { color: var(--attenzione); }
  .contatore b.oltre { color: var(--ko); }
  button.azione { padding: 7px 14px; border-radius: 8px; font-weight: 600; cursor: pointer;
                  background: transparent; color: var(--tenue); border: 1px solid var(--bordo); }
  button.azione:not(:disabled):hover { color: var(--testo); border-color: var(--tenue); }
  button.azione:disabled { opacity: .4; cursor: not-allowed; }
  #esegui { background: var(--accento); color: #10131a; border-color: var(--accento);
            white-space: nowrap; min-width: 176px; }
  #esegui.penalita { background: var(--attenzione); border-color: var(--attenzione); }
  #esegui:not(:disabled):hover { color: #10131a; border-color: #fff; }
  #esegui kbd { font: 12px var(--mono); opacity: .75; margin-left: 6px; }
  #pausa.attiva { color: var(--attenzione); border-color: var(--attenzione); }
  .avviso { color: var(--attenzione); font-size: 12.5px; }
  .riga-avviso { display: flex; justify-content: space-between; gap: 16px; flex: none;
                 min-height: 19px; margin: -4px 0 6px; }
  #avviso { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .aiuto { color: var(--tenue); font-size: 12px; white-space: nowrap; }

  /* Textarea trasparente sopra un <pre> colorato: stessi font, rientri e
     a capo, cosi' il testo colorato cade esattamente sotto il cursore. */
  .editor { --margine: 46px; position: relative; flex: 1 1 0; min-height: 200px;
            overflow: hidden; background: var(--codice); border: 1px solid var(--bordo);
            border-radius: 6px; }
  .editor:focus-within { border-color: var(--accento); }
  .editor pre, .editor textarea, .editor .numeri div {
    margin: 0; border: 0; padding: 12px 14px; tab-size: 4; white-space: pre;
    font: 13.5px/1.55 var(--mono); letter-spacing: 0; }
  .editor .numeri { position: absolute; top: 0; left: 0; bottom: 0; width: var(--margine);
                    overflow: hidden; z-index: 1; background: #0c0e11;
                    border-right: 1px solid var(--bordo); user-select: none; }
  .editor .numeri div { padding: 12px 9px 12px 0; text-align: right; color: #7a8294; }
  .editor pre { position: absolute; top: 0; left: var(--margine);
                min-width: calc(100% - var(--margine)); min-height: 100%;
                background: none; border-radius: 0; overflow: visible;
                pointer-events: none; color: var(--testo); }
  .editor textarea { position: absolute; top: 0; left: var(--margine); visibility: hidden;
                     width: calc(100% - var(--margine)); height: 100%; resize: none;
                     background: transparent; color: transparent; caret-color: var(--testo);
                     outline: none; overflow: auto; }
  .editor textarea.attiva { visibility: visible; }
  .editor textarea::selection { background: rgba(110, 168, 254, .35); }
  .editor textarea[readonly] { cursor: default; }
  .editor code { font: inherit; }
  .j-kw { color: #c792ea; } .j-tipo { color: #82aaff; } .j-str { color: #c3e88d; }
  .j-num { color: #f78c6c; } .j-ann { color: #ffcb6b; }
  .j-com { color: #8089a0; font-style: italic; }

  #esito { display: flex; flex-direction: column; flex: 0 1 auto; max-height: 45%; min-height: 0;
           margin-top: 10px; border-radius: 6px; border: 1px solid var(--bordo);
           background: var(--codice); }
  #esito[hidden] { display: none; }
  .esito-testa { display: flex; align-items: center; justify-content: space-between; gap: 12px;
                 flex: none; padding: 9px 14px; }
  #riduci { background: none; border: none; padding: 3px 6px; min-height: 24px; color: var(--tenue);
            font-size: 12.5px; cursor: pointer; }
  #riduci:hover { color: var(--testo); }
  .esito-corpo { flex: 1; min-height: 0; overflow-y: auto; padding: 0 14px 12px; }
  #esito.ridotto .esito-corpo { display: none; }
  #esito .verdetto { font-weight: 700; letter-spacing: .4px; }
  #esito.superato .verdetto { color: var(--ok); }
  #esito.fallito .verdetto, #esito.blocco .verdetto,
  #esito.non-eseguito .verdetto { color: var(--ko); }
  #esito.compilazione .verdetto { color: var(--attenzione); }
  #esito.vecchio .verdetto, #esito.in-corso .verdetto { color: var(--tenue); }
  #esito.in-corso .esito-corpo { opacity: .5; }
  #esito .nota { color: var(--tenue); font-size: 12.5px; }
  #esito pre { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; }
  #esito pre.errore-compilatore { border-color: var(--attenzione); background: #19150f; }
  #esito pre.errore-compilatore code { font-size: 13.5px; line-height: 1.65; color: #ffd08a; }
  .verifica { border-top: 1px solid var(--bordo); padding: 8px 0 7px; font-size: 13px; }
  .verifica:first-of-type { border-top: none; padding-top: 0; }
  .verifica .segno { font-weight: 700; margin-right: 7px; }
  .verifica.passata .segno { color: var(--ok); }
  .verifica.persa .segno { color: var(--ko); }
  .verifica.persa .nome { color: var(--testo); }
  .verifica .nome { color: var(--tenue); }
  .confronto { margin: 7px 0 0 22px; font-family: var(--mono); font-size: 12px; }
  .confronto div { display: flex; gap: 8px; padding: 2px 0; }
  .confronto .etichetta { color: var(--tenue); min-width: 66px; }
  .confronto .valore { color: var(--testo); overflow-wrap: anywhere; white-space: pre-wrap; }
  .confronto .valore.perso { color: var(--ko); }

  @media (max-width: 900px) {
    html, body { height: auto; }
    body { display: block; overflow: visible; }
    header { position: sticky; top: 0; z-index: 5; flex-wrap: wrap; }
    main { display: block; }
    #chiusura { flex-direction: column; }
    #traccia { max-height: 40vh; }
    .barra { flex-wrap: wrap; margin-top: 14px; }
    .editor { height: 60vh; flex: none; }
    #esito { max-height: none; }
  }
</style>
</head>
<body>
<header>
  <span class="titolo">__NOME__</span>
  <span class="spazio"></span>
  <span id="stato-consegna" class="avviso"></span>
  <button class="azione" id="pausa">Pausa</button>
  <button class="azione" id="consegna">Consegna</button>
  <div id="cronometro" role="timer" aria-label="Tempo rimanente">--:--</div>
</header>

<section id="chiusura" tabindex="-1" hidden aria-label="Prova chiusa"></section>

<main>
  <div class="colonna">
    <nav class="tab" id="tab" aria-label="Esercizi"></nav>
    <section id="traccia" tabindex="0" aria-label="Traccia"></section>
  </div>
  <section class="lavoro" aria-label="Risposta">
    <div class="barra">
      <h2>Risposta — Soluzione.java</h2>
      <span id="salvataggio"></span>
      <span class="spazio"></span>
      <span class="contatore">Esecuzioni <b id="es-conta">0 / 5</b></span>
      <button class="azione" id="esegui" title="Esegui (Cmd+Invio)"><span
        id="esegui-testo">Esegui</span><kbd aria-hidden="true">⌘↵</kbd></button>
    </div>
    <div class="riga-avviso">
      <span class="avviso" id="avviso" aria-live="polite"></span>
      <span class="aiuto">Esc esce dall'editor</span>
    </div>
    <div class="editor" tabindex="-1">
      <div class="numeri" aria-hidden="true"><div id="numeri">1</div></div>
      <pre aria-hidden="true"><code id="colorato"></code></pre>
      <textarea wrap="off" spellcheck="false" autocomplete="off" readonly
                autocorrect="off" autocapitalize="off"></textarea>
    </div>
    <div id="esito" hidden></div>
  </section>
</main>
<div class="sr" id="annuncio" role="status"></div>

<script>
const ESERCIZI = __ESERCIZI__;
const TRACCE = __TRACCE__;
const TIMEOUT = __TIMEOUT__;
let corrente = "ES1";
let stato = null;
let ricevuto = 0;   // performance.now() dell'ultimo stato arrivato dal server
let scollegato = false;
let inEsecuzione = false;
let chiusa = false;
let sogliaAnnunciata = Infinity;
const esiti = {};   // ultimo verdetto per esercizio: non deve seguire il cambio di tab
const codici = {};  // testo di ogni Soluzione.java come si trova nell'editor
const daSalvare = {};   // autosalvataggi in attesa, per esercizio
const aree = {};    // una textarea per esercizio: tiene da sola cursore, scroll e Cmd+Z
let area = null;
let caricato = false;
const colorato = document.getElementById("colorato");
const numeri = document.getElementById("numeri");
let righe = 1;

const TOKEN = /(\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$))|("(?:[^"\\\n]|\\.)*"?|'(?:[^'\\\n]|\\.)*'?)|(@\w+)|\b(\d[\w.]*)|\b(abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|record|return|short|static|super|switch|synchronized|this|throw|throws|transient|try|var|void|volatile|while|yield|true|false|null)\b|\b([A-Z]\w*)/g;
const CLASSI = [null, "j-com", "j-str", "j-ann", "j-num", "j-kw", "j-tipo"];
const ETICHETTE = {
  SUPERATO: ["superato", "TEST SUPERATO", "Tutte le verifiche sono passate."],
  FALLITO: ["fallito", "TEST FALLITO", "Almeno una verifica non è passata."],
  COMPILAZIONE: ["compilazione", "ERRORE DI COMPILAZIONE", "Esecuzione consumata comunque."],
  BLOCCO: ["blocco", "ESECUZIONE INTERROTTA", "Esecuzione consumata comunque."]
};
const BREVE = {
  superato: ["✓", "ok"], fallito: ["✗", "ko"], compilazione: ["!", "errore"],
  blocco: ["!", "blocco"], "non-eseguito": ["!", "errore"], "in-corso": ["…", "in corso"]
};
const COPPIE = {"(": ")", "[": "]", "{": "}"};

function colora(testo) {
  let fuori = "", ultimo = 0, m;
  TOKEN.lastIndex = 0;
  while ((m = TOKEN.exec(testo)) !== null) {
    const gruppo = m.findIndex((g, i) => i > 0 && g !== undefined);
    fuori += fuggi(testo.slice(ultimo, m.index))
      + '<span class="' + CLASSI[gruppo] + '">' + fuggi(m[0]) + '</span>';
    ultimo = TOKEN.lastIndex;
  }
  return fuori + fuggi(testo.slice(ultimo));
}

function allinea() {
  colorato.parentElement.style.transform =
    "translate(" + (-area.scrollLeft) + "px," + (-area.scrollTop) + "px)";
  numeri.style.transform = "translateY(" + (-area.scrollTop) + "px)";
}

function ridisegnaCodice() {
  colorato.innerHTML = colora(area.value) + "\n";
  const n = area.value.split("\n").length;   // wrap="off": una riga logica = una riga a schermo
  if (n !== righe) {
    righe = n;
    numeri.textContent = Array.from({length: n}, (_, i) => i + 1).join("\n");
  }
  allinea();
}

function mostraCodice() {
  area = aree[corrente];
  for (const es of ESERCIZI) aree[es].classList.toggle("attiva", es === corrente);
  ridisegnaCodice();
}

// Il riquadro dell'esito accorcia l'editor: il cursore non deve finire fuori vista.
function mostraCursore() {
  const riga = area.value.slice(0, area.selectionStart).split("\n").length - 1;
  const alta = parseFloat(getComputedStyle(area).lineHeight);
  const y = 12 + riga * alta;
  if (y < area.scrollTop) area.scrollTop = y - alta;
  else if (y + 2 * alta > area.scrollTop + area.clientHeight) {
    area.scrollTop = y + 2 * alta - area.clientHeight;
  }
}

function segnaSalvataggio(testo, sporco) {
  const s = document.getElementById("salvataggio");
  s.textContent = testo;
  s.className = sporco ? "sporco" : "";
}

function programmaSalvataggio(es, attesa) {
  clearTimeout(daSalvare[es]);
  segnaSalvataggio("modifiche non salvate", false);
  daSalvare[es] = setTimeout(() => salvaCodice(es), attesa);
}

async function salvaCodice(es) {
  clearTimeout(daSalvare[es]);
  delete daSalvare[es];
  try {
    const r = await fetch("/api/salva", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({es: es, codice: codici[es]})
    });
    const d = await r.json();
    if (d.errore) segnaSalvataggio(d.errore, true);
    else if (!Object.keys(daSalvare).length) segnaSalvataggio("salvato", false);
  } catch (e) {
    programmaSalvataggio(es, 3000);
    segnaSalvataggio("server non raggiungibile: nuovo tentativo…", true);
  }
}

async function salvaTutto() {
  for (const es of Object.keys(daSalvare)) await salvaCodice(es);
}

function esitoVecchio(es) {
  const r = esiti[es];
  return !!r && typeof r.codice === "string" && r.codice !== codici[es];
}

function alCambio() {
  const eraVecchio = esitoVecchio(corrente);
  codici[corrente] = area.value;
  ridisegnaCodice();
  programmaSalvataggio(corrente, 700);
  if (esitoVecchio(corrente) !== eraVecchio) { mostraEsito(); aggiornaTab(); }
  aggiornaPannello();
}

// Rientra le righe toccate dalla selezione, o toglie il rientro: mai cancella il testo scelto.
function rientra(indietro) {
  const inizio = area.selectionStart, fine = area.selectionEnd, testo = area.value;
  const da = testo.slice(0, inizio).lastIndexOf("\n") + 1;
  // Una selezione che finisce a colonna 0 non comprende quella riga.
  const ultimo = fine > inizio && testo[fine - 1] === "\n" ? fine - 1 : fine;
  const a = testo.indexOf("\n", ultimo) < 0 ? testo.length : testo.indexOf("\n", ultimo);
  const prima = testo.slice(da, a);
  const nuovo = prima.split("\n").map(r =>
    indietro ? r.replace(/^( {1,4}|\t)/, "") : (r ? "    " + r : r)).join("\n");
  if (nuovo === prima) return;
  area.setSelectionRange(da, a);
  document.execCommand("insertText", false, nuovo);
  if (inizio === fine) {
    const cursore = Math.max(da, inizio + nuovo.length - prima.length);
    area.setSelectionRange(cursore, cursore);
  } else {
    area.setSelectionRange(da, da + nuovo.length);
  }
}

// Niente esclusione di altKey: sulla tastiera italiana [ e { si scrivono con Option.
function alTasto(e) {
  if (e.key === "Escape") {     // Tab scrive nel codice: da qui si esce, su una cornice inerte
    document.querySelector(".editor").focus();
    return;
  }
  if (area.readOnly || e.metaKey || e.ctrlKey || e.isComposing) return;
  const inizio = area.selectionStart, fine = area.selectionEnd;
  const dopo = area.value[inizio];
  if (e.key === "Tab") {
    e.preventDefault();
    if (e.shiftKey || inizio !== fine) rientra(e.shiftKey);
    else document.execCommand("insertText", false, "    ");   // a differenza di setRangeText, resta annullabile
  } else if (COPPIE[e.key]) {
    e.preventDefault();
    const scelto = area.value.slice(inizio, fine);   // con una selezione, la racchiude
    document.execCommand("insertText", false, e.key + scelto + COPPIE[e.key]);
    area.setSelectionRange(inizio + 1, inizio + 1 + scelto.length);
  } else if (")]}".includes(e.key) && inizio === fine && dopo === e.key) {
    e.preventDefault();   // la chiusa c'e' gia': la si scavalca invece di duplicarla
    area.setSelectionRange(inizio + 1, inizio + 1);
  } else if (e.key === "Backspace" && inizio === fine && inizio > 0
             && COPPIE[area.value[inizio - 1]] === dopo) {
    e.preventDefault();   // coppia vuota: si cancellano entrambe
    area.setSelectionRange(inizio - 1, inizio + 1);
    document.execCommand("delete");
  } else if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    const rigaAttuale = area.value.slice(area.value.slice(0, inizio).lastIndexOf("\n") + 1, inizio);
    const rientro = rigaAttuale.match(/^[ \t]*/)[0];
    const aperta = area.value[inizio - 1] === "{";
    const dentro = "\n" + rientro + (aperta ? "    " : "");
    if (aperta && dopo === "}" && inizio === fine) {    // apre il blocco su tre righe
      document.execCommand("insertText", false, dentro + "\n" + rientro);
      area.setSelectionRange(inizio + dentro.length, inizio + dentro.length);
    } else {
      document.execCommand("insertText", false, dentro);
    }
  }
}

function creaAree() {
  const modello = document.querySelector(".editor textarea");
  for (const es of ESERCIZI) {
    const t = es === ESERCIZI[0] ? modello : modello.cloneNode();
    if (t !== modello) modello.parentNode.appendChild(t);
    t.setAttribute("aria-label", "Codice di " + es + ". Esc per uscire dall'editor.");
    t.addEventListener("scroll", allinea);
    t.addEventListener("input", alCambio);
    t.addEventListener("keydown", alTasto);
    aree[es] = t;
  }
}

// La cornice contiene la textarea: senza questo, Tab dopo Esc rientrerebbe nell'editor.
document.querySelector(".editor").addEventListener("keydown", e => {
  const dopo = document.querySelector("#riduci, .esito-corpo");
  if (e.target === e.currentTarget && e.key === "Tab" && !e.shiftKey && dopo) {
    e.preventDefault();
    dopo.focus();
  }
});

document.addEventListener("keydown", e => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
    e.preventDefault();
    document.getElementById("esegui").click();
  }
});

// Chiusura o ricarica della scheda con un salvataggio ancora in attesa.
window.addEventListener("pagehide", () => {
  for (const es of Object.keys(daSalvare)) {
    navigator.sendBeacon("/api/salva", JSON.stringify({es: es, codice: codici[es]}));
  }
});

function creaTab() {
  const tab = document.getElementById("tab");
  for (const es of ESERCIZI) {
    const b = document.createElement("button");
    b.id = "tab-" + es;
    b.innerHTML = es + '<span class="esito-tab" id="esito-' + es + '"></span>'
      + '<span class="conta" id="conta-' + es + '">0/5</span>';
    b.onclick = () => {
      corrente = es;
      aggiornaTab(); disegnaTraccia(); mostraCodice(); aggiornaPannello(); mostraEsito();
      mostraCursore();
      if (!area.readOnly) area.focus({preventScroll: true});
    };
    tab.appendChild(b);
  }
}

function aggiornaTab() {
  for (const es of ESERCIZI) {
    const b = document.getElementById("tab-" + es);
    b.className = es === corrente ? "attivo" : "";
    b.setAttribute("aria-current", es === corrente);
    const r = esiti[es], breve = r && BREVE[r.classe], vecchio = esitoVecchio(es);
    const segnale = document.getElementById("esito-" + es);
    segnale.textContent = breve ? (vecchio ? "~" : breve[0]) + " " + breve[1] : "";
    segnale.className = "esito-tab " + (vecchio ? "vecchio" : (r ? r.classe : ""));
    if (stato) {
      const n = stato.esecuzioni[es];
      document.getElementById("conta-" + es).textContent = n + "/5";
      b.setAttribute("aria-label", es + ", " + n + (n === 1 ? " esecuzione" : " esecuzioni") + " su 5"
        + (breve ? ", ultimo esito " + breve[1] : "")
        + (vecchio ? ", codice modificato dopo" : ""));
    }
  }
}

function disegnaTraccia() {
  document.getElementById("traccia").innerHTML = TRACCE[corrente];
}

function fuggi(testo) {
  return String(testo).replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]));
}

function mostraEsito() {
  const esito = document.getElementById("esito");
  const r = esiti[corrente];
  esito.hidden = !r;
  if (!r) return;
  const vecchio = esitoVecchio(corrente);
  esito.className = r.classe + (r.ridotto ? " ridotto" : "") + (vecchio ? " vecchio" : "");
  esito.innerHTML = '<div class="esito-testa"><div><div class="verdetto">' + r.titolo
    + (vecchio ? ' · codice modificato dopo questa esecuzione' : '') + '</div>'
    + '<div class="nota">' + r.nota + '</div></div>'
    + (r.corpo ? '<button id="riduci" aria-expanded="' + !r.ridotto + '">'
       + (r.ridotto ? "Espandi" : "Riduci") + '</button>' : '')
    + '</div><div class="esito-corpo" tabindex="0">' + r.corpo + '</div>';
}

document.getElementById("esito").addEventListener("click", e => {
  if (e.target.id !== "riduci") return;
  esiti[corrente].ridotto = !esiti[corrente].ridotto;
  mostraEsito();
  document.getElementById("riduci").focus();
  mostraCursore();
});

function dettaglioEsito(d) {
  let corpo = "";
  if (d.errori_compilatore) {
    corpo += '<pre class="errore-compilatore"><code>' + fuggi(d.errori_compilatore) + '</code></pre>';
  }
  for (const v of (d.verifiche || [])) {
    corpo += '<div class="verifica ' + (v.superata ? 'passata' : 'persa') + '">'
      + '<span class="segno" role="img" aria-label="' + (v.superata ? 'superata' : 'non superata')
      + '">' + (v.superata ? '✓' : '✗') + '</span>'
      + '<span class="nome">' + fuggi(v.nome) + '</span>';
    if (!v.superata && (v.atteso !== null || v.ottenuto !== null)) {
      corpo += '<div class="confronto">'
        + '<div><span class="etichetta">atteso</span>'
        + '<span class="valore">' + fuggi(v.atteso || '—') + '</span></div>'
        + '<div><span class="etichetta">ottenuto</span>'
        + '<span class="valore perso">' + fuggi(v.ottenuto || '—') + '</span></div>'
        + '</div>';
    }
    corpo += '</div>';
  }
  if (d.uscita) {
    corpo += '<pre><code>' + fuggi(d.uscita) + '</code></pre>';
  }
  return corpo;
}

function registraEsito(es, d) {
  if (d.errore) {
    esiti[es] = {classe: "non-eseguito", titolo: "NON ESEGUITO", nota: d.errore, corpo: ""};
    return;
  }
  const [classe, titolo, frase] = ETICHETTE[d.esito];
  esiti[es] = {classe: classe, titolo: titolo, corpo: dettaglioEsito(d), codice: d.codice,
    ridotto: d.esito === "SUPERATO",
    nota: es + " · " + frase + " Esecuzione " + d.n
      + (d.oltre_limite ? " oltre il limite: penalità." : " di 5.")};
}

function aggiornaPannello() {
  if (!stato) return;
  const n = stato.esecuzioni[corrente];
  const conta = document.getElementById("es-conta");
  conta.textContent = n + " / 5";
  conta.className = n >= 5 ? "oltre" : (n === 4 ? "ultima" : "");
  const bloccato = stato.consegnato || stato.scaduto || stato.in_pausa;
  const esegui = document.getElementById("esegui");
  esegui.disabled = bloccato || inEsecuzione;
  esegui.classList.toggle("penalita", n >= 5);
  document.getElementById("esegui-testo").textContent = inEsecuzione
    ? (stato.fase === "esecuzione" ? "Esecuzione…" : "Compilazione…")
    : (n >= 5 ? "Esegui (penalità)" : "Esegui");
  for (const t of Object.values(aree)) t.readOnly = bloccato || !caricato;
  document.getElementById("consegna").disabled = stato.consegnato || inEsecuzione;
  const pausa = document.getElementById("pausa");
  pausa.disabled = stato.consegnato;
  pausa.textContent = stato.in_pausa ? "Riprendi" : "Pausa";
  pausa.className = "azione" + (stato.in_pausa ? " attiva" : "");
  let testo = "";
  if (stato.in_pausa) {
    testo = "Prova in pausa: cronometro fermo, esecuzioni sospese.";
  } else if (stato.scaduto && !stato.consegnato) {
    testo = "Tempo scaduto: la prova si chiude al termine dell'esecuzione.";
  } else if (!bloccato) {
    if (n >= 5) testo = "Limite raggiunto: ogni ulteriore esecuzione è una penalità.";
    else if (n === 4) testo = "Ultima esecuzione senza penalità.";
    const r = esiti[corrente];
    if (r && r.codice === codici[corrente]) {
      testo += (testo ? " " : "") + "Codice invariato dall'ultima esecuzione.";
    }
  }
  const avviso = document.getElementById("avviso");
  if (avviso.textContent !== testo) avviso.textContent = testo;    // o la regione live ripete
}

function mmss(secondi) {
  const s = Math.floor(secondi);
  return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
}

// Conta da solo fra un poll e l'altro: il tempo non dipende dalla risposta del server.
function rimanenteOra() {
  const fermo = stato.consegnato || stato.in_pausa;
  return fermo ? stato.rimanente : stato.rimanente - (performance.now() - ricevuto) / 1000;
}

function annuncia(testo) {
  document.getElementById("annuncio").textContent = testo;
}

function aggiornaCronometro() {
  const c = document.getElementById("cronometro");
  const r = Math.max(0, Math.floor(rimanenteOra()));
  c.textContent = mmss(r);
  c.className = stato.consegnato ? (r === 0 ? "scaduto" : "pausa")
      : (stato.in_pausa ? "pausa" : (r <= 60 ? "scaduto" : (r <= 300 ? "allarme" : "")));
  for (const soglia of [300, 60]) {
    if (r > 0 && r <= soglia && soglia < sogliaAnnunciata && !stato.consegnato) {
      sogliaAnnunciata = soglia;
      annuncia(soglia === 60 ? "Resta 1 minuto." : "Restano 5 minuti.");
    }
  }
  document.getElementById("stato-consegna").textContent = scollegato
    ? "Server non raggiungibile: il codice resta nell'editor."
    : (stato.in_pausa ? "IN PAUSA" : "");
}

function mostraChiusura() {
  chiusa = true;
  const motivo = stato.motivo_consegna === "tempo scaduto" ? "Tempo scaduto" : "Consegna manuale";
  const righe = ESERCIZI.map(es => {
    const r = esiti[es];
    return '<tr><th scope="row">' + es + '</th><td>' + stato.esecuzioni[es] + ' / 5</td><td>'
      + (r ? r.titolo + (esitoVecchio(es) ? ' (codice modificato dopo)' : '') : 'Mai eseguito')
      + '</td></tr>';
  }).join("");
  const p = document.getElementById("chiusura");
  p.innerHTML = '<div><h2>Prova chiusa</h2>'
    + '<p>' + motivo + ' · tempo usato ' + mmss(stato.trascorso) + ' su '
    + mmss(stato.trascorso + stato.rimanente) + '</p>'
    + '<p class="percorso">' + fuggi(stato.report) + '</p></div>'
    + '<table><thead><tr><th scope="col">Esercizio</th><th scope="col">Esecuzioni</th>'
    + '<th scope="col">Ultimo esito</th></tr></thead><tbody>' + righe + '</tbody></table>';
  p.hidden = false;
  p.focus({preventScroll: true});
  annuncia("Prova chiusa. " + motivo + ". Report generato.");
}

async function poll() {
  try {
    const r = await fetch("/api/stato");
    stato = await r.json();
    ricevuto = performance.now();
    scollegato = false;
  } catch (e) {
    scollegato = true;
  }
  if (!stato) return;
  aggiornaCronometro();
  aggiornaPannello();
  aggiornaTab();
  if (stato.consegnato && !chiusa && !inEsecuzione && caricato) mostraChiusura();
}

async function lancia(es) {
  // Il codice viaggia con la richiesta: si compila esattamente cio' che e' nell'editor.
  clearTimeout(daSalvare[es]);
  delete daSalvare[es];
  try {
    const r = await fetch("/api/esegui", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({es: es, codice: codici[es]})
    });
    return await r.json();
  } catch (e) {
    return {errore: "Server non raggiungibile: esecuzione non completata."};
  }
}

document.getElementById("esegui").onclick = async () => {
  if (document.getElementById("esegui").disabled) return;
  const lanciato = corrente;
  const prima = esiti[lanciato] || {corpo: "", ridotto: false};
  inEsecuzione = true;
  // Il dettaglio precedente resta, attenuato: l'editor non salta a ogni esecuzione.
  esiti[lanciato] = {classe: "in-corso", titolo: "IN CORSO…", corpo: prima.corpo,
    ridotto: prima.ridotto, nota: lanciato + " · si interrompe da sola dopo " + TIMEOUT + " secondi."};
  aggiornaPannello();
  aggiornaTab();
  mostraEsito();
  const d = await lancia(lanciato);
  inEsecuzione = false;
  if (!d.errore && !Object.keys(daSalvare).length) segnaSalvataggio("salvato", false);
  registraEsito(lanciato, d);
  annuncia(lanciato + ": " + esiti[lanciato].titolo + "."
    + (d.n ? " Esecuzione " + d.n + (d.oltre_limite ? ", oltre il limite: penalità." : " di 5.") : ""));
  mostraEsito();
  await poll();
  if (corrente === lanciato && !area.readOnly) {
    area.focus({preventScroll: true});
    mostraCursore();
  }
};

document.getElementById("pausa").onclick = async () => {
  await salvaTutto();
  await fetch("/api/pausa", {method: "POST"});
  await poll();
  if (!stato.in_pausa && !area.readOnly) area.focus({preventScroll: true});
};

document.getElementById("consegna").onclick = async () => {
  const mai = ESERCIZI.filter(es => stato.esecuzioni[es] === 0);
  if (!confirm("Consegnare adesso? Restano " + mmss(Math.max(0, rimanenteOra())) + " minuti."
      + (mai.length ? " Mai eseguiti: " + mai.join(", ") + "." : "")
      + " Le esecuzioni si chiudono e viene generato il report.")) return;
  await salvaTutto();
  await fetch("/api/consegna", {method: "POST"});
  await poll();
};

async function caricaDati() {
  const [codice, ultimi] = await Promise.all([fetch("/api/codice"), fetch("/api/esiti")]);
  Object.assign(codici, await codice.json());
  const verdetti = await ultimi.json();
  for (const es of ESERCIZI) {
    aree[es].value = codici[es];
    if (verdetti[es]) registraEsito(es, verdetti[es]);
  }
  caricato = true;
  mostraCodice();
  mostraEsito();
  await poll();
}

creaTab();
creaAree();
mostraCodice();
aggiornaTab();
disegnaTraccia();
caricaDati();
setInterval(poll, 1000);
setInterval(() => { if (stato) aggiornaCronometro(); }, 250);
</script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Server
# --------------------------------------------------------------------------

class Gestore(BaseHTTPRequestHandler):

    prova: Prova = None
    pagina: str = ""
    origini: set = set()

    def log_message(self, formato, *args):
        pass

    def _json(self, dati, codice=200):
        corpo = json.dumps(dati, ensure_ascii=False).encode()
        self.send_response(codice)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if self.path.startswith("/api/stato"):
            with stato_lock:
                self.controlla_scadenza()
                p = Gestore.prova
                self._json({
                    "rimanente": p.rimanente(),
                    "trascorso": p.trascorso(),
                    "scaduto": p.scaduto(),
                    "in_pausa": p.in_pausa(),
                    "fase": p.fase,
                    "consegnato": p.dati["consegnato"],
                    "motivo_consegna": p.dati["motivo_consegna"],
                    "report": p.dati["report"],
                    "esecuzioni": {e: p.numero_esecuzioni(e) for e in ESERCIZI},
                })
            return
        if self.path == "/api/codice":
            with stato_lock:
                self._json({e: Gestore.prova.leggi_codice(e) for e in ESERCIZI})
            return
        if self.path == "/api/esiti":
            with stato_lock:
                esecuzioni = Gestore.prova.dati["esecuzioni"]
                self._json({e: risposta_esito(esecuzioni[e][-1]) if esecuzioni[e] else None
                            for e in ESERCIZI})
            return
        if self.path in ("/", "/index.html"):
            corpo = Gestore.pagina.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
            return
        self.send_error(404)

    def do_POST(self):
        # Solo la pagina dell'aula: un'altra scheda non deve poter consegnare o consumare esecuzioni.
        origine = self.headers.get("Origin")
        if origine and origine not in Gestore.origini:
            self.send_error(403)
            return
        lunghezza = int(self.headers.get("Content-Length") or 0)
        corpo = self.rfile.read(lunghezza) if lunghezza else b"{}"
        try:
            richiesta = json.loads(corpo or b"{}")
        except json.JSONDecodeError:
            richiesta = {}

        if self.path == "/api/pausa":
            with stato_lock:
                in_pausa = Gestore.prova.commuta_pausa()
            print("  Prova in pausa: cronometro fermo." if in_pausa
                  else "  Prova ripresa: cronometro riavviato.")
            self._json({"in_pausa": in_pausa})
            return

        if self.path == "/api/consegna":
            with stato_lock:
                if Gestore.prova.fase:
                    self._json({"errore": "Esecuzione in corso: consegna al termine."})
                    return
                percorso = Gestore.prova.consegna("consegna manuale")
            print(f"\n  Consegna manuale. Report: {percorso}")
            self._json({"report": os.path.basename(percorso)})
            return

        if self.path == "/api/salva":
            es, codice = richiesta.get("es"), richiesta.get("codice")
            if es not in ESERCIZI or not isinstance(codice, str):
                self._json({"errore": "Richiesta non valida."}, 400)
                return
            with stato_lock:
                self.controlla_scadenza()
                if Gestore.prova.dati["consegnato"]:
                    self._json({"errore": "prova consegnata: modifica non salvata"})
                    return
                Gestore.prova.scrivi_codice(es, codice)
            self._json({"salvato": True})
            return

        if self.path == "/api/esegui":
            es = richiesta.get("es")
            if es not in ESERCIZI:
                self._json({"errore": "Esercizio non valido."}, 400)
                return
            with stato_lock:
                self.controlla_scadenza()
                p = Gestore.prova
                if p.dati["consegnato"]:
                    self._json({"errore": "Prova consegnata: nessuna ulteriore esecuzione."})
                    return
                if p.in_pausa():
                    self._json({"errore": "Prova in pausa: riprendi per eseguire."})
                    return
                if p.fase:
                    self._json({"errore": "Un'esecuzione è già in corso."})
                    return
                p.fase = "compilazione"
                if isinstance(richiesta.get("codice"), str):
                    p.scrivi_codice(es, richiesta["codice"])
            try:
                voce = p.esegui(es)
            finally:
                p.fase = None
            print(f"  {es} — esecuzione {voce['n']}: {voce['esito']}")
            # Come su Moodle: verdetto, elenco delle verifiche con il loro
            # esito e, su quelle fallite, atteso e ottenuto. L'output grezzo
            # viaggia solo per cio' che non e' gia' mostrato altrove.
            self._json(risposta_esito(voce))
            return

        self.send_error(404)

    def controlla_scadenza(self):
        p = Gestore.prova
        if p.in_pausa() or p.fase:     # la run in corso entra nel report: si consegna dopo
            return
        if p.scaduto() and not p.dati["consegnato"]:
            percorso = p.consegna("tempo scaduto")
            print(f"\n  Tempo scaduto: consegna automatica. Report: {percorso}")


# --------------------------------------------------------------------------
# Avvio
# --------------------------------------------------------------------------

def main(argv):
    if len(argv) < 2 or argv[1].startswith("--"):
        print(__doc__)
        return 2

    cartella = Path(argv[1]).resolve()
    durata, porta = 45, 8765
    riparti = "--riparti" in argv
    apri_browser = "--senza-browser" not in argv
    for opzione, converti in (("--durata", int), ("--porta", int)):
        if opzione in argv:
            valore = converti(argv[argv.index(opzione) + 1])
            if opzione == "--durata":
                durata = valore
            else:
                porta = valore

    for es in ESERCIZI:
        for atteso in ("README.md", "Soluzione.java", "Main.class"):
            if not (cartella / es / atteso).exists():
                print(f"Manca {es}/{atteso} in {cartella}", file=sys.stderr)
                return 1

    prova = Prova(cartella, durata, riparti)
    tracce = {es: markdown((cartella / es / "README.md").read_text()) for es in ESERCIZI}

    pagina = (PAGINA
              .replace("__NOME__", html.escape(cartella.name))
              .replace("__ESERCIZI__", json.dumps(ESERCIZI))
              .replace("__TIMEOUT__", str(TIMEOUT_RUN))
              .replace("__TRACCE__", json.dumps(tracce, ensure_ascii=False)))

    Gestore.prova = prova
    Gestore.pagina = pagina
    server = ThreadingHTTPServer(("127.0.0.1", porta), Gestore)
    indirizzo = f"http://127.0.0.1:{porta}"
    Gestore.origini = {indirizzo, f"http://localhost:{porta}"}

    print(f"\n  Aula d'esame — {cartella.name}")
    print(f"  Durata: {durata} minuti · rimanenti ora: {formatta(prova.rimanente())}")
    print(f"  Pagina: {indirizzo}")
    print(f"  Il codice si scrive nella pagina e si salva in {cartella}/ESn/Soluzione.java")
    print("  Ctrl+C per chiudere la finestra senza consegnare.\n")
    if apri_browser:
        webbrowser.open(indirizzo)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Aula chiusa. Lo stato della prova resta in .aula.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
