# Website „Katholisch in Wipperfürth“ – Neugestaltung (Entwurf)

Schulprojekt Q2 Kath. Religion, Gruppe 1 – **keine offizielle Seite der Pfarrei St. Nikolaus**.
Inhalte übernommen von der bestehenden Website www.katholisch-in-wipperfuerth.de (Stand 3. November 2026).

## Aufbau

Mehrseitige, statische Website (kein Server nötig, läuft z. B. auf GitHub Pages):

| Seite | Inhalt |
|---|---|
| `index.html` | Start: nächster Gottesdienst, Bürostatus, Notruf, Anliegen, Wochenende, Aktuelles |
| `gottesdienste.html` | Tagesansicht der nächsten 7 Tage mit Filtern, komplette Gottesdienstordnung, Beichte, Seniorenheime |
| `anliegen.html` + `taufe`, `erstkommunion`, `firmung`, `hochzeit`, `beichte`, `krankensalbung`, `trauerfall`, `messe-bestellen` | je eine Seite mit Terminen, Schritten, Unterlagen, Ansprechpersonen |
| `kirchorte.html` | Geschichte von St. Nikolaus, alle 10 Kirchen mit Adresse, Zeiten, Karte |
| `gruppen.html` | Gruppen-Finder, Ehrenamt, Kitas, Gremien |
| `hilfe.html` | Notruf, Prävention mit Ansprechpersonen, Familie & Beratung, Caritas |
| `team.html`, `kontakt.html`, `aktuelles.html`, `suche.html` | Ansprechpersonen, Pastoralbüro mit Formular, Neuigkeiten, Suche |
| `konzept-entwurf-v1.html` | unser erster Konzeptentwurf mit Platzhaltern |

Alle Inhalte stehen direkt im HTML und sind auch ohne JavaScript lesbar. `assets/app.js` ergänzt
Tagesansicht, Bürostatus, Suche, Filter und Formulare.

**Inhalte ändern:** Texte und Gottesdienstzeiten in `build.py` bearbeiten, dann `python3 build.py` ausführen –
alle Seiten und `assets/data.js` werden neu erzeugt.

**Online stellen (GitHub Pages):** Repository → Settings → Pages → „Deploy from a branch“ → Branch wählen, Ordner `/ (root)`.
Die Website ist dann unter `https://<benutzer>.github.io/<repo>/website/` erreichbar.

## Analyse der alten Website → Verbesserung

| Schwäche der alten Seite | Lösung im neuen Entwurf |
|---|---|
| Lange Startseite ohne Prioritäten; Termine und Kontakt weit unten | Oben direkt: **nächster Gottesdienst** (live berechnet), **Büro geöffnet/geschlossen**, **Notruf** |
| Gottesdienstordnung als lange Textliste („1. und 3. So …“) | **Gottesdienst-Finder**: nächste 7 Tage, Filter nach Art und Ort; komplette Ordnung aufklappbar und druckbar |
| Navigation mit 6 Menüs, über 80 Unterseiten, Dubletten („Oberberg Nord GEMEINSAM“ doppelt, Taizé an mehreren Stellen) | 6 klare Bereiche nach Anliegen der Besucher („Ich möchte …“) statt nach Organisationsstruktur |
| Suche nur als „Go“-Knopf | Große Suchleiste mit Sofortvorschlägen (auch Alltagswörter wie „Beerdigung“, „heiraten“) |
| Sakramente nur als Fließtext | Lebenswege mit **3 Schritten**, Ansprechpartner und direktem Anfrage-Button |
| Postanschrift des Büros fehlt auf der Startseite, Fax-Nummer unbeschriftet | Kontaktblock mit Adresse, beschrifteten Nummern, Öffnungszeiten (heutiger Tag hervorgehoben) |
| Kontaktformular unklar | Formular mit Anliegen-Auswahl → öffnet vorbereitete E-Mail (kein Datenspeicher nötig) |
| Veraltete/leere Inhalte (leere Veranstaltungsliste, Vorträge von 2022, Datum 01.01.2026 bei allen News) | Aktuelles als Karten mit echten Daten; Verweis auf die Pfarrnachrichten |
| 13 Chöre und Gruppen auf vielen Unterseiten verstreut | Gruppen-Finder mit Filter (Kinder, Jugend, Erwachsene, Senior:innen, Musik) |
| Hilfsangebote und Prävention tief versteckt | Eigener Bereich „Hilfe & Schutz“ mit Notruf, Telefonseelsorge, Caritas, Beratung, Prävention |
| Nicht für Handy optimiert | Mobile Tab-Leiste, große Tippflächen, Dunkelmodus, barrierearm (Tastatur, Kontraste, Skip-Link) |

## Vor einer echten Nutzung
- Alle Angaben mit dem Pastoralbüro prüfen (u. a. Adresse Kirchplatz 1 vs. 3, Ferienregelungen, Ablauf Erstkommunion/Firmung/Hochzeit).
- Gottesdienstdaten im Skript (`S`) pflegen oder an ein Redaktionssystem anbinden; Feiertage und Ferien sind nicht berücksichtigt.
- Fotos der Kirchen (mit Bildrechten) ergänzen; Einwilligung zum Pfarrer-Foto einholen.
