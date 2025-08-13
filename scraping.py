import os
from typing import Dict, List, Tuple
from collections import defaultdict
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup, Tag
from images import download_image

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_animal_names"
TABLE_HEADERS = ['Collateral adjective', 'Animal']

def clean_str(s: str, replacers: Dict[str, str] | None = None) -> str:
    if not replacers:
        replacers = {"(list)": "", " ": ""}
    for k, v in replacers.items():
        s = s.replace(k, v)

    return s


def get_table(url: str, table_headers: List[str]) -> Tuple[Tag | None, int | None, int | None]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table')

    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if all(header in headers for header in table_headers):
            return table, headers.index(table_headers[0]), headers.index(table_headers[1])

    return None, None, None

def get_mapping_from_table(table: Tag, key_idx: int, value_idx: int) -> Dict[str, List[Dict[str, str]]]:
    adj_animal_mapping: Dict[str, list] = defaultdict(list)
    for row in table.find_all('tr')[1:]:
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2:
            continue
        keys = [p.strip() for p in cells[key_idx].get_text(separator="\n").split("\n") if p.strip()]
        if cells[value_idx].find('a'):
            animal = clean_str(cells[value_idx].find('a').text)
            href = cells[value_idx].find('a').get("href")
            values = {"animal": animal, "href": href}

            if keys and values:
                for key in keys:
                    adj_animal_mapping[clean_str(key)].append(values)

    return adj_animal_mapping

mapping_dict = get_mapping_from_table(*get_table(WIKI_URL, TABLE_HEADERS))

images_dict = {}
for adj, animals_list in mapping_dict.items():
    for d in animals_list:
        images_dict[d['animal']] = d['href']

os.makedirs("tmp", exist_ok=True)
# for key, val in images_dict.items():
#     download_image(val, key)
#
with ThreadPoolExecutor() as executor:
    # zip pages and save_dirs, then unpack with *
    executor.map(lambda args: download_image(*args), zip(images_dict.values(), images_dict.keys()))

print("Done")
