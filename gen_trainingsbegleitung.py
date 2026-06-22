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
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 9.5pt; color: #1a1a1a; line-height: 1.55; }

/* ── DARK HEADER ── */
.flyer-header { background: #1a1a1a; padding: 11mm 16mm 10mm; display: flex; align-items: center; justify-content: space-between; gap: 20pt; }
.flyer-logo-box { background: #ffffff; padding: 5pt 10pt 4pt; display: inline-block; }
.flyer-logo-box svg { width: 120pt; height: auto; display: block; }
.flyer-header-right { text-align: right; }
.flyer-header-right h1 { font-size: 20pt; font-weight: 800; color: #ffffff; letter-spacing: -0.5pt; line-height: 1.05; margin-bottom: 4pt; }
.flyer-header-right .tagline { font-size: 8.5pt; color: #aaaaaa; font-style: italic; }

/* ── BODY PADDING ── */
.body { padding: 11mm 16mm 10mm; }

/* ── SECTION TITLE ── */
.section-title { font-size: 7pt; font-weight: 700; letter-spacing: 2pt; text-transform: uppercase; color: #1a1a1a; margin-bottom: 7pt; padding-left: 8pt; border-left: 3pt solid #1a1a1a; break-after: avoid; page-break-after: avoid; }

/* ── SECTION BLOCK ── */
.sec { margin-bottom: 13pt; }
.sec.avoid { break-inside: avoid; page-break-inside: avoid; }

/* ── INTRO ── */
.intro p { font-size: 10pt; line-height: 1.65; margin-bottom: 5pt; }
.intro p:last-child { margin-bottom: 0; }

/* ── PULL QUOTE (roter Faden) ── */
.pull-quote { font-size: 11pt; font-style: italic; font-weight: 600; color: #1a1a1a; line-height: 1.5; text-align: center; padding: 10pt 0; border-top: 1pt solid #1a1a1a; border-bottom: 1pt solid #1a1a1a; margin-bottom: 13pt; break-inside: avoid; page-break-inside: avoid; }

/* ── EXPERTISE ── */
.expertise-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 16pt; row-gap: 5pt; }
.expertise-item { display: flex; align-items: flex-start; gap: 6pt; font-size: 9pt; line-height: 1.4; }
.expertise-dash { flex-shrink: 0; font-weight: 700; color: #1a1a1a; margin-top: 0.5pt; }

/* ── CHECKLIST ── */
.checklist-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 16pt; row-gap: 5pt; }
.checklist-item { display: flex; align-items: flex-start; gap: 6pt; font-size: 9.5pt; }
.check-mark { flex-shrink: 0; font-weight: 800; font-size: 10pt; color: #1a1a1a; margin-top: 0.5pt; }

/* ── TRAININGSINHALTE ── */
.inhalt-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; column-gap: 10pt; row-gap: 4pt; margin-bottom: 5pt; }
.inhalt-item { font-size: 8.5pt; line-height: 1.4; display: flex; align-items: flex-start; gap: 4pt; }
.inhalt-dot { flex-shrink: 0; color: #888; }
.inhalt-note { font-size: 7.5pt; color: #888; font-style: italic; margin-top: 4pt; }

/* ── FLOW ── */
.flow-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; column-gap: 7pt; }
.flow-step { border-top: 2.5pt solid #1a1a1a; padding-top: 6pt; }
.flow-step-num { font-size: 18pt; font-weight: 800; color: #e8e8e8; line-height: 1; margin-bottom: 2pt; }
.flow-step-title { font-size: 8.5pt; font-weight: 700; margin-bottom: 3pt; line-height: 1.2; }
.flow-step-text { font-size: 7.5pt; color: #555; line-height: 1.4; }

/* ── PRICE BAND ── */
.price-band { background: #1a1a1a; color: #fff; padding: 10pt 14pt; display: flex; align-items: center; justify-content: space-between; gap: 14pt; margin-bottom: 4pt; break-inside: avoid; page-break-inside: avoid; }
.price-left { display: flex; align-items: baseline; gap: 3pt; }
.price-amount { font-size: 38pt; font-weight: 800; line-height: 1; letter-spacing: -2pt; }
.price-currency { font-size: 20pt; font-weight: 700; align-self: flex-start; margin-top: 5pt; }
.price-meta { font-size: 8pt; color: #bbb; margin-top: 2pt; }
.price-divider { width: 1pt; background: #444; align-self: stretch; flex-shrink: 0; }
.price-right { font-size: 8pt; color: #bbb; line-height: 1.5; max-width: 200pt; }
.price-right strong { color: #fff; font-size: 9pt; display: block; margin-bottom: 3pt; }
.price-note { font-size: 6.5pt; color: #888; line-height: 1.3; margin-bottom: 13pt; }

/* ── FAQ ── */
.faq-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 16pt; row-gap: 6pt; }
.faq-item { break-inside: avoid; page-break-inside: avoid; }
.faq-item dt { font-size: 8.5pt; font-weight: 700; margin-bottom: 1.5pt; }
.faq-item dd { font-size: 8.5pt; color: #444; line-height: 1.45; margin-left: 0; }

/* ── CTA BAND ── */
.cta-band { background: #1a1a1a; color: #fff; padding: 10pt 14pt; display: flex; align-items: center; justify-content: space-between; gap: 16pt; margin-bottom: 7pt; break-inside: avoid; page-break-inside: avoid; }
.cta-left h3 { font-size: 12pt; font-weight: 800; letter-spacing: -0.3pt; margin-bottom: 3pt; }
.cta-left p { font-size: 8pt; color: #ccc; line-height: 1.5; }
.cta-right { text-align: right; flex-shrink: 0; }
.cta-right .cname { font-size: 9.5pt; font-weight: 700; margin-bottom: 3pt; }
.cta-right .cdetail { font-size: 8.5pt; color: #ccc; line-height: 1.6; }

/* ── LEGAL + FOOTNOTE ── */
.legal { font-size: 6.5pt; color: #777; line-height: 1.35; margin-bottom: 5pt; }
.footnote { font-size: 6pt; color: #aaa; line-height: 1.3; border-top: 0.5pt solid #ddd; padding-top: 4pt; }
</style>
</head>
<body>

<!-- ══ DARK HEADER ══ -->
<div class="flyer-header">
  <div class="flyer-logo-box">LOGO_PLACEHOLDER</div>
  <div class="flyer-header-right">
    <h1>Therapeutische<br>Trainingsbegleitung</h1>
    <div class="tagline">Von der Behandlung zur&uuml;ck in einen belastbaren Alltag.</div>
  </div>
</div>

<div class="body">

<!-- ══ INTRO ══ -->
<div class="sec">
  <div class="intro">
    <p>Viele Beschwerden kommen zur&uuml;ck &mdash; nicht wegen fehlender Behandlung, sondern weil im Alltag niemand mehr begleitet. Die Physiotherapie endet nach 45 oder 60 Minuten. Was danach kommt, entscheidet genauso &uuml;ber den Erfolg.</p>
    <p>Ich bin kein Personal Trainer mit Trainerschein &mdash; ich bin Physiotherapeut mit medizinischem Blick, klinischer Berufserfahrung und eigenem Leistungssportbackground. Diese Verbindung macht den Unterschied.</p>
  </div>
</div>

<!-- ══ EXPERTISE ══ -->
<div class="sec avoid">
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

<!-- ══ PULL QUOTE (roter Faden) ══ -->
<div class="pull-quote">
  Genau diese Kombination &mdash; medizinisches Fachwissen, eigene Verletzungserfahrung und Leistungssportbackground &mdash; ist der rote Faden hinter allem, was ich tue.
</div>

<!-- ══ WAS SIE BEKOMMEN ══ -->
<div class="sec avoid">
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

<!-- ══ TRAININGSINHALTE ══ -->
<div class="sec avoid">
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

<!-- ══ WIE ES ABLÄUFT ══ -->
<div class="sec avoid">
  <div class="section-title">Wie es abl&auml;uft</div>
  <div class="flow-grid">
    <div class="flow-step">
      <div class="flow-step-num">0</div>
      <div class="flow-step-title">Erstgespr&auml;ch &middot; kostenlos</div>
      <div class="flow-step-text">Kennenlernen, Ihre Situation, Ihre Ziele &mdash; unverbindlich. Erst danach entscheiden Sie.</div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">1</div>
      <div class="flow-step-title">Analyse &amp; Planung</div>
      <div class="flow-step-text">Bewegungsanalyse, Zieldefinition, Ern&auml;hrungsgrundlagen, individueller Trainingsplan.</div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">2&ndash;3</div>
      <div class="flow-step-title">Pers&ouml;nliches Training</div>
      <div class="flow-step-text">Abgestimmt auf Ihren K&ouml;rper und Ihr Ziel &mdash; kein Standard-Programm, kein Druck.</div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">&infin;</div>
      <div class="flow-step-title">Begleitung &amp; Anpassung</div>
      <div class="flow-step-text">WhatsApp zwischen Terminen, monatliche Plananpassung &mdash; damit der Fortschritt h&auml;lt.</div>
    </div>
  </div>
</div>

<!-- ══ PREIS ══ -->
<div class="price-band">
  <div class="price-left">
    <div class="price-currency">&euro;</div>
    <div class="price-amount">150</div>
    <div style="margin-left:8pt;">
      <div class="price-meta">pro Monat*</div>
      <div class="price-meta">= 37,50 &euro;&nbsp;/ Stunde</div>
    </div>
  </div>
  <div class="price-divider"></div>
  <div class="price-right">
    <strong>Was Sie woanders zahlen w&uuml;rden:</strong>
    Personal Trainer ohne med. Hintergrund: 60&ndash;90&nbsp;&euro;&nbsp;/ Stunde.<br>
    Hier: Therapeutisches Fachwissen + pers&ouml;nliches Training + dauerhafte Begleitung.
  </div>
</div>
<div class="price-note">* Nettobetrag. Steuerliche Behandlung (Kleinunternehmerregelung &sect;&nbsp;19 UStG oder Regelbesteuerung) auf Anfrage. Nicht steuerbefreit nach &sect;&nbsp;4 Nr.&nbsp;14 UStG.</div>

<!-- ══ FAQ ══ -->
<div class="sec avoid">
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

<!-- ══ CTA BAND ══ -->
<div class="cta-band">
  <div class="cta-left">
    <h3>Kostenloses Erstgespr&auml;ch</h3>
    <p>Einfach anrufen oder schreiben &mdash; wir schauen gemeinsam, ob die Trainingsbegleitung passt.<br>Kein Vertrag, kein Druck.</p>
  </div>
  <div class="cta-right">
    <div class="cname">Nick Grausam</div>
    <div class="cdetail">0176 4268 5146<br>info@physiotherapie-grausam.com</div>
  </div>
</div>

<!-- ══ LEGAL + FOOTNOTE ══ -->
<p class="legal"><strong>Rechtlicher Hinweis:</strong> Die Trainingsbegleitung ist eine pers&ouml;nliche Trainingsleistung &mdash; keine Heilbehandlung, keine Physiotherapie auf Verordnung und kein Ersatz f&uuml;r &auml;rztliche Behandlung. Bei akuten medizinischen Beschwerden bitte zun&auml;chst einen Arzt aufsuchen. Nicht steuerbefreit nach &sect;&nbsp;4 Nr.&nbsp;14 UStG.</p>
<p class="footnote">** Ern&auml;hrungsempfehlungen basieren auf pers&ouml;nlicher Erfahrung &mdash; kein Ersatz f&uuml;r ern&auml;hrungsmedizinische Fachberatung. Vollst&auml;ndig optional.</p>

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
    n = len(doc)
    doc.close()
    print(f"Pages: {n}")

if __name__ == "__main__":
    main()
