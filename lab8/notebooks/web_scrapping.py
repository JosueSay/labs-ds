import os, re, unicodedata, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

OUT_BASE = "./notebooks/data/raw"
os.makedirs(OUT_BASE, exist_ok=True)

YEARS = range(2013, 2024)  # 2013–2023
CATEGORIA = 140
PERIODO = 1
HEADERS = {"User-Agent": "Mozilla/5.0"}

def norm(s: str) -> str:
    s = s.strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"\s+", " ", s)
    return s

def classify_label(label: str):
    t = norm(label)
    if "provial" in t: return None
    if "diccionario" in t or "publicaciones" in t: return None
    if "hechos" in t and "transito" in t: return "hechos"
    if "vehiculo" in t and "involucr" in t: return "vehiculos"
    if "fallecid" in t and "lesion" in t: return "fallecidos_lesionados"
    return None

def original_filename_from_url(url: str) -> str:
    return os.path.basename(urlparse(url).path)

def find_base_de_datos_grid(soup: BeautifulSoup):
    for h2 in soup.find_all("h2"):
        if "base de datos" in norm(h2.get_text(" ")):
            grid = h2.find_next("div", class_="grid")
            if grid: return grid
    return soup

for y in YEARS:
    url = f"https://www.ine.gob.gt/bdatos_cargar.php?anio={y}&categoria={CATEGORIA}&periodo={PERIODO}&dire=https://www.ine.gob.gt/sistema/"
    print(f"\n=== Año {y} ===\nGET {url}")
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    grid = find_base_de_datos_grid(soup)

    year_dir = os.path.join(OUT_BASE, str(y))
    os.makedirs(year_dir, exist_ok=True)

    found_per_cat = {k: {"xlsx": None, "sav": None} for k in ["hechos","vehiculos","fallecidos_lesionados"]}

    for row in grid.find_all("div", class_=lambda c: c and "flex" in c and "justify-between" in c):
        label_span = row.find("span")
        label_text = label_span.get_text(strip=True) if label_span else row.get_text(" ", strip=True)
        cat = classify_label(label_text)
        if not cat:
            continue

        for a in row.find_all("a", href=True):
            href = a["href"].strip()
            href_l = href.lower()
            # Si el <a> no tiene texto, revisar el <img alt="">
            alt = ""
            img = a.find("img")
            if img and img.get("alt"):
                alt = norm(img["alt"])

            is_xlsx = href_l.endswith(".xlsx") or "xls" in alt
            is_sav  = href_l.endswith(".sav")  or "spss" in alt

            if is_xlsx and not found_per_cat[cat]["xlsx"]:
                found_per_cat[cat]["xlsx"] = href
            elif is_sav and not found_per_cat[cat]["sav"]:
                found_per_cat[cat]["sav"] = href

    downloaded = 0
    for cat, links in found_per_cat.items():
        href = links["xlsx"] or links["sav"]  # preferir XLSX
        if not href:
            continue
        fname = original_filename_from_url(href)
        dest = os.path.join(year_dir, fname)
        if os.path.exists(dest):
            print(f"\t• Ya existe: {dest} (skip)")
            downloaded += 1
            continue
        print(f"\t• {cat}: {fname} → {dest}")
        with requests.get(href, headers=HEADERS, timeout=180, stream=True) as resp:
            resp.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk: f.write(chunk)
        downloaded += 1

    if downloaded == 0:
        print("\t! No se encontraron enlaces PNC (XLSX/SAV) en Base de Datos para este año.")
    else:
        print(f"\t✓ Descargados {downloaded} archivo(s) para {y}")

print("\n✅ Descarga terminada. Revisa ./notebooks/data/raw/<año>/")
