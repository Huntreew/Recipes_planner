"""
Bux fixes
Adding recipes tracking used for not selecting them again in a certain days span (cca 10 days ago)
Problems: computing slows down exponentially when databases get bigger
"""

import json
from datetime import date
from dbs_handler import DatabasesHandler
import random

DEV_MODE = True  # Enables control prints and other info to console

# -------- TO DOs ---------
#
# Pokud choose_recipe vrati empty arr, vyberu zcela nahodny recept
#
# -------------------------

# today = date.today()
# today = date.strftime(today, "%d/%m/%Y").split("/")

h = DatabasesHandler("rec_test_db", "ing_test_db", "nut_test_db")
h.DEV_MODE = DEV_MODE

nuts_names = []
for i in range(1):
    perday = random.randint(1, 50)
    nut_name = str(i)
    h.nutDB.add({"name": f"{nut_name}", "perday": perday, "current": perday})
    nuts_names.append(nut_name)

ing_count = 1
for i in range(ing_count):
    nuts = {}
    for nut_name in nuts_names:
        nuts[nut_name] = random.randint(1, 100)
    h.ingDB.add({"name": f"ing{i}", "nuts": nuts})

for i in range(1):
    ings_ids = {}
    for x in range(random.randint(3, 15)):
        ings_ids[str(random.randint(1, 99))] = random.randint(50, 200) - 50
    h.recDB.add({"name": f"rec{i}", "ings_ids": ings_ids, "time": 0, "bf": False, "ln": True, "dn": True, "sn": False})
#
h.nutDB.sub_daily_supply()
rec_id = h.choose_recipe()
print(rec_id)
h.update_nutDB_by_recipe(rec_id)
