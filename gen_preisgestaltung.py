#!/usr/bin/env python3
"""
Generate Preisgestaltung-Privatpatienten.pdf
One A4 page for handout at first appointment / on request.
"""

import tempfile, os
from weasyprint import HTML

HTML_CONTENT = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Preisgestaltung für Privatpatienten</title>
<style>
  @page {
    size: A4;
    margin: 13mm 14mm 12mm 14mm;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 9pt;
    color: #1a1a1a;
    line-height: 1.45;
  }

  /* ── HEADER ── */
  .header {
    border-bottom: 1.5pt solid #1a1a1a;
    padding-bottom: 7pt;
    margin-bottom: 10pt;
  }
  .header-meta {
    font-size: 7pt;
    color: #666;
    letter-spacing: 0.3pt;
    margin-bottom: 2pt;
  }
  .header h1 {
    font-size: 16pt;
    font-weight: 800;
    letter-spacing: -0.5pt;
    line-height: 1.1;
    margin-bottom: 2pt;
  }
  .header .tagline {
    font-size: 8.5pt;
    color: #555;
  }
  .header .badge {
    display: inline-block;
    background: #1a1a1a;
    color: #fff;
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 0.8pt;
    text-transform: uppercase;
    padding: 2pt 5pt;
    border-radius: 1pt;
    margin-top: 5pt;
  }

  /* ── INTRO ── */
  .intro {
    margin-bottom: 9pt;
    padding: 7pt 10pt;
    background: #f7f7f5;
    border-left: 3pt solid #1a1a1a;
  }
  .intro p {
    font-size: 8.5pt;
    line-height: 1.5;
  }
  .intro p + p { margin-top: 3pt; }

  /* ── SECTION TITLE ── */
  .section-title {
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 1pt;
    text-transform: uppercase;
    color: #1a1a1a;
    margin-bottom: 4pt;
    padding-bottom: 2pt;
    border-bottom: 0.8pt solid #ccc;
  }

  /* ── PRICE TABLE ── */
  .price-table-wrap {
    margin-bottom: 8pt;
  }
  table.ptable {
    width: 100%;
    border-collapse: collapse;
  }
  table.ptable thead tr {
    background: #1a1a1a;
    color: #fff;
  }
  table.ptable thead td {
    padding: 4pt 7pt;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.3pt;
  }
  table.ptable tbody td {
    padding: 4.5pt 7pt;
    border-bottom: 0.5pt solid #e8e8e8;
    font-size: 8.5pt;
  }
  table.ptable tbody td.label-col {
    font-weight: 700;
  }
  table.ptable tbody td.sub-col {
    font-size: 8pt;
    color: #555;
  }
  table.ptable tbody td.price-col {
    text-align: right;
    font-weight: 700;
    white-space: nowrap;
  }
  table.ptable tfoot td {
    padding: 6pt 7pt;
    font-weight: 700;
    font-size: 9pt;
  }
  table.ptable tfoot td.total-label {
    color: #444;
  }
  table.ptable tfoot td.total-price {
    text-align: right;
    font-size: 11pt;
    font-weight: 800;
    border-top: 1.5pt solid #1a1a1a;
  }

  /* ── REIMBURSEMENT SECTION ── */
  .reimburse-wrap {
    margin-bottom: 7pt;
  }
  .scenario-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 4pt;
  }
  .scenario-box {
    border: 0.8pt solid #ccc;
    border-radius: 2pt;
    padding: 5pt 7pt;
  }
  .scenario-box.best {
    border-color: #1a1a1a;
    background: #1a1a1a;
    color: #fff;
  }
  .scenario-label {
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 0.8pt;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 3pt;
  }
  .scenario-box.best .scenario-label {
    color: rgba(255,255,255,0.6);
  }
  .scenario-coverage {
    font-size: 12pt;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 2pt;
    letter-spacing: -0.5pt;
  }
  .scenario-net {
    font-size: 7.5pt;
    color: #555;
    line-height: 1.4;
  }
  .scenario-box.best .scenario-net {
    color: rgba(255,255,255,0.75);
  }
  .scenario-note {
    font-size: 7pt;
    color: #888;
    margin-top: 4pt;
    font-style: italic;
    line-height: 1.4;
  }

  /* ── DISCLAIMER BOX ── */
  .disclaimer-box {
    margin-bottom: 7pt;
    padding: 6pt 9pt;
    background: #fff8f0;
    border: 1pt solid #e0c090;
    border-left: 3pt solid #c87800;
    border-radius: 2pt;
  }
  .disclaimer-title {
    font-size: 7.5pt;
    font-weight: 700;
    color: #c87800;
    letter-spacing: 0.5pt;
    text-transform: uppercase;
    margin-bottom: 3pt;
  }
  .disclaimer-box p {
    font-size: 8pt;
    line-height: 1.5;
    color: #333;
  }
  .disclaimer-box p + p {
    margin-top: 3pt;
  }

  /* ── WHAT TO ASK ── */
  .checklist-wrap {
    margin-bottom: 6pt;
  }
  .checklist-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3pt 14pt;
  }
  .cl-item {
    display: flex;
    align-items: flex-start;
    gap: 5pt;
    font-size: 8pt;
    line-height: 1.4;
  }
  .cl-arrow {
    flex-shrink: 0;
    font-weight: 700;
    color: #1a1a1a;
    margin-top: 0.5pt;
  }

  /* ── CONTACT BLOCK ── */
  .contact-block {
    border: 1.5pt solid #1a1a1a;
    padding: 7pt 10pt;
    border-radius: 2pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16pt;
    margin-bottom: 7pt;
  }
  .contact-left h3 {
    font-size: 9.5pt;
    font-weight: 800;
    letter-spacing: -0.2pt;
    margin-bottom: 2pt;
  }
  .contact-left p {
    font-size: 8pt;
    color: #555;
    line-height: 1.4;
  }
  .contact-right {
    text-align: right;
    flex-shrink: 0;
  }
  .contact-name {
    font-size: 8.5pt;
    font-weight: 700;
    margin-bottom: 2pt;
  }
  .contact-detail {
    font-size: 8pt;
    color: #444;
    line-height: 1.5;
  }

  /* ── FOOTER ── */
  .footer {
    font-size: 6.5pt;
    color: #999;
    line-height: 1.35;
    border-top: 0.5pt solid #ddd;
    padding-top: 4pt;
  }
</style>
</head>
<body>

<!-- ══ HEADER ══ -->
<div class="header">
  <div class="header-meta">Mobile Physiotherapie Grausam &nbsp;&middot;&nbsp; Nick Grausam &nbsp;&middot;&nbsp; Physiotherapeut</div>
  <h1>Ihre Kosten als Privatpatient</h1>
  <div class="tagline">Transparente Preise &mdash; was auf Sie zukommt und was erstattet wird.</div>
  <div>
    <span class="badge">Nur f&uuml;r Privatversicherte &amp; Beihilfeberechtigte</span>
  </div>
</div>

<!-- ══ INTRO ══ -->
<div class="intro">
  <p>Als Privatpatient oder Beihilfeberechtigter bezahlen Sie die Behandlung zun&auml;chst selbst &mdash; und reichen die Rechnung anschlie&szlig;end bei Ihrer Versicherung ein. Je nach Tarif und Versicherung erhalten Sie einen Gro&szlig;teil oder die gesamten Kosten erstattet.</p>
  <p>Diese &Uuml;bersicht zeigt Ihnen, was eine typische Verordnung kostet und was bei Ihnen bleiben kann &mdash; <strong>damit es sp&auml;ter keine &Uuml;berraschungen gibt.</strong></p>
</div>

<!-- ══ MEINE HONORARE ══ -->
<div class="price-table-wrap">
  <div class="section-title">Meine Honorare (pro Behandlung)</div>
  <table class="ptable">
    <thead>
      <tr>
        <td style="width:35%;">Leistung</td>
        <td style="width:40%;">Beschreibung</td>
        <td style="width:25%;text-align:right;">Honorar</td>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="label-col">Krankengymnastik (KG)</td>
        <td class="sub-col">Hausbesuch &middot; 30 Min. Einzelbehandlung</td>
        <td class="price-col">29,70 &euro;</td>
      </tr>
      <tr>
        <td class="label-col">Manuelle Therapie (MT)</td>
        <td class="sub-col">Hausbesuch &middot; 30 Min. Einzelbehandlung</td>
        <td class="price-col">35,80 &euro;</td>
      </tr>
      <tr>
        <td class="label-col">Fahrtkostenpauschale</td>
        <td class="sub-col">Pro Hausbesuch, pauschal</td>
        <td class="price-col">10,00 &euro;</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ══ BEISPIELRECHNUNG ══ -->
<div class="price-table-wrap">
  <div class="section-title">Beispielrechnung &mdash; typische Verordnung (6 Einheiten)</div>
  <table class="ptable">
    <thead>
      <tr>
        <td style="width:35%;">Position</td>
        <td style="width:35%;">Berechnung</td>
        <td style="width:30%;text-align:right;">Betrag</td>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="label-col">6 &times; Krankengymnastik (KG)</td>
        <td class="sub-col">6 &times; 29,70 &euro;</td>
        <td class="price-col">178,20 &euro;</td>
      </tr>
      <tr>
        <td class="label-col">6 &times; Manuelle Therapie (MT)</td>
        <td class="sub-col">6 &times; 35,80 &euro;</td>
        <td class="price-col">214,80 &euro;</td>
      </tr>
      <tr>
        <td class="label-col">6 &times; Fahrtkostenpauschale</td>
        <td class="sub-col">6 &times; 10,00 &euro;</td>
        <td class="price-col">60,00 &euro;</td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td class="total-label" colspan="2">Gesamtbetrag (von Ihnen vorzustrecken)</td>
        <td class="total-price">452,00 &euro;</td>
      </tr>
    </tfoot>
  </table>
</div>

<!-- ══ ERSTATTUNG ══ -->
<div class="reimburse-wrap">
  <div class="section-title">Was Ihre Versicherung &uuml;bernehmen kann</div>
  <div class="scenario-grid">
    <div class="scenario-box">
      <div class="scenario-label">Privatversicherung (z. B. 80%)</div>
      <div class="scenario-coverage">~362 &euro;</div>
      <div class="scenario-net">Erstattung durch PKV &middot; Eigenanteil ca. <strong>~90 &euro;</strong></div>
    </div>
    <div class="scenario-box">
      <div class="scenario-label">Beihilfe (z. B. 70%) + erg&auml;nzende PKV</div>
      <div class="scenario-coverage">~392 &euro;</div>
      <div class="scenario-net">Kombiniert Beihilfe + Restkostenversicherung &middot; Eigenanteil ca. <strong>~60 &euro;</strong></div>
    </div>
    <div class="scenario-box best">
      <div class="scenario-label">Beste Konstellation</div>
      <div class="scenario-coverage">~392+ &euro;</div>
      <div class="scenario-net">Vollst&auml;ndige Erstattung (Behandlung) &middot; Eigenanteil kann auf <strong>~60 &euro;</strong> sinken*</div>
    </div>
  </div>
  <div class="scenario-note">* Fahrtkosten (60 &euro;) werden je nach Versicherungstarif erstattet oder nicht. Die tats&auml;chliche Erstattung h&auml;ngt von Ihrem pers&ouml;nlichen Versicherungsvertrag ab.</div>
</div>

<!-- ══ DISCLAIMER ══ -->
<div class="disclaimer-box">
  <div class="disclaimer-title">&#9888; Wichtig: Vorab informieren</div>
  <p>Die Erstattungsbetr&auml;ge sind Richtwerte &mdash; kein verbindliches Versprechen. Jede Versicherung und jeder Tarif ist anders. Bitte kl&auml;ren Sie vor dem ersten Termin, ob und in welchem Umfang Ihre Versicherung Physiotherapie-Hausbesuche erstattet.</p>
  <p><strong>Fragen Sie Ihre Versicherung:</strong> Sind Hausbesuche erstattungsf&auml;hig? Gilt das GEB&Uuml;H-Preisrahmen? Ist eine vorherige Genehmigung erforderlich? Wie hoch ist Ihr pers&ouml;nlicher Erstattungssatz? &mdash; Nur so vermeiden Sie finanzielle &Uuml;berraschungen.</p>
</div>

<!-- ══ CHECKLISTE ══ -->
<div class="checklist-wrap">
  <div class="section-title">Was Sie vorab kl&auml;ren sollten</div>
  <div class="checklist-2col">
    <div class="cl-item"><span class="cl-arrow">&#10140;</span><span>Hausbesuche durch meinen Tarif erstattungsf&auml;hig?</span></div>
    <div class="cl-item"><span class="cl-arrow">&#10140;</span><span>Welcher Erstattungssatz gilt f&uuml;r mich?</span></div>
    <div class="cl-item"><span class="cl-arrow">&#10140;</span><span>Brauche ich eine Vorabgenehmigung?</span></div>
    <div class="cl-item"><span class="cl-arrow">&#10140;</span><span>Gelten Einschr&auml;nkungen bei Sonderleistungen?</span></div>
    <div class="cl-item"><span class="cl-arrow">&#10140;</span><span>Werden Fahrtkosten des Therapeuten erstattet?</span></div>
    <div class="cl-item"><span class="cl-arrow">&#10140;</span><span>Wie reiche ich die Rechnung korrekt ein?</span></div>
  </div>
</div>

<!-- ══ CONTACT ══ -->
<div class="contact-block">
  <div class="contact-left">
    <h3>Fragen zur Kostenstruktur?</h3>
    <p>Ich erkl&auml;re Ihnen beim Ersttermin alles Schritt f&uuml;r Schritt &mdash;<br>und stelle Ihnen eine klar strukturierte Rechnung f&uuml;r die Einreichung aus.</p>
  </div>
  <div class="contact-right">
    <div class="contact-name">Nick Grausam</div>
    <div class="contact-detail">0176 4268 5146</div>
    <div class="contact-detail">info@physiotherapie-grausam.com</div>
  </div>
</div>

<!-- ══ FOOTER ══ -->
<div class="footer">
  Alle Honorare sind Nettobetrag. Diese &Uuml;bersicht dient der Orientierung und ersetzt keine individuelle Auskunft Ihrer Krankenversicherung. &nbsp;&middot;&nbsp;
  Mobile Physiotherapie Grausam &nbsp;&middot;&nbsp; Nick Grausam &nbsp;&middot;&nbsp; info@physiotherapie-grausam.com &nbsp;&middot;&nbsp; 0176 4268 5146
</div>

</body>
</html>
"""

OUTPUT_PATH = "/home/user/Mobile-Physiotherapie-Grausam/dokumente/Preisgestaltung-Privatpatienten.pdf"

def main():
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
        f.write(HTML_CONTENT)
        tmp_html = f.name

    try:
        print(f"Generating PDF from {tmp_html} ...")
        html = HTML(filename=tmp_html)
        html.write_pdf(OUTPUT_PATH)
        print(f"Saved to {OUTPUT_PATH}")
    finally:
        os.unlink(tmp_html)

    import fitz
    doc = fitz.open(OUTPUT_PATH)
    pages = len(doc)
    doc.close()
    print(f"Page count: {pages}")
    if pages == 1:
        print("OK: exactly 1 page.")
    else:
        print(f"NOTE: {pages} pages — adjust margins/font sizes if 1 page is required.")

if __name__ == "__main__":
    main()
