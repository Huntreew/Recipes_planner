import pandas as pd


# ------------ PREPARATION OF INDIVIDUAL DATABASES ------------

class Database:
    """Database backbone containing some common functionality"""

    def __init__(self, filename):
        self.df = pd.DataFrame()
        self.filename = filename
        self.start_file(filename)

    @staticmethod
    def start_file(filename):
        try:
            with open(filename, "r"):
                print(filename + " EXISTS")
        except FileNotFoundError:
            with open(filename, "w"):
                print(filename + " CREATED")
        try:
            with open(filename, "r"):
                pd.read_json(filename)
        except Exception:
            with open(filename, "w") as file:
                file.write("{}")

    def clear_db(self):
        self.df = ""
        self.save_df()

    def load_df(self):
        with open(self.filename, "r") as file:
            self.df = pd.read_json(file)

    def save_df(self):
        with open(self.filename, "w") as file:
            file.write(self.df.to_json())

    def add(self, new_item: dict):
        """
        Adds new item to DataFrame
        :param new_item:
        """
        self.load_df()
        new_item["name"] = new_item["name"].lower()
        if not self.df.empty:
            new_id = self.df.tail(1).index.item() + 1
        else:
            new_id = 0
        new_item["id"] = int(new_id)
        self.df = pd.concat([self.df, pd.DataFrame([new_item])], ignore_index=True)
        self.save_df()


class RecipeDatabase(Database):
    """Database for recipes"""

    def __init__(self, filename):
        super().__init__(filename)

    def custom_rec(self):
        pass

    def select_top_recipes(self, ings: list, cooked_recipes: list, max_in_arr: int = 5) -> list:
        """
        Takes list of ingredients IDs and search the best recipes based on amount used in recipe
        :param ings:
        :param how_many:
        :return: top_recipes:
        """
        self.load_df()
        rec_scores = pd.DataFrame(list(self.df["ings_ids"]), index=list(self.df["id"]),
                                  columns=[str(x) for x in list(ings)])
        rec_scores = rec_scores.sum(axis=1)
        rec_scores = rec_scores.sort_values(ascending=False).iloc[0:max_in_arr]
        return list(rec_scores.index)


class IngredientDatabase(Database):
    """Database for ingredients"""

    def __init__(self, filename):
        super().__init__(filename)

    def custom_ing(self):
        pass

    def search_ings(self, low_nuts: pd.Series, max_in_arr: int = 10) -> list:
        """Returns arrays with top ingredients for given nutrient
        Array contains ingredients IDs"""

        self.load_df()
        pre_scores_df = pd.DataFrame(list(self.df["nuts"]),
                                     index=list(self.df["id"]),
                                     columns=[str(x) for x in list(low_nuts.index)])
        pre_scores_df = pre_scores_df.mul(low_nuts)
        scores = pre_scores_df.sum(axis=1)
        scores = scores.sort_values(ascending=False).iloc[0:max_in_arr]
        return list(scores.index)


class NutriReportDatabase(Database):

    def __init__(self, filename):
        super().__init__(filename)

    def search_for_lows(self, nuts_count: int = 20) -> pd.Series:
        self.load_df()
        deficit = list(self.df["current"] / self.df["perday"])
        s = pd.Series([abs(d) if d < 0 else 0.1 for d in deficit], [str(x) for x in list(self.df["id"])])
        return s.sort_values(ascending=False).iloc[0:nuts_count]

    def sub_daily_supply(self):
        """Subs daily supply from current"""
        self.load_df()
        self.df["current"] -= self.df["perday"]
        self.save_df()

