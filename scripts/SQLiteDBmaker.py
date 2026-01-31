import re
import json
import requests
import sqlite3

def zapisz_wszystko_do_sqlite(dane_wejsciowe):
    conn = sqlite3.connect('eqmfo.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS przedmioty (
            id INTEGER PRIMARY KEY, nazwa TEXT, poziom INTEGER, typ TEXT, atrybut TEXT,
            profesja TEXT, jakosc TEXT, sloty INTEGER, opis TEXT, wartosc INTEGER, cena_zetonow INTEGER,
            ikonka_rzad INTEGER, ikonka_kolumna INTEGER, ikonka TEXT, ikonka_wysokosc INTEGER, ikonka_szerokosc INTEGER,
            obrazenia INTEGER, hp INTEGER, mp INTEGER, atak INTEGER, atak_magiczny INTEGER, 
            obrona INTEGER, obrona_magiczna INTEGER, szczescie INTEGER, szybkosc INTEGER, 
            celnosc INTEGER, uniki INTEGER, miecz INTEGER, wlocznia INTEGER, topor INTEGER, 
            bulawa INTEGER, ogien INTEGER, lod INTEGER, ziemia INTEGER, wiatr INTEGER, 
            exp_mod INTEGER, ap_mod INTEGER, gold_mod INTEGER, encounter INTEGER
        )
    ''')

    def to_int(val):
        try:
            return int(val) if val is not None else 0
        except (ValueError, TypeError):
            return 0

    if isinstance(dane_wejsciowe, dict):
        lista_itemow = [dane_wejsciowe]
    else:
        lista_itemow = dane_wejsciowe

    query = f"INSERT OR REPLACE INTO przedmioty VALUES ({','.join(['?']*39)})"

    for s in lista_itemow:
        dane_do_sql = (
            to_int(s.get("id")), str(s.get("nazwa")), to_int(s.get("poziom")),
            str(s.get("typ")), str(s.get("atrybut")), str(s.get("profesja")),
            str(s.get("jakość")), to_int(s.get("sloty")), str(s.get("opis")),
            to_int(s.get("wartosc")), to_int(s.get("cena_zetonow")),
            to_int(s.get("ikonka_rzad")), to_int(s.get("ikonka_kolumna")),
            str(s.get("ikonka")), to_int(s.get("ikonka_wysokosc")), to_int(s.get("ikonka_szerokosc")),
            to_int(s.get("obrazenia")), to_int(s.get("hp")), to_int(s.get("mp")),
            to_int(s.get("atak")), to_int(s.get("atak_magiczny")),
            to_int(s.get("obrona")), to_int(s.get("obrona magiczna")),
            to_int(s.get("szczescie")), to_int(s.get("szybkosc")),
            to_int(s.get("celnosc")), to_int(s.get("uniki")),
            to_int(s.get("miecz")), to_int(s.get("wlocznia")),
            to_int(s.get("topor")), to_int(s.get("bulawa")),
            to_int(s.get("ogien")), to_int(s.get("lod")),
            to_int(s.get("ziemia")), to_int(s.get("wiatr")),
            to_int(s.get("exp")), to_int(s.get("ap")),
            to_int(s.get("gold")), to_int(s.get("encounter"))
        )
        cursor.execute(query, dane_do_sql)

    conn.commit()
    conn.close()
    print(f"Zapisano {len(lista_itemow)} przedmiot(ów) do bazy.")

def wpis(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    else:
        print("Błąd podczas pobierania strony:", response.status_code)
        html = ""

    pattern = r"ArmorInfo\.create\('[^']+',\s*({.*?})\s*,\s*null\);"

    match = re.search(pattern, html, re.DOTALL)
    if match:
        json_data = match.group(1)
        armor_info = json.loads(json_data)
        Statystyki = {"id": armor_info.get("armor_id"), "nazwa": armor_info.get("name").strip(),
                      "poziom": armor_info.get("level"), "typ": armor_info.get("type"),
                      "atrybut": armor_info.get("attribute"), "profesja": armor_info.get("profession"),
                      "jakość": armor_info.get("quality"), "sloty": armor_info.get("slots"),
                      "opis": armor_info.get("description"), "wartosc": armor_info.get("cost_gold"),
                      "cena_zetonow": armor_info.get("cost_token"),
                      "ikonka_rzad": armor_info.get("icon").get("source").get("x"),
                      "ikonka_kolumna": armor_info.get("icon").get("source").get("y"),
                      "ikonka": armor_info.get("icon").get("graphic").get("src").split('?')[0],
                      "ikonka_wysokosc": armor_info.get("icon").get("graphic").get("size").get("x"),
                      "ikonka_szerokosc": armor_info.get("icon").get("graphic").get("size").get("y"),
                      "obrazenia": armor_info.get("stats").get('DAMAGE'), "hp": armor_info.get("stats").get('MAXHP'),
                      "mp": armor_info.get("stats").get('MAXMP'), "atak": armor_info.get("stats").get('ATK'),
                      "atak_magiczny": armor_info.get("stats").get('MAGATK'),
                      "obrona": armor_info.get("stats").get('DEF'),
                      "obrona magiczna": armor_info.get("stats").get('MAGDEF'),
                      "szczescie": armor_info.get("stats").get('LCK'), "szybkosc": armor_info.get("stats").get('SPD'),
                      "celnosc": armor_info.get("stats").get('HIT'), "uniki": armor_info.get("stats").get('EVA'),
                      "miecz": armor_info.get('stats').get('SWORDDEF'),
                      "wlocznia": armor_info.get('stats').get('SPEARDEF'),
                      "topor": armor_info.get('stats').get('AXEDEF'), "bulawa": armor_info.get('stats').get('MACEDEF'),
                      "ogien": armor_info.get('stats').get('FIREDEF'), "lod": armor_info.get('stats').get('ICEDEF'),
                      "ziemia": armor_info.get('stats').get('EARTHDEF'),
                      "wiatr": armor_info.get('stats').get('WINDDEF'), "exp": armor_info.get('stats').get('EXP_MOD'),
                      "ap": armor_info.get('stats').get('AP_MOD'), "gold": armor_info.get('stats').get('GOLD_MOD'),
                      "encounter": armor_info.get('stats').get('ENCOUNTER')}
        #print(Statystyki)
        return Statystyki
    else:
        #print("Nie znaleziono danych ArmorInfo.")
        return 0


if __name__ == "__main__":
    pliki_do_pobrania = set()
    Items = []
    for id in range (0, 1111):
        Item = wpis(f"https://mfo3.pl/view/a/{id}")
        if Item != 0:
            pliki_do_pobrania.add(Item["ikonka"])
            Items.append(Item)
    zapisz_wszystko_do_sqlite(Items)