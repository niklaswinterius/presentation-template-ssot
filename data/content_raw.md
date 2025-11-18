
# Projekt: Automatisierte Präsentation – Task Force KI, GenAI & Agentic AI (SAP/ABAP)

Dieses Dokument ist die **einzige inhaltliche Quelle** (content_raw) für das Pitch Deck.
Alle Layout-Informationen kommen **ausschließlich** aus dem SSOT-JSON.

---

## A. Meta-Guidelines (für Ebene B – Content-Normalisierung)

- Ziel: 12–14 Folien, ca. 30 Minuten Management-Präsentation.
- Zielgruppe: Michael Kienzig (Vice President, Körber Supply Chain).
- Ton: kritisch, faktenbasiert, ohne Marketing-Blabla.
- Struktur: Problem → Kontext → Lösung (Task Force) → Roadmap → Business Case → Entscheidung.

**Content-Typen, die der Normalisierungs-Agent zuweisen muss:**

- `title` – Folientitel, eine Zeile, maximal 120 Zeichen.
- `subtitle` – ergänzender Kontext / Frame, maximal 160 Zeichen.
- `body_text` – Fließtext in ganzen Sätzen.
- `bullets` – Liste kurzer Bulletpoints.
- `image_hint` – kurze Beschreibung für ein Icon oder Bild.
- `chart_hint` – Beschreibung eines Diagramms (Art, Achsen, Message).
- `table_hint` – Beschreibung einer Tabelle (Spalten, Zeilen, Message).

**Beziehungstypen auf Folienebene (`relation_type`):**

- `single_story` – eine Kernaussage (Standard).
- `comparison` – Gegenüberstellung von 2 Seiten (z. B. Chancen vs. Risiken).
- `before_after` – Heute vs. Zielbild.
- `problem_solution` – Problem links, Lösung rechts.
- `pros_cons` – Vor-/Nachteile.

---

## B. SSOT-relevante Designvorgaben (Kurzfassung)

- Fonts: Arial (Title 24 pt, Subtitle 14 pt, Content 16 pt, Footer 9 pt).
- Textbox-Defaults: Margins 0 cm, Autofit aus, Wrap-On, Vertical Alignment Top.
- Layouts: `content_single_main` (eine Content-Fläche), `content_two_column` (zwei Spalten).

---

## C. Wissensdokument – Inhalt für das Pitch Deck

(hier folgt dein vollständiger Fachinhalt – gekürzt im Beispiel)

### 1. Zielbild & Entscheidungsfrage

Ziel der Präsentation: Entscheidung, ob eine Task Force „KI, GenAI & Agentic AI“ im SAP/ABAP-Kontext formal gestartet wird – mit Mandat, Ressourcen und klaren KPIs. Fokus auf produktive ABAP-Entwicklung, Clean Core / S/4HANA-Transformation und neue Serviceangebote für Kunden.

Kernbotschaft: SAP verschiebt die Spielregeln der Entwicklung hin zu Joule Copilot, Agenten auf der BTP und ABAP-spezifischen LLMs. Wer das strukturiert nutzt, gewinnt Produktivität, Qualität und neue Angebote – wer es laufen lässt, kassiert Wildwuchs, Governance-Risiken und Wettbewerbsnachteile. Die Task Force ist das Instrument, um geplante Pilotierung, Governance und Skalierung zu sichern – statt unkoordinierten Einzelaktionen.

### 2. Strategischer Kontext: SAP TechEd 2025 & Roadmap

(… hier stehen deine TechEd-Punkte und Markt-Signale …)

### 3. Ausgangslage & Problemstellung bei Körber

(… Skill-Gap, Tool-Governance, Clean Core vs. Legacy, Risiken …)

### 4. SAP Joule & Agentic AI – Funktionskern & Reifegrad

(… Joule for Developers, Joule Studio, benötigte Infrastruktur …)

### 5. Interne Potenziale

(… Produktivität, Qualität, Clean Core, Skills …)

### 6. Externe Potenziale

(… Kunden-Use-Cases & Services …)

### 7. Risiken & Governance

(… Halluzinationen, Datenschutz, Vendor Lock-in, Rolle der Task Force …)

### 8. Task Force – Mandat, Rollen, Scope

(… Mandat, Rollen, Scope …)

### 9. Roadmap

(… Phasen 1–5 …)

### 10. KPIs & Business Case

(… Produktivität, Qualität, Time-to-Market, ROI …)

### 11. Management-Botschaft & Entscheidung

(… Warum jetzt, was entschieden werden soll …)
