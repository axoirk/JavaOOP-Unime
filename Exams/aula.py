#!/usr/bin/env python3
"""aula.py — replica in locale la pagina d'esame Moodle per una simulazione.

Apre una finestra del browser con le tre tracce, il cronometro dei
45 minuti complessivi e il pulsante Esegui per esercizio (max 5 esecuzioni, oltre
scatta la penalita'). Il codice si scrive nella pagina stessa, sotto la
traccia, come su Moodle: un editor con la sola colorazione della sintassi
Java (nessun completamento, nessun controllo degli errori). Ogni modifica
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
        (self.cartella / es / "Soluzione.java").write_text(codice)

    def esegui(self, es: str) -> dict:
        cartella_es = self.cartella / es
        n = self.numero_esecuzioni(es) + 1
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
        }
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
        r.append("- **Ambiente:** editor nella pagina, sola colorazione della sintassi "
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
        if in_lista:
            fuori.append("</ol>")
            in_lista = False

        if riga_s.startswith("### "):
            fuori.append(f"<h3>{inline(riga_s[4:])}</h3>")
        elif riga_s.startswith("## "):
            fuori.append(f"<h2>{inline(riga_s[3:])}</h2>")
        elif riga_s.startswith("# "):
            fuori.append(f"<h1>{inline(riga_s[2:])}</h1>")
        elif riga_s.startswith("- "):
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
<title>Aula — __NOME__</title>
<style>
  :root {
    --sfondo: #14161a; --pannello: #1b1e24; --bordo: #2c313a;
    --testo: #e6e8ec; --tenue: #9aa2b1; --accento: #6ea8fe;
    --ok: #5fd08a; --ko: #ff6b6b; --attenzione: #ffb454;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--sfondo); color: var(--testo);
         font: 14px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
  header { display: flex; align-items: center; gap: 18px; padding: 10px 18px;
           background: var(--pannello); border-bottom: 1px solid var(--bordo);
           position: sticky; top: 0; z-index: 5; }
  header .titolo { font-weight: 600; letter-spacing: .2px; }
  header .spazio { flex: 1; }
  #cronometro { font: 600 22px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
                padding: 6px 12px; border: 1px solid var(--bordo); border-radius: 8px; }
  #cronometro.allarme { color: var(--attenzione); border-color: var(--attenzione); }
  #cronometro.scaduto { color: var(--ko); border-color: var(--ko); }
  .tab { display: flex; gap: 6px; padding: 10px 18px 0; }
  .tab button { background: transparent; color: var(--tenue); border: 1px solid transparent;
                border-bottom: none; padding: 8px 16px; border-radius: 8px 8px 0 0;
                font-size: 14px; cursor: pointer; }
  .tab button.attivo { background: var(--pannello); color: var(--testo);
                       border-color: var(--bordo); }
  .tab button .conta { color: var(--tenue); font-size: 12px; margin-left: 8px; }
  main { display: grid; grid-template-columns: 1fr 440px; gap: 16px;
         padding: 0 18px 18px; align-items: start; }
  .riquadro { background: var(--pannello); border: 1px solid var(--bordo);
              border-radius: 0 8px 8px 8px; padding: 18px 22px; }
  .laterale { border-radius: 8px; position: sticky; top: 74px; }
  h1 { font-size: 19px; margin: 0 0 14px; }
  h2 { font-size: 15px; margin: 20px 0 8px; color: var(--tenue);
       text-transform: uppercase; letter-spacing: .6px; }
  pre { background: #0f1115; border: 1px solid var(--bordo); border-radius: 6px;
        padding: 12px 14px; overflow-x: auto; }
  code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }
  p code { background: #0f1115; padding: 1px 5px; border-radius: 4px; }
  ol { padding-left: 22px; } li { margin-bottom: 6px; }
  .trattino { margin-left: 14px; }
  button.azione { width: 100%; padding: 11px; border-radius: 8px; border: none;
                  font-size: 14px; font-weight: 600; cursor: pointer; }
  #esegui { background: var(--accento); color: #10131a; }
  #esegui:disabled, #consegna:disabled { opacity: .4; cursor: not-allowed; }
  #pausa, #consegna { background: transparent; color: var(--tenue);
              border: 1px solid var(--bordo); margin-top: 10px; }
  #pausa.attiva { color: var(--attenzione); border-color: var(--attenzione); }
  #cronometro.pausa { color: var(--tenue); border-style: dashed; }
  .riga { display: flex; justify-content: space-between; color: var(--tenue);
          font-size: 13px; padding: 3px 0; }
  .riga b { color: var(--testo); font-weight: 600; }
  #esito { margin-top: 14px; border-radius: 6px; padding: 12px 14px;
           border: 1px solid var(--bordo); background: #0f1115; }
  #esito .verdetto { font-weight: 700; letter-spacing: .4px; }
  #esito.superato .verdetto { color: var(--ok); }
  #esito.fallito .verdetto, #esito.blocco .verdetto { color: var(--ko); }
  #esito.compilazione .verdetto { color: var(--attenzione); }
  #esito .nota { color: var(--tenue); font-size: 12.5px; margin-top: 6px; }
  #esito pre { margin: 10px 0 0; max-height: 220px; }
  #esito pre.errore-compilatore { max-height: 420px; border-color: var(--ko);
    background: #1a1214; }
  #esito pre.errore-compilatore code { font-size: 13.5px; line-height: 1.65;
    color: #ff9d9d; }
  .verifica { border-top: 1px solid var(--bordo); padding: 8px 0 7px; font-size: 13px; }
  .verifica:first-of-type { border-top: none; margin-top: 6px; }
  .verifica .segno { font-weight: 700; margin-right: 7px; }
  .verifica.passata .segno { color: var(--ok); }
  .verifica.persa .segno { color: var(--ko); }
  .verifica.persa .nome { color: var(--testo); }
  .verifica .nome { color: var(--tenue); }
  .confronto { margin: 7px 0 0 22px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
               font-size: 12px; }
  .confronto div { display: flex; gap: 8px; padding: 2px 0; }
  .confronto .etichetta { color: var(--tenue); min-width: 66px; }
  .confronto .valore { color: var(--testo); word-break: break-all; white-space: pre-wrap; }
  .confronto .valore.perso { color: var(--ko); }
  .avviso { color: var(--attenzione); font-size: 12.5px; margin-top: 10px; }
  .colonna { display: flex; flex-direction: column; gap: 16px; min-width: 0; }
  .editor-testa { display: flex; justify-content: space-between; align-items: baseline;
                  margin-bottom: 8px; }
  .editor-testa h2 { margin: 0; }
  #salvataggio { color: var(--tenue); font-size: 12px; }
  #salvataggio.sporco { color: var(--attenzione); }
  /* Textarea trasparente sopra un <pre> colorato: stessi font, rientri e
     a capo, cosi' il testo colorato cade esattamente sotto il cursore. */
  .editor { position: relative; height: 62vh; min-height: 260px; resize: vertical;
            overflow: hidden; background: #0f1115; border: 1px solid var(--bordo);
            border-radius: 6px; }
  .editor { --margine: 46px; }
  .editor pre, .editor textarea, .editor .numeri div {
    margin: 0; border: 0; padding: 12px 14px; tab-size: 4; white-space: pre;
    font: 13.5px/1.55 ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: 0; }
  .editor .numeri { position: absolute; top: 0; left: 0; bottom: 0; width: var(--margine);
                    overflow: hidden; z-index: 1; background: #0c0e11;
                    border-right: 1px solid var(--bordo); user-select: none; }
  .editor .numeri div { padding: 12px 9px 12px 0; text-align: right; color: #4b5263; }
  .editor pre { position: absolute; top: 0; left: var(--margine);
                min-width: calc(100% - var(--margine)); min-height: 100%;
                background: none; border-radius: 0; overflow: visible;
                pointer-events: none; color: var(--testo); }
  .editor textarea { position: absolute; top: 0; left: var(--margine);
                     width: calc(100% - var(--margine)); height: 100%; resize: none;
                     background: transparent; color: transparent; caret-color: var(--testo);
                     outline: none; overflow: auto; }
  .editor textarea::selection { background: rgba(110, 168, 254, .35); }
  .editor textarea[readonly] { cursor: default; }
  .editor code { font: inherit; }
  .colonna .riquadro + .riquadro { border-radius: 8px; }
  .j-kw { color: #c792ea; } .j-tipo { color: #82aaff; } .j-str { color: #c3e88d; }
  .j-num { color: #f78c6c; } .j-ann { color: #ffcb6b; }
  .j-com { color: #6b7385; font-style: italic; }
</style>
</head>
<body>
<header>
  <span class="titolo">__NOME__</span>
  <span class="spazio"></span>
  <span id="stato-consegna" class="avviso"></span>
  <div id="cronometro">--:--</div>
</header>

<div class="tab" id="tab"></div>

<main>
  <div class="colonna">
    <section class="riquadro" id="traccia"></section>
    <section class="riquadro">
      <div class="editor-testa">
        <h2>Risposta — Soluzione.java</h2>
        <span id="salvataggio"></span>
      </div>
      <div class="editor">
        <div class="numeri" aria-hidden="true"><div id="numeri">1</div></div>
        <pre aria-hidden="true"><code id="colorato"></code></pre>
        <textarea id="codice" wrap="off" spellcheck="false" autocomplete="off"
                  autocorrect="off" autocapitalize="off" aria-label="Codice dell'esercizio"></textarea>
      </div>
    </section>
  </div>
  <aside class="riquadro laterale">
    <h2 style="margin-top:0">Esecuzione</h2>
    <div class="riga"><span>Esercizio</span><b id="es-corrente">ES1</b></div>
    <div class="riga"><span>Esecuzioni</span><b id="es-conta">0 / 5</b></div>
    <div class="riga"><span>Punti</span><b id="es-punti">5</b></div>
    <button class="azione" id="esegui">Esegui</button>
    <button class="azione" id="pausa">Pausa</button>
    <button class="azione" id="consegna">Consegna</button>
    <div id="esito" hidden></div>
    <div class="avviso" id="avviso"></div>
  </aside>
</main>

<script>
const ESERCIZI = __ESERCIZI__;
const TRACCE = __TRACCE__;
const PUNTI = __PUNTI__;
let corrente = "ES1";
let stato = null;
const esiti = {};   // ultimo verdetto per esercizio: non deve seguire il cambio di tab
const codici = {};  // testo di ogni Soluzione.java come si trova nell'editor
const daSalvare = {};   // autosalvataggi in attesa, per esercizio
let caricato = false;
const area = document.getElementById("codice");
const colorato = document.getElementById("colorato");
const numeri = document.getElementById("numeri");
let righe = 1;

const TOKEN = /(\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$))|("(?:[^"\\\n]|\\.)*"?|'(?:[^'\\\n]|\\.)*'?)|(@\w+)|\b(\d[\w.]*)|\b(abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|record|return|short|static|super|switch|synchronized|this|throw|throws|transient|try|var|void|volatile|while|yield|true|false|null)\b|\b([A-Z]\w*)/g;
const CLASSI = [null, "j-com", "j-str", "j-ann", "j-num", "j-kw", "j-tipo"];

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
  area.value = codici[corrente] || "";
  area.scrollTop = area.scrollLeft = 0;
  ridisegnaCodice();
}

function segnaSalvataggio(testo, sporco) {
  const s = document.getElementById("salvataggio");
  s.textContent = testo;
  s.className = sporco ? "sporco" : "";
}

function programmaSalvataggio(es, attesa) {
  clearTimeout(daSalvare[es]);
  segnaSalvataggio("modifiche non salvate", true);
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
    segnaSalvataggio("server non raggiungibile: nuovo tentativo…", true);
    programmaSalvataggio(es, 3000);
  }
}

async function salvaTutto() {
  for (const es of Object.keys(daSalvare)) await salvaCodice(es);
}

async function caricaCodice() {
  const r = await fetch("/api/codice");
  Object.assign(codici, await r.json());
  caricato = true;
  mostraCodice();
  aggiornaPannello();
}

area.addEventListener("scroll", allinea);
area.addEventListener("input", () => {
  codici[corrente] = area.value;
  ridisegnaCodice();
  programmaSalvataggio(corrente, 700);
});
area.addEventListener("keydown", e => {
  if (e.key === "Tab" && !e.shiftKey && !area.readOnly) {
    e.preventDefault();
    document.execCommand("insertText", false, "    ");   // a differenza di setRangeText, resta annullabile
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
    b.innerHTML = es + '<span class="conta" id="conta-' + es + '">0/5</span>';
    b.onclick = () => {
      corrente = es;
      aggiornaTab(); disegnaTraccia(); mostraCodice(); aggiornaPannello(); mostraEsito();
    };
    tab.appendChild(b);
  }
}

function aggiornaTab() {
  for (const es of ESERCIZI) {
    document.getElementById("tab-" + es).className = es === corrente ? "attivo" : "";
    if (stato) {
      document.getElementById("conta-" + es).textContent = stato.esecuzioni[es] + "/5";
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
  const registrato = esiti[corrente];
  esito.hidden = !registrato;
  esito.className = registrato ? registrato.classe : "";
  esito.innerHTML = registrato ? registrato.html : "";
}

function aggiornaPannello() {
  if (!stato) return;
  const n = stato.esecuzioni[corrente];
  document.getElementById("es-corrente").textContent = corrente;
  document.getElementById("es-conta").textContent = n + " / 5";
  document.getElementById("es-punti").textContent = PUNTI[corrente];
  const bloccato = stato.consegnato || stato.scaduto || stato.in_pausa;
  document.getElementById("esegui").disabled = bloccato;
  area.readOnly = bloccato || !caricato;
  document.getElementById("consegna").disabled = stato.consegnato;
  const pausa = document.getElementById("pausa");
  pausa.disabled = stato.consegnato;
  pausa.textContent = stato.in_pausa ? "Riprendi" : "Pausa";
  pausa.className = "azione" + (stato.in_pausa ? " attiva" : "");
  const avviso = document.getElementById("avviso");
  if (stato.in_pausa) {
    avviso.textContent = "Prova in pausa: cronometro fermo, esecuzioni sospese.";
  } else if (n >= 5 && !bloccato) {
    avviso.textContent = "Limite raggiunto: ogni ulteriore esecuzione è una penalità.";
  } else { avviso.textContent = ""; }
}

function aggiornaCronometro() {
  const c = document.getElementById("cronometro");
  const r = Math.max(0, Math.floor(stato.rimanente));
  const m = String(Math.floor(r / 60)).padStart(2, "0");
  const s = String(r % 60).padStart(2, "0");
  c.textContent = m + ":" + s;
  c.className = stato.consegnato ? ""
      : (stato.in_pausa ? "pausa" : (r === 0 ? "scaduto" : (r <= 300 ? "allarme" : "")));
  const nota = document.getElementById("stato-consegna");
  if (stato.consegnato) {
    nota.textContent = "Consegnato (" + stato.motivo_consegna + ") — report: " + stato.report;
  } else if (stato.in_pausa) {
    nota.textContent = "IN PAUSA";
  } else { nota.textContent = ""; }
}

async function poll() {
  const r = await fetch("/api/stato");
  stato = await r.json();
  aggiornaCronometro();
  aggiornaPannello();
  aggiornaTab();
}

document.getElementById("esegui").onclick = async () => {
  const bottone = document.getElementById("esegui");
  const lanciato = corrente;
  bottone.disabled = true;
  bottone.textContent = "Compilazione…";
  esiti[lanciato] = {classe: "", html: '<div class="verdetto">IN CORSO…</div>'};
  mostraEsito();
  // Il codice viaggia con la richiesta: si compila esattamente cio' che e' nell'editor.
  clearTimeout(daSalvare[lanciato]);
  delete daSalvare[lanciato];
  const r = await fetch("/api/esegui", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({es: lanciato, codice: codici[lanciato]})
  });
  const d = await r.json();
  bottone.textContent = "Esegui";
  if (!d.errore && !Object.keys(daSalvare).length) segnaSalvataggio("salvato", false);
  if (d.errore) {
    esiti[lanciato] = {classe: "fallito",
      html: '<div class="verdetto">NON ESEGUITO</div><div class="nota">' + d.errore + '</div>'};
  } else {
    const etichette = {
      SUPERATO: ["superato", "TEST SUPERATO", "Tutte le verifiche sono passate."],
      FALLITO: ["fallito", "TEST FALLITO", "Almeno una verifica non è passata."],
      COMPILAZIONE: ["compilazione", "ERRORE DI COMPILAZIONE", "Esecuzione consumata comunque."],
      BLOCCO: ["blocco", "ESECUZIONE INTERROTTA", "Il programma non ha risposto entro il tempo limite."]
    };
    const [cls, titolo, nota] = etichette[d.esito];
    let corpo = '<div class="verdetto">' + titolo + '</div><div class="nota">' + lanciato + ' · '
      + nota + ' Esecuzione ' + d.n + ' di 5.'
      + (d.oltre_limite ? ' <b>Oltre il limite: penalità.</b>' : '') + '</div>';
    if (d.errori_compilatore) {
      corpo += '<pre class="errore-compilatore"><code>' + fuggi(d.errori_compilatore) + '</code></pre>';
    }
    for (const v of (d.verifiche || [])) {
      corpo += '<div class="verifica ' + (v.superata ? 'passata' : 'persa') + '">'
        + '<span class="segno">' + (v.superata ? '✓' : '✗') + '</span>'
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
    esiti[lanciato] = {classe: cls, html: corpo};
  }
  mostraEsito();
  await poll();
};

document.getElementById("pausa").onclick = async () => {
  await salvaTutto();
  await fetch("/api/pausa", {method: "POST"});
  await poll();
};

document.getElementById("consegna").onclick = async () => {
  if (!confirm("Consegnare adesso? Le esecuzioni si chiudono e viene generato il report.")) return;
  await salvaTutto();
  await fetch("/api/consegna", {method: "POST"});
  for (const es of ESERCIZI) {
    esiti[es] = {classe: "", html: '<div class="verdetto">CONSEGNATO</div><div class="nota">'
      + 'Report generato nella cartella della simulazione.</div>'};
  }
  mostraEsito();
  await poll();
};

creaTab();
aggiornaTab();
disegnaTraccia();
mostraEsito();
caricaCodice();
poll();
setInterval(poll, 1000);
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
                    "consegnato": p.dati["consegnato"],
                    "motivo_consegna": p.dati["motivo_consegna"],
                    "report": os.path.basename(p.dati["report"]) if p.dati["report"] else None,
                    "esecuzioni": {e: p.numero_esecuzioni(e) for e in ESERCIZI},
                })
            return
        if self.path == "/api/codice":
            with stato_lock:
                self._json({e: Gestore.prova.leggi_codice(e) for e in ESERCIZI})
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
                if isinstance(richiesta.get("codice"), str):
                    p.scrivi_codice(es, richiesta["codice"])
                voce = p.esegui(es)
            print(f"  {es} — esecuzione {voce['n']}: {voce['esito']}")
            # Come su Moodle: verdetto, elenco delle verifiche con il loro
            # esito e, su quelle fallite, atteso e ottenuto. Se il tester non
            # segue la convenzione, o il test fallisce (eccezioni su stderr),
            # viaggia anche l'output grezzo.
            self._json({
                "n": voce["n"],
                "esito": voce["esito"],
                "oltre_limite": voce["oltre_limite"],
                "errori_compilatore": voce["errori_compilatore"],
                "verifiche": voce["verifiche"],
                "uscita": voce["uscita"]
                          if not voce["verifiche"] or voce["esito"] == "FALLITO" else "",
            })
            return

        self.send_error(404)

    def controlla_scadenza(self):
        p = Gestore.prova
        if p.in_pausa():
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
              .replace("__PUNTI__", json.dumps(PUNTI))
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
