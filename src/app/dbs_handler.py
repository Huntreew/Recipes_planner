from databases import RecipeDatabase, IngredientDatabase, NutriReportDatabase
import random
import datetime
import time

TOP_INGREDIENTS_COUNT = 5
TOP_RECIPES_COUNT = 3


# ----------- DATABASES HANDLER ------------

class DatabasesHandler:

    def __init__(self, rec_db_filename, ing_db_filename, nut_db_filename):
        self.recDB = RecipeDatabase(rec_db_filename)
        self.ingDB = IngredientDatabase(ing_db_filename)
        self.nutDB = NutriReportDatabase(nut_db_filename)
        self.DEV_MODE = False
        self.cooked = {}

    def clear_all_DBs(self):
        self.recDB.clear_db()
        self.ingDB.clear_db()
        self.nutDB.clear_db()

    def choose_recipe(self):
        start = time.time()
        # Setup array with most needed nutrients
        low_nuts_raw = self.nutDB.search_for_lows()  # finds most needed nuts
        low_nuts = self.nutDB.sort_lows(low_nuts_raw=low_nuts_raw)  # sorts nuts
        if self.DEV_MODE:
            print("\nLOW NUTS: ", low_nuts, "\n")
            print(f"Search for low nuts: {time.time() - start}")
        # Setup array with top ingredients containing needed nuts
        ings_total = []
        start = time.time()
        for nut_dicty in low_nuts:
            max_ings_count = len(low_nuts) - low_nuts.index(nut_dicty)  # bigger deficit is, more ingredients are added
            ings = self.ingDB.search_ings(nut_dicty["name"], max_in_arr=max_ings_count)
            ings_total.append(ings)
        top_ings = self.ingDB.select_top_ings(ings_total=ings_total, how_many=TOP_INGREDIENTS_COUNT)
        if self.DEV_MODE:
            # print("\nINGS TOTAL: ", ings_total, "\n")
            print("\nTOP INGS: ", top_ings, "\n")
            print(f"Top ings search: {time.time() - start}")
        top_recipes = self.recDB.select_top_recipes(top_ings, cooked_recipes=[], how_many=TOP_RECIPES_COUNT)
        if top_recipes:
            # Creating arr where the better recipe has bigger chance
            arr = [rec for rec in top_recipes for _ in range(len(top_recipes) - top_recipes.index(rec))]
            return random.choice(arr)
        else:
            return []

    def update_nutDB_by_recipe(self, recipe_id: str or int):
        self.recDB.load_db()
        self.ingDB.load_db()
        self.nutDB.load_db()
        used_ings = self.recDB.db[str(recipe_id)]["ings_ids"]
        for ing_id in used_ings:
            amount = used_ings[ing_id]
            ing_nuts = self.ingDB.db[str(ing_id)]["nuts"]
            for nut in ing_nuts:
                self.nutDB.db[nut]["current"] += ing_nuts[nut] * amount / 100
        self.nutDB.save_db()
