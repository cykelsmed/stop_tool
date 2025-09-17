"""Stoptool – kravspec v1.3

Formål

Beregner og foreslår Nyt stop pr. aktie. Aldrig sænke eksisterende stop: hvis Beregnet stop < Gammelt stop → ingen ændring. Du opdaterer manuelt i Nordnet.

Input og filer

Portefølje (Yahoo CSV, UTF-8)
Kolonner: Symbol,Trade Date,Quantity,Purchase Price,Commission

NVDA,2023-01-15,10,145.30,0
MSFT,2022-10-01,5,250.00,0


config.yaml

price_source: yfinance
report:
  dir: reports
  formats: [csv, md]
defaults:
  rule: {type: ma, use: [50,150], buffer_pct: 1.0, min_atr_mult: 1.0}
  fallback:
    if_only_50: {type: ma, use: [50], buffer_pct: 1.0, min_atr_mult: 1.0}
    if_no_ma:   {type: percent, p: 12}
overrides: {}   # pr. ticker: buffer_pct, min_atr_mult, p


state.json (pr. ticker)

{
  "NVDA": {"peak_close": 154.20, "last_stop": 137.80, "last_update": "2025-09-17"}
}

Datakilder og valuta

Kurskilde: yfinance. Brug daglig Adj Close, seneste ~252 handelsdage. Valuta = aktiens handelsvaluta. Ingen konvertering i rapport.

Indikatorer

SMA50, SMA150 (simpel). ATR14 (Wilder).

Regler og beregning

Hierarki for Beregnet stop

SMA50 og SMA150 findes: min(SMA50,SMA150) * (1 - buffer_pct/100)

Kun SMA50: SMA50 * (1 - buffer_pct/100)

Ingen MA: peak_close * (1 - p/100)

ATR-krav
Stop skal ligge mindst min_atr_mult * ATR14 under Seneste luk (Close). Hvis Close - beregnet < mult*ATR14 → sæt beregnet = Close - mult*ATR14 og årsag = ATR_BLOCKED.

Endelig fastsættelse
nyt_stop = max(last_stop, beregnet)
Peak: peak_close = max(peak_close, Close)

Defaults

buffer_pct=1.0, min_atr_mult=1.0, p=12.

Rapport

Formater: CSV og Markdown. Kolonner:
Dato | Ticker | Navn | Valuta | Seneste luk | SMA50 | SMA150 | ATR14 | Peak (højeste luk) | Gammelt stop | Beregnet stop | Nyt stop | Ændring | Beslutning | Regel | Årsag | Note

Beslutning: HÆV / INGEN

Regel: MA / MA50 / %12

Årsag: MA_min, ONLY_SMA50, FALLBACK_PERCENT, ATR_BLOCKED, KANDIDAT<LAST_STOP, NO_DATA, SYMBOL_ERROR

Note: kort JSON (source, adj, buffer, atr_mult, ts)

Eksempel (én række)
2025-09-17,NVDA,NVIDIA Corp.,USD,150.60,145.30,128.90,6.80,154.20,137.80,143.10,143.10,5.30,HÆV,MA,MA_min,"{""buffer"":1.0,""atr_mult"":1.0}"

State

Opdater peak_close når Close sætter ny top. Opdater last_stop kun ved HÆV. Datoformat ISO YYYY-MM-DD.

CLI

Kommandoer:

stoptool run --report md,csv
stoptool run --report md --tickers NVDA,SOFI
stoptool run --report csv --dry-run


Parametre: --report, --tickers, --dry-run
Exit codes: 0=ok, 1=input/config/state-fejl, 2=datakilde-fejl.

Log og revisionsspor

Terminallinje pr. ticker:
NVDA: HÆV 137.80 → 143.10 | Regel=MA | Årsag=MA_min | SMA50=145.3 SMA150=128.9 ATR=6.8 Peak=154.2
Note-felt i rapport: JSON som ovenfor.

Fejl og edge cases

Ny IPO → %12 fallback. Ingen SMA150 → ONLY_SMA50. Ingen data → NO_DATA.
ATR-blokering → ATR_BLOCKED, Beslutning=INGEN.
Symbolfejl → SYMBOL_ERROR i log, ingen crash.
Splits/udbytte → brug Adj Close.

Ordliste

Seneste luk, SMA50/SMA150, ATR14, Peak (højeste luk), Gammelt stop, Beregnet stop, Nyt stop, Beslutning.

Acceptkriterier

Ingen stops sænkes

ATR-krav respekteres

Fallback-regler anvendes korrekt

Rapport indeholder klare feltnavne og årsager

Note/revisionsspor på alle rækker

--dry-run rører ikke state

Overrides anvendes korrekt

Symbolfejl håndteres uden crash
"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Create the command line parser for Stoptool."""
    parser = argparse.ArgumentParser(
        description="Stoptool – beregningsværktøj til stop-opdateringer"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        help="Kommando der skal køres (fx run). Flere kommandoer tilføjes senere.",
    )
    parser.add_argument(
        "--report",
        dest="report_formats",
        default="md,csv",
        help="Rapportformater separeret med komma (fx md,csv).",
    )
    parser.add_argument(
        "--tickers",
        dest="tickers",
        default=None,
        help="Kommasepareret liste over tickers der skal behandles.",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Kør uden at opdatere state.json.",
    )
    return parser


def main() -> None:
    """Entrypoint for the CLI placeholder."""
    parser = build_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()
