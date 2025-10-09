import os, re, unicodedata, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Configuración de rutas y cache
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directorio del script
OUT_BASE = os.path.join(BASE_DIR, "data", "raw")
CACHE_BASE = os.path.join(BASE_DIR, "cache")
CACHE_WEB_SCRAPPING = "cache_web_scrapping.txt"
MANIFEST_LOG = os.path.join(OUT_BASE, "manifest.log")

YEARS = range(2013, 2024)  # 2013–2023
CATEGORIA = 140
PERIODO = 1
HEADERS = {"User-Agent": "Mozilla/5.0"}

def norm(s: str) -> str:
    s = s.strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"\s+", " ", s)
    return s

def classifyLabel(label: str):
    t = norm(label)
    if "provial" in t: return None
    if "diccionario" in t or "publicaciones" in t: return None
    if "hechos" in t and "transito" in t: return "hechos"
    if "vehiculo" in t and "involucr" in t: return "vehiculos"
    if "fallecid" in t and "lesion" in t: return "fallecidos_lesionados"
    return None

def originalFilenameFromUrl(url: str) -> str:
    return os.path.basename(urlparse(url).path)

def findBaseDeDatosGrid(soup: BeautifulSoup):
    for h2 in soup.find_all("h2"):
        if "base de datos" in norm(h2.get_text(" ")):
            grid = h2.find_next("div", class_="grid")
            if grid: return grid
    return soup

def scrapYear(year: int, manifestLines: list):
    url = f"https://www.ine.gob.gt/bdatos_cargar.php?anio={year}&categoria={CATEGORIA}&periodo={PERIODO}&dire=https://www.ine.gob.gt/sistema/"
    manifestLines.append(f"\n=== Año {year} ===\nGET {url}")
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    grid = findBaseDeDatosGrid(soup)

    yearDir = os.path.join(OUT_BASE, str(year))
    os.makedirs(yearDir, exist_ok=True)

    foundPerCat = {k: {"xlsx": None, "sav": None} for k in ["hechos","vehiculos","fallecidos_lesionados"]}

    for row in grid.find_all("div", class_=lambda c: c and "flex" in c and "justify-between" in c):
        label_span = row.find("span")
        label_text = label_span.get_text(strip=True) if label_span else row.get_text(" ", strip=True)
        cat = classifyLabel(label_text)
        if not cat: continue

        for a in row.find_all("a", href=True):
            href = a["href"].strip()
            href_l = href.lower()
            alt = ""
            img = a.find("img")
            if img and img.get("alt"):
                alt = norm(img["alt"])

            is_xlsx = href_l.endswith(".xlsx") or "xls" in alt
            is_sav  = href_l.endswith(".sav")  or "spss" in alt

            if is_xlsx and not foundPerCat[cat]["xlsx"]:
                foundPerCat[cat]["xlsx"] = href
            elif is_sav and not foundPerCat[cat]["sav"]:
                foundPerCat[cat]["sav"] = href

    downloaded = 0
    for cat, links in foundPerCat.items():
        href = links["xlsx"] or links["sav"]  # preferir XLSX
        if not href: continue

        fname = originalFilenameFromUrl(href)
        dest = os.path.join(yearDir, fname)
        if os.path.exists(dest):
            manifestLines.append(f"\t• {cat}: {fname} -> {dest} (skip)")
            downloaded += 1
            continue

        manifestLines.append(f"\t• {cat}: {fname} -> {dest}")
        with requests.get(href, headers=HEADERS, timeout=180, stream=True) as resp:
            resp.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk: f.write(chunk)
        downloaded += 1

    if downloaded == 0:
        manifestLines.append(f"\t! No se encontraron enlaces PNC (XLSX/SAV) en Base de Datos para este año.")
    else:
        manifestLines.append(f"\t✓ Descargados {downloaded} archivo(s) para {year}")

def main():
    cacheFilePath = os.path.join(CACHE_BASE, CACHE_WEB_SCRAPPING)
    if os.path.exists(cacheFilePath):
        print(f"Cache encontrado en {cacheFilePath}, saltando scraping.")
        return

    manifestLines = []
    for y in YEARS:
        scrapYear(y, manifestLines)

    manifestLines.append("\nDescarga terminada. Revisa ./data/raw/<año>/")

    # Guardar manifest.log
    with open(MANIFEST_LOG, "w", encoding="utf-8") as f:
        for line in manifestLines:
            f.write(line + "\n")

    # Crear cache al final
    with open(cacheFilePath, "w") as f:
        f.write("Web scraping completado.\n")

    print("\n".join(manifestLines))

if __name__ == "__main__":
    main()
