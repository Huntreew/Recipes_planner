import json


# ------------ PREPARATION OF INDIVIDUAL DATABASES ------------

class Database:
    """Database backbone containing some common functionality"""

    def __init__(self, filename):
        self.db = None
        self.filename = filename
        self.start_file(self.filename)

    @staticmethod
    def start_file(filename):
        try:
            with open(filename, "r"):
                print(filename + " EXISTS")
        except FileNotFoundError:
            with open(filename, "w"):
                print(filename + " CREATED")
        try:
            with open(filename, "r") as file:
                json.load(file)
        except Exception:
            with open(filename, "w") as file:
                json.dump({}, file)

    def clear_db(self):
        self.db = {}
        self.save_db()

    def load_db(self):
        with open(self.filename, "r") as file:
            self.db = json.load(file)

    def save_db(self):
        with open(self.filename, "w") as file:
            json.dump(self.db, file)

    def add(self, new_item: dict):
        """
        Adds new item to database
        Dictionary format -> ID is the KEY holding recipe dictionary
        :param new_item:
        """
        self.load_db()
        new_item["name"] = new_item["name"].lower()
        if self.db:
            new_id = int(max(list(self.db.keys()))) + 1
        else:
            new_id = 0
        new_item["id"] = new_id
        self.db[new_id] = new_item
        self.save_db()

    def remove(self, item_id: str or int) -> bool:
        self.load_db()
        try:
            self.db.pop(str(item_id))
            self.save_db()
            return True
        except KeyError:
            pass
        return False


class RecipeDatabase(Database):
    """Database for recipes"""

    def __init__(self, filename):
        super().__init__(filename)

    def custom_rec(self):
        pass

    def select_top_recipes(self, ings: list, how_many: int = 5) -> list:
        """
        Takes list of ingredients IDs and search the best recipes based on amount used in recipe
        :param ings:
        :param how_many:
        :return: top_recipes:
        """
        self.load_db()
        recipes = self.db
        top_recipes: list = []
        recipes_scores: dict = {}
        for recipe_id in recipes:
            for ing_id in ings:
                # Check if recipe already has a score
                try:
                    recipes_scores[recipe_id]
                except KeyError:
                    recipes_scores[recipe_id] = 0
                try:
                    ings_ids = recipes[recipe_id]["ings_ids"]
                    recipes_scores[recipe_id] += ings_ids[str(ing_id)]     # ads AMOUNT of the ingredient
                except KeyError:
                    pass
        print("\nRecipes Scores: ", recipes_scores)
        if how_many > len(recipes_scores):
            how_many = len(recipes_scores)
        # This block shall be remade
        for i in range(how_many):  # determines how many ids will be returned
            best: dict = {"id": 0, "score": -1}
            for recipe_id in recipes_scores:
                if recipes_scores[recipe_id] > best["score"]:
                    best["id"] = recipe_id
                    best["score"] = recipes_scores[recipe_id]
            top_recipes.append(best["id"])
            recipes_scores.pop(best["id"])
        print("\nTOP RECIPES: ", top_recipes)
        return top_recipes


class IngredientDatabase(Database):
    """Database for ingredients"""

    def __init__(self, filename):
        super().__init__(filename)

    def custom_ing(self):
        pass

    def search_ings(self, nut_name: str, max_in_arr: int = 10) -> list:
        """Returns arrays with top ingredients for given nutrient
        Array contains ingredients IDs"""

        self.load_db()
        best_ings = []
        for ing_id in self.db:
            ing_nuts = self.db[ing_id]["nuts"]
            try:
                if ing_nuts[nut_name] > 0:                         # check if there is needed nutrient
                    best_ings.append(self.db[ing_id])              # appending whole ingredient dictionary
            except KeyError:
                pass
        # Sorting best ingredients
        sorted_ings = self.sort_ings_by_nut(ing_arr=best_ings, nut_name=nut_name)
        if max_in_arr <= len(sorted_ings):
            sorted_ings = sorted_ings[0:max_in_arr]                 # shortens array to maximal item count
        return sorted_ings

    @staticmethod
    def sort_ings_by_nut(ing_arr: list, nut_name: str) -> list:
        """Returns sorted list with only IDs of ingredients"""

        ings_sorted = []
        values_sorted = reversed(sorted([ing["nuts"][nut_name] for ing in ing_arr]))    # just sorting numbers in array
        # Sorting ingredients via sorted values
        for val in values_sorted:
            for ing in ing_arr:
                if ing["nuts"][nut_name] == val:
                    ings_sorted.append(ing["id"])
                    ing_arr.remove(ing)
                    break
        return ings_sorted

    @staticmethod
    def select_top_ings(ings_total: list, how_many: int = 5) -> list:
        """
        Takes array with arrays containing ingredient ids
        :param ings_total:
        :param how_many:
        :return: top_ings:
        """
        top_ings: list = []
        ings_scores: dict = {}
        # Computing score for every ingredient id
        for ing_arr in ings_total:
            for ing_id in ing_arr:
                try:
                    ings_scores[ing_id]
                except KeyError:
                    ings_scores[ing_id] = 0
                ings_scores[ing_id] += len(ing_arr) - ing_arr.index(ing_id)

        print("\nIngredient Scores: ", ings_scores)
        # Sorting out top ingredient IDs
        if how_many > len(ings_scores):
            how_many = len(ings_scores)
        for i in range(how_many):           # determines how many ids will be returned
            best: int = list(ings_scores.keys())[0]
            for ing_id in ings_scores:
                if ings_scores[ing_id] > ings_scores[best]:
                    best = ing_id
            top_ings.append(best)
            ings_scores.pop(best)
        return top_ings


class NutriReportDatabase:

    def __init__(self, filename):
        self.db = None
        self.filename = filename
        self.start_file(self.filename)

    @staticmethod
    def start_file(filename):
        try:
            with open(filename, "r"):
                print(filename + " EXISTS")
        except FileNotFoundError:
            with open(filename, "w"):
                print(filename + " CREATED")
        try:
            with open(filename, "r") as file:
                json.load(file)
        except Exception:
            with open(filename, "w") as file:
                json.dump({}, file)

    def clear_db(self):
        self.db = None
        self.save_db()

    def load_db(self):
        with open(self.filename, "r") as file:
            self.db = json.load(file)

    def save_db(self):
        with open(self.filename, "w") as file:
            json.dump(self.db, file)

    def add_from_csv(self, file):
        pass

    def add(self, new_nutrient: dict):
        """
        Adds new nutrient for tracking in database
        Dictionary format -> name: {name: , current: , perday: }
        :param new_nutrient:
        :return: None
        """
        self.load_db()
        new_nutrient["name"] = new_nutrient["name"].lower()
        try:
            var = self.db[new_nutrient["name"]]
            print("\nNutrient NAME already TAKEN\n")
        except KeyError:
            self.db[new_nutrient["name"]] = new_nutrient
            self.save_db()

    def search_for_lows(self) -> list:
        self.load_db()
        deficit_arr = []
        for nut_name in self.db:
            deficit = self.db[nut_name]["current"] / self.db[nut_name]["perday"]
            deficit_arr.append({"name": self.db[nut_name]["name"], "deficit": deficit})
        return deficit_arr

    @staticmethod
    def sort_lows(low_nuts_raw) -> list:
        """
        :param low_nuts_raw:
        :return low_nuts_sorted: in format [{name: , deficit: }]
        """
        low_nuts_sorted = []
        deficits_sorted = sorted([val["deficit"] for val in low_nuts_raw])
        for val in deficits_sorted:
            for nut in low_nuts_raw:
                if nut["deficit"] == val:
                    low_nuts_sorted.append(nut)
        return low_nuts_sorted

    def sub_daily_supply(self):
        """Subs daily supply from current"""
        self.load_db()
        for nut_name in self.db:
            self.db[nut_name]["current"] -= self.db[nut_name]["perday"]
        self.save_db()

