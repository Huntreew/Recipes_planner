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
        low_nuts = self.nutDB.search_for_lows()  # finds most needed nuts
        print(time.time() - start)
        # Setup array with top ingredients containing needed nuts
        start = time.time()
        ings = self.ingDB.search_ings(low_nuts=low_nuts, max_in_arr=TOP_INGREDIENTS_COUNT)
        print(time.time() - start)
        start = time.time()
        top_recipes = self.recDB.select_top_recipes(ings, cooked_recipes=[], max_in_arr=TOP_RECIPES_COUNT)
        print(time.time() - start)
        if top_recipes:
            # Creating arr where the better recipe has bigger chance
            arr = [rec for rec in top_recipes for _ in range(len(top_recipes) - top_recipes.index(rec))]
            return random.choice(arr)
        else:
            return []

    def update_nutDB_by_recipe(self, recipe_id: str or int):
        self.recDB.load_df()
        self.ingDB.load_df()
        self.nutDB.load_df()
        used_ings = self.recDB.df.iloc[recipe_id]["ings_ids"]
        for ing_id in used_ings:
            amount = used_ings[ing_id]
            ing_nuts = self.ingDB.df[str(ing_id)]["nuts"]
            for nut in ing_nuts:
                self.nutDB.df[nut]["current"] += ing_nuts[nut] * amount / 100
        self.nutDB.save_df()
