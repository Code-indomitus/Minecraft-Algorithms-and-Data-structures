from __future__ import annotations
from random import random

from material import Material
from random_gen import RandomGen

# List of food names from https://github.com/vectorwing/FarmersDelight/tree/1.18.2/src/main/resources/assets/farmersdelight/textures/item
FOOD_NAMES = [
    "Apple Cider",
    "Apple Pie",
    "Apple Pie Slice",
    "Bacon",
    "Bacon And Eggs",
    "Bacon Sandwich",
    "Baked Cod Stew",
    "Barbecue Stick",
    "Beef Patty",
    "Beef Stew",
    "Cabbage",
    "Cabbage Leaf",
    "Cabbage Rolls",
    "Cabbage Seeds",
    "Cake Slice",
    "Chicken Cuts",
    "Chicken Sandwich",
    "Chicken Soup",
    "Chocolate Pie",
    "Chocolate Pie Slice",
    "Cod Slice",
    "Cooked Bacon",
    "Cooked Chicken Cuts",
    "Cooked Cod Slice",
    "Cooked Mutton Chops",
    "Cooked Rice",
    "Cooked Salmon Slice",
    "Dog Food",
    "Dumplings",
    "Egg Sandwich",
    "Fish Stew",
    "Fried Egg",
    "Fried Rice",
    "Fruit Salad",
    "Grilled Salmon",
    "Ham",
    "Hamburger",
    "Honey Cookie",
    "Honey Glazed Ham",
    "Honey Glazed Ham Block",
    "Horse Feed",
    "Hot Cocoa",
    "Melon Juice",
    "Melon Popsicle",
    "Milk Bottle",
    "Minced Beef",
    "Mixed Salad",
    "Mutton Chops",
    "Mutton Wrap",
    "Nether Salad",
    "Noodle Soup",
    "Onion",
    "Pasta With Meatballs",
    "Pasta With Mutton Chop",
    "Pie Crust",
    "Pumpkin Pie Slice",
    "Pumpkin Slice",
    "Pumpkin Soup",
    "Ratatouille",
    "Raw Pasta",
    "Rice",
    "Rice Panicle",
    "Roast Chicken",
    "Roast Chicken Block",
    "Roasted Mutton Chops",
    "Rotten Tomato",
    "Salmon Slice",
    "Shepherds Pie",
    "Shepherds Pie Block",
    "Smoked Ham",
    "Squid Ink Pasta",
    "Steak And Potatoes",
    "Stuffed Potato",
    "Stuffed Pumpkin",
    "Stuffed Pumpkin Block",
    "Sweet Berry Cheesecake",
    "Sweet Berry Cheesecake Slice",
    "Sweet Berry Cookie",
    "Tomato",
    "Tomato Sauce",
    "Tomato Seeds",
    "Vegetable Noodles",
    "Vegetable Soup",
]

class Food:
    
    def __init__(self, name: str, hunger_bars: int, price: int) -> None:
        '''
        Constructor for Food
        Attributes :
        1) name of food
        2) hunger bars food provides
        3) price of the food
        '''
        self.name = name 
        self.hunger_bars = hunger_bars 
        self.price = price
    
    def __str__(self) -> str:
        return self.name + " gives " + str(self.hunger_bars) + " hunger bars and costs " + str(self.price)

    @classmethod
    def random_food(cls) -> Food:
        '''
        Generate random instance of Food
        '''
        random_name = RandomGen.random_choice(FOOD_NAMES)
        random_hunger_bars = RandomGen.random_choice(50,500)
        random_price = RandomGen.randint(5,50)
        return Food(random_name,random_hunger_bars,random_price)

if __name__ == "__main__":
    print(Food.random_food())
