#!/usr/bin/env python3
"""
Generate Therapeutische-Trainingsbegleitung.pdf — 2 A4 pages.
"""
import tempfile, os
from weasyprint import HTML

TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<style>
@page { size: A4; margin: 15mm 18mm; border-top: 2.5pt solid #1a1a1a; border-bottom: 2.5pt solid #1a1a1a; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 10pt; color: #1a1a1a; line-height: 1.62; }

/* HEADER */
.header { display: flex; align-items: flex-end; justify-content: space-between; gap: 16pt; padding-bottom: 11pt; margin-bottom: 18pt; border-bottom: 1pt solid #1a1a1a; }
.logo-wrap svg { width: 34%; height: auto; display: block; }
.header-right { text-align: right; }
.header-right h1 { font-size: 19pt; font-weight: 800; letter-spacing: -0.5pt; line-height: 1.05; margin-bottom: 3pt; }
.header-right .tagline { font-size: 9pt; color: #666; font-style: italic; }

/* SECTION TITLE */
.section-title { font-size: 7.5pt; font-weight: 700; letter-spacing: 2.5pt; text-transform: uppercase; color: #999; margin-bottom: 10pt; break-after: avoid; page-break-after: avoid; }

/* INTRO */
.intro-text { margin-bottom: 17pt; }
.intro-text p { margin-bottom: 8pt; font-size: 10pt; line-height: 1.65; }
.intro-text p:last-child { margin-bottom: 0; }

/* EXPERTISE */
.expertise-section { margin-bottom: 17pt; }
.expertise-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 18pt; row-gap: 7pt; }
.expertise-item { display: flex; align-items: flex-start; gap: 7pt; font-size: 9.5pt; line-height: 1.45; }
.expertise-dash { flex-shrink: 0; color: #bbb; }

/* RED THREAD */
.red-thread { margin-bottom: 17pt; font-size: 10.5pt; line-height: 1.65; font-style: italic; color: #1a1a1a; padding: 11pt 12pt; border-top: 0.5pt solid #ccc; border-bottom: 0.5pt solid #ccc; text-align: center; }

/* CHECKLIST */
.checklist-section { margin-bottom: 17pt; }
.checklist-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 18pt; row-gap: 7pt; }
.checklist-item { display: flex; align-items: flex-start; gap: 7pt; font-size: 10pt; }
.check-mark { flex-shrink: 0; font-weight: 800; color: #1a1a1a; margin-top: 0.5pt; }

/* TRAININGSINHALTE */
.inhalt-section { margin-bottom: 17pt; }
.inhalt-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; column-gap: 12pt; row-gap: 6pt; margin-bottom: 6pt; }
.inhalt-item { font-size: 9.5pt; line-height: 1.45; display: flex; align-items: flex-start; gap: 5pt; }
.inhalt-dot { flex-shrink: 0; color: #bbb; }
.inhalt-note { font-size: 8pt; color: #999; font-style: italic; }

/* FLOW */
.flow-section { margin-bottom: 17pt; }
.flow-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; column-gap: 11pt; }
.flow-step { border-top: 1.5pt solid #1a1a1a; padding-top: 8pt; }
.flow-step-label { font-size: 7pt; font-weight: 700; letter-spacing: 1pt; text-transform: uppercase; color: #999; margin-bottom: 4pt; }
.flow-step-title { font-size: 9pt; font-weight: 700; margin-bottom: 4pt; line-height: 1.2; }
.flow-step-text { font-size: 8.5pt; color: #555; line-height: 1.45; }

/* PRICE */
.price-section { margin-bottom: 5pt; }
.price-block { background: #1a1a1a; color: #fff; padding: 13pt 16pt; display: flex; align-items: center; justify-content: space-between; gap: 14pt; }
.price-left { display: flex; align-items: baseline; gap: 3pt; }
.price-amount { font-size: 38pt; font-weight: 800; line-height: 1; letter-spacing: -2pt; }
.price-currency { font-size: 20pt; font-weight: 700; align-self: flex-start; margin-top: 5pt; }
.price-meta { margin-left: 8pt; }
.price-per-month { font-size: 9pt; color: #bbb; }
.price-per-hour { font-size: 8pt; color: #999; }
.price-compare { font-size: 8.5pt; color: #bbb; border-left: 0.5pt solid #444; padding-left: 14pt; max-width: 175pt; line-height: 1.5; }
.price-footnote { font-size: 6.5pt; color: #888; margin-top: 4pt; line-height: 1.3; margin-bottom: 17pt; }

/* FAQ */
.faq-section { margin-bottom: 17pt; }
.faq-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 18pt; row-gap: 10pt; }
.faq-item { break-inside: avoid; page-break-inside: avoid; }
.faq-item dt { font-size: 9.5pt; font-weight: 700; margin-bottom: 2.5pt; line-height: 1.3; }
.faq-item dd { font-size: 9pt; color: #444; line-height: 1.5; margin-left: 0; }

/* CTA */
.cta-section { margin-bottom: 17pt; }
.cta-box { border: 1pt solid #1a1a1a; padding: 11pt 15pt; display: flex; justify-content: space-between; align-items: center; gap: 16pt; }
.cta-left h3 { font-size: 11pt; font-weight: 800; margin-bottom: 4pt; letter-spacing: -0.2pt; }
.cta-left p { font-size: 9pt; color: #555; line-height: 1.5; }
.cta-right { text-align: right; flex-shrink: 0; }
.cta-right .cname { font-size: 9.5pt; font-weight: 700; margin-bottom: 3pt; }
.cta-right .cdetail { font-size: 9pt; color: #444; line-height: 1.65; }

/* LEGAL + FOOTNOTE */
.legal { font-size: 7pt; color: #777; line-height: 1.45; margin-bottom: 4pt; }
.footnote { font-size: 6.5pt; color: #aaa; line-height: 1.3; border-top: 0.5pt solid #eee; padding-top: 3pt; }
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="logo-wrap">LOGO_PLACEHOLDER</div>
  <div class="header-right">
    <h1>Therapeutische Trainingsbegleitung</h1>
    <div class="tagline">Von der Behandlung zur&uuml;ck in einen belastbaren Alltag.</div>
  </div>
</div>

<!-- INTRO -->
<div class="intro-text">
  <p>Viele Beschwerden kommen zur&uuml;ck &mdash; nicht wegen fehlender Behandlung, sondern weil im Alltag niemand mehr begleitet. Die Physiotherapie endet nach 45 oder 60 Minuten. Was danach kommt, entscheidet genauso &uuml;ber den Erfolg.</p>
  <p>Ich bin kein Personal Trainer mit Trainerschein &mdash; ich bin Physiotherapeut mit medizinischem Blick, klinischer Berufserfahrung und eigenem Leistungssportbackground. Diese Verbindung macht den Unterschied.</p>
</div>

<!-- EXPERTISE -->
<div class="expertise-section">
  <div class="section-title">Meine Expertise</div>
  <div class="expertise-grid">
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Leistungshandball im NLZ der Rhein-Neckar L&ouml;wen (Handball-Bundesliga)</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Kraft- &amp; Athletiktraining ab dem 13. Lebensjahr bei den Rhein-Neckar L&ouml;wen</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Technikschulung durch Trainer aus dem olympischen Gewichtheben</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Eigene Verletzungserfahrung &mdash; Training trotz und mit Einschr&auml;nkungen</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Qualifikation: Krankengymnastik am Ger&auml;t (KGG)</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Fortbildung beim langjährigen Physiotherapeuten der deutschen Fu&szlig;ballnationalmannschaft</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Stetige Weiterbildung in Therapie, Training und Sport</span></div>
    <div class="expertise-item"><span class="expertise-dash">&ndash;</span><span>Jung und motiviert</span></div>
  </div>
</div>

<!-- RED THREAD -->
<div class="red-thread">Genau diese Kombination &mdash; medizinisches Fachwissen, eigene Verletzungserfahrung und Leistungssportbackground &mdash; ist der rote Faden hinter allem, was ich tue.</div>

<!-- WAS SIE BEKOMMEN -->
<div class="checklist-section">
  <div class="section-title">Was Sie bekommen</div>
  <div class="checklist-grid">
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>4 pers&ouml;nliche Termine &agrave; 60 Min. pro Monat</span></div>
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>Schriftlicher, individueller Trainingsplan</span></div>
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>WhatsApp-Erreichbarkeit zwischen den Terminen</span></div>
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>Monatliche Plananpassung</span></div>
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>Fachwissen mit therapeutischem Hintergrund</span></div>
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>Ern&auml;hrungsempfehlungen auf Wunsch**</span></div>
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>Kostenloses Erstgespr&auml;ch zum Kennenlernen</span></div>
    <div class="checklist-item"><span class="check-mark">&#10003;</span><span>Keine Vorauszahlung &mdash; monatlich k&uuml;ndbar</span></div>
  </div>
</div>

<!-- TRAININGSINHALTE -->
<div class="inhalt-section">
  <div class="section-title">M&ouml;gliche Trainingsinhalte &mdash; Beispiel</div>
  <div class="inhalt-grid">
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Kraft &amp; Muskelaufbau</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Mobilit&auml;t &amp; Beweglichkeit</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Koordination &amp; Balance</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>R&uuml;cken &amp; Haltung</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Ausdauer &amp; Kondition</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Verletzungspr&auml;vention</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Rehabilitation &amp; Wiederbelastung</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Atemtechnik &amp; Entspannung</span></div>
    <div class="inhalt-item"><span class="inhalt-dot">&ndash;</span><span>Alltagsbewegungen verbessern</span></div>
  </div>
  <div class="inhalt-note">Die genauen Inhalte sind frei w&auml;hlbar &mdash; das Beispiel zeigt, was m&ouml;glich ist.</div>
</div>

<!-- WIE ES ABLÄUFT -->
<div class="flow-section">
  <div class="section-title">Wie es abl&auml;uft</div>
  <div class="flow-grid">
    <div class="flow-step">
      <div class="flow-step-label">Schritt 0 &middot; kostenlos</div>
      <div class="flow-step-title">Erstgespr&auml;ch</div>
      <div class="flow-step-text">Kennenlernen, Ihre Situation, Ihre Ziele &mdash; unverbindlich. Erst danach entscheiden Sie.</div>
    </div>
    <div class="flow-step">
      <div class="flow-step-label">Einheit 1</div>
      <div class="flow-step-title">Analyse &amp; Planung</div>
      <div class="flow-step-text">Bewegungsanalyse, Zieldefinition, Ern&auml;hrungsgrundlagen, individueller Trainingsplan.</div>
    </div>
    <div class="flow-step">
      <div class="flow-step-label">Einheiten 2&ndash;3</div>
      <div class="flow-step-title">Pers&ouml;nliches Training</div>
      <div class="flow-step-text">Abgestimmt auf Ihren K&ouml;rper und Ihr Ziel &mdash; kein Standard-Programm, kein Druck.</div>
    </div>
    <div class="flow-step">
      <div class="flow-step-label">Laufend</div>
      <div class="flow-step-title">Begleitung &amp; Anpassung</div>
      <div class="flow-step-text">WhatsApp zwischen Terminen, monatliche Plananpassung &mdash; damit der Fortschritt h&auml;lt.</div>
    </div>
  </div>
</div>

<!-- PREIS -->
<div class="price-section">
  <div class="price-block">
    <div class="price-left">
      <div class="price-currency">&euro;</div>
      <div class="price-amount">150</div>
      <div class="price-meta">
        <div class="price-per-month">pro Monat*</div>
        <div class="price-per-hour">= 37,50 &euro;&nbsp;/ Stunde</div>
      </div>
    </div>
    <div class="price-compare">Personal Trainer ohne medizinischen Hintergrund: 60&ndash;90&nbsp;&euro;&nbsp;/ Stunde. Hier: Fachwissen mit therapeutischem Hintergrund + pers&ouml;nliches Training + dauerhafte Begleitung.</div>
  </div>
</div>
<div class="price-footnote">* Nettobetrag. Steuerliche Behandlung (Kleinunternehmerregelung &sect;&nbsp;19 UStG oder Regelbesteuerung) auf Anfrage. Nicht steuerbefreit nach &sect;&nbsp;4 Nr.&nbsp;14 UStG.</div>

<!-- FAQ -->
<div class="faq-section">
  <div class="section-title">H&auml;ufige Fragen</div>
  <dl class="faq-grid">
    <div class="faq-item"><dt>F&uuml;r wen ist das geeignet?</dt><dd>F&uuml;r jeden, der sich langfristig besser bewegen m&ouml;chte &mdash; nach einer Verletzung, mitten in der Therapie oder pr&auml;ventiv. Keine Vorkenntnisse n&ouml;tig.</dd></div>
    <div class="faq-item"><dt>Kann ich mit Schmerzen trainieren?</dt><dd>Ja &mdash; das Training wird an Ihren K&ouml;rper angepasst. Sie trainieren mit mir, nicht gegen Ihren K&ouml;rper. Bei akuten Beschwerden zuerst den Arzt aufsuchen.</dd></div>
    <div class="faq-item"><dt>Wo findet das Training statt?</dt><dd>Individuell abgestimmt: bei Ihnen zu Hause, im Freien oder im Fitnessstudio &mdash; je nach Situation.</dd></div>
    <div class="faq-item"><dt>Muss ich schon sportlich aktiv sein?</dt><dd>Nein. Wir starten dort, wo Sie stehen &mdash; ohne Druck, ohne Voraussetzungen.</dd></div>
    <div class="faq-item"><dt>Wie l&auml;uft der Einstieg ab?</dt><dd>Kostenloses Erstgespr&auml;ch &mdash; kein Vertrag, keine Vorauszahlung. Erst nach der ersten Einheit entscheiden Sie.</dd></div>
    <div class="faq-item"><dt>Wie lange l&auml;uft das Coaching?</dt><dd>Monatlich ohne Mindestlaufzeit. K&uuml;ndigung formlos per Nachricht, jederzeit m&ouml;glich.</dd></div>
  </dl>
</div>

<!-- CTA -->
<div class="cta-section">
  <div class="cta-box">
    <div class="cta-left">
      <h3>Kostenloses Erstgespr&auml;ch</h3>
      <p>Einfach anrufen oder eine Nachricht schicken &mdash; wir schauen gemeinsam, ob die Trainingsbegleitung zu Ihrer Situation passt. Kein Vertrag, kein Druck.</p>
    </div>
    <div class="cta-right">
      <div class="cname">Nick Grausam</div>
      <div class="cdetail">0176 4268 5146<br>info@physiotherapie-grausam.com</div>
    </div>
  </div>
</div>

<!-- LEGAL + FOOTNOTE -->
<p class="legal"><strong>Rechtlicher Hinweis:</strong> Die Trainingsbegleitung ist eine pers&ouml;nliche Trainingsleistung &mdash; keine Heilbehandlung, keine Physiotherapie auf Verordnung und kein Ersatz f&uuml;r &auml;rztliche Behandlung. Bei akuten medizinischen Beschwerden bitte zun&auml;chst einen Arzt aufsuchen. Nicht steuerbefreit nach &sect;&nbsp;4 Nr.&nbsp;14 UStG.</p>
<p class="footnote">** Ern&auml;hrungsempfehlungen basieren auf pers&ouml;nlicher Erfahrung &mdash; kein Ersatz f&uuml;r ern&auml;hrungsmedizinische Fachberatung. Vollst&auml;ndig optional.</p>

</body>
</html>"""

OUTPUT_PATH = "/home/user/Mobile-Physiotherapie-Grausam/dokumente/Therapeutische-Trainingsbegleitung.pdf"
LOGO_PATH   = "/home/user/Mobile-Physiotherapie-Grausam/logo.svg"

def main():
    with open(LOGO_PATH) as f:
        svg = f.read()
    svg_scaled = svg.replace(
        'viewBox="0 0 226.8 66"',
        'viewBox="0 0 226.8 66" style="width:130pt;height:auto;display:block;"',
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

if __name__ == "__main__":
    main()
