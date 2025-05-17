class CocktailAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("Cocktail already exists")


class CocktailNotFoundError(Exception):
    def __init__(self):
        super().__init__("Cocktail not found")
