""" File that holds all code that creates the different types of traders in the game."""

from __future__ import annotations

from abc import abstractmethod, ABC

from avl import AVLTree
from material import Material
from random_gen import RandomGen

__author__ = 'Shyam Kamalesh Borkar and Jobin Mathew Dan'

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]

class Trader(ABC):
    """ Abstract class for traders"""
    
    def __init__(self, name: str) -> None:
        """
        Constructor for trader
        :param name: Name of the Trader
        :complexity: The best and worst case complexity is O(1).
        """

        self.name = name
        self.inventory = AVLTree() 
        self.active_deal = None
        self.trader_type = None
 
    @classmethod
    @abstractmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of Trader
        '''
        pass
    
    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Setting all the materials into the trader's inventory
        
        :param mats: The list of materials that the trader would sell
        :complexity: The best and worst case complexity is O(N * log(n))
        where N is the number of materials and n is the size of the inventory
        """

        self.inventory = AVLTree()
        for material in mats:
            self.add_material(material)
    
    def add_material(self, mat: Material) -> None:
        """
        Adding the material into the trader's inventory
        
        :param mat: The material that is added to the trader's inventory
        :complexity: The best and worst case complexity is O(log(n)) where
        n is the number of items in the inventory (AVL tree).
        """

        self.inventory[mat.mining_rate] = mat
    
    def remove_material(self, mat: Material) -> None:
        """
        Removing the known material from the traders inventory
        
        :param mat: The material that is removed from the trader's inventory
        :complexity: The best and worst case complexity is O(log(n)) where
        n is the number of items in the inventory (AVL tree).
        """

        del self.inventory[mat.mining_rate]
    
    def is_currently_selling(self) -> bool:
        """
        Checks if the trader is currently selling a deal

        :return: Returns the state of the active deal
        :complexity: The best and worst case complexity is O(1).
        """

        if self.active_deal is None:
            return False
        else:
            return True

    def current_deal(self) -> tuple[Material, float]:
        """
        It would be showing the current deal of the material to the player
 
        :return: Returns the material and its price in a tuple format
        :raise ValueError: When there is no active deal
        :complexity: The best and worst case complexity is O(1).
        """

        if self.active_deal is None:
            raise ValueError()
        return self.active_deal

    @abstractmethod
    def generate_deal(self) -> None:
        """
        Generating the deal of the material
        """
        pass

    def generate_price(self) -> float:
        """
        Generating the price of the material
        :complexity: The best and worst case complexity is O(1).
        """

        return round(2 + 8 * RandomGen.random_float(), 2)

    def stop_deal(self) -> None:
        """
        The trader stops the current deal
        :complexity: The best and worst case complexity is O(1).
        """

        self.active_deal = None

    def __str__(self) -> str:
        """
        A string representation of the trader with the current deal
        :complexity: The best and worst case complexity is O(1).
        :return: Returns the traders' name and what they would be selling
        """

        if not self.is_currently_selling():
            result  = "<{}: {} not currently buying>".format(self.trader_type, self.name)
        else:
            material = self.active_deal[0]
            price = self.active_deal[1]
            result = "<{}: {} buying [{}: {}🍗/💎] for {}💰>".format(self.trader_type, self.name, material.name, material.mining_rate, price)
        
        return result

class RandomTrader(Trader):
    """ Class that represents a random trader in the game"""

    def __init__(self, name: str) -> None:
        """
        Constructor for random trader type
        :param name: Name of the Random Trader
        :complexity: The best and worst case complexity is O(1).
        """

        Trader.__init__(self, name)
        self.trader_type = "RandomTrader"
    

    def generate_deal(self) -> None:
        """
        Generating the deal of the material
        :complexity: The best and worst case complexity is O(n) where 
        n is the number of items in the trader's inventory.
        """

        material_list = self.inventory.range_between(0, len(self.inventory) - 1)
        material = RandomGen.random_choice(material_list)
        price = self.generate_price()
        self.active_deal = (material, price)
    
    @classmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of Random Trader
        :complexity: The best and worst case complexity is O(1).
        :return: the random trader object is returned
        '''

        random_name = RandomGen.random_choice(TRADER_NAMES)
        return RandomTrader(random_name)

class RangeTrader(Trader):
    """ Class that represents a range trader in the game"""

    def __init__(self, name: str) -> None:
        """
        Constructor for range trader type
        :param name: Name of the Range Trader
        :complexity: The best and worst case complexity is O(1).
        """

        Trader.__init__(self, name)
        self.trader_type = "RangeTrader"
   

    def generate_deal(self) -> None:
        """
        Generating the deal of the material
        :complexity: The best and worst case complexity is O(n) where 
        n is the number of items in the trader's inventory.
        """

        i = RandomGen.randint(1, len(self.inventory))
        j = RandomGen.randint(i, len(self.inventory))

        material_list = self.materials_between(i - 1, j - 1) # subtract 1 from i and j as index should start from 0
        material = RandomGen.random_choice(material_list)
        price = self.generate_price()
        self.active_deal = (material, price)

    def materials_between(self, i: int, j: int) -> list[Material]:
        """
        Gets the material between the materials in the traders inventory
        
        :param i: the index of the easiest to mine in the list of materials
        :param j: the index of the easiest to mine in the list of materials
        :complexity: The best and worst case complexity is O(N) where N 
        represents the number of items in the inventory.
        :return: Gets the list of materials between the index i and j
        """

        return self.inventory.range_between(i, j)
    
    @classmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of range Trader

        :complexity: The best and worst case complexity is O(1).
        :return: the range trader object is returned
        '''

        random_name = RandomGen.random_choice(TRADER_NAMES)
        return RangeTrader(random_name)

class HardTrader(Trader):
    """ Class that represents a hard trader in the game"""

    def __init__(self, name: str) -> None:
        """
        Constructor for hard trader type
        :param name: Name of the Hard Trader
        :complexity: The best and worst case complexity is O(1).
        """

        Trader.__init__(self, name)
        self.trader_type = "HardTrader"


    def generate_deal(self) -> None:
        """
        Generating the deal of the material

        :complexity: The best and worst case complexity is O(n) 
        where n is the size of the inventory.
        """

        material_list = self.inventory.range_between(0, len(self.inventory) - 1)
        material = material_list[-1]
        self.remove_material(material)
        price = self.generate_price()
        self.active_deal = (material, price)
    
    @classmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of Hard Trader

        :complexity: The best and worst case complexity is O(1).
        :return: the Hard trader object is returned
        '''

        random_name = RandomGen.random_choice(TRADER_NAMES)
        return HardTrader(random_name)

if __name__ == "__main__":
    trader = RangeTrader("Jackson")
    print(trader)
    trader.set_materials([
        Material("Coal", 4.5),
        Material("Diamonds", 3),
        Material("Redstone", 20),
    ])
    trader.generate_deal()
    print(trader)
    trader.stop_deal()
    print(trader)
