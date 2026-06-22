#!/usr/bin/env python3
"""
Generate Preisgestaltung-Privatpatienten.pdf — 1 A4 page.
Logo oben links (groß), Expertise direkt darunter, kein doppelter Footer.
"""
import tempfile, os
from weasyprint import HTML

TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<style>
@page { size: A4; margin: 10mm 13mm 10mm 13mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 8.5pt; color: #1a1a1a; line-height: 1.4; }

/* HEADER */
.header { border-bottom: 1.5pt solid #1a1a1a; padding-bottom: 6pt; margin-bottom: 4pt; }
.logo-wrap { margin-bottom: 3pt; }
.logo-wrap svg { width: 50%; height: auto; display: block; }
.header-text h1 { font-size: 16pt; font-weight: 800; letter-spacing: -0.5pt; line-height: 1.1; margin-bottom: 2pt; }
.header-text .tagline { font-size: 8.5pt; color: #555; }
.badge { display: inline-block; background: #1a1a1a; color: #fff; font-size: 7pt; font-weight: 700; letter-spacing: 0.8pt; text-transform: uppercase; padding: 2pt 5pt; border-radius: 1pt; margin-top: 4pt; }

/* SECTION TITLE */
.section-title { font-size: 7pt; font-weight: 700; letter-spacing: 1pt; text-transform: uppercase; color: #1a1a1a; margin-bottom: 2pt; padding-bottom: 2pt; border-bottom: 0.8pt solid #ccc; }

/* EXPERTISE */
.expertise-section { margin-bottom: 3pt; }
.expertise-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 14pt; row-gap: 1.5pt; }
.expertise-item { display: flex; align-items: flex-start; gap: 4pt; font-size: 8pt; line-height: 1.35; }
.expertise-dash { flex-shrink: 0; color: #888; margin-top: 0.5pt; }

/* INTRO */
.intro { margin-bottom: 3pt; padding: 5pt 9pt; background: #f7f7f5; border-left: 3pt solid #1a1a1a; }
.intro p { font-size: 8.5pt; line-height: 1.5; }
.intro p + p { margin-top: 3pt; }

/* PRICE TABLE */
.price-table-wrap { margin-bottom: 3pt; }
table.ptable { width: 100%; border-collapse: collapse; }
table.ptable thead tr { background: #1a1a1a; color: #fff; }
table.ptable thead td { padding: 4pt 7pt; font-size: 7.5pt; font-weight: 700; letter-spacing: 0.3pt; }
table.ptable tbody td { padding: 4.5pt 7pt; border-bottom: 0.5pt solid #e8e8e8; font-size: 8.5pt; }
table.ptable tbody td.lc { font-weight: 700; }
table.ptable tbody td.sc { font-size: 8pt; color: #555; }
table.ptable tbody td.pc { text-align: right; font-weight: 700; white-space: nowrap; }
table.ptable tfoot td { padding: 5.5pt 7pt; font-weight: 700; font-size: 9pt; }
table.ptable tfoot td.tl { color: #444; }
table.ptable tfoot td.tp { text-align: right; font-size: 11pt; font-weight: 800; border-top: 1.5pt solid #1a1a1a; }

/* SCENARIOS */
.reimburse-wrap { margin-bottom: 3pt; }
.scenario-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4pt; }
.scenario-box { border: 0.8pt solid #ccc; border-radius: 2pt; padding: 5pt 7pt; }
.scenario-box.best { border-color: #1a1a1a; background: #1a1a1a; color: #fff; }
.scenario-label { font-size: 7pt; font-weight: 700; letter-spacing: 0.8pt; text-transform: uppercase; color: #888; margin-bottom: 2pt; }
.scenario-box.best .scenario-label { color: rgba(255,255,255,0.6); }
.scenario-coverage { font-size: 12pt; font-weight: 800; line-height: 1; margin-bottom: 2pt; letter-spacing: -0.5pt; }
.scenario-net { font-size: 7.5pt; color: #555; line-height: 1.4; }
.scenario-box.best .scenario-net { color: rgba(255,255,255,0.75); }
.scenario-note { font-size: 7pt; color: #888; margin-top: 4pt; font-style: italic; line-height: 1.4; }

/* DISCLAIMER */
.disclaimer-box { margin-bottom: 3pt; padding: 5pt 9pt; background: #fff8f0; border: 1pt solid #e0c090; border-left: 3pt solid #c87800; border-radius: 2pt; }
.disclaimer-title { font-size: 7.5pt; font-weight: 700; color: #c87800; letter-spacing: 0.5pt; text-transform: uppercase; margin-bottom: 2pt; }
.disclaimer-box p { font-size: 8pt; line-height: 1.5; color: #333; }
.disclaimer-box p + p { margin-top: 3pt; }

/* CHECKLIST */
.checklist-wrap { margin-bottom: 3pt; }
.checklist-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 3pt 14pt; }
.cl-item { display: flex; align-items: flex-start; gap: 5pt; font-size: 8pt; line-height: 1.4; }
.cl-arrow { flex-shrink: 0; font-weight: 700; color: #1a1a1a; margin-top: 0.5pt; }

/* CONTACT */
.contact-block { border: 1.5pt solid #1a1a1a; padding: 7pt 10pt; border-radius: 2pt; display: flex; justify-content: space-between; align-items: center; gap: 16pt; margin-bottom: 3pt; }
.contact-left h3 { font-size: 9.5pt; font-weight: 800; letter-spacing: -0.2pt; margin-bottom: 2pt; }
.contact-left p { font-size: 8pt; color: #555; line-height: 1.4; }
.contact-right { text-align: right; flex-shrink: 0; }
.contact-name { font-size: 8.5pt; font-weight: 700; margin-bottom: 2pt; }
.contact-detail { font-size: 8pt; color: #444; line-height: 1.5; }

/* LEGAL NOTE */
.legal-note { font-size: 6.5pt; color: #999; line-height: 1.35; border-top: 0.5pt solid #ddd; padding-top: 4pt; }
</style>
</head>
<body>

<!-- HEADER: Logo oben, Titel darunter -->
<div class="header">
  <div class="logo-wrap">LOGO_PLACEHOLDER</div>
  <div class="header-text">
    <h1>Ihre Kosten als Privatpatient</h1>
    <div class="tagline">Transparente Preise &mdash; was auf Sie zukommt und was erstattet wird.</div>
    <div><span class="badge">Nur f&uuml;r Privatversicherte &amp; Beihilfeberechtigte</span></div>
  </div>
</div>

<!-- MEINE EXPERTISE -->
<div class="expertise-section">
  <div class="section-title">Meine Expertise</div>
  <div class="expertise-grid">
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Physiotherapeut &mdash; klinische Berufserfahrung, medizinischer Blick auf Bewegung &amp; Rehabilitation</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Leistungshandball im NLZ der Rhein-Neckar L&ouml;wen (Handball-Bundesliga)</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Fortbildung beim ehemaligen Physio der deutschen Fu&szlig;ballnationalmannschaft</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Qualifikation KGG &middot; Technikschulung olympisches Gewichtheben &middot; eigene Verletzungserfahrung</span></div>
  </div>
</div>

<!-- INTRO -->
<div class="intro">
  <p>Als Privatpatient oder Beihilfeberechtigter bezahlen Sie die Behandlung zun&auml;chst selbst &mdash; und reichen die Rechnung anschlie&szlig;end bei Ihrer Versicherung ein. Je nach Tarif erhalten Sie einen Gro&szlig;teil oder alle Kosten erstattet.</p>
  <p>Diese &Uuml;bersicht zeigt, was eine typische Verordnung kostet und was bei Ihnen bleiben kann &mdash; <strong>damit es sp&auml;ter keine &Uuml;berraschungen gibt.</strong></p>
</div>

<!-- HONORARE -->
<div class="price-table-wrap">
  <div class="section-title">Meine Honorare (pro Behandlung)</div>
  <table class="ptable">
    <thead><tr><td style="width:35%;">Leistung</td><td style="width:40%;">Beschreibung</td><td style="width:25%;text-align:right;">Honorar</td></tr></thead>
    <tbody>
      <tr><td class="lc">Krankengymnastik (KG)</td><td class="sc">Hausbesuch &middot; 30 Min.</td><td class="pc">29,70 &euro;</td></tr>
      <tr><td class="lc">Manuelle Therapie (MT)</td><td class="sc">Hausbesuch &middot; 30 Min.</td><td class="pc">35,80 &euro;</td></tr>
      <tr><td class="lc">Fahrtkostenpauschale</td><td class="sc">Pro Hausbesuch, pauschal</td><td class="pc">10,00 &euro;</td></tr>
    </tbody>
  </table>
</div>

<!-- BEISPIELRECHNUNG -->
<div class="price-table-wrap">
  <div class="section-title">Beispielrechnung &mdash; typische Verordnung (6 Einheiten)</div>
  <table class="ptable">
    <thead><tr><td style="width:40%;">Position</td><td style="width:30%;">Berechnung</td><td style="width:30%;text-align:right;">Betrag</td></tr></thead>
    <tbody>
      <tr><td class="lc">6 &times; Krankengymnastik (KG)</td><td class="sc">6 &times; 29,70 &euro;</td><td class="pc">178,20 &euro;</td></tr>
      <tr><td class="lc">6 &times; Manuelle Therapie (MT)</td><td class="sc">6 &times; 35,80 &euro;</td><td class="pc">214,80 &euro;</td></tr>
      <tr><td class="lc">6 &times; Fahrtkostenpauschale</td><td class="sc">6 &times; 10,00 &euro;</td><td class="pc">60,00 &euro;</td></tr>
    </tbody>
    <tfoot><tr><td class="tl" colspan="2">Gesamtbetrag (von Ihnen vorzustrecken)</td><td class="tp">452,00 &euro;</td></tr></tfoot>
  </table>
</div>

<!-- ERSTATTUNG -->
<div class="reimburse-wrap">
  <div class="section-title">Was Ihre Versicherung &uuml;bernehmen kann</div>
  <div class="scenario-grid">
    <div class="scenario-box">
      <div class="scenario-label">Privatversicherung (z. B. 80%)</div>
      <div class="scenario-coverage">~362 &euro;</div>
      <div class="scenario-net">Erstattung durch PKV &middot; Eigenanteil ca. <strong>~90 &euro;</strong></div>
    </div>
    <div class="scenario-box">
      <div class="scenario-label">Beihilfe (70%) + erg&auml;nzende PKV</div>
      <div class="scenario-coverage">~392 &euro;</div>
      <div class="scenario-net">Kombiniert &middot; Eigenanteil ca. <strong>~60 &euro;</strong></div>
    </div>
    <div class="scenario-box best">
      <div class="scenario-label">Beste Konstellation</div>
      <div class="scenario-coverage">~392+ &euro;</div>
      <div class="scenario-net">Vollst&auml;ndige Erstattung &middot; Eigenanteil kann auf <strong>~60 &euro;</strong> sinken*</div>
    </div>
  </div>
  <div class="scenario-note">* Fahrtkosten (60 &euro;) werden je nach Tarif erstattet oder nicht. Tats&auml;chliche Erstattung h&auml;ngt vom pers&ouml;nlichen Versicherungsvertrag ab.</div>
</div>

<!-- DISCLAIMER -->
<div class="disclaimer-box">
  <div class="disclaimer-title">&#9888; Wichtig: Vorab informieren</div>
  <p>Diese Betr&auml;ge sind Richtwerte &mdash; kein verbindliches Versprechen. Bitte kl&auml;ren Sie vor dem ersten Termin, ob und in welchem Umfang Ihre Versicherung Physiotherapie-Hausbesuche erstattet.</p>
  <p><strong>Fragen Sie Ihre Versicherung:</strong> Sind Hausbesuche erstattungsf&auml;hig? Ist eine Vorabgenehmigung n&ouml;tig? Wie hoch ist Ihr Erstattungssatz? Werden Fahrtkosten erstattet?</p>
</div>

<!-- CONTACT -->
<div class="contact-block">
  <div class="contact-left">
    <h3>Fragen zur Kostenstruktur?</h3>
    <p>Ich erkl&auml;re Ihnen beim Ersttermin alles Schritt f&uuml;r Schritt &mdash; und stelle Ihnen eine klar strukturierte Rechnung f&uuml;r die Einreichung aus.</p>
  </div>
  <div class="contact-right">
    <div class="contact-name">Nick Grausam</div>
    <div class="contact-detail">0176 4268 5146</div>
    <div class="contact-detail">info@physiotherapie-grausam.com</div>
  </div>
</div>

<!-- LEGAL NOTE — kein doppelter Kontakt -->
<div class="legal-note">
  Alle Honorare sind Nettobetrag. Diese &Uuml;bersicht dient der Orientierung und ersetzt keine individuelle Auskunft Ihrer Krankenversicherung.
</div>

</body>
</html>"""

OUTPUT_PATH = "/home/user/Mobile-Physiotherapie-Grausam/dokumente/Preisgestaltung-Privatpatienten.pdf"
LOGO_PATH   = "/home/user/Mobile-Physiotherapie-Grausam/logo.svg"

def main():
    with open(LOGO_PATH) as f:
        svg = f.read()
    svg_scaled = svg.replace(
        'viewBox="0 0 226.8 66"',
        'viewBox="0 0 226.8 66" style="width:50%;height:auto;display:block;"',
        1
    )
    html = TEMPLATE.replace('LOGO_PLACEHOLDER', svg_scaled)

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
        f.write(html)
        tmp = f.name

    try:
        HTML(filename=tmp).write_pdf(OUTPUT_PATH)
        print(f"Saved: {OUTPUT_PATH}")
    finally:
        os.unlink(tmp)

    import fitz
    doc = fitz.open(OUTPUT_PATH)
    n = len(doc)
    doc.close()
    print(f"Pages: {n}")
    if n != 1:
        print(f"NOTE: expected 1, got {n} — adjust spacing")

if __name__ == "__main__":
    main()
