import os, re, unicodedata, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# ------------------ Configuración ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_BASE = os.path.join(BASE_DIR, "data", "variables")
CACHE_BASE = os.path.join(BASE_DIR, "cache")
CACHE_VARIABLES = "cache_variables.txt"
MANIFEST_LOG = os.path.join(OUT_BASE, "manifest.log")

YEARS = range(2013, 2024)  # 2013–2023
CATEGORIA = 140
PERIODO = 1
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ------------------ Funciones auxiliares ------------------
def norm(s: str) -> str:
    """Normaliza un string: quita acentos, espacios extras y pasa a minúsculas."""
    s = s.strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"\s+", " ", s)
    return s

def classifyLabel(label: str):
    """Clasifica un label en tipo de diccionario."""
    t = norm(label)
    if "diccionario" in t or "provial" in t:
        if "fallecid" in t and "lesion" in t: 
            return "fallecidos_lesionados"
        if "hechos" in t and "transito" in t: 
            return "hechos"
        if "vehiculo" in t and "involucr" in t: 
            return "vehiculos"
    return None

def originalFilenameFromUrl(url: str) -> str:
    return os.path.basename(urlparse(url).path)

def findDiccionarioGrid(soup: BeautifulSoup):
    """Encuentra el contenedor del diccionario en la página."""
    for h2 in soup.find_all("h2"):
        # print(f"[DEBUG] Encontrado h2: {h2.get_text(strip=True)}")
        if "diccionario de variables" in norm(h2.get_text(" ")):
            parent = h2.find_next(["div", "section"])
            if parent:
                # print(f"[DEBUG] Contenedor siguiente: {parent.name}, clases: {parent.get('class')}")
                return parent
    # print("[DEBUG] No se encontró h2 de diccionario, devolviendo soup completo")
    return soup

# ------------------ Función principal por año ------------------
def scrapYearVariables(year: int, manifestLines: list):
    url = f"https://www.ine.gob.gt/bdatos_cargar.php?anio={year}&categoria={CATEGORIA}&periodo={PERIODO}&dire=https://www.ine.gob.gt/sistema/"
    manifestLines.append(f"\n=== Año {year} ===\nGET {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
    except requests.RequestException as e:
        manifestLines.append(f"\t! Error al acceder: {e}")
        return

    soup = BeautifulSoup(r.text, "html.parser")
    grid = findDiccionarioGrid(soup)

    yearDir = os.path.join(OUT_BASE, str(year))
    os.makedirs(yearDir, exist_ok=True)

    foundPerCat = {k: None for k in ["hechos","vehiculos","fallecidos_lesionados"]}

    for row in grid.find_all("div", class_=lambda c: c and "flex" in c and "justify-between" in c):
        label_span = row.find("span")
        label_text = label_span.get_text(strip=True) if label_span else row.get_text(" ", strip=True)
        cat = classifyLabel(label_text)
        if not cat: 
            continue

        for a in row.find_all("a", href=True):
            href = a["href"].strip()
            # Aceptar tanto .xlsx como .xls
            if (href.lower().endswith(".xlsx") or href.lower().endswith(".xls")) and not foundPerCat[cat]:
                foundPerCat[cat] = href

    downloaded = 0
    for cat, href in foundPerCat.items():
        if not href: 
            continue

        fname = originalFilenameFromUrl(href)
        dest = os.path.join(yearDir, fname)
        if os.path.exists(dest):
            manifestLines.append(f"\t• {cat}: {fname} -> {dest} (skip)")
            downloaded += 1
            continue

        manifestLines.append(f"\t• {cat}: {fname} -> {dest}")
        try:
            with requests.get(href, headers=HEADERS, timeout=180, stream=True) as resp:
                resp.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk: 
                            f.write(chunk)
            downloaded += 1
        except requests.RequestException as e:
            manifestLines.append(f"\t! Error descargando {fname}: {e}")

    if downloaded == 0:
        manifestLines.append(f"\t! No se encontraron diccionarios de variables en este año.")
    else:
        manifestLines.append(f"\t✓ Descargados {downloaded} archivo(s) para {year}")


# ------------------ Función main ------------------
def main():
    cacheFilePath = os.path.join(CACHE_BASE, CACHE_VARIABLES)
    if os.path.exists(cacheFilePath):
        print(f"Cache encontrado en {cacheFilePath}, saltando scraping.")
        return

    manifestLines = []
    for y in YEARS:
        scrapYearVariables(y, manifestLines)

    manifestLines.append("\nDescarga terminada. Revisa ./data/variables/<año>/")

    # Guardar manifest.log
    with open(MANIFEST_LOG, "w", encoding="utf-8") as f:
        for line in manifestLines:
            f.write(line + "\n")

    # Crear cache al final
    with open(cacheFilePath, "w") as f:
        f.write("Scraping de diccionarios completado.\n")

    print("\n".join(manifestLines))

if __name__ == "__main__":
    main()
