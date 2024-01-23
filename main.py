from subito import *
from datetime import datetime
import platform
import os

search_for = input("Inseriri i termini della ricerca: ")
results = int(input("Numero di annunci da ricercare (minimo 100): "))
exclude_past_ads = input("Escludi gli annunci passati (y/n): ")
exclude_past_ads = True if exclude_past_ads == "y" else False
max_price = input("Prezzo massimo (lascia vuoto per non utilizzare): ")
if max_price == "":
    max_price = 999999
else:
    max_price = int(max_price)

min_price = input("Prezzo minimo (lascia vuoto per non utilizzare): ")
if min_price == "":
    min_price = -1
else:
    min_price = int(min_price)

with open("blacklist_words.json", mode="r") as jsonfile:
    blacklist_words = json.load(jsonfile)

with open("past_ads.json", mode="r") as jsonfile:
    past_ads = json.load(jsonfile)

with open("blacklist_user.json", mode="r") as jsonfile:
    user_blacklist = json.load(jsonfile)

searcher = Subito(search_for)
results: dict = searcher.search(results=results)

ordered_results = []


def sort_by_price(lista: list):
    return float(lista[0])


for result in results:
    ad_id = result.get("urn").split(":list:")[1]
    if (exclude_past_ads) and (ad_id in past_ads):
        continue
    else:
        if ad_id not in past_ads:
            past_ads.append(ad_id)
        title = result.get("subject")
        body = result.get("body")
        date = result.get("dates").get("display")
        venditore_id = result.get("advertiser").get("user_id")
        venditore_nome = result.get("advertiser").get("name")
        url = result.get("urls").get("default")
        features = result.get("features")
        prezzo = 0
        spedizione = 0
        venduto = False
        for feature in features:
            if feature.get("label") == "Prezzo":
                prezzo = float(feature.get("values")[0].get("key").replace(",", "."))
            if feature.get("label") == "Costo della spedizione":
                spedizione = float(
                    feature.get("values")[0].get("key").replace(",", ".")
                )
            stato = feature.get("values")[0].get("value")
            if stato == "SOLD":
                venduto = True
        blacklisted_by_word = False
        for word in blacklist_words:
            if word in title.replace(" ", "").lower():
                blacklisted_by_word = True
        if (
            (prezzo < max_price)
            and (prezzo > min_price)
            and (venditore_id not in user_blacklist)
            and (search_for.replace(" ", "").lower() in title.replace(" ", "").lower())
            and venduto is False
        ):
            ordered_results.append(
                [
                    prezzo,
                    f"{title}\n{date}\n{url}\n{prezzo} EUR\nuser_id:{venditore_id}\n====================\n",
                ]
            )
with open("past_ads.json", mode="w") as jsonfile:
    json.dump(past_ads, jsonfile, indent=4)

ordered_results.sort(key=sort_by_price)


time = f"{search_for.replace(" ", "_")}{int(datetime.now().timestamp())}.txt"
with open(f"reports/{time}", mode="w") as reportfile:
    for line in ordered_results:
        reportfile.write(line[1])

if platform.system() == "Windows":
    os.chdir("reports")
    os.system(time)
else:
    os.system(f"xdg-open reports/{time}")
