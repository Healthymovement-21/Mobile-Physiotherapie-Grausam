#!/usr/bin/env python3
"""Generate Ernaehrungsguide.pdf — Allgemeine Ernährungsempfehlungen."""
import tempfile, os
from weasyprint import HTML

TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<style>
@page { size: A4; margin: 16mm 18mm; border-top: 2pt solid #1a1a1a; border-bottom: 2pt solid #1a1a1a; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 9.5pt; color: #1a1a1a; line-height: 1.6; }

.cover { padding-bottom: 12pt; margin-bottom: 14pt; border-bottom: 1pt solid #1a1a1a; display: flex; justify-content: space-between; align-items: flex-end; }
.cover-left h1 { font-size: 20pt; font-weight: 800; letter-spacing: -0.5pt; line-height: 1.05; margin-bottom: 3pt; }
.cover-left .sub { font-size: 10pt; color: #555; }
.cover-right { text-align: right; }
.logo-wrap svg { width: 120pt; height: auto; display: block; }

.disclaimer { background: #f7f7f7; border-left: 2pt solid #aaa; padding: 9pt 12pt; margin-bottom: 16pt; font-size: 8pt; color: #555; line-height: 1.55; }
.disclaimer strong { color: #1a1a1a; display: block; margin-bottom: 4pt; font-size: 8.5pt; }
.disclaimer p { margin-bottom: 4pt; }
.disclaimer p:last-child { margin-bottom: 0; }

.section { margin-bottom: 16pt; }
.section-title { font-size: 7.5pt; font-weight: 700; letter-spacing: 2.5pt; text-transform: uppercase; color: #999; margin-bottom: 9pt; break-after: avoid; page-break-after: avoid; }
.section-heading { font-size: 11.5pt; font-weight: 800; margin-bottom: 7pt; letter-spacing: -0.2pt; break-after: avoid; page-break-after: avoid; }
p { margin-bottom: 6pt; }
p:last-child { margin-bottom: 0; }

.sub-heading { font-size: 9.5pt; font-weight: 700; margin-top: 8pt; margin-bottom: 4pt; break-after: avoid; page-break-after: avoid; }
ul { margin: 4pt 0 8pt 14pt; }
ul li { margin-bottom: 2pt; font-size: 9.5pt; line-height: 1.5; }

table.data { width: 100%; border-collapse: collapse; margin: 6pt 0 8pt; font-size: 9pt; }
table.data thead tr { background: #1a1a1a; color: #fff; }
table.data thead td { padding: 5pt 8pt; font-weight: 700; font-size: 8pt; letter-spacing: .3pt; }
table.data tbody td { padding: 4pt 8pt; border-bottom: .5pt solid #eee; }
table.data tbody tr:last-child td { border-bottom: none; }

.formula-box { background: #f5f5f5; padding: 8pt 12pt; margin: 6pt 0 8pt; border-radius: 1pt; font-size: 9pt; line-height: 1.7; }
.formula-box .formula { font-weight: 700; font-size: 10pt; }

.summary-box { border: 1pt solid #1a1a1a; padding: 10pt 14pt; margin-top: 6pt; }
.summary-box .stitle { font-size: 9pt; font-weight: 800; margin-bottom: 7pt; letter-spacing: -0.1pt; }
.summary-item { display: flex; gap: 8pt; margin-bottom: 4pt; font-size: 9.5pt; line-height: 1.5; }
.summary-check { flex-shrink: 0; font-weight: 800; }

.rule { border: none; border-top: .5pt solid #ddd; margin: 14pt 0; }

.footer-note { font-size: 7pt; color: #aaa; border-top: .5pt solid #eee; padding-top: 5pt; margin-top: 8pt; line-height: 1.4; }
</style>
</head>
<body>

<!-- COVER HEADER -->
<div class="cover">
  <div class="cover-left">
    <h1>Allgemeine Ern&auml;hrungsempfehlungen</h1>
    <div class="sub">Grundlagen einer ausgewogenen Ern&auml;hrung</div>
  </div>
  <div class="cover-right">
    <div class="logo-wrap">LOGO_PLACEHOLDER</div>
  </div>
</div>

<!-- DISCLAIMER -->
<div class="disclaimer">
  <strong>Wichtiger Hinweis</strong>
  <p>Diese Informationen dienen ausschlie&szlig;lich der allgemeinen Gesundheitsbildung und Information. Sie stellen keine individuelle Ern&auml;hrungsberatung, Ern&auml;hrungstherapie oder medizinische Behandlung dar.</p>
  <p>Die Inhalte basieren auf allgemein anerkannten Grundlagen der Ern&auml;hrungswissenschaft und Sportern&auml;hrung. Sie ersetzen weder die Untersuchung noch die Beratung durch einen Arzt, eine Ern&auml;hrungsfachkraft oder einen Di&auml;tassistenten.</p>
  <p>Bei Erkrankungen, Allergien, Unvertr&auml;glichkeiten, Stoffwechselerkrankungen, Medikamenteneinnahme, Schwangerschaft oder anderen gesundheitlichen Besonderheiten sollte vor einer Ern&auml;hrungsumstellung fachlicher Rat eingeholt werden. Die Umsetzung der Inhalte erfolgt eigenverantwortlich.</p>
</div>

<!-- 1. ENERGIEBEDARF -->
<div class="section">
  <div class="section-title">1 &mdash; Energiebedarf</div>
  <div class="section-heading">Wie viel Energie ben&ouml;tigt der K&ouml;rper?</div>
  <p>Der K&ouml;rper ben&ouml;tigt t&auml;glich Energie f&uuml;r lebenswichtige Funktionen wie Atmung, Herzschlag, Stoffwechsel und Bewegung. Der Grundumsatz beschreibt die Energiemenge in vollst&auml;ndiger Ruhe. Zusammen mit der k&ouml;rperlichen Aktivit&auml;t ergibt sich der t&auml;gliche Gesamtenergiebedarf.</p>
  <div class="sub-heading">Grobe Orientierung f&uuml;r den Grundumsatz</div>
  <div class="formula-box">
    <span class="formula">M&auml;nner:</span> K&ouml;rpergewicht (kg) &times; 24 = kcal pro Tag<br>
    <span class="formula">Frauen:</span> K&ouml;rpergewicht (kg) &times; 22 = kcal pro Tag<br>
    <span style="font-size:8pt;color:#888;">Diese Formel dient lediglich als Orientierung. Der tats&auml;chliche Bedarf kann abh&auml;ngig von Alter, Muskelmasse und Aktivit&auml;tsniveau variieren.</span>
  </div>
  <div class="sub-heading">Aktivit&auml;tsfaktoren</div>
  <table class="data">
    <thead><tr><td>Aktivit&auml;t</td><td>Faktor</td></tr></thead>
    <tbody>
      <tr><td>&Uuml;berwiegend sitzende T&auml;tigkeit</td><td>1,2</td></tr>
      <tr><td>Leicht aktiv</td><td>1,4&ndash;1,5</td></tr>
      <tr><td>M&auml;&szlig;ig aktiv</td><td>1,6&ndash;1,7</td></tr>
      <tr><td>Sehr aktiv</td><td>1,8&ndash;1,9</td></tr>
    </tbody>
  </table>
  <div class="formula-box"><span class="formula">Gesamtenergiebedarf</span> = Grundumsatz &times; Aktivit&auml;tsfaktor</div>
  <div class="sub-heading">M&ouml;gliche Zielanpassungen</div>
  <p><strong>Gewichtsreduktion:</strong> ca. 300&ndash;500 kcal unter dem t&auml;glichen Bedarf<br>
  <strong>Gewichtszunahme:</strong> ca. 200&ndash;300 kcal &uuml;ber dem t&auml;glichen Bedarf</p>
  <p style="font-size:8.5pt;color:#666;">Langfristige und moderate Anpassungen sind meist nachhaltiger als kurzfristige Extremma&szlig;nahmen.</p>
</div>

<hr class="rule">

<!-- 2. MAKRONÄHRSTOFFE -->
<div class="section">
  <div class="section-title">2 &mdash; Makron&auml;hrstoffe</div>
  <div class="section-heading">Die drei Energietr&auml;ger</div>
  <table class="data">
    <thead><tr><td>Makron&auml;hrstoff</td><td>Energiegehalt</td></tr></thead>
    <tbody>
      <tr><td>Eiweiß (Protein)</td><td>4 kcal/g</td></tr>
      <tr><td>Kohlenhydrate</td><td>4 kcal/g</td></tr>
      <tr><td>Fett</td><td>9 kcal/g</td></tr>
    </tbody>
  </table>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10pt;margin-bottom:6pt;">
    <div>
      <div class="sub-heading" style="margin-top:0;">Eiweiß</div>
      <ul>
        <li>Muskelerhalt &amp; -aufbau</li>
        <li>Regeneration</li>
        <li>S&auml;ttigung</li>
      </ul>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Kohlenhydrate</div>
      <ul>
        <li>Energiequelle f&uuml;r Gehirn</li>
        <li>Nervensystem</li>
        <li>Muskulatur</li>
      </ul>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Fette</div>
      <ul>
        <li>Zellmembranen</li>
        <li>Hormonfunktionen</li>
        <li>Vitamine A, D, E, K</li>
      </ul>
    </div>
  </div>
  <div class="formula-box" style="font-size:8.5pt;">
    M&ouml;gliche Orientierung: &nbsp;<strong>Eiweiß 25&ndash;35 %</strong> &nbsp;&middot;&nbsp; <strong>Kohlenhydrate 40&ndash;50 %</strong> &nbsp;&middot;&nbsp; <strong>Fett 20&ndash;30 %</strong><br>
    <span style="color:#888;">Die optimale Verteilung kann individuell unterschiedlich ausfallen.</span>
  </div>
</div>

<hr class="rule">

<!-- 3. EIWEISS -->
<div class="section">
  <div class="section-title">3 &mdash; Eiweiß</div>
  <div class="section-heading">Ein wichtiger Baustoff</div>
  <p>F&uuml;r sportlich aktive Personen werden h&auml;ufig Mengen von etwa <strong>1,6&ndash;2,0 g Protein pro kg K&ouml;rpergewicht</strong> und Tag empfohlen.</p>
  <div class="formula-box">Beispiel 80 kg: ca. <strong>128&ndash;160 g Protein</strong> t&auml;glich</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14pt;margin-bottom:6pt;">
    <div>
      <div class="sub-heading" style="margin-top:0;">Tierische Quellen</div>
      <ul>
        <li>H&auml;hnchenbrust</li><li>Fisch</li><li>Eier</li><li>Magerquark &amp; Skyr</li>
        <li>Naturjoghurt</li><li>Cottage Cheese</li><li>Mageres Rindfleisch</li>
      </ul>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Pflanzliche Quellen</div>
      <ul>
        <li>Tofu &amp; Tempeh</li><li>Seitan</li><li>Linsen</li><li>Kichererbsen</li>
        <li>Bohnen &amp; Edamame</li><li>Quinoa</li>
      </ul>
    </div>
  </div>
  <p style="font-size:8.5pt;color:#666;">F&uuml;r die Muskelproteinsynthese scheinen etwa 20&ndash;40 g hochwertiges Protein pro Mahlzeit ausreichend. Viele Menschen profitieren davon, ihre Eiwei&szlig;zufuhr auf mehrere Mahlzeiten zu verteilen. Proteinshakes k&ouml;nnen eine praktische Erg&auml;nzung sein, sind jedoch nicht zwingend erforderlich.</p>
</div>

<hr class="rule">

<!-- 4. FETTE -->
<div class="section">
  <div class="section-title">4 &mdash; Fette</div>
  <div class="section-heading">Qualit&auml;t vor Menge</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10pt;margin-bottom:6pt;">
    <div>
      <div class="sub-heading" style="margin-top:0;">Einfach unges&auml;ttigt</div>
      <ul><li>Oliven&ouml;l</li><li>Avocado</li><li>Mandeln</li><li>Cashewkerne</li></ul>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Mehrfach unges&auml;ttigt</div>
      <ul><li>Lachs, Hering, Makrele</li><li>Walln&uuml;sse</li><li>Leinsamen</li><li>Chiasamen</li></ul>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Ges&auml;ttigt</div>
      <ul><li>Butter</li><li>Eier</li><li>Fleisch</li><li>Milchprodukte</li></ul>
    </div>
  </div>
  <p style="font-size:8.5pt;color:#666;"><strong style="color:#1a1a1a;">Omega-3:</strong> Regelm&auml;&szlig;iger Verzehr omega-3-reicher Lebensmittel (fettreicher Seefisch, Leinsamen, Walnüsse) ist empfehlenswert. Eine Supplementierung kann mit einem Arzt besprochen werden.</p>
  <p style="font-size:8.5pt;color:#666;"><strong style="color:#1a1a1a;">H&auml;ufig reduzieren:</strong> Stark verarbeitete Fertigprodukte &middot; Fast Food &middot; stark zuckerhaltige Lebensmittel &middot; industrielle Backwaren. Entscheidend ist stets die gesamte Ern&auml;hrungsweise.</p>
</div>

<hr class="rule">

<!-- 5. GEMÜSE & BALLASTSTOFFE -->
<div class="section">
  <div class="section-title">5 &mdash; Gem&uuml;se, Obst &amp; Ballaststoffe</div>
  <div class="section-heading">Vitamine, Mineralstoffe &amp; Verdauung</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14pt;margin-bottom:6pt;">
    <div>
      <p><strong>Empfehlung:</strong> Mindestens 3 Portionen Gem&uuml;se + 2 Portionen Obst t&auml;glich.</p>
      <p><strong>Ballaststoffe:</strong> Mindestens 30 g pro Tag &mdash; aus Vollkornprodukten, H&uuml;lsenfr&uuml;chten, Gem&uuml;se, Obst, N&uuml;ssen und Samen.</p>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Die Teller-Methode</div>
      <ul>
        <li><strong>&frac12; Teller</strong> Gem&uuml;se oder Salat</li>
        <li><strong>&frac14; Teller</strong> Eiwei&szlig;quelle</li>
        <li><strong>&frac14; Teller</strong> Kohlenhydrate (Kartoffeln, Reis, Vollkornnudeln)</li>
      </ul>
    </div>
  </div>
</div>

<hr class="rule">

<!-- 6. NACHHALTIGKEIT -->
<div class="section">
  <div class="section-title">6 &mdash; Nachhaltigkeit</div>
  <div class="section-heading">Langfristige Gewohnheiten statt Perfektion</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14pt;margin-bottom:4pt;">
    <div>
      <ul>
        <li>Ausgewogene Ern&auml;hrung ist wichtiger als einzelne Mahlzeiten.</li>
        <li>Gelegentliche Genussmittel k&ouml;nnen Teil einer ausgewogenen Ern&auml;hrung sein.</li>
        <li>Extreme Verbote sind langfristig h&auml;ufig schwer umzusetzen.</li>
      </ul>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Die 80/20-Regel</div>
      <p style="font-size:9pt;">Etwa 80&nbsp;% ausgewogen gestalten und gleichzeitig Raum f&uuml;r pers&ouml;nliche Vorlieben lassen.</p>
    </div>
  </div>
</div>

<hr class="rule">

<!-- 7. PRAXISTIPPS -->
<div class="section">
  <div class="section-title">7 &mdash; Praxis</div>
  <div class="section-heading">Tipps f&uuml;r den Alltag</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14pt;margin-bottom:6pt;">
    <div>
      <div class="sub-heading" style="margin-top:0;">Mahlzeiten dokumentieren</div>
      <p style="font-size:9pt;">MyFitnessPal oder Cronometer helfen, Portionsgr&ouml;&szlig;en und Essgewohnheiten einzusch&auml;tzen.</p>
      <div class="sub-heading">Meal Prep</div>
      <p style="font-size:9pt;">Vorkochen erleichtert den Alltag und reduziert spontane, weniger ausgewogene Entscheidungen.</p>
      <div class="sub-heading">Restaurantbesuche</div>
      <p style="font-size:9pt;">Eiwei&szlig;quelle w&auml;hlen &middot; Gem&uuml;se erg&auml;nzen &middot; Saucen bei Bedarf separat bestellen.</p>
    </div>
    <div>
      <div class="sub-heading" style="margin-top:0;">Praktische Snacks</div>
      <ul><li>Skyr / Naturjoghurt / Magerquark</li><li>Obst &amp; Gem&uuml;sesticks</li><li>N&uuml;sse</li><li>Hartkochte Eier</li></ul>
      <div class="sub-heading">Familienalltag</div>
      <ul><li>Mehr Gem&uuml;se in bestehende Gerichte</li><li>Eiwei&szlig;quellen erg&auml;nzen</li><li>Portionsgr&ouml;&szlig;en individuell anpassen</li></ul>
    </div>
  </div>
</div>

<hr class="rule">

<!-- ZUSAMMENFASSUNG -->
<div class="summary-box">
  <div class="stitle">Zusammenfassung &mdash; Die f&uuml;nf wichtigsten Punkte</div>
  <div class="summary-item"><span class="summary-check">&#10003;</span><span>Den pers&ouml;nlichen Energiebedarf grob kennen</span></div>
  <div class="summary-item"><span class="summary-check">&#10003;</span><span>Auf eine ausreichende Eiwei&szlig;zufuhr achten</span></div>
  <div class="summary-item"><span class="summary-check">&#10003;</span><span>T&auml;glich Gem&uuml;se, Obst und ballaststoffreiche Lebensmittel integrieren</span></div>
  <div class="summary-item"><span class="summary-check">&#10003;</span><span>Regelm&auml;&szlig;ig omega-3-reiche Lebensmittel verzehren</span></div>
  <div class="summary-item" style="margin-bottom:0;"><span class="summary-check">&#10003;</span><span>Langfristige Gewohnheiten &uuml;ber kurzfristige Di&auml;ten stellen</span></div>
</div>

<p class="footer-note">Mobile Physiotherapie Grausam &mdash; Informationsbroschuere zur allgemeinen Gesundheitsf&ouml;rderung. Kein Ersatz f&uuml;r &auml;rztliche Diagnostik, Therapie oder individuelle Ern&auml;hrungsberatung.</p>

</body>
</html>"""

OUTPUT_PATH = "/home/user/Mobile-Physiotherapie-Grausam/dokumente/Ernaehrungsguide.pdf"
LOGO_PATH   = "/home/user/Mobile-Physiotherapie-Grausam/logo.svg"

def main():
    with open(LOGO_PATH) as f:
        svg = f.read()
    svg_scaled = svg.replace(
        'viewBox="0 0 226.8 66"',
        'viewBox="0 0 226.8 66" style="width:120pt;height:auto;display:block;"',
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
    print(f"Pages: {len(doc)}")
    doc.close()

if __name__ == "__main__":
    main()
