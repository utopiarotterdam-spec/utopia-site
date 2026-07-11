#!/usr/bin/env python3
"""
Haalt alle foto's (en PDF's) op die nu nog op de oude site
(www.utopia-rotterdam.nl) staan, zet ze in media/oud/ en past de
verwijzingen in data/*.json automatisch aan.

BELANGRIJK: draai dit VOORDAT de oude site offline gaat.

Gebruik (vanuit de hoofdmap van de site):
    python3 scripts/haal_oude_fotos.py
"""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "media" / "oud"
PATTERN = re.compile(r"https://www\.utopia-rotterdam\.nl/wp-content/uploads/[^\s\"\\]+")
HEADERS = {"User-Agent": "Mozilla/5.0 (utopia-site-migratie)"}


def lokale_naam(url: str) -> str:
    # /uploads/2014/03/betty1.jpg  ->  2014-03-betty1.jpg
    deel = url.split("/wp-content/uploads/", 1)[1]
    return deel.replace("/", "-")


def main():
    MEDIA.mkdir(parents=True, exist_ok=True)
    gelukt, mislukt = 0, []

    for jf in sorted((ROOT / "data").glob("*.json")):
        tekst = jf.read_text(encoding="utf-8")
        urls = sorted(set(PATTERN.findall(tekst)))
        for url in urls:
            doel = MEDIA / lokale_naam(url)
            if not doel.exists():
                try:
                    req = urllib.request.Request(url, headers=HEADERS)
                    with urllib.request.urlopen(req, timeout=30) as r:
                        doel.write_bytes(r.read())
                    print(f"  OK  {doel.name}")
                    gelukt += 1
                except Exception as e:
                    print(f"  FOUT {url} — {e}")
                    mislukt.append(url)
                    continue
            tekst = tekst.replace(url, f"media/oud/{doel.name}")
        jf.write_text(tekst, encoding="utf-8")
        print(f"{jf.name} bijgewerkt")

    print(f"\nKlaar: {gelukt} bestanden gedownload, {len(mislukt)} mislukt.")
    if mislukt:
        print("Mislukte downloads (probeer opnieuw of sla handmatig op):")
        for u in mislukt:
            print("  " + u)


if __name__ == "__main__":
    main()
