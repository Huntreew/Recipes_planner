from databases import RecipeDatabase, IngredientDatabase, NutriReportDatabase
import random
import datetime
import time
import pandas as pd

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
        # Searching for top recipes
        top_recipes = self.recDB.select_top_recipes(ings, cooked_recipes=[], max_in_arr=TOP_RECIPES_COUNT)
        print(time.time() - start)
        if top_recipes:
            # Creating arr where the better recipe has bigger chance
            arr = [rec for rec in top_recipes for _ in range(len(top_recipes) - top_recipes.index(rec))]
            return random.choice(arr)
        else:
            return []

    def update_nutDB_by_recipe(self, recipe_id: str or int) -> None:
        self.recDB.load_df()
        self.ingDB.load_df()
        self.nutDB.load_df()

        # Series with ing ID and its amount in grams
        amount = pd.Series(self.recDB.df["ings_ids"][int(recipe_id)])

        # Selecting only ings used in recipe
        rows = [int(r) for r in list(amount.index)]
        data = list(self.ingDB.df["nuts"][rows])

        # Ings IDs as index, Nuts IDs as columns names
        # Charts how many of nuts does every ingredient have per 100g
        used_ings = pd.DataFrame(data, index=[str(i) for i in list(amount.index)])

        # Multiplying every ing row by its amount
        used_ings = used_ings.mul(amount, axis=0)

        # Dividing all by 100 to get values in grams
        used_ings = used_ings.div(100)

        # Summing all rows to get how many of individual nuts did we get in grams
        used_s = pd.Series(list(used_ings.sum(axis=0)), index=[int(c) for c in list(used_ings.columns)])

        # Adding earned nuts to the column
        self.nutDB.df["current"] = self.nutDB.df["current"].add(used_s, fill_value=0)
        self.nutDB.save_df()
