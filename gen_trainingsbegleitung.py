#!/usr/bin/env python3
"""
Generate Therapeutische-Trainingsbegleitung.pdf — 2 A4 pages.
Layout: Logo oben links (groß), Expertise direkt danach (vollständig), kein doppelter Footer.
"""
import tempfile, os
from weasyprint import HTML

TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<style>
@page { size: A4; margin: 20mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 10pt; color: #1a1a1a; line-height: 1.55; }

/* HEADER */
.header { margin-bottom: 14pt; padding-bottom: 10pt; border-bottom: 1.5pt solid #1a1a1a; }
.logo-wrap { margin-bottom: 10pt; }
.logo-wrap svg { width: 31%; height: auto; display: block; }
.header-title h1 { font-size: 19pt; font-weight: 800; letter-spacing: -0.5pt; line-height: 1.1; margin-bottom: 2pt; }
.header-title .tagline { font-size: 9pt; color: #555; font-style: italic; }

/* SECTION TITLE */
.section-title { font-size: 8pt; font-weight: 700; letter-spacing: 1.2pt; text-transform: uppercase; color: #1a1a1a; margin-bottom: 6pt; padding-bottom: 3pt; border-bottom: 0.8pt solid #ccc; break-after: avoid; page-break-after: avoid; }

/* INTRO TEXT */
.intro-text { margin-bottom: 12pt; }
.intro-text p { margin-bottom: 5pt; font-size: 10pt; line-height: 1.6; }
.intro-text p:last-child { margin-bottom: 0; }

/* EXPERTISE */
.expertise-section { margin-bottom: 14pt; break-inside: avoid; page-break-inside: avoid; }
.expertise-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 14pt; row-gap: 4pt; }
.expertise-item { display: flex; align-items: flex-start; gap: 5pt; font-size: 9pt; line-height: 1.4; }
.expertise-dash { flex-shrink: 0; color: #888; margin-top: 0.5pt; }

/* ROTER FADEN */
.red-thread { margin-bottom: 12pt; font-size: 10pt; line-height: 1.6; font-style: italic; color: #333; border-left: 3pt solid #1a1a1a; padding-left: 10pt; }

/* TRAININGSINHALTE */
.inhalt-section { margin-bottom: 12pt; break-inside: avoid; page-break-inside: avoid; }
.inhalt-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; column-gap: 10pt; row-gap: 4pt; margin-bottom: 5pt; }
.inhalt-item { font-size: 8.5pt; line-height: 1.4; display: flex; align-items: flex-start; gap: 4pt; }
.inhalt-dot { flex-shrink: 0; color: #888; }
.inhalt-note { font-size: 7.5pt; color: #888; font-style: italic; }

/* CHECKLIST */
.checklist-section { margin-bottom: 12pt; break-inside: avoid; page-break-inside: avoid; }
.checklist-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 14pt; row-gap: 4pt; }
.checklist-item { display: flex; align-items: flex-start; gap: 4pt; font-size: 9.5pt; }
.check-mark { color: #1a1a1a; font-weight: 700; flex-shrink: 0; margin-top: 0.5pt; }

/* FLOW */
.flow-section { margin-bottom: 12pt; break-inside: avoid; page-break-inside: avoid; }
.flow-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; column-gap: 8pt; }
.flow-step { border: 0.8pt solid #ccc; padding: 8pt 9pt; border-radius: 2pt; }
.flow-step-label { font-size: 7pt; font-weight: 700; letter-spacing: 0.8pt; text-transform: uppercase; color: #777; margin-bottom: 3pt; }
.flow-step-title { font-size: 9pt; font-weight: 700; margin-bottom: 3pt; line-height: 1.2; }
.flow-step-text { font-size: 8pt; color: #444; line-height: 1.4; }

/* PRICE */
.price-section { margin-bottom: 12pt; break-inside: avoid; page-break-inside: avoid; }
.price-block { background: #1a1a1a; color: #fff; padding: 8pt 11pt; border-radius: 2pt; display: flex; align-items: center; justify-content: space-between; gap: 12pt; }
.price-left { display: flex; align-items: baseline; gap: 4pt; }
.price-amount { font-size: 32pt; font-weight: 800; line-height: 1; letter-spacing: -1pt; }
.price-currency { font-size: 18pt; font-weight: 700; align-self: flex-start; margin-top: 4pt; }
.price-meta { display: flex; flex-direction: column; gap: 1pt; }
.price-per-month { font-size: 8.5pt; color: #ccc; }
.price-per-hour { font-size: 8pt; color: #aaa; }
.price-compare { font-size: 7.5pt; color: #bbb; border-left: 1pt solid #444; padding-left: 12pt; max-width: 170pt; line-height: 1.35; }
.price-footnote { font-size: 6.5pt; color: #999; margin-top: 3pt; line-height: 1.3; }

/* FAQ */
.faq-section { margin-bottom: 12pt; break-inside: avoid; page-break-inside: avoid; }
.faq-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 14pt; row-gap: 7pt; }
.faq-item { break-inside: avoid; page-break-inside: avoid; }
.faq-item dt { font-size: 9pt; font-weight: 700; margin-bottom: 2pt; line-height: 1.3; }
.faq-item dd { font-size: 9pt; color: #333; line-height: 1.45; margin-left: 0; }

/* CTA */
.cta-section { margin-bottom: 12pt; break-inside: avoid; page-break-inside: avoid; }
.cta-box { border: 1.5pt solid #1a1a1a; padding: 8pt 11pt; border-radius: 2pt; display: flex; justify-content: space-between; align-items: center; gap: 16pt; }
.cta-left h3 { font-size: 10.5pt; font-weight: 800; margin-bottom: 3pt; letter-spacing: -0.2pt; }
.cta-left p { font-size: 8.5pt; color: #444; line-height: 1.4; }
.cta-right { text-align: right; flex-shrink: 0; }
.cta-right .contact-name { font-size: 9pt; font-weight: 700; margin-bottom: 2pt; }
.cta-right .contact-detail { font-size: 8.5pt; color: #333; line-height: 1.5; }

/* LEGAL */
.legal-box { background: #f3f3f3; border: 0.5pt solid #ddd; padding: 4pt 7pt; border-radius: 2pt; margin-bottom: 5pt; }
.legal-box p { font-size: 7pt; color: #555; line-height: 1.3; }
.legal-box p + p { margin-top: 2pt; }

/* FOOTNOTE */
.footer-block { font-size: 6.5pt; color: #888; line-height: 1.35; border-top: 0.5pt solid #ddd; padding-top: 4pt; }
</style>
</head>
<body>

<!-- HEADER: Logo oben, Titel darunter -->
<div class="header">
  <div class="logo-wrap">LOGO_PLACEHOLDER</div>
  <div class="header-title">
    <h1>Therapeutische Trainingsbegleitung</h1>
    <div class="tagline">Von der Behandlung zur&uuml;ck in einen belastbaren Alltag.</div>
  </div>
</div>

<!-- INTRO TEXT -->
<div class="intro-text">
  <p>Viele Beschwerden kommen zur&uuml;ck &mdash; nicht wegen fehlender Behandlung, sondern weil im Alltag niemand mehr begleitet. Die Physiotherapie endet nach 45 oder 60 Minuten. Was danach kommt, entscheidet genauso &uuml;ber den Erfolg.</p>
  <p>Ich bin kein Personal Trainer mit Trainerschein &mdash; ich bin Physiotherapeut mit medizinischem Blick, klinischer Berufserfahrung und eigenem Leistungssportbackground. Diese Verbindung aus Therapiehintergrund, Training und pers&ouml;nlicher Begleitung macht den Unterschied.</p>
</div>

<!-- MEINE EXPERTISE (chronologisch) -->
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

<!-- ROTER FADEN -->
<p class="red-thread">Genau diese Kombination &mdash; medizinisches Fachwissen, eigene Verletzungserfahrung und Leistungssportbackground &mdash; ist der rote Faden hinter allem, was ich tue.</p>

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

<!-- TRAININGSINHALTE (Beispiel) -->
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
  <div class="inhalt-note">Die genauen Inhalte sind frei w&auml;hlbar und werden gemeinsam im Erstgespr&auml;ch festgelegt &mdash; das Beispiel oben zeigt, was m&ouml;glich ist.</div>
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
        <div class="price-per-hour">= 37,50 &euro; pro Stunde</div>
      </div>
    </div>
    <div class="price-compare">Personal Trainer ohne medizinischen Hintergrund: 60&ndash;90&nbsp;&euro;&nbsp;/ Stunde. Hier: Fachwissen mit therapeutischem Hintergrund + pers&ouml;nliches Training + dauerhafte Begleitung.</div>
  </div>
  <div class="price-footnote">* Nettobetrag. Steuerliche Behandlung (Kleinunternehmerregelung &sect;&nbsp;19 UStG oder Regelbesteuerung) auf Anfrage. Nicht steuerbefreit nach &sect;&nbsp;4 Nr.&nbsp;14 UStG.</div>
</div>

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
      <div class="contact-name">Nick Grausam</div>
      <div class="contact-detail">0176 4268 5146</div>
      <div class="contact-detail">info@physiotherapie-grausam.com</div>
    </div>
  </div>
</div>

<!-- LEGAL -->
<div class="legal-box">
  <p><strong>Rechtlicher Hinweis:</strong> Die angebotene Trainingsbegleitung ist eine pers&ouml;nliche Trainings- und Begleitungsleistung und stellt keine Heilbehandlung, keine Physiotherapie auf &auml;rztliche Verordnung und keinen Ersatz f&uuml;r &auml;rztliche oder physiotherapeutische Behandlung dar. Die Leistung wird auf eigene Initiative des Kunden erbracht. Bei akuten medizinischen Beschwerden wenden Sie sich bitte an einen Arzt.</p>
  <p>Die Trainingsbegleitung f&auml;llt nicht unter die Steuerbefreiung nach &sect;&nbsp;4 Nr.&nbsp;14 UStG. Die steuerliche Behandlung wird auf Anfrage mitgeteilt.</p>
</div>

<!-- FOOTNOTE ONLY — kein doppelter Kontakt -->
<div class="footer-block">
  <p>** Ern&auml;hrungsempfehlungen basieren auf pers&ouml;nlicher Erfahrung und eigener Recherche &mdash; nicht auf einer Weiterbildung als Ern&auml;hrungsberater. Vollst&auml;ndig optional, auf ausdr&uuml;cklichen Wunsch verf&uuml;gbar.</p>
</div>

</body>
</html>"""

OUTPUT_PATH = "/home/user/Mobile-Physiotherapie-Grausam/dokumente/Therapeutische-Trainingsbegleitung.pdf"
LOGO_PATH   = "/home/user/Mobile-Physiotherapie-Grausam/logo.svg"

def main():
    with open(LOGO_PATH) as f:
        svg = f.read()
    # Inject height via style attribute on the root svg element
    svg_scaled = svg.replace(
        'viewBox="0 0 226.8 66"',
        'viewBox="0 0 226.8 66" style="width:31%;height:auto;display:block;"',
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
