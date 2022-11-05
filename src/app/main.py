"""
Bux fixes
Adding recipes tracking used for not selecting them again in a certain days span (cca 10 days ago)
Problems: computing slows down exponentially when databases get bigger
"""

import json
from datetime import date
from dbs_handler import DatabasesHandler
import random


h = DatabasesHandler("rec_test_db.json", "ing_test_db.json", "nut_test_db.json")
h.DEV_MODE = True    # Enables control prints and other info to console

# -------- TO DOs ---------
# Update nut db by recipe
# Pridat funkci cooked recipes do select top recipe!!!
# Omrknout numexpr a bottleneck libs - zrychleni dealovani s daty v pandas
# Pokud choose_recipe vrati empty arr, vyberu zcela nahodny recept
# Posilat automaticke emaily s daty nebo jina internetova komunikace (twisted lib, asyncore)
#
# -------------------------

# today = date.today()
# today = date.strftime(today, "%d/%m/%Y").split("/")



nuts_ids = []
# for i in range(1000):
#     perday = random.randint(1, 50)
#     nut_name = i
#     h.nutDB.add({"name": f"{nut_name}", "perday": perday, "current": perday})
#     nuts_ids.append(nut_name)
# #
# ing_count = 400
# for i in range(ing_count):
#     nuts = {}
#     for nut_name in nuts_ids:
#         nuts[nut_name] = random.randint(1, 100)
#     h.ingDB.add({"name": f"ing{i}", "nuts": nuts})
#
# for i in range(500):
#     ings_ids = {}
#     for x in range(random.randint(3, 15)):
#         ings_ids[str(random.randint(0, ing_count))] = random.randint(50, 200) - 50
#     h.recDB.add({"name": f"rec{i}", "ings_ids": ings_ids, "time": 0, "bf": False, "ln": True, "dn": True, "sn": False})

h.nutDB.sub_daily_supply()
rec_id = h.choose_recipe()
print(rec_id)
# h.update_nutDB_by_recipe(rec_id)
