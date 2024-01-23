from subito import *
from datetime import datetime

searcher = Subito("Stampante 3D")
results: dict = searcher.search(1000)

with open("results.json", mode="w") as jsonfile:
    json.dump(results, jsonfile, indent=4)

with open("past_ads.json", mode="r") as jsonfile:
    past_ads = json.load(jsonfile)

prezzo_max = 40  # HARDCODED
with open("blacklist_user.json", mode="r") as jsonfile:
    user_blacklist = json.load(jsonfile)

with open(f"report{int(datetime.now().timestamp())}.txt", mode="w") as report:
    for result in results:
        ad_id = result.get("urn").split(":list:")[1]

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
                print(ad_id)
                print("sold")

        if (
            (prezzo < prezzo_max)
            and (venditore_id not in user_blacklist)
            and ("stampante3d" in title.replace(" ", "").lower())
            and venduto is False
            # and (ad_id not in past_ads)
        ):
            past_ads.append(ad_id)
            report.write(
                f"{title}\n{date}\n{url}\n{prezzo} EUR\nuser_id:{venditore_id}\n====================\n"
            )

with open("past_ads.json", mode="w") as jsonfile:
    json.dump(past_ads, jsonfile, indent=4)
