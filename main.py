# Import knihoven
import argparse
import requests
from bs4 import BeautifulSoup as bs
import csv

# Funkce
def get_soup(url):
    """Načte HTML stránku a vrátí objekt BeautifulSoup."""
    response = requests.get(url)
    return bs(response.text, features="html.parser")


def get_obec_links(base_url):
    """Získá kódy obcí a odkazy na jejich detailní výsledky."""
    soup = get_soup(base_url)
    td_tags = soup.find_all("td", class_="cislo")

    links = {}                      # prázdný slovník
    for td in td_tags:              # projdeme všechny <td> s class="cislo"
        if td.a:                    # kontrola, že uvnitř je <a>
            key = td.a.text         # klíč = text odkazu (číslo obce)
            href = td.a["href"]     # hodnota = href
            full_url = f"https://www.volby.cz/pls/ps2017nss/{href}"
            links[key] = full_url   # vložíme do slovníku
    return links


def clean_number(text):
    """Odstraní nezlomitelné mezery a běžné mezery."""
    return text.replace("\xa0", "").replace(" ", "")


def parse_obec_results(url):
    """Získá výsledky hlasování pro jednu obec."""
    soup = get_soup(url)
    data = {}

    # Základní informace
    header = soup.select("h3:nth-child(4)") # publikace > h3:nth-child(4)
    header_txt = header[0].get_text(strip=True)
    kod_obce = url.split("xobec=")[1].split("&")[0]
    data["code"] = kod_obce
    data["location"] = header_txt.replace("Obec: ","")
    
    # Statistika - data z první tabulky na stránce konkrétní obce
    td_reg = soup.find("td", headers="sa2") 
    td_env = soup.find("td", headers="sa5")
    td_val = soup.find("td", headers="sa6")
    data["registered"] = int(clean_number(td_reg.get_text(strip=True)))
    data["envelopes"] = int(clean_number(td_env.get_text(strip=True)))
    data["valid"] = int(clean_number(td_val.get_text(strip=True)))

    # Hlasy pro strany - data z druhé tabulky na stránce konkrétní obce
    for table in soup.find_all("table")[1:]: 
        rows = table.find_all("tr")[2:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                party = cols[1].text.strip()
                votes = clean_number(cols[2].text.strip())
                data[party] = votes
    return data


def save_to_csv(data, filename):
    """Uloží výsledky do CSV souboru. Oddělovačem je čárka (nikoli středník)."""
    if not data:
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def main():
    """Vyžádá vstup od uživatele a vrátí volební výsledky v požadovaném okrese do csv souboru."""
    parser = argparse.ArgumentParser(description="Scraper volebních výsledků pro daný územní celek.")
    parser.add_argument("url", help="URL stránky s výpisem obcí")
    parser.add_argument("output", help="Název výstupního CSV souboru")
    args = parser.parse_args()

    # Kontrola url
    if not args.url.startswith("https://www.volby.cz/pls/ps2017nss/"):
        parser.error("URL je první argument a musí začínat na 'https://www.volby.cz/pls/ps2017nss/'.")

    # Kontrola názvu souboru
    if not args.output.endswith(".csv"):
        parser.error("Výstupní soubor musí mít příponu .csv.")

    try:
        obec_links = get_obec_links(args.url)
        if not obec_links:
            parser.error("Nepodařilo se získat odkazy na obce z dané URL.")

        results = []
        for name, url in obec_links.items():
            print(f"Zpracovávám: {name}")
            results.append(parse_obec_results(url))
        save_to_csv(results, args.output)
        print(f"Hotovo! Výsledky uloženy do {args.output}")
    except Exception as e:
        parser.error(f"Nastala chyba: {e}")


# Spuštění kódu
if __name__ == "__main__":
    main()