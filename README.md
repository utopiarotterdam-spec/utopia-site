# Utopia Rotterdam — website

De site is opgesplitst in drie lagen, zodat inhoud bewerken losstaat van de code:

```
index.html          de site zelf (vormgeving + gedrag) — hier hoef je zelden in
data/
  nu.json           gebeurtenissen "Nu"
  toen.json         gebeurtenissen "Toen"
  leden.json        alle leden
media/
  nu/  toen/  leden/  site/   foto's, als gewone bestanden
  oud/                        foto's overgenomen van de oude site (na stap 1)
scripts/
  haal_oude_fotos.py          eenmalig draaien, zie stap 1
  oude-site-bestanden.txt     lijst van bestanden die nu nog op de oude site staan
.pages.yml          configuratie voor de beheeromgeving (Pages CMS)
```

## Lokaal bekijken

De site laadt zijn data via `fetch`, en dat werkt niet als je `index.html`
dubbelklikt. Start een mini-webserver in deze map:

```
python3 -m http.server
```

en open dan **http://localhost:8000** in je browser.

## Stap 1 — oude foto's veiligstellen (eenmalig, vóór de oude site offline gaat!)

51 ledenfoto's staan nu nog op `www.utopia-rotterdam.nl`. Haal ze binnen met:

```
python3 scripts/haal_oude_fotos.py
```

Dit downloadt alles naar `media/oud/` en past `data/leden.json` automatisch aan.

## Stap 2 — op GitHub zetten

1. Maak een gratis account op github.com.
2. Kies rechtsboven **+ → New repository**, noem hem bijv. `utopia-site`,
   zet hem op **Public**, klik **Create repository**.
3. Kies **uploading an existing file** en sleep de complete inhoud van deze
   map erin (inclusief de mappen). Klik **Commit changes**.
   Let op: `.pages.yml` begint met een punt en wordt door sommige systemen
   verborgen — controleer dat hij is meegekomen.
4. Ga naar **Settings → Pages**, kies bij "Source": **Deploy from a branch**,
   branch **main**, map **/ (root)**, klik **Save**.
5. Na een minuut staat de site live op `https://<gebruikersnaam>.github.io/utopia-site/`.

Elke wijziging die je daarna commit (via GitHub of via het CMS) staat binnen
een minuut live. Elke oude versie blijft bewaard en is terug te zetten.

## Stap 3 — beheeromgeving koppelen (Pages CMS)

1. Ga naar **app.pagescms.org** en log in met je GitHub-account.
2. Kies de repository `utopia-site`. Pages CMS leest `.pages.yml` en toont
   drie secties: **Nu**, **Toen** en **Leden** — met invulformulieren en
   drag-and-drop voor foto's.
3. Nodig leden uit via **Settings → Collaborators** (op e-mailadres; zij
   hebben géén GitHub-account nodig).

Een gebeurtenis toevoegen is dan: sectie openen → item toevoegen → velden
invullen → foto erin slepen → **Save**. Klaar.

## Inhoud met de hand bewerken (kan ook altijd)

Een gebeurtenis in `data/nu.json` ziet er zo uit:

```json
{
  "y": "mrt 2027",
  "t": "Titel van de gebeurtenis",
  "lid": "Naam Lid",
  "d": "Korte beschrijving. De naam van het lid wordt automatisch klikbaar.",
  "imgs": [
    { "s": "media/nu/mijn-foto.jpg", "c": "bijschrift" }
  ]
}
```

Een lid in `data/leden.json`:

```json
{
  "n": "Voornaam Achternaam",
  "r": "Rol of ondertitel",
  "b": "Bio.\nElke \\n wordt een nieuwe alinea. E-mail en websites worden automatisch klikbaar.",
  "imgs": ["media/leden/foto.jpg"]
}
```

Lid verwijderen = het hele blokje (inclusief komma) weghalen.

## Vuistregels voor foto's

- Streef naar **maximaal ~1600 px** aan de lange zijde en JPEG-formaat;
  een foto rechtstreeks van een telefoon is al snel 5–10 MB en maakt de
  site traag.
- Geef bestanden herkenbare namen zonder spaties: `nina-simone-1983.jpg`.

## Later: het echte domein

Pas als alles naar wens werkt op het github.io-adres: DNS van het domein
omzetten naar GitHub Pages. Maak vóór die stap een volledig archief van de
oude site, en laat de MX-records (e-mail) ongemoeid.
